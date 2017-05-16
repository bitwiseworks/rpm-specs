Summary: IBM OS/2 Developer's Toolkit Version 4.5
Name: os2tk45
Version: 4.5.2
Release: 4%{?dist}
Group: System Environment/Libraries
License: IBM
Vendor: bww bitwise works GmbH

%scm_source github https://github.com/bitwiseworks/%{name} 660fdb07c929623bd9043c88f2734f08c741e714

# Act like a meta-package and install all essential subpackages
Requires: %{name}-headers = %{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}
Requires: %{name}-rc = %{version}-%{release}
Requires: %{name}-books = %{version}-%{release}

%description
The IBM OS/2 Developer's Toolkit Version 4.5 provides development support
for new features in the "OS/2 Warp Server for e-business" operating system
and eComStation.

%package readme
Summary: IBM OS/2 Developer's Toolkit readme
BuildArch: noarch
# The readme subpackage is required by everybody, so use it as a place for
# common dependencies (meta package isn't good for it as it may be not
# installed):
# - os2-base 0.0.0-12 sets up BOOK/HELP/DPATH for UNIXROOT in config.sys
Requires: os2-base >= 0.0.0-12

%description readme
Provides IBM OS/2 Developer's Toolkit readme and changelog files.

%package headers
Summary: IBM OS/2 Developer's Toolkit headers
Requires: %{name}-readme = %{version}-%{release}
BuildArch: noarch

%description headers
Provides IBM OS/2 Developer's Toolkit header files.

%package libs
Summary: IBM OS/2 Developer's Toolkit libraries
Requires: %{name}-readme = %{version}-%{release}

%description libs
Provides IBM OS/2 Developer's Toolkit library files.

%package rc
Summary: IBM OS/2 Developer's Toolkit resource compilers
Requires: %{name}-readme = %{version}-%{release}

%description rc
Provides IBM OS/2 Developer's Toolkit resource compilers. Both 32-bit and 16-bit
resource compilers (version 5.xxx and 4.xxx, respectively) are included in this
package.

%package books
Summary: IBM OS/2 Developer's Toolkit books
Requires: %{name}-readme = %{version}-%{release}
BuildArch: noarch

%description books
Provides IBM OS/2 Developer's Toolkit book files in INF and HLP formats.

%prep
%scm_setup

%build

%install

mkdir -p %{buildroot}%{_includedir}/os2tk45
cp -pR h/* %{buildroot}%{_includedir}/os2tk45/
# copy inc directory inside to avoid one more dir under include
cp -pR inc %{buildroot}%{_includedir}/os2tk45/
# remove LIBC stuff, will go to a separate subpackage one day
rm -rf %{buildroot}%{_includedir}/os2tk45/libc
# remove SOM stuff, it will go to a separate subpackage one day
rm %{buildroot}%{_includedir}/os2tk45/wincfg.*h
rm %{buildroot}%{_includedir}/os2tk45/wp*.*h

mkdir -p %{buildroot}%{_libdir}
cp -pR lib/* %{buildroot}%{_libdir}/
# remove LIBC stuff, will go to a separate subpackage one day
rm %{buildroot}%{_libdir}/libc*.lib
# remove cryptol.lib, it will go to a separate subpackage one day
rm %{buildroot}%{_libdir}/crypto.lib

mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/os2/lang

cp -p bin/rc*.exe %{buildroot}%{_bindir}/
cp -p bin/rcpp.* %{buildroot}%{_bindir}/
cp -p msg/rc*.msg %{buildroot}%{_datadir}/os2/lang/

mkdir -p %{buildroot}%{_datadir}/os2/book
cp -p book/* %{buildroot}%{_datadir}/os2/book/

%files
# nothing of its own in the meta-package

%files readme
%doc readme
%doc changelog

%files headers
%{_includedir}/os2tk45

%files libs
%{_libdir}/*.lib

%files rc
%{_bindir}/rc*.exe
%{_bindir}/rcpp.*
%{_datadir}/os2/lang/rc*.msg

%files books
%{_datadir}/os2/book/*

%post headers
%cube {ADDSTRING "%UNIXROOT%\usr\include\os2tk45\inc;%UNIXROOT%\usr\include\os2tk45\gl;%UNIXROOT%\usr\include\os2tk45;" IN "SET INCLUDE=" (FIRST IFNEW BEFORE ADDBOTTOM RS(%%)} c:\config.sys > NUL

%postun headers
if [ "$1" = 0 ] ; then
# execute only on last uninstall
%cube {DELSTRING "%UNIXROOT%\usr\include\os2tk45\inc;%UNIXROOT%\usr\include\os2tk45\gl;%UNIXROOT%\usr\include\os2tk45;" IN "SET INCLUDE=" (FIRST RS(%%)} c:\config.sys > NUL
fi

%post libs
%cube {ADDSTRING "%UNIXROOT%\usr\lib;" IN "SET LIB=" (FIRST IFNEW BEFORE ADDBOTTOM RS(%%)} c:\config.sys > NUL

%postun libs
if [ "$1" = 0 ] ; then
# execute only on last uninstall
%cube {DELSTRING "%UNIXROOT%\usr\lib;" IN "SET LIB=" (FIRST RS(%%)} c:\config.sys > NUL
fi

%post books
%cube {REPLINE "SET CPREF=" WITH "SET CPREF=CP1.INF+CP2.INF+CP3.INF" (ADDBOTTOM} c:\config.sys > NUL
%cube {REPLINE "SET GPIREF=" WITH "SET GPIREF=GPI1.INF+GPI2.INF+GPI3.INF+GPI4.INF" (ADDBOTTOM} c:\config.sys > NUL
%cube {REPLINE "SET MMREF=" WITH "SET MMREF=MMREF1.INF+MMREF2.INF+MMREF3.INF" (ADDBOTTOM} c:\config.sys > NUL
%cube {REPLINE "SET PMREF=" WITH "SET PMREF=PM1.INF+PM2.INF+PM3.INF+PM4.INF+PM5.INF" (ADDBOTTOM} c:\config.sys > NUL
%cube {REPLINE "SET WPSREF=" WITH "SET WPSREF=WPS1.INF+WPS2.INF+WPS3.INF" (ADDBOTTOM} c:\config.sys > NUL

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
* Tue May 16 2017 Dmitriy Kuminov <coding@dmik.org> 4.5.2-4
- Add rc subpackage that contains resource compilers version 4 and 5.
- Remove noarch from libs subpackage.
- Make libs subpackage properly clean up LIB statement in config.sys.
- Update config.sys settings upon each update/reinstall.

* Thu Feb 4 2016 Dmitriy Kuminov <coding@dmik.org> 4.5.2-3
- Remove crypto.lib from libs package (conflicts with openssl-devel).

* Wed Jan 27 2016 Dmitriy Kuminov <coding@dmik.org> 4.5.2-2
- Add libs package.
- Remove LIBC related files from headers and libraries.

* Wed Jan 27 2016 Dmitriy Kuminov <coding@dmik.org> 4.5.2-1
- Initial package for Toolkit version 4.5.2.
- Remove ancient DOS EOF symbol (0x1A) from headers.
