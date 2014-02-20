%define serfver 1

Summary:	A high-performance asynchronous HTTP client library
Name:		serf
Version:	1.2.1
Release:        5%{?dist}
License:	Apache License
Group:		System/Libraries
URL:		http://code.google.com/p/serf/
Source0:	http://serf.googlecode.com/files/%{name}-%{version}.tar.bz2
Source1:	serf-1.def
Patch1:         serf-os2.patch

BuildRequires:	apr-devel
BuildRequires:	apr-util-devel
#BuildRequires:	autoconf2.5
#BuildRequires:	automake
#BuildRequires:	libtool
BuildRequires:	openssl-devel
BuildRequires:	zlib-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The serf library is a C-based HTTP client library built upon the Apache
Portable Runtime (APR) library. It multiplexes connections, running the
read/write communication asynchronously. Memory copies and transformations are
kept to a minimum to provide high performance operation.

%package devel
Summary:	Development libraries and headers for %{name}
Group:		Development/C
Requires:	%{name} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description devel
The serf library is a C-based HTTP client library built upon the Apache
Portable Runtime (APR) library. It multiplexes connections, running the
read/write communication asynchronously. Memory copies and transformations are
kept to a minimum to provide high performance operation.

This package contains all of the development files that you will need in order
to compile %{name} applications.

%package debug
Summary: HLL debug data for exception handling support.

%description debug
HLL debug data for exception handling support.

%prep

%setup -q
%patch1 -p1 -b .os2

cp %{SOURCE1} .

# don't link against ldap libs
#perl -pi -e "s|apu_config --link-libtool --libs|apu_config --link-libtool --avoid-ldap --libs|g" configure*
# lib64 fix
#perl -pi -e "s|/lib\b|/%{_lib}|g" configure*
# no static builds
#perl -pi -e "s|-static||g" Makefile*

%build
export CONFIG_SHELL="/@unixroot/usr/bin/sh.exe"
export LDFLAGS="-Zhigh-mem -Zargs-wild -Zargs-resp"
export LIBS="-lurpo -lmmap"
%configure \
	--includedir=/@unixroot/usr/include/serf-1 \
       "--cache-file=%{_topdir}/cache/%{name}-%{_target_cpu}.cache"
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# add serf dir symlink for AOO
ln -s /@unixroot/usr/include/serf-1 $RPM_BUILD_ROOT/@unixroot/usr/include/serf

# Unpackaged files:
rm -f $RPM_BUILD_ROOT%{_libdir}/serf-*.la

# rename static library
mv $RPM_BUILD_ROOT%{_libdir}/serf-%{serfver}.lib $RPM_BUILD_ROOT%{_libdir}/serf-%{serfver}_s.lib
# import library
emximp -o $RPM_BUILD_ROOT%{_libdir}/serf-%{serfver}.lib $RPM_BUILD_ROOT%{_libdir}/serf-%{serfver}.dll

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc CHANGES LICENSE NOTICE README design-guide.txt
%attr(0755,root,root) %{_libdir}/serf*.dll
%exclude %{_libdir}/*.dbg

%files devel
%defattr(-,root,root)
%attr(0644,root,root) %{_includedir}/serf-1/*.h
%attr(0644,root,root) %{_includedir}/serf
%attr(0755,root,root) %{_libdir}/serf*.lib
%{_libdir}/pkgconfig/*.pc

%files debug
%defattr(-,root,root)
%{_libdir}/*.dbg

%changelog
* Thu Feb 20 2014 yd
- update source to release 1.2.1 (required for AOO 4.x)
- added debug package with symbolic info for exceptq.

* Wed Jun 27 2012 yd
- update source to release 1.1.0 (required for AOO 3.5.x)
- added missing export.

* Fri Mar 02 2012 yd
- added http://code.google.com/p/serf/issues/detail?id=68

* Fri Mar 02 2012 yd
- initial unixroot build.
