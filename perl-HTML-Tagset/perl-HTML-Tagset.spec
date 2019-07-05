%define perl_bootstrap 0

Name:           perl-HTML-Tagset
Version:        3.20
Release:        1%{?dist}
Summary:        HTML::Tagset - data tables useful in parsing HTML
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/HTML-Tagset/
Vendor:         bww bitwise works GmbH
Source0:        http://search.cpan.org/CPAN/authors/id/P/PE/PETDANCE/HTML-Tagset-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
#BuildRequires:  perl(Test)
#BuildRequires:  perl(Test::More)
# Test::Pod -> Pod::Simple -> HTML::Entities (HTML::Parser) -> HTML::Tagset
%if 0%{!?perl_bootstrap:1}
BuildRequires:  perl(Test::Pod)
%endif
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
This module contains several data tables useful in various kinds of
HTML parsing operations, such as tag and entity names.

%prep
%setup -q -n HTML-Tagset-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}
make manifypods

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} ';' 2>/dev/null
%{_fixperms} %{buildroot}

%check
#make test

%files
%doc Changes README
%{perl_vendorlib}/HTML/
%{_mandir}/man3/HTML.Tagset.3pm*

%changelog
* Mon May 08 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.20-1
- initial version
