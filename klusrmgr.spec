%define debug_package %{nil}

Summary:    kLIBC User Management
Name:       klusrmgr
Version:    1.1.3
Release:    2%{?dist}
License:    proprietary
Group:      Applications/System
URL:        http://www.netlabs.org/vxapps
Vendor:     bww bitwise works GmbH
Source:     %{name}-%{version}.zip
BuildRoot:  %_tmppath/%name-%version-%release-root
Requires:   wpi4rpm >= 0.9.2
Requires:   rxcrypt >= 1.0.0
Requires:   bww-resources-rpm >= 1.1.0
Obsoletes:  kLIBCum <= 1.0.10

%description
The purpose of this utility is to manage kLIBC users and groups.
These files are found in %UNIXROOT%\etc and have the following names
- master.passwd
- group

These files are syntactically properly maintained and compiled into
pwd.db and spwd.db using the pwdmkdb.exe utility.


%prep
%setup -n "%{name}-%{version}" -Tc
unzip -q %{_sourcedir}/%{name}-%{version}.zip

%build


%install
mkdir -p $RPM_BUILD_ROOT%{_bindir}
cp usr/bin/*.exe $RPM_BUILD_ROOT%{_bindir}
cp usr/bin/*.EXE $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-%{version}
cp usr/share/doc/klusrmgr/readme.txt $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-%{version}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/os2/lang
cp usr/share/os2/lang/*.msg $RPM_BUILD_ROOT%{_datadir}/os2/lang


%clean
rm -rf "$RPM_BUILD_ROOT"

%post
if [ "$1" -ge 1 ]; then # (upon update)
    %wps_object_delete_all
    wpi4rpm del %{vendor}/%{name}/binaries %{version}-%{release}
fi
%global title %{summary}
%bww_folder -t %{title}
%bww_app -f %{_bindir}/%{name}.exe -t %{title} 
%bww_readme -f %{_defaultdocdir}/%{name}-%{version}/readme.txt
%bww_app_shadow -t %{title}
%bww_app_shadow -t %{title} -d WP_CONFIG
wpi4rpm add %{vendor}/%{name}/binaries %{version}-%{release}
klusrmgr -init

%postun
if [ "$1" -eq 0 ]; then # (upon removal)
    %wps_object_delete_all
    wpi4rpm del %{vendor}/%{name}/binaries %{version}-%{release}
fi

%files
%defattr(-,root,root,-)
%_defaultdocdir/%{name}-%{version}/readme.txt
%_bindir/*.exe
%_bindir/*.EXE
%_datadir/os2/lang/*.msg


%changelog
* Tue Dec 12 2017 hb <herwig.bauernfeind@bitwiseworks.com> 1.1.3-1
- fix -init switch and repair structural bugs and omission introduced by 1.1.x

* Thu Jun 08 2017 hb <herwig.bauernfeind@bitwiseworks.com> 1.1.2-1
- add root group with GID 0 as a default group
- fix several small bugs

* Mon Apr 24 2017 hb <herwig.bauernfeind@bitwiseworks.com> 1.1.1-1
- add -init switch and ensure default files are created upon installation

* Sun Feb 05 2017 hb <herwig.bauernfeind@bitwiseworks.com> 1.1.0-3
- put RxCrypt.DLL into a separate package

* Thu Jan 26 2017 hb <herwig.bauernfeind@bitwiseworks.com> 1.1.0-2
- renamed to klusrmgr
- added support for shell
- completely rewrote user properties dialogue

* Fri Nov 18 2016 hb <herwig.bauernfeind@bitwiseworks.com> 1.0.10
- fix Ticket #7
- fix minor bugs in user properties page
- rework and simplify join/leave dialogue

* Thu Nov 17 2016 hb <herwig.bauernfeind@bitwiseworks.com> 1.0.9-2
- fix minor bug 

* Thu Nov 17 2016 hb <herwig.bauernfeind@bitwiseworks.com> 1.0.9
- Limited group editing
- bigger buttons, new icons
- fix Ticket #125 (Unix ports)
- fix new user bug
- add ignore root shell error warning
- make debug stick across sessions

* Tue Nov 15 2016 hb <herwig.bauernfeind@bitwiseworks.com> 1.0.8
- add functionality to add/remove multiple user from/to groups
- double click on user open user properties to edit

* Fri Nov 11 2016 hb <herwig.bauernfeind@bitwiseworks.com> 1.0.7-2
- fix minor bug 

* Fri Nov 11 2016 hb <herwig.bauernfeind@bitwiseworks.com> 1.0.7-1
- Add smbusers.exe check, fix missing NLV translations, 
- add NL, IT and RU language files

* Thu Nov 10 2016 hb <herwig.bauernfeind@bitwiseworks.com> 1.0.6-1
- Add "Remove user from group" functionality, fix missing NLV translations

* Fri Nov 04 2016 hb <herwig.bauernfeind@bitwiseworks.com> 1.0.5-1
- Add some hints, fix wrong hints

* Thu Oct 27 2016 hb <herwig.bauernfeind@bitwiseworks.com> 1.0.4-1
- bigger buttons, shortened strings for EN, ES

* Mon Oct 24 2016 scs <silvan.scherrer@bitwiseworks.com> 1.0.3-1
- first public version

