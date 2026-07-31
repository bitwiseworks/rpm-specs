%if !0%{?os2_version}
%bcond perl_Unicode_EastAsianWidth_enables_Module_Package %{undefined rhel}
%else
%bcond_with perl_Unicode_EastAsianWidth_enables_Module_Package
%endif

Name:		perl-Unicode-EastAsianWidth
Version:	12.0
Release:	1%{?dist}
Summary:	East Asian Width properties
License:	CC0-1.0
URL:		https://metacpan.org/release/Unicode-EastAsianWidth
Source0:	https://cpan.metacpan.org/authors/id/A/AU/AUDREYT/Unicode-EastAsianWidth-%{version}.tar.gz
%if 0%{?os2_version}
Vendor:         bww bitwise works GmbH
%endif
BuildArch:	noarch
BuildRequires:	coreutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(base)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:	perl(lib)
%if %{with perl_Unicode_EastAsianWidth_enables_Module_Package}
BuildRequires:	perl(Module::Package)
BuildRequires:	perl(Module::Package::Au)
%else
BuildRequires:	perl(inc::Module::Install)
%endif
BuildRequires:	perl(strict)
BuildRequires:	perl(Test)
BuildRequires:	perl(vars)
BuildRequires:	perl(warnings)

# Don't "provide" private Perl libs
%{?perl_default_filter}

%description
This module provide user-defined Unicode properties that deal with width
status of East Asian characters, as specified in
<http://www.unicode.org/unicode/reports/tr11/>.

%prep
%setup -q -n Unicode-EastAsianWidth-%{version}
rm -rf inc
perl -i -ne 'print $_ unless m{^inc/}' MANIFEST
%if %{without perl_Unicode_EastAsianWidth_enables_Module_Package}
perl -i -ne 'print m{Au:dry} ? "use inc::Module::Install;" : $_' Makefile.PL
cat >> Makefile.PL <<_EOF
name 'Unicode-EastAsianWidth';
all_from 'lib/Unicode/EastAsianWidth.pm';
WriteAll;
_EOF
%endif

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
find %{buildroot} -type f -name '*.bs' -empty -delete
%{_fixperms} %{buildroot}

%check
%if !0%{?os2_version}
make test
%endif

%files
%doc Changes README
%{perl_vendorlib}/Unicode/
%if !0%{?os2_version}
%{_mandir}/man3/Unicode::EastAsianWidth.3pm*
%else
%{_mandir}/man3/Unicode.EastAsianWidth.3pm*
%endif

%changelog
* Fri Jul 31 2026 Silvan Scherrer <silvan.scherrer@aroa.ch> - 12.0-1
- initial version
