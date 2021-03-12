Name:           libpsl
Version:        0.21.1
Release:        1%{?dist}
Summary:        C library for the Publix Suffix List
License:        MIT
URL:            https://rockdaboot.github.io/libpsl
%if !0%{?os2_version}
Source0:        https://github.com/rockdaboot/libpsl/releases/download/%{version}/libpsl-%{version}.tar.gz
%else
Vendor:         bww bitwise works GmbH
%scm_source github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2
%endif
BuildRequires:  gcc
BuildRequires:  gettext-devel
BuildRequires:  glib2-devel
%if !0%{?os2_version}
BuildRequires:  gtk-doc
%endif
BuildRequires:  libicu-devel
BuildRequires:  libidn2-devel
BuildRequires:  libunistring-devel
BuildRequires:  libxslt
BuildRequires:  make
%if !0%{?os2_version}
BuildRequires:  publicsuffix-list
BuildRequires:  python3-devel
Requires:       publicsuffix-list-dafsa
%endif

%description
libpsl is a C library to handle the Public Suffix List. A "public suffix" is a
domain name under which Internet users can directly register own names.

Browsers and other web clients can use it to

- Avoid privacy-leaking "supercookies";
- Avoid privacy-leaking "super domain" certificates;
- Domain highlighting parts of the domain in a user interface;
- Sorting domain lists by site;

Libpsl...

- has built-in PSL data for fast access;
- allows to load PSL data from files;
- checks if a given domain is a "public suffix";
- provides immediate cookie domain verification;
- finds the longest public part of a given domain;
- finds the shortest private part of a given domain;
- works with international domains (UTF-8 and IDNA2008 Punycode);
- is thread-safe;
- handles IDNA2008 UTS#46;

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
%if !0%{?os2_version}
Requires:       publicsuffix-list
%endif

%description    devel
This package contains libraries and header files for
developing applications that use %{name}.

%package -n     psl
Summary:        Commandline utility to explore the Public Suffix List

%description -n psl
This package contains a commandline utility to explore the Public Suffix List,
for example it checks if domains are public suffixes, checks if cookie-domain
is acceptable for domains and so on.

%package -n     psl-make-dafsa
Summary:        Compiles the Public Suffix List into DAFSA form

%description -n psl-make-dafsa
This script produces C/C++ code or an architecture-independent binary object
which represents a Deterministic Acyclic Finite State Automaton (DAFSA)
from a plain text Public Suffix List.


%debug_package

%prep
%if !0%{?os2_version}
%autosetup -p1
rm -frv list
ln -sv %{_datadir}/publicsuffix list
sed -i -e "1s|#!.*|#!%{__python3}|" src/psl-make-dafsa
%else
%scm_setup
autoreconf -fiv
%endif

%build
%if 0%{?os2_version}
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
export VENDOR="%{vendor}"
%endif

# Tarballs from github have 2 versions, one is raw files from repo, and
# the other one from CDN contains pre-generated autotools files.
# But makefile hack is not upstreamed yet so we continue reconfiguring these.
# [ -f configure ] || autoreconf -fiv
# autoreconf -fiv

# libicu does allow support for a newer IDN specification (IDN 2008) than
# libidn 1.x (IDN 2003). However, libpsl mostly relies on an internally
# compiled list, which is generated at buildtime and the testsuite thereof
# requires either libidn or libicu only at buildtime; the runtime
# requirement is only for loading external lists, which IIUC neither curl
# nor wget support. libidn2 supports IDN 2008 as well, and is *much* smaller
# than libicu.
#
# curl (as of 7.51.0-1.fc25) and wget (as of 1.19-1.fc26) now depend on libidn2.
# Therefore, we use libidn2 at runtime to help minimize core dependencies.
%configure --disable-silent-rules \
           --disable-static       \
           --enable-man           \
%if !0%{?os2_version}
           --enable-gtk-doc       \
%endif
           --enable-builtin=libicu \
           --enable-runtime=libidn2 \
%if !0%{?os2_version}
           --with-psl-distfile=%{_datadir}/publicsuffix/public_suffix_list.dafsa  \
           --with-psl-file=%{_datadir}/publicsuffix/effective_tld_names.dat       \
           --with-psl-testfile=%{_datadir}/publicsuffix/test_psl.txt
%endif

# avoid using rpath
sed -i libtool \
    -e 's|^\(runpath_var=\).*$|\1|' \
    -e 's|^\(hardcode_libdir_flag_spec=\).*$|\1|'

%if !0%{?os2_version}
%make_build
%else
make %{?_smp_mflags}
%endif

%install
%make_install

# the script is noinst but the manpage is installed
install -m0755 src/psl-make-dafsa %{buildroot}%{_bindir}/

find %{buildroot} -name '*.la' -delete -print


%check
%if 0%{?os2_version}
export BEGINLIBPATH=%{_builddir}/%{buildsubdir}/src/.libs
%endif
make check || cat tests/test-suite.log

%if !0%{?os2_version}
%ldconfig_scriptlets
%endif

%files
%license COPYING
%if !0%{?os2_version}
%{_libdir}/libpsl.so.5
%{_libdir}/libpsl.so.5.*
%else
%{_libdir}/psl*.dll
%endif

%files devel
%doc AUTHORS NEWS
%{_datadir}/gtk-doc/html/libpsl/
%{_includedir}/libpsl.h
%if !0%{?os2_version}
%{_libdir}/libpsl.so
%else
%{_libdir}/psl*_dll.a
%endif
%{_libdir}/pkgconfig/libpsl.pc
%if !0%{?os2_version}
%{_mandir}/man3/libpsl.3*
%endif

%files -n psl
%doc AUTHORS NEWS
%license COPYING
%if !0%{?os2_version}
%{_bindir}/psl
%else
%{_bindir}/psl.exe
%endif
%{_mandir}/man1/psl.1*

%files -n psl-make-dafsa
%license COPYING
%{_bindir}/psl-make-dafsa
%{_mandir}/man1/psl-make-dafsa.1*

%changelog
* Fri Mar 12 2021 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.21.1-1
- update to version 0.21.1
- resync with fedora spec

* Fri Mar 03 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.17.0-1
- update to version 0.17.0
- use the new scm_source and scm_setup macros

* Thu Nov 24 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.15.0-2
- libcx req is 0.4 and not 0.4.0

* Tue Nov 15 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.15.0-1
- first version
