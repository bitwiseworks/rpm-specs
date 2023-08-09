# For the generated library symbol suffix
%if 0%{?__isa_bits} == 32
%global libsymbolsuffix %{nil}
%else
%global libsymbolsuffix ()(%{__isa_bits}bit)
%endif

# For declaring rich dependency on libdecor
%global libdecor_majver 0

Name:           SDL2
Version:        2.28.1
Release:        1%{?dist}
Summary:        Cross-platform multimedia library
License:        Zlib AND MIT AND Apache-2.0 AND (Apache-2.0 OR MIT)
URL:            http://www.libsdl.org/
%if !0%{?os2_version}
Source0:        http://www.libsdl.org/release/%{name}-%{version}.tar.gz
Source1:        SDL_config.h
Source2:        SDL_revision.h

Patch0:         multilib.patch
# Prefer Wayland by default
Patch1:         SDL2-2.0.22-prefer-wayland.patch

%else
Vendor:         bww bitwise works GmbH
%scm_source     github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2
%endif

BuildRequires:  git-core
BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  gcc-c++
%if !0%{?os2_version}
BuildRequires:  alsa-lib-devel
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
%endif
%if !0%{?os2_version}
BuildRequires:  libXinerama-devel
BuildRequires:  libXcursor-devel
BuildRequires:  systemd-devel
%endif
BuildRequires:  pkgconfig(libusb-1.0)
%if !0%{?os2_version}
# PulseAudio
BuildRequires:  pkgconfig(libpulse-simple)
# Jack
BuildRequires:  pkgconfig(jack)
# PipeWire
BuildRequires:  pkgconfig(libpipewire-0.3)
# D-Bus
BuildRequires:  pkgconfig(dbus-1)
# IBus
BuildRequires:  pkgconfig(ibus-1.0)
# Wayland
BuildRequires:  pkgconfig(libdecor-%{libdecor_majver})
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
%if 0%{?os2_version}
BuildRequires:  os2tk45-libs os2tk45-headers
%endif

%if !0%{?os2_version}
# Ensure libdecor is pulled in when libwayland-client is (rhbz#1992804)
Requires:       (libdecor-%{libdecor_majver}.so.%{libdecor_majver}%{libsymbolsuffix} if libwayland-client)
%endif

%description
Simple DirectMedia Layer (SDL) is a cross-platform multimedia library designed
to provide fast access to the graphics frame buffer and audio device.

%package devel
Summary:        Files needed to develop Simple DirectMedia Layer applications
Requires:       %{name}%{?_isa} = %{version}-%{release}
%if !0%{?os2_version}
Requires:       mesa-libEGL-devel%{?_isa}
Requires:       mesa-libGLES-devel%{?_isa}
Requires:       libX11-devel%{?_isa}
%endif
# Conflict with versions before libSDLmain moved here
Conflicts:      %{name}-static < 2.0.18-4

%description devel
Simple DirectMedia Layer (SDL) is a cross-platform multimedia library designed
to provide fast access to the graphics frame buffer and audio device. This
package provides the libraries, include files, and other resources needed for
developing SDL applications.

%package static
Summary:        Static libraries for SDL2
# Needed to keep CMake happy
Requires:       %{name}-devel = %{version}-%{release}
# Conflict with versions before libSDLmain moved to -devel
Conflicts:      %{name}-devel < 2.0.18-4

%description static
Static libraries for SDL2.

%if 0%{?os2_version}
%debug_package
%endif

%prep
%if !0%{?os2_version}
%autosetup -S git
sed -i -e 's/\r//g' TODO.txt README.md WhatsNew.txt BUGS.txt LICENSE.txt CREDITS.txt README-SDL.txt
%else
%scm_setup
%endif

%build
# Deal with new CMake policy around whitespace in LDFLAGS...
%if !0%{?os2_version}
export LDFLAGS="%{shrink:%{build_ldflags}}"
%else
export VENDOR="%{vendor}"
export LDFLAGS=" -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx -lmmpm2"
export CFLAGS="-idirafter /@unixroot/usr/include/os2tk45"
mkdir build
%endif

%cmake \
    -DSDL_DLOPEN=ON \
%if !0%{?os2_version}
    -DSDL_VIDEO_KMSDRM=ON \
%endif
    -DSDL_ARTS=OFF \
    -DSDL_ESD=OFF \
    -DSDL_NAS=OFF \
%if !0%{?os2_version}
    -DSDL_PULSEAUDIO_SHARED=ON \
    -DSDL_JACK_SHARED=ON \
    -DSDL_PIPEWIRE_SHARED=ON \
    -DSDL_ALSA=ON \
    -DSDL_VIDEO_WAYLAND=ON \
%endif
    -DSDL_LIBDECOR_SHARED=ON \
%if !0%{?os2_version}
    -DSDL_VIDEO_VULKAN=ON \
%endif
    -DSDL_SSE3=OFF \
    -DSDL_RPATH=OFF \
    -DSDL_STATIC=ON \
    -DSDL_STATIC_PIC=ON \
%ifarch ppc64le
    -DSDL_ALTIVEC=OFF \
%endif
%if 0%{?os2_version}
    -DSDL_LIBC=ON \
    -S . -B build \
%endif

%if !0%{?os2_version}
%cmake_build
%else
make VERBOSE=1 -C build
%endif

%install
%if !0%{?os2_version}
%cmake_install
%else
%make_install -C build
%endif

%if !0%{?os2_version}
# Rename SDL_config.h to SDL_config-<arch>.h to avoid file conflicts on
# multilib systems and install SDL_config.h wrapper
mv %{buildroot}%{_includedir}/SDL2/SDL_config.h %{buildroot}%{_includedir}/SDL2/SDL_config-%{_arch}.h
install -p -m 644 %{SOURCE1} %{buildroot}%{_includedir}/SDL2/SDL_config.h

# Rename SDL_revision.h to SDL_revision-<arch>.h to avoid file conflicts on
# multilib systems and install SDL_revision.h wrapper
# TODO: Figure out how in the hell the SDL_REVISION changes between architectures on the same SRPM.
mv %{buildroot}%{_includedir}/SDL2/SDL_revision.h %{buildroot}%{_includedir}/SDL2/SDL_revision-%{_arch}.h
install -p -m 644 %{SOURCE2} %{buildroot}%{_includedir}/SDL2/SDL_revision.h
%else
rm -rf ${RPM_BUILD_ROOT}/%{_licensedir}/SDL2
%endif

%files
%license LICENSE.txt
%doc BUGS.txt CREDITS.txt README-SDL.txt
%if !0%{?os2_version}
%{_libdir}/libSDL2-2.0.so.0*
%else
%{_libdir}/SDL2*.dll
%endif

%files devel
%doc README.md TODO.txt WhatsNew.txt
%{_bindir}/*-config
%if !0%{?os2_version}
%{_libdir}/lib*.so
%{_libdir}/libSDL2main.a
%else
%{_libdir}/*_dll.a
%{_libdir}/SDL2main.a
%endif
%{_libdir}/pkgconfig/sdl2.pc
%dir %{_libdir}/cmake/SDL2
%{_libdir}/cmake/SDL2/SDL2Config*.cmake
%{_libdir}/cmake/SDL2/sdlfind.cmake
%{_libdir}/cmake/SDL2/SDL2Targets*.cmake
%{_libdir}/cmake/SDL2/SDL2mainTargets*.cmake
%{_includedir}/SDL2
%{_datadir}/aclocal/*
%if !0%{?os2_version}
%{_libdir}/libSDL2_test.a
%else
%{_libdir}/SDL2_test.a
%endif
%{_libdir}/cmake/SDL2/SDL2testTargets*.cmake

%files static
%license LICENSE.txt
%if !0%{?os2_version}
%{_libdir}/libSDL2.a
%else
%{_libdir}/SDL2.a
%endif
%{_libdir}/cmake/SDL2/SDL2staticTargets*.cmake

%changelog
* Wed Aug 09 2023 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.28.1-1
- updated to vendor version 2.28.1
- resync with latest fedora spec

* Wed Jul 26 2023 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.0.18-3
- added/changed/fixed audio suppoert (mostly done by Lars and Josch)

* Sun Jun 18 2023 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.0.18-2
- fixed some issues (mostly done by Josch)

* Fri Jan 21 2022 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.0.18-1
- updated to version 2.0.18
- change buildsystem to cmake

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
