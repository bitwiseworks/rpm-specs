Name:           perl-File-ShareDir-Install
Version:        0.14
Release:        1%{?dist}
Summary:        Install shared files
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/File-ShareDir-Install
Source0:        https://cpan.metacpan.org/modules/by-module/File/File-ShareDir-Install-%{version}.tar.gz
%if 0%{?os2_version}
Vendor:         bww bitwise works GmbH
%endif
BuildArch:      noarch
# Module Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker)
# Module Runtime
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(IO::Dir)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Test Suite
BuildRequires:  perl(Config)
BuildRequires:  perl(CPAN::Meta::YAML)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(Test::More)
# Dependencies
# (none)

%description
File::ShareDir::Install allows you to install read-only data files from a
distribution. It is a companion module to File::ShareDir, which allows you
to locate these files after installation.

%prep
%setup -q -n File-ShareDir-Install-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

%check
%if !0%{?os2_version}
make test
%endif

%files
%license LICENSE
%doc Changes CONTRIBUTING README
%{perl_vendorlib}/File/
%if !0%{?os2_version}
%{_mandir}/man3/File::ShareDir::Install.3*
%else
%{_mandir}/man3/File.ShareDir.Install.3*
%endif

%changelog
* Fri May 08 2026 Silvan Scherrer <silvan.scherrer@aroa.ch> 0.14-1
- initial rpm
