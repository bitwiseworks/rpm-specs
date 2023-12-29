
# feature macro to enable samples (or not)
%if 0%{?rhel} != 7
%global samples 1
%endif

Summary: Library for reading RAW files obtained from digital photo cameras
Name: LibRaw
Version: 0.21.1
Release: 2%{?dist}
License: BSD-3-Clause and (CDDL-1.0 or  LGPL-2.1-only)
URL: http://www.libraw.org

BuildRequires: gcc-c++
BuildRequires: pkgconfig(lcms2)
BuildRequires: pkgconfig(jasper)
BuildRequires: pkgconfig(libjpeg)
BuildRequires: autoconf automake libtool
BuildRequires: make

%if !0%{?os2_version}
Source0: http://github.com/LibRaw/LibRaw/archive/%{version}.tar.gz
%else
%scm_source github https://github.com/Tellie//%{name}-os2 %{version}-os2
%endif
%if !0%{?os2_version}
Patch0: LibRaw-pkgconfig.patch
Patch1: 9ab70f6dca19229cb5caad7cc31af4e7501bac93.patch
%endif
Provides: bundled(dcraw) = 9.25

%description
LibRaw is a library for reading RAW files obtained from digital photo
cameras (CRW/CR2, NEF, RAF, DNG, and others).

LibRaw is based on the source codes of the dcraw utility, where part of
drawbacks have already been eliminated and part will be fixed in future.

%package devel
Summary: LibRaw development libraries
Requires:   %{name}%{?_isa} = %{version}-%{release}

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
Requires: %{name} = %{version}-%{release}

%description samples
LibRaw sample programs

%prep
%if !0%{?os2_version}
%autosetup -p1 -n %{name}-%{version}
%else
%scm_setup
%endif

%build
autoreconf -ifv
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx -lpthread"

%configure \
    --enable-examples=%{?samples:yes}%{!?samples:no} \
    --enable-jasper \
    --enable-jpeg \
    --enable-lcms
%if !0%{?os2_version}
    --enable-openmp
%endif

# https://fedoraproject.org/wiki/Packaging:Guidelines#Beware_of_Rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%if !0%{?os2_version}
%make_build
%else
make %{?_smp_mflags} 
%endif

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

%if !0%{?os2_version}
%ldconfig_scriptlets
%endif

%files
%doc Changelog.txt
%license LICENSE.CDDL LICENSE.LGPL COPYRIGHT
%if !0%{?os2_version}
%{_libdir}/libraw.so.23*
%{_libdir}/libraw_r.so.23*
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

%if 0%{?samples}
%files samples
%{_bindir}/*
%endif

%changelog
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

