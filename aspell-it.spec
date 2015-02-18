%define lang it
%define langrelease 0
%define aspellversion 6
Summary: Italian dictionaries for Aspell
Name: aspell-%{lang}
Version: 2.2_20050523
Release: 1%{?dist}
License: GPLv2+
Group: Applications/Text
URL: http://aspell.net/
Source: ftp://ftp.gnu.org/gnu/aspell/dict/%{lang}/aspell%{aspellversion}-%{lang}-%{version}-%{langrelease}.tar.bz2
Requires: aspell >= 0.60

Buildrequires: aspell >= 0.60
BuildArch: noarch

%define debug_package %{nil}

%description
Provides the word list/dictionaries for the following: Italian

%prep
%setup -q -n aspell%{aspellversion}-%{lang}-%{version}-%{langrelease}

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
%doc COPYING Copyright
%{_libdir}/aspell-0.60/*

%changelog
* Wed Feb 18 2015 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.2_20050523-1
- initial version