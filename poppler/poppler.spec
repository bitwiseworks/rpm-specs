%global test_sha 45f55f1e03b9bf3fbd334c31776b6f5e472889ec
%global test_date 2018-12-18

%global with_glib 0

Summary:	PDF rendering library
Name:	poppler
Version:	0.84.0
Release:	1%{?dist}
License:	(GPLv2 or GPLv3) and GPLv2+ and LGPLv2+ and MIT
URL:		http://poppler.freedesktop.org/

Vendor:		bww bitwise works GmbH
%scm_source github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2

BuildRequires: cmake
BuildRequires: gcc-c++
BuildRequires: gettext-devel
#BuildRequires: pkgconfig(cairo)
#BuildRequires: pkgconfig(cairo-ft)
#BuildRequires: pkgconfig(cairo-pdf)
#BuildRequires: pkgconfig(cairo-ps)
#BuildRequires: pkgconfig(cairo-svg)
BuildRequires: cairo-devel
BuildRequires: pkgconfig(fontconfig)
BuildRequires: pkgconfig(freetype2)

#BuildRequires: pkgconfig(gdk-pixbuf-2.0)
#BuildRequires: pkgconfig(gio-2.0)
#BuildRequires: pkgconfig(gobject-2.0)
#BuildRequires: pkgconfig(gobject-introspection-1.0) 
#BuildRequires: pkgconfig(gtk+-3.0)
#BuildRequires: pkgconfig(gtk-doc)
BuildRequires: pkgconfig(lcms2)
BuildRequires: pkgconfig(libjpeg)
BuildRequires: pkgconfig(libopenjp2)
BuildRequires: pkgconfig(libpng)
BuildRequires: pkgconfig(libtiff-4)
BuildRequires: pkgconfig(nss)
BuildRequires: pkgconfig(poppler-data)
BuildRequires: pkgconfig(Qt5Core)
BuildRequires: pkgconfig(Qt5Gui)
BuildRequires: pkgconfig(Qt5Test)
BuildRequires: pkgconfig(Qt5Widgets)
BuildRequires: pkgconfig(Qt5Xml)
#BuildRequires: pkgconfig(QtCore)
#BuildRequires: pkgconfig(QtGui)
#BuildRequires: pkgconfig(QtTest)
#BuildRequires: pkgconfig(QtXml)
BuildRequires:libqt4-devel

Requires: poppler-data

%if %{with_glib}
Obsoletes: poppler-glib-demos < 0.60.1-1
%endif

%description
%{name} is a PDF rendering library.

%package devel
Summary:	Libraries and headers for poppler
Requires:	%{name} = %{version}-%{release}

%description devel
You should install the poppler-devel package if you would like to
compile applications based on poppler.

%if %{with_glib}
%package glib
Summary: Glib wrapper for poppler
Requires: %{name}%{?_isa} = %{version}-%{release}

%description glib
%{summary}.

%package glib-devel
Summary: Development files for glib wrapper
Requires: %{name}-glib%{?_isa} = %{version}-%{release}
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
Suggests: %{name}-doc = %{version}-%{release}

%description glib-devel
%{summary}.

%package glib-doc
Summary: Documentation for glib wrapper
BuildArch: noarch

%description glib-doc
%{summary}.
%endif

%package qt
Summary:	Qt4 wrapper for poppler
Requires:	%{name} = %{version}-%{release}
%{?_qt4:Requires: qt4 >= %{_qt4_version}}
Obsoletes:	poppler-qt4 < 0.16.0-3
Provides:	poppler-qt4 = %{version}-%{release}
%description qt
%{summary}.

%package qt-devel
Summary:	Development files for Qt4 wrapper
Requires:	%{name}-qt = %{version}-%{release}
Requires:	%{name}-devel = %{version}-%{release}
Obsoletes:	poppler-qt4-devel < 0.16.0-3
Provides:	poppler-qt4-devel = %{version}-%{release}
Requires:	qt4-devel-kit
%description qt-devel
%{summary}.

%package qt5
Summary: Qt5 wrapper for poppler
Requires: %{name} = %{version}-%{release}
%description qt5
%{summary}.

%package qt5-devel
Summary: Development files for Qt5 wrapper
Requires: %{name}-qt5 = %{version}-%{release}
Requires: %{name}-devel = %{version}-%{release}
Requires: qt5-qtbase-devel
%description qt5-devel
%{summary}.

%package cpp
Summary: Pure C++ wrapper for poppler
Requires: %{name} = %{version}-%{release}

%description cpp
%{summary}.

%package cpp-devel
Summary: Development files for C++ wrapper
Requires: %{name}-cpp = %{version}-%{release}
Requires: %{name}-devel = %{version}-%{release}

%description cpp-devel
%{summary}.

%package utils
Summary:	Command line utilities for converting PDF files
Requires:	%{name} = %{version}-%{release}
%description utils
Command line tools for manipulating PDF files and converting them to
other formats.

%legacy_runtime_packages

%debug_package

%prep
%scm_setup

%build
export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"
export LDFLAGS="-Zomf -Zhigh-mem -lcx %{?__global_ldflags}"
export VENDOR="%{vendor}"

mkdir build
cd build
%cmake \
  -DENABLE_CMS=lcms2 \
  -DENABLE_DCTDECODER=libjpeg \
%if %{with_glib}
  -DENABLE_GTK_DOC=ON \
%endif
  -DENABLE_LIBOPENJPEG=openjpeg2 \
  -DENABLE_UNSTABLE_API_ABI_HEADERS=ON \
  -DENABLE_ZLIB=OFF \
  ..

%{__make} %{?_smp_mflags}

%install
%make_install -C build

%check
#make_build test

# verify pkg-config sanity/version
export PKG_CONFIG_PATH="%{buildroot}%{_datadir}/pkgconfig;%{buildroot}%{_libdir}/pkgconfig"
# !!!
# we have to use main_version when available, as the legacy macro screws the version
# !!!
test "$(pkg-config --modversion poppler)" = "%{?main_version}%{!?main_version:%{version}}"
test "$(pkg-config --modversion poppler-cairo)" = "%{?main_version}%{!?main_version:%{version}}"
test "$(pkg-config --modversion poppler-cpp)" = "%{?main_version}%{!?main_version:%{version}}"
%if %{with_glib}
test "$(pkg-config --modversion poppler-glib)" = "%{?main_version}%{!?main_version:%{version}}"
%endif
test "$(pkg-config --modversion poppler-qt4)" = "%{?main_version}%{!?main_version:%{version}}"
test "$(pkg-config --modversion poppler-qt5)" = "%{?main_version}%{!?main_version:%{version}}"
test "$(pkg-config --modversion poppler-splash)" = "%{?main_version}%{!?main_version:%{version}}"

#ldconfig_scriptlets

#ldconfig_scriptlets glib

#ldconfig_scriptlets qt

#ldconfig_scriptlets qt5

#ldconfig_scriptlets cpp

%files
%doc README.md
%license COPYING
%{_libdir}/popple94.dll

%files devel
%{_libdir}/pkgconfig/poppler.pc
%{_libdir}/pkgconfig/poppler-splash.pc
%{_libdir}/poppler_dll.a
%dir %{_includedir}/poppler/
# xpdf headers
%{_includedir}/poppler/*.h
%{_includedir}/poppler/fofi/
%{_includedir}/poppler/goo/
%{_includedir}/poppler/splash/
%if !%{with_glib}
%{_libdir}/pkgconfig/poppler-cairo.pc
%endif

%if %{with_glib}
%files glib
%{_libdir}/popplg*.dll
%{_libdir}/girepository-1.0/Poppler-0.18.typelib

%files glib-devel
%{_libdir}/pkgconfig/poppler-glib.pc
%{_libdir}/pkgconfig/poppler-cairo.pc
%{_libdir}/poppler-glib_dll.a
%{_datadir}/gir-1.0/Poppler-0.18.gir
%{_includedir}/poppler/glib/

%files glib-doc
%license COPYING
%{_datadir}/gtk-doc/
%endif

%files qt
%{_libdir}/poppq4*.dll

%files qt-devel
%{_libdir}/poppler-qt4_dll.a
%{_libdir}/pkgconfig/poppler-qt4.pc
%{_includedir}/poppler/qt4/

%files qt5
%{_libdir}/poppq5*.dll

%files qt5-devel
%{_libdir}/poppler-qt5_dll.a
%{_libdir}/pkgconfig/poppler-qt5.pc
%{_includedir}/poppler/qt5/

%files cpp
%{_libdir}/popplc*.dll

%files cpp-devel
%{_libdir}/pkgconfig/poppler-cpp.pc
%{_libdir}/poppler-cpp_dll.a
%{_includedir}/poppler/cpp

%files utils
%{_bindir}/pdf*.exe
%{_bindir}/text2pdf.exe
%{_mandir}/man1/*


%changelog
* Mon Feb 03 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.84.0-1
- update to vendor version 0.84.0
- adapt the spec to latest fedora spec
- add qt4 backend again like fedora does

* Mon Sep 23 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.61.1-1
- update to vendor version 0.61.1
- include qt5 backend

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