Name:           perl-Mozilla-CA
# You do not need to back-port new version for list of certificates solely.
# They are taken from ca-certificates package instead per bug #738383.
Version:        20160104
Release:        1%{?dist}
Summary:        Mozilla's CA cert bundle in PEM format
License:        MPLv2.0
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Mozilla-CA/
Vendor:         bww bitwise works GmbH
Source0:        http://www.cpan.org/authors/id/A/AB/ABH/Mozilla-CA-%{version}.tar.gz
# Use CA bundle from ca-certificates package, bug #738383
Patch0:         Mozilla-CA-20160104-Redirect-to-ca-certificates-bundle.patch
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
#BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  sed
# Run-time:
BuildRequires:  ca-certificates
BuildRequires:  perl(strict)
BuildRequires:  perl(File::Spec)
# Tests:
BuildRequires:  perl(Test)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       ca-certificates

%description
Mozilla::CA provides a path to ca-certificates copy of Mozilla's bundle of
certificate authority certificates in a form that can be consumed by modules
and libraries based on OpenSSL.

%prep
%setup -q -n Mozilla-CA-%{version}
%patch0 -p1
# Remove bundled CA bundle for sure
rm lib/Mozilla/CA/cacert.pem
# Do not distribute Mozilla downloader, we take certificates from
# ca-certificates package
rm mk-ca-bundle.pl
sed -i '/^mk-ca-bundle.pl$/d' MANIFEST

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
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Thu Feb 22 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> - 20160104-1
- initial version
