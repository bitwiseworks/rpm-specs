%global commit a302128d2e23984501ed0a77413594ad440eddde
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           sqlitebrowser
Version:        3.13.0
%if !0%{?os2_version}
Release:        0.8%{?commit:.git%{shortcommit}}%{?dist}
%else
Release:        2%{?dist}
%endif
%if 0%{?os2_version}
Vendor:        TeLLie OS2 forever
Distribution:  OS/2
Packager:      TeLLie
%endif 
Summary:        Create, design, and edit SQLite database files

License:        GPL-3.0-or-later OR MPL-2.0
URL:            https://github.com/%{name}/%{name}
%if !0%{?os2_version}
%if 0%{?commit:1}
Source0:        https://github.com/%{name}/%{name}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        https://github.com/%{name}/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
%endif
%else
%scm_source github https://github.com/Tellie/sqlitebrowser-os2 %{version}-os2-1
%endif

%if !0%{?os2_version}
# Unbundle bundled libraries
Patch0:         sqlitebrowser_unbundle.patch

BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  sqlcipher-devel
BuildRequires:  qcustomplot-qt5-devel
BuildRequires:  qhexedit2-qt5-devel
BuildRequires:  qscintilla-qt5-devel
%else
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qttools-devel
%endif

%if !0%{?os2_version}
Requires:       hicolor-icon-theme
%endif

%description
SQLite Database Browser is a high quality, visual, open source tool to create,
design, and edit database files compatible with SQLite.


%prep
%if !0%{?os2_version}
%if 0%{?commit:1}
%autosetup -p1 -n %{name}-%{commit}
%else
%autosetup -p1 -n %{name}-%{version}
%endif
%else
%scm_setup
%endif

# Unbundle
%if !0%{?os2_version}
rm -rf libs/{qcustomplot-source,qhexedit,qscintilla}
# add sqlcipher to include path
sed -i 's@^\(\s*\)set(LIBSQLITE_NAME sqlcipher)@&\n\1include_directories(%{_prefix}/include/sqlcipher)@' CMakeLists.txt
%endif

%build
%if !0%{?os2_version}
%cmake \
    -DBUILD_SHARED_LIBS=OFF \
    -DENABLE_TESTING=1 \
    -DFORCE_INTERNAL_QCUSTOMPLOT=OFF \
    -DFORCE_INTERNAL_QHEXEDIT=OFF \
    -DQSCINTILLA_INCLUDE_DIR=%{_qt5_includedir} \
    -DQSCINTILLA_LIBRARY=%{_libdir}/libqscintilla2_qt5.so \
    -Dsqlcipher=1
%else
%cmake \
    -DBUILD_SHARED_LIBS=OFF \
    -DENABLE_TESTING=1 \
    -DFORCE_INTERNAL_QCUSTOMPLOT=ON \
    -DFORCE_INTERNAL_QHEXEDIT=ON \
    -DQSCINTILLA_INCLUDE_DIR=%{_qt5_includedir} \
    -DQSCINTILLA_LIBRARY=%{_libdir}/qscintilla2.a \
    -Dsqlcipher=0
%endif

%cmake_build

%install
%cmake_install
%if 0%{?os2_version}     
mkdir -p %{buildroot}%{_datadir}/os2/icons/
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/
cp -a src/%{name}.ico %{buildroot}%{_datadir}/os2/icons/%{name}.ico
cp -a src/icons/%{name}.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
%endif
%if !0%{?os2_version}
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/metainfo/%{name}.desktop.appdata.xml
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
%endif

%check
%ctest -V

%files
%license LICENSE
%doc README.md  
%if !0%{?os2_version}
%{_bindir}/%{name}
%{_datadir}/metainfo/%{name}.desktop.appdata.xml
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%else
%doc CHANGELOG.md README-OS2.txt BUILDING.md
%{_bindir}/%{name}.exe
%{_datadir}/os2/icons/%{name}.ico
%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
%endif

%if 0%{?os2_version}
%global wps_folder_title Sqlitebrowser

%post -e
if [ "$1" -ge 1 ]; then # (upon update)
    %wps_object_delete_all
fi
%global wps_app_title Sqlitebrowser
%bww_folder -t %{wps_folder_title}
%bww_app -f %{_bindir}/%{name}.exe -t %{wps_app_title} -i ${name}.ico
%bww_app_shadow
%bww_file BUILDING.md -f %_defaultdocdir/%{name}-%{version}/BUILDING.md
%bww_file CHANGELOG.md -f %_defaultdocdir/%{name}-%{version}/CHANGELOG.md
%bww_file README-OS2.txt -f %_defaultdocdir/%{name}-%{version}/README-os2.txt
%bww_file README.md -f %_defaultdocdir/%{name}-%{version}/README.md

%postun
if [ "$1" -eq 0 ]; then # (upon removal)
    %wps_object_delete_all
fi
%endif


%changelog
* Wed Aug 07 2024 Elbert Pol <elbert.pol@gmail.com> -3.13.0-2
- Update some changes that where not ok.
- Remove wrc and do it the probper way in cmakelists

* Tue Aug 06 2024 Elbert Pol <elbert.pol@gmail.com> -3.13.0-1
- Updated to latest version
- Add icon and a wps map

* Sat May 15 2021 Elbert Pol <elbert.pol@gmail.com> - 3.12.2-1
- First RPM for OS2 v3.12.2
