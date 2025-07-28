%if 0%{?fedora}
%bcond_without mingw
%else
%bcond_with mingw
%endif

%global common_description %{expand:
Xerces-C is a validating XML parser written in a portable subset of C++.
Xerces-C makes it easy to give your application the ability to read and write
XML data. A shared library is provided for parsing, generating, manipulating,
and validating XML documents. Xerces-C is faithful to the XML 1.0
recommendation and associated standards: XML 1.0 (Third Edition), XML 1.1
(First Edition), DOM Level 1, 2, 3 Core, DOM Level 2.0 Traversal and Range, DOM
Level 3.0 Load and Save, SAX 1.0 and SAX 2.0, Namespaces in XML, Namespaces in
XML 1.1, XML Schema, XML Inclusions).}

Name:		xerces-c
Version:	3.3.0
Release:  1%{?dist}
Summary:	Validating XML Parser

License:	Apache-2.0
URL:		https://xerces.apache.org/xerces-c/
%if !0%{?os2_version}
Source0:	https://downloads.apache.org/xerces/c/3/sources/xerces-c-%{version}.tar.xz
Source1:	https://downloads.apache.org/xerces/c/3/sources/xerces-c-%{version}.tar.xz.asc
Source2:	https://downloads.apache.org/xerces/c/KEYS
Patch1:		xerces-c_mingw.patch
%else
Vendor:   bww bitwise works GmbH
%scm_source github http://github.com/bitwiseworks/%{name}-os2 v%{version}-os2
%endif

BuildRequires:	cmake
BuildRequires:	dos2unix
BuildRequires:	gcc-c++
BuildRequires:	gnupg2
BuildRequires:	make

%if %{with mingw}
BuildRequires:  mingw32-filesystem
BuildRequires:  mingw32-gcc-c++

BuildRequires:  mingw64-filesystem
BuildRequires:  mingw64-gcc-c++
%endif

%description
%{common_description}

%package	devel
Summary:	Header files, libraries and development documentation for %{name}
%if !0%{?os2_version}
Requires:	%{name}%{?_isa} = %{version}-%{release}
%else
Requires: %{name} = %{version}-%{release}
%endif

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%package doc
Summary:	Documentation for Xerces-C++ validating XML parser
BuildArch:	noarch

%description doc
Documentation for Xerces-C++.

%if %{with mingw}
%package -n mingw32-%{name}
Summary:        MingGW x86 Windows validating XML parser
BuildArch:	noarch

%description -n mingw32-xerces-c
%{common_description}

%package -n mingw64-%{name}
Summary:        MingGW x64 Windows validating XML parser
BuildArch:	noarch

%description -n mingw64-%{name}
%{common_description}
%endif

%{?mingw_debug_package}

%if 0%{?os2_version}
%debug_package
%endif

%prep
%if !0%{?os2_version}
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -p1
%else
%scm_setup
%endif
# Copy samples before build to avoid including built binaries in -doc package
mkdir -p _docs
cp -a samples/ _docs/

%build
# --disable-sse2 makes sure explicit -msse2 isn't passed to gcc so
# the binaries would be compatible with non-SSE2 i686 hardware.
# This only affects i686, as on x86_64 the compiler uses SSE2 by default.
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
export CXXFLAGS="$CFLAGS"
%if 0%{?os2_version}
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"
export VENDOR="%{vendor}"
%endif
%cmake -Dsse2=FALSE
%cmake_build

%if %{with mingw}
%mingw_cmake -Dsse2=FALSE
# FIXME we don't have Mingw version of cmake_build
%mingw_make_build
%endif

%install
%cmake_install
# Correct errors in encoding
iconv -f iso8859-1 -t utf-8 CREDITS > CREDITS.tmp && mv -f CREDITS.tmp CREDITS
# Correct errors in line endings
%if !0%{?os2_version}
pushd doc; dos2unix -k *.xml; popd
%else
cd doc; dos2unix -k *.xml; cd ..
%endif
# Remove unwanted binaries
rm -rf $RPM_BUILD_ROOT%{_bindir}
# Remove .la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
# Remove installed docs
rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}

%if %{with mingw}
# FIXME we don't have Mingw version of cmake_install
%mingw_make_install

rm -f %{buildroot}%{mingw32_bindir}/*.exe
rm -f %{buildroot}%{mingw64_bindir}/*.exe
rm -rf %{buildroot}%{mingw32_datadir}/doc/
rm -rf %{buildroot}%{mingw64_datadir}/doc/
%endif

%{?mingw_debug_install_post}

%files
%license LICENSE
%if !0%{?os2_version}
%{_libdir}/libxerces-c-3.3.so
%else
%{_libdir}/xerces33.dll
%endif

%files devel
%{_includedir}/xercesc/
%{_libdir}/cmake/XercesC/
%if !0%{?os2_version}
%{_libdir}/libxerces-c.so
%else
%{_libdir}/xerces-c_dll.a
%endif
%{_libdir}/pkgconfig/xerces-c.pc

%files doc
%license LICENSE
%doc README NOTICE CREDITS doc/html/* _docs/samples/

%if %{with mingw}
%files -n mingw32-%{name}
%license LICENSE
%{mingw32_bindir}/libxerces-c-3.3.dll
%{mingw32_includedir}/xercesc/
%{mingw32_libdir}/cmake/XercesC/
%{mingw32_libdir}/libxerces-c.dll.a
%{mingw32_libdir}/pkgconfig/xerces-c.pc

%files -n mingw64-%{name}
%license LICENSE
%{mingw64_bindir}/libxerces-c-3.3.dll
%{mingw64_includedir}/xercesc/
%{mingw64_libdir}/cmake/XercesC/
%{mingw64_libdir}/libxerces-c.dll.a
%{mingw64_libdir}/pkgconfig/xerces-c.pc
%endif

%changelog
* Mon Jul 28 2025 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.3.0-1
- first OS/2 rpm
