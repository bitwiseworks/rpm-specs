%global somajor 8
%global sominor 0
%global sotiny  0
%global soversion %{somajor}.%{sominor}.%{sotiny}

Name:			libvpx
Summary:		VP8/VP9 Video Codec SDK
Version:		1.13.1
Release:		1%{?dist}
License:		BSD-3-Clause
URL:			http://www.webmproject.org/code/
%if !0%{?os2_version}
Source0:		https://github.com/webmproject/libvpx/archive/v%{version}.tar.gz
Source1:		vpx_config.h
# Thanks to debian.
Source2:		libvpx.ver
# Do not disable FORTIFY_SOURCE=2
Patch0:			libvpx-1.7.0-leave-fortify-source-on.patch
%else
Vendor:			bww bitwise works GmbH
%scm_source github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2
%endif
BuildRequires:		gcc
BuildRequires:		gcc-c++
BuildRequires:		make
%if !0%{?os2_version}
%ifarch %{ix86} x86_64
BuildRequires:		yasm
%endif
%else
BuildRequires:		nasm
%endif
%if !0%{?os2_version}
BuildRequires:		doxygen, php-cli, perl(Getopt::Long)
%else
BuildRequires:		doxygen, perl(Getopt::Long)
%endif

%description
libvpx provides the VP8/VP9 SDK, which allows you to integrate your applications
with the VP8 and VP9 video codecs, high quality, royalty free, open source codecs
deployed on millions of computers and devices worldwide.

%package devel
Summary:		Development files for libvpx
Requires:		%{name} = %{version}-%{release}

%description devel
Development libraries and headers for developing software against
libvpx.

%package utils
Summary:		VP8 utilities and tools
Requires:		%{name} = %{version}-%{release}

%description utils
A selection of utilities and tools for VP8, including a sample encoder
and decoder.

%if 0%{?os2_version}
%legacy_runtime_packages

%debug_package
%endif

%prep
%if !0%{?os2_version}
%setup -q -n libvpx-%{version}
%patch -P0 -p1 -b .fortify-source-on
%else
%scm_setup
%endif

%build

%ifarch %{ix86}
%if !0%{?os2_version}
%global vpxtarget x86-linux-gcc
%else
%global vpxtarget x86-os2-gcc
%endif
%else
%ifarch	x86_64
%global	vpxtarget x86_64-linux-gcc
%else
%ifarch aarch64
%global vpxtarget arm64-linux-gcc
%else
%global vpxtarget generic-gnu
%endif
%endif
%endif

%if 0%{?os2_version}
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"
export VENDOR="%{vendor}"
%endif
# History: The configure script used to reject the shared flag on the generic target.
# This meant that we needed to fall back to manual shared lib creation.
# However, the modern configure script permits the shared flag and assumes ELF.
# Additionally, the libvpx.ver would need to be updated to work properly.
# As a result, we disable this universally, but keep it around in case we ever need to support
# something "special".
%if "%{vpxtarget}" == "generic-gnu"
%global generic_target 0
%else
%global	generic_target 0
%endif

%set_build_flags

./configure --target=%{vpxtarget} \
--enable-pic --disable-install-srcs \
--enable-vp9-decoder --enable-vp9-encoder \
--enable-experimental \
--enable-vp9-highbitdepth \
--enable-debug \
%if ! %{generic_target}
--enable-shared \
%endif
--enable-install-srcs \
--prefix=%{_prefix} --libdir=%{_libdir} --size-limit=16384x16384

%if !0%{?os2_version}
%make_build verbose=true
%else
make %{?_smp_mflags} verbose=true
%endif

# Manual shared library creation
# We should never need to do this anymore, and if we do, we need to fix the version-script.
%if %{generic_target}
mkdir tmp
cd tmp
ar x ../libvpx_g.a
cd ..
gcc -fPIC -shared -pthread -lm -Wl,--no-undefined -Wl,-soname,libvpx.so.%{somajor} -Wl,--version-script,%{SOURCE2} -Wl,-z,noexecstack -o libvpx.so.%{soversion} tmp/*.o
rm -rf tmp
%endif

# Temporarily dance the static libs out of the way
# mv libvpx.a libNOTvpx.a
# mv libvpx_g.a libNOTvpx_g.a

# We need to do this so the examples can link against it.
# ln -sf libvpx.so.%{soversion} libvpx.so

# %make_build verbose=true target=examples CONFIG_SHARED=1
# %make_build verbose=true target=docs

# Put them back so the install doesn't fail
# mv libNOTvpx.a libvpx.a
# mv libNOTvpx_g.a libvpx_g.a

%install
make DIST_DIR=%{buildroot}%{_prefix} dist

# Simpler to label the dir as %%doc.
if [ -d %{buildroot}%{_prefix}/docs ]; then
   mv %{buildroot}%{_prefix}/docs doc/
fi

# Again, we should never need to do this anymore.
%if %{generic_target}
install -p libvpx.so.%{soversion} %{buildroot}%{_libdir}
pushd %{buildroot}%{_libdir}
ln -sf libvpx.so.%{soversion} libvpx.so
ln -sf libvpx.so.%{soversion} libvpx.so.%{somajor}
ln -sf libvpx.so.%{soversion} libvpx.so.%{somajor}.%{sominor}
popd
%endif

%if !0%{?os2_version}
pushd %{buildroot}
%else
cd %{buildroot}
%endif

# Stuff we don't need.
%if !0%{?os2_version}
rm -rf .%{_prefix}/build/ .%{_prefix}/md5sums.txt .%{_libdir}*/*.a .%{_prefix}/CHANGELOG .%{_prefix}/README
%else
rm -rf .%{_prefix}/build/ .%{_prefix}/md5sums.txt .%{_libdir}*/libvpx.a .%{_prefix}/CHANGELOG .%{_prefix}/README
%endif
# No, bad google. No treat.
mv .%{_bindir}/examples/* .%{_bindir}
rm -rf .%{_bindir}/examples

# Rename a few examples
%if !0%{?os2_version}
mv .%{_bindir}/postproc .%{_bindir}/vp8_postproc
mv .%{_bindir}/simple_decoder .%{_bindir}/vp8_simple_decoder
mv .%{_bindir}/simple_encoder .%{_bindir}/vp8_simple_encoder
mv .%{_bindir}/twopass_encoder .%{_bindir}/vp8_twopass_encoder
%else
mv .%{_bindir}/postproc.exe .%{_bindir}/vp8_postproc.exe
mv .%{_bindir}/simple_decoder.exe .%{_bindir}/vp8_simple_decoder.exe
mv .%{_bindir}/simple_encoder.exe .%{_bindir}/vp8_simple_encoder.exe
mv .%{_bindir}/twopass_encoder.exe .%{_bindir}/vp8_twopass_encoder.exe
%endif
# Fix the binary permissions
chmod 755 .%{_bindir}/*
%if !0%{?os2_version}
popd
%else
cd ..
%endif

# Get the vpx_config.h file
%if !0%{?os2_version}
# Does ppc64le need its own?
%ifarch ppc64 ppc64le
cp -a vpx_config.h %{buildroot}%{_includedir}/vpx/vpx_config-ppc64.h
%else
%ifarch s390 s390x
cp -a vpx_config.h %{buildroot}%{_includedir}/vpx/vpx_config-s390.h
%else
%ifarch %{ix86}
cp -a vpx_config.h %{buildroot}%{_includedir}/vpx/vpx_config-x86.h
%else
cp -a vpx_config.h %{buildroot}%{_includedir}/vpx/vpx_config-%{_arch}.h
%endif
%endif
%endif
cp %{SOURCE1} %{buildroot}%{_includedir}/vpx/vpx_config.h
# for timestamp sync
touch -r AUTHORS %{buildroot}%{_includedir}/vpx/vpx_config.h
%endif

mv %{buildroot}%{_prefix}/src/vpx_dsp %{buildroot}%{_includedir}/
mv %{buildroot}%{_prefix}/src/vpx_mem %{buildroot}%{_includedir}/
mv %{buildroot}%{_prefix}/src/vpx_ports %{buildroot}%{_includedir}/
mv %{buildroot}%{_prefix}/src/vpx_scale %{buildroot}%{_includedir}/

rm -rf %{buildroot}%{_prefix}/src

%if !0%{?os2_version}
%ldconfig_scriptlets
%endif

%files
%license LICENSE
%doc AUTHORS CHANGELOG README
%if !0%{?os2_version}
%{_libdir}/libvpx.so.%{somajor}*
%else
%{_libdir}/libvpx8.dll
%endif

%files devel
# These are SDK docs, not really useful to an end-user.
%doc docs/html/
%{_includedir}/vpx/
%{_includedir}/vpx_dsp/
%{_includedir}/vpx_mem/
%{_includedir}/vpx_ports/
%{_includedir}/vpx_scale/
%{_libdir}/pkgconfig/vpx.pc
%if !0%{?os2_version}
%{_libdir}/libvpx.so
%else
%{_libdir}/libvpx_dll.a
%endif

%files utils
%if !0%{?os2_version}
%{_bindir}/*
%{_bindir}/tools/*
%else
%{_bindir}/*.exe
%{_bindir}/tools/*.exe
%endif

%changelog
* Wed Nov 08 2023 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.13.1-1
- Update to version 1.13.1.

* Mon Apr 20 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.8.2-1
- Update to version 1.8.2.
- syncronized with latest fedora spec
- moved source to github

* Fri Feb 3 2017 Dmitriy Kuminov <coding@dmik.org> 1.6.1-1
- Update to version 1.6.1.
- Generate development documentation and provide it in a separate sub-package.
- Provide legacy packages with DLLs for old ABI.

* Fri Feb 3 2017 Dmitriy Kuminov <coding@dmik.org> 1.4.0-2
- Use -Zomf to preserve HLL debug info and significantly reduce DLL size.
- Use per-platform optimization flags.
- Remove static library and OMF libraries.

* Tue Nov 17 2015 Valery Sedletski <_valerius@mail.ru> - 1.4.0 OS/2 initial build
- initial OS/2 build
