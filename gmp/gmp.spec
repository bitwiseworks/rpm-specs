#
# Important for %%{ix86}:
# This rpm has to be build on a CPU with sse2 support like Pentium 4 !
#

Summary: A GNU arbitrary precision library
Name: gmp
Version: 6.2.0
Release: 2%{?dist}
Epoch: 1
URL: http://gmplib.org/

#Source0: ftp://ftp.gmplib.org/pub/gmp-%{version}/gmp-%{version}.tar.bz2
%scm_source github https://github.com/bitwiseworks/%{name}-os2 %{version}-os2
Vendor: bww bitwise works GmbH
# DEF files to create forwarders for the legacy package
Source10:       gmp.def

License: LGPLv3+ or GPLv2+
BuildRequires: autoconf automake libtool
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: git
%if 0
#autoreconf on arm needs:
BuildRequires: perl-Carp
%endif
# don't Generate the .hmac checksum unless --with fips is used
%bcond_with	fips
%if %{with fips}
BuildRequires: fipscheck
%endif

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

%package c++
Summary: C++ bindings for the GNU MP arbitrary precision library
Requires: %{name} = %{epoch}:%{version}-%{release}

%description c++
Bindings for using the GNU MP arbitrary precision library in C++ applications.

%package devel
Summary: Development tools for the GNU MP arbitrary precision library
Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: %{name}-c++ = %{epoch}:%{version}-%{release}

%description devel
The libraries, header files and documentation for using the GNU MP 
arbitrary precision library in applications.

If you want to develop applications which will use the GNU MP library,
you'll need to install the gmp-devel package.  You'll also need to
install the gmp package.

%package static
Summary: Development tools for the GNU MP arbitrary precision library
Requires: %{name}-devel = %{epoch}:%{version}-%{release}

%description static
The static libraries for using the GNU MP arbitrary precision library 
in applications.

%debug_package

%prep
%scm_setup

# switch the defaults to new cpus on s390x
%ifarch s390x
( cd mpn/s390_64; ln -s z10 s390x )
%endif

# Prepare forwarder DLLs.
for m in %{SOURCE10}; do
  cp ${m} .
done

%build
autoreconf -ifv
if as --help | grep -q execstack; then
  # the object files do not require an executable stack
  export CCAS="gcc -c -Wa,--noexecstack"
fi

export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"

# as our arch is mostly wrong don't use that
%if 0
%ifarch %{ix86}
  export CFLAGS=$(echo %{optflags} | sed -e "s/-mtune=[^ ]*//g" | sed -e "s/-march=[^ ]*/-march=i686/g")
  export CXXFLAGS=$(echo %{optflags} | sed -e "s/-mtune=[^ ]*//g" | sed -e "s/-march=[^ ]*/-march=i686/g")
%endif
%endif

%configure --enable-cxx --enable-fat

sed -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
    -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
    -e 's|-lstdc++ -lm|-lstdc++|' \
    -i libtool

# Set BUILDLEVEL to be embedded to all DLLs built with Libtool.
export LT_BUILDLEVEL="@#%{vendor}:%{version}-%{release}#@##1## `LANG=C date +'%%d %%b %%Y %%H:%%M:%%S'`     `uname -n`::::0::"

export LD_LIBRARY_PATH=`pwd`/.libs
make %{?_smp_mflags}

%if %{with fips}
%define __spec_install_post \
    %{?__debug_package:%{__debug_install_post}} \
    %{__arch_install_post} \
    %{__os_install_post} \
    fipshmac -d $RPM_BUILD_ROOT%{_libdir} $RPM_BUILD_ROOT%{_libdir}/libgmp.so.10.* \
    file=`basename $RPM_BUILD_ROOT%{_libdir}/libgmp.so.10.*.hmac` && \
        mv $RPM_BUILD_ROOT%{_libdir}/$file $RPM_BUILD_ROOT%{_libdir}/.$file && \
        ln -s .$file $RPM_BUILD_ROOT%{_libdir}/.libgmp.so.10.hmac
%{nil}
%endif

%install
export BEGINLIBPATH=`pwd`/.libs
export LD_LIBRARY_PATH=`pwd`/.libs
make install DESTDIR=$RPM_BUILD_ROOT
install -m 644 gmp-mparam.h ${RPM_BUILD_ROOT}%{_includedir}
rm -f $RPM_BUILD_ROOT%{_libdir}/libgmp.la
rm -f $RPM_BUILD_ROOT%{_libdir}/libmp.la
rm -f $RPM_BUILD_ROOT%{_libdir}/libgmpxx.la
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
#/sbin/ldconfig -n $RPM_BUILD_ROOT%{_libdir}
#ln -sf libgmpxx.so.4 $RPM_BUILD_ROOT%{_libdir}/libgmpxx.so

# don't do that on os2, as not needed
%if 0
# Rename gmp.h to gmp-<arch>.h and gmp-mparam.h to gmp-mparam-<arch>.h to 
# avoid file conflicts on multilib systems and install wrapper include files
# gmp.h and gmp-mparam-<arch>.h
basearch=%{_arch}
# always use i386 for iX86
%ifarch %{ix86}
basearch=i386
%endif
# always use arm for arm*
%ifarch %{arm}
basearch=arm
%endif
# superH architecture support
%ifarch sh3 sh4
basearch=sh
%endif
# Rename files and install wrappers

mv %{buildroot}/%{_includedir}/gmp.h %{buildroot}/%{_includedir}/gmp-${basearch}.h
install -m644 %{SOURCE2} %{buildroot}/%{_includedir}/gmp.h
mv %{buildroot}/%{_includedir}/gmp-mparam.h %{buildroot}/%{_includedir}/gmp-mparam-${basearch}.h
install -m644 %{SOURCE3} %{buildroot}/%{_includedir}/gmp-mparam.h
%endif

# Generate & install forwarder DLLs.
gcc -Zomf -Zdll -nostdlib gmp.def -l$RPM_BUILD_ROOT/%{_libdir}/gmp10.dll -lend -o $RPM_BUILD_ROOT/%{_libdir}/gmp.dll

%check
%ifnarch ppc
export BEGINLIBPATH=`pwd`/.libs
export LD_LIBRARY_PATH=`pwd`/.libs
make %{?_smp_mflags} check
%endif

#ldconfig_scriptlets

#ldconfig_scriptlets c++

%files
%{!?_licensedir:%global license %%doc}
%license COPYING COPYING.LESSERv3 COPYINGv2 COPYINGv3
%doc NEWS README
%{_libdir}/gmp10.dll
%{_libdir}/gmp.dll
%if %{with fips}
%{_libdir}/.libgmp.so.*.hmac
%endif

%files c++
%{_libdir}/gmpxx4.dll

%files devel
%{_libdir}/gmp*_dll.a
%{_includedir}/*.h
%{_infodir}/gmp.info*
%{_libdir}/pkgconfig/gmp.pc
%{_libdir}/pkgconfig/gmpxx.pc

%files static
%{_libdir}/gmp.a
%{_libdir}/gmpxx.a

%changelog
* Mon Sep 07 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1:6.2.0-2
- move pc files to devel (fedora resync)

* Mon Mar 09 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1:6.2.0-1
- update to version 6.2.0
- move source to github
- redo the spec heavily

* Fri Dec 02 2011 yd
- build as dll

* Thu Dec 01 2011 yd
- build as static lib
