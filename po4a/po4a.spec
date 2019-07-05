# as all doc are already gziped, we don't have to do it twice
%define __os_install_post %{nil}

Name: po4a
Version: 0.51
Release: 1%{?dist}
Summary: A tool maintaining translations anywhere
License: GPL+
URL: https://po4a.alioth.debian.org/

Vendor: bww bitwise works GmbH
%scm_source github https://github.com/bitwiseworks/%{name}-os2 %{version}-os2
#%scm_source git file://e:/Trees/po4a/git master-os2

BuildArch: noarch
BuildRequires: %{_bindir}/xsltproc.exe
BuildRequires: coreutils
BuildRequires: docbook-style-xsl
BuildRequires: findutils
BuildRequires: grep
# Requires a pod2man which supports --utf8
# Seemingly added in perl-5.10.1
BuildRequires: perl >= 4:5.10.1
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
#BuildRequires: %{_bindir}/nsgmls.exe
BuildRequires: gettext
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
#BuildRequires: perl(SGMLS) >= 1.03ii
BuildRequires: perl(strict)
BuildRequires: perl(subs)
BuildRequires: perl(Time::Local)
BuildRequires: perl(vars)
BuildRequires: perl(warnings)
# hope texlive-kpseas-bin missing deps was fixed
# epel7 doesn't have /usr/share/texlive/texmf-dist/web2c/texmf.cnf
#BuildRequires: texlive-kpathsea
#BuildRequires: texlive-kpathsea-bin

# Optional run-time:
BuildRequires: perl(I18N::Langinfo)
BuildRequires: perl(Locale::gettext) >= 1.01
#BuildRequires: perl(Term::ReadKey)
#BuildRequires: perl(Text::WrapI18N)
#BuildRequires: perl(Unicode::GCString)

# Required by the tests:
#BuildRequires: perl(Test::More)


#Requires: %{_bindir}/nsgmls.exe
Requires: %{_bindir}/xsltproc.exe
Requires: gettext
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
# hope texlive-kpseas-bin missing deps was fixed
# epel7 doesn't have /usr/share/texlive/texmf-dist/web2c/texmf.cnf
#Requires: texlive-kpathsea
#Requires: texlive-kpathsea-bin

# Optional, but package is quite useless without
# Until have perl-gettext on epel7 ppc64 (rhbz #1196539)
%if 0%{?rhel} != 7
Requires: perl(Locale::gettext) >= 1.01
%endif

%description
The po4a (po for anything) project goal is to ease translations (and
more interestingly, the maintenance of translations) using gettext
tools on areas where they were not expected like documentation.

%prep
%scm_setup

chmod +x scripts/*

# Fix bang path /usr/bin/env perl -> %{_bindir}/perl (RHBZ#987035).
%{__perl} -p -i.bak -e 's,#!\s*/usr/bin/env perl,#!/\@unixroot/usr/bin/perl,' \
  $(find . -type f -executable |
    xargs grep -l "/usr/bin/env perl")

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
#./Build test


%files -f %{name}.lang
%doc README* TODO
%license COPYING
%{_bindir}/po4a*
%{_bindir}/msguntypot
%{perl_vendorlib}/Locale
%{_mandir}/man1/po4a*.1*
%{_mandir}/man1/msguntypot.1*
%{_mandir}/man3/Locale.Po4a.*.3*
%{_mandir}/man5/po4a-build.conf*.5*
%{_mandir}/man7/po4a-runtime.7*
%{_mandir}/man7/po4a.7*
%{_mandir}/*/man1/po4a*.1*
%{_mandir}/*/man1/msguntypot.1*
%{_mandir}/*/man3/Locale.Po4a.*.3*
%{_mandir}/*/man5/po4a-build.conf.5*
%{_mandir}/*/man7/po4a.7*
%{_mandir}/*/man7/po4a-runtime.7*

%changelog
* Fri May 05 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.51-1
- initial version
