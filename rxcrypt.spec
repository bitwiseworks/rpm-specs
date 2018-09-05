%define debug_package %{nil}
%define _strip_opts --no-compress --no-debuginfo



Summary:    Dmitry A.Steklenev's RxCrypt library
Name:       rxcrypt
Version:    1.0.0
Release:    3%{?dist}
License:    Public Domain
Group:      Applications/System
URL:        http://glass.ptv.ru
Vendor:     Dmitry A.Steklenev
Source:     %{name}-%{version}.zip
BuildRoot:  %_tmppath/%name-%version-%release-root
Requires:   os2-rpm >= 1-2

%description
This Rexx DLL provides a crypt API.

%prep
%setup -n "%{name}-%{version}" -Tc
unzip -qj %{_sourcedir}/%{name}-%{version}.zip

%build


%install
install -p -m0644 -D rxcrypt.dll  $RPM_BUILD_ROOT%{_libdir}/rxcrypt.dll


%clean
rm -rf "$RPM_BUILD_ROOT"

%post
if [ "$1" -ge 1 ]; then # (upon update)
    %wps_object_delete_all
    %{_rpmconfigdir_os2}/wpi4rpm del %{vendor}/RxCrypt/Library %{version}-%{release}
fi
%wps_object_create_begin
WP_BWWHELP:WPFolder|bww Help|<WP_ASSISTANCE>|TITLE=bitwiseworks Help Center;SHOWALLINTREEVIEW=YES;ICONRESOURCE=60,PMWP.DLL;
%wps_object_create_end
%{_rpmconfigdir_os2}/wpi4rpm add %{vendor}/RxCrypt/Library %{version}-%{release}

%postun
if [ "$1" -eq 0 ]; then # (upon removal)
    %wps_object_delete_all
    %{_rpmconfigdir_os2}/wpi4rpm del %{vendor}/RxCrypt/Library %{version}-%{release}
fi

%files
%defattr(-,root,root,-)
%doc *.html *.phtml *.gif crypt.txt sample.cmd rxcryptsrc.zip
%_libdir/*.dll


%changelog
* Wed Sep 05 2018 hb <herwig.bauernfeind@bitwiseworks.com> 1.0.0-3
- fix the spec file (Silvan Scherrer)

* Wed Jun 06 2018 hb <herwig.bauernfeind@bitwiseworks.com> 1.0.0-2
- fix the location of wpi4rpm

* Sun Feb 05 2017 hb <herwig.bauernfeind@bitwiseworks.com> 1.0.0-1
- final and only release from Dmitry A.Steklenev AKA GlassMan
