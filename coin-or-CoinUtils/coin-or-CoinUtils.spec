%global		module		CoinUtils

Name:		coin-or-%{module}
Group:		Applications/Engineering
Summary:	Coin-or Utilities
Version:	2.10.13
Release:	1%{?dist}
License:	EPL
URL:		http://projects.coin-or.org/%{module}
Source0:	http://www.coin-or.org/download/pkgsource/%{module}/%{module}-%{version}.tgz
BuildRequires:	bzip2-devel
BuildRequires:	coin-or-Sample
BuildRequires:	doxygen
BuildRequires:	pkgconfig
BuildRequires:	readline-devel
BuildRequires:	zlib-devel

Patch0:		coin-or-CoinUtils.patch
Patch1:		coin-or-CoinUtils-docdir.patch

%description
CoinUtils (Coin-or Utilities) is an open-source collection of classes
and functions that are generally useful to more than one COIN-OR project.
These utilities include:

  * Vector classes
  * Matrix classes
  * MPS file reading
  * Comparing floating point numbers with a tolerance

%package	devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	bzip2-devel
Requires:	coin-or-Sample
Requires:	pkgconfig(zlib)

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package	doc
Summary:	Documentation files for %{name}
Group:		Documentation
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description	doc
This package contains the documentation for %{name}.

%prep
%setup -q -n %{module}-%{version}
%patch0 -p1
%patch1 -p1

%build
export CONFIG_SITE=/@unixroot/usr/share/config-legacy.site
%configure --disable-shared --enable-static
make %{?_smp_mflags} all doxydoc

%install
make install DESTDIR=%{buildroot}
rm %{buildroot}%{_libdir}/*.la
cp -a doxydoc/html %{buildroot}%{_docdir}/%{name}

%check

%files
%dir %{_docdir}/%{name}
%doc %{_docdir}/%{name}/AUTHORS
%doc %{_docdir}/%{name}/coinutils_addlibs.txt
%doc %{_docdir}/%{name}/LICENSE
%doc %{_docdir}/%{name}/README

%files		devel
%{_includedir}/coin
%{_libdir}/pkgconfig/*
%{_libdir}/*.a

%files		doc
%doc %{_docdir}/%{name}/html

%changelog
* Tue Feb 19 2019 yd <yd@os2power.com> 2.10.13-1
- initial rpm build.
