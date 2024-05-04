
%undefine __cmake_in_source_build

Summary: Exif and Iptc metadata manipulation library
Name:    exiv2
Version: 0.28.2
%global internal_ver %{version}
Release: 1%{?dist}

License: GPL-2.0-or-later
URL:     http://www.exiv2.org/
%if !0%{?os2_version}
%if 0%{?beta:1}
Source0: https://github.com/Exiv2/exiv2/archive/v%{version}-%{beta}/%{name}-%{version}-%{beta}.tar.gz
%else
Source0: http://exiv2.org/builds/%{name}-%{version}-Source.tar.gz
%endif
%else
Vendor:         bww bitwise works GmbH
%scm_source github https://github.com/bitwiseworks/%{name}-os2 v%{version}-os2
%endif

## upstream patches

## upstreamable patches

BuildRequires: cmake
BuildRequires: expat-devel
BuildRequires: gcc-c++
BuildRequires: gettext
BuildRequires: pkgconfig
BuildRequires: zlib-devel
# docs
%if !0%{?os2_version}
BuildRequires: doxygen graphviz libxslt
%endif

%if !0%{?os2_version}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
%else
Requires: %{name}-libs = %{version}-%{release}
%endif

%description
A command line utility to access image metadata, allowing one to:
* print the Exif metadata of Jpeg images as summary info, interpreted values,
  or the plain data for each tag
* print the Iptc metadata of Jpeg images
* print the Jpeg comment of Jpeg images
* set, add and delete Exif and Iptc metadata of Jpeg images
* adjust the Exif timestamp (that's how it all started...)
* rename Exif image files according to the Exif timestamp
* extract, insert and delete Exif metadata (including thumbnails),
  Iptc metadata and Jpeg comments

%package devel
Summary: Header files, libraries and development documentation for %{name}
%if !0%{?os2_version}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
%else
Requires: %{name}-libs = %{version}-%{release}
%endif
%description devel
%{summary}.

%package libs
Summary: Exif and Iptc metadata manipulation library
# not strictly required, but convenient and expected
%if 0%{?rhel} && 0%{?rhel} <= 7
Requires: %{name} = %{version}-%{release}
%else
Recommends: %{name} = %{version}-%{release}
%endif
%description libs
A C++ library to access image metadata, supporting full read and write access
to the Exif and Iptc metadata, Exif MakerNote support, extract and delete
methods for Exif thumbnails, classes to access Ifd and so on.

%package doc
Summary: Api documentation for %{name}
BuildArch: noarch
%description doc
%{summary}.


%prep
%if !0%{?os2_version}
%autosetup -n %{name}-%{version}-%{?beta}%{!?beta:Source} -p1
%else
%scm_setup
%endif

%build
%if 0%{?os2_version}
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx -lpthread -fstack-protector"
export VENDOR="%{vendor}"
%endif

%cmake \
  -DCMAKE_INSTALL_DOCDIR="%{_pkgdocdir}" \
%if !0%{?os2_version}
  -DEXIV2_BUILD_DOC:BOOL=ON \
%endif
  -DEXIV2_ENABLE_NLS:BOOL=ON \
%if 0%{?os2_version}
  -DEXIV2_ENABLE_BROTLI:BOOL=OFF \
  -DEXIV2_ENABLE_INIH:BOOL=OFF \
  -DICONV_ACCEPTS_CONST_INPUT:BOOL=ON \
%endif
  -DEXIV2_BUILD_SAMPLES:BOOL=OFF

%cmake_build
%if !0%{?os2_version}
%cmake_build --target doc
%endif

%install
%cmake_install

%find_lang exiv2 --with-man


%check
%if !0%{?os2_version}
export PKG_CONFIG_PATH="%{buildroot}%{_libdir}/pkgconfig${PKG_CONFIG_PATH:+:}${PKG_CONFIG_PATH}"
test "$(pkg-config --modversion exiv2)" = "%{internal_ver}"
test "$(pkg-config --variable=libdir exiv2)" = "%{_libdir}"
test -x %{buildroot}%{_libdir}/libexiv2.so
%endif

%files -f exiv2.lang
%license COPYING
%doc doc/ChangeLog
# README is mostly installation instructions
#doc README.md
%if !0%{?os2_version}
%{_bindir}/exiv2
%else
%{_bindir}/exiv2.exe
%endif
%{_mandir}/man1/exiv2*.1*

%if !0%{?os2_version}
%ldconfig_scriptlets libs
%endif

%files libs
%if !0%{?os2_version}
%{_libdir}/libexiv2.so.27*
%{_libdir}/libexiv2.so.%{internal_ver}
%else
%{_libdir}/exiv228.dll
%endif

%files devel
%{_includedir}/exiv2/
%if !0%{?os2_version}
%{_libdir}/libexiv2.so
%else
%{_libdir}/exiv2_dll.a
%endif
%{_libdir}/pkgconfig/exiv2.pc
%{_libdir}/cmake/exiv2/
# todo: -static subpkg?  -- rex
%if !0%{?os2_version}
%{_libdir}/libexiv2-xmp.a
%endif

%files doc
%{_pkgdocdir}/


%changelog
* Fri May 03 2024 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.28.2-1
- first OS/2 rpm
