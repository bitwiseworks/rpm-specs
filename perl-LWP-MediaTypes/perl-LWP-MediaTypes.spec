# Use system-wide mailcap database
%if !0%{?os2_version}
%bcond_without perl_LWP_MediaTypes_enables_mailcap
%else
%bcond_with perl_LWP_MediaTypes_enables_mailcap
%endif

Name:           perl-LWP-MediaTypes
Version:        6.04
Release:        1%{?dist}
Summary:        Guess media type for a file or a URL
# lib/LWP/media.types:      CC0-1.0
# lib/LWP/MediaTypes.pm:    GPL-1.0-or-later OR Artistic-1.0-Perl
License:        (GPL-1.0-or-later OR Artistic-1.0-Perl) AND CC0-1.0
URL:            https://metacpan.org/release/LWP-MediaTypes
Source0:        https://cpan.metacpan.org/authors/id/O/OA/OALDERS/LWP-MediaTypes-%{version}.tar.gz
%if 0%{?os2_version}
Vendor:         bww bitwise works GmbH
%endif
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.6.2
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  sed
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(Scalar::Util)
# Tests only:
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(overload)
%if !0%{?os2_version}
BuildRequires:  perl(Test::Fatal)
%endif
BuildRequires:  perl(Test::More)
# Optional tests:
# CPAN::Meta not helpful
# CPAN::Meta::Prereqs not helpful
Requires:       perl(File::Basename)
%if %{with perl_LWP_MediaTypes_enables_mailcap}
Requires:       mailcap
%endif
Conflicts:      perl-libwww-perl < 6

%description
This module provides functions for handling media (also known as MIME)
types and encodings. The mapping from file extensions to media types is
defined by the media.types file. If the ~/.media.types file exists it is
used instead. For backwards compatibility we will also look for
~/.mime.types.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n LWP-MediaTypes-%{version}
%if %{with perl_LWP_MediaTypes_enables_mailcap}
# Use system-wide mailcap database
sed -i -e '/my @priv_files = ();/ s|()|("/etc/mime.types")|' \
    lib/LWP/MediaTypes.pm
%endif
# Help generators to recognize Perl scripts
for F in $(find t/ -name '*.t'); do
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
# README file is used in tests
cp README %{buildroot}%{_libexecdir}/%{name}
rm -f %{buildroot}%{_libexecdir}/%{name}/t/00*
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/sh
cd %{_libexecdir}/%{name} && exec prove -I . -j "$(getconf _NPROCESSORS_ONLN)" -r
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test
%{_fixperms} %{buildroot}/*

%check
%if !0%{?os2_version}
make test
%endif

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%files tests
%{_libexecdir}/%{name}

%changelog
* Wed May 06 2026 Silvan Scherrer <silvan.scherrer@aroa.ch> - 6.04-1
- update to version 6.04
- resync with latet fedora spec

* Mon May 08 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> - 6.02-1
- initial version
