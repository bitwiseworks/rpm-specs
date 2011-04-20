Summary: A utility for getting files from remote servers (FTP, HTTP, and others)
Name: curl
Version: 7.21.1
Release: 2%{?dist}
License: MIT
Group: Applications/Internet
Source: http://curl.haxx.se/download/%{name}-%{version}.tar.gz

Patch0: curl-os2.diff

Provides: webclient
URL: http://curl.haxx.se/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

#BuildRequires: automake
#BuildRequires: groff
#BuildRequires: krb5-devel
#BuildRequires: libidn-devel
#BuildRequires: libssh2-devel >= 1.2
#BuildRequires: nss-devel
#BuildRequires: openldap-devel
#BuildRequires: openssh-clients
#BuildRequires: openssh-server
BuildRequires: openssl-devel
BuildRequires: pkgconfig
#BuildRequires: stunnel

# valgrind is not available on s390(x)
%ifnarch s390 s390x
#BuildRequires: valgrind
%endif

BuildRequires: zlib-devel
Requires: libcurl = %{version}-%{release}

# TODO: mention also IMAP(S), POP3(S), SMTP(S) and RTSP protocols
%description
cURL is a tool for getting files from HTTP, FTP, FILE, LDAP, LDAPS,
DICT, TELNET and TFTP servers, using any of the supported protocols.
cURL is designed to work without user interaction or any kind of
interactivity. cURL offers many useful capabilities, like proxy support,
user authentication, FTP upload, HTTP post, and file transfer resume.

%package -n libcurl
Summary: A library for getting files from web servers
Group: Development/Libraries

# libssh2 ABI has been changed since libssh2-1.0
# this forces update of libssh2 before update of libcurl
#Requires: libssh2 >= 1.2
Requires: openssl

%description -n libcurl
This package provides a way for applications to use FTP, HTTP, Gopher and
other servers for getting files.

%package -n libcurl-devel
Summary: Files needed for building applications with libcurl
Group: Development/Libraries
#Requires: automake
Requires: libcurl = %{version}-%{release}
#Requires: libidn-devel
Requires: pkgconfig

Provides: curl-devel = %{version}-%{release}
Obsoletes: curl-devel < %{version}-%{release}

%description -n libcurl-devel
cURL is a tool for getting files from FTP, HTTP, Gopher, Telnet, and
Dict servers, using any of the supported protocols. The libcurl-devel
package includes files needed for developing applications which can
use cURL's capabilities internally.

%prep
%setup -q

# Convert docs to UTF-8
# NOTE: we do this _before_ applying of all patches, which are already UTF-8
#for f in CHANGES README; do
#    iconv -f iso-8859-1 -t utf8 < ${f} > ${f}.utf8
#    mv -f ${f}.utf8 ${f}
#done

%patch0 -p1 -b .os2~

#autoreconf
# replace hard wired port numbers in the test suite
#sed -i s/899\\\([0-9]\\\)/%{?__isa_bits}9\\1/ tests/data/test*

%build
export CONFIG_SHELL="/bin/sh" ; \
export LDFLAGS="-Zbin-files -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp" ; \
export LIBS="-lurpo -lmmap -lpthread" ; \
%configure \
    --disable-ipv6 \
    --disable-ldaps \
    --enable-manual \
    --with-ca-bundle=%{_sysconfdir}/pki/tls/certs/ca-bundle.crt \
    --with-gssapi=%{_prefix}/kerberos \
    --without-libidn \
    --without-libssh2 \
    --with-ssl --without-nss \
    --enable-shared --disable-static \
    "--cache-file=%{_topdir}/cache/%{name}-%{_target_cpu}.cache"

# uncomment to turn off optimizations
# find -name Makefile | xargs sed -i 's/-O2/-O0/'
# Remove bogus rpath
#sed -i \
#	-e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
#	-e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}

#%check
#LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{_libdir}
#export LD_LIBRARY_PATH
#cd tests
#make %{?_smp_mflags}
# use different port range for 32bit and 64bit build, thus make it possible
# to run both in parallel on the same machine
#./runtests.pl -a -b%{?__isa_bits}90 -p -v

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT INSTALL="%{__install} -p" install

rm -f ${RPM_BUILD_ROOT}%{_libdir}/libcurl.la

install -d $RPM_BUILD_ROOT/%{_datadir}/aclocal
install -m 644 docs/libcurl/libcurl.m4 $RPM_BUILD_ROOT/%{_datadir}/aclocal

install -m 755 lib/curl7.dll $RPM_BUILD_ROOT/%{_libdir}
#install -m 755 lib/.libs/curl.lib $RPM_BUILD_ROOT/%{_libdir}
install -m 755 lib/.libs/curl_s.a $RPM_BUILD_ROOT/%{_libdir}

#%define _curlbuild_h curlbuild-32.h
#mv $RPM_BUILD_ROOT%{_includedir}/curl/curlbuild.h \
#   $RPM_BUILD_ROOT%{_includedir}/curl/%{_curlbuild_h}
#install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_includedir}/curl/curlbuild.h

%clean
rm -rf $RPM_BUILD_ROOT

#%post -n libcurl -p /sbin/ldconfig

#%postun -n libcurl -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc CHANGES README* COPYING
%doc docs/BUGS docs/FAQ docs/FEATURES
%doc docs/MANUAL docs/RESOURCES
%doc docs/TheArtOfHttpScripting docs/TODO
%{_bindir}/curl.exe
%{_mandir}/man1/curl.1*

%files -n libcurl
%defattr(-,root,root,-)
%{_libdir}/curl7.dll

%files -n libcurl-devel
%defattr(-,root,root,-)
%doc docs/examples/*.c docs/examples/Makefile.example docs/INTERNALS
%doc docs/CONTRIBUTE docs/libcurl/ABI
%{_bindir}/curl-config*
%{_includedir}/curl
%{_libdir}/*.a
#%{_libdir}/*.lib
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man1/curl-config.1*
%{_mandir}/man3/*
%{_datadir}/aclocal/libcurl.m4

%changelog
