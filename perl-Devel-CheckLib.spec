Name:           perl-Devel-CheckLib
Version:        1.11
Release:        1%{?dist}
Summary:        Check that a library is available

License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Devel-CheckLib/
Vendor:         bww bitwise works GmbH
Source0:        http://www.cpan.org/modules/by-module/Devel/Devel-CheckLib-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  make
#BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
# Run-time:
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Temp) >= 0.16
BuildRequires:  perl(Text::ParseWords)
# Tests:
BuildRequires:  perl(Cwd)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(IO::File)
#BuildRequires:  perl(IO::CaptureOutput) >= 1.0801
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::More) >= 0.62
# Optional tests
#BuildRequires:  perl(Mock::Config)

Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
Devel::CheckLib is a perl module that checks whether a particular C library
and its headers are available.

%prep
%setup -q -n Devel-CheckLib-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}
make manifypods

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
%{_fixperms} $RPM_BUILD_ROOT/*

%check
#make test

%files
%doc CHANGES README TODO
%{_bindir}/*
%{perl_vendorlib}/Devel*
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3*

%changelog
* Wed Feb 21 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.11-1
- initial rpm
