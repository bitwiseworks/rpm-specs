Name:           perl-Module-Install
Version:        1.19
Release:        1%{?dist}
Summary:        Standalone, extensible Perl module installer
License:        GPL+ or Artistic
Vendor:         bww bitwise works GmbH
URL:            http://search.cpan.org/dist/Module-Install/
Source0:        http://search.cpan.org/CPAN/authors/id/E/ET/ETHER/Module-Install-%{version}.tar.gz
BuildArch:      noarch
# Build
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
#BuildRequires:  perl-interpreter
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
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.63
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
# XXX: BuildRequires:  perl(Module::ScanDeps) >= 1.09
# XXX: BuildRequires:  perl(Net::FTP)
# XXX: BuildRequires:  perl(PAR::Dist) >= 0.29
BuildRequires:  perl(Parse::CPAN::Meta) >= 1.4413
# XXX: BuildRequires:  perl(Socket)
BuildRequires:  perl(vars)
BuildRequires:  perl(YAML::Tiny) >= 1.38
# Tests only
#BuildRequires:  perl(autodie)
#BuildRequires:  perl(ExtUtils::MM)
#BuildRequires:  perl(Symbol)
#BuildRequires:  perl(Test::More)
# Optional tests only
#%if 0%{!?perl_bootstrap:1}
#BuildRequires:  perl(Module::Install::AuthorTests)
#BuildRequires:  perl(Module::Install::ExtraTests) >= 0.007
#%endif
BuildRequires:  perl(utf8)
Requires:       perl(:MODULE_COMPAT_%(eval "$(perl -V:version)"; echo $version))
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


%description
Module::Install is a package for writing installers for CPAN (or CPAN-like)
distributions that are clean, simple, minimalist, act in a strictly correct
manner with ExtUtils::MakeMaker, and will run on any Perl installation
version 5.005 or newer.

%prep
%setup -q -n Module-Install-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}
make manifypods

%install
make pure_install DESTDIR=%{buildroot}
rm -f %{buildroot}/blib/lib/auto/share/dist/Module-Install/dist_file.txt
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} %{buildroot}/*

%check
#make test

%files
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Thu May 03 2018  Elbert Pol <elbert.pol@gmail.com> - 1.19-1
-  initial rpm for OS2
