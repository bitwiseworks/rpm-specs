%if 0%{?rhel} >= 9 || 0%{?os2_version}
%bcond_with perl_IO_Socket_SSL_test_unused_idn
%bcond_with perl_IO_Socket_SSL_test_IO_Socket_INET6
%else
%bcond_without perl_IO_Socket_SSL_test_unused_idn
%bcond_without perl_IO_Socket_SSL_test_IO_Socket_INET6
%endif

Name:		perl-IO-Socket-SSL
Version:	2.098
Release:	1%{?dist}
Summary:	Perl library for transparent SSL
License:	(GPL-1.0-or-later OR Artistic-1.0-Perl) AND MPL-2.0
URL:		https://metacpan.org/release/IO-Socket-SSL
Source0:	https://cpan.metacpan.org/modules/by-module/IO/IO-Socket-SSL-%{version}.tar.gz
Patch0:		IO-Socket-SSL-2.096-use-system-default-cipher-list.patch
Patch1:		IO-Socket-SSL-2.098-use-system-default-SSL-version.patch
# A test for Enable-Post-Handshake-Authentication-TLSv1.3-feature.patch,
# bug #1632660, requires openssl tool
Patch2:		IO-Socket-SSL-2.087-Test-client-performs-Post-Handshake-Authentication.patch
%if 0%{?os2_version}
Vendor:         bww bitwise works GmbH
%endif
BuildArch:	noarch
# Module Build
BuildRequires:	coreutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker) >= 6.76
# Module Runtime
BuildRequires:	openssl-libs >= 0.9.8
BuildRequires:	perl(Carp)
BuildRequires:	perl(Config)
BuildRequires:	perl(constant)
BuildRequires:	perl(Errno)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(HTTP::Tiny)
BuildRequires:	perl(IO::Socket)
BuildRequires:	perl(IO::Socket::INET)
BuildRequires:	perl(IO::Socket::IP) >= 0.31
BuildRequires:	perl(Net::SSLeay) >= 1.46
BuildRequires:	perl(Scalar::Util)
BuildRequires:	perl(Socket) >= 1.95
BuildRequires:	perl(strict)
BuildRequires:	perl(Symbol)
BuildRequires:	perl(URI::_idna)
BuildRequires:	perl(vars)
BuildRequires:	perl(warnings)
# Test Suite
# openssl tool required for Test-client-performs-Post-Handshake-Authentication.patch
BuildRequires:	openssl
BuildRequires:	perl(Data::Dumper)
BuildRequires:	perl(File::Temp)
BuildRequires:	perl(FindBin)
BuildRequires:	perl(IO::Select)
%if %{with perl_IO_Socket_SSL_test_IO_Socket_INET6}
BuildRequires:	perl(IO::Socket::INET6) >= 2.62
%endif
# IPC::Run for Test-client-performs-Post-Handshake-Authentication.patch
%if !0%{?os2_version}
BuildRequires:	perl(IPC::Run)
%endif
%if %{with perl_IO_Socket_SSL_test_unused_idn}
BuildRequires:	perl(Net::IDN::Encode)
BuildRequires:	perl(Net::LibIDN)
%endif
BuildRequires:	perl(Test::More) >= 0.88
BuildRequires:	perl(utf8)
%if !0%{?os2_version}
BuildRequires:	procps
%endif
# Dependencies
Requires:	openssl-libs >= 0.9.8
Requires:	perl(Config)
Requires:	perl(HTTP::Tiny)
Requires:	perl(IO::Socket::INET)
Requires:	perl(IO::Socket::IP) >= 0.31
Requires:	perl(Socket) >= 1.95
Requires:	perl(URI::_idna)

%description
This module is a true drop-in replacement for IO::Socket::INET that
uses SSL to encrypt data before it is transferred to a remote server
or client. IO::Socket::SSL supports all the extra features that one
needs to write a full-featured SSL client or server application:
multiple SSL contexts, cipher selection, certificate verification, and
SSL version selection. As an extra bonus, it works perfectly with
mod_perl.

%prep
%setup -q -n IO-Socket-SSL-%{version}

# Use system-wide default cipher list to support use of system-wide
# crypto policy (#1076390, #1127577, CPAN RT#97816)
# https://fedoraproject.org/wiki/Changes/CryptoPolicy
%patch -P 0

# Use system-default SSL version too
%patch -P 1

# Add a test for PHA
%patch -P 2 -p1

%build
NO_NETWORK_TESTING=1 perl Makefile.PL \
	INSTALLDIRS=vendor \
	NO_PACKLIST=1 \
	NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} -c %{buildroot}

%check
%if !0%{?os2_version}
make test
%endif

%files
# GPL-1.0-or-later OR Artistic-1.0-Perl
%doc BUGS Changes README docs/ example/
%dir %{perl_vendorlib}/IO/
%dir %{perl_vendorlib}/IO/Socket/
%dir %{perl_vendorlib}/IO/Socket/SSL/
%doc %{perl_vendorlib}/IO/Socket/SSL.pod
%{perl_vendorlib}/IO/Socket/SSL.pm
%{perl_vendorlib}/IO/Socket/SSL/Intercept.pm
%{perl_vendorlib}/IO/Socket/SSL/Utils.pm
%if !0%{?os2_version}
%{_mandir}/man3/IO::Socket::SSL.3*
%{_mandir}/man3/IO::Socket::SSL::Intercept.3*
%{_mandir}/man3/IO::Socket::SSL::Utils.3*
%else
%{_mandir}/man3/IO.Socket.SSL.3*
%{_mandir}/man3/IO.Socket.SSL.Intercept.3*
%{_mandir}/man3/IO.Socket.SSL.Utils.3*
%endif
# MPL-2.0
%{perl_vendorlib}/IO/Socket/SSL/PublicSuffix.pm
%if !0%{?os2_version}
%{_mandir}/man3/IO::Socket::SSL::PublicSuffix.3*
%else
%{_mandir}/man3/IO.Socket.SSL.PublicSuffix.3*
%endif

%changelog
* Fri May 08 2026 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.098-1
- update to version 2.098
- resync with latet fedora spec

* Fri Feb 23 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.056-1
- initial version
