%define debug_package %{nil}

Summary:    Dion Gillard's RXExtras REXX library
Name:       rxextras
Version:    1.g.0
Release:    1%{?dist}
License:    Freeware
Group:      System/Libraries
URL:        http://www.edm2.com/index.php/OS2_API:RXU
Vendor:     Dave Boll
Source:     %{name}-%{version}.zip
BuildRoot:  %_tmppath/%name-%version-%release-root
Requires:   wpi4rpm >= 0.9.2

%description
RxExtras is a set of functions to enhance OS/2's REXX programming language, 
and is accompanied by additional functions to be used by other PM Rexx-based 
software (VisPro/Rexx and VX-Rexx, among others). Some of the functions 
provided by RxExtras can be accomplished by various other means using "pure" 
OS/2 REXX code, but RxExtras provides an easier interface and more efficient 
processing. 

%prep
%setup -n "%{name}-%{version}" -Tc
unzip -q %{_sourcedir}/%{name}-%{version}.zip

%build


%install
mkdir -p $RPM_BUILD_ROOT%{_libdir}
cp usr/lib/*.dll $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-%{version}
cp usr/share/doc/rxextras/* $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-%{version}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/os2/book
cp usr/share/os2/book/*.inf $RPM_BUILD_ROOT%{_datadir}/os2/book

%clean
rm -rf "$RPM_BUILD_ROOT"

%post
if [ "$1" -ge 1 ]; then # (upon update)
    %wps_object_delete_all
    wpi4rpm del %{vendor}/%{name}/Library %{version}-%{release}
fi
%global title %{summary}
wpi4rpm add %{vendor}/%{name}/Library %{version}-%{release}

%postun
if [ "$1" -eq 0 ]; then # (upon removal)
    %wps_object_delete_all
    wpi4rpm del %{vendor}/%{name}/Library %{version}-%{release}
fi

%files
%defattr(-,root,root,-)
%_defaultdocdir/%{name}-%{version}/*
%_libdir/*.dll
%_datadir/os2/book/*.inf

%changelog
* Sun Feb 05 2017 hb <herwig.bauernfeind@bitwiseworks.com> 1.g.0-1
- final release by Dion Gillard
