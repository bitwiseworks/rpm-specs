# Based on http://pkgs.fedoraproject.org/cgit/rpms/perl-Error.git/tree/perl-Error.spec?id=7314bd991225612bc2db6cd4770568ea1ff3d283

Name:           perl-Error
Epoch:          1
Version:        0.17024
Release:        1%{?dist}
Summary:        Error/exception handling in an OO-ish way
License:        (GPL+ or Artistic) and MIT
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Error/
Vendor:         bww bitwise works GmbH
Source0:        http://www.cpan.org/authors/id/S/SH/SHLOMIF/Error-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  perl-generators
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(lib)
BuildRequires:  perl(Module::Build)
# Run-requires:
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# TODO No Test::Pod on OS/2 yet.
%if 0
# Tests:
BuildRequires:  perl(base)
BuildRequires:  perl(Test::More)
# Optional tests:
%if !%{defined perl_bootstrap}
BuildRequires:  perl(Test::Pod) >= 1.14
BuildRequires:  perl(Test::Pod::Coverage) >= 1.04
%endif
%endif
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
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
perl Build.PL --installdirs=vendor
./Build

%install
rm -rf $RPM_BUILD_ROOT
./Build install --destdir=$RPM_BUILD_ROOT --create_packlist=0
%{_fixperms} $RPM_BUILD_ROOT

%check
# TODO No Test::Pod on OS/2 yet.
%if 0
./Build test
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%if 0%{?_licensedir:1}
%license LICENSE
%else
%doc LICENSE
%endif
# GPL+ or Artistic
%doc ChangeLog README examples/
%{perl_vendorlib}/Error.pm
%{_mandir}/man3/Error.3*
# MIT
%{perl_vendorlib}/Error/
%{_mandir}/man3/Error.Simple.3*

%changelog
* Thu Apr 6 2017 Dmitriy Kuminov <coding@dmik.org> 1:0.17024-1
- Initial release.
