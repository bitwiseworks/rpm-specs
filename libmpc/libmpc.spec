# build compat-libmpc for bootstrapping purposes
%global bootstrap 0
%global bootstrap_version 0.9

Summary: C library for multiple precision complex arithmetic
Name: libmpc
Version: 1.1.0
Release: 1%{?dist}
License: LGPLv3+
URL: http://www.multiprecision.org/mpc/
#Source0: https://ftp.gnu.org/gnu/mpc/mpc-%{version}.tar.gz
%if 0%{?bootstrap}
Source1: https://ftp.gnu.org/gnu/mpc/mpc-%{bootstrap_version}.tar.gz
%endif

Vendor:	bww bitwise works GmbH
%scm_source github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2
# DEF files to create forwarders
Source10:       mpc.def

BuildRequires: gcc
BuildRequires: gmp-devel >= 5.0.0
BuildRequires: mpfr-devel

Obsoletes: libmpc3 
Provides: libmpc3 = %{version}-%{release}

%if 0%{?bootstrap} == 0
Obsoletes: compat-libmpc < %{version}-1
Provides: compat-libmpc = %{version}-%{release}
%endif

%description
MPC is a C library for the arithmetic of complex numbers with
arbitrarily high precision and correct rounding of the result. It is
built upon and follows the same principles as Mpfr.

%package devel
Summary:        MPC multiple-precision complex library development files
Requires: %{name} = %{version}-%{release}
Requires: gmp-devel
Requires: mpfr-devel

%description devel
Header files and shared library symlinks for the MPC library.

%package doc
Summary: Documentation for the MPC library
License: GFDL
BuildArch: noarch

%description doc
Documentation for the MPC library.

%if 0%{?bootstrap}
%package -n compat-libmpc
Summary: compat/bootstrap mpc-%{bootstrap_version} library

%description -n compat-libmpc
Contains the .so files for mpc version %{bootstrap-version}.
%endif

%debug_package

%prep
%scm_setup
%if 0%{?bootstrap}
%setup -q -n mpc-%{version} -a 1
%endif

# Prepare forwarder DLLs.
for m in %{SOURCE10}; do
  cp ${m} .
done

autoreconf -fvi

%build
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"
%configure --disable-static

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

%if 0%{?bootstrap}
export CPPFLAGS="%{optflags} -std=gnu99"
export CFLAGS="%{optflags} -std=gnu99"
export EGREP=egrep

pushd mpc-%{bootstrap_version}
%configure --disable-static
%make_build
popd
%endif

%install
%if 0%{?bootstrap}
%make_install -C mpc-%{bootstrap_version}

## remove everything but shlib
rm -fv %{buildroot}%{_libdir}/libmpc.so
rm -fv %{buildroot}%{_includedir}/*
rm -fv %{buildroot}%{_infodir}/*
%endif

%makeinstall
rm -f %{buildroot}/%{_libdir}/*.la
rm -f %{buildroot}/%{_infodir}/dir

# Generate & install forwarder DLLs.
gcc -Zomf -Zdll -nostdlib mpc.def -l$RPM_BUILD_ROOT/%{_libdir}/mpc3.dll -lend -o $RPM_BUILD_ROOT/%{_libdir}/mpc.dll

%check
export BEGINLIBPATH=%{buildroot}%{_libdir}
export LD_LIBRARY_PATH=%{buildroot}%{_libdir}
make check

%files
%license COPYING.LESSER
%doc README NEWS
%{_libdir}/mpc*.dll

%files devel
%{_libdir}/mpc*_dll.a
%{_includedir}/mpc.h

%files doc
%doc AUTHORS
%{_infodir}/*.info*

%if 0%{?bootstrap}
%files -n compat-libmpc
%{_libdir}/libmpc.so.2*
%endif

%changelog
* Wed Mar 11 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.1.0-1
- update to version 1.1.0
- add a forwarder dll
- reworked the spec, including name change as in fedora

* Tue Aug 05 2014 yd
- resolve dll conflict with devel package, fixes ticket#82.
- added debug package with symbolic info for exceptq.

* Wed Nov 20 2013 yd
- rebuild with newer gcc runtime.

* Sat Oct 26 2013 yd
- initial rpm build as dll.
