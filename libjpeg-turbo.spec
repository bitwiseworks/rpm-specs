Name:           libjpeg-turbo
Version:        1.5.1
Release:        1%{?dist}
Summary:        A MMX/SSE2/SIMD accelerated library for manipulating JPEG image files
License:        IJG
URL:            http://sourceforge.net/projects/libjpeg-turbo

Vendor:         bww bitwise works GmbH
%scm_source github https://github.com/bitwiseworks/%{name}-os2 %{version}-os2

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  nasm

Obsoletes:      libjpeg < 8d-3
# add provides (even if it not needed) to workaround bad packages, like
# java-1.6.0-openjdk (#rh607554) -- atkac
Provides:       libjpeg = 8d-3%{?dist}

%description
The libjpeg-turbo package contains a library of functions for manipulating JPEG
images.

%package devel
Summary:        Headers for the libjpeg-turbo library
Obsoletes:      libjpeg-devel < 8d-3
Provides:       libjpeg-devel = 8d-3%{?dist}
Requires:       libjpeg-turbo = %{version}-%{release}
Obsoletes:      libjpeg-turbo-static < 1.3.1
Provides:       libjpeg-turbo-static = 1.3.1%{?dist}

%description devel
This package contains header files necessary for developing programs which will
manipulate JPEG files using the libjpeg-turbo library.

%package utils
Summary:        Utilities for manipulating JPEG images
Requires:       libjpeg-turbo = %{version}-%{release}

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
Requires:       turbojpeg = %{version}-%{release}

%description -n turbojpeg-devel
This package contains header files necessary for developing programs which will
manipulate JPEG files using the TurboJPEG library.
%debug_package


%prep
%scm_setup

%build
autoreconf -vif

export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
export VENDOR="%{vendor}"
%configure --disable-static --enable-shared --with-jpeg8

# we need to tweak the libtool a bit, as else it's not building see also ticket #94
sed 's/emxexp \\$libobjs \\$convenience/emxexp \\$libobjs/' -i.bak libtool

make %{?_smp_mflags} V=1

%install
make install DESTDIR=%{buildroot}
find %{buildroot} -name "*.la" -delete

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
# this export is needed, as else the dll for the tests are not found
export BEGINLIBPATH=%{_builddir}/%{buildsubdir}/.libs
make test %{?_smp_mflags}

#post -p /sbin/ldconfig
#postun -p /sbin/ldconfig

#post -n turbojpeg -p /sbin/ldconfig
#postun -n turbojpeg -p /sbin/ldconfig

%files
%doc README.md README.ijg ChangeLog.md
%{_libdir}/jpeg*.dll

%files devel
%doc coderules.txt jconfig.txt libjpeg.txt structure.txt example.c
%{_includedir}/jconfig*.h
%{_includedir}/jerror.h
%{_includedir}/jmorecfg.h
%{_includedir}/jpeglib.h
%{_libdir}/jpeg*_dll.a
%{_libdir}/pkgconfig/libjpeg.pc

%files utils
%doc usage.txt wizard.txt
%{_bindir}/cjpeg.exe
%{_bindir}/djpeg.exe
%{_bindir}/jpegtran.exe
%{_bindir}/rdjpgcom.exe
%{_bindir}/wrjpgcom.exe
%{_mandir}/man1/cjpeg.1*
%{_mandir}/man1/djpeg.1*
%{_mandir}/man1/jpegtran.1*
%{_mandir}/man1/rdjpgcom.1*
%{_mandir}/man1/wrjpgcom.1*

%files -n turbojpeg
%{_libdir}/turbo*.dll

%files -n turbojpeg-devel
%{_includedir}/turbojpeg.h
%{_libdir}/turbo*_dll.a
%{_libdir}/pkgconfig/libturbojpeg.pc

%changelog
* Fri May 12 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.5.1-1
- Initial version
