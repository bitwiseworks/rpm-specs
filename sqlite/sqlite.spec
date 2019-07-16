# bcond default logic is nicely backwards...
%bcond_without tcl
%bcond_with static
%bcond_with check

%global without_amalgamation 1

%define realver 3280000
%define docver 3280000
%define rpmver 3.28.0

Summary: Library that implements an embeddable SQL database engine
Name: sqlite
Version: %{rpmver}
Release: 1%{?dist}
License: Public Domain
URL: http://www.sqlite.org/

Vendor: bww bitwise works GmbH

%scm_source github https://github.com/bitwiseworks/%{name}-os2 master-os2
Source1: http://www.sqlite.org/2019/sqlite-doc-%{docver}.zip

# DEF files to create forwarders for the legacy package
Source10:       sqlit3.def

BuildRequires: gcc
BuildRequires: ncurses-devel readline-devel
BuildRequires: autoconf
%if %{with tcl}
BuildRequires: /@unixroot/usr/bin/tclsh.exe
BuildRequires: tcl-devel
%{!?tcl_version: %global tcl_version 8.5}
%{!?tcl_sitearch: %global tcl_sitearch %{_libdir}/tcl%{tcl_version}}
%endif

Requires: %{name}-libs = %{version}-%{release}

# Ensure updates from pre-split work on multi-lib systems
Obsoletes: %{name} < 3.11.0-1
Conflicts: %{name} < 3.11.0-1

%description
SQLite is a C library that implements an SQL database engine. A large
subset of SQL92 is supported. A complete database is stored in a
single disk file. The API is designed for convenience and ease of use.
Applications that link against SQLite can enjoy the power and
flexibility of an SQL database without the administrative hassles of
supporting a separate database server.  Version 2 and version 3 binaries
are named to permit each to be installed on a single host

%package devel
Summary: Development tools for the sqlite3 embeddable SQL database engine
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: pkgconfig

%description devel
This package contains the header files and development documentation 
for %{name}. If you like to develop programs using %{name}, you will need 
to install %{name}-devel.

%package libs
Summary: Shared library for the sqlite3 embeddable SQL database engine.

# Ensure updates from pre-split work on multi-lib systems
Obsoletes: %{name} < 3.11.0-1
Conflicts: %{name} < 3.11.0-1
# we need this version because of the fchown() libc bug in earlier versions
Requires: libc >= 1:0.1.2

%description libs
This package contains the shared library for %{name}.

%package doc
Summary: Documentation for sqlite
BuildArch: noarch

%description doc
This package contains most of the static HTML files that comprise the
www.sqlite.org website, including all of the SQL Syntax and the 
C/C++ interface specs and other miscellaneous documentation.

%package -n lemon
Summary: A parser generator

%description -n lemon
Lemon is an LALR(1) parser generator for C or C++. It does the same
job as bison and yacc. But lemon is not another bison or yacc
clone. It uses a different grammar syntax which is designed to reduce
the number of coding errors. Lemon also uses a more sophisticated
parsing engine that is faster than yacc and bison and which is both
reentrant and thread-safe. Furthermore, Lemon implements features
that can be used to eliminate resource leaks, making is suitable for
use in long-running programs such as graphical user interfaces or
embedded controllers.

%if %{with tcl}
%package tcl
Summary: Tcl module for the sqlite3 embeddable SQL database engine
Requires: %{name} = %{version}-%{release}
Requires: tcl(abi) = %{tcl_version}

%description tcl
This package contains the tcl modules for %{name}.

%package analyzer
Summary: An analysis program for sqlite3 database files
Requires: %{name} = %{version}-%{release}
Requires: tcl(abi) = %{tcl_version}

%description analyzer
This package contains the analysis program for %{name}.
%endif

%debug_package

%prep
%scm_setup
unzip %{SOURCE1}

# Remove backup-file
rm -f %{name}-doc-%{docver}/sqlite.css~ || :

autoreconf -fvi

# Prepare forwarder DLLs.
for m in %{SOURCE10}; do
  cp ${m} .
done

%build
export CFLAGS="$RPM_OPT_FLAGS $RPM_LD_FLAGS -DSQLITE_ENABLE_COLUMN_METADATA=1 \
               -DSQLITE_DISABLE_DIRSYNC=1 -DSQLITE_ENABLE_FTS3=3 \
               -DSQLITE_ENABLE_RTREE=1 -DSQLITE_SECURE_DELETE=1 \
               -DSQLITE_ENABLE_UNLOCK_NOTIFY=1 -DSQLITE_ENABLE_DBSTAT_VTAB=1 \
               -DSQLITE_ENABLE_FTS3_PARENTHESIS=1 -DSQLITE_ENABLE_JSON1=1 \
               -Wall -fno-strict-aliasing"
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
export VENDOR="%{vendor}"
%configure %{!?with_tcl:--disable-tcl} \
           --enable-fts5 \
           --enable-threadsafe \
           --enable-threads-override-locks \
           --enable-load-extension \
           %{?without_amalgamation:--disable-amalgamation} \
           %{?with_tcl:TCLLIBDIR=%{tcl_sitearch}/sqlite3}

# rpath removal
#sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
#sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}

# Build sqlite3_analyzer
# depends on tcl
%if %{with tcl}
make %{?_smp_mflags} sqlite3_analyzer.exe
%endif

%install
make DESTDIR=${RPM_BUILD_ROOT} install

install -D -m0644 sqlite3.1 $RPM_BUILD_ROOT/%{_mandir}/man1/sqlite3.1
install -D -m0755 lemon.exe $RPM_BUILD_ROOT/%{_bindir}/lemon.exe
install -D -m0644 tool/lempar.c $RPM_BUILD_ROOT/%{_datadir}/lemon/lempar.c

# Generate & install forwarder DLLs.
gcc -Zomf -Zdll -nostdlib sqlit3.def -l$RPM_BUILD_ROOT/%{_libdir}/sqlite30.dll -lend -o $RPM_BUILD_ROOT/%{_libdir}/sqlit3.dll

%if %{with tcl}
# fix up permissions to enable dep extraction
chmod 0755 ${RPM_BUILD_ROOT}/%{tcl_sitearch}/sqlite3/*.dll
# Install sqlite3_analyzer
install -D -m0755 sqlite3_analyzer.exe $RPM_BUILD_ROOT/%{_bindir}/sqlite3_analyzer.exe
%endif

%if ! %{with static}
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT/%{_libdir}/sqlite3.a
rm -f $RPM_BUILD_ROOT/%{tcl_sitearch}/sqlite3/tclsqlite3.a
%endif

%if %{with check}
%check
# XXX shell tests are broken due to loading system libsqlite3, work around...
export LD_LIBRARY_PATH=`pwd`/.libs
export MALLOC_CHECK_=3

# csv01 hangs on all non-intel archs i've tried
%ifarch x86_64 %{ix86}
%else
rm test/csv01.test
%endif

%ifarch s390x ppc64
rm test/fts3conf.test
%endif

make test
%endif # with check

#ldconfig_scriptlets libs

%files
%{_bindir}/sqlite3.exe
%{_mandir}/man?/*

%files libs
%doc README.md
%{_libdir}/*.dll

%files devel
%{_includedir}/*.h
%{_libdir}/sqlit*_dll.a
%{_libdir}/pkgconfig/*.pc
%if %{with static}
%{_libdir}/sqlite3.a
%exclude %{_libdir}/*.la
%endif

%files doc
%doc %{name}-doc-%{docver}/*

%files -n lemon
%{_bindir}/lemon.exe
%{_datadir}/lemon

%if %{with tcl}
%files tcl
%{tcl_sitearch}/sqlite3
%exclude %{tcl_sitearch}/sqlite3/*.dbg

%files analyzer
%{_bindir}/sqlite3_analyzer.exe
%endif

%changelog
* Wed Jul 03 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> 3.28.0-1
- update version to 3.28.0

* Wed Mar 27 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> 3.27.2-1
- update version to 3.27.2
- add a nice bldlevel to the dll
- use the nix codepath where possible
- use latest scm_ macros

* Mon Jan 16 2012 yd
- rebuild with libc 0.6.4 runtime.
