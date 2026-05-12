# Test using JSON::MaybeXS instead of JSON::PP
%if ! (0%{?rhel} || 0%{?os2_version})
%{bcond_without perl_YAML_Tiny_enables_JSON_MaybeX_test}
%else
%{bcond_with perl_YAML_Tiny_enables_JSON_MaybeX_test}
%endif

Name:           perl-YAML-Tiny
Version:        1.76
Release:        1%{?dist}
Summary:        Read/Write YAML files with as little code as possible
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/YAML-Tiny
Source0:        https://www.cpan.org/modules/by-module/YAML/YAML-Tiny-%{version}.tar.gz
%if 0%{?os2_version}
Vendor:         bww bitwise works GmbH
%endif
BuildArch:      noarch
# Module Build
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# Module Runtime
BuildRequires:  perl(B)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Test Suite
BuildRequires:  perl(base)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Spec) >= 0.80
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(File::Temp) >= 0.19
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(IO::Dir)
BuildRequires:  perl(JSON::PP)
BuildRequires:  perl(lib)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(open)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(utf8)
BuildRequires:  perl(vars)
# Optional Tests
BuildRequires:  perl(CPAN::Meta) >= 2.120900
%if %{with perl_YAML_Tiny_enables_JSON_MaybeX_test}
BuildRequires:  perl(JSON::MaybeXS) >= 1.001000
%endif
# Dependencies
Requires:       perl(Carp)
Requires:       perl(Config)
Requires:       perl(Fcntl)

%description
YAML::Tiny is a Perl class for reading and writing YAML-style files,
written with as little code as possible, reducing load time and
memory overhead.

%prep
%setup -q -n YAML-Tiny-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}
%if 0%{?os2_version}
make manifypods
%endif

%install
%{make_install}
%{_fixperms} -c %{buildroot}

%check
%if !0%{?os2_version}
make test
%endif

%files
%license LICENSE
%doc Changes CONTRIBUTING README
%{perl_vendorlib}/YAML/
%if !0%{?os2_version}
%{_mandir}/man3/YAML::Tiny.3*
%else
%{_mandir}/man3/YAML.Tiny.3*
%endif

%changelog
* Tue May 12 2026 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.76-1
- initial version
