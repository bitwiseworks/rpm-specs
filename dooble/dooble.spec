%undefine _debugsource_packages

Name:		dooble
Version:	2022.03.20
Release:	1
Summary:	A colorful Web browser
Group:		System/Libraries
License:	GPLv2
URL:		https://textbrowser.github.io/dooble/
Requires: libstdc++ >= 9.2.0
Requires: libicu >= 68.1
Requires: libcx >= 0.7.2
Requires: os2-base >= 0.0.1-3
%if !0%{?os2_version}
Source0:  U:/rpmbuild/SOURCES/dooble/dooble.pro      
#https://github.com/textbrowser/dooble/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
%else
%scm_source github https://github.com/textbrowser/dooble 2022.02.15
%endif

BuildRequires:	qt5-qtbase-devel
#BuildRequires:  libgcrypt-devel
#BuildRequires:  libgpg-error-devel
#%if !0%{?os2_version}
#BuildRequires:  desktop-file-utils
#%endif
#BuildRequires:  gcc-c++
#BuildRequires:  sqlite-devel

%description
Dooble the finest browser known today.

%build
qmake-qt5 U:/rpmbuild/SOURCES/dooble/dooble.pro -r
#%if !0%{?os2_version}
make
#%else
#make %{?_smp_mflags}
#%endif
lrelease-qt5 U:/rpmbuild/SOURCES/dooble/Translations/*.ts
wrc -bt=os2 -zm -r U:/rpmbuild/SOURCES/dooble/Icons/dooble.rc
wrc -bt=os2 -zm U:/rpmbuild/SOURCES/dooble/Icons/dooble.res Dooble.exe

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cd ../SOURCES/dooble
cp -a Data Dictionaries Documentation dooble.sh Translations %{buildroot}%{_libexecdir}/%{name}
rm %{buildroot}%{_libexecdir}/%{name}/Translations/*.ts
cp Icons/Logo/%{name}.png %{buildroot}%{_libexecdir}/%{name}
mkdir -p %{buildroot}%{_bindir}
cd ../../BUILD
cp -p %{name}.exe %{buildroot}%{_bindir}/
ln -s ../libexec/%{name}/%{name}.sh %{buildroot}%{_bindir}/%{name}
cd ../SOURCES/dooble
install -Dm644 dooble.desktop %{buildroot}%{_datadir}/applications/%{name}.desktop
ln -s %{_libdir}/qt5/plugins/platforms %{buildroot}%{_libexecdir}/%{name}/Lib
cd %{buildroot}%{_libexecdir}/%{name}
rm -rf %{name}.pro Makefile %{name}.doxygen DEBIAN/ Doxygen/ Source/ temp/ Windows/ Translations/*.ts Qt/


%files
%doc U:/rpmbuild/SOURCES/dooble/Documentation/Dooble.html U:\rpmbuild\SOURCES\dooble\Documentation\DOOBLE-LICENSE.html
%{_libexecdir}/%{name}
%if !0%{?os2_version}
%{_datadir}/applications/%{name}.desktop
%{_bindir}/%{name}
%else
%{_bindir}/%{name}.exe
%endif

%post -e
if [ "$1" -ge 1 ]; then # (upon update)
    %wps_object_delete_all
fi
%cube {ADDLINE "SET QTWEBENGINE_CHROMIUM_FLAGS=--single-process" (AFTER "SET "} %%{os2_config_sys} >nul
echo; echo "NOTE:"
echo; echo "The file '%%{os2_config_sys}' has been changed. You need to reboot your"
echo "computer in order to activate these changes."
echo
%wps_object_create_begin
DOOBLE_FOLDER:WPFolder|Dooble Scientific Browser|<WP_DESKTOP>
DOOBLE_EXE:WPProgram|Dooble Browser|<DOOBLE_FOLDER>|EXENAME=((%{_bindir}/dooble.exe))
%wps_object_create_end

%postun
if [ "$1" -eq 0 ]; then # (upon removal)
    %wps_object_delete_all
fi
%cube {DELLINE "SET QTWEBENGINE_CHROMIUM_FLAGS="} %%{os2_config_sys} >nul
echo; echo "NOTE:"
echo; echo "The file '%%{os2_config_sys}' has been changed. You need to reboot your"
echo "computer in order to activate these changes."
echo

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Sun Mar 20 2022 Gregg Young <ygk@qwest.com>
- Initial OS2 release
