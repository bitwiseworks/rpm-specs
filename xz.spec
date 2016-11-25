#define svn_url     F:/rd/ports/xz/trunk
%define svn_url     http://svn.netlabs.org/repos/ports/xz/trunk
%define svn_rev     1831

# enable the forwarder section if needed
%global with_forwarder 0

# Not needed for f21+ and probably RHEL8+
%{!?_licensedir:%global license %%doc}

Name:           xz
Summary:	LZMA compression utilities
Version:        5.2.2
Release:        1%{?dist}
Group:          Applications/File

# Scripts xz{grep,diff,less,more} and symlinks (copied from gzip) are
# GPLv2+, binaries are Public Domain (linked against LGPL getopt_long but its
# OK), documentation is Public Domain.
License:        GPLv2+ and Public Domain
URL:		http://tukaani.org/%{name}/
Vendor:         bww bitwise works GmbH

Source: %{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip

# DEF files to create forwarders for the legacy package
Source10:       lzma.def

Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
Requires:       libcx >= 0.4

# For /usr/libexec/grepconf.sh (RHBZ#1189120).
# Unfortunately F21 has a newer version of grep which doesn't
# have grepconf, but we're only concerned with F22 here.
Requires:	grep >= 2.20-5

BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
XZ Utils are an attempt to make LZMA compression easy to use on free (as in
freedom) operating systems. This is achieved by providing tools and libraries
which are similar to use than the equivalents of the most popular existing
compression algorithms.

LZMA is a general purpose compression algorithm designed by Igor Pavlov as
part of 7-Zip. It provides high compression ratio while keeping the
decompression speed fast.

%package 	libs
Summary:	Libraries for decoding LZMA compression
Group:		System Environment/Libraries
License:	Public Domain
Obsoletes:	%{name}-compat-libs < %{version}-%{release}

%description 	libs
Libraries for decoding files compressed with LZMA or XZ utils.

%package 	devel
Summary:	Devel libraries & headers for liblzma
Group:		Development/Libraries
License:	Public Domain
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
Requires:	pkgconfig

%description	devel
Devel libraries and headers for liblzma.

%package 	lzma-compat
Summary:	Older LZMA format compatibility binaries
Group:		Development/Libraries
# Just a set of symlinks to 'xz' + two Public Domain binaries.
License:	Public Domain
Requires:	%{name}%{?_isa} = %{version}-%{release}
Obsoletes:	lzma < %{version}
Provides:	lzma = %{version}

%description	lzma-compat
The lzma-compat package contains compatibility links for older
commands that deal with the older LZMA format.

%debug_package

%prep
%if %{?svn_rev:%(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')}%{!?svn_rev):0}
%setup -q
%else
%setup -n "%{name}-%{version}" -Tc
svn export %{?svn_rev:-r %{svn_rev}} %{svn_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip" "%{name}-%{version}")
%endif

# Prepare forwarder DLLs.
for m in %{SOURCE10}; do
  cp ${m} .
done

autoreconf -fvi

%build

export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx -lpthread"
export VENDOR="%{vendor}"
%configure --enable-shared --disable-static

make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_libdir}/*.la

%if 0%{?with_forwarder}
# Generate & install forwarder DLLs.
gcc -Zomf -Zdll lzma.def -l$RPM_BUILD_ROOT/%{_libdir}/lzma5.dll -o $RPM_BUILD_ROOT/%{_libdir}/lzma.dll
%endif

%find_lang %name

%clean
rm -fr $RPM_BUILD_ROOT

%check
#LD_LIBRARY_PATH=$PWD/src/liblzma/.libs make check

#%post libs -p /sbin/ldconfig

#%postun libs -p /sbin/ldconfig

%files -f %{name}.lang
%license %{_docdir}/xz/COPYING*
%doc %{_docdir}/xz
%exclude %{_docdir}/xz/examples*
%{_bindir}/*xz*
%exclude %{_bindir}/*.dbg
%{_mandir}/man1/*xz*

%files libs
%license %{_docdir}/xz/COPYING
%{_libdir}/*.dll

%files devel
%dir %{_includedir}/lzma
%{_includedir}/lzma/*.h
%{_includedir}/lzma.h
%{_libdir}/*_dll.a
%{_libdir}/pkgconfig/liblzma.pc
%doc %{_docdir}/xz/examples*

%files lzma-compat
%{_bindir}/*lz*
%exclude %{_bindir}/*.dbg
%{_mandir}/man1/*lz*

%changelog
* Fri Nov 25 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> 5.2.2-1
- update to version 5.2.2

* Mon Jun 13 2016 yd <yd@os2power.com> 4.999.9beta-5
- rebuild package, fixes ticket#183.
- added debug package.
