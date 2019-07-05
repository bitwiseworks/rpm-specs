%define debug_package %{nil}

Summary:    Paul Ratcliffe's PR1UTIL library
Name:       pr1util
Version:    1.6.5
Release:    2%{?dist}
License:    Freeware
Group:      Applications/System
URL:        http://home.clara.net/orac/os2.htm
Vendor:     Paul Ratcliffe
Source:     %{name}-%{version}.zip
BuildRoot:  %_tmppath/%name-%version-%release-root
Obsoletes:  PR1UTIL
Requires:   os2-rpm >= 1-2

%description
PR1UTIL is a REXX library of miscellaneous functions. It uses TCP/IP
libraries and thus requires TCP/IP to be installed. The program is freeware
and as such USE OF THIS PROGRAM IS ENTIRELY AT YOUR OWN RISK.

%prep
%setup -n "%{name}-%{version}" -Tc
unzip -qj %{_sourcedir}/%{name}-%{version}.zip

%build


%install
install -p -m0644 -D pr1util.dll $RPM_BUILD_ROOT%{_libdir}/pr1util.dll


%clean
rm -rf "$RPM_BUILD_ROOT"


%post
if [ "$1" -ge 1 ]; then # (upon update)
    %wps_object_delete_all
    %{_rpmconfigdir_os2}/wpi4rpm del %{vendor}/Pr1Util/Library %{version}-%{release}
fi
%{_rpmconfigdir_os2}/wpi4rpm add %{vendor}/Pr1Util/Library %{version}-%{release}


%postun
if [ "$1" -eq 0 ]; then # (upon removal)
    %wps_object_delete_all
    %{_rpmconfigdir_os2}/wpi4rpm del %{vendor}/Pr1Util/Library %{version}-%{release}
fi


%files
%defattr(-,root,root,-)
%doc pr1util.txt
%_libdir/*.dll


%changelog
* Tue Sep 11 2018 hb <herwig.bauernfeind@bitwiseworks.com> 1.6.5-2
- fixed rpm and case 
* Sun Feb 05 2017 hb <herwig.bauernfeind@bitwiseworks.com> 1.6.5-1
- final release from Paul Ratcliffe
