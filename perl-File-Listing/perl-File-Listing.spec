Name:           perl-File-Listing
Version:        6.04
Release:        1%{?dist}
Summary:        Parse directory listing
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/File-Listing/
Vendor:         bww bitwise works GmbH
Source0:        http://www.cpan.org/authors/id/G/GA/GAAS/File-Listing-%{version}.tar.gz
BuildArch:      noarch
#BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(HTTP::Date) >= 6
BuildRequires:  perl(strict)
BuildRequires:  perl(Time::Local)
BuildRequires:  perl(vars)
# Tests:
# Do not BuildRequire optinal perl(LWP::Simple) to break dependency circle.
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "$(perl -V:version)"; echo $version))
Requires:       perl(HTTP::Date) >= 6
Requires:       perl(Time::Local)
Conflicts:      perl-libwww-perl < 6

# RPM 4.9 style
# Remove underspecified dependencies
%global __requires_exclude %{?__requires_exclude:__requires_exclude|}^perl\\(HTTP::Date\\)\s*$
# Do not provide private modules
%global __provides_exclude %{?__provides_exclude:__provides_exclude|}^perl\\(File::Listing::

%description
This module exports a single function called parse_dir(), which can be used
to parse directory listings.

%prep
%setup -q -n File-Listing-%{version}

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
* Fri Mar 02 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> 6.04-1
- initial rpm
