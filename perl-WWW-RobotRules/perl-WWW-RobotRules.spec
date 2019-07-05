Name:           perl-WWW-RobotRules
Version:        6.02
Release:        1%{?dist}
Summary:        Database of robots.txt-derived permissions
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/WWW-RobotRules/
Vendor:         bww bitwise works GmbH
Source0:        http://www.cpan.org/authors/id/G/GA/GAAS/WWW-RobotRules-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl-generators
BuildRequires:  perl(AnyDBM_File)
BuildRequires:  perl(Carp)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(URI) >= 1.10
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(URI) >= 1.10
Conflicts:      perl-libwww-perl < 6

# Remove underspecified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}perl\\(URI\\)$
# Do not provide private imlementation of abstract class methods
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}perl\\(WWW::RobotRules::InCore\\)

%description
This module parses /robots.txt files as specified in "A Standard for Robot
Exclusion", at <http://www.robotstxt.org/wc/norobots.html>. Webmasters can
use the /robots.txt file to forbid conforming robots from accessing parts
of their web site.

%prep
%setup -q -n WWW-RobotRules-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}
make manifypods

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;
%{_fixperms} $RPM_BUILD_ROOT/*

%check
#make test

%files
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Fri Feb 23 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> - 6.02-1
- initial version
