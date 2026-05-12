Name:           perl-XML-Parser
Version:        2.58
Release:        1%{?dist}
Summary:        Perl module for parsing XML documents

License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Url:            https://metacpan.org/release/XML-Parser
Source0:        https://cpan.metacpan.org/authors/id/T/TO/TODDR/XML-Parser-%{version}.tar.gz
%if 0%{?os2_version}
Vendor:         bww bitwise works GmbH
%endif

# Build
BuildRequires:  coreutils
%if !0%{?os2_version}
BuildRequires:  expat-devel >= 2.7.2
%else
BuildRequires:  expat-devel >= 2.7.1
%endif
BuildRequires:  findutils
BuildRequires:  gcc
%if !0%{?os2_version}
BuildRequires:  glibc-common
%endif
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(File::ShareDir::Install)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(lib)
# Required for bundled Devel::CheckLib
BuildRequires:  perl(Text::ParseWords)
BuildRequires:  perl(vars)
# Runtime
BuildRequires:  perl(Carp)
BuildRequires:  perl(FileHandle)
BuildRequires:  perl(File::ShareDir)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(if)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(IO::Handle)
# LWPExternEnt.pl script is loaded by Parser.pm
BuildRequires:  perl(LWP::UserAgent)
BuildRequires:  perl(overload)
BuildRequires:  perl(strict)
BuildRequires:  perl(URI)
BuildRequires:  perl(URI::file)
BuildRequires:  perl(XSLoader)
# Tests
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(if)
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(warnings)
Requires:       perl(IO::File)
Requires:       perl(IO::Handle)
Requires:       perl(LWP::UserAgent)
Requires:       perl(URI)
Requires:       perl(URI::file)

%{?perl_default_filter}
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}perl\\(XML::Parser\\)$

%description
This module provides ways to parse XML documents. It is built on top
of XML::Parser::Expat, which is a lower level interface to James
Clark's expat library. Each call to one of the parsing methods creates
a new instance of XML::Parser::Expat which is then used to parse the
document. Expat options may be provided when the XML::Parser object is
created. These options are then passed on to the Expat object on each
parse call. They can also be given as extra arguments to the parse
methods, in which case they override options given at XML::Parser
creation time.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n XML-Parser-%{version} 
%if !0%{?os2_version}
chmod 644 samples/{canonical,xml*}
%else
chmod 644 samples/canonical
chmod 644 samples/xml*
%endif
perl -MConfig -pi -e 's|^#!/usr/local/bin/perl\b|$Config{startperl}|' samples/{canonical,xml*}

# Help generators to recognize Perl scripts
for F in t/*.t; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*perl\b}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1 OPTIMIZE="$RPM_OPT_FLAGS"
%{make_build}

%install
%{make_install}
find $RPM_BUILD_ROOT -type f -name '*.bs' -a -size 0 -delete
%{_fixperms} $RPM_BUILD_ROOT/*

%if !0%{?os2_version}
for file in samples/REC-xml-19980210.xml; do
  iconv -f iso-8859-1 -t utf-8 < "$file" > "${file}_"
  mv -f "${file}_" "$file"
  perl -i -pe "s/encoding='ISO-8859-1'/encoding='UTF-8'/" "$file"
done
%endif

# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t samples %{buildroot}%{_libexecdir}/%{name}
cp -a inc %{buildroot}%{_libexecdir}/%{name}
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/bash
set -e
# Some tests write into temporary files/directories. The easiest solution
# is to copy the tests into a writable directory and execute them from there.
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
%doc README.md Changes samples/
%license LICENSE
%{perl_vendorarch}/XML/
%dir %{perl_vendorarch}/auto
%dir %{perl_vendorarch}/auto/share
%dir %{perl_vendorarch}/auto/share/dist
%{perl_vendorarch}/auto/share/dist/XML-Parser
%{perl_vendorarch}/auto/XML/
%if !0%{?os2_version}
%{_mandir}/man3/XML::Parser*.3*
%else
%{_mandir}/man3/XML.Parser*.3*
%endif

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri May 08 2026 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.58-1
- update to version 2.58
- resync with fedora spec

* Mon Feb 26 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.44-1
- initial rpm
