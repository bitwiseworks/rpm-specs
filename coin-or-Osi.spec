%global		module		Osi

Name:		coin-or-%{module}
Group:		Applications/Engineering
Summary:	COIN-OR Open Solver Interface Library
Version:	0.107.8
Release:	1%{?dist}
License:	EPL
URL:		https://projects.coin-or.org/%{module}
Source0:	http://www.coin-or.org/download/pkgsource/%{module}/%{module}-%{version}.tgz
#BuildRequires:	atlas-devel
#BuildRequires:	blas-devel
BuildRequires:	bzip2-devel
BuildRequires:	coin-or-CoinUtils-devel
BuildRequires:	doxygen
#BuildRequires:	glpk-devel
#BuildRequires:	lapack-devel
BuildRequires:	pkgconfig
BuildRequires:	readline-devel
BuildRequires:	zlib-devel

# Install documentation in standard rpm directory
Patch0:		%{name}-docdir.patch

%description
The COIN-OR Open Solver Interface Library is a collection of solver
interfaces (SIs) that provide a common interface --- the OSI API --- for all
the supported solvers.

%package	devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	coin-or-CoinUtils-devel
Requires:	%{name}%{?_isa} = %{version}-%{release}

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

%build
export CONFIG_SITE=/@unixroot/usr/share/config-legacy.site
%configure --disable-shared --enable-static
make %{?_smp_mflags} all doxydoc

%install
make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_libdir}/*.la
cp -a doxydoc/html %{buildroot}%{_docdir}/%{name}

%check

%files
%dir %{_docdir}/%{name}
%doc %{_docdir}/%{name}/AUTHORS
%doc %{_docdir}/%{name}/LICENSE
%doc %{_docdir}/%{name}/README
%doc %{_docdir}/%{name}/osi_addlibs.txt

%files		devel
%{_includedir}/coin/*
%{_libdir}/pkgconfig/*
%{_libdir}/*.a

%files		doc
%doc %{_docdir}/%{name}/html

%changelog
* Tue Feb 19 2019 yd <yd@os2power.com> 0.107.8-1
- initial rpm build.
