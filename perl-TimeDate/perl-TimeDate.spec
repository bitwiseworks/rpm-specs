# Perform optional tests
%if 0%{?rhel} || 0%{?os2_version}
%bcond_with perl_TimeDate_enables_optional_test
%else
%bcond_without perl_TimeDate_enables_optional_test
%endif

Name:           perl-TimeDate
Version:        2.35
Epoch:          1
Release:        1%{?dist}
Summary:        A Perl module for time and date manipulation
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/TimeDate
Source0:        https://cpan.metacpan.org/authors/id/A/AT/ATOOMIC/TimeDate-%{version}.tar.gz
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
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Time::Local)
BuildRequires:  perl(utf8)
# Tests:
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Test::More)
%if %{with perl_TimeDate_enables_optional_test}
# Optional tests:
BuildRequires:  perl(Pod::Checker)
%endif

%description
This module includes a number of smaller modules suited for
manipulation of time and date strings with Perl. In particular, the
Date::Format and Date::Parse modules can display and read times and
dates in various formats, providing a more reliable interface to
textual representations of points in time.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n TimeDate-%{version}
%if %{without perl_TimeDate_enables_optional_test}
    rm t/pod-valid.t
    perl -i -ne 'print $_ unless m{\At/pod-valid\.t\b}' MANIFEST
%endif
# Bogus exec permissions on some language modules
%if !0%{?os2_version}
chmod -x lib/Date/Language/{Russian_cp1251,Russian_koi8r,Turkish}.pm
%else
chmod -x lib/Date/Language/Russian_cp1251.pm
chmod -x lib/Date/Language/Russian_koi8r.pm
chmod -x lib/Date/Language/Turkish.pm
%endif

# Help generators to recognize Perl scripts
for F in t/*.t; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*perl\b}{$Config{startperl}}' "$F"
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
%if %{with perl_TimeDate_enables_optional_test}
    # Does not work without modules in ./lib
    rm %{buildroot}%{_libexecdir}/%{name}/t/pod-valid.t
%endif
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/sh
cd %{_libexecdir}/%{name} && exec prove -I . -r -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
%if !0%{?os2_version}
make test
%endif

%files 
%doc README Changes SECURITY.md
%license LICENSE
%dir %{perl_vendorlib}/Date/
%{perl_vendorlib}/Date/Format*
%{perl_vendorlib}/Date/Language*
%{perl_vendorlib}/Date/Parse.pm
%dir %{perl_vendorlib}/Time/
%{perl_vendorlib}/Time/Zone.pm
%{perl_vendorlib}/TimeDate.pm
%if !0%{?os2_version}
%{_mandir}/man3/Date::Format*.3*
%{_mandir}/man3/Date::Language*.3*
%{_mandir}/man3/Date::Parse*.3*
%{_mandir}/man3/Time::Zone*.3*
%else
%{_mandir}/man3/Date.Format*.3*
%{_mandir}/man3/Date.Language*.3*
%{_mandir}/man3/Date.Parse*.3*
%{_mandir}/man3/Time.Zone*.3*
%endif
%{_mandir}/man3/TimeDate*.3*

%files tests
%{_libexecdir}/%{name}

%changelog
* Wed May 06 2026 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.35-1
- update to version 2.35
- resync with fedora spec

* Mon May 08 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.30-1
- initial version
