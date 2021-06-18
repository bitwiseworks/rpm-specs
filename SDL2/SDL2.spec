Name:           SDL2
Version:        2.0.12
Release:        3%{?dist}
Summary:        Cross-platform multimedia library

License:        zlib and MIT
URL:            http://www.libsdl.org/
Vendor:         bww bitwise works GmbH
%scm_source     github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2-1


BuildRequires:  gcc
%if !0%{?os2_version}
BuildRequires:  alsa-lib-devel
BuildRequires:  audiofile-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libGLU-devel
BuildRequires:  mesa-libEGL-devel
BuildRequires:  mesa-libGLES-devel
BuildRequires:  libXext-devel
BuildRequires:  libX11-devel
BuildRequires:  libXi-devel
BuildRequires:  libXrandr-devel
BuildRequires:  libXrender-devel
BuildRequires:  libXScrnSaver-devel
BuildRequires:  libusb-devel
BuildRequires:  libXinerama-devel
BuildRequires:  libXcursor-devel
BuildRequires:  systemd-devel
# PulseAudio
BuildRequires:  pkgconfig(libpulse-simple)
# Jack
BuildRequires:  pkgconfig(jack)
# D-Bus
BuildRequires:  pkgconfig(dbus-1)
# IBus
BuildRequires:  pkgconfig(ibus-1.0)
# Wayland
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(xkbcommon)
# Vulkan
BuildRequires:  vulkan-devel
# KMS
BuildRequires:  mesa-libgbm-devel
BuildRequires:  libdrm-devel
%endif
BuildRequires:  os2tk45-libs os2tk45-headers

%description
Simple DirectMedia Layer (SDL) is a cross-platform multimedia library designed
to provide fast access to the graphics frame buffer and audio device.

%package devel
Summary:        Files needed to develop Simple DirectMedia Layer applications
Requires:       %{name} = %{version}-%{release}
%if !0%{?os2_version}
Requires:       mesa-libEGL-devel
Requires:       mesa-libGLES-devel
Requires:       libX11-devel
%endif

%description devel
Simple DirectMedia Layer (SDL) is a cross-platform multimedia library designed
to provide fast access to the graphics frame buffer and audio device. This
package provides the libraries, include files, and other resources needed for
developing SDL applications.

%package static
Summary:        Static libraries for SDL2

%description static
Static libraries for SDL2.

%debug_package

%prep
%scm_setup

# Compilation without ESD
%if !0%{?os2_version}
sed -i -e 's/.*AM_PATH_ESD.*//' configure.ac
sed -i -e 's/\r//g' TODO.txt README.txt WhatsNew.txt BUGS.txt COPYING.txt CREDITS.txt README-SDL.txt
%endif
autoreconf -fvi

%build
export LDFLAGS=" -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx -lmmpm2"
export CFLAGS="-idirafter /@unixroot/usr/include/os2tk45"

%configure \
    --enable-sdl-dlopen \
%if !0%{?os2_version}
    --enable-video-kmsdrm \
%endif
    --disable-arts \
    --disable-esd \
    --disable-nas \
%if !0%{?os2_version}
    --enable-pulseaudio-shared \
    --enable-jack-shared \
    --enable-alsa \
    --enable-video-wayland \
    --enable-video-vulkan \
%endif
    --enable-sse2=no \
    --enable-sse3=no \
    --disable-rpath \
%ifarch ppc64le
    --disable-altivec \
%endif

# Set BUILDLEVEL to be embedded to all DLLs built with Libtool.
export LT_BUILDLEVEL="@#%{vendor}:%{version}-%{release}#@##1## `LANG=C date +'%%d %%b %%Y %%H:%%M:%%S'`     `uname -n`::::0::"
make %{?_smp_mflags}

%install
%make_install

%if !0%{?os2_version}
# Rename SDL_config.h to SDL_config-<arch>.h to avoid file conflicts on
# multilib systems and install SDL_config.h wrapper
mv %{buildroot}%{_includedir}/SDL2/SDL_config.h %{buildroot}%{_includedir}/SDL2/SDL_config-%{_arch}.h
install -p -m 644 %{SOURCE1} %{buildroot}%{_includedir}/SDL2/SDL_config.h
%endif

# remove libtool .la file
rm -vf %{buildroot}%{_libdir}/*.la
# remove static .a file
# rm -f %{buildroot}%{_libdir}/*.a

%if !0%{?os2_version}
%ldconfig_scriptlets
%endif

%files
%license COPYING.txt
%doc BUGS.txt CREDITS.txt README-SDL.txt
%{_libdir}/*.dll

%files devel
%doc README.txt TODO.txt WhatsNew.txt
%{_bindir}/*-config
%{_libdir}/*_dll.a
%{_libdir}/pkgconfig/sdl2.pc
%{_libdir}/cmake/SDL2/
%{_includedir}/SDL2
%{_datadir}/aclocal/*

%files static
%license COPYING.txt
%{_libdir}/*.a
%exclude %{_libdir}/*_dll.a

%changelog
* Fri Jun 18 2021 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.0.12-3
- added pull request #1 from josch1710
- added pull request #2 from josch1710

* Mon Sep 28 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.0.12-2
- fix a sigsegv in some situations
- don't enable a capture device for now
- unify debug
- mark our SW renderer as accelerated

* Wed Sep 02 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.0.12-1
- first OS/2 rpm
