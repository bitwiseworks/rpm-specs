Name:           perl-Package-Constants
Epoch:          1
Version:        0.06
Release:        1%{?dist}
Summary:        List all constants declared in a package
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Package-Constants
Source0:        https://cpan.metacpan.org/authors/id/B/BI/BINGOS/Package-Constants-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  make
%if !0%{?os2_version}
BuildRequires:  perl-generators
BuildRequires:  perl(:VERSION) >= 5.6
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
%endif
BuildRequires:  perl(strict)
# Run-time:
BuildRequires:  perl(if)
BuildRequires:  perl(deprecate)
BuildRequires:  perl(warnings)
# Tests:
BuildRequires:  perl(constant)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(vars)
Requires:       perl(deprecate)

%description
Package::Constants lists all the constants defined in a certain package.
This can be useful for, among others, setting up an auto-generated
@EXPORT/@EXPORT_OK for a Constants.pm file.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Package-Constants-%{version}
# Help generators to recognize Perl scripts
for F in $(find t/ -name '*.t'); do
    perl -i.bkp -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!\s*perl}{$Config{startperl}}' "$F"
    chmod +x "$F"
done
%if 0%{?os2_version}
find t/ -type f -name '*.bkp' -delete
%endif

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
%if 0%{?os2_version}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete
%endif

%check
%if !0%{?os2_version}
make test
%endif

%files
%doc CHANGES README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%files tests
%{_libexecdir}/%{name}

%changelog
* Mon Apr 27 2026 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1:0.06-1
- initial version
