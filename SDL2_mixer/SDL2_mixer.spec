Name:           SDL2_mixer
Version:        2.0.4
Release:        3%{?dist}
Summary:        Simple DirectMedia Layer - Sample Mixer Library

License:        zlib
URL:            https://www.libsdl.org/projects/SDL_mixer/
%if !0%{?os2_version}
Source0:        https://www.libsdl.org/projects/SDL_mixer/release/%{name}-%{version}.tar.gz
%else
Vendor:         bww bitwise works GmbH
%scm_source github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2-1
%endif

BuildRequires:  SDL2-devel
BuildRequires:  libvorbis-devel
BuildRequires:  flac-devel
BuildRequires:  fluidsynth-devel
BuildRequires:  opusfile-devel

%if !0%{?os2_version}
BuildRequires:  libmikmod-devel
BuildRequires:  mpg123-devel
BuildRequires:  chrpath
BuildRequires:  pkgconfig(libmodplug) >= 0.8.8
%endif

%description
SDL_mixer is a sample multi-channel audio mixer library.
It supports any number of simultaneously playing channels of 16 bit stereo
audio, plus a single channel of music, mixed by the popular FLAC,
MikMod MOD, Timidity MIDI, Ogg Vorbis, and SMPEG MP3 libraries. 

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%if 0%{?os2_version}
%debug_package
%endif

%prep
%if !0%{?os2_version}
%autosetup -p1
%else
%scm_setup
autoreconf -fiv -I acinclude
%endif

sed -i -e 's/\r//g' README.txt CHANGES.txt COPYING.txt
rm -vrf external/

%build
%if 0%{?os2_version}
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
export INCLUDE=''
# Set BUILDLEVEL to be embedded to all DLLs built with Libtool.
export LT_BUILDLEVEL="@#%{vendor}:%{version}-%{release}#@##1## `LANG=C date +'%%d %%b %%Y %%H:%%M:%%S'`     `uname -n`::::0::"
%endif

%configure --disable-dependency-tracking \
           --disable-static
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool

%if !0%{?os2_version}
%make_build
%else
make %{?_smp_mflags}
%endif

%install
%make_install install-bin

%if !0%{?os2_version}
for i in playmus playwave
do
  chrpath -d %{buildroot}%{_bindir}/${i}
  mv %{buildroot}%{_bindir}/${i} %{buildroot}%{_bindir}/${i}2
done
%endif

find %{buildroot} -name '*.la' -print -delete

%if !0%{?os2_version}
%ldconfig_scriptlets
%endif

%files
%license COPYING.txt
%doc CHANGES.txt
%if !0%{?os2_version}
%{_bindir}/playmus
%{_bindir}/playwave
%else
%{_bindir}/playmus.exe
%{_bindir}/playwave.exe
%endif
%if !0%{?os2_version}
%{_libdir}/libSDL2_mixer-2.0.so.*
%else
%{_libdir}/*.dll
%endif

%files devel
%doc README.txt
%if !0%{?os2_version}
%{_libdir}/libSDL2_mixer.so
%else
%{_libdir}/*.a
%endif
%{_libdir}/pkgconfig/SDL2_mixer.pc
%{_includedir}/SDL2/SDL_mixer.h

%changelog
* Fri Jun 11 2021 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.0.4-3
- rebuild with latest changes from josch1710 (pull request #1)
- adapt spec a bit

* Tue Oct 20 2020 Elbert Pol <elbert.pol@gmail.com> - 2.0.4-2
- Update cause i had a wrong macros.dist

* Tue Sep 08 2020 Elbert Pol <elbert.pol@gmail.com> - 2.0.4-1
- First rpm for OS2

