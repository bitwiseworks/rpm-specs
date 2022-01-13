Name:           hidapi
Version:        0.11.2
Release:        1%{?dist}
Summary:        Library for communicating with USB and Bluetooth HID devices

License:        GPLv3 or BSD
URL:            https://github.com/libusb/hidapi

%if !0%{?os2_version}
Source0:        https://github.com/libusb/hidapi/archive/%{name}-%{version}.tar.gz
%else
Vendor:         bww bitwise works GmbH
%scm_source     github https://github.com/bitwiseworks/%{name}-os2 %{name}-%{version}-os2
%endif

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: gcc
BuildRequires: libtool
%if !0%{?os2_version}
BuildRequires: libudev-devel
%endif
BuildRequires: libusb1-devel
BuildRequires: m4
BuildRequires: make

%description
HIDAPI is a multi-platform library which allows an application to interface
with USB and Bluetooth HID-class devices on Windows, Linux, FreeBSD and Mac OS
X.  On Linux, either the hidraw or the libusb back-end can be used. There are
trade-offs and the functionality supported is slightly different.

%package devel
Summary: Development files for hidapi
Requires: %{name} = %{version}-%{release}

%description -n hidapi-devel
This package contains development files for hidapi which provides access to
USB and Bluetooth HID-class devices.

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
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
# Set BUILDLEVEL to be embedded to all DLLs built with Libtool.
export LT_BUILDLEVEL="@#%{vendor}:%{version}-%{release}#@##1## `LANG=C date +'%%d %%b %%Y %%H:%%M:%%S'`     `uname -n`::::0::"
%endif
autoreconf -vif
%configure --disable-testgui --disable-static
make %{?_smp_mflags} V=1

%install
make install DESTDIR=%{buildroot}

rm -f %{buildroot}%{_libdir}/*.la
rm -rf %{buildroot}%{_defaultdocdir}/%{name}

%if !0%{?os2_version}
%ldconfig_scriptlets
%endif

%files
%doc AUTHORS.txt README.md LICENSE*.txt
%if !0%{?os2_version}
%{_libdir}/libhidapi-*.so.*
%else
%{_libdir}/hidapi*.dll
%endif

%files devel
%{_includedir}/hidapi
%if !0%{?os2_version}
%{_libdir}/libhidapi-hidraw.so
%{_libdir}/libhidapi-libusb.so
%{_libdir}/pkgconfig/hidapi-hidraw.pc
%{_libdir}/pkgconfig/hidapi-libusb.pc
%else
%{_libdir}/hidapi*_dll.a
%{_libdir}/pkgconfig/hidapi.pc
%endif

%changelog
* Tue Jan 13 2022 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.11.2-1
- don't use iconv, as we don't have WCHAR_T iconv functions (Dave Yeo)
- update to version 0.11.2

* Wed Jan 12 2022 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.11.0-1
- first OS/2 rpm
