Summary: Command-line tools and library for transforming PDF files
Name:    qpdf
Version: 9.0.1
Release: 1%{?dist}
# MIT: e.g. libqpdf/sha2.c
# upstream uses ASL 2.0 now, but he allowed other to distribute qpdf under
# old license (see README)
License: (Artistic 2.0 or ASL 2.0) and MIT
URL:     http://qpdf.sourceforge.net/

Vendor:	 bww bitwise works GmbH
%scm_source github http://github.com/bitwiseworks/libqpdf-os2 %{version}-os2

BuildRequires: gcc
BuildRequires: zlib-devel
BuildRequires: libjpeg-turbo-devel
BuildRequires: pcre-devel

# for fix-qdf and test suite
BuildRequires: perl
# as we disabled the testsuit in the rpm build process we don't need the below
# requirement
#BuildRequires: perl-generators
#BuildRequires: perl(Digest::MD5)

# for autoreconf
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool

Requires: %{name}-libs = %{version}-%{release}

%package libs
Summary: QPDF library for transforming PDF files

%package devel
Summary: Development files for QPDF library
Requires: %{name}-libs = %{version}-%{release}

%package doc
Summary: QPDF Manual
BuildArch: noarch
Requires: %{name}-libs = %{version}-%{release}

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
%scm_setup

sed -i -e '1s,^#!/usr/bin/env perl,#!/@unixroot/usr/bin/perl,' qpdf/fix-qdf

%build
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"
export VENDOR="%{vendor}"

# work-around check-rpaths errors
autoreconf --verbose --force --install
# automake files needed to be regenerated in 8.4.0 - check if this can be removed
# in the next qpdf release
./autogen.sh

%configure --disable-static\
           --enable-show-failed-test-output \
           --disable-os-secure-random --enable-insecure-random \
           --docdir=%{_pkgdocdir}


make %{?_smp_mflags}

%install
%make_install

rm -f %{buildroot}%{_libdir}/libqpdf.la

%check
#make check

#ldconfig_scriptlets libs
 
%files
%{_bindir}/fix-qdf
%{_bindir}/qpdf.exe
%{_bindir}/zlib-flate.exe
%{_mandir}/man1/*

%files libs
%doc README.md TODO ChangeLog
%license Artistic-2.0
%{_libdir}/qpdf*.dll

%files devel
%doc examples/*.cc examples/*.c
%{_includedir}/*
%{_libdir}/qpdf*_dll.a
%{_libdir}/pkgconfig/libqpdf.pc

%files doc
%{_pkgdocdir}


%changelog
* Wed Sep 25 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> - 9.0.1-1
- update to version 9.0.1

* Fri Feb 19 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 6.0.0-1
- initial version
