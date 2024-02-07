#global candidate rc2

%if 0%{?fedora}
%bcond_without mingw

# uses wine, requires enabled binfmt
%bcond_with tests
%else
%bcond_with mingw
%endif

Name:     opus
Version:  1.4
Release:  1%{?candidate:.%{candidate}}%{?dist}
Summary:  An audio codec for use in low-delay speech and audio communication
License:  BSD-3-Clause AND BSD-2-Clause
URL:      https://www.opus-codec.org/

%if !0%{?os2_version}
Source0:  https://ftp.osuosl.org/pub/xiph/releases/%{name}/%{name}-%{version}%{?candidate:-%{candidate}}.tar.gz
%else
Vendor:   bww bitwise works GmbH
%scm_source github https://github.com/bitwiseworks/%{name}-os2 v%{version}-os2
%endif
# This is the final IETF Working Group RFC
Source1:  https://tools.ietf.org/rfc/rfc6716.txt
Source2:  https://tools.ietf.org/rfc/rfc8251.txt

BuildRequires: make
BuildRequires: gcc
BuildRequires: doxygen
BuildRequires: libtool

%if %{with mingw}
BuildRequires: mingw32-filesystem
BuildRequires: mingw32-gcc

BuildRequires: mingw64-gcc
BuildRequires: mingw64-filesystem

%if %{with tests}
BuildRequires: wine
%endif
%endif

%description
The Opus codec is designed for interactive speech and audio transmission over
the Internet. It is designed by the IETF Codec Working Group and incorporates
technology from Skype's SILK codec and Xiph.Org's CELT codec.

%package  devel
Summary:  Development package for opus
Requires: libogg-devel
Requires: opus = %{version}-%{release}

%description devel
Files for development with opus.

%if %{with mingw}
%package -n mingw32-%{name}
Summary: MinGW compiled %{name} library for Win32 target
BuildArch: noarch

%description -n mingw32-%{name}
This package contains the MinGW compiled library of %{name}
for Win32 target.

%package -n mingw64-%{name}
Summary: MinGW compiled %{name} library for Win64 target
BuildArch: noarch

%description -n mingw64-%{name}
This package contains the MinGW compiled library of %{name}
for Win64 target.

%{?mingw_debug_package}
%endif

%if 0%{?os2_version}
%debug_package
%endif

%prep
%if !0%{?os2_version}
%setup -q %{?candidate:-n %{name}-%{version}-%{candidate}}
%else
%scm_setup
echo PACKAGE_VERSION="%{version}" > package_version
%endif
cp %{SOURCE1} .
cp %{SOURCE2} .

%build
autoreconf -ivf
mkdir build_native
%if !0%{?os2_version}
pushd build_native
%else
cd build_native
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"
export LIBS="-lcx"
# Set BUILDLEVEL to be embedded to all DLLs built with Libtool.
export LT_BUILDLEVEL="@#%{vendor}:%{version}-%{release}#@##1## `LANG=C date +'%%d %%b %%Y %%H:%%M:%%S'`     `uname -n`::::0::"
%endif
%global _configure ../configure
%configure --enable-custom-modes --disable-static \
           --enable-hardening \
%ifarch %{arm} %{arm64} %{power64}
        --enable-fixed-point
%endif

%make_build
%if !0%{?os2_version}
popd
%else
cd ..
%endif

%if %{with mingw}
%mingw_configure --enable-custom-modes --disable-static --disable-doc
%mingw_make %{?_smp_mflags} V=1
%endif

%install
%make_install -C build_native

rm %{buildroot}%{_libdir}/libopus.la
rm -rf %{buildroot}%{_datadir}/doc/opus

%if %{with mingw}
%mingw_make_install DESTDIR=%{buildroot}
rm %{buildroot}%{mingw32_libdir}/libopus.la
rm %{buildroot}%{mingw64_libdir}/libopus.la
%mingw_debug_install_post
%endif

%check
%if 0%{?os2_version}
export BEGINLIBPATH=%{_builddir}/%{buildsubdir}/build_native/.libs
%endif
make -C build_native check %{?_smp_mflags} V=1

%if !0%{?os2_version}
%ldconfig_scriptlets
%endif

%if %{with mingw}
%if %{with tests}
%mingw_make check
%endif
%endif

%files
%license COPYING
%if !0%{?os2_version}
%{_libdir}/libopus.so.*
%else
%{_libdir}/opus*.dll
%endif

%files devel
%doc README build_native/doc/html rfc6716.txt rfc8251.txt
%{_includedir}/opus
%if !0%{?os2_version}
%{_libdir}/libopus.so
%else
%{_libdir}/*.a
%endif
%{_libdir}/pkgconfig/opus.pc
%{_datadir}/aclocal/opus.m4
%{_datadir}/man/man3/opus_*.3.gz

%if %{with mingw}
%files -n mingw32-%{name}
%license COPYING
%dir %{mingw32_includedir}/opus/
%{mingw32_bindir}/libopus-0.dll
%{mingw32_includedir}/opus/*.h
%{mingw32_libdir}/libopus.dll.a
%{mingw32_libdir}/pkgconfig/opus.pc
%{mingw32_datadir}/aclocal/opus.m4

%files -n mingw64-%{name}
%license COPYING
%dir %{mingw64_includedir}/opus/
%{mingw64_bindir}/libopus-0.dll
%{mingw64_includedir}/opus/*.h
%{mingw64_libdir}/libopus.dll.a
%{mingw64_libdir}/pkgconfig/opus.pc
%{mingw64_datadir}/aclocal/opus.m4
%endif

%changelog
* Wed Feb 07 2024 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.4-1
- updated to latest version
- syncronized the spec with lated fedora spec

* Mon Sep 07 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.3.1-2
- make sure we get the right version in the .pc file and in config.h

* Wed Apr 15 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.3.1-1
- cloned source to out github repo
- updated to latest version
- syncronized the spec with lated fedora spec
- add bldlevel info to the dll

* Mon Mar 04 2019 Elbert Pol <elbert.pol@gmail.com> - 1.3-2
- Add dll to right section

* Sun Mar 03 2019 Elbert Pol <elbert.pol@gmail.com> - 1.3-1
- first RPM release for OS2
