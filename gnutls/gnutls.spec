%define srpmhash() %{lua:
local files = rpm.expand("%_specdir/gnutls.spec")
for i, p in ipairs(patches) do
   files = files.." "..p
end
for i, p in ipairs(sources) do
   files = files.." "..p
end
local sha256sum = assert(io.popen("cat "..files.."| sha256sum"))
local hash = sha256sum:read("*a")
sha256sum:close()
print(string.sub(hash, 0, 16))
}

Version: 3.8.2
Release: %{?autorelease}%{!?autorelease:1%{?dist}}
%if !0%{?os2_version}
Patch: gnutls-3.2.7-rpath.patch

# follow https://gitlab.com/gnutls/gnutls/-/issues/1443
Patch: gnutls-3.7.8-ktls_skip_tls12_chachapoly_test.patch

# tentatively reverted for https://gitlab.com/gnutls/gnutls/-/issues/1515
Patch: gnutls-3.8.2-revert-pkcs11-ed448.patch
%endif

%bcond_without bootstrap
%if !0%{?os2_version}
%bcond_without dane
%bcond_without fips
%else
%bcond_with dane
%bcond_with fips
%endif
%bcond_with tpm12
%if !0%{?os2_version}
%bcond_without tpm2
%else
%bcond_with tpm2
%endif
%bcond_without gost
%bcond_with certificate_compression
%if !0%{?os2_version}
%bcond_without tests
%else
%bcond_with tests
%endif

%if 0%{?fedora} && 0%{?fedora} < 38
%bcond_without srp
%else
%bcond_with srp
%endif

%if 0%{?fedora}
%bcond_without mingw
%else
%bcond_with mingw
%endif


Summary: A TLS protocol implementation
Name: gnutls
# The libraries are LGPLv2.1+, utilities are GPLv3+
License: GPL-3.0-or-later AND LGPL-2.1-or-later
BuildRequires: p11-kit-devel >= 0.21.3, gettext-devel
BuildRequires: readline-devel, libtasn1-devel >= 4.3
%if %{with certificate_compression}
BuildRequires: zlib-devel, brotli-devel, libzstd-devel
%endif
%if %{with bootstrap}
BuildRequires: automake, autoconf, gperf, libtool, texinfo
%endif
BuildRequires: nettle-devel >= 3.9.1
%if %{with tpm12}
BuildRequires: trousers-devel >= 0.3.11.2
%endif
%if %{with tpm2}
BuildRequires: tpm2-tss-devel >= 3.0.3
%endif
BuildRequires: libidn2-devel
BuildRequires: libunistring-devel
%if !0%{?os2_version}
BuildRequires: net-tools, softhsm, gcc, gcc-c++
BuildRequires: gnupg2
%else
BuildRequires: gcc, gcc-c++
%endif
BuildRequires: git-core

# for a sanity check on cert loading
BuildRequires: p11-kit-trust, ca-certificates
%if !0%{?os2_version}
Requires: crypto-policies
%endif
Requires: p11-kit-trust
Requires: libtasn1 >= 4.3
Requires: nettle >= 3.9.1
%if %{with tpm12}
Recommends: trousers >= 0.3.11.2
%endif

%if %{with dane}
BuildRequires: unbound-devel unbound-libs
%endif
%if !0%{?os2_version}
BuildRequires: make gtk-doc
%else
BuildRequires: make
%endif

%if %{with mingw}
BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-libtasn1 >= 4.3
BuildRequires:  mingw32-readline
BuildRequires:  mingw32-zlib
BuildRequires:  mingw32-p11-kit >= 0.23.1
BuildRequires:  mingw32-nettle >= 3.6
BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw64-gcc
BuildRequires:  mingw64-gcc-c++
BuildRequires:  mingw64-libtasn1 >= 4.3
BuildRequires:  mingw64-readline
BuildRequires:  mingw64-zlib
BuildRequires:  mingw64-p11-kit >= 0.23.1
BuildRequires:  mingw64-nettle >= 3.6
%endif

URL: http://www.gnutls.org/
%define short_version %(echo %{version} | grep -m1 -o "[0-9]*\.[0-9]*" | head -1)
%if !0%{?os2_version}
Source0: https://www.gnupg.org/ftp/gcrypt/gnutls/v%{short_version}/%{name}-%{version}.tar.xz
Source1: https://www.gnupg.org/ftp/gcrypt/gnutls/v%{short_version}/%{name}-%{version}.tar.xz.sig
Source2: https://gnutls.org/gnutls-release-keyring.gpg
%else
Vendor: bww bitwise works GmbH
%scm_source github https://github.com/bitwiseworks/%{name}-os2 %{version}-os2
%endif

# Wildcard bundling exception https://fedorahosted.org/fpc/ticket/174
%if !0%{?os2_version}
Provides: bundled(gnulib) = 20130424
%endif

%package c++
Summary: The C++ interface to GnuTLS
%if !0%{?os2_version}
Requires: %{name}%{?_isa} = %{version}-%{release}
%else
Requires: %{name} = %{version}-%{release}
%endif

%package devel
Summary: Development files for the %{name} package
%if !0%{?os2_version}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: %{name}-c++%{?_isa} = %{version}-%{release}
%else
Requires: %{name} = %{version}-%{release}
Requires: %{name}-c++ = %{version}-%{release}
%endif
%if %{with dane}
%if !0%{?os2_version}
Requires: %{name}-dane%{?_isa} = %{version}-%{release}
%else
Requires: %{name}-dane = %{version}-%{release}
%endif
%endif
Requires: pkgconfig

%package utils
License: GPL-3.0-or-later
Summary: Command line tools for TLS protocol
%if !0%{?os2_version}
Requires: %{name}%{?_isa} = %{version}-%{release}
%else
Requires: %{name} = %{version}-%{release}
%endif
%if %{with dane}
%if !0%{?os2_version}
Requires: %{name}-dane%{?_isa} = %{version}-%{release}
%else
Requires: %{name}-dane = %{version}-%{release}
%endif
%endif

%if %{with dane}
%package dane
Summary: A DANE protocol implementation for GnuTLS
%if !0%{?os2_version}
Requires: %{name}%{?_isa} = %{version}-%{release}
%else
Requires: %{name} = %{version}-%{release}
%endif
%endif

%description
GnuTLS is a secure communications library implementing the SSL, TLS and DTLS 
protocols and technologies around them. It provides a simple C language 
application programming interface (API) to access the secure communications 
protocols as well as APIs to parse and write X.509, PKCS #12, OpenPGP and 
other required structures. 

%description c++
GnuTLS is a secure communications library implementing the SSL, TLS and DTLS 
protocols and technologies around them. It provides a simple C language 
application programming interface (API) to access the secure communications 
protocols as well as APIs to parse and write X.509, PKCS #12, OpenPGP and 
other required structures. 

%description devel
GnuTLS is a secure communications library implementing the SSL, TLS and DTLS 
protocols and technologies around them. It provides a simple C language 
application programming interface (API) to access the secure communications 
protocols as well as APIs to parse and write X.509, PKCS #12, OpenPGP and 
other required structures. 
This package contains files needed for developing applications with
the GnuTLS library.

%description utils
GnuTLS is a secure communications library implementing the SSL, TLS and DTLS 
protocols and technologies around them. It provides a simple C language 
application programming interface (API) to access the secure communications 
protocols as well as APIs to parse and write X.509, PKCS #12, OpenPGP and 
other required structures. 
This package contains command line TLS client and server and certificate
manipulation tools.

%if %{with dane}
%description dane
GnuTLS is a secure communications library implementing the SSL, TLS and DTLS 
protocols and technologies around them. It provides a simple C language 
application programming interface (API) to access the secure communications 
protocols as well as APIs to parse and write X.509, PKCS #12, OpenPGP and 
other required structures. 
This package contains library that implements the DANE protocol for verifying
TLS certificates through DNSSEC.
%endif

%if %{with mingw}
%package -n mingw32-%{name}
Summary:        MinGW GnuTLS TLS/SSL encryption library
Requires:       pkgconfig
Requires:       mingw32-libtasn1 >= 4.3
BuildArch:      noarch

%description -n mingw32-gnutls
GnuTLS TLS/SSL encryption library.  This library is cross-compiled
for MinGW.

%package -n mingw64-%{name}
Summary:        MinGW GnuTLS TLS/SSL encryption library
Requires:       pkgconfig
Requires:       mingw64-libtasn1 >= 4.3
BuildArch:      noarch

%description -n mingw64-gnutls
GnuTLS TLS/SSL encryption library.  This library is cross-compiled
for MinGW.

%{?mingw_debug_package}
%endif

%if 0%{?os2_version}
%debug_package
%endif

%prep
%if !0%{?os2_version}
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'

%autosetup -p1 -S git
%else
%scm_setup
%endif

%build
%define _lto_cflags %{nil}

%if %{with bootstrap}
autoreconf -fi
%endif

%if !0%{?os2_version}
sed -i -e 's|sys_lib_dlsearch_path_spec="/lib /usr/lib|sys_lib_dlsearch_path_spec="/lib /usr/lib %{_libdir}|g' configure
%endif
rm -f lib/minitasn1/*.c lib/minitasn1/*.h

echo "SYSTEM=NORMAL" >> tests/system.prio

%if !0%{?os2_version}
CCASFLAGS="$CCASFLAGS -Wa,--generate-missing-build-notes=yes"
export CCASFLAGS
%endif

%if %{with fips}
eval $(sed -n 's/^\(\(NAME\|VERSION_ID\)=.*\)/OS_\1/p' /etc/os-release)
export FIPS_MODULE_NAME="$OS_NAME ${OS_VERSION_ID%%.*} %name"
%endif

mkdir native_build
%if !0%{?os2_version}
pushd native_build
%else
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"
export LIBS="-lcx"
# Set BUILDLEVEL to be embedded to all DLLs built with Libtool.
export LT_BUILDLEVEL="@#%{vendor}:%{version}-%{release}#@##1## `LANG=C date +'%%d %%b %%Y %%H:%%M:%%S'`     `uname -n`::::0::"
cd native_build
%endif
%global _configure ../configure
%configure \
%if %{with fips}
           --enable-fips140-mode \
           --with-fips140-module-name="$FIPS_MODULE_NAME" \
           --with-fips140-module-version=%{version}-%{srpmhash} \
%endif
%if %{with gost}
    	   --enable-gost \
%else
	   --disable-gost \
%endif
%if %{with srp}
           --enable-srp-authentication \
%endif
%ifarch %{ix86}
           --disable-year2038 \
%endif
	   --enable-sha1-support \
           --disable-static \
%if !0%{?os2_version}
           --disable-openssl-compatibility \
%else
           --enable-openssl-compatibility \
%endif
           --disable-non-suiteb-curves \
%if !0%{?os2_version}
           --with-system-priority-file=%{_sysconfdir}/crypto-policies/back-ends/gnutls.config \
%endif
           --with-default-trust-store-pkcs11="pkcs11:" \
%if %{with tpm12}
           --with-trousers-lib=%{_libdir}/libtspi.so.1 \
%else
           --without-tpm \
%endif
%if %{with tpm2}
           --with-tpm2 \
%else
           --without-tpm2 \
%endif
%if !0%{?os2_version}
           --enable-ktls \
%endif
           --htmldir=%{_docdir}/manual \
%if %{with dane}
           --with-unbound-root-key-file=/var/lib/unbound/root.key \
           --enable-libdane \
%else
           --disable-libdane \
%endif
%if %{with certificate_compression}
	   --with-zlib --with-brotli --with-zstd \
%else
	   --without-zlib --without-brotli --without-zstd \
%endif
           --disable-rpath \
           --with-default-priority-string="@SYSTEM"

%if !0%{?os2_version}
%make_build
popd
%else
make %{?_smp_mflags} V=1
cd ..
%endif

%if %{with mingw}
# MinGW does not support CCASFLAGS
export CCASFLAGS=""
%mingw_configure \
%if %{with srp}
    --enable-srp-authentication \
%endif
    --enable-sha1-support \
    --disable-static \
    --disable-openssl-compatibility \
    --disable-non-suiteb-curves \
    --disable-libdane \
    --disable-rpath \
    --disable-nls \
    --disable-cxx \
    --enable-local-libopts \
    --enable-shared \
    --without-tpm \
    --with-included-unistring \
    --disable-doc \
    --with-default-priority-string="@SYSTEM"
%mingw_make %{?_smp_mflags}
%endif

%install
%make_install -C native_build
%if !0%{?os2_version}
pushd native_build
%else
cd native_build
%endif
make -C doc install-html DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
%if %{without dane}
rm -f $RPM_BUILD_ROOT%{_libdir}/pkgconfig/gnutls-dane.pc
%endif

%if %{with fips}
# doing it twice should be a no-op the second time,
# and this way we avoid redefining it and missing a future change
%{__spec_install_post}
fname=`basename $RPM_BUILD_ROOT%{_libdir}/libgnutls.so.30.*.*`
./lib/fipshmac "$RPM_BUILD_ROOT%{_libdir}/libgnutls.so.30" > "$RPM_BUILD_ROOT%{_libdir}/.$fname.hmac"
sed -i "s^$RPM_BUILD_ROOT/usr^^" "$RPM_BUILD_ROOT%{_libdir}/.$fname.hmac"
ln -s ".$fname.hmac" "$RPM_BUILD_ROOT%{_libdir}/.libgnutls.so.30.hmac"
%endif

%if %{with fips}
%define __spec_install_post \
	%{?__debug_package:%{__debug_install_post}} \
	%{__arch_install_post} \
	%{__os_install_post} \
%{nil}
%endif

%find_lang gnutls
%if !0%{?os2_version}
popd
%else
cd ..
%endif

%if %{with mingw}
%mingw_make_install

# Remove .la files
rm -f $RPM_BUILD_ROOT%{mingw32_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{mingw64_libdir}/*.la

# The .def files aren't interesting for other binaries
rm -f $RPM_BUILD_ROOT%{mingw32_bindir}/*.def
rm -f $RPM_BUILD_ROOT%{mingw64_bindir}/*.def

# Remove info and man pages which duplicate stuff in Fedora already.
rm -rf $RPM_BUILD_ROOT%{mingw32_infodir}
rm -rf $RPM_BUILD_ROOT%{mingw32_mandir}
rm -rf $RPM_BUILD_ROOT%{mingw32_docdir}/gnutls

rm -rf $RPM_BUILD_ROOT%{mingw64_infodir}
rm -rf $RPM_BUILD_ROOT%{mingw64_mandir}
rm -rf $RPM_BUILD_ROOT%{mingw64_docdir}/gnutls

# Remove test libraries
rm -f $RPM_BUILD_ROOT%{mingw32_libdir}/crypt32.dll*
rm -f $RPM_BUILD_ROOT%{mingw32_libdir}/ncrypt.dll*
rm -f $RPM_BUILD_ROOT%{mingw64_libdir}/crypt32.dll*
rm -f $RPM_BUILD_ROOT%{mingw64_libdir}/ncrypt.dll*

%mingw_debug_install_post
%endif

%check
%if %{with tests}
%if !0%{?os2_version}
pushd native_build
%else
cd native_build
%endif

# KeyUpdate is not yet supported in the kernel.
xfail_tests=ktls_keyupdate.sh

# The ktls.sh test currently only supports kernel 5.11+.  This needs to
# be checked at run time, as the koji builder might be using a different
# version of kernel on the host than the one indicated by the
# kernel-devel package.

case "$(uname -r)" in
  4.* | 5.[0-9].* | 5.10.* )
    xfail_tests="$xfail_tests ktls.sh"
    ;;
esac

make check %{?_smp_mflags} GNUTLS_SYSTEM_PRIORITY_FILE=/dev/null XFAIL_TESTS="$xfail_tests"
%if !0%{?os2_version}
popd
%else
cd ..
%endif
%endif

%files -f native_build/gnutls.lang
%if !0%{?os2_version}
%{_libdir}/libgnutls.so.30*
%else
%{_libdir}/gtls*.dll
%exclude %{_libdir}/gtlsxx*.dll
%endif
%if %{with fips}
%{_libdir}/.libgnutls.so.30*.hmac
%endif
%doc README.md AUTHORS NEWS THANKS
%license LICENSE doc/COPYING doc/COPYING.LESSER

%files c++
%if !0%{?os2_version}
%{_libdir}/libgnutlsxx.so.*
%else
%{_libdir}/gtlsxx*.dll
%endif

%files devel
%{_includedir}/*
%if !0%{?os2_version}
%{_libdir}/libgnutls*.so
%else
%{_libdir}/gnutls*_dll.a
%endif

%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*
%{_infodir}/gnutls*
%{_infodir}/pkcs11-vision*
%{_docdir}/manual/*

%files utils
%if !0%{?os2_version}
%{_bindir}/certtool
%else
%{_bindir}/certtool.exe
%endif
%if %{with tpm12}
%{_bindir}/tpmtool
%endif
%if !0%{?os2_version}
%{_bindir}/ocsptool
%{_bindir}/psktool
%{_bindir}/p11tool
%else
%{_bindir}/ocsptool.exe
%{_bindir}/psktool.exe
%{_bindir}/p11tool.exe
%endif
%if %{with srp}
%{_bindir}/srptool
%endif
%if %{with dane}
%{_bindir}/danetool
%endif
%if !0%{?os2_version}
%{_bindir}/gnutls*
%else
%{_bindir}/gnutls*.exe
%endif
%{_mandir}/man1/*
%doc doc/certtool.cfg

%if %{with dane}
%files dane
%{_libdir}/libgnutls-dane.so.*
%endif

%if %{with mingw}
%files -n mingw32-%{name}
%license LICENSE doc/COPYING doc/COPYING.LESSER
%{mingw32_bindir}/certtool.exe
%{mingw32_bindir}/gnutls-cli-debug.exe
%{mingw32_bindir}/gnutls-cli.exe
%{mingw32_bindir}/gnutls-serv.exe
%{mingw32_bindir}/libgnutls-30.dll
%{mingw32_bindir}/ocsptool.exe
%{mingw32_bindir}/p11tool.exe
%{mingw32_bindir}/psktool.exe
%if %{with srp}
%{mingw32_bindir}/srptool.exe
%endif
%{mingw32_libdir}/libgnutls.dll.a
%{mingw32_libdir}/libgnutls-30.def
%{mingw32_libdir}/pkgconfig/gnutls.pc
%{mingw32_includedir}/gnutls/

%files -n mingw64-%{name}
%license LICENSE doc/COPYING doc/COPYING.LESSER
%{mingw64_bindir}/certtool.exe
%{mingw64_bindir}/gnutls-cli-debug.exe
%{mingw64_bindir}/gnutls-cli.exe
%{mingw64_bindir}/gnutls-serv.exe
%{mingw64_bindir}/libgnutls-30.dll
%{mingw64_bindir}/ocsptool.exe
%{mingw64_bindir}/p11tool.exe
%{mingw64_bindir}/psktool.exe
%if %{with srp}
%{mingw64_bindir}/srptool.exe
%endif
%{mingw64_libdir}/libgnutls.dll.a
%{mingw64_libdir}/libgnutls-30.def
%{mingw64_libdir}/pkgconfig/gnutls.pc
%{mingw64_includedir}/gnutls/
%endif

%changelog
* Tue Jan 23 2024 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.8.2-1
- update to version 3.8.2
- resync spec with fedora

* Sat Apr 04 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.6.12-1
- first OS/2 rpm version
