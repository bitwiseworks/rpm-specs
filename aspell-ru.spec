%global lang ru
%global langrelease 1
%global aspellversion 6
%global debug_package %{nil}

Summary: Russian dictionaries for Aspell
Name: aspell-%{lang}
Version: 0.99f7
Release: 1%{?dist}
License: ARL
Group: Applications/Text
URL: ftp://ftp.gnu.org/gnu/aspell/dict/0index.html#0.60
Source0: ftp://ftp.gnu.org/gnu/aspell/dict/%{lang}/aspell%{aspellversion}-%{lang}-%{version}-%{langrelease}.tar.bz2
Source1: russian.alias

Buildrequires: aspell >= 0.60
BuildArch: noarch
Requires: aspell >= 0.60

%description
Provides the word list/dictionaries for the following: Russian

%prep
%setup -q -n aspell%{aspellversion}-%{lang}-%{version}-%{langrelease}

%build
./configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
%{__install} -p %{SOURCE1} $RPM_BUILD_ROOT%{_libdir}/aspell-0.60/

%files
%doc Copyright
%{_libdir}/aspell-0.60/*

%changelog
* Wed Feb 18 2015 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.99f7-1
- initial version