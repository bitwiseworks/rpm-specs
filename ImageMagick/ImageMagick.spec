%if !0%{os2_version}
%bcond_without tests
%else
%bcond_with tests
%endif

%if !0%{os2_version}
%bcond_without libheif
%else
%bcond_with libheif
%endif

%if 0%{?flatpak} || 0%{os2_version}
%bcond_with perl
%else
%bcond_without perl
%endif

# Disable automatic .la file removal
%global __brp_remove_la_files %nil

Name:           ImageMagick
Epoch:          1
Version:        7.1.2.15
Release:        1%{?dist}
Summary:        An X application for displaying and manipulating images

%if !0%{os2_version}
%global VER %(foo=%{version}; echo ${foo:0:5})
%global Patchlevel %(foo=%{version}; echo ${foo:6})
%else
%global VER %(foo=%{version}; echo ${foo} | cut -c -5)
%global Patchlevel %(foo=%{version}; echo ${foo} | cut -c 7-)
%endif
%global libsover 10
%global subsover VERS_10.0
%global libcxxsover 5
License:        ImageMagick
URL:            https://imagemagick.org/
%if !0%{os2_version}
Source0:        https://imagemagick.org/archive/releases/%{name}-%{VER}-%{Patchlevel}.tar.xz
Source1:        https://imagemagick.org/archive/releases/%{name}-%{VER}-%{Patchlevel}.tar.xz.asc
Source2:        ImageMagick.keyring
%else
Vendor:    bww bitwise works GmbH
%scm_source git e:/trees/imagemagick/git master-os2
#scm_source github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2
%endif

BuildRequires:  pkgconfig(bzip2)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libtiff-4)
BuildRequires:  giflib-devel
BuildRequires:  pkgconfig(zlib)
%if %{with perl}
BuildRequires:  perl-devel >= 5.8.1
%if !0%{os2_version}
BuildRequires:  perl-generators
%endif
%endif
%if !0%{os2_version}
BuildRequires:  libgs-devel
%endif
# Used in configure to check device availability
BuildRequires:  ghostscript
BuildRequires:  pkgconfig(ddjvuapi)
%if !0%{os2_version}
BuildRequires:  pkgconfig(libwmf)
BuildRequires:  pkgconfig(jasper)
%endif
BuildRequires:  libtool-ltdl-devel
%if !0%{os2_version}
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xt)
%endif
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(libxml-2.0)
%if !0%{os2_version}
BuildRequires:  pkgconfig(librsvg-2.0)
%if 0%{?rhel} && 0%{?rhel} < 9
BuildRequires:  pkgconfig(IlmBase), pkgconfig(OpenEXR) < 2.5.6
%else
BuildRequires:  pkgconfig(OpenEXR)
%endif
BuildRequires:  pkgconfig(fftw3)
%endif
BuildRequires:  pkgconfig(libwebp)
BuildRequires:  jbigkit-devel
%if !0%{os2_version}
BuildRequires:  pkgconfig(libjxl)
%endif
BuildRequires:  pkgconfig(libopenjp2) >= 2.1.0
%if !0%{os2_version}
BuildRequires:  pkgconfig(libcgraph) >= 2.9.0
BuildRequires:  pkgconfig(raqm)
%if 0%{?fedora} || 0%{?rhel} > 8
BuildRequires:  pkgconfig(lqr-1)
%endif
BuildRequires:  pkgconfig(libraw) >= 0.14.8
%endif
# Ultra HDR support available of Fedora 43 and onward
%if 0%{?fedora} >= 43
BuildRequires:  pkgconfig(libuhdr) >= 1.3.0
%endif
BuildRequires:  pkgconfig(libzstd)
%if !0%{os2_version}
BuildRequires:  pkgconfig(libzip) >= 1.0.0
BuildRequires:  pkgconfig(pango) >= 1.28.1
BuildRequires:  pkgconfig(pangocairo) >= 1.28.1
%endif
BuildRequires:  urw-base35-fonts-devel
BuildRequires:  autoconf automake gcc gcc-c++
BuildRequires:  make
%if !0%{os2_version}
BuildRequires:  gnupg2
%endif
# for doc
BuildRequires:  doxygen

%if !0%{os2_version}
Requires:       %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
%else
Requires:       %{name}-libs = %{epoch}:%{version}-%{release}
%endif
# allow smooth upgrade for 3rd party repository
# providing latest version/soname as ImageMagick7
Obsoletes:      %{name}7            < %{epoch}:%{version}-%{release}
Provides:       %{name}7            = %{epoch}:%{version}-%{release}

%description
ImageMagick is an image display and manipulation tool for the X
Window System. ImageMagick can read and write JPEG, TIFF, PNM, GIF,
and Photo CD image formats. It can resize, rotate, sharpen, color
reduce, or add special effects to an image, and when finished you can
either save the completed work in the original format or a different
one. ImageMagick also includes command line programs for creating
animated or transparent .gifs, creating composite images, creating
thumbnail images, and more.

ImageMagick is one of your choices if you need a program to manipulate
and display images. If you want to develop your own applications
which use ImageMagick code or APIs, you need to install
ImageMagick-devel as well.


%package devel
Summary:        Library links and header files for ImageMagick app development
%if !0%{os2_version}
Requires:       %{name}%{?_isa} = %{epoch}:%{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
%else
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       %{name}-libs = %{epoch}:%{version}-%{release}
%endif
Obsoletes:      %{name}7-devel       < %{epoch}:%{version}-%{release}
Provides:       %{name}7-devel       = %{epoch}:%{version}-%{release}

%description devel
ImageMagick-devel contains the library links and header files you'll
need to develop ImageMagick applications. ImageMagick is an image
manipulation program.

If you want to create applications that will use ImageMagick code or
APIs, you need to install ImageMagick-devel as well as ImageMagick.
You do not need to install it if you just want to use ImageMagick,
however.


%package libs
Summary: ImageMagick libraries to link with
Obsoletes: %{name}7-libs < %{epoch}:%{version}-%{release}
Provides:  %{name}7-libs = %{epoch}:%{version}-%{release}
# These may be used for some functions
Recommends: urw-base35-fonts
# default font is OpenSans-Regular
Recommends: open-sans-fonts

%description libs
This packages contains a shared libraries to use within other applications.


%if !0%{os2_version}
%package djvu
Summary: DjVu plugin for ImageMagick
Requires: %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
Obsoletes: %{name}7-djvu       < %{epoch}:%{version}-%{release}
Provides:  %{name}7-djvu       = %{epoch}:%{version}-%{release}

%description djvu
This packages contains a plugin for ImageMagick which makes it possible to
save and load DjvU files from ImageMagick and libMagickCore using applications.
%endif


%if %{with libheif}
%package heic
Summary: HEIC plugin for ImageMagick
BuildRequires:  pkgconfig(libheif) >= 1.4.0
Requires:       %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}

%description heic
This packages contains a plugin for ImageMagick which makes it possible to
save and load HEIC files from ImageMagick and libMagickCore using applications.
%endif


%package doc
Summary: ImageMagick html documentation
Obsoletes: %{name}7-doc < %{epoch}:%{version}-%{release}
Provides:  %{name}7-doc = %{epoch}:%{version}-%{release}

%description doc
ImageMagick documentation, this package contains usage (for the
commandline tools) and API (for the libraries) documentation in html format.
Note this documentation can also be found on the ImageMagick website:
http://www.imagemagick.org/


%if %{with perl}
%package perl
Summary:        ImageMagick perl bindings
%if !0%{os2_version}
Requires:       %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
%else
Requires:       %{name}-libs = %{epoch}:%{version}-%{release}
%endif
Obsoletes:      %{name}7-perl        < %{epoch}:%{version}-%{release}
Provides:       %{name}7-perl        = %{epoch}:%{version}-%{release}

%description perl
Perl bindings to ImageMagick.

Install ImageMagick-perl if you want to use any perl scripts that use
ImageMagick.
%endif


%package c++
Summary:        ImageMagick Magick++ library (C++ bindings)
%if !0%{os2_version}
Requires:       %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
%else
Requires:       %{name}-libs = %{epoch}:%{version}-%{release}
%endif
Obsoletes:      %{name}7-c++         < %{epoch}:%{version}-%{release}
Provides:       %{name}7-c++         = %{epoch}:%{version}-%{release}

%description c++
This package contains the Magick++ library, a C++ binding to the ImageMagick
graphics manipulation library.

Install ImageMagick-c++ if you want to use any applications that use Magick++.


%package c++-devel
Summary:        C++ bindings for the ImageMagick library
%if !0%{os2_version}
Requires:       %{name}-c++%{?_isa} = %{epoch}:%{version}-%{release}
Requires:       %{name}-devel%{?_isa} = %{epoch}:%{version}-%{release}
%else
Requires:       %{name}-c++ = %{epoch}:%{version}-%{release}
Requires:       %{name}-devel = %{epoch}:%{version}-%{release}
%endif
Obsoletes:      %{name}7-c++-devel    < %{epoch}:%{version}-%{release}
Provides:       %{name}7-c++-devel    = %{epoch}:%{version}-%{release}

%description c++-devel
ImageMagick-devel contains the static libraries and header files you'll
need to develop ImageMagick applications using the Magick++ C++ bindings.
ImageMagick is an image manipulation program.

If you want to create applications that will use Magick++ code
or APIs, you'll need to install ImageMagick-c++-devel, ImageMagick-devel and
ImageMagick.
You don't need to install it if you just want to use ImageMagick, or if you
want to develop/compile applications using the ImageMagick C interface,
however.


%if 0%{os2_version}
%debug_package
%endif


%prep
%if !0%{os2_version}
%{gpgverify} --keyring=%{SOURCE2} --signature=%{SOURCE1} --data=%{SOURCE0}
%autosetup -p1 -n %{name}-%{VER}-%{Patchlevel}
%else
%scm_setup
%endif


%build
%if !0%{os2_version}
autoconf -f -i -v
# Reduce thread contention, upstream sets this flag for Linux hosts
export CFLAGS="%{optflags} -DIMPNG_SETJMP_IS_THREAD_SAFE"
%else
autoreconf -fvi
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"
export VENDOR="%{vendor}"
%endif
%configure \
        --enable-shared \
        --disable-static \
%if !0%{os2_version}
        --with-modules \
%endif
%if %{with perl}
        --with-perl \
        --with-perl-options="INSTALLDIRS=vendor %{?perl_prefix} CC='%__cc -L$PWD/magick/.libs' LDDLFLAGS='-shared -L$PWD/magick/.libs'" \
%endif
%if !0%{os2_version}
        --with-x \
%endif
        --with-threads \
        --with-magick_plus_plus \
        --with-gslib \
        --with-pango \
        --with-fftw \
        --with-wmf \
        --with-webp \
        --with-openexr \
        --with-rsvg \
        --with-xml \
        --with-urw-base35-font-dir="%{urw_base35_fontpath}" \
        --without-dps \
        --enable-openmp \
        --without-gcc-arch \
        --with-jbig \
        --with-jxl \
        --with-openjp2 \
        --with-raw \
%if 0%{?fedora} || 0%{?rhel} > 8
        --with-lqr \
%if 0%{?fedora} >= 43
        --with-uhdr \
%endif
%endif
        --with-gvc \
        --with-raqm \
%if %{with libheif}
           --with-heic \
%endif

# Do *NOT* use %%{?_smp_mflags}, this causes PerlMagick to be silently misbuild
make
# Generate API docs
make html-local


%install
%make_install

# Compatibility symlinks for headers for IM6->IM7 transition
ln -sr %{buildroot}%{_includedir}/%{name}-7/MagickCore %{buildroot}%{_includedir}/%{name}-7/magick
ln -sr %{buildroot}%{_includedir}/%{name}-7/MagickWand %{buildroot}%{_includedir}/%{name}-7/wand

# Do NOT remove .la files for codecs
# https://bugzilla.opensuse.org/show_bug.cgi?id=579798
# Delete *ONLY* _libdir/*.la files! .la files used internally to handle plugins - BUG#185237!!!
rm %{buildroot}%{_libdir}/*.la

%if 0%{os2_version}
rm %{buildroot}%{_libdir}/MagickCore-7.Q16HDRI%{libsover}_dll.a
rm %{buildroot}%{_libdir}/MagickWand-7.Q16HDRI%{libsover}_dll.a
rm %{buildroot}%{_libdir}/Magick++-7.Q16HDRI%{libcxxsover}_dll.a
%endif

%if %{with perl}
# fix weird perl module permissions
chmod 755 %{buildroot}%{perl_vendorarch}/auto/Image/Magick/Q16HDRI/Q16HDRI.so

# perlmagick: fix perl path of demo files
%{__perl} -MExtUtils::MakeMaker -e 'MY->fixin(@ARGV)' PerlMagick/demo/*.pl

# perlmagick: cleanup various perl tempfiles from the build which get installed
find %{buildroot} -name "*.bs" |xargs rm -f
find %{buildroot} -name ".packlist" |xargs rm -f
find %{buildroot} -name "perllocal.pod" |xargs rm -f

# perlmagick: build files list
find %{buildroot}/%{_libdir}/perl* -type f -print \
        | sed "s@^%{buildroot}@@g" > perl-pkg-files
find %{buildroot}%{perl_vendorarch} -type d -print \
        | sed "s@^%{buildroot}@%dir @g" \
        | grep -v '^%dir %{perl_vendorarch}$' \
        | grep -v '/auto$' >> perl-pkg-files
if [ -z perl-pkg-files ] ; then
        echo "ERROR: EMPTY FILE LIST"
        exit -1
fi
%endif

%if !0%{os2_version}
# fix multilib issues: Rename the provided file with platform-bits in name.
# Create platform independent file inplace of the provided one and conditionally
# include the required one.
# $1 - filename.h to process.
function multilibFileVersions(){
mv $1 ${1%%.h}-%{__isa_bits}.h

local basename=$(basename $1)

cat >$1 <<EOF
#include <bits/wordsize.h>

#if __WORDSIZE == 32
# include "${basename%%.h}-32.h"
#elif __WORDSIZE == 64
# include "${basename%%.h}-64.h"
#else
# error "unexpected value for __WORDSIZE macro"
#endif
EOF
}

multilibFileVersions %{buildroot}%{_includedir}/%{name}-7/MagickCore/magick-config.h
multilibFileVersions %{buildroot}%{_includedir}/%{name}-7/MagickCore/magick-baseconfig.h
multilibFileVersions %{buildroot}%{_includedir}/%{name}-7/MagickCore/version.h
%endif

find %{buildroot} -type f -name "*%{subsover}*" >/dev/null 2>&1
if [ $? -ne 0 ]; then
    echo Error: No files containing %{subsover} found
    exit 1
fi

%check
%if %{with tests}
export LD_LIBRARY_PATH=%{buildroot}/%{_libdir}
%make_build check
%endif
rm PerlMagick/demo/Generic.ttf


%files
%doc NOTICE AUTHORS.txt
%license LICENSE
%{_bindir}/[a-z]*
%{_mandir}/man[145]/[a-z]*
%{_mandir}/man1/%{name}.*

%files libs
%doc NOTICE AUTHORS.txt
%license LICENSE
%if !0%{os2_version}
%{_libdir}/libMagickCore-7.Q16HDRI.so.%{libsover}{,.*}
%{_libdir}/libMagickWand-7.Q16HDRI.so.%{libsover}{,.*}
%else
%{_libdir}/Magicc%{libsover}.dll
%{_libdir}/Magicw%{libsover}.dll
%endif
%{_libdir}/%{name}-%{VER}
%{_datadir}/%{name}-7
%if !0%{os2_version}
%exclude %{_libdir}/%{name}-%{VER}/modules-Q16HDRI/coders/djvu.*
%endif
%if %{with libheif}
%exclude %{_libdir}/%{name}-%{VER}/modules-Q16HDRI/coders/heic.*
%endif
%dir %{_sysconfdir}/%{name}-7
%config(noreplace) %{_sysconfdir}/%{name}-7/*.xml

%files devel
%{_bindir}/MagickCore-config
%{_bindir}/MagickWand-config
%if !0%{os2_version}
%{_libdir}/libMagickCore-7.Q16HDRI.so
%{_libdir}/libMagickWand-7.Q16HDRI.so
%else
%{_libdir}/MagickCore-7.Q16HDRI_dll.a
%{_libdir}/MagickWand-7.Q16HDRI_dll.a
%endif
%{_libdir}/pkgconfig/MagickCore.pc
%{_libdir}/pkgconfig/MagickCore-7.Q16HDRI.pc
%{_libdir}/pkgconfig/ImageMagick.pc
%{_libdir}/pkgconfig/ImageMagick-7.Q16HDRI.pc
%{_libdir}/pkgconfig/MagickWand.pc
%{_libdir}/pkgconfig/MagickWand-7.Q16HDRI.pc
%dir %{_includedir}/%{name}-7
%{_includedir}/%{name}-7/MagickCore/
%{_includedir}/%{name}-7/MagickWand/
%{_includedir}/%{name}-7/magick
%{_includedir}/%{name}-7/wand
%{_mandir}/man1/MagickCore-config.*
%{_mandir}/man1/MagickWand-config.*

%if !0%{os2_version}
%files djvu
%{_libdir}/%{name}-%{VER}/modules-Q16HDRI/coders/djvu.*
%endif

%if %{with libheif}
%files heic
%{_libdir}/%{name}-%{VER}/modules-Q16HDRI/coders/heic.*
%endif

%files doc
%doc %{_datadir}/doc/%{name}-7

%files c++
%doc Magick++/AUTHORS
%license Magick++/LICENSE
%if !0%{os2_version}
%{_libdir}/libMagick++-7.Q16HDRI.so.%{libcxxsover}{,.*}
%else
%{_libdir}/Magick+%{libcxxsover}.dll
%endif

%files c++-devel
%doc Magick++/demo
%{_bindir}/Magick++-config
%{_includedir}/%{name}-7/Magick++/
%{_includedir}/%{name}-7/Magick++.h
%if !0%{os2_version}
%{_libdir}/libMagick++-7.Q16HDRI.so
%else
%{_libdir}/Magick++-7.Q16HDRI_dll.a
%endif
%{_libdir}/pkgconfig/Magick++.pc
%{_libdir}/pkgconfig/Magick++-7.Q16HDRI.pc
%{_mandir}/man1/Magick++-config.*

%if %{with perl}
%files perl -f perl-pkg-files
%{_mandir}/man3/*
%doc PerlMagick/demo/ PerlMagick/Changelog PerlMagick/README.txt
%endif

%changelog
* Fri Mar 06 2026 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1:7.1.2.15-1
- first OS/2 rpm

