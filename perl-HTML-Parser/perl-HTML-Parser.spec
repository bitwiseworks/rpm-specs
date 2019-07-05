Name:           perl-HTML-Parser
Summary:        Perl module for parsing HTML
Version:        3.72
Release:        1%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/G/GA/GAAS/HTML-Parser-%{version}.tar.gz 
URL:            http://search.cpan.org/dist/HTML-Parser/
Vendor:         bww bitwise works GmbH
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
BuildRequires:  coreutils
BuildRequires:  findutils
#BuildRequires:  glibc-common
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(FileHandle)
BuildRequires:  perl(HTML::Tagset) >= 3
%if %{undefined perl_bootstrap}
# This creates cycle with perl-HTTP-Message.
BuildRequires:  perl(HTTP::Headers)
%endif
BuildRequires:  perl(IO::File)
BuildRequires:  perl(SelectSaver)
BuildRequires:  perl(strict)
BuildRequires:  perl(Test)
#BuildRequires:  perl(Test::More)
BuildRequires:  perl(threads)
BuildRequires:  perl(URI)
BuildRequires:  perl(vars)
BuildRequires:  perl(XSLoader)
Requires:       perl(HTML::Tagset) >= 3
Requires:       perl(HTTP::Headers)
Requires:       perl(IO::File)
Requires:       perl(URI)

%{?perl_default_filter}
#{?perl_default_subpackage_tests}
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}perl\\(HTML::Tagset\\)$

%description
The HTML-Parser module for perl to parse and extract information from
HTML documents, including the HTML::Entities, HTML::HeadParser,
HTML::LinkExtor, HTML::PullParser, and HTML::TokeParser modules.

%prep
%setup -q -n HTML-Parser-%{version}
chmod -c a-x eg/*

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}
make manifypods

%install
make pure_install DESTDIR=%{buildroot}
file=%{buildroot}%{_mandir}/man3/HTML.Entities.3pm
#iconv -f iso-8859-1 -t utf-8 <"$file" > "${file}_" && \
#    touch -r ${file} ${file}_ && \
#    mv -f "${file}_" "$file"
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name '*.bs' -empty -delete
chmod -R u+w %{buildroot}/*

%check
#make test

%files
%doc Changes README TODO eg/
%{perl_vendorarch}/HTML/
%{perl_vendorarch}/auto/HTML/
%{_mandir}/man3/*.3pm*

%changelog
* Mon May 08 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.72-1
- initial version
