# Run optional test
%if ! (0%{?rhel} || 0%{?os2_version})
%bcond_without perl_Module_Install_enables_optional_test
%else
%bcond_with perl_Module_Install_enables_optional_test
%endif

Name:           perl-Module-Install
Version:        1.21
Release:        1%{?dist}
Summary:        Standalone, extensible Perl module installer
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Module-Install
%if 0%{?os2_version}
Vendor:         bww bitwise works GmbH
%endif
Source0:        https://cpan.metacpan.org/authors/id/E/ET/ETHER/Module-Install-%{version}.tar.gz
%if !0%{?os2_version}
# Fix a crash when looking up 5.010 Perl core modules, CPAN RT#71565, proposed
# to upstream <https://github.com/Perl-Toolchain-Gang/Module-Install/pull/64>
Patch0:         Module-Install-1.19-Fix-Perl-version-lookup-with-Module-CoreList.patch
%endif
BuildArch:      noarch
# Build
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(lib)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Runtime
# XXX: BuildRequires:  perl(Archive::Zip) >= 1.37
# XXX: BuildRequires:  perl(Carp)
# XXX: BuildRequires:  perl(CPAN)
# XXX: BuildRequires:  perl(CPANPLUS::Backend)
BuildRequires:  perl(Config)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Devel::PPPort) >= 3.16
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(ExtUtils::Manifest)
BuildRequires:  perl(ExtUtils::MM_Unix)
# XXX: BuildRequires:  perl(ExtUtils::MM_Cygwin)
# XXX: BuildRequires:  perl(ExtUtils::MM_Win32)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Find)
# XXX: BuildRequires:  perl(File::HomeDir) >= 1
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Remove) >= 1.42
BuildRequires:  perl(File::Spec) >= 3.28
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(FileHandle)
BuildRequires:  perl(FindBin)
# XXX: BuildRequires:  perl(JSON) >= 2.9
# XXX: BuildRequires:  perl(LWP::Simple) >= 6.00
# XXX: BuildRequires:  perl(Module::Build) >= 0.29
BuildRequires:  perl(Module::CoreList) >= 2.17
BuildRequires:  perl(Module::ScanDeps) >= 1.09
# XXX: BuildRequires:  perl(Net::FTP)
# XXX: BuildRequires:  perl(PAR::Dist) >= 0.29
BuildRequires:  perl(Parse::CPAN::Meta) >= 1.4413
# XXX: BuildRequires:  perl(Socket)
BuildRequires:  perl(vars)
BuildRequires:  perl(YAML::Tiny) >= 1.38
# Tests only
BuildRequires:  perl(autodie)
BuildRequires:  perl(ExtUtils::MM)
BuildRequires:  perl(Symbol)
BuildRequires:  perl(Test::More)
# Optional tests only
%if %{with perl_Module_Install_enables_optional_test} && 0%{!?perl_bootstrap:1}
BuildRequires:  perl(Module::Install::AuthorTests)
BuildRequires:  perl(Module::Install::ExtraTests) >= 0.007
%endif
BuildRequires:  perl(utf8)
Requires:       perl(Archive::Zip) >= 1.37
Requires:       perl(Carp)
Requires:       perl(CPAN)
# CPANPLUS is preferred over CPAN, but it's in a build cycle
# (perl-Module-Install → perl-CPANPLUS → perl-DBIx-Simple → perl-SQL-Abstract
# → perl-Module-Install), not necessary if all dependencies are retrived
# from an RPM repository, and upstream still considered as an option. Thus do
# not hard require the CPANPLUS.
Recommends:     perl(CPANPLUS::Backend)
Requires:       perl(Devel::PPPort) >= 3.16
Requires:       perl(ExtUtils::MakeMaker) >= 6.59
# Unused: Requires:       perl(ExtUtils::MM_Cygwin)
Requires:       perl(ExtUtils::MM_Unix)
# Unused: Requires:       perl(ExtUtils::MM_Win32)
# Unneeded: Requires:       perl(File::HomeDir) >= 1
Requires:       perl(File::Remove) >= 1.42
Requires:       perl(File::Spec) >= 3.28
Requires:       perl(File::Temp)
Requires:       perl(FileHandle)
Requires:       perl(FindBin)
# Optional: Requires:       perl(JSON) >= 2.9
# Optional: Requires:       perl(LWP::Simple) >= 6.00
Requires:       perl(Module::Build) >= 0.29
Requires:       perl(Module::CoreList) >= 2.17
Requires:       perl(Module::ScanDeps) >= 1.09
# Optional: Requires:       perl(Net::FTP)
# Optional: Requires:       perl(PAR::Dist) >= 0.29
Requires:       perl(Parse::CPAN::Meta) >= 1.4413
Requires:       perl(Socket)
Requires:       perl(YAML::Tiny) >= 1.38

%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Devel::PPPort\\)$
%global __requires_exclude %__requires_exclude|^perl\\(ExtUtils::MakeMaker\\)$
%global __requires_exclude %__requires_exclude|^perl\\(File::Remove\\)$
%global __requires_exclude %__requires_exclude|^perl\\(File::Spec\\)$
%global __requires_exclude %__requires_exclude|^perl\\(YAML::Tiny\\)$

# Filter modules bundled for tests
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}^%{_libexecdir}
%global __requires_exclude %__requires_exclude|^perl\\(MyTest\\)$

%description
Module::Install is a package for writing installers for CPAN (or CPAN-like)
distributions that are clean, simple, minimalist, act in a strictly correct
manner with ExtUtils::MakeMaker, and will run on any Perl installation
version 5.005 or newer.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness
%if %{with perl_Module_Install_enables_optional_test} && 0%{!?perl_bootstrap:1}
Requires:       perl(Module::Install::AuthorTests)
Requires:       perl(Module::Install::ExtraTests) >= 0.007
%endif
Requires:       perl(utf8)

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Module-Install-%{version}
%if !0%{?os2_version}
%patch -P0 -p1
%endif
# Help generators to recognize Perl scripts
for F in `find t -name *.t`; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*perl\b}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
rm -f %{buildroot}/blib/lib/auto/share/dist/Module-Install/dist_file.txt
%{_fixperms} %{buildroot}/*

# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
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
%doc Changes README
%{perl_vendorlib}/Module*
%{perl_vendorlib}/inc*
%if !0%{?os2_version}
%{_mandir}/man3/Module::*
%{_mandir}/man3/inc::*
%else
%{_mandir}/man3/Module.*
%{_mandir}/man3/inc.*
%endif

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 31 2026  Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.21-1
- update to version 1.21
- resync with latest fedora spec

* Thu May 03 2018  Elbert Pol <elbert.pol@gmail.com> - 1.19-1
-  initial rpm for OS2
