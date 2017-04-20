%define debug_package %{nil}

Summary:    User controls for DrDialog
Name:       DrCtl
Version:    0.1.7
Release:    2%{?dist}
License:    BSD 3 Clauses alike
Group:      Applications/System
URL:        http://www.os2world.com/wiki/index.php/DrDialog_Control
Vendor:     Chris Wohlgemuth
Source:     %{name}-%{version}.zip
BuildRoot:  %_tmppath/%name-%version-%release-root
Requires:   wpi4rpm >= 0.9.2

%description
A percent bar (DRD_PERCENTBAR)
A fly overhelp control (DRD_BUBBLEHELP)
New with V01.1.2: An image control (DRD_IMAGE) which displays any image file supported by OS/2.
New with V0.1.2: a directory picker
New with V0.1.5: a histogram control showing the histogram of an image
Some functions are included to set the parent-child relationship between dialogs. 

%prep
%setup -n "%{name}-%{version}" -Tc
unzip -q %{_sourcedir}/%{name}-%{version}.zip

%build


%install
mkdir -p $RPM_BUILD_ROOT%{_libdir}
cp usr/lib/*.dll $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-%{version}
cp usr/share/doc/drctl/readme.txt $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-%{version}

%clean
rm -rf "$RPM_BUILD_ROOT"

%pre
%warpin_conflicts_begin
%{vendor}\%{name}XXX\Library
%warpin_conflicts_end

%post
if [ "$1" -ge 1 ]; then # (upon update)
    %wps_object_delete_all
    wpi4rpm del %{vendor}/%{name}XXX/Library %{version}-%{release}
fi
%wps_object_create_begin
WP_BWWHELP:WPFolder|bww Help|<WP_ASSISTANCE>|TITLE=bitwiseworks Help Center;SHOWALLINTREEVIEW=YES;ICONRESOURCE=60,PMWP.DLL;
%{name}_BWWHELP:WPShadow|Readme|<WP_BWWHELP>|SHADOWID=((%_defaultdocdir/%{name}-%{version}))
%wps_object_create_end
wpi4rpm add %{vendor}/%{name}XXX/Library %{version}-%{release}

%postun
if [ "$1" -eq 0 ]; then # (upon removal)
    %wps_object_delete_all
    wpi4rpm del %{vendor}/%{name}XXX/Library %{version}-%{release}
fi

%files
%defattr(-,root,root,-)
%_defaultdocdir/%{name}-%{version}/readme.txt
%_libdir/*.dll


%changelog
* Tue Feb 07 2017 hb <herwig.bauernfeind@bitwiseworks.com> 0.1.7-2
- bumped release to 2 to be higher than WarpIN
- remove false WPS objects
* Mon Jan 30 2017 hb <herwig.bauernfeind@bitwiseworks.com> 0.1.7-1
- final release from Chris Wohlgemuth
