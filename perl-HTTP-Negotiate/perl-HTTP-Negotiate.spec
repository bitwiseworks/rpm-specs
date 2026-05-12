Name:           perl-HTTP-Negotiate
Version:        6.01
Release:        2%{?dist}
Summary:        Choose a variant to serve
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/HTTP-Negotiate
Source0:        https://cpan.metacpan.org/authors/id/G/GA/GAAS/HTTP-Negotiate-%{version}.tar.gz
Patch0:         0001-Fix-warning-in-test.patch
%if 0%{?os2_version}
Vendor:         bww bitwise works GmbH
%endif
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(:VERSION) >= 5.8.1
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
# Run-time:
BuildRequires:  perl(Exporter)
BuildRequires:  perl(HTTP::Headers) >= 6
# Tests only:
BuildRequires:  perl(HTTP::Request)
BuildRequires:  perl(Test)
Requires:       perl(HTTP::Headers) >= 6
Conflicts:      perl-libwww-perl < 6

# Remove underspecified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}perl\\(HTTP::Headers\\)$

%description
This module provides a complete implementation of the HTTP content
negotiation algorithm specified in draft-ietf-http-v11-spec-00.ps chapter
12. Content negotiation allows for the selection of a preferred content
representation based upon attributes of the negotiable variants and the
value of the various Accept* header fields in the request.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n HTTP-Negotiate-%{version}
%patch -P0 -p1
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
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/sh
cd %{_libexecdir}/%{name} && exec prove -I . -j "$(getconf _NPROCESSORS_ONLN)" -r
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test
%{_fixperms} %{buildroot}/*

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
* Mon May 11 2026 Silvan Scherrer <silvan.scherrer@aroa.ch> - 6.01-2
- rebuild with perl 5.42
- resync with fedora spec

* Fri Feb 23 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> - 6.01-1
- initial version
