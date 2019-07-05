
%define apuver 1

Summary: Apache Portable Runtime Utility library
Name: apr-util
Version: 1.4.1
Release: 1%{?dist}
License: ASL 2.0
Group: System Environment/Libraries
URL: http://apr.apache.org/
Source0: http://www.apache.org/dist/apr/%{name}-%{version}.tar.bz2

Patch1: aprutil-os2.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: apr-devel >= 1.3.0
#BuildRequires: autoconf
#BuildRequires: db4-devel, expat-devel, libuuid-devel

%description
The mission of the Apache Portable Runtime (APR) is to provide a
free library of C data structures and routines.  This library
contains additional utility interfaces for APR; including support
for XML, LDAP, database interfaces, URI parsing and more.

%package devel
Group: Development/Libraries
Summary: APR utility library development kit
Requires: apr-util = %{version}-%{release}, apr-devel, pkgconfig
Requires: db4-devel
#Requires: expat-devel
#Requires: openldap-devel

%description devel
This package provides the support files which can be used to 
build applications using the APR utility library.  The mission 
of the Apache Portable Runtime (APR) is to provide a free 
library of C data structures and routines.

%package pgsql
Group: Development/Libraries
Summary: APR utility library PostgreSQL DBD driver
#BuildRequires: postgresql-devel
Requires: apr-util = %{version}-%{release}

%description pgsql
This package provides the PostgreSQL driver for the apr-util
DBD (database abstraction) interface.

%package mysql
Group: Development/Libraries
Summary: APR utility library MySQL DBD driver
#BuildRequires: mysql-devel
Requires: apr-util = %{version}-%{release}

%description mysql
This package provides the MySQL driver for the apr-util DBD
(database abstraction) interface.

%package sqlite
Group: Development/Libraries
Summary: APR utility library SQLite DBD driver
BuildRequires: sqlite-devel >= 3.0.0
Requires: apr-util = %{version}-%{release}

%description sqlite
This package provides the SQLite driver for the apr-util DBD
(database abstraction) interface.

%package freetds
Group: Development/Libraries
Summary: APR utility library FreeTDS DBD driver
#BuildRequires: freetds-devel
Requires: apr-util = %{version}-%{release}

%description freetds
This package provides the FreeTDS driver for the apr-util DBD
(database abstraction) interface.

%package odbc
Group: Development/Libraries
Summary: APR utility library ODBC DBD driver
#BuildRequires: unixODBC-devel
Requires: apr-util = %{version}-%{release}

%description odbc
This package provides the ODBC driver for the apr-util DBD
(database abstraction) interface.

%package ldap
Group: Development/Libraries
Summary: APR utility library LDAP support
#BuildRequires: openldap-devel
Requires: apr-util = %{version}-%{release}

%description ldap
This package provides the LDAP support for the apr-util.

%prep
%setup -q
%patch1 -p1 -b .os2

%build
#autoheader && autoconf
# A fragile autoconf test which fails if the code trips
# any other warning; force correct result for OpenLDAP:
#export ac_cv_ldap_set_rebind_proc_style=three

export CONFIG_SHELL="/@unixroot/usr/bin/sh.exe"
export LDFLAGS="-Zhigh-mem -Zargs-wild -Zargs-resp"
export LIBS="-lurpo -lmmap"

%configure --with-apr=%{_prefix} \
        --includedir=%{_includedir}/apr-%{apuver} \
       "--cache-file=%{_topdir}/cache/%{name}-%{_target_cpu}.cache"

#        --with-ldap --without-gdbm \
#        --with-sqlite3 --with-pgsql --with-mysql --with-freetds --with-odbc \
#        --with-berkeley-db \
#        --without-sqlite2

# the TARGET_LIB hack prevents smp builds. %{?_smp_mflags}
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/%{_datadir}/aclocal
install -m 644 build/find_apu.m4 $RPM_BUILD_ROOT/%{_datadir}/aclocal

# Unpackaged files; remove the static libaprutil
rm -f $RPM_BUILD_ROOT%{_libdir}/aprutil.exp \
      $RPM_BUILD_ROOT%{_libdir}/apr*.la

# And remove the reference to the static libaprutil from the .la
# file.
#sed -i '/^old_library/s,libapr.*\.a,,' \
#      $RPM_BUILD_ROOT%{_libdir}/apr*.la
# Remove unnecessary exports from dependency_libs
#sed -ri '/^dependency_libs/{s,-l(pq|sqlite[0-9]|rt|dl|uuid) ,,g}' \
#      $RPM_BUILD_ROOT%{_libdir}/apr*.la

# Trim libtool DSO cruft
rm -f $RPM_BUILD_ROOT%{_libdir}/apr-util-%{apuver}/*.*a

# rename static library
mv $RPM_BUILD_ROOT%{_libdir}/apru-%{apuver}.lib $RPM_BUILD_ROOT%{_libdir}/apru-%{apuver}_s.lib
# import library
emximp -o $RPM_BUILD_ROOT%{_libdir}/apru-%{apuver}.lib $RPM_BUILD_ROOT%{_libdir}/apru-%{apuver}.dll

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc CHANGES LICENSE NOTICE
%{_libdir}/apru-%{apuver}.dll
%dir %{_libdir}/apr-util-%{apuver}

%files pgsql
%defattr(-,root,root,-)
#%{_libdir}/apr-util-%{apuver}/apr_dbd_pgsql*

%files mysql
%defattr(-,root,root,-)
#%{_libdir}/apr-util-%{apuver}/apr_dbd_mysql*

%files sqlite
%defattr(-,root,root,-)
%{_libdir}/apr-util-%{apuver}/apr_dbd_sqlite*

%files freetds
%defattr(-,root,root,-)
#%{_libdir}/apr-util-%{apuver}/apr_dbd_freetds*

%files odbc
%defattr(-,root,root,-)
#%{_libdir}/apr-util-%{apuver}/apr_dbd_odbc*

%files ldap
%defattr(-,root,root,-)
#%{_libdir}/apr-util-%{apuver}/apr_ldap*

%files devel
%defattr(-,root,root,-)
%{_bindir}/apu-%{apuver}-config
%{_libdir}/apru-%{apuver}_s.lib
%{_libdir}/apru-%{apuver}.lib
%{_includedir}/apr-%{apuver}/*.h
%{_libdir}/pkgconfig/*.pc
%{_datadir}/aclocal/*.m4

%changelog
* Fri Mar 02 2012 yd
- initial unixroot build.
