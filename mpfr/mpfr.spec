Summary: A C library for multiple-precision floating-point computations
Name: mpfr
Version: 4.0.2
Release: 1%{?dist}
URL: http://www.mpfr.org/

License: LGPLv3+
BuildRequires: gmp-devel gcc

#Source0: http://www.mpfr.org/%{name}-%{version}/%{name}-%{version}.tar.xz
Vendor:	bww bitwise works GmbH
%scm_source github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2

%description
The MPFR library is a C library for multiple-precision floating-point
computations with "correct rounding". The MPFR is efficient and 
also has a well-defined semantics. It copies the good ideas from the 
ANSI/IEEE-754 standard for double-precision floating-point arithmetic 
(53-bit mantissa). MPFR is based on the GMP multiple-precision library.

%package devel
Summary: Development tools A C library for mpfr library
Requires: %{name} = %{version}-%{release}
Requires: gmp-devel

%description devel
The static libraries, header files and documentation for using the MPFR 
multiple-precision floating-point library in applications.

If you want to develop applications which will use the MPFR library,
you'll need to install the mpfr-devel package.  You'll also need to
install the mpfr package.

%package doc
Summary: Documentation for the MPFR library
License: GFDL
BuildArch: noarch

%description doc
Documentation for the MPFR library.

%legacy_runtime_packages

%debug_package

%prep
%scm_setup
autoreconf -fvi

%build
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"
%configure --disable-assert --disable-static

%if 0
# Get rid of undesirable hardcoded rpaths; workaround libtool reordering
# -Wl,--as-needed after all the libraries.
sed -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
    -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
    -e 's|CC="\(g..\)"|CC="\1 -Wl,--as-needed"|' \
    -i libtool
%endif

# Set BUILDLEVEL to be embedded to all DLLs built with Libtool.
export LT_BUILDLEVEL="@#%{vendor}:%{version}-%{release}#@##1## `LANG=C date +'%%d %%b %%Y %%H:%%M:%%S'`     `uname -n`::::0::"

make %{?_smp_mflags}

%install
%make_install
cp -p PATCHES README %{buildroot}%{_docdir}/%{name}
rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_infodir}/dir

#these go into licenses, not doc
rm -f %{buildroot}%{_docdir}/%{name}/COPYING
rm -f %{buildroot}%{_docdir}/%{name}/COPYING.LESSER

%check
export BEGINLIBPATH=%{buildroot}%{_libdir}
export LD_LIBRARY_PATH=%{buildroot}%{_libdir}
make check

%files
%license COPYING COPYING.LESSER
%{_docdir}/%{name}/BUGS
%{_docdir}/%{name}/NEWS
%{_docdir}/%{name}/PATCHES
%{_docdir}/%{name}/README
%{_libdir}/mpfr6.dll

%files devel
%{_libdir}/mpfr*_dll.a
%{_includedir}/mpfr.h
%{_includedir}/mpf2mpfr.h
%{_libdir}/pkgconfig/mpfr.pc

%files doc
%{_docdir}/%{name}/AUTHORS
%{_docdir}/%{name}/examples
%{_docdir}/%{name}/FAQ.html
%{_docdir}/%{name}/TODO
%{_infodir}/mpfr.info*

%changelog
* Wed Mar 11 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 4.0.2-1
- update to version 4.0.2
- add legacy dll
- reworked the spec

* Fri Dec 02 2011 yd
- build as dll

* Thu Dec 01 2011 yd
- build as static lib
