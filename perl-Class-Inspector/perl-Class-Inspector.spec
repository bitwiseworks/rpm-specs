Name:		perl-Class-Inspector
Version:	1.36
Release:	2%{?dist}
Summary:	Get information about a class and its structure
License:	GPL-1.0-or-later OR Artistic-1.0-Perl
URL:		https://metacpan.org/release/Class-Inspector
Source0:	https://cpan.metacpan.org/authors/id/P/PL/PLICEASE/Class-Inspector-%{version}.tar.gz
%if 0%{?os2_version}
Vendor:         bww bitwise works GmbH
%endif

BuildArch: noarch

BuildRequires:	%{__make}
BuildRequires:	perl-generators
BuildRequires:	perl(Exporter)
BuildRequires:	perl(Test::More)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(File::Spec) >= 0.80
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)

%description
Class::Inspector allows you to get information about a loaded class.
Most or all of this information can be found in other ways, but they aren't
always very friendly, and usually involve a relatively high level of Perl
wizardry, or strange and unusual looking code. Class::Inspector attempts to
provide an easier, more friendly interface to this information.

%prep
%setup -q -n Class-Inspector-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}
%if 0%{?os2_version}
make manifypods
%endif

%install
%{make_install}
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
%{_fixperms} $RPM_BUILD_ROOT/*

%check
%if !0%{?os2_version}
%{__make} test
%endif

%files
%doc Changes README
%license LICENSE
%{perl_vendorlib}/Class
%{_mandir}/man3/*

%changelog
* Fri May 08 2026 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.36-1
- initial rpm
