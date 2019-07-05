Name:           perl-IO-HTML
Version:        1.001
Release:        1%{?dist}
Summary:        Open an HTML file with automatic character set detection
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/IO-HTML/
Vendor:         bww bitwise works GmbH
Source0:        http://www.cpan.org/authors/id/C/CJ/CJM/IO-HTML-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.30
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(Encode) >= 2.10
BuildRequires:  perl(Exporter) >= 5.57
# Tests:
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(Scalar::Util)
#BuildRequires:  perl(Test::More) >= 0.88
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
IO::HTML provides an easy way to open a file containing HTML while
automatically determining its encoding. It uses the HTML5 encoding sniffing
algorithm specified in section 8.2.2.1 of the draft standard.

%prep
%setup -q -n IO-HTML-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}
make manifypods

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
%{_fixperms} $RPM_BUILD_ROOT/*

%check
#make test

%files
%doc Changes LICENSE README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Mon May 08 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.001-1
- initial version
