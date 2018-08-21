# Note: this .spec is borrowed from pixman-0.33.6-1.fc24.src.rpm

Name:           pixman
Version:        0.32.8
Release:        4%{?dist}
Summary:        Pixel manipulation library

Group:          System Environment/Libraries
License:        MIT
URL:            http://cgit.freedesktop.org/pixman/
Vendor:         bww bitwise works GmbH

%scm_source  svn http://svn.netlabs.org/repos/ports/pixman/trunk 1232

BuildRequires: gcc make subversion zip

BuildRequires:  automake autoconf libtool

%description
Pixman is a pixel manipulation library for X and Cairo.

%package devel
Summary: Pixel manipulation library development package
Group: Development/Libraries
Requires: %{name}%{?isa} = %{version}-%{release}
Requires: pkgconfig

%description devel
Development library for pixman.

%prep
%scm_setup

# Generate confuigure and friends
NOCONFIGURE=1 autogen.sh

%build
export LDFLAGS="-Zhigh-mem"
export LIBS="-lcx"
%configure \
  --disable-static

make %{?_smp_mflags} V=1

%install
make install DESTDIR=$RPM_BUILD_ROOT

find %{buildroot} -type f -name "*.la" -delete

%check
make check %{?_smp_mflags} V=1 ||:

#%post -p /sbin/ldconfig
#%postun -p /sbin/ldconfig

%files
%doc COPYING
%{_libdir}/pixman1*.dll

%files devel
%dir %{_includedir}/pixman-1
%{_includedir}/pixman-1/pixman.h
%{_includedir}/pixman-1/pixman-version.h
%{_libdir}/pixman-1*.a
%{_libdir}/pkgconfig/pixman-1.pc

%changelog
* Tue Aug 21 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> 0.32.8-4
- rebuild with latest tool chain
- use new scm_ macros
- use libcx

* Tue Mar 1 2016 Dmitriy Kuminov <coding@dmik.org> 0.32.8-3
- Use respective optimization flags for different architectures.

* Sat Feb 20 2016 Dmitriy Kuminov <coding@dmik.org> 0.32.8-2
- Allow loading DLL into high memory.

* Tue Dec 29 2015 Dmitriy Kuminov <coding@dmik.org> 0.32.8-1
- Initial package for version 0.38.2.
