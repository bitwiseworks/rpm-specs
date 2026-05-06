Name:           perl-Encode-Locale
Version:        1.05
Release:        2%{?dist}
Summary:        Determine the locale encoding
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Encode-Locale
Source0:        https://cpan.metacpan.org/authors/id/G/GA/GAAS/Encode-Locale-%{version}.tar.gz
%if 0%{?os2_version}
Vendor:         bww bitwise works GmbH
%endif
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# Run-time:
BuildRequires:  perl(base)
BuildRequires:  perl(Encode) >= 2
BuildRequires:  perl(Encode::Alias)
# Encode::HanExtra not used at tests, not yet packaged
BuildRequires:  perl(Exporter)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Win32 not used on Linux
# Win32::API not used on Linux
# Win32::Console not used on Linux
# Recommended:
BuildRequires:  perl(I18N::Langinfo)
# Tests only:
BuildRequires:  perl(Test::More)
BuildRequires:  perl(utf8)
Requires:       perl(Encode) >= 2
# Encode::HanExtra not yet packaged
# Recommended:
Requires:       perl(I18N::Langinfo)
Requires:       perl(warnings)

%{?perl_default_filter}
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Encode\\)$

%description
In many applications it's wise to let Perl use Unicode for the strings
it processes.  Most of the interfaces Perl has to the outside world is
still byte based.  Programs therefore needs to decode byte strings
that enter the program from the outside and encode them again on the
way out.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Encode-Locale-%{version}
# Help generators to recognize Perl scripts
for F in t/*.t; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!\s*perl}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}
%if 0%{?os2_version}
make manifypods
%endif

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
make test
%endif

%files
%doc Changes README
%{perl_vendorlib}/Encode/
%if !0%{?os2_version}
%{_mandir}/man3/Encode::Locale.3*
%else
%{_mandir}/man3/Encode.Locale.3*
%endif

%files tests
%{_libexecdir}/%{name}

%changelog
* Wed May 06 2026 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.05-2
- rebuild with latest perl
- resync with fedora spec

* Mon May 08 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.05-1
- initial version
