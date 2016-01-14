Summary: Library of functions for manipulating TIFF format image files
Name: libtiff
Version: 4.0.6
Release: 1%{?dist}

License: libtiff
Group: System Environment/Libraries
URL: http://www.remotesensing.org/libtiff/
Vendor:	bww bitwise works GmbH

#define svn_url	    e:/trees/libtiff/trunk
%define svn_url     http://svn.netlabs.org/repos/ports/libtiff/trunk
%define svn_rev     1251

Source: %{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip

BuildRequires: zlib-devel libjpeg-devel pkgconfig
BuildRequires: libtool automake autoconf

# @todo Temporary enforce dependency on the legacy package 
# to have it installed. This should be dropped at some point.
Requires: libtiff-legacy

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
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

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
Requires: %{name}-devel = %{version}-%{release}

%description static
The libtiff-static package contains the statically linkable version of libtiff.
Linking to static libraries is discouraged for most applications, but it is
necessary for some boot packages.

%package tools
Summary: Command-line utility programs for manipulating TIFF files
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description tools
This package contains command-line programs for manipulating TIFF format
image files using the libtiff library.

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

# Use build system's libtool.m4, not the one in the package.
autogen.sh

%build
export LDFLAGS="-Zbin-files -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export CFLAGS="%{optflags} -fno-strict-aliasing"
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

# remove what we didn't want installed
rm $RPM_BUILD_ROOT%{_libdir}/*.la
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/

# no libGL dependency, please
rm -f $RPM_BUILD_ROOT%{_bindir}/tiffgt
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/tiffgt.1
rm -f html/man/tiffgt.1.html

# no sgi2tiff or tiffsv, either
rm -f $RPM_BUILD_ROOT%{_bindir}/sgi2tiff
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/sgi2tiff.1
rm -f html/man/sgi2tiff.1.html
rm -f $RPM_BUILD_ROOT%{_bindir}/tiffsv
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/tiffsv.1
rm -f html/man/tiffsv.1.html


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,0755)
%doc COPYRIGHT README RELEASE-DATE VERSION
%{_libdir}/tiff*.dll

%files devel
%defattr(-,root,root,0755)
%doc TODO ChangeLog html
%{_includedir}/*
%{_libdir}/tiff*_dll.a
%{_libdir}/tiffxx*_dll.a
%{_libdir}/pkgconfig/libtiff-4.pc
%{_mandir}/man3/*

%files static
%defattr(-,root,root,0755)
%{_libdir}/*.a

%files tools
%defattr(-,root,root,0755)
%{_bindir}/*.exe
%{_mandir}/man1/*

%changelog
* Wed Jan 13 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> 4.0.6-1
- updated source to 4.0.6 version
- adjusted debug package creation to latest rpm macros

* Thu Apr 17 2014 yd
- first public build.
