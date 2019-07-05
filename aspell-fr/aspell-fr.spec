%define lang fr
%define langrelease 3
Summary: French dictionaries for Aspell
Name: aspell-%{lang}
Version: 0.50
Release: 1%{?dist}
License: GPLv2+
Group: Applications/Text
URL: http://aspell.net/
Source: ftp://ftp.gnu.org/gnu/aspell/dict/%{lang}/aspell-%{lang}-%{version}-%{langrelease}.tar.bz2
Requires: aspell >= 0.60

Buildrequires: aspell >= 0.60
BuildArch: noarch

%define debug_package %{nil}

%description
Provides the word list/dictionaries for the following: French, Swiss French

%prep
%setup -q -n aspell-%{lang}-%{version}-%{langrelease}

%build
./configure
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/aspell-0.60/*

%changelog
* Wed Feb 18 2015 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.50-1
- initial version