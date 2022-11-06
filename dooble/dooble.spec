%undefine _debugsource_packages

Name:		dooble
Version:	2022.10.15
Release:	1%{?dist}
Summary:	Free and opensource Web browser
Group:		System/Libraries
License:	GPLv2
URL:		https://textbrowser.github.io/dooble/
%if !0%{?os2_version}
Source0:    https://github.com/textbrowser/dooble/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
%else
%scm_source github https://github.com/bitwiseworks/%{name}-os2 %{version}-os2
#scm_source git file://D:/Coding/%{name}/main 5040150
%endif

%if 0%{os2_version}
Vendor:         bww bitwise works GmbH

Source100:      %{name}-os2.ico
Source101:      %{name}-os2.rc

# For scm macros
BuildRequires:  curl zip

# for WPS macros
BuildRequires:  bww-resources-rpm-build
Requires:       bww-resources-rpm
%endif

BuildRequires:  make gcc-c++
BuildRequires:	qt5-qtbase-devel
BuildRequires:  qt5-qtwebengine-devel
#BuildRequires:  libgcrypt-devel
#BuildRequires:  libgpg-error-devel
#BuildRequires:  desktop-file-utils
#BuildRequires:  sqlite-devel

%description
Dooble the finest browser known today.

%debug_package

%prep
%if 0%{?os2_version}
%scm_setup
cp -a %{SOURCE100} %{SOURCE101} .
%else
%setup -q -n %{name}-%{version}/2.x
sed -i 's|/usr/local|/usr/libexec|g' dooble.desktop dooble.sh Qt/qt.conf
sed -i '10i export QT_QPA_PLATFORM_PLUGIN_PATH=%{_libdir}/qt5/plugins/platforms' dooble.sh
sed -i '1i #include <QWebEngineCertificateError>' Source/dooble_web_engine_page.cc
sed -i 's|-Werror||' %{name}.pro
%endif

%build
qmake-qt5 dooble.pro
make %{?_smp_mflags}
#lrelease-qt5 Translations/*.ts
%if 0%{?os2_version}
wrc -bt=os2 -zm -r %{name}-os2.rc
wrc -bt=os2 -zm %{name}-os2.res %{name}.exe
%endif

%install
rm -rf %{buildroot}
%if !0%{?os2_version}
# Looks like these are not needed in proper RPM environment (needs checking)
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a Data Dictionaries Documentation Dooble dooble.sh qwebengine_dictionaries Translations %{buildroot}%{_libexecdir}/%{name}
rm %{buildroot}%{_libexecdir}/%{name}/Translations/*.ts
cp Icons/Logo/%{name}.png %{buildroot}%{_libexecdir}/%{name}
mkdir -p %{buildroot}%{_bindir}
ln -s ../libexec/%{name}/%{name}.sh %{buildroot}%{_bindir}/%{name}
install -Dm644 dooble.desktop %{buildroot}%{_datadir}/applications/%{name}.desktop
ln -s %{_libdir}/qt5/plugins/platforms %{buildroot}%{_libexecdir}/%{name}/Lib
%else
mkdir -p %{buildroot}%{_datadir}/%{name}/Translations
cp -a Translations/dooble_*.qm %{buildroot}%{_datadir}/%{name}/Translations
mkdir -p %{buildroot}%{_bindir}
cp -a %{name}.exe %{buildroot}%{_bindir}/
mkdir -p %{buildroot}%{_datadir}/os2/icons/
cp -a %{name}-os2.ico %{buildroot}%{_datadir}/os2/icons/%{name}.ico
%endif
#cd %{buildroot}%{_libexecdir}/%{name}
#rm -rf %{name}.pro Makefile %{name}.doxygen DEBIAN/ Doxygen/ Source/ temp/ Windows/ Translations/*.ts Qt/

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{debug_package_exclude_files}
%doc README Documentation/TO-DO README-os2.txt CHANGES-os2.txt
%license LICENSE
%if 0%{?os2_version}
%{_bindir}/%{name}.exe
%{_datadir}/%{name}/Translations
%{_datadir}/os2/icons/%{name}.ico
%else
%{_libexecdir}/%{name}
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%endif

%if 0%{?os2_version}
%global wps_folder_title Dooble

%post -e
if [ "$1" -ge 1 ]; then # (upon update)
    %wps_object_delete_all
fi
%global wps_app_title Dooble
%bww_folder -t %{wps_folder_title}
%bww_app -f %{_bindir}/%{name}.exe -t %{wps_app_title} -i ${name}.ico
%bww_app_shadow
%bww_readme -f %_defaultdocdir/%{name}-%{version}/README
%bww_license -f %_defaultlicensedir/%{name}-%{version}/LICENSE
%bww_file TODO -f %_defaultdocdir/%{name}-%{version}/TO-DO
%bww_file README_OS2 -f %_defaultdocdir/%{name}-%{version}/README-os2.txt
%bww_file CHANGES_OS2 -f %_defaultdocdir/%{name}-%{version}/CHANGES-os2.txt

%postun
if [ "$1" -eq 0 ]; then # (upon removal)
    %wps_object_delete_all
fi
%endif

%changelog
* Sun Nov 06 2022 Dmitriy Kuminov <coding@dmik.org> 2022.10.15-1
- Release new version (see CHANGES-os2.txt for details).
- Install Translation files.

* Sun Apr 24 2022 Dmitriy Kuminov <coding@dmik.org> 2022.04.04-1
- Update source to build 2022.04.04.
- Make it build from bww repo using scm macros.
- Create standard BWW folders with app exe and readmes.
- Add debuginfo package.
- Remove CONFIG.SYS change (to be done by a separate RPM).
- Cleanup and comment out non-OS/2 stuff.

* Sun Mar 20 2022 Gregg Young <ygk@qwest.com> 2022.03.20-1
- Initial OS2 release
