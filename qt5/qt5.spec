# include qt5,qt5-devel metapackages or not
# dropped for f32+
%if 0
%global metapackage 1
%endif

Name: qt5
Version: 5.15.2
Release: 1%{?dist}
Summary: Qt5 meta package
License: GPLv3
URL: https://getfedora.org/
Vendor:  bww bitwise works GmbH
Source0: macros.qt5
Source1: macros.qt5-srpm
Source2: qmake-qt5.sh
BuildArch: noarch

# TODO: later, we don't have it all yet.
#Requires: qt5-qdbusviewer
#Requires: qt5-qt3d
Requires: qt5-qtbase
Requires: qt5-qtbase-gui
# TODO: No SQL drivers besides sqlite for now (which is part of main pkg)
#Requires: qt5-qtbase-mysql
#Requires: qt5-qtbase-postgresql
#Requires: qt5-qtconnectivity
Requires: qt5-qtdeclarative
#Requires: qt5-qtdoc
#Requires: qt5-qtgraphicaleffects
#Requires: qt5-qtimageformats
#Requires: qt5-qtlocation
Requires: qt5-qtmultimedia
#Requires: qt5-qtquickcontrols
#Requires: qt5-qtquickcontrols2
#Requires: qt5-qtscript
#Requires: qt5-qtsensors
#Requires: qt5-qtserialport
Requires: qt5-qtsvg
Requires: qt5-qttools
#Requires: qt5-qtwayland
Requires: qt5-qtwebchannel
## qtwebengine is not available on all archs, omit for now
## else, need to make qt5 arch'd and deps conditional (on arch)
#Requires: qt5-qtwebengine
Requires: qt5-qtwebsockets
#Requires: qt5-qtx11extras
#Requires: qt5-qtxmlpatterns

%description
%{summary}.

%package devel
Summary: Qt5 meta devel package
Requires: qt5-rpm-macros
Requires: qt5-qttools-static
Requires: qt5-qtdeclarative-static
Requires: qt5-qtbase-static
Requires: qt5-designer
#Requires: qt5-qdoc
Requires: qt5-qhelpgenerator
Requires: qt5-linguist
# TODO: later, we don't have it all yet.
#Requires: qt5-qt3d-devel
Requires: qt5-qtbase-devel
#Requires: qt5-qtconnectivity-devel
Requires: qt5-qtdeclarative-devel
#Requires: qt5-qtlocation-devel
Requires: qt5-qtmultimedia-devel
#Requires: qt5-qtscript-devel
#Requires: qt5-qtsensors-devel
#Requires: qt5-qtserialport-devel
Requires: qt5-qtsvg-devel
Requires: qt5-qttools-devel
#Requires: qt5-qtwayland-devel
Requires: qt5-qtwebchannel-devel
#Requires: qt5-qtwebengine-devel
Requires: qt5-qtwebsockets-devel
#Requires: qt5-qtx11extras-devel
#Requires: qt5-qtxmlpatterns-devel

%description devel
%{summary}.

%package rpm-macros
Summary: RPM macros for building Qt5 and KDE Frameworks 5 packages
Conflicts: qt5-qtbase-devel < 5.6.0-0.23
Requires: cmake >= 3
Requires: gcc-c++
%description rpm-macros
%{summary}.

%package srpm-macros
Summary: RPM macros for source Qt5 packages
%description srpm-macros
%{summary}.


%install
install -Dpm644 %{SOURCE0} %{buildroot}%{_rpmconfigdir}/macros.d/macros.qt5
install -Dpm644 %{SOURCE1} %{buildroot}%{_rpmconfigdir}/macros.d/macros.qt5-srpm
install -Dpm755 %{SOURCE2} %{buildroot}%{_bindir}/qmake-qt5.sh
mkdir -p %{buildroot}%{_datadir}/qt5/wrappers
ln -s %{_bindir}/qmake-qt5.sh %{buildroot}%{_datadir}/qt5/wrappers/qmake-qt5
ln -s %{_bindir}/qmake-qt5.sh %{buildroot}%{_datadir}/qt5/wrappers/qmake

# substitute custom flags, and the path to binaries: binaries referenced from
# macros should not change if an application is built with a different prefix.
# %_libdir is left as /usr/%{_lib} (e.g.) so that the resulting macros are
# architecture independent, and don't hardcode /usr/lib or /usr/lib64.
sed -i \
  -e "s|@@QT5_CFLAGS@@|%{?qt5_cflags}|g" \
  -e "s|@@QT5_CXXFLAGS@@|%{?qt5_cxxflags}|g" \
  -e "s|@@QT5_RPM_LD_FLAGS@@|%{?qt5_rpm_ld_flags}|g" \
  -e "s|@@QT5_RPM_OPT_FLAGS@@|%{?qt5_rpm_opt_flags}|g" \
  -e "s|@@QMAKE@@|%{_prefix}/%%{_lib}/qt5/bin/qmake|g" \
  -e "s|@@QMAKE_QT5_WRAPPER@@|%{_bindir}/qmake-qt5.sh|g" \
  %{buildroot}%{_rpmconfigdir}/macros.d/macros.qt5

%if 0%{?metapackage}
mkdir -p %{buildroot}%{_docdir}/qt5
mkdir -p %{buildroot}%{_docdir}/qt5-devel
echo "- Qt5 meta package" > %{buildroot}%{_docdir}/qt5/README
echo "- Qt5 devel meta package" > %{buildroot}%{_docdir}/qt5-devel/README

%files
%{_docdir}/qt5/README

%files devel
%{_docdir}/qt5-devel/README
%endif

%files rpm-macros
%{_rpmconfigdir}/macros.d/macros.qt5
%{_bindir}/qmake-qt5.sh
%{_datadir}/qt5/wrappers/

%files srpm-macros
%{_rpmconfigdir}/macros.d/macros.qt5-srpm


%changelog
* Wed Sep 22 2021 Dmitriy Kuminov <coding@dmik.org> 5.15.2-1
- Release version 5.15.2 for OS/2.
- Add qtmultimedia, qtwebchannel, qtwebsockets to dependencies.

* Thu Oct 17 2019 Dmitriy Kuminov <coding@dmik.org> 5.13.1-1
- Release version 5.13.1 for OS/2.
- Add qtsvg, qtdeclarative and qttools to dependencies.
- Add _qt5_examples_package_* macros.

* Mon Aug 12 2019 Dmitriy Kuminov <coding@dmik.org> 5.11.0-1
- Initial release.
