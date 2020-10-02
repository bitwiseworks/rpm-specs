Name:		transfig
Version:	3.2.7b
Release:	1%{?dist}
Epoch:		1
Summary:	Utility for converting FIG files (made by xfig) to other formats
License:	MIT
URL:		https://sourceforge.net/projects/mcj/

Vendor:		bww bitwise works GmbH
%scm_source     github https://github.com/bitwiseworks/fig2dev-os2 %{version}-os2

Requires:	ghostscript
Requires:	bc
Requires:	netpbm-progs

BuildRequires:	gcc libtool
BuildRequires:	libpng-devel
BuildRequires:	libjpeg-devel
%if !0%{?os2_version}
BuildRequires:	libXpm-devel
%endif
BuildRequires:	ghostscript

%description
The transfig utility creates a makefile which translates FIG (created
by xfig) or PIC figures into a specified LaTeX graphics language (for
example, PostScript(TM)).  Transfig is used to create TeX documents
which are portable (i.e., they can be printed in a wide variety of
environments).

Install transfig if you need a utility for translating FIG or PIC
figures into certain graphics languages.

%debug_package

%prep
%scm_setup
autoreconf -fvi
# Fix the manpage not being in UTF-8
%if !0%{?os2_version}
iconv -f ISO-8859-15 -t UTF-8 man/fig2dev.1.in -o fig2dev.1.in.new
touch -r man/fig2dev.1.in fig2dev.1.in.new
mv fig2dev.1.in.new man/fig2dev.1.in
%endif

%build
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"

%configure --enable-transfig
%if !0%{?os2_version}
%make_build
%else
make
%endif

%install
%make_install


%files
%doc CHANGES transfig/doc/manual.pdf
%if !0%{?os2_version}
%{_bindir}/transfig
%{_bindir}/fig2dev
%else
%{_bindir}/transfig.exe
%{_bindir}/fig2dev.exe
%endif
%{_bindir}/fig2ps2tex
%{_bindir}/pic2tpic
%{_datadir}/fig2dev/i18n/*.ps
%{_mandir}/man1/*.1.gz


%changelog
* Fri Oct 2 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1:3.2.7b-1
- first OS/2 rpm version
