# Run prefork and optional test
%if ! (0%{?rhel} || 0%{?os2_version})
%{bcond_without perl_Module_ScanDeps_enables_prefork}
%{bcond_without perl_Module_ScanDeps_enables_optional_tests}
%else
%{bcond_with perl_Module_ScanDeps_enables_prefork}
%{bcond_with perl_Module_ScanDeps_enables_optional_tests}
%endif

Name:           perl-Module-ScanDeps
Summary:        Recursively scan Perl code for dependencies
Version:        1.37
Release:        1%{?dist}
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Module-ScanDeps
Source0:        https://cpan.metacpan.org/authors/id/R/RS/RSCHUPP/Module-ScanDeps-%{version}.tar.gz
%if 0%{?os2_version}
Vendor:         bww bitwise works GmbH
%endif
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(B)
BuildRequires:  perl(Config)
BuildRequires:  perl(constant)
# CPANPLUS::Backend is optional and not used by tests
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Data::Dumper)
# Digest::MD5 is optional and not used by tests
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(Encode)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(FileHandle)
BuildRequires:  perl(FindBin)
# Getopt::Long not used by tests
BuildRequires:  perl(List::Util)
BuildRequires:  perl(Module::Metadata)
# Storable is optional and not used by tests
# subs not used by tests
# Text::ParseWords not used by tests
BuildRequires:  perl(vars)
BuildRequires:  perl(version)
# VMS::Filespec never used
# Tests:
BuildRequires:  perl(autouse)
BuildRequires:  perl(AutoLoader)
BuildRequires:  perl(blib)
BuildRequires:  perl(Carp)
BuildRequires:  perl(if)
%if !0%{?os2_version}
BuildRequires:  perl(IPC::Run3) >= 0.048
%endif
BuildRequires:  perl(less)
BuildRequires:  perl(lib)
BuildRequires:  perl(Net::FTP)
BuildRequires:  perl(Test::More)
%if !0%{?os2_version}
BuildRequires:  perl(Test::Requires)
%endif
# Optional tests:
%if %{with perl_Module_ScanDeps_enables_optional_tests}
BuildRequires:  perl(Module::Pluggable)
%if !%{defined perl_bootstrap} && %{with perl_Module_ScanDeps_enables_prefork}
# Cycle: perl-Module-ScanDeps → perl-prefork → perl-Perl-MinimumVersion
# → perl-Perl-Critic → perl-Pod-Spell → perl-File-ShareDir-ProjectDistDir
# → perl-Path-Tiny → perl-Unicode-UTF8 → perl-Module-Install
# → perl-Module-ScanDeps
BuildRequires:  perl(prefork)
%endif
BuildRequires:  perl(Test::Pod) >= 1.00
%endif
Requires:       perl(B)
Requires:       perl(DynaLoader)
Requires:       perl(Data::Dumper)
Requires:       perl(Encode)
Requires:       perl(File::Find)
Requires:       perl(FindBin)
Requires:       perl(Text::ParseWords)
Recommends:     perl(Digest::MD5)
Recommends:     perl(Storable)
Suggests:       perl(CPANPLUS::Backend)

# Filter modules bundled for tests
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}^%{_libexecdir}/%{name}
%global __requires_exclude_from %{?__requires_exclude_from:%__requires_exclude_from|}^%{_libexecdir}/%{name}/t/data
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Utils\\)

%description
This module scans potential modules used by perl programs and returns a
hash reference.  Its keys are the module names as they appear in %%INC (e.g.
Test/More.pm).  The values are hash references.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness
Requires:       perl(AutoLoader)
Requires:       perl(autouse)
Requires:       perl(Carp)
Requires:       perl(if)
Requires:       perl(less)
Requires:       perl(Net::FTP)
# Optional tests:
%if %{with perl_Module_ScanDeps_enables_optional_tests}
Requires:       perl(Module::Pluggable)
%if !%{defined perl_bootstrap} && %{with perl_Module_ScanDeps_enables_prefork}
Requires:       perl(prefork)
%endif
%endif

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Module-ScanDeps-%{version}

# Help file to recognise the Perl scripts
for F in `find t -name *.t -o -name *.pl`; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*perl\b}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} %{buildroot}

# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
rm -f %{buildroot}%{_libexecdir}/%{name}/t/0-pod.t
perl -i -pe 's{ "-Mblib",}{}' %{buildroot}%{_libexecdir}/%{name}/t/19-autosplit.t
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

%check
%if !0%{?os2_version}
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
make test
%endif

%files
%license LICENSE
%doc AUTHORS Changes README
%{_bindir}/scandeps.pl
%{perl_vendorlib}/Module/
%{_mandir}/man1/scandeps.pl.1*
%if !0%{?os2_version}
%{_mandir}/man3/Module::ScanDeps.3pm*
%else
%{_mandir}/man3/Module.ScanDeps.3pm*
%endif

%files tests
%{_libexecdir}/%{name}

%changelog
* Tue Jul 30 2026  Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.37-1
- update to version 1.37
- resync with latest fedora spec

* Fri May 04 2018  Elbert Pol <elbert.pol@gmail.com> - 1.24-1
- initial rpm for OS2
