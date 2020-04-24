%bcond_without documentation

Summary: A portable x86 assembler which uses Intel-like syntax
Name: nasm
Version: 2.14.02
Release: 1%{?dist}
License: BSD
URL: http://www.nasm.us
Vendor: bww bitwise works GmbH
%scm_source github https://github.com/bitwiseworks/%{name}-os2 %{version}-os2
Source1: http://www.nasm.us/pub/nasm/releasebuilds/%{version}/%{name}-%{version}-xdoc.tar.bz2

BuildRequires: perl
BuildRequires: autoconf
BuildRequires: asciidoc
BuildRequires: xmlto
BuildRequires: gcc
BuildRequires: make

%if %{with documentation}
%package doc
Summary: Documentation for NASM
BuildRequires: perl(Font::TTF::Font)
BuildRequires: perl(Sort::Versions)
BuildRequires: perl(File::Spec)
BuildRequires: adobe-source-sans-pro-fonts
BuildRequires: adobe-source-code-pro-fonts
BuildRequires: ghostscript
BuildArch: noarch
# For arch to noarch conversion
Obsoletes: %{name}-doc < %{version}-%{release}
%endif

%package rdoff
Summary: Tools for the RDOFF binary format, sometimes used with NASM

%description
NASM is the Netwide Assembler, a free portable assembler for the Intel
80x86 microprocessor series, using primarily the traditional Intel
instruction mnemonics and syntax.

%if %{with documentation}
%description doc
This package contains documentation for the Netwide Assembler (NASM),
in HTML, info, PostScript, and text formats.
%endif

%description rdoff
Tools for the operating-system independent RDOFF binary format, which
is sometimes used with the Netwide Assembler (NASM). These tools
include linker, library manager, loader, and information dump.

%debug_package

%prep
%scm_setup

tar xjf %{SOURCE1} --strip-components 1

%build
autoreconf
export LDFLAGS="-Zbin-files -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
%configure
%if %{with documentation}
make everything %{?_smp_mflags}
gzip -9f doc/nasmdoc.ps
gzip -9f doc/nasmdoc.txt
%else
make all %{?_smp_mflags}
%endif

%install
%make_install install_rdf

%files
%doc AUTHORS CHANGES README TODO
%{_bindir}/nasm.exe
%{_bindir}/ndisasm.exe
%{_mandir}/man1/nasm*
%{_mandir}/man1/ndisasm*

%if %{with documentation}
%files doc
%doc doc/html doc/nasmdoc.txt.gz doc/nasmdoc.ps.gz doc/nasmdoc.pdf
%endif

%files rdoff
%{_bindir}/ldrdf.exe
%{_bindir}/rdf2bin.exe
%{_bindir}/rdf2ihx.exe
%{_bindir}/rdf2com.exe
%{_bindir}/rdfdump.exe
%{_bindir}/rdflib.exe
%{_bindir}/rdx.exe
%{_bindir}/rdf2ith.exe
%{_bindir}/rdf2srec.exe
%{_mandir}/man1/rd*
%{_mandir}/man1/ld*

%changelog
* Thu Apr 23 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.14.02-1
- updated to vendor version 2.14.02
- synchronized with fedora spec

* Wed Feb 21 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.13.03-1
- updated to vendor version 2.13.03

* Tue Dec 29 2015 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.11.8-2
- added enhancement from http://sourceforge.net/p/nasm/mailman/message/34609638/
  this is needed for vbox port, see vbox ticket #31 for further reference
- changed debug creation to latest rpm macros

* Thu Apr 30 2015 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.11.8-1
- update to 2.11.8