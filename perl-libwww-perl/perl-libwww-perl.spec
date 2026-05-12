# Run optional tests
%if !0%{?os2_version}
%bcond_without perl_libwww_perl_enables_optional_test
%else
%bcond_with perl_libwww_perl_enables_optional_test
%endif
# Perform tests that need the Internet
%bcond_with perl_libwww_perl_enables_internet_test

Name:           perl-libwww-perl
Version:        6.82
Release:        1%{?dist}
Summary:        A Perl interface to the World-Wide Web
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/libwww-perl
Source0:        https://cpan.metacpan.org/authors/id/O/OA/OALDERS/libwww-perl-%{version}.tar.gz
# Normalize shelbangs, not suitable for an upstream
Patch0:         libwww-perl-6.39-Normalize-shebangs-in-examples.patch
%if 0%{?os2_version}
Vendor:         bww bitwise works GmbH
%endif
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.8.1
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)

# Run-time:
# Authen::NTLM 1.02 not used at tests
BuildRequires:  perl(Carp)
# Data::Dump 1.13 not used at tests
# Data::Dump::Trace not used at tests
BuildRequires:  perl(Digest::MD5)
BuildRequires:  perl(Encode) >= 2.12
BuildRequires:  perl(Encode::Locale)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Temp)
# Fcntl not used at tests
# File::Listing 6 not used at tests
# File::Spec not used at tests
BuildRequires:  perl(HTML::Entities)
BuildRequires:  perl(HTML::HeadParser) => 3.71
BuildRequires:  perl(HTTP::Config)
BuildRequires:  perl(HTTP::Cookies) >= 6
BuildRequires:  perl(HTTP::Date) >= 6
BuildRequires:  perl(HTTP::Headers::Util)
# HTTP::Negotiate 6 not used at tests
BuildRequires:  perl(HTTP::Request) >= 6.18
BuildRequires:  perl(HTTP::Request::Common) >= 6.18
BuildRequires:  perl(HTTP::Response) >= 6.18
BuildRequires:  perl(HTTP::Status) >= 6.18
# integer not used at tests
BuildRequires:  perl(IO::Select)
BuildRequires:  perl(IO::Socket)
BuildRequires:  perl(LWP::MediaTypes) >= 6
# Mail::Internet not needed
BuildRequires:  perl(MIME::Base64) >= 2.1
BuildRequires:  perl(Module::Load)
# Net::FTP 2.58 not used at tests
BuildRequires:  perl(Net::HTTP) >= 6.18
# Net::NNTP not used at tests
BuildRequires:  perl(parent) >= 0.217
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
BuildRequires:  perl(FindBin)
%if !0%{?os2_version}
BuildRequires:  perl(HTTP::CookieJar::LWP)
BuildRequires:  perl(HTTP::Daemon) >= 6.01
BuildRequires:  perl(Test::Fatal)
%endif
BuildRequires:  perl(Test::More) >= 0.96
%if %{with perl_libwww_perl_enables_internet_test}
BuildRequires:  perl(Test::RequiresInternet)
%endif
BuildRequires:  perl(utf8)
%if %{with perl_libwww_perl_enables_internet_test}
BuildRequires:  perl(Test::Needs)
%if %{with perl_libwww_perl_enables_optional_test}
# Optional tests:
# CPAN::Meta not helpful
# CPAN::Meta::Prereqs not helpful
BuildRequires:  perl(Test::LeakTrace)
%endif
%endif

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
Requires:       perl(HTTP::Request) >= 6.18
Requires:       perl(HTTP::Request::Common) >= 6.18
Requires:       perl(HTTP::Response) >= 6.18
Requires:       perl(HTTP::Status) >= 6.18
Requires:       perl(LWP::MediaTypes) >= 6
Suggests:       perl(LWP::Protocol::https) >= 6.02
Requires:       perl(MIME::Base64) >= 2.1
Requires:       perl(Net::FTP) >= 2.58
Requires:       perl(Net::HTTP) >= 6.18
Requires:       perl(URI) >= 1.10
Requires:       perl(URI::Escape)
Requires:       perl(WWW::RobotRules) >= 6
Provides:       perl(LWP::Debug::TraceHTTP::Socket) = %{version}
Provides:       perl(LWP::Protocol::http::Socket) = %{version}
Provides:       perl(LWP::Protocol::http::SocketMethods) = %{version}

# Remove underspecified dependencies
%global __requires_exclude %{?__requires_exclude:%{__requires_exclude}|}^perl\\((Authen::NTLM|Encode|File::Listing|HTTP::Cookies|HTTP::Daemon|HTTP::Date|HTTP::Negotiate|HTTP::Request|HTTP::Response|HTTP::Status|LWP::MediaTypes|MIME::Base64|Net::FTP|Net::HTTP|Test::More|URI|WWW::RobotRules)\\)$

%description
The libwww-perl collection is a set of Perl modules which provides a simple and
consistent application programming interface to the World-Wide Web.  The main
focus of the library is to provide classes and functions that allow you to
write WWW clients. The library also contain modules that are of more general
use and even classes that help you implement simple HTTP servers.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       coreutils
Requires:       perl-Test-Harness
Requires:       perl(HTTP::Cookies) >= 6
Requires:       perl(HTTP::CookieJar::LWP)
Requires:       perl(HTTP::Daemon) >= 6.01
Requires:       perl(HTTP::Request) >= 6.18
Requires:       perl(HTTP::Response) >= 6.18
Requires:       perl(Net::HTTP) >= 6.18
Requires:       perl(Test::More) >= 0.96
%if %{with perl_libwww_perl_enables_internet_test} && %{with perl_libwww_perl_enables_optional_test}
Requires:       perl(Test::LeakTrace)
%endif
Requires:       perl(URI) >= 1.10
Suggests:       perl(JSON::PP) => 2.27300

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n libwww-perl-%{version} 
%patch -P 0 -p1
%if !%{with perl_libwww_perl_enables_internet_test}
rm t/base/protocols/nntp.t t/leak/no_leak.t t/redirect.t
perl -i -ne 'print $_ unless m{^(?:t/base/protocols/nntp\.t|t/leak/no_leak\.t|t/redirect\.t)}' MANIFEST
%endif
# Help generators to recognize a Perl code
for F in $(find t -name '*.t') talk-to-ourself; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*\bperl}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
# Install the aliases by default
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1 --aliases < /dev/null
%{make_build}

%install
%{make_install}
%{_fixperms} %{buildroot}/*
# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t talk-to-ourself %{buildroot}%{_libexecdir}/%{name}
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/bash
set -e
# t/local/http.t writes to CWD
DIR=$(mktemp -d)
cp -a %{_libexecdir}/%{name}/* "$DIR"
pushd "$DIR"
unset COVERAGE PERL_LWP_ENV_HTTP_TEST_SERVER_TIMEOUT PERL_LWP_ENV_HTTP_TEST_URL
prove -I . -j "$(getconf _NPROCESSORS_ONLN)" -r
popd
rm -r "$DIR"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
%if !0%{?os2_version}
unset COVERAGE PERL_LWP_ENV_HTTP_TEST_SERVER_TIMEOUT PERL_LWP_ENV_HTTP_TEST_URL
make test
%endif

%files
%license LICENSE
%doc Changes examples README.SSL
%{_bindir}/*
%{perl_vendorlib}/*
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3*

%files tests
%{_libexecdir}/%{name}

%changelog
* Wed May 06 2026 Silvan Scherrer <silvan.scherrer@aroa.ch> - 6.82-1
- update to version 6.82
- resync with fedora spec

* Fri Mar 2 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> - 6.32-2
- enable more BuildRequires

* Thu Feb 22 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> - 6.32-1
- initial version
