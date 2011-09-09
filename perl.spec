
%define perl_version    5.10.0
%define perl_epoch      0

Name:           perl
Version:        %{perl_version}
Release:        3%{?dist}
Epoch:          %{perl_epoch}
Summary:        The Perl programming language
Group:          Development/Languages
# Modules Tie::File and Getopt::Long are licenced under "GPLv2+ or Artistic,"
# we have to reflect that in the sub-package containing them.
# FIXME: Digest::MD5 has a must-advertise-RSA license with an exception,
# the tag does not reflect that (yet).
License:        (GPL+ or Artistic) and (GPLv2+ or Artistic)
Url:            http://www.perl.org/
Source0:        perl.zip

BuildRoot:      %{_tmppath}/%{name}-%{perl_version}-%{release}-root-%(%{__id_u} -n)
#BuildRequires:  tcsh, dos2unix, man, groff
#BuildRequires:  gdbm-devel, db4-devel

%description
Perl is a high-level programming language with roots in C, sed, awk
and shell scripting.  Perl is good at handling processes and files,
and is especially good at handling text.  Perl's hallmarks are
practicality and efficiency.  While it is used to do a lot of
different things, Perl's most common applications are system
administration utilities and web programming.  A large proportion of
the CGI scripts on the web are written in Perl.  You need the perl
package installed on your system so that your system can handle Perl
scripts.

Install this package if you want to program in Perl or enable your
system to handle Perl scripts.

%prep
%setup -q -n %{name}-%{perl_version}

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}

cp -p usr/bin/perl %{buildroot}%{_bindir}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/perl
