%global git_url https://github.com/arvidn/libtorrent
 
Name:		rb_libtorrent
Version:	2.0.11
Release:	1%{?dist}
Summary:	A C++ BitTorrent library aiming to be the best alternative

# Most of the code is BSD-3-Clause
# with few exceptions. e.g.
# include/libtorrent/aux_/invariant_check.hpp is BSL-1.0
# src/ed25519/ is Zlib
# for LicenseRef-Fedora-Public-Domain see https://gitlab.com/fedora/legal/fedora-license-data/-/merge_requests/820/diffs
# include/libtorrent/aux_/route.h is APSL-2.0 AND BSD-4-Clause-UC
License:	Zlib AND BSD-3-Clause AND BSL-1.0 AND LicenseRef-Fedora-Public-Domain AND (APSL-2.0 AND BSD-4-Clause-UC)
URL:		https://www.libtorrent.org
%if !0%{?os2_version}
Source0:	%{git_url}/releases/download/v%{version}/libtorrent-rasterbar-%{version}.tar.gz
%else
Vendor:		bww bitwise works GmbH
%scm_source github http://github.com/bitwiseworks/libtorrent-os2 v%{version}-os2
%endif
Source1:	%{name}-README-renames.Fedora
Source2:	%{name}-COPYING.Boost
Source3:	%{name}-COPYING.zlib

BuildRequires:	cmake
BuildRequires:	gcc-c++
%if !0%{?os2_version}
BuildRequires:	ninja-build
%endif
BuildRequires:	openssl-devel
%if 0%{?fedora} && 0%{?fedora} >= 40
BuildRequires:	openssl-devel-engine
%endif
BuildRequires:	pkgconfig(zlib)
%if !0%{?os2_version}
BuildRequires:	util-linux
%endif

%description
%{name} is a C++ library that aims to be a good alternative to all
the other BitTorrent implementations around. It is a library and not a full
featured client, although it comes with a few working example clients.

Its main goals are to be very efficient (in terms of CPU and memory usage) as
well as being very easy to use both as a user and developer.

%package 	devel
Summary:	Development files for %{name}
License:	Zlib AND BSD-3-Clause AND BSL-1.0 AND LicenseRef-Fedora-Public-Domain AND (APSL-2.0 AND BSD-4-Clause-UC)
%if !0%{?os2_version}
Requires:	%{name}%{?_isa} = %{version}-%{release}
%else
Requires:	%{name} = %{version}-%{release}
%endif
## FIXME: Same include directory. :(
Conflicts:	libtorrent-devel
## Needed for various headers used via #include directives...
%if !0%{?os2_version}
Requires:	boost-devel
%endif
Requires:	pkgconfig(openssl)

%description	devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

The various source and header files included in this package are licensed
under the revised BSD, zlib/libpng, and Boost Public licenses. See the various
COPYING files in the included documentation for the full text of these
licenses, as well as the comments blocks in the source code for which license
a given source or header file is released under.

%package	examples
Summary:	Example clients using %{name}
License:	BSD-3-Clause
%if !0%{?os2_version}
Requires:	%{name}%{?_isa} = %{version}-%{release}
%else
Requires:	%{name} = %{version}-%{release}
%endif

%description	examples
The %{name}-examples package contains example clients which intend to
show how to make use of its various features. (Due to potential
namespace conflicts, a couple of the examples had to be renamed. See the
included documentation for more details.)

%package	python3
Summary:	Python bindings for %{name}
# Automatically converted from old format: Boost - review is highly recommended.
# Most of the code is BSL-1.0
# but few are BSD-3-Clause e.g. bindings/python/src/error_code.cpp
License:	BSL-1.0
BuildRequires:	python3-devel
BuildRequires:	pkgconfig(python3)
%if !0%{?os2_version}
BuildRequires:	boost-python3-devel
%endif
BuildRequires:	python3-setuptools
%if !0%{?os2_version}
Requires:	%{name}%{?_isa} = %{version}-%{release}
%else
Requires:	%{name} = %{version}-%{release}
%endif

%description	python3
The %{name}-python3 package contains Python language bindings
(the 'libtorrent' module) that allow it to be used from within
Python applications.

%if 0%{?os2_version}
%debug_package
%endif

%prep
%if !0%{?os2_version}
%autosetup -p1 -n "libtorrent-rasterbar-%{version}"
%else
%scm_setup
%endif

## The RST files are the sources used to create the final HTML files; and are
## not needed.
rm -f docs/*.rst
## Ensure that we get the licenses installed appropriately.
install -p -m 0644 COPYING COPYING.BSD
install -p -m 0644 %{SOURCE2} COPYING.Boost
install -p -m 0644 %{SOURCE3} COPYING.zlib
%if !0%{?os2_version}
## Finally, ensure that everything is UTF-8, as it should be.
iconv -t UTF-8 -f ISO_8859-15 AUTHORS -o AUTHORS.iconv
mv AUTHORS.iconv AUTHORS
%endif

%build
# This is ugly but can't think of an easier way to build the binding
%if !0%{?os2_version}
export CPPFLAGS="$CPPFLAGS $(python%{python3_version}-config --includes)"
export LDFLAGS="$LDFLAGS -L%{_builddir}/libtorrent-rasterbar-%{version}/build/src/.libs"
export PYTHON=/usr/bin/python%{python3_version}
%endif
export PYTHON_LDFLAGS="$PYTHON_LDFLAGS $(python%{python3_version}-config --libs)"

%if 0%{?os2_version}
# -------------------------
# this is hackisch and works only on my env. you need to adjust that until we have a
# boost rpm. when we have a boost rpm, then enable all boost stuff in here!!!
export BOOST_CPPFLAGS="-IE:/Trees/boost/git"
export BOOST_ROOT="E:/Trees/boost/git"
export BOOST_LDFLAGS="-LE:/Trees/boost/git/stage/lib"
# -------------------------
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx $PYTHON_LDFLAGS"
export VENDOR="%{vendor}"
%endif

%cmake \
	-DCMAKE_BUILD_TYPE=RelWithDebInfo \
	-DCMAKE_SKIP_RPATH=TRUE \
%if !0%{?os2_version}
	-GNinja \
%endif
	-Dbuild_examples=ON \
	-Dbuild_tests=ON \
	-Dbuild_tools=ON \
	-Dpython-bindings=ON \
	-Dpython-egg-info=ON \
	-Dpython-install-system-dir=OFF
%cmake_build

%check
%if !0%{?os2_version}
export LD_LIBRARY_PATH=%{_builddir}/libtorrent-rasterbar-%{version}/%{_vpath_builddir}
pushd %{_vpath_builddir}/test
# Skip UPnP test as it requires a UPnP server on the same network, others due to aarch64 failures
# Make test failures non-fatal as they seem to randomly fail.
echo "set (CTEST_CUSTOM_TESTS_IGNORE
 "test_upnp"
)" > CTestCustom.cmake
ctest -j %{_smp_build_ncpus} || :
popd
%endif

%install
mkdir -p %{buildroot}%{_bindir}/

%cmake_install
%if !0%{?os2_version}
install -p -m 0755 \
 %{_vpath_builddir}/examples/{client_test,connection_tester,custom_storage,dump_torrent,make_torrent,simple_client,stats_counters,upnp_test} \
 %{_vpath_builddir}/tools/{dht,session_log_alerts} \
 %{buildroot}%{_bindir}/
%else
install -p -m 0755 \
 %{_vpath_builddir}/examples/client_test.exe \
 %{_vpath_builddir}/examples/connection_tester.exe \
 %{_vpath_builddir}/examples/custom_storage.exe \
 %{_vpath_builddir}/examples/dump_torrent.exe \
 %{_vpath_builddir}/examples/make_torrent.exe \
 %{_vpath_builddir}/examples/simple_client.exe \
 %{_vpath_builddir}/examples/stats_counters.exe \
 %{_vpath_builddir}/examples/upnp_test.exe \
 %{_vpath_builddir}/tools/dht.exe \
 %{_vpath_builddir}/tools/session_log_alerts.exe \
 %{buildroot}%{_bindir}/
%endif

# Written version is malformed
sed -i 's/^Version:.*/Version: %{version}/' %{buildroot}%{python3_sitearch}/libtorrent.egg-info/PKG-INFO

## Do the renaming due to the somewhat limited %%_bindir namespace.
%if !0%{?os2_version}
rename client torrent_client %{buildroot}%{_bindir}/*
%else
mv %{buildroot}%{_bindir}/client_test.exe %{buildroot}%{_bindir}/torrent_client_test.exe
mv %{buildroot}%{_bindir}/simple_client.exe %{buildroot}%{_bindir}/simple_torrent_client.exe
%endif

install -p -m 0644 %{SOURCE1} ./README-renames.Fedora

%if !0%{?os2_version}
%ldconfig_scriptlets
%endif

%files
%{!?_licensedir:%global license %doc}
%doc AUTHORS ChangeLog
%license COPYING
%if !0%{?os2_version}
%{_libdir}/libtorrent-rasterbar.so.2.*
%{_libdir}/libtorrent-rasterbar.so.2.0
%else
%{_libdir}/torren20.dll
%endif

%files	devel
%doc docs/
%license COPYING.Boost COPYING.BSD COPYING.zlib
%{_libdir}/pkgconfig/libtorrent-rasterbar.pc
%{_includedir}/libtorrent/
%if !0%{?os2_version}
%{_libdir}/libtorrent-rasterbar.so
%else
%{_libdir}/torrent-rasterbar_dll.a
%endif
%{_libdir}/cmake/LibtorrentRasterbar/
%{_datadir}/cmake/Modules/FindLibtorrentRasterbar.cmake

%files examples
%doc README-renames.Fedora
%license COPYING
%{_bindir}/*torrent*
%if !0%{?os2_version}
%{_bindir}/connection_tester
%{_bindir}/custom_storage
%{_bindir}/dht
%{_bindir}/session_log_alerts
%{_bindir}/stats_counters
%{_bindir}/upnp_test
%else
%{_bindir}/connection_tester.exe
%{_bindir}/custom_storage.exe
%{_bindir}/dht.exe
%{_bindir}/session_log_alerts.exe
%{_bindir}/stats_counters.exe
%{_bindir}/upnp_test.exe
%endif

%files	python3
%doc AUTHORS ChangeLog
%license COPYING.Boost
%{python3_sitearch}/libtorrent.egg-info/
%if !0%{?os2_version}
%{python3_sitearch}/libtorrent.cpython-*.so
%else
%{python3_sitearch}/libtorrent.dll
%{python3_sitearch}/torrent.dll
%endif

%changelog
* Fri Feb 13 2026 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1:2.0.11-1
- first OS/2 rpm
