%define lang de
%define langrelease 1
%define aspellversion 6
Summary: German dictionaries for Aspell
Name: aspell-%{lang}
Version: 20030222
Release: 1%{?dist}
License: GPLv2
Group: Applications/Text
URL: http://aspell.net/
Source: ftp://ftp.gnu.org/gnu/aspell/dict/%{lang}/aspell%{aspellversion}-%{lang}-%{version}-%{langrelease}.tar.bz2
Requires: aspell >= 0.60

Buildrequires: aspell >= 0.60
BuildArch: noarch
%define debug_package %{nil}

%description
Provides the word list/dictionaries for the following: German, Swiss German

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
%doc COPYING
%defattr(-,root,root,-)

%{_libdir}/aspell-0.60/*

%changelog
* Wed Feb 18 2015 Silvan Scherrer <silvan.scherrer@aroa.ch> - 20030322-1
- initial version