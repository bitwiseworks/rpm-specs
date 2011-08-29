Summary: The zlib compression and decompression library.
Name: zlib
Version: 1.2.5
Release: 3%{?dist}
License: BSD
Group: System Environment/Libraries
URL: http://www.zlib.net
Source: %url/zlib-%version.tar.bz2
Patch0: zlib-os2.diff
Prefix: %_prefix
BuildRoot: /override/%name-%version

%description
The zlib compression library provides in-memory compression and
decompression functions, including integrity checks of the uncompressed
data.  This version of the library supports only one compression method
(deflation), but other algorithms may be added later, which will have
the same stream interface.  The zlib library is used by many different
system programs.

%package devel
Summary: Header files and libraries for developing apps which will use zlib.
Group: Development/Libraries
Requires: %name = %version-%release

%description devel
The zlib-devel package contains the header files and libraries needed to
develop programs that use the zlib compression and decompression library.

%prep
%setup -q
%patch0 -p0 -b .os2~

# Use optflags_lib for this package if defined.
%{expand:%%define optflags %{?optflags_lib:%optflags_lib}%{!?optflags_lib:%optflags} -Wall}

%build
# first build and test static zlib
export TEST_LDFLAGS="-Zomf"
CFLAGS="%optflags" \
./configure --prefix=/@unixroot/usr --static

! grep -wE 'NO_vsnprintf|HAS_vsprintf_void|HAS_vsnprintf_void|NO_snprintf|HAS_sprintf_void|HAS_snprintf_void' Makefile
%__make
%__make z.dll

%{!?_without_check:%{!?_without_test:%__make test}}
rm -f *.s *.o

# next build and test shared zlib
#CFLAGS="%optflags -fPIC" ./configure --prefix=%_prefix --shared
#! grep -wE 'NO_vsnprintf|HAS_vsprintf_void|HAS_vsnprintf_void|NO_snprintf|HAS_sprintf_void|HAS_snprintf_void' Makefile
#%__make
#%{!?_without_check:%{!?_without_test:%__make test}}

#bzip2 -9fk ChangeLog FAQ algorithm.txt

%install
rm -rf %buildroot
mkdir -p %buildroot%_libdir
mkdir -p %buildroot%_includedir
mkdir -p %buildroot%_mandir/man3

cp -a libz.a %buildroot%_libdir/
cp -a libz_s.a %buildroot%_libdir/
cp -a z.dll %buildroot%_libdir/

install -p -m644 zlib.h zconf.h %buildroot%_includedir/
install -p -m644 zlib.3 %buildroot%_mandir/man3/

%define docdir %_docdir/%name-%version
mkdir -p %buildroot%docdir
install -p -m644 README \
	example.c minigzip.c %buildroot%docdir/
# License {FAQ,ChangeLog,algorithm.txt}.bz2

%files
%defattr(-,root,root)
%_libdir/z.dll
%dir %docdir
#%docdir/License
%docdir/README

%files devel
%defattr(-,root,root)
%_libdir/*.a
%_libdir/z.dll
%_includedir/*
%_mandir/man?/*
%dir %docdir
%docdir/*.c
#%docdir/*.bz2

%changelog
