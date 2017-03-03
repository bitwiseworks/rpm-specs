%define debug_package %{nil}
%define _strip_opts --no-compress --no-debuginfo



Summary:    bitwiseworks icons and folders
Name:       bwwres
Version:    1.0.0
Release:    1%{?dist}
License:    Proprietory
Group:      Applications/System
URL:        http://www.bitwiseworks.com
Vendor:     bww bitwiseworks GmbH
Source:     %{name}-%{version}.zip
BuildRoot:  %_tmppath/%name-%version-%release-root

%description
This package provides bitwiseworks icons and folder background

%prep
%setup -n "%{name}-%{version}" -Tc
unzip -q %{_sourcedir}/%{name}-%{version}.zip

%build


%install
mkdir -p $RPM_BUILD_ROOT%{_libdir}
cp usr/lib/bwwres.dll $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_libdir}/rpm/macros.d
cp usr/lib/rpm/macros.d/macros.bww $RPM_BUILD_ROOT%{_libdir}/rpm/macros.d
mkdir -p $RPM_BUILD_ROOT%{_datadir}/os2/bww
cp usr/share/os2/bww/bwwfbkg.bmp $RPM_BUILD_ROOT%{_datadir}/os2/bww
cp usr/share/os2/bww/*.ico $RPM_BUILD_ROOT%{_datadir}/os2/bww

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
* Fri Mar 03 2017 hb <herwig.bauernfeind@bitwiseworks.com> 1.0.0-1
- first release of bitwiseworks icons, bitmaps and macros
