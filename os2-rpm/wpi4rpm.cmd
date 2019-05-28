/* WPI4RPM */

ScriptVer = '1.0.0.0'

/*  Synopsis:

    Add or remove fake WarpIN packages to the WarpIN database in order to make 
    sure RPM/YUM/ANPM installed packages keep dependent WPI packages happy.
   
    Author: Herwig Bauernfeind

    Version: 0.9.9.1 - 2018-08-20 (Silvan Scherrer)
    - adjust the app not found message in the DEL routine

    Version: 0.9.9.0 - 2018-08-19 (Herwig Bauernfeind)
    - Delete all WarpIN packages of a given vendor/app/package combination

    (c) 2017-2018 Herwig Bauernfeind for bww bitwise works GmbH.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

 */

call RxFuncAdd 'SysLoadFuncs', 'RexxUtil', 'SysLoadFuncs'
call SysLoadFuncs

signal on error name errorhandler
signal on syntax name errorhandler

verbose   = (value("VERBOSE",,"OS2ENVIRONMENT") <> "")

arguments = arg(1)
anr       = words(arguments)
if anr = 0 then arguments = 'HELP'
Mode      = strip(word(arguments,1))
if words(Mode) > 1 then do
    say "ERROR: wpi4rpm: Parameter parsing error. Aborting..."
    exit -1
end
Mode = translate(mode)

if Mode = "ADD" | Mode = "DEL" | Mode = "CHK" then do
    if verbose then say 'INFO:  wpi4rpm: Mode = "'Mode'"'
    if words(arguments) = 2 then arguments = arguments' 99.99.99-99'
    cversion  = word(arguments,words(arguments))
    pRApp     = substr(arguments,length(mode)+2,length(arguments)-(length(mode)+1)-(length(cversion)+1))
    parse var cversion RMV'.'RLV'.'RBL'-'RRV'.' .

    RMV       = strip(RMV)
    RLV       = strip(RLV)
    RBL       = strip(RBL)
    RRV       = strip(RRV)
    if datatype(RMV) <> "NUM" then RMV = 99
    if datatype(RLV) <> "NUM" then RLV = 99
    if datatype(RBL) <> "NUM" then RBL = 99
    if datatype(RRV) <> "NUM" then RRV = 99
    
    if pos('/',pRApp) = 0 then do
        RApp = strip(pRApp)
        RVendor   = "wpi4rpm" /* We do not add the true vendor on purpose */
        RPackage  = "wpi4rpm" /* We do not add the true packages on purpose */
    end
    else do
        parse var pRApp RVendor '/' pRApp
        if pos('/',pRApp) = 0 then do
            RApp = pRApp
            RPackage  = "wpi4rpm" /* We do not add the true packages on purpose */
        end
        else do
            parse var pRApp RApp '/' RPackage
        end
    end
end
else do
    say 'WPI4RPM Version 'ScriptVer' (c) 2017-2019 Herwig Bauernfeind for bww bitwise works GmbH.'
    say 
    say '  Adds dummy, removes or checks for WPI packages in WarpIN database.'
    say 
    say '  wpi4rpm ADD "Vendor/App/Package" x.x.x-x'
    say '  wpi4rpm DEL "Vendor/App/Package" x.x.x-x'
    say '  wpi4rpm CHK "Vendor/App/Package" [x.x.x-x]'
    say '  wpi4rpm HELP | /? | /H | /HELP | -H | --HELP'
    say 
    say '  Commands are not case sensitive.'
    say
    say '  Vendor and Package are optional and get a fixed value of wpi4rpm if omitted.'
    say '  x.x.x-x is the rpm version number'
    say
    say '  Note: In case more than 1 DATAS_?.INI file is found, the first one will be'
    say '        used and a warning thrown.'
    exit 0
end
    
WarpINPath = ''
DatBas     = ''

WarpINPath = strip(SysIni("USER","WarpIN","Path"),,'00'x)

ok = SysFileTree(WarpINPath"\DATBAS*",WarpINbas.,"FO")
select 
    when WarpINbas.0 = 0 then do
        if verbose then say 'INFO:  wpi4rpm: WarpINPath = "'WarpINPath'"'
        say "ERROR: wpi4rpm: No WarpIN database found."
        exit -2
    end
    when WarpINbas.0 > 1 then do
        if verbose then say 'INFO:  wpi4rpm: WarpINPath = "'WarpINPath'"'
        say "ERROR: wpi4rpm: Warning: "WarpINbas.0" WarpIN databases found. Using "WarpINbas.1
        DatBas = WarpINbas.1
    end
    otherwise DatBas = WarpINbas.1
end

ok = SysIni(DatBas,"ALL:",WarpINApps.)
if datatype(WarpINApps.0) <> "NUM" then do
    if verbose then say 'ERROR: wpi4rpm: Could not open WarpIN database "'datbas'".'
    say 'ERROR: wpi4rpm: Please, close WarpIN and reinstall "'RApp'" again.'
    exit -3
end
AppString = RVendor'\'RApp'\'RPackage'\'RMV'\'RLV'\'RBL'\'RRV

select
    when Mode = "ADD" then do
        if verbose then say 'INFO:  wpi4rpm: "'Datbas'" will be used.'
        InstTime = time()
        InstDate = date('S')
        ihh      = right('0'||d2x(left(InstTime,2)),2)
        imm      = right('0'||d2x(substr(InstTime,4,2)),2)
        iss      = right('0'||d2x(substr(InstTime,7,2)),2)
        iyyyy    = right('0'||d2x(left(InstDate,4)),4)
        iyyyy    = right(iyyyy,2)||left(iyyyy,2)
        imt      = right('0'||d2x(substr(InstDate,5,2)),2)
        idd      = right('0'||d2x(substr(InstDate,7,2)),2)
        istr     = ihh||imm||iss||'00'||idd||imt||iyyyy||'FFFF0300'
        dyn      = "idt = '"istr"'x"
        interpret dyn
        
        ok = SysIni(DatBas, AppString, "Description", "This package was installed using RPM/YUM technology. This is a dummy entry."||"00"x)
        ok = SysIni(DatBas, AppString, "Files", "rpmdummy"||"00"x||"00000000"x||"00000000"x||"00000000"x||"00"x)
        ok = SysIni(DatBas, AppString, "InstalledUsing", "9.9.9.9"||"00"x)
        ok = SysIni(DatBas, AppString, "InstallDateTime", idt)
        ok = SysIni(DatBas, AppString, "TargetPath", "DEV\NULL"||"00"x)
        ok = SysIni(DatBas, AppString, "WIPackHeader",copies("00"x,16)||"Pck001"||copies("00"x,26))
        if verbose then say 'INFO:  wpi4rpm: "'Appstring'" added.'
        exit ok
    end
    when mode = "DEL" then do
        if verbose then say 'INFO:  wpi4rpm: "'Datbas'" will be used.'
        AppRemoved = 0
        do I = 1 to WarpINApps.0
            parse var WarpINApps.I WVendor '\' WApp '\' WPackage '\' WMV '\' WLV '\' WBL '\' WRV
            if pos(WVendor'\'WApp'\'WPackage'\', AppString) = 1 then do
                ok = SysIni(DatBas, WarpINApps.I, "DELETE:")
                AppRemoved = 1
                if verbose then say 'INFO:  wpi4rpm: "'WarpINApps.I'" removed.'
            end
        end
        if (WarpINApps.0 = 0 & AppRemoved = 0) then do
            if verbose then say 'ERROR: wpi4rpm: "'AppString'" not found.'
            exit -4
        end
    end
    when mode = "CHK" then do
        if verbose then say 'INFO:  wpi4rpm: "'Datbas'" will be used.'
        AppFound = 0
        do I = 1 to WarpINApps.0
            parse var WarpINApps.I WVendor '\' WApp '\' WPackage '\' WMV '\' WLV '\' WBL '\' WRV
            if pos(WApp'\', AppString) > 0 then do
                if RMV'\'RLV'\'RBL'\'RRV = '99\99\99\99' then Appfound = 1
                else if pos(WMV'\'WLV'\'WBL'\'WRV, AppString) > 0 then Appfound = 1
                if verbose then say 'INFO:  wpi4rpm: "'WarpINApps.I'" found.'
            end
            if Appfound = 1 then leave
		end
		exit AppFound
    end
    otherwise do
        say "ERROR: wpi4rpm: Unknown command invoked. Run wpi4rpm help to learn about usage."
    end
end

exit 0

errorhandler:
    say "ERROR: wpi4rpm: An error occured in line "sigl" "left(strip(sourceline(sigl)),40)'...'
exit 255
