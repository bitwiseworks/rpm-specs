Summary: IBM OS/2 Developer's Toolkit Version 4.5
Name: os2tk45
Version: 4.5.2
Release: 1%{?dist}
Group: System Environment/Libraries
License: IBM
Vendor: bww bitwise works GmbH

%define github_name os2tk45
%define github_url  https://github.com/bitwiseworks/%{github_name}/archive
%define github_rev  660fdb07c929623bd9043c88f2734f08c741e714

Source: %{github_name}-%{github_rev}.zip

BuildRequires: curl zip

# os2-base 0.0.0-12 sets up BOOK and HELP for UNIXROOT in config.sys
Requires: os2-base >= 0.0.0-12

# Act like a meta-package and install all essential subpackages
Requires: %{name}-headers = %{version}
Requires: %{name}-books = %{version}

%description
The IBM OS/2 Developer's Toolkit Version 4.5 provides development support
for new features in the "OS/2 Warp Server for e-business" operating system
and eComStation.

%package readme
Summary: IBM OS/2 Developer's Toolkit readme
BuildArch: noarch

%description readme
Provides IBM OS/2 Developer's Toolkit readme and changelog files.

%package headers
Summary: IBM OS/2 Developer's Toolkit headers
Requires: %{name}-readme = %{version}-%{release}
BuildArch: noarch

%description headers
Provides IBM OS/2 Developer's Toolkit header files.

%package books
Summary: IBM OS/2 Developer's Toolkit books
Requires: %{name}-readme = %{version}-%{release}
BuildArch: noarch

%description books
Provides IBM OS/2 Developer's Toolkit book files in INF and HLP formats.

%prep
%if %(sh -c 'if test -f "%{_sourcedir}/%{github_name}-%{github_rev}.zip" ; then echo 1 ; else echo 0 ; fi')
%setup -n "%{github_name}-%{github_rev}" -q
%else
%setup -n "%{github_name}-%{github_rev}" -Tc
rm -f "%{_sourcedir}/%{github_name}-%{github_rev}.zip"
curl -sSL "%{github_url}/%{github_rev}.zip" -o "%{_sourcedir}/%{github_name}-%{github_rev}.zip"
unzip "%{_sourcedir}/%{github_name}-%{github_rev}.zip" -d ..
%endif

%build

%install

mkdir -p %{buildroot}%{_includedir}/os2tk45
cp -pR h/* %{buildroot}%{_includedir}/os2tk45/
# copy inc directory inside to avoid one more dir under include
cp -pR inc %{buildroot}%{_includedir}/os2tk45/
# remove SOM stuff, it will go to a separate subpackage one day
rm %{buildroot}%{_includedir}/os2tk45/wincfg.*h
rm %{buildroot}%{_includedir}/os2tk45/wp*.*h

mkdir -p %{buildroot}%{_datadir}/os2/book
cp -p book/* %{buildroot}%{_datadir}/os2/book/

%files

%files readme
%doc readme
%doc changelog

%files headers
%{_includedir}/os2tk45

%files books
%{_datadir}/os2/book/*

%post headers
if [ "$1" = 1 ] ; then
# execute only on first install
%cube {ADDSTRING "%UNIXROOT%\usr\include\os2tk45\inc;%UNIXROOT%\usr\include\os2tk45\gl;%UNIXROOT%\usr\include\os2tk45;%UNIXROOT%\usr\include\os2tk45\libc;" IN "SET INCLUDE=" (FIRST IFNEW BEFORE ADDBOTTOM RS(%%)} c:\config.sys > NUL
fi

%postun headers
if [ "$1" = 0 ] ; then
# execute only on last uninstall
%cube {DELSTRING "%UNIXROOT%\usr\include\os2tk45\inc;%UNIXROOT%\usr\include\os2tk45\gl;%UNIXROOT%\usr\include\os2tk45;%UNIXROOT%\usr\include\os2tk45\libc;" IN "SET INCLUDE=" (FIRST} c:\config.sys > NUL
fi

%post books
if [ "$1" = 1 ] ; then
# execute only on first install
%cube {REPLINE "SET CPREF=" WITH "SET CPREF=CP1.INF+CP2.INF+CP3.INF" (ADDBOTTOM} c:\config.sys > NUL
%cube {REPLINE "SET GPIREF=" WITH "SET GPIREF=GPI1.INF+GPI2.INF+GPI3.INF+GPI4.INF" (ADDBOTTOM} c:\config.sys > NUL
%cube {REPLINE "SET MMREF=" WITH "SET MMREF=MMREF1.INF+MMREF2.INF+MMREF3.INF" (ADDBOTTOM} c:\config.sys > NUL
%cube {REPLINE "SET PMREF=" WITH "SET PMREF=PM1.INF+PM2.INF+PM3.INF+PM4.INF+PM5.INF" (ADDBOTTOM} c:\config.sys > NUL
%cube {REPLINE "SET WPSREF=" WITH "SET WPSREF=WPS1.INF+WPS2.INF+WPS3.INF" (ADDBOTTOM} c:\config.sys > NUL
fi

%postun books
if [ "$1" = 0 ] ; then
# execute only on last uninstall
%cube {DELLINE "SET CPREF="} c:\config.sys > NUL
%cube {DELLINE "SET GPIREF="} c:\config.sys > NUL
%cube {DELLINE "SET MMREF="} c:\config.sys > NUL
%cube {DELLINE "SET PMREF="} c:\config.sys > NUL
%cube {DELLINE "SET WPSREF="} c:\config.sys > NUL
fi

%changelog
* Wed Jan 27 2016 Dmitriy Kuminov <coding@dmik.org> 4.5.2-1
- Initial package for Toolkit version 4.5.2.
- Remove ancient DOS EOF symbol (0x1A) from headers.
