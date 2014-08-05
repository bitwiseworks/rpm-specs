
Name:           mpc
BuildRequires:  gmp-devel
BuildRequires:  mpfr-devel
Version:        1.0.1
Release:        3
Summary:        MPC multiple-precision complex shared library
License:        LGPL-3.0+
Group:          Development/Libraries/C and C++
Url:            http://www.multiprecision.org/mpc/
Source:         mpc-%{version}.tar.gz
Patch0:         mpc-os2.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
MPC is a C library for the arithmetic of complex numbers with
arbitrarily high precision and correct rounding of the result. It is
built upon and follows the same principles as MPFR.



%package -n libmpc3
Summary:        MPC multiple-precision complex shared library
Group:          Development/Libraries/C and C++

%description -n libmpc3
MPC is a C library for the arithmetic of complex numbers with
arbitrarily high precision and correct rounding of the result. It is
built upon and follows the same principles as MPFR.



%package devel
Summary:        MPC multiple-precision complex library development files
Group:          Development/Libraries/C and C++
Requires:       libmpc3 = %{version}
Requires:       mpfr-devel

%description devel
MPC multiple-precision complex library development files.



%prep
%setup -q
%patch0 -p1 -b .os2~

%build
export CONFIG_SHELL="/@unixroot/usr/bin/sh.exe"
%configure \
        --disable-shared --enable-static \
        "--cache-file=%{_topdir}/cache/%{name}-%{_target_cpu}.cache"
make %{?_smp_mflags}

%install
%makeinstall
rm $RPM_BUILD_ROOT%{_libdir}/libmpc.la

cp -p src/mpc.dll $RPM_BUILD_ROOT%{_libdir}
cp -p src/.libs/mpc_s.a $RPM_BUILD_ROOT%{_libdir}

%files -n libmpc3
%defattr(-,root,root)
%{_libdir}/mpc.dll

%files devel
%defattr(-,root,root)
%doc AUTHORS NEWS COPYING.LESSER
%doc %{_infodir}/*
%{_libdir}/mpc*.a
%{_includedir}/mpc.h

%changelog
* Thu Aug 05 2014 yd
- resolve dll conflict with devel package, fixes ticket#82.

* Wed Nov 20 2013 yd
- rebuild with newer gcc runtime.

* Sat Oct 26 2013 yd
- initial rpm build as dll.
