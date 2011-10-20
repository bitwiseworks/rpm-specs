%global gcc_version 3.3.5

Summary: Various compilers (C, C++, Objective-C, Java, ...)
Name: gcc
Version: %{gcc_version}
Release: 6%{?dist}
# libgcc, libgfortran, libmudflap, libgomp, libstdc++ and crtstuff have
# GCC Runtime Exception.
License: GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions
Group: Development/Languages
Source0: gcc-%{version}.zip
URL: http://gcc.gnu.org

BuildRoot: %{_tmppath}/%{name}-%{version}-root-%(%{__id_u} -n)

Requires: libgcc335 = %{gcc_version}
Requires: libc-devel >= 0.6.3
Requires: binutils

%description
The gcc package contains the GNU Compiler Collection version 4.4.
You'll need this package in order to compile C code.

%package -n libgcc335
Summary: GCC version 3.3 shared support library
Group: System Environment/Libraries
Autoreq: false

%description -n libgcc335
This package contains GCC shared support library which is needed
e.g. for exception handling support.

%prep
%setup -q -c


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_usr}/man
mkdir -p %{buildroot}%{_usr}/share
cp -p -r "usr/bin/*" %{buildroot}%{_bindir}
cp -p -r "usr/include/*" %{buildroot}%{_includedir}
cp -p -r "usr/lib/*" %{buildroot}%{_libdir}
cp -p -r "usr/man/*" %{buildroot}%{_usr}/man
cp -p -r "usr/share/*" %{buildroot}%{_usr}/share

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_usr}/bin
%{_usr}/include
%{_libdir}/*.*a
%{_libdir}/gcc-lib/*
%{_usr}/man
%{_usr}/share


%files -n libgcc335
%defattr(-,root,root,-)
%{_libdir}/gcc335.dll
%doc usr/doc/gcc-3.3.5/*


%changelog
* Tue Sep 04 2011 yd
- update to csd4
