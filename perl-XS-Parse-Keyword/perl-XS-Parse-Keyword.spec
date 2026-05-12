# Perform optional tests
%if !0%{?os2_version}
%bcond_without perl_XS_Parse_Keyword_enables_optional_test
%else
%bcond_with perl_XS_Parse_Keyword_enables_optional_test
%endif

Name:           perl-XS-Parse-Keyword
Version:        0.49
Release:        1%{?dist}
Summary:        XS functions to assist in parsing keyword syntax
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/XS-Parse-Keyword
Source0:        https://cpan.metacpan.org/authors/id/P/PE/PEVANS/XS-Parse-Keyword-%{version}.tar.gz
Source1:        macros.perl-XS-Parse-Keyword
%if 0%{?os2_version}
Vendor:         bww bitwise works GmbH
%endif
BuildRequires:  coreutils
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.14
BuildRequires:  perl(B)
BuildRequires:  perl(base)
BuildRequires:  perl(ExtUtils::CBuilder)
BuildRequires:  perl(ExtUtils::CChecker) >= 0.11
BuildRequires:  perl(lib)
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(File::ShareDir) >= 1.00
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(XSLoader)
# Tests:
BuildRequires:  perl(B::Deparse)
# Some t/*.xs tests need a newer ExtUtils::ParseXS
BuildRequires:  perl(ExtUtils::ParseXS) >= 3.16
BuildRequires:  perl(feature)
BuildRequires:  perl(overload)
BuildRequires:  perl(utf8)
BuildRequires:  perl(Test2::V0)
%if %{with perl_XS_Parse_Keyword_enables_optional_test}
# Optional tests:
BuildRequires:  perl(Test::Pod) >= 1.00
%endif
# This module maintains multiple ABIs whose compatibility is checked at
# run-time by S_boot_xs_parse_keyword() compiled into the users of this module.
# This ABI range is defined with XS::Parse::Keyword/ABIVERSION_MIN and
# XS::Parse::Keyword/ABIVERSION_MAX in lib/XS/Parse/Keyword.xs.
Provides:       perl(:XS_Parse_Keyword_ABI_1) = 1
Provides:       perl(:XS_Parse_Keyword_ABI_2) = 2
# This module maintains multiple ABIs whose compatibility is checked at
# run-time by S_boot_xs_parse_infix() compiled into the users of this module.
# This ABI range is defined with XS::Parse::Infix/ABIVERSION_MIN and
# XS::Parse::Infix/ABIVERSION_MAX in lib/XS/Parse/Keyword.xs.
Provides:       perl(:XS_Parse_Infix_ABI_1) = 1
Provides:       perl(:XS_Parse_Infix_ABI_2) = 2

# Filter private modules
%global __requires_exclude %{?__requires_exclude:%{__requires_exclude}|}^perl\\(testcase\\)
%global __provides_exclude %{?__provides_exclude:%{__provides_exclude}|}^perl\\(testcase\\)

%description
This module provides some XS functions to assist in writing syntax modules
that provide new perl-visible syntax, primarily for authors of keyword plugins
using the PL_keyword_plugin hook mechanism.

%package Builder
Summary:        Build-time support for XS::Parse::Keyword
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-interpreter
Requires:       perl(File::ShareDir) >= 1.00
Requires:       perl(File::Spec)
Requires:       perl(XS::Parse::Infix)
Requires:       perl(XS::Parse::Keyword)
# Subpackaged in 0.06
Conflicts:      %{name}%{?_isa} < 0.06

%description Builder
This module provides a build-time helper to assist authors writing XS modules
that use XS::Parse::Keyword. It prepares a Module::Build-using distribution to
be able to make use of XS::Parse::Keyword.

%package tests
Summary:        Tests for %{name}
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness
# ExtUtils::ParseXS is not needed at run-time because the XS tests are
# packaged precompiled.
Requires:       perl(XSLoader)

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%autosetup -p1 -n XS-Parse-Keyword-%{version}
%if !%{with perl_XS_Parse_Keyword_enables_optional_test}
rm t/99pod.t
perl -i -ne 'print $_ unless m{\A\Qt/99pod.t\E\b}' MANIFEST
%endif
chmod +x t/*.t

%build
perl Build.PL --installdirs=vendor --optimize="$RPM_OPT_FLAGS"
./Build
# Build object files for tests now. They are installed into tests subpackage.
./Build testlib

%install
./Build install --destdir=%{buildroot} --create_packlist=0
find %{buildroot} -type f -name '*.bs' -size 0 -delete
%{_fixperms} %{buildroot}/*
install -D -m 0644 -t %{buildroot}%{_rpmmacrodir} %{SOURCE1}
# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
find %{buildroot}%{_libexecdir}/%{name} -type f \
    \( -name '*.bs' -o -name '*.c' -o -name '*.o' \) -delete
%if %{with perl_XS_Parse_Keyword_enables_optional_test}
rm %{buildroot}%{_libexecdir}/%{name}/t/99pod.t
%endif
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/sh
cd %{_libexecdir}/%{name} && exec prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
%if !0%{?os2_version}
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
./Build test
%endif

%files
%license LICENSE
%doc Changes README
%dir %{perl_vendorarch}/auto/XS
%dir %{perl_vendorarch}/auto/XS/Parse
%{perl_vendorarch}/auto/XS/Parse/Keyword
%dir %{perl_vendorarch}/XS
%dir %{perl_vendorarch}/XS/Parse
%{perl_vendorarch}/XS/Parse/Infix.pm
%{perl_vendorarch}/XS/Parse/Keyword.pm
%if !0%{?os2_version}
%{_mandir}/man3/XS::Parse::Infix.*
%{_mandir}/man3/XS::Parse::Keyword.*
%else
%{_mandir}/man3/XS.Parse.Infix.3*
%{_mandir}/man3/XS.Parse.Keyword.3*
%endif

%files Builder
%dir %{perl_vendorarch}/auto/share
%dir %{perl_vendorarch}/auto/share/module
%{perl_vendorarch}/auto/share/module/XS-Parse-Infix
%{perl_vendorarch}/auto/share/module/XS-Parse-Keyword
%{perl_vendorarch}/XS/Parse/Infix
%{perl_vendorarch}/XS/Parse/Keyword
%if !0%{?os2_version}
%{_mandir}/man3/XS::Parse::Infix::*
%{_mandir}/man3/XS::Parse::Keyword::*
%else
%{_mandir}/man3/XS.Parse.Infix.B*
%{_mandir}/man3/XS.Parse.Keyword.B*
%endif
%{_rpmmacrodir}/macros.%{name}

%files tests
%{_libexecdir}/%{name}

%changelog
* Tue May 12 2026 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.49-1
- initial version
