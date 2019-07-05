#define svn_url     F:/rd/ports/bzip2/trunk
%define svn_url     http://svn.netlabs.org/repos/ports/bzip2/trunk
%define svn_rev     192

Summary: A file compression utility
Name: bzip2
Version: 1.0.6
Release: 6%{?dist}
License: BSD
Group: Applications/File
URL: http://www.bzip.org/
Source: %{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip

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
Summary: Header files developing apps which will use bzip2
Group: Development/Libraries
Requires: bzip2-libs = %{version}-%{release}

%description devel
Header files and a library of bzip2 functions, for developing apps
which will use the library.

%package libs
Summary: Libraries for applications using bzip2
Group: System Environment/Libraries

%description libs
Libraries for applications using the bzip2 compression format.

%debug_package

%prep
%if %{?svn_rev:%(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')}%{!?svn_rev):0}
%setup -q
%else
%setup -n "%{name}-%{version}" -Tc
echo %{svn_rev}
svn export %{?svn_rev:-r %{svn_rev}} %{svn_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip" "%{name}-%{version}")
%endif

%build

make -f Makefile-libbz2_so CC="%{__cc}" AR="%{__ar}" RANLIB="%{__ranlib}" \
	CFLAGS="$RPM_OPT_FLAGS -D_FILE_OFFSET_BITS=64 -fpic -fPIC" \
	LDFLAGS="-g -Zbin-files -Zhigh-mem -Zdll -Zomf -Zargs-wild -Zargs-resp" \
	%{?_smp_mflags} dll

make CC="%{__cc}" AR="%{__ar}" RANLIB="%{__ranlib}" \
	CFLAGS="$RPM_OPT_FLAGS -D_FILE_OFFSET_BITS=64" \
	LDFLAGS="-g -Zbin-files -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp" \
	%{?_smp_mflags} all

%install
rm -rf ${RPM_BUILD_ROOT}

chmod 644 bzlib.h 
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
#mkdir -p $RPM_BUILD_ROOT%{_lib}
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_includedir}
cp -p bzlib.h $RPM_BUILD_ROOT%{_includedir}
install -m 755 libbz2.a $RPM_BUILD_ROOT/%{_libdir}
install -m 755 bzip2.exe  $RPM_BUILD_ROOT%{_bindir}
install -m 755 bzip2recover.exe bzgrep bzdiff bzmore  $RPM_BUILD_ROOT%{_bindir}/
cp -p bzip2.1 bzdiff.1 bzgrep.1 bzmore.1  $RPM_BUILD_ROOT%{_mandir}/man1/
cp bzip2.exe $RPM_BUILD_ROOT%{_bindir}/bunzip2.exe
cp bzip2.exe $RPM_BUILD_ROOT%{_bindir}/bzcat.exe
ln -s bzdiff $RPM_BUILD_ROOT%{_bindir}/bzcmp
ln -s bzmore $RPM_BUILD_ROOT%{_bindir}/bzless
cp bz2.dll $RPM_BUILD_ROOT/%{_libdir}
#ln -s ../../%{_lib}/libbz2.so.1 $RPM_BUILD_ROOT/%{_libdir}/libbz2.so
ln -s bzip2.1 $RPM_BUILD_ROOT%{_mandir}/man1/bzip2recover.1
ln -s bzip2.1 $RPM_BUILD_ROOT%{_mandir}/man1/bunzip2.1
ln -s bzip2.1 $RPM_BUILD_ROOT%{_mandir}/man1/bzcat.1
ln -s bzdiff.1 $RPM_BUILD_ROOT%{_mandir}/man1/bzcmp.1
ln -s bzmore.1 $RPM_BUILD_ROOT%{_mandir}/man1/bzless.1


#%post libs -p /sbin/ldconfig

#%postun libs  -p /sbin/ldconfig

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root,-)
%doc LICENSE CHANGES README 
%{_bindir}/*
%{_mandir}/*/*

%files libs
%defattr(-,root,root,-)
%doc LICENSE
%{_libdir}/*.dll

%files devel
%defattr(-,root,root,-)
%doc manual.html manual.pdf
%{_includedir}/*
%{_libdir}/*.a

%changelog
* Wed Jun 22 2016 yd <yd@os2power.com> 1.0.6-6
- rebuild package, fixes ticket#183.
- added debug package.
