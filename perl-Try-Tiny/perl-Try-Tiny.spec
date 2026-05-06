%if ! (0%{?rhel} || 0%{?os2_version})
%{bcond_without perl_Try_Tiny_enables_optional_test}
%else
%{bcond_with perl_Try_Tiny_enables_optional_test}
%endif

Name:		perl-Try-Tiny
Summary:	Minimal try/catch with proper localization of $@
Version:	0.32
Release:	1%{?dist}
License:	MIT
URL:		https://metacpan.org/release/Try-Tiny
Source0:	https://cpan.metacpan.org/authors/id/E/ET/ETHER/Try-Tiny-%{version}.tar.gz
%if 0%{?os2_version}
Vendor:         bww bitwise works GmbH
%endif
BuildArch:	noarch
# Module Build
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker)
# Module
BuildRequires:	perl(Carp)
BuildRequires:	perl(constant)
BuildRequires:	perl(Exporter) >= 5.57
BuildRequires:	perl(strict)
BuildRequires:	perl(Sub::Util)
BuildRequires:	perl(warnings)
# Test Suite
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(Test::More) >= 0.96
# Optional Tests
%if %{with perl_Try_Tiny_enables_optional_test}
BuildRequires:	perl(Capture::Tiny) >= 0.12
BuildRequires:	perl(CPAN::Meta) >= 2.120900
BuildRequires:	perl(CPAN::Meta::Check) >= 0.011
BuildRequires:	perl(CPAN::Meta::Requirements)
%endif
# Dependencies
Requires:	perl(Sub::Util)

# Do not provide private modules from tests packaged as a documentation
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}^%{_docdir}/

%description
This module provides bare bones try/catch statements that are designed to
minimize common mistakes with eval blocks, and NOTHING else.

This is unlike TryCatch, which provides a nice syntax and avoids adding
another call stack layer, and supports calling return from the try block to
return from the parent subroutine. These extra features come at a cost of a
few dependencies, namely Devel::Declare and Scope::Upper that are occasionally
problematic, and the additional catch filtering uses Moose type constraints,
which may not be desirable either.

%prep
%setup -q -n Try-Tiny-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}
%if 0%{?os2_version}
make manifypods
%endif

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

%check
%if !0%{?os2_version}
make test
%endif

%files
%license LICENCE
%doc Changes CONTRIBUTING README t/
%{perl_vendorlib}/Try/
%if !0%{?os2_version}
%{_mandir}/man3/Try::Tiny.3*
%else
%{_mandir}/man3/Try.Tiny.3*
%endif

%changelog
* Wed May 06 2026 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.32-1
- update to version 0.32
- resync with fedora spec

* Fri Feb 23 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.30-1
- initial version
