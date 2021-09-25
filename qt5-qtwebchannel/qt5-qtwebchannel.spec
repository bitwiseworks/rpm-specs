%global qt_module qtwebchannel

# Only compress main Qt DLLs - plugins cannot be compressed as it destroys their QTMETADATA.
# TODO: Enhance _strip_opts to support masks with pathnames and to override LXLITE options for masks.
%global _strip_opts --compress -n "*.exe,Qt5*.dll"

# TODO: our make lacks -O flag, need to fix rpm macros for the time being...
%global make_build %{__make} %{?_smp_mflags}

Summary: Qt5 - WebChannel component
Name:    qt5-%{qt_module}
Version: 5.15.2
Release: 1%{?dist}

# See LICENSE.GPL LICENSE.LGPL LGPL_EXCEPTION.txt, for details
License: LGPLv2 with exceptions or GPLv3 with exceptions
Url: http://qt.io
%global majmin %(echo %{version} | cut -d. -f1-2)

# OS/2 is missing from official tarballs and has its own repo.
#Source0: https://download.qt.io/official_releases/qt/%{majmin}/%{version}/submodules/%{qt_module}-everywhere-src-%{version}.tar.xz

Vendor:  bww bitwise works GmbH

%scm_source github https://github.com/bitwiseworks/qtwebchannel-os2 v%{version}-os2-b1
#scm_source git file://D:/Coding/qt5/qt5/qtwebchannel xxxxxxx

# filter plugin/qml/examples provides
%global __provides_exclude_from ^(%{_qt5_qmldir}|%{_qt5_plugindir}|%{_qt5_examplesdir})/.*\\.dll$

BuildRequires: make
BuildRequires: qt5-rpm-macros >= %{version}
BuildRequires: qt5-qtbase-devel >= %{version}
BuildRequires: qt5-qtbase-private-devel
#libQt5Core.so.5(Qt_5_PRIVATE_API)(64bit)
%{?_qt5:Requires: %{_qt5}%{?_isa} = %{_qt5_version}}
BuildRequires: qt5-qtdeclarative-devel
BuildRequires: qt5-qtwebsockets-devel

# To support github tags starting with `v` (nasty github bug!)
BuildRequires: os2-rpm-build >= 1-8
# To pick up SSE2 alignment and no AVX optflags.
BuildRequires: rpm >= 4.13.0-20

%_qt5_examples_package_builddeps

%description
The Qt WebChannel module provides a library for seamless integration of C++
and QML applications with HTML/JavaScript clients. Any QObject can be
published to remote clients, where its public API becomes available.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt5-qtbase-devel%{?_isa}
%description devel
%{summary}.

%package examples
Summary: Programming examples for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%_qt5_examples_package_deps
%description examples
%{summary}.

%debug_package


%prep
#setup -q -n %{qt_module}-everywhere-src-%{version}
%scm_setup


%build

# configure expects either a git clone w/o include dir or a source tarball with
# it but we are neither. Pretend we are the former.
test -d .git || mkdir .git

%{qmake_qt5}

%make_build


%install
make install INSTALL_ROOT=%{buildroot}

## .prl file love
# nuke .prl reference(s) to %%buildroot
PWD_SAVE=$PWD
cd %{buildroot}%{_qt5_libdir}
for prl_file in Qt5*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
done
cd $PWD_SAVE


%files -f %{debug_package_exclude_files}
%doc README*.md CHANGELOG.md
%license LICENSE.*
%{_qt5_libdir}/Qt5WebH.dll
%{_qt5_archdatadir}/qml/QtWebChannel/

%files devel -f %{debug_package_exclude_files}
%{_qt5_headerdir}/QtWebChannel/
%{_qt5_libdir}/Qt5WebChannel.lib
%{_qt5_libdir}/Qt5WebChannel.prl
%dir %{_qt5_libdir}/cmake/Qt5WebChannel/
%{_qt5_libdir}/cmake/Qt5WebChannel/Qt5WebChannelConfig*.cmake
%{_qt5_libdir}/pkgconfig/Qt5WebChannel.pc
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_webchannel*.pri

%if 0%{?_qt5_examplesdir:1}
%files examples -f %{debug_package_exclude_files}
%{_qt5_examplesdir}/
%endif


%changelog
* Wed Sep 22 2021 Dmitriy Kuminov <coding@dmik.org> 5.15.2-1
- Initial release.
