# Run optional test
%if ! (0%{?rhel} || 0%{?os2_version})
%bcond_without perl_Devel_CheckLib_enables_optional_test
%else
%bcond_with perl_Devel_CheckLib_enables_optional_test
%endif

Name:           perl-Devel-CheckLib
Version:        1.16
Release:        1%{?dist}
Summary:        Check that a library is available

License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Devel-CheckLib
Source0:        https://cpan.metacpan.org/modules/by-module/Devel/Devel-CheckLib-%{version}.tar.gz
%if 0%{?os2_version}
Vendor:         bww bitwise works GmbH
%endif

BuildArch:      noarch

BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker)
# Run-time:
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Temp) >= 0.16
BuildRequires:  perl(Text::ParseWords)
# Tests:
BuildRequires:  gcc
BuildRequires:  perl(blib)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(IO::File)
%if !0%{?os2_version}
BuildRequires:  perl(Capture::Tiny)
%endif
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::More) >= 0.88
# Optional tests
%if %{with perl_Devel_CheckLib_enables_optional_test}
BuildRequires:  perl(Mock::Config)
%endif
# perl inherits the compiler flags it was built with, hence we need this on hardened systems
%if !0%{?os2_version}
Requires:       redhat-rpm-config
%else	
Requires:       os2-rpm >= 1-12
%endif

# Filter modules bundled for tests
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}^%{_libexecdir}

%description
Devel::CheckLib is a perl module that checks whether a particular C library
and its headers are available.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness
Requires:       gcc
# Optional tests
%if %{with perl_Devel_CheckLib_enables_optional_test}
Requires:       perl(Mock::Config)
%endif

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Devel-CheckLib-%{version}

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
%{_fixperms} %{buildroot}/*

# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
perl -i -ne 'print $_ unless m{\Q'-Mblib'\E}' %{buildroot}%{_libexecdir}/%{name}/t/cmdline-LIBS-INC.t
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/bash
set -e
# Some tests need to write into temporary files/directories.
# Copy the tests into a writable directory and execute them from there.
DIR=$(mktemp -d)
pushd "$DIR"
cp -a %{_libexecdir}/%{name}/* ./
prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
popd
rm -rf "$DIR"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
%if !0%{?os2_version}
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
make test
%endif

%files
%doc CHANGES README TODO
%{_bindir}/use-devel-checklib
%{perl_vendorlib}/Devel*
%{_mandir}/man1/use-devel-checklib.1*
%if !0%{?os2_version}
%{_mandir}/man3/Devel::CheckLib.3*
%else
%{_mandir}/man3/Devel.CheckLib.3*
%endif

%files tests
%{_libexecdir}/%{name}

%changelog
* Tue May 05 2026 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.16-1
- update to version 1.16
- resync spec with fedora

* Wed Feb 21 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.11-1
- initial rpm
