Name:           perl-Locale-Codes
Version:        3.88
Release:        2%{?dist}
Summary:        Distribution of modules to handle locale codes
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Locale-Codes
Source0:        https://cpan.metacpan.org/authors/id/S/SB/SBECK/Locale-Codes-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(:VERSION) >= 5.6
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(deprecate)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(if)
BuildRequires:  perl(utf8)
# Tests:
# Release tests are deleted
%if !0%{?os2_version}
BuildRequires:  perl(Test::Inter) >= 1.09
%endif
Requires:       perl(deprecate)

# Filter dependencies on private modules, they are not provided. Generator:
# for F in $(find lib -type f); do perl -e '$/ = undef; $_ = <>; if (/^package #\R([\w:]*);/m) { print qq{|^perl\\\\($1\\\\)} }' "$F"; done
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Locale::Codes::Country_Retired\\)|^perl\\(Locale::Codes::LangFam_Retired\\)|^perl\\(Locale::Codes::Script_Retired\\)|^perl\\(Locale::Codes::LangExt_Codes\\)|^perl\\(Locale::Codes::LangFam_Codes\\)|^perl\\(Locale::Codes::Script_Codes\\)|^perl\\(Locale::Codes::Language_Codes\\)|^perl\\(Locale::Codes::LangExt_Retired\\)|^perl\\(Locale::Codes::Currency_Codes\\)|^perl\\(Locale::Codes::LangVar_Retired\\)|^perl\\(Locale::Codes::Language_Retired\\)|^perl\\(Locale::Codes::Country_Codes\\)|^perl\\(Locale::Codes::LangVar_Codes\\)|^perl\\(Locale::Codes::Currency_Retired\\)
# Filter dependencies on test subscripts
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(do_tests\\.pl\\)
# Filter underspecified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Test::Inter\\)$

%description
Locale-Codes is a distribution containing a set of modules. The modules
each deal with different types of codes which identify parts of the locale
including languages, countries, currency, etc.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness
Requires:       perl(Test::Inter) >= 1.09

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Locale-Codes-%{version}
chmod -x examples/*
chmod +x t/*.pl
# Delete release tests
rm t/_*
perl -i.bkp -lne 'print $_ unless m{\At/_}' MANIFEST
# Delete unused files
rm t/runtests t/runtests.bat
perl -i.bkp -lne 'print $_ unless m{\At/runtests}' MANIFEST
%if 0%{?os2_version}
find t/ -type f -name '*.bkp' -delete
%endif

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} %{buildroot}/*
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/usr/bin/sh
cd %{_libexecdir}/%{name} && exec prove -j $(getconf _NPROCESSORS_ONLN)
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
%if !0%{?os2_version}
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
make test
%endif

%files
%license LICENSE
%doc Changes examples README README.first
%{perl_vendorlib}/*
%{_mandir}/man3/*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri May 08 2026 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.88-2
- rebuild with perl 5.42

* Mon Apr 27 2026 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.88-1
- initial version
