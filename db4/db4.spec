 
# the set of arches on which libgcj provides gcj and libgcj-javac-placeholder.sh
#%define java_arches __%{ix86} alpha ia64 ppc sparc sparcv9 x86_64 s390 s390x
%define java_arches 0
%global __soversion_major 4
%global __soversion %{__soversion_major}.8
%global __dllversion %{__soversion_major}8

# switch back to md5 file digests (due to rpm) until the dust settles a bit
%define _source_filedigest_algorithm 0
%define _binary_filedigest_algorithm 0

Summary: The Berkeley DB database library (version 4) for C
Name: db4
Version: 4.8.30
Release: 9%{?dist}

Vendor:  bww bitwise works GmbH
#scm_source  github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2
%scm_source  git e:/trees/db4/git master

URL: http://www.oracle.com/database/berkeley-db/
License: Sleepycat and BSD

BuildRequires: perl, libtool, ed, tcl-devel
#BuildRequires: util-linux-ng
BuildRequires: tcl-devel >= 8.5.2-3
%ifarch %{java_arches}
BuildRequires: java-1.6.0-openjdk-devel
%endif


%description
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. The Berkeley DB includes B+tree, Extended
Linear Hashing, Fixed and Variable-length record access methods,
transactions, locking, logging, shared memory caching, and database
recovery. The Berkeley DB supports C, C++, Java, and Perl APIs. It is
used by many applications, including Python and Perl, so this should
be installed on all systems.

%package utils
Summary: Command line tools for managing Berkeley DB (version 4) databases
Requires: %{name} = %{version}-%{release}

%description utils
This package contains command-line tools for managing Berkeley DB (version
4) databases.

%package devel
Summary: C development files for the Berkeley DB (version 4) library
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files and libraries for building C
programs which use the Berkley DB.

%package doc
Summary: Documentation for the Berkeley DB
BuildArch: noarch

%description doc
This package includes documentation files for the Berkeley DB database.

%package devel-static
Summary: Berkeley DB (version 4) static libraries
Requires: %{name}-devel = %{version}-%{release}

%description devel-static
This package contains static libraries needed for applications that
require static linking of Berkley DB.

%package cxx
Summary: The Berkeley DB database library (version 4) for C++
Requires: %{name} = %{version}-%{release}

%description cxx
This package contains the C++ version of the Berkley DB library (v4).

%package cxx-devel
Summary: C++ development files for the Berkeley DB library (version 4)
Requires: %{name}-cxx = %{version}-%{release}
Requires: %{name}-devel = %{version}-%{release}

%description cxx-devel
This package contains the header files and libraries for building C++
programs which use the Berkley DB.

%package tcl
Summary: Development files for using the Berkeley DB (version 4) with tcl
Requires: %{name} = %{version}-%{release}

%description tcl
This package contains the libraries for building programs which use the
Berkley DB in Tcl.

%package tcl-devel
Summary: Development files for using the the Berkeley DB (version 4) with tcl
Requires: %{name}-tcl = %{version}-%{release}

%description tcl-devel
This package contains the libraries for building programs which use the
Berkley DB in Tcl.

%ifarch %{java_arches}
%package java
Summary: Development files for using the Berkeley DB (version 4) with Java
Requires: %{name} = %{version}-%{release}

%description java
This package contains the libraries for building programs which use the
Berkley DB in Java.

%package java-devel
Summary: Development files for using the Berkeley DB (version 4) with Java
Requires: %{name}-java = %{version}-%{release}

%description java-devel
This package contains the libraries for building programs which use the
Berkley DB in Java.
%endif

%debug_package

%prep
%scm_setup

# Fix HREF references in the docs, which would otherwise break when we split the docs up into subpackages.
set +x
for doc in `find . -name "*.html"`; do
	chmod u+w ${doc}
	sed	-e 's,="../api_c/,="../../%{name}-devel-%{version}/api_c/,g' \
		-e 's,="api_c/,="../%{name}-devel-%{version}/api_c/,g' \
		-e 's,="../api_cxx/,="../../%{name}-devel-%{version}/api_cxx/,g' \
		-e 's,="api_cxx/,="../%{name}-devel-%{version}/api_cxx/,g' \
		-e 's,="../api_tcl/,="../../%{name}-devel-%{version}/api_tcl/,g' \
		-e 's,="api_tcl/,="../%{name}-devel-%{version}/api_tcl/,g' \
		-e 's,="../java/,="../../%{name}-devel-%{version}/java/,g' \
		-e 's,="java/,="../%{name}-devel-%{version}/java/,g' \
		-e 's,="../examples_c/,="../../%{name}-devel-%{version}/examples_c/,g' \
		-e 's,="examples_c/,="../%{name}-devel-%{version}/examples_c/,g' \
		-e 's,="../examples_cxx/,="../../%{name}-devel-%{version}/examples_cxx/,g' \
		-e 's,="examples_cxx/,="../%{name}-devel-%{version}/examples_cxx/,g' \
		-e 's,="../ref/,="../../%{name}-devel-%{version}/ref/,g' \
		-e 's,="ref/,="../%{name}-devel-%{version}/ref/,g' \
		-e 's,="../images/,="../../%{name}-devel-%{version}/images/,g' \
		-e 's,="images/,="../%{name}-devel-%{version}/images/,g' \
		-e 's,="../utility/,="../../%{name}-utils-%{version}/utility/,g' \
		-e 's,="utility/,="../%{name}-utils-%{version}/utility/,g' ${doc} > ${doc}.new
	touch -r ${doc} ${doc}.new
	cat ${doc}.new > ${doc}
	touch -r ${doc}.new ${doc}
	rm -f ${doc}.new
done
set -x

cd dist
./s_config

%build
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp" 
export LIBS="-lcx -lpthread" 
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
export VENDOR="%{vendor}"

# Build the old db-185 libraries.
#make -C db.1.85/PORT/%{_os} OORG="$CFLAGS"

test -d dist/os2 || mkdir dist/os2
cd dist/os2
# we need to copy it, as else brain dead config.status doesn't work
cp ../configure .

%configure -C \
    --enable-compat185 \
    --enable-shared --enable-static \
    --enable-cxx \
    --enable-tcl --with-tcl=%{_libdir} \
    --enable-test \
%ifarch %{java_arches}
    --enable-java \
%else
    --disable-java \
%endif

# Remove libtool predep_objects and postdep_objects wonkiness so that
# building without -nostdlib doesn't include them twice.  Because we
# already link with g++, weird stuff happens if you don't let the
# compiler handle this.
#	perl -pi -e 's/^predep_objects=".*$/predep_objects=""/' libtool
#	perl -pi -e 's/^postdep_objects=".*$/postdep_objects=""/' libtool
#	perl -pi -e 's/-shared -nostdlib/-shared/' libtool

make %{?_smp_mflags}

%ifarch %{java_arches}
# XXX hack around libtool not creating ./libs/libdb_java-X.Y.lai
LDBJ=./.libs/libdb_java-%{__soversion}.la
if test -f ${LDBJ} -a ! -f ${LDBJ}i; then
	sed -e 's,^installed=no,installed=yes,' < ${LDBJ} > ${LDBJ}i
fi
%endif
cd ..
cd ..

%install
mkdir -p ${RPM_BUILD_ROOT}%{_includedir}
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}

%makeinstall STRIP=/@unixroot/usr/bin/true -C dist/os2

# XXX Nuke non-versioned archives and symlinks
rm -f ${RPM_BUILD_ROOT}%{_libdir}/libdb.a
rm -f ${RPM_BUILD_ROOT}%{_libdir}/libdb_cxx.a

chmod +x ${RPM_BUILD_ROOT}%{_libdir}/*.dll

# add symlink without version number
ln -s db-%{__soversion}_dll.a $RPM_BUILD_ROOT/%{_libdir}/db_dll.a
ln -s db_cxx-%{__soversion}_dll.a $RPM_BUILD_ROOT/%{_libdir}/db_cxx_dll.a
ln -s db_tcl-%{__soversion}_dll.a $RPM_BUILD_ROOT/%{_libdir}/db_tcl_dll.a

# Move the header files to a subdirectory, in case we're deploying on a
# system with multiple versions of DB installed.
mkdir -p ${RPM_BUILD_ROOT}%{_includedir}/db4
mv ${RPM_BUILD_ROOT}%{_includedir}/*.h ${RPM_BUILD_ROOT}%{_includedir}/db4/

# Create symlinks to includes so that "use <db.h> and link with -ldb" works.
# db_185.h
for i in db.h db_cxx.h; do
	ln -s db4/$i ${RPM_BUILD_ROOT}%{_includedir}
done

%ifarch %{java_arches}
# Move java jar file to the correct place
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/java
mv ${RPM_BUILD_ROOT}%{_libdir}/*.jar ${RPM_BUILD_ROOT}%{_datadir}/java
%endif

# Eliminate installed doco
rm -rf ${RPM_BUILD_ROOT}%{_prefix}/docs

# unify documentation and examples, rmove stuff we don't need
rm -rf docs/csharp
rm -rf examples/csharp
rm -rf docs/installation

# XXX Avoid Permission denied. strip when building as non-root.
chmod u+w ${RPM_BUILD_ROOT}%{_bindir} ${RPM_BUILD_ROOT}%{_bindir}/*

# remove unneeded .la files (#225675)
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la


%files
%license LICENSE
%doc README
%{_libdir}/db%{__dllversion}.dll

%files devel
%{_libdir}/db-%{__soversion}_dll.a
%{_libdir}/db_dll.a
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/db.h
%{_includedir}/%{name}/db_185.h
%{_includedir}/db.h

%files doc
%doc docs/*
%doc examples_c examples_cxx examples_java

%files devel-static
%{_libdir}/db-%{__soversion}.a
%{_libdir}/db_cxx-%{__soversion}.a
%{_libdir}/db_tcl-%{__soversion}.a
%ifarch %{java_arches}
%{_libdir}/libdb_java-%{__soversion}.a
%endif

%files utils
%{_bindir}/db*_archive.exe
%{_bindir}/db*_checkpoint.exe
%{_bindir}/db*_deadlock.exe
%{_bindir}/db*_dump*.exe
%{_bindir}/db*_hotbackup.exe
%{_bindir}/db*_load.exe
%{_bindir}/db*_printlog.exe
%{_bindir}/db*_recover.exe
%{_bindir}/db*_sql.exe
%{_bindir}/db*_stat.exe
%{_bindir}/db*_upgrade.exe
%{_bindir}/db*_verify.exe

%files cxx
%{_libdir}/db%{__dllversion}cxx.dll

%files cxx-devel
%{_includedir}/%{name}/db_cxx.h
%{_includedir}/db_cxx.h
%{_libdir}/db_cxx*_dll.a

%files tcl
%{_libdir}/db%{__dllversion}tcl.dll

%files tcl-devel
%{_libdir}/db_tcl*_dll.a

%ifarch %{java_arches}
%files java
%{_libdir}/libdb_java*.so
%{_datadir}/java/*.jar

%files java-devel
%{_libdir}/db_java*_dll.a
%endif

%changelog
* Fri Feb 21 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> 4.8.30-9
- fix some /tmp glitches which crashed heimdal
- rebuilt with gcc 9
- big overhaul of the spec file
- add documentation

* Thu Apr 13 2017 yd <yd@os2power.com> 4.8.30-8
- enable db 1.8.5 compatibility api.

* Wed Feb 08 2017 yd <yd@os2power.com> 4.8.30-7
- r1981, disable docs.
- r1980, remove mmap hack.
- build with libcx memory mapping.
- update build scripts.

* Wed Jan 11 2012 yd
- avoid hpfs386 unpacking issues.

* Mon Jan 09 2012 yd
- build also c++ dll.
- include docs in developer package.

