# the set of arches on which libgcj provides gcj and libgcj-javac-placeholder.sh
%define java_arches __%{ix86} alpha ia64 ppc sparc sparcv9 x86_64 s390 s390x
%define __soversion 4.8
%define __dllversion 48

# switch back to md5 file digests (due to rpm) until the dust settles a bit
%define _source_filedigest_algorithm 0
%define _binary_filedigest_algorithm 0

Summary: The Berkeley DB database library (version 4) for C
Name: db4
Version: 4.8.30
Release: 3%{?dist}
Source0: http://download.oracle.com/berkeley-db/db-%{version}.tar.gz

Patch0: db-os2.diff

URL: http://www.oracle.com/database/berkeley-db/
License: BSD
Group: System Environment/Libraries
# unversioned obsoletes are OK here as these BDB versions never occur again
Obsoletes: db1, db2, db3

Requires: mmap >= 20110102

#BuildRequires: perl, libtool, ed, util-linux-ng
BuildRequires: tcl-devel >= 8.5.2-3
%ifarch %{java_arches}
BuildRequires: gcc-java
BuildRequires: java-1.6.0-openjdk-devel
%endif
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. The Berkeley DB includes B+tree, Extended
Linear Hashing, Fixed and Variable-length record access methods,
transactions, locking, logging, shared memory caching, and database
recovery. The Berkeley DB supports C, C++, Java, and Perl APIs. It is
used by many applications, including Python and Perl, so this should
be installed on all systems.

%package cxx
Summary: The Berkeley DB database library (version 4) for C++
Group: System Environment/Libraries

%description cxx
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
Group: Applications/Databases
Requires: db4 = %{version}-%{release}
Obsoletes: db1-utils, db2-utils, db3-utils

%description utils
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. Berkeley DB includes B+tree, Extended
Linear Hashing, Fixed and Variable-length record access methods,
transactions, locking, logging, shared memory caching, and database
recovery. DB supports C, C++, Java and Perl APIs.

%package devel
Summary: C development files for the Berkeley DB (version 4) library
Group: Development/Libraries
Requires: db4 = %{version}-%{release}
Obsoletes: db1-devel, db2-devel, db3-devel

%description devel
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. This package contains the header files,
libraries, and documentation for building programs which use the
Berkeley DB.

%package devel-static
Summary: Berkeley DB (version 4) static libraries
Group: Development/Libraries

%description devel-static
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. This package contains static libraries
needed for applications that require statical linking of
Berkeley DB.

#%package tcl
#Summary: Development files for using the Berkeley DB (version 4) with tcl
#Group: Development/Libraries
#Requires: %{name} = %{version}-%{release}

#%description tcl
#The Berkeley Database (Berkeley DB) is a programmatic toolkit that
#provides embedded database support for both traditional and
#client/server applications. This package contains the libraries
#for building programs which use the Berkeley DB in Tcl.

#%package java
#Summary: Development files for using the Berkeley DB (version 4) with Java
#Group: Development/Libraries
#Requires: %{name} = %{version}-%{release}

#%description java
#The Berkeley Database (Berkeley DB) is a programmatic toolkit that
#provides embedded database support for both traditional and
#client/server applications. This package contains the libraries
#for building programs which use the Berkeley DB in Java.

%prep
%setup -q -n db-%{version}

%patch0 -p1 -b .os2~

# Remove tags files which we don't need.
find . -name tags | xargs rm -f
# Define a shell function for fixing HREF references in the docs, which
# would otherwise break when we split the docs up into subpackages.
fixup_href() {
	for doc in $@ ; do
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
}

set +x
# Fix all of the HTML files.
fixup_href `find . -name "*.html"`
set -x

#cd dist
#./s_config

mkdir dist/os2

%build
export CONFIG_SHELL="/bin/sh"
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp" 
export LIBS="-lurpo -lmmap -lpthread" 
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"

# Build the old db-185 libraries.
#make -C db.1.85/PORT/%{_os} OORG="$CFLAGS"

cd dist/os2
ln -sf ../configure .

	# XXX --enable-diagnostic should be disabled for production (but is
	# useful).
	# XXX --enable-debug_{r,w}op should be disabled for production.
	%configure -C \
    --enable-tcl --with-tcl=/@unixroot/usr/lib \
    --disable-shared --enable-static \
    --disable-cxx \
    --disable-java \
%ifarch %{java_arches}
		--enable-java \
%else
		--disable-java \
%endif
    "--cache-file=%{_topdir}/cache/%{name}.cache" \
		# --enable-diagnostic \
		# --enable-debug --enable-debug_rop --enable-debug_wop \

	# Remove libtool predep_objects and postdep_objects wonkiness so that
	# building without -nostdlib doesn't include them twice.  Because we
	# already link with g++, weird stuff happens if you don't let the
	# compiler handle this.
#	perl -pi -e 's/^predep_objects=".*$/predep_objects=""/' libtool
#	perl -pi -e 's/^postdep_objects=".*$/postdep_objects=""/' libtool
#	perl -pi -e 's/-shared -nostdlib/-shared/' libtool

	make %{?_smp_mflags}

#	# XXX hack around libtool not creating ./libs/libdb_java-X.Y.lai
#	LDBJ=./.libs/libdb_java-%{__soversion}.la
#	if test -f ${LDBJ} -a ! -f ${LDBJ}i; then
#		sed -e 's,^installed=no,installed=yes,' < ${LDBJ} > ${LDBJ}i
#	fi


%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_includedir}
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}

%makeinstall -C dist/os2

cp dist/os2/libdb-%{__soversion}_s.a ${RPM_BUILD_ROOT}%{_libdir}

# XXX Nuke non-versioned archives and symlinks
rm -f ${RPM_BUILD_ROOT}%{_libdir}/libdb.a
rm -f ${RPM_BUILD_ROOT}%{_libdir}/libdb_cxx.a

# Move the main shared library from /usr/lib* to /lib* directory.
#if [ "%{_libdir}" != "/%{_lib}" ]; then
#  mkdir -p $RPM_BUILD_ROOT/%{_lib}/
#  mv $RPM_BUILD_ROOT/%{_libdir}/libdb-%{__soversion}.so $RPM_BUILD_ROOT/%{_lib}/
# Leave relative symlinks in %{_libdir}.
#  touch $RPM_BUILD_ROOT/rootfile
#  root=..
#  while [ ! -e $RPM_BUILD_ROOT/%{_libdir}/${root}/rootfile ] ; do
#	root=${root}/..
#  done
#  rm $RPM_BUILD_ROOT/rootfile
#
#  ln -sf ${root}/%{_lib}/libdb-%{__soversion}.so $RPM_BUILD_ROOT/%{_libdir}/libdb.so
#  ln -sf ${root}/%{_lib}/libdb-%{__soversion}.so $RPM_BUILD_ROOT/%{_libdir}/
#  ln -sf libdb_cxx-%{__soversion}.so $RPM_BUILD_ROOT/%{_libdir}/libdb_cxx.so
#fi

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

# XXX Avoid Permission denied. strip when building as non-root.
#chmod u+w ${RPM_BUILD_ROOT}%{_bindir} ${RPM_BUILD_ROOT}%{_bindir}/*

# remove unneeded .la files (#225675)
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la

%clean
rm -rf ${RPM_BUILD_ROOT}

#%post -p /sbin/ldconfig

#%postun -p /sbin/ldconfig

#%post -p /sbin/ldconfig tcl

#%postun -p /sbin/ldconfig tcl

#%post -p /sbin/ldconfig java

#%postun -p /sbin/ldconfig java

%files
%defattr(-,root,root)
%doc LICENSE README
%{_libdir}/db%{__dllversion}.dll

#%files cxx
#%defattr(-,root,root)
#%{_libdir}/libdb_cxx-%{__soversion}.so

%files utils
%defattr(-,root,root)
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

%files devel
%defattr(-,root,root)
#%doc	docs/*
#%doc	examples_c examples_cxx
%{_libdir}/db*.dll
#%{_libdir}/libdb_cxx.so
%{_libdir}/libdb-%{__soversion}.a
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/db.h
#%{_includedir}/%{name}/db_185.h
%{_includedir}/%{name}/db_cxx.h
%{_includedir}/db.h
#%{_includedir}/db_185.h
%{_includedir}/db_cxx.h

%files devel-static
%defattr(-,root,root)
%{_libdir}/libdb-%{__soversion}_s.a
#%{_libdir}/libdb_cxx-%{__soversion}.a
#%{_libdir}/libdb_tcl-%{__soversion}.a
%ifarch %{java_arches}
%{_libdir}/libdb_java-%{__soversion}.a
%endif

#%files tcl
#%defattr(-,root,root)
#%{_libdir}/libdb_tcl-%{__soversion}.so

#%ifarch %{java_arches}
#%files java
#%defattr(-,root,root)
#%doc docs/java
#%doc examples_java
#%{_libdir}/libdb_java*.so
#%{_datadir}/java/*.jar
#%endif

%changelog
