# bcond default logic is nicely backwards...
#%bcond_without tcl
#%bcond_with static
#%bcond_without check

%undefine tcl
%undefine with_tcl
%undefine static
%undefine with_static

# upstream doesn't provide separate -docs sources for all minor releases
%define basever 3.7.2
%define docver %(echo %{basever}|sed -e "s/\\./_/g")

Summary: Library that implements an embeddable SQL database engine
Name: sqlite
Version: %{basever}
Release: 1
License: Public Domain
Group: Applications/Databases
URL: http://www.sqlite.org/
Source0: http://www.sqlite.org/sqlite-%{version}.tar.gz
Source1: http://www.sqlite.org/sqlite_docs_%{docver}.zip

Patch1: sqlite-os2.diff

BuildRequires: ncurses-devel readline-devel libc-devel
# libdl patch needs
#BuildRequires: autoconf
%if %{with tcl}
#BuildRequires: /usr/bin/tclsh
#BuildRequires: tcl-devel
%{!?tcl_version: %global tcl_version 8.5}
%{!?tcl_sitearch: %global tcl_sitearch %{_libdir}/tcl%{tcl_version}}
%endif
BuildRoot: %{_tmppath}/%{name}-root

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
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
This package contains the header files and development documentation 
for %{name}. If you like to develop programs using %{name}, you will need 
to install %{name}-devel.

%package doc
Summary: Documentation for sqlite
Group: Documentation

%description doc
This package contains most of the static HTML files that comprise the
www.sqlite.org website, including all of the SQL Syntax and the 
C/C++ interface specs and other miscellaneous documentation.

%package -n lemon
Summary: A parser generator
Group: Development/Tools

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
Group: Development/Languages
Requires: %{name} = %{version}-%{release}
Requires: tcl(abi) = %{tcl_version}

%description tcl
This package contains the tcl modules for %{name}.
%endif

%prep
%setup -q -a1
%patch1 -p1 -b .os2~

%build
#autoconf
#export CFLAGS="$RPM_OPT_FLAGS -DSQLITE_ENABLE_COLUMN_METADATA=1 -DSQLITE_DISABLE_DIRSYNC=1 -DSQLITE_ENABLE_FTS3=3 -DSQLITE_ENABLE_RTREE=1 -Wall -fno-strict-aliasing"
export CONFIG_SHELL="/bin/sh"
export LDFLAGS="-Zbin-files -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lurpo"
%configure %{!?with_tcl:--disable-tcl} \
    --enable-threadsafe \
    --enable-threads-override-locks \
    --enable-load-extension \
    %{?with_tcl:TCLLIBDIR=%{tcl_sitearch}/sqlite3} \
    --disable-shared \
    "--cache-file=%{_topdir}/cache/%{name}.cache"

# rpath removal
#sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
#sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=${RPM_BUILD_ROOT} install

install -D -m0644 sqlite3.1 $RPM_BUILD_ROOT/%{_mandir}/man1/sqlite3.1
install -D -m0755 lemon.exe $RPM_BUILD_ROOT/%{_bindir}/lemon.exe
install -D -m0644 tool/lempar.c $RPM_BUILD_ROOT/%{_datadir}/lemon/lempar.c


%if %{with tcl}
# fix up permissions to enable dep extraction
#chmod 0755 ${RPM_BUILD_ROOT}/%{tcl_sitearch}/sqlite3/*.so
%endif

%if ! %{with static}
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.a
%endif

# YD install dll
install -D -m0755 sqlite3.dll $RPM_BUILD_ROOT/%{_libdir}/
install -D -m0755 .libs/sqlite3.a $RPM_BUILD_ROOT/%{_libdir}/
install -D -m0755 .libs/sqlite3_s.a $RPM_BUILD_ROOT/%{_libdir}/
install -D -m0755 .libs/sqlite3.lib $RPM_BUILD_ROOT/%{_libdir}/

# YD check requires tcl
#%if %{with check}
#%check
#%ifarch s390 ppc ppc64
#make test || :
#%else
#make test
#%endif
#%endif

%clean
rm -rf $RPM_BUILD_ROOT

#%post -p /sbin/ldconfig

#%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%doc README
%{_bindir}/sqlite3.exe
%{_libdir}/*.dll
%{_mandir}/man?/*

%files devel
%defattr(-, root, root)
%{_includedir}/*.h
%{_libdir}/*.dll
%{_libdir}/*.a
%{_libdir}/*.lib
%{_libdir}/pkgconfig/*.pc
%if %{with static}
%{_libdir}/*_s.a
%exclude %{_libdir}/*.la
%endif

%files doc
%defattr(-, root, root)
%doc %{name}-%{docver}-docs/*

%files -n lemon
%defattr(-, root, root)
%{_bindir}/lemon.exe
%{_datadir}/lemon

%if %{with tcl}
%files tcl
%defattr(-, root, root)
%{tcl_sitearch}/sqlite3
%endif

%changelog
