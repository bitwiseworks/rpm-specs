#
# Temporary libgcc package, until a complete GCC 4.5 bundle is made
#

Summary: Various compilers (C, C++, Objective-C, Java, ...)
Name:    gcc
Version: 4.5.2
Release: 2%{?dist}

# libgcc, libgfortran, libmudflap, libgomp, libstdc++ and crtstuff have
# GCC Runtime Exception.
License: GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions
Group: Development/Languages
URL: http://gcc.gnu.org

Source: libgcc4core.zip

%description
The gcc package contains the GNU Compiler Collection version 4.4.
You'll need this package in order to compile C code.

%package -n libgcc432
Summary: GCC version 4.32 shared support library
Group: System Environment/Libraries

%description -n libgcc432
This package contains GCC shared support library which is needed
e.g. for exception handling support.

%package -n libgcc433
Summary: GCC version 4.33 shared support library
Group: System Environment/Libraries

%description -n libgcc433
This package contains GCC shared support library which is needed
e.g. for exception handling support.

%package -n libgcc434
Summary: GCC version 4.34 shared support library
Group: System Environment/Libraries

%description -n libgcc434
This package contains GCC shared support library which is needed
e.g. for exception handling support.

%package -n libgcc440
Summary: GCC version 4.40 shared support library
Group: System Environment/Libraries

%description -n libgcc440
This package contains GCC shared support library which is needed
e.g. for exception handling support.

%package -n libgcc441
Summary: GCC version 4.41 shared support library
Group: System Environment/Libraries

%description -n libgcc441
This package contains GCC shared support library which is needed
e.g. for exception handling support.

%package -n libgcc442
Summary: GCC version 4.42 shared support library
Group: System Environment/Libraries

%description -n libgcc442
This package contains GCC shared support library which is needed
e.g. for exception handling support.

%package -n libgcc444
Summary: GCC version 4.44 shared support library
Group: System Environment/Libraries

%description -n libgcc444
This package contains GCC shared support library which is needed
e.g. for exception handling support.

%package -n libgcc445
Summary: GCC version 4.45 shared support library
Group: System Environment/Libraries

%description -n libgcc445
This package contains GCC shared support library which is needed
e.g. for exception handling support.

%package -n libgcc452
Summary: GCC version 4.5 shared support library
Group: System Environment/Libraries

%description -n libgcc452
This package contains GCC shared support library which is needed
e.g. for exception handling support.

%package -n libgcc453
Summary: GCC version 4.53 shared support library
Group: System Environment/Libraries

%description -n libgcc453
This package contains GCC shared support library which is needed
e.g. for exception handling support.

%prep

%setup -q -c -n "libgcc-%{version}"

%build

%install

rm -rf "%{buildroot}"

mkdir -p "%{buildroot}/%{_libdir}/"
cp -dp *.dll "%{buildroot}/%{_libdir}/"

%clean
rm -rf "%{buildroot}"


%files -n libgcc432
%defattr(-,root,root,-)
%{_libdir}/gcc432.dll
%doc COPYING*

%files -n libgcc433
%defattr(-,root,root,-)
%{_libdir}/gcc433.dll
%doc COPYING*

%files -n libgcc434
%defattr(-,root,root,-)
%{_libdir}/gcc434.dll
%doc COPYING*

%files -n libgcc440
%defattr(-,root,root,-)
%{_libdir}/gcc440.dll
%doc COPYING*

%files -n libgcc441
%defattr(-,root,root,-)
%{_libdir}/gcc441.dll
%doc COPYING*

%files -n libgcc442
%defattr(-,root,root,-)
%{_libdir}/gcc442.dll
%doc COPYING*

%files -n libgcc444
%defattr(-,root,root,-)
%{_libdir}/gcc444.dll
%doc COPYING*

%files -n libgcc445
%defattr(-,root,root,-)
%{_libdir}/gcc445.dll
%doc COPYING*

%files -n libgcc452
%defattr(-,root,root,-)
%{_libdir}/gcc452.dll
%doc COPYING*

%files -n libgcc453
%defattr(-,root,root,-)
%{_libdir}/gcc453.dll
%doc COPYING*

%changelog
