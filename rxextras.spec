%define debug_package %{nil}

Summary:    Dion Gillard's RXExtras REXX library
Name:       rxextras
Version:    1.g.0
Release:    2%{?dist}
License:    Freeware
Group:      System/Libraries
URL:        http://www.edm2.com/index.php/OS2_API:RXU
Vendor:     Dave Boll
Source:     %{name}-%{version}.zip
BuildRoot:  %_tmppath/%name-%version-%release-root
Requires:   os2-rpm >= 1-2

%description
RxExtras is a set of functions to enhance OS/2's REXX programming language, 
and is accompanied by additional functions to be used by other PM Rexx-based 
software (VisPro/Rexx and VX-Rexx, among others). Some of the functions 
provided by RxExtras can be accomplished by various other means using "pure" 
OS/2 REXX code, but RxExtras provides an easier interface and more efficient 
processing. 

%prep
%setup -n "%{name}-%{version}" -Tc
unzip -qj %{_sourcedir}/%{name}-%{version}.zip

%build


%install
install -p -m0644 -D rxextras.dll $RPM_BUILD_ROOT%{_libdir}/rxextras.dll
install -p -m0644 -D rxextras.inf $RPM_BUILD_ROOT%{_datadir}/os2/book/rxextras.inf

%clean
rm -rf "$RPM_BUILD_ROOT"

%post
if [ "$1" -ge 1 ]; then # (upon update)
    %wps_object_delete_all
    %{_rpmconfigdir_os2}/wpi4rpm del %{vendor}/%{name}/Library %{version}-%{release}
fi
%global title %{summary}
%{_rpmconfigdir_os2}/wpi4rpm add %{vendor}/%{name}/Library %{version}-%{release}

%postun
if [ "$1" -eq 0 ]; then # (upon removal)
    %wps_object_delete_all
    %{_rpmconfigdir_os2}/wpi4rpm del %{vendor}/%{name}/Library %{version}-%{release}
fi

%files
%defattr(-,root,root,-)
%doc rxextras.cmd rxextras.lib rxextras.mtc vprxx.zip
%_libdir/*.dll
%_datadir/os2/book/*.inf

%changelog
* Wed Sep 05 2018 hb <herwig.bauernfeind@bitwiseworks.com> 1.g.0-2
- fixes to spec files (Silvan Scherrer)

* Sun Feb 05 2017 hb <herwig.bauernfeind@bitwiseworks.com> 1.g.0-1
- final release by Dion Gillard
