%define debug_package %{nil}

Summary:	kLIBC User Management
Name:		kLIBCum
Version:	1.0.9
Release:	2%{?dist}
License:	proprietary
Group:		Applications/System
URL:		http://www.netlabs.org/vxapps
Vendor:		bww bitwise works GmbH

Source:		%{name}-%{version}.zip
BuildRoot:	%_tmppath/%name-%version-%release-root


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
mkdir -p $RPM_BUILD_ROOT%{_libdir}
cp usr/lib/*.dll $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-%{version}
cp usr/share/doc/klibcum/readme.txt $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-%{version}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/os2/lang
cp usr/share/os2/lang/*.msg $RPM_BUILD_ROOT%{_datadir}/os2/lang


%clean
rm -rf "$RPM_BUILD_ROOT"

%post
if [ "$1" -ge 1 ]; then # (upon update)
    %wps_object_delete_all
fi
%wps_object_create_begin
KLIBCUM_FOLDER:WPFolder|kLIBCum|<WP_DESKTOP>|TITLE=kLIBC User Management;
KLIBCUM_README:WPShadow|Readme|<KLIBCUM_FOLDER>|SHADOWID=((%_defaultdocdir/%{name}-%{version}/readme.txt))
KLIBCUM_EXE:WPProgram|User Management|<KLIBCUM_FOLDER>|EXENAME=((%_bindir/klibcum.exe));STARTUPDIR=((%_bindir));TITLE=User Management;
%wps_object_create_end

%postun
if [ "$1" -eq 0 ]; then # (upon removal)
    %wps_object_delete_all
fi

%files
%defattr(-,root,root,-)
%_defaultdocdir/%{name}-%{version}/readme.txt
%_bindir/*.exe
%_bindir/*.EXE
%_libdir/*.dll
%_datadir/os2/lang/*.msg


%changelog
* Fri Nov 17 2016 hb <herwig.bauernfeind@bitwiseworks.com> 1.0.9-2
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
* Mon Oct 24 2016 yd <silvan.scherrer@bitwiseworks.com> 1.0.3-1
- first public version
