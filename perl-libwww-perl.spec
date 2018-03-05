Name:           perl-libwww-perl
Version:        6.32
Release:        2%{?dist}
Summary:        A Perl interface to the World-Wide Web
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/libwww-perl/
Vendor:         bww bitwise works GmbH
Source0:        http://www.cpan.org/authors/id/O/OA/OALDERS/libwww-perl-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl-generators
#BuildRequires:  perl-interpreter
#BuildRequires:  perl(:VERSION) >= 5.8.1
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)

# Run-time:
# Authen::NTLM 1.02 not used at tests
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
# Data::Dump 1.13 not used at tests
# Data::Dump::Trace not used at tests
BuildRequires:  perl(Digest::MD5)
BuildRequires:  perl(Encode) >= 2.12
BuildRequires:  perl(Encode::Locale)
BuildRequires:  perl(Exporter)
# Fcntl not used at tests
# File::Listing 6 not used at tests
# File::Spec not used at tests
BuildRequires:  perl(HTML::Entities)
BuildRequires:  perl(HTML::HeadParser)
BuildRequires:  perl(HTTP::Config)
# HTTP::Cookies 6 not used at tests
BuildRequires:  perl(HTTP::Date) >= 6
BuildRequires:  perl(HTTP::Headers::Util)
# HTTP::Negotiate 6 not used at tests
BuildRequires:  perl(HTTP::Request) >= 6
BuildRequires:  perl(HTTP::Request::Common) >= 6
BuildRequires:  perl(HTTP::Response) >= 6
BuildRequires:  perl(HTTP::Status) >= 6
# integer not used at tests
BuildRequires:  perl(IO::Select)
BuildRequires:  perl(IO::Socket)
BuildRequires:  perl(LWP::MediaTypes) >= 6
# Mail::Internet not needed
BuildRequires:  perl(MIME::Base64) >= 2.1
# Net::FTP 2.58 not used at tests
BuildRequires:  perl(Net::HTTP) >= 6.07
# Net::NNTP not used at tests
BuildRequires:  perl(parent)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Try::Tiny)
BuildRequires:  perl(URI) >= 1.10
BuildRequires:  perl(URI::Escape)
# URI::Heuristic not used at tests
BuildRequires:  perl(WWW::RobotRules) >= 6
# Optional run-time:
# CPAN::Config not used at tests
# HTML::Parse not used at tests

# Tests:
BuildRequires:  perl(Config)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(FindBin)
#BuildRequires:  perl(HTTP::Daemon) >= 6
#BuildRequires:  perl(Test::Fatal)
BuildRequires:  perl(Test::More)
#BuildRequires:  perl(Test::RequiresInternet)
BuildRequires:  perl(utf8)
# Optional tests:
# CPAN::Meta not helpful
# CPAN::Meta::Prereqs not helpful

Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Authen::NTLM) >= 1.02
Suggests:       perl(CPAN::Config)
Requires:       perl(Encode) >= 2.12
Requires:       perl(File::Spec)
Requires:       perl(File::Listing) >= 6
# Keep HTML::FormatPS optional
Suggests:       perl(HTML::FormatPS)
# Keep HTML::FormatText optional
Suggests:       perl(HTML::FormatText)
Requires:       perl(HTML::Entities)
Requires:       perl(HTML::HeadParser)
Suggests:       perl(HTML::Parse)
Requires:       perl(HTTP::Config)
Requires:       perl(HTTP::Cookies) >= 6
Requires:       perl(HTTP::Date) >= 6
Requires:       perl(HTTP::Headers::Util)
Requires:       perl(HTTP::Negotiate) >= 6
Requires:       perl(HTTP::Request) >= 6
Requires:       perl(HTTP::Request::Common) >= 6
Requires:       perl(HTTP::Response) >= 6
Requires:       perl(HTTP::Status) >= 6
Requires:       perl(LWP::MediaTypes) >= 6
Suggests:       perl(LWP::Protocol::https) >= 6.02
Requires:       perl(MIME::Base64) >= 2.1
Requires:       perl(Net::FTP) >= 2.58
Requires:       perl(Net::HTTP) >= 6.07
Requires:       perl(URI) >= 1.10
Requires:       perl(URI::Escape)
Requires:       perl(WWW::RobotRules) >= 6
Provides:       perl(LWP::Debug::TraceHTTP::Socket) = %{version}
Provides:       perl(LWP::Protocol::http::Socket) = %{version}
Provides:       perl(LWP::Protocol::http::SocketMethods) = %{version}

%description
The libwww-perl collection is a set of Perl modules which provides a simple and
consistent application programming interface to the World-Wide Web.  The main
focus of the library is to provide classes and functions that allow you to
write WWW clients. The library also contain modules that are of more general
use and even classes that help you implement simple HTTP servers.

# Remove underspecified dependencies
%global __requires_exclude %{?__requires_exclude:%{__requires_exclude}|}^perl\\((Authen::NTLM|Encode|File::Listing|HTTP::Date|HTTP::Negotiate|HTTP::Request|HTTP::Response|HTTP::Status|LWP::MediaTypes|MIME::Base64|Net::FTP|Net::HTTP|URI|WWW::RobotRules)\\)$

%prep
%setup -q -n libwww-perl-%{version} 

%build
# Install the aliases by default
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 --aliases < /dev/null
make %{?_smp_mflags}
make manifypods

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} $RPM_BUILD_ROOT/*

%check
unset PERL_LWP_ENV_HTTP_TEST_URL
# Some optional tests require resolvable hostname
#make test

%files
%license LICENSE
%doc Changes README.SSL
%{_bindir}/*
%{perl_vendorlib}/libwww/
%{perl_vendorlib}/LWP.pm
%{perl_vendorlib}/LWP/
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3*

%changelog
* Fri Mar 2 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> - 6.32-2
- enable more BuildRequires

* Thu Feb 22 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> - 6.32-1
- initial version
