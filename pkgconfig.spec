#define svn_url     e:/trees/pkgconfig/trunk
%define svn_url     http://svn.netlabs.org/repos/ports/pkgconfig/trunk
%define svn_rev     1562

Summary: A tool for determining compilation options
Name: pkgconfig
Version: 0.29.1
Release: 1%{?dist}
Epoch: 1
License: GPLv2+
URL: http://pkgconfig.freedesktop.org
Group: Development/Tools
Vendor: bww bitwise works GmbH
Source: %{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip

BuildRequires: autoconf, automake, libtool
BuildRequires: glib2-devel

Provides: pkgconfig(pkg-config) = %{version}

%description
The pkgconfig tool determines compilation options. For each required
library, it reads the configuration file and outputs the necessary
compiler and linker flags.

%prep
%if %{?svn_rev:%(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')}%{!?svn_rev):0}
%setup -q
%else
%setup -n "%{name}-%{version}" -Tc
svn export %{?svn_rev:-r %{svn_rev}} %{svn_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip" "%{name}-%{version}")
%endif

%build
autoreconf -fi
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
%configure \
        --disable-shared \
        --with-installed-glib \
        "--with-pc-path=%{_libdir}/pkgconfig;%{_datadir}/pkgconfig" \
        --with-system-include-path=%{_includedir} \
        --enable-host-tool=no

make

%install
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_libdir}/pkgconfig
mkdir -p $RPM_BUILD_ROOT%{_datadir}/pkgconfig

# we include this below, already
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/pkg-config

%files
%doc AUTHORS README NEWS COPYING pkg-config-guide.html
%{_mandir}/*/*
%{_bindir}/*
%{_libdir}/pkgconfig
%{_datadir}/pkgconfig
%{_datadir}/aclocal/*

%changelog


%changelog
* Fri Apr 29 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> 0.29.1-1
- updated to version 0.29.1

* Sat Aug 27 2011 yd <yd@os2power.com> 0.25-4
- Initial version
