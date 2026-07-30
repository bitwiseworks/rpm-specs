Name:		perl-File-Remove
Version:	1.61
Release:	1%{?dist}
Summary:	Convenience module for removing files and directories
License:	GPL-1.0-or-later OR Artistic-1.0-Perl

URL:		https://metacpan.org/release/File-Remove
Source0:	https://cpan.metacpan.org/authors/id/S/SH/SHLOMIF/File-Remove-%{version}.tar.gz
%if 0%{?os2_version}
Vendor:         bww bitwise works GmbH
%endif

BuildRequires:	%{__perl}
BuildRequires:	%{__make}

BuildRequires:	perl-generators
BuildRequires:	perl(blib)
BuildRequires:	perl(constant)
BuildRequires:	perl(Cwd) >= 3.29
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(File::Copy)
BuildRequires:	perl(File::Glob)
BuildRequires:	perl(File::Path)
BuildRequires:	perl(File::Spec) >= 3.29
BuildRequires:	perl(File::Spec::Functions)
BuildRequires:	perl(File::Temp)
BuildRequires:	perl(IO::Handle)
BuildRequires:	perl(IPC::Open3)
BuildRequires:	perl(strict)
BuildRequires:	perl(Test::More) >= 0.42
BuildRequires:	perl(vars)
BuildRequires:	perl(warnings)

BuildArch:	noarch

%description
%{summary}

%prep
%setup -q -n File-Remove-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install} DESTDIR="$RPM_BUILD_ROOT"
%{_fixperms} "$RPM_BUILD_ROOT"/*

%check
%if !0%{?os2_version}
%{__make} test
%endif

%files
%doc Changes README
%license LICENSE
%{perl_vendorlib}/File
%{_mandir}/man3/*

%changelog
* Tue Jul 30 2026  Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.61-1
- update to version 1.61
- resync with latest fedora spec

* Fri May 04 2018  Elbert Pol <elbert.pol@gmail.com> - 1.57-1
- initial rpm for OS2
