# Run prefork optional test
#%{bcond_without perl_Module_ScanDeps_enables_prefork}

Name:           perl-Module-ScanDeps
Summary:        Recursively scan Perl code for dependencies
Version:        1.24
Release:        1%{?dist}
License:        GPL+ or Artistic
Vendor:         bww bitwise works GmbH
Source0:        http://search.cpan.org/CPAN/authors/id/R/RS/RSCHUPP/Module-ScanDeps-%{version}.tar.gz 
URL:            http://search.cpan.org/dist/Module-ScanDeps/
BuildArch:      noarch
BuildRequires:  make
#BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.63
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
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(FileHandle)
# Getopt::Long not used by tests
BuildRequires:  perl(Module::Metadata)
# Storable is optional and not used by tests
# subs not used by tests
# Text::ParseWords not used by tests
BuildRequires:  perl(vars)
BuildRequires:  perl(version)
# VMS::Filespec never used
# Tests:
#BuildRequires:  perl(autouse)
#BuildRequires:  perl(if)
#BuildRequires:  perl(lib)
#BuildRequires:  perl(Test::More)
#BuildRequires:  perl(Test::Requires)
# Optional tests:
#BuildRequires:  perl(Module::Pluggable)
#%if !%{defined perl_bootstrap} && %{with perl_Module_ScanDeps_enables_prefork}
# Cycle: perl-Module-ScanDeps → perl-prefork → perl-Perl-MinimumVersion
# → perl-Perl-Critic → perl-Pod-Spell → perl-File-ShareDir-ProjectDistDir
# → perl-Path-Tiny → perl-Unicode-UTF8 → perl-Module-Install
# → perl-Module-ScanDeps
#BuildRequires:  perl(prefork)
#%endif
#BuildRequires:  perl(Test::Pod) >= 1.00
#Requires:       perl(:MODULE_COMPAT_%(eval "$(perl -V:version)"; echo $version))
#Requires:       perl(B)
#Requires:       perl(DynaLoader)
#Requires:       perl(Data::Dumper)
#Requires:       perl(Encode)
#Requires:       perl(File::Find)
#Requires:       perl(Text::ParseWords)
#Recommends:     perl(Digest::MD5)
#Recommends:     perl(Storable)
Suggests:       perl(CPANPLUS::Backend)

%description
This module scans potential modules used by perl programs and returns a
hash reference.  Its keys are the module names as they appear in %%INC (e.g.
Test/More.pm).  The values are hash references.

%prep
%setup -q -n Module-ScanDeps-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}
make manifypods

%install
make pure_install DESTDIR=%{buildroot}
%{_fixperms} %{buildroot}
find %{buildroot} -type f -name .packlist -delete

%check
#make test

%files
%license LICENSE
%doc AUTHORS Changes README
%{_bindir}/scandeps.pl
%{perl_vendorlib}/Module/
%{_mandir}/man1/scandeps.pl.1*
#%{_mandir}/man3/Module::ScanDeps.3pm*
%{_mandir}/man3/*.3pm*

%changelog
* Fri May 04 2018  Elbert Pol <elbert.pol@gmail.com> - 1.24-1
-  initial rpm for OS2
