%global qt_module qtdeclarative

# Only compress main Qt DLLs - plugins cannot be compressed as it destroys their QTMETADATA.
# TODO: Enhance _strip_opts to support masks with pathnames and to override LXLITE options for masks.
%global _strip_opts --compress -n "*.exe,Qt5*.dll"

# TODO: our make lacks -O flag, need to fix rpm macros for the time being...
%global make_build %{__make} %{?_smp_mflags}

#global bootstrap 1

Summary: Qt5 - QtDeclarative component
Name:    qt5-%{qt_module}
Version: 5.13.1
Release: 1%{?dist}

# See LICENSE.GPL LICENSE.LGPL LGPL_EXCEPTION.txt, for details
License: LGPLv2 with exceptions or GPLv3 with exceptions
Url:     http://www.qt.io
%global majmin %(echo %{version} | cut -d. -f1-2)

# OS/2 is missing from official tarballs and has its own repo.
#Source0: https://download.qt.io/official_releases/qt/%{majmin}/%{version}/submodules/%{qt_module}-everywhere-src-%{version}.tar.xz

Vendor:  bww bitwise works GmbH

%scm_source github https://github.com/bitwiseworks/qtdeclarative-os2 v%{version}-os2-b1
#scm_source git file://D:/Coding/qt5/qt5/qtdeclarative xxxxxxx

# filter qml provides
%global __provides_exclude_from ^%{_qt5_archdatadir}/qml/.*\\.dll$

Obsoletes: qt5-qtjsbackend < 5.2.0
Obsoletes: qt5-qtdeclarative-render2d < 5.7.1-10

# TODO: we don't have specific gcc sub-packages so far.
#BuildRequires: gcc-c++
BuildRequires: qt5-rpm-macros >= %{version}
BuildRequires: qt5-qtbase-devel >= %{version}
BuildRequires: qt5-qtbase-private-devel
%{?_qt5:Requires: %{_qt5}%{?_isa} = %{_qt5_version}}
BuildRequires: python

%if 0%{?bootstrap}
Obsoletes: %{name}-examples < %{version}-%{release}
%global no_examples CONFIG-=compile_examples
%endif

%if 0%{?tests}
#BuildRequires: time
%endif

# To support github tags starting with `v` (nasty github bug!)
BuildRequires: os2-rpm-build >= 1-8

%if ! 0%{?no_examples:1}
%_qt5_examples_package_builddeps
%endif

%description
%{summary}.

%package devel
Summary: Development files for %{name}
Obsoletes: qt5-qtjsbackend-devel < 5.2.0
Obsoletes: qt5-qtdeclarative-render2d-devel < 5.7.1-10
Provides:  %{name}-private-devel = %{version}-%{release}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt5-qtbase-devel%{?_isa}
%description devel
%{summary}.

%package static
Summary: Static library files for %{name}
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
%description static
%{summary}.

%if ! 0%{?no_examples:1}
%package examples
Summary: Programming examples for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%_qt5_examples_package_deps
%description examples
%{summary}.
%endif

%debug_package


%prep
#setup -q -n %{qt_module}-everywhere-src-%{version}
%scm_setup


%build

# configure expects either a git clone w/o include dir or a source tarball with
# it but we are neither. Pretend we are the former.
test -d .git || mkdir .git

%qmake_qt5

%make_build


%install
%make_install INSTALL_ROOT=%{buildroot}

# hardlink files to %{_bindir}, add -qt5 postfix to not conflict
# note that on OS/2 there is no hard linking so we move and symlink back instead
# (symlinking should be fine since _qt5_bindir is internal, not exposied in PATH
# so files from there are to be only operated by kLIBC which can read symlinks)
mkdir %{buildroot}%{_bindir}
PWD_SAVE=$PWD
cd %{buildroot}%{_qt5_bindir}
for i in * ; do
  case "${i}" in
    # qt4 conflicts
    qmlplugindump.exe|qmlprofiler.exe)
      ext=${i##*.}
      targ=%{_bindir}/${i%%.${ext}}-qt5.${ext}
      mv     ${i} %{buildroot}${targ}
      ln -sv ${targ} ${i}
      ln -sv ${targ} ${i%%.${ext}}-qt5.${ext}
      ;;
    # qtchooser stuff
    qml.exe|qmlbundle.exe|qmlmin.exe|qmlscene.exe)
      ext=${i##*.}
      targ=%{_bindir}/${i%%.${ext}}-qt5.${ext}
      mv     ${i} %{buildroot}${targ}
      ln -sv ${i%%.${ext}}-qt5.${ext} %{buildroot}%{_bindir}/${i}
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
%if 0%{?tests}
export CTEST_OUTPUT_ON_FAILURE=1
export PATH=%{buildroot}%{_qt5_bindir};$PATH
export LD_LIBRARY_PATH=%{buildroot}%{_qt5_libdir}
make sub-tests-all %{?_smp_mflags}
xvfb-run -a \
dbus-launch --exit-with-session \
time \
make check -k -C tests ||:
%endif


%files -f %{debug_package_exclude_files}
%doc README.md CHANGELOG.md
%license LICENSE.LGPL*
%{_qt5_libdir}/Qt5Qml.dll
%{_qt5_libdir}/Qt5Q.dll
%{_qt5_libdir}/Qt5QWgt.dll
# TODO: later (requires opengl)
#{_qt5_libdir}/Qt5QPrt.dll
%{_qt5_libdir}/Qt5QShp.dll
%{_qt5_libdir}/Qt5QTst.dll
%{_qt5_plugindir}/qmltooling/
%{_qt5_archdatadir}/qml/

%files devel -f %{debug_package_exclude_files}
%{_bindir}/qml*
%{_qt5_bindir}/qml*
%{_qt5_headerdir}/Qt*/
%{_qt5_libdir}/Qt5Q*.lib
%{_qt5_libdir}/Qt5Q*.prl
%dir %{_qt5_libdir}/cmake/Qt5Quick*/
%{_qt5_libdir}/cmake/Qt5*/Qt5*Config*.cmake
%{_qt5_libdir}/pkgconfig/Qt5*.pc
%{_qt5_archdatadir}/mkspecs/modules/*.pri
%{_qt5_archdatadir}/mkspecs/features/*.prf
%dir %{_qt5_libdir}/cmake/Qt5Qml/
%{_qt5_libdir}/cmake/Qt5Qml/Qt5Qml_*Factory.cmake

%files static -f %{debug_package_exclude_files}
%{_qt5_libdir}/Qt5QmlDevTools.lib
%{_qt5_libdir}/Qt5QmlDevTools.prl
%{_qt5_libdir}/Qt5PacketProtocol.lib
%{_qt5_libdir}/Qt5PacketProtocol.prl
%{_qt5_libdir}/Qt5QmlDebug.lib
%{_qt5_libdir}/Qt5QmlDebug.prl

%if ! 0%{?no_examples:1}
%files examples -f %{debug_package_exclude_files}
%{_qt5_examplesdir}/

%_qt5_examples_package_post
%_qt5_examples_package_postun
%endif


%changelog
* Thu Oct 17 2019 Dmitriy Kuminov <coding@dmik.org> 5.13.1-1
- Initial release.
