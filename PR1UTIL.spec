%define debug_package %{nil}

Summary:    Paul Ratcliffe's PR1UTIL library
Name:       PR1UTIL
Version:    1.6.5
Release:    1%{?dist}
License:    Freeware
Group:      Applications/System
URL:        http://home.clara.net/orac/os2.htm
Vendor:     Paul Ratcliffe
Source:     %{name}-%{version}.zip
BuildRoot:  %_tmppath/%name-%version-%release-root
Requires:   wpi4rpm >= 0.9.2

%description
PR1UTIL is a REXX library of miscellaneous functions. It uses TCP/IP
libraries and thus requires TCP/IP to be installed. The program is freeware
and as such USE OF THIS PROGRAM IS ENTIRELY AT YOUR OWN RISK.

%prep
%setup -n "%{name}-%{version}" -Tc
unzip -q %{_sourcedir}/%{name}-%{version}.zip

%build


%install
mkdir -p $RPM_BUILD_ROOT%{_libdir}
cp usr/lib/*.dll $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-%{version}
cp usr/share/doc/pr1util/* $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-%{version}

%clean
rm -rf "$RPM_BUILD_ROOT"

%post
if [ "$1" -ge 1 ]; then # (upon update)
    %wps_object_delete_all
    wpi4rpm del %{vendor}/Pr1Util/Library %{version}-%{release}
fi
%wps_object_create_begin
WP_BWWHELP:WPFolder|bww Help|<WP_ASSISTANCE>|TITLE=bitwiseworks Help Center;SHOWALLINTREEVIEW=YES;ICONRESOURCE=60,PMWP.DLL;
%{name}_BWWHELP:WPShadow|Readme|<WP_BWWHELP>|SHADOWID=((%_defaultdocdir/%{name}-%{version}))
%wps_object_create_end
wpi4rpm add %{vendor}/Pr1Util/Library %{version}-%{release}


%postun
if [ "$1" -eq 0 ]; then # (upon removal)
    %wps_object_delete_all
    wpi4rpm del %{vendor}/Pr1Util/Library %{version}-%{release}
fi

%files
%defattr(-,root,root,-)
%_defaultdocdir/%{name}-%{version}/*
%_libdir/*.dll


%changelog
* Sun Feb 05 2017 hb <herwig.bauernfeind@bitwiseworks.com> 1.6.5-1
- final release from Paul Ratcliffe
