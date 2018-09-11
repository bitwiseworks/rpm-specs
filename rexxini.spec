%define debug_package %{nil}
%define _strip_opts --no-compress --no-debuginfo


Summary:    Steven Elliott's REXXINI library
Name:       REXXINI
Version:    1.0.0
Release:    2%{?dist}
License:    Freeware
Group:      Applications/System
URL:        http://www.edm2.com/index.php/RexxINI
Vendor:     Steven Elliott
Source:     %{name}-%{version}.zip
BuildRoot:  %_tmppath/%name-%version-%release-root
Requires:   os2-rpm >= 1-2

%description
Rexx API's for manipulation of Text Based INI Files (used by Samba and WINOS2)
Useful for manipulating and fixing text ini files used by Samba, DOS and windows programs


%prep
%setup -n "%{name}-%{version}" -Tc
unzip -q %{_sourcedir}/%{name}-%{version}.zip

%build


%install
install -p -m0644 -D rexxini.dll $RPM_BUILD_ROOT%{_libdir}/rexxini.dll


%clean
rm -rf "$RPM_BUILD_ROOT"


%post
if [ "$1" -ge 1 ]; then # (upon update)
    %wps_object_delete_all
    %{_rpmconfigdir_os2}/wpi4rpm del Steven Elliot/REXXIni/Library %{version}-%{release}
fi
%{_rpmconfigdir_os2}/wpi4rpm add Steven Elliot/REXXIni/Library %{version}-%{release}


%postun
if [ "$1" -eq 0 ]; then # (upon removal)
    %wps_object_delete_all
    %{_rpmconfigdir_os2}/wpi4rpm del Steven Elliot/REXXIni/Library %{version}-%{release}
fi


%files
%defattr(-,root,root,-)
%doc rexxini.txt
%_libdir/*.dll


%changelog
* Fri May 12 2017 hb <herwig.bauernfeind@bitwiseworks.com> 1.0.0-2
- do not lxlite rexxini.dll
* Sun Feb 05 2017 hb <herwig.bauernfeind@bitwiseworks.com> 1.0.0-1
- final release from Steven Elliott
