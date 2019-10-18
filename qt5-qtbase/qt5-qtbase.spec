# TODO: support openssl-1.1 (not yet ported to OS/2)
#global openssl11 1
%global openssl -openssl-linked

%global platform os2-g++

%global qt_module qtbase

%global rpm_macros_dir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)

%global examples 1
## skip for now, until we're better at it --rex
#global tests 1

# Only compress main Qt DLLs - plugins cannot be compressed as it destroys their QTMETADATA.
# TODO: Enhance _strip_opts to support masks with pathnames and to override LXLITE options for masks.
%global _strip_opts --compress -n "*.exe,Qt5*.dll"

# TODO: our make lacks -O flag, need to fix rpm macros for the time being...
%global make_build %{__make} %{?_smp_mflags}

Name:    qt5-qtbase
Summary: Qt5 - QtBase components
Version: 5.13.1
Release: 1%{?dist}

# See LGPL_EXCEPTIONS.txt, for exception details
License: LGPLv2 with exceptions or GPLv3 with exceptions
Url:     http://qt-project.org/
%global  majmin %(echo %{version} | cut -d. -f1-2)

# OS/2 is missing from official tarballs and has its own repo.
#Source0: https://download.qt.io/official_releases/qt/%{majmin}/%{version}/submodules/%{qt_module}-everywhere-src-%{version}.tar.xz

Vendor:  bww bitwise works GmbH

%scm_source github https://github.com/bitwiseworks/qtbase-os2 v%{version}-os2-b1
#scm_source git file://D:/Coding/qt5/qt5/qtbase xxxxxxx

# Disable debug messages by default.
Source1: qtlogging.ini

# macros
Source10: macros.qt5-qtbase

BuildRequires: cups-devel
BuildRequires: findutils
BuildRequires: libjpeg-devel
# TODO: it seems Qt doesn't support mng/tiff by default, remove?
#BuildRequires: libmng-devel
#BuildRequires: libtiff-devel
# TODO: we don't have specific gcc sub-packages so far.
#BuildRequires: gcc-c++
BuildRequires: pkgconfig(fontconfig)
BuildRequires: pkgconfig(libpng)
BuildRequires: openssl-devel%{?openssl11: >= 1.1}
%global sqlite -system-sqlite
BuildRequires: pkgconfig(sqlite3) >= 3.7
# TODO no system harfbuzz yet
#global harfbuzz -system-harfbuzz
#BuildRequires: pkgconfig(harfbuzz) >= 0.9.42
BuildRequires: pkgconfig(icu-i18n)
# TODO our system pcre is too old, needs updating
#BuildRequires: pkgconfig(libpcre2-posix) >= 10.20
#BuildRequires: pkgconfig(libpcre) >= 8.0
#%global pcre -system-pcre
# TODO need?
#BuildRequires: libicu-devel
%global pcre -qt-pcre
BuildRequires: pkgconfig(zlib)
BuildRequires: perl-generators
BuildRequires: qt5-rpm-macros

# To support github tags starting with `v` (nasty github bug!)
BuildRequires: os2-rpm-build >= 1-8

%if 0%{?examples}
%_qt5_examples_package_builddeps
%endif

Requires: %{name}-common = %{version}-%{release}

%description
Qt is a software toolkit for developing applications.

This package contains base tools, like string, xml, and network
handling.

%package common
Summary: Common files for Qt5
Requires: %{name} = %{version}-%{release}
BuildArch: noarch
%description common
%{summary}.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: %{name}-gui%{?_isa}
Requires: qt5-rpm-macros
%description devel
%{summary}.

%package private-devel
Summary: Development files for %{name} private APIs
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
# QtPrintSupport/private requires cups/ppd.h
Requires: cups-devel
%description private-devel
%{summary}.

%if 0%{?examples}
%package examples
Summary: Programming examples for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%_qt5_examples_package_deps

%description examples
%{summary}.
%endif

%package static
Summary: Static library files for %{name}
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
Requires: pkgconfig(fontconfig)
Requires: pkgconfig(zlib)

%description static
%{summary}.

# TODO: No SQL drivers besides sqlite for now (which is part of main pkg)
%if 0
%if "%{?ibase}" != "-no-sql-ibase"
%package ibase
Summary: IBase driver for Qt5's SQL classes
BuildRequires: firebird-devel
Requires: %{name}%{?_isa} = %{version}-%{release}
%description ibase
%{summary}.
%endif

%package mysql
Summary: MySQL driver for Qt5's SQL classes
%if 0%{?fedora} > 27
BuildRequires: mariadb-connector-c-devel
%else
BuildRequires: mysql-devel
%endif
Requires: %{name}%{?_isa} = %{version}-%{release}
%description mysql
%{summary}.

%package odbc
Summary: ODBC driver for Qt5's SQL classes
BuildRequires: unixODBC-devel
Requires: %{name}%{?_isa} = %{version}-%{release}
%description odbc
%{summary}.

%package postgresql
Summary: PostgreSQL driver for Qt5's SQL classes
BuildRequires: libpq-devel
Requires: %{name}%{?_isa} = %{version}-%{release}
%description postgresql
%{summary}.
%endif

# debating whether to do 1 subpkg per library or not -- rex
%package gui
Summary: Qt5 GUI-related libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Provides:  qt5-qtbase-os2 = %{version}-%{release}
%description gui
Qt5 libraries used for drawing widgets and OpenGL items.

%debug_package


%prep
#setup -q -n %{qt_module}-everywhere-src-%{version}
%scm_setup

# move some bundled libs to ensure they're not accidentally used
PWD_SAVE=$PWD
cd src/3rdparty
mkdir UNUSED
mv freetype libjpeg libpng zlib UNUSED/
%if "%{?sqlite}" == "-system-sqlite"
mv sqlite UNUSED/
%endif
cd $PWD_SAVE

# use proper perl interpretter so autodeps work as expected
sed -i -e "s|^#!/usr/bin/env perl$|#!%{__perl}|" \
 bin/fixqt4headers.pl \
 bin/syncqt.pl \
 mkspecs/features/data/unix/findclasslist.pl


%build

## adjust $RPM_OPT_FLAGS
# TODO: Later (needs -no-sse in rpm macros for pentium4 builds etc.)
#RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's|-fexceptions||g'`
#RPM_OPT_FLAGS="$RPM_OPT_FLAGS %{?qt5_arm_flag} %{?qt5_deprecated_flag} %{?qt5_null_flag}"

# TODO: Later (needs -no-sse in rpm macros for pentium4 builds etc.)
#export CFLAGS="$CFLAGS $RPM_OPT_FLAGS"
#export CXXFLAGS="$CXXFLAGS $RPM_OPT_FLAGS"
#export LDFLAGS="$LDFLAGS $RPM_LD_FLAGS"
export MAKEFLAGS="%{?_smp_mflags}"

# configure expects either a git clone w/o include dir or a source tarball with
# it but we are neither. Pretend we are the former.
test -d .git || mkdir .git

./configure \
  -verbose \
  -confirm-license \
  -opensource \
  -prefix %{_qt5_prefix} \
  -archdatadir %{_qt5_archdatadir} \
  -bindir %{_qt5_bindir} \
  -libdir %{_qt5_libdir} \
  -libexecdir %{_qt5_libexecdir} \
  -datadir %{_qt5_datadir} \
  -docdir %{_qt5_docdir} \
  -examplesdir %{_qt5_examplesdir} \
  -headerdir %{_qt5_headerdir} \
  -importdir %{_qt5_importdir} \
  -plugindir %{_qt5_plugindir} \
  -sysconfdir %{_qt5_sysconfdir} \
  -translationdir %{_qt5_translationdir} \
  -platform %{platform} \
  -release \
  -shared \
  -fontconfig \
  -icu \
  -optimized-qmake \
  %{?openssl} \
  %{!?examples:-nomake examples} \
  %{!?tests:-nomake tests} \
  -force-debug-info \
  -system-libjpeg \
  -system-libpng \
  %{?harfbuzz} \
  %{?pcre} \
  %{?sqlite} \
  -system-zlib \
  -no-opengl \

# TODO: Later (needs -no-sse in rpm macros for pentium4 builds etc.)
#  QMAKE_CFLAGS_RELEASE="${CFLAGS:-$RPM_OPT_FLAGS}" \
#  QMAKE_CXXFLAGS_RELEASE="${CXXFLAGS:-$RPM_OPT_FLAGS}" \
#  QMAKE_LFLAGS_RELEASE="${LDFLAGS:-$RPM_LD_FLAGS}"

# ensure qmake build using optflags (which can happen if not munging qmake.conf defaults)
make clean -C qmake
%make_build -C qmake all binary \

# TODO: Later (needs -no-sse in rpm macros for pentium4 builds etc.)
#  QMAKE_CFLAGS_RELEASE="${CFLAGS:-$RPM_OPT_FLAGS}" \
#  QMAKE_CXXFLAGS_RELEASE="${CXXFLAGS:-$RPM_OPT_FLAGS}" \
#  QMAKE_LFLAGS_RELEASE="${LDFLAGS:-$RPM_LD_FLAGS}" \
#  QMAKE_STRIP=

%make_build


%install
make install INSTALL_ROOT=%{buildroot}

install -m644 -p -D %{SOURCE1} %{buildroot}%{_qt5_datadir}/qtlogging.ini

# Qt5.pc
cat >%{buildroot}%{_libdir}/pkgconfig/Qt5.pc<<EOF
prefix=%{_qt5_prefix}
archdatadir=%{_qt5_archdatadir}
bindir=%{_qt5_bindir}
datadir=%{_qt5_datadir}

docdir=%{_qt5_docdir}
examplesdir=%{_qt5_examplesdir}
headerdir=%{_qt5_headerdir}
importdir=%{_qt5_importdir}
libdir=%{_qt5_libdir}
libexecdir=%{_qt5_libexecdir}
moc=%{_qt5_bindir}/moc
plugindir=%{_qt5_plugindir}
qmake=%{_qt5_bindir}/qmake
settingsdir=%{_qt5_settingsdir}
sysconfdir=%{_qt5_sysconfdir}
translationdir=%{_qt5_translationdir}

Name: Qt5
Description: Qt5 Configuration
Version: %{version}
EOF

# rpm macros
install -p -m644 -D %{SOURCE10} \
  %{buildroot}%{rpm_macros_dir}/macros.qt5-qtbase
sed -i \
  -e "s|@@NAME@@|%{name}|g" \
  -e "s|@@EPOCH@@|%{?epoch}%{!?epoch:0}|g" \
  -e "s|@@VERSION@@|%{version}|g" \
  -e "s|@@EVR@@|%{?epoch:%{epoch:}}%{version}-%{release}|g" \
  %{buildroot}%{rpm_macros_dir}/macros.qt5-qtbase

# create/own dirs
for i in %{_qt5_archdatadir}/mkspecs/modules %{_qt5_importdir} %{_qt5_libexecdir} \
         %{_qt5_plugindir}/designer %{_qt5_plugindir}/iconengines \
         %{_qt5_plugindir}/script %{_qt5_plugindir}/styles \
         %{_qt5_translationdir} ; do
  mkdir -p %{buildroot}${i}
done
mkdir -p %{buildroot}%{_sysconfdir}/xdg/QtProject

# hardlink files to {_bindir}, add -qt5 postfix to not conflict
# note that on OS/2 there is no hard linking so we move and symlink back instead
# (symlinking should be fine since _qt5_bindir is internal, not exposied in PATH
# so files from there are to be only operated by kLIBC which can read symlinks)
mkdir %{buildroot}%{_bindir}
PWD_SAVE=$PWD
cd %{buildroot}%{_qt5_bindir}
for i in * ; do
  case "${i}" in
    moc.exe|qdbuscpp2xml.exe|qdbusxml2cpp.exe|qmake.exe|rcc.exe|syncqt.pl|uic.exe)
      ext=${i##*.}
      targ=%{_bindir}/${i%%.${ext}}-qt5.${ext}
      mv     ${i} %{buildroot}${targ}
      ln -sv ${targ} ${i}
      ln -sv ${targ} ${i%%.${ext}}-qt5.${ext}
      ;;
    *)
      targ=%{_bindir}/${i}
      mv     ${i} %{buildroot}${targ}
      ln -sv ${targ} ${i}
      ;;
  esac
done
cd $PWD_SAVE

## .prl file love
# nuke .prl reference(s) to %%buildroot
PWD_SAVE=$PWD
cd %{buildroot}%{_qt5_libdir}
for prl_file in Qt5*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
done
cd $PWD_SAVE


%check
# verify Qt5.pc
export PKG_CONFIG_PATH=%{buildroot}%{_libdir}/pkgconfig
test "$(pkg-config --modversion Qt5)" = "%{version}"
%if 0%{?tests}
## see tests/README for expected environment (running a plasma session essentially)
## we are not quite there yet
export CTEST_OUTPUT_ON_FAILURE=1
export PATH=%{buildroot}%{_qt5_bindir}:$PATH
export LD_LIBRARY_PATH=%{buildroot}%{_qt5_libdir}
# dbus tests error out when building if session bus is not available
dbus-launch --exit-with-session \
%make_build sub-tests  -k ||:
xvfb-run -a --server-args="-screen 0 1280x1024x32" \
dbus-launch --exit-with-session \
time \
make check -k ||:
%endif


%files -f %{debug_package_exclude_files}
%doc README.md CHANGELOG.md
%license LICENSE.FDL
%license LICENSE.GPL*
%license LICENSE.LGPL*
%dir %{_sysconfdir}/xdg/QtProject/
%{_qt5_libdir}/Qt5Cncr.dll
%{_qt5_libdir}/Qt5Core.dll
%{_qt5_libdir}/Qt5DBus.dll
%{_qt5_libdir}/Qt5Net.dll
%{_qt5_libdir}/Qt5Sql.dll
%{_qt5_libdir}/Qt5Test.dll
%{_qt5_libdir}/Qt5Xml.dll
%dir %{_qt5_libdir}/cmake/
%dir %{_qt5_libdir}/cmake/Qt5/
%dir %{_qt5_libdir}/cmake/Qt5Concurrent/
%dir %{_qt5_libdir}/cmake/Qt5Core/
%dir %{_qt5_libdir}/cmake/Qt5DBus/
%dir %{_qt5_libdir}/cmake/Qt5Gui/
%dir %{_qt5_libdir}/cmake/Qt5Network/
%if 0%{?egl}
%dir %{_qt5_libdir}/cmake/Qt5OpenGL/
%endif
%dir %{_qt5_libdir}/cmake/Qt5PrintSupport/
%dir %{_qt5_libdir}/cmake/Qt5Sql/
%dir %{_qt5_libdir}/cmake/Qt5Test/
%dir %{_qt5_libdir}/cmake/Qt5Widgets/
%dir %{_qt5_libdir}/cmake/Qt5Xml/
%dir %{_qt5_docdir}/
%{_qt5_docdir}/global/
%{_qt5_docdir}/config/
%{_qt5_importdir}/
%{_qt5_translationdir}/
%if "%{_qt5_prefix}" != "%{_prefix}"
%dir %{_qt5_prefix}/
%endif
%dir %{_qt5_archdatadir}/
%dir %{_qt5_datadir}/
%{_qt5_datadir}/qtlogging.ini
%dir %{_qt5_libexecdir}/
%dir %{_qt5_plugindir}/
%dir %{_qt5_plugindir}/bearer/
%{_qt5_plugindir}/bearer/qgbear.dll
%{_qt5_libdir}/cmake/Qt5Network/Qt5Network_QGenericEnginePlugin.cmake
%dir %{_qt5_plugindir}/designer/
%dir %{_qt5_plugindir}/generic/
%dir %{_qt5_plugindir}/iconengines/
%dir %{_qt5_plugindir}/imageformats/
# TODO later?
#dir %{_qt5_plugindir}/platforminputcontexts/
%dir %{_qt5_plugindir}/platforms/
%dir %{_qt5_plugindir}/platformthemes/
%dir %{_qt5_plugindir}/printsupport/
%dir %{_qt5_plugindir}/script/
%dir %{_qt5_plugindir}/sqldrivers/
%dir %{_qt5_plugindir}/styles/
%{_qt5_plugindir}/sqldrivers/qsqlite.dll
%{_qt5_libdir}/cmake/Qt5Sql/Qt5Sql_QSQLiteDriverPlugin.cmake

%files common -f %{debug_package_exclude_files}
# mostly empty for now, consider: filesystem/dir ownership, licenses
%{rpm_macros_dir}/macros.qt5-qtbase

%files devel -f %{debug_package_exclude_files}
%if "%{_qt5_bindir}" != "%{_bindir}"
%dir %{_qt5_bindir}
%endif
%{_bindir}/moc*
%{_bindir}/qdbuscpp2xml*
%{_bindir}/qdbusxml2cpp*
%{_bindir}/qmake*
%{_bindir}/rcc*
%{_bindir}/syncqt*
%{_bindir}/uic*
%{_bindir}/qlalr*
%{_bindir}/fixqt4headers.pl
%{_bindir}/qvkgen*
%{_qt5_bindir}/moc*
%{_qt5_bindir}/qdbuscpp2xml*
%{_qt5_bindir}/qdbusxml2cpp*
%{_qt5_bindir}/qmake*
%{_qt5_bindir}/rcc*
%{_qt5_bindir}/syncqt*
%{_qt5_bindir}/uic*
%{_qt5_bindir}/qlalr*
%{_qt5_bindir}/fixqt4headers.pl
%{_qt5_bindir}/qvkgen*
%if "%{_qt5_headerdir}" != "%{_includedir}"
%dir %{_qt5_headerdir}
%endif
%{_qt5_headerdir}/QtConcurrent/
%{_qt5_headerdir}/QtCore/
%{_qt5_headerdir}/QtDBus/
%{_qt5_headerdir}/QtGui/
%{_qt5_headerdir}/QtNetwork/
%if 0%{?egl}
%{_qt5_headerdir}/QtOpenGL/
%endif
%{_qt5_headerdir}/QtPlatformHeaders/
%{_qt5_headerdir}/QtPrintSupport/
%{_qt5_headerdir}/QtSql/
%{_qt5_headerdir}/QtTest/
%{_qt5_headerdir}/QtWidgets/
%{_qt5_headerdir}/QtXml/
%if 0%{?egl}
%{_qt5_headerdir}/QtEglFSDeviceIntegration
%endif
# TODO later?
#{_qt5_headerdir}/QtInputSupport
%{_qt5_headerdir}/QtEdidSupport
%{_qt5_archdatadir}/mkspecs/
%{_qt5_libdir}/Qt5Concurrent.prl
%{_qt5_libdir}/Qt5Concurrent.lib
%{_qt5_libdir}/Qt5Core.prl
%{_qt5_libdir}/Qt5Core.lib
%{_qt5_libdir}/Qt5DBus.prl
%{_qt5_libdir}/Qt5DBus.lib
%{_qt5_libdir}/Qt5Gui.prl
%{_qt5_libdir}/Qt5Gui.lib
%{_qt5_libdir}/Qt5Network.prl
%{_qt5_libdir}/Qt5Network.lib
%if 0%{?egl}
%{_qt5_libdir}/Qt5OpenGL.prl
%{_qt5_libdir}/Qt5OpenGL.lib
%endif
%{_qt5_libdir}/Qt5PrintSupport.prl
%{_qt5_libdir}/Qt5PrintSupport.lib
%{_qt5_libdir}/Qt5Sql.prl
%{_qt5_libdir}/Qt5Sql.lib
%{_qt5_libdir}/Qt5Test.prl
%{_qt5_libdir}/Qt5Test.lib
%{_qt5_libdir}/Qt5Widgets.prl
%{_qt5_libdir}/Qt5Widgets.lib
%{_qt5_libdir}/Qt5Xml.prl
%{_qt5_libdir}/Qt5Xml.lib
%if 0%{?egl}
%{_qt5_libdir}/Qt5EglFSDeviceIntegration.prl
%{_qt5_libdir}/Qt5EglFSDeviceIntegration.lib
%endif
%{_qt5_libdir}/cmake/Qt5/Qt5Config*.cmake
%{_qt5_libdir}/cmake/Qt5Concurrent/Qt5ConcurrentConfig*.cmake
%{_qt5_libdir}/cmake/Qt5Core/Qt5CoreConfig*.cmake
%{_qt5_libdir}/cmake/Qt5Core/Qt5CoreMacros.cmake
%{_qt5_libdir}/cmake/Qt5Core/Qt5CTestMacros.cmake
%{_qt5_libdir}/cmake/Qt5DBus/Qt5DBusConfig*.cmake
%{_qt5_libdir}/cmake/Qt5DBus/Qt5DBusMacros.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5GuiConfig*.cmake
%{_qt5_libdir}/cmake/Qt5Network/Qt5NetworkConfig*.cmake
%if 0%{?egl}
%{_qt5_libdir}/cmake/Qt5OpenGL/Qt5OpenGLConfig*.cmake
%endif
%{_qt5_libdir}/cmake/Qt5AccessibilitySupport/Qt5AccessibilitySupportConfig*.cmake
%{_qt5_libdir}/cmake/Qt5Bootstrap/Qt5BootstrapConfig*.cmake
%{_qt5_libdir}/cmake/Qt5DeviceDiscoverySupport/Qt5DeviceDiscoverySupportConfig*.cmake
%{_qt5_libdir}/cmake/Qt5EdidSupport/Qt5EdidSupportConfig*.cmake
%{_qt5_libdir}/cmake/Qt5EventDispatcherSupport/Qt5EventDispatcherSupportConfig*.cmake
%{_qt5_libdir}/cmake/Qt5FbSupport/Qt5FbSupportConfig*.cmake
%{_qt5_libdir}/cmake/Qt5FontDatabaseSupport/Qt5FontDatabaseSupportConfig*.cmake
%{_qt5_libdir}/cmake/Qt5ThemeSupport/Qt5ThemeSupportConfig*.cmake
%{_qt5_libdir}/cmake/Qt5PrintSupport/Qt5PrintSupportConfig*.cmake
%{_qt5_libdir}/cmake/Qt5Sql/Qt5SqlConfig*.cmake
%{_qt5_libdir}/cmake/Qt5Test/Qt5TestConfig*.cmake
%{_qt5_libdir}/cmake/Qt5Widgets/Qt5WidgetsConfig*.cmake
%{_qt5_libdir}/cmake/Qt5Widgets/Qt5WidgetsMacros.cmake
%{_qt5_libdir}/cmake/Qt5Xml/Qt5XmlConfig*.cmake
%{_qt5_libdir}/cmake/Qt5/Qt5ModuleLocation.cmake
%{_qt5_libdir}/pkgconfig/Qt5.pc
%{_qt5_libdir}/pkgconfig/Qt5Concurrent.pc
%{_qt5_libdir}/pkgconfig/Qt5Core.pc
%{_qt5_libdir}/pkgconfig/Qt5DBus.pc
%{_qt5_libdir}/pkgconfig/Qt5Gui.pc
%{_qt5_libdir}/pkgconfig/Qt5Network.pc
%if 0%{?egl}
%{_qt5_libdir}/pkgconfig/Qt5OpenGL.pc
%endif
%{_qt5_libdir}/pkgconfig/Qt5PrintSupport.pc
%{_qt5_libdir}/pkgconfig/Qt5Sql.pc
%{_qt5_libdir}/pkgconfig/Qt5Test.pc
%{_qt5_libdir}/pkgconfig/Qt5Widgets.pc
%{_qt5_libdir}/pkgconfig/Qt5Xml.pc
%if 0%{?egl}
%{_qt5_libdir}/Qt5EglFsKmsSupport.prl
%{_qt5_libdir}/Qt5EglFsKmsSupport.lib
%endif
## private-devel globs
# keep mkspecs/modules stuff  in -devel for now, https://bugzilla.redhat.com/show_bug.cgi?id=1705280
#exclude %{_qt5_archdatadir}/mkspecs/modules/qt_lib_*_private.pri
%exclude %{_qt5_headerdir}/*/%{version}/*/private/

%files private-devel -f %{debug_package_exclude_files}
%{_qt5_headerdir}/*/%{version}/*/private/
#{_qt5_archdatadir}/mkspecs/modules/qt_lib_*_private.pri

%files static -f %{debug_package_exclude_files}
%{_qt5_libdir}/Qt5Bootstrap.lib
%{_qt5_libdir}/Qt5Bootstrap.prl
%if 0%{?egl}
%{_qt5_headerdir}/QtOpenGLExtensions/
%{_qt5_libdir}/Qt5OpenGLExtensions.lib
%{_qt5_libdir}/Qt5OpenGLExtensions.prl
%{_qt5_libdir}/cmake/Qt5OpenGLExtensions/
%{_qt5_libdir}/pkgconfig/Qt5OpenGLExtensions.pc
%endif
%{_qt5_libdir}/Qt5AccessibilitySupport.lib
%{_qt5_libdir}/Qt5AccessibilitySupport.prl
%{_qt5_headerdir}/QtAccessibilitySupport
%{_qt5_libdir}/Qt5DeviceDiscoverySupport.lib
%{_qt5_libdir}/Qt5DeviceDiscoverySupport.prl
%{_qt5_headerdir}/QtDeviceDiscoverySupport
%if 0%{?egl}
%{_qt5_libdir}/Qt5EglSupport.lib
%{_qt5_libdir}/Qt5EglSupport.prl
%{_qt5_headerdir}/QtEglSupport
%endif
%{_qt5_libdir}/Qt5EventDispatcherSupport.lib
%{_qt5_libdir}/Qt5EventDispatcherSupport.prl
%{_qt5_headerdir}/QtEventDispatcherSupport
%{_qt5_libdir}/Qt5FbSupport.lib
%{_qt5_libdir}/Qt5FbSupport.prl
%{_qt5_headerdir}/QtFbSupport
%{_qt5_libdir}/Qt5FontDatabaseSupport.lib
%{_qt5_libdir}/Qt5FontDatabaseSupport.prl
%{_qt5_headerdir}/QtFontDatabaseSupport
%if 0%{?egl}
%{_qt5_libdir}/Qt5GlxSupport.lib
%{_qt5_libdir}/Qt5GlxSupport.prl
%{_qt5_headerdir}/QtGlxSupport
%endif
# TODO later?
#{_qt5_libdir}/Qt5InputSupport.lib
#{_qt5_libdir}/Qt5InputSupport.prl
#{_qt5_libdir}/Qt5PlatformCompositorSupport.lib
#{_qt5_libdir}/Qt5PlatformCompositorSupport.prl
#{_qt5_headerdir}/QtPlatformCompositorSupport
#{_qt5_libdir}/Qt5ServiceSupport.lib
#{_qt5_libdir}/Qt5ServiceSupport.prl
#{_qt5_headerdir}/QtServiceSupport
%{_qt5_libdir}/Qt5ThemeSupport.lib
%{_qt5_libdir}/Qt5ThemeSupport.prl
%{_qt5_headerdir}/QtThemeSupport
%{_qt5_libdir}/Qt5EdidSupport.lib
%{_qt5_libdir}/Qt5EdidSupport.prl

%if 0%{?examples}
%files examples -f %{debug_package_exclude_files}
%{_qt5_examplesdir}/
%endif

# TODO: No SQL drivers besides sqlite for now (which is part of main pkg)
%if 0
%if "%{?ibase}" != "-no-sql-ibase"
%files ibase -f %{debug_package_exclude_files}
%{_qt5_plugindir}/sqldrivers/qsqlibas.dll
%{_qt5_libdir}/cmake/Qt5Sql/Qt5Sql_QIBaseDriverPlugin.cmake
%endif

%files mysql -f %{debug_package_exclude_files}
%{_qt5_plugindir}/sqldrivers/qsqlmysq.dll
%{_qt5_libdir}/cmake/Qt5Sql/Qt5Sql_QMYSQLDriverPlugin.cmake

%files odbc -f %{debug_package_exclude_files}
%{_qt5_plugindir}/sqldrivers/qsqlodbc.dll
%{_qt5_libdir}/cmake/Qt5Sql/Qt5Sql_QODBCDriverPlugin.cmake

%files postgresql -f %{debug_package_exclude_files}
%{_qt5_plugindir}/sqldrivers/qsqlpsql.dll
%{_qt5_libdir}/cmake/Qt5Sql/Qt5Sql_QPSQLDriverPlugin.cmake
%endif

%files gui -f %{debug_package_exclude_files}
%{_qt5_libdir}/Qt5Gui.dll
%if 0%{?egl}
%{_qt5_libdir}/Qt5OGL.dll
%endif
%{_qt5_libdir}/Qt5Prnt.dll
%{_qt5_libdir}/Qt5Wdgt.dll
%{_qt5_plugindir}/generic/qtuiotp.dll
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QTuioTouchPlugin.cmake
%{_qt5_plugindir}/imageformats/qgif.dll
%{_qt5_plugindir}/imageformats/qico.dll
%{_qt5_plugindir}/imageformats/qjpeg.dll
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QGifPlugin.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QICOPlugin.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QJpegPlugin.cmake
# TODO later?
#{_qt5_plugindir}/platforminputcontexts/libcomposeplatforminputcontextplugin.so
#{_qt5_plugindir}/platforminputcontexts/libibusplatforminputcontextplugin.so
#{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QComposePlatformInputContextPlugin.cmake
#{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QIbusPlatformInputContextPlugin.cmake
%if 0%{?egl}
%{_qt5_libdir}/libQt5EglFSDeviceIntegration.so.5*
%{_qt5_libdir}/libQt5EglFsKmsSupport.so.5*
%{_qt5_plugindir}/platforms/libqeglfs.so
%{_qt5_plugindir}/platforms/libqminimalegl.so
%dir %{_qt5_plugindir}/egldeviceintegrations/
%{_qt5_plugindir}/egldeviceintegrations/libqeglfs-kms-integration.so
%{_qt5_plugindir}/egldeviceintegrations/libqeglfs-x11-integration.so
%{_qt5_plugindir}/xcbglintegrations/libqxcb-egl-integration.so
%{_qt5_plugindir}/egldeviceintegrations/libqeglfs-kms-egldevice-integration.so
%{_qt5_plugindir}/egldeviceintegrations/libqeglfs-emu-integration.so
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QMinimalEglIntegrationPlugin.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QEglFSIntegrationPlugin.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QEglFSX11IntegrationPlugin.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QEglFSKmsGbmIntegrationPlugin.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QXcbEglIntegrationPlugin.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QEglFSKmsEglDeviceIntegrationPlugin.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QEglFSEmulatorIntegrationPlugin.cmake
%endif
%{_qt5_plugindir}/platforms/qplmin.dll
%{_qt5_plugindir}/platforms/qoffscr.dll
%{_qt5_plugindir}/platforms/qos2.dll
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QMinimalIntegrationPlugin.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QOffscreenIntegrationPlugin.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QOS2IntegrationPlugin.cmake
%{_qt5_plugindir}/platformthemes/qxdgdp.dll
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QXdgDesktopPortalThemePlugin.cmake
%{_qt5_plugindir}/printsupport/cupsprn.dll
%{_qt5_libdir}/cmake/Qt5PrintSupport/Qt5PrintSupport_QCupsPrinterSupportPlugin.cmake


%post
# We used to install some WPS objects in 5.11.0, make sure they are gone with an update.
if [ "$1" -ge 1 ]; then # (upon update)
    %wps_object_delete_all
fi

%if 0%{?examples}
%_qt5_examples_package_post
%_qt5_examples_package_postun
%endif

%changelog
* Thu Oct 17 2019 Dmitriy Kuminov <coding@dmik.org> 5.13.1-1
- Release version 5.13.1 Beta 1 for OS/2.
  (https://github.com/bitwiseworks/qtbase-os2/blob/v5.13.1-os2-b1/CHANGELOG.md).
- Remove glib dependency from static sub-package (not needed on OS/2).
- Configure explicitly for fontconfig and ICU as we expose explicit deps.
- Enable debug logging in qtlogging.ini by default (it's more expected by apps).
- Don't install READMEs in Programs/bitwiseworks Apps and Ports.

* Mon Aug 12 2019 Dmitriy Kuminov <coding@dmik.org> 5.11.0-1
- Initial release.
