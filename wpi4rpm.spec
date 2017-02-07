%define debug_package %{nil}
%define _strip_opts --no-compress --no-debuginfo

Summary:	WarpIN package entry for rpms
Name:		wpi4rpm
Version:	0.9.5
Release:	1%{?dist}
License:	proprietary
Group:		Applications/System
URL:		http://trac.netlabs.org/rpm
Vendor:		bww bitwise works GmbH
Source:		%{name}-%{version}.zip
BuildRequires: rexx_exe
BuildRoot:	%_tmppath/%name-%version-%release-root

%description
The purpose of this utility is to create fake WarpIN database entries
for rpm/yum packages.

%prep
%setup -n "%{name}-%{version}" -Tc
unzip -q %{_sourcedir}/%{name}-%{version}.zip

%build

%install
mkdir -p $RPM_BUILD_ROOT%{_bindir}
rexx2vio wpi4rpm.cmd $RPM_BUILD_ROOT%{_bindir}/wpi4rpm.exe
mkdir -p $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-%{version}
cp readme.txt $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-%{version}

%clean
rm -rf "$RPM_BUILD_ROOT"

%files
%defattr(-,root,root,-)
%_defaultdocdir/%{name}-%{version}/readme.txt
%_bindir/*.exe

%changelog
* Tue Feb 07 2017 hb <herwig.bauernfeind@bitwiseworks.com> 0.9.5-1
- Dummy path changed to DEV\NULL 
  (prevents WarpIN from "updating" a fake package).
- Make it quiet (but support VERBOSE=bla env var).
* Thu Feb 02 2017 hb <herwig.bauernfeind@bitwiseworks.com> 0.9.4-1
- Write proper install date/time
- Fix cosmetic error on package removal
* Mon Jan 30 2017 hb <herwig.bauernfeind@bitwiseworks.com> 0.9.3-1
- Add errorhandler
- Allow all kind of help switches
* Sat Jan 28 2017 hb <herwig.bauernfeind@bitwiseworks.com> 0.9.2-1
- Add support for vendor and package
* Fri Jan 27 2017 hb <herwig.bauernfeind@bitwiseworks.com> 0.9.1-1
- Initial release
* Thu Jan 26 2017 hb <herwig.bauernfeind@bitwiseworks.com> 0.9.0-1
- Initial working model
