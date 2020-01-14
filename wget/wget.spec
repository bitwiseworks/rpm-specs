Summary: A utility for retrieving files using the HTTP or FTP protocols
Name: wget
Version: 1.20.3
Release: 2%{?dist}
License: GPLv3+
Url: http://www.gnu.org/software/wget/

Vendor:  bww bitwise works GmbH
%scm_source  github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2-2

Provides: webclient
Requires: libcx >= 0.4
# needed for test suite
#BuildRequires: perl-HTTP-Daemon, python2
BuildRequires: openssl-devel, pkgconfig, texinfo
BuildRequires: gettext >= 0.19, autoconf
BuildRequires: libidn2-devel, libpsl-devel, gcc, zlib-devel
#BuildRequires: gnutls-devel, perl-podlators, libmetalink-devel, gpgme-devel

%description
GNU Wget is a file retrieval utility which can use either the HTTP or
FTP protocols. Wget features include the ability to work in the
background while you are logged out, recursive retrieval of
directories, file name wildcard matching, remote file timestamp
storage and comparison, use of Rest with FTP servers and Range with
HTTP servers to retrieve files over slow or unstable connections,
support for Proxy servers, and configurability.


%debug_package


%prep
%scm_setup

autoreconf -fvi


%build
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
#    --with-ssl=gnutls \
#    --with-metalink \
#    --enable-ipv6 \
%configure \
    --with-ssl=openssl \
    --with-openssl \
    --with-libpsl \
    --enable-largefile \
    --enable-opie \
    --enable-digest \
    --enable-ntlm \
    --enable-nls \
    --disable-rpath

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT CFLAGS="$RPM_OPT_FLAGS"
rm -f $RPM_BUILD_ROOT/%{_infodir}/dir

%find_lang %{name}

%check
#make check

%files -f %{name}.lang
%doc AUTHORS MAILING-LIST NEWS README COPYING doc/sample.wgetrc
%config(noreplace) %{_sysconfdir}/wgetrc
%{_mandir}/man1/wget.*
%{_bindir}/wget.exe
%{_infodir}/*

%changelog
* Mon Jan 13 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.20.3-2
- enable libidn2

* Fri Nov 08 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.20.3-1
- update to version 1.20.3

* Wed Feb 08 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.18-3
- workaround libc ticket #310 pathconf()
- use the new scm_source and scm_setup macros

* Fri Nov 25 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.18-2
- enable libidn and libpsl

* Mon Nov 14 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.18-1
- Initial version 1.18