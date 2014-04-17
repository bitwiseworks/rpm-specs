Summary: A library of functions for manipulating PNG image format files
Name: libpng
Version: 1.6.10
Release: 1%{?dist}
License: zlib
Group: System Environment/Libraries
URL: http://www.libpng.org/pub/png/

# Note: non-current tarballs get moved to the history/ subdirectory,
# so look there if you fail to retrieve the version you want
Source0: ftp://ftp.simplesystems.org/pub/libpng/png/src/libpng16/libpng-%{version}.tar.xz

Patch0: libpng-os2.patch

BuildRequires: zlib-devel, pkgconfig
#BuildRequires: libtool, autoconf >= 2.65
#BuildRequires: automake

%description
The libpng package contains a library of functions for creating and
manipulating PNG (Portable Network Graphics) image format files.  PNG
is a bit-mapped graphics format similar to the GIF format.  PNG was
created to replace the GIF format, since GIF uses a patented data
compression algorithm.

Libpng should be installed if you need to manipulate PNG format image
files.

%package devel
Summary: Development tools for programs to manipulate PNG image format files
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: zlib-devel%{?_isa} pkgconfig%{?_isa}

%description devel
The libpng-devel package contains header files and documentation necessary
for developing programs using the PNG (Portable Network Graphics) library.

If you want to develop programs which will manipulate PNG image format
files, you should install libpng-devel.  You'll also need to install
the libpng package.

%package static
Summary: Static PNG image format file library
Group: Development/Libraries
Requires: %{name}-devel%{?_isa} = %{version}-%{release}

%description static
The libpng-static package contains the statically linkable version of libpng.
Linking to static libraries is discouraged for most applications, but it is
necessary for some boot packages.

%package tools
Summary: Tools for PNG image format file library
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description tools
The libpng-tools package contains tools used by the authors of libpng.

%package debug
Summary: HLL debug data for exception handling support.

%description debug
HLL debug data for exception handling support.

%prep
%setup -q
%patch0 -p1

%build
export CONFIG_SHELL="/@unixroot/usr/bin/sh.exe"
export LDFLAGS="-Zbin-files -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp" ; \
export LIBS="-lurpo -lmmap -lpthread" ; \
%configure
make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT install

cp -p .libs/*.dll %{buildroot}%{_libdir}
cp -p libpng*.a %{buildroot}%{_libdir}
cp -p libpng*.lib %{buildroot}%{_libdir}
rm %{buildroot}%{_libdir}/png*.a

# We don't ship .la files.
rm -rf $RPM_BUILD_ROOT%{_libdir}/*.la

%files
%doc libpng-manual.txt example.c README TODO CHANGES LICENSE
%{_libdir}/png*.dll
%{_mandir}/man5/*

%files devel
%{_bindir}/*.exe
%{_bindir}/*-config
%{_includedir}/*
%{_libdir}/libpng.a
%{_libdir}/libpng??.a
%{_libdir}/libpng??.lib
%{_libdir}/pkgconfig/libpng*.pc
%{_mandir}/man3/*

%files static
%{_libdir}/libpng*_s.a

%files tools
%{_bindir}/pngfix.exe

%files debug
%defattr(-,root,root)
%{_bindir}/*.dbg
%{_libdir}/*.dbg

%changelog
* Thu Apr 17 2014 yd
- first public build.
