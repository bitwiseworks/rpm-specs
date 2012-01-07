Summary: A C library for multiple-precision floating-point computations
Name: mpfr
Version: 3.1.0
Release: 2%{?dist}
URL: http://www.mpfr.org/

Source0: http://www.mpfr.org/mpfr-current/%{name}-%{version}.tar.gz
Patch0: mpfr.diff

License: LGPLv2+ and GPLv2+ and GFDL
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
#BuildRequires: autoconf libtool gmp-devel
Requires: gmp >= 4.2.1

%description
The MPFR library is a C library for multiple-precision floating-point
computations with "correct rounding". The MPFR is efficient and 
also has a well-defined semantics. It copies the good ideas from the 
ANSI/IEEE-754 standard for double-precision floating-point arithmetic 
(53-bit mantissa). MPFR is based on the GMP multiple-precision library.

%package devel
Summary: Development tools A C library for mpfr library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
#Requires: gmp-devel

%description devel
The static libraries, header files and documentation for using the MPFR 
multiple-precision floating-point library in applications.

If you want to develop applications which will use the MPFR library,
you'll need to install the mpfr-devel package.  You'll also need to
install the mpfr package.

%prep
%setup -q
%patch0 -p1 -b .os2~

%build
export CONFIG_SHELL="/@unixroot/usr/bin/sh.exe"
%configure \
        --disable-shared --enable-static \
        --disable-assert \
        "--cache-file=%{_topdir}/cache/%{name}-%{_target_cpu}.cache"
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
#iconv  -f iso-8859-1 -t utf-8 mpfr.info >mpfr.info.aux
#mv mpfr.info.aux mpfr.info
make install DESTDIR=$RPM_BUILD_ROOT

cp -p src/mpfr.dll $RPM_BUILD_ROOT%{_libdir}
cp -p src/.libs/mpfr_s.a $RPM_BUILD_ROOT%{_libdir}

rm -f $RPM_BUILD_ROOT%{_libdir}/libmpfr.la
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
rm -f $RPM_BUILD_ROOT%{_libdir}/libmpfr.a
cd ..
mkdir $RPM_BUILD_ROOT/%{_docdir}/%{name}-%{version}
mv $RPM_BUILD_ROOT/%{_docdir}/%{name}/ $RPM_BUILD_ROOT/%{_docdir}/%{name}-%{version}/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc COPYING NEWS README
%{_libdir}/mpfr.dll

%files devel
%defattr(-,root,root,-)
%{_libdir}/mpfr*.a
%{_includedir}/*.h
%{_infodir}/mpfr.info*

%changelog
* Fri Dec 02 2011 yd
- build as dll

* Thu Dec 01 2011 yd
- build as static lib
