# Perform optional tests
# Build-cycle: perl-Class-DBI → perl-DBD-Pg → perl-DBI → perl-Clone
%if !0%{?os2_version}
%bcond perl_Clone_enables_optional_test %[%{undefined rhel} && %{undefined perl_bootstrap}]
%else
%bcond_with perl_Clone_enables_optional_test 
%endif

Name:           perl-Clone
Version:        0.50
Release:        1%{?dist}
Summary:        Recursively copy perl data types
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Clone
Source0:        https://cpan.metacpan.org/modules/by-module/Clone/Clone-%{version}.tar.gz
%if 0%{?os2_version}
# follow Win for MAX_DEPTH
Patch0:         Clone-0.50.patch
Vendor:         bww bitwise works GmbH
%endif
# Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(Exporter)
BuildRequires:  perl(XSLoader)
# Tests:
BuildRequires:  perl(B)
%if !0%{?os2_version}
BuildRequires:  perl(B::COW) >= 0.004
%endif
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(overload)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(threads)
BuildRequires:  perl(threads::shared)
BuildRequires:  perl(utf8)
BuildRequires:  perl(vars)
%if %{with perl_Clone_enables_optional_test}
# Optional tests:
BuildRequires:  perl(base)
BuildRequires:  perl(Class::DBI)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(DBD::SQLite)
BuildRequires:  perl(DBI)
BuildRequires:  perl(Devel::Peek)
BuildRequires:  perl(Hash::Util::FieldHash)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IO::Socket::INET)
BuildRequires:  perl(Math::BigInt)
BuildRequires:  perl(Math::BigInt::GMP)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Storable)
BuildRequires:  perl(Taint::Runtime)
%endif
# Dependencies
# (none)

%{?perl_default_filter}

%description
This module provides a clone() method that makes recursive
copies of nested hash, array, scalar and reference types,
including tied variables and objects.

clone() takes a scalar argument and an optional parameter that
can be used to limit the depth of the copy. To duplicate lists,
arrays or hashes, pass them in by reference.

%package tests
Summary:        Tests for %{name}
BuildArch:      noarch
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness
%if %{with perl_Clone_enables_optional_test}
Requires:       perl(base)
Requires:       perl(Class::DBI)
Requires:       perl(Data::Dumper)
Requires:       perl(DBD::SQLite)
Requires:       perl(DBI)
Requires:       perl(Devel::Peek)
Requires:       perl(Hash::Util::FieldHash)
Requires:       perl(IO::File)
Requires:       perl(IO::Handle)
Requires:       perl(IO::Socket::INET)
Requires:       perl(Math::BigInt)
Requires:       perl(Math::BigInt::GMP)
Requires:       perl(POSIX)
Requires:       perl(Storable)
Requires:       perl(Taint::Runtime)
%endif

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Clone-%{version}
%if 0%{?os2_version}
%patch -P 0 -p1
%endif
# Help generators to recognize Perl scripts
for F in t/*.t t/*.pl; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!\s*perl}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1 OPTIMIZE="%{optflags}"
%{make_build}
%{make_build}
%if 0%{?os2_version}
make manifypods
%endif

%install
%{make_install}
find %{buildroot} -type f -name '*.bs' -empty -delete
%{_fixperms} -c %{buildroot}
# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/sh
cd %{_libexecdir}/%{name} && exec prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
%if !0%{?os2_version}
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
make test
%endif

%files
%doc AI_POLICY.md Changes README.md SECURITY.md
%{perl_vendorarch}/auto/Clone/
%{perl_vendorarch}/Clone.pm
%{_mandir}/man3/Clone.3*

%files tests
%{_libexecdir}/%{name}

%changelog
* Tue May 05 2026 Silvan Scherrer <silvan.scherrer@aroa.ch> 0.50-1
- initial rpm
