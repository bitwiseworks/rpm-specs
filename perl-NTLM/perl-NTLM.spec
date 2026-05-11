# Perform optional tests
%if !0%{?os2_version}
%bcond_without perl_NTLM_enables_optional_test
%else
%bcond_with perl_NTLM_enables_optional_test
%endif

Name:           perl-NTLM
Version:        1.09
Release:        2%{?dist}
Summary:        NTLM Perl module
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/NTLM
Source0:        https://cpan.metacpan.org/authors/id/N/NB/NBEBOUT/NTLM-%{version}.tar.gz
# Remove useless shebangs from the module files, CPAN RT#132167,
# submitted to the upstream
Patch0:         NTLM-1.09-Remove-shebangs-from-the-modules.patch
%if 0%{?os2_version}
Vendor:         bww bitwise works GmbH
%endif
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# Run-time
BuildRequires:  perl(constant)
BuildRequires:  perl(Digest::HMAC_MD5)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(MIME::Base64)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
# Tests
BuildRequires:  perl(Test::More)
BuildRequires:  perl(warnings)
%if %{with perl_NTLM_enables_optional_test}
# Optional tests
BuildRequires:  perl(Test::Pod)
%endif

%description
This module provides methods to use NTLM authentication.  It can be used
as an authenticate method with the Mail::IMAPClient module to perform
the challenge/response mechanism for NTLM connections or it can be used
on its own for NTLM authentication with other protocols (eg. HTTP).

%prep
%setup -q -n NTLM-%{version}
%patch -P0 -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}
%if 0%{?os2_version}
make manifypods
%endif

%install
%{make_install}
%{_fixperms} $RPM_BUILD_ROOT/*

%check
%if !0%{?os2_version}
make test
%endif

%files
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Mon May 11 2026 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.09-2
- rebuild with perl 5.42
- resync with fedora spec

* Fri Mar 02 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.09-1
- initial rpm
