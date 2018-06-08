%define debug_package %{nil}
# Disable compression completely
%define _strip_no_compress 1

Summary:    kLIBC User Management
Name:       klusrmgr
Version:    1.1.4
Release:    2%{?dist}
License:    proprietary
Group:      Applications/System
URL:        http://www.netlabs.org/vxapps
Vendor:     bww bitwise works GmbH
Source:     %{name}-%{version}.zip
BuildRoot:  %_tmppath/%name-%version-%release-root
Requires:   os2-rpm >= 1-2
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
for f in *.exe *.EXE ; do
  install -p -m0755 -D $f  $RPM_BUILD_ROOT%{_bindir}/$f
done
for f in readme.txt ; do
  install -p -m0644 -D $f  $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-%{version}/$f
done
for f in *.msg ; do
  install -p -m0644 -D $f  $RPM_BUILD_ROOT%{_datadir}/os2/lang/$f
done


%clean
rm -rf "$RPM_BUILD_ROOT"

%post
if [ "$1" -ge 1 ]; then # (upon update)
    %wps_object_delete_all
    %{_rpmconfigdir_os2}/wpi4rpm del %{vendor}/%{name}/binaries %{version}-%{release}
fi
%global title %{summary}
%bww_folder -t %{title}
%bww_app -f %{_bindir}/%{name}.exe -t %{title} 
%bww_readme -f %{_defaultdocdir}/%{name}-%{version}/readme.txt
%bww_app_shadow 
%bww_app_shadow -d WP_CONFIG
%{_rpmconfigdir_os2}/wpi4rpm add %{vendor}/%{name}/binaries %{version}-%{release}
cmd /c klusrmgr.exe -init

%postun
if [ "$1" -eq 0 ]; then # (upon removal)
    %wps_object_delete_all
    %{_rpmconfigdir_os2}/wpi4rpm del %{vendor}/%{name}/binaries %{version}-%{release}
fi

%files
%defattr(-,root,root,-)
%_defaultdocdir/%{name}-%{version}/readme.txt
%_bindir/*.exe
%_bindir/*.EXE
%_datadir/os2/lang/*.msg


%changelog
* Sun May 27 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.1.4-2
- fix the location of wpi4rpm
- make klusrmgr -init workable from rpm

* Tue Feb 06 2018 hb <herwig.bauernfeind@bitwiseworks.com> 1.1.4-1
- Fix: Missing msgs from 1.1.x sometimes did not work
- Fix: Tab order on user page
- Fix: Verify if passwords match also for new users

* Tue Dec 12 2017 hb <herwig.bauernfeind@bitwiseworks.com> 1.1.3-2
- fix buglet in package creation

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

