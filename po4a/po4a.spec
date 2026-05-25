Name: po4a
Version: 0.74
Release: 1%{?dist}
Summary: A tool maintaining translations anywhere

# Note: source is imprecise about 2.0-only vs 2.0-or-later
# https://github.com/mquinson/po4a/issues/434
License: GPL-2.0-or-later
URL: https://po4a.org/

%if !0%{?os2_version}
Source0: https://github.com/mquinson/po4a/archive/v%{version}/%{name}-%{version}.tar.gz
%else
%scm_source github https://github.com/bitwiseworks/%{name}-os2 v%{version}-os2
Vendor: bww bitwise works GmbH
%endif

BuildArch: noarch
%if !0%{?os2_version}
BuildRequires: /usr/bin/xsltproc
%else
BuildRequires: %{_bindir}/xsltproc.exe
%endif
BuildRequires: coreutils
BuildRequires: docbook-style-xsl
BuildRequires: findutils
BuildRequires: grep
# Requires a pod2man which supports --utf8
# Seemingly added in perl-5.10.1
%if !0%{?os2_version}
BuildRequires: glibc-all-langpacks
%endif
BuildRequires: perl-interpreter >= 4:5.10.1
BuildRequires: perl-generators
BuildRequires: perl(lib)
BuildRequires: perl(Encode)
BuildRequires: perl(ExtUtils::Install)
BuildRequires: perl(File::Basename)
BuildRequires: perl(File::Copy)
BuildRequires: perl(File::Path)
BuildRequires: perl(File::Spec)
BuildRequires: perl(File::stat)
BuildRequires: perl(Module::Build)
BuildRequires: perl(Pod::Man)

# Run-time:
BuildRequires: gettext
%if !0%{?os2_version}
BuildRequires: opensp
%endif
BuildRequires: perl(Carp)
BuildRequires: perl(Config)
BuildRequires: perl(Cwd)
BuildRequires: perl(DynaLoader)
BuildRequires: perl(Encode::Guess)
BuildRequires: perl(Exporter)
BuildRequires: perl(Fcntl)
BuildRequires: perl(File::Temp)
BuildRequires: perl(Getopt::Long)
BuildRequires: perl(Getopt::Std)
BuildRequires: perl(IO::File)
BuildRequires: perl(Pod::Parser)
BuildRequires: perl(Pod::Usage)
BuildRequires: perl(POSIX)
%if !0%{?os2_version}
BuildRequires: perl(SGMLS) >= 1.03ii
%endif
BuildRequires: perl(strict)
BuildRequires: perl(subs)
BuildRequires: perl(Time::Local)
BuildRequires: perl(vars)
BuildRequires: perl(warnings)
# hope texlive-kpseas-bin missing deps was fixed
# epel7 doesn't have /usr/share/texlive/texmf-dist/web2c/texmf.cnf
%if !0%{?os2_version}
BuildRequires: texlive-kpathsea
BuildRequires: texlive-kpathsea-bin
BuildRequires: tex(article.cls)
%endif

BuildRequires: perl(I18N::Langinfo)
BuildRequires: perl(Locale::gettext) >= 1.01
%if !0%{?os2_version}
BuildRequires: perl(Term::ReadKey)
BuildRequires: perl(Text::WrapI18N)
BuildRequires: perl(Unicode::GCString)
%endif

# Required by the tests:
BuildRequires: perl(Syntax::Keyword::Try)
BuildRequires: perl(Test::More)
%if !0%{?os2_version}
BuildRequires: perl(Test::Pod)
%endif
BuildRequires: perl(YAML::Tiny)


%if !0%{?os2_version}
Requires: /usr/bin/xsltproc
%else
Requires: %{_bindir}/xsltproc.exe
%endif
Requires: gettext
%if !0%{?os2_version}
Requires: opensp
%endif
# hope texlive-kpseas-bin missing deps was fixed
# epel7 doesn't have /usr/share/texlive/texmf-dist/web2c/texmf.cnf
%if !0%{?os2_version}
Requires: texlive-kpathsea
Requires: texlive-kpathsea-bin
%endif

# Optional, but package is quite useless without
Requires: perl(Locale::gettext) >= 1.01
# Optional run-time:
Requires: perl(I18N::Langinfo)
%if !0%{?os2_version}
Requires: perl(Term::ReadKey)
Requires: perl(Text::WrapI18N)
Requires: perl(Unicode::GCString)
%endif

%description
The po4a (po for anything) project goal is to ease translations (and
more interestingly, the maintenance of translations) using gettext
tools on areas where they were not expected like documentation.

%prep
%if !0%{?os2_version}
%autosetup -p1
%else
%scm_setup
%endif
chmod +x scripts/*

%build
export PO4AFLAGS="-v -v -v"
%{__perl} ./Build.PL installdirs=vendor
./Build

%install
./Build install destdir=$RPM_BUILD_ROOT create_packlist=0
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'

%{_fixperms} $RPM_BUILD_ROOT/*
%find_lang %{name}

%check
%if !0%{?os2_version}
./Build test || :
%endif


%files -f %{name}.lang
%doc README* TODO
%license COPYING
%{_bindir}/po4a*
%{_bindir}/msguntypot
%{perl_vendorlib}/Locale
%{_mandir}/man1/po4a*.1*
%{_mandir}/man1/msguntypot.1*
%if !0%{?os2_version}
%{_mandir}/man3/Locale::Po4a::*.3*
%else
%{_mandir}/man3/Locale.Po4a.*.3*
%endif
#{_mandir}/man5/po4a-build.conf*.5*
#{_mandir}/man7/po4a-runtime.7*
%{_mandir}/man7/po4a.7*
%{_mandir}/*/man1/po4a*.1*
%{_mandir}/*/man1/msguntypot.1*
%if !0%{?os2_version}
%{_mandir}/*/man3/Locale::Po4a::*.3*
%else
%{_mandir}/*/man3/Locale.Po4a.*.3*
%endif
#{_mandir}/*/man5/po4a-build.conf.5*
#{_mandir}/*/man7/po4a-runtime.7*
%{_mandir}/*/man7/po4a.7*

%changelog
* Tue May 12 2026 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.74-1
- update to version 0.74
- resync with fedora spec

* Fri May 05 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.51-1
- initial version
