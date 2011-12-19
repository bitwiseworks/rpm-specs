Summary: A library for manipulating JPEG image format files
Name: libjpeg
Version: 8c
Release: 1%{?dist}
License: IJG
Group: System Environment/Libraries
URL: http://www.ijg.org/

Source0: ftp://ftp.uu.net/graphics/jpeg/jpegsrc.v%{version}.tar.gz

Patch1: jpeg-os2.diff

#BuildRequires: autoconf libtool
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
The libjpeg package contains a library of functions for manipulating
JPEG images, as well as simple client programs for accessing the
libjpeg functions.  Libjpeg client programs include cjpeg, djpeg,
jpegtran, rdjpgcom and wrjpgcom.  Cjpeg compresses an image file into
JPEG format.  Djpeg decompresses a JPEG file into a regular image
file.  Jpegtran can perform various useful transformations on JPEG
files.  Rdjpgcom displays any text comments included in a JPEG file.
Wrjpgcom inserts text comments into a JPEG file.

%package devel
Summary: Development tools for programs which will use the libjpeg library
Group: Development/Libraries
Requires: libjpeg = %{version}-%{release}

%description devel
The libjpeg-devel package includes the header files and documentation
necessary for developing programs which will manipulate JPEG files using
the libjpeg library.

If you are going to develop programs which will manipulate JPEG images,
you should install libjpeg-devel.  You'll also need to have the libjpeg
package installed.

%package static
Summary: Static JPEG image format file library
Group: Development/Libraries
Requires: libjpeg-devel = %{version}-%{release}

%description static
The libjpeg-static package contains the statically linkable version of libjpeg.
Linking to static libraries is discouraged for most applications, but it is
necessary for some boot packages.

%prep
%setup -q -n jpeg-%{version}

%patch1 -p1 -b .os2~

%build
export CONFIG_SHELL="/@unixroot/usr/bin/sh.exe"
export CFLAGS="$RPM_OPT_FLAGS"
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
%configure \
     --disable-shared --enable-static \
    "--cache-file=%{_topdir}/cache/%{name}-%{_target_cpu}.cache"

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall

install -m 755 jpeg.dll $RPM_BUILD_ROOT/%{_libdir}
install -m 755 .libs/jpeg_s.a $RPM_BUILD_ROOT/%{_libdir}

# We don't ship .la files.
rm $RPM_BUILD_ROOT%{_libdir}/*.la

%files
%defattr(-,root,root)
%doc usage.txt README
%{_libdir}/jpeg*.dll
%{_bindir}/*
%{_mandir}/*/*

%files devel
%defattr(-,root,root)
%doc libjpeg.txt coderules.txt structure.txt wizard.txt example.c
%{_libdir}/jpeg.a
%{_includedir}/*.h

%files static
%defattr(-,root,root)
%{_libdir}/jpeg_s.a

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Mon Dec 19 2011 yd
- initial build.
