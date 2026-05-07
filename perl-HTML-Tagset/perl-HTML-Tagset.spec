%if ! (0%{?rhel} || 0%{?os2_version})
%{bcond_without perl_HTML_Tagset_enables_optional_test}
%else
%{bcond_with perl_HTML_Tagset_enables_optional_test}
%endif

Name:           perl-HTML-Tagset
Version:        3.24
Release:        1%{?dist}
Summary:        HTML::Tagset - data tables useful in parsing HTML
License:        Artistic-2.0
URL:            https://metacpan.org/release/HTML-Tagset
Source0:        https://cpan.metacpan.org/authors/id/P/PE/PETDANCE/HTML-Tagset-%{version}.tar.gz
%if 0%{?os2_version}
Vendor:         bww bitwise works GmbH
%endif
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.10
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
# Run-time
# Tests
BuildRequires:  perl(Test::More)
BuildRequires:  perl(warnings)
# Optional tests
# Test::Pod -> Pod::Simple -> HTML::Entities (HTML::Parser) -> HTML::Tagset
%if 0%{!?perl_bootstrap:1}
%if %{with perl_HTML_Tagset_enables_optional_test}
BuildRequires:  perl(Test::Pod) >= 1.14
%endif
%endif

%description
This module contains several data tables useful in various kinds of
HTML parsing operations, such as tag and entity names.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n HTML-Tagset-%{version}

# Help generators to recognize Perl scripts
for F in t/*.t; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*perl\b}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}
%if 0%{?os2_version}
make manifypods
%endif

%install
%{make_install}
%{_fixperms} %{buildroot}

# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
rm %{buildroot}%{_libexecdir}/%{name}/t/pod.t
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/sh
cd %{_libexecdir}/%{name} && exec prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
%if !0%{?os2_version}
make test
%endif

%files
%doc Changes README.md
%{perl_vendorlib}/HTML/
%if !0%{?os2_version}
%{_mandir}/man3/HTML::Tagset.3pm*
%else
%{_mandir}/man3/HTML.Tagset.3pm*
%endif

%files tests
%{_libexecdir}/%{name}

%changelog
* Thu May 07 2026 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.24-1
- update to version 3.24
- resync with fedora spec

* Mon May 08 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.20-1
- initial version
