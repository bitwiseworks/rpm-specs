%global _hardened_build 1
%global have_java 0
%global have_glut 0

Name:          libwebp
Version:       1.1.0
Release:       1%{?dist}
URL:           http://webmproject.org/
Summary:       Library and tools for the WebP graphics format
# Additional IPR is licensed as well. See PATENTS file for details
License:       BSD
Vendor:        bww bitwise works GmbH
%scm_source github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2

BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: giflib-devel
BuildRequires: libtiff-devel
%if %{have_java}
BuildRequires: java-devel
BuildRequires: jpackage-utils
BuildRequires: swig
%endif
BuildRequires: autoconf automake libtool
%if %{have_glut}
BuildRequires: freeglut-devel
%endif

%description
WebP is an image format that does lossy compression of digital
photographic images. WebP consists of a codec based on VP8, and a
container based on RIFF. Webmasters, web developers and browser
developers can use WebP to compress, archive and distribute digital
images more efficiently.


%package tools
Summary:       The WebP command line tools

%description tools
WebP is an image format that does lossy compression of digital
photographic images. WebP consists of a codec based on VP8, and a
container based on RIFF. Webmasters, web developers and browser
developers can use WebP to compress, archive and distribute digital
images more efficiently.


%package devel
Summary:       Development files for libwebp, a library for the WebP format
Requires:      %{name} = %{version}-%{release}

%description devel
WebP is an image format that does lossy compression of digital
photographic images. WebP consists of a codec based on VP8, and a
container based on RIFF. Webmasters, web developers and browser
developers can use WebP to compress, archive and distribute digital
images more efficiently.


%if %{have_java}
%package java
Summary:       Java bindings for libwebp, a library for the WebP format
Requires:      %{name} = %{version}-%{release}
Requires:      java-headless
Requires:      jpackage-utils

%description java
Java bindings for libwebp.
%endif


%debug_package


%prep
%scm_setup


%build
autoreconf -vif
%ifarch aarch64
export CFLAGS="%{optflags} -frename-registers"
%endif
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"
export LIBS="-lcx"
# Neon disabled due to resulting CFLAGS conflict resulting in
# inlining failed in call to always_inline '[...]': target specific option mismatch
%configure --disable-static --enable-libwebpmux \
           --enable-libwebpdemux --enable-libwebpdecoder \
           --disable-neon

# Set BUILDLEVEL to be embedded to all DLLs built with Libtool.
export LT_BUILDLEVEL="@#%{vendor}:%{version}-%{release}#@##1## `LANG=C date +'%%d %%b %%Y %%H:%%M:%%S'`     `uname -n`::::0::"

make V=1
make -C examples vwebp

%if %{have_java}
# swig generated Java bindings
cp %{SOURCE1} .
cd swig
rm -rf libwebp.jar libwebp_java_wrap.c
mkdir -p java/com/google/webp
swig -ignoremissing -I../src -java \
    -package com.google.webp  \
    -outdir java/com/google/webp \
    -o libwebp_java_wrap.c libwebp.swig

gcc %{__global_ldflags} %{optflags} -shared \
    -I/usr/lib/jvm/java/include \
    -I/usr/lib/jvm/java/include/linux \
    -I../src \
    -L../src/.libs -lwebp libwebp_java_wrap.c \
    -o libwebp_jni.so

cd java
javac com/google/webp/libwebp.java
jar cvf ../libwebp.jar com/google/webp/*.class
%endif


%install
%make_install
%if %{have_glut}
install -m 755 examples/vwebp %{buildroot}%{_bindir}/vwebp
%endif
find "%{buildroot}/%{_libdir}" -type f -name "*.la" -delete

# swig generated Java bindings
%if %{have_java}
mkdir -p %{buildroot}/%{_libdir}/%{name}-java
cp swig/*.jar swig/*.so %{buildroot}/%{_libdir}/%{name}-java/
%endif


#ldconfig_scriptlets


%files tools
%{_bindir}/cwebp.exe
%{_bindir}/dwebp.exe
%{_bindir}/gif2webp.exe
%{_bindir}/img2webp.exe
%{_bindir}/webpinfo.exe
%{_bindir}/webpmux.exe
%if %{have_glut}
%{_bindir}/vwebp.exe
%endif
%{_mandir}/man*/*

%files -n %{name}
%doc README PATENTS NEWS AUTHORS
%license COPYING
%{_libdir}/webp7.dll
%{_libdir}/webpdec3.dll
%{_libdir}/webpdem2.dll
%{_libdir}/webpmux3.dll

%files devel
%{_libdir}/webp*_dll.a
%{_includedir}/*
%{_libdir}/pkgconfig/*

%if %{have_java}
%files java
%doc libwebp_jni_example.java
%{_libdir}/%{name}-java/
%endif


%changelog
* Wed Apr 15 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.1.0-1
- first rpm for OS/2
