Name:           perl-Error
Epoch:          1
Version:        0.17030
Release:        1%{?dist}
Summary:        Error/exception handling in an OO-ish way
License:        (GPL-1.0-or-later OR Artistic-1.0-Perl) AND X11
URL:            https://metacpan.org/release/Error
Source0:        https://cpan.metacpan.org/modules/by-module/Error/Error-%{version}.tar.gz
%if 0%{?os2_version}
Vendor:         bww bitwise works GmbH
%endif
BuildArch:      noarch
# Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
%if !0%{?os2_version}
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
%endif
BuildRequires:  perl(ExtUtils::MakeMaker)
# Runtime
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(overload)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
# Tests
BuildRequires:  perl(base)
BuildRequires:  perl(blib)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::More)
# Dependencies
Requires:       perl(Carp)

# Avoid provides/requires from examples
%global __provides_exclude_from ^%{_docdir}
%global __requires_exclude_from ^%{_docdir}

%description
The Error package provides two interfaces. Firstly Error provides a
procedural interface to exception handling. Secondly Error is a base class
for errors/exceptions that can either be thrown, for subsequent catch, or
can simply be recorded.

%prep
%setup -q -n Error-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}
%if 0%{?os2_version}
make manifypods
%endif

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

%check
%if !0%{?os2_version}
make test
%endif

%files
%license LICENSE
# GPL-1.0-or-later OR Artistic-1.0-Perl
%doc ChangeLog Changes README examples/
%{perl_vendorlib}/Error.pm
%{_mandir}/man3/Error.3*
# X11
%{perl_vendorlib}/Error/
%if !0%{?os2_version}
%{_mandir}/man3/Error::Simple.3*
%else
%{_mandir}/man3/Error.Simple.3*
%endif

%changelog
* Mon Apr 27 2026 Silvan Scherrer <silvan.scherrer@aroa.ch> 1:0.17030-1
- update to 0.17030
- resync with fedora spec

* Thu Apr 6 2017 Dmitriy Kuminov <coding@dmik.org> 1:0.17024-1
- Initial release.
