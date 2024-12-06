Name:           yaz
Version:        5.34.2
Release:        1%{?dist}
Summary:        Z39.50/SRW/SRU toolkit
# SPDX confirmed
License:        BSD-3-Clause
URL:            http://www.indexdata.com/yaz/
%if 0%{?os2_version}
Vendor:         TeLLie OS2 forever
Distribution:   OS/2
Packager:       TeLLeRBoP
%endif
%if !0%{?os2_version}
Source0:        http://ftp.indexdata.com/pub/yaz/yaz-%{version}.tar.gz
%else
%scm_source github https://github.com/Tellie/%{name}-os2 %{version}-os2
%endif
BuildRequires:  gcc
BuildRequires:  bison
BuildRequires:  make

BuildRequires:  pkgconfig(libexslt)
BuildRequires:  pkgconfig(gnutls)
%if !0%{?os2_version}
BuildRequires:  pkgconfig(hiredis)
BuildRequires:  pkgconfig(libmemcached)
%endif
BuildRequires:  pkgconfig(icu-i18n)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(libxslt)

BuildRequires:  ncurses-devel
BuildRequires:  readline-devel
%if !0%{?os2_version}
BuildRequires:  /usr/bin/tclsh
%endif

Requires:       lib%{name}%{?_isa} = %{version}-%{release}

%description
YAZ is a programmers toolkit supporting the development of Z39.50/SRW/SRU 
clients and servers. Z39.50-2003 (version 3) as well as SRW/SRU version 1.1 
are supported in both the client and server roles. The SOLR webservice is 
supported in the client role through the ZOOM API.

The current version of YAZ includes support for the industry standard ZOOM 
API for Z39.50. This API vastly simplifies the process of writing new clients 
using YAZ, and it reduces your dependency on any single toolkit. YAZ can be 
used by itself to build Z39.50 applications in C.For programmers preferring 
another language, YAZ has three language bindings to commonly used application
development languages.

This package contains both a test-server and clients (normal & ssl).

%package -n     lib%{name}
Summary:        Shared libraries for %{name}

%description -n lib%{name}
This packages contains shared libraries for %{name}.

%package -n     lib%{name}-devel
Summary:        Development files for %{name}
Requires:       lib%{name}%{?_isa} = %{version}-%{release}

%description -n lib%{name}-devel
This package contains libraries and header files for
developing applications that use lib%{name}.

%package        doc
Summary:        Documentation for %{name}
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description    doc
This package contains documentation for %{name}, a Z39.50 protocol
server and client.

%prep
%if !0%{?os2_version}
%setup -q
%else
%scm_setup
%endif

%build
%if 0%{?os2_version}
export LDFLAGS=" -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx -ltinfo -lpthread"

# Set BUILDLEVEL to be embedded to all DLLs built with Libtool.
export LT_BUILDLEVEL="@#%{vendor}:%{version}-%{release}#@##1## `LANG=C date +'%%d %%b %%Y %%H:%%M:%%S'`     `uname -n`::::0::"
%endif
autoreconf -I M4 -fiv

sed -i.rpath configure \
	-e 's|hardcode_libdir_flag_spec=|hardcode_libdir_flag_spec_goodby=|' \
	-e '\@sys_lib_dlsearch_path_spec=@s|/lib /usr/lib|/lib /usr/lib %{_libdir} /%{_lib}|' \
	%{nil}

%configure \
        --enable-shared \
%if !0%{?os2_version}
        --with-memcached \
        --with-redis \
%else		
        --without-memcached \
        --without-redis \
%endif
        --disable-static \
        %{nil}

%make_build

%install
%make_install

# Remove cruft
%if !0%{?os2_version}
find %{buildroot} -name '*.*a' -delete -print
%else
find %{buildroot} -name '*.la' -delete -print
%endif

%check
%if !0%{?os2_version}
make check
%else
export BEGINLIBPATH=%{_builddir}/%{buildsubdir}/src/.libs
make -k check
%endif

%if !0%{?os2_version}
%ldconfig_scriptlets -n lib%{name}

%ldconfig_scriptlets -n lib%{name}
%endif

%files
%doc NEWS
%doc README.md
%license LICENSE
%if !0%{?os2_version}
%{_bindir}/yaz-client
%{_bindir}/yaz-iconv
%{_bindir}/yaz-icu
%{_bindir}/yaz-illclient
%{_bindir}/yaz-json-parse
%{_bindir}/yaz-marcdump
%{_bindir}/yaz-record-conv
%{_bindir}/yaz-url
%{_bindir}/yaz-ztest
%{_bindir}/zoomsh
%else
%{_bindir}/yaz-client.exe
%{_bindir}/yaz-iconv.exe
%{_bindir}/yaz-icu.exe
%{_bindir}/yaz-illclient.exe
%{_bindir}/yaz-json-parse.exe
%{_bindir}/yaz-marcdump.exe
%{_bindir}/yaz-record-conv.exe
%{_bindir}/yaz-url.exe
%{_bindir}/yaz-ztest.exe
%{_bindir}/zoomsh.exe
%endif
%{_mandir}/man1/yaz-client.*
%{_mandir}/man1/yaz-iconv.*
%{_mandir}/man1/yaz-icu.*
%{_mandir}/man1/yaz-illclient.*
%{_mandir}/man1/yaz-json-parse.*
%{_mandir}/man7/yaz-log.*
%{_mandir}/man1/yaz-marcdump.*
%{_mandir}/man1/yaz-record-conv.*
%{_mandir}/man1/yaz-url.*
%{_mandir}/man8/yaz-ztest.*
%{_mandir}/man1/zoomsh.*

%files -n lib%{name}
%license LICENSE
%if !0%{?os2_version}
%{_libdir}/libyaz.so.5*
%{_libdir}/libyaz_icu.so.5*
%{_libdir}/libyaz_server.so.5*
%else
%{_libdir}/*.dll
%endif
%{_mandir}/man7/yaz.*
%{_mandir}/man7/bib1-attr.*

%files -n lib%{name}-devel
%doc NEWS README.md
%{_bindir}/yaz-asncomp
%{_bindir}/yaz-config
%{_libdir}/pkgconfig/*
%if !0%{?os2_version}
%{_libdir}/*.so
%else
%{_libdir}/*.a
%endif
%{_includedir}/%{name}/
%{_datadir}/yaz/
%{_datadir}/aclocal/*
%{_mandir}/man1/yaz-asncomp.*
%{_mandir}/man1/yaz-config.*

%files -n %{name}-doc
%if !0%{?os2_version}
%{_pkgdocdir}
%else
%{_docdir}/yaz/*
%endif

%changelog
* Fri Dec 06 2024 Elbert Pol <elbert.pol@gmail.com> - 5.34.2-1
- Updated to latest version

* Fri Oct 06 2023 Elbert Pol <elbert.pol@gmail.com> - 5.34.0-1
- Updated to latest version

* Mon Jan 02 2023 Elbert Pol <elbert.pol@gmail.com> - 5.33.0-1
- Updated to latest version

* Thu Apr 07 2022 Elbert Pol <elbert.pol@gmail.com - 5.31.1-2
_ Update spec file to right Fedora spec.

* Fri Mar 25 2022 Elbert Pol <elbert.pol@gmail.com> - 5.31.1-1
- Updated to latest version
- Thankz Silvan for helping me fixing some problems.

* Sat May 08 2021 Elbert Pol <elbert.pol@gmail.com> - 5.31.0-1
- Updated to latest version

* Tue Oct 20 2020 Elbert Pol <elbert.pol@gmail.com> - 5.30.3-3
- Add the forgotten %{dist}

* Sun Oct 18 2020 Elbert Pol <elbert.pol@gmail.com> - 5.30.3-2
- Update to own github source
- Updated the spec file

* Sat Aug 01 2020 Elbert Pol <elbert.pol@gmail.com> - 5.30.3-1
- Updated to latest source
- Updated the spec file
- Added patched to get is build and to get the test build

* Thu Jul 26 2018 Elbert Pol <elbert.pol@gmail.com> -5.26.1-4
- Updated to latest Xslt and Xml2

* Wed Jul 25 2018 Elbert Pol <elbert.pol@gmail.com> -5.26.1-3
- Add $(exeext) for tclsh

* Sat Jul 14 2018 Elbert Pol <elbert.pol@gmail.com> - 5.26.1-2
- remove some dependicies

* Sat Jul 14 2018 Elbert Pol <elbert.pol@gmail.com> - 5.26.1-1
- Initial build for OS2
