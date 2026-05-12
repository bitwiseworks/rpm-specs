Name:           perl-Data-Dump
Version:        1.25
Release:        1%{?dist}
Summary:        Pretty printing of data structures
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Data-Dump
Source0:        https://cpan.metacpan.org/modules/by-module/Data/Data-Dump-%{version}.tar.gz
%if 0%{?os2_version}
Vendor:         bww bitwise works GmbH
%endif
BuildArch:      noarch
# Build
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# Runtime
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(MIME::Base64)
BuildRequires:  perl(overload)
BuildRequires:  perl(strict)
BuildRequires:  perl(subs)
BuildRequires:  perl(Term::ANSIColor)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
# Tests only
BuildRequires:  perl(IO::Socket::INET)
BuildRequires:  perl(Symbol)
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::More)
# Really optional
Suggests:       perl(MIME::Base64)

%description
This module provides a single function called dump() that takes a list of
values as its argument and produces a string as its result. The string
contains Perl code that, when evaled, produces a deep copy of the original
arguments. The string is formatted for easy reading.

%prep
%setup -q -n Data-Dump-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} -c %{buildroot}

%check
%if !0%{?os2_version}
make test
%endif

%files
%doc Changes README.md
%{perl_vendorlib}/Data/
%if !0%{?os2_version}
%{_mandir}/man3/Data::Dump.3*
%{_mandir}/man3/Data::Dump::Filtered.3*
%{_mandir}/man3/Data::Dump::Trace.3*
%else
%{_mandir}/man3/Data.Dump.3*
%{_mandir}/man3/Data.Dump.Filtered.3*
%{_mandir}/man3/Data.Dump.Trace.3*
%endif

%changelog
* Fri May 08 2026 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.25-1
- update to version 1.25
- resync with fedora spec

* Fri Feb 23 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.23-1
- initial version
