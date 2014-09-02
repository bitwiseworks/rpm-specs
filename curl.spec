Summary: A utility for getting files from remote servers (FTP, HTTP, and others)
Name: curl
Version: 7.37.0
Release: 1%{?dist}
License: MIT
Group: Applications/Internet
#Source: http://curl.haxx.se/download/%{name}-%{version}.tar.gz

Provides: webclient
URL: http://curl.haxx.se/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%define svn_url     http://svn.netlabs.org/repos/ports/curl/trunk
%define svn_rev     831

Source: %{name}-%{version}-r%{svn_rev}.zip

BuildRequires: gcc make subversion zip automake libtool

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
%if %(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')
%setup -q
%else
%setup -n "%{name}-%{version}" -Tc
svn export -r %{svn_rev} %{svn_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" "%{name}-%{version}")
%endif

# Convert docs to UTF-8
# NOTE: we do this _before_ applying of all patches, which are already UTF-8
#for f in CHANGES README; do
#    iconv -f iso-8859-1 -t utf8 < ${f} > ${f}.utf8
#    mv -f ${f}.utf8 ${f}
#done

# make sure configure is updated to properly support OS/2
buildconf

#autoreconf
# replace hard wired port numbers in the test suite
#sed -i s/899\\\([0-9]\\\)/%{?__isa_bits}9\\1/ tests/data/test*

%build

# curl m4 extensions override the nice autoconf PATH_SEPARATOR check with a very
# stupid method designed to always fail on Windows and OS/2
export PATH_SEPARATOR=';'

export CFLAGS="-Zomf $RPM_OPT_FLAGS"
export LDFLAGS="-Zomf -Zhigh-mem -Zargs-wild -Zargs-resp -Zbin-files"
export LIBS="-lurpo"
%configure \
    --disable-ipv6 \
    --disable-ldaps \
    --enable-manual \
    --with-ca-bundle=%{_sysconfdir}/pki/tls/certs/ca-bundle.crt \
    --with-gssapi=%{_prefix}/kerberos \
    --without-libidn \
    --without-libssh2 \
    --with-ssl --without-nss \
    --enable-shared --disable-static

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

#%define _curlbuild_h curlbuild-32.h
#mv $RPM_BUILD_ROOT%{_includedir}/curl/curlbuild.h \
#   $RPM_BUILD_ROOT%{_includedir}/curl/%{_curlbuild_h}
#install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_includedir}/curl/curlbuild.h

%clean
rm -rf $RPM_BUILD_ROOT

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
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man1/curl-config.1*
%{_mandir}/man3/*
%{_datadir}/aclocal/libcurl.m4

%changelog
* Tue Sep 2 2014 Dmitriy Kuminov <coding@dmik.org> 7.37.0-1
- Update to version 7.37.0.
- Use proper sleep function on OS/2.

* Mon Jan 16 2012 yd
- rebuild with libc 0.6.4 runtime.
