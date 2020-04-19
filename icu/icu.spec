#%%global debugtrace 1
%global with_test 0

Name:      icu
Version:   65.1
Release:   1%{?dist}
Summary:   International Components for Unicode

License:   MIT and UCD and Public Domain
URL:       http://site.icu-project.org/
Vendor:    bww bitwise works GmbH

#scm_source github http://github.com(bitwiseworks/%{name}-os2 %{version}-os2
%scm_source git e:/trees/icu/git %{version}-os2

BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: doxygen, autoconf, python
Requires: lib%{name} = %{version}-%{release}

%description
Tools and utilities for developing with icu.

%package -n lib%{name}
Summary: International Components for Unicode - libraries

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
Requires: lib%{name} = %{version}-%{release}
Requires: pkgconfig

%description -n lib%{name}-devel
Includes and definitions for developing with icu.

%package -n lib%{name}-doc
Summary: Documentation for International Components for Unicode
BuildArch: noarch

%description -n lib%{name}-doc
%{summary}.

%if !0%{os2_version}
%{!?endian: %global endian %(%{__python} -c "import sys;print (0 if sys.byteorder=='big' else 1)")}
# " this line just fixes syntax highlighting for vim that is confused by the above and continues literal
%endif

%debug_package


%prep
%scm_setup


%build

cd source
autoreconf -fvi
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"
export VENDOR="%{vendor}"

#rhbz856594 do not use --disable-renaming or cope with the mess
OPTIONS='--with-data-packaging=library --disable-samples'
%if 0%{?debugtrace}
OPTIONS=$OPTIONS' --enable-debug --enable-tracing'
%endif

# We deal with the mess it seems :)
# We use --disable-renaming in configure options to build a non-versioned librariy for
# system-wide installation on OS/2. This installation also requires hiding draft and
# deprecated API to maintain backward ABI compatibility (see
# http://userguide.icu-project.org/design#TOC-ICU-Binary-Compatibility:-Using-ICU-as-an-Operating-System-Level-Library).
# Note that we cannot use --disable-draft because it defines U_HIDE_INTERNAL_API but
# this breaks the build (upstream bug). Note that we also cannot use U_HIDE_SYSTEM_API
# or U_HIDE_DEPRECATED_API (despite readme.html recommedation) for the same reason...
# Note that we actually can't use U_HIDE_DRAFT_API... This part of ICU is really broken.
# And the open source model is really evil. Really. Low code quality.
%if 0%{os2_version}
OPTIONS=$OPTIONS' --disable-renaming --enable-shared --disable-static'
%endif
%configure $OPTIONS

#rhbz#225896
%if !0%{os2_version}
sed -i 's|-nodefaultlibs -nostdlib||' config/mh-linux
%endif
#rhbz#813484
sed -i 's| \$(docfilesdir)/installdox||' Makefile
# There is no source/doc/html/search/ directory
sed -i '/^\s\+\$(INSTALL_DATA) \$(docsrchfiles) \$(DESTDIR)\$(docdir)\/\$(docsubsrchdir)\s*$/d' Makefile
# rhbz#856594 The configure --disable-renaming and possibly other options
# result in icu/source/uconfig.h.prepend being created, include that content in
# icu/source/common/unicode/uconfig.h to propagate to consumer packages.
test -f uconfig.h.prepend && sed -e '/^#define __UCONFIG_H__/ r uconfig.h.prepend' -i common/unicode/uconfig.h

# more verbosity for build.log
sed -i -r 's|(PKGDATA_OPTS = )|\1-v |' data/Makefile

make %{?_smp_mflags} VERBOSE=1
make %{?_smp_mflags} doc


%install
rm -rf $RPM_BUILD_ROOT source/__docs
make %{?_smp_mflags} -C source install DESTDIR=$RPM_BUILD_ROOT
make %{?_smp_mflags} -C source install-doc docdir=__docs
%if !0%{os2_version}
chmod +x $RPM_BUILD_ROOT%{_libdir}/*.so.*
(
 cd $RPM_BUILD_ROOT%{_bindir}
 mv icu-config icu-config-%{__isa_bits}
)
install -p -m755 -D %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/icu-config
%endif

%check
# test to ensure that -j(X>1) didn't "break" man pages. b.f.u #2357
if grep -q @VERSION@ source/tools/*/*.8 source/tools/*/*.1 source/config/*.1; then
    exit 1
fi
%if 0%{?with_test}
make %{?_smp_mflags} -C source check
%endif

# log available codes
%if !0%{os2_version}
pushd source
LD_LIBRARY_PATH=lib:stubdata:tools/ctestfw:$LD_LIBRARY_PATH bin/uconv -l
%endif


%if !0%{os2_version}
%ldconfig_scriptlets -n lib%{name}
%endif


%files
%license license.html
%exclude %{_datadir}/%{name}/*/LICENSE
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
%license LICENSE
%doc readme.html
%{_libdir}/*.dll

%files -n lib%{name}-devel
%license LICENSE
%doc source/samples/
%{_bindir}/%{name}-config
%{_bindir}/icuinfo.exe
%{_mandir}/man1/%{name}-config.1*
%{_mandir}/man1/icuinfo.1*
%{_includedir}/unicode
%{_libdir}/*_dll.a
%{_libdir}/pkgconfig/*.pc
%{_libdir}/%{name}
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/%{version}
%{_datadir}/%{name}/%{version}/install-sh
%{_datadir}/%{name}/%{version}/mkinstalldirs
%{_datadir}/%{name}/%{version}/config

%files -n lib%{name}-doc
%license LICENSE
%doc readme.html
%doc source/__docs/%{name}/html/*


%changelog
* Wed Apr 15 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> 65.1-1
- moved source to github
- enable doxygen
- add bldlevel to the dll
- update to latest source

* Wed Dec 27 2017 Dmitriy Kuminov <coding@dmik.org> 56.1-2
- Build with high memory support.
- Use scm_source macro and friends.

* Tue Mar 15 2016 Dmitriy Kuminov <coding@dmik.org> 56.1-1
- Initial package for version 56.1.
