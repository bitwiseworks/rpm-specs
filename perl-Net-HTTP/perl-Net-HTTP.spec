# Add support for IPv6
%if 0%{?os2_version}
%{bcond_without perl_Net_HTTP_enables_ipv6}
%else
%{bcond_with perl_Net_HTTP_enables_ipv6}
%endif
# Do not run network tests accessing Internet
%{bcond_with perl_Net_HTTP_enables_network_test}
# Add support for TLS/SSL
%{bcond_without perl_Net_HTTP_enables_ssl}

Name:           perl-Net-HTTP
Version:        6.24
Release:        1%{?dist}
Summary:        Low-level HTTP connection (client)
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Net-HTTP
Source0:        https://cpan.metacpan.org/authors/id/O/OA/OALDERS/Net-HTTP-%{version}.tar.gz
%if 0%{?os2_version}
Vendor:         bww bitwise works GmbH
%endif
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.6.2
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(strict)
# Run-time:
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Compress::Raw::Zlib)
# Prefer IO::Socket::IP over IO::Socket::INET
%if %{with perl_Net_HTTP_enables_ipv6}
BuildRequires:  perl(IO::Socket::IP)
%else
BuildRequires:  perl(IO::Socket)
%endif
%if %{with perl_Net_HTTP_enables_ssl}
# IO::Socket::SSL or Net::SSL
BuildRequires:  perl(IO::Socket::SSL) >= 2.012
%endif
BuildRequires:  perl(IO::Uncompress::Gunzip)
BuildRequires:  perl(Symbol)
BuildRequires:  perl(URI)
BuildRequires:  perl(warnings)
# Tests only:
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(IO::Select)
BuildRequires:  perl(IO::Socket::INET)
BuildRequires:  perl(Socket)
BuildRequires:  perl(Test::More)
Requires:       perl(Compress::Raw::Zlib)
Requires:       perl(IO::Uncompress::Gunzip)
# Prefer IO::Socket::IP over IO::Socket::INET
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

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness
%if %{with perl_Net_HTTP_enables_network_test}
%if %{with perl_Net_HTTP_enables_ssl}
Requires:  perl(IO::Socket::SSL) >= 2.012
%endif
%endif

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Net-HTTP-%{version}
%if %{without perl_Net_HTTP_enables_network_test}
rm t/live*.t
perl -i -ne 'print $_ unless m{^t/live.*\.t}' MANIFEST
%endif
# Help generators to recognize a Perl code
for F in t/*.t; do
    perl -i -MConfig -pe 'print qq{$Config{startperl}\n} if $. == 1 && !s{\A#!.*\bperl}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} %{buildroot}/*
# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/sh
set -e
cd %{_libexecdir}/%{name} && exec prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
%if !0%{?os2_version}
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
make test
%endif

%files
%license LICENSE
%doc Changes CONTRIBUTORS README.md
%{perl_vendorlib}/*
%{_mandir}/man3/*

%files tests
%{_libexecdir}/%{name}

%changelog
* Thu May 07 2026 Silvan Scherrer <silvan.scherrer@aroa.ch> - 6.24-1
- update to version 6.24
- resync with fedora spec

* Thu Feb 22 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> - 6.17-1
- initial version
