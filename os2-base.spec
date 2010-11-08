
Summary: OS/2 - eComStation 2.0 base
Name: os2-base
Version: 0.0.0
Release: 1

License: free

Requires: cube
Requires: os2-release

Provides: ansicall
Provides: asiacol
Provides: bdbvh
Provides: bdcall32
Provides: bdcalls
Provides: bdime
Provides: bdview
Provides: bdwpcls
Provides: bidipm
Provides: bkscalls
Provides: bmscalls
Provides: bvhinit
Provides: bvhmpa
Provides: bvhsvga
Provides: bvhvga
Provides: bvhwndw
Provides: bvscalls
Provides: cdtbl
Provides: chkdsk32
Provides: cidlog
Provides: cometdll
Provides: cyrime
Provides: dibdrvr
Provides: display
Provides: dmiapi
Provides: dmiquery
Provides: dmqsprof
Provides: doscall1
Provides: doscalls
Provides: dosrfico
Provides: dspimri
Provides: dspres
Provides: ehxdlmri
Provides: engine
Provides: errlog
Provides: errtxt
Provides: ffconfig
Provides: ffdump
Provides: ffgui
Provides: ffipc
Provides: ffpct
Provides: ffprobe
Provides: ffst
Provides: filever
Provides: fka
Provides: fw2dll
Provides: gbm
Provides: gengradd
Provides: genpmi
Provides: glocmri
Provides: glut
Provides: gre2vman
Provides: helpmgr
Provides: hpmgrmri
Provides: hwdvpd
Provides: ibmdev32
Provides: ibmgpmi
Provides: ibmhmgr
Provides: ibmvga32
Provides: imp
Provides: inscfg32
Provides: inspgm32
Provides: inst32
Provides: install
Provides: instres
Provides: ivm
Provides: kbdcalls
Provides: lfapi
Provides: libaux
Provides: libcm
Provides: libcn
Provides: libcs
Provides: libtk
Provides: libuni
Provides: lmdll
Provides: locale
Provides: lvm
Provides: mdmi
Provides: minxmri
Provides: minxobj
Provides: mipmini
Provides: mirrors
Provides: mmioi
Provides: mmpmcrts
Provides: mmpmini
Provides: mmsniff
Provides: moncalls
Provides: moucalls
Provides: msg
Provides: namedsp
Provides: namefw
Provides: namerexx
Provides: nampipes
Provides: nls
Provides: npfimri
Provides: npxemltr
Provides: nwiapi
Provides: oasis
Provides: objdata
Provides: opengl
Provides: orexutil
Provides: orexx
Provides: orexxsc
Provides: orexxsom
Provides: orexxwps
Provides: os2char
Provides: os2mm
Provides: os2om30
Provides: os2oooc
Provides: os2oor3u
Provides: os2sm
Provides: panogrex
Provides: picv
Provides: pmatm
Provides: pmbidi
Provides: pmbind
Provides: pmchkdsk
Provides: pmclip
Provides: pmctls
Provides: pmdde
Provides: pmddeml
Provides: pmdfmsg
Provides: pmdrag
Provides: pmex
Provides: pmformat
Provides: pmgpi
Provides: pmgre
Provides: pmi10c8
Provides: pmi102b
Provides: pmi102c
Provides: pmi1002
Provides: pmi1023
Provides: pmi5333
Provides: pmmerge
Provides: pmmle
Provides: pmmrgres
Provides: pmpic
Provides: pmpre
Provides: pmrexxio
Provides: pmsdmri
Provides: pmshapi
Provides: pmshltkt
Provides: pmspl
Provides: pmtkt
Provides: pmunif
Provides: pmvdmh
Provides: pmvdmp
Provides: pmviop
Provides: pmwin
Provides: pmwinx
Provides: pmwp
Provides: pmwpmri
Provides: pnp
Provides: pnpmri
Provides: prodmri
Provides: prog
Provides: progfldr
Provides: quecalls
Provides: registry
Provides: rexx
Provides: rexxapi
Provides: rexxcrt
Provides: rexxinit
Provides: rexxsom
Provides: rexxutil
Provides: rminfo
Provides: rspimri
Provides: rxvidcfg
Provides: s3pmi
Provides: sbfilter
Provides: scenter
Provides: seamless
Provides: sesmgr
Provides: shield
Provides: shpiinst
Provides: softdraw
Provides: som
Provides: somd
Provides: somem
Provides: somir
Provides: soms
Provides: somsec
Provides: somtc
Provides: somu
Provides: somuc
Provides: spl1b
Provides: spoolcp
Provides: svga
Provides: svgaimri
Provides: svgainst
Provides: svgamri
Provides: sysfont
Provides: syslogpm
Provides: thailib
Provides: tracedll
Provides: trcformt
Provides: truetype
Provides: ucdfs
Provides: uconv
Provides: uhpfs
Provides: ujfs
Provides: unikbd
Provides: uudf
Provides: vbe2grad
Provides: vcfgmri
Provides: vgagradd
Provides: videocfg
Provides: videopmi
Provides: viocalls
Provides: vman
Provides: wcfgmri
Provides: wincfg
Provides: winprf
Provides: wpcomet
Provides: wpconfig
Provides: wpconmri
Provides: wpdserv
Provides: wpdsrvp
Provides: wpinet
Provides: wpinstal
Provides: wpintmri
Provides: wpnls
Provides: wppansys
Provides: wpprint
Provides: wpprtmri
Provides: wpstkmou
Provides: wpstkmri
Provides: wpvidsys


%description
Virtual package for OS/2 base shared libraries packaging.


%prep
# nothing to do

%build
# nothing to do

%install
# nothing to do

%clean
# nothing to do

%files
# no files in a virtual package

%post
%cube {ADDSTRING "%UNIXROOT%\usr\sbin;%UNIXROOT%\usr\bin;%UNIXROOT%\sbin;%UNIXROOT%\bin;" IN "SET PATH=" (FIRST IFNEW BEFORE RS(%%)} c:\config.sys c:\config.sys.yum > NUL
%cube {ADDSTRING "%UNIXROOT%\usr\lib;" IN "LIBPATH=" (FIRST IFNEW BEFORE RS(%%)} c:\config.sys > NUL
%cube {DELLINE "SET UNIXROOT="} c:\config.sys > NUL
%cube {ADDLINE "SET UNIXROOT=%UNIXROOT%"} c:\config.sys > NUL

%postun
%cube {DELSTRING "%UNIXROOT%\usr\sbin;%UNIXROOT%\usr\bin;%UNIXROOT%\sbin;%UNIXROOT%\bin;" IN "SET PATH=" (FIRST IFNEW BEFORE RS(%%)} c:\config.sys > NUL
%cube {DELSTRING "%UNIXROOT%\usr\lib;" IN "LIBPATH=" (FIRST IFNEW BEFORE RS(%%)} c:\config.sys > NUL
%cube {DELLINE "SET UNIXROOT="} c:\config.sys > NUL
