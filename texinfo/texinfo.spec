# Note: this .spec is borrowed from texinfo-5.2-8.fc22.src.rpm

%global tex_texinfo %{_datadir}/texmf/tex/texinfo

Summary: Tools needed to create Texinfo format documentation files
Name: texinfo
Version: 5.2
Release: 3%{?dist}
License: GPLv3+
Group: Applications/Publishing
Url: http://www.gnu.org/software/texinfo/
Vendor: bww bitwise works GmbH

%scm_source svn http://svn.netlabs.org/repos/ports/texinfo/trunk 1066

Source2: info-dir
Source5: macros.info

# TODO: Do we lack these perl bits on OS/2?
%define perl_i18n_support 0

Requires(post): %{_sbindir}/install-info.exe
Requires(preun): %{_sbindir}/install-info.exe
Requires: perl >= 5.7.3
Requires: perl(Data::Dumper)
%if %{?perl_i18n_support}
Requires: perl(Text::Unidecode), perl(Unicode::EastAsianWidth), perl(Locale::Messages)
%endif
BuildRequires: zlib-devel, ncurses-devel, help2man
BuildRequires: perl(Data::Dumper)
%if %{?perl_i18n_support}
BuildRequires: perl(Locale::Messages), perl(Unicode::EastAsianWidth), perl(Text::Unidecode)
%endif

# Two reasons for the following dependency:
# 1. texinfo.mo is installed by info rather by texinfo (since info needs it and for most users
#    texinfo itself isn't necessary), so texinfo must depend on it.
# 2. Packages that contain .info documentation often use BuildRequires: texinfo so that they
#    can build it. However, if they want to use info_requires/info_post()/info_preun() macros
#    they must have macros.info installed at rpm-build time which is provided by info.
Requires: info = %{version}-%{release}

# Texinfo perl packages are not installed in default perl library dirs
%global __provides_exclude ^perl\\(.*Texinfo.*\\)$
%global __requires_exclude ^perl\\(.*Texinfo.*\\)$
# Also no need to look into installed perl stuff at all (this filters out
# quile a lot of deps like perl(Locale::RecodeData::*) on OS/2)
%global __provides_exclude_from ^%{_datadir}/texinfo
%global __requires_exclude_from ^%{_datadir}/texinfo

%description
Texinfo is a documentation system that can produce both online
information and printed output from a single source file. The GNU
Project uses the Texinfo file format for most of its documentation.

Install texinfo if you want a documentation system for producing both
online and print documentation from the same source file and/or if you
are going to write documentation for the GNU Project.

%package -n info
Summary: A stand-alone TTY-based reader for GNU texinfo documentation
Group: System Environment/Base

%description -n info
The GNU project uses the texinfo file format for much of its
documentation. The info package provides a standalone TTY-based
browser program for viewing texinfo files.

%package tex
Summary: Tools for formatting Texinfo documentation files using TeX
Group: Applications/Publishing
Requires: texinfo = %{version}-%{release}
Requires: tex(tex) tex(epsf.tex)
Requires(post): %{_bindir}/texconfig-sys
Requires(postun): %{_bindir}/texconfig-sys

%description tex
Texinfo is a documentation system that can produce both online
information and printed output from a single source file. The GNU
Project uses the Texinfo file format for most of its documentation.

The texinfo-tex package provides tools to format Texinfo documents
for printing using TeX.

%prep
%scm_setup

# Create files necessary for configure
autogen.sh

# Change DEFAULT_INFOPATH to match prefix
sed -i -e "/define DEFAULT_INFOPATH/ s,/usr,%{_prefix},g" info/filesys.h

%build
%configure
%if %{?perl_i18n_support}
           --with-external-Text-Unidecode \
           --with-external-libintl-perl \
           --with-external-Unicode-EastAsianWidth
%endif
# This is necessary so that Perl module search path is properly set
# when running help2man on makeinfo etc.
export TEXINFO_DEV_SOURCE=1

make %{?_smp_mflags}

%install
mkdir -p ${RPM_BUILD_ROOT}%{_sbindir}

make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'

mkdir -p $RPM_BUILD_ROOT%{tex_texinfo}
install -p -m644 doc/texinfo.tex doc/txi-??.tex $RPM_BUILD_ROOT%{tex_texinfo}

install -p -m644 %{SOURCE2} $RPM_BUILD_ROOT%{_infodir}/dir
mv $RPM_BUILD_ROOT%{_bindir}/install-info.exe $RPM_BUILD_ROOT%{_sbindir}

mkdir -p $RPM_BUILD_ROOT%{_rpmconfigdir}/macros.d
cp %{SOURCE5} $RPM_BUILD_ROOT%{_rpmconfigdir}/macros.d

%find_lang %{name}
%find_lang %{name}_document

# TODO: Disabled for now
#%check
#export ALL_TESTS=yes
#make %{?_smp_mflags} check

%post
if [ -f %{_infodir}/texinfo.gz ]; then # --excludedocs?
    %{_sbindir}/install-info.exe %{_infodir}/texinfo.gz %{_infodir}/dir || :
elif [ -f %{_infodir}/texinfo.info ]; then # --excludedocs?
    %{_sbindir}/install-info.exe %{_infodir}/texinfo.info %{_infodir}/dir || :
fi

%preun
if [ $1 = 0 ]; then
    if [ -f %{_infodir}/texinfo.gz ]; then # --excludedocs?
        %{_sbindir}/install-info.exe --delete %{_infodir}/texinfo.gz %{_infodir}/dir || :
    elif [ -f %{_infodir}/texinfo.info ]; then # --excludedocs?
        %{_sbindir}/install-info.exe --delete %{_infodir}/texinfo.info %{_infodir}/dir || :
    fi
fi

%post -n info
if [ -f %{_infodir}/info-stnd.info ]; then # --excludedocs?
    %{_sbindir}/install-info.exe %{_infodir}/info-stnd.info %{_infodir}/dir
fi
if [ -x %{_bindir}/sed ]; then
    %{_bindir}/sed -i '/^This is.*produced by makeinfo.*from/d' %{_infodir}/dir || :
fi

%preun -n info
if [ $1 = 0 ]; then
    if [ -f %{_infodir}/info-stnd.info ]; then # --excludedocs?
        %{_sbindir}/install-info.exe --delete %{_infodir}/info-stnd.info %{_infodir}/dir \
        || :
    fi
fi

%post tex
%{_bindir}/texconfig-sys rehash 2> /dev/null || :

%postun tex
%{_bindir}/texconfig-sys rehash 2> /dev/null || :


%files -f %{name}_document.lang
%doc AUTHORS ChangeLog NEWS README TODO
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_bindir}/makeinfo
%{_bindir}/texi2any
%{_bindir}/pod2texi
%{_datadir}/texinfo
%{_infodir}/texinfo*
%{_mandir}/man1/makeinfo.1*
%{_mandir}/man5/texinfo.5*
%{_mandir}/man1/texi2any.1*
%{_mandir}/man1/pod2texi.1*

%files -n info -f %{name}.lang
%config(noreplace) %verify(not md5 size mtime) %{_infodir}/dir
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_bindir}/info.exe
%{_bindir}/infokey.exe
%{_infodir}/info.info*
%{_infodir}/info-stnd.info*
%{_sbindir}/install-info.exe
%{_mandir}/man1/info.1*
%{_mandir}/man1/infokey.1*
%{_mandir}/man1/install-info.1*
%{_mandir}/man5/info.5*
%{_rpmconfigdir}/macros.d/macros.info

%files tex
%{_bindir}/texindex.exe
%{_bindir}/texi2dvi
%{_bindir}/texi2pdf
%{_bindir}/pdftexi2dvi
%{tex_texinfo}/
%{_mandir}/man1/texindex.1*
%{_mandir}/man1/texi2dvi.1*
%{_mandir}/man1/texi2pdf.1*
%{_mandir}/man1/pdftexi2dvi.1*

%changelog
* Fri May 12 2017 Dmitriy Kuminov <coding@dmik.org> 5.2-3
- Use scm_source and friends.
- Fix broken info_preun macro (bashism).

* Tue Feb 17 2015 Dmitriy Kuminov <coding@dmik.org> 5.2-2
- Make @unixroot strings properly quoted in perl scripts.

* Fri Feb 13 2015 Dmitriy Kuminov <coding@dmik.org> 5.2-1
- Initial package for version 5.2.
