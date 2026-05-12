Name:           perl-Pod-Coverage
Version:        0.23
Release:        2%{?dist}
Summary:        Checks if the documentation of a module is comprehensive
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
%if 0%{?os2_version}
Vendor:         bww bitwise works GmbH
%endif
URL:            https://metacpan.org/release/Pod-Coverage
Source0:        https://cpan.metacpan.org/authors/id/R/RC/RCLAMP/Pod-Coverage-%{version}.tar.gz
# Make pod_cover more secure, CPAN RT#85540
%if !0%{?os2_version}
Patch0:         Pod-Coverage-0.23-Do-not-search-.-lib-by-pod_cover.patch
%endif
BuildArch:      noarch
BuildRequires: make
BuildRequires:  perl-interpreter
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
%if !0%{?os2_version}
%patch -P0 -p1
%endif

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
%{_fixperms} %{buildroot}/*

%check
%if !0%{?os2_version}
make test
%endif

%files
%doc Changes examples
%{_bindir}/pod_cover
%{perl_vendorlib}/Pod/
%if !0%{?os2_version}
%{_mandir}/man3/Pod::Coverage.3pm*
%{_mandir}/man3/Pod::Coverage::CountParents.3pm*
%{_mandir}/man3/Pod::Coverage::ExportOnly.3pm*
%{_mandir}/man3/Pod::Coverage::Overloader.3pm*
%else
%{_mandir}/man3/*.3*
%endif

%changelog
* Thu May 07 2026 Elbert Pol <elbert.pol@gmail.com> -0.23-2
- Sync with Fedora spec
- Rebuild with latest perl

* Wed Mar 07 2018 Elbert Pol <elbert.pol@gmail.com> - 0.23-1
-  initial rpm for OS2
