Name:           perl-Encode-Locale
Version:        1.05
Release:        1%{?dist}
Summary:        Determine the locale encoding
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Encode-Locale/
Vendor:         bww bitwise works GmbH
Source0:        http://www.cpan.org/authors/id/G/GA/GAAS/Encode-Locale-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
# Run-time:
BuildRequires:  perl(base)
BuildRequires:  perl(Encode) >= 2
BuildRequires:  perl(Encode::Alias)
# Encode::HanExtra not used at tests, not yet packaged
BuildRequires:  perl(Exporter)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Win32 not used on Linux
# Win32::API not used on Linux
# Win32::Console not used on Linux
# Recommended:
BuildRequires:  perl(I18N::Langinfo)
# Tests only:
#BuildRequires:  perl(Test::More)
BuildRequires:  perl(utf8)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Encode) >= 2
# Encode::HanExtra not yet packaged
# Recommended:
Requires:       perl(I18N::Langinfo)
Requires:       perl(warnings)

%{?perl_default_filter}
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Encode\\)$

%description
In many applications it's wise to let Perl use Unicode for the strings
it processes.  Most of the interfaces Perl has to the outside world is
still byte based.  Programs therefore needs to decode byte strings
that enter the program from the outside and encode them again on the
way out.

%prep
%setup -q -n Encode-Locale-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}
make manifypods

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
%{_fixperms} $RPM_BUILD_ROOT/*

%check
#make test

%files
%doc Changes README
%{perl_vendorlib}/Encode/
%{_mandir}/man3/Encode.Locale.3*

%changelog
* Mon May 08 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.05-1
- initial version
