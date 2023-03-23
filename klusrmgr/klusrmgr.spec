%define debug_package %{nil}
# Disable compression completely
%define _strip_no_compress 1
%global exename klUsrMgr.EXE

Summary:    (kLIBC) User Manager
Name:       klusrmgr
Version:    1.4.5
Release:    1%{?dist}
License:    proprietary
Group:      Applications/System
URL:        https://github.com/bitwiseworks/klusrmgr
Vendor:     bww bitwise works GmbH
Source:     %{name}-%{version}.zip
BuildRoot:  %_tmppath/%name-%version-%release-root
Requires:   os2-rpm >= 1-2
Requires:   rxcrypt >= 1.0.0
Requires:   bww-resources-rpm >= 1.1.0
Requires:   libc >= 1:0.1.2
Obsoletes:  kLIBCum <= 1.0.10

%description
The purpose of this utility is to manage kLIBC users and groups.
These files are found in %UNIXROOT%\etc and have the following names
- master.passwd
- group

These files are syntactically properly maintained and compiled into
pwd.db and spwd.db using the pwd_mkdb.exe utility from libc package.


%prep
%setup -n "%{name}-%{version}" -Tc
unzip -qj %{_sourcedir}/%{name}-%{version}.zip


%build
rexx2vio usermod.cmd usermod.exe
rexx2vio groupmod.cmd groupmod.exe


%install
for f in useradd userdel userren groupadd groupdel *.exe ; do
  install -p -m0755 -D $f $RPM_BUILD_ROOT%{_bindir}/$f
done

# don't change the case of the klusrmgr.exe name
install -p -m0755 -D %{name}.EXE $RPM_BUILD_ROOT%{_bindir}/%{exename}

for f in *.msg ; do
  install -p -m0644 -D $f $RPM_BUILD_ROOT%{_datadir}/os2/lang/$f
done

for f in *.hlp ; do
  install -p -m0644 -D $f $RPM_BUILD_ROOT%{_datadir}/os2/help/$f
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
%bww_app -f %{_bindir}/%{exename} -t %{title} 
%bww_readme -f %{_defaultdocdir}/%{name}-%{version}/readme.txt
%bww_app_shadow 
%bww_app_shadow -d WP_CONFIG
%{_rpmconfigdir_os2}/wpi4rpm add %{vendor}/%{name}/binaries %{version}-%{release}
cmd /c klusrmgr.exe -init
cmd /c groupmod.exe -xx "wheel"

%postun
if [ "$1" -eq 0 ]; then # (upon removal)
    %wps_object_delete_all
    %{_rpmconfigdir_os2}/wpi4rpm del %{vendor}/%{name}/binaries %{version}-%{release}
fi


%files
%defattr(-,root,root,-)
%doc readme.txt
%_bindir/*
%_datadir/os2/lang/*.msg


%changelog
* Thu Mar 23 2023 hb <herwig.bauernfeind@bitwiseworks.com> 1.4.5-1
- Add helpfiles for several languages

* Wed Mar 22 2023 hb <herwig.bauernfeind@bitwiseworks.com> 1.4.4-1
- fix ticket #9 

* Wed Jun 23 2021 hb <herwig.bauernfeind@bitwiseworks.com> 1.4.3-1
- fix error when WarpIN is not present, do not crash

* Tue Jan 5 2021 hb <herwig.bauernfeind@bitwiseworks.com> 1.4.2-1
- add context menu for users and groups pages
- fix error when manipulating groups with numbers below 10
- fix ticket #11 by adding -xx switch for silent removal in usermod
  and groupmod

* Tue Dec 1 2020 hb <herwig.bauernfeind@bitwiseworks.com> 1.4.1-1
- transparently handle /@unixroot/ (both for reading and writing)

* Sun May 10 2020 hb <herwig.bauernfeind@bitwiseworks.com> 1.4.0-1
- Fix vxapps tickets #12 and #13
- Remove "wheel" group upon installation
- Add a refresh timer to the GUI in order to detect externally changed 
  users

* Tue Apr 21 2020 hb <herwig.bauernfeind@bitwiseworks.com> 1.3.2-3
- Repackage with proper zip file

* Tue Apr 14 2020 hb <herwig.bauernfeind@bitwiseworks.com> 1.3.2-2
- Clean fix for uninitiazed groupname. stem variable

* Sun Apr 12 2020 hb <herwig.bauernfeind@bitwiseworks.com> 1.3.2-1
- Testfix for uninitislized groupname variable

* Thu Dec 05 2019 hb <herwig.bauernfeind@bitwiseworks.com> 1.3.1-1
- fix bug when -init was invoked

* Sun Nov 17 2019 hb <herwig.bauernfeind@bitwiseworks.com> 1.3.0-1
- added additional default groups and users
- internal: Addition of group/user manipulation routines without GUI

* Fri Jul 12 2019 hb <herwig.bauernfeind@bitwiseworks.com> 1.2.2-1
- remove pwd_mkdb.exe as in libc now
- added requires of libc

* Tue Sep 04 2018 hb <herwig.bauernfeind@bitwiseworks.com> 1.2.1-1
- useradd and groupmod are compiled into .exe
- standardized error messages in usermod and groupmod

* Thu Aug 09 2018 hb <herwig.bauernfeind@bitwiseworks.com> 1.2.0-1
- add useradd and friend shell scripts as wrapper to usermod/groupmod (Silvan)
- changed usermod and groupmod to accept a lot more options

* Mon Jul 30 2018 hb <herwig.bauernfeind@bitwiseworks.com> 1.1.6-1
- add usermod and groupmod commands from Samba

* Wed Jun 13 2018 hb <herwig.bauernfeind@bitwiseworks.com> 1.1.5-1
- disable potentially dangeraous operations in case Samba User Manager is found

* Fri Jun 8 2018 hb <herwig.bauernfeind@bitwiseworks.com> 1.1.4-3
- make klusrmgr -init workable from rpm (fix by Silvan Scherrer)

* Sun May 27 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.1.4-2
- fix the location of wpi4rpm

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

