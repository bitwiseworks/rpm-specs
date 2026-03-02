# bcond default logic is nicely backwards...
%bcond_without tcl
%bcond_without sqldiff
%bcond_with static
%if !0%{?os2_version}
%bcond_without check
%else
%bcond_with check
%endif

%define realver 3470200
%define docver 3470200
%define rpmver 3.47.2
%define year 2024

Summary: Library that implements an embeddable SQL database engine
Name: sqlite
Version: %{rpmver}
Release: 1%{?dist}
License: blessing
URL: http://www.sqlite.org/

%if !0%{?os2_version}
Source0: http://www.sqlite.org/%{year}/sqlite-src-%{realver}.zip
%else
Vendor: bww bitwise works GmbH
%scm_source github https://github.com/bitwiseworks/%{name}-os2 %{version}-os2
# DEF files to create forwarders for the legacy package
Source10: sqlit3.def
%endif
Source1: http://www.sqlite.org/%{year}/sqlite-doc-%{docver}.zip
%if !0%{?os2_version}
Source2: http://www.sqlite.org/%{year}/sqlite-autoconf-%{realver}.tar.gz
# Support a system-wide lemon template
Patch1: sqlite-3.6.23-lemon-system-template.patch
Patch2: sqlite-3.47.0-Fix-install-tcl-on-tcl8.6-in-buildtclext.patch
Patch3: sqlite-3.47.0-Backport-FTS3-corruption-test-fix-for-big-endian.patch
%endif

BuildRequires: make
BuildRequires: gcc
%if !0%{?os2_version}
BuildRequires: ncurses-devel readline-devel glibc-devel
%else
BuildRequires: ncurses-devel readline-devel
%endif
BuildRequires: autoconf
%if !0%{?os2_version}
BuildRequires: /usr/bin/tclsh
BuildRequires: zlib-ng-compat-devel
%else
BuildRequires: /@unixroot/usr/bin/tclsh.exe
BuildRequires: zlib-devel
%endif
%if %{with tcl}
BuildRequires: tcl-devel
%{!?tcl_version: %global tcl_version 8.6}
%{!?tcl_sitearch: %global tcl_sitearch %{_libdir}/tcl%{tcl_version}}
%endif

Requires: %{name}-libs = %{version}-%{release}
Provides: %{name}3 = %{version}-%{release}

# Ensure updates from pre-split work on multi-lib systems
Obsoletes: %{name} < 3.11.0-1
Conflicts: %{name} < 3.11.0-1

%description
SQLite is a C library that implements an SQL database engine. A large
subset of SQL92 is supported. A complete database is stored in a
single disk file. The API is designed for convenience and ease of use.
Applications that link against SQLite can enjoy the power and
flexibility of an SQL database without the administrative hassles of
supporting a separate database server. Version 2 and version 3 binaries
are named to permit each to be installed on a single host

SQLite is built with some non-default settings:
- Additional APIs for table's and query's metadata are enabled 
  (SQLITE_ENABLE_COLUMN_METADATA)
- Directory syncs are disabled (SQLITE_DISABLE_DIRSYNC)
- `secure_delete` defaults to 'on', so deleted content is overwritten
  with zeros (SQLITE_SECURE_DELETE)
- `sqlite3_unlock_notify()` is enabled - this feature allows to register a 
  callback that's invoked when lock is removed (SQLITE_ENABLE_UNLOCK_NOTIFY)
- `dbstat` virtual table with disk space usage is enabled
- `dbpage` virtual table providing direct access to underlying database file
  is enabled (SQLITE_ENABLE_DBPAGE_VTAB)
- Threadsafe mode is set to 1 - Serialized, so it is safe to use in a 
  multithreaded environment (SQLITE_THREADSAFE=1)
- FTS3, FTS4 and FTS5 are enabled so versions 3 to 5 of the full-text search
  engine are available (SQLITE_ENABLE_FTS3, SQLITE_ENABLE_FTS4, 
  SQLITE_ENABLE_FTS5)
- Pattern parser in FTS3 extension supports nested parenthesis and operators
  `AND`, `OR` (SQLITE_ENABLE_FTS3_PARENTHESIS)
- R*Tree index extension is enabled (SQLITE_ENABLE_RTREE)
- Extension loading is enabled

It is also important to note that shell has some extensions as its dependencies,
so some extensions are enabled by default in SQLite shell, but not in the system
libraries. Only the aforementioned extensions are available in the libraries:
FTS3, FTS4, FTS5, R*Tree


%package devel
Summary: Development tools for the sqlite3 embeddable SQL database engine
%if !0%{?os2_version}
Requires: %{name}%{?_isa} = %{version}-%{release}
%else
Requires: %{name} = %{version}-%{release}
%endif
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
%if 0%{?os2_version}
# we need this version because of the fchown() libc bug in earlier versions
Requires: libc >= 1:0.1.2
%endif

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


%package debug
Summary: SQLite shell configured for development and debugging purposes

%description debug
This version of SQLite shell contains features that are useful for
debugging purposes. These features are not present in a normal SQLite shell
because some have negative impact on a non-developer user experience.

Current list of modification from normal SQLite shell (in sqlite package):
- Ability to enable .scanstats for metrics regarding query speeds


%if %{with sqldiff}
%package tools
Summary: %{name} tools
Group: Development/Tools

%description tools
%{name} related tools. Currently contains only sqldiff.
- sqldiff: The sqldiff binary is a command-line utility program
  that displays the differences between SQLite databases.
%endif

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

%if 0%{?os2_version}
%debug_package
%endif

%prep
%if !0%{?os2_version}
%setup -q -a1 -n %{name}-src-%{realver}
%patch -P 1 -p1
%patch -P 2 -p1
%patch -P 3 -p1
%else
%scm_setup
unzip %{SOURCE1}
%endif

# The atof test is failing on the i686 architecture, when binary configured with
# --enable-rtree option. Failing part is text->real conversion and
# text->real->text conversion in lower significant values after decimal point in a number.
# func4 tests fail for i686 on float<->int conversions.
%ifarch == i686
rm test/atof1.test
rm test/func4.test
%endif

# Remove backup-file
rm -f %{name}-doc-%{docver}/sqlite.css~ || :

%if !0%{?os2_version}
autoupdate
autoconf # Rerun with new autoconf to add support for aarm64
%else
autoreconf -fvi
%endif

%build
%if 0%{?os2_version}
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx -licuuc -licuin"
export VENDOR="%{vendor}"
%endif
# First build executable for debug subpackage
# following CFLAGS are not possible to set via the configure script
export CFLAGS="$RPM_OPT_FLAGS $RPM_LD_FLAGS \
               -DSQLITE_ENABLE_COLUMN_METADATA=1 \
               -DSQLITE_DISABLE_DIRSYNC=1 \
               -DSQLITE_SECURE_DELETE=1 \
               -DSQLITE_ENABLE_UNLOCK_NOTIFY=1 -DSQLITE_ENABLE_DBSTAT_VTAB=1 \
               -DSQLITE_ENABLE_FTS3_PARENTHESIS=1 \
               -DSQLITE_ENABLE_STMT_SCANSTATUS \
               -DSQLITE_ENABLE_DBPAGE_VTAB \
%if 0%{?os2_version}
               -DSQLITE_ENABLE_ICU=1 \
%endif
               -Wall -fno-strict-aliasing"

%configure %{!?with_tcl:--disable-tcl} \
           --enable-rtree \
           --enable-fts3 \
           --enable-fts4 \
           --enable-fts5 \
           --enable-threadsafe \
           --enable-threads-override-locks \
           --enable-load-extension \
%if 0%{?os2_version}
           --disable-amalgamation \
%endif

%if !0%{?os2_version}
# rpath removal
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%endif

%make_build

%if !0%{?os2_version}
mv sqlite3 sqlite3-debug
%else
mv sqlite3.exe sqlite3-debug.exe
%endif

make clean

# Now rebuild rest of the packages normally
export CFLAGS="$RPM_OPT_FLAGS $RPM_LD_FLAGS \
               -DSQLITE_ENABLE_COLUMN_METADATA=1 \
               -DSQLITE_DISABLE_DIRSYNC=1 \
               -DSQLITE_SECURE_DELETE=1 \
               -DSQLITE_ENABLE_UNLOCK_NOTIFY=1 -DSQLITE_ENABLE_DBSTAT_VTAB=1 \
               -DSQLITE_ENABLE_FTS3_PARENTHESIS=1 \
               -DSQLITE_ENABLE_DBPAGE_VTAB \
%if 0%{?os2_version}
               -DSQLITE_ENABLE_ICU=1 \
%endif
               -Wall -fno-strict-aliasing"

%configure %{!?with_tcl:--disable-tcl} \
           --enable-rtree \
           --enable-fts3 \
           --enable-fts4 \
           --enable-fts5 \
           --enable-threadsafe \
           --enable-threads-override-locks \
           --enable-load-extension \
%if 0%{?os2_version}
           --disable-amalgamation \
%endif

%if !0%{?os2_version}
# rpath removal
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%endif

%make_build

# Build sqlite3_analyzer
# depends on tcl
%if %{with tcl}
%if !0%{?os2_version}
%make_build sqlite3_analyzer
%else
%make_build sqlite3_analyzer.exe
%endif
%endif

# Build sqldiff
%if %{with sqldiff}
%if !0%{?os2_version}
%make_build sqldiff
%else
%make_build sqldiff.exe
%endif
%endif

%install
%if 0%{?os2_version}
# we need to export the path, as else its installed in /usr/share
export tcllibpath=%{tcl_sitearch}
%endif
mkdir -p ${RPM_BUILD_ROOT}%{tcl_sitearch}
%make_install

install -D -m0644 sqlite3.1 $RPM_BUILD_ROOT/%{_mandir}/man1/sqlite3.1
%if !0%{?os2_version}
install -D -m0755 lemon $RPM_BUILD_ROOT/%{_bindir}/lemon
%else
install -D -m0755 lemon.exe $RPM_BUILD_ROOT/%{_bindir}/lemon.exe
%endif
install -D -m0644 tool/lempar.c $RPM_BUILD_ROOT/%{_datadir}/lemon/lempar.c
%if !0%{?os2_version}
install -D -m0755 sqlite3-debug $RPM_BUILD_ROOT/%{_bindir}/sqlite3-debug
%else
install -D -m0755 sqlite3-debug.exe $RPM_BUILD_ROOT/%{_bindir}/sqlite3-debug.exe
%endif

%if 0%{?os2_version}
# Generate & install forwarder DLLs.
gcc -Zomf -Zdll -nostdlib %{SOURCE10} -l$RPM_BUILD_ROOT/%{_libdir}/sqlite30.dll -lend -o $RPM_BUILD_ROOT/%{_libdir}/sqlit3.dll
%endif

%if %{with tcl}
# fix up permissions to enable dep extraction
install -d $RPM_BUILD_ROOT%{tcl_sitearch}
mv $RPM_BUILD_ROOT%{_datadir}/tcl%{tcl_version}/sqlite* $RPM_BUILD_ROOT%{tcl_sitearch}/
%if !0%{?os2_version}
chmod 0755 ${RPM_BUILD_ROOT}/%{tcl_sitearch}/sqlite%{rpmver}/*.so
%else
chmod 0755 ${RPM_BUILD_ROOT}/%{tcl_sitearch}/sqlite%{rpmver}/*.dll
%endif
# Install sqlite3_analyzer
%if !0%{?os2_version}
install -D -m0755 sqlite3_analyzer $RPM_BUILD_ROOT/%{_bindir}/sqlite3_analyzer
%else
install -D -m0755 sqlite3_analyzer.exe $RPM_BUILD_ROOT/%{_bindir}/sqlite3_analyzer.exe
%endif
%endif

# Install sqldiff
%if %{with sqldiff}
%if !0%{?os2_version}
install -D -m0755 sqldiff $RPM_BUILD_ROOT/%{_bindir}/sqldiff
%else
install -D -m0755 sqldiff.exe $RPM_BUILD_ROOT/%{_bindir}/sqldiff.exe
%endif
%endif

%if ! %{with static}
%if !0%{?os2_version}
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.{la,a}
%else
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT/%{_libdir}/sqlite3.a
%endif
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

make test
%endif
# ends %%{with check} if

%if !0%{?os2_version}
%ldconfig_scriptlets libs
%endif

%files
%if !0%{?os2_version}
%{_bindir}/sqlite3
%else
%{_bindir}/sqlite3.exe
%endif
%{_mandir}/man?/*

%files libs
%doc README.md
%if !0%{?os2_version}
%{_libdir}/*.so.0.8.6
%{_libdir}/*.so.0
%else
%{_libdir}/*.dll
%endif

%files devel
%{_includedir}/*.h
%if !0%{?os2_version}
%{_libdir}/*.so
%else
%{_libdir}/sqlit*_dll.a
%endif
%{_libdir}/pkgconfig/*.pc
%if %{with static}
%{_libdir}/*.a
%exclude %{_libdir}/*.la
%endif

%files doc
%doc %{name}-doc-%{docver}/*

%files -n lemon
%if !0%{?os2_version}
%{_bindir}/lemon
%else
%{_bindir}/lemon.exe
%endif
%{_datadir}/lemon

%files debug
%if !0%{?os2_version}
%{_bindir}/sqlite3-debug
%else
%{_bindir}/sqlite3-debug.exe
%endif

%if %{with tcl}
%files tcl
%{tcl_sitearch}/sqlite%{rpmver}
%if 0%{?os2_version}
%exclude %{tcl_sitearch}/sqlite%{rpmver}/*.dbg
%endif

%if %{with sqldiff}
%files tools
%if !0%{?os2_version}
%{_bindir}/sqldiff
%else
%{_bindir}/sqldiff.exe
%endif
%endif

%files analyzer
%if !0%{?os2_version}
%{_bindir}/sqlite3_analyzer
%else
%{_bindir}/sqlite3_analyzer.exe
%endif
%endif

%changelog
* Wed Feb 18 2026 Silvan Scherrer <silvan.scherrer@aroa.ch> 3.47.2-1
- update version to 3.47.2
- add icu support
- adjust spec to fedora spec

* Wed Jul 03 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> 3.28.0-1
- update version to 3.28.0

* Wed Mar 27 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> 3.27.2-1
- update version to 3.27.2
- add a nice bldlevel to the dll
- use the nix codepath where possible
- use latest scm_ macros

* Mon Jan 16 2012 yd
- rebuild with libc 0.6.4 runtime.
