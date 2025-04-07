Name:           perl-HTML-Parser
Summary:        Perl module for parsing HTML
Version:        3.83
Release:        1%{?dist}
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Source0:        https://cpan.metacpan.org/authors/id/O/OA/OALDERS/HTML-Parser-%{version}.tar.gz
URL:            https://metacpan.org/release/HTML-Parser
%if 0%{?os2_version}
Vendor:         bww bitwise works GmbH
%endif
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
%if !0%{?os2_version}
BuildRequires:  glibc-common
%endif
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
%if !0%{?os2_version}
BuildRequires:  perl-interpreter
%else
BuildRequires:  perl
%endif
BuildRequires:  perl(Config)
%if !0%{?os2_version}
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
%else
BuildRequires:  perl(ExtUtils::MakeMaker)
%endif
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(HTML::Tagset) >= 3
BuildRequires:  perl(HTTP::Headers)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(URI)
BuildRequires:  perl(XSLoader)
# Tests
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(SelectSaver)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(threads)
Requires:       perl(HTML::Tagset) >= 3
Requires:       perl(HTTP::Headers)
Requires:       perl(IO::File)
Requires:       perl(URI)

%{?perl_default_filter}
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}perl\\(HTML::Tagset\\)$

%description
The HTML-Parser module for perl to parse and extract information from
HTML documents, including the HTML::Entities, HTML::HeadParser,
HTML::LinkExtor, HTML::PullParser, and HTML::TokeParser modules.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n HTML-Parser-%{version}
chmod -c a-x eg/*

# Help file to recognise the Perl scripts and normalize shebangs
for F in t/*.t; do
    perl -i.bkp -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*perl\b}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}" NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}
%if 0%{?os2_version}
make manifypods
%endif

%install
%{make_install}
%if !0%{?os2_version}
file=%{buildroot}%{_mandir}/man3/HTML::Entities.3pm
%else
file=%{buildroot}%{_mandir}/man3/HTML.Entities.3pm
%endif
%if !0%{?os2_version}
iconv -f iso-8859-1 -t utf-8 <"$file" > "${file}_" && \
    touch -r ${file} ${file}_ && \
    mv -f "${file}_" "$file"
%endif
find %{buildroot} -type f -name '*.bs' -empty -delete
%if 0%{?os2_version}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete
%endif
%{_fixperms} %{buildroot}/*

# Install tests
mkdir -p %{buildroot}/%{_libexecdir}/%{name}
cp -a t %{buildroot}/%{_libexecdir}/%{name}
cat > %{buildroot}/%{_libexecdir}/%{name}/test << 'EOF'
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
chmod +x %{buildroot}/%{_libexecdir}/%{name}/test

%check
%if !0%{?os2_version}
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
make test
%endif

%files
%license LICENSE
%doc Changes README TODO eg/
%{perl_vendorarch}/HTML/
%{perl_vendorarch}/auto/HTML/
%if !0%{?os2_version}
%{_mandir}/man3/HTML::*.3pm*
%else
%{_mandir}/man3/*.3pm*
%endif

%files tests
%{_libexecdir}/%{name}

%changelog
* Mon Apr 07 2025 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.83-1
- update to version 3.83

* Mon May 08 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.72-1
- initial version
