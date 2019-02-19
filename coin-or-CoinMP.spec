%global		module		CoinMP

Name:		coin-or-%{module}
Group:		Applications/Engineering
Summary:	C-API interface to CLP, CBC and CGL
Version:	1.8.3
Release:	1%{?dist}
License:	CPL
URL:		http://projects.coin-or.org/%{module}
Source0:	http://www.coin-or.org/download/pkgsource/%{module}/%{module}-%{version}.tgz
#BuildRequires:	atlas-devel
#BuildRequires:	blas-devel
BuildRequires:	bzip2-devel
BuildRequires:	coin-or-Cbc-devel
BuildRequires:	coin-or-Cgl-devel
BuildRequires:	coin-or-Clp-devel
BuildRequires:	coin-or-CoinUtils-devel
BuildRequires:	coin-or-Osi-devel
#BuildRequires:	glpk-devel
#BuildRequires:	lapack-devel
BuildRequires:	pkgconfig
BuildRequires:	readline-devel
BuildRequires:	zlib-devel

# Install documentation in standard rpm directory
Patch0:		%{name}-docdir.patch
Patch1:		%{name}.patch

%description
CoinMP is a C-API library that supports most of the functionality of CLP
(Coin LP), CBC (Coin Branch-and-Cut), and CGL (Cut Generation Library)
projects.

%package	devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	coin-or-CoinUtils-devel
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n %{module}-%{version}
%patch0 -p1
%patch1 -p0
# Use unix style line endings
for file in README AUTHORS examples/example.c LICENSE; do
    sed -i 's|\r||' $file
done

%build
export CONFIG_SITE=/@unixroot/usr/share/config-legacy.site
%configure
make %{?_smp_mflags} all

%install
make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_libdir}/*.la
# Some install rule install 2 sample doc files under buildroot/buildroot
for file in `find %{buildroot}%{buildroot} -type f`; do
    mv $file `echo $file | sed -e 's|%{buildroot}||'`
done
rm %{buildroot}%{_docdir}/%{name}/Makefile
rm %{buildroot}%{_docdir}/%{name}/LICENSE
cp -p src/CoinMP.dll %{buildroot}%{_libdir}

%check

%files
%license LICENSE
%doc %{_docdir}/%{name}/AUTHORS
%doc %{_docdir}/%{name}/README
%doc %{_docdir}/%{name}/coinmp_addlibs.txt
%doc %{_docdir}/%{name}/example.c
%{_libdir}/*.dll

%files		devel
%{_includedir}/coin/*
%{_libdir}/pkgconfig/*
%{_libdir}/*.a

%changelog
* Tue Feb 19 2019 yd <yd@os2power.com> 1.8.3-1
- initial rpm build.
