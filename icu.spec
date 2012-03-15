%global _icu_full_version 4.2.1
%global _icu_dll_version 42

Summary:        International Components for Unicode
Name:           icu
License:        X11/MIT
Group:          System/Libraries
Version:        %{_icu_full_version}
Release:        1%{?dist}
Requires:       libicu = %{version}
Url:            http://ibm.com/software/globalization/icu

Source0:        icu4c-4_2_1-src.tgz
Source1:        icu-mh-os2
Patch0:         icu-os2.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
ICU is a set of C and C++ libraries that provides robust and
full-featured Unicode and locale support. The library provides calendar
support, conversions for many character sets, language sensitive
collation, date and time formatting, support for many locales, message
catalogs and resources, message formatting, normalization, number and
currency formatting, time zone support, transliteration, and word,
line, and sentence breaking, etc.

This package contains the Unicode character database and derived
properties along with converters and time zone data.

This package contains the runtime libraries for ICU. It does not
contain any of the data files needed at runtime and present in the icu
and icu-locales packages.



Authors:
--------
    The ICU project, International Business Machines (IBM) and Others.  <icu@oss.software.ibm.com>

%package -n libicu
License:        IBM Public License
Summary:        International Components for Unicode (development files)
Group:          Development/Libraries/C and C++

%description -n libicu
ICU is a set of C and C++ libraries that provides robust and
full-featured Unicode support. This package contains the runtime
libraries for ICU. It does not contain any of the data files needed at
runtime and present in the `icu' and `icu-locales` packages.



Authors:
--------
    The ICU project, International Business Machines (IBM) and Others.  <icu@oss.software.ibm.com>

%package -n libicu-devel
License:        IBM Public License
Summary:        International Components for Unicode (development files)
Group:          Development/Libraries/C and C++
Requires:       libicu = %{version}

%description -n libicu-devel
ICU is a C++ and C library that provides robust and full-featured
Unicode support. This package contains the development files for ICU.



Authors:
--------
    The ICU project, International Business Machines (IBM) and Others.  <icu@oss.software.ibm.com>

%package -n libicu-doc
License:        IBM Public License
Summary:        International Components for Unicode  (html documentation)
Group:          Development/Libraries/C and C++

%description -n libicu-doc
ICU is a C++ and C library that provides robust and full-featured
Unicode support. This package contains the html documentation.



Authors:
--------
    The ICU project, International Business Machines (IBM) and Others.  <icu@oss.software.ibm.com>

%package -n icu-data
License:        IBM Public License
Summary:        International Components for Unicode (Sources for the Data in ICU)
Group:          System/Libraries
Requires:       libicu >= %{version}

%description -n icu-data
ICU is a C++ and C library that provides robust and full-featured
Unicode support. This package contains the source files for the data
found in the "icu" package.

This data describes the Unicode data (normative and informative) and
also all the table-based converters provided in the ICU distribution.

This package contains uncompiled source data. Precompiled data is in
the `libicu%{version}' package.



Authors:
--------
    The ICU project, International Business Machines (IBM) and Others.  <icu@oss.software.ibm.com>

%prep
%setup -q -n icu
%patch0 -p1

cp %{SOURCE1} source/config/mh-os2

%build

cd source
rm -f config.cache

script_dir=%{_topdir}/BUILD/%{name}/source
export PATH="$script_dir/bin${PATH:+;$PATH}"
export BEGINLIBPATH="$script_dir/lib;$script_dir/stubdata;$script_dir/tools/ctestfw;${BEGINLIBPATH:+;$BEGINLIBPATH}"
export LIBPATHSTRICT=T

#force libc to use sh for system() in pkgdata.exe
export EEEMXSHELL="sh"

export CONFIG_SHELL="/@unixroot/usr/bin/sh.exe"
export LDFLAGS="-Zomf -Zhigh-mem"
export LIBS="-lurpo -lpthread"
%configure \
    --disable-static \
    --enable-shared \
    --without-samples \
   "--cache-file=%{_topdir}/cache/%{name}-%{_target_cpu}.cache"
make %{?_smp_mflags}

%install
rm -rf ${RPM_BUILD_ROOT}

script_dir=%{_topdir}/BUILD/%{name}/source
export PATH="$script_dir/bin${PATH:+;$PATH}"
export BEGINLIBPATH="$script_dir/lib;$script_dir/stubdata;$script_dir/tools/ctestfw;${BEGINLIBPATH:+;$BEGINLIBPATH}"
export LIBPATHSTRICT=T

cd source
make DESTDIR=$RPM_BUILD_ROOT install
# to extract debug info
#chmod a+rx $RPM_BUILD_ROOT%{_libdir}/*.so.*
# install uncompiled source data:
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icu/%{version}/unidata
install -m 644 data/unidata/*.txt $RPM_BUILD_ROOT%{_datadir}/icu/%{version}/unidata
ln -s unidata/UnicodeData.txt $RPM_BUILD_ROOT%{_datadir}/icu/%{version}/

rm $RPM_BUILD_ROOT%{_libdir}/*.a.bak
rm $RPM_BUILD_ROOT%{_libdir}/icu??.dll
rm $RPM_BUILD_ROOT%{_libdir}/icudt??.dll
mv $RPM_BUILD_ROOT%{_libdir}/icudt%{_icu_dll_version}.1.dll $RPM_BUILD_ROOT%{_libdir}/icudt%{_icu_dll_version}.dll

# run test suite:
#pushd data
#ln -sf build/*.cnv build/*.res build/*.dat build/*.brk .
#popd
#make check || echo "make check returned $?, ignored."
#popd
rm $RPM_BUILD_ROOT/%{_datadir}/icu/%{version}/license.html
rm $RPM_BUILD_ROOT/%{_datadir}/icu/%{version}/install-sh

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%doc license.html readme.html
%dir %{_libdir}/icu/
%dir %{_libdir}/icu/%{version}
%{_libdir}/icu/current
%{_bindir}/derb.exe
%{_bindir}/genbrk.exe
%{_bindir}/gencfu.exe
%{_bindir}/gencnval.exe
%{_bindir}/genrb.exe
%{_bindir}/genctd.exe
%{_bindir}/makeconv.exe
%{_bindir}/pkgdata.exe
%{_bindir}/uconv.exe
%{_mandir}/*/*

%files -n libicu
%defattr(-, root, root)
%attr (755, root, root) %{_libdir}/*.dll

%files -n libicu-devel
%defattr(-, root, root)
%{_libdir}/*.a
%{_includedir}/unicode/
%{_includedir}/layout/
%{_libdir}/icu/%{version}/Makefile.inc
%{_libdir}/icu/%{version}/pkgdata.inc
%{_libdir}/icu/Makefile.inc
%{_libdir}/icu/pkgdata.inc
%{_bindir}/icu-config
%dir %{_datadir}/icu
%dir %{_datadir}/icu/%{version}
%{_datadir}/icu/%{version}/mkinstalldirs
%{_datadir}/icu/%{version}/config/
%{_sbindir}/*.exe

#%files -n libicu-doc
#%defattr(-, root, root)
#%doc html/

%files -n icu-data
%defattr(-, root, root)
%{_datadir}/icu/%{version}/unidata/
%{_datadir}/icu/%{version}/UnicodeData.txt

%changelog
