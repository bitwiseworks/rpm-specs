%global with_python3 0

Summary: A utility for determining file types
Name: file
Version: 5.30
Release: 1%{?dist}
License: BSD
Group: Applications/File

Vendor:  bww bitwise works GmbH
%scm_source svn  http://svn.netlabs.org/repos/ports/file/trunk 2149

# DEF files to create forwarders for the legacy package
Source10:       magic.def

URL: http://www.darwinsys.com/file/
Requires: file-libs = %{version}-%{release}
BuildRequires: zlib-devel
BuildRequires: autoconf automake libtool

%description
The file command is used to identify a particular file according to the
type of data contained by the file.  File can identify many different
file types, including ELF binaries, system libraries, RPM packages, and
different graphics formats.

%package libs
Summary: Libraries for applications using libmagic
Group:   Applications/File
License: BSD

%description libs

Libraries for applications using libmagic.

%package devel
Summary:  Libraries and header files for file development
Group:    Applications/File
Requires: %{name} = %{version}-%{release}

%description devel
The file-devel package contains the header files and libmagic library
necessary for developing programs using libmagic.

%package -n python-magic
Summary: Python 2 bindings for the libmagic API
Group:   Development/Libraries
BuildRequires: python2-devel
BuildArch: noarch
Requires: %{name} = %{version}-%{release}

%description -n python-magic
This package contains the Python bindings to allow access to the
libmagic API. The libmagic library is also used by the familiar
file(1) command.

%if %{with_python3}
%package -n python3-magic
Summary: Python 3 bindings for the libmagic API
Group:   Development/Libraries
BuildRequires: python3-devel
BuildArch: noarch
Requires: %{name} = %{version}-%{release}

%description -n python3-magic
This package contains the Python 3 bindings to allow access to the
libmagic API. The libmagic library is also used by the familiar
file(1) command.
%endif

%debug_package

%prep
%scm_setup
autoreconf -fvi

# Prepare forwarder DLLs.
for m in %{SOURCE10}; do
  cp ${m} .
done

#iconv -f iso-8859-1 -t utf-8 < doc/libmagic.man > doc/libmagic.man_
touch -r doc/libmagic.man doc/libmagic.man_
mv doc/libmagic.man_ doc/libmagic.man

%if %{with_python3}
rm -rf %{py3dir}
cp -a python %{py3dir}
%endif

%build
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
export CFLAGS="%{optflags} -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE"
export VENDOR="%{vendor}"
%configure --enable-fsect-man5 --disable-rpath

export BEGINLIBPATH=%{_builddir}/%{name}-%{version}/src/.libs
make %{?_smp_mflags}

cd python
CFLAGS="%{optflags}" %{__python} setup.py build
%if %{with_python3}
cd %{py3dir}
CFLAGS="%{optflags}" %{__python3} setup.py build
%endif

%install
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man1
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man5
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/misc
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/file

make DESTDIR=${RPM_BUILD_ROOT} install
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la

cat magic/Magdir/* > ${RPM_BUILD_ROOT}%{_datadir}/misc/magic
ln -s misc/magic ${RPM_BUILD_ROOT}%{_datadir}/magic
ln -s ../magic ${RPM_BUILD_ROOT}%{_datadir}/file/magic

# Generate & install forwarder DLLs.
gcc -Zomf -Zdll -nostdlib magic.def -l$RPM_BUILD_ROOT/%{_libdir}/magic1.dll -lend -o $RPM_BUILD_ROOT/%{_libdir}/magic.dll

cd python
%{__python} setup.py install -O1 --skip-build --root ${RPM_BUILD_ROOT}
%if %{with_python3}
cd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root ${RPM_BUILD_ROOT}
%endif
%{__install} -d ${RPM_BUILD_ROOT}%{_datadir}/%{name}

#post libs -p /sbin/ldconfig

#postun libs -p /sbin/ldconfig

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc ChangeLog README
%{_bindir}/*.exe
%{_mandir}/man1/*

%files libs
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc ChangeLog README
%{_libdir}/*.dll
%{_datadir}/magic*
%{_mandir}/man5/*
%{_datadir}/file
%{_datadir}/misc/*

%files devel
%{_libdir}/magic*_dll.a
%{_includedir}/magic.h
%{_mandir}/man3/*


%files -n python-magic
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc python/README python/example.py
%{_libdir}/python*/*
%{python_sitelib}/magic.py
%{python_sitelib}/magic.pyc
%{python_sitelib}/magic.pyo
%{python_sitelib}/*egg-info

%if %{with_python3}
%files -n python3-magic
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc python/README python/example.py
%{python3_sitelib}/magic.py
%{python3_sitelib}/*egg-info
%{python3_sitelib}/__pycache__/*
%endif

%changelog
* Mon Mar 06 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 5.30-1
- updated to vendor version 5.30
- use scm_ macros
- add forwarder

* Mon Feb 02 2015 yd <yd@os2power.com> 5.04-7
- r266, rebuilt with gcc 4.9.2 and python 2.7.
