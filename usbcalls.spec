#define svn_url     F:/rd/usb/repos/resmgr/trunk/usbcalls
%define svn_url     http://svn.netlabs.org/repos/usb/resmgr/trunk/usbcalls
%define svn_rev     1238

Summary: User level USB bus wrapper library
Name: usbcalls
Version: 20150212
Release: 1%{?dist}
License: unknown
Group: Development/Libraries

Source: %{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip


%description
A user level USB bus wrapper library.

%package devel
Summary: Header files developing apps which will use usbcalls
Group: Development/Libraries

%description devel
Header files and a library of usbcalls functions, for developing apps
which will use the library.

%package debug
Summary: HLL debug data for exception handling support.

%description debug
HLL debug data for exception handling support.

%prep
%if %{?svn_rev:%(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')}%{!?svn_rev):0}
%setup -q
%else
%setup -n "%{name}-%{version}" -Tc
svn export %{?svn_rev:-r %{svn_rev}} %{svn_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip" "%{name}-%{version}")
%endif


%build
find . -name "*.exe" -exec rm -f {} ';'
find . -name "*.dll" -exec rm -f {} ';'
sed -i 's/USB devices/USB devices %{version}-%{release}/' usbcalls-gcc.def
gcc %{optflags} -Zomf -Zhigh-mem -Zdll usbcalls.c usbrexx.c usbcalls-gcc.def
emximp -o usbcalls.lib usbcalls-gcc.def
emximp -o usbcalls.a usbcalls-gcc.def

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}

cp usbcalls.dll %{buildroot}%{_libdir}
cp usbcalls.a %{buildroot}%{_libdir}
cp usbcalls.lib %{buildroot}%{_libdir}
cp usbcalls.h %{buildroot}%{_includedir}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/*.dll

%files devel
%defattr(-,root,root)
%{_libdir}/*.a
%{_libdir}/*.lib
%{_includedir}/*
%doc test
%doc samples

%files debug
%defattr(-,root,root)
%{_libdir}/*.dbg

%changelog
* Wed Apr 16 2014 yd
- first public build.
