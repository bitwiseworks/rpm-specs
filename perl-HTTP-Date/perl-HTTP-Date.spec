Name:           perl-HTTP-Date
Version:        6.06
Release:        1%{?dist}
Summary:        Date conversion routines
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/HTTP-Date
Source0:        https://cpan.metacpan.org/authors/id/O/OA/OALDERS/HTTP-Date-%{version}.tar.gz
%if 0%{?os2_version}
Vendor:         bww bitwise works GmbH
%endif
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.6.2
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Time::Local) >= 1.28
# Time::Zone not used
# Tests:
BuildRequires:  perl(blib)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl(Test::More)
# Optional tests:
# CPAN::Meta not helpful
# CPAN::Meta::Prereqs not helpful
Requires:       perl(Time::Local) >= 1.28
# Strongly recommended:
Requires:       perl(Time::Zone)
Conflicts:      perl-libwww-perl < 6
Suggests:       perl(JSON::PP) >= 2.27300

# Remove under-specified version
%global __requires_exclude %{?__requires_exclude:%{__requires_exclude}|}^perl\\(Time::Local\\)$

%description
This module provides functions that deal the date formats used by the HTTP
protocol (and then some more). Only the first two functions, time2str() and
str2time(), are exported by default.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n HTTP-Date-%{version}
# Help generators to recognize Perl scripts
for F in $(find t/ -name '*.t'); do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!\s*perl}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
# Remove author tests
rm -f %{buildroot}%{_libexecdir}/%{name}/t/00-*
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/sh
cd %{_libexecdir}/%{name} && exec prove -I . -j "$(getconf _NPROCESSORS_ONLN)" -r
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test
%{_fixperms} %{buildroot}/*

%check
%if !0%{?os2_version}
unset AUTHOR_TESTING PERL_COMPILE_TEST_DEBUG
make test
%endif

%files
%license LICENSE
%doc Changes CONTRIBUTORS README.md
%{perl_vendorlib}/*
%{_mandir}/man3/*

%files tests
%{_libexecdir}/%{name}

%changelog
* Wed May 06 2026 Silvan Scherrer <silvan.scherrer@aroa.ch> - 6.06-1
- update to version 6.06
- resync with fedora spec

* Mon May 08 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> - 6.02-1
- initial version
