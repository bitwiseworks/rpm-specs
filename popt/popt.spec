%define ver 1.18
#define snap rc1
%define srcver %{ver}%{?snap:-%{snap}}

Summary:        C library for parsing command line parameters
Name:           popt
Version:        %{ver}%{?snap:~%{snap}}
Release:        2%{?dist}
License:        MIT
URL:            https://github.com/rpm-software-management/popt/
%if !0%{?os2_version}
Source0:        http://ftp.rpm.org/popt/releases/popt-1.x/%{name}-%{srcver}.tar.gz
Patch0:		popt-1.18-ltname.patch
%else
Epoch:          1
Vendor:         bww bitwise works GmbH
%scm_source     github http://github.com/bitwiseworks/%{name}-os2 %{name}-%{version}-release-os2
# DEF files to create forwarders for the legacy package
Source10:       popt.def
Source11:       iconv.m4
Obsoletes:      popt-libs < %{epoch}:1.18-1
Provides:       popt-libs = %{epoch}:%{version}-%{release}
Obsoletes:      popt-data < %{epoch}:1.18-1
%endif
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  make

%description
Popt is a C library for parsing command line parameters. Popt was
heavily influenced by the getopt() and getopt_long() functions, but
it improves on them by allowing more powerful argument expansion.
Popt can parse arbitrary argv[] style arrays and automatically set
variables based on command line arguments. Popt allows command line
arguments to be aliased via configuration files and includes utility
functions for parsing arbitrary strings into argv[] arrays using
shell-like rules.

%package devel
Summary:        Development files for the popt library
%if !0%{?os2_version}
Requires:       %{name} = %{version}-%{release}, pkgconfig
%else
Requires:       %{name} = %{epoch}:%{version}-%{release}, pkgconfig
%endif

%description devel
The popt-devel package includes header files and libraries necessary
for developing programs which use the popt C library. It contains the
API documentation of the popt library, too.

%if 0%{!?_without_static:1}
%package static
Summary:        Static library for parsing command line parameters
%if !0%{?os2_version}
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}
%else
Requires:       %{name}-devel = %{epoch}:%{version}-%{release}
%endif

%description static
The popt-static package includes static libraries of the popt library.
Install it if you need to link statically with libpopt.
%endif

%if 0%{?os2_version}
%debug_package
%endif

%prep
%if !0%{?os2_version}
%autosetup -n %{name}-%{srcver} -p1
%else
%scm_setup

# Prepare forwarder DLLs.
cp %{SOURCE10} .

mkdir -p m4
cp %{SOURCE11} m4

autoreconf -vi
%endif

%build
%if 0%{?os2_version}
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"
export LIBS='-lcx -lpthread'
# Set BUILDLEVEL to be embedded to all DLLs built with Libtool.
export LT_BUILDLEVEL="@#%{vendor}:%{version}-%{release}#@##1## `LANG=C date +'%%d %%b %%Y %%H:%%M:%%S'`     `uname -n`::::0::"
%endif
%configure %{?_without_static:--disable-static}
%if !0%{?os2_version}
%make_build
%else
make %{?_smp_mflags}
%endif

%install
%make_install

# Don't install any libtool .la files
rm -f $RPM_BUILD_ROOT%{_libdir}/libpopt.la

# Multiple popt configurations are possible
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/popt.d/

%if 0%{?os2_version}
# Generate & install forwarder DLLs.
gcc -Zomf -Zdll -nostdlib %{SOURCE10} -l$RPM_BUILD_ROOT/%{_libdir}/popt0.dll -lend -o $RPM_BUILD_ROOT/%{_libdir}/popt.dll
%endif

%find_lang %{name}

%check
%if 0%{?os2_version}
# this export is needed, as else the dll for the tests are not found
export BEGINLIBPATH=%{_builddir}/%{buildsubdir}/src/.libs
%endif
make check || (cat tests/*.log; exit 1)

%if !0%{?os2_version}
%ldconfig_scriptlets
%endif

%files -f %{name}.lang
%license COPYING
%doc CHANGES
%{_sysconfdir}/popt.d/
%if !0%{?os2_version}
%{_libdir}/libpopt.so.*
%else
%{_libdir}/popt*.dll
%endif

%files devel
%doc README
%if !0%{?os2_version}
%{_libdir}/libpopt.so
%else
%{_libdir}/popt*_dll.a
%endif
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/popt.h
%{_mandir}/man3/popt.3*

%if 0%{!?_without_static:1}
%files static
%if !0%{?os2_version}
%{_libdir}/libpopt.a
%else
%{_libdir}/popt.a
%endif
%endif

%changelog
* Mon Sep 20 2021 Silvan Scherrer <silvan.scerrer@aroa.ch> 1.18-2
- obsolete and provide -libs and -data
- use epoch 1, as old spec had it

* Fri Sep 17 2021 Silvan Scherrer <silvan.scerrer@aroa.ch> 1.18-1
- update to version 1.18
- add a forwarder to the old popt.dll
- resync with fedora spec

* Tue Dec 08 2015 yd <yd@os2power.com> 1.15-5
- r1209, strip path and extension from programname.
- added debug package with symbolic info for exceptq.
