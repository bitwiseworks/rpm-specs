%global		module		Clp

Name:		coin-or-%{module}
Group:		Applications/Engineering
Summary:	Coin-or linear programming
Version:	1.16.10
Release:	1%{?dist}
License:	EPL
URL:		http://projects.coin-or.org/%{module}
Source0:	http://www.coin-or.org/download/pkgsource/%{module}/%{module}-%{version}.tgz
#BuildRequires:	atlas-devel
#BuildRequires:	blas-devel
BuildRequires:	bzip2-devel
BuildRequires:	coin-or-CoinUtils-devel
BuildRequires:	coin-or-Osi-devel
BuildRequires:	doxygen
#BuildRequires:	glpk-devel
#BuildRequires:	graphviz
#BuildRequires:	lapack-devel
BuildRequires:	pkgconfig
BuildRequires:	readline-devel
BuildRequires: 	zlib-devel

# Install documentation in standard rpm directory
Patch0:		%{name}-docdir.patch

%description
Clp (Coin-or linear programming) is an open-source linear programming
solver written in C++. It is primarily meant to be used as a callable
library, but a basic, stand-alone executable version is also available.

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
export LDFLAGS="$LDFLAGS -Zomf -Zhigh-mem"
%configure --disable-shared --enable-static
# Kill rpaths
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags} all doxydoc

%install
make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_libdir}/*.la
cp -a doxydoc/html %{buildroot}%{_docdir}/%{name}

%check

%files
%dir %{_docdir}/%{name}
%doc %{_docdir}/%{name}/AUTHORS
%doc %{_docdir}/%{name}/clp_addlibs.txt
%doc %{_docdir}/%{name}/LICENSE
%doc %{_docdir}/%{name}/README
%{_bindir}/clp.exe

%files		devel
%{_includedir}/coin/*
%{_libdir}/pkgconfig/*
%{_libdir}/*.a

%files		doc
%doc %{_docdir}/%{name}/html

%changelog
* Tue Feb 19 2019 yd <yd@os2power.com> 1.16.10-1
- initial rpm build.
