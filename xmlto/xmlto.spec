%global with_tex 0

Summary: A tool for converting XML files to various formats
Name: xmlto
Version: 0.0.28
Release: 1%{?dist}
License: GPLv2+
URL: https://pagure.io/xmlto/

Vendor: bww bitwise works GmbH
%scm_source github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2


BuildRequires: docbook-xsl
BuildRequires: libxslt
BuildRequires: flex
#BuildRequires: util-linux
BuildRequires: getopt
BuildRequires: gcc

# We rely heavily on the DocBook XSL stylesheets!
Requires: docbook-xsl
Requires: libxslt
Requires: docbook-dtds
Requires: flex
#Requires: util-linux
Requires: getopt

%description
This is a package for converting XML files to various formats using XSL
stylesheets.

%if %{with_tex}
%package tex
License: GPLv2+
Summary: A set of xmlto backends with TeX requirements
# For full functionality, we need passivetex.
Requires: tex-passivetex
# We require main package
Requires: xmlto = %{version}-%{release}
BuildArch: noarch


%description tex
This subpackage contains xmlto backend scripts which do require
PassiveTeX/TeX for functionality.
%endif

%package xhtml
License: GPLv2+
Summary: A set of xmlto backends for xhtml1 source format
# For functionality we need stylesheets xhtml2fo-style-xsl
Requires: xhtml2fo-style-xsl
# We require main package
Requires: xmlto = %{version}-%{release}
BuildArch: noarch

%description xhtml
This subpackage contains xmlto backend scripts for processing
xhtml1 source format.

%debug_package

%prep
%scm_setup

%build
# we do autoreconf even fedora doesn't do it
autoreconf -fvi
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
export VENDOR="%{vendor}"
%configure BASH=/@unixroot/usr/bin/sh 
make %{?_smp_mflags}

%check
make check

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

%files
%doc COPYING ChangeLog README AUTHORS NEWS
%{_bindir}/*
%exclude %{_bindir}/*.dbg
%{_mandir}/*/*
%{_datadir}/xmlto
%exclude %{_datadir}/xmlto/format/fo/dvi
%exclude %{_datadir}/xmlto/format/fo/ps
%exclude %{_datadir}/xmlto/format/fo/pdf
%exclude %dir %{_datadir}/xmlto/format/xhtml1/
%exclude %{_datadir}/xmlto/format/xhtml1


%if %{with_tex}
%files tex
%{_datadir}/xmlto/format/fo/dvi
%{_datadir}/xmlto/format/fo/ps
%{_datadir}/xmlto/format/fo/pdf
%endif


%files xhtml
%dir %{_datadir}/xmlto/format/xhtml1/
%{_datadir}/xmlto/format/xhtml1/*


%changelog
* Tue Nov 12 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.0.28-1
- first OS/2 rpm version
