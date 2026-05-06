Name:           perl-Devel-Symdump
Epoch:          1
Version:        2.18
Release:        1%{?dist}
Summary:        A Perl module for inspecting Perl's symbol table
Group:          Development/Libraries
License:        GPL+ or Artistic
Vendor:         bww bitwise works GmbH 
Url:            http://search.cpan.org/dist/Devel-Symdump/
Source0:        http://www.cpan.org/authors/id/A/AN/ANDK/Devel-Symdump-%{version}.tar.gz
BuildArch:      noarch
# Module Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
#BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
# Module Runtime
BuildRequires:  perl(B)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(constant)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
# Test Suite
BuildRequires:  perl(English)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::Harness) >= 3.04
BuildRequires:  perl(Test::More)
BuildRequires:  perl(warnings)
# Author Tests
#%if 0%{!?perl_bootstrap:1}
# Compress::Zlib (IO-Compress) ⇒ Test::NoWarnings ⇒ Devel::StackTrace ⇒
#   Test::NoTabs ⇒ Test::Pod::Coverage ⇒ Pod::Coverage ⇒ Devel::Symdump
#BuildRequires:  perl(Compress::Zlib)
#BuildRequires:  perl(Test::Pod) >= 1.00
# Test::Pod::Coverage ⇒ Pod::Coverage ⇒ Devel::Symdump
#BuildRequires:  perl(Test::Pod::Coverage)
#%endif
# Runtime
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(B)

%description
The perl module Devel::Symdump provides a convenient way to inspect
perl's symbol table and the class hierarchy within a running program.

%prep
%setup -q -n Devel-Symdump-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}
make manifypods

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

%check
#make test %{!?perl_bootstrap:AUTHOR_TEST=1}

%files
%doc Changes README
%{perl_vendorlib}/Devel/
%{_mandir}/man3/*.3*

%changelog
* Wed Mar 07 2018 Elbert Pol <elbert.pol@gmail.com> - 2.18-1
-  initial rpm for OS2
