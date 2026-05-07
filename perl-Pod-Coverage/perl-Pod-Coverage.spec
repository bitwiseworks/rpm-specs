Name:           perl-Pod-Coverage
Version:        0.23
Release:        1%{?dist}
Summary:        Checks if the documentation of a module is comprehensive
License:        GPL+ or Artistic
Group:          Development/Libraries
Vendor:         bww bitwise works GmbH 
URL:            http://search.cpan.org/dist/Pod-Coverage/
Source0:        http://www.cpan.org/authors/id/R/RC/RCLAMP/Pod-Coverage-%{version}.tar.gz
# Make pod_cover more secure, CPAN RT#85540
#Patch0:         Pod-Coverage-0.23-Do-not-search-.-lib-by-pod_cover.patch
BuildArch:      noarch
#BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(B)
BuildRequires:  perl(base)
BuildRequires:  perl(constant)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Devel::Symdump) >= 2.01
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(lib)
BuildRequires:  perl(Pod::Find) >= 0.21
BuildRequires:  perl(Pod::Parser) >= 1.13
BuildRequires:  perl(strict)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
Requires:       perl(Devel::Symdump) >= 2.01
Requires:       perl(Pod::Find) >= 0.21
Requires:       perl(Pod::Parser) >= 1.13
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}
%global __requires_exclude %{?__requires_exclude:__requires_exclude|}^perl\\(Devel::Symdump\\)$
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Pod::Find\\)$
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Pod::Parser\\)$

%description
Developers hate writing documentation.  They'd hate it even more if their
computer tattled on them, but maybe they'll be even more thankful in the
long run.  Even if not, perlmodstyle tells you to, so you must obey.

This module provides a mechanism for determining if the pod for a given
module is comprehensive.

%prep
%setup -q -n Pod-Coverage-%{version}
#%patch0 -p1

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
%doc Changes examples
%{_bindir}/pod_cover
%{perl_vendorlib}/Pod/
#%{_mandir}/man3/Pod::Coverage.3pm*
#%{_mandir}/man3/Pod::Coverage::CountParents.3pm*
#%{_mandir}/man3/Pod::Coverage::ExportOnly.3pm*
#%{_mandir}/man3/Pod::Coverage::Overloader.3pm*
%{_mandir}/man3/*.3pm*

%changelog
* Wed Mar 07 2018 Elbert Pol <elbert.pol@gmail.com> - 0.23-1
-  initial rpm for OS2
