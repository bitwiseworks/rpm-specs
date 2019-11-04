Summary:	The ASN.1 library used in GNUTLS
Name:		libtasn1
Version:	4.14
Release:	1%{?dist}

# The libtasn1 library is LGPLv2+, utilities are GPLv3+
License:	GPLv3+ and LGPLv2+
URL:		http://www.gnu.org/software/libtasn1/
Vendor:		bww bitwise works GmbH
%scm_source     github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2

BuildRequires:	gcc
BuildRequires:	bison, pkgconfig, help2man
BuildRequires:	autoconf, automake, libtool
#BuildRequires:	valgrind-devel
# Wildcard bundling exception https://fedorahosted.org/fpc/ticket/174
Provides: bundled(gnulib) = 20130324

%package devel
Summary:	Files for development of applications which will use libtasn1
Requires:	%{name} = %{version}-%{release}

Requires:	%name = %version-%release
Requires:	%{name}-tools = %{version}-%{release}
Requires:	pkgconfig


%package tools
Summary:	Some ASN.1 tools
License:	GPLv3+
Requires:	%{name} = %{version}-%{release}


%description
A library that provides Abstract Syntax Notation One (ASN.1, as specified
by the X.680 ITU-T recommendation) parsing and structures management, and
Distinguished Encoding Rules (DER, as per X.690) encoding and decoding functions.

%description devel
This package contains files for development of applications which will
use libtasn1.


%description tools
This package contains simple tools that can decode and encode ASN.1
data.

%debug_package


%prep
%scm_setup


%build
autoreconf -v -f --install

export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
export VENDOR="%{vendor}"
%configure --disable-static --disable-silent-rules
# libtasn1 likes to regenerate docs
touch doc/stamp_docs
# recreate ASN1.c with bison
touch lib/ASN1.y

make %{?_smp_mflags}


%install
make DESTDIR="$RPM_BUILD_ROOT" install

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_infodir}/dir


%check
export BEGINLIBPATH=%{_builddir}/%{buildsubdir}/lib/.libs
make check

%files
%license LICENSE doc/COPYING*
%doc AUTHORS NEWS README.md
%{_libdir}/*.dll

%files tools
%{_bindir}/asn1*
%{_mandir}/man1/asn1*

%files devel
%doc doc/TODO doc/*.pdf
%{_libdir}/*_dll.a
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_infodir}/*.info.*
%{_mandir}/man3/*asn1*


%changelog
* Mon Nov 04 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> - 4.14-1
- initial OS/2 RPM
