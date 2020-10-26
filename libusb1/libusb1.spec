Summary:        A library which allows userspace access to USB devices
Name:           libusb1
Version:        1.0.21
Release:        2%{?dist}

License:        LGPLv2+
Group:          System Environment/Libraries
URL:            http://libusb.info/

Vendor:         bww bitwise works GmbH
%scm_source github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2-2

BuildRequires:  usbcalls-devel
BuildRequires:  doxygen libtool
Requires:       usbcalls

%description
This package provides a way for applications to access USB devices. Note that
this library is not compatible with the original libusb-0.1 series.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-devel-doc = %{version}-%{release}
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        devel-doc
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}-devel = %{version}-%{release}
BuildArch:      noarch

%description    devel-doc
This package contains API documentation for %{name}.

%legacy_runtime_packages

%debug_package


%prep
%scm_setup

autoreconf -ifv


%build
export LDFLAGS="-Zhigh-mem -Zomf"
export LIBS="-lcx"
export VENDOR="%{vendor}"

%configure --disable-static
make

cd doc
make docs
cd ..


%install
%make_install
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la


%clean
rm -rf $RPM_BUILD_ROOT


#post -p /sbin/ldconfig
#postun -p /sbin/ldconfig


%files
%defattr(-,root,root)
%license COPYING
%doc AUTHORS README ChangeLog
%{_libdir}/*.dll
%exclude %{_libdir}/libusb10.dll


%files devel
%defattr(-,root,root)
%{_includedir}/libusb-1.0
%{_libdir}/*_dll.a
%{_libdir}/pkgconfig/libusb-1.0.pc


%files devel-doc
%defattr(-,root,root)
%doc doc/html examples/*.c


%changelog
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
