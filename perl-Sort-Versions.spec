Name:           perl-Sort-Versions
Version:        1.62
Release:        1%{?dist}
Summary:        Perl module for sorting of revision-like numbers
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Sort-Versions/
Vendor:         bww bitwise works GmbH
Source0:        http://www.cpan.org/modules/by-module/Sort/Sort-Versions-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
A perl 5 module for sorting of revision-like numbers

Sort::Versions allows easy sorting of mixed non-numeric and numeric strings,
like the 'version numbers' that many shared library systems and revision
control packages use. This is quite useful if you are trying to deal with
shared libraries. It can also be applied to applications that intersperse
variable-width numeric fields within text. Other applications can
undoubtedly be found.

%prep
%setup -q -n Sort-Versions-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}
make manifypods

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} $RPM_BUILD_ROOT/*

%check
#make test

%files
%doc Changes
%license LICENSE
%{perl_vendorlib}/Sort
%{_mandir}/man3/*

%changelog
* Wed Mar 07 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.62-1
- initial version
