Name:           lcms2
Version:        2.11
Release:        1%{?dist}
Summary:        Color Management Engine
License:        MIT
URL:            http://www.littlecms.com/
%if !0%{?os2_version}
Source0:        http://www.littlecms.com/lcms2-%{version}.tar.gz
%else
Vendor:         bww bitwise works GmbH
%scm_source github http://github.com/bitwiseworks/%{name}-os2 v%{version}-os2
%endif

BuildRequires:  gcc
BuildRequires:  libjpeg-devel
BuildRequires:  libtiff-devel
BuildRequires:  zlib-devel

%description
LittleCMS intends to be a small-footprint, speed optimized color management
engine in open source form. LCMS2 is the current version of LCMS, and can be
parallel installed with the original (deprecated) lcms.

%package        utils
Summary:        Utility applications for %{name}
Requires:       %{name} = %{version}-%{release}

%description    utils
The %{name}-utils package contains utility applications for %{name}.

%package        devel
Summary:        Development files for LittleCMS
Requires:       %{name} = %{version}-%{release}
Provides:       littlecms-devel = %{version}-%{release}

%description    devel
Development files for LittleCMS.

%if 0%{?os2_version}
%debug_package
%endif

%prep
%if !0%{?os2_version}
%autosetup -p1
%else
%scm_setup
export NOCONFIGURE=1
libtoolize -fc
autogen.sh
%endif


%build
%if 0%{?os2_version}
export LDFLAGS=" -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"
export VENDOR="%{vendor}"
%endif

%configure \
  --disable-static \
  --program-suffix=2

# remove rpath from libtool
sed -i.rpath 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i.rpath 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%if !0%{?os2_version}
%make_build
%else
make %{?_smp_mflags}
%endif


%install
%make_install

rm -fv %{buildroot}%{_libdir}/lib*.la

# rename docs (for use with %%doc below)
%if !0%{?os2_version}
cp -alf doc/LittleCMS2.??\ API.odt api.odt
cp -alf doc/LittleCMS2.??\ Plugin\ API.odt plugin-api.odt
cp -alf doc/LittleCMS2.??\ tutorial.odt tutorial.odt
%else
cp -af doc/LittleCMS2.??\ API.odt api.odt
cp -af doc/LittleCMS2.??\ Plugin\ API.odt plugin-api.odt
cp -af doc/LittleCMS2.??\ tutorial.odt tutorial.odt
%endif


%check
%if !0%{?os2_version}
%make_build check -k ||:
%else
export BEGINLIBPATH=%{_builddir}/%{buildsubdir}/src/.libs
make check -k ||:
%endif


%if !0%{?os2_version}
%ldconfig_scriptlets
%endif

%files
%doc AUTHORS
%license COPYING
%if !0%{?os2_version}
%{_libdir}/liblcms2.so.2*
%else
%{_libdir}/*.dll
%endif

%files utils
%if !0%{?os2_version}
%{_bindir}/*
%else
%{_bindir}/*.exe
%endif
%{_mandir}/man1/*

%files devel
%doc api.odt plugin-api.odt tutorial.odt
%{_includedir}/lcms2*.h
%if !0%{?os2_version}
%{_libdir}/liblcms2.so
%else
%{_libdir}/*_dll.a
%endif
%{_libdir}/pkgconfig/lcms2.pc


%changelog
* Tue Dec 29 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.11-1
- update to vendor version 2.11
- resynced with fedora spec

* Sat Dec 29 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.9-1
- update to vendor version 2.9

* Fri Mar 03 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.8-1
- update to vendor version 2.8
- use scm_ macros

* Wed Mar 16 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.7-1
- remove dbg files from normal packages

* Tue Feb 16 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.7-0
- First release
