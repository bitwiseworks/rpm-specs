# Build documentation in HTML with images
%bcond_without jsoncpp_enables_doc

%global jsondir json

# Avoid accidental so-name bumps.
# ATTENTION!!!  You need to run a bootstrap build
# of cmake *BEFORE* bumping the so-name here!
%global sover 25


Name:           jsoncpp
Version:        1.9.5
Release:        1%{?dist}
Summary:        JSON library implemented in C++

License:        Public Domain or MIT
URL:            https://github.com/open-source-parsers/%{name}
%if !0%{?os2_version}
Source0:        %{url}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
%else
Vendor:         bww bitwise works GmbH
%scm_source github https://github.com/bitwiseworks/%{name}-os2 %{version}-os2
# Setup _vpath_builddir if not defined already
%{!?_vpath_builddir:%global _vpath_builddir %(echo '%{_target_platform}' | sed -e 's!/!!g')}
%{!?_vpath_srcdir:%global _vpath_srcdir .}
%endif

BuildRequires:  cmake >= 3.1
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  python3-devel

%description
%{name} is an implementation of a JSON (http://json.org) reader and writer in
C++. JSON (JavaScript Object Notation) is a lightweight data-interchange format.
It is easy for humans to read and write. It is easy for machines to parse and
generate.


%package        devel
Summary:        Development headers and library for %{name}
%if !0%{?os2_version}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%else
Requires:       %{name} = %{version}-%{release}
%endif

%description    devel
This package contains the development headers and library for %{name}.


%if %{with jsoncpp_enables_doc}
%package        doc
Summary:        Documentation for %{name}

BuildRequires:  doxygen
%if !0%{?os2_version}
BuildRequires:  graphviz
BuildRequires:  hardlink
%endif

BuildArch:      noarch

%description    doc
This package contains the documentation for %{name}.
%endif


%prep
%if !0%{?os2_version}
%autosetup -p 1
%else
%scm_setup
%endif
%if %{with jsoncpp_enables_doc}
doxygen -s -u doc/doxyfile.in
sed -i -e 's!^DOT_FONTNAME.*=.*!DOT_FONTNAME =!g' doc/doxyfile.in
%endif


%build
%if 0%{?os2_version}
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx" 
export VENDOR="%{vendor}"
%endif

%cmake                                         \
  -DBUILD_STATIC_LIBS:BOOL=OFF                 \
  -DBUILD_OBJECT_LIBS:BOOL=OFF                 \
  -DJSONCPP_WITH_CMAKE_PACKAGE:BOOL=ON         \
  -DJSONCPP_WITH_EXAMPLE:BOOL=OFF              \
  -DJSONCPP_WITH_PKGCONFIG_SUPPORT:BOOL=ON     \
  -DJSONCPP_WITH_POST_BUILD_UNITTEST:BOOL=OFF  \
  -DJSONCPP_WITH_STRICT_ISO:BOOL=ON            \
  -DJSONCPP_WITH_TESTS:BOOL=ON                 \
  -DJSONCPP_WITH_WARNING_AS_ERROR:BOOL=OFF     \
  -DPYTHON_EXECUTABLE:STRING="%{__python3}"
%cmake_build

%if %{with jsoncpp_enables_doc}
# Build the doc
cp -p %{__cmake_builddir}/version .
%if !0%{?os2_version}
%{__python3} doxybuild.py --with-dot --doxygen %{_bindir}/doxygen
%else
%{__python3} doxybuild.py --doxygen %{_bindir}/doxygen.exe
%endif
rm -f version
%endif


%install
%cmake_install

mkdir -p %{buildroot}%{_docdir}/%{name}
install -pm 0644 README.md %{buildroot}%{_docdir}/%{name}

%if %{with jsoncpp_enables_doc}
mkdir -p %{buildroot}%{_docdir}/%{name}/html
cp -a dist/doxygen/jsoncpp-api-html-/* %{buildroot}%{_docdir}/%{name}/html
find %{buildroot}%{_docdir} -type d -print0 | xargs -0 chmod -c 0755
find %{buildroot}%{_docdir} -type f -print0 | xargs -0 chmod -c 0644
%if !0%{?os2_version}
hardlink -cfv %{buildroot}%{_docdir}/%{name}
%endif
%endif


%check
# Run tests single threaded.
%if 0%{?os2_version}
# this export is needed, as else the dll for the tests are not found
export BEGINLIBPATH=%{_builddir}/%{buildsubdir}/%{_vpath_builddir}/lib
%endif
%global _smp_mflags -j1
%ctest


%if !0%{?os2_version}
%ldconfig_scriptlets
%endif


%files
%license AUTHORS LICENSE
%doc %dir %{_docdir}/%{name}
%doc %{_docdir}/%{name}/README.md
%if %{with jsoncpp_enables_doc}
%exclude %{_docdir}/%{name}/html
%endif
%if !0%{?os2_version}
%{_libdir}/lib%{name}.so.%{sover}*
%{_libdir}/lib%{name}.so.%{version}
%else
%{_libdir}/*.dll
%endif


%files devel
%if !0%{?os2_version}
%{_libdir}/lib%{name}.so
%else
%{_libdir}/*.a
%endif
%{_includedir}/%{jsondir}
%{_libdir}/cmake/*
%{_libdir}/pkgconfig/%{name}.pc


%if %{with jsoncpp_enables_doc}
%files doc
%if !0%{?os2_version}
%license %{_datadir}/licenses/%{name}
%endif
%doc %{_docdir}/%{name}
%endif


%changelog
* Mon Jan 30 2023 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.9.5-1
- Update to latest version
- Synced spec with fedora version

* Sun Oct 25 2020 Elbert Pol <elbert.pol@gmail.com> - 1.9.4-1
- Update to latest version
- Update spec file

* Fri Sep 18 2020 Elbert Pol <elbert.pol@gmail.com> - 1.9.3-1
- First RPM for OS2

