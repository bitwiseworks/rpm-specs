%define aprver 1

Summary: Apache Portable Runtime library
Name: apr
Version: 1.4.5
Release: 1%{?dist}
License: ASL 2.0
Group: System Environment/Libraries
URL: http://apr.apache.org/
Source0: http://www.apache.org/dist/apr/%{name}-%{version}.tar.bz2

Patch1: apr-os2.patch
Patch2: apr-1.2.2-locktimeout.patch
Patch3: apr-1.2.2-libdir.patch
Patch4: apr-1.2.7-pkgconf.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

#BuildRequires: autoconf, libtool, libuuid-devel, python
# To enable SCTP support
#BuildRequires: lksctp-tools-devel

%description
The mission of the Apache Portable Runtime (APR) is to provide a
free library of C data structures and routines, forming a system
portability layer to as many operating systems as possible,
including Unices, MS Win32, BeOS and OS/2.

%package devel
Group: Development/Libraries
Summary: APR library development kit
Conflicts: subversion-devel < 0.20.1-2
Requires: apr = %{version}-%{release}, pkgconfig

%description devel
This package provides the support files which can be used to 
build applications using the APR library.  The mission of the
Apache Portable Runtime (APR) is to provide a free library of 
C data structures and routines.

%prep
%setup -q
%patch1 -p1 -b .os2
%patch2 -p1 -b .locktimeout
%patch3 -p1 -b .libdir
%patch4 -p1 -b .pkgconf

%build
# regenerate configure script etc.
#./buildconf

# Forcibly prevent detection of shm_open (which then picks up but
# does not use -lrt).
#export ac_cv_search_shm_open=no

export CONFIG_SHELL="/@unixroot/usr/bin/sh.exe"
export LDFLAGS="-Zhigh-mem -Zargs-wild -Zargs-resp"
export LIBS="-lurpo -lmmap"

%configure \
        --includedir=%{_includedir}/apr-%{aprver} \
        --with-installbuilddir=%{_datadir}/apr-%{aprver}/build \
       "--cache-file=%{_topdir}/cache/%{name}-%{_target_cpu}.cache"
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/%{_datadir}/aclocal
install -m 644 build/find_apr.m4 $RPM_BUILD_ROOT/%{_datadir}/aclocal

# Trim exported dependecies
sed -ri '/^dependency_libs/{s,-l(uuid|crypt) ,,g}' \
      $RPM_BUILD_ROOT%{_libdir}/apr*.la
sed -ri '/^LIBS=/{s,-l(uuid|crypt) ,,g;s/  */ /g}' \
      $RPM_BUILD_ROOT%{_bindir}/apr-%{aprver}-config
sed -ri '/^Libs/{s,-l(uuid|crypt) ,,g}' \
      $RPM_BUILD_ROOT%{_libdir}/pkgconfig/apr-%{aprver}.pc

# Unpackaged files:
rm -f $RPM_BUILD_ROOT%{_libdir}/apr.exp \
      $RPM_BUILD_ROOT%{_libdir}/apr-*.la

# rename static library
mv $RPM_BUILD_ROOT%{_libdir}/apr-%{aprver}.lib $RPM_BUILD_ROOT%{_libdir}/apr-%{aprver}_s.lib
# import library
emximp -o $RPM_BUILD_ROOT%{_libdir}/apr-%{aprver}.lib $RPM_BUILD_ROOT%{_libdir}/apr-%{aprver}.dll
# add jlibtool
install -m 755 build/jlibtool.exe $RPM_BUILD_ROOT/%{_datadir}/apr-%{aprver}/build
sed -ri 's#LIBTOOL=./build/jlibtool#LIBTOOL=%{_datadir}/apr-%{aprver}/build/jlibtool.exe#' \
      $RPM_BUILD_ROOT%{_datadir}/apr-%{aprver}/build/apr_rules.mk


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc CHANGES LICENSE NOTICE
%{_libdir}/apr-%{aprver}.dll

%files devel
%defattr(-,root,root,-)
%doc docs/APRDesign.html docs/canonical_filenames.html
%doc docs/incomplete_types docs/non_apr_programs
%{_bindir}/apr-%{aprver}-config
%{_libdir}/apr-%{aprver}_s.lib
%{_libdir}/apr-%{aprver}.lib
%{_libdir}/pkgconfig/*.pc
%dir %{_datadir}/apr-%{aprver}
%dir %{_datadir}/apr-%{aprver}/build
%{_datadir}/apr-%{aprver}/build/*
%dir %{_includedir}/apr-%{aprver}
%{_includedir}/apr-%{aprver}/*.h
%{_datadir}/aclocal/*.m4

%changelog
* Fri Mar 02 2012 yd
- initial unixroot build.
