%{bcond_with perl_Net_SSLeay_enables_optional_test}

# Provides/Requires filtering is different from rpm 4.9 onwards
%global rpm49 %(rpm --version | perl -p -e 's/^.* (\\d+)\\.(\\d+).*/sprintf("%d.%03d",$1,$2) ge 4.009 ? 1 : 0/e' 2>/dev/null || echo 0)

Name:		perl-Net-SSLeay
Version:	1.84
Release:	1%{?dist}
Summary:	Perl extension for using OpenSSL
License:	Artistic 2.0
URL:		http://search.cpan.org/dist/Net-SSLeay/
Vendor:         bww bitwise works GmbH
Source0:	http://search.cpan.org/CPAN/authors/id/M/MI/MIKEM/Net-SSLeay-%{version}.tar.gz
# =========== Module Build ===========================
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	gcc
BuildRequires:	make
BuildRequires:	openssl
BuildRequires:	openssl-devel
BuildRequires:	perl-devel
BuildRequires:	perl-generators
#BuildRequires:	perl-interpreter
BuildRequires:	perl(Cwd)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(File::Path)
BuildRequires:	perl(lib)
# =========== Module Runtime =========================
BuildRequires:	perl(AutoLoader)
BuildRequires:	perl(Carp)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(MIME::Base64)
BuildRequires:	perl(Socket)
BuildRequires:	perl(XSLoader)
# =========== Test Suite =============================
BuildRequires:	perl(Config)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(HTTP::Tiny)
BuildRequires:	perl(IO::Handle)
BuildRequires:	perl(IO::Socket::INET)
BuildRequires:	perl(strict)
BuildRequires:	perl(Test::More) >= 0.61
BuildRequires:	perl(threads)
BuildRequires:	perl(warnings)
# =========== Optional Test Suite ====================
%if %{with perl_Net_SSLeay_enables_optional_test}
BuildRequires:	perl(Test::Exception)
BuildRequires:	perl(Test::NoWarnings)
BuildRequires:	perl(Test::Pod) >= 1.0
BuildRequires:	perl(Test::Warn)
%endif
# =========== Module Runtime =========================
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	perl(MIME::Base64)
Requires:	perl(XSLoader)

# Don't "provide" private Perl libs or the redundant unversioned perl(Net::SSLeay) provide
%global __provides_exclude ^(perl\\(Net::SSLeay\\)$|SSLeay\\.so)

%description
This module offers some high level convenience functions for accessing
web pages on SSL servers (for symmetry, same API is offered for
accessing http servers, too), a sslcat() function for writing your own
clients, and finally access to the SSL API of SSLeay/OpenSSL package
so you can write servers or clients for more complicated applications.

%prep
%setup -q -n Net-SSLeay-%{version}

# Fix permissions in examples to avoid bogus doc-file dependencies
chmod -c 644 examples/*

# Remove redundant unversioned provide if we don't have rpm 4.9 or later
%if ! %{rpm49}
%global provfilt /bin/sh -c "%{__perl_provides} | grep -Fvx 'perl(Net::SSLeay)'"
%global __perl_provides %{provfilt}
%endif

%build
PERL_MM_USE_DEFAULT=1 perl Makefile.PL \
	INSTALLDIRS=vendor \
	OPTIMIZE="%{optflags}"
make %{?_smp_mflags}
make manifypods

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name '*.bs' -empty -delete
%{_fixperms} -c %{buildroot}

# Remove script we don't want packaged
rm -f %{buildroot}%{perl_vendorarch}/Net/ptrtstrun.pl

%check
#make test

# Check for https://bugzilla.redhat.com/show_bug.cgi?id=1222521
#perl -Iblib/{arch,lib} -MNet::SSLeay -e 'Net::SSLeay::CTX_v3_new()'

%files
%if 0%{?_licensedir:1}
%license LICENSE
%else
%doc LICENSE
%endif
%doc Changes Credits QuickRef README examples/
%{perl_vendorarch}/auto/Net/
%dir %{perl_vendorarch}/Net/
%{perl_vendorarch}/Net/SSLeay/
%{perl_vendorarch}/Net/SSLeay.pm
%doc %{perl_vendorarch}/Net/SSLeay.pod
%{_mandir}/man3/Net.SSLeay.3*
%{_mandir}/man3/Net.SSLeay.Handle.3*

%changelog
* Fri Feb 23 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.84-1
- initial version
