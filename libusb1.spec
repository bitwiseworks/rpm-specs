Summary: A library which allows userspace access to USB devices
Name: libusb1
Version: 1.0.16
Release: 1%{?dist}
Source0: http://downloads.sourceforge.net/libusb/libusb-%{version}.tar.gz

License: LGPLv2+
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
URL: http://libusb.wiki.sourceforge.net/Libusb1.0

Patch0: libusb1-os2.patch
Patch1: libusb1-os2-src.patch

%description
This package provides a way for applications to access USB devices. Note that
this library is not compatible with the original libusb-0.1 series.

%package devel
Summary: Development files for libusb
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: %{name}-devel-doc = %{version}-%{release}
Requires: pkgconfig

%description devel
This package contains the header files and libraries needed to develop
applications that use libusb1.

%package devel-doc
Summary: Development files for libusb
Group: Development/Libraries
Requires: %{name}-devel = %{version}-%{release}
BuildArch: noarch

%description devel-doc
This package contains documentation needed to develop applications that
use libusb1.

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
%setup -q -n libusb-%{version}
%patch0 -p1 -b ~os2
%patch1 -p1 -b ~os2

%build
export CONFIG_SHELL="/@unixroot/usr/bin/sh.exe"
%configure --libdir=/%{_lib}
make CFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT/%{_lib}/*.la

mkdir -p %{buildroot}%{_libdir}/pkgconfig
mv %{buildroot}/%{_lib}/pkgconfig/* %{buildroot}%{_libdir}/pkgconfig/
mv %{buildroot}/%{_lib}/*.a %{buildroot}%{_libdir}

cp -p libusb/*.dll %{buildroot}%{_libdir}
cp -p libusb/.libs/usb-*_s.a %{buildroot}%{_libdir}
rm -fr %{buildroot}/%{_lib}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc AUTHORS COPYING README NEWS ChangeLog
%{_libdir}/*.dll

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*-1.0.a
%{_libdir}/pkgconfig/libusb-1.0.pc

%files devel-doc
%defattr(-,root,root)
%doc examples/*.c

%files static
%defattr(-,root,root)
%{_libdir}/*-1.0_s.a

%files debug
%defattr(-,root,root)
%{_libdir}/*.dbg

%changelog
* Wed Apr 16 2014 yd
- first public build.
