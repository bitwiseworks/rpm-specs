%if !0%{?os2_version}
%global  with_liq   1
%global  with_raqm  1
%else
%global  with_liq   0
%global  with_raqm  0
%endif


Summary:       A graphics library for quick creation of PNG or JPEG images
Name:          gd
Version:       2.3.0
Release:       1%{?prever}%{?short}%{?dist}
License:       MIT
URL:           http://libgd.github.io/
%if !0%{?os2_version}
%if 0%{?commit:1}
# git clone https://github.com/libgd/libgd.git; cd gd-libgd
# git archive  --format=tgz --output=libgd-%{version}-%{commit}.tgz --prefix=libgd-%{version}/  master
Source0:       libgd-%{version}-%{commit}.tgz
%else
Source0:       https://github.com/libgd/libgd/releases/download/gd-%{version}/libgd-%{version}.tar.xz
%endif
# Missing, temporary workaround, fixed upstream for next version
Source1:       https://raw.githubusercontent.com/libgd/libgd/gd-%{version}/config/getlib.sh

Patch0:        gd-bug615.patch
%else
Vendor: bww bitwise works GmbH
%scm_source github https://github.com/bitwiseworks/%{name}-os2 gd-%{version}-os2
%endif
BuildRequires: freetype-devel
BuildRequires: fontconfig-devel
BuildRequires: gettext-devel
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: libtiff-devel
BuildRequires: libwebp-devel
%if %{with_liq}
BuildRequires: libimagequant-devel
%endif
%if %{with_raqm}
BuildRequires: libraqm-devel
%endif
%if !0%{?os2_version}
BuildRequires: libX11-devel
BuildRequires: libXpm-devel
%endif
BuildRequires: zlib-devel
BuildRequires: pkgconfig
BuildRequires: libtool
%if !0%{?os2_version}
BuildRequires: perl-interpreter
%else
BuildRequires: perl
%endif
BuildRequires: perl-generators
BuildRequires: perl(FindBin)
# for fontconfig/basic test
#BuildRequires: liberation-sans-fonts


%description
The gd graphics library allows your code to quickly draw images
complete with lines, arcs, text, multiple colors, cut and paste from
other images, and flood fills, and to write out the result as a PNG or
JPEG file. This is particularly useful in Web applications, where PNG
and JPEG are two of the formats accepted for inline images by most
browsers. Note that gd is not a paint program.


%package progs
Requires:       %{name} = %{version}-%{release}
Summary:        Utility programs that use libgd

%description progs
The gd-progs package includes utility programs supplied with gd, a
graphics library for creating PNG and JPEG images.


%package devel
Summary:  The development libraries and header files for gd
Requires: %{name} = %{version}-%{release}
Requires: freetype-devel
Requires: fontconfig-devel
Requires: libjpeg-devel
Requires: libpng-devel
Requires: libtiff-devel
Requires: libwebp-devel
%if !0%{?os2_version}
Requires: libX11-devel
Requires: libXpm-devel
%endif
Requires: zlib-devel
%if %{with_liq}
Requires: libimagequant-devel
%endif
%if %{with_raqm}
Requires: libraqm-devel
%endif


%description devel
The gd-devel package contains the development libraries and header
files for gd, a graphics library for creating PNG and JPEG graphics.

%if !0%{?os2_version}
%debug_package
%endif

%prep
%if !0%{?os2_version}
%setup -q -n libgd-%{version}%{?prever:-%{prever}}
%patch0 -p1
install -m 0755 %{SOURCE1} config/

: $(perl config/getver.pl)

: regenerate autotool stuff
if [ -f configure ]; then
   libtoolize --copy --force
   autoreconf -vif
else
   ./bootstrap.sh
fi
%else
%scm_setup
autoreconf -fvi
%endif


%build
# Provide a correct default font search path
%if !0%{?os2_version}
CFLAGS="$RPM_OPT_FLAGS -DDEFAULT_FONTPATH='\"\
/usr/share/fonts/bitstream-vera:\
/usr/share/fonts/dejavu:\
/usr/share/fonts/default/Type1:\
/usr/share/X11/fonts/Type1:\
/usr/share/fonts/liberation\"'"
%else
CFLAGS="$RPM_OPT_FLAGS -DDEFAULT_FONTPATH='\"\
/@unixroot/usr/share/fonts/bitstream-vera;\
/@unixroot/usr/share/fonts/dejavu;\
/@unixroot/usr/share/fonts/default/Type1;\
/@unixroot/usr/share/fonts/liberation\"'"
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"
export LIBS="-lcx -lpthread"
# Set BUILDLEVEL to be embedded to all DLLs built with Libtool.
export LT_BUILDLEVEL="@#%{vendor}:%{version}-%{release}#@##1## `LANG=C date +'%%d %%b %%Y %%H:%%M:%%S'`     `uname -n`::::0::"
%endif

%ifarch %{ix86}
# see https://github.com/libgd/libgd/issues/242
CFLAGS="$CFLAGS -msse -mfpmath=sse"
%endif

%ifarch aarch64 ppc64 ppc64le s390 s390x
# workaround for https://bugzilla.redhat.com/show_bug.cgi?id=1359680
export CFLAGS="$CFLAGS -ffp-contract=off"
%endif

%configure \
    --with-tiff=%{_prefix} \
    --disable-rpath
make %{?_smp_mflags}


%install
make install INSTALL='install -p' DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT/%{_libdir}/libgd.la
rm -f $RPM_BUILD_ROOT/%{_libdir}/libgd.a


%check
%if 0%{?os2_version}
export BEGINLIBPATH=%{_builddir}/%{buildsubdir}/src/.libs
export LIBPATHSTRICT=T
%endif
# minor diff in size
XFAIL_TESTS="gdimagestringft/gdimagestringft_bbox"
%ifarch s390x
XFAIL_TESTS="gdimagestring16/gdimagestring16 gdimagestringup16/gdimagestringup16 $XFAIL_TESTS"
%endif
%if 0%{?os2_version} && "%{_target_cpu}" == "i686"
XFAIL_TESTS="$XFAIL_TESTS gdimagegrayscale/basic.exe"
%endif
export XFAIL_TESTS

: Upstream test suite
make check

: Check content of pkgconfig
grep %{version} $RPM_BUILD_ROOT%{_libdir}/pkgconfig/gdlib.pc


%if !0%{?os2_version}
%ldconfig_scriptlets
%endif


%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%if !0%{?os2_version}
%{_libdir}/*.so.*
%else
%{_libdir}/*.dll
%endif

%files progs
%{_bindir}/*
%if 0%{?os2_version}
%exclude %{_bindir}/*.dbg
%endif

%files devel
%{_includedir}/*
%if !0%{?os2_version}
%{_libdir}/*.so
%else
%{_libdir}/*.a
%endif
%{_libdir}/pkgconfig/gdlib.pc


%changelog
* Wed Dec 16 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.3.0-1
- updated to version 2.3.0
- resync with fedora spec
- added changelog entry
