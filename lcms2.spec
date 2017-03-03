Name:           lcms2
Version:        2.8
Release:        1%{?dist}
Summary:        Color Management Engine
License:        MIT
URL:            http://www.littlecms.com/

Vendor:         bww bitwise works GmbH
%scm_source svn http://svn.netlabs.org/repos/ports/lcms2/trunk 2123

BuildRequires:  libjpeg-devel
BuildRequires:  libtiff-devel
BuildRequires:  zlib-devel

%description
LittleCMS intends to be a small-footprint, speed optimized color management
engine in open source form. LCMS2 is the current version of LCMS, and can be
parallel installed with the original (deprecated) lcms.

%package        utils
Summary:        Utility applications for %{name}
Group:          Applications/Productivity
Requires:       %{name} = %{version}-%{release}

%description    utils
The %{name}-utils package contains utility applications for %{name}.

%package        devel
Summary:        Development files for LittleCMS
Group:          Development/Libraries
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
export LDFLAGS=" -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export VENDOR="%{vendor}"

%configure --disable-static --enable-shared

make %{?_smp_mflags}

%install
rm -rf ${RPM_BUILD_ROOT}
make install DESTDIR=${RPM_BUILD_ROOT} INSTALL="install -p"
find ${RPM_BUILD_ROOT} -type f -name "*.la" -exec rm -f {} ';'

# install docs as this is all we've got
install -D -m 644 doc/LittleCMS2.?\ tutorial.pdf ${RPM_BUILD_ROOT}/%{_datadir}/doc/lcms2-devel-%{version}/tutorial.pdf
install -D -m 644 doc/LittleCMS2.?\ API.pdf ${RPM_BUILD_ROOT}%{_datadir}/doc/lcms2-devel-%{version}/api.pdf
install -D -m 644 doc/LittleCMS2.?\ Plugin\ API.pdf ${RPM_BUILD_ROOT}%{_datadir}/doc/lcms2-devel-%{version}/plugin-api.pdf

%clean
rm -rf ${RPM_BUILD_ROOT}

#%post -p /sbin/ldconfig

#%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING
%{_libdir}/*.dll

%files utils
%defattr(-,root,root,-)
%{_bindir}/*.exe
%{_mandir}/man1/*

%files devel
%defattr(-,root,root,-)
%{_datadir}/doc/lcms2-devel-%{version}/*.pdf
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Fri Mar 03 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.8-1
- update to vendor version 2.8
_ use scm_ macros

* Wed Mar 16 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.7-1
- remove dbg files from normal packages

* Thu Feb 16 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.7-0
- First release
