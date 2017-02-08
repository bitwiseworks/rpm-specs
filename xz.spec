# Not needed for f21+ and probably RHEL8+
%{!?_licensedir:%global license %%doc}

Name:           xz
Summary:        LZMA compression utilities
Version:        5.2.3
Release:        1%{?dist}
Group:          Applications/File

# Scripts xz{grep,diff,less,more} and symlinks (copied from gzip) are
# GPLv2+, binaries are Public Domain (linked against LGPL getopt_long but its
# OK), documentation is Public Domain.
License:        GPLv2+ and Public Domain
URL:            http://tukaani.org/%{name}/

Vendor:         bww bitwise works GmbH
%scm_source  svn http://svn.netlabs.org/repos/ports/xz/trunk 1995

Requires:       %{name}-libs = %{version}-%{release}
Requires:       libcx >= 0.4

# For /usr/libexec/grepconf.sh (RHBZ#1189120).
# Unfortunately F21 has a newer version of grep which doesn't
# have grepconf, but we're only concerned with F22 here.
Requires:       grep >= 2.20-5

BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
XZ Utils are an attempt to make LZMA compression easy to use on free (as in
freedom) operating systems. This is achieved by providing tools and libraries
which are similar to use than the equivalents of the most popular existing
compression algorithms.

LZMA is a general purpose compression algorithm designed by Igor Pavlov as
part of 7-Zip. It provides high compression ratio while keeping the
decompression speed fast.

%package        libs
Summary:        Libraries for decoding LZMA compression
Group:          System Environment/Libraries
License:        Public Domain
Obsoletes:      %{name}-compat-libs < %{version}-%{release}

%description    libs
Libraries for decoding files compressed with LZMA or XZ utils.

%package        devel
Summary:        Devel libraries & headers for liblzma
Group:          Development/Libraries
License:        Public Domain
Requires:       %{name}-libs = %{version}-%{release}
Requires:       pkgconfig

%description    devel
Devel libraries and headers for liblzma.

%package        lzma-compat
Summary:        Older LZMA format compatibility binaries
Group:	        Development/Libraries
# Just a set of symlinks to 'xz' + two Public Domain binaries.
License:        Public Domain
Requires:       %{name} = %{version}-%{release}
Obsoletes:      lzma < %{version}
Provides:       lzma = %{version}

%description    lzma-compat
The lzma-compat package contains compatibility links for older
commands that deal with the older LZMA format.

%legacy_runtime_packages

%debug_package

%prep
%scm_setup

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
%exclude %{_libdir}/lzma.dll

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
* Wed Feb 08 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 5.2.3-1
- update to version 5.2.3
- use the new scm_source and scm_setup macros
- don't use a forwarder, use the legacy script

* Fri Nov 25 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> 5.2.2-1
- update to version 5.2.2

* Mon Jun 13 2016 yd <yd@os2power.com> 4.999.9beta-5
- rebuild package, fixes ticket#183.
- added debug package.
