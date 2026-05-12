Name:           perl-inc-latest
Epoch:          2
Version:        0.500
Release:        1%{?dist}
Summary:        Use modules bundled in inc/ if they are newer than installed ones
License:        Apache-2.0
URL:            https://metacpan.org/release/inc-latest
Source0:        https://cpan.metacpan.org/authors/id/D/DA/DAGOLDEN/inc-latest-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  make
%if !0%{?os2_version}
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
%endif
BuildRequires:  perl(Config)
%if !0%{?os2_version}
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
%endif
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Tests
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Test::More)
Requires:       perl(ExtUtils::Installed)
Conflicts:      perl-Module-Build < 2:0.42.10-4

%description
The inc::latest module helps bootstrap configure-time dependencies for CPAN
distributions. These dependencies get bundled into the inc directory within
a distribution and are used by Makefile.PL or Build.PL.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n inc-latest-%{version}
# Help generators to recognize Perl scripts
for F in t/*.t; do
    perl -i.bkp -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*perl\b}{$Config{startperl}}' "$F"
    chmod +x "$F"
done
%if 0%{?os2_version}
find t/ -type f -name '*.bkp' -delete
%endif

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} %{buildroot}/*
%if 0%{?os2_version}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete
%endif

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
%license LICENSE
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%files tests
%{_libexecdir}/%{name}

%changelog
* Mon Apr 27 2026 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2:0.500-1
- initial version
