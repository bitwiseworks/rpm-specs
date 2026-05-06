# Run extra test
#%bcond_without perl_Test_Fatal_enables_extra_test
# Run optional test
#%bcond_without perl_Test_Fatal_enables_optional_test

Summary:	Incredibly simple helpers for testing code with exceptions 
Name:		perl-Test-Fatal
Version:	0.014
Release:	1%{?dist}
License:	GPL+ or Artistic
Group:		Development/Libraries
Vendor:         bww bitwise works GmbH
Url:		http://search.cpan.org/dist/Test-Fatal/
Source0:	http://search.cpan.org/CPAN/authors/id/R/RJ/RJBS/Test-Fatal-%{version}.tar.gz
BuildArch:	noarch
# Module Build
#BuildRequires:	perl-interpreter
BuildRequires:	perl-generators
BuildRequires:	perl(ExtUtils::MakeMaker)
# Module Runtime
BuildRequires:	perl(Carp)
BuildRequires:	perl(Exporter) >= 5.57
BuildRequires:	perl(strict)
BuildRequires:	perl(Test::Builder)
BuildRequires:	perl(Try::Tiny) >= 0.07
BuildRequires:	perl(warnings)
# Test Suite
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(overload)
BuildRequires:	perl(Test::Builder::Tester)
BuildRequires:	perl(Test::More) >= 0.96
#%if %{with perl_Test_Fatal_enables_optional_test}
# Optional Tests
#BuildRequires:	perl(CPAN::Meta) >= 2.120900
#%endif
#%if %{with perl_Test_Fatal_enables_extra_test}
# Extra Tests
#BuildRequires:	perl(Test::Pod) >= 1.41
#%endif
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
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
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}
make manifypods

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} %{buildroot}

%check
#make test
#%if %{with perl_Test_Fatal_enables_extra_test}
#make test TEST_FILES="$(echo $(find xt/ -name '*.t'))"
#%endif

%files
%license LICENSE
%doc Changes README examples/
%{perl_vendorlib}/Test/
%{_mandir}/man3/*.3*

%changelog
* Thu Mar 13 2018 Elbert Pol <elbert.pol@gmail.com> - 0.014-1
-  initial rpm for OS2

