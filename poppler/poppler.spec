Summary:	PDF rendering library
Name:		poppler
Version:	0.59.0
Release:	3%{?dist}
License:	(GPLv2 or GPLv3) and GPLv2+ and LGPLv2+ and MIT
Group:		Development/Libraries
URL:		http://poppler.freedesktop.org/

Vendor:		bww bitwise works GmbH
%scm_source svn http://svn.netlabs.org/repos/ports/poppler/trunk 2299

Requires: poppler-data >= 0.4.0
Requires: nss >= 3.23.0
BuildRequires: gcc make subversion zip

BuildRequires:  gettext-devel
BuildRequires:  libjpeg-devel
BuildRequires:  openjpeg2-devel
BuildRequires:  cairo-devel
BuildRequires:  lcms2-devel
BuildRequires:	libqt4-devel
#BuildRequires:	libqt5-devel
BuildRequires:  libtiff-devel
BuildRequires:  libpng-devel
BuildRequires:  nss-devel >= 3.23.0
BuildRequires:  freetype-devel >= 2.5.3
BuildRequires:  fontconfig-devel >= 2.11.94

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:  pkgconfig
BuildRequires:	zlib-devel

%description
%{name} is a PDF rendering library.

%package devel
Summary:	Libraries and headers for poppler
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
You should install the poppler-devel package if you would like to
compile applications based on poppler.

%package qt
Summary:	Qt4 wrapper for poppler
Group:		System Environment/Libraries
Requires:	%{name} = %{version}-%{release}
%{?_qt4:Requires: qt4 >= %{_qt4_version}}
Obsoletes:	poppler-qt4 < 0.16.0-3
Provides:	poppler-qt4 = %{version}-%{release}

%description qt
%{summary}.

%package qt-devel
Summary:	Development files for Qt4 wrapper
Group:		Development/Libraries
Requires:	%{name}-qt = %{version}-%{release}
Requires:	%{name}-devel = %{version}-%{release}
Obsoletes:	poppler-qt4-devel < 0.16.0-3
Provides:	poppler-qt4-devel = %{version}-%{release}
Requires:	qt4-devel-kit

%description qt-devel
%{summary}.

#%package qt5
#Summary: Qt5 wrapper for poppler
#Group:   System Environment/Libraries
#Requires: %{name} = %{version}-%{release}
#%{?_qt5:Requires: qt5-qtbase >= %{_qt5_version}}
#%description qt5
#%{summary}.

#%package qt5-devel
#Summary: Development files for Qt5 wrapper
#Group:   Development/Libraries
#Requires: %{name}-qt5 = %{version}-%{release}
#Requires: %{name}-devel = %{version}-%{release}
#Requires: qt5-qtbase-devel
#%description qt5-devel
#%{summary}.

%package cpp
Summary: Pure C++ wrapper for poppler
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description cpp
%{summary}.

%package cpp-devel
Summary: Development files for C++ wrapper
Group: Development/Libraries
Requires: %{name}-cpp = %{version}-%{release}
Requires: %{name}-devel = %{version}-%{release}

%description cpp-devel
%{summary}.

%package utils
Summary:	Command line utilities for converting PDF files
Group:		Applications/Text
Requires:	%{name} = %{version}-%{release}

%description utils
Command line tools for manipulating PDF files and converting them to
other formats.

%package demos
Summary:	Demos for poppler
Group:		Applications/Text
Requires:	%{name}-glib = %{version}-%{release}

%description demos
%{summary}.

%legacy_runtime_packages

%debug_package

%prep
%scm_setup

# hammer to nuke rpaths, recheck on new releases
autoreconf -fvi

%build

# these defines needs to go, as soon as we have a pkg-conf for qt
POPPLER_QT4_CFLAGS='-D__OS2__'
POPPLER_QT4_LIBS='-lQtCore4 -lQtGui4 -lQtNetwork4 -lQtXml4'
POPPLER_QT4_TEST_CFLAGS=$POPPLER_QT4_CFLAGS
POPPLER_QT4_TEST_LIBS=$POPPLER_QT4_LIBS
PATH=$PATH';/@unixroot/usr/lib/qt4/bin'

LDFLAGS=" -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"

export LDFLAGS
export POPPLER_QT4_CFLAGS
export POPPLER_QT4_LIBS
export POPPLER_QT4_TEST_CFLAGS
export POPPLER_QT4_TEST_LIBS
export PATH
export VENDOR="%{vendor}"

%configure \
	--enable-poppler-qt4=yes --enable-zlib=yes \
	--enable-zlib-uncompress=yes \
	--enable-shared --disable-static \
	--enable-xpdf-headers

%{__make} %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{_libdir}/lib*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc README
%license COPYING
%attr(755,root,root) %{_libdir}/popple70.dll

%files devel
%attr(755,root,root) %{_libdir}/poppler_dll.a
%attr(755,root,root) %{_libdir}/poppler70_dll.a
%{_libdir}/pkgconfig/poppler.pc
%{_libdir}/pkgconfig/poppler-splash.pc
%{_libdir}/pkgconfig/poppler-cairo.pc
%dir %{_includedir}/poppler/
# xpdf headers
%{_includedir}/poppler/*.h
%{_includedir}/poppler/fofi/
%{_includedir}/poppler/goo/
%{_includedir}/poppler/splash/

%files qt
%attr(755,root,root) %{_libdir}/poppq4*.dll

%files qt-devel
%attr(755,root,root) %{_libdir}/poppler-qt4*_dll.a
%{_libdir}/pkgconfig/poppler-qt4.pc
%{_includedir}/poppler/qt4/

#%files qt5
#%attr(755,root,root) %{_libdir}/poppq5*.dll

#%files qt5-devel
#%attr(755,root,root) %{_libdir}/poppler-qt5*_dll.a
#%{_libdir}/pkgconfig/poppler-qt5.pc
#%{_includedir}/poppler/qt5/

%files cpp
%attr(755,root,root) %{_libdir}/popplc*.dll

%files cpp-devel
%{_libdir}/pkgconfig/poppler-cpp.pc
%attr(755,root,root) %{_libdir}/poppler-cpp*_dll.a
%{_includedir}/poppler/cpp

%files utils
%{_bindir}/pdf*.exe
%{_bindir}/text2pdf.exe
%{_mandir}/man1/*


%changelog
* Tue Nov 20 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.59.0-3
- enable openjpeg2

* Fri Nov 2 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.59.0-2
- enable the unmaintained JPXDecoder for now

* Mon Aug 20 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.59.0-1
- update to vendor version 0.59.0
- fix for ticket #185 by Steven H. Levine

* Fri Feb 17 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.52.0-1
- fix inclusion of dll in main package
- update to vendor version 0.52.0

* Tue Feb 14 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.51.0-1
- remove forwarders and use the legacy_runtime_package macro instead
- adjust spec to scm_ macros usage
- update to vendor version 0.51.0

* Wed Nov 30 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.49.0-2
- add -nostdlib to forwarders, to need less heap

* Mon Nov 21 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> 0.49.0-1
- added text2pdf utility to poppler-utils
- updated poppler to 0.49.0
- added a forwarder dll for version 0.47

* Mon Aug 22 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> 0.47.0-1
- updated poppler to 0.47.0

* Fri Apr 1 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> 0.42.0-2
- enabled nss for signature handling

* Tue Mar 22 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> 0.42.0-1
- updated poppler to 0.42.0

* Mon Mar 14 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> 0.38.0-3
- remove %{?_isa} macro
- enable LCMS support

* Mon Jan 18 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> 0.38.0-2
- updated required fontconfig to 2.11.94
- adjusted debug package creation to latest rpm macros
- create all pages in PSoutputDev, when writing to stdout

* Tue Nov 17 2015 Silvan Scherrer <silvan.scherrer@aroa.ch> 0.38.0-1
- updated poppler to 0.38.0

* Tue Aug 11 2015 Silvan Scherrer <silvan.scherrer@aroa.ch> 0.35.0-1
- updated poppler to 0.35.0

* Tue Jun 9 2015 Silvan Scherrer <silvan.scherrer@aroa.ch> 0.33.0-1
- updated poppler to 0.33.0

* Wed Feb 11 2015 Silvan Scherrer <silvan.scherrer@aroa.ch> 0.31.0-1
- updated poppler to 0.31.0
- added .dbg files

* Mon Dec 15 2014 Silvan Scherrer <silvan.scherrer@aroa.ch> 0.29.0
- updated poppler to 0.29.0
- added poppler-data as requirement

* Thu Oct 9 2014 Silvan Scherrer <silvan.scherrer@aroa.ch> 0.26.5-3
- fixed opening of files bin vs text due to bogous ifdef

* Mon Oct 6 2014 Silvan Scherrer <silvan.scherrer@aroa.ch> 0.26.5-2
- rebuilt with new libtool, which gave new dll names

* Tue Sep 30 2014 Silvan Scherrer <silvan.scherrer@aroa.ch> 0.26.5-1
- update poppler to 0.26.5
- added cpp part
- added qt5 part as comment

* Fri Sep 26 2014 Silvan Scherrer <silvan.scherrer@aroa.ch> 0.26.0
- first rpm version