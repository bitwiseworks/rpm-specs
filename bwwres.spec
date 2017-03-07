%define debug_package %{nil}
%define _strip_opts --no-compress --no-debuginfo

Summary:    bitwiseworks icons and folders
Name:       bwwres
Version:    1.0.0
Release:    2%{?dist}
License:    Proprietory
Group:      Applications/System
URL:        http://www.bitwiseworks.com
Vendor:     bww bitwiseworks GmbH
Source1:    bwwres.dll
Source2:    macros.bww
Source10:   bwwfbkg.bmp
Source11:   bwwfldrc.ico
Source12:   bwwfldro.ico
BuildRoot:  %_tmppath/%name-%version-%release-root

%description
This package provides bitwiseworks icons and folder background

%prep
%setup -n "%{name}-%{version}" -Tc

%build


%install
install -p -m0644 -D %{SOURCE1}  $RPM_BUILD_ROOT%{_libdir}/bwwres.dll
install -p -m0644 -D %{SOURCE2}  $RPM_BUILD_ROOT%{_rpmconfigdir}/macros.d/macros.bww
install -p -m0644 -D %{SOURCE10} $RPM_BUILD_ROOT%{_datadir}/os2/bww/bwwfbkg.bmp 
install -p -m0644 -D %{SOURCE11} $RPM_BUILD_ROOT%{_datadir}/os2/bww/bwwfldrc.ico
install -p -m0644 -D %{SOURCE12} $RPM_BUILD_ROOT%{_datadir}/os2/bww/bwwfldro.ico

%clean
rm -rf "$RPM_BUILD_ROOT"

%post
if [ "$1" -ge 1 ]; then # (upon update)
    %wps_object_delete_all
fi

%postun
if [ "$1" -eq 0 ]; then # (upon removal)
    %wps_object_delete_all
fi

%files
%defattr(-,root,root,-)
%_libdir/bwwres.dll
%_libdir/rpm/macros.d/macros.bww
%_datadir/os2/bww/bwwfbkg.bmp
%_datadir/os2/bww/*.ico

%changelog
* Mon Mar 06 2017 hb <herwig.bauernfeind@bitwiseworks.com> 1.0.0-2
- fix exe shadow
- heavily modified specfile (diver)
* Fri Mar 03 2017 hb <herwig.bauernfeind@bitwiseworks.com> 1.0.0-1
- first release of bitwiseworks icons, bitmaps and macros
