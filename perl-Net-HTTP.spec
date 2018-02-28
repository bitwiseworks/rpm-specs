# Add support for IPv6 (not for OS/2)
%{bcond_with perl_Net_HTTP_enables_ipv6}
# Do not run network tests accessing Internet
%{bcond_with perl_Net_HTTP_enables_network_test}
# Add support for TLS/SSL
%{bcond_without perl_Net_HTTP_enables_ssl}

Name:           perl-Net-HTTP
Version:        6.17
Release:        1%{?dist}
Summary:        Low-level HTTP connection (client)
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Net-HTTP/
Vendor:         bww bitwise works GmbH
Source0:        http://www.cpan.org/authors/id/O/OA/OALDERS/Net-HTTP-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  make
#BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
#BuildRequires:  perl(:VERSION) >= 5.6.2
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(strict)
# Run-time:
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Compress::Raw::Zlib)
# Prefer IO::Socket::IP over IO::Socket::INET and IO::Socket::INET6
%if %{with perl_Net_HTTP_enables_ipv6}
BuildRequires:  perl(IO::Socket::IP)
%else
BuildRequires:  perl(IO::Socket)
%endif
%if %{with perl_Net_HTTP_enables_ssl}
BuildRequires:  perl(IO::Socket::SSL) >= 2.012
%endif
BuildRequires:  perl(IO::Uncompress::Gunzip)
BuildRequires:  perl(Symbol)
BuildRequires:  perl(URI)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
# Tests only:
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(IO::Select)
BuildRequires:  perl(IO::Socket::INET)
BuildRequires:  perl(Socket)
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Compress::Raw::Zlib)
Requires:       perl(IO::Uncompress::Gunzip)
# Prefer IO::Socket::IP over IO::Socket::INET and IO::Socket::INET6
%if %{with perl_Net_HTTP_enables_ipv6}
Requires:       perl(IO::Socket::IP)
%else
Requires:       perl(IO::Socket)
%endif
Requires:       perl(Symbol)
%if %{with perl_Net_HTTP_enables_ssl}
Requires:       perl(IO::Socket::SSL) >= 2.012
%endif
Conflicts:      perl-libwww-perl < 6

%description
The Net::HTTP class is a low-level HTTP client. An instance of the
Net::HTTP class represents a connection to an HTTP server. The HTTP
protocol is described in RFC 2616. The Net::HTTP class supports HTTP/1.0
and HTTP/1.1.

%prep
%setup -q -n Net-HTTP-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make manifypods
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} $RPM_BUILD_ROOT/*

%check
export NO_NETWORK_TESTING=%{without perl_Net_HTTP_enables_network_test}
#make test

%files
%license LICENSE
%doc Changes CONTRIBUTORS README.md
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Thu Feb 22 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> - 6.17-1
- initial version
