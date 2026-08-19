%global tex_texinfo %{_datadir}/texlive/texmf-dist/tex/texinfo

Summary: Tools needed to create Texinfo format documentation files
Name: texinfo
Version: 7.3
Release: 1%{?dist}
License: GPL-3.0-or-later
Url: http://www.gnu.org/software/texinfo/
%if !0%{?os2_version}
Source0: ftp://ftp.gnu.org/gnu/texinfo/texinfo-%{version}.tar.xz
Source1: ftp://ftp.gnu.org/gnu/texinfo/texinfo-%{version}.tar.xz.sig
%else
Vendor: bww bitwise works GmbH
%scm_source github https://github.com/bitwiseworks/%{name}-os2 %{version}-os2
%endif
Source2: fix-info-dir
# Patch0: we need to fix template fix-info-dir generates
Patch0: info-6.5-sync-fix-info-dir.patch
%if !0%{?os2_version}
# Patch1: rhbz#1592433, bug in fix-info-dir --delete
Patch1: texinfo-6.5-fix-info-dir.patch
# Patch3: fixes issues detected by static analysis
Patch3: texinfo-7.1-various-sast-fixes.patch
# Patch4: fixes issues detected by static analysis
Patch4: texinfo-7.1-make-tainted-data-safe.patch
# Patch5: add support for zstd compression
Patch5: texinfo-6.7-zstd-compression.patch
# Patch6: include limits header
Patch6: texinfo-7.3-limits.patch
%endif

BuildRequires: make
BuildRequires: gcc
BuildRequires: perl-generators
BuildRequires: ncurses-devel, help2man, perl(Data::Dumper)
%if !0%{?os2_version}
BuildRequires: perl(Locale::Messages), perl(Unicode::EastAsianWidth), perl(Text::Unidecode)
%else
BuildRequires: perl(Unicode::EastAsianWidth), perl(Text::Unidecode)
%endif
BuildRequires: perl(Storable), perl(Unicode::Normalize)

# Texinfo perl packages are not installed in default perl library dirs
%global __provides_exclude ^perl\\(.*Texinfo.*\\)$
%global __requires_exclude ^perl\\(.*Texinfo.*\\)$

%description
Texinfo is a documentation system that can produce both online
information and printed output from a single source file. The GNU
Project uses the Texinfo file format for most of its documentation.

Install texinfo if you want a documentation system for producing both
online and print documentation from the same source file and/or if you
are going to write documentation for the GNU Project.

%package -n info
Summary: A stand-alone TTY-based reader for GNU texinfo documentation
%if !0%{?os2_version}
Provides: /sbin/install-info
%else
Provides: /@unixroot/usr/sbin/install-info.exe
%endif

%description -n info
The GNU project uses the texinfo file format for much of its
documentation. The info package provides a standalone TTY-based
browser program for viewing texinfo files.

%package tex
Summary: Tools for formatting Texinfo documentation files using TeX
Requires: texinfo = %{version}-%{release}
Requires: tex(tex) tex(epsf.tex)
%if !0%{?os2_version}
Requires: /usr/bin/cmp
Requires: /usr/bin/diff
%else
Requires: /@unixroot/usr/bin/cmp.exe
Requires: /@unixroot/usr/bin/diff.exe
%endif
Requires(post): %{_bindir}/texconfig-sys
Requires(postun): %{_bindir}/texconfig-sys
Provides: tex-texinfo
Provides: texlive-texinfo
Obsoletes: texlive-texinfo <= 9:2019-15

%description tex
Texinfo is a documentation system that can produce both online
information and printed output from a single source file. The GNU
Project uses the Texinfo file format for most of its documentation.

The texinfo-tex package provides tools to format Texinfo documents
for printing using TeX.

%prep
%if !0%{?os2_version}
%setup -q
%else
%scm_setup
%endif
mkdir contrib
install -Dpm0755 -t contrib %{SOURCE2}
%if !0%{?os2_version}
%autopatch -p1
%else
autoreconf -fvi
%patch -P0 -p1
%endif

%build
%configure --with-external-Text-Unidecode \
           --with-external-libintl-perl \
           --with-external-Unicode-EastAsianWidth \
           --disable-perl-xs
%make_build

%install
%make_install

mkdir -p %{buildroot}%{tex_texinfo}
install -p -m644 doc/texinfo.tex doc/txi-??.tex %{buildroot}%{tex_texinfo}

install -Dpm0755 -t %{buildroot}%{_sbindir} contrib/fix-info-dir
%if 0%{?os2_version}
mv %{buildroot}%{_bindir}/install-info.exe %{buildroot}%{_sbindir}
%endif

%find_lang %{name}
%find_lang %{name}_document

%check
#export ALL_TESTS=yes
#%make_build check

%post tex
%{_bindir}/texconfig-sys rehash 2> /dev/null || :

%postun tex
%{_bindir}/texconfig-sys rehash 2> /dev/null || :

%transfiletriggerin -n info -- %{_infodir}
[ -f %{_infodir}/dir ] && create_arg="" || create_arg="--create"
%{_sbindir}/fix-info-dir $create_arg %{_infodir}/dir &>/dev/null || :

%transfiletriggerpostun -n info -- %{_infodir}
[ -f %{_infodir}/dir ] && %{_sbindir}/fix-info-dir --delete %{_infodir}/dir &>/dev/null || :

%files -f %{name}.lang -f %{name}_document.lang
%doc AUTHORS ChangeLog NEWS README TODO
%license COPYING
%{_bindir}/makeinfo
%{_bindir}/texi2any
%{_bindir}/pod2texi
%{_datadir}/texinfo
%{_datadir}/texi2any
%{_infodir}/texinfo*
%{_infodir}/texi2any_api.info*
%{_infodir}/texi2any_internals.info*
%{_mandir}/man1/makeinfo.1*
%{_mandir}/man5/texinfo.5*
%{_mandir}/man1/texi2any.1*
%{_mandir}/man1/pod2texi.1*

%files -n info
%license COPYING
%if !0%{?os2_version}
%{_bindir}/info
%else
%{_bindir}/info.exe
%endif
%{_infodir}/info-stnd.info*
%if !0%{?os2_version}
%{_sbindir}/install-info
%else
%{_sbindir}/install-info.exe
%endif
%{_sbindir}/fix-info-dir
%{_mandir}/man1/info.1*
%{_mandir}/man1/install-info.1*
%{_mandir}/man5/info.5*
%ghost %{_infodir}/dir
%ghost %attr(644, root, root) %{_infodir}/dir.old

%files tex
%{_bindir}/texindex
%{_bindir}/texi2dvi
%{_bindir}/texi2pdf
%{_bindir}/pdftexi2dvi
%{tex_texinfo}/
%{_mandir}/man1/texindex.1*
%{_mandir}/man1/texi2dvi.1*
%{_mandir}/man1/texi2pdf.1*
%{_mandir}/man1/pdftexi2dvi.1*

%changelog
- macros.info: Use _sys_sbindir instead of _sbindir when defined

* Fri Jul 31 2026 Silvan Scherrer <silvan.scherrer@aroa.ch> 7.3-1
- update to version 7.3
- resync wit fedora spec

* Fri May 12 2017 Dmitriy Kuminov <coding@dmik.org> 5.2-3
- Use scm_source and friends.
- Fix broken info_preun macro (bashism).

* Tue Feb 17 2015 Dmitriy Kuminov <coding@dmik.org> 5.2-2
- Make @unixroot strings properly quoted in perl scripts.

* Fri Feb 13 2015 Dmitriy Kuminov <coding@dmik.org> 5.2-1
- Initial package for version 5.2.
