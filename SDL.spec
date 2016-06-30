%define svn_url http://svn.netlabs.org/repos/ports/libsdl/trunk
%define svn_rev 1636

Name:    SDL
Version: 1.2.15
Release: 5%{?dist}
Summary:    A cross-platform multimedia library
Group:      System Environment/Libraries
URL:        http://www.libsdl.org/
# The license of the file src/video/fbcon/riva_mmio.h is bad, but the contents
# of the file has been relicensed to MIT in 2008 by Nvidia for the 
# xf86_video-nv driver, therefore it can be considered ok.
License:    LGPLv2+
# Source: http://www.libsdl.org/release/%%{name}-%%{version}.tar.gz
# To create the repackaged archive use ./repackage.sh %%{version}
Source0: %{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip
#Patch0:  SDL-os2-2.patch
# Rejected by upstream as sdl1155, rh480065
#Patch0:     SDL-1.2.10-GrabNotViewable.patch
# Proposed to upstream as sdl1680, rh891973
#Patch1:     SDL-1.2.15-x11-Bypass-SetGammaRamp-when-changing-gamma.patch
# Proposded to upstream as sdl1769
#Patch2:     SDL-1.2.15-const_XData32.patch
# sdl-config(1) manual from Debian, rh948864
#Patch3:     SDL-1.2.15-add_sdl_config_man.patch
# Upstream fix for sdl1486, rh990677
#Patch4:     SDL-1.2.15-ignore_insane_joystick_axis.patch
# Do not use backing store by default, sdl2383, rh1073057, rejected by
# upstream
#Patch5:     SDL-1.2.15-no-default-backing-store.patch
# Fix processing keyboard events if SDL_EnableUNICODE() is enabled, sdl2325,
# rh1126136, in upstream after 1.2.15
#Patch6:     SDL-1.2.15-SDL_EnableUNICODE_drops_keyboard_events.patch

#BuildRequires:  alsa-lib-devel
#%if %{with arts}
#BuildRequires:  arts-devel
#%endif
#BuildRequires:  audiofile-devel
BuildRequires:  coreutils
#%if %{with esound}
#BuildRequires:  esound-devel
#%endif
BuildRequires:  gcc
BuildRequires:  libc-devel
#BuildRequires:  mesa-libGL-devel
#BuildRequires:  mesa-libGLU-devel
#BuildRequires:  libXext-devel
#BuildRequires:  libX11-devel
#BuildRequires:  libXrandr-devel
#BuildRequires:  libXrender-devel
BuildRequires:  make
#%if %{with nas}
#BuildRequires:  nas-devel
#%endif
#%ifarch %{ix86}
BuildRequires:  nasm
#%endif
#BuildRequires:  pulseaudio-libs-devel
#%if %{with esound}
#BuildRequires:  sed
#%endif
# Autotools
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  libtool

%description
Simple DirectMedia Layer (SDL) is a cross-platform multimedia library designed
to provide fast access to the graphics frame buffer and audio device.

%package devel
Summary:    Files needed to develop Simple DirectMedia Layer applications
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
#Requires:   alsa-lib-devel
#Requires:   mesa-libGL-devel
#Requires:   mesa-libGLU-devel
#Requires:   libX11-devel
#Requires:   libXext-devel
#Requires:   libXrandr-devel
#Requires:   libXrender-devel

%description devel
Simple DirectMedia Layer (SDL) is a cross-platform multimedia library designed
to provide fast access to the graphics frame buffer and audio device. This
package provides the libraries, include files, and other resources needed for
developing SDL applications.

#%package static
#Summary:    Files needed to develop static Simple DirectMedia Layer applications
#Group:      Development/Libraries
#Requires:   SDL-devel = %{version}-%{release}

#%description static
#Simple DirectMedia Layer (SDL) is a cross-platform multimedia library designed
#to provide fast access to the graphics frame buffer and audio device. This
#package provides the static libraries needed for developing static SDL
#applications.

%debug_package

%prep
%if %{?svn_rev:%(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')}%{!?svn_rev):0}
%setup -q
%else
%setup -q -n "%{name}-%{version}" -Tc
svn export %{?svn_rev:-r %{svn_rev}} %{svn_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip" "%{name}-%{version}")
%endif

#%patch0 -p1

libtoolize -fci
./autogen.sh

%build
export  CFLAGS="-g -DBUILD_SDL -DUSE_ASM_MIXER_VC -DICONV_INBUF_NONCONST -DUSE_DOSSETPRIORITY \
	-DSDL_AUDIO_DRIVER_DARTALT -DUSE_OS2_TOOLKIT_HEADERS -idirafter /@unixroot/usr/include/os2tk45" \
	CXXFLAGS="-g -DBUILD_SDL -DUSE_ASM_MIXER_VC -DICONV_INBUF_NONCONST -DUSE_DOSSETPRIORITY \
	-DSDL_AUDIO_DRIVER_DARTALT -DUSE_OS2_TOOLKIT_HEADERS -idirafter /@unixroot/usr/include/os2tk45" \
	LDFLAGS="-Zomf -Zhigh-mem -g -lmmpm2"

%configure \
       --enable-audio \
	--enable-video \
	--enable-events \
	--enable-joystick \
	--enable-cdrom \
	--enable-threads \
	--enable-timers \
	--enable-file \
	--enable-loadso \
	--enable-cpuinfo \
	--enable-assembly \
	--disable-static \
	--enable-shared

%{__make} %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

# create OMF libs
emximp -o %{buildroot}%{_libdir}/SDL_dll.lib %{buildroot}%{_libdir}/SDL120.dll
emximp -o %{buildroot}%{_libdir}/SDL120_dll.lib %{buildroot}%{_libdir}/SDL120.dll
emximp -o %{buildroot}%{_libdir}/SDL_dll.a %{buildroot}%{_libdir}/SDL120.dll
emximp -o %{buildroot}%{_libdir}/SDL120_dll.a %{buildroot}%{_libdir}/SDL120.dll
rm -rf %{buildroot}%{_libdir}/SDLmain.a

# create forwarder
gcc -Zomf -c %{_specdir}/SDL/wrap.c -o %{buildroot}%{_libdir}/wrap.o
gcc -Zomf -Zdll -g -o %{buildroot}%{_libdir}/SDL12.dll %{_specdir}/SDL/SDL12.def \
	%{buildroot}%{_libdir}/wrap.o -L%{buildroot}%{_libdir} -lSDL
rm -rf %{buildroot}%{_libdir}/wrap.o

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc README-SDL.txt COPYING CREDITS BUGS README.OS2 README-Digi.OS2 sdl.ini
%{_libdir}/SDL12*.dll

%files devel
%doc README README-SDL.txt COPYING CREDITS BUGS WhatsNew docs.html
%doc docs/index.html docs/html
%{_bindir}/*-config
%{_libdir}/SDL*.a
%{_libdir}/SDL*.lib
%exclude %{_libdir}/lib*.la
%dir %{_includedir}/SDL
%{_includedir}/SDL/*.h
%{_libdir}/pkgconfig/sdl.pc
%{_datadir}/aclocal/*
%{_mandir}/man3/*

#%files static
#%{_libdir}/lib*.a

%changelog
* Thu Jun 30 2016 Valery V.Sedletski <_valerius@mail.ru> - 1.2.15-5
- Remove uneeded -I./src/thread/os2 from include path.

* Mon Apr 18 2016 Valery V.Sedletski <_valerius@mail.ru> - 1.2.15-4
- Moved wrap.c and SDL12.def to SDL subdir

* Thu Apr 14 2016 Valery V.Sedletski <_valerius@mail.ru> - 1.2.15-3
- Made the .spec in accordance with Fedora version, renamed to SDL in caps

* Tue Mar 15 2016 Valery V.Sedletski <_valerius@mail.ru> - 1.2.15-2
- Adding the debug info for forwarder/wrapper

* Sat Mar 12 2016 Valery V.Sedletski <_valerius@mail.ru> - 1.2.15-1
- Initial OS/2 packaging
