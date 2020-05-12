Summary: H264/AVC video streams encoder
Name: x264
Version: 0.160
Release: 1%{?dist}
License: GPLv2+
URL: https://www.videolan.org/developers/x264.html
Vendor:  bww bitwise works GmbH
%scm_source github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2


BuildRequires: gcc
BuildRequires: nasm
# we need to enforce the exact EVR for an ISA - not only the same ABI
Requires: %{name}-libs = %{version}-%{release}

%description
x264 is a free library for encoding H264/AVC video streams, written from
scratch.

This package contains the frontend.

%package libs
Summary: Library for encoding H264/AVC video streams
%if !0%{?os2_version}
Recommends: %{_libdir}/libOpenCL.so.1
%endif

%description libs
x264 is a free library for encoding H264/AVC video streams, written from
scratch.

%package devel
Summary: Development files for the x264 library
Requires: %{name}-libs = %{version}-%{release}
Requires: pkgconfig

%description devel
x264 is a free library for encoding H264/AVC video streams, written from
scratch.

This package contains the development files.

%debug_package


%prep
%scm_setup


%build
export LDFLAGS=" -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"
export LIBS="-lcx"
export VENDOR="%{vendor}"
%configure \
    --enable-debug \
    --enable-shared \
    --system-libx264

%{__make} %{?_smp_mflags}


%install
%make_install


%if !0%{?os2_version}
%ldconfig_scriptlets
%endif


%files
%{_bindir}/x264.exe

%files libs
%doc AUTHORS
%license COPYING
%{_libdir}/x264*.dll

%files devel
%doc doc/*
%{_includedir}/x264.h
%{_includedir}/x264_config.h
%{_libdir}/libx264_dll.a
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Wed May 13 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.160-1
- first OS/2 rpm
