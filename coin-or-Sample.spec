%global		module		Sample

Name:		coin-or-%{module}
Group:		Applications/Engineering
Summary:	Coin-or Sample data files
Version:	1.2.10
Release:	7%{?dist}
License:	Public Domain
URL:		https://projects.coin-or.org/svn/Data/%{module}
Source0:	http://www.coin-or.org/download/pkgsource/Data/%{module}-%{version}.tgz
Source1:	COPYING
BuildArch:	noarch

Requires:       pkgconfig

%description
Coin-or Sample data files.

%prep
%setup -q -n %{module}-%{version}

%build
%configure
cp -p %{SOURCE1} .
make %{?_smp_mflags} all

%install
make install DESTDIR=%{buildroot} pkgconfiglibdir=%{_datadir}/pkgconfig

%files
%{_datadir}/coin/
%{_datadir}/pkgconfig/*
%license COPYING

%changelog
* Tue Feb 19 2019 yd <yd@os2power.com> 1.2.10-1
- initial rpm build.
