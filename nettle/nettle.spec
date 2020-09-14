# Recent so-version, so we do not bump accidentally.
%global nettle_so_ver 7
%global hogweed_so_ver 5

# Set to 1 when building a bootstrap for a bumped so-name.
%global bootstrap 0

%if 0%{?bootstrap}
%global version_old 3.4.1rc1
%global nettle_so_ver_old 6
%global hogweed_so_ver_old 4
%endif

%bcond_with fips

Name:           nettle
Version:        3.5.1
Release:        1%{?dist}
Summary:        A low-level cryptographic library

License:        LGPLv3+ or GPLv2+
URL:            http://www.lysator.liu.se/~nisse/nettle/
Vendor:         bww bitwise works GmbH
%scm_source     github https://github.com/bitwiseworks/%{name}-os2 %{version}-os2
%if 0%{?bootstrap}
Source1:	%{name}-%{version_old}-hobbled.tar.xz
Source2:	nettle-3.3-remove-ecc-testsuite.patch
%endif

BuildRequires:  gcc
BuildRequires:  gmp-devel, m4
BuildRequires:	libtool, automake, autoconf, gettext-devel
%if %{with fips}
BuildRequires:  fipscheck
%endif

%package devel
Summary:        Development headers for a low-level cryptographic library
Requires:       %{name} = %{version}-%{release}
Requires:       gmp-devel

%description
Nettle is a cryptographic library that is designed to fit easily in more
or less any context: In crypto toolkits for object-oriented languages
(C++, Python, Pike, ...), in applications like LSH or GNUPG, or even in
kernel space.

%description devel
Nettle is a cryptographic library that is designed to fit easily in more
or less any context: In crypto toolkits for object-oriented languages
(C++, Python, Pike, ...), in applications like LSH or GNUPG, or even in
kernel space.  This package contains the files needed for developing 
applications with nettle.

%debug_package

%prep
%scm_setup

%if 0%{?bootstrap}
mkdir -p bootstrap_ver
pushd bootstrap_ver
tar --strip-components=1 -xf %{SOURCE1}
patch -p1 < %{SOURCE2}

# Disable -ggdb3 which makes debugedit unhappy
sed s/ggdb3/g/ -i configure
sed 's/ecc-192.c//g' -i Makefile.in
sed 's/ecc-224.c//g' -i Makefile.in
popd
%endif

%if !0%{?os2_version}
# Disable -ggdb3 which makes debugedit unhappy
sed s/ggdb3/g/ -i configure
sed 's/ecc-192.c//g' -i Makefile.in
sed 's/ecc-224.c//g' -i Makefile.in
%endif

%build
autoreconf -ifv
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
export VENDOR="%{vendor}"

%configure --enable-shared --enable-fat
make %{?_smp_mflags}

%if 0%{?bootstrap}
pushd bootstrap_ver
autoconf
%configure --with-tests
%make_build
popd
%endif

%if %{with fips}
%define fipshmac() \
	fipshmac -d $RPM_BUILD_ROOT%{_libdir} $RPM_BUILD_ROOT%{_libdir}/%1.* \
	file=`basename $RPM_BUILD_ROOT%{_libdir}/%1.*.hmac` && \
	mv $RPM_BUILD_ROOT%{_libdir}/$file $RPM_BUILD_ROOT%{_libdir}/.$file && \
	ln -s .$file $RPM_BUILD_ROOT%{_libdir}/.%1.hmac

%if 0%{?bootstrap}
%define bootstrap_fips 1
%endif

%define __spec_install_post \
	%{?__debug_package:%{__debug_install_post}} \
	%{__arch_install_post} \
	%{__os_install_post} \
	%fipshmac libnettle.so.%{nettle_so_ver} \
	%fipshmac libhogweed.so.%{hogweed_so_ver} \
	%{?bootstrap_fips:%fipshmac libnettle.so.%{nettle_so_ver_old}} \
	%{?bootstrap_fips:%fipshmac libhogweed.so.%{hogweed_so_ver_old}} \
%{nil}
%endif


%install
%if 0%{?bootstrap}
make -C bootstrap_ver install-shared-nettle DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
make -C bootstrap_ver install-shared-hogweed DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

chmod 0755 $RPM_BUILD_ROOT%{_libdir}/libnettle.so.%{nettle_so_ver_old}.*
chmod 0755 $RPM_BUILD_ROOT%{_libdir}/libhogweed.so.%{hogweed_so_ver_old}.*
%endif

make install DESTDIR=$RPM_BUILD_ROOT INSTALL="/@unixroot/usr/bin/install -p"
make install-shared DESTDIR=$RPM_BUILD_ROOT INSTALL="/@unixroot/usr/bin/install -p"
mkdir -p $RPM_BUILD_ROOT%{_infodir}
install -p -m 644 nettle.info $RPM_BUILD_ROOT%{_infodir}/
rm -f $RPM_BUILD_ROOT%{_libdir}/libnettle.a
rm -f $RPM_BUILD_ROOT%{_libdir}/libhogweed.a
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
rm -f $RPM_BUILD_ROOT%{_bindir}/nettle-lfib-stream.exe
rm -f $RPM_BUILD_ROOT%{_bindir}/pkcs1-conv.exe
rm -f $RPM_BUILD_ROOT%{_bindir}/sexp-conv.exe
rm -f $RPM_BUILD_ROOT%{_bindir}/nettle-hash.exe
rm -f $RPM_BUILD_ROOT%{_bindir}/nettle-pbkdf2.exe

chmod 0755 $RPM_BUILD_ROOT%{_libdir}/nettle*.dll
chmod 0755 $RPM_BUILD_ROOT%{_libdir}/hogwee*.dll

%check
export BEGINLIBPATH=%{_builddir}/%{buildsubdir}
make check

%files
%doc AUTHORS NEWS README
%license COPYINGv2 COPYING.LESSERv3
%{_infodir}/nettle.info.*
%{_libdir}/nettle*.dll
%{_libdir}/hogwee*.dll
%if 0%{?bootstrap}
%{_libdir}/libnettle.so.%{nettle_so_ver_old}
%{_libdir}/libnettle.so.%{nettle_so_ver_old}.*
%{_libdir}/libhogweed.so.%{hogweed_so_ver_old}
%{_libdir}/libhogweed.so.%{hogweed_so_ver_old}.*
%endif
%if %{with fips}
%{_libdir}/.libhogweed.so.*.hmac
%{_libdir}/.libnettle.so.*.hmac
%endif

%files devel
%doc descore.README nettle.html nettle.pdf
%{_includedir}/nettle
%{_libdir}/libnettle_dll.a
%{_libdir}/libhogweed_dll.a
%{_libdir}/pkgconfig/hogweed.pc
%{_libdir}/pkgconfig/nettle.pc

#ldconfig_scriptlets


%changelog
* Tue Mar 24 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.5.1-1
- first OS/2 rpm version
