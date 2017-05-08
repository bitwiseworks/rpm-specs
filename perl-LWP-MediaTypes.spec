# Use system-wide mailcap database
%bcond_with perl_LWP_MediaTypes_enables_mailcap

Name:           perl-LWP-MediaTypes
Version:        6.02
Release:        1%{?dist}
Summary:        Guess media type for a file or a URL
License:        (GPL+ or Artistic) and Public Domain
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/LWP-MediaTypes/
Vendor:         bww bitwise works GmbH
Source0:        http://www.cpan.org/authors/id/G/GA/GAAS/LWP-MediaTypes-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl-generators
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Basename)
# Tests only:
BuildRequires:  perl(Test)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(File::Basename)
%if %{with perl_LWP_MediaTypes_enables_mailcap}
Requires:       mailcap
%endif
Conflicts:      perl-libwww-perl < 6

%description
This module provides functions for handling media (also known as MIME)
types and encodings. The mapping from file extensions to media types is
defined by the media.types file. If the ~/.media.types file exists it is
used instead. For backwards compatibility we will also look for
~/.mime.types.

%prep
%setup -q -n LWP-MediaTypes-%{version}
%if %{with perl_LWP_MediaTypes_enables_mailcap}
# Use system-wide mailcap database
sed -i -e '/my @priv_files = ();/ s|()|("%{_sysconfdir}/mime.types")|' \
    lib/LWP/MediaTypes.pm
%endif

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}
make manifypods

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
%{_fixperms} %{buildroot}/*

%check
#make test

%files
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Mon May 08 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> - 6.02-1
- initial version
