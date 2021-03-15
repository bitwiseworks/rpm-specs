Summary: A utility for getting files from remote servers (FTP, HTTP, and others)
Name: curl
Version: 7.75.0
Release: 2%{?dist}
License: MIT
%if !0%{?os2_version}
Source: https://curl.se/download/%{name}-%{version}.tar.xz

# patch making libcurl multilib ready
Patch101: 0101-curl-7.32.0-multilib.patch

# prevent configure script from discarding -g in CFLAGS (#496778)
Patch102: 0102-curl-7.36.0-debug.patch

# use localhost6 instead of ip6-localhost in the curl test-suite
Patch104: 0104-curl-7.73.0-localhost6.patch

# prevent valgrind from reporting false positives on x86_64
Patch105: 0105-curl-7.63.0-lib1560-valgrind.patch
%else
Vendor:  bww bitwise works GmbH
%scm_source github http://github.com/bitwiseworks/%{name}-os2 curl-7_75_0-os2
%endif
Provides: curl-full = %{version}-%{release}
Provides: webclient
URL: https://curl.se/
BuildRequires: automake
%if !0%{?os2_version}
BuildRequires: brotli-devel
%endif
BuildRequires: coreutils
BuildRequires: gcc
BuildRequires: groff
%if !0%{?os2_version}
BuildRequires: krb5-devel
%endif
BuildRequires: libidn2-devel
%if !0%{?os2_version}
BuildRequires: libmetalink-devel
BuildRequires: libnghttp2-devel
%endif
BuildRequires: libpsl-devel
%if !0%{?os2_version}
BuildRequires: libssh-devel
%endif
BuildRequires: libtool
BuildRequires: make
%if !0%{?os2_version}
BuildRequires: openldap-devel
BuildRequires: openssh-clients
BuildRequires: openssh-server
%endif
BuildRequires: openssl-devel
%if !0%{?os2_version}
BuildRequires: perl-interpreter
%else
BuildRequires: perl
%endif
BuildRequires: pkgconfig
%if !0%{?os2_version}
BuildRequires: python-unversioned-command
BuildRequires: python3-devel
%endif
BuildRequires: sed
BuildRequires: zlib-devel

# needed to compress content of tool_hugehelp.c after changing curl.1 man page
BuildRequires: perl(IO::Compress::Gzip)

# needed for generation of shell completions
BuildRequires: perl(Getopt::Long)
BuildRequires: perl(Pod::Usage)
BuildRequires: perl(strict)
BuildRequires: perl(warnings)

# gnutls-serv is used by the upstream test-suite
BuildRequires: gnutls-utils

# hostname(1) is used by the test-suite but it is missing in armv7hl buildroot
%if !0%{?os2_version}
BuildRequires: hostname
%endif

# nghttpx (an HTTP/2 proxy) is used by the upstream test-suite
%if !0%{?os2_version}
BuildRequires: nghttp2
%endif

# perl modules used in the test suite
BuildRequires: perl(Cwd)
BuildRequires: perl(Digest::MD5)
BuildRequires: perl(Exporter)
BuildRequires: perl(File::Basename)
BuildRequires: perl(File::Copy)
BuildRequires: perl(File::Spec)
BuildRequires: perl(IPC::Open2)
BuildRequires: perl(MIME::Base64)
BuildRequires: perl(Time::Local)
BuildRequires: perl(Time::HiRes)
BuildRequires: perl(vars)

%if 0%{?fedora}
# needed for upstream test 1451
BuildRequires: python3-impacket
%endif

# The test-suite runs automatically through valgrind if valgrind is available
# on the system.  By not installing valgrind into mock's chroot, we disable
# this feature for production builds on architectures where valgrind is known
# to be less reliable, in order to avoid unnecessary build failures (see RHBZ
# #810992, #816175, and #886891).  Nevertheless developers are free to install
# valgrind manually to improve test coverage on any architecture.
%if !0%{?os2_version}
%ifarch x86_64
BuildRequires: valgrind
%endif
%endif

# stunnel is used by upstream tests but it does not seem to work reliably
# on s390x and occasionally breaks some tests (mainly 1561 and 1562)
%if !0%{?os2_version}
%ifnarch s390x
BuildRequires: stunnel
%endif
%endif

# using an older version of libcurl could result in CURLE_UNKNOWN_OPTION
Requires: libcurl >= %{version}-%{release}

# require at least the version of libpsl that we were built against,
# to ensure that we have the necessary symbols available (#1631804)
%global libpsl_version %(pkg-config --modversion libpsl 2>/dev/null || echo 0)

# require at least the version of libssh that we were built against,
# to ensure that we have the necessary symbols available (#525002, #642796)
%global libssh_version %(pkg-config --modversion libssh 2>/dev/null || echo 0)

# require at least the version of openssl-libs that we were built against,
# to ensure that we have the necessary symbols available (#1462184, #1462211)
%global openssl_version %(pkg-config --modversion openssl 2>/dev/null || echo 0)

%description
curl is a command line tool for transferring data with URL syntax, supporting
FTP, FTPS, HTTP, HTTPS, SCP, SFTP, TFTP, TELNET, DICT, LDAP, LDAPS, FILE, IMAP,
SMTP, POP3 and RTSP.  curl supports SSL certificates, HTTP POST, HTTP PUT, FTP
uploading, HTTP form based upload, proxies, cookies, user+password
authentication (Basic, Digest, NTLM, Negotiate, kerberos...), file transfer
resume, proxy tunneling and a busload of other useful tricks. 

%package -n libcurl
Summary: A library for getting files from web servers
Requires: libpsl >= %{libpsl_version}
%if !0%{?os2_version}
Requires: libssh >= %{libssh_version}
%endif
Requires: openssl-libs >= 1:%{openssl_version}
Provides: libcurl-full = %{version}-%{release}
%if !0%{?os2_version}
Provides: libcurl-full%{?_isa} = %{version}-%{release}
%endif

%description -n libcurl
libcurl is a free and easy-to-use client-side URL transfer library, supporting
FTP, FTPS, HTTP, HTTPS, SCP, SFTP, TFTP, TELNET, DICT, LDAP, LDAPS, FILE, IMAP,
SMTP, POP3 and RTSP. libcurl supports SSL certificates, HTTP POST, HTTP PUT,
FTP uploading, HTTP form based upload, proxies, cookies, user+password
authentication (Basic, Digest, NTLM, Negotiate, Kerberos4), file transfer
resume, http proxy tunneling and more.

%package -n libcurl-devel
Summary: Files needed for building applications with libcurl
Requires: libcurl = %{version}-%{release}

Provides: curl-devel = %{version}-%{release}
%if !0%{?os2_version}
Provides: curl-devel%{?_isa} = %{version}-%{release}
%endif
Obsoletes: curl-devel < %{version}-%{release}

%description -n libcurl-devel
The libcurl-devel package includes header files and libraries necessary for
developing programs which use the libcurl library. It contains the API
documentation of the library, too.

%package -n curl-minimal
Summary: Conservatively configured build of curl for minimal installations
Provides: curl = %{version}-%{release}
Conflicts: curl
RemovePathPostfixes: .minimal

# using an older version of libcurl could result in CURLE_UNKNOWN_OPTION
Requires: libcurl >= %{version}-%{release}

%description -n curl-minimal
This is a replacement of the 'curl' package for minimal installations.  It
comes with a limited set of features compared to the 'curl' package.  On the
other hand, the package is smaller and requires fewer run-time dependencies to
be installed.

%package -n libcurl-minimal
Summary: Conservatively configured build of libcurl for minimal installations
Requires: openssl-libs >= 1:%{openssl_version}
Provides: libcurl = %{version}-%{release}
Provides: libcurl = %{version}-%{release}
Conflicts: libcurl
RemovePathPostfixes: .minimal
# needed for RemovePathPostfixes to work with shared libraries
%undefine __brp_ldconfig

%description -n libcurl-minimal
This is a replacement of the 'libcurl' package for minimal installations.  It
comes with a limited set of features compared to the 'libcurl' package.  On the
other hand, the package is smaller and requires fewer run-time dependencies to
be installed.

%if 0%{?os2_version}
%legacy_runtime_packages

%debug_package
%endif

%prep
%if !0%{?os2_version}
%setup -q

# upstream patches

# Fedora patches
%patch101 -p1
%patch102 -p1
%patch104 -p1
%patch105 -p1
%else
%scm_setup
%endif

# regenerate the configure script and Makefile.in files
autoreconf -fiv

# disable test 1112 (#565305), test 1455 (occasionally fails with 'bind failed
# with errno 98: Address already in use' in Koji environment), and test 1801
# <https://github.com/bagder/curl/commit/21e82bd6#commitcomment-12226582>
printf "1112\n1455\n1801\n" >> tests/data/DISABLED

# disable test 1319 on ppc64 (server times out)
%ifarch ppc64
echo "1319" >> tests/data/DISABLED
%endif

# temporarily disable test 582 on s390x (client times out)
%ifarch s390x
echo "582" >> tests/data/DISABLED
%endif

# temporarily disable tests 702 703 716 on armv7hl (#1829180)
%ifarch armv7hl
printf "702\n703\n716\n" >> tests/data/DISABLED
%endif

# adapt test 323 for updated OpenSSL
sed -e 's/^35$/35,52/' -i tests/data/test323

%build

%if 0%{?os2_version}
# curl m4 extensions override the nice autoconf PATH_SEPARATOR check with a very
# stupid method designed to always fail on Windows and OS/2
export PATH_SEPARATOR=';'

export CFLAGS="-Zomf $RPM_OPT_FLAGS"
export LDFLAGS="-Zomf -Zhigh-mem -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
export VENDOR="%{vendor}"
# Set BUILDLEVEL to be embedded to all DLLs built with Libtool.
export LT_BUILDLEVEL="@#%{vendor}:%{version}-%{release}#@##1## `LANG=C date +'%%d %%b %%Y %%H:%%M:%%S'`     `uname -n`::::0::"
%endif

%if !0%{?os2_version}
mkdir build-{full,minimal}
%else
mkdir build-full
mkdir build-minimal
%endif
export common_configure_opts=" \
    --cache-file=../config.cache \
    --disable-static \
    --enable-symbol-hiding \
%if !0%{?os2_version}
    --enable-ipv6 \
    --enable-threaded-resolver \
    --with-gssapi \
    --with-nghttp2 \
%endif
    --with-ssl --with-ca-bundle=%{_sysconfdir}/pki/tls/certs/ca-bundle.crt"

%global _configure ../configure

# configure minimal build
(
    cd build-minimal
    %configure $common_configure_opts \
        --disable-ldap \
        --disable-ldaps \
        --disable-manual \
        --without-brotli \
        --without-libidn2 \
        --without-libmetalink \
        --without-libpsl \
        --without-libssh
)

# configure full build
(
    cd build-full
    %configure $common_configure_opts \
        --enable-ldap \
        --enable-ldaps \
        --enable-manual \
%if !0%{?os2_version}
        --with-brotli \
%endif
        --with-libidn2 \
%if !0%{?os2_version}
        --with-libmetalink \
%endif
        --with-libpsl \
%if !0%{?os2_version}
        --with-libssh
%endif
)

# avoid using rpath
%if !0%{?os2_version}
sed -e 's/^runpath_var=.*/runpath_var=/' \
    -e 's/^hardcode_libdir_flag_spec=".*"$/hardcode_libdir_flag_spec=""/' \
    -i build-{full,minimal}/libtool

%make_build V=1 -C build-minimal
%make_build V=1 -C build-full
%else
make %{?_smp_mflags} V=1 -C build-minimal
make %{?_smp_mflags} V=1 -C build-full
%endif

%check
%if !0%{?os2_version}
# we have to override LD_LIBRARY_PATH because we eliminated rpath
LD_LIBRARY_PATH="${PWD}/build-full/lib/.libs"
export LD_LIBRARY_PATH

# compile upstream test-cases
cd build-full/tests
%make_build V=1

# relax crypto policy for the test-suite to make it pass again (#1610888)
export OPENSSL_SYSTEM_CIPHERS_OVERRIDE=XXX
export OPENSSL_CONF=

# run the upstream test-suite
srcdir=../../tests perl -I../../tests ../../tests/runtests.pl -a -p -v '!flaky'
%endif

%install
# install and rename the library that will be packaged as libcurl-minimal
%make_install -C build-minimal/lib
%if !0%{?os2_version}
rm -f ${RPM_BUILD_ROOT}%{_libdir}/libcurl.{la,so}
%else
rm -f ${RPM_BUILD_ROOT}%{_libdir}/libcurl.la
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*_dll.a
%endif
for i in ${RPM_BUILD_ROOT}%{_libdir}/*; do
    mv -v $i $i.minimal
done

# install and rename the executable that will be packaged as curl-minimal
%make_install -C build-minimal/src
%if !0%{?os2_version}
mv -v ${RPM_BUILD_ROOT}%{_bindir}/curl{,.minimal}
%else
mv -v ${RPM_BUILD_ROOT}%{_bindir}/curl.exe ${RPM_BUILD_ROOT}%{_bindir}/curl.exe.minimal
%endif

# install libcurl.m4
install -d $RPM_BUILD_ROOT%{_datadir}/aclocal
install -m 644 docs/libcurl/libcurl.m4 $RPM_BUILD_ROOT%{_datadir}/aclocal

# install the executable and library that will be packaged as curl and libcurl
cd build-full
%make_install

# install zsh completion for curl
# (we have to override LD_LIBRARY_PATH because we eliminated rpath)
%if !0%{?os2_version}
LD_LIBRARY_PATH="$RPM_BUILD_ROOT%{_libdir}:$LD_LIBRARY_PATH" \
%else
export BEGINLIBPATH="$RPM_BUILD_ROOT%{_libdir}"
%endif
    %make_install -C scripts

# do not install /usr/share/fish/completions/curl.fish which is also installed
# by fish-3.0.2-1.module_f31+3716+57207597 and would trigger a conflict
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/fish

rm -f ${RPM_BUILD_ROOT}%{_libdir}/libcurl.la

%if !0%{?os2_version}
%ldconfig_scriptlets -n libcurl

%ldconfig_scriptlets -n libcurl-minimal
%endif

%files
%doc CHANGES
%doc README
%doc docs/BUGS.md
%doc docs/FAQ
%doc docs/FEATURES.md
%doc docs/TODO
%doc docs/TheArtOfHttpScripting.md
%if !0%{?os2_version}
%{_bindir}/curl
%else
%{_bindir}/curl.exe
%endif
%{_mandir}/man1/curl.1*
%{_datadir}/zsh

%files -n libcurl
%license COPYING
%if !0%{?os2_version}
%{_libdir}/libcurl.so.4
%{_libdir}/libcurl.so.4.[0-9].[0-9]
%else
%{_libdir}/curl4.dll
%endif

%files -n libcurl-devel
%doc docs/examples/*.c docs/examples/Makefile.example docs/INTERNALS.md
%doc docs/CONTRIBUTE.md docs/libcurl/ABI.md
%{_bindir}/curl-config*
%{_includedir}/curl
%if !0%{?os2_version}
%{_libdir}/*.so
%else
%{_libdir}/*_dll.a
%endif
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man1/curl-config.1*
%{_mandir}/man3/*
%{_datadir}/aclocal/libcurl.m4

%files -n curl-minimal
%if !0%{?os2_version}
%{_bindir}/curl.minimal
%else
%{_bindir}/curl.exe.minimal
%endif
%{_mandir}/man1/curl.1*

%files -n libcurl-minimal
%license COPYING
%if !0%{?os2_version}
%{_libdir}/libcurl.so.4.minimal
%{_libdir}/libcurl.so.4.[0-9].[0-9].minimal
%else
%{_libdir}/curl4.dll.minimal
%endif

%changelog
* Mon Mar 15 2021 Silvan Scherrer <silvan.scherrer@aroa.ch> 7.75.0-2
- add a legacy package

* Fri Mar 12 2021 Silvan Scherrer <silvan.scherrer@aroa.ch> 7.75.0-1
- update version to 7.75.0
- use scm_ macros
- resync with fedora spec

* Thu Sep 04 2014 yd
- added debug package with symbolic info for exceptq.

* Tue Sep 2 2014 Dmitriy Kuminov <coding@dmik.org> 7.37.0-1
- Update to version 7.37.0.
- Use proper sleep function on OS/2.

* Mon Jan 16 2012 yd
- rebuild with libc 0.6.4 runtime.
