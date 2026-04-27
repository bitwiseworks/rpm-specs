%global cpan_version_major 0.42
%global cpan_version_minor 34
%global cpan_version %{cpan_version_major}%{?cpan_version_minor}

# Run optional tests
%if ! (0%{?rhel}) && !0%{?os2_version}
%bcond_without perl_Module_Build_enables_optional_test
%else
%bcond_with perl_Module_Build_enables_optional_test
%endif

Name:           perl-Module-Build
Epoch:          2
Version:        %{cpan_version_major}%{?cpan_version_minor:.%cpan_version_minor}
Release:        1%{?dist}
Summary:        Build and install Perl modules
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Module-Build
%if !0%{?os2_version}
Source0:        https://cpan.metacpan.org/modules/by-module/Module/Module-Build-%{cpan_version}.tar.gz
# Handle missing ExtUtils::CBuilder as a missing compiler, bug #1547165.
Patch1:         Module-Build-0.4231-Do-not-die-on-missing-ExtUtils-CBuilder-in-have_c_co.patch
%else
Vendor:         bww bitwise works GmbH
%scm_source     github https://github.com/bitwiseworks/%{name}-os2 %{version}-os2
%endif
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  perl-devel
%if !0%{?os2_version}
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
%endif
BuildRequires:  perl(Archive::Tar)
BuildRequires:  perl(AutoSplit)
BuildRequires:  perl(base)
BuildRequires:  perl(blib)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(CPAN::Meta) >= 2.142060
BuildRequires:  perl(CPAN::Meta::Converter) >= 2.141170
BuildRequires:  perl(CPAN::Meta::Merge)
BuildRequires:  perl(CPAN::Meta::YAML) >= 0.003
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::CBuilder) >= 0.27
BuildRequires:  perl(ExtUtils::Install) >= 0.3
BuildRequires:  perl(ExtUtils::Installed)
BuildRequires:  perl(ExtUtils::Manifest) >= 1.54
BuildRequires:  perl(ExtUtils::Mkbootstrap)
BuildRequires:  perl(ExtUtils::Packlist)
BuildRequires:  perl(ExtUtils::ParseXS) >= 2.21
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Compare)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec) >= 0.82
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(File::Temp) >= 0.15
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(inc::latest)
BuildRequires:  perl(lib)
# perl(Module::Build) is loaded from ./lib
BuildRequires:  perl(Module::Metadata) >= 1.000002
BuildRequires:  perl(Parse::CPAN::Meta) >= 1.4401
BuildRequires:  perl(Perl::OSType) >= 1
BuildRequires:  perl(strict)
# Optional tests:
%if !%{defined perl_bootstrap}
%if %{with perl_Module_Build_enables_optional_test}
BuildRequires:  perl(Archive::Zip)
BuildRequires:  perl(File::ShareDir) >= 1.00
BuildRequires:  perl(PAR::Dist)
%if 0%{?fedora}  || 0%{?rhel} < 7
BuildRequires:  perl(Pod::Readme)
%endif
%endif
%endif
BuildRequires:  perl(TAP::Harness)
%if !0%{?os2_version}
BuildRequires:  perl(TAP::Harness::Env)
BuildRequires:  perl(Test::Harness) >= 3.29
%endif
BuildRequires:  perl(Test::More) >= 0.49
BuildRequires:  perl(Text::ParseWords)
BuildRequires:  perl(utf8)
BuildRequires:  perl(vars)
BuildRequires:  perl(version) >= 0.87
BuildRequires:  perl(warnings)
Requires:       perl(CPAN::Meta) >= 2.142060
Requires:       perl(CPAN::Meta::Converter) >= 2.141170
Requires:       perl(CPAN::Meta::Merge)
# Do not hard-require ExtUtils::CBuilder to allow installing Module::Build
# without gcc, bug #1547165. Module::Build users have to require
# ExtUtils::CBuilder explicitly according to "XS Extensions" section in
# Module::Build::Authoring POD.
Recommends:     perl(ExtUtils::CBuilder) >= 0.27
Requires:       perl(ExtUtils::Install) >= 0.3
Requires:       perl(ExtUtils::Manifest) >= 1.54
Requires:       perl(ExtUtils::Mkbootstrap)
Requires:       perl(ExtUtils::ParseXS) >= 2.21
Requires:       perl(inc::latest)
Requires:       perl(Module::Metadata) >= 1.000002
# Keep PAR support optional (PAR::Dist)
Requires:       perl(Perl::OSType) >= 1
Requires:       perl(TAP::Harness::Env)
Requires:       perl(Test::Harness)
%if !%{defined perl_bootstrap}
# Optional run-time needed for Software::License license identifier,
# bug #1152319
Requires:       perl(Software::License)
%endif
# Optional run-time needed for generating documentation from POD:
Requires:       perl(Pod::Html)
Requires:       perl(Pod::Man) >= 2.17
Requires:       perl(Pod::Text)
# Run-time for generated Build scripts from Build.PLs:
# Those are already found by dependency generator. Just make sure they
# present.
# Cwd
# File::Basename
# File::Spec
# strict

%{?perl_default_filter}
# Remove under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\((ExtUtils::Install|File::Spec|Module::Build|Module::Metadata|Perl::OSType)\\)$
%global __requires_exclude %__requires_exclude|^perl\\(CPAN::Meta::YAML\\) >= 0.002$

# Filter modules bundled for tests
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}^%{_libexecdir}
%global __requires_exclude %{__requires_exclude}|^perl\\(DistGen\\)
%global __requires_exclude %{__requires_exclude}|^perl\\(MBTest\\)
%global __requires_exclude %{__requires_exclude}|^perl\\(Simple\\)
%global __requires_exclude %{__requires_exclude}|^perl\\(Software::License.*\\)
%global __requires_exclude %{__requires_exclude}|^perl\\(Tie::CPHash\\)

%description
Module::Build is a system for building, testing, and installing Perl
modules. It is meant to be an alternative to ExtUtils::MakeMaker.
Developers may alter the behavior of the module through sub-classing in a
much more straightforward way than with MakeMaker. It also does not require
a make on your system - most of the Module::Build code is pure-perl and
written in a very cross-platform way. In fact, you don't even need a shell,
so even platforms like MacOS (traditional) can use it fairly easily. Its
only prerequisites are modules that are included with perl 5.6.0, and it
works fine on perl 5.005 if you can install a few additional modules.

%if !0%{?os2_version}
%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness
# Optional tests:
%if !%{defined perl_bootstrap}
%if %{with perl_Module_Build_enables_optional_test}
Requires:       perl(Archive::Zip)
Requires:       perl(File::ShareDir) >= 1.00
Requires:       perl(PAR::Dist)
%endif
%endif
Requires:       perl(TAP::Harness)
Requires:       perl(TAP::Harness::Env)
Requires:       perl(Text::ParseWords)
Requires:       perl(version) >= 0.87

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".
%endif

%prep
%if !0%{?os2_version}
%autosetup -p1 -n Module-Build-%{cpan_version}
%else
%scm_setup
%endif

# Help generators to recognize Perl scripts
for F in `find t -name *.t -o -name *.pl`; do
    perl -i.bkp -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*perl\b}{$Config{startperl}}' "$F"
    chmod +x "$F"
done
%if 0%{?os2_version}
find t/ -type f -name '*.bkp' -delete
%endif

%build
perl Build.PL --installdirs=vendor
./Build

%install
./Build install --destdir=%{buildroot} --create_packlist=0
%{_fixperms} -c %{buildroot}

# Install tests
%if !0%{?os2_version}
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t _build %{buildroot}%{_libexecdir}/%{name}
perl -pi -e 's#%{buildroot}##' %{buildroot}%{_libexecdir}/%{name}/_build/runtime_params
rm %{buildroot}%{_libexecdir}/%{name}/_build/magicnum
mkdir -p %{buildroot}%{_libexecdir}/%{name}/bin
ln -s %{_bindir}/config_data %{buildroot}%{_libexecdir}/%{name}/bin
# Requires copy of modules in test directory
rm %{buildroot}%{_libexecdir}/%{name}/t/00-compile.t
# Remove using of blib
for F in `find %{buildroot}%{_libexecdir}/%{name}/t -name *.t -o -name *.pm`; do
    perl -pi -e "s/^\s*blib_load\('([^']+)'\);/use \1;/" $F
    perl -pi -e "s/^blib_load '([^']+)';/use \1;/" $F
done
perl -pi -e "s{'-Mblib', }{'-I'.\\N{U+0024}tmp.'/Simple/blib/lib', '-I'.\\N{U+0024}tmp.'/Simple/blib/arch', }x" \
    %{buildroot}%{_libexecdir}/%{name}/t/xs.t
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/bash
set -e
# Some tests write into temporary files/directories. The easiest solution
# is to copy the tests into a writable directory and execute them from there.
DIR=$(mktemp -d)
pushd "$DIR"
cp -a %{_libexecdir}/%{name}/* ./
prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
popd
rm -rf "$DIR"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test
%endif

%check
%if !0%{?os2_version}
rm t/signature.t
LANG=C TEST_SIGNATURE=1 MB_TEST_EXPERIMENTAL=1 ./Build test
%endif

%files
%license LICENSE
%doc Changes contrib/ README
%{_bindir}/config_data
%{perl_vendorlib}/Module/
%{_mandir}/man1/config_data.1*
%if !0%{?os2_version}
%{_mandir}/man3/Module::Build*.3*
%else
%{_mandir}/man3/Module.Build*.3*
%endif

%if !0%{?os2_version}
%files tests
%{_libexecdir}/%{name}
%endif

%changelog
* Mon Apr 27 2026 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2:0.4234-1
- initial version
