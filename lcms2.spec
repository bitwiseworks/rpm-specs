Name:           lcms2
Version:        2.7
Release:        0%{?dist}
Summary:        Color Management Engine
License:        MIT
URL:            http://www.littlecms.com/
Vendor:         bww bitwise works GmbH
#Source0:        http://www.littlecms.com/lcms2-2.7.tar.gz

#define svn_url	    e:/trees/lcms2/trunk
%define svn_url     http://svn.netlabs.org/repos/ports/lcms2/trunk
%define svn_rev     1306

Source: %{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip

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
%if %{?svn_rev:%(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')}%{?!svn_rev):0}
%setup -q
%else
%setup -n "%{name}-%{version}" -Tc
svn export %{?svn_rev:-r %{svn_rev}} %{svn_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip" "%{name}-%{version}")
%endif

# hammer to nuke rpaths, recheck on new releases
export NOCONFIGURE=1
libtoolize -fc
autogen.sh

%build
export LDFLAGS=" -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
%configure --disable-static --enable-shared

make %{?_smp_mflags}

%install
rm -rf ${RPM_BUILD_ROOT}
make install DESTDIR=${RPM_BUILD_ROOT} INSTALL="install -p"
find ${RPM_BUILD_ROOT} -type f -name "*.la" -exec rm -f {} ';'

# install docs as this is all we've got
install -D -m 644 doc/LittleCMS2.?\ tutorial.pdf ${RPM_BUILD_ROOT}/%{_datadir}/doc/lcms2-devel-2.7/tutorial.pdf
install -D -m 644 doc/LittleCMS2.?\ API.pdf ${RPM_BUILD_ROOT}%{_datadir}/doc/lcms2-devel-2.7/api.pdf
install -D -m 644 doc/LittleCMS2.?\ Plugin\ API.pdf ${RPM_BUILD_ROOT}%{_datadir}/doc/lcms2-devel-2.7/plugin-api.pdf

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
%{_bindir}/*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root,-)
%{_datadir}/doc/lcms2-devel-2.7/*.pdf
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Thu Feb 16 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.7-0
- First release