Summary: A portable x86 assembler which uses Intel-like syntax
Name: nasm
Version: 2.11.08
Release: 1%{?dist}
License: BSD
Group: Development/Languages
URL: http://www.nasm.us
#define svn_url	    e:/trees/nasm/trunk
%define svn_url     http://svn.netlabs.org/repos/ports/nasm/trunk
%define svn_rev     1048

Source0: %{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip
Source1: http://www.nasm.us/pub/nasm/releasebuilds/%{version}/%{name}-%{version}-xdoc.tar.bz2

BuildRequires: perl
BuildRequires: autoconf
#Requires(post): /sbin/install-info
#Requires(preun): /sbin/install-info

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%package rdoff
Summary: Tools for the RDOFF binary format, sometimes used with NASM
Group: Development/Tools

%package doc
Summary: Documentation for NASM
BuildRequires: texinfo
#BuildRequires: ghostscript, texinfo
BuildArch: noarch
# For arch to noarch conversion
Obsoletes: %{name}-doc < %{version}-%{release}

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

%package debug
Summary: HLL debug data for exception handling support

%description debug
%{summary}.

%prep
%if %{?svn_rev:%(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')}%{?!svn_rev):0}
%setup -q
%else
%setup -n "%{name}-%{version}" -Tc
svn export %{?svn_rev:-r %{svn_rev}} %{svn_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip" "%{name}-%{version}")
%endif
tar xjf %{SOURCE1} --strip-components 1

%build
sh autogen.sh
export LDFLAGS="-Zbin-files -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
# as long as ghostscript is not there as rpm, take care that ps2pdf.cmd and gsos2
# are found in the path
export PS2PDF=ps2pdf.cmd
%configure
make everything %{?_smp_mflags}
gzip -9f doc/nasmdoc.ps
gzip -9f doc/nasmdoc.txt

%install
rm -rf $RPM_BUILD_ROOT
make INSTALLROOT=$RPM_BUILD_ROOT install install_rdf
install -d $RPM_BUILD_ROOT/%{_infodir}
install -t $RPM_BUILD_ROOT/%{_infodir} doc/info/*

%clean
rm -rf ${RPM_BUILD_ROOT}

#%post
#if [ -e %{_infodir}/nasm.info.gz ]; then
#  /sbin/install-info %{_infodir}/nasm.info.gz  %{_infodir}/dir || :
#fi

#%preun
#if [ $1 = 0 -a -e %{_infodir}/nasm.info.gz ]; then
#  /sbin/install-info --delete %{_infodir}/nasm.info.gz %{_infodir}/dir || :
#fi

%files
%doc AUTHORS CHANGES README TODO
%{_bindir}/nasm.exe
%{_bindir}/ndisasm.exe
%{_mandir}/man1/nasm*
%{_mandir}/man1/ndisasm*
%{_infodir}/nasm.info*

%files doc
%doc doc/html doc/nasmdoc.txt.gz doc/nasmdoc.ps.gz doc/nasmdoc.pdf

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

%files debug
%{_bindir}/*.dbg

%changelog
* Thu Apr 30 2015 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.11.8-1
- update to 2.11.8