%global qt_module qtwebengine

# TODO: On OS/2, qtwebengine can't be built in one go due to kernel bugs,
# uncommient this to continue from the make step after the make failure.
#global continue_from_make 1

# Only compress main Qt DLLs - plugins cannot be compressed as it destroys their QTMETADATA.
# TODO: Enhance _strip_opts to support masks with pathnames and to override LXLITE options for masks.
%global _strip_opts --compress -n "*.exe,Qt5*.dll"

# TODO: our make lacks -O flag, need to fix rpm macros for the time being...
%global make_build %{__make} %{?_smp_mflags}

# define to build docs, may need to undef this for bootstrapping
# where qt5-qttools (qt5-doctools) builds are not yet available
# TODO: no doctools on OS/2 due to clang depencency (see qt5-qttools.sped)
%global docs 0

%global use_system_libvpx 1
%global use_system_libwebp 1
#global use_system_jsoncpp 1
#global use_system_re2 1
%global use_system_libicu 1
#global use_kerberos 1

# TODO: need on OS/2?
%if !0%{?os2_version}
# the QMake CONFIG flags to force debugging information to be produced in
# release builds, and for all parts of the code
%global debug_config force_debug_info
# webcore_debug v8base_debug
%endif

#global prerelease rc

# spellchecking dictionary directory
%global _qtwebengine_dictionaries_dir %{_qt5_datadir}/qtwebengine_dictionaries

%global rpm_macros_dir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)

# filter plugin/qml/examples provides
%global __provides_exclude_from ^(%{_qt5_qmldir}|%{_qt5_plugindir}|%{_qt5_examplesdir})/.*\\.dll$

Summary: Qt5 - QtWebEngine components
Name:    qt5-%{qt_module}
Version: 5.15.2
Release: 1%{?dist}

# See LICENSE.GPL LICENSE.LGPL LGPL_EXCEPTION.txt, for details
# See also http://qt-project.org/doc/qt-5.0/qtdoc/licensing.html
# The other licenses are from Chromium and the code it bundles
License: (LGPLv2 with exceptions or GPLv3 with exceptions) and BSD and LGPLv2+ and ASL 2.0 and IJG and MIT and GPLv2+ and ISC and OpenSSL and (MPLv1.1 or GPLv2 or LGPLv2)
URL:     http://www.qt.io

# leaned tarball with patent-encumbered codecs removed from the bundled FFmpeg
# wget http://download.qt.io/official_releases/qt/5.15/5.15.1/submodules/qtwebengine-everywhere-src-5.15.1.tar.xz
# ./clean_qtwebengine.sh 5.15.1
#Source0: qtwebengine-everywhere-src-%{version}-clean.tar.xz

Vendor:  bww bitwise works GmbH

# TODO: Can't use scm macros atm because of the chromium submodule! Use a pre-packed
# zip using the following command on a fully prepared local git tree (assuming it is
# cloned to a directory named qtwebengine and changing to it):
#   ver=`grep -m1 '#### Version' CHANGELOG.md | sed -E 's/^#### Version ([0-9]+\.[0-9]+\.[0-9]+) .*/\1/'`
#   commit=`git rev-parse --short HEAD`
#   tag=`git describe --tags $commit`
#   [ -z "$tag" ] && tag="$ver-$commit"
#   cd .. && zip -rX9 qt5-qtwebengine-$tag.zip qtwebengine -x '*/.git/*'
#scm_source github https://github.com/bitwiseworks/qtwebengie-os2 v%{version}-os2-b1
#scm_source git file://D:/Coding/qt5/qt5/qtwebengine xxxxxxx
Source0: qt5-qtwebengine-v%{version}-os2-b1.zip

# macros
Source10: macros.qt5-qtwebengine

# handled by qt5-srpm-macros, which defines %%qt5_qtwebengine_arches
ExclusiveArch: %{qt5_qtwebengine_arches}

BuildRequires: make
BuildRequires: qt5-rpm-macros >= %{version}
BuildRequires: qt5-srpm-macros >= %{version}
BuildRequires: qt5-qtbase-devel
BuildRequires: qt5-qtbase-private-devel
# TODO: check of = is really needed or if >= would be good enough -- rex
%{?_qt5:Requires: %{_qt5}%{?_isa} = %{_qt5_version}}
BuildRequires: qt5-qtdeclarative-devel
%if !0%{?os2_version}
BuildRequires: qt5-qtxmlpatterns-devel
BuildRequires: qt5-qtlocation-devel
BuildRequires: qt5-qtsensors-devel
%endif
BuildRequires: qt5-qtsvg-devel
BuildRequires: qt5-qtwebchannel-devel
BuildRequires: qt5-qttools-static
%if !0%{?os2_version}
# for examples?
BuildRequires: qt5-qtquickcontrols2-devel
BuildRequires: ninja-build
%endif
BuildRequires: cmake
BuildRequires: bison
BuildRequires: flex
BuildRequires: gcc-c++
%if !0%{?os2_version}
# gn links statically (for now)
BuildRequires: libstdc++-static
%endif
BuildRequires: git-core
BuildRequires: gperf
%if 0%{?use_kerberos}
BuildRequires: krb5-devel
%endif
%if 0%{?use_system_libicu}
BuildRequires: libicu-devel >= 65
%endif
BuildRequires: libjpeg-devel
%if !0%{?os2_version}
BuildRequires: nodejs
%endif
%if 0%{?use_system_re2}
BuildRequires: re2-devel
%endif
%if !0%{?os2_version}
BuildRequires: snappy-devel
%endif
%ifarch %{ix86} x86_64
%if !0%{?os2_version}
BuildRequires: yasm
%else
BuildRequires: nasm
%endif
%endif
BuildRequires: pkgconfig(expat)
BuildRequires: pkgconfig(gobject-2.0)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(fontconfig)
BuildRequires: pkgconfig(freetype2)
%if !0%{?os2_version}
BuildRequires: pkgconfig(gl)
BuildRequires: pkgconfig(egl)
%endif
%if 0%{?use_system_jsoncpp}
BuildRequires: pkgconfig(jsoncpp)
%endif
BuildRequires: pkgconfig(libpng)
%if !0%{?os2_version}
BuildRequires: pkgconfig(libudev)
%endif
%if 0%{?use_system_libwebp}
BuildRequires: pkgconfig(libwebp) >= 0.6.0
%endif
%if !0%{?os2_version}
BuildRequires: pkgconfig(harfbuzz)
BuildRequires: pkgconfig(libdrm)
%endif
BuildRequires: pkgconfig(opus)
%if !0%{?os2_version}
BuildRequires: pkgconfig(protobuf)
%endif
BuildRequires: pkgconfig(libevent)
%if !0%{?os2_version}
BuildRequires: pkgconfig(poppler-cpp)
%endif
BuildRequires: pkgconfig(zlib)
%if (0%{?fedora} && 0%{?fedora} < 30) || 0%{?os2_version}
BuildRequires: pkgconfig(minizip)
%else
BuildConflicts: minizip-devel
Provides: bundled(minizip) = 1.2
%endif
%if !0%{?os2_version}
BuildRequires: pkgconfig(x11)
BuildRequires: pkgconfig(xi)
BuildRequires: pkgconfig(xcursor)
BuildRequires: pkgconfig(xext)
BuildRequires: pkgconfig(xfixes)
BuildRequires: pkgconfig(xrender)
BuildRequires: pkgconfig(xdamage)
BuildRequires: pkgconfig(xcomposite)
BuildRequires: pkgconfig(xtst)
BuildRequires: pkgconfig(xrandr)
BuildRequires: pkgconfig(xscrnsaver)
BuildRequires: pkgconfig(libcap)
BuildRequires: pkgconfig(libpulse)
BuildRequires: pkgconfig(alsa)
BuildRequires: pkgconfig(libpci)
%endif
BuildRequires: pkgconfig(dbus-1)
BuildRequires: pkgconfig(nss)
BuildRequires: pkgconfig(lcms2)
%if !0%{?os2_version}
BuildRequires: pkgconfig(xkbcommon)
BuildRequires: pkgconfig(xkbfile)
%endif
BuildRequires: pkgconfig(libxslt) pkgconfig(libxml-2.0)
%if !0%{?os2_version}
BuildRequires: perl-interpreter
%endif
# fesco exception to allow python2 use: https://pagure.io/fesco/issue/2208
# per https://fedoraproject.org/wiki/Changes/RetirePython2#FESCo_exceptions
# Only the interpreter is needed
%if 0%{?fedora} > 29 || 0%{?rhel} > 8 || !0%{?os2_version}
BuildRequires: %{__python2}
%else
BuildRequires: python2
BuildRequires: python2-rpm-macros
%endif
%if 0%{?use_system_libvpx}
BuildRequires: pkgconfig(vpx) >= 1.8.0
%endif
%if 0%{?os2_version}
BuildRequires: gettext-devel
BuildRequires: libssp-devel
BuildRequires: ffmpeg-devel
BuildRequires: pthread-devel >= 2:0.2.2
BuildRequires: libkai-devel >= 2.0.0
BuildRequires: pango-devel
BuildRequires: os2tk45-headers
BuildRequires: highmem
%endif

# extra (non-upstream) functions needed, see
# src/3rdparty/chromium/third_party/sqlite/README.chromium for details
#BuildRequires: pkgconfig(sqlite3)

## Various bundled libraries that Chromium does not support unbundling :-(
## Only the parts actually built are listed.
## Query for candidates:
## grep third_party/ build.log | sed 's!third_party/!\nthird_party/!g' | \
## grep third_party/ | sed 's!^third_party/!!g' | sed 's!/.*$!!g' | \
## sed 's/\;.*$//g' | sed 's/ .*$//g' | sort | uniq | less
## some false positives where only shim headers are generated for some reason
## some false positives with dummy placeholder dirs (swiftshader, widevine)
## some false negatives where a header-only library is bundled (e.g. x86inc)
## Spot's chromium.spec also has a list that I checked.

# Of course, Chromium itself is bundled. It cannot be unbundled because it is
# not a library, but forked (modified) application code.
# Lives in src/3rdparty/chromium/chrome/VERSION.
Provides: bundled(chromium) = 83.0.4103.122

# Bundled in src/3rdparty/chromium/third_party:
# Check src/3rdparty/chromium/third_party/*/README.chromium for version numbers,
# except where specified otherwise.
Provides: bundled(angle) = 2422
# Google's fork of OpenSSL
# We cannot build against NSS instead because it no longer works with NSS 3.21:
# HTTPS on, ironically, Google's sites (Google, YouTube, etc.) stops working
# completely and produces only ERR_SSL_PROTOCOL_ERROR errors:
# http://kaosx.us/phpBB3/viewtopic.php?t=1235
# https://bugs.launchpad.net/ubuntu/+source/chromium-browser/+bug/1520568
# So we have to do what Chromium now defaults to (since 47): a "chimera build",
# i.e., use the BoringSSL code and the system NSS certificates.
Provides: bundled(boringssl)
Provides: bundled(brotli)
%if !0%{?os2_version}
# Don't get too excited. MPEG and other legally problematic stuff is stripped
# out. See clean_qtwebengine.sh, clean_ffmpeg.sh, and
# get_free_ffmpeg_source_files.py.
# see src/3rdparty/chromium/third_party/ffmpeg/Changelog for the version number
Provides: bundled(ffmpeg) = 4.2
%endif
Provides: bundled(hunspell) = 1.6.0
Provides: bundled(iccjpeg)
# bundled as "khronos", headers only
Provides: bundled(khronos_headers)
# bundled as "leveldatabase"
Provides: bundled(leveldb) = 1.22
# bundled as "libjingle_xmpp"
Provides: bundled(libjingle)
# see src/3rdparty/chromium/third_party/libsrtp/CHANGES for the version number
Provides: bundled(libsrtp) = 2.2.0
%if !0%{?use_system_libvpx}
# claims "Version: 1.6.0", but according to the fine print, this is actually a
# snapshot from master from after the 1.6.1 release
Provides: bundled(libvpx) = 1.8.2
%endif
%if !0%{?use_system_libwebp}
Provides: bundled(libwebp) = 1.1.0
%endif
%if !0%{?os2_version}
# bundled as "libxml"
# see src/3rdparty/chromium/third_party/libxml/linux/include/libxml/xmlversion.h
Provides: bundled(libxml2) = 2.9.9
# see src/3rdparty/chromium/third_party/libxslt/linux/config.h for version
Provides: bundled(libxslt) = 1.1.34
%endif
Provides: bundled(libXNVCtrl) = 302.17
Provides: bundled(libyuv) = 1741
Provides: bundled(modp_b64)
#Provides: bundled(openmax_dl) = 1.0.2
Provides: bundled(ots)
# see src/3rdparty/chromium/third_party/protobuf/CHANGES.txt for the version
#Provides: bundled(protobuf) = 3.0.0-0.1.beta3
Provides: bundled(qcms) = 4
Provides: bundled(sfntly)
Provides: bundled(skia)
# bundled as "smhasher"
Provides: bundled(SMHasher) = 0-0.1.svn147
Provides: bundled(sqlite) = 3.31.1
Provides: bundled(usrsctp)
Provides: bundled(webrtc) = 90

%ifarch %{ix86} x86_64
# bundled by ffmpeg and libvpx:
# header (for assembly) only
Provides: bundled(x86inc)
%endif

# Bundled in src/3rdparty/chromium/base/third_party:
# Check src/3rdparty/chromium/third_party/base/*/README.chromium for version
# numbers, except where specified otherwise.
#Provides: bundled(dmg_fp)
Provides: bundled(dynamic_annotations) = 4384
Provides: bundled(superfasthash) = 0
Provides: bundled(symbolize)
%if !0%{?os2_version}
# bundled as "valgrind", headers only
Provides: bundled(valgrind.h)
%endif
# bundled as "xdg_mime"
Provides: bundled(xdg-mime)
# bundled as "xdg_user_dirs"
Provides: bundled(xdg-user-dirs) = 0.10

# Bundled in src/3rdparty/chromium/net/third_party:
# Check src/3rdparty/chromium/third_party/net/*/README.chromium for version
# numbers, except where specified otherwise.
Provides: bundled(mozilla_security_manager) = 1.9.2

# Bundled in src/3rdparty/chromium/url/third_party:
# Check src/3rdparty/chromium/third_party/url/*/README.chromium for version
# numbers, except where specified otherwise.
# bundled as "mozilla", file renamed and modified
Provides: bundled(nsURLParsers)

# Bundled outside of third_party, apparently not considered as such by Chromium:
Provides: bundled(mojo)
# see src/3rdparty/chromium/v8/include/v8_version.h for the version number
Provides: bundled(v8) = 8.3.110.13
# bundled by v8 (src/3rdparty/chromium/v8/src/base/ieee754.cc)
# The version number is 5.3, the last version that upstream released, years ago:
# http://www.netlib.org/fdlibm/readme
Provides: bundled(fdlibm) = 5.3

%{?_qt5_version:Requires: qt5-qtbase%{?_isa} = %{_qt5_version}}

%if 0%{?use_system_icu}
# Those versions were built with bundled ICU and want the data file.
Conflicts: qt5-qtwebengine-freeworld < 5.15.2-2
%endif

# To support github tags starting with `v` (nasty github bug!)
BuildRequires: os2-rpm-build >= 1-8
# To pick up SSE2 alignment and no AVX optflags.
BuildRequires: rpm >= 4.13.0-20

%_qt5_examples_package_builddeps

%description
%{summary}.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt5-qtbase-devel%{?_isa}
Requires: qt5-qtdeclarative-devel%{?_isa}
# not arch'd for now, see if can get away with avoiding multilib'ing -- rex
Requires: %{name}-devtools = %{version}-%{release}
%description devel
%{summary}.

%package devtools
Summary: WebEngine devtools_resources
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devtools
Support for remote debugging.

%package examples
Summary: Example files for %{name}
%_qt5_examples_package_deps
%description examples
%{summary}.

%debug_package


%if 0%{?docs}
%package doc
Summary: API documentation for %{name}
BuildRequires: qt5-qdoc
BuildRequires: qt5-qhelpgenerator
BuildRequires: qt5-qtbase-doc
Requires: qt5-qtbase-doc
BuildRequires: qt5-qtxmlpatterns-doc
Requires: qt5-qtxmlpatterns-doc
BuildRequires: qt5-qtdeclarative-doc
Requires: qt5-qtdeclarative-doc
BuildArch: noarch
%description doc
%{summary}.
%endif


%prep
%if 0%{continue_from_make}
%global _fixperms %{nil}
%setup -n %{qt_module} -TDc
%else
#setup -q -n %{qt_module}-everywhere-src-%{version}%{?prerelease:-%{prerelease}} -a20
#scm_setup
%setup -q -n %{qt_module}

%if 0%{?use_system_re2}
# http://bugzilla.redhat.com/1337585
# can't just delete, but we'll overwrite with system headers to be on the safe side
cp -bv /usr/include/re2/*.h src/3rdparty/chromium/third_party/re2/src/re2/
%endif

%if 0
#ifarch x86_64
# enable this to force -g2 on x86_64 (most arches run out of memory with -g2)
# DISABLED BECAUSE OF:
# /usr/lib/rpm/find-debuginfo.sh: line 188:  3619 Segmentation fault
# (core dumped) eu-strip --remove-comment $r $g -f "$1" "$2"
sed -i -e 's/symbol_level=1/symbol_level=2/g' src/core/config/common.pri
%endif

%if 0%{?docs}
# generate qtwebengine-3rdparty.qdoc, it is missing from the tarball
PWD_SAVE=$PWD
cd src/3rdparty
%{__python2} chromium/tools/licenses.py \
  --file-template ../../tools/about_credits.tmpl \
  --entry-template ../../tools/about_credits_entry.tmpl \
  credits >../webengine/doc/src/qtwebengine-3rdparty.qdoc
cd $PWD_SAVE
%endif

# copy the Chromium license so it is installed with the appropriate name
cp -p src/3rdparty/chromium/LICENSE LICENSE.Chromium

%if !0%{?os2_version}
# consider doing this as part of the tarball creation step instead?  rdieter
# fix/workaround
# fatal error: QtWebEngineCore/qtwebenginecoreglobal.h: No such file or directory
if [ ! -f "./include/QtWebEngineCore/qtwebenginecoreglobal.h" ]; then
%_qt5_bindir/syncqt.pl -version %{version}
fi

# abort if this doesn't get created by syncqt.pl
test -f "./include/QtWebEngineCore/qtwebenginecoreglobal.h"
%endif
%endif

%build

%if !0%{continue_from_make}
# configure expects either a git clone w/o include dir or a source tarball with
# it but we are neither. Pretend we are the former.
test -d .git || mkdir .git

%if !0%{?os2_version}
export STRIP=strip
export NINJAFLAGS="%{__ninja_common_opts}"
export NINJA_PATH=%{__ninja}
%else
# GCC may run out of memory on some files when building Chromium with more jobs.
export NINJAJOBS="-j2"
%endif

%{qmake_qt5} \
  %{?debug_config:CONFIG+="%{debug_config}"} \
  %{?use_system_libicu:QMAKE_EXTRA_ARGS+="-system-webengine-icu"} \
  QMAKE_EXTRA_ARGS+="%{?use_kerberos:-webengine-kerberos }-webengine-proprietary-codecs" \
  .
%endif

# avoid %%make_build for now, the -O flag buffers output from intermediate build steps done via ninja
make %{?_smp_mflags}

%if 0%{?docs}
%make_build docs
%endif

%install
make install INSTALL_ROOT=%{buildroot}

%if 0%{?docs}
make install_docs INSTALL_ROOT=%{buildroot}
%endif

# rpm macros
install -p -m644 -D %{SOURCE10} \
  %{buildroot}%{rpm_macros_dir}/macros.qt5-qtwebengine
sed -i \
  -e "s|@@NAME@@|%{name}|g" \
  -e "s|@@EPOCH@@|%{?epoch}%{!?epoch:0}|g" \
  -e "s|@@VERSION@@|%{version}|g" \
  -e "s|@@EVR@@|%{?epoch:%{epoch:}}%{version}-%{release}|g" \
  %{buildroot}%{rpm_macros_dir}/macros.qt5-qtwebengine

## .prl file love
# nuke .prl reference(s) to %%buildroot
PWD_SAVE=$PWD
cd %{buildroot}%{_qt5_libdir}
for prl_file in Qt5*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
done
cd $PWD_SAVE

mkdir -p %{buildroot}%{_qtwebengine_dictionaries_dir}

# adjust cmake dep(s) to allow for using the same Qt5 that was used to build it
# using the lesser of %%version, %%_qt5_version
%global lesser_version $(echo -e "%{version}\\n%{_qt5_version}" | sort -V | head -1)
sed -i -e "s|%{version} \${_Qt5WebEngine|%{lesser_version} \${_Qt5WebEngine|" \
  %{buildroot}%{_qt5_libdir}/cmake/Qt5WebEngine*/Qt5WebEngine*Config.cmake


%if !0%{?os2_version}
%filetriggerin -- %{_datadir}/myspell
while read filename ; do
  case "$filename" in
    *.dic)
      bdicname=%{_qtwebengine_dictionaries_dir}/`basename -s .dic "$filename"`.bdic
      %{_qt5_bindir}/qwebengine_convert_dict "$filename" "$bdicname" &> /dev/null || :
      ;;
  esac
done
%endif

# mark the chromium DLL for high mem, otherwise it won't last for long at runtime
highmem -c %{buildroot}%{_qt5_libdir}/Qt5WebC.dll

%files -f %{debug_package_exclude_files}
%doc README*.md CHANGELOG.md
%license LICENSE.*
%if 0%{?docs}
%license src/webengine/doc/src/qtwebengine-3rdparty.qdoc
%endif
%{_qt5_libdir}/Qt5*.dll
%{_qt5_bindir}/qwebengine_convert_dict.exe
%{_qt5_libdir}/qt5/qml/*
%{_qt5_libdir}/qt5/libexec/QtWebEngineProcess.exe
%{_qt5_plugindir}/designer/qtwebv.dll
%{_qt5_plugindir}/imageformats/qpdf.dll
%dir %{_qt5_datadir}/resources/
%if ! 0%{?use_system_libicu}
%{_qt5_datadir}/resources/icudtl.dat
%endif
%{_qt5_datadir}/resources/qtwebengine_resources_100p.pak
%{_qt5_datadir}/resources/qtwebengine_resources_200p.pak
%{_qt5_datadir}/resources/qtwebengine_resources.pak
%dir %{_qtwebengine_dictionaries_dir}
%dir %{_qt5_translationdir}/qtwebengine_locales
%lang(am) %{_qt5_translationdir}/qtwebengine_locales/am.pak
%lang(ar) %{_qt5_translationdir}/qtwebengine_locales/ar.pak
%lang(bg) %{_qt5_translationdir}/qtwebengine_locales/bg.pak
%lang(bn) %{_qt5_translationdir}/qtwebengine_locales/bn.pak
%lang(ca) %{_qt5_translationdir}/qtwebengine_locales/ca.pak
%lang(cs) %{_qt5_translationdir}/qtwebengine_locales/cs.pak
%lang(da) %{_qt5_translationdir}/qtwebengine_locales/da.pak
%lang(de) %{_qt5_translationdir}/qtwebengine_locales/de.pak
%lang(el) %{_qt5_translationdir}/qtwebengine_locales/el.pak
%lang(en) %{_qt5_translationdir}/qtwebengine_locales/en-GB.pak
%lang(en) %{_qt5_translationdir}/qtwebengine_locales/en-US.pak
%lang(es) %{_qt5_translationdir}/qtwebengine_locales/es-419.pak
%lang(es) %{_qt5_translationdir}/qtwebengine_locales/es.pak
%lang(et) %{_qt5_translationdir}/qtwebengine_locales/et.pak
%lang(fa) %{_qt5_translationdir}/qtwebengine_locales/fa.pak
%lang(fi) %{_qt5_translationdir}/qtwebengine_locales/fi.pak
%lang(fil) %{_qt5_translationdir}/qtwebengine_locales/fil.pak
%lang(fr) %{_qt5_translationdir}/qtwebengine_locales/fr.pak
%lang(gu) %{_qt5_translationdir}/qtwebengine_locales/gu.pak
%lang(he) %{_qt5_translationdir}/qtwebengine_locales/he.pak
%lang(hi) %{_qt5_translationdir}/qtwebengine_locales/hi.pak
%lang(hr) %{_qt5_translationdir}/qtwebengine_locales/hr.pak
%lang(hu) %{_qt5_translationdir}/qtwebengine_locales/hu.pak
%lang(id) %{_qt5_translationdir}/qtwebengine_locales/id.pak
%lang(it) %{_qt5_translationdir}/qtwebengine_locales/it.pak
%lang(ja) %{_qt5_translationdir}/qtwebengine_locales/ja.pak
%lang(kn) %{_qt5_translationdir}/qtwebengine_locales/kn.pak
%lang(ko) %{_qt5_translationdir}/qtwebengine_locales/ko.pak
%lang(lt) %{_qt5_translationdir}/qtwebengine_locales/lt.pak
%lang(lv) %{_qt5_translationdir}/qtwebengine_locales/lv.pak
%lang(ml) %{_qt5_translationdir}/qtwebengine_locales/ml.pak
%lang(mr) %{_qt5_translationdir}/qtwebengine_locales/mr.pak
%lang(ms) %{_qt5_translationdir}/qtwebengine_locales/ms.pak
%lang(nb) %{_qt5_translationdir}/qtwebengine_locales/nb.pak
%lang(nl) %{_qt5_translationdir}/qtwebengine_locales/nl.pak
%lang(pl) %{_qt5_translationdir}/qtwebengine_locales/pl.pak
%lang(pt_BR) %{_qt5_translationdir}/qtwebengine_locales/pt-BR.pak
%lang(pt_PT) %{_qt5_translationdir}/qtwebengine_locales/pt-PT.pak
%lang(ro) %{_qt5_translationdir}/qtwebengine_locales/ro.pak
%lang(ru) %{_qt5_translationdir}/qtwebengine_locales/ru.pak
%lang(sk) %{_qt5_translationdir}/qtwebengine_locales/sk.pak
%lang(sl) %{_qt5_translationdir}/qtwebengine_locales/sl.pak
%lang(sr) %{_qt5_translationdir}/qtwebengine_locales/sr.pak
%lang(sv) %{_qt5_translationdir}/qtwebengine_locales/sv.pak
%lang(sw) %{_qt5_translationdir}/qtwebengine_locales/sw.pak
%lang(ta) %{_qt5_translationdir}/qtwebengine_locales/ta.pak
%lang(te) %{_qt5_translationdir}/qtwebengine_locales/te.pak
%lang(th) %{_qt5_translationdir}/qtwebengine_locales/th.pak
%lang(tr) %{_qt5_translationdir}/qtwebengine_locales/tr.pak
%lang(uk) %{_qt5_translationdir}/qtwebengine_locales/uk.pak
%lang(vi) %{_qt5_translationdir}/qtwebengine_locales/vi.pak
%lang(zh_CN) %{_qt5_translationdir}/qtwebengine_locales/zh-CN.pak
%lang(zh_TW) %{_qt5_translationdir}/qtwebengine_locales/zh-TW.pak

%files devel -f %{debug_package_exclude_files}
%{rpm_macros_dir}/macros.qt5-qtwebengine
%{_qt5_headerdir}/Qt*/
%{_qt5_libdir}/Qt5*.lib
%{_qt5_libdir}/Qt5*.prl
%{_qt5_libdir}/cmake/Qt5*/
%{_qt5_libdir}/pkgconfig/Qt5*.pc
%{_qt5_archdatadir}/mkspecs/modules/*.pri

%files devtools -f %{debug_package_exclude_files}
%{_qt5_datadir}/resources/qtwebengine_devtools_resources.pak

%files examples -f %{debug_package_exclude_files}
%{_qt5_examplesdir}/

%if 0%{?docs}
%files doc
%{_qt5_docdir}/*
%endif


%changelog
* Wed Sep 22 2021 Dmitriy Kuminov <coding@dmik.org> 5.15.2-1
- Initial release.
