Name:           perl-Digest-SHA1
Version:        2.13
Release:        1%{?dist}
Summary:        Digest-SHA1 Perl module

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Digest-SHA1/
Vendor:         bww bitwise works GmbH
Source0:        http://search.cpan.org/CPAN/authors/id/G/GA/GAAS/Digest-SHA1-%{version}.tar.gz
BuildRequires:  findutils
BuildRequires:  gcc
#BuildRequires:  glibc-common
BuildRequires:  make
#BuildRequires:  perl-interpreter
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
# Run-time
BuildRequires:  perl(Digest::base)
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
# Tests
BuildRequires:  perl(Test)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Recommends:     perl(Digest::base)

%description
The Digest::SHA1 module allows you to use the NIST SHA-1 message
digest algorithm from within Perl programs. The algorithm takes as
input a message of arbitrary length and produces as output a 160-bit
"fingerprint" or "message digest" of the input.

The Digest::SHA1 module provide a procedural interface for simple use,
as well as an object oriented interface that can handle messages of
arbitrary length and which can read files directly.

A binary digest will be 20 bytes long. A hex digest will be 40
characters long. A base64 digest will be 27 characters long.


%prep
%setup -q -n Digest-SHA1-%{version} 
#f=Changes ; iconv -f iso-8859-1 -t utf-8 $f > $f.utf8 ; mv $f.utf8 $f

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS" NO_PACKLIST=1
make %{?_smp_mflags}
make manifypods

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name '*.bs' -a -size 0 -delete
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
chmod -R u+w $RPM_BUILD_ROOT/*

%check
#make test

%files
%doc Changes README fip180-1.gif fip180-1.html
%{perl_vendorarch}/Digest/
%{perl_vendorarch}/auto/Digest/
%{_mandir}/man3/*.3*

%changelog
* Fri Mar 02 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.13-1
- initial rpm
