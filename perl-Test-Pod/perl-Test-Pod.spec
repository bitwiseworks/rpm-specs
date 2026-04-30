Name:           perl-Test-Pod
Version:        1.52
Release:        2%{?dist}
Summary:        Test POD files for correctness
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
%if !0%{?os2_version}
Vendor:         bww bitwise works GmbH
%endif
URL:            https://metacpan.org/release/Test-Pod
Source0:        https://cpan.metacpan.org/authors/id/E/ET/ETHER/Test-Pod-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(warnings)
BuildRequires:  perl(strict)
# Run-time
BuildRequires:  perl(File::Find)
BuildRequires:  perl(Pod::Simple) >= 3.05
BuildRequires:  perl(Test::Builder)
# Tests
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Test::Builder::Tester) >= 1.02
BuildRequires:  perl(Test::More) >= 0.62
Requires:       perl(File::Find)
Requires:       perl(Pod::Simple) >= 3.05
Requires:       perl(Test::More) >= 0.62

# Remove under-specified dependcies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Pod::Simple\\)$
# Remove Test::Pod dependecy from *tests package
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}^%{_libexecdir}

%description
Check POD files for errors or warnings in a test file, using Pod::Simple to do
the heavy lifting.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Test-Pod-%{version}
# Help generators to recognize Perl scripts
for F in t/*.t; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*perl\b}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}
%if 0%{?os2_version}
make manifypods
%endif

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name '*.bs' -size 0 -delete
%{_fixperms} %{buildroot}
# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
cp -a lib %{buildroot}%{_libexecdir}/%{name}
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/sh
cd %{_libexecdir}/%{name} && exec prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
%if !0%{?os2_version}
LC_ALL=C make test
%endif

%files
%doc Changes README
%{perl_vendorlib}/Test/
%if !0%{?os2_version}
%{_mandir}/man3/Test::Pod.3pm*
%else
%{_mandir}/man3/*.3pm*
%endif

%files tests
%{_libexecdir}/%{name}

%changelog
* Thu Apr 30 2026 Elbert Pol <elbert.pol@gmail.com> - 1.52-2
- Enable more BuildRequires with newer Perl build

* Thu Apr 30 2026 Elbert Pol <elbert.pol@gmail.com> - 1.52-1
- Update to latest version
- Make it work with latest perl

* Wed Mar 07 2018 Elbert Pol <elbert.pol@gmail.com> - 1.51-1
-  initial rpm for OS2
