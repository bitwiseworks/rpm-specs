Name:           libpsl
Version:        0.17.0
Release:        1%{?dist}
Summary:        C library for the Publix Suffix List
License:        MIT
URL:            https://rockdaboot.github.io/libpsl

Vendor:         bww bitwise works GmbH
%scm_source svn http://svn.netlabs.org/repos/ports/libpsl/trunk 2118

BuildRequires:  gettext-devel
BuildRequires:  glib2-devel
#BuildRequires:  gtk-doc
BuildRequires:  libicu-devel
BuildRequires:  libxslt
#BuildRequires:  publicsuffix-list
Requires:       libcx >= 0.4

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
#Requires:       publicsuffix-list

%description    devel
This package contains libraries and header files for
developing applications that use %{name}.

%package -n     psl
Summary:        Commandline utility to explore the Public Suffix List

%description -n psl
This package contains a commandline utility to explore the Public Suffix List,
for example it checks if domains are public suffixes, checks if cookie-domain
is acceptable for domains and so on.


%debug_package


%prep
%scm_setup

autoreconf -fiv

%build

export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
export VENDOR="%{vendor}"
#           --with-psl-file=%{_datadir}/publicsuffix/effective_tld_names.dat           \
#           --with-psl-testfile=%{_datadir}/publicsuffix/test_psl.txt
#           --enable-gtk-doc \
%configure --disable-silent-rules \
           --disable-static \
           --enable-man
%make_build

%install
%make_install

# the corresponding script is noinst
rm %{buildroot}%{_mandir}/man1/psl-make-dafsa.1*

find %{buildroot} -name '*.la' -delete -print

%check
#make check || cat tests/test-suite.log

#%post -p /sbin/ldconfig

#%postun -p /sbin/ldconfig

%files
%license COPYING
%{_libdir}/psl*.dll

%files devel
%doc AUTHORS NEWS
#%{_datadir}/gtk-doc/html/libpsl/
%{_includedir}/libpsl.h
%{_libdir}/psl*_dll.a
%{_libdir}/pkgconfig/libpsl.pc
#%{_mandir}/man3/libpsl.3*

%files -n psl
%doc AUTHORS NEWS
%license COPYING
%{_bindir}/psl.exe
%{_mandir}/man1/psl.1*

%changelog
* Fri Mar 03 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.17.0-1
- update to version 0.17.0
- use the new scm_source and scm_setup macros

* Thu Nov 24 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.15.0-2
- libcx req is 0.4 and not 0.4.0

* Tue Nov 15 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.15.0-1
- first version
