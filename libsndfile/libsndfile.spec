Summary:	Library for reading and writing sound files
Name:		libsndfile
Version:	1.1.0
Release:	1%{?dist}
License:	LGPLv2+ and GPLv2+ and BSD
URL:		http://libsndfile.github.io/libsndfile/
%if !0%{?os2_version}
Source0:        https://github.com/libsndfile/libsndfile/releases/download/%{version}/libsndfile-%{version}.tar.bz2
%else
%scm_source github https://github.com/TeLLie/libsndfile-os2 %{version}-os2
%endif
%if !0%{?os2_version}
Patch0:		libsndfile-1.0.25-system-gsm.patch
Patch1:		libsndfile-1.0.25-zerodivfix.patch
# from upstream, fix #1984320=CVE-2021-3246, for <= 1.0.31
Patch2:		libsndfile-1.0.31-deb669ee.patch
# from upstream, fix #2027692, for <= 1.0.31
Patch3:		libsndfile-1.0.31-ced91d7b.patch
%endif
BuildRequires:  gcc-c++
%if !0%{?os2_version}
BuildRequires:	alsa-lib-devel
%endif
BuildRequires:	flac-devel
BuildRequires:	gcc
BuildRequires:	libogg-devel
BuildRequires:	libvorbis-devel
BuildRequires:	pkgconfig
BuildRequires:	sqlite-devel
%if !0%{?os2_version}
BuildRequires:	gsm-devel
%endif
BuildRequires:	libtool
BuildRequires:	make
BuildRequires:	python3
BuildRequires:  opus-devel


%description
libsndfile is a C library for reading and writing sound files such as
AIFF, AU, WAV, and others through one standard interface. It can
currently read/write 8, 16, 24 and 32-bit PCM files as well as 32 and
64-bit floating point WAV files and a number of compressed formats. It
compiles and runs on *nix, MacOS, and Win32.


%package devel
Summary:	Development files for libsndfile
Requires:	%{name}%{?_isa} = %{version}-%{release} pkgconfig


%description devel
libsndfile is a C library for reading and writing sound files such as
AIFF, AU, WAV, and others through one standard interface.
This package contains files needed to develop with libsndfile.


%package utils
Summary:	Command Line Utilities for libsndfile
Requires:	%{name} = %{version}-%{release}


%description utils
libsndfile is a C library for reading and writing sound files such as
AIFF, AU, WAV, and others through one standard interface.
This package contains command line utilities for libsndfile.


%prep
%if !0%{?os2_version}
%setup -q
%patch0 -p1 -b .system-gsm
rm -r src/GSM610
%else
%scm_setup
%endif
# TODO: check if this patch is still needed
%if !0%{?os2_version}
%patch1 -p1 -b .zerodivfix
%patch2 -p1 -b .deb669ee
%patch3 -p1 -b .ced91d7b
%endif

%build
%if !0%{?os2_version}
autoreconf -I M4 -fiv # for system-gsm patch
%configure \
	--disable-dependency-tracking \
	--enable-sqlite \
	--enable-alsa \
	--enable-largefile \
	--disable-static
%else
mkdir build
cd build
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp" 
export LIBS="-lcx"
%cmake -DCMAKE_INSTALL_PREFIX:PATH=/@unixroot/usr \
      -DCMAKE_SKIP_RPATH:BOOL=YES \
      -DOS2_USE_CXX_EMXEXP=ON \
      -DCMAKE_BUILD_TYPE=Release \
      -Wno-dev \
       ..
%endif
# Get rid of rpath
%if !0%{?os2_version}
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%endif

%if !0%{?os2_version}
%make_build
%else
make %{?_smp_mflags}
%endif

%install
%make_install -C build
rm -rf __docs
mkdir __docs
cp -pR $RPM_BUILD_ROOT%{_docdir}/%{name}/* __docs
rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}
find %{buildroot} -type f -name "*.la" -delete

# fix multilib issues
mv %{buildroot}%{_includedir}/sndfile.h \
   %{buildroot}%{_includedir}/sndfile-%{__isa_bits}.h

cat > %{buildroot}%{_includedir}/sndfile.h <<EOF
#include <bits/wordsize.h>

#if __WORDSIZE == 32
# include "sndfile-32.h"
#elif __WORDSIZE == 64
# include "sndfile-64.h"
#else
# error "unexpected value for __WORDSIZE macro"
#endif
EOF

%if 0%{?rhel} != 0 || !0%{?os2_version}
rm -f %{buildroot}%{_bindir}/sndfile-jackplay
%endif


%check
%if 0%{?os2_version}
LD_LIBRARY_PATH=$PWD/build
%endif
cd build
make -k test


%if !0%{?os2_version}
%ldconfig_scriptlets
%endif

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc AUTHORS README NEWS
%if !0%{?os2_version}
%{_libdir}/%{name}.so.*
%else
%{_libdir}/*.dll
%endif

%files utils
%if !0%{?os2_version}
%{_bindir}/sndfile-cmp
%{_bindir}/sndfile-concat
%{_bindir}/sndfile-convert
%{_bindir}/sndfile-deinterleave
%{_bindir}/sndfile-info
%{_bindir}/sndfile-interleave
%{_bindir}/sndfile-metadata-get
%{_bindir}/sndfile-metadata-set
%{_bindir}/sndfile-play
%{_bindir}/sndfile-salvage
%else
%{_bindir}/sndfile-cmp.exe
%{_bindir}/sndfile-concat.exe
%{_bindir}/sndfile-convert.exe
%{_bindir}/sndfile-deinterleave.exe
%{_bindir}/sndfile-info.exe
%{_bindir}/sndfile-interleave.exe
%{_bindir}/sndfile-metadata-get.exe
%{_bindir}/sndfile-metadata-set.exe
%{_bindir}/sndfile-play.exe
%{_bindir}/sndfile-salvage.exe
%endif
%{_mandir}/man1/sndfile-cmp.1*
%{_mandir}/man1/sndfile-concat.1*
%{_mandir}/man1/sndfile-convert.1*
%{_mandir}/man1/sndfile-deinterleave.1*
%{_mandir}/man1/sndfile-info.1*
%{_mandir}/man1/sndfile-interleave.1*
%{_mandir}/man1/sndfile-metadata-get.1*
%{_mandir}/man1/sndfile-metadata-set.1*
%{_mandir}/man1/sndfile-play.1*
%{_mandir}/man1/sndfile-salvage.1*

%files devel
%doc __docs ChangeLog
%{_includedir}/sndfile.h
%{_includedir}/sndfile.hh
%{_includedir}/sndfile-%{__isa_bits}.h
%if !0%{?os2_version}
%{_libdir}/%{name}.so
%else
%{_libdir}/*.a
%endif
%dir %{_libdir}/cmake/SndFile
%{_libdir}/cmake/SndFile/SndFileTargets-release.cmake
%{_libdir}/cmake/SndFile/SndFileConfig.cmake
%{_libdir}/cmake/SndFile/SndFileConfigVersion.cmake
%{_libdir}/cmake/SndFile/SndFileTargets.cmake
%{_libdir}/pkgconfig/sndfile.pc


%changelog
* Sun Apr 10 2022 Elbert Pol <elbert.pol@gmail.com> - 1.0.1-1
- Updated to latest version

* Sun Jan 31 2021 Elbert Pol <elbert.pol@gmail.com> - 1.0.21-2
- Update the spec more to Fedora style

* Tue Jan 26 2021 Elbert Pol <elbert.pol@gmail.com> - 1.0.31-1
- First rpm version for OS2
- Update to latest version