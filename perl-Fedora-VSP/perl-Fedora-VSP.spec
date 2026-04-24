%if 0%{?os2_version}
%define perl_bootstrap 1
%endif

Name:           perl-Fedora-VSP
Version:        0.001
Release:        1%{?dist}
Summary:        Perl version normalization for RPM
License:        GPL-3.0-or-later
URL:            https://ppisar.fedorapeople.org/Fedora-VSP/
Source0:        %{url}Fedora-VSP-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
%if !0%{?os2_version}
BuildRequires:  perl-interpreter
%endif
%if %{defined perl_bootstrap}
BuildRequires:  perl-macros
%else
# Break build cycle: perl-Fedora-VSP → perl-generators → perl-Fedora-VSP
BuildRequires:  perl-generators
%endif
BuildRequires:  perl(ExtUtils::MakeMaker)
# Run-time:
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Tests:
BuildRequires:  perl(Test::More)
BuildRequires:  perl(version)
%if %{defined perl_bootstrap}
# Break build cycle: perl-Fedora-VSP → perl-generators → perl-Fedora-VSP
Requires:       perl(strict)
Requires:       perl(warnings)
Provides:       perl(Fedora::VSP) = %{version}
%endif

%description
This module provides functions for normalizing Perl version strings for
Red Hat Package (RPM) based Linux distributions.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Fedora-VSP-%{version}
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
%if 0%{?os2_version}
make manifypods
%endif

%install
%{make_install}
%if 0%{?os2_version}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete
%endif
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
%license COPYING
%{perl_vendorlib}/*
%{_mandir}/man3/*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Apr 24 2026 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.001-1
- First package
