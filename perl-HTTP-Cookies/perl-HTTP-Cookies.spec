Name:           perl-HTTP-Cookies
Version:        6.04
Release:        1%{?dist}
Summary:        HTTP cookie jars
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/HTTP-Cookies/
Vendor:         bww bitwise works GmbH
Source0:        http://www.cpan.org/authors/id/O/OA/OALDERS/HTTP-Cookies-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl-generators
#BuildRequires:  perl-interpreter
#BuildRequires:  perl(:VERSION) >= 5.8.1
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(HTTP::Date) >= 6
BuildRequires:  perl(HTTP::Headers::Util) >= 6
BuildRequires:  perl(HTTP::Request)
BuildRequires:  perl(locale)
# Time::Local needed on MacOS only
BuildRequires:  perl(vars)
# Win32 not supported
# Tests:
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(HTTP::Response)
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(URI)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Carp)
Requires:       perl(HTTP::Date) >= 6
Requires:       perl(HTTP::Headers::Util) >= 6
Conflicts:      perl-libwww-perl < 6

# Remove underspecified dependencies.
# One function of provided HTTP::Cookies::Microsoft works on Win32 only, other
# function do not need it. We keep the module, but remove the dependency.
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}perl\\((HTTP::Date|HTTP::Headers::Util|Win32)\\)$

%description
This class is for objects that represent a "cookie jar" -- that is, a
database of all the HTTP cookies that a given LWP::UserAgent object
knows about.

%prep
%setup -q -n HTTP-Cookies-%{version}

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
%license LICENSE
%doc Changes CONTRIBUTORS README.md
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Fri Feb 23 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> - 6.04-1
- initial version
