%global		module		Cgl

Name:		coin-or-%{module}
Group:		Applications/Engineering
Summary:	Cut Generation Library
Version:	0.59.9
Release:	1%{?dist}
License:	EPL
URL:		http://projects.coin-or.org/%{module}
Source0:	http://www.coin-or.org/download/pkgsource/%{module}/%{module}-%{version}.tgz
#BuildRequires:	atlas-devel
#BuildRequires:	blas-devel
BuildRequires:	bzip2-devel
BuildRequires:	coin-or-Clp-devel
BuildRequires:	coin-or-CoinUtils-devel
BuildRequires:	coin-or-Osi-devel
BuildRequires:	doxygen
#BuildRequires:	glpk-devel
#BuildRequires:	graphviz
#BuildRequires:	lapack-devel
BuildRequires:	pkgconfig
BuildRequires:	readline-devel
BuildRequires:	zlib-devel

# Install documentation in standard rpm directory
Patch0:		%{name}-docdir.patch

%description
The COIN-OR Cut Generation Library (Cgl) is a collection of cut generators
that can be used with other COIN-OR packages that make use of cuts, such as,
among others, the linear solver Clp or the mixed integer linear programming
solvers Cbc or BCP.

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
%doc %{_docdir}/%{name}/cgl_addlibs.txt
%doc %{_docdir}/%{name}/LICENSE
%doc %{_docdir}/%{name}/README

%files		devel
%{_includedir}/coin/*
%{_libdir}/pkgconfig/*
%{_libdir}/*.a

%files		doc
%doc %{_docdir}/%{name}/html

%changelog
* Tue Feb 19 2019 yd <yd@os2power.com> 0.59.9-1
- initial rpm build.
