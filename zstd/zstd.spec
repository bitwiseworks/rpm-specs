# enable asm implementations by default
%bcond_without asm

# enable .lz4 support by default
%if !0%{?os2_version}
%bcond_without lz4
%else
%bcond_with lz4
%endif

# enable .xz/.lzma support by default
%bcond_without lzma

# enable .gz support by default
%bcond_without zlib

# enable pzstd support by default
%bcond_without pzstd

# Disable gtest on RHEL
%if !0%{?os2_version}
%bcond gtest %[ !0%{?rhel} ]
%else
%bcond_with gtest
%endif

Name:           zstd
Version:        1.5.5
Release:        1%{?dist}
Summary:        Zstd compression library

License:        BSD-3-Clause AND GPL-2.0-only
URL:            https://github.com/facebook/zstd
%if !0%{?os2_version}
Source0:        https://github.com/facebook/zstd/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

Patch1:         pzstd.1.patch
%else
Vendor: bww bitwise works GmbH
%scm_source     github http://github.com/bitwiseworks/%{name}-os2 v%{version}-os2
%endif

BuildRequires:  make
%if 0%{?os2_version}
BuildRequires:  cmake
%endif
BuildRequires:  gcc %{?with_gtest:gtest-devel}
%if %{with lz4}
BuildRequires:  lz4-devel
%endif
%if %{with lzma}
BuildRequires:  xz-devel
%endif
%if %{with pzstd}
BuildRequires:  gcc-c++
%endif
%if %{with zlib}
BuildRequires:  zlib-devel
%endif
%if !0%{?os2_version}
BuildRequires:  execstack
%endif

%description
Zstd, short for Zstandard, is a fast lossless compression algorithm,
targeting real-time compression scenarios at zlib-level compression ratio.

%package -n lib%{name}
Summary:        Zstd shared library

%description -n lib%{name}
Zstandard compression shared library.

%package -n lib%{name}-devel
Summary:        Header files for Zstd library
%if !0%{?os2_version}
Requires:       lib%{name}%{?_isa} = %{version}-%{release}
%else
Requires:       lib%{name} = %{version}-%{release}
%endif

%package -n lib%{name}-static
Summary:        Static variant of the Zstd library
Requires:       lib%{name}-devel = %{version}-%{release}

%description -n lib%{name}-devel
Header files for Zstd library.

%description -n lib%{name}-static
Static variant of the Zstd library.

%if 0%{?os2_version}
%debug_package
%endif

%prep
%if !0%{?os2_version}
%setup -q
find -name .gitignore -delete
%if %{with pzstd}
%patch1 -p1
%endif
%else
%scm_setup
%endif

%build
%if !0%{?os2_version}
export CFLAGS="$RPM_OPT_FLAGS"
export LDFLAGS="$RPM_LD_FLAGS"
export PREFIX="%{_prefix}"
export LIBDIR="%{_libdir}"
%make_build -C lib lib-mt %{!?with_asm:ZSTD_NO_ASM=1}
%make_build -C programs %{!?with_asm:ZSTD_NO_ASM=1}
%if %{with pzstd}
export CXXFLAGS="$RPM_OPT_FLAGS"
%make_build -C contrib/pzstd %{!?with_asm:ZSTD_NO_ASM=1}
%endif
%else
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"
export VENDOR="%{vendor}"
%cmake \
	-DZSTD_ZLIB_SUPPORT:BOOL=ON \
	-DZSTD_LZMA_SUPPORT:BOOL=ON \
	-DZSTD_BUILD_CONTRIB:BOOL=ON \
	-DZSTD_BUILD_TESTS:BOOL=ON \
	-DZSTD_FUZZER_FLAGS=-T20s -DZSTD_ZSTREAM_FLAGS=-T20s -DZSTD_FULLBENCH_FLAGS=-i0 \
	-S build/cmake
%cmake_build
%endif

%check
%if !0%{?os2_version}
execstack lib/libzstd.so.1

export CFLAGS="$RPM_OPT_FLAGS"
export LDFLAGS="$RPM_LD_FLAGS"
make -C tests test-zstd
%if %{with pzstd} && %{with gtest}
export CXXFLAGS="$RPM_OPT_FLAGS"
make -C contrib/pzstd test
%endif
%endif

%install
%if !0%{?os2_version}
%make_install PREFIX=%{_prefix} LIBDIR=%{_libdir}
%else
%cmake_install
%endif
%if %{with pzstd}
%if !0%{?os2_version}
install -D -m755 contrib/pzstd/pzstd %{buildroot}%{_bindir}/pzstd
%endif
install -D -m644 programs/%{name}.1 %{buildroot}%{_mandir}/man1/p%{name}.1
%endif

%files
%doc CHANGELOG README.md
%if !0%{?os2_version}
%{_bindir}/%{name}
%else
%{_bindir}/%{name}.exe
%endif
%if %{with pzstd}
%if !0%{?os2_version}
%{_bindir}/p%{name}
%else
%{_bindir}/p%{name}.exe
%endif
%{_mandir}/man1/p%{name}.1*
%endif
%{_bindir}/%{name}mt
%{_bindir}/un%{name}
%{_bindir}/%{name}cat
%{_bindir}/%{name}grep
%{_bindir}/%{name}less
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/un%{name}.1*
%{_mandir}/man1/%{name}cat.1*
%{_mandir}/man1/%{name}grep.1*
%{_mandir}/man1/%{name}less.1*
%if 0%{?os2_version}
%{_docdir}/%{name}/*.html
%endif
%license COPYING LICENSE

%files -n lib%{name}
%if !0%{?os2_version}
%{_libdir}/libzstd.so.*
%else
%{_libdir}/zstd*.dll
%endif
%license COPYING LICENSE

%files -n lib%{name}-devel
%{_includedir}/zdict.h
%{_includedir}/zstd.h
%{_includedir}/zstd_errors.h
%{_libdir}/pkgconfig/libzstd.pc
%if !0%{?os2_version}
%{_libdir}/libzstd.so
%else
%{_libdir}/zstd*_dll.a
%{_libdir}/cmake/%{name}/*.cmake
%endif

%files -n lib%{name}-static
%if !0%{?os2_version}
%{_libdir}/libzstd.a
%else
%{_libdir}/zstd.a
%endif

%if !0%{?os2_version}
%ldconfig_scriptlets -n lib%{name}
%endif

%changelog
* Wed Aug 30 2023 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.5.5-1
- First RPM for OS/2 and OS/2 based systems

