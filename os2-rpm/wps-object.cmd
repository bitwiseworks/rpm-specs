/* REXX */

/*
 * Creates or deletes a WPS object on behalf of an RPM package.
 *
 * Usage: wps-object /create PACKAGE[:EVR] OBJECTID SPECIFICATION
 *        wps-object /create PACKAGE[:EVR] OBJECTID:SPECIFICATION
 *        wps-object /create PACKAGE[:EVR] < FILE
 *        wps-object /delete PACKAGE[:EVR] OBJECTID
 *        wps-object /delete PACKAGE[:EVR] < FILE
 *        wps-object /recreateall PACKAGE[:EVR]
 *        wps-object /deleteall PACKAGE[:EVR]
 *
 * PACKAGE is a name of the RPM package. EVR is an [epoch:]version[-release] or
 * [epoch@]version[-release] of the package. A missing EVR indicates a legacy
 * package without EVR information (new-style RPM packages always supply EVR).
 * See also the COMPATIBILITY NOTE below.
 *
 * OBJECTID is an object identifier (w/o angle brackets). SPECIFICATION is a
 * string that describes the properties of the object to create and has the
 * following format (note that the whole specification string must be taken in
 * double quotes on the CMD.EXE's command line if it contains spaces or special
 * characters such as angle brackets):
 *
 *   CLASSNAME|TITLE|LOCATION[|SETUP[|OPTION]]
 *
 * Each component of this format string directly corresponds to the respective
 * argument of the SysCreateObject REXX function. Refer to to the REXX reference
 * manual for details. Note that when OPTION is not specified, U (update) mode
 * is used by default.
 *
 * FILE is a text file used to create multiple objects at once: each line in
 * this file is an object ID followed by the specification (as described above),
 * like this:
 *
 *   OBJECTID:SPECIFICATION
 *
 * This indirect FILE form is preferred and even required if one of the object
 * parameters contains a double forward slash (e.g. 'http://foo') because
 * otherwise the Classic REXX interpreter will treat it as a start of the
 * comment block and fail.
 *
 * /create and /delete commands maintain a global reference counter for each
 * object (shared by all packages): /create increases this counter by 1, /delete
 * decreases it by 1. The object is actually deleted only when its counter
 * becomes zero. Note that if there are repeated /create object calls for a
 * package with the same EVR, the object reference counter is increased only
 * once, and it will be decreased only after the matching number of /delete
 * calls for the same EVR. This allows objects to survive reinstalling the same
 * version of a package.
 *
 * Note that /delete < FILE performs object deletion in reverse order (the last
 * line is processed first) to account for ordered creation in /create < FILE
 * commands.
 *
 * /deleteall deletes all objects created for a given package and EVR at once
 * (in the order opposite to creation). If an object has repeated EVR entries
 * for the package, only the first entry is deleted.
 *
 * /recreateall recreates all objects created for a given package and EVR which
 * is useful if the package objects were accidentally deleted without removing
 * the package itself. If an object has repeated EVR entries for the package,
 * only the last entry is recreated. Note that /recreateall never changes global
 * object reference counters.
 *
 * Some object parameters (the LOCATION string or parts of the SETUP string such
 * as EXENAME) require valid OS/2 path strings as values, with back slashes
 * instead of forward slashes and @unixroot expanded to a full path. You may
 * cause this expansion by enclosing the respective part of the string in double
 * parenthesis. Note that double parenthesis may not be nested.
 *
 * COMPATIBILITY NOTE. Packages without EVR are still supported, but /deleteall
 * should not be used for them in upgrade or downgrade scenarios. If the object
 * set of a version being installed differs from the object set of a version
 * being removed, wps-object doesn't know which object entry belongs to which
 * version, and /deleteall may delete all objects added by the installed
 * version but missing in the removed version. In such cases, either save the
 * removed version's object set first and call /delete for all of them manually
 * after all /create calls for the installed package, or call /deleteall
 * *before* making any such /create calls.
 *
 * Author: Dmitrii Kuminov <coding@dmik.org>
 *
 * Version: Next
 * - Fix file I/O error handling and brush up error messages.
 * - Skip WPS object creation if CONFIG.SYS UNIXROOT mismatches environment.
 * - Add logging to /var/log/wps-object.log.
 * - Migrate state from /var/cache/rpm/wps to /var/lib/rpm-wps.
 * - Support /delete < FILE command.
 * - Make /create < FILE and /delete < FILE process all entries on errors.
 * - Add package EVR support to properly handle upgrades and downgrades.
 *
 * Version: 1.1 - 2017-02-09
 * - Fix object deletion (wrong hash map indexing).
 *
 * Version: 1.0 - 2010-11-08
 * - Initial release.
 */

trace off
numeric digits 12
'@echo off'

/*------------------------------------------------------------------------------
globals
------------------------------------------------------------------------------*/

/* all globals to be exposed in procedures */
Globals = 'G. Opt. Static.'

G.LogFile = '/var/log/wps-object.log'
G.StateDir = '/var/lib/rpm-wps'

G.PackageName = ''

G.ObjectRefs = ''
G.ObjectRefs.!modified = 0

G.PackageObjects.0 = 0
G.PackageObjects.!modified = 0
G.PackageObjects.!removed = 0

G.UndoCreateID = ''

G.InvalidObjectIDChars = '<>,;:| '
G.ValidPkgEVRChars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._+~^-@'

G.UX = ''
G.SkipWPS = 0

/*------------------------------------------------------------------------------
startup + main + termination
------------------------------------------------------------------------------*/

/* init system REXX library */
if (RxFuncQuery('SysLoadFuncs')) then do
    call RxFuncAdd 'SysLoadFuncs', 'RexxUtil', 'SysLoadFuncs'
    call SysLoadFuncs
end

parse arg aArgs
call TokenizeString aArgs, 'G.Args'

return Main()

/*------------------------------------------------------------------------------
functions
------------------------------------------------------------------------------*/

/**
 * Writes a warning message to the console.
 *
 * @param aMsg  Warning message.
 * @return      0
 */
Warning: procedure expose (Globals)
    parse arg aStr
    say 'wps-object: WARNING: 'aStr
    return 0

/**
 * Writes an error message to the console.
 *
 * @param aMsg  Error message.
 * @return      1
 */
Error: procedure expose (Globals)
    parse arg aStr
    say 'wps-object: ERROR: 'aStr
    return 1

/**
 * Calls Error and exits with its return value.
 */
ErrorExit: procedure expose (Globals)
    parse arg aStr
    exit Error(aStr)

/**
 * Just do the job.
 *
 * @param aArgs Command line arguments.
 * @return      0 on success, error code on failure.
 */
Main: procedure expose (Globals)

    if (G.Args.0 == 0) then call Usage

    cmd = translate(G.Args.1)
    select
        when (cmd == '/CREATE') then cmd = 'C'
        when (cmd == '/DELETE') then cmd = 'D'
        when (cmd == '/RECREATEALL') then cmd = 'RA'
        when (cmd == '/DELETEALL') then cmd = 'DA'
        otherwise
            call ErrorExit 'Invalid command "'G.Args.1'"'
    end

    if (G.Args.0 < 2) then
        call ErrorExit 'Missing package name'

    pkg = G.Args.2

    readStdIn = 0

    if (cmd == 'C' | cmd == 'D') then do
        if (G.Args.0 < 3) then do
            readStdIn = 1
        end
        else do
            objID = G.Args.3
            if (cmd == 'C') then do
                objSpec = ''
                /* if this is a combined form, split it */
                if (pos(':', objID) > 0) then parse var objID objID':'objSpec
                else if (G.Args.0 >= 4) then objSpec = G.Args.4
                if (objSpec == '') then
                    call ErrorExit 'Missing object specification'
            end
            if (objID = '' | verify(objID, G.InvalidObjectIDChars, 'M') > 0) then
                call ErrorExit 'Object ID "'objID'": Invalid characters'
        end
    end

    configUx = ''
    configSys = SysBootDrive()'\CONFIG.SYS'
    if (FileExists(configSys)) then do
        do while lines(configSys)
            configLine = strip(translate(linein(configSys), ' ', '09'x))
            if (\FileOk(configSys)) then do
                rc = FileErrorCode(configSys)
                call lineout configSys
                call ErrorExit ''configSys': Read error 'rc
            end
            parse var configLine s1 s2
            if (translate(s1) \== 'SET') then iterate
            parse var s2 var '=' val
            if (strip(translate(var)) \== 'UNIXROOT') then iterate
            configUx = FixPath(strip(val), 1)
        end
        call lineout configSys
    end

    G.UX = value('UNIXROOT',,'OS2ENVIRONMENT')
    if (G.UX == '') then
        call ErrorExit 'UNIXROOT environment variable is not set or empty'

    G.UX = FixPath(strip(G.UX), 1)

    /* Don't create WPS objects if UNIXROOT in the environment and in CONFIG.SYS
     * disagree (e.g. to safely use --installroot with yum) */
    if (\G.SkipWPS) then do
        G.SkipWPS = (configUx == '' | translate(configUx) \== translate(G.UX))
        if (G.SkipWPS) then
            call Warning 'UNIXROOT in 'configSys' does not match environment'
    end
    if (G.SkipWPS) then
        call Warning 'Skipping WPS object creation'

    G.LogFile = G.UX || FixPath(G.LogFile)

    G.StateDir = FixPath(G.StateDir)
    G.ObjectRefsFile = G.UX || G.StateDir || '\objects'
    G.PackageDir = G.UX || G.StateDir || '\packages'

    /* Read object refs */
    if (FileExists(G.ObjectRefsFile)) then do
        G.ObjectRefs = charin(G.ObjectRefsFile, 1, chars(G.ObjectRefsFile))
        if (\FileOk(G.ObjectRefsFile)) then do
            rc = FileErrorCode(G.ObjectRefsFile)
            call ErrorExit ''G.ObjectRefsFile': Read error 'rc
        end
        call charout G.ObjectRefsFile
    end

    parse var pkg pkg':'pkgEvr
    pkgEvr = translate(pkgEvr, '@', ':')
    if (pkgEvr \== '' & verify(pkgEvr, G.ValidPkgEVRChars) > 0) then do
        call ErrorExit 'Invalid package EVR "'pkgEvr'"'
    end

    G.PackageName = pkg

    /* Read package object list */
    pkgFile = G.PackageDir'\'pkg
    if (FileExists(pkgFile)) then do
        i = 0
        do while lines(pkgFile)
            i = i + 1
            str = linein(pkgFile)
            if (\FileOk(pkgFile)) then do
                rc = FileErrorCode(pkgFile)
                call ErrorExit ''pkgFile': Read error 'rc
            end
            parse var str evr'>'id':'spec
            if (evr \== '' & verify(evr, G.ValidPkgEVRChars) > 0) then
                call ErrorExit ''pkgFile':'i': Invalid package EVR "'evr'"'
            if (id == '' | verify(id, G.InvalidObjectIDChars, 'M') > 0 |,
                spec == '') then
                call ErrorExit ''pkgFile':'i': Invalid Object ID "'id'" or SPEC'
            key = evr'>'id
            G.PackageObjects.i = spec
            G.PackageObjects.i.!evr = evr
            G.PackageObjects.i.!id = id
            /* Package reinstall will use the same EVR, account for it */
            if (symbol('G.PackageObjects.!map.key') == 'VAR') then
                G.PackageObjects.!map.key = G.PackageObjects.!map.key i
            else
                G.PackageObjects.!map.key = i
        end
        G.PackageObjects.0 = i
        call lineout pkgFile
    end

    errors = 0
    rc = 0

    if (cmd == 'C' | cmd == 'D') then do
        if (readStdIn) then do
            ids = ''
            do while lines()
                rc = 0
                str = linein()
                if (strip(str) == '') then iterate
                parse var str id':'spec
                if (id == '' | verify(id, G.InvalidObjectIDChars, 'M') > 0) then
                    rc = Error('Object ID "'id'": Invalid characters')
                else if (cmd == 'C') then
                    rc = CreateObject(pkgEvr, id, spec)
                else
                    ids = id' 'ids
                if (rc \= 0) then
                    errors = errors + 1
            end
            /* Delete the objects in reverse order */
            if (cmd == 'D') then do i = 1 to words(ids)
                rc = DeleteObject(pkgEvr, word(ids, i))
                if (rc \= 0) then
                    errors = errors + 1
            end
        end
        else do
            if (cmd == 'C') then
                rc = CreateObject(pkgEvr, objID, objSpec)
            else
                rc = DeleteObject(pkgEvr, objID)
            if (rc \= 0) then
                errors = errors + 1
        end
    end
    else if (cmd == 'RA') then do
        do i = 1 to G.PackageObjects.0
            if G.PackageObjects.i.!evr \== pkgEvr then iterate
            /* only recreate the last of multiple EVR entries */
            key = G.PackageObjects.i.!evr'>'G.PackageObjects.i.!id
            entries = G.PackageObjects.!map.key
            if (word(entries, words(entries)) \== i) then iterate
            rc = CreateObject(pkgEvr, G.PackageObjects.i.!id, G.PackageObjects.i, 1)
            if (rc \= 0) then
                errors = errors + 1
        end
    end
    else if (cmd == 'DA') then do
        do i = G.PackageObjects.0 to 1 by -1
            if G.PackageObjects.i.!evr \== pkgEvr then iterate
            /* only delete the first of multiple EVR entries */
            key = G.PackageObjects.i.!evr'>'G.PackageObjects.i.!id
            if (word(G.PackageObjects.!map.key, 1) \== i) then iterate
            rc = DeleteObject(pkgEvr, G.PackageObjects.i.!id)
            if (rc \= 0) then
                errors = errors + 1
        end
    end

    /* Note: save object/package states even on failures as the batch mode could
     * successfully create or delete some objects */

    /* save object refs */
    if (G.ObjectRefs.!modified) then do
        rc = EnsureFileDir(G.ObjectRefsFile)
        if (rc = 0) then do
            refsFileTmp = SysTempFileName(G.ObjectRefsFile'.?????.tmp')
            rc = charout(refsFileTmp, G.ObjectRefs)
            if (rc \= 0 | \FileOk(refsFileTmp)) then do
                rc = FileErrorCode(refsFileTmp)
                call Error ''refsFileTmp': Write error 'rc
            end
            else do
                call lineout refsFileTmp
                rc = SafeRename(refsFileTmp, G.ObjectRefsFile)
            end
        end
        if (rc \= 0) then do
            G.PackageObjects.!modified = 0
        end
    end

    /* save package object list */
    if (G.PackageObjects.!modified) then do
        if (G.PackageObjects.0 = G.PackageObjects.!removed) then do
            rc = SysFileDelete(pkgFile)
            if (rc \= 0) then
                call Error 'Failed to delete 'pkgFile': Error 'rc
        end
        else do
            rc = EnsureFileDir(pkgFile)
            if (rc = 0) then do
                pkgFileTmp = SysTempFileName(pkgFile'.?????.tmp')
                do i = 1 to G.PackageObjects.0
                    if (G.PackageObjects.i == '') then iterate /* skip removed */
                    key = G.PackageObjects.i.!evr'>'G.PackageObjects.i.!id
                    rc = lineout(pkgFileTmp, key':'G.PackageObjects.i)
                    if (rc \= 0 | \FileOk(pkgFileTmp)) then do
                        rc = FileErrorCode(pkgFileTmp)
                        call Error ''pkgFileTmp': Write error 'rc
                        leave
                    end
                end
                if (rc = 0) then do
                    call lineout pkgFileTmp
                    rc = SafeRename(pkgFileTmp, pkgFile)
                end
            end
        end
    end

    if (rc \= 0 & G.UndoCreateID \== '' & \G.SkipWPS) then do
        rc2 = SysDestroyObject('<'G.UndoCreateID'>')
        call Log 'DELETE 'pkg':'pkgEvr' 'G.UndoCreateID' = 'rc2
    end

    return (rc \= 0) | (errors \= 0)

/**
 * Writes a line to the log file.
 *
 * @param aLine Line to write.
 * @return      0 on success, 1 on failure.
 */
Log: procedure expose (Globals)
    parse arg aLine
    return lineout(G.LogFile, date()' 'time()' 'aLine)

/**
 * Creates a WPS object.
 *
 * @param aEVR      Package EVR.
 * @param aID       Object ID.
 * @param aSpec     Object specification string.
 * @param aNoRefs   1 to skip adjusting reference counters.
 * @return          0 on success, error code on failure.
 */
CreateObject: procedure expose (Globals)

    parse arg aEVR, aID, aSpec, aNoRefs

    aSpec = ExpandUnixRoot(aSpec)

    parse var aSpec class'|'title'|'location'|'setup'|'option
    if (class == '' | title == '' | location == '') then
        return Error('<'aID'>: Invalid specification "'aSpec'"')
    if (pos('OBJECTID=', setup) > 0) then
        return Error('<'aID'>: OBJECTID in setup string "'setup'"')

    if (setup \== '') then setup = setup';'
    setup = setup'OBJECTID=<'aID'>'

    if (option == '') then option = 'U' /* Update by default */

    objIndex = pos('<'aID'>', G.ObjectRefs)

    if (\G.SkipWPS) then do
        rc = SysCreateObject(class, title, location, setup, option)
        if (objIndex == 0) then mode = 'CREATE'
        else mode = 'UPDATE'
        call Log mode' 'G.PackageName':'aEVR' 'aID':'aSpec'|'option' = 'rc
        if (rc \== 1) then
            /* Assume the object is not there, return before referencing */
            return Error('Failed to create object <'aID'> with specification "'aSpec'"')
    end

    if (aNoRefs == 1) then
        return 0

    key = aEVR'>'aID
    ok = 1

    /* check if there is an object with this id for this package */
    if (symbol('G.PackageObjects.!map.key') == 'VAR') then do
        /* yes, e.g. same EVR during reinstall, add another entry */
        i = G.PackageObjects.0 + 1
        G.PackageObjects.i = aSpec
        G.PackageObjects.i.!evr = aEVR
        G.PackageObjects.i.!id = aID
        G.PackageObjects.!map.key = G.PackageObjects.!map.key i
        G.PackageObjects.0 = i
        G.PackageObjects.!modified = 1
    end
    else do
        /* add a new package reference */
        i = G.PackageObjects.0 + 1
        G.PackageObjects.i = aSpec
        G.PackageObjects.i.!evr = aEVR
        G.PackageObjects.i.!id = aID
        G.PackageObjects.!map.key = i
        G.PackageObjects.0 = i
        G.PackageObjects.!modified = 1

        /* increase the object refcount */
        i = objIndex
        if (i == 0) then do
            /* new object */
            G.ObjectRefs = G.ObjectRefs'<'aID'>1'
            G.ObjectRefs.!modified = 1
            /* mark as a candidate for undoing creation on failure */
            G.UndoCreateID = aID
        end
        else do
            /* existing object */
            ok = 0
            j = i + length(aId) + 2
            if (j <= length(G.ObjectRefs)) then do
                k = pos('<', G.ObjectRefs, j)
                if (k = 0) then k = length(G.ObjectRefs) + 1
                refcnt = substr(G.ObjectRefs, j, k - j)
                if (datatype(refcnt, 'W') & refcnt >= 0) then do
                    refcnt = refcnt + 1
                    G.ObjectRefs = delstr(G.ObjectRefs, i, k - i)
                    G.ObjectRefs = insert('<'aID'>'refcnt, G.ObjectRefs, i - 1)
                    G.ObjectRefs.!modified = 1
                    ok = 1
                end
            end
        end
        if (\ok) then do
            call Error ''G.ObjectRefsFile': Errors near object <'aID'>'
            G.PackageObjects.!modified = 0
        end
    end

    return (ok == 0)

/**
 * Deletes a WPS object.
 *
 * @param aEVR  Package EVR.
 * @param aID   Object ID.
 * @return      0 on success, error code on failure.
 */
DeleteObject: procedure expose (Globals)

    parse arg aEVR, aID

    key = aEVR'>'aID

    /* check if there is an object with this id for this package */
    if (symbol('G.PackageObjects.!map.key') \== 'VAR') then do
        /* nothing to do */
        return 0
    end

    /* check if there are multiple entries, e.g. same EVR during reinstall */
    multiple = words(G.PackageObjects.!map.key) > 1

    /* mark as removed */
    if (multiple) then do
        /* remove the first entry */
        i = word(G.PackageObjects.!map.key, 1)
        G.PackageObjects.!map.key = subword(G.PackageObjects.!map.key, 2)
    end
    else do
        i = G.PackageObjects.!map.key
        drop G.PackageObjects.!map.key
    end
    G.PackageObjects.i = ''
    G.PackageObjects.!removed = G.PackageObjects.!removed + 1
    G.PackageObjects.!modified = 1

    if (multiple) then
        return 0 /* object is still in use, nothing to do */

    ok = 1

    /* decrease the object refcount */
    i = pos('<'aID'>', G.ObjectRefs)
    if (i == 0) then do
        /* there must be an object with this ID... */
        ok = 0
    end
    else do
        ok = 0
        j = i + length(aId) + 2
        if (j <= length(G.ObjectRefs)) then do
            k = pos('<', G.ObjectRefs, j)
            if (k = 0) then k = length(G.ObjectRefs) + 1
            refcnt = substr(G.ObjectRefs, j, k - j)
            if (datatype(refcnt, 'W') & refcnt > 0) then do
                refcnt = refcnt - 1
                G.ObjectRefs = delstr(G.ObjectRefs, i, k - i)
                if (refcnt > 0) then do
                    G.ObjectRefs = insert('<'aID'>'refcnt, G.ObjectRefs, i - 1)
                end
                else if (\G.SkipWPS) then do
                    rc = SysDestroyObject('<'aID'>')
                    call Log 'DELETE 'G.PackageName':'aEVR' 'aID' = 'rc
                    if (rc \== 1) then
                        /* Assume the object is not there, go on to dereference */
                        call Warning 'Failed to delete object <'aID'>'
                end
                G.ObjectRefs.!modified = 1
                ok = 1
            end
        end
    end
    if (\ok) then do
        call Error G.ObjectRefsFile': Errors near object <'aID'>'
        G.PackageObjects.!modified = 0
    end

    return (ok == 0)

/**
 * Print usage information.
 */
Usage: procedure expose (Globals)

    say 'This script is intended to be run by RPM only.'
    exit 0

/**
 * Expands "/@unixroot" to the value of the UNIXROOT environment variable and
 * replaces all forward slashes with back slashes in parts of the given string
 * enclosed with double parenthesis. Parenthesis are removed after expansion.
 *
 * @param aString   String to expand double-parenthesed parts in.
 * @return          Setring with parts expanded.
 */
ExpandUnixRoot: procedure expose (Globals)

    parse arg aString

    i = 1
    do forever
        i = pos('((', aString, i)
        if (i <= 0) then leave
        j = pos('))', aString, i + 2)
        if (j <= 0) then leave
        str = substr(aString, i + 2, j - i - 2)
        str = FixPath(Replace(str, '/@unixroot', G.UX))
        aString = delstr(aString, i, j - i + 2)
        aString = insert(str, aString, i - 1)
        i = i + length(str)
    end

    return aString

/**
 * Creates a directory for the given file.
 *
 * @param aFile     File name.
 * @return          0 on success or an error code on failure.
 */
EnsureFileDir: procedure expose (Globals)

    parse arg aFile

    dir = FixPath(filespec('D', aFile)||filespec('P', aFile))
    rc = MakeDir(dir)
    if (rc \= 0) then
        return Error('Failed to create directory 'dir': Error 'rc)

    return 0

/**
 * Renames one file to another. Both files must reside in the same directory.
 * If the target file exists, it will be silently deleted before renaming the
 * source file (that must exist) to it.
 *
 * @param aFileFrom     Current file name.
 * @param aFileTo       New file name.
 * @return              0 on success or an error code on failure.
 */
SafeRename: procedure expose (Globals)

    parse arg aFileFrom, aFileTo

    dirFrom = FixPath(filespec('D', aFileFrom)||filespec('P', aFileFrom))
    dirTo = FixPath(filespec('D', aFileTo)||filespec('P', aFileTo))
    if (translate(dirFrom) \== translate(dirTo)) then
        return Error(''aFileFrom' and 'aFileTo' are in different directories')

    if (FileExists(aFileTo)) then do
        rc = SysFileDelete(aFileTo)
        if (rc \= 0) then
            return Error('Failed to delete 'aFileTo': Error 'rc)
    end

    address 'cmd' 'rename 'aFileFrom filespec('N', aFileTo)
    if (rc \= 0) then
        return Error('Failed to rename 'aFileFrom' to 'aFileTo': Error 'rc)

    return 0

MakeDir: procedure expose (Globals)
    parse arg aDir
    aDir = translate(aDir, '\', '/')
    curdir = directory()
    base = aDir
    todo.0 = 0
    do while 1
        d = directory(base)
        if (d \== '') then
            leave
        i = todo.0 + 1
        todo.i = filespec('N', base)
        todo.0 = i
        drv = filespec('D', base)
        path = filespec('P', base)
        if (path == '\' | path == '') then do
            base = drv||path
            leave
        end
        base = drv||strip(path, 'T', '\')
    end
    call directory curdir
    do i = todo.0 to 1 by -1
        if (i < todo.0 | (base \== '' & right(base,1) \== '\' &,
                                        right(base,1) \== ':')) then
            base = base'\'
        base = base||todo.i
        rc = SysMkDir(base)
        if (rc \= 0) then return rc
    end
    return 0

/**
 *  Fixes the file or directory path by a) converting all slashes to back
 *  slashes and b) ensuring that the trailing slash is present if
 *  the path is the root directory, and absent otherwise.
 *
 *  @param path     the file or directory path
 *  @param noslash
 *      optional argument. If 1, the path returned will not have a
 *      trailing slash anyway. Useful for concatenating it with a
 *      file name.
 */
FixPath: procedure expose (Globals)
    parse arg path, noslash
    noslash = (noslash = 1)
    path = translate(path, '\', '/')
    if (right(path, 1) == '\' &,
        (noslash | \(length(path) == 3 & (substr(path, 2, 1) == ':')))) then
        path = substr(path, 1, length(path) - 1)
    return path

/**
 *  Returns 1 if the specified file exists and 0 otherwise.
 */
FileExists: procedure expose (Globals)
    parse arg file
    return (GetAbsFilePath(file) \= '')

/**
 *  Returns 1 if the specified file status is READY or NOTREADY.
 */
FileOk: procedure expose (Globals)
    parse arg aFile
    status = stream(aFile, 'S')
    return (status = 'READY' | status = 'NOTREADY')

/**
 * Returns the error code of the specified file or -1 if the error code is
 * not available. Should only be called if FileOk() returns false.
 */
FileErrorCode: procedure expose (Globals)
    parse arg aFile
    parse value stream(aFile, 'D') with .':'rc
    if (\datatype(rc, 'W') | rc == 0) then rc = -1
    return rc

/**
 *  Returns the absolute path to the given file (including the filename)
 *  or an empty string if no file exists.
 */
GetAbsFilePath: procedure expose (Globals)
    parse arg file
    if (file \= '') then do
        file = stream(FixPath(file), 'C', 'QUERY EXISTS')
    end
    return file

/**
 *  Replaces all occurences of a given substring in a string with another
 *  substring.
 *
 *  @param  str the string where to replace
 *  @param  s1  the substring which to replace
 *  @param  s2  the substring to replace with
 *  @return     the processed string
 *
 *  @version 1.1
 */
Replace: procedure expose (Globals)
    parse arg str, s1, s2
    l1  = length(s1)
    l2  = length(s2)
    i   = 1
    do while (i > 0)
        i = pos(s1, str, i)
        if (i > 0) then do
            str = delstr(str, i, l1)
            str = insert(s2, str, i-1)
            i = i + l2
        end
    end
    return str

/**
 *  Returns a list of all words from the string as a stem.
 *  Delimiters are spaces, tabs and new line characters.
 *  Words containg spaces must be enclosed with double
 *  quotes. Double quote symbols that need to be a part
 *  of the word, must be doubled.
 *
 *  @param string   the string to tokenize
 *  @param stem
 *      the name of the stem. The stem must be global
 *      (i.e. its name must start with 'G.!'), for example,
 *      'G.!wordlist'.
 *  @param leave_ws
 *      1 means whitespace chars are considered as a part of words they follow.
 *      Leading whitespace (if any) is always a part of the first word (if any).
 *
 *  @version 1.1
 */
TokenizeString: procedure expose (Globals)

    parse arg string, stem, leave_ws
    leave_ws = (leave_ws == 1)

    delims  = '20090D0A'x
    quote   = '22'x /* " */

    num = 0
    token = ''

    len = length(string)
    last_state = '' /* D - in delim, Q - in quotes, W - in word */
    seen_QW = 0

    do i = 1 to len
        c = substr(string, i, 1)
        /* determine a new state */
        if (c == quote) then do
            if (last_state == 'Q') then do
                /* detect two double quotes in a row */
                if (substr(string, i + 1, 1) == quote) then i = i + 1
                else state = 'W'
            end
            else state = 'Q'
        end
        else if (verify(c, delims) == 0 & last_state \== 'Q') then do
            state = 'D'
        end
        else do
            if (last_state == 'Q') then state = 'Q'
            else state = 'W'
        end
        /* process state transitions */
        if ((last_state == 'Q' | state == 'Q') & state \== last_state) then c = ''
        else if (state == 'D' & \leave_ws) then c = ''
        if (last_state == 'D' & state \== 'D' & seen_QW) then do
            /* flush the token */
            num = num + 1
            call value stem'.'num, token
            token = ''
        end
        token = token||c
        last_state = state
        seen_QW = (seen_QW | state \== 'D')
    end

    /* flush the last token if any */
    if (token \== '' | seen_QW) then do
        num = num + 1
        call value stem'.'num, token
    end

    call value stem'.0', num

    return

