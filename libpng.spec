Summary: A library of functions for manipulating PNG image format files
Name: libpng
Version: 1.6.21
Release: 3%{?dist}
License: zlib
Group: System Environment/Libraries
URL: http://www.libpng.org/pub/png/
Vendor: bww bitwise works GmbH
#define svn_url	    e:/trees/libpng/trunk
%define svn_url     http://svn.netlabs.org/repos/ports/libpng/trunk
%define svn_rev     1533

Source: %{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip

BuildRequires: zlib-devel, pkgconfig
BuildRequires: libtool, autoconf >= 2.65
BuildRequires: automake

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
Requires: %{name} = %{version}-%{release}
Requires: zlib-devel pkgconfig

%description devel
The libpng-devel package contains header files and documentation necessary
for developing programs using the PNG (Portable Network Graphics) library.

If you want to develop programs which will manipulate PNG image format
files, you should install libpng-devel.  You'll also need to install
the libpng package.

%package static
Summary: Static PNG image format file library
Group: Development/Libraries
Requires: %{name}-devel = %{version}-%{release}

%description static
The libpng-static package contains the statically linkable version of libpng.
Linking to static libraries is discouraged for most applications, but it is
necessary for some boot packages.

%package tools
Summary: Tools for PNG image format file library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description tools
The libpng-tools package contains tools used by the authors of libpng.

%debug_package

%prep
%if %{?svn_rev:%(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')}%{?!svn_rev):0}
%setup -q
%else
%setup -n "%{name}-%{version}" -Tc
svn export %{?svn_rev:-r %{svn_rev}} %{svn_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip" "%{name}-%{version}")
%endif

autoreconf -f -i

%build
export LDFLAGS=" -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"

%configure
make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT install

# We don't ship .la files
rm -rf $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc libpng-manual.txt example.c README TODO CHANGES LICENSE
%{_libdir}/png*.dll
%{_mandir}/man5/*

%files devel
%{_bindir}/*.exe
%exclude %{_bindir}/pngfix.exe
%{_bindir}/*-config
%{_includedir}/*
%{_libdir}/png*_dll.a
%{_libdir}/libpng_dll.a
%{_libdir}/pkgconfig/libpng*.pc
%{_mandir}/man3/*

%files static
%{_libdir}/png??.a
%{_libdir}/libpng.a

%files tools
%{_bindir}/pngfix.exe

%changelog
* Thu Apr 7 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.6.21-3
- added apng support
  used patch from https://sourceforge.net/projects/libpng-apng/files
- removed -Zbin-files, as not needed

* Fri Feb 26 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.6.21-2
- remove %{?_isa} macro

* Fri Feb 26 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.6.21-1
- updated libpng to 1.6.21
- adjusted debug package creation to latest rpm macros

* Tue Sep 15 2015 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.6.18-1
- updated libpng to 1.6.18

* Mon Feb 16 2015 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.6.16-1
- updated libpng to 1.6.16
- add symlink for libpng

* Tue Feb 10 2015 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.6.14-1
- updated libpng to 1.6.14
- added .dbg files

* Thu Apr 17 2014 yd
- first public build.
