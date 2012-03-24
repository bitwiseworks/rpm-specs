# -*- coding: utf-8 -*-
Summary: A portable x86 assembler which uses Intel-like syntax
Name: nasm
Version: 2.10
Release: 1%{?dist}
License: BSD
Group: Development/Languages
URL: http://www.nasm.us

Source0: nasm-%{version}.tar.xz
Source1: nasm-%{version}-xdoc.tar.xz

Patch0: nasm-os2.patch

BuildRequires: perl
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%package doc
Summary: Documentation for NASM
Group: Development/Languages
#BuildRequires: ghostscript, texinfo

%package rdoff
Summary: Tools for the RDOFF binary format, sometimes used with NASM
Group: Development/Tools

%description
NASM is the Netwide Assembler, a free portable assembler for the Intel
80x86 microprocessor series, using primarily the traditional Intel
instruction mnemonics and syntax.

%description doc
This package contains documentation for the Netwide Assembler (NASM),
in HTML, info, PostScript, and text formats.

%description rdoff
Tools for the operating-system independent RDOFF binary format, which
is sometimes used with the Netwide Assembler (NASM). These tools
include linker, library manager, loader, and information dump.

%prep
%setup -q
%patch0 -p1 -b .os2~
tar xf %{SOURCE1} --strip-components 1

%build

export CONFIG_SHELL="/@unixroot/usr/bin/sh.exe"
export LDFLAGS="-Zbin-files -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lurpo -lmmap"
%configure \
   "--cache-file=%{_topdir}/cache/%{name}-%{_target_cpu}.cache"

make %{?_smp_mflags}
gzip -9f doc/nasmdoc.ps
gzip -9f doc/nasmdoc.txt

%install
rm -rf $RPM_BUILD_ROOT
#mkdir -p $RPM_BUILD_ROOT%{_bindir}
#mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man1
make INSTALLROOT=$RPM_BUILD_ROOT install 
#install_rdf
install -d $RPM_BUILD_ROOT/%{_infodir}
install -t $RPM_BUILD_ROOT/%{_infodir} doc/info/*

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%doc AUTHORS CHANGES README TODO
%{_bindir}/nasm.exe
%{_bindir}/ndisasm.exe
%{_mandir}/*/*
%{_infodir}/nasm.info*

%files doc
%defattr(-,root,root)
%doc doc/html doc/nasmdoc.txt.gz doc/nasmdoc.ps.gz

#%files rdoff
#%defattr(-,root,root)
#%{_bindir}/ldrdf
#%{_bindir}/rdf2bin
#%{_bindir}/rdf2ihx
#%{_bindir}/rdf2com
#%{_bindir}/rdfdump
#%{_bindir}/rdflib
#%{_bindir}/rdx
#%{_bindir}/rdf2ith
#%{_bindir}/rdf2srec

%changelog
