# This package should be renamed into perl-Locale-gettext
%global tarname Locale-gettext

Name:           perl-gettext
Version:        1.07
Release:        2%{?dist}
Summary:        Interface to gettext family of functions

License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/gettext
Source0:        https://cpan.metacpan.org/authors/id/P/PV/PVANDRY/%{tarname}-%{version}.tar.gz
%if 0%{?os2_version}
Vendor:         bww bitwise works GmbH
%endif

BuildRequires:  gcc
BuildRequires:  %{__make}
BuildRequires:  %{__perl}

BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  gettext
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(POSIX)

# Optional
BuildRequires:  perl(Encode)
# Tests:
BuildRequires:  perl(Test)

# Need to allow LANG=en_US.UTF-8
# Testsuite fails w/ LANG=C.UTF-8 on fedora >= 40
%if !0%{?os2_version}
BuildRequires:  glibc-langpack-en
%endif

%description
The gettext module permits access from perl to the gettext() family of
functions for retrieving message strings from databases constructed to
internationalize software.


%package -n perl-%{tarname}
Summary:        %{summary}

%description -n perl-%{tarname}
The gettext module permits access from perl to the gettext() family of
functions for retrieving message strings from databases constructed to
internationalize software.

%prep
%setup -q -n %{tarname}-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS" NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}


%install
%{make_install}
%{_fixperms} $RPM_BUILD_ROOT/*


%check
# Testsuite fails w/ LANG=C.UTF-8 on fedora >= 40
%if !0%{?os2_version}
LANG=en_US.UTF-8 %{__make} test
%endif


%files -n perl-%{tarname}
%doc README
%{perl_vendorarch}/auto/Locale
%{perl_vendorarch}/Locale
%{_mandir}/man3/*.3*


%changelog
* Tue May 12 2026 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.07-2
- rebuild with perl 5.42.2

* Tue Apr 25 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.07-1
- initial version
