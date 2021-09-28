
Summary: OS/2 - eComStation 2.0 - ArcaOS 5.0 base
Name: os2-base
Version: 0.0.1
Release: 3%{?dist}

License: free

Requires: os2-release

# For os2_expand_unixroot
BuildRequires: os2-rpm >= 1-2
Requires: os2-rpm >= 1-2
Requires: libc >= 1:0.1.0-1

Provides: ansicall.dll
Provides: asiacol.dll
Provides: bdbvh.dll
Provides: bdcall32.dll
Provides: bdcalls.dll
Provides: bdime.dll
Provides: bdview.dll
Provides: bdwpcls.dll
Provides: bidipm.dll
Provides: bkscalls.dll
Provides: bmscalls.dll
Provides: bvhinit.dll
Provides: bvhmpa.dll
Provides: bvhsvga.dll
Provides: bvhvga.dll
Provides: bvhwndw.dll
Provides: bvscalls.dll
Provides: cdtbl.dll
Provides: chkdsk32.dll
Provides: cidlog.dll
Provides: cometdll.dll
Provides: cyrime.dll
Provides: dibdrvr.dll
Provides: display.dll
Provides: dmiapi.dll
Provides: dmiquery.dll
Provides: dmqsprof.dll
Provides: doscall1.dll
Provides: doscalls.dll
Provides: dosrfico.dll
Provides: dspimri.dll
Provides: dspres.dll
Provides: ehxdlmri.dll
Provides: engine.dll
Provides: errlog.dll
Provides: errtxt.dll
Provides: ffconfig.dll
Provides: ffdump.dll
Provides: ffgui.dll
Provides: ffipc.dll
Provides: ffpct.dll
Provides: ffprobe.dll
Provides: ffst.dll
Provides: filever.dll
Provides: fka.dll
Provides: fw2dll.dll
Provides: gbm.dll
Provides: gengradd.dll
Provides: genpmi.dll
Provides: glocmri.dll
Provides: glut.dll
Provides: gre2vman.dll
Provides: helpmgr.dll
Provides: hpmgrmri.dll
Provides: hwdvpd.dll
Provides: ibmdev32.dll
Provides: ibmgpmi.dll
Provides: ibmhmgr.dll
Provides: ibmvga32.dll
Provides: imp.dll
Provides: inscfg32.dll
Provides: inspgm32.dll
Provides: inst32.dll
Provides: install.dll
Provides: instres.dll
Provides: ivm.dll
Provides: kbdcalls.dll
Provides: lfapi.dll
Provides: libaux.dll
Provides: libcm.dll
Provides: libcn.dll
Provides: libcs.dll
Provides: libtk.dll
Provides: libuni.dll
Provides: lmdll.dll
Provides: locale.dll
Provides: lvm.dll
Provides: mdmi.dll
Provides: minxmri.dll
Provides: minxobj.dll
Provides: mipmini.dll
Provides: mirrors.dll
Provides: mmio.dll
Provides: mmpmcrts.dll
Provides: mmpmini.dll
Provides: mmsniff.dll
Provides: moncalls.dll
Provides: moucalls.dll
Provides: msg.dll
Provides: namedsp.dll
Provides: namefw.dll
Provides: namerexx.dll
Provides: nampipes.dll
Provides: nls.dll
Provides: npfimri.dll
Provides: npxemltr.dll
Provides: nwiapi.dll
Provides: oasis.dll
Provides: objdata.dll
Provides: opengl.dll
Provides: orexutil.dll
Provides: orexx.dll
Provides: orexxsc.dll
Provides: orexxsom.dll
Provides: orexxwps.dll
Provides: os2char.dll
Provides: os2mm.dll
Provides: os2om30.dll
Provides: os2oooc.dll
Provides: os2oor3u.dll
Provides: os2sm.dll
Provides: panogrex.dll
Provides: picv.dll
Provides: pmatm.dll
Provides: pmbidi.dll
Provides: pmbind.dll
Provides: pmchkdsk.dll
Provides: pmclip.dll
Provides: pmctls.dll
Provides: pmdde.dll
Provides: pmddeml.dll
Provides: pmdfmsg.dll
Provides: pmdrag.dll
Provides: pmex.dll
Provides: pmformat.dll
Provides: pmgpi.dll
Provides: pmgre.dll
Provides: pmi10c8.dll
Provides: pmi102b.dll
Provides: pmi102c.dll
Provides: pmi1002.dll
Provides: pmi1023.dll
Provides: pmi5333.dll
Provides: pmmerge.dll
Provides: pmmle.dll
Provides: pmmrgres.dll
Provides: pmpic.dll
Provides: pmpre.dll
Provides: pmrexxio.dll
Provides: pmsdmri.dll
Provides: pmshapi.dll
Provides: pmshltkt.dll
Provides: pmspl.dll
Provides: pmtkt.dll
Provides: pmunif.dll
Provides: pmvdmh.dll
Provides: pmvdmp.dll
Provides: pmviop.dll
Provides: pmwin.dll
Provides: pmwinx.dll
Provides: pmwp.dll
Provides: pmwpmri.dll
Provides: pnp.dll
Provides: pnpmri.dll
Provides: prodmri.dll
Provides: prog.dll
Provides: progfldr.dll
Provides: quecalls.dll
Provides: registry.dll
Provides: rexx.dll
Provides: rexxapi.dll
Provides: rexxcrt.dll
Provides: rexxinit.dll
Provides: rexxsom.dll
Provides: rexxutil.dll
Provides: rminfo.dll
Provides: rspimri.dll
Provides: rxvidcfg.dll
Provides: s3pmi.dll
Provides: sbfilter.dll
Provides: scenter.dll
Provides: seamless.dll
Provides: sesmgr.dll
Provides: shield.dll
Provides: shpiinst.dll
Provides: softdraw.dll
Provides: som.dll
Provides: somd.dll
Provides: somem.dll
Provides: somir.dll
Provides: soms.dll
Provides: somsec.dll
Provides: somtc.dll
Provides: somu.dll
Provides: somuc.dll
Provides: spl1b.dll
Provides: spoolcp.dll
Provides: svga.dll
Provides: svgaimri.dll
Provides: svgainst.dll
Provides: svgamri.dll
Provides: sysfont.dll
Provides: syslogpm.dll
Provides: thailib.dll
Provides: tracedll.dll
Provides: trcformt.dll
Provides: truetype.dll
Provides: ucdfs.dll
Provides: uconv.dll
Provides: uhpfs.dll
Provides: ujfs.dll
Provides: unikbd.dll
Provides: uudf.dll
Provides: vbe2grad.dll
Provides: vcfgmri.dll
Provides: vgagradd.dll
Provides: videocfg.dll
Provides: videopmi.dll
Provides: viocalls.dll
Provides: vman.dll
Provides: wcfgmri.dll
Provides: wincfg.dll
Provides: winprf.dll
Provides: wpcomet.dll
Provides: wpconfig.dll
Provides: wpconmri.dll
Provides: wpdserv.dll
Provides: wpdsrvp.dll
Provides: wpinet.dll
Provides: wpinstal.dll
Provides: wpintmri.dll
Provides: wpnls.dll
Provides: wppansys.dll
Provides: wpprint.dll
Provides: wpprtmri.dll
Provides: wpstkmou.dll
Provides: wpstkmri.dll
Provides: wpvidsys.dll

%description
Virtual package for OS/2 base shared libraries packaging.

%package unixtools-path
License:        free
Summary:        Makes unix tools from findutils and coreutils first in PATH.

%description unixtools-path
Adds /@unixroot/usr/libexec/bin at beginning of system PATH, to allow conflicting
tools from findutils and coreutils to be used instead of default OS/2 tools.


%prep
# nothing to do

%build
# nothing to do

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__mkdir_p} -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/rpm
echo pentium4-OS/2-OS/2 > $RPM_BUILD_ROOT%{_sysconfdir}/rpm/platform

%{__mkdir_p} %{buildroot}%{os2_bookdir}
%{__mkdir_p} %{buildroot}%{os2_helpdir}
%{__mkdir_p} %{buildroot}%{os2_langdir}


%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/rpm/platform
%dir %{os2_bookdir}
%dir %{os2_helpdir}
%dir %{os2_langdir}

%files unixtools-path
%defattr(-,root,root,-)
# no files in a virtual package


%post -e
if [ "$1" = 1 ] ; then
#execute only on first install
%cube {ADDSTRING "%{os2_dos_path %{_sbindir};%{_bindir}};" IN "SET PATH=" (FIRST IFNEW BEFORE RS(%%)} %%{os2_config_sys} %%{os2_config_sys}.yum > NUL
%cube {ADDSTRING "%{os2_dos_path %{_libdir}};" IN "LIBPATH=" (FIRST IFNEW BEFORE RS(%%)} %%{os2_config_sys} > NUL
%cube {DELLINE "SET UNIXROOT="} %%{os2_config_sys} > NUL
%cube {ADDLINE "SET UNIXROOT=%UNIXROOT%" (ALWAYS)} %%{os2_config_sys} > NUL
fi
%cube {ADDLINE "SET TERM=os2" (IFNOT "SET TERM=")} %%{os2_config_sys} > NUL
%cube {ADDLINE "REM [ Default shell values ]" (IFNOT "REM [ Default shell values ]")} %%{os2_config_sys} > NUL
%cube {ADDLINE "SET SHELL=%%{os2_expand_unixroot %%{_bindir}/sh.exe}" (IFNOT "SET SHELL=")} %%{os2_config_sys} > NUL
%cube {ADDLINE "SET EMXSHELL=%%{os2_expand_unixroot %%{_bindir}/sh.exe}" (IFNOT "SET EMXSHELL=")} %%{os2_config_sys} > NUL
%cube {ADDLINE "SET CONFIG_SHELL=%%{os2_expand_unixroot %%{_bindir}/sh.exe}" (IFNOT "SET CONFIG_SHELL=")} %%{os2_config_sys} > NUL
%cube {ADDLINE "SET MAKESHELL=%%{os2_expand_unixroot %%{_bindir}/sh.exe}" (IFNOT "SET MAKESHELL=")} %%{os2_config_sys} > NUL
%cube {ADDLINE "SET EXECSHELL=%%{os2_expand_unixroot %%{_bindir}/sh.exe}" (IFNOT "SET EXECSHELL=")} %%{os2_config_sys} > NUL
%cube {ADDLINE "REM [ Temporary directory ]" (IFNOT "REM [ Temporary directory ]")} %%{os2_config_sys} > NUL
%cube {ADDLINE "SET TMP=%{os2_dos_path /@unixroot/var/tmp}" (IFNOT "SET TMP=")} %%{os2_config_sys} > NUL
%cube {ADDLINE "SET TEMP=%{os2_dos_path /@unixroot/var/tmp}" (IFNOT "SET TEMP=")} %%{os2_config_sys} > NUL
%cube {ADDLINE "SET TMPDIR=%{os2_dos_path /@unixroot/var/tmp}" (IFNOT "SET TMPDIR=")} %%{os2_config_sys} > NUL
%cube {ADDSTRING "%{os2_dos_path %{os2_bookdir}};" IN "SET BOOKSHELF=" (FIRST IFNEW BEFORE RS(%%)} %%{os2_config_sys} > NUL
%cube {ADDSTRING "%{os2_dos_path %{os2_helpdir}};" IN "SET HELP=" (FIRST IFNEW BEFORE RS(%%)} %%{os2_config_sys} > NUL
%cube {ADDSTRING "%{os2_dos_path %{os2_langdir}};" IN "SET DPATH=" (FIRST IFNEW BEFORE RS(%%)} %%{os2_config_sys} > NUL

%postun -e
if [ "$1" = 0 ] ; then
#execute only on last uninstall
%cube {DELSTRING "%{os2_dos_path %{_sbindir};%{_bindir}};" IN "SET PATH=" (FIRST IFNEW BEFORE RS(%%)} %%{os2_config_sys} > NUL
%cube {DELSTRING "%{os2_dos_path %{_libdir}};" IN "LIBPATH=" (FIRST IFNEW BEFORE RS(%%)} %%{os2_config_sys} > NUL
%cube {DELLINE "SET UNIXROOT="} %%{os2_config_sys} > NUL
%cube {DELSTRING "%{os2_dos_path %{os2_bookdir}};" IN "SET BOOKSHELF=" (FIRST} %%{os2_config_sys} > NUL
%cube {DELSTRING "%{os2_dos_path %{os2_helpdir}};" IN "SET HELP=" (FIRST} %%{os2_config_sys} > NUL
%cube {DELSTRING "%{os2_dos_path %{os2_langdir}};" IN "SET DPATH=" (FIRST} %%{os2_config_sys} > NUL
fi

%post unixtools-path -e
if [ "$1" = 1 ] ; then
#execute only on first install
%cube {ADDSTRING "%UNIXROOT%\usr\libexec\bin;" IN "SET PATH=" (FIRST IFNEW BEFORE RS(%%)} %%{os2_config_sys} %%{os2_config_sys}.yum > NUL
fi

%postun unixtools-path -e
if [ "$1" = 0 ] ; then
#execute only on last uninstall
%cube {DELSTRING "%UNIXROOT%\usr\libexec\bin;" IN "SET PATH=" (FIRST IFNEW BEFORE RS(%%)} %%{os2_config_sys} > NUL
fi


%changelog
* Tue Sep 28 2021 Dmitriy Kuminov <coding@dmik.org> 0.0.1-3
- Set pentium4 as defalut platform.

* Mon Nov 18 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> 0.0.1-2
- fix usage os os2_config_sys macro
- use -e for all post/pre state

* Fri Jun 21 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> 0.0.1-1
- remove the fhs package, as not needed with libcn
- add requires to libcn (libc version 1:0.1.0 or better)

* Mon Jun 18 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> 0.0.0-19
- use %{os2_config_sys} macro instead of fixed c:\config.sys

* Mon Apr 23 2018 Dmitriy Kuminov <coding@dmik.org> 0.0.0-18
- Make sure SHELL/EMXSHELL and friends in CONFIG.SYS use forward slashes.

* Fri Jul 28 2017 Dmitriy Kuminov <coding@dmik.org> 0.0.0-17
- Use handy os2_dos_path, os2_langdir etc. macros from os2-rpm.
- Make os2-base own os2_langdir.

* Fri Jun 9 2017 Dmitriy Kuminov <coding@dmik.org> 0.0.0-16
- Make os2-rpm a requirement for os2-base (contains essential macros used in scriptlets).

* Mon Feb 20 2017 scs, hb  <herwig,bauernfeind@bitwiseworks.com> 0.0.0-15
- Add SHELL statements
- Add ArcaOS to summary

* Mon Jan 30 2017 hb <herwig,bauernfeind@bitwiseworks.com> 0.0.0-14
- Correct typo from mmioi.dll to mmio.dll

* Wed Jun 08 2016 yd <yd@os2power.com> 0.0.0-13
- Add special UNIXROOT lang directory to DPATH in config.sys.

* Wed Jan 27 2016 Dmitriy Kuminov <coding@dmik.org> 0.0.0-12
- Add special UNIXROOT directories to BOOKSHELF and HELP in config.sys.

* Thu Dec 17 2015 yd <yd@os2power.com> 0.0.0-11
- set i686 as default platform.

* Tue Feb 17 2015 yd <yd@os2power.com> 0.0.0-10
- set TERM to os2 only if undefined.

* Sat Feb 14 2015 yd <yd@os2power.com> 0.0.0-8
- force TERM to ansi (texinfo requirement).

* Tue Jul 30 2013 yd
- add unixtool-path package to prepend /@unixroot/usr/libexec/bin to PATH.

* Wed Jul 24 2013 yd
- put /bin into unixroot drive (requires scripting).

* Thu Mar 21 2013 yd
- added fhs package to provide /bin symlink (for FHS script compatibility).
