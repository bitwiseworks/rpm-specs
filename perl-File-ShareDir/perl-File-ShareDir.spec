# Enable optional dependencies
%if !0%{?os2_version}
%bcond_without perl_File_ShareDir_enables_optional_deps
%else
%bcond_with perl_File_ShareDir_enables_optional_deps
%endif

Name:           perl-File-ShareDir
Version:        1.118
Release:        1%{?dist}
Summary:        Locate per-dist and per-module shared files
# other files:              GPL+ or Artistic
## not in binary packages
# inc/latest/private.pm:    ASL 2.0
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/File-ShareDir
Source0:        https://cpan.metacpan.org/authors/id/R/RE/REHSACK/File-ShareDir-%{version}.tar.gz
%if 0%{?os2_version}
Vendor:         bww bitwise works GmbH
%endif
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(File::ShareDir::Install)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(IO::Dir)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(lib)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
# Run-time
BuildRequires:  perl(base)
BuildRequires:  perl(Class::Inspector) >= 1.12
BuildRequires:  perl(constant)
# Optional run-time
%if %{with perl_File_ShareDir_enables_optional_deps}
BuildRequires:  perl(List::MoreUtils) >= 0.428
BuildRequires:  perl(Params::Util) >= 1.07
%endif
# Tests
BuildRequires:  perl(Cwd)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(parent)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Test::More) >= 0.47
# Optional tests
BuildRequires:  perl(CPAN::Meta)
Requires:       perl(Class::Inspector) >= 1.12
%if %{with perl_File_ShareDir_enables_optional_deps}
Recommends:     perl(List::MoreUtils) >= 0.428
Recommends:     perl(Params::Util) >= 1.07
%endif

%{?perl_default_filter}
%global __requires_exclude %{?__requires_exclude}|perl\\(Class::Inspector\\)$

%description
The intent of File::ShareDir is to provide a companion to Class::Inspector
and File::HomeDir, modules that take a process that is well-known by
advanced Perl developers but gets a little tricky, and make it more
available to the larger Perl community.

%prep
%setup -q -n File-ShareDir-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}
%if 0%{?os2_version}
make manifypods
%endif

%install
%{make_install}
%{_fixperms} %{buildroot}/*
chmod 644 share/sample.txt
chmod 644 share/subdir/sample.txt
rm -rf %{buildroot}/blib/lib/auto/share/dist/File-ShareDir/
rm -rf %{buildroot}/blib/lib/auto/share/module/File-ShareDir/test_file.txt

%check
%if !0%{?os2_version}
make test AUTOMATED_TESTING=1
%endif

%files
%license LICENSE
%doc Changes README.md
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Fri May 08 2026 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.118-1
- initial rpm
