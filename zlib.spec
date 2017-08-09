
Summary: The compression and decompression library
Name: zlib
Version: 1.2.11
Release: 2%{?dist}
License: zlib and Boost
Group: System Environment/Libraries
URL: http://www.zlib.net
Vendor:  bww bitwise works GmbH
%scm_source  svn http://svn.netlabs.org/repos/ports/zlib/trunk 1948

# DEF files to create forwarders for the legacy package
Source10:       z.def

BuildRequires: automake, autoconf, libtool

%description
Zlib is a general-purpose, patent-free, lossless data compression
library which is used by many different programs.

%package devel
Summary: Header files and libraries for Zlib development
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
The zlib-devel package contains the header files and libraries needed
to develop programs that use the zlib compression and decompression
library.

%package static
Summary: Static libraries for Zlib development
Group: Development/Libraries
Requires: %{name}-devel = %{version}-%{release}

%description static
The zlib-static package includes static libraries needed
to develop programs that use the zlib compression and
decompression library.

%package -n minizip
Summary: Library for manipulation with .zip archives
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}

%description -n minizip
Minizip is a library for manipulation with files from .zip archives.

%package -n minizip-devel
Summary: Development files for the minizip library
Group: Development/Libraries
Requires: minizip = %{version}-%{release}
Requires: %{name}-devel = %{version}-%{release}
Requires: pkgconfig

%description -n minizip-devel
This package contains the libraries and header files needed for
developing applications which use minizip.

%debug_package

%prep
%scm_setup

# Prepare forwarder DLLs.
for m in %{SOURCE10}; do
  cp ${m} .
done

%build
export CFLAGS="$RPM_OPT_FLAGS"
export LDFLAGS="$LDFLAGS -Zomf -Zhigh-mem -lcx"
export VENDOR="%{vendor}"
./configure --libdir=%{_libdir} --includedir=%{_includedir} --prefix=%{_prefix}
make %{?_smp_mflags}

cd contrib/minizip
autoreconf -fvi
%configure --enable-static=no
make %{?_smp_mflags}

%check
make test

%install
make install DESTDIR=$RPM_BUILD_ROOT

cd contrib/minizip
make install DESTDIR=$RPM_BUILD_ROOT
# we need to get back to root, as else the debugfile list is created at
# the wrong location
cd ..
cd ..

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

# Generate & install forwarder DLLs.
gcc -Zomf -Zdll -nostdlib z.def -l$RPM_BUILD_ROOT/%{_libdir}/z1.dll -lend -o $RPM_BUILD_ROOT/%{_libdir}/z.dll

#post -p /sbin/ldconfig

#postun -p /sbin/ldconfig

#post -n minizip -p /sbin/ldconfig

#postun -n minizip -p /sbin/ldconfig

%files
%{!?_licensedir:%global license %%doc}
%license README
%doc ChangeLog FAQ
%{_libdir}/z*.dll

%files devel
%{!?_licensedir:%global license %%doc}
%license README
%doc doc/algorithm.txt test/example.c
%{_libdir}/libz_dll.a
%{_libdir}/pkgconfig/zlib.pc
%{_includedir}/zlib.h
%{_includedir}/zconf.h
%{_mandir}/man3/zlib.3*

%files static
%{!?_licensedir:%global license %%doc}
%license README
%{_libdir}/libz.a

%files -n minizip
%doc contrib/minizip/MiniZip64_info.txt contrib/minizip/MiniZip64_Changes.txt
%{_libdir}/minizip*.dll

%files -n minizip-devel
%dir %{_includedir}/minizip
%{_includedir}/minizip/*.h
%{_libdir}/minizip*_dll.a
%{_libdir}/pkgconfig/minizip.pc

%changelog
* Wed Aug 09 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.2.11-2
- use new scm_source and scm_setup macro

* Tue Jan 24 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.2.11-1
- update to version 1.2.11

* Thu Feb 18 2016 yd <yd@os2power.com> 1.2.5-6
- added .pc file to distribution.
- use new debug macros.

* Mon Jun 02 2014 yd
- remove dll from devel package.
- added debug package with symbolic info for exceptq.

* Mon Jan 16 2012 yd
- rebuild with libc 0.6.4 runtime.
