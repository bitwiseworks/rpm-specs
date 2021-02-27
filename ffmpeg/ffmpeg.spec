# Note: this .spec is borrowed from ffmpeg-4.3.1-9.fc33.src.rpm (rpmfusion.org)

%if 0%{?os2_version}
%global _with_webp        1
%global _without_frei0r   1
%global _without_jack     1
%global _without_ladspa   1
%global _without_aom      1
%global _without_dav1d    1
%global _without_ass      1
%global _without_bluray   1
%global _without_cdio     1
%global _without_lensfun  1
%global _without_amr      1
%global _without_pulse    1
%global _without_openal   1
%global _without_opencl   1
%global _without_zvbi     1
%global _without_vaapi    1
%global _without_x265     1
%global _without_vidstab  1
%global _without_fribidi  1
%global _without_opengl   1
%endif

# Native Opus decoder is currently broken on OS/2, see
# https://github.com/bitwiseworks/ffmpeg-os2/issues/4
%if 0%{?os2_version}
%global _without_native_opus    1
%endif

# AVX2 and above will not work on OS/2 due to alignment problems in GCC. Also
# we need to dsiable merging uninitialized vars to get proper alignment for AVX,
# see https://github.com/bitwiseworks/ffmpeg-os2/issues/5
%if 0%{?os2_version}
%global _without_avx2           1
%global _no_var_merge           1
%endif

# TODO: add make test to %%check section

#global branch  oldabi-
#global date    20200606
#global rel     rc1

%ifarch %{ix86}
# Fails due to asm issue
%global _lto_cflags %{nil}
# libavfilter has undefined glslang symbols
%global _without_vulkan   1
%endif

# rav1e is rawhide only so there is no point enabling it.
%if 0%{?fedora} > 33
#global _with_rav1e       1
%endif

# Cuda and others are only available on some arches
%global cuda_arches x86_64

%if 0%{?el7}
%global _without_aom      1
%global _without_dav1d    1
%global _without_frei0r   1
%global _without_opus     1
%global _without_vpx      1
%endif

%if 0%{?fedora} || 0%{?rhel} > 7
%ifarch x86_64 i686
%global _with_vapoursynth 1
%endif
%ifarch x86_64
%global _with_mfx         1
%global _with_vmaf        1
%endif
%endif

%if 0%{?rhel} || 0%{?os2_version}
%global _without_lensfun  1
%global _without_vulkan   1
%endif

# flavor nonfree
%if 0%{?_with_cuda:1}
%global debug_package %{nil}
%global flavor           -cuda
%global progs_suffix     -cuda
#global build_suffix     -lgpl
%ifarch %{cuda_arches}
%global _with_cuvid      1
%global _with_libnpp     1
%endif
%global _with_fdk_aac    1
%global _without_cdio    1
%global _without_frei0r  1
%global _without_gpl     1
%global _without_vidstab 1
%global _without_x264    1
%global _without_x265    1
%global _without_xvid    1
%endif

# Disable nvenc when not relevant
%ifnarch %{cuda_arches} aarch64
%global _without_nvenc    1
%endif

# extras flags
%if 0%{!?_cuda_version:1}
%global _cuda_version 10.2
%endif
%global _cuda_version_rpm %(echo %{_cuda_version} | sed -e 's/\\./-/')
%global _cuda_bindir %{_cuda_prefix}/bin
%if 0%{?_with_cuda:1}
%global cuda_cflags $(pkg-config --cflags cuda-%{_cuda_version})
%global cuda_ldflags $(pkg-config --libs cuda-%{_cuda_version})
%endif

%if 0%{?_with_libnpp:1}
%global libnpp_cflags $(pkg-config --cflags nppi-%{_cuda_version} nppc-%{_cuda_version})
%global libnpp_ldlags $(pkg-config --libs-only-L nppi-%{_cuda_version} nppc-%{_cuda_version})
%endif

%if 0%{?_with_rpi:1}
%global _with_omx        1
%global _with_omx_rpi    1
%global _with_mmal       1
ExclusiveArch: armv7hnl
%endif

%if 0%{?_without_gpl}
%global lesser L
%endif

%if 0%{!?_without_amr} || 0%{?_with_gmp} || 0%{?_with_smb}
%global ffmpeg_license %{?lesser}GPLv3+
%else
%global ffmpeg_license %{?lesser}GPLv2+
%endif

Summary:        Digital VCR and streaming server
Name:           ffmpeg%{?flavor}
Version:        4.2.2
Release:        4%{?date}%{?date:git}%{?rel}%{?dist}
License:        %{ffmpeg_license}
URL:            http://ffmpeg.org/
%if !0%{?os2_version}
%if 0%{?date}
Source0:        ffmpeg-%{?branch}%{date}.tar.bz2
%else
Source0:        http://ffmpeg.org/releases/ffmpeg-%{version}.tar.xz
%endif
%else
Vendor:         bww bitwise works GmbH
%scm_source     github http://github.com/bitwiseworks/%{name}-os2 n%{version}-os2
%endif
Requires:       %{name}-libs = %{version}-%{release}
%{?_with_cuda:BuildRequires: cuda-minimal-build-%{_cuda_version_rpm} cuda-drivers-devel}
%{?_with_libnpp:BuildRequires: pkgconfig(nppc-%{_cuda_version})}
%if !0%{?os2_version}
BuildRequires:  alsa-lib-devel
%endif
BuildRequires:  bzip2-devel
%{?_with_faac:BuildRequires: faac-devel}
%{?_with_fdk_aac:BuildRequires: fdk-aac-devel}
%{?_with_flite:BuildRequires: flite-devel}
BuildRequires:  fontconfig-devel
BuildRequires:  freetype-devel
%if !0%{?os2_version}
BuildRequires:  fribidi-devel
%endif
%{!?_without_frei0r:BuildRequires: frei0r-devel}
%{?_with_gme:BuildRequires: game-music-emu-devel}
BuildRequires:  gnutls-devel
%if !0%{?os2_version}
BuildRequires:  gsm-devel
%endif
%{?_with_ilbc:BuildRequires: ilbc-devel}
BuildRequires:  lame-devel >= 3.98.3
%{!?_without_jack:BuildRequires: jack-audio-connection-kit-devel}
%{!?_without_ladspa:BuildRequires: ladspa-devel}
%{!?_without_aom:BuildRequires:  libaom-devel}
%{!?_without_dav1d:BuildRequires:  libdav1d-devel >= 0.2.1}
%{!?_without_ass:BuildRequires:  libass-devel}
%{!?_without_bluray:BuildRequires:  libbluray-devel}
%{?_with_bs2b:BuildRequires: libbs2b-devel}
%{?_with_caca:BuildRequires: libcaca-devel}
%{!?_without_cdio:BuildRequires: libcdio-paranoia-devel}
%{?_with_chromaprint:BuildRequires: libchromaprint-devel}
%{?_with_crystalhd:BuildRequires: libcrystalhd-devel}
%{!?_without_lensfun:BuildRequires: lensfun-devel}
%if 0%{?_with_ieee1394}
BuildRequires:  libavc1394-devel
BuildRequires:  libdc1394-devel
BuildRequires:  libiec61883-devel
%endif
%if !0%{?os2_version}
BuildRequires:  libdrm-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  libGL-devel
BuildRequires:  libmodplug-devel
BuildRequires:  libmysofa-devel
BuildRequires:  libopenmpt-devel
BuildRequires:  librsvg2-devel
%endif
%{?_with_rtmp:BuildRequires: librtmp-devel}
%{?_with_smb:BuildRequires: libsmbclient-devel}
%if !0%{?os2_version}
BuildRequires:  libssh-devel
%endif
BuildRequires:  libtheora-devel
%if !0%{?os2_version}
BuildRequires:  libv4l-devel
%endif
%{?!_without_vaapi:BuildRequires: libva-devel >= 0.31.0}
%if !0%{?os2_version}
BuildRequires:  libvdpau-devel
%endif
BuildRequires:  libvorbis-devel
%{?_with_vapoursynth:BuildRequires: vapoursynth-devel}
%{?!_without_vpx:BuildRequires: libvpx-devel >= 1.4.0}
%{?_with_mfx:BuildRequires: pkgconfig(libmfx) >= 1.23-1}
%ifarch %{ix86} x86_64
BuildRequires:  nasm
%endif
%{?_with_webp:BuildRequires: libwebp-devel}
%{?_with_netcdf:BuildRequires: netcdf-devel}
%{?_with_rpi:BuildRequires: raspberrypi-vc-devel}
%{!?_without_nvenc:BuildRequires: nv-codec-headers}
%{!?_without_amr:BuildRequires: opencore-amr-devel vo-amrwbenc-devel}
%{?_with_omx:BuildRequires: libomxil-bellagio-devel}
%if !0%{?os2_version}
BuildRequires:  libxcb-devel
%endif
%{!?_without_openal:BuildRequires: openal-soft-devel}
%if 0%{!?_without_opencl:1}
BuildRequires:  opencl-headers ocl-icd-devel
%{?fedora:Recommends: opencl-icd}
%endif
%{?_with_opencv:BuildRequires: opencv-devel}
BuildRequires:  openjpeg2-devel
%{!?_without_opus:BuildRequires: opus-devel >= 1.1.3}
%{!?_without_pulse:BuildRequires: pulseaudio-libs-devel}
BuildRequires:  perl(Pod::Man)
%{?_with_rav1e:BuildRequires: rav1e-devel}
%{?_with_rubberband:BuildRequires: rubberband-devel}
%{!?_without_tools:BuildRequires: SDL2-devel}
%{?_with_snappy:BuildRequires: snappy-devel}
%if !0%{?os2_version}
BuildRequires:  soxr-devel
BuildRequires:  speex-devel
BuildRequires:  pkgconfig(srt)
%endif
%{?_with_tesseract:BuildRequires: tesseract-devel}
#BuildRequires:  texi2html
BuildRequires:  texinfo
%{?_with_twolame:BuildRequires: twolame-devel}
%{?_with_vmaf:BuildRequires: libvmaf-devel}
%{?_with_wavpack:BuildRequires: wavpack-devel}
%{!?_without_vidstab:BuildRequires:  vid.stab-devel}
%{!?_without_vulkan:BuildRequires:  vulkan-loader-devel glslang-devel >= 11.0}
%{!?_without_x264:BuildRequires: x264-devel >= 0.0.0-0.31}
%{!?_without_x265:BuildRequires: x265-devel}
%{!?_without_xvid:BuildRequires: xvidcore-devel}
%if !0%{?os2_version}
BuildRequires:  zimg-devel >= 2.7.0
%endif
BuildRequires:  zlib-devel
%{?_with_zmq:BuildRequires: zeromq-devel}
%{!?_without_zvbi:BuildRequires: zvbi-devel}

%description
FFmpeg is a complete and free Internet live audio and video
broadcasting solution for Linux/Unix. It also includes a digital
VCR. It can encode in real time in many formats including MPEG1 audio
and video, MPEG4, h263, ac3, asf, avi, real, mjpeg, and flash.

%package        libs
Summary:        Libraries for %{name}

%description    libs
FFmpeg is a complete and free Internet live audio and video
broadcasting solution for Linux/Unix. It also includes a digital
VCR. It can encode in real time in many formats including MPEG1 audio
and video, MPEG4, h263, ac3, asf, avi, real, mjpeg, and flash.
This package contains the libraries for %{name}

%package     -n libavdevice%{?flavor}
Summary:        Special devices muxing/demuxing library
Requires:       %{name}-libs = %{version}-%{release}

%description -n libavdevice%{?flavor}
Libavdevice is a complementary library to libavf "libavformat". It provides
various "special" platform-specific muxers and demuxers, e.g. for grabbing
devices, audio capture and playback etc.

%package        devel
Summary:        Development package for %{name}
Requires:       %{name}-libs = %{version}-%{release}
Requires:       libavdevice = %{version}-%{release}
Requires:       pkgconfig

%description    devel
FFmpeg is a complete and free Internet live audio and video
broadcasting solution for Linux/Unix. It also includes a digital
VCR. It can encode in real time in many formats including MPEG1 audio
and video, MPEG4, h263, ac3, asf, avi, real, mjpeg, and flash.
This package contains development files for %{name}

%legacy_runtime_packages

%debug_package

%global ff_configure \
./configure \\\
    --prefix=%{_prefix} \\\
    --bindir=%{_bindir} \\\
    --datadir=%{_datadir}/%{name} \\\
    --docdir=%{_docdir}/%{name} \\\
    --incdir=%{_includedir}/%{name} \\\
    --libdir=%{_libdir} \\\
    --mandir=%{_mandir} \\\
    --arch=%{_target_cpu} \\\
    --optflags="%{optflags}" \\\
    --extra-ldflags="-Zhigh-mem %{?__global_ldflags} %{?cuda_ldflags} %{?libnpp_ldlags}" \\\
    --extra-cflags="%{?cuda_cflags} %{?libnpp_cflags} %{?_no_var_merge:-fno-common}" \\\
    %{?_without_avx2:--disable-avx2 --disable-avx512} \\\
    %{?flavor:--disable-manpages} \\\
    %{?progs_suffix:--progs-suffix=%{progs_suffix}} \\\
    %{?build_suffix:--build-suffix=%{build_suffix}} \\\
    %{!?_without_amr:--enable-libopencore-amrnb --enable-libopencore-amrwb --enable-libvo-amrwbenc --enable-version3} \\\
    --enable-bzlib \\\
    %{?_with_chromaprint:--enable-chromaprint} \\\
    %{!?_with_crystalhd:--disable-crystalhd} \\\
    --enable-fontconfig \\\
    %{!?_without_frei0r:--enable-frei0r} \\\
    %{?!os2_version:--enable-gcrypt} \\\
    %{?_with_gmp:--enable-gmp --enable-version3} \\\
    --enable-gnutls \\\
    %{!?_without_ladspa:--enable-ladspa} \\\
    %{!?_without_aom:--enable-libaom} \\\
    %{!?_without_dav1d:--enable-libdav1d} \\\
    %{!?_without_ass:--enable-libass} \\\
    %{!?_without_bluray:--enable-libbluray} \\\
    %{?_with_bs2b:--enable-libbs2b} \\\
    %{?_with_caca:--enable-libcaca} \\\
    %{?_with_cuda:--enable-cuda-sdk --enable-nonfree} \\\
    %{?_with_cuvid:--enable-cuvid --enable-nonfree} \\\
    %{!?_without_cdio:--enable-libcdio} \\\
    %{?_with_ieee1394:--enable-libdc1394 --enable-libiec61883} \\\
    %{?!os2_version:--enable-libdrm} \\\
    %{?_with_faac:--enable-libfaac --enable-nonfree} \\\
    %{?_with_fdk_aac:--enable-libfdk-aac --enable-nonfree} \\\
    %{?_with_flite:--enable-libflite} \\\
    %{!?_without_jack:--enable-libjack} \\\
    --enable-libfreetype \\\
    %{!?_without_fribidi:--enable-libfribidi} \\\
    %{?_with_gme:--enable-libgme} \\\
    %{?!os2_version:--enable-libgsm} \\\
    %{?_with_ilbc:--enable-libilbc} \\\
    %{!?_without_lensfun:--enable-liblensfun} \\\
    %{?_with_libnpp:--enable-libnpp --enable-nonfree} \\\
    --enable-libmp3lame \\\
    %{?!os2_version:--enable-libmysofa} \\\
    %{?_with_netcdf:--enable-netcdf} \\\
    %{?_with_mmal:--enable-mmal} \\\
    %{!?_without_nvenc:--enable-nvenc} \\\
    %{?_with_omx:--enable-omx} \\\
    %{?_with_omx_rpi:--enable-omx-rpi} \\\
    %{!?_without_openal:--enable-openal} \\\
    %{!?_without_opencl:--enable-opencl} \\\
    %{?_with_opencv:--enable-libopencv} \\\
    %{!?_without_opengl:--enable-opengl} \\\
    --enable-libopenjpeg \\\
    %{?!os2_version:--enable-libopenmpt} \\\
    %{!?_without_opus:--enable-libopus} \\\
    %{?_without_native_opus:--disable-decoder=opus} \\\
    %{?_without_native_opus:--disable-encoder=opus} \\\
    %{!?_without_pulse:--enable-libpulse} \\\
    %{?!os2_version:--enable-librsvg} \\\
    %{?_with_rav1e:--enable-librav1e} \\\
    %{?_with_rtmp:--enable-librtmp} \\\
    %{?_with_rubberband:--enable-librubberband} \\\
    %{?_with_smb:--enable-libsmbclient} \\\
    %{?_with_snappy:--enable-libsnappy} \\\
    %{?!os2_version:--enable-libsoxr} \\\
    %{?!os2_version:--enable-libspeex} \\\
    %{?!os2_version:--enable-libssh} \\\
    %{?_with_tesseract:--enable-libtesseract} \\\
    --enable-libtheora \\\
    %{?_with_twolame:--enable-libtwolame} \\\
    --enable-libvorbis \\\
    %{?!os2_version:--enable-libv4l2} \\\
    %{!?_without_vidstab:--enable-libvidstab} \\\
    %{?_with_vmaf:--enable-libvmaf --enable-version3} \\\
    %{?_with_vapoursynth:--enable-vapoursynth} \\\
    %{!?_without_vpx:--enable-libvpx} \\\
    %{!?_without_vulkan:--enable-vulkan --enable-libglslang} \\\
    %{?_with_webp:--enable-libwebp} \\\
    %{!?_without_x264:--enable-libx264} \\\
    %{!?_without_x265:--enable-libx265} \\\
    %{!?_without_xvid:--enable-libxvid} \\\
    %{?!os2_version:--enable-libzimg} \\\
    %{?_with_zmq:--enable-libzmq} \\\
    %{!?_without_zvbi:--enable-libzvbi} \\\
    --enable-avfilter \\\
    --enable-avresample \\\
    %{?!os2_version:--enable-libmodplug} \\\
    --enable-postproc \\\
    %{?!os2_version:--enable-pthreads} \\\
    --disable-static \\\
    --enable-shared \\\
    %{!?_without_gpl:--enable-gpl} \\\
    --disable-debug \\\
    --disable-stripping


%prep
%if !0%{?os2_version}
%if 0%{?date}
%autosetup -p1 -n ffmpeg-%{?branch}%{date}
echo "git-snapshot-%{?branch}%{date}-rpmfusion" > VERSION
%else
%autosetup -p1 -n ffmpeg-%{version}
%endif
%else
%scm_setup
%endif
# fix -O3 -g in host_cflags
sed -i "s|check_host_cflags -O3|check_host_cflags %{optflags}|" configure
mkdir -p _doc/examples
cp -pr doc/examples/*.c _doc/examples/
cp -pr doc/examples/Makefile _doc/examples/
cp -pr doc/examples/README _doc/examples/

%build
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"
export LIBS="-lcx"
export VENDOR="${vendor}"
%{?_with_cuda:export PATH=${PATH}:%{_cuda_bindir}}
%{ff_configure}\
    --shlibdir=%{_libdir} \
%if 0%{?_without_tools:1}
    --disable-doc \
    --disable-ffmpeg --disable-ffplay --disable-ffprobe \
%endif
%ifnarch %{ix86}
    --enable-lto \
%endif
%ifarch %{ix86}
    --cpu=%{_target_cpu} \
%endif
    %{?_with_mfx:--enable-libmfx} \
%ifarch %{ix86} x86_64 %{power64}
    --enable-runtime-cpudetect \
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

make %{?_smp_mflags} V=1
make documentation V=1
make alltools V=1

%install
%make_install V=1
%if 0%{!?flavor:1}
rm -r %{buildroot}%{_datadir}/%{name}/examples
%endif
%if 0%{!?progs_suffix:1}
install -pm755 tools/qt-faststart.exe %{buildroot}%{_bindir}
%endif

%if !0%{?os2_version}
%ldconfig_scriptlets  libs
%ldconfig_scriptlets -n libavdevice%{?flavor}
%endif

%if 0%{!?_without_tools:1}
%files
%{_bindir}/ffmpeg.exe
%{_bindir}/ffplay.exe
%{_bindir}/ffprobe.exe
%{!?progs_suffix:%{_bindir}/qt-faststart.exe}
%{!?flavor:
%{_mandir}/man1/ffmpeg*.1*
%{_mandir}/man1/ffplay*.1*
%{_mandir}/man1/ffprobe*.1*
}
%{_datadir}/%{name}
%endif

%files libs
%doc  CREDITS README.md
%license COPYING.*
%{_libdir}/avcode58.dll
%{_libdir}/avfilt7.dll
%{_libdir}/avform58.dll
%{_libdir}/avresa4.dll
%{_libdir}/avutil56.dll
%{_libdir}/postpr55.dll
%{_libdir}/swresa3.dll
%{_libdir}/swscal5.dll
%{!?flavor:%{_mandir}/man3/lib*.3.*
%exclude %{_mandir}/man3/libavdevice.3*
}

%files -n libavdevice%{?flavor}
%{_libdir}/avdevi58.dll
%{!?flavor:%{_mandir}/man3/libavdevice.3*}

%files devel
%doc MAINTAINERS doc/APIchanges doc/*.txt
%doc _doc/examples
%doc %{_docdir}/%{name}/*.html
%{_includedir}/%{name}
%{_libdir}/pkgconfig/lib*.pc
%{_libdir}/*_dll.a
%{_libdir}/*.lib


%changelog
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
