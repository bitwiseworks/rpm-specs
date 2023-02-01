Summary: A utility for retrieving files using the HTTP or FTP protocols
Name: wget
Version: 1.21.3
Release: 1%{?dist}
License: GPLv3+
Url: http://www.gnu.org/software/wget/
%if !0%{?os2_version}
Source: ftp://ftp.gnu.org/gnu/wget/wget-%{version}.tar.gz

Patch1: wget-1.17-path.patch
Patch2: wget-1.21.3-hsts-32bit.patch
%else
Vendor:  bww bitwise works GmbH
%scm_source  github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2
%endif

Provides: webclient
Provides: bundled(gnulib) 
%if !0%{?os2_version}
Requires: libcx >= 0.4
%endif
# needed for test suite
BuildRequires: make
BuildRequires: perl(lib)
BuildRequires: perl(English)
%if !0%{?os2_version}
BuildRequires: perl(HTTP::Daemon)
%endif
BuildRequires: python3
BuildRequires: gnutls-devel
%if 0%{?os2_version}
BuildRequires: openssl-devel
%endif
BuildRequires: pkgconfig
BuildRequires: texinfo
BuildRequires: gettext
BuildRequires: autoconf
BuildRequires: libidn2-devel
%if !0%{?os2_version}
BuildRequires: libuuid-devel
BuildRequires: perl-podlators
%endif
BuildRequires: libpsl-devel
%if !0%{?os2_version}
BuildRequires: gpgme-devel
%endif
BuildRequires: gcc
BuildRequires: zlib-devel
%if !0%{?os2_version}
BuildRequires: libmetalink-devel
%endif
BuildRequires: git-core

%description
GNU Wget is a file retrieval utility which can use either the HTTP or
FTP protocols. Wget features include the ability to work in the
background while you are logged out, recursive retrieval of
directories, file name wildcard matching, remote file timestamp
storage and comparison, use of Rest with FTP servers and Range with
HTTP servers to retrieve files over slow or unstable connections,
support for Proxy servers, and configurability.

%if 0%{?os2_version}
%debug_package
%endif

%prep
%if !0%{?os2_version}
%autosetup -S git
%else
%scm_setup
autoreconf -fvi
%endif

# modify the package string
sed -i "s|\(PACKAGE_STRING='wget .*\)'|\1 (Red Hat modified)'|" configure
grep "PACKAGE_STRING='wget .* (Red Hat modified)'" configure || exit 1

%build
%if 0%{?os2_version}
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
%endif
%configure \
%if !0%{?os2_version}
    --with-ssl=gnutls \
%else
    --with-ssl=openssl \
    --with-openssl \
%endif
    --with-libpsl \
    --enable-largefile \
    --enable-opie \
    --enable-digest \
    --enable-ntlm \
    --enable-nls \
%if !0%{?os2_version}
    --enable-ipv6 \
%endif
    --disable-rpath \
%if !0%{?os2_version}
    --with-metalink \
%endif
    --disable-year2038

%if !0%{?os2_version}
%{make_build}
%else
make %{?_smp_mflags}
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{make_install} CFLAGS="$RPM_OPT_FLAGS"
rm -f $RPM_BUILD_ROOT/%{_infodir}/dir

%find_lang %{name}
%find_lang %{name}-gnulib

%check
%if !0%{?os2_version}
make check
%endif

%files -f %{name}.lang -f %{name}-gnulib.lang
%doc AUTHORS MAILING-LIST NEWS README COPYING doc/sample.wgetrc
%config(noreplace) %{_sysconfdir}/wgetrc
%{_mandir}/man1/wget.*
%if !0%{?os2_version}
%{_bindir}/wget
%else
%{_bindir}/wget.exe
%endif
%{_infodir}/*

%changelog
* Wed Feb 01 2023 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.21.3-1
- update to version 1.21.3
- resync with latest fedora spec
- fix ticket #2 (fix done by komh thx)

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