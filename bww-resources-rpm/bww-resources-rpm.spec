%define debug_package %{nil}
%define _strip_opts --no-compress --no-debuginfo

Summary:       bitwise works icons and folders
Name:          bww-resources-rpm
Version:       1.1.3
Release:       1%{?dist}
License:       Proprietory
Group:         Applications/System
URL:           http://www.bitwiseworks.com
Vendor:        bww bitwise works GmbH
Source1:       macros.bww
Source2:       bww-fix-docdir.cmd
Source10:      bwwfbkg.bmp
Source11:      bwwfldrc.ico
Source12:      bwwfldro.ico
Source13:      mkres.obj
BuildRoot:     %_tmppath/%name-%version-%release-root
BuildArch:     noarch
Obsoletes:     bwwres
Provides:      bwwres = %{version}
Requires:      os2-rpm >= 0-4

BuildRequires: rexx_exe

%description
This package provides bitwise works icons and folder background

%package build
Summary:    bww rpm macros for rpm
Group:      Development/Libraries

%description build
This package provides bitwise works macros for rpm builds

%prep
%setup -n "%{name}-%{version}" -Tc

# Prepare forwarder DLLs.
for m in %{SOURCE1} %{SOURCE2} %{SOURCE10} %{SOURCE11} %{SOURCE12} %{SOURCE13}; do
  cp ${m} .
done

cat << EOF >mkres.def
;  MKRES.DEF: Definition file for resource DLL's
;  -----------------------------------------------


LIBRARY

CODE SHARED
DATA SHARED SINGLE

PROTMODE
EOF

cat << EOF >bwwres.rc
ICON     1 BWWFLDRC.ICO
ICON     2 BWWFLDRO.ICO
BITMAP   3 BWWFBKG.BMP
EOF

%build
link386 /A:4 /BASE:0x12000000 /NOD /NOL mkres.obj, bwwres.dll, nul, , mkres;
rc bwwres.rc bwwres.dll

%install
install -p -m0644 -D bwwres.dll  $RPM_BUILD_ROOT%{_libdir}/bwwres.dll
install -p -m0644 -D macros.bww  $RPM_BUILD_ROOT%{_rpmconfigdir}/macros.d/macros.bww
install -p -m0644 -D bwwfbkg.bmp $RPM_BUILD_ROOT%{_datadir}/os2/bww/bwwfbkg.bmp 
install -p -m0644 -D bwwfldrc.ico $RPM_BUILD_ROOT%{_datadir}/os2/bww/bwwfldrc.ico
install -p -m0644 -D bwwfldro.ico $RPM_BUILD_ROOT%{_datadir}/os2/bww/bwwfldro.ico

%{__mkdir_p} %{buildroot}%{_bindir}
for f in *.cmd; do
  rexx2vio "$f" "%{buildroot}%{_bindir}/${f%.cmd}.exe"
done

%clean
rm -rf "$RPM_BUILD_ROOT"

%post
bww-fix-docdir

%postun

%files
%defattr(-,root,root,-)
%{_bindir}/bww-fix-docdir.exe
%{_libdir}/bwwres.dll
%{_datadir}/os2/bww/bwwfbkg.bmp
%{_datadir}/os2/bww/*.ico

%files build
%{_libdir}/rpm/macros.d/macros.bww

%changelog
* Mon Aug 12 2019 Dmitriy Kuminov <coding@dmik.org> 1.1.3-1
- Open package folder instead of help folder when using bww_folder.

* Fri Dec 15 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.1.2-1
- adjusted bww_app_shadow a bit
- reworded the help and info in the macro (no functional change)

* Thu Dec 14 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.1.1-1
- added bww_app_shadow and removed the -s switch from bww_app

* Wed Oct 04 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.1.0-3
- changed bww_doc to bww_docdir
- changed "Documentation" to "Package Documentation"

* Tue Oct 03 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.1.0-2
- added bww_changelog macro
- added a req for os2-rpm >= 0-4 to be sure all exe and symlink are available

* Thu Sep 07 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.1.0-1
- big overhaul of the macros
- added better documentation
- add several presentation parameters to the bitwise help center

* Thu Jun 29 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.0.2-1
- added -nv parameter to the macro
- fixed a possible wps id issue in the readme part of the macro

* Thu Jun 08 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.0.1-1
- redesigned the macro completely
- moved the macro to -devel
- renamed the spec

* Sat Mar 18 2017 hb <herwig.bauernfeind@bitwiseworks.com> 1.0.0-5
- fix -a switch (diver)

* Tue Mar 14 2017 hb <herwig.bauernfeind@bitwiseworks.com> 1.0.0-4
- -a switch in order to allow file filters

* Mon Mar 06 2017 hb <herwig.bauernfeind@bitwiseworks.com> 1.0.0-3
- -t switch in order to allow custom object titles (diver)

* Mon Mar 06 2017 hb <herwig.bauernfeind@bitwiseworks.com> 1.0.0-2
- fix exe shadow
- heavily modified specfile (diver)

* Fri Mar 03 2017 hb <herwig.bauernfeind@bitwiseworks.com> 1.0.0-1
- first release of bitwise works icons, bitmaps and macros
