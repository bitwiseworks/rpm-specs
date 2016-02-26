Summary: Command-line tools and library for transforming PDF files
Name:    qpdf
Version: 6.0.0
Release: 1%{?dist}
# MIT: e.g. libqpdf/sha2.c
License: Artistic 2.0 and MIT
URL:     http://qpdf.sourceforge.net/
Vendor:	 bww bitwise works GmbH
#Source0: http://downloads.sourceforge.net/sourceforge/qpdf/qpdf-%{version}.tar.gz

#define svn_url	    e:/trees/libqpdf/trunk
%define svn_url     http://svn.netlabs.org/repos/ports/libqpdf/trunk
%define svn_rev     1344

Source: %{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip

BuildRequires: zlib-devel
BuildRequires: pcre-devel

# for fix-qdf and test suite
BuildRequires: perl
# as we disabled the testsuit in the rpm build process we don't need the below
# requirement
#BuildRequires: perl(Digest::MD5)

# for autoreconf
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool

Requires: qpdf-libs = %{version}-%{release}

%package libs
Summary: QPDF library for transforming PDF files
Group:   System Environment/Libraries

%package devel
Summary: Development files for QPDF library
Group:   Development/Libraries
Requires: qpdf-libs = %{version}-%{release}

%package doc
Summary: QPDF Manual
Group:   Documentation
BuildArch: noarch
Requires: qpdf-libs = %{version}-%{release}

%description
QPDF is a command-line program that does structural, content-preserving
transformations on PDF files. It could have been called something
like pdf-to-pdf. It includes support for merging and splitting PDFs
and to manipulate the list of pages in a PDF file. It is not a PDF viewer
or a program capable of converting PDF into other formats.

%description libs
QPDF is a C++ library that inspect and manipulate the structure of PDF files.
It can encrypt and linearize files, expose the internals of a PDF file,
and do many other operations useful to PDF developers.

%description devel
Header files and libraries necessary
for developing programs using the QPDF library.

%description doc
QPDF Manual

%debug_package

%prep
%if %{?svn_rev:%(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')}%{?!svn_rev):0}
%setup -q
%else
%setup -n "%{name}-%{version}" -Tc
svn export %{?svn_rev:-r %{svn_rev}} %{svn_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip" "%{name}-%{version}")
%endif

sed -i -e '1s,^#!/usr/bin/env perl,#!/@unixroot/usr/bin/perl,' qpdf/fix-qdf
sed -i -e '1s,^#!/usr/bin/env perl,#!/@unixroot/usr/bin/perl,' qtest/bin/qtest-driver

%build
# work-around check-rpaths errors
export LDFLAGS='-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp'
autoreconf --verbose --force --install

%configure --enable-shared --disable-static\
           --enable-show-failed-test-output \
           --disable-os-secure-random --enable-insecure-random

make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

rm -f %{buildroot}%{_libdir}/libqpdf.la

%check
#make check

#post libs -p /sbin/ldconfig

#postun libs -p /sbin/ldconfig

%files
%{_bindir}/fix-qdf
%{_bindir}/qpdf.exe
%{_bindir}/zlib-flate.exe
%{_mandir}/man1/*

%files libs
%doc README TODO ChangeLog Artistic-2.0
%{_libdir}/qpdf*.dll

%files devel
%doc examples/*.cc examples/*.c
%{_includedir}/*
%{_libdir}/qpdf*_dll.a
%{_libdir}/pkgconfig/libqpdf.pc

%files doc
%{_defaultdocdir}/qpdf


%changelog
* Fri Feb 19 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 6.0.0-1
- initial version
