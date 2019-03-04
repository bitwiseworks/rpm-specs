Summary: IBM OS/2 Developer's Toolkit Version 4.5
Name: os2tk45
Version: 4.5.2
Release: 8%{?dist}
Group: System Environment/Libraries
License: IBM
Vendor: bww bitwise works GmbH

%scm_source github https://github.com/bitwiseworks/%{name} c0ec7250eded133e9152416a7ae8906c319f7dd6

%global os2_ipfcdir %{_datadir}/os2/ipfc
%global os2tk45_includedir %{_includedir}/os2tk45

# Act like a meta-package and install all essential subpackages
Requires: %{name}-headers = %{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}
Requires: %{name}-rc = %{version}-%{release}
Requires: %{name}-utils = %{version}-%{release}
Requires: %{name}-books = %{version}-%{release}

# For os2_dos_path, os2_langdir etc. macros
Requires: os2-rpm >= 0-4

%description
The IBM OS/2 Developer's Toolkit Version 4.5 provides development support
for new features in the "OS/2 Warp Server for e-business" operating system,
ArcaOS and eComStation.

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

%package utils
Summary: IBM OS/2 Developer's Toolkit utilities
Requires: %{name}-readme = %{version}-%{release}

%description utils
Provides IBM OS/2 Developer's Toolkit utility programs.

%package ipfc
Summary: IBM OS/2 Developer's Toolkit IPFC tool
Requires: %{name}-readme = %{version}-%{release}

%description ipfc
Provides IBM OS/2 Developer's Toolkit Information Presentation Facility tool
including the IPF complier and support files.

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

%{__mkdir_p} %{buildroot}%{os2tk45_includedir}
%{__cp} -pR h/* %{buildroot}%{os2tk45_includedir}
# copy inc directory inside to avoid one more dir under include
%{__cp} -pR inc %{buildroot}%{os2tk45_includedir}
# remove LIBC stuff, will go to a separate subpackage one day
%{__rm} -rf %{buildroot}%{os2tk45_includedir}/libc
# remove SOM stuff, it will go to a separate subpackage one day
%{__rm} %{buildroot}%{os2tk45_includedir}/wincfg.*h
%{__rm} %{buildroot}%{os2tk45_includedir}/wp*.*h

%{__mkdir_p} -p %{buildroot}%{_libdir}
%{__cp} -pR lib/* %{buildroot}%{_libdir}
# remove LIBC stuff, will go to a separate subpackage one day
%{__rm} %{buildroot}%{_libdir}/libc*.lib
# remove cryptol.lib, it will go to a separate subpackage one day
%{__rm} %{buildroot}%{_libdir}/crypto.lib

%{__mkdir_p} %{buildroot}%{_bindir}
%{__mkdir_p} %{buildroot}%{os2_langdir}

# rc
%{__cp} -p bin/rc.exe %{buildroot}%{_bindir}
%{__cp} -p bin/rc16.exe %{buildroot}%{_bindir}
%{__cp} -p bin/rcpp.* %{buildroot}%{_bindir}
%{__cp} -p msg/rc*.msg %{buildroot}%{os2_langdir}
%{__cp} -p msg/messages.msg %{buildroot}%{os2_langdir}

# utils
%{__cp} -p bin/exehdr.exe %{buildroot}%{_bindir}
%{__cp} -p bin/alp.exe %{buildroot}%{_bindir}
%{__cp} -p bin/alp.msg %{buildroot}%{os2_langdir}
%{__cp} -p bin/mapsym.exe %{buildroot}%{_bindir}

# ipfc
%{__mkdir_p} %{buildroot}%{os2_ipfcdir}
%{__cp} -p bin/ipfc.exe %{buildroot}%{_bindir}
%{__cp} -p ipfc/* %{buildroot}%{os2_ipfcdir}

# books
%{__mkdir_p} %{buildroot}%{os2_bookdir}
%{__cp} -p book/* %{buildroot}%{os2_bookdir}

%files
# nothing of its own in the meta-package

%files readme
%doc readme
%doc changelog

%files headers
%dir %{os2tk45_includedir}
%{os2tk45_includedir}

%files libs
%{_libdir}/*.lib

%files rc
%{_bindir}/rc.exe
%{_bindir}/rc16.exe
%{_bindir}/rcpp.*
%{os2_langdir}/rc*.msg
%{os2_langdir}/messages.msg

%files utils
%{_bindir}/exehdr.exe
%{_bindir}/alp.exe
%{os2_langdir}/alp.msg
%{_bindir}/mapsym.exe

%files ipfc
%{_bindir}/ipfc.exe
%{os2_ipfcdir}/*

%files books
%{os2_bookdir}/*

%post headers
%cube {ADDSTRING "%{os2_dos_path %{os2tk45_includedir}/inc;%{os2tk45_includedir}/gl;%{os2tk45_includedir}};" IN "SET INCLUDE=" (FIRST IFNEW BEFORE ADDBOTTOM RS(%%)} %{os2_config_sys} > NUL

%postun headers
if [ "$1" = 0 ] ; then
# execute only on last uninstall
%cube {DELSTRING "%{os2_dos_path %{os2tk45_includedir}/inc;%{os2tk45_includedir}/gl;%{os2tk45_includedir}};" IN "SET INCLUDE=" (FIRST RS(%%)} %{os2_config_sys} > NUL
fi

%post ipfc
%cube {ADDSTRING "%{os2_dos_path %{_datadir}/os2/ipfc};" IN "SET IPFC=" (FIRST IFNEW BEFORE ADDBOTTOM RS(%%)} %{os2_config_sys} > NUL

%postun ipfc
if [ "$1" = 0 ] ; then
# execute only on last uninstall
%cube {DELSTRING "%{os2_dos_path %{_datadir}/os2/ipfc};" IN "SET IPFC=" (FIRST RS(%%)} %{os2_config_sys} > NUL
fi

%post libs
%cube {ADDSTRING "%{os2_dos_path %{_libdir}};" IN "SET LIB=" (FIRST IFNEW BEFORE ADDBOTTOM RS(%%)} %{os2_config_sys} > NUL

%postun libs
if [ "$1" = 0 ] ; then
# execute only on last uninstall
%cube {DELSTRING "%{os2_dos_path %{_libdir}};" IN "SET LIB=" (FIRST RS(%%)} %{os2_config_sys} > NUL
fi

%post books
%cube {REPLINE "SET CPREF=" WITH "SET CPREF=CP1.INF+CP2.INF+CP3.INF" (ADDBOTTOM} %{os2_config_sys} > NUL
%cube {REPLINE "SET GPIREF=" WITH "SET GPIREF=GPI1.INF+GPI2.INF+GPI3.INF+GPI4.INF" (ADDBOTTOM} %{os2_config_sys} > NUL
%cube {REPLINE "SET MMREF=" WITH "SET MMREF=MMREF1.INF+MMREF2.INF+MMREF3.INF" (ADDBOTTOM} %{os2_config_sys} > NUL
%cube {REPLINE "SET PMREF=" WITH "SET PMREF=PM1.INF+PM2.INF+PM3.INF+PM4.INF+PM5.INF" (ADDBOTTOM} %{os2_config_sys} > NUL
%cube {REPLINE "SET WPSREF=" WITH "SET WPSREF=WPS1.INF+WPS2.INF+WPS3.INF" (ADDBOTTOM} %{os2_config_sys} > NUL

%postun books
if [ "$1" = 0 ] ; then
# execute only on last uninstall
%cube {DELLINE "SET CPREF="} %{os2_config_sys} > NUL
%cube {DELLINE "SET GPIREF="} %{os2_config_sys} > NUL
%cube {DELLINE "SET MMREF="} %{os2_config_sys} > NUL
%cube {DELLINE "SET PMREF="} %{os2_config_sys} > NUL
%cube {DELLINE "SET WPSREF="} %{os2_config_sys} > NUL
fi

%changelog
* Tue Sep 04 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> 4.5.2-8
- add pdpublic.h ticket #1
- fix ticket #3

* Mon Jun 18 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> 4.5.2-7
- use %{os2_config_sys} macro instead of fixed c:\config.sys

* Fri Jul 28 2017 Dmitriy Kuminov <coding@dmik.org> 4.5.2-6
- Add utils sub-package (currently with EXEHDR, ALP and MAPSYM).
- Add ipfc sub-package with IPFC and support files.
- Use handy os2_dos_path, os2_langdir etc. macros from os2-rpm.

* Sat Jun 10 2017 Dmitriy Kuminov <coding@dmik.org> 4.5.2-5
- Add messages.msg to os2tk45-rc sub-package.
- Brush up %install by using mkdir/cp/rm macros.

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
