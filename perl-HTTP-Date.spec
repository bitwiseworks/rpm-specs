Name:           perl-HTTP-Date
Version:        6.02
Release:        1%{?dist}
Summary:        Date conversion routines
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/HTTP-Date/
Vendor:         bww bitwise works GmbH
Source0:        http://www.cpan.org/authors/id/G/GA/GAAS/HTTP-Date-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(strict)
# Run-time
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Time::Local)
# perl(Time::Zone) not used
BuildRequires:  perl(vars)
# Tests only:
BuildRequires:  perl(Test)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
# Strongly recommended:
Requires:       perl(Time::Zone)
Conflicts:      perl-libwww-perl < 6

%description
This module provides functions that deal the date formats used by the HTTP
protocol (and then some more). Only the first two functions, time2str() and
str2time(), are exported by default.

%prep
%setup -q -n HTTP-Date-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
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
* Mon May 08 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> - 6.02-1
- initial version
