Summary: Library of functions for manipulating TIFF format image files
Name: libtiff
Version: 3.9.5
Release: 1%{?dist}

License: libtiff
Group: System Environment/Libraries
URL: http://www.remotesensing.org/libtiff/

Source: ftp://ftp.remotesensing.org/pub/libtiff/tiff-%{version}.tar.gz

Patch0: libtiff-os2.patch

BuildRequires: zlib-devel libjpeg-devel pkgconfig
#BuildRequires: libtool automake autoconf jbigkit-devel

%description
The libtiff package contains a library of functions for manipulating
TIFF (Tagged Image File Format) image format files.  TIFF is a widely
used file format for bitmapped images.  TIFF files usually end in the
.tif extension and they are often quite large.

The libtiff package should be installed if you need to manipulate TIFF
format image files.

%package devel
Summary: Development tools for programs which will use the libtiff library
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: pkgconfig%{?_isa}

%description devel
This package contains the header files and documentation necessary for
developing programs which will manipulate TIFF format image files
using the libtiff library.

If you need to develop programs which will manipulate TIFF format
image files, you should install this package.  You'll also need to
install the libtiff package.

%package static
Summary: Static TIFF image format file library
Group: Development/Libraries
Requires: %{name}-devel%{?_isa} = %{version}-%{release}

%description static
The libtiff-static package contains the statically linkable version of libtiff.
Linking to static libraries is discouraged for most applications, but it is
necessary for some boot packages.

%package tools
Summary: Command-line utility programs for manipulating TIFF files
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description tools
This package contains command-line programs for manipulating TIFF format
image files using the libtiff library.

%package debug
Summary: HLL debug data for exception handling support.

%description debug
HLL debug data for exception handling support.

%prep
%setup -q -n tiff-%{version}
%patch0 -p1

# Use build system's libtool.m4, not the one in the package.
#rm -f libtool.m4
#libtoolize --force  --copy
#aclocal -I . -I m4
#automake --add-missing --copy
#autoconf
#autoheader

%build
export CONFIG_SHELL="/@unixroot/usr/bin/sh.exe"
export LDFLAGS="-Zbin-files -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp" ; \
export LIBS="-lurpo -lmmap -lpthread" ; \
export CFLAGS="%{optflags} -fno-strict-aliasing"
%configure
make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT install

cp -p libtiff/*.dll %{buildroot}%{_libdir}
cp -p libtiff/.libs/tiff.a %{buildroot}%{_libdir}
cp -p libtiff/.libs/tiff.lib %{buildroot}%{_libdir}
cp -p libtiff/.libs/tiff_s.a %{buildroot}%{_libdir}

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
#rm -f html/man/tiffgt.1.html
#rm -f html/man/sgi2tiff.1.html
#rm -f html/man/tiffsv.1.html


%files
%doc COPYRIGHT README RELEASE-DATE VERSION
%{_libdir}/tiff.dll

%files devel
%doc TODO ChangeLog html
%{_includedir}/*
%{_libdir}/tiff.a
%{_libdir}/tiff.lib
%{_libdir}/tiffxx.a
#%{_libdir}/pkgconfig/libtiff*.pc
%{_mandir}/man3/*

%files static
%{_libdir}/*.a

%files tools
%{_bindir}/*.exe
%{_mandir}/man1/*

%files debug
%defattr(-,root,root)
%{_bindir}/*.dbg
%{_libdir}/*.dbg

%changelog
* Thu Apr 17 2014 yd
- first public build.
