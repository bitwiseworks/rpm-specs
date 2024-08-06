Name:           sqlitebrowser
Version:        3.12.2
Release:        1%{?dist}
Summary:        Create, design, and edit SQLite database files

License:        GPLv3+ or MPLv2.0
URL:            https://github.com/%{name}/%{name}
%if !0%{?os2_version}
Source0:        https://github.com/%{name}/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
%else 
%scm_source github https://github.com/Tellie/%{name}-os2 %{version}-os2
%endif
# Unbundle bundled libraries
%if !0%{?os2_version}
Patch0:         sqlitebrowser_unbundle.patch

BuildRequires:  antlr-C++
%endif
BuildRequires:  cmake
%if !0%{?os2_version}
BuildRequires:  desktop-file-utils
%endif
BuildRequires:  gcc-c++
%if !0%{?os2_version}
BuildRequires:  libappstream-glib
%endif
BuildRequires:  make
%if !0%{?os2_version}
BuildRequires:  qcustomplot-qt5-devel
BuildRequires:  qhexedit2-qt5-devel
%endif
BuildRequires:  sqlite-devel
%if !0%{?os2_version}
BuildRequires:  qscintilla-qt5-devel
%endif
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qttools-devel
%if !0%{?os2_version}
Requires:       hicolor-icon-theme
%endif
%description
SQLite Database Browser is a high quality, visual, open source tool to create,
design, and edit database files compatible with SQLite.


%prep
%if !0%{?os2_version}
%autosetup -p1
%else
%scm_setup
%endif
# Unbundle
rm -rf libs/{qcustomplot-source,qhexedit,qscintilla}

%build
%if 0%{?os2_version}
mkdir -p build
cd build
export LDFLAGS="-Zhigh-mem -Zomf -lcx -lpthread"
export CFLAGS="-O2 -g -march=i686"
export CXXFLAGS="-O2 -g -march=i686"
export FFLAGS="-O2 -g -march=i686"
export FCFLAGS="-O2 -g -march=i686"

cmake -DCMAKE_INSTALL_PREFIX:PATH=/@unixroot/usr \
       -DCMAKE_SKIP_RPATH:BOOL=YES \
       -DCMAKE_BUILD_TYPE=Release \
       -DOS2_USE_CXX_EMXEXP=ON \
       -DBUILD_STABLE_VERSION=1  \
       -DENABLE_TESTING=ON \
       -Wno-dev .. 
%endif

%if !0%{?os2_version}
%cmake \
    -DUSE_QT5=1 \
    -DENABLE_TESTING=1 \
    -DFORCE_INTERNAL_QCUSTOMPLOT=OFF \
    -DFORCE_INTERNAL_QHEXEDIT=OFF \
    -DQT_INCLUDE_DIR=%{_includedir}/qt5 \
   ..
%endif

%if !0%{?os2_version}
%cmake_build
%else
make %{?_smp_mflags}
%endif

%install
%if !0%{?os2_version}
%cmake_install
%{_bindir}/appstream-util validate-relax --nonet %{buildroot}%{_datadir}/metainfo/%{name}.desktop.appdata.xml
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
%else
make DESTDIR=$RPM_BUILD_ROOT -C build install
install -Dm 0644 src/icons/%{name}.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/sqlitebrowser.png
%endif

%check
%if !0%{?os2_version}
%ctest
%endif

%files
%license LICENSE
%doc README.md
%if !0%{?os2_version}
%{_bindir}/%{name}
%{_datadir}/metainfo/%{name}.desktop.appdata.xml
%{_datadir}/applications/%{name}.desktop
%else
%{_bindir}/%{name}.exe
%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
%endif

%changelog
* Sat May 15 2021 Elbert Pol <elbert.pol@gmail.com> - 3.12.2-1
- First RPM for OS2 v3.12.2
