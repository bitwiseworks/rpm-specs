# For a complete build enable this
%if !0%{?os2_version}
%bcond all_codecs 0
%else
%bcond_without all_codecs
%endif

# Break dependency cycles by disabling certain optional dependencies.
%if !0%{?os2_version}
%bcond bootstrap 0
%else
%bcond_with bootstrap
%endif

# If building with all codecs, then set the pkg_suffix to %%nil.
# We can't handle this with a conditional, as srpm
# generation would not take it into account.
%if !0%{?os2_version}
%global pkg_suffix -free
%else
%global pkg_suffix %{nil}
%endif

# For alternative builds (do not enable in Fedora!)
%if !0%{?os2_version}
%bcond freeworld_lavc 0
%else
%bcond_with freeworld_lavc
%endif

%if %{with freeworld_lavc}
# Freeworld builds enable all codecs
%global with_all_codecs 1
# Freeworld builds do not need a package suffix
%global pkg_suffix %{nil}
%global basepkg_suffix -free
%endif

# Fails due to asm issue
%ifarch %{ix86} %{arm}
%if !0%{?os2_version}
%bcond lto 0
# relocations in .text from nasm-compiled code on i686 only
# https://bugzilla.redhat.com/show_bug.cgi?id=2428281
%global _pkg_extra_ldflags "-Wl,-z,notext"
%else
%bcond_with lto
%endif
%else
%bcond lto 1
%endif

%ifarch x86_64
%bcond vpl 1
%bcond vmaf 1
%else
%if !0%{?os2_version}
%bcond vpl 0
%bcond vmaf 0
%else
%bcond_with vpl
%bcond_with vmaf
%endif
%endif

%ifarch s390 s390x riscv64
%bcond dc1394 0
%bcond ffnvcodec 0
%else
%if !0%{?os2_version}
%bcond dc1394 1
%bcond ffnvcodec 1
%else
%bcond_with dc1394
%bcond_with ffnvcodec
%endif
%endif

%if !0%{?os2_version}
%if 0%{?rhel}
# Disable dependencies not available or wanted on RHEL/EPEL
%bcond chromaprint 0
%bcond flite 0
%else
# Break chromaprint dependency cycle (Fedora-only):
#   ffmpeg (libavcodec-free)  chromaprint  ffmpeg
%bcond chromaprint %{?with_bootstrap:0}%{!?with_bootstrap:1}
%bcond flite 1
%endif
%else
%bcond_with chromaprint
%bcond_with flite
%endif

%if 0%{?rhel} && 0%{?rhel} <= 9
# Disable some features because RHEL 9 packages are too old
%bcond lcms2 0
%bcond placebo 0
%else
%if !0%{?os2_version}
%bcond lcms2 1
%bcond placebo 1
%else
%bcond_without lcms2
%bcond_with placebo
%endif
%endif

%if 0%{?el10}
# Disable temporarily while we want for liblc3 to be upgraded
# Cf. https://issues.redhat.com/browse/RHEL-127169
%bcond lc3 0
%else
%if !0%{?os2_version}
%bcond lc3 1
%else
%bcond_with lc3
%endif
%endif

# For using an alternative build of EVC codecs
%if !0%{?os2_version}
%bcond evc_main 0
%else
%bcond_with evc_main
%endif

%if %{with all_codecs}
%if !0%{?os2_version}
%bcond rtmp 1
%bcond vvc 1
%bcond x264 1
%bcond x265 1
%else
%bcond_with rtmp
%bcond_without vvc
%bcond_without x264
%bcond_with x265
%endif
%else
%bcond rtmp 0
%bcond vvc 0
%bcond x264 0
%bcond x265 0
%endif

%if %{without lto}
%global _lto_cflags %{nil}
%endif

# FIXME: GCC says there's incompatible pointer casts going on in libavdevice...
%global build_type_safety_c 2

%global av_codec_soversion 62
%global av_device_soversion 62
%global av_filter_soversion 11
%global av_format_soversion 62
%global av_util_soversion 60
%global swresample_soversion 6
%global swscale_soversion 9

Name:           ffmpeg
%global pkg_name %{name}%{?pkg_suffix}

Version:        8.0.1
Release:        1%{?dist}
Summary:        A complete solution to record, convert and stream audio and video
License:        GPL-3.0-or-later
URL:            https://ffmpeg.org/
%if !0%{?os2_version}
Source0:        https://ffmpeg.org/releases/ffmpeg-%{version}.tar.xz
Source1:        https://ffmpeg.org/releases/ffmpeg-%{version}.tar.xz.asc
# https://ffmpeg.org/ffmpeg-devel.asc
# gpg2 --import --import-options import-export,import-minimal ffmpeg-devel.asc > ./ffmpeg.keyring
Source2:        ffmpeg.keyring
Source20:       enable_decoders
Source21:       enable_encoders

# Fixes for reduced codec selection on free build
Patch1:         ffmpeg-codec-choice.patch
# Allow to build with fdk-aac-free
# See https://bugzilla.redhat.com/show_bug.cgi?id=1501522#c112
Patch2:         ffmpeg-allow-fdk-aac-free.patch
# Support building with EVC base profile libraries
Patch3:         https://code.ffmpeg.org/FFmpeg/FFmpeg/pulls/20329.patch#/ffmpeg-support-evc-base-libraries.patch

# Add first_dts getter to libavformat for Chromium
# See: https://bugzilla.redhat.com/show_bug.cgi?id=2240127
# Reference: https://crbug.com/1306560
Patch1002:      ffmpeg-chromium.patch
%else
Vendor:         bww bitwise works GmbH
%scm_source     github http://github.com/bitwiseworks/%{name}-os2 n%{version}-os2
%endif


%if !0%{?os2_version}
Requires:       libavcodec%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libavdevice%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libavfilter%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libavformat%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libavutil%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libswresample%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libswscale%{?pkg_suffix}%{_isa} = %{version}-%{release}
%else
Requires:       libavcodec%{?pkg_suffix} = %{version}-%{release}
Requires:       libavdevice%{?pkg_suffix} = %{version}-%{release}
Requires:       libavfilter%{?pkg_suffix} = %{version}-%{release}
Requires:       libavformat%{?pkg_suffix} = %{version}-%{release}
Requires:       libavutil%{?pkg_suffix} = %{version}-%{release}
Requires:       libswresample%{?pkg_suffix} = %{version}-%{release}
Requires:       libswscale%{?pkg_suffix} = %{version}-%{release}
%endif

%if !0%{?os2_version}
BuildRequires:  AMF-devel
BuildRequires:  fdk-aac-free-devel
%endif
%if %{with flite}
BuildRequires:  flite-devel >= 2.2
%endif
%if !0%{?os2_version}
BuildRequires:  game-music-emu-devel
%endif
BuildRequires:  gcc
BuildRequires:  git-core
%if !0%{?os2_version}
BuildRequires:  gnupg2
BuildRequires:  gsm-devel
BuildRequires:  ladspa-devel
%endif
BuildRequires:  lame-devel
BuildRequires:  libgcrypt-devel
%if !0%{?os2_version}
BuildRequires:  libklvanc-devel
BuildRequires:  libmysofa-devel
BuildRequires:  libX11-devel
BuildRequires:  libXext-devel
BuildRequires:  libXv-devel
%endif
BuildRequires:  make
BuildRequires:  nasm
BuildRequires:  perl(Pod::Man)
%if !0%{?os2_version}
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(aom)
BuildRequires:  pkgconfig(aribb24) >= 1.0.3
%endif
BuildRequires:  pkgconfig(bzip2)
%if !0%{?os2_version}
BuildRequires:  pkgconfig(caca)
BuildRequires:  pkgconfig(codec2)
BuildRequires:  pkgconfig(dav1d)
BuildRequires:  pkgconfig(dvdnav)
BuildRequires:  pkgconfig(dvdread)
BuildRequires:  pkgconfig(ffnvcodec)
%endif
BuildRequires:  pkgconfig(flac)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(freetype2)
%if !0%{?os2_version}
BuildRequires:  pkgconfig(frei0r)
BuildRequires:  pkgconfig(fribidi)
BuildRequires:  pkgconfig(gl)
%endif
BuildRequires:  pkgconfig(gnutls)
%if !0%{?os2_version}
BuildRequires:  pkgconfig(harfbuzz)
BuildRequires:  pkgconfig(libilbc)
BuildRequires:  pkgconfig(jack)
%endif
%if %{with lc3}
BuildRequires:  pkgconfig(lc3) >= 1.1.0
%endif
%if %{with lcms2}
BuildRequires:  pkgconfig(lcms2) >= 2.13
%endif
%if !0%{?os2_version}
BuildRequires:  pkgconfig(libaribcaption) >= 1.1.1
BuildRequires:  pkgconfig(libass)
BuildRequires:  pkgconfig(libbluray)
BuildRequires:  pkgconfig(libbs2b)
BuildRequires:  pkgconfig(libcdio)
BuildRequires:  pkgconfig(libcdio_paranoia)
%endif
%if %{with chromaprint}
BuildRequires:  pkgconfig(libchromaprint)
%endif
%if !0%{?os2_version}
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libjxl) >= 0.7.0
BuildRequires:  pkgconfig(libmodplug)
%endif
BuildRequires:  pkgconfig(libopenjp2)
%if !0%{?os2_version}
BuildRequires:  pkgconfig(libopenmpt)
%endif
%if %{with placebo}
BuildRequires:  pkgconfig(libplacebo) >= 4.192.0
%endif
%if !0%{?os2_version}
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libqrencode)
BuildRequires:  pkgconfig(librabbitmq)
BuildRequires:  pkgconfig(librist)
BuildRequires:  pkgconfig(librsvg-2.0)
BuildRequires:  pkgconfig(libssh)
BuildRequires:  pkgconfig(libv4l2)
BuildRequires:  pkgconfig(libva)
BuildRequires:  pkgconfig(libva-drm)
BuildRequires:  pkgconfig(libva-x11)
%endif
BuildRequires:  pkgconfig(libwebp)
BuildRequires:  pkgconfig(libxml-2.0)
%if !0%{?os2_version}
BuildRequires:  pkgconfig(libzmq)
BuildRequires:  pkgconfig(lilv-0)
BuildRequires:  pkgconfig(lv2)
BuildRequires:  pkgconfig(oapv)
%endif
BuildRequires:  pkgconfig(ogg)
%if !0%{?os2_version}
BuildRequires:  pkgconfig(openal)
BuildRequires:  pkgconfig(opencore-amrnb)
BuildRequires:  pkgconfig(OpenCL)
BuildRequires:  pkgconfig(openh264)
%endif
BuildRequires:  pkgconfig(opus)
%if !0%{?os2_version}
BuildRequires:  pkgconfig(rav1e)
BuildRequires:  pkgconfig(rubberband)
%endif
BuildRequires:  pkgconfig(sdl2)
%if !0%{?os2_version}
BuildRequires:  pkgconfig(shaderc) >= 2019.1
BuildRequires:  pkgconfig(smbclient)
BuildRequires:  pkgconfig(snappy)
BuildRequires:  pkgconfig(soxr)
BuildRequires:  pkgconfig(speex)
BuildRequires:  pkgconfig(srt)
BuildRequires:  pkgconfig(SvtAv1Enc) >= 0.9.0
BuildRequires:  pkgconfig(tesseract)
%endif
BuildRequires:  pkgconfig(theora)
%if !0%{?os2_version}
BuildRequires:  pkgconfig(twolame)
BuildRequires:  pkgconfig(vapoursynth)
BuildRequires:  pkgconfig(vdpau)
BuildRequires:  pkgconfig(vidstab)
%endif
BuildRequires:  pkgconfig(vorbis)
%if !0%{?os2_version}
BuildRequires:  pkgconfig(vo-amrwbenc)
%endif
BuildRequires:  pkgconfig(vpx)
%if !0%{?os2_version}
BuildRequires:  pkgconfig(vulkan) >= 1.3.255
BuildRequires:  pkgconfig(wavpack)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-render)
BuildRequires:  pkgconfig(xcb-shape)
BuildRequires:  pkgconfig(xcb-shm)
BuildRequires:  pkgconfig(xcb-xfixes)
BuildRequires:  pkgconfig(zimg)
%endif
BuildRequires:  pkgconfig(zlib)
%if !0%{?os2_version}
BuildRequires:  pkgconfig(zvbi-0.2)
%endif

BuildRequires:  texinfo
BuildRequires:  xvidcore-devel

%if %{with dc1394}
BuildRequires:  pkgconfig(libavc1394)
BuildRequires:  pkgconfig(libdc1394-2)
BuildRequires:  pkgconfig(libiec61883)
%endif
%if %{with rtmp}
BuildRequires:  librtmp-devel
%endif
%if %{with vpl}
BuildRequires:  pkgconfig(vpl) >= 2.6
%endif
%if !0%{?os2_version}
%if %{with evc_main}
BuildRequires:  pkgconfig(xevd)
BuildRequires:  pkgconfig(xeve)
%else
BuildRequires:  pkgconfig(xevdb)
BuildRequires:  pkgconfig(xeveb)
%endif
%endif
%if %{with x264}
BuildRequires:  pkgconfig(x264)
%endif
%if %{with x265}
BuildRequires:  pkgconfig(x265)
%endif
%if %{with vmaf}
BuildRequires:  pkgconfig(libvmaf)
%endif


%description
FFmpeg is a leading multimedia framework, able to decode, encode, transcode,
mux, demux, stream, filter and play pretty much anything that humans and
machines have created. It supports the most obscure ancient formats up to the
cutting edge. No matter if they were designed by some standards committee, the
community or a corporation.

%if %{without all_codecs}
This build of ffmpeg is limited in the number of codecs supported.
%endif

%dnl --------------------------------------------------------------------------------

%if ! %{with freeworld_lavc}

%if "x%{?pkg_suffix}" != "x"
%package -n     %{pkg_name}
Summary:        A complete solution to record, convert and stream audio and video
Requires:       libavcodec%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libavdevice%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libavfilter%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libavformat%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libavutil%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libswresample%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libswscale%{?pkg_suffix}%{_isa} = %{version}-%{release}


%description -n %{pkg_name}
FFmpeg is a leading multimedia framework, able to decode, encode, transcode,
mux, demux, stream, filter and play pretty much anything that humans and
machines have created. It supports the most obscure ancient formats up to the
cutting edge. No matter if they were designed by some standards committee, the
community or a corporation.

%if %{without all_codecs}
This build of ffmpeg is limited in the number of codecs supported.
%endif

#/ "x%%{?pkg_suffix}" != "x"
%endif

%files -n %{pkg_name}
%doc CREDITS README.md
%if !0%{?os2_version}
%{_bindir}/ffmpeg
%{_bindir}/ffplay
%{_bindir}/ffprobe
%else
%{_bindir}/ffmpeg.exe
%{_bindir}/ffplay.exe
%{_bindir}/ffprobe.exe
%endif
%{_mandir}/man1/ff*.1*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/ffprobe.xsd
%{_datadir}/%{name}/libvpx-*.ffpreset

%dnl --------------------------------------------------------------------------------

%package -n     %{pkg_name}-devel
Summary:        Development package for %{name}
Requires:       libavcodec%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libavdevice%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libavfilter%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libavformat%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libavutil%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libswresample%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libswscale%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       pkgconfig

%description -n %{pkg_name}-devel
FFmpeg is a leading multimedia framework, able to decode, encode, transcode,
mux, demux, stream, filter and play pretty much anything that humans and
machines have created. It supports the most obscure ancient formats up to the
cutting edge. No matter if they were designed by some standards committee, the
community or a corporation.

%files -n %{pkg_name}-devel
%doc MAINTAINERS doc/APIchanges doc/*.txt
%doc _doc/examples

%dnl --------------------------------------------------------------------------------

%package -n libavcodec%{?pkg_suffix}
Summary:        FFmpeg codec library
%if !0%{?os2_version}
Requires:       libavutil%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libswresample%{?pkg_suffix}%{_isa} = %{version}-%{release}
# We require libopenh264 library, which has a dummy implementation and a real one
# In the event that this is being installed, we want to prefer openh264 if available
Suggests:       openh264%{_isa}
%else
Requires:       libavutil%{?pkg_suffix} = %{version}-%{release}
Requires:       libswresample%{?pkg_suffix} = %{version}-%{release}
Suggests:       openh264
%endif

%description -n libavcodec%{?pkg_suffix}
The libavcodec library provides a generic encoding/decoding framework
and contains multiple decoders and encoders for audio, video and
subtitle streams, and several bitstream filters.

%if %{without all_codecs}
This build of ffmpeg is limited in the number of codecs supported.
%endif

%files -n libavcodec%{?pkg_suffix}
%license COPYING.GPLv2 LICENSE.md
%if !0%{?os2_version}
%{_libdir}/libavcodec.so.%{av_codec_soversion}{,.*}
%else
%{_libdir}/avcode62.dll
%endif

%dnl --------------------------------------------------------------------------------

%package -n libavcodec%{?pkg_suffix}-devel
Summary:        Development files for FFmpeg's codec library
Requires:       libavutil%{?pkg_suffix}-devel = %{version}-%{release}
%if !0%{?os2_version}
Requires:       libavcodec%{?pkg_suffix}%{_isa} = %{version}-%{release}
%else
Requires:       libavcodec%{?pkg_suffix} = %{version}-%{release}
%endif
Requires:       pkgconfig

%description -n libavcodec%{?pkg_suffix}-devel
The libavcodec library provides a generic encoding/decoding framework
and contains multiple decoders and encoders for audio, video and
subtitle streams, and several bitstream filters.

This subpackage contains the headers for FFmpeg libavcodec.

%files -n libavcodec%{?pkg_suffix}-devel
%{_includedir}/%{name}/libavcodec
%{_libdir}/pkgconfig/libavcodec.pc
%if !0%{?os2_version}
%{_libdir}/libavcodec.so
%else
%{_libdir}/libavcodec_dll.a
%{_libdir}/libavcodec_dll.lib
%endif
%{_mandir}/man3/libavcodec.3*

%dnl --------------------------------------------------------------------------------

%package -n libavdevice%{?pkg_suffix}
Summary:        FFmpeg device library
%if !0%{?os2_version}
Requires:       libavcodec%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libavfilter%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libavformat%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libavutil%{?pkg_suffix}%{_isa} = %{version}-%{release}
%else
Requires:       libavcodec%{?pkg_suffix} = %{version}-%{release}
Requires:       libavfilter%{?pkg_suffix} = %{version}-%{release}
Requires:       libavformat%{?pkg_suffix} = %{version}-%{release}
Requires:       libavutil%{?pkg_suffix} = %{version}-%{release}
%endif

%description -n libavdevice%{?pkg_suffix}
The libavdevice library provides a generic framework for grabbing from
and rendering to many common multimedia input/output devices, and
supports several input and output devices, including Video4Linux2, VfW,
DShow, and ALSA.

%files -n libavdevice%{?pkg_suffix}
%license COPYING.GPLv2 LICENSE.md
%if !0%{?os2_version}
%{_libdir}/libavdevice.so.%{av_device_soversion}{,.*}
%else
%{_libdir}/avdevi62.dll
%endif

%dnl --------------------------------------------------------------------------------

%package -n libavdevice%{?pkg_suffix}-devel
Summary:        Development files for FFmpeg's device library
Requires:       libavcodec%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libavfilter%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libavformat%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libavutil%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libswresample%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libswscale%{?pkg_suffix}-devel = %{version}-%{release}
%if !0%{?os2_version}
Requires:       libavdevice%{?pkg_suffix}%{_isa} = %{version}-%{release}
%else
Requires:       libavdevice%{?pkg_suffix} = %{version}-%{release}
%endif
Requires:       pkgconfig

%description -n libavdevice%{?pkg_suffix}-devel
The libavdevice library provides a generic framework for grabbing from
and rendering to many common multimedia input/output devices, and
supports several input and output devices, including Video4Linux2, VfW,
DShow, and ALSA.

This subpackage contains the headers for FFmpeg libavdevice.

%files -n libavdevice%{?pkg_suffix}-devel
%{_includedir}/%{name}/libavdevice
%{_libdir}/pkgconfig/libavdevice.pc
%if !0%{?os2_version}
%{_libdir}/libavdevice.so
%else
%{_libdir}/libavdevice_dll.a
%{_libdir}/libavdevice_dll.lib
%endif
%{_mandir}/man3/libavdevice.3*

%dnl --------------------------------------------------------------------------------

%package -n libavfilter%{?pkg_suffix}
Summary:        FFmpeg audio and video filtering library
%if !0%{?os2_version}
Requires:       libavcodec%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libavformat%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libavutil%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libswresample%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libswscale%{?pkg_suffix}%{_isa} = %{version}-%{release}
%else
Requires:       libavcodec%{?pkg_suffix} = %{version}-%{release}
Requires:       libavformat%{?pkg_suffix} = %{version}-%{release}
Requires:       libavutil%{?pkg_suffix} = %{version}-%{release}
Requires:       libswresample%{?pkg_suffix} = %{version}-%{release}
Requires:       libswscale%{?pkg_suffix} = %{version}-%{release}
%endif

%description -n libavfilter%{?pkg_suffix}
The libavfilter library provides a generic audio/video filtering
framework containing several filters, sources and sinks.

%files -n libavfilter%{?pkg_suffix}
%license COPYING.GPLv2 LICENSE.md
%if !0%{?os2_version}
%{_libdir}/libavfilter.so.%{av_filter_soversion}{,.*}
%else
%{_libdir}/avfilt11.dll
%endif

%dnl --------------------------------------------------------------------------------

%package -n libavfilter%{?pkg_suffix}-devel
Summary:        Development files for FFmpeg's audio/video filter library
Requires:       libavcodec%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libavformat%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libavutil%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libswresample%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libswscale%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libavfilter%{?pkg_suffix} = %{version}-%{release}
Requires:       pkgconfig

%description -n libavfilter%{?pkg_suffix}-devel
The libavfilter library provides a generic audio/video filtering
framework containing several filters, sources and sinks.

This subpackage contains the headers for FFmpeg libavfilter.

%files -n libavfilter%{?pkg_suffix}-devel
%{_includedir}/%{name}/libavfilter
%{_libdir}/pkgconfig/libavfilter.pc
%if !0%{?os2_version}
%{_libdir}/libavfilter.so
%else
%{_libdir}/libavfilter_dll.a
%{_libdir}/libavfilter_dll.lib
%endif
%{_mandir}/man3/libavfilter.3*

%dnl --------------------------------------------------------------------------------

%package -n libavformat%{?pkg_suffix}
Summary:        FFmpeg's stream format library
%if !0%{?os2_version}
Requires:       libavcodec%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libavutil%{?pkg_suffix}%{_isa} = %{version}-%{release}
%else
Requires:       libavcodec%{?pkg_suffix} = %{version}-%{release}
Requires:       libavutil%{?pkg_suffix} = %{version}-%{release}
%endif

%description -n libavformat%{?pkg_suffix}
The libavformat library provides a generic framework for multiplexing
and demultiplexing (muxing and demuxing) audio, video and subtitle
streams. It encompasses multiple muxers and demuxers for multimedia
container formats.

%if %{without all_codecs}
This build of ffmpeg is limited in the number of codecs supported.
%endif

%files -n libavformat%{?pkg_suffix}
%license COPYING.GPLv2 LICENSE.md
%if !0%{?os2_version}
%{_libdir}/libavformat.so.%{av_format_soversion}{,.*}
%else
%{_libdir}/avform62.dll
%endif

%dnl --------------------------------------------------------------------------------

%package -n libavformat%{?pkg_suffix}-devel
Summary:        Development files for FFmpeg's stream format library
Requires:       libavcodec%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libavutil%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libswresample%{?pkg_suffix}-devel = %{version}-%{release}
%if !0%{?os2_version}
Requires:       libavformat%{?pkg_suffix}%{_isa} = %{version}-%{release}
%else
Requires:       libavformat%{?pkg_suffix} = %{version}-%{release}
%endif
Requires:       pkgconfig

%description -n libavformat%{?pkg_suffix}-devel
The libavformat library provides a generic framework for multiplexing
and demultiplexing (muxing and demuxing) audio, video and subtitle
streams. It encompasses multiple muxers and demuxers for multimedia
container formats.

This subpackage contains the headers for FFmpeg libavformat.

%files -n libavformat%{?pkg_suffix}-devel
%{_includedir}/%{name}/libavformat
%{_libdir}/pkgconfig/libavformat.pc
%if !0%{?os2_version}
%{_libdir}/libavformat.so
%else
%{_libdir}/libavformat_dll.a
%{_libdir}/libavformat_dll.lib
%endif
%{_mandir}/man3/libavformat.3*

%dnl --------------------------------------------------------------------------------

%package -n libavutil%{?pkg_suffix}
Summary:        FFmpeg's utility library
Group:          System/Libraries
Obsoletes:      libpostproc%{?pkg_suffix} < 8.0

%description -n libavutil%{?pkg_suffix}
The libavutil library is a utility library to aid portable multimedia
programming. It contains safe portable string functions, random
number generators, data structures, additional mathematics functions,
cryptography and multimedia related functionality (like enumerations
for pixel and sample formats).

%files -n libavutil%{?pkg_suffix}
%license COPYING.GPLv2 LICENSE.md
%if !0%{?os2_version}
%{_libdir}/libavutil.so.%{av_util_soversion}{,.*}
%else
%{_libdir}/avutil60.dll
%endif

%dnl --------------------------------------------------------------------------------

%package -n libavutil%{?pkg_suffix}-devel
Summary:        Development files for FFmpeg's utility library
%if !0%{?os2_version}
Requires:       libavutil%{?pkg_suffix}%{_isa} = %{version}-%{release}
%else
Requires:       libavutil%{?pkg_suffix} = %{version}-%{release}
%endif
Requires:       pkgconfig
Obsoletes:      libpostproc%{?pkg_suffix}-devel < 8.0

%description -n libavutil%{?pkg_suffix}-devel
The libavutil library is a utility library to aid portable multimedia
programming. It contains safe portable string functions, random
number generators, data structures, additional mathematics functions,
cryptography and multimedia related functionality (like enumerations
for pixel and sample formats).

This subpackage contains the headers for FFmpeg libavutil.

%files -n libavutil%{?pkg_suffix}-devel
%{_includedir}/%{name}/libavutil
%{_libdir}/pkgconfig/libavutil.pc
%if !0%{?os2_version}
%{_libdir}/libavutil.so
%else
%{_libdir}/libavutil_dll.a
%{_libdir}/libavutil_dll.lib
%endif
%{_mandir}/man3/libavutil.3*

%dnl --------------------------------------------------------------------------------

%package -n libswresample%{?pkg_suffix}
Summary:        FFmpeg software resampling library
%if !0%{?os2_version}
Requires:       libavutil%{?pkg_suffix}%{_isa} = %{version}-%{release}
%else
Requires:       libavutil%{?pkg_suffix} = %{version}-%{release}
%endif

%description -n libswresample%{?pkg_suffix}
The libswresample library performs audio conversion between different
sample rates, channel layout and channel formats.

%files -n libswresample%{?pkg_suffix}
%license COPYING.GPLv2 LICENSE.md
%if !0%{?os2_version}
%{_libdir}/libswresample.so.%{swresample_soversion}{,.*}
%else
%{_libdir}/swresa6.dll
%endif

%dnl --------------------------------------------------------------------------------

%package -n libswresample%{?pkg_suffix}-devel
Summary:        Development files for the FFmpeg software resampling library
Requires:       libavutil%{?pkg_suffix}-devel = %{version}-%{release}
%if !0%{?os2_version}
Requires:       libswresample%{?pkg_suffix}%{_isa} = %{version}-%{release}
%else
Requires:       libswresample%{?pkg_suffix} = %{version}-%{release}
%endif

%description -n libswresample%{?pkg_suffix}-devel
The libswresample library performs audio conversion between different
sample rates, channel layout and channel formats.

This subpackage contains the headers for FFmpeg libswresample.

%files -n libswresample%{?pkg_suffix}-devel
%{_includedir}/%{name}/libswresample
%{_libdir}/pkgconfig/libswresample.pc
%if !0%{?os2_version}
%{_libdir}/libswresample.so
%else
%{_libdir}/libswresample_dll.a
%{_libdir}/libswresample_dll.lib
%endif
%{_mandir}/man3/libswresample.3*

%dnl --------------------------------------------------------------------------------

%package -n libswscale%{?pkg_suffix}
Summary:        FFmpeg image scaling and colorspace/pixel conversion library
%if !0%{?os2_version}
Requires:       libavutil%{?pkg_suffix}%{_isa} = %{version}-%{release}
%else
Requires:       libavutil%{?pkg_suffix} = %{version}-%{release}
%endif

%description -n libswscale%{?pkg_suffix}
The libswscale library performs image scaling and colorspace and
pixel format conversion operations.

%files -n libswscale%{?pkg_suffix}
%license COPYING.GPLv2 LICENSE.md
%if !0%{?os2_version}
%{_libdir}/libswscale.so.%{swscale_soversion}{,.*}
%else
%{_libdir}/swscal9.dll
%endif

%dnl --------------------------------------------------------------------------------

%package -n libswscale%{?pkg_suffix}-devel
Summary:        Development files for FFmpeg's image scaling and colorspace library
Provides:       libswscale%{?pkg_suffix}-devel = %{version}-%{release}
Conflicts:      libswscale%{?pkg_suffix}-devel < %{version}-%{release}
Requires:       libavutil%{?pkg_suffix}-devel = %{version}-%{release}
%if !0%{?os2_version}
Requires:       libswscale%{?pkg_suffix}%{_isa} = %{version}-%{release}
%else
Requires:       libswscale%{?pkg_suffix} = %{version}-%{release}
%endif

%description -n libswscale%{?pkg_suffix}-devel
The libswscale library performs image scaling and colorspace and
pixel format conversion operations.

This subpackage contains the headers for FFmpeg libswscale.

%files -n libswscale%{?pkg_suffix}-devel
%{_includedir}/%{name}/libswscale
%{_libdir}/pkgconfig/libswscale.pc
%if !0%{?os2_version}
%{_libdir}/libswscale.so
%else
%{_libdir}/libswscale_dll.a
%{_libdir}/libswscale_dll.lib
%endif
%{_mandir}/man3/libswscale.3*

%endif
# freeworld_lavc bcond

%dnl --------------------------------------------------------------------------------

%if %{with freeworld_lavc}
%package -n libavcodec-freeworld
Summary:        FFmpeg codec library - freeworld overlay
Requires:       libavutil%{?basepkg_suffix}%{_isa} >= %{version}-%{release}
Requires:       libswresample%{?basepkg_suffix}%{_isa} >= %{version}-%{release}
Supplements:    libavcodec%{?basepkg_suffix}%{_isa} >= %{version}-%{release}
# We require libopenh264 library, which has a dummy implementation and a real one
# In the event that this is being installed, we want to install this version
Requires:       openh264%{_isa}

%description -n libavcodec-freeworld
The libavcodec library provides a generic encoding/decoding framework
and contains multiple decoders and encoders for audio, video and
subtitle streams, and several bitstream filters.

This build includes the full range of codecs offered by ffmpeg.

%files -n libavcodec-freeworld
%{_sysconfdir}/ld.so.conf.d/%{name}-%{_lib}.conf
%{_libdir}/%{name}/libavcodec.so.%{av_codec_soversion}{,.*}

# Re-enable ldconfig_scriptlets macros
%{!?ldconfig:%global ldconfig /sbin/ldconfig}
%ldconfig_scriptlets -n libavcodec-freeworld

%endif

%dnl --------------------------------------------------------------------------------

%if 0%{?os2_version}
%legacy_runtime_packages

%debug_package
%endif

%prep
%if !0%{?os2_version}
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'

%autosetup -S git_am
install -m 0644 %{SOURCE20} enable_decoders
install -m 0644 %{SOURCE21} enable_encoders
%else
%scm_setup
%endif
# fix -O3 -g in host_cflags
sed -i "s|check_host_cflags -O3|check_host_cflags %{optflags}|" configure
install -m0755 -d _doc/examples
%if !0%{?os2_version}
cp -a doc/examples/{*.c,Makefile,README} _doc/examples/
%else
cp -a doc/examples/*.c _doc/examples/
cp -a doc/examples/Makefile _doc/examples/
cp -a doc/examples/README _doc/examples/
%endif

%if !0%{?os2_version}
%conf
%else
%build
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"
export LIBS="-lcx"
export VENDOR="${vendor}"
%endif
%set_build_flags

# This is not a normal configure script, don't use %%configure
./configure \
    --prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --datadir=%{_datadir}/%{name} \
    --docdir=%{_docdir}/%{name} \
    --incdir=%{_includedir}/%{name} \
    --libdir=%{_libdir} \
    --mandir=%{_mandir} \
    --arch=%{_target_cpu} \
    --optflags="%{build_cflags}" \
    --extra-ldflags="%{build_ldflags}" \
    --disable-htmlpages \
    --disable-static \
    --disable-stripping \
    --enable-pic \
    --enable-shared \
    --enable-gpl \
    --enable-version3 \
%if !0%{?os2_version}
    --enable-amf \
%endif
    --enable-avcodec \
    --enable-avdevice \
    --enable-avfilter \
    --enable-avformat \
%if !0%{?os2_version}
    --enable-alsa \
%endif
    --enable-bzlib \
%if %{with chromaprint}
    --enable-chromaprint \
%else
    --disable-chromaprint \
%endif
    --disable-cuda-nvcc \
%if %{with ffnvcodec}
    --enable-cuvid \
%endif
    --disable-decklink \
%if !0%{?os2_version}
    --enable-frei0r \
%endif
    --enable-gcrypt \
    --enable-gmp \
    --enable-gnutls \
    --enable-gray \
    --enable-iconv \
%if !0%{?os2_version}
    --enable-ladspa \
%endif
%if %{with lcms2}
    --enable-lcms2 \
%endif
%if !0%{?os2_version}
    --enable-libaom \
    --enable-libaribb24 \
    --enable-libaribcaption \
    --enable-libass \
    --enable-libbluray \
    --enable-libbs2b \
    --enable-libcaca \
    --enable-libcdio \
    --enable-libcodec2 \
    --enable-libdav1d \
%endif
    --disable-libdavs2 \
%if %{with dc1394}
    --enable-libdc1394 \
%endif
%if !0%{?os2_version}
    --enable-libdvdnav \
    --enable-libdvdread \
    --enable-libfdk-aac \
%endif
%if %{with flite}
    --enable-libflite \
%endif
    --enable-libfontconfig \
    --enable-libfreetype \
%if !0%{?os2_version}
    --enable-libfribidi \
    --enable-libgme \
    --enable-libharfbuzz \
    --enable-libgsm \
%endif
%if %{with dc1394}
    --enable-libiec61883 \
%endif
%if !0%{?os2_version}
    --enable-libilbc \
    --enable-libjack \
    --enable-libjxl \
    --enable-libklvanc \
%endif
    --disable-liblensfun \
    --disable-liblcevc-dec \
%if %{with lc3}
    --enable-liblc3 \
%endif
%if !0%{?os2_version}
    --enable-libmodplug \
%endif
    --enable-libmp3lame \
%if !0%{?os2_version}
    --enable-libmysofa \
%endif
    --disable-libnpp \
%if !0%{?os2_version}
    --enable-libopencore-amrnb \
    --enable-libopencore-amrwb \
%endif
    --disable-libopencv \
%if !0%{?os2_version}
    --enable-liboapv \
    --enable-libopenh264 \
%endif
    --enable-libopenjpeg \
%if !0%{?os2_version}
    --enable-libopenmpt \
%endif
    --enable-libopus \
%if %{with placebo}
    --enable-libplacebo \
%endif
%if !0%{?os2_version}
    --enable-libpulse \
    --enable-libqrencode \
%endif
    --disable-libquirc \
%if !0%{?os2_version}
    --enable-librabbitmq \
    --enable-librav1e \
    --enable-librist \
    --enable-librsvg \
%endif
%if %{with librtmp}
    --enable-librtmp \
%endif
%if !0%{?os2_version}
    --enable-librubberband \
    --enable-libshaderc \
%endif
    --disable-libshine \
%if !0%{?os2_version}
    --enable-libsmbclient \
    --enable-libsnappy \
    --enable-libsvtav1 \
    --enable-libsoxr \
    --enable-libspeex \
    --enable-libsrt \
    --enable-libssh \
%endif
    --disable-libtensorflow \
%if !0%{?os2_version}
    --enable-libtesseract \
%endif
    --enable-libtheora \
    --disable-libtorch \
    --disable-libuavs3d \
%if !0%{?os2_version}
    --enable-libtwolame \
    --enable-libv4l2 \
    --enable-libvidstab \
%endif
%if %{with vmaf}
    --enable-libvmaf \
%endif
%if !0%{?os2_version}
    --enable-libvo-amrwbenc \
%endif
    --enable-libvorbis \
%if %{with vpl}
    --enable-libvpl \
%endif
    --enable-libvpx \
    --enable-libwebp \
%if %{with x264}
    --enable-libx264 \
%endif
%if %{with x265}
    --enable-libx265 \
%endif
    --disable-libxavs2 \
    --disable-libxavs \
%if !0%{?os2_version}
    --enable-libxcb \
    --enable-libxcb-shape \
    --enable-libxcb-shm \
    --enable-libxcb-xfixes \
%endif
%if !0%{?os2_version}
%if %{with evc_main}
    --enable-libxeve \
    --enable-libxevd \
%else
    --enable-libxeveb \
    --enable-libxevdb \
%endif
%endif
    --enable-libxml2 \
    --enable-libxvid \
%if !0%{?os2_version}
    --enable-libzimg \
    --enable-libzmq \
    --enable-libzvbi \
%endif
%if %{with lto}
    --enable-lto \
%endif
%if !0%{?os2_version}
    --enable-lv2 \
%endif
    --enable-lzma \
    --enable-manpages \
%if %{with ffnvcodec}
    --enable-nvdec \
    --enable-nvenc \
%endif
%if !0%{?os2_version}
    --enable-openal \
%endif
    --disable-openssl \
    --enable-pthreads \
    --enable-sdl2 \
    --enable-shared \
    --enable-swresample \
    --enable-swscale \
%if !0%{?os2_version}
    --enable-v4l2-m2m \
    --enable-vaapi \
    --enable-vapoursynth \
    --enable-vdpau \
    --enable-vulkan \
    --enable-xlib \
%endif
    --enable-zlib \
%if 0%{?os2_version}
    --disable-decoder=opus \
    --disable-encoder=opus \
    --disable-avx2 --disable-avx512 \
    --extra-cflags="-fno-common" \
%endif
%if %{without all_codecs}
    --enable-muxers \
    --enable-demuxers \
    --enable-hwaccels \
    --disable-encoders \
    --disable-decoders \
    --disable-decoder="h264,hevc,vc1,vvc" \
    --enable-encoder="$(perl -pe 's{^(\w*).*}{$1,}gs' <enable_encoders)" \
    --enable-decoder="$(perl -pe 's{^(\w*).*}{$1,}gs' <enable_decoders)" \
%endif
%ifarch %{power64}
%ifarch ppc64
    --cpu=g5 \
%endif
%ifarch ppc64p7
    --cpu=power7 \
%endif
%ifarch ppc64le
    --cpu=power8 \
%endif
    --enable-pic \
%endif
%ifarch %{arm}
    --disable-runtime-cpudetect --arch=arm \
%ifarch armv6hl
    --cpu=armv6 \
%endif
%ifarch armv7hl armv7hnl
    --cpu=armv7-a \
    --enable-vfpv3 \
    --enable-thumb \
%endif
%ifarch armv7hl
    --disable-neon \
%endif
%ifarch armv7hnl
    --enable-neon \
%endif
%endif
    || cat ffbuild/config.log

cat config.h
cat config_components.h

# Paranoia check
%if %{without all_codecs}
# DECODER
for i in H264 HEVC HEVC_RKMPP VC1 VVC; do
    grep -q "#define CONFIG_${i}_DECODER 0" config_components.h
done

# ENCODER
for i in LIBX264 LIBX264RGB LIBX265; do
    grep -q "#define CONFIG_${i}_ENCODER 0" config_components.h
done
for i in H264 HEVC; do
    for j in MF VIDEOTOOLBOX; do
        grep -q "#define CONFIG_${i}_${j}_ENCODER 0" config_components.h
    done
done
%endif

%if !0%{?os2_version}
%build
%set_build_flags
%endif

%make_build V=1
%make_build documentation V=1
%make_build alltools V=1

%install
%make_install V=1

# We will package is as %%doc in the devel package
rm -rf %{buildroot}%{_datadir}/%{name}/examples

%if %{with freeworld_lavc}
# Install the libavcodec freeworld counterpart
mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d/
mkdir -p %{buildroot}%{_libdir}/%{name}
echo -e "%{_libdir}/%{name}\n" > %{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}-%{_lib}.conf
cp -pa %{buildroot}%{_libdir}/libavcodec.so.%{av_codec_soversion}{,.*} %{buildroot}%{_libdir}/%{name}
# Drop unneeded stuff
rm -f %{buildroot}%{_libdir}/*.*
rm -rf %{buildroot}%{_libdir}/pkgconfig
rm -rf %{buildroot}%{_includedir}
rm -rf %{buildroot}%{_bindir}
rm -rf %{buildroot}%{_datadir}
%endif


%changelog
* Fri Mar 13 2026 Silvan Scherrer <silvan.scherrer@aroa.ch> 8.0.1-1
- update to version 8.0.1
- spec file is now fedora based

* Sat Feb 27 2021 Dmitriy Kuminov <coding@dmik.org> 4.2.2-4
- Fix crashes on AVX hardware [bitwiseworks/ffmpeg-os2#4].

* Mon Jan 4 2021 Dmitriy Kuminov <coding@dmik.org> 4.2.2-3
- Disable broken native Opus decoder/encoder [ffmpeg-os2#4].

* Mon Oct 19 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> 4.2.2-2
- add a legacy package to version 2.8.6 to please ffox
- adjusted spec a bit to have legacy working

* Fri Sep 04 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> 4.2.2-1
- update to version 4.2.2
- enable all features we have available as rpm
- rework the spec file heavily

* Mon Apr 18 2016 Dmitriy Kuminov <coding@dmik.org> 2.8.6-2
- Enable high memory support.

* Fri Apr 15 2016 Dmitriy Kuminov <coding@dmik.org> 2.8.6-1
- Initial release of version 2.8.6.
