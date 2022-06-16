Name:           libuvc
Version:        0.0.6
Release:        5%{?dist}
Summary:        A cross-platform library for USB video devices

License:        GPLv3 or BSD
URL:            https://github.com/libuvc/libuvc

%if !0%{?os2_version}
Source0:        https://github.com/libuvc/libuvc/archive/%{name}-%{version}.tar.gz
%else
Vendor:         bww bitwise works GmbH
%scm_source     github https://github.com/bitwiseworks/%{name}-os2 v%{version}-os2-4
%global __cmake_in_source_build 1
%endif

BuildRequires: cmake
BuildRequires: gcc
BuildRequires: libusb1-devel
BuildRequires: libjpeg-devel
BuildRequires: make

%description
`libuvc` is a cross-platform library for USB video devices, built atop `libusb`.
It enables fine-grained control over USB video devices exporting the standard
USB Video Class(UVC) interface, enabling developers to write drivers for
previously unsupported devices, or just access UVC devices in a generic fashion.

%package devel
Summary: Development files for libuvc
Requires: %{name} = %{version}-%{release}

%description devel
This package contains development files for libuvc

%if 0%{?os2_version}
%debug_package
%endif

%prep
%if !0%{?os2_version}
%autosetup -n %{name}-%{name}-%{version}
%else
%scm_setup
%endif

%build
%if 0%{?os2_version}
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx -lpthread"
export VENDOR="%{vendor}"
%endif
%{cmake} \
         -DCMAKE_BUILD_TARGET:STRING=Shared \
         .
%cmake_build

%install
%cmake_install

%files
%doc README.md LICENSE.txt
%if !0%{?os2_version}
%{_libdir}/libuvc-*.so.*
%else
%{_libdir}/uvc*.dll
%endif

%files devel
%{_includedir}/libuvc
%if !0%{?os2_version}
%{_libdir}/libuvc.so
%else
%{_libdir}/uvc*_dll.a
%endif
%{_libdir}/pkgconfig/libuvc.pc
%{_libdir}/cmake/libuvc/

%changelog
* Thu Jun 16 2022 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.0.6-4
- some more fixes/changes done by Lars Erdmann
- merged with latest upstream sources

* Thu Apr 07 2022 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.0.6-4
- some more fixes/changes done by Lars Erdmann

* Mon Feb 21 2022 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.0.6-3
- some more fixes/changes done by Lars Erdmann

* Mon Jan 24 2022 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.0.6-2
- fix example.c (Lars Erdmann)

* Wed Jan 12 2022 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.0.6-1
- first OS/2 rpm
