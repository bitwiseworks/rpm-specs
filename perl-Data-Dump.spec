Name:           perl-Data-Dump
Version:        1.23
Release:        1%{?dist}
Summary:        Pretty printing of data structures
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Data-Dump/
Vendor:         bww bitwise works GmbH
Source0:        http://search.cpan.org/CPAN/authors/id/G/GA/GAAS/Data-Dump-%{version}.tar.gz
BuildArch:      noarch
# Build
BuildRequires:  make
#BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
# Runtime
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(MIME::Base64)
BuildRequires:  perl(overload)
BuildRequires:  perl(strict)
BuildRequires:  perl(subs)
# XXX: BuildRequires:  perl(Term::ANSIColor)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
# Tests only
BuildRequires:  perl(IO::Socket::INET)
BuildRequires:  perl(Symbol)
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "$(perl -V:version)"; echo $version))
# Really optional
Suggests:       perl(MIME::Base64)

%description
This module provides a single function called dump() that takes a list of
values as its argument and produces a string as its result. The string
contains Perl code that, when evaled, produces a deep copy of the original
arguments. The string is formatted for easy reading.

%prep
%setup -q -n Data-Dump-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}
make manifypods

%install
make pure_install DESTDIR=%{buildroot}
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} %{buildroot}/*

%check
#make test

%files
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Fri Feb 23 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.23-1
- initial version
