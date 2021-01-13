Name:           perl-Scalar-List-Utils
Epoch:          3
Version:        1.49
Release:        2%{?dist}
Summary:        A selection of general-utility scalar and list subroutines
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Scalar-List-Utils/
Vendor:         bww bitwise works GmbH
Source0:        http://search.cpan.org/CPAN/authors/id/P/PE/PEVANS/Scalar-List-Utils-%{version}.tar.gz
# Build
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
#BuildRequires:  perl-interpreter
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Runtime
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(XSLoader)
# Tests only
BuildRequires:  perl(B::Deparse)
BuildRequires:  perl(base)
BuildRequires:  perl(constant)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(Math::BigInt)
BuildRequires:  perl(overload)
BuildRequires:  perl(Symbol)
#BuildRequires:  perl(Sub::Util)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(threads)
BuildRequires:  perl(threads::shared)
BuildRequires:  perl(Tie::Handle)
BuildRequires:  perl(Tie::Scalar)
BuildRequires:  perl(Tie::StdScalar)
BuildRequires:  perl(vars)
Requires:       perl(:MODULE_COMPAT_%(eval "$(perl -V:version)"; echo $version))
Requires:       perl(Carp)

%{?perl_default_filter}

%description
This package contains a selection of subroutines that people have expressed
would be nice to have in the perl core, but the usage would not really be
high enough to warrant the use of a keyword, and the size so small such
that being individual extensions would be wasteful.

%prep
%setup -q -n Scalar-List-Utils-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}" NO_PACKLIST=1
make manifypods
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name '*.bs' -size 0 -delete
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} %{buildroot}/*

%check
#make test

%files
%doc Changes README
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/List*
%{perl_vendorarch}/Scalar*
%{perl_vendorarch}/Sub*
%{_mandir}/man3/*

%changelog
* Wed Jan 13 2021 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.49-2
- rebuilt with latest tools, fixes a crash

* Thu Feb 22 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.49-1
- initial version
