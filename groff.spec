%global with_x 0

Summary: A document formatting system
Name: groff
Version: 1.22.3
Release: 1%{?dist}
License: GPLv3+ and GFDL and BSD and MIT
Group: Applications/Publishing
URL: http://www.gnu.org/software/groff/
Vendor: bww bitwise works GmbH
%scm_source github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2

Requires: coreutils, groff-base = %{version}-%{release}
BuildRequires: gcc
BuildRequires: git, netpbm-progs, perl-generators, psutils, ghostscript
Provides: nroff-i18n = %{version}-%{release}

%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\([^.]*\\.pl\\)

%description
Groff is a document formatting system. Groff takes standard text and
formatting commands as input and produces formatted output. The
created documents can be shown on a display or printed on a printer.
Groff's formatting commands allow you to specify font type and size,
bold type, italic type, the number and size of columns on a page, and
more.

Groff can also be used to format man pages. If you are going to use
groff with the X Window System, you will also need to install the
groff-x11 package.

%package base
Summary: Parts of the groff formatting system required to display manual pages
Group: Applications/Publishing

%description base
The groff-base package contains only necessary parts of groff formatting
system which are required to display manual pages, and the groff's default
display device (PostScript).

%package perl
Summary: Parts of the groff formatting system that require Perl
Group: Applications/Publishing
Requires: groff-base = %{version}-%{release}

%description perl
The groff-perl package contains the parts of the groff text processor
package that require Perl. These include the afmtodit (font processor
for creating PostScript font files), groffer (tool for displaying groff
files), grog (utility that can be used to automatically determine groff
command-line options), chem (groff preprocessor for producing chemical
structure diagrams), mmroff (reference preprocessor) and roff2dvi
roff2html roff2pdf roff2ps roff2text roff2x (roff code converters).

%if %{with_x}
%package x11
Summary: Parts of the groff formatting system that require X Windows System
Group: Applications/Publishing
Requires: groff-base = %{version}-%{release}
BuildRequires: libXaw-devel, libXmu-devel
Provides: groff-gxditview = %{version}-%{release}
Obsoletes: groff-gxditview < 1.20.1

%description x11
The groff-x11 package contains the parts of the groff text processor
package that require X Windows System. These include gxditview (display
groff intermediate output files on X Window System display) and
xtotroff (converts X font metrics into groff font metrics).
%endif

%package doc
Summary: Documentation for groff document formatting system
Group: Documentation
BuildArch: noarch
Requires: groff = %{version}-%{release}

%description doc
The groff-doc package includes additional documentation for groff
text processor package. It contains examples, documentation for PIC
language and documentation for creating PDF files.

%debug_package

%prep
%scm_setup

%if 0
for file in NEWS src/devices/grolbp/grolbp.man doc/{groff.info*,webpage.ms} \
                contrib/mm/*.man contrib/mom/examples/{README.txt,*.mom,mom.vim}; do
    iconv -f iso-8859-1 -t utf-8 < "$file" > "${file}_"
    mv "${file}_" "$file"
done
%endif

# Create files necessary for configure
autoreconf -fvi -I m4
# do the same in the gnulib part
cd src/libs/gnulib
autoreconf -fvi

%build
export LDFLAGS=" -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
%configure \
    --docdir=%{_pkgdocdir} \
    --with-appresdir=%{_datadir}/X11/app-defaults \
    --with-grofferdir=%{_datadir}/%{name}/%{version}/groffer
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

# some binaries need alias with 'g' or 'z' prefix
for file in gnroff gtroff gtbl gpic geqn gneqn grefer glookbib gindxbib gsoelim zsoelim; do
    ln -s ${file#?} %{buildroot}%{_bindir}/${file}
    ln -s ${file#?}.1.gz %{buildroot}%{_mandir}/man1/${file}.1.gz
done

# charset.alias is really not needed
rm -f %{buildroot}%{_libdir}/charset.alias
# as we don't have X we need to remove those files
rm -f %{buildroot}%{_datadir}/%{name}/%{version}/tmac/X.tmac
rm -f %{buildroot}%{_datadir}/%{name}/%{version}/tmac/Xps.tmac

# fix absolute symlink to relative symlink
rm -f %{buildroot}%{_pkgdocdir}/pdf/mom-pdf.pdf
ln -s ../examples/mom/mom-pdf.pdf %{buildroot}%{_pkgdocdir}/pdf/mom-pdf.pdf

# rename groff downloadable postscript fonts to meet Fedora Font Packaging guidelines,
# as these files are more PS instructions, than general-purpose fonts (bz #477394)
for file in $(find %{buildroot}%{_datadir}/%{name}/%{version}/font/devps -name "*.pfa"); do
    mv ${file} ${file}_
done
sed --in-place 's/\.pfa$/.pfa_/' %{buildroot}%{_datadir}/%{name}/%{version}/font/devps/download

# remove unnecessary files
rm -f %{buildroot}%{_infodir}/dir

# fix privileges
chmod 755 %{buildroot}%{_datadir}/groff/%{version}/groffer/version.sh
chmod 755 %{buildroot}%{_datadir}/groff/%{version}/font/devlj4/generate/special.awk

# I dislike the below fedora change, so I disabled it
%if 0
# remove CreationDate from documentation
pushd %{buildroot}%{_pkgdocdir}
    find -name "*.html" | xargs sed -i "/^<!-- CreationDate: /d"
    find -name "*.ps"   | xargs sed -i "/^%%%%CreationDate: /d"
popd
%endif

# /bin/sed is in /@unixroot/usr/bin/sed in
sed --in-place 's|#! /bin/sed -f|#! /@unixroot/usr/bin/sed -f|' %{buildroot}%{_datadir}/groff/%{version}/font/devps/generate/symbol.sed

%files
# data
%{_datadir}/%{name}/%{version}/font/devdvi/
%{_datadir}/%{name}/%{version}/font/devlbp/
%{_datadir}/%{name}/%{version}/font/devlj4/
%{_datadir}/%{name}/%{version}/oldfont/
%{_datadir}/%{name}/%{version}/pic/
%{_datadir}/%{name}/%{version}/tmac/62bit.tmac
%{_datadir}/%{name}/%{version}/tmac/a4.tmac
%{_datadir}/%{name}/%{version}/tmac/dvi.tmac
%{_datadir}/%{name}/%{version}/tmac/e.tmac
%{_datadir}/%{name}/%{version}/tmac/ec.tmac
%{_datadir}/%{name}/%{version}/tmac/hdmisc.tmac
%{_datadir}/%{name}/%{version}/tmac/hdtbl.tmac
%{_datadir}/%{name}/%{version}/tmac/lbp.tmac
%{_datadir}/%{name}/%{version}/tmac/lj4.tmac
%{_datadir}/%{name}/%{version}/tmac/m.tmac
%{_datadir}/%{name}/%{version}/tmac/me.tmac
%{_datadir}/%{name}/%{version}/tmac/mm.tmac
%{_datadir}/%{name}/%{version}/tmac/mm/
%{_datadir}/%{name}/%{version}/tmac/mmse.tmac
%{_datadir}/%{name}/%{version}/tmac/mom.tmac
%{_datadir}/%{name}/%{version}/tmac/ms.tmac
%{_datadir}/%{name}/%{version}/tmac/mse.tmac
%{_datadir}/%{name}/%{version}/tmac/om.tmac
%{_datadir}/%{name}/%{version}/tmac/pdfmark.tmac
%{_datadir}/%{name}/%{version}/tmac/refer-me.tmac
%{_datadir}/%{name}/%{version}/tmac/refer-mm.tmac
%{_datadir}/%{name}/%{version}/tmac/refer-ms.tmac
%{_datadir}/%{name}/%{version}/tmac/refer.tmac
%{_datadir}/%{name}/%{version}/tmac/s.tmac
%{_datadir}/%{name}/%{version}/tmac/spdf.tmac
%{_datadir}/%{name}/%{version}/tmac/trace.tmac
# programs
%{_bindir}/addftinfo.exe
%{_bindir}/eqn2graph
%{_bindir}/gdiffmk
%{_bindir}/grap2graph
%{_bindir}/grn.exe
%{_bindir}/grodvi.exe
%{_bindir}/grolbp.exe
%{_bindir}/grolj4.exe
%{_bindir}/hpftodit.exe
%{_bindir}/indxbib.exe
%{_bindir}/lkbib.exe
%{_bindir}/lookbib.exe
%{_bindir}/pdfroff
%{_bindir}/pfbtops.exe
%{_bindir}/pic2graph
%{_bindir}/refer.exe
%{_bindir}/tfmtodit.exe
%{_libdir}/groff/groff_opts_no_arg.txt
%{_libdir}/groff/groff_opts_with_arg.txt
%{_mandir}/man1/addftinfo.*
%{_mandir}/man1/eqn2graph.*
%{_mandir}/man1/gdiffmk.*
%{_mandir}/man1/grap2graph.*
%{_mandir}/man1/grn.*
%{_mandir}/man1/grodvi.*
%{_mandir}/man1/grohtml.*
%{_mandir}/man1/grolbp.*
%{_mandir}/man1/grolj4.*
%{_mandir}/man1/hpftodit.*
%{_mandir}/man1/indxbib.*
%{_mandir}/man1/lkbib.*
%{_mandir}/man1/lookbib.*
%{_mandir}/man1/pdfroff.*
%{_mandir}/man1/pfbtops.*
%{_mandir}/man1/pic2graph.*
%{_mandir}/man1/refer.*
%{_mandir}/man1/tfmtodit.*
# compatibility symlinks
%{_bindir}/grefer
%{_bindir}/glookbib
%{_bindir}/gindxbib
%{_mandir}/man1/grefer.*
%{_mandir}/man1/glookbib.*
%{_mandir}/man1/gindxbib.*
# groff processor documentation
%{_mandir}/man5/*
%{_mandir}/man7/*
%{_infodir}/groff.info*

%files base
%{!?_licensedir:%global license %%doc}
%license COPYING FDL LICENSES
%doc BUG-REPORT MORE.STUFF NEWS PROBLEMS
# configuration
%dir %{_sysconfdir}/groff/
%config(noreplace) %{_sysconfdir}/groff/*
# data
%dir %{_datadir}/%{name}/
%dir %{_datadir}/%{name}/%{version}/
%dir %{_datadir}/%{name}/%{version}/font/
%dir %{_datadir}/%{name}/%{version}/tmac/
%{_datadir}/%{name}/current
%{_datadir}/%{name}/%{version}/eign
%{_datadir}/%{name}/%{version}/font/devascii/
%{_datadir}/%{name}/%{version}/font/devlatin1/
%{_datadir}/%{name}/%{version}/font/devps/
%{_datadir}/%{name}/%{version}/font/devutf8/
%{_datadir}/%{name}/%{version}/font/devhtml/
%{_datadir}/%{name}/%{version}/tmac/an-ext.tmac
%{_datadir}/%{name}/%{version}/tmac/an-old.tmac
%{_datadir}/%{name}/%{version}/tmac/an.tmac
%{_datadir}/%{name}/%{version}/tmac/andoc.tmac
%{_datadir}/%{name}/%{version}/tmac/composite.tmac
%{_datadir}/%{name}/%{version}/tmac/cp1047.tmac
%{_datadir}/%{name}/%{version}/tmac/cs.tmac
%{_datadir}/%{name}/%{version}/tmac/de.tmac
%{_datadir}/%{name}/%{version}/tmac/den.tmac
%{_datadir}/%{name}/%{version}/tmac/devtag.tmac
%{_datadir}/%{name}/%{version}/tmac/doc-old.tmac
%{_datadir}/%{name}/%{version}/tmac/doc.tmac
%{_datadir}/%{name}/%{version}/tmac/eqnrc
%{_datadir}/%{name}/%{version}/tmac/europs.tmac
%{_datadir}/%{name}/%{version}/tmac/fallbacks.tmac
%{_datadir}/%{name}/%{version}/tmac/fr.tmac
%{_datadir}/%{name}/%{version}/tmac/html-end.tmac
%{_datadir}/%{name}/%{version}/tmac/html.tmac
%{_datadir}/%{name}/%{version}/tmac/hyphen.cs
%{_datadir}/%{name}/%{version}/tmac/hyphen.den
%{_datadir}/%{name}/%{version}/tmac/hyphen.det
%{_datadir}/%{name}/%{version}/tmac/hyphen.fr
%{_datadir}/%{name}/%{version}/tmac/hyphen.sv
%{_datadir}/%{name}/%{version}/tmac/hyphen.us
%{_datadir}/%{name}/%{version}/tmac/hyphenex.cs
%{_datadir}/%{name}/%{version}/tmac/hyphenex.det
%{_datadir}/%{name}/%{version}/tmac/hyphenex.us
%{_datadir}/%{name}/%{version}/tmac/ja.tmac
%{_datadir}/%{name}/%{version}/tmac/latin1.tmac
%{_datadir}/%{name}/%{version}/tmac/latin2.tmac
%{_datadir}/%{name}/%{version}/tmac/latin5.tmac
%{_datadir}/%{name}/%{version}/tmac/latin9.tmac
%{_datadir}/%{name}/%{version}/tmac/man.tmac
%{_datadir}/%{name}/%{version}/tmac/mandoc.tmac
%{_datadir}/%{name}/%{version}/tmac/mdoc.tmac
%{_datadir}/%{name}/%{version}/tmac/mdoc/
%{_datadir}/%{name}/%{version}/tmac/papersize.tmac
%{_datadir}/%{name}/%{version}/tmac/pic.tmac
%{_datadir}/%{name}/%{version}/tmac/ps.tmac
%{_datadir}/%{name}/%{version}/tmac/psatk.tmac
%{_datadir}/%{name}/%{version}/tmac/psold.tmac
%{_datadir}/%{name}/%{version}/tmac/pspic.tmac
%{_datadir}/%{name}/%{version}/tmac/safer.tmac
%{_datadir}/%{name}/%{version}/tmac/sv.tmac
%{_datadir}/%{name}/%{version}/tmac/trans.tmac
%{_datadir}/%{name}/%{version}/tmac/troffrc
%{_datadir}/%{name}/%{version}/tmac/troffrc-end
%{_datadir}/%{name}/%{version}/tmac/tty-char.tmac
%{_datadir}/%{name}/%{version}/tmac/tty.tmac
%{_datadir}/%{name}/%{version}/tmac/unicode.tmac
%{_datadir}/%{name}/%{version}/tmac/www.tmac
# programs
%{_bindir}/eqn.exe
%{_bindir}/groff.exe
%{_bindir}/grops.exe
%{_bindir}/grotty.exe
%{_bindir}/neqn
%{_bindir}/nroff
%{_bindir}/pic.exe
%{_bindir}/post-grohtml.exe
%{_bindir}/pre-grohtml.exe
%{_bindir}/preconv.exe
%{_bindir}/soelim.exe
%{_bindir}/tbl.exe
%{_bindir}/troff.exe
%{_mandir}/man1/eqn.*
%{_mandir}/man1/groff.*
%{_mandir}/man1/grops.*
%{_mandir}/man1/grotty.*
%{_mandir}/man1/neqn.*
%{_mandir}/man1/nroff.*
%{_mandir}/man1/pic.*
%{_mandir}/man1/preconv.*
%{_mandir}/man1/soelim.*
%{_mandir}/man1/tbl.*
%{_mandir}/man1/troff.*
# compatibility symlinks
%{_bindir}/gnroff
%{_bindir}/gtroff
%{_bindir}/gtbl
%{_bindir}/gpic
%{_bindir}/geqn
%{_bindir}/gneqn
%{_bindir}/gsoelim
%{_bindir}/zsoelim
%{_mandir}/man1/gnroff.*
%{_mandir}/man1/gtroff.*
%{_mandir}/man1/gtbl.*
%{_mandir}/man1/gpic.*
%{_mandir}/man1/geqn.*
%{_mandir}/man1/gneqn.*
%{_mandir}/man1/gsoelim.*
%{_mandir}/man1/zsoelim.*
%dir %{_libdir}/groff/

%files perl
# data
%{_datadir}/%{name}/%{version}/font/devpdf/
%{_datadir}/%{name}/%{version}/groffer/
%{_datadir}/%{name}/%{version}/tmac/pdf.tmac
# programs
%{_bindir}/afmtodit
%{_bindir}/chem
%{_bindir}/gperl
%{_bindir}/gpinyin
%{_bindir}/glilypond
%{_bindir}/groffer
%{_bindir}/grog
%{_bindir}/gropdf
%{_bindir}/mmroff
%{_bindir}/pdfmom
%{_bindir}/roff2dvi
%{_bindir}/roff2html
%{_bindir}/roff2pdf
%{_bindir}/roff2ps
%{_bindir}/roff2text
%{_bindir}/roff2x
%{_mandir}/man1/afmtodit.*
%{_mandir}/man1/chem.*
%{_mandir}/man1/gperl.*
%{_mandir}/man1/gpinyin.*
%{_mandir}/man1/glilypond.*
%{_mandir}/man1/groffer.*
%{_mandir}/man1/grog.*
%{_mandir}/man1/gropdf.*
%{_mandir}/man1/mmroff.*
%{_mandir}/man1/pdfmom.*
%{_mandir}/man1/roff2dvi.*
%{_mandir}/man1/roff2html.*
%{_mandir}/man1/roff2pdf.*
%{_mandir}/man1/roff2ps.*
%{_mandir}/man1/roff2text.*
%{_mandir}/man1/roff2x.*
%dir %{_libdir}/groff/glilypond/
%dir %{_libdir}/groff/gpinyin/
%dir %{_libdir}/groff/grog/
%{_libdir}/groff/glilypond/args.pl
%{_libdir}/groff/glilypond/oop_fh.pl
%{_libdir}/groff/glilypond/subs.pl
%{_libdir}/groff/gpinyin/subs.pl
%{_libdir}/groff/grog/subs.pl

%if %{with_x}
%files x11
# data
%{_datadir}/%{name}/%{version}/font/devX*/
%{_datadir}/%{name}/%{version}/tmac/X.tmac
%{_datadir}/%{name}/%{version}/tmac/Xps.tmac
%{_datadir}/X11/app-defaults/GXditview
%{_datadir}/X11/app-defaults/GXditview-color
# programs
%{_bindir}/gxditview
%{_bindir}/xtotroff
%{_mandir}/man1/gxditview.*
%{_mandir}/man1/xtotroff.*
%endif

%files doc
%doc %{_pkgdocdir}/*.me
%doc %{_pkgdocdir}/*.ps
%doc %{_pkgdocdir}/*.ms
%doc %{_pkgdocdir}/examples/
%doc %{_pkgdocdir}/html/
%doc %{_pkgdocdir}/pdf/

%changelog
* Fri Oct 26 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.22.3-1
- first os/2 rpm
