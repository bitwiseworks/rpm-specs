# Note: this .spec is borrowed from icu-56.1-3.fc24.src.rpm

Name:      icu
Version:   56.1
Release:   2%{?dist}
Summary:   International Components for Unicode
Group:     Development/Tools
License:   MIT and UCD and Public Domain
URL:       http://www.icu-project.org/
#Source0:   http://download.icu-project.org/files/icu4c/56.1/icu4c-56_1-src.tgz

# @todo (dmik) no doxygen RPM yet
#BuildRequires: doxygen
BuildRequires: autoconf
Requires: lib%{name}%{?_isa} = %{version}-%{release}

%scm_source svn http://svn.netlabs.org/repos/ports/icu/trunk 1388

BuildRequires: gcc make

Patch4: gennorm2-man.patch
Patch5: icuinfo-man.patch

%description
Tools and utilities for developing with icu.

%package -n lib%{name}
Summary: International Components for Unicode - libraries
Group:   System Environment/Libraries

%description -n lib%{name}
The International Components for Unicode (ICU) libraries provide
robust and full-featured Unicode services on a wide variety of
platforms. ICU supports the most current version of the Unicode
standard, and they provide support for supplementary Unicode
characters (needed for GB 18030 repertoire support).
As computing environments become more heterogeneous, software
portability becomes more important. ICU lets you produce the same
results across all the various platforms you support, without
sacrificing performance. It offers great flexibility to extend and
customize the supplied services.

%package  -n lib%{name}-devel
Summary:  Development files for International Components for Unicode
Group:    Development/Libraries
Requires: lib%{name}%{?_isa} = %{version}-%{release}
Requires: pkgconfig

%description -n lib%{name}-devel
Includes and definitions for developing with icu.

# @todo (dmik) no doxygen RPM yet
#%package -n lib%{name}-doc
#Summary: Documentation for International Components for Unicode
#Group:   Documentation
#BuildArch: noarch

# @todo (dmik) no doxygen RPM yet
#%description -n lib%{name}-doc
#%{summary}.

%prep

%scm_setup

%patch4 -p1
%patch5 -p1

%build

cd source
autoreconf -fvi
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
%configure --with-data-packaging=library --disable-samples \
           --disable-renaming \
           --enable-shared --disable-static

# The configure --disable-renaming and possibly other options
# result in icu/source/uconfig.h.prepend being created, include that content in
# icu/source/common/unicode/uconfig.h to propagate to consumer packages.
test -f uconfig.h.prepend && sed -e '/^#define __UCONFIG_H__/ r uconfig.h.prepend' -i common/unicode/uconfig.h

# We use --disable-renaming in configure options to build a non-versioned librariy for
# system-wide installation on OS/2. This installation also requires hiding draft and
# deprecated API to maintain backward ABI compatibility (see
# http://userguide.icu-project.org/design#TOC-ICU-Binary-Compatibility:-Using-ICU-as-an-Operating-System-Level-Library).
# Note that we cannot use --disable-draft because it defines U_HIDE_INTERNAL_API but
# this breaks the build (upstream bug). Note that we also cannot use U_HIDE_SYSTEM_API
# or U_HIDE_DEPRECATED_API (despite readme.html recommedation) for the same reason...
# Note that we actually can't use U_HIDE_DRAFT_API... This part of ICU is really broken.
# And the open source model is really evil. Really. Low code quality.
#echo '
##define U_HIDE_DRAFT_API 1
#' > uconfig.h.prepend
#sed -e '/^#define __UCONFIG_H__/ r uconfig.h.prepend' -i common/unicode/uconfig.h

make %{?_smp_mflags}
# @todo (dmik) no doxygen RPM yet
#make %{?_smp_mflags} doc

%install

# @todo (dmik) no doxygen RPM yet
#rm -rf $RPM_BUILD_ROOT source/__docs
make %{?_smp_mflags} -C source install DESTDIR=$RPM_BUILD_ROOT

# @todo (dmik) no doxygen RPM yet
#make %{?_smp_mflags} -C source install-doc docdir=__docs

%check

# test to ensure that -j(X>1) didn't "break" man pages. b.f.u #2357
if grep -q @VERSION@ source/tools/*/*.8 source/tools/*/*.1 source/config/*.1; then
    exit 1
fi
# make %{?_smp_mflags} -C source check

%files
%defattr(-,root,root,-)
%{_bindir}/derb.exe
%{_bindir}/genbrk.exe
%{_bindir}/gencfu.exe
%{_bindir}/gencnval.exe
%{_bindir}/gendict.exe
%{_bindir}/genrb.exe
%{_bindir}/makeconv.exe
%{_bindir}/pkgdata.exe
%{_bindir}/uconv.exe
%{_sbindir}/*
%{_mandir}/man1/derb.1*
%{_mandir}/man1/gencfu.1*
%{_mandir}/man1/gencnval.1*
%{_mandir}/man1/gendict.1*
%{_mandir}/man1/genrb.1*
%{_mandir}/man1/genbrk.1*
%{_mandir}/man1/makeconv.1*
%{_mandir}/man1/pkgdata.1*
%{_mandir}/man1/uconv.1*
%{_mandir}/man8/*.8*

%files -n lib%{name}
%defattr(-,root,root,-)
%doc license.html readme.html
%{_libdir}/*.dll

%files -n lib%{name}-devel
%defattr(-,root,root,-)
%{_bindir}/%{name}-config
%{_bindir}/icuinfo.exe
%{_mandir}/man1/%{name}-config.1*
%{_mandir}/man1/icuinfo.1*
%{_includedir}/layout
%{_includedir}/unicode
%{_libdir}/*_dll.a
%{_libdir}/pkgconfig/*.pc
%{_libdir}/%{name}
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/%{version}
%{_datadir}/%{name}/%{version}/install-sh
%{_datadir}/%{name}/%{version}/mkinstalldirs
%{_datadir}/%{name}/%{version}/config
%doc %{_datadir}/%{name}/%{version}/license.html

# @todo (dmik) no doxygen RPM yet
#%files -n lib%{name}-doc
#%defattr(-,root,root,-)
#%doc license.html readme.html
#%doc source/__docs/%{name}/html/*

%changelog
* Wed Dec 27 2017 Dmitriy Kuminov <coding@dmik.org> 56.1-2
- Build with high memory support.
- Use scm_source macro and friends.

* Tue Mar 15 2016 Dmitriy Kuminov <coding@dmik.org> 56.1-1
- Initial package for version 56.1.
