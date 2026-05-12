%if ! (0%{?rhel}) && !0%{?os2_version}
# Run extra test
%bcond_without perl_Test_Fatal_enables_extra_test
# Run optional test
%bcond_without perl_Test_Fatal_enables_optional_test
%else
%bcond_with perl_Test_Fatal_enables_extra_test
%bcond_with perl_Test_Fatal_enables_optional_test
%endif

Summary:	Incredibly simple helpers for testing code with exceptions 
Name:		perl-Test-Fatal
Version:	0.018
Release:	1%{?dist}
License:	GPL-1.0-or-later OR Artistic-1.0-Perl
%if 0%{?os2_version}
Vendor:   bww bitwise works GmbH
%endif
URL:		https://metacpan.org/release/Test-Fatal
Source0:	https://cpan.metacpan.org/modules/by-module/Test/Test-Fatal-%{version}.tar.gz
BuildArch:	noarch
# Module Build
BuildRequires:	coreutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(:VERSION) >= 5.12
BuildRequires:	perl(ExtUtils::MakeMaker) >= 6.78
BuildRequires:	perl(strict)
# Module Runtime
BuildRequires:	perl(Carp)
BuildRequires:	perl(Exporter) >= 5.57
BuildRequires:	perl(Test::Builder)
BuildRequires:	perl(Try::Tiny) >= 0.07
BuildRequires:	perl(warnings)
# Test Suite
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(overload)
BuildRequires:	perl(Test::Builder::Tester)
BuildRequires:	perl(Test::More) >= 0.65
%if %{with perl_Test_Fatal_enables_optional_test}
# Optional Tests
BuildRequires:	perl(CPAN::Meta) >= 2.120900
%endif
%if %{with perl_Test_Fatal_enables_extra_test}
# Extra Tests
BuildRequires:	findutils
BuildRequires:	perl(Encode)
BuildRequires:	perl(Test::Pod) >= 1.41
%endif
# Dependencies
Requires:	perl(Test::Builder)

%description
Test::Fatal is an alternative to the popular Test::Exception. It does much
less, but should allow greater flexibility in testing exception-throwing code
with about the same amount of typing.

%prep
%setup -q -n Test-Fatal-%{version}

# Avoid doc-file dependencies
chmod -c -x examples/*

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} -c %{buildroot}

%check
%if !0%{?os2_version}
make test
%if %{with perl_Test_Fatal_enables_extra_test}
make test TEST_FILES="$(echo $(find xt/ -name '*.t'))"
%endif
%endif

%files
%license LICENSE
%doc Changes README examples/
%{perl_vendorlib}/Test/
%if !0%{?os2_version}
%{_mandir}/man3/Test::Fatal.3*
%else
%{_mandir}/man3/Test.Fatal.3*
%endif

%changelog
* Tue May 06 2026 Elbert Pol <elbert.pol@gmail.com> - 0.018
- Updated to latest version
- Sync with fedora spec

* Thu Mar 13 2018 Elbert Pol <elbert.pol@gmail.com> - 0.014-1
-  initial rpm for OS2

