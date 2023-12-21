Name:           libjpeg-turbo
Version:        3.0.1
Release:        1%{?dist}
Summary:        A MMX/SSE2/SIMD accelerated library for manipulating JPEG image files
License:        IJG
URL:            http://sourceforge.net/projects/libjpeg-turbo

%if !0%{?os2_version}
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Patch0:         libjpeg-turbo-cmake.patch
Patch1:         libjpeg-turbo-CET.patch
%else
Vendor:         bww bitwise works GmbH
%scm_source github https://github.com/bitwiseworks/%{name}-os2 %{version}-os2
# DEF files to create forwarders for the legacy package
Source10:       jpeg.def
%endif

BuildRequires:  gcc
BuildRequires:  cmake
BuildRequires:  libtool
BuildRequires:  nasm

%if !0%{?os2_version}
Obsoletes:      libjpeg < 6b-47
%else
Obsoletes:      libjpeg < 8d-3
%endif
# add provides (even if it not needed) to workaround bad packages, like
# java-1.6.0-openjdk (#rh607554) -- atkac
%if !0%{?os2_version}
Provides:       libjpeg = 6b-47%{?dist}
%if "%{?_isa}" != ""
Provides:       libjpeg%{_isa} = 6b-47%{?dist}
%endif
%else
Provides:       libjpeg = 8d-3%{?dist}
%endif

%description
The libjpeg-turbo package contains a library of functions for manipulating JPEG
images.

%package devel
Summary:        Headers for the libjpeg-turbo library
%if !0%{?os2_version}
Obsoletes:      libjpeg-devel < 6b-47
Provides:       libjpeg-devel = 6b-47%{?dist}
%if "%{?_isa}" != ""
Provides:       libjpeg-devel%{_isa} = 6b-47%{?dist}
%endif
Requires:       libjpeg-turbo%{?_isa} = %{version}-%{release}
%else
Obsoletes:      libjpeg-devel < 8d-3
Provides:       libjpeg-devel = 8d-3%{?dist}
Requires:       libjpeg-turbo = %{version}-%{release}
%endif
Obsoletes:      libjpeg-turbo-static < 1.3.1
Provides:       libjpeg-turbo-static = 1.3.1%{?dist}

%description devel
This package contains header files necessary for developing programs which will
manipulate JPEG files using the libjpeg-turbo library.

%package utils
Summary:        Utilities for manipulating JPEG images
%if !0%{?os2_version}
Requires:       libjpeg-turbo%{?_isa} = %{version}-%{release}
%else
Requires:       libjpeg-turbo = %{version}-%{release}
%endif

%description utils
The libjpeg-turbo-utils package contains simple client programs for accessing
the libjpeg functions. It contains cjpeg, djpeg, jpegtran, rdjpgcom and
wrjpgcom. Cjpeg compresses an image file into JPEG format. Djpeg decompresses a
JPEG file into a regular image file. Jpegtran can perform various useful
transformations on JPEG files. Rdjpgcom displays any text comments included in a
JPEG file. Wrjpgcom inserts text comments into a JPEG file.

%package -n turbojpeg
Summary:        TurboJPEG library

%description -n turbojpeg
The turbojpeg package contains the TurboJPEG shared library.

%package -n turbojpeg-devel
Summary:        Headers for the TurboJPEG library
%if !0%{?os2_version}
Requires:       turbojpeg%{?_isa} = %{version}-%{release}
%else
Requires:       turbojpeg = %{version}-%{release}
%endif

%description -n turbojpeg-devel
This package contains header files necessary for developing programs which will
manipulate JPEG files using the TurboJPEG library.

%if 0%{?os2_version}
%debug_package
%endif

%prep
%if !0%{?os2_version}
%autosetup -p1
%else
%scm_setup

# Prepare forwarder DLLs.
for m in %{SOURCE10}; do
  cp ${m} .
done
%endif

%build
# NASM object files are missing GNU Property note for Intel CET,
# force it on the resulting library
%ifarch %{ix86} x86_64
export LDFLAGS="$RPM_LD_FLAGS -Wl,-z,ibt -Wl,-z,shstk"
%endif
%if 0%{?os2_version}
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"
export VENDOR="%{vendor}"
%endif

%{cmake} -DCMAKE_SKIP_RPATH:BOOL=YES \
         -DCMAKE_SKIP_INSTALL_RPATH:BOOL=YES \
%ifarch s390x
         -DFLOATTEST:STRING="fp-contract" \
%endif
%if !0%{?os2_version}
         -DENABLE_STATIC:BOOL=NO
%else
         -DENABLE_STATIC:BOOL=NO \
         -DWITH_JPEG8:BOOL=YES
%endif

%cmake_build

%install
%cmake_install
find %{buildroot} -name "*.la" -delete

%if 0%{?os2_version}
# Generate & install forwarder DLLs.
gcc -Zomf -Zdll -nostdlib jpeg.def -l$RPM_BUILD_ROOT/%{_libdir}/jpeg8.dll -lend -o $RPM_BUILD_ROOT/%{_libdir}/jpeg.dll
%endif

# Fix perms
chmod -x README.md

# multilib header hack
# we only apply this to known Red Hat multilib arches, per bug #1264675
case `uname -i` in
  i386 | ppc | s390 | sparc )
    wordsize="32"
    ;;
  x86_64 | ppc64 | s390x | sparc64 )
    wordsize="64"
    ;;
  *)
    wordsize=""
    ;;
esac

if test -n "$wordsize"
then
  mv $RPM_BUILD_ROOT%{_includedir}/jconfig.h \
     $RPM_BUILD_ROOT%{_includedir}/jconfig-$wordsize.h

  cat >$RPM_BUILD_ROOT%{_includedir}/jconfig.h <<EOF
#ifndef JCONFIG_H_MULTILIB
#define JCONFIG_H_MULTILIB

#include <bits/wordsize.h>

#if __WORDSIZE == 32
# include "jconfig-32.h"
#elif __WORDSIZE == 64
# include "jconfig-64.h"
#else
# error "unexpected value for __WORDSIZE macro"
#endif

#endif
EOF

fi

%check
%if !0%{?os2_version}
export LD_LIBRARY_PATH=%{buildroot}%{_libdir}
%else
# this export is needed, as else the dll for the tests are not found
export BEGINLIBPATH=%{_builddir}/%{buildsubdir}
%endif
%ctest

%if !0%{?os2_version}
%ldconfig_scriptlets
%ldconfig_scriptlets -n turbojpeg
%endif

%files
%license LICENSE.md
%doc README.md README.ijg ChangeLog.md
%if !0%{?os2_version}
%{_libdir}/libjpeg.so.62*
%else
%{_libdir}/jpeg*.dll
%endif

%files devel
%doc coderules.txt jconfig.txt libjpeg.txt structure.txt example.c
%{_includedir}/jconfig*.h
%{_includedir}/jerror.h
%{_includedir}/jmorecfg.h
%{_includedir}/jpegint.h
%{_includedir}/jpeglib.h
%if !0%{?os2_version}
%{_libdir}/libjpeg.so
%else
%{_libdir}/jpeg*_dll.a
%endif
%{_libdir}/pkgconfig/libjpeg.pc
%{_libdir}/cmake/%{name}/%{name}*.cmake

%files utils
%doc usage.txt wizard.txt
%if !0%{?os2_version}
%{_bindir}/cjpeg
%{_bindir}/djpeg
%{_bindir}/jpegtran
%{_bindir}/rdjpgcom
%{_bindir}/wrjpgcom
%else
%{_bindir}/cjpeg.exe
%{_bindir}/djpeg.exe
%{_bindir}/jpegtran.exe
%{_bindir}/rdjpgcom.exe
%{_bindir}/wrjpgcom.exe
%endif
%{_mandir}/man1/cjpeg.1*
%{_mandir}/man1/djpeg.1*
%{_mandir}/man1/jpegtran.1*
%{_mandir}/man1/rdjpgcom.1*
%{_mandir}/man1/wrjpgcom.1*

%files -n turbojpeg
%license LICENSE.md
%doc README.md README.ijg ChangeLog.md
%if !0%{?os2_version}
%{_libdir}/libturbojpeg.so.0*
%else
%{_libdir}/turbo*.dll
%endif

%files -n turbojpeg-devel
%doc tjexample.c
%{_includedir}/turbojpeg.h
%if !0%{?os2_version}
%{_libdir}/libturbojpeg.so
%else
%{_libdir}/turbo*_dll.a
%endif
%{_libdir}/pkgconfig/libturbojpeg.pc

%changelog
* Thu Dec 21 2023 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.0.1-1
- update version to 2.1.4

* Fri Jan 13 2023 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.1.4-1
- update version to 2.1.4
- merged spec to fedora version

* Mon Sep 30 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.0.3-1
- update version to 2.0.3

* Fri May 12 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.5.1-1
- Initial version
