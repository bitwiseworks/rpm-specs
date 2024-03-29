# Recent so-version, so we do not bump accidentally.
%global nettle_so_ver 8
%global hogweed_so_ver 6

# Set to 1 when building a bootstrap for a bumped so-name.
%global bootstrap 0

%if 0%{?bootstrap}
%global version_old 3.5.1
%global nettle_so_ver_old 7
%global hogweed_so_ver_old 5
%endif

%bcond_with fips

Name:           nettle
Version:        3.9.1
Release:        %{?autorelease}%{!?autorelease:1%{?dist}}
Summary:        A low-level cryptographic library

License:        LGPL-3.0-or-later OR GPL-2.0-or-later
URL:            http://www.lysator.liu.se/~nisse/nettle/
%if !0%{?os2_version}
Source0:	%{name}-%{version}-hobbled.tar.xz
#Source0:        http://www.lysator.liu.se/~nisse/archive/%%{name}-%%{version}.tar.gz
%if 0%{?bootstrap}
Source1:	%{name}-%{version_old}-hobbled.tar.xz
Source2:	nettle-3.5-remove-ecc-testsuite.patch
%endif
%else
Vendor:         bww bitwise works GmbH
%scm_source     github https://github.com/bitwiseworks/%{name}-os2 %{version}-os2
%endif

BuildRequires: make
BuildRequires:  gcc
BuildRequires:  gmp-devel, m4
BuildRequires:	libtool, automake, autoconf, gettext-devel
%if %{with fips}
BuildRequires:  fipscheck
%endif

%package devel
Summary:        Development headers for a low-level cryptographic library
Requires:       %{name} = %{version}-%{release}
%if !0%{?os2_version}
Requires:       gmp-devel%{?_isa}
%else
Requires:       gmp-devel
%endif

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

%if 0%{?os2_version}
%legacy_runtime_packages
%debug_package
%endif

%prep
%if !0%{?os2_version}
%autosetup -Tb 0 -p1
%else
%scm_setup
%endif

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
sed 's/ecc-secp192r1.c//g' -i Makefile.in
sed 's/ecc-secp224r1.c//g' -i Makefile.in
%endif

%build
autoreconf -ifv
# For annocheck
%if !0%{?os2_version}
export ASM_FLAGS="-Wa,--generate-missing-build-notes=yes"
%else
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
export VENDOR="%{vendor}"
%endif

%configure --enable-shared --enable-fat
%if !0%{?os2_version}
%make_build
%else
make %{?_smp_mflags}
%endif

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

%if !0%{?os2_version}
%make_install
make install-shared DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
%else
%make_install INSTALL="/@unixroot/usr/bin/install -p"
make install-shared DESTDIR=$RPM_BUILD_ROOT INSTALL="/@unixroot/usr/bin/install -p"
%endif
mkdir -p $RPM_BUILD_ROOT%{_infodir}
install -p -m 644 nettle.info $RPM_BUILD_ROOT%{_infodir}/
%if !0%{?os2_version}
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
%else
rm -f $RPM_BUILD_ROOT%{_libdir}/libnettle.a
rm -f $RPM_BUILD_ROOT%{_libdir}/libhogweed.a
%endif
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
%if !0%{?os2_version}
rm -f $RPM_BUILD_ROOT%{_bindir}/nettle-lfib-stream
rm -f $RPM_BUILD_ROOT%{_bindir}/pkcs1-conv
rm -f $RPM_BUILD_ROOT%{_bindir}/sexp-conv
rm -f $RPM_BUILD_ROOT%{_bindir}/nettle-hash
rm -f $RPM_BUILD_ROOT%{_bindir}/nettle-pbkdf2
%else
rm -f $RPM_BUILD_ROOT%{_bindir}/nettle-lfib-stream.exe
rm -f $RPM_BUILD_ROOT%{_bindir}/pkcs1-conv.exe
rm -f $RPM_BUILD_ROOT%{_bindir}/sexp-conv.exe
rm -f $RPM_BUILD_ROOT%{_bindir}/nettle-hash.exe
rm -f $RPM_BUILD_ROOT%{_bindir}/nettle-pbkdf2.exe
%endif

%if !0%{?os2_version}
chmod 0755 $RPM_BUILD_ROOT%{_libdir}/libnettle.so.%{nettle_so_ver}.*
chmod 0755 $RPM_BUILD_ROOT%{_libdir}/libhogweed.so.%{hogweed_so_ver}.*
%else
chmod 0755 $RPM_BUILD_ROOT%{_libdir}/nettle*.dll
chmod 0755 $RPM_BUILD_ROOT%{_libdir}/hogwee*.dll
%endif

%check
%if 0%{?os2_version}
export BEGINLIBPATH=%{_builddir}/%{buildsubdir}
%endif
make check

%files
%doc AUTHORS NEWS README
%license COPYINGv2 COPYING.LESSERv3
%{_infodir}/nettle.info.*
%if !0%{?os2_version}
%{_libdir}/libnettle.so.%{nettle_so_ver}
%{_libdir}/libnettle.so.%{nettle_so_ver}.*
%{_libdir}/libhogweed.so.%{hogweed_so_ver}
%{_libdir}/libhogweed.so.%{hogweed_so_ver}.*
%else
%{_libdir}/nettle*.dll
%{_libdir}/hogwee*.dll
%endif
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
%if !0%{?os2_version}
%{_libdir}/libnettle.so
%{_libdir}/libhogweed.so
%else
%{_libdir}/libnettle_dll.a
%{_libdir}/libhogweed_dll.a
%endif
%{_libdir}/pkgconfig/hogweed.pc
%{_libdir}/pkgconfig/nettle.pc

%if !0%{?os2_version}
%ldconfig_scriptlets
%endif

%changelog
* Tue Mar 24 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.9.1-1
- update to version 3.9.1
- resync with fedora spec

* Tue Mar 24 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.5.1-1
- first OS/2 rpm version
