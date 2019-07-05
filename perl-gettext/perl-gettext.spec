# This package should be renamed into perl-Locale-gettext
%global tarname Locale-gettext

Name:           perl-gettext
Version:        1.07
Release:        1%{?dist}
Summary:        Interface to gettext family of functions

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/gettext/
Vendor:         bww bitwise works GmbH
Source0:        http://search.cpan.org/CPAN/authors/id/P/PV/PVANDRY/%{tarname}-%{version}.tar.gz

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

%description
The gettext module permits access from perl to the gettext() family of
functions for retrieving message strings from databases constructed to
internationalize software.


%package -n perl-%{tarname}
Summary:        %{summary}
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

Obsoletes: perl-gettext < %{version}-%{release}
Obsoletes: perl-gettext%{?_isa} < %{version}-%{release}
Provides: perl-gettext = %{version}-%{release}
Provides: perl-gettext%{?_isa} = %{version}-%{release}


%description -n perl-%{tarname}
The gettext module permits access from perl to the gettext() family of
functions for retrieving message strings from databases constructed to
internationalize software.

%prep
%setup -q -n %{tarname}-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
# not supported by perl < 5.22
# NO_PACKLIST=1
make %{?_smp_mflags}
make manifypods

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
%{_fixperms} $RPM_BUILD_ROOT/*


%check
#make test


%files -n perl-%{tarname}
%doc README
%{perl_vendorarch}/auto/Locale
%{perl_vendorarch}/Locale
%{_mandir}/man3/*.3*


%changelog
* Tue Apr 25 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.07-1
- initial version
