# Note: this .spec is borrowed from ffmpeg-2.6.8-1.fc22.src.rpm (rpmfusion.org)

# TODO: add make test to %%check section

%global _without_frei0r   1
%global _without_opencv   1
%global _without_ladspa   1
%global _without_openal   1
%global _without_lame     1
%global _without_cdio     1
%global _without_theora   1
%global _without_vorbis   1
%global _without_vaapi    1
%global _without_x264     1
%global _without_x265     1
%global _without_xvidcore 1
%global _without_pulse    1

%global _without_extra    1

Summary:        Digital VCR and streaming server
Name:           ffmpeg
Version:        2.8.6
Release:        2%{?dist}
%if 0%{?_with_amr:1}
License:        GPLv3+
%else
License:        GPLv2+
%endif
URL:            http://ffmpeg.org/
#Source0:        http://ffmpeg.org/releases/ffmpeg-%{version}.tar.bz2
Vendor:         bww bitwise works GmbH
Requires:       %{name}-libs = %{version}-%{release}

%define github_name FFmpeg
%define github_url  https://github.com/bitwiseworks/%{github_name}/archive
%define github_rev  2587a3aa8d80fb40a0b96d84deda3140bdb4aac8

Source: %{github_name}-%{github_rev}.zip

BuildRequires: gcc make curl zip

BuildRequires: bzip2-devel
BuildRequires: freetype-devel
BuildRequires: fontconfig-devel
%{?_with_celt:BuildRequires: celt-devel}
%{?_with_dirac:BuildRequires: dirac-devel}
%{?_with_faac:BuildRequires: faac-devel}
%{?_with_fdk_aac:BuildRequires: fdk-aac-devel}
BuildRequires:  freetype-devel
%{!?_without_frei0r:BuildRequires: frei0r-devel}
%{!?_without_extra:BuildRequires: gnutls-devel}
%{!?_without_extra:BuildRequires: gsm-devel}
%{!?_without_lame:BuildRequires: lame-devel >= 3.98.3}
%{?_with_jack:BuildRequires: jack-audio-connection-kit-devel}
%{!?_without_ladspa:BuildRequires: ladspa-devel}
%{!?_without_extra:BuildRequires: libass-devel}
%{!?_without_cdio:BuildRequires: libcdio-paranoia-devel}
#libcrystalhd is currently broken
%{?_with_crystalhd:BuildRequires: libcrystalhd-devel}
%{!?_without_extra:BuildRequires: libdc1394-devel}
%{!?_without_extra:Buildrequires: libmodplug-devel}
%{?_with_rtmp:BuildRequires: librtmp-devel}
%{!?_without_theora:BuildRequires: libtheora-devel}
%{!?_without_extra:BuildRequires: libv4l-devel}
%{!?_without_extra:BuildRequires: libvdpau-devel}
%{!?_without_vorbis:BuildRequires:  libvorbis-devel}
%{!?_without_vpx:BuildRequires: libvpx-devel >= 0.9.1}
%ifarch %{ix86} x86_64
%{!?_without_extra:BuildRequires: libXvMC-devel}
%{?!_without_vaapi:BuildRequires: libva-devel >= 0.31.0}
%endif
%{?_with_amr:BuildRequires: opencore-amr-devel vo-amrwbenc-devel}
%{!?_without_openal:BuildRequires: openal-soft-devel}
%{?_with_opencl:BuildRequires: opencl-headers ocl-icd-devel}
%{!?_without_opencv:BuildRequires: opencv-devel}
%{!?_without_extra:BuildRequires: openjpeg-devel}
%{!?_without_extra:BuildRequires: opus-devel}
%{!?_without_pulse:BuildRequires: pulseaudio-libs-devel}
#BuildRequires:  perl(Pod::Man)
%{!?_without_extra:BuildRequires: schroedinger-devel}
BuildRequires: SDL-devel
%{!?_without_extra:BuildRequires: soxr-devel}
%{!?_without_extra:BuildRequires: speex-devel}
#BuildRequires: subversion
#BuildRequires:  texi2html
BuildRequires:  texinfo
%{!?_without_x264:BuildRequires: x264-devel >= 0.0.0-0.31}
%{!?_without_x265:BuildRequires: x265-devel}
%{!?_without_xvidcore:BuildRequires: xvidcore-devel}
BuildRequires:  zlib-devel
%ifarch %{ix86} x86_64
#BuildRequires:  yasm
%endif

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

%package     -n libavdevice
Summary:        Special devices muxing/demuxing library

%description -n libavdevice
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

%debug_package

%global ff_configure \
./configure \\\
    --prefix=%{_prefix} \\\
    --bindir=%{_bindir} \\\
    --datadir=%{_datadir}/%{name} \\\
    --incdir=%{_includedir}/%{name} \\\
    --libdir=%{_libdir} \\\
    --mandir=%{_mandir} \\\
    --arch=%{_arch} \\\
    --optflags="$RPM_OPT_FLAGS" \\\
    %{?_with_amr:--enable-libopencore-amrnb --enable-libopencore-amrwb --enable-libvo-amrwbenc --enable-version3} \\\
    --enable-bzlib \\\
    %{!?_with_crystalhd:--disable-crystalhd} \\\
    %{!?_without_frei0r:--enable-frei0r} \\\
    %{!?_without_extra:--enable-gnutls} \\\
    %{!?_without_ladspa:--enable-ladspa} \\\
    %{!?_without_extra:--enable-libass} \\\
    %{!?_without_cdio:--enable-libcdio} \\\
    %{?_with_celt:--enable-libcelt} \\\
    %{!?_without_extra:--enable-libdc1394} \\\
    %{?_with_dirac:--enable-libdirac} \\\
    %{?_with_faac:--enable-libfaac --enable-nonfree} \\\
    %{?_with_fdk-aac:--enable-libfdk-aac --enable-nonfree} \\\
    %{!?_with_jack:--disable-indev=jack} \\\
    --enable-libfreetype \\\
    --enable-fontconfig \\\
    %{!?_without_extra:--enable-libgsm} \\\
    %{!?_without_lame:--enable-libmp3lame} \\\
    %{?_with_nvenc:--enable-nvenc  --enable-nonfree} \\\
    %{!?_without_openal:--enable-openal} \\\
    %{?_with_opencl:--enable-opencl} \\\
    %{!?_without_opencv:--enable-libopencv} \\\
    %{!?_without_extra:--enable-libopenjpeg} \\\
    %{!?_without_extra:--enable-libopus} \\\
    %{!?_without_pulse:--enable-libpulse} \\\
    %{?_with_rtmp:--enable-librtmp} \\\
    %{!?_without_extra:--enable-libschroedinger} \\\
    %{!?_without_extra:--enable-libsoxr} \\\
    %{!?_without_extra:--enable-libspeex} \\\
    %{!?_without_theora:--enable-libtheora} \\\
    %{!?_without_vorbis:--enable-libvorbis} \\\
    %{!?_without_extra:--enable-libv4l2} \\\
    %{!?_without_vpx:--enable-libvpx} \\\
    %{!?_without_x264:--enable-libx264} \\\
    %{!?_without_x265:--enable-libx265} \\\
    %{!?_without_xvidcore:--enable-libxvid} \\\
    %{!?_without_extra:--enable-x11grab} \\\
    --enable-avfilter \\\
    --enable-avresample \\\
    --enable-postproc \\\
    %{!?_without_extra:--enable-pthreads} \\\
    --disable-static \\\
    --enable-shared \\\
    --enable-gpl \\\
    --disable-debug \\\
    --disable-stripping


%prep
%if %(sh -c 'if test -f "%{_sourcedir}/%{github_name}-%{github_rev}.zip" ; then echo 1 ; else echo 0 ; fi')
%setup -n "%{github_name}-%{github_rev}" -q
%else
%setup -n "%{github_name}-%{github_rev}" -Tc
rm -f "%{_sourcedir}/%{github_name}-%{github_rev}.zip"
curl -sSL "%{github_url}/%{github_rev}.zip" -o "%{_sourcedir}/%{github_name}-%{github_rev}.zip"
unzip "%{_sourcedir}/%{github_name}-%{github_rev}.zip" -d ..
%endif

# fix -O3 -g in host_cflags
sed -i "s|-O3 -g|$RPM_OPT_FLAGS|" configure

%build
%{ff_configure}\
    --shlibdir=%{_libdir} \
    --disable-doc \
%if 0%{?ffmpegsuffix:1}
    --build-suffix=%{ffmpegsuffix} \
    --disable-ffmpeg --disable-ffplay --disable-ffprobe --disable-ffserver \
%else
%ifarch %{ix86}
    --cpu=%{_target_cpu} \
%endif
%ifarch %{ix86} x86_64 ppc ppc64
    --enable-runtime-cpudetect \
%endif
%endif
    --extra-ldflags="-Zhigh-mem" \
    --extra-libs="-lpoll -lmmap"

make %{?_smp_mflags} V=1
make documentation V=1
make alltools V=1

%install
make install DESTDIR=$RPM_BUILD_ROOT V=1
%if 0%{!?ffmpegsuffix:1}
install -pm755 tools/qt-faststart.exe $RPM_BUILD_ROOT%{_bindir}
%endif

%post libs

%postun libs

%if 0%{!?ffmpegsuffix:1}
%files
%doc COPYING.* CREDITS README.md doc/ffserver.conf
%{_bindir}/ffmpeg.exe
%{_bindir}/ffplay.exe
%{_bindir}/ffprobe.exe
%{_bindir}/ffserver.exe
%{_bindir}/qt-faststart.exe
# @todo we miss perl(Pod::Man) or such
#%{_mandir}/man1/ffmpeg*.1*
#%{_mandir}/man1/ffplay*.1*
#%{_mandir}/man1/ffprobe*.1*
#%{_mandir}/man1/ffserver*.1*
%{_datadir}/ffmpeg
%endif

%files libs
%{_libdir}/*.dll
%exclude %{_libdir}/avdevi*.dll
# @todo we miss perl(Pod::Man) or such
#%{_mandir}/man3/lib*.3.gz

%files -n libavdevice
%{_libdir}/avdevi*.dll

%files devel
%doc MAINTAINERS doc/APIchanges doc/*.txt
%{_includedir}/ffmpeg
%{_libdir}/pkgconfig/lib*.pc
%{_libdir}/*.a
%{_libdir}/*.lib


%changelog
* Mon Apr 18 2016 Dmitriy Kuminov <coding@dmik.org> 2.8.6-2
- Enable high memory support.

* Fri Apr 15 2016 Dmitriy Kuminov <coding@dmik.org> 2.8.6-1
- Initial release of version 2.8.6.
