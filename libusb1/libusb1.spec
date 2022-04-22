Summary:        Library for accessing USB devices
Name:           libusb1
Version:        1.0.24
Release:        5%{?dist}
%if !0%{?os2_version}
Source0:        https://github.com/libusb/libusb/releases/download/v%{version}/libusb-%{version}.tar.bz2
%else
Vendor:         bww bitwise works GmbH
%scm_source     github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2-4
%endif
License:        LGPLv2+
URL:            http://libusb.info
%if !0%{?os2_version}
BuildRequires:  systemd-devel doxygen libtool
%else
BuildRequires:  doxygen libtool
BuildRequires:  usbcalls-devel
%endif
BuildRequires:  make
BuildRequires:  gcc
%if !0%{?os2_version}
# libusbx was removed in F34
Provides:       libusbx = %{version}-%{release}
Obsoletes:      libusbx < %{version}-%{release}

Patch001:       0001-linux_usbfs-Accept-sysfs-attributes-not-terminated-w.patch
Patch002:       0001-linux_usbfs-Fix-parsing-of-descriptors-for-multi-con.patch
Patch003:       0002-linux_usbfs-Gracefully-handle-buggy-devices-with-a-c.patch
%endif

%description
This package provides a way for applications to access USB devices.

libusb is a library for USB device access from Linux, OS/2, macOS,
Windows, OpenBSD/NetBSD, Haiku and Solaris userspace.

libusb is abstracted internally in such a way that it can hopefully
be ported to other operating systems.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
%if !0%{?os2_version}
Provides:       libusbx-devel = %{version}-%{release}
Obsoletes:      libusbx-devel < %{version}-%{release}
%endif

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package devel-doc
Summary:        Development files for %{name}
Requires:       libusb1-devel = %{version}-%{release}
%if !0%{?os2_version}
Provides:       libusbx-devel-doc = %{version}-%{release}
Obsoletes:      libusbx-devel-doc < %{version}-%{release}
%endif
BuildArch:      noarch

%description devel-doc
This package contains API documentation for %{name}.


%package        tests-examples
Summary:        Tests and examples for %{name}
# The fxload example is GPLv2+, the rest is LGPLv2+, like libusb itself.
License:        LGPLv2+ and GPLv2+
Requires:       %{name} = %{version}-%{release}
%if 0%{?os2_version}
Provides:       libusbx-tests-examples = %{version}-%{release}
Obsoletes:      libusbx-tests-examples < %{version}-%{release}
%endif

%description tests-examples
This package contains tests and examples for %{name}.


%if 0%{?os2_version}
%legacy_runtime_packages

%debug_package
%endif


%prep
%if !0%{?os2_version}
%autosetup -p1 -n libusb-%{version}
%else
%scm_setup
%endif
chmod -x examples/*.c
mkdir -p m4
%if 0%{?os2_version}
autoreconf -fvi
%endif


%build
%if 0%{?os2_version}
export LDFLAGS="-Zhigh-mem -Zomf"
export LIBS="-lcx"
export VENDOR="%{vendor}"
%endif
%configure --disable-static --enable-examples-build
%if !0%{?os2_version}
%{make_build}
pushd doc
%else
make
cd doc
%endif
make docs
%if !0%{?os2_version}
popd
pushd tests
%else
cd ..
cd tests
%endif
make
%if !0%{?os2_version}
popd
%else
cd ..
%endif


%install
%{make_install}
mkdir -p $RPM_BUILD_ROOT%{_bindir}
%if !0%{?os2_version}
install -m 755 tests/.libs/stress $RPM_BUILD_ROOT%{_bindir}/libusb-test-stress
install -m 755 examples/.libs/testlibusb \
    $RPM_BUILD_ROOT%{_bindir}/libusb-test-libusb
# Some examples are very device-specific / require specific hw and miss --help
# So we only install a subset of more generic / useful examples
for i in fxload listdevs xusb; do
    install -m 755 examples/.libs/$i \
        $RPM_BUILD_ROOT%{_bindir}/libusb-example-$i
done
%else
install -m 755 tests/stress.exe $RPM_BUILD_ROOT%{_bindir}/libusb-test-stress.exe
install -m 755 examples/testlibusb.exe \
    $RPM_BUILD_ROOT%{_bindir}/libusb-test-libusb.exe
# Some examples are very device-specific / require specific hw and miss --help
# So we only install a subset of more generic / useful examples
for i in fxload.exe listdevs.exe xusb.exe; do
    install -m 755 examples/$i \
        $RPM_BUILD_ROOT%{_bindir}/libusb-example-$i
done
%endif
rm $RPM_BUILD_ROOT%{_libdir}/*.la


%check
%if !0%{?os2_version}
LD_LIBRARY_PATH=libusb/.libs ldd $RPM_BUILD_ROOT%{_bindir}/libusb-test-stress
LD_LIBRARY_PATH=libusb/.libs $RPM_BUILD_ROOT%{_bindir}/libusb-test-stress
LD_LIBRARY_PATH=libusb/.libs $RPM_BUILD_ROOT%{_bindir}/libusb-test-libusb
LD_LIBRARY_PATH=libusb/.libs $RPM_BUILD_ROOT%{_bindir}/libusb-example-listdevs
%endif


%if !0%{?os2_version}
%ldconfig_scriptlets
%endif


%files
%license COPYING
%doc AUTHORS README ChangeLog
%if !0%{?os2_version}
%{_libdir}/*.so.*
%else
%{_libdir}/*.dll
%exclude %{_libdir}/libusb10.dll
%endif

%files devel
%{_includedir}/libusb-1.0
%if !0%{?os2_version}
%{_libdir}/*.so
%else
%{_libdir}/*_dll.a
%endif
%{_libdir}/pkgconfig/libusb-1.0.pc

%files devel-doc
%doc doc/api-1.0 examples/*.c

%files tests-examples
%if !0%{?os2_version}
%{_bindir}/libusb-example-fxload
%{_bindir}/libusb-example-listdevs
%{_bindir}/libusb-example-xusb
%{_bindir}/libusb-test-stress
%{_bindir}/libusb-test-libusb
%else
%{_bindir}/libusb-example-fxload.exe
%{_bindir}/libusb-example-listdevs.exe
%{_bindir}/libusb-example-xusb.exe
%{_bindir}/libusb-test-stress.exe
%{_bindir}/libusb-test-libusb.exe
%endif


%changelog
* Fri Apr 22 2022 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.0.24-5
- some more fixes/changes done by Lars Erdmann

* Thu Apr 07 2022 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.0.24-4
- some more fixes/changes done by Lars Erdmann

* Mon Feb 21 2022 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.0.24-3
- some more fixes/changes done by Lars Erdmann

* Mon Jan 24 2022 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.0.24-2
- reduce number of worker threads (Lars Erdmann)

* Wed Jan 12 2022 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.0.24-1
- update to version 1.0.24
- implement iso transfer (Lars Erdmann)
- fix a lot issues (Lars Erdmann)
- resync with fedora spec

* Mon Dec 23 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.0.21-2
- remove unused poll implementation
- finetune errorhandling
- handle the case when we opened the device already, this is to mimik the nix
  behaviour better (libsane testcases failed because of that)

* Mon Dec 12 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.0.21-1
- update to version 1.0.21
- add the documention
- use the new scm_source and scm_setup macros

* Wed Jun 15 2016 yd <yd@os2power.com> 1.0.16-2
- added requirements.
- added debug package.

* Wed Apr 16 2014 yd
- first public build.
