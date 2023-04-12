
Summary:  User level USB bus wrapper library
Name:     usbcalls
Epoch:    2
Version:  10.299
Release:  2%{?dist}
License:  unknown
Source:   %{name}.zip

Provides: %{name}.dll

%description
A user level USB bus wrapper library.


%package devel
Summary: Header files for developing apps which will use usbcalls

%description devel
Header files and a library of usbcalls functions, for developing apps
which will use the library.


%prep
%setup -q -c -n %{name}

%build
emximp -o %{name}.a %{name}.lib


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}

cp %{name}.a %{buildroot}%{_libdir}
cp %{name}.lib %{buildroot}%{_libdir}
cp %{name}.h %{buildroot}%{_includedir}


%files

%files devel
%{_libdir}/*.a
%{_libdir}/*.lib
%{_includedir}/*


%changelog
* Wed Apr 12 2023 Silvan Scherrer <silvan.scherrer@aroa.ch> 2:10.299-2
- update with latest header and lib from Lars

* Mon Jan 18 2021 Silvan Scherrer <silvan.scherrer@aroa.ch> 2:10.299-1
- bump epoch
- no dll and sys files anymore, only a virtual package for those

* Wed Apr 16 2014 yd
- first public build.
