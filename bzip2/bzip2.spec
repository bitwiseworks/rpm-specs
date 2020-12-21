%global library_version 1.0.8

Summary: A file compression utility
Name: bzip2
Version: 1.0.8
Release: 1%{?dist}
License: BSD
URL: http://www.bzip.org/
%if !0%{?os2_version}
#Source0: http://www.bzip.org/%{version}/%{name}-%{version}.tar.gz
Source0: https://sourceware.org/pub/bzip2/%{name}-%{version}.tar.gz
%else
%scm_source github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2
Vendor: bww bitwise works GmbH
%endif
Source1: bzip2.pc

%if !0%{?os2_version}
Patch0: bzip2-saneso.patch
Patch1: bzip2-cflags.patch
Patch2: bzip2-ldflags.patch
%endif

BuildRequires: gcc
BuildRequires: make

%description
Bzip2 is a freely available, patent-free, high quality data compressor.
Bzip2 compresses files to within 10 to 15 percent of the capabilities
of the best techniques available.  However, bzip2 has the added benefit
of being approximately two times faster at compression and six times
faster at decompression than those techniques.  Bzip2 is not the
fastest compression utility, but it does strike a balance between speed
and compression capability.

Install bzip2 if you need a compression utility.

%package devel
Summary: Libraries and header files for apps which will use bzip2
Requires: bzip2-libs = %{version}-%{release}

%description devel

Header files and a library of bzip2 functions, for developing apps
which will use the library.

%package libs
Summary: Libraries for applications using bzip2

%description libs

Libraries for applications using the bzip2 compression format.

%package static
Summary: Libraries for applications using bzip2

%description static

Static libraries for applications using the bzip2 compression format.

%if 0%{?os2_version}
%debug_package
%endif

%prep
%if !0%{?os2_version}
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%else
%scm_setup
%endif

cp -a %{SOURCE1} .
sed -i "s|^libdir=|libdir=%{_libdir}|" bzip2.pc
%if 0%{?os2_version}
sed -i "s|^Version:|Version: %{version}|" bzip2.pc
%endif

%build
%if 0%{?rhel} >= 7
    %ifarch ppc64
        export O3="-O3"
    %else
        export O3=""
    %endif
%else
    export O3=""
%endif

%if !0%{?os2_version}
%make_build -f Makefile-libbz2_so CC="%{__cc}" AR="%{__ar}" RANLIB="%{__ranlib}" \
    CFLAGS="$RPM_OPT_FLAGS -D_FILE_OFFSET_BITS=64 -fpic -fPIC $O3" \
    LDFLAGS="%{__global_ldflags}" \
    all
%else
export VENDOR="%{vendor}"
LDFLAGS="-g -Zhigh-mem -Zdll -Zomf -Zargs-wild -Zargs-resp -lcx"
make        -f Makefile-libbz2_so CC="gcc" AR="%{__ar}" RANLIB="%{__ranlib}" \
    CFLAGS="$RPM_OPT_FLAGS -D_FILE_OFFSET_BITS=64 -fpic -fPIC $O3" \
    LDFLAGS="$LDFLAGS" \
    dll
%endif

rm -f *.o
%if !0%{?os2_version}
%make_build CC="%{__cc}" AR="%{__ar}" RANLIB="%{__ranlib}" \
    CFLAGS="$RPM_OPT_FLAGS -D_FILE_OFFSET_BITS=64 $O3" \
    LDFLAGS="%{__global_ldflags}" \
    all
%else
LDFLAGS="-g -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"
make CC="gcc" AR="%{__ar}" RANLIB="%{__ranlib}" \
    CFLAGS="$RPM_OPT_FLAGS -D_FILE_OFFSET_BITS=64 $O3" \
    LDFLAGS="$LDFLAGS" \
    all
%endif

%install
chmod 644 bzlib.h
%if !0%{?os2_version}
mkdir -p $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1,%{_libdir}/pkgconfig,%{_includedir}}
%else
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
mkdir -p $RPM_BUILD_ROOT%{_libdir}/pkgconfig
mkdir -p $RPM_BUILD_ROOT%{_includedir}
%endif
cp -p bzlib.h $RPM_BUILD_ROOT%{_includedir}
%if !0%{?os2_version}
install -m 755 libbz2.so.%{library_version} $RPM_BUILD_ROOT%{_libdir}
install -m 644 libbz2.a $RPM_BUILD_ROOT%{_libdir}
install -m 755 bzip2-shared  $RPM_BUILD_ROOT%{_bindir}/bzip2
install -m 755 bzip2recover bzgrep bzdiff bzmore  $RPM_BUILD_ROOT%{_bindir}/
%else
install -m 755 bz2.dll $RPM_BUILD_ROOT/%{_libdir}
install -m 644 libbz2_dll.a $RPM_BUILD_ROOT/%{_libdir}
install -m 644 libbz2.a $RPM_BUILD_ROOT/%{_libdir}
install -m 755 bzip2.exe  $RPM_BUILD_ROOT%{_bindir}
install -m 755 bzip2recover.exe bzgrep bzdiff bzmore  $RPM_BUILD_ROOT%{_bindir}/
%endif
install -m 644 bzip2.pc $RPM_BUILD_ROOT%{_libdir}/pkgconfig/bzip2.pc
cp -p bzip2.1 bzdiff.1 bzgrep.1 bzmore.1  $RPM_BUILD_ROOT%{_mandir}/man1/
%if !0%{?os2_version}
ln -s bzip2 $RPM_BUILD_ROOT%{_bindir}/bunzip2
ln -s bzip2 $RPM_BUILD_ROOT%{_bindir}/bzcat
%else
cp bzip2.exe $RPM_BUILD_ROOT%{_bindir}/bunzip2.exe
cp bzip2.exe $RPM_BUILD_ROOT%{_bindir}/bzcat.exe
%endif
ln -s bzdiff $RPM_BUILD_ROOT%{_bindir}/bzcmp
ln -s bzmore $RPM_BUILD_ROOT%{_bindir}/bzless
ln -s bzgrep $RPM_BUILD_ROOT%{_bindir}/bzegrep
ln -s bzgrep $RPM_BUILD_ROOT%{_bindir}/bzfgrep
%if !0%{?os2_version}
ln -s libbz2.so.%{library_version} $RPM_BUILD_ROOT%{_libdir}/libbz2.so.1
ln -s libbz2.so.1 $RPM_BUILD_ROOT%{_libdir}/libbz2.so
%endif
ln -s bzip2.1 $RPM_BUILD_ROOT%{_mandir}/man1/bzip2recover.1
ln -s bzip2.1 $RPM_BUILD_ROOT%{_mandir}/man1/bunzip2.1
ln -s bzip2.1 $RPM_BUILD_ROOT%{_mandir}/man1/bzcat.1
ln -s bzdiff.1 $RPM_BUILD_ROOT%{_mandir}/man1/bzcmp.1
ln -s bzmore.1 $RPM_BUILD_ROOT%{_mandir}/man1/bzless.1
ln -s bzgrep.1 $RPM_BUILD_ROOT%{_mandir}/man1/bzegrep.1
ln -s bzgrep.1 $RPM_BUILD_ROOT%{_mandir}/man1/bzfgrep.1

%if !0%{?os2_version}
%ldconfig_scriptlets libs
%endif

%files
%doc LICENSE CHANGES README
%{!?_licensedir:%global license %%doc}
%license LICENSE
%{_bindir}/*
%if 0%{?os2_version}
%exclude %{_bindir}/*.dbg
%endif
%{_mandir}/*/*

%files libs
%{!?_licensedir:%global license %%doc}
%license LICENSE
%if !0%{?os2_version}
%{_libdir}/libbz2.so.1*
%else
%{_libdir}/*.dll
%endif

%files static
%{!?_licensedir:%global license %%doc}
%license LICENSE
%{_libdir}/libbz2.a

%files devel
%doc manual.html manual.pdf
%{_includedir}/*
%if !0%{?os2_version}
%{_libdir}/*.so
%else
%{_libdir}/*_dll.a
%endif
%{_libdir}/pkgconfig/bzip2.pc

%changelog
* Mon Dec 21 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.0.8-1
- updated to version 1.0.8
- resynced the spec with fedora

* Wed Jun 22 2016 yd <yd@os2power.com> 1.0.6-6
- rebuild package, fixes ticket#183.
- added debug package.
