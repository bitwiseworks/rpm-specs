Name:           lcms2
Version:        2.9
Release:        1%{?dist}
Summary:        Color Management Engine
License:        MIT
URL:            http://www.littlecms.com/

Vendor:         bww bitwise works GmbH
%scm_source svn http://svn.netlabs.org/repos/ports/lcms2/trunk 2316

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

%debug_package


%prep
%scm_setup

# hammer to nuke rpaths, recheck on new releases
export NOCONFIGURE=1
libtoolize -fc
autogen.sh


%build
export LDFLAGS=" -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"
export VENDOR="%{vendor}"

%configure --disable-static --enable-shared

make %{?_smp_mflags}


%install
make install DESTDIR=${RPM_BUILD_ROOT} INSTALL="install -p"

rm -fv %{buildroot}%{_libdir}/lib*.la

# rename docs (for use with %%doc below)
cp -af doc/LittleCMS2.?\ API.pdf api.pdf
cp -af doc/LittleCMS2.?\ Plugin\ API.pdf plugin-api.pdf
cp -af doc/LittleCMS2.?\ tutorial.pdf tutorial.pdf


%check
export BEGINLIBPATH=%{_builddir}/%{buildsubdir}/src/.libs
make check -k ||:


#%ldconfig_scriplets


%files
%doc AUTHORS
%license COPYING
%{_libdir}/*.dll

%files utils
%{_bindir}/*.exe
%{_mandir}/man1/*

%files devel
%doc api.pdf plugin-api.pdf tutorial.pdf
%{_includedir}/lcms2*.h
%{_libdir}/*.a
%{_libdir}/pkgconfig/lcms2.pc


%changelog
* Sat Dec 29 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.9-1
- update to vendor version 2.9

* Fri Mar 03 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.8-1
- update to vendor version 2.8
- use scm_ macros

* Wed Mar 16 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.7-1
- remove dbg files from normal packages

* Tue Feb 16 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.7-0
- First release
