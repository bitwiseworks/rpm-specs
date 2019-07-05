
Summary: User level USB bus wrapper library
Name: usbcalls
Version: 20140416
Release: 1%{?dist}
License: unknown
Group: Development/Libraries
Source: usbcalls.zip


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
%setup -q -c -n usbcalls


%build
BldLevelInf.cmd -Nnetlabs -V%{version} -DUsbcalls_wrapper usbcalls-gcc.def
gcc %{optflags} -Zomf -Zhigh-mem -Zdll -DOS2EMX_PLAIN_CHAR usbcalls.c usbcalls-gcc.def
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
