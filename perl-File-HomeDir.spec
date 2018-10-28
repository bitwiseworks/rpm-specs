Name:           perl-File-HomeDir
Version:        1.004
Release:        3%{?dist}
Summary:        Find your home and other directories on any platform
License:        GPL+ or Artistic
URL:            https://metacpan.org/release/File-HomeDir
Source0:        https://cpan.metacpan.org/authors/id/R/RE/REHSACK/File-HomeDir-%{version}.zip
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
#BuildRequires:  perl-interpreter
#BuildRequires:  perl(:VERSION) >= 5.5.3
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker)
# POSIX not used on Linux
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Cwd) >= 3.12
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Path) >= 2.01
BuildRequires:  perl(File::Spec) >= 3.12
BuildRequires:  perl(File::Temp) >= 0.19
BuildRequires:  perl(File::Which) >= 0.05
# Mac::Files not used on Linux
# Mac::SystemDirectory not used on Linux
BuildRequires:  perl(vars)
# Win32 not used on Linux
# Tests:
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(Test::More) >= 0.90
# Dependencies:
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Cwd) >= 3.12
Requires:       perl(File::Path) >= 2.01
Requires:       perl(File::Spec) >= 3.12
Requires:       perl(File::Temp) >= 0.19
Requires:       perl(File::Which) >= 0.05

# Remove unwanted and under-specified dependencies
%global __requires_exclude perl\\(Cwd\\)|perl\\(File::Path\\)|perl\\(File::Spec\\)|perl\\(File::Temp\\)|perl\\(File::Which\\)|perl\\(Mac::|perl\\(Win32

%description
File::HomeDir is a module for locating the directories that are "owned"
by a user (typically your user) and to solve the various issues that
arise trying to find them consistently across a wide variety of
platforms.

%prep
%setup -q -n File-HomeDir-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
make %{?_smp_mflags}
make manifypods

%install
make install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -exec rm -f {} ';'
%{_fixperms} -c %{buildroot}

%check
#make test

%files
%license LICENSE
%doc Changes README.md
%{perl_vendorlib}/File/
%{_mandir}/man3/File.HomeDir.3*
%{_mandir}/man3/File.HomeDir.Darwin.3*
%{_mandir}/man3/File.HomeDir.Darwin.Carbon.3*
%{_mandir}/man3/File.HomeDir.Darwin.Cocoa.3*
%{_mandir}/man3/File.HomeDir.Driver.3*
%{_mandir}/man3/File.HomeDir.FreeDesktop.3*
%{_mandir}/man3/File.HomeDir.MacOS9.3*
%{_mandir}/man3/File.HomeDir.Test.3*
%{_mandir}/man3/File.HomeDir.Unix.3*
%{_mandir}/man3/File.HomeDir.Windows.3*

%changelog
* Sun Oct 28 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.004-1
- first os2 rpm version
