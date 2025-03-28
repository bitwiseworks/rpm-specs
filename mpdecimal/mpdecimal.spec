# Whether to package the compatibility .so from the previous release.
# This installs self as a build dependency and copies the files.
# Once disabled, it can only be built when the previous version is tagged in.
# It is required to be able to rebuild Pythons with the new library.
%if !0%{?os2_version}
%bcond compat 0
%else
%bcond_with compat
%endif

Name:           mpdecimal
Version:        4.0.0
Release:        1%{?dist}
Summary:        Library for general decimal arithmetic
License:        BSD-2-Clause

URL:            https://www.bytereef.org/mpdecimal/index.html
%if !0%{?os2_version}
Source0:        https://www.bytereef.org/software/mpdecimal/releases/mpdecimal-%{version}.tar.gz
%else
Vendor:         bww bitwise works GmbH
%scm_source     github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2
%endif
Source1:        https://speleotrove.com/decimal/dectest.zip

BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  unzip
%if %{with compat}
BuildRequires:  %{name}
%endif

%description
The package contains a library libmpdec implementing General Decimal
Arithmetic Specification. The specification, written by Mike Cowlishaw from
IBM, defines a general purpose arbitrary precision data type together with
rigorously specified functions and rounding behavior.

%package -n %{name}++
Requires:       %{name}%{?_isa} = %{version}-%{release}
Summary:        Library for general decimal arithmetic (C++)

%description -n %{name}++
The package contains a library libmpdec++ implementing General Decimal
Arithmetic Specification. The specification, written by Mike Cowlishaw from
IBM, defines a general purpose arbitrary precision data type together with
rigorously specified functions and rounding behavior.

%package        devel
%if !0%{?os2_version}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}++%{?_isa} = %{version}-%{release}
%else
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}++ = %{version}-%{release}
%endif
Summary:        Development headers for mpdecimal library

%description devel
The package contains development headers for the mpdecimal library.

%if 0%{?os2_version}
%debug_package
%endif

%prep
%if !0%{?os2_version}
%autosetup
%else
%scm_setup
autoreconf -fvi
%endif
unzip -d tests/testdata %{SOURCE1}

%build
%if 0%{?os2_version}
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"
export LDXXFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx -lpthread"
export LIBS="-lcx -lpthread"
export VENDOR="%{vendor}"
%endif
%configure --disable-static
# Set LDXXFLAGS to properly pass the buildroot
# linker flags to the C++ extension.
%make_build LDXXFLAGS="%{build_ldflags}"

%check
%make_build check

%install
%make_install

# license will go into dedicated directory
rm %{buildroot}%{_docdir}/%{name}/COPYRIGHT.txt

%if %{with compat}
cp -a %{_libdir}/libmpdec.so.2.5.1 %{buildroot}%{_libdir}/libmpdec.so.3
%endif

%files
%doc README.txt CHANGELOG.txt
%license COPYRIGHT.txt
%if !0%{?os2_version}
%{_libdir}/libmpdec.so.%{version}
%{_libdir}/libmpdec.so.4
%else
%{_libdir}/mpdec4.dll
%endif
%if %{with compat}
%{_libdir}/libmpdec.so.3
%endif

%files -n %{name}++
%if !0%{?os2_version}
%{_libdir}/libmpdec++.so.%{version}
%{_libdir}/libmpdec++.so.4
%else
%{_libdir}/mpdec++4.dll
%endif

%files devel
%if !0%{?os2_version}
%{_libdir}/libmpdec.so
%{_libdir}/libmpdec++.so
%else
%{_libdir}/libmpdec_dll.a
%{_libdir}/libmpdec++_dll.a
%endif
%{_includedir}/mpdecimal.h
%{_includedir}/decimal.hh
%{_libdir}/pkgconfig/libmpdec.pc
%{_libdir}/pkgconfig/libmpdec++.pc
%{_mandir}/man3/libmpdec.3*
%{_mandir}/man3/libmpdec++.3*
%{_mandir}/man3/mpdecimal*.3*

%changelog
* Fri Mar 28 2025 Silvan Scherrer <silvan.scherrer@aroa.ch> 4.0.0-1
- first OS/2 rpm
