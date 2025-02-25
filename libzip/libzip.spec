%bcond_without tests

Name:    libzip
Version: 1.11.3
Release: 2%{?dist}
Summary: C library for reading, creating, and modifying zip archives

License: BSD-3-Clause
URL:     https://libzip.org/
%if !0%{?os2_version}
Source0: https://libzip.org/download/libzip-%{version}.tar.xz
%else
%scm_source github https://github.com/TeLLie/%{name}-os2 %{version}-os2
%endif


BuildRequires:  gcc
BuildRequires:  zlib-devel
BuildRequires:  bzip2-devel
BuildRequires:  openssl-devel
BuildRequires:  xz-devel
BuildRequires:  libzstd-devel >= 1.3.6
BuildRequires:  cmake >= 3.10
%if !0%{?os2_version}
BuildRequires:  mandoc
%if %{with tests}
BuildRequires:  nihtest
%endif
%endif

%description
libzip is a C library for reading, creating, and modifying zip archives. Files
can be added from data buffers, files, or compressed data copied directly from 
other zip archives. Changes made without closing the archive can be reverted. 
The API is documented by man pages.


%package devel
Summary:  Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package tools
Summary:  Command line tools from %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description tools
The %{name}-tools package provides command line tools split off %{name}:
- zipcmp
- zipmerge
- ziptool


%prep
%if !0%{?os2_version}
%autosetup -p1
%else
%scm_setup
%endif

# unwanted in package documentation
rm INSTALL.md

# drop skipped test which make test suite fails (cmake issue ?)
sed -e '/clone-fs-/d' \
    -i regress/CMakeLists.txt


%build
%cmake \
  -DENABLE_COMMONCRYPTO:BOOL=OFF \
  -DENABLE_GNUTLS:BOOL=OFF \
  -DENABLE_MBEDTLS:BOOL=OFF \
  -DENABLE_OPENSSL:BOOL=ON \
  -DENABLE_WINDOWS_CRYPTO:BOOL=OFF \
  -DENABLE_BZIP2:BOOL=ON \
  -DENABLE_LZMA:BOOL=ON \
  -DENABLE_ZSTD:BOOL=ON \
  -DBUILD_TOOLS:BOOL=ON \
  -DBUILD_REGRESS:BOOL=ON \
  -DBUILD_EXAMPLES:BOOL=OFF \
  -DBUILD_DOC:BOOL=ON

%cmake_build


%install
%cmake_install


%check
%if %{with tests}
%ctest
%else
: Test suite disabled
%endif

%if !0%{?os2_version}
%ldconfig_scriptlets
%endif

%files
%license LICENSE
%if !0%{?os2_version}
%{_libdir}/libzip.so.5*
%else
%{_libdir}/*.dll
%endif

%files tools
%if !0%{?os2_version}
%{_bindir}/zipcmp
%{_bindir}/zipmerge
%{_bindir}/ziptool
%else
%{_mandir}/man1/zip*
%{_bindir}/zipcmp.exe
%{_bindir}/zipmerge.exe
%{_bindir}/ziptool.exe
%endif

%files devel
%doc AUTHORS THANKS *.md
%{_includedir}/zip.h
%{_includedir}/zipconf*.h
%if !0%{?os2_version}
%{_libdir}/libzip.so
%else
%{_libdir}/*.a
%endif

%{_libdir}/pkgconfig/libzip.pc
%{_libdir}/cmake/libzip
%{_mandir}/man3/libzip*
%{_mandir}/man3/zip*
%{_mandir}/man3/ZIP*

%changelog
* Tue Feb 25 2025 Elbert Pol <elbert.pol@gmail.com> - 1.11.3-2
- Fix a macros.dist error

* Mon Jan 20 2025 Elbert Pol <elbert.pol@gmail.com> - 1.11.3-1
- Updated to latest version

* Sun Sep 22 2024 Elbert pol <elbert.pol@gmail.com> - 1.11.1-1 
- Updated to latest version

* Fri Aug 25 2023 Elbert pol <elbert.pol@gmail.com> - 1.10.1
- Updated to latest version.

* Wed Jul 05 2023 Elbert Pol <elbert.pol@gmail.com> - 1.10.0
- Updated to latest version.

* Sun Jan 15 2023 Elbert Pol <elbert.pol@gmail.com> - 1.9.2 - 1
- Updated to latest version

* Sun Jun 19 2022 Elbert Pol <elbert.pol@gmail.com> - 1.9.0 - 1
- Updated to latest version

* Sun Jul 04 2021 Elbert Pol <elbert.pol@gmail.com> - 1.8.0 - 1
- Update to latest version

* Wed Jan 06 2021 Elbert Pol <elbert.pol@gmail.com> - 1.22 - 1
- Update to latest version
- Finetuning the spec file

* Thu Jan 31 2019 Elbert Pol <elbert.pol@gmail.com> - 1.21-2
- Upload src to github

* Sat Jan 12 2019 Elbert Pol <elbert.pol@gmail.com> 1.21-1
- Updated to latest source

* Sun Sep 09 2018 Elbert Pol <elbert.pol@gmail.com> 1.20-2
- Some changes for Spec file

* Sun Sep 09 2018 Elbert Pol <elbert.pol@gmail.com> 1.20-1
- First OS/2 rpm release
