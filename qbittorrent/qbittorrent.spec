%if 0%{?fedora} >= 38
%ifnarch s390x
%global _with_qt6 1
%global _qtver Qt6
%else
%global _qtver Qt5
%endif
%else
%global _qtver Qt5
%endif
# Use old cmake macro
%global __cmake_in_source_build 1

%if 0%{?os2_version}
%global wps_folder_title The qBittorrent BitTorrent client
%endif

Name:    qbittorrent
Summary: A Bittorrent Client
Epoch:   1
Version: 4.6.7
Release: 2%{?dist}
# Automatically converted from old format: GPLv2+ - review is highly recommended.
License: GPL-2.0-or-later
URL:     https://www.qbittorrent.org

%if !0%{?os2_version}
Source0: https://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.xz
Source1: https://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.xz.asc
Source2: https://github.com/qbittorrent/qBittorrent/raw/master/5B7CC9A2.asc
Source3: qbittorrent-nox.README

ExcludeArch:   %{ix86}
%else
Vendor:  bww bitwise works GmbH
%scm_source github http://github.com/bitwiseworks/%{name}-os2 release-%{version}-os2
%endif

BuildRequires: cmake
BuildRequires: gcc-c++
%if !0%{?os2_version}
BuildRequires: gnupg2
BuildRequires: ninja-build
BuildRequires: systemd
%endif
%if 0%{?_with_qt6}
BuildRequires: cmake(Qt6Core)
BuildRequires: cmake(Qt6Gui)
BuildRequires: cmake(Qt6Svg)
BuildRequires: cmake(Qt6LinguistTools)
BuildRequires: libxkbcommon-devel
BuildRequires: qt6-qtbase-private-devel
BuildRequires: qt6-linguist
%else
BuildRequires: cmake(Qt5Core)
BuildRequires: cmake(Qt5Gui)
BuildRequires: cmake(Qt5Svg)
BuildRequires: qt5-qtbase-private-devel
BuildRequires: qt5-linguist
%endif
BuildRequires: rb_libtorrent-devel >= 1.2.12
%if !0%{?os2_version}
BuildRequires: desktop-file-utils
BuildRequires: boost-devel >= 1.60
BuildRequires: libappstream-glib
%endif
BuildRequires: openssl-devel-engine
%if !0%{?os2_version}
BuildRequires: zlib-ng-compat-static
%else
BuildRequires: zlib
%endif

Requires: python3
%if 0%{?_with_qt6}
%if !0%{?os2_version}
Recommends: (qgnomeplatform-qt6%{?_isa} if gnome-shell)
Recommends: (qgnomeplatform-qt6%{?_isa} if cinnamon)
Requires:   qt6-qtsvg%{?_isa}
%endif
%else
%if !0%{?os2_version}
Recommends: (qgnomeplatform-qt5%{?_isa} if gnome-shell)
Recommends: (qgnomeplatform-qt5%{?_isa} if cinnamon)
%endif
Requires:   qt5-qtsvg%{?_isa}
%endif

%description
A Bittorrent client using rb_libtorrent and a %{_qtver} Graphical User Interface.
It aims to be as fast as possible and to provide multi-OS, unicode support.

%if !0%{?os2_version}
%package nox
Summary: A Headless Bittorrent Client

%description nox
A Headless Bittorrent client using rb_libtorrent.
It aims to be as fast as possible and to provide multi-OS, unicode support.
%endif

%if 0%{?os2_version}
%debug_package
%endif

%prep
%if !0%{?os2_version}
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup
cp %{SOURCE3} .
%else
%scm_setup
%endif

%build
%if 0%{?os2_version}
# -------------------------
# this is hackisch and works only on my env. you need to adjust that until we have a
# boost rpm. when we have a boost rpm, then enable all boost stuff in here!!!
export BOOST_CPPFLAGS="-IE:/Trees/boost/git"
export BOOST_ROOT="E:/Trees/boost/git"
export BOOST_LDFLAGS="-LE:/Trees/boost/git/stage/lib"
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"
export VENDOR="%{vendor}"
%endif
%if !0%{?os2_version}
mkdir build-nox
pushd build-nox
%cmake \
 -DSYSTEMD=ON \
 -Wno-dev \
 -GNinja \
%if 0%{?_with_qt6}
 -DQT6=ON \
%endif
 -DGUI=OFF \
 ..
%cmake_build
popd
%endif

# Build gui version
mkdir build
%if !0%{?os2_version}
pushd build
%else
cd build
%endif
%cmake \
 -Wno-dev \
%if 0%{?_with_qt6}
 -DQT6=ON \
%endif
%if !0%{?os2_version}
 -GNinja \
%endif
%if 0%{?os2_version}
 -DSTACKTRACE=OFF \
%endif
 ..
%cmake_build
%if !0%{?os2_version}
popd
%else
cd ..
%endif

%install
%if !0%{?os2_version}
# install headless version
pushd build-nox
%cmake_install
popd
%endif

# install gui version
%if !0%{?os2_version}
pushd build
%else
cd build
%endif
%cmake_install
%if !0%{?os2_version}
popd
%else
cd ..
%endif

%if !0%{?os2_version}
desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications/ \
  %{buildroot}%{_datadir}/applications/org.qbittorrent.qBittorrent.desktop

appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/org.qbittorrent.qBittorrent.metainfo.xml
%endif

%if 0%{?os2_version}
%post
if [ "$1" -ge 1 ]; then # (upon update)
    %wps_object_delete_all
fi
# for the definition of the parameters see macros.bww
%bww_folder -t %{quote:%{wps_folder_title}}
%bww_app -f %{_bindir}/%{name}.exe -t %{quote:%{wps_folder_title}} -a *.torrent
%bww_app_shadow
%bww_readme -f %_defaultdocdir/%{name}/README.md

%postun
if [ "$1" -eq 0 ]; then # (upon removal)
    %wps_object_delete_all
fi
%endif

%files
%license COPYING
%doc README.md AUTHORS Changelog
%if !0%{?os2_version}
%{_bindir}/qbittorrent
%{_metainfodir}/org.qbittorrent.qBittorrent.metainfo.xml
%{_datadir}/applications/org.qbittorrent.qBittorrent.desktop
%{_datadir}/icons/hicolor/*/apps/qbittorrent.*
%{_datadir}/icons/hicolor/*/status/qbittorrent-tray*
%else
%{_bindir}/qbittorrent.exe
%endif
%{_mandir}/man1/qbittorrent.1*

%if !0%{?os2_version}
%files nox
%license COPYING
%doc qbittorrent-nox.README AUTHORS Changelog
%{_bindir}/qbittorrent-nox
%{_unitdir}/qbittorrent-nox@.service
%{_mandir}/man1/qbittorrent-nox.1*
%endif

%changelog
* Wed Feb 18 2026 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1:4.6.7-2
- fix a crash becuase we habe no /dev/urandom

* Mon Feb 16 2026 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1:4.6.7-1
- first OS/2 rpm
