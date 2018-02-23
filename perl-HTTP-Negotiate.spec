Name:           perl-HTTP-Negotiate
Version:        6.01
Release:        1%{?dist}
Summary:        Choose a variant to serve
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/HTTP-Negotiate/
Vendor:         bww bitwise works GmbH
Source0:        http://www.cpan.org/authors/id/G/GA/GAAS/HTTP-Negotiate-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  make
#BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
#BuildRequires:  perl(:VERSION) >= 5.8.1
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(strict)
# Run-time:
BuildRequires:  perl(Exporter)
BuildRequires:  perl(HTTP::Headers) >= 6
# Tests only:
BuildRequires:  perl(HTTP::Request)
BuildRequires:  perl(Test)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
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

%prep
%setup -q -n HTTP-Negotiate-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}
make manifypods

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
%{_fixperms} %{buildroot}/*

%check
#make test

%files
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Fri Feb 23 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> - 6.01-1
- initial version
