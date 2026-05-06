Name:           perl-Devel-Symdump
Epoch:          1
Version:        2.18
Release:        2%{?dist}
%if 0%{?os2_version}
Vendor:         bww bitwise works GmbH
%endif
Summary:        A Perl module for inspecting Perl's symbol table
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Url:            https://metacpan.org/release/Devel-Symdump
Source0:        https://cpan.metacpan.org/authors/id/A/AN/ANDK/Devel-Symdump-%{version}.tar.gz
BuildArch:      noarch
# Module Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# Module Runtime
BuildRequires:  perl(B)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(constant)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
# Test Suite
BuildRequires:  perl(English)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::Harness) >= 3.04
BuildRequires:  perl(Test::More)
BuildRequires:  perl(warnings)
# Author Tests
%if 0%{!?perl_bootstrap:1} && !0%{?os2_version} 
# Compress::Zlib (IO-Compress) ? Test::NoWarnings ? Devel::StackTrace ?
#   Test::NoTabs ? Test::Pod::Coverage ? Pod::Coverage ? Devel::Symdump
BuildRequires:  perl(Compress::Zlib)
BuildRequires:  perl(Test::Pod) >= 1.00
# Test::Pod::Coverage ? Pod::Coverage ? Devel::Symdump
BuildRequires:  perl(Test::Pod::Coverage)
%endif
# Runtime
Requires:       perl(B)

%description
The perl module Devel::Symdump provides a convenient way to inspect
perl's symbol table and the class hierarchy within a running program.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Devel-Symdump-%{version}
# Help generators to recognize Perl scripts
for F in t/*.t; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*perl\b}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}
%if 0%{?os2_version}
make manifypods
%endif

%install
%{make_install}
%{_fixperms} -c %{buildroot}
# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
# Remove author tests
rm %{buildroot}%{_libexecdir}/%{name}/t/pod*.t
rm %{buildroot}%{_libexecdir}/%{name}/t/glob_to*.t
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/sh
cd %{_libexecdir}/%{name} && exec prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
%if !0%{?os2_version}
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
make test %{!?perl_bootstrap:AUTHOR_TEST=1}
%endif

%files
%doc Changes README
%{perl_vendorlib}/Devel/
%if !0%{?os2_version}
%{_mandir}/man3/Devel::Symdump.3*
%else
%{_mandir}/man3/*.3*
%endif

%files tests
%{_libexecdir}/%{name}

%changelog
* Wed May 06 2026 Elbert Pol <elbert.pol@gmail.com> - 2.18-2
- Updated with latest perl
- Sync with latest Fedora spec

* Wed Mar 07 2018 Elbert Pol <elbert.pol@gmail.com> - 2.18-1
-  initial rpm for OS2
