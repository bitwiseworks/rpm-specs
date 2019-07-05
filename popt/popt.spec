#define svn_url     F:/rd/ports/popt/trunk
%define svn_url     http://svn.netlabs.org/repos/ports/popt/trunk
%define svn_rev     1209

%define name popt
%define version 1.15

Summary:	C library for parsing command line parameters
Name:		%{name}
Version:	%{version}
Release:        5%{?dist}
Epoch:		1
License:	MIT
Group:		System/Libraries
Url:		http://rpm5.org/files/popt/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Source: %{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip

Requires: popt-libs = %{epoch}:%{version}-%{release}
Requires: popt-data = %{epoch}:%{version}-%{release}

%description
Popt is a C library for parsing command line parameters. Popt was
heavily influenced by the getopt() and getopt_long() functions, but
it improves on them by allowing more powerful argument expansion.
Popt can parse arbitrary argv[] style arrays and automatically set
variables based on command line arguments. Popt allows command line
arguments to be aliased via configuration files and includes utility
functions for parsing arbitrary strings into argv[] arrays using
shell-like rules.

%package libs
Summary:	Main %{name} library
Group:		System/Libraries
Requires:	popt-data = %{epoch}:%{version}

%description libs
This package contains the library needed to run programs dynamically
linked with the %{name} library.

%package devel
Summary:	Development headers and libraries for %{name}
Group:		Development/C
Requires:	popt-libs >= %{epoch}:%{version}

%description devel
This package contains the header files and libraries needed for
developing programs using the %{name} library.

%package data
Summary:	Data files for %{name}
Group:		System/Libraries

%description data
This package contains popt data files like locales.

%package debug
Summary: HLL debug data for exception handling support.

%description debug
HLL debug data for exception handling support.

%prep
%if %{?svn_rev:%(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')}%{!?svn_rev):0}
%setup -q
%else
%setup -n "%{name}-%{version}" -Tc
svn export %{?svn_rev:-r %{svn_rev}} %{svn_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip" "%{name}-%{version}")
%endif

%build
export CONFIG_SITE="/@unixroot/usr/share/config.legacy";
export LDFLAGS="-Zbin-files -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp";
%configure --disable-rpath \
    --disable-shared --enable-static

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=${RPM_BUILD_ROOT} install
cp popt.dll $RPM_BUILD_ROOT/%{_libdir}
%find_lang %name

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README

%files libs
%defattr(-,root,root)
%doc README
%{_libdir}/*.dll

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}.h
%{_libdir}/%{name}*a
%{_libdir}/lib%{name}*a
%{_mandir}/man3/popt.*
%files data -f %{name}.lang

%files debug
%defattr(-,root,root)
%{_libdir}/*.dbg

%changelog
* Tue Dec 08 2015 yd <yd@os2power.com> 1.15-5
- r1209, strip path and extension from programname.
- added debug package with symbolic info for exceptq.
