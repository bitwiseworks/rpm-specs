#
# spec file for package xz (Version 4.999.9beta)
#
# Copyright (c) 2010 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#



Name:           xz
Summary:        A Program for Compressing Files
Version:        4.999.9beta
Release:        3%{?dist}
Group:          Productivity/Archiving/Compression
License:        LGPLv2.1+
Url:            http://tukaani.org/lzma/

Source:         %{name}-4.999.9beta.tar.bz2
#Source2:        baselibs.conf

Patch0:         %{name}-os2.diff

BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  pkgconfig
Provides:       lzma = %version
Obsoletes:      lzma < %version
Requires:       liblzma0 = %{version}
# avoid bootstrapping problem
%define _binary_payload w9.bzdio

%description
The xz command is a very powerful program for compressing files.

* Average compression ratio of LZMA is about 30% better than that of
   gzip, and 15% better than that of bzip2.

* Decompression speed is only little slower than that of gzip, being
   two to five times faster than bzip2.

* In fast mode, compresses faster than bzip2 with a comparable
   compression ratio.

* Achieving the best compression ratios takes four to even twelve
   times longer than with bzip2. However. this doesn't affect
   decompressing speed.

* Very similar command line interface to what gzip and bzip2 have.

%package -n liblzma0
License:        LGPLv2.1+
Summary:        LZMA library
Group:          System/Libraries

%description -n liblzma0
Library for encoding/decoding LZMA files.

%package devel
License:        LGPLv2.1+
Summary:        Development package for the LZMA library
Group:          Development/Libraries/C and C++
Requires:       liblzma0 = %{version}
Provides:       lzma-devel = %version
Obsoletes:      lzma-devel < %version
Provides:       lzma-alpha-devel = %version
Obsoletes:      lzma-alpha-devel < %version

%description devel
This package contains the header files and libraries needed for
compiling programs using the LZMA library.

%prep
%setup -q -n %{name}-4.999.9beta
%patch0 -p1 -b .os2~

%build
#AUTOPOINT=true autoreconf -fi
#configure --libdir=/%{_lib} --disable-static --with-pic --docdir=%_docdir/%name

export CONFIG_SHELL="/bin/sh"
export LDFLAGS="-Zbin-files -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lurpo -lmmap -lpthread"
%configure \
    --enable-shared --disable-static \
    "--cache-file=%{_topdir}/cache/%{name}-%{_target_cpu}.cache"

make %{?_smp_mflags}

#%check
#LD_LIBRARY_PATH=$PWD/src/liblzma/.libs make check

%install
make install DESTDIR=$RPM_BUILD_ROOT
#%{__mkdir_p} %{buildroot}%{_libdir}
#%{__ln_s} -v /%{_lib}/$(readlink %{buildroot}/%{_lib}/liblzma.so) %{buildroot}%{_libdir}/liblzma.so
#%{__mv} -v  %{buildroot}/%{_lib}/pkgconfig %{buildroot}%{_libdir}
#%{__rm} -v %{buildroot}/%{_lib}/liblzma.{so,la}
cp src/liblzma/*.dll $RPM_BUILD_ROOT%{_libdir}
cp src/liblzma/.libs/*.lib $RPM_BUILD_ROOT%{_libdir}
# fix exe installation
cp src/lzmainfo/.libs/*.exe $RPM_BUILD_ROOT%{_bindir}
cp src/xz/.libs/*.exe $RPM_BUILD_ROOT%{_bindir}
cp src/xzdec/.libs/*.exe $RPM_BUILD_ROOT%{_bindir}

%clean
rm -fr $RPM_BUILD_ROOT

#%post -n liblzma0 -p /sbin/ldconfig

#%postun -n liblzma0 -p /sbin/ldconfig

%files
%defattr(-, root, root)
%_docdir/%name
%{_bindir}/*
%{_mandir}/man?/*

%files -n liblzma0
%defattr(-, root, root)
%{_libdir}/*.dll

%files devel
%defattr(-, root, root)
%{_includedir}/*.h
%{_includedir}/lzma
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.lib
%{_libdir}/pkgconfig/*.pc

%changelog
