# Utilize Business::ISBN that needs gd library
%bcond_with perl_URI_enables_Business_ISBN

Name:           perl-URI
Version:        1.71
Release:        1%{?dist}
Summary:        A Perl module implementing URI parsing and manipulation
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/URI/
Vendor:         bww bitwise works GmbH
Source0:        http://www.cpan.org/authors/id/E/ET/ETHER/URI-%{version}.tar.gz
BuildArch:      noarch
# Module Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
#BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(utf8)
# Module Runtime
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Encode)
BuildRequires:  perl(Exporter) >= 5.57
BuildRequires:  perl(integer)
BuildRequires:  perl(MIME::Base64) >= 2
BuildRequires:  perl(Net::Domain)
BuildRequires:  perl(overload)
BuildRequires:  perl(parent)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Test Suite
BuildRequires:  perl(Config)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(Storable)
BuildRequires:  perl(Test)
#BuildRequires:  perl(Test::More) >= 0.96
# Runtime
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Cwd)
Requires:       perl(Data::Dumper)
Requires:       perl(Encode)
Requires:       perl(MIME::Base64) >= 2
Requires:       perl(Net::Domain)

# Optional Functionality
%if %{with perl_URI_enables_Business_ISBN}
# Business::ISBN pulls in gd and X libraries for barcode support, hence this soft dependency (#1380152)
# Business::ISBN  Test::Pod  Pod::Simple  HTML::Entities (HTML::Parser)  URI
%if 0%{!?perl_bootstrap:1}
BuildRequires:  perl(Business::ISBN)
%endif
Suggests:       perl(Business::ISBN)
%endif

%description
This module implements the URI class. Objects of this class represent
"Uniform Resource Identifier references" as specified in RFC 2396 (and
updated by RFC 2732).

%prep
%setup -q -n URI-%{version}
chmod -c 644 uri-test

%build
perl Makefile.PL INSTALLDIRS=perl NO_PACKLIST=true
make %{?_smp_mflags}
make manifypods

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
%{_fixperms} %{buildroot}

%check
#make test

%files
%license LICENSE
%doc Changes README uri-test
%{perl_privlib}/URI.pm
%{perl_privlib}/URI/
%{_mandir}/man3/URI.3*
%{_mandir}/man3/URI.Escape.3*
%{_mandir}/man3/URI.Heuristic.3*
%{_mandir}/man3/URI.QueryParam.3*
%{_mandir}/man3/URI.Split.3*
%{_mandir}/man3/URI.URL.3*
%{_mandir}/man3/URI.WithBase.3*
%{_mandir}/man3/URI._punycode.3*
%{_mandir}/man3/URI.data.3*
%{_mandir}/man3/URI.file.3*
%{_mandir}/man3/URI.ldap.3*

%changelog
* Mon May 08 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.71-1
- initial version
