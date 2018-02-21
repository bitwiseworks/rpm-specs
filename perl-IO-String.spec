Name:           perl-IO-String
Version:        1.08
Release:        1%{?dist}
Summary:        Emulate file interface for in-core strings
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/IO-String/
Vendor:         bww bitwise works GmbH
Source0:        http://www.cpan.org/authors/id/G/GA/GAAS/IO-String-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
# Run-time:
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(IO::Handle)
# Tests:
BuildRequires:  perl(Test)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Data::Dumper)
Requires:       perl(IO::Handle)

%description
The "IO::String" module provides the "IO::File" interface for in-core
strings.  An "IO::String" object can be attached to a string, and
makes it possible to use the normal file operations for reading or
writing data, as well as for seeking to various locations of the
string.  This is useful when you want to use a library module that
only provides an interface to file handles on data that you have in a
string variable.

Note that perl-5.8 and better has built-in support for "in memory"
files, which are set up by passing a reference instead of a filename
to the open() call. The reason for using this module is that it makes
the code backwards compatible with older versions of Perl.


%prep
%setup -q -n IO-String-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}
make manifypods

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
chmod -R u+w %{buildroot}/*

%check
#make test

%files
%doc Changes README
%{perl_vendorlib}/IO/
%{_mandir}/man3/*.3*

%changelog
%changelog
* Wed Feb 21 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.08-1
- initial rpm