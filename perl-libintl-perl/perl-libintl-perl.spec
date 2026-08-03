Summary:        Internationalization library for Perl, compatible with gettext
Name:           perl-libintl-perl
Version:        1.37
Release:        1%{?dist}
# gettext_xs/gettext_xs.pm:     GPL-3.0-or-later
# gettext_xs/Makefile.PL:       LGPL-2.0-or-later
# lib/Locale/gettext_xs.pod:    LGPL-2.0-or-later
# lib/Locale/RecodeData.pm:     GPL-3.0-or-later
# lib/Locale/libintlFAQ.pod:    LGPL-2.0-or-later
# COPYING:                      GPL-3.0-or-later
License:        GPL-3.0-or-later AND LGPL-2.0-or-later
URL:            https://metacpan.org/release/libintl-perl
Source0:        https://cpan.metacpan.org/authors/id/G/GU/GUIDO/libintl-perl-%{version}.tar.gz
%if 0%{?os2_version}
Vendor:         bww bitwise works GmbH
%endif
# this module was renamed in the f25 dev cycle
Provides:       perl-libintl = %{version}-%{release}
Obsoletes:      perl-libintl < 1.25

BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
%if !0%{?os2_version}
BuildRequires:  glibc-common
%endif
BuildRequires:  make
BuildRequires:  perl-interpreter
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
BuildRequires:  sed
# Run-time:
BuildRequires:  perl(base)
BuildRequires:  perl(bytes)
BuildRequires:  perl(constant)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(Encode)
BuildRequires:  perl(Encode::Alias)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(integer)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(locale)
BuildRequires:  perl(POSIX)
# Optional run-time:
BuildRequires:  perl(File::ShareDir)
BuildRequires:  perl(I18N::Langinfo)
# Tests:
# Needed for tests/03bind_textdomain_codeset_pp.t
%if !0%{?os2_version}
BuildRequires:  glibc-langpack-de
# Needed for tests/04find_domain_bug.t
BuildRequires:  glibc-langpack-en
%endif
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::Harness)
Requires:       perl(Carp)
Requires:       perl(Encode::Alias)
Requires:       perl(POSIX)
Recommends:     perl(File::ShareDir)
Recommends:     perl(I18N::Langinfo)

%{?perl_default_filter}

%description
The package libintl-perl is an internationalization library for Perl that
aims to be compatible with the Uniforum message translations system as
implemented for example in GNU gettext.


%prep
%setup -q -n libintl-perl-%{version}
find -type f -exec chmod -x {} \;
find lib/Locale gettext_xs \( -name '*.pm' -o -name '*.pod' \) \
    -exec sed -i -e '/^#! \/bin\/false/d' {} \;
# Fix rpmlint errors and warnings
cd sample/simplecal
sed -i -e '1i#!%{__perl}' bin/simplecal.pl Makefile.PL
for file in po/*.po; do
    iconv -f ISO-8859-1 -t UTF-8 -o $file.new $file && \
    mv $file.new $file
done
rm .gitignore MANIFEST


%build
%if !0%{?os2_version}
/usr/bin/perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}" NO_PERLLOCAL=1
%else
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%endif
%make_build

%install
%make_install
%if !0%{?os2_version}
/usr/bin/find %{buildroot} -type f \( -name .packlist -o \
                  -name '*.bs' -size 0 \) -delete
%endif
%{_fixperms} %{buildroot}

%check
%if !0%{?os2_version}
%make_build test
%endif

%files
%license COPYING
%doc Changes Credits FAQ README REFERENCES TODO
%doc sample
%{perl_vendorlib}/Locale/
%{perl_vendorarch}/auto/Locale/
%{_mandir}/man?/*

%changelog
* Mon Aug 03 2026 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.37-1
- initial version
