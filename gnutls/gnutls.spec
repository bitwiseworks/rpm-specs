# This spec file has been automatically updated
Version:	3.6.12
Release: 1%{?dist}
%bcond_with dane
%if 0%{?rhel}
%bcond_with guile
%bcond_without fips
%else
%if 0%{?os2_version}
%bcond_with guile
%bcond_with fips
%else
%bcond_without guile
%bcond_without fips
%endif
%endif

# no manpages for now, as install can't handle it. spawn error
%global with_manpages 0

Summary: A TLS protocol implementation
Name: gnutls
# The libraries are LGPLv2.1+, utilities are GPLv3+
License: GPLv3+ and LGPLv2+
BuildRequires: p11-kit-devel >= 0.21.3, gettext-devel
BuildRequires: zlib-devel, readline-devel, libtasn1-devel >= 4.3
BuildRequires: libtool, automake, autoconf, texinfo
%if !0%{?os2_version}
BuildRequires: autogen-libopts-devel >= 5.18 autogen
%endif
BuildRequires: nettle-devel >= 3.5.1
%if !0%{?os2_version}
BuildRequires: trousers-devel >= 0.3.11.2
%endif
BuildRequires: libidn2-devel
BuildRequires: libunistring-devel
BuildRequires: gperf, gcc, gcc-c++
%if !0%{?os2_version}
BuildRequires: net-tools, datefudge, softhsm
BuildRequires: gnupg2
%endif
%if %{with fips}
BuildRequires: fipscheck
%endif

# for a sanity check on cert loading
BuildRequires: p11-kit-trust, ca-certificates
%if !0%{?os2_version}
Requires: crypto-policies
%endif
Requires: p11-kit-trust
Requires: libtasn1 >= 4.3
Requires: nettle >= 3.4.1
%if !0%{?os2_version}
Recommends: trousers >= 0.3.11.2
%endif

%if %{with dane}
BuildRequires: unbound-devel unbound-libs
%endif
%if %{with guile}
BuildRequires: guile22-devel
%endif
URL: http://www.gnutls.org/
Vendor: bww bitwise works GmbH
%scm_source github https://github.com/bitwiseworks/%{name}-os2 %{version}-os2

# Wildcard bundling exception https://fedorahosted.org/fpc/ticket/174
%if !0%{?os2_version}
Provides: bundled(gnulib) = 20130424
%endif

%package c++
Summary: The C++ interface to GnuTLS
Requires: %{name} = %{version}-%{release}

%package devel
Summary: Development files for the %{name} package
Requires: %{name} = %{version}-%{release}
Requires: %{name}-c++ = %{version}-%{release}
%if %{with dane}
Requires: %{name}-dane = %{version}-%{release}
%endif
Requires: pkgconfig

%package utils
License: GPLv3+
Summary: Command line tools for TLS protocol
Requires: %{name} = %{version}-%{release}
%if %{with dane}
Requires: %{name}-dane = %{version}-%{release}
%endif

%if %{with dane}
%package dane
Summary: A DANE protocol implementation for GnuTLS
Requires: %{name} = %{version}-%{release}
%endif

%if %{with guile}
%package guile
Summary: Guile bindings for the GNUTLS library
Requires: %{name} = %{version}-%{release}
Requires: guile22
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

%if %{with guile}
%description guile
GnuTLS is a secure communications library implementing the SSL, TLS and DTLS 
protocols and technologies around them. It provides a simple C language 
application programming interface (API) to access the secure communications 
protocols as well as APIs to parse and write X.509, PKCS #12, OpenPGP and 
other required structures. 
This package contains Guile bindings for the library.
%endif

%debug_package

%prep
%scm_setup

autoreconf -fvi

rm -f lib/minitasn1/*.c lib/minitasn1/*.h
%if !0%{?os2_version}
rm -f src/libopts/*.c src/libopts/*.h src/libopts/compat/*.c src/libopts/compat/*.h 
%endif

echo "SYSTEM=NORMAL" >> tests/system.prio

# Note that we explicitly enable SHA1, as SHA1 deprecation is handled
# via the crypto policies

%build

# These should be checked by m4/guile.m4 instead of configure.ac
# taking into account of _guile_suffix
%if %{with guile}
guile_snarf=%{_bindir}/guile-snarf2.2
export guile_snarf
GUILD=%{_bindir}/guild2.2
export GUILD
%endif

export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"
export LIBS="-lcx"
%configure --with-libtasn1-prefix=%{_prefix} \
%if %{with fips}
           --enable-fips140-mode \
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
%if !0%{?os2_version}
           --with-trousers-lib=%{_libdir}/libtspi.so.1 \
%endif
           --htmldir=%{_docdir}/manual \
%if %{with guile}
           --enable-guile \
           --with-guile-extension-dir=%{_libdir}/guile/2.2 \
%else
           --disable-guile \
%endif
%if %{with dane}
           --with-unbound-root-key-file=/var/lib/unbound/root.key \
           --enable-libdane \
%else
           --disable-libdane \
%endif
           --disable-rpath \
%if !%{with_manpages}
           --enable-manpages=no \
%endif
           --with-default-priority-string="@SYSTEM"

# Set BUILDLEVEL to be embedded to all DLLs built with Libtool.
export LT_BUILDLEVEL="@#%{vendor}:%{version}-%{release}#@##1## `LANG=C date +'%%d %%b %%Y %%H:%%M:%%S'`     `uname -n`::::0::"

make %{?_smp_mflags} V=1

%if %{with fips}
%define __spec_install_post \
	%{?__debug_package:%{__debug_install_post}} \
	%{__arch_install_post} \
	%{__os_install_post} \
	fipshmac -d $RPM_BUILD_ROOT%{_libdir} $RPM_BUILD_ROOT%{_libdir}/libgnutls.so.30.*.* \
	file=`basename $RPM_BUILD_ROOT%{_libdir}/libgnutls.so.30.*.hmac` && mv $RPM_BUILD_ROOT%{_libdir}/$file $RPM_BUILD_ROOT%{_libdir}/.$file && ln -s .$file $RPM_BUILD_ROOT%{_libdir}/.libgnutls.so.30.hmac \
%{nil}
%endif

%install
make install DESTDIR=$RPM_BUILD_ROOT
make -C doc install-html DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/guile/2.2/guile-gnutls*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/guile/2.2/guile-gnutls*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/gnutls/libpkcs11mock1.*
rm -f $RPM_BUILD_ROOT%{_libdir}/gnutls/pkcs11m*.dll
%if %{without dane}
rm -f $RPM_BUILD_ROOT%{_libdir}/pkgconfig/gnutls-dane.pc
%endif

%find_lang gnutls

%check
%if !0%{?os2_version}
make check %{?_smp_mflags} GNUTLS_SYSTEM_PRIORITY_FILE=/dev/null
%endif

%files -f gnutls.lang
%defattr(-,root,root,-)
%{_libdir}/gtls*.dll
%exclude %{_libdir}/gtlsxx*.dll
%if %{with fips}
%{_libdir}/.libgnutls.so.30*.hmac
%endif
%doc README.md AUTHORS NEWS THANKS
%license LICENSE doc/COPYING doc/COPYING.LESSER

%files c++
%{_libdir}/gtlsxx*.dll

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/gnutls*_dll.a
%if %{with fips}
%{_libdir}/.libgnutls.so.*.hmac
%endif

%{_libdir}/pkgconfig/*.pc
%if %{with_manpages}
%{_mandir}/man3/*
%endif
%{_infodir}/gnutls*
%{_infodir}/pkcs11-vision*
%{_docdir}/manual/*

%files utils
%defattr(-,root,root,-)
%{_bindir}/certtool.exe
%if !0%{?os2_version}
%{_bindir}/tpmtool.exe
%endif
%{_bindir}/ocsptool.exe
%{_bindir}/psktool.exe
%{_bindir}/p11tool.exe
%{_bindir}/srptool.exe
%if %{with dane}
%{_bindir}/danetool
%endif
%{_bindir}/gnutls*.exe
%if %{with_manpages}
%{_mandir}/man1/*
%endif
%doc doc/certtool.cfg

%if %{with dane}
%files dane
%defattr(-,root,root,-)
%{_libdir}/gnutld*.dll
%endif

%if %{with guile}
%files guile
%defattr(-,root,root,-)
%{_libdir}/guile/2.2/gnutlg*.dll
%{_libdir}/guile/2.2/site-ccache/gnutls.go
%{_libdir}/guile/2.2/site-ccache/gnutls/extra.go
%{_datadir}/guile/site/2.2/gnutls.scm
%{_datadir}/guile/site/2.2/gnutls/extra.scm
%endif

%changelog
* Sat Apr 04 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.6.12-1
- first OS/2 rpm version
