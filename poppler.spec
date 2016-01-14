Summary:	PDF rendering library
Name:		poppler
Version:	0.38.0
Release:	2%{?dist}
License:	(GPLv2 or GPLv3) and GPLv2+ and LGPLv2+ and MIT
Group:		Development/Libraries
Vendor:		bww bitwise works GmbH
# Source0:	http://poppler.freedesktop.org/%{name}-%{version}.tar.xz
URL:		http://poppler.freedesktop.org/
#define svn_url	    e:/trees/poppler/trunk
%define svn_url     http://svn.netlabs.org/repos/ports/poppler/trunk
%define svn_rev     1176

Source: %{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip

Requires: poppler-data >= 0.4.0
BuildRequires: gcc make subversion zip

BuildRequires:	libqt4-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:  pkgconfig
BuildRequires:	zlib-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libpng-devel
BuildRequires:  libtiff-devel
BuildRequires:  freetype-devel >= 2.5.3
BuildRequires:  fontconfig-devel >= 2.11.94
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Poppler, a PDF rendering library, is a fork of the xpdf PDF
viewer developed by Derek Noonburg of Glyph and Cog, LLC.

%package devel
Summary:	Libraries and headers for poppler
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
You should install the poppler-devel package if you would like to
compile applications based on poppler.

%package qt
Summary:	Qt4 wrapper for poppler
Group:		System Environment/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}
%{?_qt4:Requires: qt4%{?_isa} >= %{_qt4_version}}
Obsoletes:	poppler-qt4 < 0.16.0-3
Provides:	poppler-qt4 = %{version}-%{release}

%description qt
Qt4 wrapper for poppler.

%package qt-devel
Summary:	Development files for Qt4 wrapper
Group:		Development/Libraries
Requires:	%{name}-qt%{?_isa} = %{version}-%{release}
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}
Obsoletes:	poppler-qt4-devel < 0.16.0-3
Provides:	poppler-qt4-devel = %{version}-%{release}
Requires:	qt4-devel-kit

%description qt-devel
Header files for Qt4 wrapper for poppler.

#%package qt5
#Summary: Qt5 wrapper for poppler
#Group:   System Environment/Libraries
#Requires: %{name}%{?_isa} = %{version}-%{release}
#%{?_qt5:Requires: qt5-qtbase%{?_isa} >= %{_qt5_version}}
#%description qt5
#%{summary}.

#%package qt5-devel
#Summary: Development files for Qt5 wrapper
#Group:   Development/Libraries
#Requires: %{name}-qt5%{?_isa} = %{version}-%{release}
#Requires: %{name}-devel%{?_isa} = %{version}-%{release}
#Requires: qt5-qtbase-devel
#%description qt5-devel
#%{summary}.

%package cpp
Summary: Pure C++ wrapper for poppler
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description cpp
%{summary}.

%package cpp-devel
Summary: Development files for C++ wrapper
Group: Development/Libraries
Requires: %{name}-cpp%{?_isa} = %{version}-%{release}
Requires: %{name}-devel%{?_isa} = %{version}-%{release}

%description cpp-devel
%{summary}.

%package utils
Summary:	Command line utilities for converting PDF files
Group:		Applications/Text
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description utils
Poppler, a PDF rendering library, is a fork of the xpdf PDF
viewer developed by Derek Noonburg of Glyph and Cog, LLC.

This utils package installs a number of command line tools for
converting PDF files to a number of other formats.

%package demos
Summary:	Demos for poppler
Group:		Applications/Text
Requires:	%{name}-glib%{?_isa} = %{version}-%{release}

%description demos
%{summary}.

%debug_package

%prep
%if %{?svn_rev:%(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')}%{?!svn_rev):0}
%setup -q
%else
%setup -n "%{name}-%{version}" -Tc
svn export %{?svn_rev:-r %{svn_rev}} %{svn_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip" "%{name}-%{version}")
%endif

# hammer to nuke rpaths, recheck on new releases
autoreconf -f -i

%build

# these defines needs to go, as soon as we have a pkg-conf for qt
POPPLER_QT4_CFLAGS='-D__OS2__'
POPPLER_QT4_LIBS='-lQtCore4 -lQtGui4 -lQtNetwork4 -lQtXml4'
POPPLER_QT4_TEST_CFLAGS=$POPPLER_QT4_CFLAGS
POPPLER_QT4_TEST_LIBS=$POPPLER_QT4_LIBS
LDFLAGS='-Zomf -Zhigh-mem'

export LDFLAGS
export POPPLER_QT4_CFLAGS
export POPPLER_QT4_LIBS
export POPPLER_QT4_TEST_CFLAGS
export POPPLER_QT4_TEST_LIBS

%configure \
	--enable-poppler-qt4=yes --enable-zlib=yes \
	--enable-libopenjpeg=none \
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
%defattr(644,root,root,755)
%doc COPYING README
%attr(755,root,root) %{_libdir}/popple*.dll

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/poppler_dll.a
%attr(755,root,root) %{_libdir}/poppler57_dll.a
%{_libdir}/pkgconfig/poppler.pc
%{_libdir}/pkgconfig/poppler-splash.pc
%dir %{_includedir}/poppler/
# xpdf headers
%{_includedir}/poppler/*.h
%{_includedir}/poppler/fofi/
%{_includedir}/poppler/goo/
%{_includedir}/poppler/splash/

%files qt
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/poppq4*.dll

%files qt-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/poppler-qt4*_dll.a
%{_libdir}/pkgconfig/poppler-qt4.pc
%{_includedir}/poppler/qt4/

#%files qt5
#%defattr(644,root,root,755)
#%attr(755,root,root) %{_libdir}/poppq5*.dll

#%files qt5-devel
#%defattr(644,root,root,755)
#%attr(755,root,root) %{_libdir}/poppler-qt5*_dll.a
#%{_libdir}/pkgconfig/poppler-qt5.pc
#%{_includedir}/poppler/qt5/

%files cpp
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/popplc*.dll

%files cpp-devel
%defattr(644,root,root,755)
%{_libdir}/pkgconfig/poppler-cpp.pc
%attr(755,root,root) %{_libdir}/poppler-cpp*_dll.a
%{_includedir}/poppler/cpp

%files utils
%defattr(644,root,root,755)
%{_bindir}/pdf*.exe
%{_mandir}/man1/*


%changelog
* Thu Dec 29 2015 Silvan Scherrer <silvan.scherrer@aroa.ch> 0.38.0-2
- updated required fontconfig to 2.11.94
- adjusted debug package creation to latest rpm macros

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

* Mon Oct 9 2014 Silvan Scherrer <silvan.scherrer@aroa.ch> 0.26.5-3
- fixed opening of files bin vs text due to bogous ifdef

* Mon Oct 6 2014 Silvan Scherrer <silvan.scherrer@aroa.ch> 0.26.5-2
- rebuilt with new libtool, which gave new dll names

* Tue Sep 30 2014 Silvan Scherrer <silvan.scherrer@aroa.ch> 0.26.5-1
- update poppler to 0.26.5
- added cpp part
- added qt5 part as comment

* Fri Sep 26 2014 Silvan Scherrer <silvan.scherrer@aroa.ch> 0.26.0
- first rpm version