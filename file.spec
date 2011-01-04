%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%define __libtoolize :

Summary: A utility for determining file types
Name: file
Version: 5.04
Release: 5%{?dist}
License: BSD
Group: Applications/File
Source0: ftp://ftp.astron.com/pub/file/file-%{version}.tar.gz
URL: http://www.darwinsys.com/file/

Patch0: file-os2.diff

Requires: file-libs = %{version}-%{release}
Requires: mmap >= 20110103

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: zlib-devel

%description
The file command is used to identify a particular file according to the
type of data contained by the file.  File can identify many different
file types, including ELF binaries, system libraries, RPM packages, and
different graphics formats.

%package libs
Summary: Libraries for applications using libmagic
Group:   Applications/File

%description libs

Libraries for applications using libmagic.

%package devel
Summary:  Libraries and header files for file development
Group:    Applications/File
Requires: %{name} = %{version}-%{release}

%description devel
The file-devel package contains the header files and libmagic library
necessary for developing programs using libmagic.

%package static
Summary: Static library for file development
Group:    Applications/File
Requires: %{name} = %{version}-%{release}

%description static
The file-static package contains the static version of
the libmagic library.

%package -n python-magic
Summary: Python bindings for the libmagic API
Group:   Development/Libraries
BuildRequires: python-devel
Requires: %{name} = %{version}-%{release}

%description -n python-magic
This package contains the Python bindings to allow access to the
libmagic API. The libmagic library is also used by the familiar
file(1) command.

%prep

# Don't use -b -- it will lead to poblems when compiling magic file
%setup -q
%patch0 -p1

#iconv -f iso-8859-1 -t utf-8 < doc/libmagic.man > doc/libmagic.man_
touch -r doc/libmagic.man doc/libmagic.man_
mv doc/libmagic.man_ doc/libmagic.man

%build
export CONFIG_SHELL="/bin/sh"
export LDFLAGS="-Zbin-files -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lurpo -lmmap"
export CFLAGS="%{optflags} -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE"
%configure \
        --enable-fsect-man5 --disable-rpath \
        --disable-shared --disable-static \
        "--cache-file=%{_topdir}/cache/%{name}.cache"

# remove hardcoded library paths from local libtool
#sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
#sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
#export LD_LIBRARY_PATH=%{_builddir}/%{name}-%{version}/src/.libs
make %{?_smp_mflags}

cd python
CFLAGS="%{optflags}" %{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man1
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man5
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/misc
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/file

make DESTDIR=${RPM_BUILD_ROOT} install
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la

cat magic/Magdir/* > ${RPM_BUILD_ROOT}%{_datadir}/misc/magic
ln -s misc/magic ${RPM_BUILD_ROOT}%{_datadir}/magic
#ln -s file/magic.mime ${RPM_BUILD_ROOT}%{_datadir}/magic.mime
ln -s ../magic ${RPM_BUILD_ROOT}%{_datadir}/file/magic

cp src/magic.dll ${RPM_BUILD_ROOT}%{_libdir}
cp src/.libs/magic_s.a ${RPM_BUILD_ROOT}%{_libdir}

cd python
%{__python} setup.py install -O1 --skip-build --root ${RPM_BUILD_ROOT}
%{__install} -d ${RPM_BUILD_ROOT}%{_datadir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

#%post libs -p /sbin/ldconfig

#%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING ChangeLog README
%{_bindir}/*
%{_mandir}/man1/*

%files libs
%defattr(-,root,root,-)
%{_libdir}/*.dll
%{_datadir}/magic*
%{_mandir}/man5/*
%{_datadir}/file
%{_datadir}/misc/*

%files devel
%defattr(-,root,root,-)
%{_libdir}/*.dll
%{_libdir}/magic.a
%{_includedir}/magic.h
%{_mandir}/man3/*

%files static
%defattr(-,root,root,-)
%{_libdir}/*_s.a

%files -n python-magic
%defattr(-, root, root, -)
%doc python/README COPYING python/example.py
%{_libdir}/python*/*

%changelog
