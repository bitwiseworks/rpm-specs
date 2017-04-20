%define debug_package %{nil}

Summary:    Steven Elliott's REXXINI library
Name:       REXXINI
Version:    1.0.0
Release:    1%{?dist}
License:    Freeware
Group:      Applications/System
URL:        http://www.edm2.com/index.php/RexxINI
Vendor:     Steven Elliott
Source:     %{name}-%{version}.zip
BuildRoot:  %_tmppath/%name-%version-%release-root
Requires:   wpi4rpm >= 0.9.2

%description
Rexx API's for manipulation of Text Based INI Files (used by Samba and WINOS2)
Useful for manipulating and fixing text ini files used by Samba, DOS and windows programs


%prep
%setup -n "%{name}-%{version}" -Tc
unzip -q %{_sourcedir}/%{name}-%{version}.zip

%build


%install
mkdir -p $RPM_BUILD_ROOT%{_libdir}
cp usr/lib/*.dll $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-%{version}
cp usr/share/doc/rexxini/* $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-%{version}

%clean
rm -rf "$RPM_BUILD_ROOT"

%post
if [ "$1" -ge 1 ]; then # (upon update)
    %wps_object_delete_all
    wpi4rpm del Steven Elliot/REXXIni/Library %{version}-%{release}
fi
%wps_object_create_begin
WP_BWWHELP:WPFolder|bww Help|<WP_ASSISTANCE>|TITLE=bitwiseworks Help Center;SHOWALLINTREEVIEW=YES;ICONRESOURCE=60,PMWP.DLL;
%{name}_BWWHELP:WPShadow|Readme|<WP_BWWHELP>|SHADOWID=((%_defaultdocdir/%{name}-%{version}))
%wps_object_create_end
wpi4rpm add Steven Elliot/REXXIni/Library %{version}-%{release}


%postun
if [ "$1" -eq 0 ]; then # (upon removal)
    %wps_object_delete_all
    wpi4rpm del Steven Elliot/REXXIni/Library %{version}-%{release}
fi

%files
%defattr(-,root,root,-)
%_defaultdocdir/%{name}-%{version}/*
%_libdir/*.dll


%changelog
* Sun Feb 05 2017 hb <herwig.bauernfeind@bitwiseworks.com> 1.0.0-1
- final release from Steven Elliott


