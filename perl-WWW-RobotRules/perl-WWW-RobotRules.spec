Name:           perl-WWW-RobotRules
Version:        6.02
Release:        2%{?dist}
Summary:        Database of robots.txt-derived permissions
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/WWW-RobotRules
Source0:        https://cpan.metacpan.org/authors/id/G/GA/GAAS/WWW-RobotRules-%{version}.tar.gz
%if 0%{?os2_version}
Vendor:         bww bitwise works GmbH
%endif
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.8.1
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
# Run-time:
BuildRequires:  perl(AnyDBM_File)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(URI) >= 1.10
BuildRequires:  perl(vars)
# Tests:
# LWP::RobotUA not used
# URI::URL not used
Requires:       perl(URI) >= 1.10
Conflicts:      perl-libwww-perl < 6

# Remove underspecified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}perl\\(URI\\)$
# Do not provide private imlementation of abstract class methods
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}perl\\(WWW::RobotRules::InCore\\)

%description
This module parses /robots.txt files as specified in "A Standard for Robot
Exclusion", at <https://www.robotstxt.org/robotstxt.html>. Webmasters can
use the /robots.txt file to forbid conforming robots from accessing parts
of their web site.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       coreutils
Requires:       perl-Test-Harness

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n WWW-RobotRules-%{version}
# Help generators to recognize Perl scripts
for F in t/*.t; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!\s*perl}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} $RPM_BUILD_ROOT/*
# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
rm -fr %{buildroot}%{_libexecdir}/%{name}/t/misc
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/bash
set -e
# Test t/rules-dbm.t write into CWD
DIR=$(mktemp -d)
cp -a %{_libexecdir}/%{name}/* "$DIR"
pushd "$DIR"
prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
popd
rm -r "$DIR"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
%if !0%{?os2_version}
make test
%endif

%files
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%files tests
%{_libexecdir}/%{name}

%changelog
* Thu May 07 2026 Silvan Scherrer <silvan.scherrer@aroa.ch> - 6.02-2
- rebuild with latest perl
- resync with fedora spec

* Fri Feb 23 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> - 6.02-1
- initial version
