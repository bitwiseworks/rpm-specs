%define debug_package %{nil}
%define _strip_opts --no-compress --no-debuginfo

Summary:    bitwiseworks icons and folders
Name:       bww-resources-rpm
Version:    1.0.2
Release:    1%{?dist}
License:    Proprietory
Group:      Applications/System
URL:        http://www.bitwiseworks.com
Vendor:     bww bitwiseworks GmbH
Source1:    macros.bww
Source10:   bwwfbkg.bmp
Source11:   bwwfldrc.ico
Source12:   bwwfldro.ico
Source13:   mkres.obj
BuildRoot:  %_tmppath/%name-%version-%release-root
BuildArch:  noarch
Obsoletes:  bwwres
Provides:   bwwres = %{version}

%description
This package provides bitwiseworks icons and folder background

%package build
Summary:    bww rpm macros for rpm
Group:      Development/Libraries

%description build
This package provides bitwiseworks macros for rpm builds

%prep
%setup -n "%{name}-%{version}" -Tc

# Prepare forwarder DLLs.
for m in %{SOURCE1} %{SOURCE10} %{SOURCE11} %{SOURCE12} %{SOURCE13}; do
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

%clean
rm -rf "$RPM_BUILD_ROOT"

%post
if [ "$1" -eq 0 ]; then # (upon install)
    %wps_object_create WP_BWWHELP:WPFolder|bww Help|<WP_ASSISTANCE>|TITLE=bitwiseworks Help Center;SHOWALLINTREEVIEW=YES;ICONRESOURCE=60,PMWP.DLL;ICONNRESOURCE=83,PMWP.DLL;BACKGROUND=((/@unixroot/usr/share/os2/bww/bwwfbkg.bmp));\
    %wps_object_create WP_BWWDOC:WPShadow|Documentation|<WP_BWWHELP>|SHADOWID=((/@unixroot/usr/share/doc));\
    %wps_object_create WP_BWWAPPS:WPFolder|bww Apps|<WP_PROGRAMSFOLDER>|TITLE=bitwiseworks Apps and Ports;ICONRESOURCE=1,BWWRES.DLL;ICONNFILE=((/@unixroot/usr/share/os2/bww/bwwfldro.ico));BACKGROUND=((/@unixroot/usr/share/os2/bww/bwwfbkg.bmp));ICONVIEW=FLOWED;\
    %wps_object_create WP_BWWHELPSHADOW:WPShadow|bitwiseworks Help Center|<WP_BWWAPPS>|SHADOWID=<WP_BWWHELP>;
fi


%postun
if [ "$1" -eq 0 ]; then # (upon removal)
    %wps_object_delete_all
fi

%files
%defattr(-,root,root,-)
%_libdir/bwwres.dll
%_datadir/os2/bww/bwwfbkg.bmp
%_datadir/os2/bww/*.ico

%files build
%_libdir/rpm/macros.d/macros.bww

%changelog
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
- first release of bitwiseworks icons, bitmaps and macros
