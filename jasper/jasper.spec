
# NOTE: packages that can use jasper:
# ImageMagick
# netpbm

Summary: Implementation of the JPEG-2000 standard, Part 1
Name:    jasper
Version: 4.2.8
Release: 1%{?dist}

License: JasPer-2.0
%if 0%{?os2_version}
Vendor:         TeLLie OS2 forever
Distribution:   OS/2
Packager:       TeLLeRBoP
%endif
URL:     http://www.ece.uvic.ca/~frodo/jasper/
%if !0%{?os2_version}
Source0: https://github.com/jasper-software/%{name}/archive/refs/tags/version-%{version}.tar.gz
%else
%scm_source github https://github.com/Tellie/%{name}-os2 %{version}-os2
%endif

%if !0%{?os2_version}
# architecture related patches
Patch100: jasper-2.0.2-test-ppc64-disable.patch
Patch101: jasper-2.0.2-test-ppc64le-disable.patch
Patch102: jasper-4.1.0-test-i686-disable.patch
%endif

# autoreconf
BuildRequires: cmake
%if !0%{?os2_version}
BuildRequires: freeglut-devel 
BuildRequires: libGLU-devel
BuildRequires: mesa-libGL-devel
BuildRequires: libXmu-devel libXi-devel
%endif
BuildRequires: pkgconfig doxygen
BuildRequires: libjpeg-devel


Requires: %{name}-libs%{?_isa} = %{version}-%{release}
BuildRequires: gcc
BuildRequires: make

%description
This package contains an implementation of the image compression
standard JPEG-2000, Part 1. It consists of tools for conversion to and
from the JP2 and JPC formats.

%package devel
Summary: Header files, libraries and developer documentation
Provides: libjasper-devel = %{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: libjpeg-devel
Requires: pkgconfig
%description devel
%{summary}.

%package libs
Summary: Runtime libraries for %{name}
Conflicts: jasper < 1.900.1-4
%description libs
%{summary}.

%package utils
Summary: Nonessential utilities for %{name}
Requires: %{name} = %{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
%description utils
%{summary}, including jiv and tmrdemo.


%prep
%if !0%{?os2_version}
%setup -q -n %{name}-version-%{version}
%else
%scm_setup
%endif

%if !0%{?os2_version}
patch 1 -p1 -b .-rpath

# Need to disable one test to be able to build it on ppc64 arch
# At ppc64 this test just stuck (nothing happend - no exception or error)

%if "%{_arch}" == "ppc64"
%patch 100 -p1 -b .test-ppc64-disable
%endif

# Need to disable two tests to be able to build it on ppc64le arch
# At ppc64le this tests just stuck (nothing happend - no exception or error)

%if "%{_arch}" == "ppc64le"
%patch 101 -p1 -b .test-ppc64le-disable
%endif

%ifarch %ix86
%patch102 -p1 -b .test-i686-disable
%endif
%endif

%if 0%{?os2_version}
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp" 
export LIBS="-lcx -lpthread"
%endif
%cmake \
  -DJAS_ENABLE_DOC:BOOL=OFF \
  -DALLOW_IN_SOURCE_BUILD:BOOL=ON \

%cmake_build 


%install
%cmake_install

# Unpackaged files
rm -f doc/README
rm -f %{buildroot}%{_libdir}/lib*.la


%check
%ctest 

%if !0%{?os2_version}
%ldconfig_scriptlets libs
%endif

%files
%if !0%{?os2_version}
%{_bindir}/imgcmp
%{_bindir}/imginfo
%{_bindir}/jasper
%else
%{_bindir}/imgcmp.exe
%{_bindir}/imginfo.exe
%{_bindir}/jasper.exe
%endif
%{_mandir}/man1/img*
%{_mandir}/man1/jasper.1*
%{_docdir}/JasPer/*

%files devel
%doc doc/*
%{_includedir}/jasper/
%if !0%{?os2_version}
%{_libdir}/libjasper.so
%else
%{_libdir}/*_dll.a
%endif
%{_libdir}/pkgconfig/jasper.pc

%files libs
%doc README.md
%license COPYRIGHT.txt LICENSE.txt
%if !0%{?os2_version}
%{_libdir}/libjasper.so.7*
%else
%{_libdir}/*.dll
%endif

%files utils
%if !0%{?os2_version}
%{_bindir}/jiv
%{_mandir}/man1/jiv.1*
%endif

%changelog
* Fri Dec 05 2025 Elbert Pol <elbert.pol@gmail.com> - 4.2.8-1
- Updated to latest version
- Sync with latest fedora spec file

* Sat Aug 17 2024  Elbert Pol <elbert.pol@gmail.com> - 4.2.4-1
- Updated to latest source
- Add info to the lib file

* Tue Dec 26 2023 Elbert Pol <elbert.pol@gmail.com> - 4.1.1-1
- Updated to latest version
- Disable utils, as jiv required opengl and glut

* Sat Apr 09 2022 Elbert Pol <elbert.pol@gmail.com> - 3.0.3-1
- Updated to latest version

* Fri Oct 08 2021 Elbert Pol <elbert.pol@gmail.com> - 2.0.33-1
- Updated to latest version

* Fri Feb 26 2021 Elbert Pol <elbert.pol@gmail.com> - 2.0.25-1
- Updated to latest version 2.0.25

* Thu Jan 07 2021 Elbert Pol <elbert.pol@gmail.com> - 2.0.24-1
- Updated to latest version 2.0.24

* Sat Oct 17 2020 Elbert Pol <elbert.pol@gmail.com> - 2.0.22-1
- Updated to latest version 2.0.22
- Change more os2 specifated lines in spec file

* Fri Dec 28 2018 Elbert Pol <elbert.pol@gmail.com>  - 2.0.14-2
- Removed the dll from bindir

* Thu Dec 27 2018 Elbert Pol <elbert.pol@gmail.com>  - 2.0.14-1
- First Rpm for OS/2
