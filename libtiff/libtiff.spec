Summary:       Library of functions for manipulating TIFF format image files
Name:          libtiff
Version:       4.7.0
Release:       1%{?dist}
License:       libtiff
URL:           http://www.simplesystems.org/libtiff/

%if !0%{?os2_version}
Source:        http://download.osgeo.org/libtiff/tiff-%{version}.tar.gz
#from upstream, for <=4.7.0, fix s390x test failure, upstream issue #652
Patch1:        libsndfile-1.2.2-fixdirectorytest.patch
%else
Vendor:        bww bitwise works GmbH
%scm_source  github https://github.com/bitwiseworks/libtiff-os2 %{version}-os2
%endif

BuildRequires: gcc, gcc-c++
%if !0%{?os2_version}
BuildRequires: zlib-devel libjpeg-devel jbigkit-devel libzstd-devel libwebp-devel liblerc-devel
%else
BuildRequires: zlib-devel libjpeg-devel jbigkit-devel libzstd-devel libwebp-devel
%endif
BuildRequires: libtool automake autoconf pkgconfig
%if 0%{?fedora} == 40
# Add old libtiff to work with packages not built with new libtiff.so.6
BuildRequires: libtiff
%endif
BuildRequires: make

%description
The libtiff package contains a library of functions for manipulating
TIFF (Tagged Image File Format) image format files.  TIFF is a widely
used file format for bitmapped images.  TIFF files usually end in the
.tif extension and they are often quite large.

The libtiff package should be installed if you need to manipulate TIFF
format image files.

%package devel
Summary:       Development tools for programs which will use the libtiff library
%if !0%{?os2_version}
Requires:      %{name}%{?_isa} = %{version}-%{release}
%else
Requires:      %{name} = %{version}-%{release}
%endif
Requires:      pkgconfig
%if 0%{?os2_version}
Obsoletes:     %{name}-legacy-devel
%endif

%description devel
This package contains the header files and documentation necessary for
developing programs which will manipulate TIFF format image files
using the libtiff library.

If you need to develop programs which will manipulate TIFF format
image files, you should install this package.  You'll also need to
install the libtiff package.

%package static
Summary:     Static TIFF image format file library
%if !0%{?os2_version}
Requires:    %{name}-devel%{?_isa} = %{version}-%{release}
%else
Requires:    %{name}-devel = %{version}-%{release}
Obsoletes:   %{name}-legacy-static
%endif

%description static
The libtiff-static package contains the statically linkable version of libtiff.
Linking to static libraries is discouraged for most applications, but it is
necessary for some boot packages.

%package tools
Summary:    Command-line utility programs for manipulating TIFF files
%if !0%{?os2_version}
Requires:   %{name}%{?_isa} = %{version}-%{release}
%else
Requires:   %{name} = %{version}-%{release}
Obsoletes:  %{name}-legacy-tools
%endif

%description tools
This package contains command-line programs for manipulating TIFF format
image files using the libtiff library.

%if 0%{?os2_version}
%legacy_runtime_packages

%debug_package
%endif

%prep
%if !0%{?os2_version}
%autosetup -n tiff-%{version} -N
%patch -P 1 -p1 -b .fixdirtest
%else
%scm_setup
%endif

# Use build system's libtool.m4, not the one in the package.
rm -f libtool.m4

libtoolize --force  --copy
aclocal -I . -I m4
automake --add-missing --copy
autoconf
autoheader

%build
%if 0%{?os2_version}
export VENDOR="%{vendor}"
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
%endif
export CFLAGS="%{optflags} -fno-strict-aliasing"
%configure --enable-ld-version-script
%make_build

%install
%make_install

# remove what we didn't want installed
rm $RPM_BUILD_ROOT%{_libdir}/*.la
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/

# no libGL dependency, please
rm -f $RPM_BUILD_ROOT%{_bindir}/tiffgt

# no sgi2tiff or tiffsv, either
rm -f $RPM_BUILD_ROOT%{_bindir}/sgi2tiff
rm -f $RPM_BUILD_ROOT%{_bindir}/tiffsv

rm -f $RPM_BUILD_ROOT%{_mandir}/man1/tiffgt.1
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/sgi2tiff.1
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/tiffsv.1

%if !0%{?os2_version}
# multilib header hack
# we only apply this to known Red Hat multilib arches, per bug #233091
case `uname -m` in
  i?86 | ppc | s390 | sparc )
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
  mv $RPM_BUILD_ROOT%{_includedir}/tiffconf.h \
     $RPM_BUILD_ROOT%{_includedir}/tiffconf-$wordsize.h

  cat >$RPM_BUILD_ROOT%{_includedir}/tiffconf.h <<EOF
#ifndef TIFFCONF_H_MULTILIB
#define TIFFCONF_H_MULTILIB

#include <bits/wordsize.h>

#if __WORDSIZE == 32
# include "tiffconf-32.h"
#elif __WORDSIZE == 64
# include "tiffconf-64.h"
#else
# error "unexpected value for __WORDSIZE macro"
#endif

#endif
EOF

fi

%if 0%{?fedora} == 40
# Copy old soname %{_libdir}/libtiff.so.5
# Copy old soname %{_libdir}/libtiffxx.so.5
cp %{_libdir}/libtiff.so.5* $RPM_BUILD_ROOT%{_libdir}
cp %{_libdir}/libtiffxx.so.5* $RPM_BUILD_ROOT%{_libdir}
%endif

%ldconfig_scriptlets
%endif

%check
%if !0%{?os2_version}
export LD_LIBRARY_PATH=$PWD:$LD_LIBRARY_PATH
%else
export BEGINLIBPATH=%{_builddir}/%{buildsubdir}/libtiff/.libs
%endif
if ! make check
then
  cat test/test-suite.log
  false
fi

%files
%license LICENSE.md
%doc README.md RELEASE-DATE VERSION
%if !0%{?os2_version}
%{_libdir}/libtiff.so.*
%{_libdir}/libtiffxx.so.*
%else
%{_libdir}/tiff*.dll
%exclude %{_libdir}/tiff.dll
%endif

%files devel
%doc TODO ChangeLog
%{_includedir}/*
%if !0%{?os2_version}
%{_libdir}/libtiff.so
%{_libdir}/libtiffxx.so
%else
%{_libdir}/tiff*_dll.a
%endif
%{_libdir}/pkgconfig/libtiff*.pc
%{_mandir}/man3/*

%files static
%{_libdir}/*.a
%if 0%{?os2_version}
%exclude %{_libdir}/*_dll.a
%endif

%files tools
%if !0%{?os2_version}
%{_bindir}/*
%else
%{_bindir}/*.exe
%endif
%{_mandir}/man1/*

%changelog
* Wed Apr 16 2025 Silvan Scherrer <silvan.scherrer@aroa.ch> 4.7.0-1
- update to version 4.7.0
- resync spec with fedora

* Mon Nov 27 2023 Silvan Scherrer <silvan.scherrer@aroa.ch> 4.6.0-1
- update to version 4.6.0
- resync spec with fedora

* Fri Dec 01 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 4.0.9-1
- enable jbig encoding
- updated source to 4.0.9 version

* Wed Feb 15 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 4.0.7-3
- obsolete devel, static and tools legacy rpm

* Tue Feb 14 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 4.0.7-2
- rebuild with changed legacy_runtime_packages macro

* Wed Feb 08 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 4.0.7-1
- updated source to 4.0.7 version
- join legazy package to the main with our new macro
- use the new scm_source and scm_setup macros
- add bldlevel info to the dll

* Wed Jan 13 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> 4.0.6-1
- updated source to 4.0.6 version
- adjusted debug package creation to latest rpm macros

* Thu Apr 17 2014 yd
- first public build.
