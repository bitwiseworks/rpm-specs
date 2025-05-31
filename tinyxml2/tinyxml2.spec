%global soversion 10

Name:           tinyxml2
Version:        11.0.0
Release:        1%{?dist}
Summary:        Simple, small and efficient C++ XML parser

License:        zlib
%if 0%{os2_version}
Vendor:         TeLLie OS2 forever
Distribution:   OS/2
Packager:       TeLLeRBoP
%endif
URL:            https://github.com/leethomason/tinyxml2
%if !0%{os2_version}
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
%else
%scm_source github https://github.com/tellie/%{name}-os2 %{version}-os2
%endif

BuildRequires:  make
BuildRequires:  cmake >= 2.6
BuildRequires:  gcc
BuildRequires:  gcc-c++

%description
TinyXML-2 is a simple, small, efficient, C++ XML parser that can be
easily integrated into other programs. It uses a Document Object Model
(DOM), meaning the XML data is parsed into a C++ objects that can be
browsed and manipulated, and then written to disk or another output stream.

TinyXML-2 doesn't parse or use DTDs (Document Type Definitions) nor XSLs
(eXtensible Stylesheet Language).

TinyXML-2 uses a similar API to TinyXML-1, But the implementation of the
parser was completely re-written to make it more appropriate for use in a
game. It uses less memory, is faster, and uses far fewer memory allocations.

%package devel
Summary:        Development files for %{name}
%if !0%{os2_version}
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
%else
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
%endif
%description devel
This package contains the libraries and header files that are needed
for writing applications with the %{name} library.

%prep
%if !0%{os2_version}
%autosetup
%else
%scm_setup
%endif
chmod -c -x *.cpp *.h

%if 0%{?os2_version}
%legacy_runtime_packages
%endif

%build
%if 0%{os2_version}
#Otherwise the test failed!
mkdir resources/out 
%endif
%cmake 
%cmake_build

# Library tests were disabled in 3.0.0
# and partially re-enabled in 6.0.0
%check
%if 0%{os2_version}
export BEGINLIBPATH=%{_builddir}/%{buildsubdir}/pc-os2-emx-build
%endif
%ctest

%install
%cmake_install

%files
%doc readme.md
%if !0%{os2_version}
%{_libdir}/lib%{name}.so.%{soversion}*
%else
%{_libdir}/*.dll
%endif

%files devel
%{_includedir}/%{name}.h
%if !0%{os2_version}
%{_libdir}/lib%{name}.so
%else
%{_libdir}/%{name}_dll.a
%endif
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/cmake/%{name}/

%changelog
* Sat May 31 2025 Elbert Pol <elbert.pol@gmail.com> - 11.0.0-1
- Updated to latest version

* Sat Feb 24 2024 Elbert Pol <elbert.pol@gmail.com> - 10.0.0-2
- Build with the right version, and not with master
- Add a defination for that we dont have dllimport

* Sat Feb 24 2024 Elbert Pol <elbert.pol@gmail.com> - 10.0.0-1
- Updated to latest version
- Add bldlevel nfo for os2
- Provide legacy packages with DLLs for old ABI.

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
