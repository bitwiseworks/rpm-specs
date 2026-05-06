# Run optional test
%if ! (0%{?rhel}) && !0%{?os2_version}
%bcond_without perl_Pod_Parser_enables_optional_test
%else
%bcond_with perl_Pod_Parser_enables_optional_test
%endif

Name:           perl-Pod-Parser
Version:        1.67
Release:        2%{?dist}
Summary:        Basic perl modules for handling Plain Old Documentation (POD)
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Pod-Parser
%if 0%{?os2_version}
Vendor:         bww bitwise works GmbH
%endif
Source0:        https://cpan.metacpan.org/authors/id/M/MA/MAREKR/Pod-Parser-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.5.0
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(File::Spec) >= 0.82
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Find)
# Getopt::Long not used for tests
# Pod::Usage not used for tests
BuildRequires:  perl(strict)
# Symbol not used since perl 5.6
BuildRequires:  perl(vars)
# Tests:
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(FileHandle)
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::More) >= 0.6
# VMS::Filespec not used
%if %{with perl_Pod_Parser_enables_optional_test}
# Optional tests:
BuildRequires:  perl(IO::String)
BuildRequires:  perl(Pod::Checker) >= 1.40
%endif
Requires:       perl(Config)
# Circular dependency Pod::Usage <-> Pod::Select

%description
This software distribution contains the packages for using Perl5 POD (Plain
Old Documentation). See the "perlpod" and "perlsyn" manual pages from your
Perl5 distribution for more information about POD.

%prep
%setup -q -n Pod-Parser-%{version}
find -type f -exec chmod -x {} +
chmod +x scripts/*
for F in ANNOUNCE CHANGES README TODO; do
    tr -d '\r' < "$F" > "${F}.unix"
    touch -r "$F" "${F}.unix"
    mv "${F}.unix" "$F"
done

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}
%if 0%{?os2_version}
make manifypods
%endif

%install
%{make_install}
%{_fixperms} %{buildroot}/*

%check
%if !0%{?os2_version}
make test
%endif

%files
%doc ANNOUNCE CHANGES README TODO
%{_bindir}/podselect
%{perl_vendorlib}/*
%{_mandir}/man1/*
%{_mandir}/man3/*

%changelog
* Wed May 06 2026 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.67-2
- rebuild with perl 5.42

* Fri Apr 24 2026 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.67-1
- perl > 5.16 removed this package, so break it out like fedora did
- initial version
