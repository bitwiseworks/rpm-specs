# python3 is not available on RHEL <= 7
%if 0%{?fedora} || 0%{?rhel} > 7 || 0%{?os2_version}
%bcond_without python3
%else
%bcond_with python3
%endif

# python2 is not available on RHEL > 7
%if 0%{?fedora} > 31 || 0%{?rhel} > 7 || 0%{?os2_version}
%bcond_with python2
%else
%bcond_without python2
%endif

Summary: Utility for determining file types
Name: file
Version: 5.48
Release: 2%{?dist}

# Main license is BSD-2-Clause-Darwin
# Shipped exceptions:
# * some src/*.{c.h} - BSD-2-Clause
# Not shipped in Fedora:
# * src/mygetopt.h - BSD-4-Clause
# * src/strcasestr.h - BSD-3-Clause
# * src/strlc{at,py}.c - ISC
# * src/vasprintf.c - BSD-2-Clause-Darwin AND BSD-3-Clause
License: BSD-2-Clause-Darwin AND BSD-2-Clause

%if !0%{?os2_version}
Source0: http://ftp.astron.com/pub/file/file-%{version}.tar.gz
Source1: http://ftp.astron.com/pub/file/file-%{version}.tar.gz.asc

# gpg --keyserver hkp://keys.gnupg.net --recv-keys BE04995BA8F90ED0C0C176C471112AB16CB33B3A
# gpg --output christoskey.asc --armor --export christos@zoulas.com
Source2: christoskey.asc

# Upstream says it's up to distributions to add a way to support local-magic.
Patch0: file-localmagic.patch

# not yet upstream
Patch1: file-4.17-rpm-name.patch
Patch2: file-5.04-volume_key.patch

# revert upstream commits (rhbz#2167964)
# 1. https://github.com/file/file/commit/e1233247bbe4d2d66b891224336a23384a93cce1
# 2. https://github.com/file/file/commit/f7a65dbf1739a8f8671621e41c5648d1f7e9f6ae
Patch3: file-5.45-readelf-limit-revert.patch

Patch4: file-5.46-fix-tests-rpm-magic.patch
%else
Vendor:  bww bitwise works GmbH
%scm_source github  https://github.com/bitwiseworks/%{name}-os2 %{version}-os2-1
%endif

URL: https://www.darwinsys.com/file/
%if !0%{?os2_version}
Requires: file-libs%{?_isa} = %{version}-%{release}
%else
Requires: file-libs = %{version}-%{release}
%endif
BuildRequires: zlib-devel
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
BuildRequires: make
%if !0%{?os2_version}
BuildRequires: gnupg2
%endif

%description
The file command is used to identify a particular file according to the
type of data contained by the file.  File can identify many different
file types, including ELF binaries, system libraries, RPM packages, and
different graphics formats.

%package libs
Summary: Libraries for applications using libmagic

%description libs

Libraries for applications using libmagic.

%package devel
Summary:  Libraries and header files for file development
%if !0%{?os2_version}
Requires: file-libs%{?_isa} = %{version}-%{release}
%else
Requires: file-libs = %{version}-%{release}
%endif

%description devel
The file-devel package contains the header files and libmagic library
necessary for developing programs using libmagic.

%package static
Summary: Static library for file development
Requires: file-devel = %{version}-%{release}

%description static
The file-static package contains the static version of the libmagic library.

%if %{with python2}
%package -n python2-magic
Summary: Python 2 bindings for the libmagic API
BuildRequires: python2-devel
BuildRequires: python2-setuptools
BuildArch: noarch
Requires: file-libs = %{version}-%{release}
%{?python_provide:%python_provide python2-magic}

%description -n python2-magic
This package contains the Python 2 bindings to allow access to the
libmagic API. The libmagic library is also used by the familiar
file(1) command.
%endif

%if %{with python3}
%package -n python3-file-magic
Summary: Python 3 bindings for the libmagic API
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildArch: noarch
Requires: file-libs = %{version}-%{release}
Conflicts: python3-magic

%description -n python3-file-magic
This package contains the Python 3 bindings to allow access to the
libmagic API. The libmagic library is also used by the familiar
file(1) command.
%endif

%if 0%{?os2_version}
%debug_package
%endif

%prep
%if !0%{?os2_version}
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -p1
%else
%scm_setup
%endif

iconv -f iso-8859-1 -t utf-8 < doc/libmagic.man > doc/libmagic.man_
touch -r doc/libmagic.man doc/libmagic.man_
mv doc/libmagic.man_ doc/libmagic.man

%if %{with python3}
rm -rf %{py3dir}
cp -a python %{py3dir}
%endif

%build
# Fix config.guess to find aarch64 - #925339
autoreconf -fi

%if 0%{?os2_version}
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
export VENDOR="%{vendor}"
%endif
CFLAGS="%{optflags} -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE" \
%configure --enable-fsect-man5 --disable-rpath --enable-static
# remove hardcoded library paths from local libtool
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%if !0%{?os2_version}
export LD_LIBRARY_PATH=$PWD/src/.libs
%else
export LIBPATHSTRICT=T
export BEGINLIBPATH=$PWD/src/.libs
%endif
%make_build
%if %{with python2}
cd python
CFLAGS="%{optflags}" %{__python2} setup.py build
%endif
%if %{with python3}
cd %{py3dir}
CFLAGS="%{optflags}" %{__python3} setup.py build
%endif

%install
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man1
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man5
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/misc
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/file

%make_install
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la

# local magic in /etc/magic
%if !0%{?os2_version}
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}
cp -a ./magic/magic.local ${RPM_BUILD_ROOT}%{_sysconfdir}/magic
%endif

cat magic/Magdir/* > ${RPM_BUILD_ROOT}%{_datadir}/misc/magic
ln -s misc/magic ${RPM_BUILD_ROOT}%{_datadir}/magic
ln -s ../magic ${RPM_BUILD_ROOT}%{_datadir}/file/magic

%if %{with python2}
cd python
%{__python2} setup.py install -O1 --skip-build --root ${RPM_BUILD_ROOT}
%endif
%if %{with python3}
cd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root ${RPM_BUILD_ROOT}
%endif
%{__install} -d ${RPM_BUILD_ROOT}%{_datadir}/%{name}

%if !0%{?os2_version}
%ldconfig_scriptlets libs
%endif

%check
%if !0%{?os2_version}
export LD_LIBRARY_PATH=$PWD/src/.libs
%else
export LIBPATHSTRICT=T
export BEGINLIBPATH=$PWD/src/.libs
%endif
%ifarch s390x
# efi-signature-list-sha256: New in 5.47 (commit 2a457644). EFI Signature List magic
# in magic/Magdir/efi uses little-endian types; on big-endian s390x file reports
# "data" instead of the expected string and the test fails. Remove on s390x until
# upstream makes the EFI magic endian-safe.
rm -f tests/efi-signature-list-sha256.testfile tests/efi-signature-list-sha256.result
%endif
make -C tests check

%files
%license COPYING
%doc ChangeLog
%if !0%{?os2_version}
%{_bindir}/*
%else
%{_bindir}/*.exe
%endif
%{_mandir}/man1/*
%if !0%{?os2_version}
%config(noreplace) %{_sysconfdir}/magic
%endif

%files libs
%license COPYING
%doc ChangeLog
%if !0%{?os2_version}
%{_libdir}/*so.*
%else
%{_libdir}/*.dll
%endif
%{_datadir}/magic*
%{_mandir}/man5/*
%{_datadir}/file
%{_datadir}/misc/*

%files devel
%if !0%{?os2_version}
%{_libdir}/*.so
%else
%{_libdir}/*_dll.a
%endif
%{_includedir}/magic.h
%{_mandir}/man3/*
%{_libdir}/pkgconfig/libmagic.pc

%files static
%if !0%{?os2_version}
%{_libdir}/libmagic.a
%else
%{_libdir}/magic.a
%endif

%if %{with python2}
%files -n python2-magic
%license COPYING
%doc python/README.md python/example.py
%{python2_sitelib}/magic.py
%{python2_sitelib}/magic.pyc
%{python2_sitelib}/magic.pyo
%if 0%{?fedora} || 0%{?rhel} >= 6 || 0%{?os2_version}
%{python2_sitelib}/*egg-info
%endif
%endif

%if %{with python3}
%files -n python3-file-magic
%license COPYING
%doc python/README.md python/example.py
%{python3_sitelib}/magic.py
%{python3_sitelib}/*egg-info
%{python3_sitelib}/__pycache__/*
%endif

%changelog
* Mon Aug 17 2026 Silvan Scherrer <silvan.scherrer@aroa.ch> 5.48-2
- make sure option -Z (HAVE_FORK) is defined fixes issue #1

* Mon Aug 10 2026 Silvan Scherrer <silvan.scherrer@aroa.ch> 5.48-1
- updated to vendor version 5.48
- resync with fedora spec
- remove the old magic.dll

* Wed Apr 05 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 5.30-2
- fix a regex issue (this will be rolled back, when libc issue 375 or libcx
  issue 35 is done)
- added buildlevel information

* Mon Mar 06 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 5.30-1
- updated to vendor version 5.30
- use scm_ macros
- add forwarder

* Mon Feb 02 2015 yd <yd@os2power.com> 5.04-7
- r266, rebuilt with gcc 4.9.2 and python 2.7.
