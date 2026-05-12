%if !0%{?os2_version}
%bcond perl_HTTP_Message_enables_IO_Compress_Brotli %{undefined rhel}
%else
%bcond_with perl_HTTP_Message_enables_IO_Compress_Brotli
%endif

Name:           perl-HTTP-Message
Version:        7.01
Release:        1%{?dist}
Summary:        HTTP style message
# CONTRIBUTING.md:  CC0-1.0
# other files:      GPL-1.0-or-later OR Artistic-1.0-Perl
License:        (GPL-1.0-or-later OR Artistic-1.0-Perl) AND CC0-1.0
URL:            https://metacpan.org/release/HTTP-Message
Source0:        https://cpan.metacpan.org/authors/id/O/OA/OALDERS/HTTP-Message-%{version}.tar.gz
%if 0%{?os2_version}
Vendor:         bww bitwise works GmbH
%endif
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(parent)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Clone)
BuildRequires:  perl(Compress::Raw::Zlib)
BuildRequires:  perl(Encode) >= 3.01
BuildRequires:  perl(Encode::Locale) >= 1
BuildRequires:  perl(Exporter) >= 5.57
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(HTTP::Date) >= 6
%if %{with perl_HTTP_Message_enables_IO_Compress_Brotli}
BuildRequires:  perl(IO::Compress::Brotli)
%endif
BuildRequires:  perl(IO::Compress::Bzip2) >= 2.021
BuildRequires:  perl(IO::Compress::Deflate)
BuildRequires:  perl(IO::Compress::Gzip)
BuildRequires:  perl(IO::HTML)
BuildRequires:  perl(IO::Uncompress::Inflate)
BuildRequires:  perl(IO::Uncompress::RawInflate)
BuildRequires:  perl(LWP::MediaTypes) >= 6
BuildRequires:  perl(MIME::Base64) >= 2.1
BuildRequires:  perl(MIME::QuotedPrint)
BuildRequires:  perl(URI) >= 1.10
# Tests only:
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(lib)
BuildRequires:  perl(overload)
BuildRequires:  perl(PerlIO::encoding)
BuildRequires:  perl(Test::More) >= 0.88
%if !0%{?os2_version}
BuildRequires:  perl(Test::Needs)
%endif
# Time::Local only used on MacOS
BuildRequires:  perl(Try::Tiny)
BuildRequires:  perl(URI::URL)
%if %{with perl_HTTP_Message_enables_IO_Compress_Brotli}
Recommends:     perl(IO::Compress::Brotli)
%endif
Requires:       perl(Clone) => 0.46
Requires:       perl(Compress::Raw::Zlib) >= 2.062
Requires:       perl(Encode) >= 3.01
Requires:       perl(Encode::Locale) >= 1
Requires:       perl(HTTP::Date) >= 6
Requires:       perl(IO::Compress::Bzip2) >= 2.021
Requires:       perl(IO::Compress::Deflate)
Requires:       perl(IO::Compress::Gzip)
Requires:       perl(IO::HTML)
Requires:       perl(IO::Uncompress::Inflate)
Requires:       perl(IO::Uncompress::RawInflate)
Requires:       perl(LWP::MediaTypes) >= 6
Requires:       perl(MIME::Base64) >= 2.1
Requires:       perl(MIME::QuotedPrint)
Requires:       perl(URI) >= 1.10
Conflicts:      perl-libwww-perl < 6

# Remove underspecified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\((Clone|Exporter|HTTP::Date|URI)\\)$
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(HTTP::Headers\\)$
# Remove private modules and unused dependencies
%global __requires_exclude %{__requires_exclude}|^perl\\((Secret|Time::Local)\\)
%global __provides_exclude %{__provides_exclude}|^perl\\(Secret\\)$

%description
The HTTP-Message distribution contains classes useful for representing the
messages passed in HTTP style communication.  These are classes representing
requests, responses and the headers contained within them.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness
Requires:       perl(URI::URL)
%if %{with perl_HTTP_Message_enables_IO_Compress_Brotli}
Requires:       perl(IO::Compress::Brotli)
%endif

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n HTTP-Message-%{version}
# Help generators to recognize Perl scripts
for F in t/*.t; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!\s*perl}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/sh
cd %{_libexecdir}/%{name} && exec prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test
%{_fixperms} %{buildroot}/*

%check
%if !0%{?os2_version}
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
make test
%endif

%files
%license LICENSE
%doc Changes CONTRIBUTING.md README.md
%{perl_vendorlib}/*
%{_mandir}/man3/*

%files tests
%{_libexecdir}/%{name}

%changelog
* Wed May 06 2026 Silvan Scherrer <silvan.scherrer@aroa.ch> - 7.01-1
- update to version 7.01
- resync with fedora spec

* Mon May 08 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> - 6.11-1
- initial version
