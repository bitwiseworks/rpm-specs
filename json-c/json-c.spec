%if !0%{?os2_version}
%{!?_pkgdocdir:%global _pkgdocdir %{_docdir}/%{name}-%{version}}
%else
%global _pkgdocdir %{_docdir}/%{name}-%{main_version}
%endif

# We don't want accidental SONAME bumps.
# When there is a SONAME bump in json-c, we need to request
# a side-tag for bootstrap purposes:
#
# 1. Build a bootstrap build of the systemd package, and wait
#    for it to be available inside the side-tag.
# 2. Re-build the following build-chain for bootstrap:
#    json-c : cryptsetup
# 3. Untag the systemd bootstrap build from the side-tag, and
#    disable bootstrapping in the systemd package.  Re-build
#    the systemd package into Rawhide.
# 4. Wait for the changes to populate and re-build the following
#    chain into the side-tag:
#    satyr : libdnf libreport
# 5. Merge the side-tag using Bodhi.
#
# After that procedure any other cosumers can be re-build
# in Rawhide as usual.
%global so_ver 5

# Releases are tagged with a date stamp.
%global reldate 20220414


Name:           json-c
Version:        0.16
Release:        1%{?dist}
Summary:        JSON implementation in C

License:        MIT
URL:            https://github.com/%{name}/%{name}
%if !0%{?os2_version}
Source0:        %{url}/archive/%{name}-%{version}-%{reldate}.tar.gz
%else
Vendor:         bww bitwise works GmbH
#scm_source     github https://github.com/bitwiseworks/%{name}-os2 %{name}-%{version}-%{reldate}-os2
%scm_source     git e:/trees/json-c/git master-os2
%global __cmake_in_source_build 1
%endif

%if !0%{?os2_version}
# Cherry-picked from upstream.
Patch0000:      %{url}/commit/870965e1eaa956324f7ed0825fd29ef584c20bc8.patch
Patch0001:      %{url}/commit/55bf2d365de8157968d26c3bd0847776ffb2af29.patch
Patch0002:      %{url}/commit/6cf48477960b96aedca2c87cf7bb53861ceeecd2.patch
Patch0003:      %{url}/commit/46eea845544bb89e8298a25ccc1d3ffdf4967e38.patch
Patch0004:      %{url}/commit/4e9e44e5258dee7654f74948b0dd5da39c28beec.patch
Patch0005:      %{url}/commit/0ffb38440935b2c71fa4851d2f44f2d120f24735.patch
Patch0006:      %{url}/commit/f052e42f56eae6b8a5b3833731e1d85e054fa09e.patch
Patch0007:      %{url}/commit/2b439ea59857747067e8272011ad67303e0d4cf1.patch
Patch0008:      %{url}/commit/4298431150df9a83390a14006217c230e684994b.patch
Patch0009:      %{url}/commit/583911a66c5b1103e7c98e59ef165631c0cbf290.patch
Patch0010:      %{url}/commit/e50154f615cbd2a14857a6f68462e3a699be42d8.patch
Patch0011:      %{url}/commit/bcb6d7d3474b687718cbaee7bf203db4456fb6b3.patch
Patch0012:      %{url}/commit/df62119b7f11dbd97715668a6311410f67bea3c9.patch
Patch0013:      %{url}/commit/369e8477d25132e9eeefb89ae1dacb3c4a738652.patch
Patch0014:      %{url}/commit/7af593c140523efa04e863f3772f0632c7ffcde3.patch
Patch0015:      %{url}/commit/0fd3b7d316bcfbca2bac875eea396fbc9cf08b33.patch
Patch0016:      %{url}/commit/987d3b2c86748299f2ceb83345264c6aaa8e1db6.patch
Patch0017:      %{url}/commit/0f61f6921b2e4395d1e354ad356137e44d6a7e11.patch
Patch0018:      %{url}/commit/c456963110fa5af9a209218c718d81033ad53669.patch
Patch0019:      %{url}/commit/f787810890b91b2b141ce7630d5be85c5f8cfcc3.patch
Patch0020:      %{url}/commit/041cef434afe0d0c6da8b6ac1d1fa26087246dda.patch
Patch0021:      %{url}/commit/ba181548bca566d320899f7b78e5b753c0dba611.patch
Patch0022:      %{url}/commit/9c0565100afde7d40ef0a6b34e9df2bfe84f2735.patch
Patch0023:      %{url}/commit/1f8b64f62c76cb23a8eb041fdde341db604aae75.patch
Patch0024:      %{url}/commit/8abeebc9b20ee830867df1c21cfa87bd6fdbaa38.patch
Patch0025:      %{url}/commit/9b53c92ea398c479f59f77b2cbd24d2ccf1fc29a.patch
Patch0026:      %{url}/commit/9ca50cf2f81ff66b9f0cf9b5c418cafafce82715.patch
Patch0027:      %{url}/commit/75bf657cc285c1b726492ed6af3645ea95fe17ac.patch
Patch0028:      %{url}/commit/9dde931a1c3aa4fd9ffc0be910ee03dceda156f8.patch
%endif

BuildRequires:  cmake
BuildRequires:  gcc
%if !0%{?os2_version}
BuildRequires:  ninja-build
%endif
%ifarch %{valgrind_arches}
BuildRequires:  valgrind
%endif

%description
JSON-C implements a reference counting object model that allows you
to easily construct JSON objects in C, output them as JSON formatted
strings and parse JSON formatted strings back into the C representation
of JSON objects.  It aims to conform to RFC 7159.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
This package contains libraries and header files for
developing applications that use %{name}.


%package        doc
Summary:        Reference manual for json-c

#BuildArch:     noarch

BuildRequires:  doxygen
%if !0%{?os2_version}
BuildRequires:  hardlink
%endif

%description    doc
This package contains the reference manual for %{name}.

%if 0%{?os2_version}
%legacy_runtime_packages
%debug_package
%endif

%prep
%if !0%{?os2_version}
%autosetup -n %{name}-%{name}-%{version}-%{reldate} -p 1
%else
%scm_setup
%endif

# Remove pre-built html documentation.
rm -fr doc/html

# Update Doxyfile.
doxygen -s -u doc/Doxyfile.in


%build
%if 0%{?os2_version}
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"
export VENDOR="%{vendor}"
%endif

%cmake \
  -DBUILD_STATIC_LIBS:BOOL=OFF       \
  -DCMAKE_BUILD_TYPE:STRING=RELEASE  \
  -DCMAKE_C_FLAGS_RELEASE:STRING=""  \
  -DDISABLE_BSYMBOLIC:BOOL=OFF       \
  -DDISABLE_WERROR:BOOL=ON           \
%if !0%{?os2_version}
  -DENABLE_RDRAND:BOOL=ON            \
  -DENABLE_THREADING:BOOL=ON         \
  -G Ninja
%else
  -DENABLE_THREADING:BOOL=ON
%endif
%cmake_build --target all doc


%install
%cmake_install

# Documentation
mkdir -p %{buildroot}%{_pkgdocdir}
cp -a %{__cmake_builddir}/doc/html ChangeLog README README.* \
  %{buildroot}%{_pkgdocdir}
%if !0%{?os2_version}
hardlink -cfv %{buildroot}%{_pkgdocdir}
%endif

%check
export USE_VALGRIND=0
%if !0%{?os2_version}
%ctest
%endif
%ifarch %{valgrind_arches}
export USE_VALGRIND=1
%ctest
%endif
unset USE_VALGRIND


%if !0%{?os2_version}
%ldconfig_scriptlets
%endif

%files
%license AUTHORS
%license COPYING
%if !0%{?os2_version}
%{_libdir}/lib%{name}.so.%{so_ver}*
%else
%{_libdir}/jsonc*.dll
%endif

%files devel
%doc %dir %{_pkgdocdir}
%doc %{_pkgdocdir}/ChangeLog
%doc %{_pkgdocdir}/README*
%{_includedir}/%{name}
%{_libdir}/cmake/%{name}
%if !0%{?os2_version}
%{_libdir}/lib%{name}.so
%else
%{_libdir}/%{name}_dll.a
%endif
%{_libdir}/pkgconfig/%{name}.pc


%files doc
%if 0%{?fedora} || 0%{?rhel} >= 7 || 0%{?os2_version}
%license %{_datadir}/licenses/%{name}*
%endif
%doc %{_pkgdocdir}


%changelog
* Tue May 03 2022 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.16-1
- update to version 0.16

* Sat Dec 29 2012 yd
- add object iterator to library, reduce exports to API only.

* Fri Dec 28 2012 yd
- initial build.
