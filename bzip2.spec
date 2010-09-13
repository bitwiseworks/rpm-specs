%define library_version 1.0.5

Summary: A file compression utility
Name: bzip2
Version: 1.0.5
Release: 1
License: BSD
Group: Applications/File
URL: http://www.bzip.org/
Source: http://www.bzip.org/%{version}/bzip2-%{version}.tar.gz
Patch0: bzip2-1.0.5-setmode.diff
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

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

%prep
# -D Do not delete the directory before unpacking.
# -T Disable the automatic unpacking of the archives.
%setup
%patch0 -p1 -b .setmode~

%build

make CC="%{__cc}" AR="%{__ar}" RANLIB="%{__ranlib}" \
	CFLAGS="$RPM_OPT_FLAGS -D_FILE_OFFSET_BITS=64" \
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
#ln -s libbz2.so.%{library_version} $RPM_BUILD_ROOT/%{_lib}/libbz2.so.1
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
#/%{_lib}/*so.*

%files devel
%defattr(-,root,root,-)
%doc manual.html manual.pdf
%{_includedir}/*
/%{_libdir}/*.a

%changelog
