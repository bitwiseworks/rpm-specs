Name:           perl-Digest-HMAC
Version:        1.03
Release:        1%{?dist}
Summary:        Keyed-Hashing for Message Authentication
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Digest-HMAC/
Vendor:         bww bitwise works GmbH
Source0:        http://www.cpan.org/authors/id/G/GA/GAAS/Digest-HMAC-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl-generators
BuildRequires:  perl(Digest::MD5), perl(Digest::SHA1), perl(ExtUtils::MakeMaker)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
HMAC is used for message integrity checks between two parties that
share a secret key, and works in combination with some other Digest
algorithm, usually MD5 or SHA-1. The HMAC mechanism is described in
RFC 2104.

HMAC follow the common Digest:: interface, but the constructor takes
the secret key and the name of some other simple Digest:: as argument.


%prep
%setup -q -n Digest-HMAC-%{version} 


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}
make manifypods


%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*


%check
#make test


%files
%doc Changes README
%{perl_vendorlib}/Digest/
%{_mandir}/man3/*.3*


%changelog
* Fri Mar 02 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.03-1
- initial rpm
