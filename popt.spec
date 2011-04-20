%define name popt
%define version 1.15

Summary:	C library for parsing command line parameters
Name:		%{name}
Version:	%{version}
Release:        3%{?dist}
Epoch:		1
License:	MIT
Group:		System/Libraries
Url:		http://rpm5.org/files/popt/
Source0:	http://rpm5.org/files/popt/%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

Patch0: popt-os2.diff

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

%prep
%setup -q
%patch0 -p1 -b .os2~

%build
CONFIG_SHELL="/bin/sh" ; export CONFIG_SHELL ; \
LDFLAGS="-Zbin-files -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp" ; export LDFLAGS ; \
%configure --disable-rpath \
    --disable-shared --enable-static \
    "--cache-file=%{_topdir}/cache/%{name}-%{_target_cpu}.cache"

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=${RPM_BUILD_ROOT} install
cp popt.dll $RPM_BUILD_ROOT/%{_libdir}
#%find_lang %name

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
#%{_libdir}/*.dll
%{_mandir}/man3/popt.*

%files data
# -f %{name}.lang
%defattr(-,root,root)
%{_datadir}/locale/*


%changelog
