%global		module		Cbc

Name:		coin-or-%{module}
Group:		Applications/Engineering
Summary:	Coin-or branch and cut
Version:	2.9.8
Release:	1%{?dist}
License:	EPL
URL:		http://projects.coin-or.org/%{module}
Source0:	http://www.coin-or.org/download/pkgsource/%{module}/%{module}-%{version}.tgz
#BuildRequires:	atlas-devel
#BuildRequires:	blas-devel
BuildRequires:	bzip2-devel
BuildRequires:	coin-or-Clp-devel
BuildRequires:	coin-or-Cgl-devel
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
Cbc (Coin-or branch and cut) is an open-source mixed integer programming
solver written in C++. It can be used as a callable library or using a
stand-alone executable. It can be called through AMPL (natively), GAMS
(using the links provided by the "Optimization Services" and "GAMSlinks"
projects), MPL (through the "CoinMP" project), AIMMS (through the "AIMMSlinks"
project), or "PuLP".

Cbc links to a number of other COIN projects for additional functionality,
including:

   * Clp (the default solver for LP relaxations)
   * Cgl (for cut generation)
   * CoinUtils (for reading input files and various utilities)

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

# silence doxygen deprecation warnings
sed -i 's/^\(SYMBOL_CACHE_SIZE\|SHOW_DIRECTORIES\|HTML_ALIGN_MEMBERS\|USE_INLINE_TREES\|DOT_FONTNAME\)/#\1/g' doxydoc/doxygen.conf.in

%build
export CONFIG_SITE=/@unixroot/usr/share/config-legacy.site
%configure --disable-shared --enable-static
# Kill rpaths
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags} all doxydoc

%install
make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_libdir}/*.la
cp -a doxydoc/html %{buildroot}%{_docdir}/%{name}
cp -p src/CbcParam.hpp %{buildroot}%{_includedir}/coin/

%check

%files
%dir %{_docdir}/%{name}
%doc %{_docdir}/%{name}/AUTHORS
%doc %{_docdir}/%{name}/LICENSE
%doc %{_docdir}/%{name}/README
%doc %{_docdir}/%{name}/cbc_addlibs.txt
%{_bindir}/cbc.exe

%files		devel
%{_includedir}/coin/*
%{_libdir}/pkgconfig/*
%{_libdir}/*.a

%files		doc
%doc %{_docdir}/%{name}/html

%changelog
* Tue Feb 19 2019 yd <yd@os2power.com> 2.9.8-1
- initial rpm build.
