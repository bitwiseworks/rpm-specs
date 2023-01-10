# Run the tests by default
%if !0%{?os2_version}
%bcond_without tests
%else
%bcond_with tests
%endif

Name:           libuv
Epoch:          1
Version:        1.44.3
%if !0%{?os2_version}
Release:        %autorelease
%else
Release:        1%{?dist}
%endif
Summary:        Platform layer for node.js

# the licensing breakdown is described in detail in the LICENSE file
License:        MIT and BSD and ISC
URL:            http://libuv.org/
%if !0%{?os2_version}
Source0:        http://dist.libuv.org/dist/v%{version}/libuv-v%{version}.tar.gz
Source2:        %{name}.pc.in
Source3:        libuv.abignore
%else
Vendor:         bww bitwise works GmbH
%scm_source github http://github.com/bitwiseworks/%{name}-os2 v1.x-os2
%endif
%if !0%{?os2_version}
BuildRequires:  autoconf automake libtool
%else
BuildRequires:  cmake
%endif
BuildRequires:  gcc
BuildRequires:  make

# -- Patches -- #

# Disable some tests that fail in the network-free Koji builders
%if !0%{?os2_version}
Patch0001: 0001-Fedora-Skip-tests-that-can-t-run-in-Koji.patch
%endif

%description
libuv is a new platform layer for Node. Its purpose is to abstract IOCP on
Windows and libev on Unix systems. We intend to eventually contain all platform
differences in this library.

%package devel
Summary:        Development libraries for libuv
%if !0%{?os2_version}
Requires:       %{name}%{?_isa} = %{epoch}:%{version}-%{release}
%else
Requires:       %{name} = %{epoch}:%{version}-%{release}
%endif

%description devel
Development libraries for libuv

%package static
Summary:        Platform layer for node.js - static library
%if !0%{?os2_version}
Requires:       %{name}-devel%{?_isa} = %{epoch}:%{version}-%{release}
%else
Requires:       %{name}-devel = %{epoch}:%{version}-%{release}
%endif

%description static
Static library (.a) version of libuv.

%if 0%{?os2_version}
%debug_package
%endif

%prep
%if !0%{?os2_version}
%autosetup -n %{name}-v%{version} -p1
%else
%scm_setup
%endif

%build
%if !0%{?os2_version}
./autogen.sh
%configure --disable-silent-rules
%make_build
%else
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"
export VENDOR="%{vendor}"
%{cmake} -S . -B build
make %{?_smp_mflags} -C build V=1
%endif

%install
%if !0%{?os2_version}
%make_install
%else
%make_install -C build
rm -f %{buildroot}%{_docdir}/libuv/LICENSE
%endif
rm -f %{buildroot}%{_libdir}/libuv.la

%if !0%{?os2_version}
mkdir -p %{buildroot}%{_libdir}/libuv/
install -Dm0644 -t %{buildroot}%{_libdir}/libuv/ %{SOURCE3}
%endif

%check
%if %{with tests}
%make_build check
%endif

%if !0%{?os2_version}
%ldconfig_scriptlets
%endif

%files
%doc README.md AUTHORS CONTRIBUTING.md MAINTAINERS.md SUPPORTED_PLATFORMS.md
%doc ChangeLog
%license LICENSE
%if !0%{?os2_version}
%{_libdir}/%{name}.so.*
%{_libdir}/libuv/libuv.abignore
%else
%{_libdir}/uv1.dll
%endif

%files devel
%if !0%{?os2_version}
%{_libdir}/%{name}.so
%else
%{_libdir}/uv_dll.a
%{_libdir}/cmake/libuv/
%endif
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/uv.h
%{_includedir}/uv/

%files static
%if !0%{?os2_version}
%{_libdir}/%{name}.a
%else
%{_libdir}/pkgconfig/%{name}-static.pc
%{_libdir}/uv_a.a
%endif

%changelog
%if !0%{?os2_version}
%autochangelog
%else
* Tue Jan 10 2023 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.44.3-1
- first rpm version
%endif