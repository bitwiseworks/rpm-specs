Name:           SDL2_image
Version:        2.0.5
Release:        5%{?dist}
Summary:        Image loading library for SDL

# IMG_png.c is LGPLv2+ and zlib, rest is just zlib
# nanosvg is zlib
# miniz is Public Domain
License:        LGPLv2+ and zlib
URL:            http://www.libsdl.org/projects/SDL_image/
%if !0%{?os2_version}
Source0:        http://www.libsdl.org/projects/SDL_image/release/%{name}-%{version}.tar.gz
%else
Vendor:         bww bitwise works GmbH
%scm_source     github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2
%endif

BuildRequires:  gcc
BuildRequires:  SDL2-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libpng-devel
BuildRequires:  libtiff-devel
BuildRequires:  libwebp-devel
%if !0%{?os2_version}
BuildRequires:  chrpath
%endif
Provides:       bundled(miniz) = 1.15
# Some custom version of it
Provides:       bundled(nanosvg)

%description
Simple DirectMedia Layer (SDL) is a cross-platform multimedia library
designed to provide fast access to the graphics frame buffer and audio
device.  This package contains a simple library for loading images of
various formats (BMP, PPM, PCX, GIF, JPEG, PNG) as SDL surfaces.

%package devel
Summary:        Development files for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%debug_package

%prep
%if !0%{?os2_version}
%autosetup -p1
rm -rf external/
%else
%scm_setup
autoreconf -fvi -I acinclude
%endif
sed -i -e 's/\r//g' README.txt CHANGES.txt COPYING.txt

%build
export LDFLAGS=" -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"

%configure --disable-dependency-tracking \
           --disable-jpg-shared \
           --disable-png-shared \
           --disable-tif-shared \
           --disable-webp-shared \
           --disable-static
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool

# Set BUILDLEVEL to be embedded to all DLLs built with Libtool.
export LT_BUILDLEVEL="@#%{vendor}:%{version}-%{release}#@##1## `LANG=C date +'%%d %%b %%Y %%H:%%M:%%S'`     `uname -n`::::0::"

make %{?_smp_mflags}

%install
%make_install
mkdir -p %{buildroot}%{_bindir}
./libtool --mode=install /@unixroot/usr/bin/install showimage.exe %{buildroot}%{_bindir}/showimage2.exe
%if !0%{?os2_version}
chrpath -d %{buildroot}%{_bindir}/showimage2
%endif

rm -f %{buildroot}%{_libdir}/*.la

%if !0%{?os2_version}
%ldconfig_scriptlets
%endif

%files
%license COPYING.txt
%doc CHANGES.txt
%{_bindir}/showimage2.exe
%{_libdir}/*.dll

%files devel
%doc README.txt
%{_libdir}/*_dll.a
%{_includedir}/SDL2/SDL_image.h
%{_libdir}/pkgconfig/SDL2_image.pc

%changelog
* Thu Sep 03 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.0.5-5
- first OS/2 rpm
