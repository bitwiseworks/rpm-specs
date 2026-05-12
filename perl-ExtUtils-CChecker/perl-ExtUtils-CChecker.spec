Name:           perl-ExtUtils-CChecker
Version:        0.12
Release:        1%{?dist}
Summary:        Configure-time utilities for using C headers, libraries, or OS features
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/ExtUtils-CChecker
Source0:        https://cpan.metacpan.org/modules/by-module/ExtUtils/ExtUtils-CChecker-%{version}.tar.gz
BuildArch:      noarch
%if 0%{?os2_version}
Vendor:         bww bitwise works GmbH
%endif
# Build:
BuildRequires:  coreutils
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(:VERSION) >= 5.14
BuildRequires:  perl(Carp)
BuildRequires:  perl(ExtUtils::CBuilder)
# Tests:
BuildRequires:  perl(Config)
BuildRequires:  perl(Test2::V0)
# Optional Tests:
%if !0%{?os2_version}
BuildRequires:  perl(Test::Pod) >= 1.00
%endif
# Dependencies:
Requires:       perl(Module::Build)

%description
Often Perl modules are written to wrap functionality found in existing C
headers, libraries, or to use OS-specific features. It is useful in the
Build.PL or Makefile.PL file to check for the existence of these
requirements before attempting to actually build the module.

%prep
%setup -qn ExtUtils-CChecker-%{version}

%build
perl Build.PL --installdirs=vendor
./Build

%install
./Build install --destdir=%{buildroot} --create_packlist=0
%{_fixperms} -c %{buildroot}

%check
%if !0%{?os2_version}
./Build test
%endif

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/ExtUtils/
%if !0%{?os2_version}
%{_mandir}/man3/ExtUtils::CChecker.3*
%else
%{_mandir}/man3/ExtUtils.CChecker.3*
%endif

%changelog
* Tue May 12 2026 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.12-1
- initial version
