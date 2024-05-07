%if 0%{?rhel} || 0%{?os2_version}
# EPEL - only Qt5 packages
%bcond_with	qt4
%bcond_without	qt5
%bcond_with	qt6
%else
# Fedora - build everything
%bcond_without	qt4
%bcond_without	qt5
%bcond_without	qt6
%endif

%bcond_without test

# see top-ldevel CMakeLists.txt for variables of same name
%global QUAZIP_LIB_VERSION %{version} 
%global QUAZIP_LIB_SOVERSION 1.4.0

Name:		quazip
Version:	1.4
Release:	1%{?dist}
Summary:	Qt/C++ wrapper for the minizip library
License:	GPLv2+ or LGPLv2+
URL:		https://github.com/stachenov/quazip
%if !0%{?os2_version}
Source0:	%{url}/archive/v%{version}/%{name}-v%{version}.tar.gz
# pre-1.0 compat CMake module
Source1:	FindQuaZip.cmake
%else
Vendor:         bww bitwise works GmbH
%scm_source github https://github.com/bitwiseworks/%{name}-os2 v%{version}-os2
%endif
BuildRequires:	bzip2-devel
BuildRequires:	cmake
BuildRequires:	gcc-c++
BuildRequires:	zlib-devel
%if %{with qt4}
BuildRequires:	qt4-devel
%endif
%if %{with qt5}
BuildRequires:	qt5-qtbase-devel
%endif
%if %{with qt6}
BuildRequires:	qt6-qtbase-devel
BuildRequires:	qt6-qt5compat-devel
%endif
%if !0%{?os2_version}
BuildRequires:	doxygen graphviz
%else
BuildRequires:	doxygen
%endif

%description
QuaZIP is a simple C++ wrapper over Gilles Vollant's ZIP/UNZIP package that
can be used to access ZIP archives. It uses Trolltech's Qt toolkit.

QuaZIP allows you to access files inside ZIP archives using QIODevice API,
and - yes! - that means that you can also use QTextStream, QDataStream or
whatever you would like to use on your zipped files.

QuaZIP provides complete abstraction of the ZIP/UNZIP API, for both reading
from and writing to ZIP archives.


%if %{with qt4}
%package devel
Summary:	Development files for %{name}
%if !0%{?os2_version}
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	bzip2-devel%{?_isa}
Requires:	qt4-devel%{?_isa}
Requires:	zlib-devel%{?_isa}
%else
Requires:	%{name} = %{version}-%{release}
Requires:	bzip2-devel
Requires:	qt4-devel
Requires:	zlib-devel
%endif

%description devel
The %{name}-devel package contains libraries, header files and documentation
for developing applications that use %{name}. 
%endif

%if %{with qt5}
%package qt5
Summary: Qt5 wrapper for the minizip library
%description qt5
QuaZIP is a simple C++ wrapper over Gilles Vollant's ZIP/UNZIP package that
can be used to access ZIP archives. It uses Trolltech's Qt toolkit.

QuaZIP allows you to access files inside ZIP archives using QIODevice API,
and - yes! - that means that you can also use QTextStream, QDataStream or
whatever you would like to use on your zipped files.

QuaZIP provides complete abstraction of the ZIP/UNZIP API, for both reading
from and writing to ZIP archives.

%package qt5-devel
Summary:	Development files for %{name}-qt5
%if !0%{?os2_version}
Requires:	%{name}-qt5%{?_isa} = %{version}-%{release}
Requires:	bzip2-devel%{?_isa}
Requires:	qt5-qtbase-devel%{?_isa}
Requires:	zlib-devel%{?_isa}
%else
Requires:	%{name}-qt5 = %{version}-%{release}
Requires:	bzip2-devel
Requires:	qt5-qtbase-devel
Requires:	zlib-devel
%endif

%description qt5-devel
The %{name}-qt5-devel package contains libraries, header files and documentation
for developing applications that use %{name}-qt5.
%endif

%if %{with qt6}
%package qt6
Summary: Qt6 wrapper for the minizip library
%description qt6
QuaZIP is a simple C++ wrapper over Gilles Vollant's ZIP/UNZIP package that
can be used to access ZIP archives. It uses Trolltech's Qt toolkit.

QuaZIP allows you to access files inside ZIP archives using QIODevice API,
and - yes! - that means that you can also use QTextStream, QDataStream or
whatever you would like to use on your zipped files.

QuaZIP provides complete abstraction of the ZIP/UNZIP API, for both reading
from and writing to ZIP archives.

%package qt6-devel
Summary:	Development files for %{name}-qt6
%if !0%{?os2_version}
Requires:	%{name}-qt6%{?_isa} = %{version}-%{release}
Requires:	bzip2-devel%{?_isa}
Requires:	qt6-qtbase-devel%{?_isa}
Requires:	qt6-qt5compat-devel%{?_isa}
Requires:	zlib-devel%{?_isa}
%else
Requires:	%{name}-qt6 = %{version}-%{release}
Requires:	bzip2-devel
Requires:	qt6-qtbase-devel
Requires:	qt6-qt5compat-devel
Requires:	zlib-devel
%endif

%description qt6-devel
The %{name}-qt6-devel package contains libraries, header files and documentation
for developing applications that use %{name}-qt6.
%endif


%prep
%if !0%{?os2_version}
%autosetup -p1
%else
%scm_setup
%endif

%build
%if 0%{?os2_version}
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx -lpthread -fstack-protector"
export VENDOR="%{vendor}"
%endif

%if %{with qt4}
%global _vpath_builddir build-qt4
%cmake -DQUAZIP_QT_MAJOR_VERSION=4 -DQUAZIP_ENABLE_TESTS=ON
%cmake_build
%endif

%if %{with qt5}
%global _vpath_builddir build-qt5
%cmake -DQUAZIP_QT_MAJOR_VERSION=5 -DQUAZIP_ENABLE_TESTS=ON
%cmake_build
%endif

%if %{with qt6}
%global _vpath_builddir build-qt6
%cmake -DQUAZIP_QT_MAJOR_VERSION=6 -DQUAZIP_ENABLE_TESTS=ON
%cmake_build
%endif

doxygen Doxyfile
for file in doc/html/*; do
	touch -r Doxyfile $file
done

%install
%if %{with qt4}
%global _vpath_builddir build-qt4
%cmake_install
%endif

%if %{with qt5}
%global _vpath_builddir build-qt5
%cmake_install
%endif

%if %{with qt6}
%global _vpath_builddir build-qt6
%cmake_install
%endif

%if !0%{?os2_version}
# Create compat symlinks/files so that packages that use the old (pre-1.0)
# library location, include paths, or CMake module still build against the
# devel package. Note that the resulting binaries will refer to the new
# library name, though.
#
# These symlinks should probably be removed once all dependent packages are
# switched to use the new pkgconfig or CMake modules.
%if %{with qt4}
ln -s libquazip1-qt4.so %{buildroot}%{_libdir}/libquazip.so

install -d %{buildroot}%{_includedir}/quazip
pushd %{buildroot}%{_includedir}/QuaZip-Qt4-%{version}/quazip
for f in *; do
	ln -s ../QuaZip-Qt4-%{version}/quazip/$f %{buildroot}%{_includedir}/quazip/$f
done
popd

install -d %{buildroot}%{_datadir}/cmake/Modules
install -pm 0644 %{SOURCE1} %{buildroot}%{_datadir}/cmake/Modules/FindQuaZip.cmake
%endif

%if %{with qt5}
ln -s libquazip1-qt5.so %{buildroot}%{_libdir}/libquazip5.so

install -d %{buildroot}%{_includedir}/quazip5
pushd %{buildroot}%{_includedir}/QuaZip-Qt5-%{version}/quazip
for f in *; do
	ln -s ../QuaZip-Qt5-%{version}/quazip/$f %{buildroot}%{_includedir}/quazip5/$f
done
popd

install -d %{buildroot}%{_datadir}/cmake/Modules
install -pm 0644 %{SOURCE1} %{buildroot}%{_datadir}/cmake/Modules/FindQuaZip5.cmake
%endif
%endif

%if %{with test}
%check
# Qt4 uses the locale rather than libicu to determine file name encoding.
# Thus we need to force a UTF-8 locale, otherwise the tests will fail
# under Qt4.
# https://github.com/stachenov/quazip/issues/127
export LC_ALL=C.UTF-8
# In some emulated environments (such as the s390x mock chroot emulated
# on x86_64) the regexp JIT is broken, so turn it off to avoid incorrect
# test failures.
export QT_ENABLE_REGEXP_JIT=0

%if %{with qt4}
%global _vpath_builddir build-qt4
%ctest
%endif

%if %{with qt5}
%global _vpath_builddir build-qt5
%ctest
%endif

%if %{with qt6}
%global _vpath_builddir build-qt6
%ctest
%endif
%endif


%if %{with qt4}
%files
%doc NEWS.txt README.md
%license COPYING
%if !0%{?os2_version}
%{_libdir}/libquazip1-qt4.so.%{QUAZIP_LIB_VERSION}
%{_libdir}/libquazip1-qt4.so.%{QUAZIP_LIB_SOVERSION}
%else
%{_libdir}/quazq414.dll
%endif

%files devel
%doc doc/html
%{_includedir}/QuaZip-Qt4-%{version}/
%if !0%{?os2_version}
%{_libdir}/libquazip1-qt4.so
%else
%{_libdir}/quazip1-qt4.so
%endif
%{_libdir}/cmake/QuaZip-Qt4-%{version}/
%{_libdir}/pkgconfig/quazip1-qt4.pc
%if !0%{?os2_version}
# pre-1.0 compat files
%{_includedir}/quazip/
%{_libdir}/libquazip.so
%{_datadir}/cmake/Modules/FindQuaZip.cmake
%endif
%endif

%if %{with qt5}
%files qt5
%doc NEWS.txt README.md
%license COPYING
%if !0%{?os2_version}
%{_libdir}/libquazip1-qt5.so.%{QUAZIP_LIB_VERSION}
%{_libdir}/libquazip1-qt5.so.%{QUAZIP_LIB_SOVERSION}
%else
%{_libdir}/quazq514.dll
%endif

%files qt5-devel
%doc doc/html
%{_includedir}/QuaZip-Qt5-%{version}/
%if !0%{?os2_version}
%{_libdir}/libquazip1-qt5.so
%else
%{_libdir}/quazip1-qt5_dll.a
%endif
%{_libdir}/cmake/QuaZip-Qt5-%{version}/
%{_libdir}/pkgconfig/quazip1-qt5.pc
%if !0%{?os2_version}
# pre-1.0 compat files
%{_includedir}/quazip5/
%{_libdir}/libquazip5.so
%{_datadir}/cmake/Modules/FindQuaZip5.cmake
%endif
%endif

%if %{with qt6}
%files qt6
%doc NEWS.txt README.md
%license COPYING
%if !0%{?os2_version}
%{_libdir}/libquazip1-qt6.so.%{QUAZIP_LIB_VERSION}
%{_libdir}/libquazip1-qt6.so.%{QUAZIP_LIB_SOVERSION}
%else
%{_libdir}/quazq614.dll
%endif

%files qt6-devel
%doc doc/html
%{_includedir}/QuaZip-Qt6-%{version}/
%if !0%{?os2_version}
%{_libdir}/libquazip1-qt6.so
%else
%{_libdir}/quazip1-qt6_dll.a
%endif
%{_libdir}/cmake/QuaZip-Qt6-%{version}/
%{_libdir}/pkgconfig/quazip1-qt6.pc
%endif


%changelog
* Wed May 08 2024 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.4-1
- first OS/2 rpm
