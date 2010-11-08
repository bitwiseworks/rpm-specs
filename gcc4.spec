%global gcc_version 4.4.4

Summary: Various compilers (C, C++, Objective-C, Java, ...)
Name: gcc
Version: %{gcc_version}
Release: 1
# libgcc, libgfortran, libmudflap, libgomp, libstdc++ and crtstuff have
# GCC Runtime Exception.
License: GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions
Group: Development/Languages
Source0: gcc-%{version}.zip
URL: http://gcc.gnu.org

BuildRoot: %{_tmppath}/%{name}-%{version}-root-%(%{__id_u} -n)

Obsoletes: gcc < %{gcc_version}
Requires: libgcc444 = %{gcc_version}
Requires: libc-devel >= 0.6.3

%description
The gcc package contains the GNU Compiler Collection version 4.4.
You'll need this package in order to compile C code.

%package -n libgcc444
Summary: GCC version 4.4 shared support library
Group: System Environment/Libraries
Autoreq: false

%description -n libgcc444
This package contains GCC shared support library which is needed
e.g. for exception handling support.

%prep
%setup -q -n gcc-%{version}

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p %{buildroot}%{_usr}
cp -r "*" %{buildroot}%{_usr}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_usr}/bin
%{_usr}/include
%{_libdir}/*.*a
%{_libdir}/*.spec
%{_libdir}/gcc/*
%{_usr}/libexec
%{_usr}/man
%{_usr}/share


%files -n libgcc444
%defattr(-,root,root,-)
%{_libdir}/gcc444.dll
%doc %{_datadir}/doc/*

%changelog
