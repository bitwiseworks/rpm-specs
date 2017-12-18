%define debug_package %{nil}

Summary:    bwwping subnet monitoring utility
Name:       bwwping
Version:    2.0.0
Release:    2%{?dist}
License:    proprietary
Group:      Applications/System
URL:        http://www.netlabs.org/vxapps
Vendor:     bww bitwise works GmbH
Source:     %{name}-%{version}.zip
BuildRoot:  %_tmppath/%name-%version-%release-root
Requires:   wpi4rpm >= 0.9.2
Requires:   bww-resources-rpm  >= 1.1.0

%description
The purpose of this utility is to monitor hosts on a network.
As such it is a direct replacement for IBM's PMPING, which it supercedes
featurewise. It can import from and export the ping list to HOSTS, it can 
wake known hosts via Wake-on-LAN.

%prep
%setup -n "%{name}-%{version}" -Tc
unzip -q %{_sourcedir}/%{name}-%{version}.zip

%build


%install
mkdir -p $RPM_BUILD_ROOT%{_bindir}
cp *.exe $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-%{version}
cp readme.txt $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-%{version}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/os2/lang
cp *.msg $RPM_BUILD_ROOT%{_datadir}/os2/lang


%clean
rm -rf "$RPM_BUILD_ROOT"

%post
if [ "$1" -ge 1 ]; then # (upon update)
    %wps_object_delete_all
    wpi4rpm del %{vendor}/%{name}/binaries %{version}-%{release}
fi
%global title %{name}
%bww_folder -t %{title}
%bww_app -f %{_bindir}/%{name}.exe -t %{title}
%bww_readme -f %{_defaultdocdir}/%{name}-%{version}/readme.txt
%bww_app_shadow 
%bww_app_shadow -d WP_INETTOOLS
wpi4rpm add %{vendor}/%{name}/binaries %{version}-%{release}

%postun
if [ "$1" -eq 0 ]; then # (upon removal)
    %wps_object_delete_all
    wpi4rpm del %{vendor}/%{name}/binaries %{version}-%{release}
fi

%files
%defattr(-,root,root,-)
%_defaultdocdir/%{name}-%{version}/readme.txt
%_bindir/*.exe
%_datadir/os2/lang/*.msg


%changelog
* Mon Dec 18 2017 hb <herwig.bauernfeind@bitwiseworks.com> 2.0.0-2
- first public version

* Tue Sep 05 2017 hb <herwig.bauernfeind@bitwiseworks.com> 2.0.0-1
- first public version
