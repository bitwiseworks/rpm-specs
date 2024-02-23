#
# spec file for package tinyxml2
#
# Copyright (c) 2021 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#

%if !0%{?os2_version}
%define so_version 9
%define lib_package lib%{name}-%{so_version}
%endif
Name:           tinyxml2
Version:        9.0.0
Release:        1%{?dist}
Vendor:         TeLLie
Summary:        Basic XML parser in C++
License:        Zlib
Group:          Development/Libraries/C and C++
URL:            https://github.com/leethomason/tinyxml2
%if !0%{?os2_version}
Source:         https://github.com/leethomason/tinyxml2/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
%else
%scm_source github https://github.com/Tellie/%{name}-os2 master-os2
%endif
BuildRequires:  cmake >= 3.15
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig

%description
TinyXML is a feature-bounded XML parser in C++ that can be integrated
into other programs.

TinyXML-2 does not parse or use DTDs (Document Type Definitions) or
XSLs (eXtensible Stylesheet Language). There are other parsers (with
different footprints) to do such.

%package -n     %{lib_package}
Summary:        Basic XML parser in C++
License:        Zlib
Group:          System/Libraries

%description -n %{lib_package}
TinyXML is a feature-bounded XML parser in C++ that can be integrated
into other programs.

TinyXML-2 does not parse or use DTDs (Document Type Definitions) or
XSLs (eXtensible Stylesheet Language). There are other parsers (with
different footprints) to do such.

%package        devel
Summary:        Development files for libtinyxml2
License:        GPL-2.0-or-later
Group:          Development/Libraries/C and C++
%if !0%{?os2_version}
Requires:       %{lib_package} = %{version}
%else
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
%endif
%description    devel
Contains libraries and header files for
developing applications that use libtinyxml2.

%debug_package

%prep
%if !0%{?os2_version}
%setup -q
%else
%scm_setup
chmod -c -x *.cpp *.h
%endif

%build
%if 0%{?os2_version}
mkdir builder
cd builder
export LDFLAGS="-Zhigh-mem -Zomf -lcx"
export CFLAGS="-O2 -g -march=i686"
export CXXFLAGS="-O2 -g -march=i686"
export FFLAGS="-O2 -g -march=i686"
export FCFLAGS="-O2 -g -march=i686"

cmake -DCMAKE_INSTALL_PREFIX:PATH=/@unixroot/usr \
      -DCMAKE_SKIP_RPATH:BOOL=YES \
      -DBUILD_SHARED_LIBS=ON \
      -DCMAKE_BUILD_TYPE=Release \
      -DOS2_USE_CXX_EMXEXP=ON \
      -DBUILD_TESTING=ON \
      -Wno-dev \
      .. 2>stdout 1>stderr
make %{?_smp_mflags}
%else
%cmake  
%make_build
%endif

%install
%if !0%{?os2_version}
%cmake_install
find %{buildroot} -type f -name "*.la" -delete -print
# /usr/lib/cmake is not owned by cmake; avoid any further conflicts
if [ ! -d "%{buildroot}/%{_libdir}/cmake/%{name}" ]; then
mkdir -p %{buildroot}/%{_libdir}/cmake/%{name}
mv %{buildroot}%{_prefix}/lib/cmake/tinyxml2 %{buildroot}/%{_libdir}/cmake/tinyxml2
fi
%else
rm -rf %{buildroot}
cd builder
make install DESTDIR=%{buildroot}
%endif

%check
%if !0%{?os2_version}
%make_build test
%else
cd builder
export BEGINLIBPATH=%{_builddir}/%{buildsubdir}/builder
make -k test
%endif

%if !0%{?os2_version}
%post -n %{lib_package} -p /sbin/ldconfig
%postun -n %{lib_package} -p /sbin/ldconfig
%endif

%files 
%defattr(-,root,root,-)
%license LICENSE.txt
%doc readme.md
%if !0%{?os2_version}
%{_libdir}/libtinyxml2.so.%{so_version}*
%else
%{_libdir}/tinyxml9.dll
%endif

%files devel
%license LICENSE.txt
%{_includedir}/tinyxml2.h
%if !0%{?os2_version}
%{_libdir}/libtinyxml2.so
%else
%{_libdir}/tinyxml2_dll.a
%endif
%{_libdir}/pkgconfig/tinyxml2.pc
%{_libdir}/cmake/tinyxml2

%changelog
* Thu Apr 28 2022 Elbert Pol <elbert.pol@gmail.com> - 9.0.0 -1
- Updated to latest version
- Add os2 specification 

* Sun May 05 2019 Elbert Pol <elbert.pol@gmail.com> - 7.0.1-2
- Add debug package

* Sat May 04 2019 Elbert Pol <elbert.pol@gmail.com> - 7.0.1-1
- Updated to latest source
- Fix wrong dll place

* Fri May 11 2018  Elbert Pol <elbert.pol@gmail.com> - 6.2.0-1
-  initial rpm for OS2
-  Add buildlevel os2
