%global qt_module qtmultimedia

# Only compress main Qt DLLs - plugins cannot be compressed as it destroys their QTMETADATA.
# TODO: Enhance _strip_opts to support masks with pathnames and to override LXLITE options for masks.
%global _strip_opts --compress -n "*.exe,Qt5*.dll"

# TODO: our make lacks -O flag, need to fix rpm macros for the time being...
%global make_build %{__make} %{?_smp_mflags}

# TODO: No audio interfaces suported on OS/2 yet.
%global noaudio 1

%if !0%{?noaudio}
%global openal 1

%global gst 0.10
%if 0%{?fedora} || 0%{?rhel} > 7
%global gst 1.0
%endif
%endif

Summary: Qt5 - Multimedia support
Name:    qt5-%{qt_module}
Version: 5.15.2
Release: 1%{?dist}

# See LGPL_EXCEPTIONS.txt, LICENSE.GPL3, respectively, for exception details
License: LGPLv2 with exceptions or GPLv3 with exceptions
Url:     http://www.qt.io
%global majmin %(echo %{version} | cut -d. -f1-2)

# OS/2 is missing from official tarballs and has its own repo.
#Source0: https://download.qt.io/official_releases/qt/%{majmin}/%{version}/submodules/%{qt_module}-everywhere-src-%{version}.tar.xz

Vendor:  bww bitwise works GmbH

%scm_source github https://github.com/bitwiseworks/qtmultimedia-os2 v%{version}-os2-b1
#scm_source git file://D:/Coding/qt5/qt5/qtmultimedia xxxxxxx

# filter plugin/qml/examples provides
%global __provides_exclude_from ^(%{_qt5_qmldir}|%{_qt5_plugindir}|%{_qt5_examplesdir})/.*\\.dll$

BuildRequires: make
BuildRequires: qt5-rpm-macros >= %{version}
BuildRequires: qt5-qtbase-devel >= %{version}
BuildRequires: qt5-qtbase-private-devel
%{?_qt5:Requires: %{_qt5}%{?_isa} = %{_qt5_version}}
BuildRequires: qt5-qtdeclarative-devel >= %{version}
%if !0%{?noaudio}
BuildRequires: pkgconfig(alsa)
%if "%{?gst}" == "0.10"
BuildRequires: pkgconfig(gstreamer-interfaces-0.10)
%endif
BuildRequires: pkgconfig(gstreamer-%{gst})
BuildRequires: pkgconfig(gstreamer-app-%{gst})
BuildRequires: pkgconfig(gstreamer-audio-%{gst})
BuildRequires: pkgconfig(gstreamer-base-%{gst})
BuildRequires: pkgconfig(gstreamer-pbutils-%{gst})
BuildRequires: pkgconfig(gstreamer-plugins-bad-%{gst})
BuildRequires: pkgconfig(gstreamer-video-%{gst})
BuildRequires: pkgconfig(libpulse) pkgconfig(libpulse-mainloop-glib)
%if 0%{?openal}
BuildRequires: pkgconfig(openal)
%endif
BuildRequires: pkgconfig(xv)
# workaround missing dep
# /usr/include/gstreamer-1.0/gst/gl/wayland/gstgldisplay_wayland.h:26:10: fatal error: wayland-client.h: No such file or directory
BuildRequires: wayland-devel
%endif

# To support github tags starting with `v` (nasty github bug!)
BuildRequires: os2-rpm-build >= 1-8
# To pick up SSE2 alignment and no AVX optflags.
BuildRequires: rpm >= 4.13.0-20

%_qt5_examples_package_builddeps

%description
The Qt Multimedia module provides a rich feature set that enables you to
easily take advantage of a platforms multimedia capabilites and hardware.
This ranges from the playback and recording of audio and video content to
the use of available devices like cameras and radios.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt5-qtbase-devel%{?_isa}
Requires: qt5-qtdeclarative-devel%{?_isa}
%if !0%{?noaudio}
# Qt5Multimedia.pc containts:
# Libs.private: ... -lpulse-mainloop-glib -lpulse -lglib-2.0
Requires: pkgconfig(libpulse-mainloop-glib)
%endif
%description devel
%{summary}.

%package examples
Summary: Programming examples for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%_qt5_examples_package_deps
%description examples
%{summary}.

%debug_package


%prep
#setup -q -n %{qt_module}-everywhere-src-%{version}
%scm_setup


%build

# configure expects either a git clone w/o include dir or a source tarball with
# it but we are neither. Pretend we are the former.
test -d .git || mkdir .git

%{qmake_qt5} \
  CONFIG+=git_build \
  GST_VERSION=%{gst}

%make_build


%install
make install INSTALL_ROOT=%{buildroot}

## .prl file love
# nuke .prl reference(s) to %%buildroot
PWD_SAVE=$PWD
cd %{buildroot}%{_qt5_libdir}
for prl_file in *.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
done
cd $PWD_SAVE


%files -f %{debug_package_exclude_files}
%doc README.md CHANGELOG.md
%license LICENSE.*
%{_qt5_libdir}/Qt5MM.dll
%{_qt5_libdir}/Qt5MMQ.dll
%{_qt5_libdir}/Qt5MMW.dll
%if !0%{?noaudio}
%{_qt5_libdir}/Qt5MMGT.dll
%if 0%{?openal}
%{_qt5_archdatadir}/qml/QtAudioEngine/
%endif
%endif
%{_qt5_archdatadir}/qml/QtMultimedia/
%if !0%{?noaudio}
%{_qt5_plugindir}/audio/
%{_qt5_plugindir}/mediaservice/
%endif
%{_qt5_plugindir}/playlistformats/
%dir %{_qt5_libdir}/cmake/Qt5Multimedia/
%{_qt5_libdir}/cmake/Qt5Multimedia/Qt5Multimedia_*Plugin.cmake
%dir %{_qt5_libdir}/cmake/Qt5MultimediaWidgets/

%files devel -f %{debug_package_exclude_files}
%{_qt5_headerdir}/QtMultimedia/
%{_qt5_headerdir}/QtMultimediaQuick/
%{_qt5_headerdir}/QtMultimediaWidgets/
%if !0%{?noaudio}
%{_qt5_headerdir}/QtMultimediaGstTools/
%endif
%{_qt5_libdir}/Qt5Multimedia.lib
%{_qt5_libdir}/Qt5Multimedia.prl
%{_qt5_libdir}/Qt5MultimediaQuick.lib
%{_qt5_libdir}/Qt5MultimediaQuick.prl
%{_qt5_libdir}/Qt5MultimediaWidgets.lib
%{_qt5_libdir}/Qt5MultimediaWidgets.prl
%if !0%{?noaudio}
%{_qt5_libdir}/Qt5MultimediaGstTools.lib
%{_qt5_libdir}/Qt5MultimediaGstTools.prl
%endif
%{_qt5_libdir}/cmake/Qt5Multimedia/Qt5MultimediaConfig*.cmake
%{_qt5_libdir}/cmake/Qt5MultimediaWidgets/Qt5MultimediaWidgetsConfig*.cmake
%if !0%{?noaudio}
%{_qt5_libdir}/cmake/Qt5MultimediaGstTools/Qt5MultimediaGstToolsConfig*.cmake
%endif
%{_qt5_libdir}/cmake/Qt5MultimediaQuick/Qt5MultimediaQuickConfig*.cmake
%{_qt5_libdir}/pkgconfig/Qt5Multimedia.pc
%{_qt5_libdir}/pkgconfig/Qt5MultimediaWidgets.pc
%{_qt5_archdatadir}/mkspecs/modules/*.pri

%if 0%{?_qt5_examplesdir:1}
%files examples -f %{debug_package_exclude_files}
%license LICENSE.FDL
%{_qt5_examplesdir}/
%endif


%changelog
* Wed Sep 22 2021 Dmitriy Kuminov <coding@dmik.org> 5.15.2-1
- Initial release.
