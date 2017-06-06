/* REXX */

/*
 * Creates or deletes a WPS object on behalf of an RPM package.
 *
 * Usage: wps-object /create PACKAGE OBJECTID SPECIFICATION
 *        wps-object /create PACKAGE OBJECTID:SPECIFICATION
 *        wps-object /create PACKAGE < FILE
 *        wps-object /delete PACKAGE OBJECTID
 *        wps-object /recreateall PACKAGE
 *        wps-object /deleteall PACKAGE
 *
 * PACKAGE is a name of the RPM package. OBJECTID is an object identifier
 * (w/o angle brackets). SPECIFICATION is a string that describes the
 * properties of the object to create and has the following format (note
 * that the whole specification string must be taken in double quotes on
 * the CMD.EXE's command line if it contains spaces or special characters such
 * as angle bracets):
 *
 *   CLASSNAME|TITLE|LOCATION[|SETUP[|OPTION]]
 *
 * Each component of this format string directly corresponds to the
 * respective argument of the SysCreateObject REXX function. Refer to
 * to the REXX reference manual for details. Note that when OPTION is not
 * specified, U (update) mode is used by default.
 *
 * FILE is a text file used to create multiple objects at once: each line
 * in this file is an object ID followed by the specification (as described
 * above), like this:
 *
 *   OBJECTID:SPECIFICATION
 *
 * This indirect FILE form is preferred and even required if one of the
 * object parameters contains a double forward slash (e.g. 'http://foo')
 * because otherwise the Classic REXX interpreter will treat it as a start of
 * the comment block and fail.
 *
 * Note that /create and /delete commands maintain a global reference
 * counter for each object (shared by all packages): /create increases
 * this counter by 1, /delete decreases it by 1. The object is actually
 * deleted only when its counter becomes zero.
 *
 * /deleteall deletes all objects created for a given package at once (in
 * the order opposite to creation). /recreateall recreataes all object
 * created for a given package which is useful if the package objects were
 * accidentially deleted (w/o removing the package itself).
 *
 * Some object parameters (the LOCATION string or parts of the SETUP string such
 * as EXENAME) require valid OS/2 path strings as values, with back slashes
 * instead of forward slashes and @unixroot expanded to a full path. You may
 * cause this expansion by enclosing the respective part of the string in double
 * parenthesis. Note that double parenthesis may not be nested.
 *
 * Author: Dmitry A. Kuminov
 *
 * Version: 1.1 - 2017-02-09
 * - Fix object deletion (wrong hash map indexing).
 *
 * Version: 1.0 - 2010-11-08
 * - Inital release.
 */

trace off
numeric digits 12
'@echo off'

/*------------------------------------------------------------------------------
 globals
------------------------------------------------------------------------------*/

/* all globals to be exposed in procedures */
Globals = 'G. Opt. Static.'

G.ObjectRefs = ''
G.ObjectRefs.!modified = 0

G.PackageObjects.0 = 0
G.PackageObjects.!modified = 0
G.PackageObjects.!removed = 0

G.UndoCreateID = ''

G.InvalidObjectIDChars = '<>,;:|'

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
 * Just do the job.
 *
 * @param aArgs Comand line arguments.
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
        otherwise do
            say 'ERROR: Invalid command "'G.Args.1'".'
            return 1
        end
    end

    if (G.Args.0 < 2) then do
        say 'ERROR: Missing package name.'
        return 1
    end
    pkg = G.Args.2

    readStdIn = 0

    if (cmd == 'C' & G.Args.0 < 3) then do
        readStdIn = 1
    end
    else if (cmd == 'C' | cmd == 'D') then do
        if (G.Args.0 < 3) then do
            say 'ERROR: Missing object ID.'
            return 1
        end
        id = G.Args.3

        if (cmd == 'C') then do
            spec = ''
            /* if this is a combined form, split it */
            if (pos(':', id) > 0) then parse var id id':'spec
            else if (G.Args.0 >= 4) then spec = G.Args.4
            if (spec == '') then do
                say 'ERROR: Missing object specification.'
                return 1
            end
        end

        if (verify(id, G.InvalidObjectIDChars, 'M') > 0) then do
            say 'ERROR: Object ID "'id'" contains invalid characters.'
            return 1
        end
    end

    ux = value('UNIXROOT',,'OS2ENVIRONMENT')
    if (ux == '') then do
        say 'ERROR: UNIXROOT environment variable is not set.'
        return 1
    end

    G.ObjectRefsFile = FixDir(ux'/var/cache/rpm/wps/objects')
    G.PackageDir = FixDir(ux'/var/cache/rpm/wps/packages')

    /* Read object refs */
    if (FileExists(G.ObjectRefsFile)) then do
        G.ObjectRefs = charin(G.ObjectRefsFile, 1, chars(G.ObjectRefsFile))
        if (\FileOk(G.ObjectRefsFile)) then do
            rc = FileErrorCode(G.ObjectRefsFile)
            say 'ERROR: Could not read "'G.ObjectRefsFile'" (rc='rc').'
            return rc
        end
        call charout G.ObjectRefsFile
    end

    /* Read package object list */
    pkgFile = G.PackageDir'\'pkg
    if (FileExists(pkgFile)) then do
        i = 0
        do while lines(pkgFile)
            i = i + 1
            str = linein(pkgFile)
            if (\FileOk(pkgFile)) then do
                rc = FileErrorCode(pkgFile)
                say 'ERROR: Could not read "'pkgFile'" (rc='rc').'
                return rc
            end
            parse var str s1':'s2 /* id:spec */
            if (s1 == '' | verify(s1, G.InvalidObjectIDChars, 'M') > 0 |,
                s2 == '') then do
                rc = -1
                say 'ERROR: Line #'i 'in file "'pkgFile'" is invalid.'
                return rc
            end
            G.PackageObjects.i = str
            G.PackageObjects.i.!id = s1
            G.PackageObjects.!map.s1 = i
        end
        G.PackageObjects.0 = i
        call lineout pkgFile
    end

    if (cmd == 'C') then do
        if (readStdIn) then do
            rc = 0
            do while lines()
                str = linein()
                if (strip(str) == '') then iterate
                parse var str id':'spec
                rc = CreateObject(id, spec)
                if (rc \= 0) then leave
            end
        end
        else do
            rc = CreateObject(id, spec)
        end
    end
    else if (cmd == 'D') then do
        rc = DeleteObject(id)
    end
    else if (cmd == 'RA') then do
        rc = 0
        do i = 1 to G.PackageObjects.0
            parse var G.PackageObjects.i id':'spec
            rc = CreateObject(id, spec)
            if (rc \= 0) then leave
        end
    end
    else if (cmd == 'DA') then do
        rc = 0
        do i = G.PackageObjects.0 to 1 by -1
            rc = DeleteObject(G.PackageObjects.i.!id)
            if (rc \= 0) then leave
        end
    end

    /* save object refs */
    if (G.ObjectRefs.!modified) then do
        rc = EnsureFileDir(G.ObjectRefsFile)
        if (rc = 0) then do
            refsFileTmp = SysTempFileName(G.ObjectRefsFile'.?????.tmp')
            rc = charout(refsFileTmp, G.ObjectRefs)
            if (rc \= 0 | \FileOk(refsFileTmp)) then do
                rc = FileErrorCode(refsFileTmp)
                say 'ERROR: Could not write to "'refsFileTmp'" (rc='rc').'
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
            if (rc \= 0) then do
                say 'ERROR: Could not delete "'pkgFile'".'
            end
        end
        else do
            rc = EnsureFileDir(pkgFile)
            if (rc = 0) then do
                pkgFileTmp = SysTempFileName(pkgFile'.?????.tmp')
                do i = 1 to G.PackageObjects.0
                    if (G.PackageObjects.i == '') then iterate /* skip removed */
                    rc = lineout(pkgFileTmp, G.PackageObjects.i)
                    if (rc \= 0 | \FileOk(pkgFileTmp)) then do
                        rc = FileErrorCode(pkgFileTmp)
                        say 'ERROR: Could not write to "'pkgFileTmp'" (rc='rc').'
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

    if (rc \= 0 & G.UndoCreateID \== '') then do
        call SysDestroyObject '<'G.UndoCreateID'>'
    end

    return rc

/**
 * Creates a WPS object.
 *
 * @param aID   Object ID.
 * @param aSpec Object specification string.
 * @return      0 on success, error code on failure.
 */
CreateObject: procedure expose (Globals)

    parse arg aID, aSpec

    aSpec = ExpandUnixRoot(aSpec)

    parse var aSpec class'|'title'|'location'|'setup'|'option
    if (class == '' | title == '' | location == '') then do
        say 'ERROR: Specification "'aSpec'" is invalid.'
        return 1
    end
    if (pos('OBJECTID=', setup) > 0) then do
        say 'ERROR: Specification string must not contain OBJECTID.'
        return 1
    end

    if (setup \== '') then setup = setup';'
    setup = setup'OBJECTID=<'aID'>'

    if (option == '') then option = 'U' /* Update by default */

    rc = SysCreateObject(class, title, location, setup, option)
    if (rc \== 1) then do
        say 'ERROR: Could not create an object with ID <'aID'> and',
            'specification "'aSpec'".'
        return 1
    end

    ok = 1

    /* check if there is an object with this id for this package */
    if (symbol('G.PackageObjects.!map.aID') == 'VAR') then do
        /* update it */
        i = G.PackageObjects.!map.aID
        G.PackageObjects.i = aID':'aSpec
        G.PackageObjects.!modified = 1
    end
    else do
        /* add a new */
        i = G.PackageObjects.0 + 1
        G.PackageObjects.i = aID':'aSpec
        G.PackageObjects.i.!id = aID
        G.PackageObjects.!map.aID = i
        G.PackageObjects.0 = i
        G.PackageObjects.!modified = 1

        /* increase the refcount */
        i = pos('<'aID'>', G.ObjectRefs)
        if (i == 0) then do
            G.ObjectRefs = G.ObjectRefs'<'aID'>1'
            G.ObjectRefs.!modified = 1
            /* mark as a candidate for undoing creation on failure */
            G.UndoCreateID = aID
        end
        else do
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
            say 'ERROR: Object reference file "'G.ObjectRefsFile'" is invalid',
                'near object ID <'aID'>.'
            G.PackageObjects.!modified = 0
        end
    end

    return (ok == 0)

/**
 * Deletes a WPS object.
 *
 * @param aID   Object ID.
 * @return      0 on success, error code on failure.
 */
DeleteObject: procedure expose (Globals)

    parse arg aID

    /* check if there is an object with this id for this package */
    if (symbol('G.PackageObjects.!map.aID') \== 'VAR') then do
        /* nothing to do */
        return 0
    end

    /* mark as removed */
    i = G.PackageObjects.!map.aID
    G.PackageObjects.i = ''
    G.PackageObjects.!removed = G.PackageObjects.!removed + 1
    G.PackageObjects.!modified = 1

    ok = 1

    /* decrease the refcount */
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
                else do
                    call SysDestroyObject '<'aID'>'
                end
                G.ObjectRefs.!modified = 1
                ok = 1
            end
        end
    end
    if (\ok) then do
        say 'ERROR: Object reference file "'G.ObjectRefsFile'" is invalid',
            'near object ID <'aID'>.'
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
        str = Replace(str, '/@unixroot', value('UNIXROOT',,'OS2ENVIRONMENT'))
        str = translate(str, '\', '/')
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

    dir = FixDir(filespec('D', aFile)||filespec('P', aFile))
    rc = MakeDir(dir)
    if (rc \= 0) then do
        say 'ERROR: Could not make directory "'dir'" (rc='rc').'
        return rc
    end

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

    dirFrom = FixDir(filespec('D', aFileFrom)||filespec('P', aFileFrom))
    dirTo = FixDir(filespec('D', aFileTo)||filespec('P', aFileTo))
    if (translate(dirFrom) \== translate(dirTo)) then do
        say 'ERROR: "'aFileFrom'" and "'aFileTo'" must reside in the same',
            'directory.'
        return -1
    end

    if (FileExists(aFileTo)) then do
        rc = SysFileDelete(aFileTo)
        if (rc \= 0) then do
            say 'ERROR: Could not delete "'aFileTo'" (rc='rc').'
            return rc
        end
    end

    address 'cmd' 'rename 'aFileFrom filespec('N', aFileTo)
    if (rc \= 0) then do
        say 'ERROR: Could not rename "'aFileFrom'" to "'aFileTo'" (rc='rc').'
        return rc
    end

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
 *  Fixes the directory path by a) converting all slashes to back
 *  slashes and b) ensuring that the trailing slash is present if
 *  the directory is the root directory, and absent otherwise.
 *
 *  @param dir      the directory path
 *  @param noslash
 *      optional argument. If 1, the path returned will not have a
 *      trailing slash anyway. Useful for concatenating it with a
 *      file name.
 */
FixDir: procedure expose (Globals)
    parse arg dir, noslash
    noslash = (noslash = 1)
    dir = translate(dir, '\', '/')
    if (right(dir, 1) == '\' &,
        (noslash | \(length(dir) == 3 & (substr(dir, 2, 1) == ':')))) then
        dir = substr(dir, 1, length(dir) - 1)
    return dir

/**
 *  Returns 1 if the specified file exists and 0 otherwise.
 */
FileExists: procedure expose (Globals)
    parse arg file
    return (GetAbsFilePath(file) \= '')

/**
 *  Returns 1 if the specified file status is other than READY or NOTREADY.
 */
FileOk: procedure expose (Globals)
    parse arg aFile
    status = stream(file, 'S')
    return (status \= 'READY' & status \= 'NOTREADY')

/**
 * Returns the error code of the specified file or -1 if the error code is
 * not available. Should only be called if FileOk() returns false.
 */
FileErrorCode: procedure expose (Globals)
    parse arg file
    parse value stream(file, 'D') with .':'rc
    if (datatype(rc) \= 'W') then rc = -1
    return rc

/**
 *  Returns the absolute path to the given file (including the filename)
 *  or an empty string if no file exists.
 */
GetAbsFilePath: procedure expose (Globals)
    parse arg file
    if (file \= '') then do
        file = stream(FixDir(file), 'C', 'QUERY EXISTS')
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

