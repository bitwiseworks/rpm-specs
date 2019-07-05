Name:		perl-IO-Socket-SSL
Version:	2.056
Release:	1%{?dist}
Summary:	Perl library for transparent SSL
License:	GPL+ or Artistic
URL:		http://search.cpan.org/dist/IO-Socket-SSL/
Vendor:         bww bitwise works GmbH
Source0:	http://search.cpan.org/CPAN/authors/id/S/SU/SULLR/IO-Socket-SSL-%{version}.tar.gz
BuildArch:	noarch
# Module Build
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	make
BuildRequires:	perl-generators
#BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker)
# Module Runtime
BuildRequires:	openssl >= 0.9.8
BuildRequires:	perl(Carp)
BuildRequires:	perl(Config)
BuildRequires:	perl(constant)
BuildRequires:	perl(Errno)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(HTTP::Tiny)
BuildRequires:	perl(IO::Socket)
#BuildRequires:	perl(IO::Socket::INET6) >= 2.62
BuildRequires:	perl(Net::SSLeay) >= 1.46
BuildRequires:	perl(Scalar::Util)
BuildRequires:	perl(Socket)
#BuildRequires:	perl(Socket6)
BuildRequires:	perl(strict)
BuildRequires:	perl(vars)
BuildRequires:	perl(warnings)
# Test Suite
BuildRequires:	perl(Data::Dumper)
BuildRequires:	perl(File::Temp)
BuildRequires:	perl(FindBin)
BuildRequires:	perl(IO::Select)
BuildRequires:	perl(IO::Socket::INET)
BuildRequires:	perl(Test::More) >= 0.88
BuildRequires:	perl(utf8)
#BuildRequires:	procps
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	openssl >= 0.9.8
Requires:	perl(Config)
Requires:	perl(HTTP::Tiny)

# no IPV6 on OS/2
%if 0
# Use IO::Socket::IP for IPv6 support where available, else IO::Socket::INET6
%if 0%{?fedora} > 15 || 0%{?rhel} > 6
BuildRequires:	perl(IO::Socket::IP) >= 0.20, perl(Socket) >= 1.95
Requires:	perl(IO::Socket::IP) >= 0.20, perl(Socket) >= 1.95
%else
Requires:	perl(IO::Socket::INET6) >= 2.62, perl(Socket6)
%endif
%endif

# IDN back-ends: URI::_idna (from URI  1.50) is preferred
# but Net::IDN::Encode (next pref) and Net::LibIDN are also tested
%if 0
BuildRequires:	perl(Net::IDN::Encode)
BuildRequires:	perl(Net::LibIDN)
%endif
%if 0%{?fedora:1} || 0%{?rhel} > 6 || 0%{?os2:1}
BuildRequires:	perl(URI::_idna)
Requires:	perl(URI::_idna)
%else
Requires:	perl(Net::IDN::Encode)
%endif

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

%build
NO_NETWORK_TESTING=1 perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}
make manifypods

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

%check
#make test

%files
%doc BUGS Changes README docs/ certs/ example/
%dir %{perl_vendorlib}/IO/
%dir %{perl_vendorlib}/IO/Socket/
%doc %{perl_vendorlib}/IO/Socket/SSL.pod
%{perl_vendorlib}/IO/Socket/SSL.pm
%{perl_vendorlib}/IO/Socket/SSL/
%{_mandir}/man3/IO.Socket.SSL.3*
%{_mandir}/man3/IO.Socket.SSL.Intercept.3*
%{_mandir}/man3/IO.Socket.SSL.PublicSuffix.3*
%{_mandir}/man3/IO.Socket.SSL.Utils.3*

%changelog
* Fri Feb 23 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.056-1
- initial version
