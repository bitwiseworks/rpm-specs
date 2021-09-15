%global qt_module qtwebengine

%global _hardened_build 1

# define to build docs, may need to undef this for bootstrapping
# where qt5-qttools (qt5-doctools) builds are not yet available
%global docs 1

%if 0%{?fedora}
# need libvpx >= 1.8.0 (need commit 297dfd869609d7c3c5cd5faa3ebc7b43a394434e)
%global use_system_libvpx 1
%endif
%if 0%{?fedora} > 30 || 0%{?epel} > 7
# need libwebp >= 0.6.0
%global use_system_libwebp 1
%global use_system_jsoncpp 1
%global use_system_re2 1
%endif

%if 0%{?fedora} > 32
# need libicu >= 65, only currently available on f33+
%global use_system_libicu 1
%endif

# NEON support on ARM (detected at runtime) - disable this if you are hitting
# FTBFS due to e.g. GCC bug https://bugzilla.redhat.com/show_bug.cgi?id=1282495
#global arm_neon 1

# the QMake CONFIG flags to force debugging information to be produced in
# release builds, and for all parts of the code
%ifarch %{arm} aarch64
# the ARM builder runs out of memory during linking with the full setting below,
# so omit debugging information for the parts upstream deems it dispensable for
# (webcore, v8base)
%global debug_config %{nil}
%else
%global debug_config force_debug_info
# webcore_debug v8base_debug
%endif

#global prerelease rc

# spellchecking dictionary directory
%global _qtwebengine_dictionaries_dir %{_qt5_datadir}/qtwebengine_dictionaries

%global rpm_macros_dir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)

# exclude plugins
%global __provides_exclude ^lib.*plugin\\.so.*$
# and designer plugins
%global __provides_exclude_from ^%{_qt5_plugindir}/.*\\.so$

Summary: Qt5 - QtWebEngine components
Name:    qt5-qtwebengine
Version: 5.15.6
Release: 1%{?dist}

# See LICENSE.GPL LICENSE.LGPL LGPL_EXCEPTION.txt, for details
# See also http://qt-project.org/doc/qt-5.0/qtdoc/licensing.html
# The other licenses are from Chromium and the code it bundles
License: (LGPLv2 with exceptions or GPLv3 with exceptions) and BSD and LGPLv2+ and ASL 2.0 and IJG and MIT and GPLv2+ and ISC and OpenSSL and (MPLv1.1 or GPLv2 or LGPLv2)
URL:     http://www.qt.io
# leaned tarball with patent-encumbered codecs removed from the bundled FFmpeg
# wget http://download.qt.io/official_releases/qt/5.15/5.15.1/submodules/qtwebengine-everywhere-src-5.15.1.tar.xz
# ./clean_qtwebengine.sh 5.15.1
Source0: qtwebengine-everywhere-src-%{version}-clean.tar.xz
# cleanup scripts used above
Source1: clean_qtwebengine.sh
Source2: clean_ffmpeg.sh
Source3: get_free_ffmpeg_source_files.py
# macros
Source10: macros.qt5-qtwebengine

# pulseaudio headers
Source20: pulseaudio-12.2-headers.tar.gz

# some tweaks to linux.pri (system yasm, link libpci, run unbundling script)
# FIXME/TODO: review, I *think* this is no longer needed -- rdieter
Patch0:  qtwebengine-everywhere-src-5.10.0-linux-pri.patch
# quick hack to avoid checking for the nonexistent icudtl.dat and silence the
# resulting warnings - not upstreamable as is because it removes the fallback
# mechanism for the ICU data directory (which is not used in our builds because
# we use the system ICU, which embeds the data statically) completely
Patch1:  qtwebengine-everywhere-src-5.15.0-no-icudtl-dat.patch
# fix extractCFlag to also look in QMAKE_CFLAGS_RELEASE, needed to detect the
# ARM flags with our %%qmake_qt5 macro, including for the next patch
Patch2:  qtwebengine-opensource-src-5.12.4-fix-extractcflag.patch
# disable NEON vector instructions on ARM where the NEON code FTBFS due to
# GCC bug https://bugzilla.redhat.com/show_bug.cgi?id=1282495
Patch3:  qtwebengine-opensource-src-5.9.0-no-neon.patch
# workaround FTBFS against kernel-headers-5.2.0+
Patch4:  qtwebengine-SIOCGSTAMP.patch
#  fix build when using qt < 5.14
Patch5:  qtwebengine-5.15.0-QT_DEPRECATED_VERSION.patch
# remove Android dependencies from openmax_dl ARM NEON detection (detect.c)
Patch10: qtwebengine-opensource-src-5.9.0-openmax-dl-neon.patch
# Fix/workaround FTBFS on aarch64 with newer glibc
Patch24: qtwebengine-everywhere-src-5.11.3-aarch64-new-stat.patch
# Use Python2
Patch26: qtwebengine-everywhere-5.15.5-use-python2.patch
# Fix sandbox issue breaking text rendering with glibc >= 2.33 (#1904652)
# https://bugs.chromium.org/p/chromium/issues/detail?id=1164975
Patch28: qtwebengine-everywhere-src-5.15.5-#1904652.patch
# Fix sandbox issue on 32-bit architectures with glibc >= 2.31 (from Debian)
Patch29: qtwebengine-everywhere-src-5.15.5-sandbox-time64-syscalls.patch
# don't assume type-ness of SIGSTKSZ,
# https://bugzilla.redhat.com/show_bug.cgi?id=1945595
Patch30: qtwebengine-everywhere-src-5.15.5-SIGSTKSZ.patch
# FTBFS TRUE/FALSE undeclared
Patch31: qtwebengine-everywhere-src-5.15.5-TRUE.patch
# Issue 1213452: Sandbox doesn't work with clone3
# https://bugs.chromium.org/p/chromium/issues/detail?id=1213452
Patch32: qtwebengine-everywhere-src-5.15.6-clone3.patch

## Upstream patches:

%if 0%{?fedora} || 0%{?epel} > 7
# handled by qt5-srpm-macros, which defines %%qt5_qtwebengine_arches
ExclusiveArch: %{qt5_qtwebengine_arches}
%endif

BuildRequires: make
BuildRequires: qt5-qtbase-devel
BuildRequires: qt5-qtbase-private-devel
# TODO: check of = is really needed or if >= would be good enough -- rex
%{?_qt5:Requires: %{_qt5}%{?_isa} = %{_qt5_version}}
BuildRequires: qt5-qtdeclarative-devel
BuildRequires: qt5-qtxmlpatterns-devel
BuildRequires: qt5-qtlocation-devel
BuildRequires: qt5-qtsensors-devel
BuildRequires: qt5-qtsvg-devel
BuildRequires: qt5-qtwebchannel-devel
BuildRequires: qt5-qttools-static
# for examples?
BuildRequires: qt5-qtquickcontrols2-devel
BuildRequires: ninja-build
BuildRequires: cmake
BuildRequires: bison
BuildRequires: flex
BuildRequires: gcc-c++
# gn links statically (for now)
BuildRequires: libstdc++-static
BuildRequires: git-core
BuildRequires: gperf
BuildRequires: krb5-devel
%if 0%{?use_system_libicu}
BuildRequires: libicu-devel >= 65
%endif
BuildRequires: libjpeg-devel
BuildRequires: nodejs
%if 0%{?use_system_re2}
BuildRequires: re2-devel
%endif
BuildRequires: snappy-devel
%ifarch %{ix86} x86_64
BuildRequires: yasm
%endif
BuildRequires: pkgconfig(expat)
BuildRequires: pkgconfig(gobject-2.0)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(fontconfig)
BuildRequires: pkgconfig(freetype2)
BuildRequires: pkgconfig(gl)
BuildRequires: pkgconfig(egl)
%if 0%{?use_system_jsoncpp}
BuildRequires: pkgconfig(jsoncpp)
%endif
BuildRequires: pkgconfig(libpng)
BuildRequires: pkgconfig(libudev)
%if 0%{?use_system_libwebp}
BuildRequires: pkgconfig(libwebp) >= 0.6.0
%endif
BuildRequires: pkgconfig(harfbuzz)
BuildRequires: pkgconfig(libdrm)
BuildRequires: pkgconfig(opus)
BuildRequires: pkgconfig(protobuf)
BuildRequires: pkgconfig(libevent)
BuildRequires: pkgconfig(poppler-cpp)
BuildRequires: pkgconfig(zlib)
%if 0%{?fedora} && 0%{?fedora} < 30
BuildRequires: pkgconfig(minizip)
%else
BuildConflicts: minizip-devel
Provides: bundled(minizip) = 1.2
%endif
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
BuildRequires: pkgconfig(dbus-1)
BuildRequires: pkgconfig(nss)
BuildRequires: pkgconfig(lcms2)
BuildRequires: pkgconfig(xkbcommon)
BuildRequires: pkgconfig(xkbfile)
## https://bugreports.qt.io/browse/QTBUG-59094
## requires libxml2 built with icu support
#BuildRequires: pkgconfig(libxslt) pkgconfig(libxml-2.0)
BuildRequires: perl-interpreter
# fesco exception to allow python2 use: https://pagure.io/fesco/issue/2208
# per https://fedoraproject.org/wiki/Changes/RetirePython2#FESCo_exceptions
# Only the interpreter is needed
%if 0%{?fedora} > 29 || 0%{?rhel} > 8
BuildRequires: %{__python2}
%else
BuildRequires: python2
BuildRequires: python2-rpm-macros
%endif
%if 0%{?use_system_libvpx}
BuildRequires: pkgconfig(vpx) >= 1.8.0
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
Provides: bundled(chromium) = 90.0.44.30.228

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
# Don't get too excited. MPEG and other legally problematic stuff is stripped
# out. See clean_qtwebengine.sh, clean_ffmpeg.sh, and
# get_free_ffmpeg_source_files.py.
# see src/3rdparty/chromium/third_party/ffmpeg/Changelog for the version number
Provides: bundled(ffmpeg) = 3.3
Provides: bundled(hunspell) = 1.6.0
Provides: bundled(iccjpeg)
# bundled as "khronos", headers only
Provides: bundled(khronos_headers)
# bundled as "leveldatabase"
Provides: bundled(leveldb) = 1.20
# bundled as "libjingle_xmpp"
Provides: bundled(libjingle)
# see src/3rdparty/chromium/third_party/libsrtp/CHANGES for the version number
Provides: bundled(libsrtp) = 2.1.0
%if !0%{?use_system_libvpx}
# claims "Version: 1.6.0", but according to the fine print, this is actually a
# snapshot from master from after the 1.6.1 release
Provides: bundled(libvpx) = 1.6.1
%endif
%if !0%{?use_system_libwebp}
Provides: bundled(libwebp) = 0.6.0
%endif
# bundled as "libxml"
# see src/3rdparty/chromium/third_party/libxml/linux/include/libxml/xmlversion.h
Provides: bundled(libxml2) = 2.9.4
# see src/3rdparty/chromium/third_party/libxslt/linux/config.h for version
Provides: bundled(libxslt) = 1.1.29
Provides: bundled(libXNVCtrl) = 302.17
Provides: bundled(libyuv) = 1658
Provides: bundled(modp_b64)
Provides: bundled(openmax_dl) = 1.0.2
Provides: bundled(ots)
# see src/3rdparty/chromium/third_party/protobuf/CHANGES.txt for the version
#Provides: bundled(protobuf) = 3.0.0-0.1.beta3
Provides: bundled(qcms) = 4
Provides: bundled(sfntly)
Provides: bundled(skia)
# bundled as "smhasher"
Provides: bundled(SMHasher) = 0-0.1.svn147
Provides: bundled(sqlite) = 3.20
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
Provides: bundled(dmg_fp)
Provides: bundled(dynamic_annotations) = 4384
Provides: bundled(superfasthash) = 0
Provides: bundled(symbolize)
# bundled as "valgrind", headers only
Provides: bundled(valgrind.h)
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
Provides: bundled(v8) = 6.1.534.44
# bundled by v8 (src/3rdparty/chromium/v8/src/base/ieee754.cc)
# The version number is 5.3, the last version that upstream released, years ago:
# http://www.netlib.org/fdlibm/readme
Provides: bundled(fdlibm) = 5.3

%{?_qt5_version:Requires: qt5-qtbase%{?_isa} = %{_qt5_version}}

%if 0%{?use_system_icu}
# Those versions were built with bundled ICU and want the data file.
Conflicts: qt5-qtwebengine-freeworld < 5.15.2-2
%endif

%if 0%{?rhel} == 7
BuildRequires: devtoolset-7-toolchain	
%endif

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

%description examples
%{summary}.


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
%setup -q -n %{qt_module}-everywhere-src-%{version}%{?prerelease:-%{prerelease}} -a20

mv pulse src/3rdparty/chromium/

pushd src/3rdparty/chromium
popd

#patch0 -p1 -b .linux-pri
%if 0%{?use_system_libicu}
%patch1 -p1 -b .no-icudtl-dat
%endif
%patch2 -p1 -b .fix-extractcflag
%if !0%{?arm_neon}
%patch3 -p1 -b .no-neon
%endif
%patch4 -p1 -b .SIOCGSTAMP
%patch5 -p1 -b .QT_DEPRECATED_VERSION

## upstream patches

#patch10 -p1 -b .openmax-dl-neon
%patch24 -p1 -b .aarch64-new-stat
%patch26 -p1 -b .use-python2
%patch28 -p1 -b .rh#1904652
%patch29 -p1 -b .sandbox-time64-syscalls
%patch30 -p1 -b .SIGSTKSZ
%patch31 -p1 -b .TRUE
%patch32 -p1 -b .clone3

# delete all "toolprefix = " lines from build/toolchain/linux/BUILD.gn, as we
# never cross-compile in native Fedora RPMs, fixes ARM and aarch64 FTBFS
sed -i -e '/toolprefix = /d' -e 's/\${toolprefix}//g' \
  src/3rdparty/chromium/build/toolchain/linux/BUILD.gn

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

# generate qtwebengine-3rdparty.qdoc, it is missing from the tarball
pushd src/3rdparty
%{__python2} chromium/tools/licenses.py \
  --file-template ../../tools/about_credits.tmpl \
  --entry-template ../../tools/about_credits_entry.tmpl \
  credits >../webengine/doc/src/qtwebengine-3rdparty.qdoc
popd

# copy the Chromium license so it is installed with the appropriate name
cp -p src/3rdparty/chromium/LICENSE LICENSE.Chromium

# consider doing this as part of the tarball creation step instead?  rdieter
# fix/workaround
# fatal error: QtWebEngineCore/qtwebenginecoreglobal.h: No such file or directory
if [ ! -f "./include/QtWebEngineCore/qtwebenginecoreglobal.h" ]; then
%_qt5_bindir/syncqt.pl -version %{version}
fi

# abort if this doesn't get created by syncqt.pl
test -f "./include/QtWebEngineCore/qtwebenginecoreglobal.h"


%build
%if 0%{?rhel} == 7
. /opt/rh/devtoolset-7/enable
%endif

export STRIP=strip
export NINJAFLAGS="%{__ninja_common_opts}"
export NINJA_PATH=%{__ninja}

%{qmake_qt5} \
  %{?debug_config:CONFIG+="%{debug_config}}" \
  CONFIG+="link_pulseaudio use_gold_linker" \
  %{?use_system_libicu:QMAKE_EXTRA_ARGS+="-system-webengine-icu"} \
  QMAKE_EXTRA_ARGS+="-webengine-kerberos" \
  .

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

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt5_libdir}
for prl_file in libQt5*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
# explicitly omit, at least until there's a real library installed associated with it -- rex
rm -fv Qt5WebEngineCore.la
popd

mkdir -p %{buildroot}%{_qtwebengine_dictionaries_dir}

# adjust cmake dep(s) to allow for using the same Qt5 that was used to build it
# using the lesser of %%version, %%_qt5_version
%global lesser_version $(echo -e "%{version}\\n%{_qt5_version}" | sort -V | head -1)
sed -i -e "s|%{version} \${_Qt5WebEngine|%{lesser_version} \${_Qt5WebEngine|" \
  %{buildroot}%{_qt5_libdir}/cmake/Qt5WebEngine*/Qt5WebEngine*Config.cmake


%ldconfig_scriptlets

%filetriggerin -- %{_datadir}/myspell
while read filename ; do
  case "$filename" in
    *.dic)
      bdicname=%{_qtwebengine_dictionaries_dir}/`basename -s .dic "$filename"`.bdic
      %{_qt5_bindir}/qwebengine_convert_dict "$filename" "$bdicname" &> /dev/null || :
      ;;
  esac
done

%files
%license LICENSE.* src/webengine/doc/src/qtwebengine-3rdparty.qdoc
%{_qt5_libdir}/libQt5*.so.*
%{_qt5_bindir}/qwebengine_convert_dict
%{_qt5_libdir}/qt5/qml/*
%{_qt5_libdir}/qt5/libexec/QtWebEngineProcess
%{_qt5_plugindir}/designer/libqwebengineview.so
%{_qt5_plugindir}/imageformats/libqpdf.so
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

%files devel
%{rpm_macros_dir}/macros.qt5-qtwebengine
%{_qt5_headerdir}/Qt*/
%{_qt5_libdir}/libQt5*.so
%{_qt5_libdir}/libQt5*.prl
%{_qt5_libdir}/cmake/Qt5*/
%{_qt5_libdir}/pkgconfig/Qt5*.pc
%{_qt5_archdatadir}/mkspecs/modules/*.pri

%files devtools
%{_qt5_datadir}/resources/qtwebengine_devtools_resources.pak

%files examples
%{_qt5_examplesdir}/

%if 0%{?docs}
%files doc
%{_qt5_docdir}/*
%endif


%changelog
* Fri Sep 03 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.15.6-1
- 5.15.6

* Thu Aug 12 2021 Troy Dawson <tdawson@redhat.com> - 5.15.5-3
- Fix use-python2.patch

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 23 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.15.5-1
- 5.15.5

* Wed Jun 16 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.15.2-12
- workaround SIGSTKSZ FTBFS (#19455950
- workaround 'TRUE'/'FALSE' was not declared in this scope

* Thu May 20 2021 Pete Walter <pwalter@fedoraproject.org> - 5.15.2-11
- Rebuild for ICU 69

* Mon May 10 2021 Jonathan Wakely <jwakely@redhat.com> - 5.15.2-10
- Rebuilt for removed libstdc++ symbols (#1937698)

* Tue Mar 30 2021 Jonathan Wakely <jwakely@redhat.com> - 5.15.2-9
- Rebuilt for removed libstdc++ symbol (#1937698)

* Tue Jan 26 2021 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.15.2-8
- Add versioned Conflicts with -freeworld built against bundled ICU (#1920379)

* Sat Jan 23 2021 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.15.2-7
- Fix sandbox issue on 32-bit architectures with glibc >= 2.31 (from Debian)

* Sat Jan 23 2021 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.15.2-6
- Reenable system ICU on F33+, ICU 67 supported since 5.15.1 according to Debian

* Wed Jan 20 2021 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.15.2-5
- Fix sandbox issue breaking text rendering with glibc 2.33 (#1904652)

* Wed Dec 30 2020 Mattia Verga <mattia.verga@protonmail.com> - 5.15.2-4
- Rebuild for gcc bugfix upgrade

* Fri Dec 04 2020 Jeff Law <law@redhat.com> - 5.15.2-3
- Fix another missing #include for gcc-11

* Tue Nov 24 07:55:13 CET 2020 Jan Grulich <jgrulich@redhat.com> - 5.15.2-2
- Rebuild for qtbase with -no-reduce-relocations option

* Fri Nov 20 09:12:35 CET 2020 Jan Grulich <jgrulich@redhat.com> - 5.15.2-1
- 5.15.2

* Wed Nov 04 2020 Jeff Law <law@redhat.com> - 5.15.1-3
- Fix missing #includes for gcc-11

* Wed Sep 23 12:52:56 CEST 2020 Jan Grulich <jgrulich@redhat.com> - 5.15.1-2
- Rebuild (libevent)

* Fri Sep 11 2020 Jan Grulich <jgrulich@redhat.com> - 5.15.1-1
- 5.15.1

* Fri Sep 04 2020 Than Ngo <than@redhat.com> - 5.15.0-4
- Fix FTBFS

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.0-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jun 10 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.15.0-1
- 5.15.0
- f33's icu-67.x currently not compatible, use bundled icu

* Sat Apr 04 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.14.2-2
- rebuild (qt5)

* Wed Apr 01 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.14.2-1
- 5.14.2

* Wed Mar 25 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.14.1-1
- 5.14.1
- use_system_icu on f32+
- drop upstreamed patches

* Wed Mar 25 2020 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 5.13.2-4
- Add patch to allow clock_nanosleep in Linux sandbox (Chromium)

* Fri Feb 21 2020 Troy Dawson <tdawson@redhat.com> - 5.13.2-3
- Patch 3rd party chromium, fix FTBFS (#1799084)

* Wed Jan 08 2020 Than Ngo <than@redhat.com> - 5.13.2-2
- merged Pull-Request, keep ppc files in ffmpeg

* Mon Dec 09 2019 Jan Grulich <jgrulich@redhat.com> - 5.13.2-1
- 5.13.2

* Mon Dec 02 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.12.6-1
- 5.12.6

* Wed Oct 02 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.12.5-2
- explicitly omit QtWebEngineCore.la from packaging

* Thu Sep 26 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.12.5-1
- 5.12.5

* Tue Sep 24 2019 Jan Grulich <jgrulich@redhat.com> - 5.12.4-10
- rebuild (qt5)

* Wed Aug 14 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.12.4-9
- rebuild (re2)

* Mon Aug 12 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.12.4-8
- CONFIG+=link_pulseaudio

* Wed Aug 07 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.12.4-7
- rebuild (re2, #1672014#c10)
- build using bundled pulse headers, workaround FTBFS bug #1729806

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.12.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jun 26 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.12.4-5
- pull in some upstream fixes

* Tue Jun 25 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.12.4-4
- rebuild (qt5)

* Tue Jun 18 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.12.4-3
- fix-extractcflag.patch rebased

* Mon Jun 17 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.12.4-2
- rebuild (qt5)

* Mon Jun 17 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.12.4-1
- 5.12.4

* Tue Jun 11 2019 Jan Grulich <jgrulich@redhat.com> - 5.12.3-4
- rebuild (qt5)

* Tue Jun 04 2019 Jan Grulich <jgrulich@redhat.com> - 5.12.3-3
- rebuild (qt5)

* Sun May 12 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.12.3-2
- rebuild (icu)

* Thu Apr 18 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.12.3-1
- 5.12.3

* Mon Mar 25 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.12.2-2
- revert bundled libxml2/libxslt

* Mon Mar 25 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.12.2-1
- 5.12.2
- use system libxml2/libxslt

* Sun Feb 24 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.12.1-1
- 5.12.1
- enable kerberos support

* Tue Feb 05 2019 Björn Esser <besser82@fedoraproject.org> - 5.11.3-5
- rebuilt (libvpx)

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.11.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 03 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.11.3-3
- -devtools subpkg, workaround multilib conflicts (#1663299)

* Tue Dec 11 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.11.3-2
- rebuild (Qt5)

* Tue Dec 04 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.11.3-1
- 5.11.3

* Wed Sep 26 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.11.2-2
- avoid using %%make_build for now

* Mon Sep 24 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.11.2-1
- 5.11.2

* Mon Sep 24 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.11.1-8
- use bundled minizip on f30+ (#1632196)

* Fri Sep 21 2018 Jan Grulich <jgrulich@redhat.com> - 5.11.1-7
- rebuild (qt5)

* Tue Sep 18 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.11.1-6
- cleaner (imo) minizip deps, workaround rhbz#1630448

* Tue Aug 28 2018 Patrik Novotný <panovotn@redhat.com> - 5.11.1-5
- change requires to minizip-compat(-devel), rhbz#1609830, rhbz#1615381

* Sun Jul 15 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.11.1-4
- BR: /usr/bin/python

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.11.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Pete Walter <pwalter@fedoraproject.org> - 5.11.1-2
- Rebuild for ICU 62

* Fri Jun 22 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.11.1-1
- 5.11.1

* Wed Jun 20 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.11.0-2
- rebuild (qt5)

* Thu Jun 14 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.11.0-1
- 5.11.0
- drop shadow build (to match other qt5 packages where it has been problematic)
- drop upstreamed patches
- rebase no-icudtl-dat.patch
- pull in upstream gcc8 FTBFS fix
- update clean_ffmpeg whitelist
- patches needswork: system-nspr-prtime,system-icu-utf,no-sse2,skia-neon,icu59
- minimal debug/debuginfo (for now)
- use macros %%make_build %%ldconfig_scriptlets %%__ninja %%__ninja_common_opts

* Sun May 27 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.10.1-7
- rebuild (qt5 5.11.0)
- Add patch by spot from the Fedora Chromium RPM for FTBFS with GCC 8 on i686
- include 0027-Fix-compilation-of-simplebrowser-example.patch (5.11 branch)

* Mon Apr 30 2018 Pete Walter <pwalter@fedoraproject.org> - 5.10.1-6
- Rebuild for ICU 61.1

* Sun Mar 18 2018 Iryna Shcherbina <ishcherb@redhat.com> - 5.10.1-5
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Sun Mar 18 2018 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.10.1-4
- Fix (from 5.9.5) for incomplete, ineffective fix for CVE-2018-6033 in 5.10.1

* Sat Mar 17 2018 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.10.1-3
- Forward-port security backports from 5.9.5 LTS (up to Chromium 65.0.3325.146)

* Fri Feb 23 2018 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.10.1-2
- Drop -fabi-version=11 workaround, gcc-8.0.1-0.16.fc28 should fix this

* Sun Feb 18 2018 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.10.1-1
- Update to 5.10.1
- Rediff (unfuzz) no-sse2 patch

* Fri Feb 16 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.10.0-6
- workaround FTBFS, build with -fabi-version=11 (#1545918)

* Sat Feb 10 2018 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.10.0-5
- Reenable system libvpx on F28+, Rawhide (future F28) has libvpx 1.7.0 now

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.10.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 26 2018 Tom Callaway <spot@fedoraproject.org> - 5.10.0-3
- rebuild for new libvpx

* Sat Dec 30 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.10.0-2
- rebuild (qt-5.10.0)

* Thu Dec 28 2017 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.10.0-1
- Update to 5.10.0
- Update version numbers of bundled stuff
- Drop support for Fedora < 26 (in particular, WEBENGINE_CONFIG F25 workarounds)
- Drop qt57 patch, support for Qt 5.7 was completely dropped upstream
- Update get_free_ffmpeg_source_files.py from Fedora Chromium packaging
- Update clean_ffmpeg.sh whitelist (sync from Fedora Chromium packaging)
- clean_qtwebengine.sh: Update for the changed tarball naming scheme
- Use QMAKE_EXTRA_ARGS instead of the removed WEBENGINE_CONFIG
- Rebase linux-pri, system-nspr-prtime, system-icu-utf, no-sse2, skia-neon and
  gn-bootstrap-verbose patches
- In particular, restore the removed V8 x87 backend in the no-sse2 patch
- Re-backport no-aspirational-scripts from upstream (undo 5.9 backport)
- Disable system libvpx support for now, requires unreleased libvpx (1.6.2+)
- Add new BuildRequires: flex (required) and pkgconfig(lcms2) (unbundled)
- Forward-port missing parts of 5.9 ICU>=59 build fix (QTBUG-60886, QTBUG-65090)
- Reduce debugging info on ARM also on F27+ (as on F26- since 5.9.0)

* Tue Dec 19 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.3-5
- properly escape newline in lesser_version hack

* Thu Dec 14 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.3-4
- adjust Qt5WebEngineCoreConfig.cmake unconditionally

* Sat Dec 02 2017 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.9.3-3
- Drop support for Unicode "aspirational scripts", fixes #error with ICU >= 60

* Thu Nov 30 2017 Pete Walter <pwalter@fedoraproject.org> - 5.9.3-2
- Rebuild for ICU 60.1

* Sun Nov 26 2017 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.9.3-1
- Update to 5.9.3
- Enable docs on F27

* Sun Nov 26 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.2-3
- rebuild (qt5)

* Sat Oct 14 2017 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.9.2-2
- linux-pri patch: Do not call the Chromium unbundling script on re2,
  QtWebEngine now auto-detects and uses the system re2 out of the box
- Drop system-re2 patch (patching the no longer used unbundle/re2.gn), the
  QtWebEngine re2/BUILD.gn is already correct
- Explicitly force use_system_re2, the autodetection does not work on F25
- Fix FTBFS with Qt 5.7

* Tue Oct 10 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.2-1
- Update to 5.9.2
- Add BuildRequires: qt5-qtquickcontrols2-devel for the examples
- Rebase linux-pri patch
- Drop qt57 and qtbug-61521 patches, fixed upstream
- arm-fpu-fix patch: Drop the host tools hunk added in 5.9.0-2, fixed upstream

* Mon Oct 09 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.1-5
- rebuild (qt5)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.9.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 19 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.1-2
- rebuild (qt5)

* Sat Jul 01 2017 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.9.1-1
- Update to 5.9.1
- Rebase qtbug-61521 patch (drop the parts that are already in 5.9.1)
- Drop backported GN aarch64 patches already included in 5.9.1
- no-sse2 patch: Upstream added 2 examples, add -Wl,-rpath-link to them too

* Mon Jun 26 2017 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.9.0-4
- Add a hunk to the QTBUG-61521 fix according to the upstream review

* Sun Jun 25 2017 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.9.0-3
- Fix broken binary compatibility for C memory management functions (incomplete
  upstream fix for QTBUG-60565) (QTBUG-61521)

* Tue Jun 13 2017 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.9.0-2
- arm-fpu-fix patch: Also build the host tools (i.e., GN) with the correct FPU

* Mon Jun 12 2017 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.9.0-1
- Update to 5.9.0
- Update version numbers of bundled stuff
- Use bundled libsrtp and protobuf, Chromium dropped unbundling support for them
- Use bundled libxml2 and libxslt, QtWebEngine 5.9 requires a libxml2 built with
  ICU due to https://bugreports.qt.io/browse/QTBUG-59094, Fedora libxml2 is not
- Add missing Provides: bundled(hunspell) for the spellchecking added in 5.8
- Rebase linux-pri, no-neon, system-icu-utf, no-sse2, arm-fpu-fix,
  openmax-dl-neon and webrtc-neon-detect patches (port to GN)
- Sync system-nspr-prtime patch with Debian (they ported it to GN)
- Rebase fix-extractcflag patch
- Restore NEON runtime detection in Skia, drop old skia-neon patch (rewritten)
- Drop webrtc-neon, v8-gcc7, pdfium-gcc7, wtf-gcc7, fix-open-in-new-tab and
  fix-dead-keys patches, fixed upstream
- Update system libvpx/libwebp version requirements (libvpx now F25+ only)
- Drop the flag hacks (-g1 -fno-delete-null-pointer-checks), fixed upstream
- Force verbose output from the GN bootstrap process
- Backport upstream patch to fix GN FTBFS on aarch64 (QTBUG-61128)
- Backport patch to fix FTBFS with GCC on aarch64 from upstream Chromium
- Fix src/3rdparty/chromium/build/linux/unbundle/re2.gn
- Delete all "toolprefix = " lines from build/toolchain/linux/BUILD.gn
- Reduce debugging info on ARM on F26-

* Sat May 13 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.8.0-14
- fix rpm macros

* Thu May 11 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.8.0-13
- apply Qt5WebEngineCoreConfig.cmake hack only on < f27

* Wed May 10 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.8.0-12
- rebuild (Qt-5.9), disable docs for f27+

* Fri Apr 28 2017 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.8.0-11
- Backport upstream fix for non-functional dead keys in text fields

* Tue Apr 25 2017 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.8.0-10
- Backport upstream fix for blank pages when a link opens in a new tab

* Mon Apr 17 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.8.0-9
- +macros.qt5-qtwebengine

* Mon Apr 10 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.8.0-8
- Qt5WebEngineCoreConfig.cmake: fix when using Qt < %%version (#1438877)

* Tue Apr 04 2017 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.8.0-7
- File trigger: silence qwebengine_convert_dict output and ignore its exit code

* Mon Apr 03 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.8.0-6
- build docs on all archs

* Fri Mar 31 2017 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.8.0-5
- Enable use_spellchecker explicitly so that it is also enabled on Qt 5.7
- Use file triggers to automatically convert system hunspell dictionaries

* Fri Mar 31 2017 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.8.0-4
- Fix no-sse2 patch FTBFS (on i686)

* Thu Mar 30 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.8.0-3
- make buildable against qt5 < 5.8 too

* Tue Mar 07 2017 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.8.0-2
- Fix FTBFS in the WTF part of Blink/WebKit with GCC 7

* Mon Mar 06 2017 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.8.0-1
- Update to 5.8.0
- Update version numbers of bundled stuff
- Rebase (unfuzz) system-nspr-prtime and system-icu-utf patches
- Drop system-icu54 patch, ICU 5.4 no longer supported
- Rebase the webrtc-neon-detect patch (backported portions no longer needed)
- Rebase the no-sse2 patch
- Update clean_ffmpeg.sh: autorename* files now #include the unrenamed ones
- Update -docs BuildRequires and Requires (Helio Castro)
- Fix FTBFS in V8 with GCC 7 (by Ben Noordhuis, backported from Chromium RPM)
- Fix FTBFS in PDFium with GCC 7: backport upstream cleanup removing that code
- Generate qtwebengine-3rdparty.qdoc, it is missing from the tarball
- Work around missing qt5_qtwebengine_arches macro on F24
- Upstream added a qwebengine_convert_dict executable, package it

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.7.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 01 2017 Sandro Mani <manisandro@gmail.com> - 5.7.1-7
- Rebuild (libwebp)

* Thu Jan 26 2017 Orion Poplawski <orion@cora.nwra.com> - 5.7.1-6
- Rebuild for protobuf 3.2.0

* Mon Jan 02 2017 Rex Dieter <rdieter@math.unl.edu> - 5.7.1-5
- filter (designer) plugin provides

* Thu Dec 08 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.7.1-4
- Respun tarball (now really includes the page margin fix)
- Change qt5-qtbase dependency from >= to =

* Sun Dec 04 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.7.1-3
- Ship the license files

* Sun Dec 04 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.7.1-2
- clean_qtwebengine.sh: Rip out openh264 sources
- Rebase no-neon patch, add new arm-fpu-fix patch where no-neon not wanted
- Try enabling arm_neon unconditionally, #1282495 should be fixed even in F23
- Remove Android dependencies from openmax_dl ARM NEON detection (detect.c)
- Set CFLAGS, unset both CFLAGS and CXXFLAGS between qmake and make
- chromium-skia: build SkUtilsArm.cpp also on non-Android ARM
- webrtc: backport CPU feature detection for ARM Linux, enable it for Chromium

* Thu Nov 10 2016 Helio Chissini de Castro <helio@kde.org> - 5.7.1-1
- New upstream version

* Wed Sep 14 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.0-8
- ExclusiveArch: %%{qt5_qtwebengine_arches} (defined by qt5-srpm-macros)

* Fri Sep 09 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.7.0-7
- apply the correct page margins from the QPageLayout to Chromium printing

* Sat Aug 13 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.7.0-6
- Fix crash when building against glibc 2.24 (#1364781) (upstream patch)

* Sun Jul 31 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.0-5
- BR: cmake (for cmake autoprovides support mostly)

* Tue Jul 26 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.7.0-4
- Restore system-icu54 patch, the fix was lost upstream

* Sat Jul 23 2016 Christian Dersch <lupinix@mailbox.org> - 5.7.0-3
- Rebuilt for libvpx.so.4 soname bump

* Wed Jul 20 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.7.0-2
- clean_ffmpeg.sh: Whitelist libavutil/aarch64/timer.h (#1358428)

* Mon Jul 18 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.7.0-1
- Update to 5.7.0
- Update version numbers of bundled stuff
- Update system libvpx/libwebp version requirements (now F24+ only)
- Drop no-format patch, fixed upstream (they stopped passing -Wno-format)
- Rebase linux-pri patch (use_system_protobuf is now a qmake flag)
- Rebase system-nspr-prtime, system-icu-utf and no-sse2 patches
- Fix ARM NEON handling in webrtc gyp files (honor arm_neon=0)

* Tue Jun 14 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.1-3
- rebuild (glibc)

* Sun Jun 12 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.1-2
- add versioned qt5-qtbase runtime dep

* Sat Jun 11 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.6.1-1
- Update to 5.6.1
- Rebase linux-pri patch (drop the parts already fixed upstream)
- Drop backported chimera-nss-init patch, already applied upstream
- Rebase no-sse2 patch (the core_module.pro change)
- Add the new designer/libqwebengineview.so plugin to the file list

* Mon Jun 06 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.0-8
- workaround stackmashing runtime errors in re2-related bundled headers (#1337585)

* Sat May 21 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.0-7
- rebuild (pciutuils)

* Wed May 18 2016 Rex Dieter <rdieter@fedoraproject.org> 5.6.0-6
- BR: git-core

* Fri Apr 15 2016 David Tardon <dtardon@redhat.com> - 5.6.0-5
- rebuild for ICU 57.1

* Fri Apr 08 2016 Than Ngo <than@redhat.com> - 5.6.0-4
- drop ppc ppc64 ppc64le from ExclusiveArch, it's not supported yet

* Thu Mar 24 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.6.0-3
- Build with CONFIG+="webcore_debug v8base_debug force_debug_info"
- Force -fno-delete-null-pointer-checks through CXXFLAGS, Qt flags not used here
- Use -g1 instead of -g on non-x86_64 to avoid memory exhaustion
- Work around debugedit failure by removing "./" from #line commands and
  changing "//" to "/" in an #include command

* Fri Mar 18 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.6.0-2
- Avoid checking for the nonexistent icudtl.dat and silence the warnings

* Thu Mar 17 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.6.0-1
- Update to 5.6.0 (final)
- Drop system-icu54 patch, fixed upstream

* Thu Feb 25 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.6.0-0.19.rc
- Update to 5.6.0 RC
- Rebase linux-pri and no-sse2 patches
- Remove BuildRequires pkgconfig(flac), pkgconfig(speex), no longer needed
- Update file list for 5.6.0 RC (resources now in resources/ subdirectory)
- Tag translations with correct %%lang tags

* Wed Feb 24 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.6.0-0.18.beta
- no-sse2 patch: Fix FFT (RealFourier) in webrtc on non-SSE2 x86

* Tue Feb 23 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.6.0-0.17.beta
- Fix FTBFS on aarch64: Respin tarball with fixed clean_ffmpeg.sh (#1310753).

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.0-0.16.beta
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 19 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.6.0-0.15.beta
- Build V8 as a shared library on i686 to allow for swappable backends
- Build both the x87 version and the SSE2 version of V8 on i686
- Add the private library directory to the file list on i686
- Add Provides/Requires filtering for libv8.so (i686) and for plugins

* Sun Jan 17 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.6.0-0.14.beta
- Do not require SSE2 on i686

* Thu Jan 14 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.6.0-0.13.beta
- Drop nss321 backport (and the related nss-headers patch), it did not help
- Do an NSS/BoringSSL "chimera build" as will be the default in Chromium 47
- Update License accordingly (add "OpenSSL")
- Fix the "chimera build" to call EnsureNSSHttpIOInit (backport from Chromium)

* Wed Jan 13 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.6.0-0.12.beta
- Update forked NSS SSL code to 3.21, match system NSS (backport from Chromium)

* Wed Jan 13 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.6.0-0.11.beta
- Add an (optimistic) ExclusiveArch list because of V8 (tracking bug: #1298011)

* Tue Jan 12 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.6.0-0.10.beta
- Unbundle prtime.cc, use the system NSPR instead (which is already required)
- Unbundle icu_utf.cc, use the system ICU instead (which is already required)

* Mon Jan 11 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.6.0-0.9.beta
- linux-pri.patch: Set icu_use_data_file_flag=0 for system ICU

* Mon Jan 11 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.6.0-0.8.beta
- Build against the system libvpx also on F23 (1.4.0), worked in Copr

* Mon Jan 11 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.6.0-0.7.beta
- Use the system libvpx on F24+ (1.5.0)
- Fixes to Provides: bundled(*): libwebp if bundled, x86inc only on x86

* Sun Jan 10 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.6.0-0.6.beta
- Fix extractCFlag to also look in QMAKE_CFLAGS_RELEASE (needed for ARM)
- Fix FTBFS on ARM: Disable NEON due to #1282495 (GCC bug)

* Sat Jan 09 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.6.0-0.5.beta
- Fix FTBFS on ARM: linux-pri patch: Set use_system_yasm only on x86_64 and i386
- Fix FTBFS on ARM: Respin tarball with: clean_ffmpeg.sh: Add missing ARM files

* Sat Jan 09 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.6.0-0.4.beta.1
- Use more specific BuildRequires for docs (thanks to rdieter)
- Fix FTBFS against ICU 54 (F22/F23), thanks to spot for the Chromium fix

* Fri Jan 08 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.6.0-0.4.beta
- Fix License tag
- Use %%_qt5_examplesdir macro
- Add Provides: bundled(*) for all the bundled libraries that I found

* Wed Jan 06 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.6.0-0.3.beta
- linux-pri patch: Add use_system_protobuf, went missing in the 5.6 rebase

* Wed Jan 06 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.6.0-0.2.beta
- linux-pri patch: Add missing newline at the end of the log line
- Use export for NINJA_PATH (fixes system ninja-build use)

* Wed Jan 06 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.6.0-0.1.beta
- Readd BR pkgconfig(jsoncpp) because linux.pri now checks for it
- BR yasm only on x86 (i686, x86_64)
- Add dot at the end of %%description
- Rebase no-format patch
- Replace unbundle-gyp.patch with new linux-pri.patch
- Use system ninja-build instead of the bundled one
- Run the unbundling script replace_gyp_files.py in linux.pri rather than here
- Update file list for 5.6.0-beta (no more libffmpegsumo since Chromium 45)

* Tue Jan 05 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.5.1-4
- Remove unused BRs flex, libgcrypt-devel, bzip2-devel, pkgconfig(gio-2.0),
  pkgconfig(hunspell), pkgconfig(libpcre), pkgconfig(libssl),
  pkgconfig(libcrypto), pkgconfig(jsoncpp), pkgconfig(libmtp),
  pkgconfig(libexif), pkgconfig(liblzma), pkgconfig(cairo), pkgconfig(libusb),
  perl(version), perl(Digest::MD5), perl(Text::ParseWords), ruby
- Add missing explicit BRs on pkgconfig(x11),  pkgconfig(xext),
  pkgconfig(xfixes), pkgconfig(xdamage), pkgconfig(egl)
- Fix BR pkgconfig(flac++) to pkgconfig(flac) (libFLAC++ not used, only libFLAC)
- Fix BR python-devel to python
- Remove unused -Duse_system_openssl=1 flag (QtWebEngine uses NSS instead)
- Remove unused -Duse_system_jsoncpp=1 and -Duse_system_libusb=1 flags

* Mon Jan 04 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.5.1-3
- Update file list for 5.5.1 (add qtwebengine_resources_[12]00p.pak)

* Mon Jan 04 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.5.1-2
- Add missing explicit BRs on pkgconfig(expat) and pkgconfig(libxml-2.0)
- Remove unused BR v8-devel (cannot currently be unbundled)

* Thu Dec 24 2015 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.5.1-1
- Update to 5.5.1
- Remove patent-encumbered codecs in the bundled FFmpeg from the tarball

* Fri Jul 17 2015 Helio Chissini de Castro <helio@kde.org> - 5.5.0-2
- Update with unbundle flags. Adapted from original 5.4 Suse package
- Disable vpx and sqlite as unbundle due some compilation issues
- Enable verbose build

* Fri Jul 17 2015 Helio Chissini de Castro <helio@kde.org> - 5.5.0-1
- Initial spec

* Thu Jun 25 2015 Helio Chissini de Castro <helio@kde.org> - 5.5.0-0.2.rc
- Update for official RC1 released packages
