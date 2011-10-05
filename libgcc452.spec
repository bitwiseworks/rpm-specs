#
# Temporary libgcc package, until a complete GCC 4.5 bundle is made
#

Summary: Various compilers (C, C++, Objective-C, Java, ...)
Name:    gcc
Version: 4.5.2
Release: 1%{?dist}

# libgcc, libgfortran, libmudflap, libgomp, libstdc++ and crtstuff have
# GCC Runtime Exception.
License: GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions
Group: Development/Languages
URL: http://gcc.gnu.org

Source: libgcc-%{version}.zip

%description
The gcc package contains the GNU Compiler Collection version 4.4.
You'll need this package in order to compile C code.

%package -n libgcc452
Summary: GCC version 4.5 shared support library
Group: System Environment/Libraries

%description -n libgcc452
This package contains GCC shared support library which is needed
e.g. for exception handling support.

%files -n libgcc452
%defattr(-,root,root,-)
%{_libdir}/gcc452.dll

%prep

%setup -q -n "libgcc-%{version}"

%build

%install

rm -rf "%{buildroot}"

mkdir -p "%{buildroot}/%{_libdir}/"
cp -dp gcc452.dll "%{buildroot}/%{_libdir}/"

%clean

rm -rf "%{buildroot}"

%changelog
