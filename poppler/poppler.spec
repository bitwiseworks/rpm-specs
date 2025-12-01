%global test_sha 03a4b9eb854a06a83c465e82de601796c458bbe9
%global test_date 2021-01-11

%if !0%{?os2_version}
%bcond qt 1

%if %{with qt}
# Enable qt5 support (or not)
# RHEL 10 drops support for Qt5, adds Qt6
%if %{undefined rhel} || 0%{?rhel} < 10
%global qt5 1
%endif
%if %{undefined rhel} || 0%{?rhel} >= 10
%global qt6 1
%endif
%endif
%else
%global qt5 1
%endif

Summary: PDF rendering library
Name:    poppler
Version: 23.11.0
Release: 1%{?dist}
License: (GPLv2 or GPLv3) and GPLv2+ and LGPLv2+ and MIT
URL:     http://poppler.freedesktop.org/
%if !0%{?os2_version}
Source0: http://poppler.freedesktop.org/poppler-%{version}.tar.xz
# git archive --prefix test/
Source1: %{name}-test-%{test_date}-%{test_sha}.tar.xz

Patch1:  poppler-0.90.0-position-independent-code.patch

Patch3:  poppler-21.01.0-glib-introspection.patch

%else
Vendor:  bww bitwise works GmbH
%scm_source github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2
%endif

BuildRequires: cmake
BuildRequires: gcc-c++
BuildRequires: gettext-devel
%if !0%{?os2_version}
BuildRequires: pkgconfig(cairo)
BuildRequires: pkgconfig(cairo-ft)
BuildRequires: pkgconfig(cairo-pdf)
BuildRequires: pkgconfig(cairo-ps)
BuildRequires: pkgconfig(cairo-svg)
%else
BuildRequires: cairo-devel
%endif
BuildRequires: pkgconfig(fontconfig)
BuildRequires: pkgconfig(freetype2)
%if !0%{?os2_version}
BuildRequires: pkgconfig(gdk-pixbuf-2.0)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(gobject-2.0)
BuildRequires: pkgconfig(gobject-introspection-1.0)
BuildRequires: pkgconfig(gtk+-3.0)
BuildRequires: pkgconfig(gtk-doc)
%endif
BuildRequires: pkgconfig(lcms2)
BuildRequires: pkgconfig(libjpeg)
BuildRequires: pkgconfig(libopenjp2)
BuildRequires: pkgconfig(libpng)
BuildRequires: pkgconfig(libtiff-4)
BuildRequires: pkgconfig(nss)
BuildRequires: pkgconfig(poppler-data)
%if 0%{?qt5}
BuildRequires: pkgconfig(Qt5Core)
BuildRequires: pkgconfig(Qt5Gui)
BuildRequires: pkgconfig(Qt5Test)
BuildRequires: pkgconfig(Qt5Widgets)
BuildRequires: pkgconfig(Qt5Xml)
%endif
%if 0%{?qt6}
BuildRequires: cmake(Qt6Core)
BuildRequires: cmake(Qt6Gui)
BuildRequires: cmake(Qt6Test)
BuildRequires: cmake(Qt6Widgets)
BuildRequires: cmake(Qt6Xml)
%endif
%if !0%{?os2_version}
BuildRequires: boost-devel
%endif

Requires: poppler-data

%if !0%{?os2_version}
Obsoletes: poppler-glib-demos < 0.60.1-1
%endif

%description
%{name} is a PDF rendering library.

%package devel
Summary: Libraries and headers for poppler
%if !0%{?os2_version}
Requires: %{name}%{?_isa} = %{version}-%{release}
%else
Requires: %{name} = %{version}-%{release}
%endif

%description devel
You should install the poppler-devel package if you would like to
compile applications based on poppler.

%if !0%{?os2_version}
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

%if 0%{?qt5}
%package qt5
Summary: Qt5 wrapper for poppler
%if !0%{?os2_version}
Requires: %{name}%{?_isa} = %{version}-%{release}
%else
Requires: %{name} = %{version}-%{release}
%endif
Obsoletes: %{name}-qt < 0.90.0-9
%description qt5
%{summary}.

%package qt5-devel
Summary: Development files for Qt5 wrapper
%if !0%{?os2_version}
Requires: %{name}-qt5%{?_isa} = %{version}-%{release}
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
%else
Requires: %{name}-qt5 = %{version}-%{release}
Requires: %{name}-devel = %{version}-%{release}
%endif
Requires: qt5-qtbase-devel
Obsoletes: %{name}-qt-devel < 0.90.0-9
%description qt5-devel
%{summary}.
%endif

%if 0%{?qt6}
%package qt6
Summary: Qt6 wrapper for poppler
Requires: %{name}%{?_isa} = %{version}-%{release}
%description qt6
%{summary}.

%package qt6-devel
Summary: Development files for Qt6 wrapper
Requires: %{name}-qt6%{?_isa} = %{version}-%{release}
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
Requires: qt6-qtbase-devel
%description qt6-devel
%{summary}.
%endif

%package cpp
Summary: Pure C++ wrapper for poppler
%if !0%{?os2_version}
Requires: %{name}%{?_isa} = %{version}-%{release}
%else
Requires: %{name} = %{version}-%{release}
%endif

%description cpp
%{summary}.

%package cpp-devel
Summary: Development files for C++ wrapper
%if !0%{?os2_version}
Requires: %{name}-cpp%{?_isa} = %{version}-%{release}
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
%else
Requires: %{name}-cpp = %{version}-%{release}
Requires: %{name}-devel = %{version}-%{release}
%endif

%description cpp-devel
%{summary}.

%package utils
Summary: Command line utilities for converting PDF files
%if !0%{?os2_version}
Requires: %{name}%{?_isa} = %{version}-%{release}
%else
Requires: %{name} = %{version}-%{release}
%endif
%description utils
Command line tools for manipulating PDF files and converting them to
other formats.

%if 0%{?os2_version}
%legacy_runtime_packages

%debug_package
%endif

%prep
%if !0%{?os2_version}
%autosetup -p1 -b 1
%else
%scm_setup
%endif

chmod -x poppler/CairoFontEngine.cc

%build
%if 0%{?os2_version}
export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"
export LDFLAGS="-Zomf -Zhigh-mem -lcx %{?__global_ldflags}"
export VENDOR="%{vendor}"
%endif

%cmake \
  -DENABLE_CMS=lcms2 \
  -DENABLE_DCTDECODER=libjpeg \
%if !0%{?os2_version}
  -DENABLE_GTK_DOC=ON \
%endif
  -DENABLE_LIBOPENJPEG=openjpeg2 \
%if ! 0%{?qt5}
  -DENABLE_QT5=OFF \
%endif
%if ! 0%{?qt6}
  -DENABLE_QT6=OFF \
%endif
  -DENABLE_UNSTABLE_API_ABI_HEADERS=ON \
  -DENABLE_ZLIB=OFF \
%if 0%{?os2_version}
  -DENABLE_GPGME=OFF \
  -DENABLE_BOOST=OFF \
%endif
  ..
%cmake_build

%install
%cmake_install

%check
%if !0%{?os2_version}
%make_build test
%endif

# verify pkg-config sanity/version
%if !0%{?os2_version}
export PKG_CONFIG_PATH=%{buildroot}%{_datadir}/pkgconfig:%{buildroot}%{_libdir}/pkgconfig
test "$(pkg-config --modversion poppler)" = "%{version}"
test "$(pkg-config --modversion poppler-cpp)" = "%{version}"
test "$(pkg-config --modversion poppler-glib)" = "%{version}"
%if 0%{?qt5}
test "$(pkg-config --modversion poppler-qt5)" = "%{version}"
%endif
%if 0%{?qt6}
test "$(pkg-config --modversion poppler-qt6)" = "%{version}"
%endif
%else
export PKG_CONFIG_PATH="%{buildroot}%{_datadir}/pkgconfig;%{buildroot}%{_libdir}/pkgconfig"
# !!!
# we have to use main_version when available, as the legacy macro screws the version
# !!!
test "$(pkg-config --modversion poppler)" = "%{?main_version}%{!?main_version:%{version}}"
test "$(pkg-config --modversion poppler-cpp)" = "%{?main_version}%{!?main_version:%{version}}"
%if 0%{?qt5}
test "$(pkg-config --modversion poppler-qt5)" = "%{?main_version}%{!?main_version:%{version}}"
%endif
%if 0%{?qt6}
test "$(pkg-config --modversion poppler-qt6)" = "%{?main_version}%{!?main_version:%{version}}"
%endif
%endif

%if !0%{?os2_version}
%ldconfig_scriptlets

%ldconfig_scriptlets glib

%if 0%{?qt5}
%ldconfig_scriptlets qt5
%endif

%if 0%{?qt6}
%ldconfig_scriptlets qt6
%endif

%ldconfig_scriptlets cpp
%endif

%files
%doc README.md
%license COPYING
%if !0%{?os2_version}
%{_libdir}/libpoppler.so.133*
%else
%{_libdir}/poppl133.dll
%endif

%files devel
%{_libdir}/pkgconfig/poppler.pc
%if !0%{?os2_version}
%{_libdir}/libpoppler.so
%else
%{_libdir}/poppler_dll.a
%endif
%dir %{_includedir}/poppler/
# xpdf headers
%{_includedir}/poppler/*.h
%{_includedir}/poppler/fofi/
%{_includedir}/poppler/goo/
%{_includedir}/poppler/splash/

%if !0%{?os2_version}
%files glib
%{_libdir}/libpoppler-glib.so.8*
%{_libdir}/girepository-1.0/Poppler-0.18.typelib

%files glib-devel
%{_libdir}/pkgconfig/poppler-glib.pc
%{_libdir}/libpoppler-glib.so
%{_datadir}/gir-1.0/Poppler-0.18.gir
%{_includedir}/poppler/glib/

%files glib-doc
%license COPYING
%{_datadir}/gtk-doc/
%endif

%if 0%{?qt5}
%files qt5
%if !0%{?os2_version}
%{_libdir}/libpoppler-qt5.so.1*
%else
%{_libdir}/poppq5*.dll
%endif

%files qt5-devel
%if !0%{?os2_version}
%{_libdir}/libpoppler-qt5.so
%else
%{_libdir}/poppler-qt5_dll.a
%endif
%{_libdir}/pkgconfig/poppler-qt5.pc
%{_includedir}/poppler/qt5/
%endif

%if 0%{?qt6}
%files qt6
%{_libdir}/libpoppler-qt6.so.3*

%files qt6-devel
%{_libdir}/libpoppler-qt6.so
%{_libdir}/pkgconfig/poppler-qt6.pc
%{_includedir}/poppler/qt6/
%endif

%files cpp
%if !0%{?os2_version}
%{_libdir}/libpoppler-cpp.so.0*
%else
%{_libdir}/popplc*.dll
%endif

%files cpp-devel
%{_libdir}/pkgconfig/poppler-cpp.pc
%if !0%{?os2_version}
%{_libdir}/libpoppler-cpp.so
%else
%{_libdir}/poppler-cpp_dll.a
%endif
%{_includedir}/poppler/cpp

%files utils
%{_bindir}/pdf*
%if 0%{?os2_version}
%{_bindir}/text2pdf.exe
%exclude %{_bindir}/*.dbg
%endif
%{_mandir}/man1/*

%changelog
* Mon Nov 10 2025 Silvan Scherrer <silvan.scherrer@aroa.ch> - 23.11.0-1
- update to vendor version 23.11.0
- removed qt4 backend
- adapt the spec to latest fedora spec

* Tue Nov 03 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.90.1-1
- update to vendor version 0.90.1
- adapt the spec to latest fedora spec

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