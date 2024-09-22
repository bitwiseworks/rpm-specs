%global somajor 23

Summary: Library for reading RAW files obtained from digital photo cameras
Name: libraw
Version: 0.21.3
Release: 1%{?dist}
License: BSD-3-Clause and (CDDL-1.0 or LGPL-2.1-only)
URL: https://www.libraw.org
%if 0%{?os2_version}
Vendor:         TeLLie OS2 forever
Distribution:   OS/2
Packager:       TeLLeRBoP
%endif
%if !0%{?os2_version}
Source0: %{url}/data/%{name}-%{version}.tar.gz
Patch0: LibRaw-pkgconfig.patch
%else
%scm_source github https://github.com/Tellie/%{name}-os2 %{version}-os2
%endif

BuildRequires: gcc-c++
BuildRequires: pkgconfig(lcms2)
BuildRequires: pkgconfig(jasper)
BuildRequires: pkgconfig(libjpeg)
BuildRequires: pkgconfig(zlib)
BuildRequires: autoconf automake libtool
BuildRequires: make

Provides: bundled(dcraw) = 9.25

%description
LibRaw is a library for reading RAW files obtained from digital photo
cameras (CRW/CR2, NEF, RAF, DNG, and others).

LibRaw is based on the source codes of the dcraw utility, where part of
drawbacks have already been eliminated and part will be fixed in future.

%package devel
Summary: LibRaw development libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
LibRaw development libraries.

This package contains libraries that applications can use to build
against LibRaw.

%package static
Summary: LibRaw static development libraries
Requires: %{name}-devel%{?_isa} = %{version}-%{release}

%description static
LibRaw static development libraries.

%package samples
Summary: LibRaw sample programs
Requires: %{name}%{?_isa} = %{version}-%{release}

%description samples
LibRaw sample programs

%prep
%if !0%{?os2_version}
%autosetup -p1 -n %{name}-%{version}
%else
%scm_setup
%endif

%build
%if 0%{?os2_version}
# Set BUILDLEVEL to be embedded to all DLLs built with Libtool.
export LT_BUILDLEVEL="@#%{vendor}:%{version}-%{release}#@##1## `LANG=C date +'%%d %%b %%Y %%H:%%M:%%S'`     `uname -n`::::0::"
%endif
autoreconf -if
%configure \
    --enable-examples=yes \
    --enable-jasper \
    --enable-jpeg \
    --enable-lcms \
    --enable-zlib \
%if !0%{?os2_version}
    --enable-openmp \
%else
   --disable-openmp
%endif

# https://fedoraproject.org/wiki/Packaging:Guidelines#Beware_of_Rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build

%install
cp -pr doc manual
chmod 644 LICENSE.CDDL LICENSE.LGPL COPYRIGHT Changelog.txt
chmod 644 manual/*.html

# The Libraries
%make_install

rm -rfv samples/.deps
rm -fv samples/.dirstamp
rm -fv samples/*.o

rm -fv %{buildroot}%{_libdir}/lib*.la

%files
%doc Changelog.txt
%license LICENSE.CDDL LICENSE.LGPL COPYRIGHT
%if !0%{?os2_version}
%{_libdir}/libraw.so.%{somajor}{,.*}
%{_libdir}/libraw_r.so.%{somajor}{,.*}
%else
%{_libdir}/*.dll
%endif

%files static
%if !0%{?os2_version}
%{_libdir}/libraw.a
%{_libdir}/libraw_r.a
%else
%{_libdir}/raw_r.a
%{_libdir}/raw.a
%endif

%files devel
%doc manual
%doc samples
%{_includedir}/libraw/
%if !0%{?os2_version}
%{_libdir}/libraw.so
%{_libdir}/libraw_r.so
%else
%{_libdir}/raw_dll.a
%{_libdir}/raw23_dll.a
%{_libdir}/raw_r_dll.a
%{_libdir}/raw_r23_dll.a
%endif
%{_libdir}/pkgconfig/libraw.pc
%{_libdir}/pkgconfig/libraw_r.pc
%exclude %{_docdir}/libraw/*

%files samples
%{_bindir}/*


%changelog
* Fri Sep 20 2024 Elbert Pol <elbert.pol@gmail.com> - 0.21.3-1
- Updated to latest version

* Wed Dec 27 2023 Elbert Pol <elbert.pol@gmail.com> - 0.21.2-1
- Updated to latest version
- Updated to latest Fedora spec

* Tue Sep 19 2023 Elbert Pol <elbert.pol@gmail.com> - 0.21.1-2
- Set the static files to the right section
- Remove defattr frpm spec file

* Wed Sep 13 2023 Elbert Pol <elbert.pol@gmail.com> - 0.21.1-1
- Updated to latest version.

* Thu Oct 15 2020 Elbert Pol <elbert.pol@gmail.com> - 0.20.2-1
- Updated to latest version

* Thu Jan 31 2019 Elbert Pol <elbert.pol@gmail.com> - 0.19.2-5
- Remove dll's from the devel package.

* Wed Jan 30 2019 Elbert Pol <elbert.pol@gmail.com> - 0.19.2-4
- Add the raw_*.a files to devel package.

* Sat Dec 29 2018 Elbert Pol <elbert.pol@gmail.com> - 0.19.2-3
- Link with newer Lcms2

* Fri Dec 28 2018 Elbert Pol <elbert.pol@gmail.com> - 0.19.2-2
- Add patch to source as thats better if have own repo

* Thu Dec 27 2018 Elbert Pol <elbert.pol@gmail.com> - 0.19.2-1
- First Rpm version OS/2
