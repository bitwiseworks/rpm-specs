Name:       libusb-compat
Version:    0.1.5
Release:    1%{?dist}
Summary:    libusb-compat

Group:      System Environment/libraries
License:    GPLv2+
Url:        http://libusb.sourceforge.net
Source:     http://downloads.sourceforge.net/libusb/%{name}-%{version}.tar.bz2
Patch0:     libusb-compat-os2.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-build
BuildRequires:  libusb1-devel

%description
The libusb-compat package aims to look, feel and behave exactly like libusb-0.1. It is a compatibility layer needed by packages that have not been upgraded to the libusb-1.0 API.

%package devel
Summary: Development files for libusb-compat
Group: Development/Libraries

%description devel
This package contains the header files and libraries needed to develop
applications that use libusb-compat.

%package static
Summary: Static development files for libusb
Group: Development/Libraries
Requires: %{name}-devel = %{version}-%{release}

%description static
This package contains static libraries to develop applications that use libusb1.

%package debug
Summary: HLL debug data for exception handling support.

%description debug
HLL debug data for exception handling support.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1 -b ~os2

%build
export CONFIG_SHELL="/@unixroot/usr/bin/sh.exe"
%configure
make CFLAGS="$RPM_OPT_FLAGS" %{?_smp_mflags}

%check

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

cp -p libusb/*.dll %{buildroot}%{_libdir}
cp -p libusb/.libs/usb_s.a %{buildroot}%{_libdir}
rm %{buildroot}%{_libdir}/*.la

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_libdir}/libusbc.dll

%files devel
%defattr(-,root,root,-)
%{_bindir}/libusb-config
%{_includedir}/usb.h
%{_libdir}/usb.a
%{_libdir}/pkgconfig/libusb.pc

%files static
%defattr(-,root,root)
%{_libdir}/usb_s.a

%files debug
%defattr(-,root,root)
%{_libdir}/*.dbg

%changelog
* Wed Apr 16 2014 yd
- first public build.
