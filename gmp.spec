#
# Important for %{ix86}:
# This rpm has to be build on a CPU with sse2 support like Pentium 4 !
#

Summary: A GNU arbitrary precision library
Name: gmp
Version: 5.0.2
Release: 2%{?dist}
URL: http://gmplib.org/

Source0: ftp://ftp.gnu.org/pub/gnu/gmp/gmp-%{version}.tar.bz2
Patch0: gmp.diff

License: LGPLv3+
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
#BuildRequires: autoconf automake libtool

%description
The gmp package contains GNU MP, a library for arbitrary precision
arithmetic, signed integers operations, rational numbers and floating
point numbers. GNU MP is designed for speed, for both small and very
large operands. GNU MP is fast because it uses fullwords as the basic
arithmetic type, it uses fast algorithms, it carefully optimizes
assembly code for many CPUs' most common inner loops, and it generally
emphasizes speed over simplicity/elegance in its operations.

Install the gmp package if you need a fast arbitrary precision
library.

%package devel
Summary: Development tools for the GNU MP arbitrary precision library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
#Requires(post): /sbin/install-info
#Requires(preun): /sbin/install-info

%description devel
The libraries, header files and documentation for using the GNU MP 
arbitrary precision library in applications.

If you want to develop applications which will use the GNU MP library,
you'll need to install the gmp-devel package.  You'll also need to
install the gmp package.

%package static
Summary: Development tools for the GNU MP arbitrary precision library
Group: Development/Libraries
Requires: %{name}-devel = %{version}-%{release}

%description static
The static libraries for using the GNU MP arbitrary precision library 
in applications.

%prep
%setup -q 
%patch0 -p1 -b .os2~

%build
export CONFIG_SHELL="/@unixroot/usr/bin/sh.exe"
%configure \
	--host=none-pc-os2-emx --build=none-pc-os2-emx \
        --disable-shared --enable-static \
        "--cache-file=%{_topdir}/cache/%{name}-%{_target_cpu}.cache"
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

cp -p gmp.dll $RPM_BUILD_ROOT%{_libdir}
cp -p .libs/gmp_s.a $RPM_BUILD_ROOT%{_libdir}

install -m 644 gmp-mparam.h ${RPM_BUILD_ROOT}%{_includedir}
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.la
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc COPYING COPYING.LIB NEWS README
%{_libdir}/*.dll

%files devel
%defattr(-,root,root,-)
%{_libdir}/gmp.a
%{_includedir}/*.h
%{_infodir}/gmp.info*

%files static
%defattr(-,root,root,-)
%{_libdir}/gmp_s.a

%changelog
* Fri Dec 02 2011 yd
- build as dll

* Thu Dec 01 2011 yd
- build as static lib
