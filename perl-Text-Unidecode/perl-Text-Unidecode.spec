Name:           perl-Text-Unidecode
Version:        1.30
Release:        1%{?dist}
Summary:        US-ASCII transliterations of Unicode text
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Text-Unidecode
Source0:        https://cpan.metacpan.org/modules/by-module/Text/Text-Unidecode-%{version}.tar.gz
%if 0%{?os2_version}
Vendor:         bww bitwise works GmbH
%endif
BuildArch:      noarch
# Build
BuildRequires:  make
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# Runtime
BuildRequires:  perl(Exporter)
BuildRequires:  perl(integer)
BuildRequires:  perl(strict)
BuildRequires:  perl(utf8)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
# Tests only
BuildRequires:  perl(Test)
BuildRequires:  perl(Text::Wrap)

%description

Text::Unidecode provides a function, `unidecode(...)' that takes
Unicode data and tries to represent it in US-ASCII characters (i.e.,
the universally displayable characters between 0x00 and 0x7F). The
representation is almost always an attempt at *transliteration* -- i.e.,
conveying, in Roman letters, the pronunciation expressed by the text in
some other writing system.

%prep
%setup -q -n Text-Unidecode-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
%{_fixperms} %{buildroot}/*

%check
%if !0%{?os2_version}
make test
%endif

%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README TODO.txt ChangeLog
%{perl_vendorlib}/Text/
%{_mandir}/man3/*.3*

%changelog
* Tue Jul 30 2026 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.30-1
- initial version
