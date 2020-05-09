%global gcc_major 9
%global gcc_version %{gcc_major}.2.0
# Note, gcc_release must be integer, if you want to add suffixes to
# %%{release}, append them after %%{gcc_release} on Release: line.
%global gcc_release 4

%global build_ada 0
%global build_objc 0
%global build_go 0
%global build_d 0
%global build_gfortran 0

%global build_libquadmath 1
%global build_libasan 0
%global build_libtsan 0
%global build_liblsan 0
%global build_libubsan 0
%global build_libatomic 0
%global build_libitm 0
%global build_libgomp 0
%global build_libgccjit 0
%global build_isl 0
%global build_libstdcxx_docs 0
%global attr_ifunc 0

%global enable_plugin 0
%global enable_gdb 0

Summary: Various compilers (C, C++, Objective-C, ...)
Name: gcc
Version: %{gcc_version}
Release: %{gcc_release}%{?dist}
# libgcc, libgfortran, libgomp, libstdc++ and crtstuff have
# GCC Runtime Exception.
License: GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions and LGPLv2+ and BSD

# OS/2 uses its own Git repo
## The source for this package was pulled from upstream's vcs.  Use the
## following commands to generate the tarball:
## svn export svn://gcc.gnu.org/svn/gcc/branches/redhat/gcc-9-branch@%%{SVNREV} gcc-%%{version}-%%{DATE}
## tar cf - gcc-%%{version}-%%{DATE} | xz -9e > gcc-%%{version}-%%{DATE}.tar.xz
#Source0: gcc-%{version}-%{DATE}.tar.xz

# GCC uses tags with underscores between version components.
%{lua:
rpm.define(string.format("version_underscores %s",
           string.gsub(rpm.expand('%{version}'), '%.', '_')))
}

%scm_source github https://github.com/bitwiseworks/gcc-os2 gcc-%{version_underscores}-release-os2-b2
#scm_source git file://D:/Coding/gcc/master cf3ddd6

Source1: gcc335.def
Source2: gcc432.def
Source3: gcc433.def
Source4: gcc434.def
Source5: gcc435.def
Source6: gcc440.def
Source7: gcc441.def
Source8: gcc442.def
Source9: gcc444.def
Source10: gcc445.def
Source11: gcc446.def
Source12: gcc452.def
Source13: gcc453.def
Source14: gcc454.def
Source15: gcc464.def
Source16: gcc473.def
Source17: gcc474.def
Source18: gcc482.def
Source19: gcc483.def
Source20: gcc490.def
Source21: gcc491.def
Source22: gcc492.def
Source23: fwdstub.s

Source101: ssp.def
Source102: stdcpp.def

%global isl_version 0.16.1

URL: http://gcc.gnu.org
Vendor:  bww bitwise works GmbH

# For fixed EMXOMF with new libibetry from binutils 2.33.1, wide char support.
Requires: libc >= 1:0.1.4
BuildRequires: libc-devel >= 1:0.1.4
BuildRequires: binutils >= 2.33.1, make

BuildRequires: zlib-devel, gettext, bison, flex
BuildRequires: gettext-devel
# TODO don't have these
# dejagnu, sharutils
BuildRequires: texinfo, perl
# TODO texinfo tex is broken for now
# texinfo-tex
BuildRequires: gmp-devel >= 4.1.2-8, mpfr-devel >= 2.2.1, libmpc-devel >= 0.8.1
BuildRequires: python-devel python
BuildRequires: gcc gcc-c++
BuildRequires: gcc-wlink
# Need Libtool with LT_BUILDLEVEL support.
BuildRequires: libtool >= 2.4.6-4
%if %{build_go}
BuildRequires: hostname, procps
%endif
%if %{build_ada}
# Ada requires Ada to build
BuildRequires: gcc-gnat >= 3.1, libgnat >= 3.1
%endif
%if %{build_isl}
BuildRequires: isl = %{isl_version}
BuildRequires: isl-devel = %{isl_version}
Requires: libisl.so.15
%endif
%if %{build_libstdcxx_docs}
BuildRequires: doxygen >= 1.7.1
BuildRequires: graphviz, dblatex, texlive-collection-latex, docbook5-style-xsl
%endif
Requires: cpp = %{version}-%{release}
Requires: libgcc = %{version}-%{release}
%if %{build_libgomp}
Requires: libgomp = %{version}-%{release}
%endif
# TODO not sure we need this.
%if 0
Provides: bundled(libiberty)
%endif
Provides: gcc(major) = %{gcc_major}

# Under OS/2, RPM target platform is always i386 for now. But we want it to be
# be at least i686 for gcc (as build/host/target) to make it use some CPU
# optimizations (e.g i486/atomicity.h in libstdc++ instead of i386/atomicity.h
# and similar things). Note that this will also be used as a default value for
# -mtune and -march options.
%global gcc_target_cpu i686

# TODO _target_platform is broken (see https://github.com/bitwiseworks/rpm-os2/issues/1),
# use _host for now which is a regular configure triplet (cpu-vendor-os).
%global gcc_target_platform %{lua: print((string.gsub(rpm.expand('%{_host}'), '^[%a%d]+', rpm.expand('%{gcc_target_cpu}'))))}

%if %{build_go}
# Avoid stripping these libraries and binaries.
%global __os_install_post \
chmod 644 %{buildroot}%{_prefix}/%{_lib}/libgo.so.14.* \
chmod 644 %{buildroot}%{_prefix}/bin/go.gcc \
chmod 644 %{buildroot}%{_prefix}/bin/gofmt.gcc \
chmod 644 %{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/cgo \
chmod 644 %{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/buildid \
chmod 644 %{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/test2json \
chmod 644 %{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/vet \
%__os_install_post \
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgo.so.14.* \
chmod 755 %{buildroot}%{_prefix}/bin/go.gcc \
chmod 755 %{buildroot}%{_prefix}/bin/gofmt.gcc \
chmod 755 %{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/cgo \
chmod 755 %{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/buildid \
chmod 755 %{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/test2json \
chmod 755 %{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/vet \
%{nil}
%endif

%description
The gcc package contains the GNU Compiler Collection version %{gcc_major}.
You'll need this package in order to compile C code.

%package -n libgcc
Summary: GCC version %{gcc_major} shared support library
# Obsolete GCC 4.x package
Obsoletes: libgcc1 < %{version}-%{release}
Provides: libgcc1 = %{version}-%{release}

%description -n libgcc
This package contains GCC shared support library which is needed
e.g. for exception handling support.

%package -n libgcc-fwd
Summary: GCC shared support forwarder library
Obsoletes: libgcc335 libgcc432 libgcc433 libgcc434 libgcc440 libgcc441
Obsoletes: libgcc442 libgcc444 libgcc445 libgcc446 libgcc452 libgcc453
Obsoletes: libgcc473 libgcc490 libgcc492
Requires: libgcc = %{version}-%{release}

%description -n libgcc-fwd
This package contains GCC shared support forwarder library which is needed
e.g. for exception handling support in programs compiled with earlier
GCC versions.

%package -n libssp
Summary: GCC version %{gcc_major} stack protector library
Requires: libgcc = %{version}-%{release}
Obsoletes: gcc-stack-protector

%description -n libssp
This package contains GCC library which is needed
for stack protector support.

%package -n libssp-fwd
Summary: GCC stack protector support forwarder library
Requires: libssp = %{version}-%{release}

%description -n libssp-fwd
This package contains GCC forwarder library which is needed
for stack protector support in programs compiled with earlier
GCC versions.

%package -n libssp-devel
Summary: Header files and libraries for GCC stack protector
Requires: libssp = %{version}-%{release}

%description -n libssp-devel
This package includes the header files and libraries needed for using
the GCC stack protector feature.

%package c++
Summary: C++ support for GCC
Requires: gcc = %{version}-%{release}
Requires: libstdc++ = %{version}-%{release}
Requires: libstdc++-devel = %{version}-%{release}
Provides: gcc-g++ = %{version}-%{release}
Provides: g++ = %{version}-%{release}

%description c++
This package adds C++ support to the GNU Compiler Collection.
It includes support for most of the current C++ specification,
including templates and exception handling.

%package -n libstdc++
Summary: GNU Standard C++ Library
Requires: libgcc = %{version}-%{release}
# Obsolete GCC 4.x packages
Obsoletes: libstdc++6 < %{version}-%{release}
Obsoletes: libsupc++6 < %{version}-%{release}
Provides: libstdc++6 = %{version}-%{release}
Provides: libsupc++6 = %{version}-%{release}

%description -n libstdc++
The libstdc++ package contains a rewritten standard compliant GCC Standard
C++ Library.

%package -n libstdc++-fwd
Summary: GCC Standard C++ forwarder library
Requires: libstdc++ = %{version}-%{release}

%description -n libstdc++-fwd
This package contains GCC Standard C++ forwarder library which is needed
for C++ support in programs compiled with earlier GCC versions.

%package -n libstdc++-devel
Summary: Header files and libraries for C++ development
Requires: libstdc++ = %{version}-%{release}

%description -n libstdc++-devel
This is the GNU implementation of the standard C++ libraries.  This
package includes the header files and libraries needed for C++
development. This includes rewritten implementation of STL.

%package -n libstdc++-static
Summary: Static libraries for the GNU standard C++ library
Requires: libstdc++-devel = %{version}-%{release}

%description -n libstdc++-static
Static libraries for the GNU standard C++ library.

%if %{build_libstdcxx_docs}
%package -n libstdc++-docs
Summary: Documentation for the GNU standard C++ library

%description -n libstdc++-docs
Manual, doxygen generated API information and Frequently Asked Questions
for the GNU standard C++ library.
%endif

%if %{build_objc}
%package objc
Summary: Objective-C support for GCC
Requires: gcc = %{version}-%{release}
Requires: libobjc = %{version}-%{release}

%description objc
gcc-objc provides Objective-C support for the GCC.
Mainly used on systems running NeXTSTEP, Objective-C is an
object-oriented derivative of the C language.

%package objc++
Summary: Objective-C++ support for GCC
Requires: gcc-c++ = %{version}-%{release}, gcc-objc = %{version}-%{release}

%description objc++
gcc-objc++ package provides Objective-C++ support for the GCC.

%package -n libobjc
Summary: Objective-C runtime

%description -n libobjc
This package contains Objective-C shared library which is needed to run
Objective-C dynamically linked programs.
%endif

%if %{build_gfortran}
%package gfortran
Summary: Fortran support
Requires: gcc = %{version}-%{release}
Requires: libgfortran = %{version}-%{release}
%if %{build_libquadmath}
Requires: libquadmath = %{version}-%{release}
Requires: libquadmath-devel = %{version}-%{release}
%endif
Provides: gcc-fortran = %{version}-%{release}
Provides: gfortran = %{version}-%{release}

%description gfortran
The gcc-gfortran package provides support for compiling Fortran
programs with the GNU Compiler Collection.

%package -n libgfortran
Summary: Fortran runtime
%if %{build_libquadmath}
Requires: libquadmath = %{version}-%{release}
%endif

%description -n libgfortran
This package contains Fortran shared library which is needed to run
Fortran dynamically linked programs.

%package -n libgfortran-static
Summary: Static Fortran libraries
Requires: libgfortran = %{version}-%{release}
Requires: gcc = %{version}-%{release}
%if %{build_libquadmath}
Requires: libquadmath-static = %{version}-%{release}
%endif

%description -n libgfortran-static
This package contains static Fortran libraries.
%endif

%if %{build_d}
%package gdc
Summary: D support
Requires: gcc = %{version}-%{release}
Requires: libgphobos = %{version}-%{release}
Provides: gcc-d = %{version}-%{release}
Provides: gdc = %{version}-%{release}

%description gdc
The gcc-gdc package provides support for compiling D
programs with the GNU Compiler Collection.

%package -n libgphobos
Summary: D runtime

%description -n libgphobos
This package contains D shared library which is needed to run
D dynamically linked programs.

%package -n libgphobos-static
Summary: Static D libraries
Requires: libgphobos = %{version}-%{release}
Requires: gcc-gdc = %{version}-%{release}

%description -n libgphobos-static
This package contains static D libraries.
%endif

%if %{build_libgomp}
%package -n libgomp
Summary: GCC OpenMP v4.5 shared support library

%description -n libgomp
This package contains GCC shared support library which is needed
for OpenMP v4.5 support.
%endif

%if %{enable_gdb}
%package gdb-plugin
Summary: GCC plugin for GDB
Requires: gcc = %{version}-%{release}

%description gdb-plugin
This package contains GCC plugin for GDB C expression evaluation.
%endif

%if %{build_libgccjit}
%package -n libgccjit
Summary: Library for embedding GCC inside programs and libraries
Requires: gcc = %{version}-%{release}

%description -n libgccjit
This package contains shared library with GCC JIT front-end.

%package -n libgccjit-devel
Summary: Support for embedding GCC inside programs and libraries
BuildRequires: python-sphinx
Requires: libgccjit = %{version}-%{release}

%description -n libgccjit-devel
This package contains header files and documentation for GCC JIT front-end.
%endif

%package -n libquadmath
Summary: GCC __float128 shared support library

%description -n libquadmath
This package contains GCC shared support library which is needed
for __float128 math support and for Fortran REAL*16 support.

%package -n libquadmath-devel
Summary: GCC __float128 support
Requires: libquadmath = %{version}-%{release}
Requires: gcc = %{version}-%{release}

%description -n libquadmath-devel
This package contains headers for building Fortran programs using
REAL*16 and programs using __float128 math.

%package -n libquadmath-static
Summary: Static libraries for __float128 support
Requires: libquadmath-devel = %{version}-%{release}

%description -n libquadmath-static
This package contains static libraries for building Fortran programs
using REAL*16 and programs using __float128 math.

%if %{build_libitm}
%package -n libitm
Summary: The GNU Transactional Memory library

%description -n libitm
This package contains the GNU Transactional Memory library
which is a GCC transactional memory support runtime library.

%package -n libitm-devel
Summary: The GNU Transactional Memory support
Requires: libitm = %{version}-%{release}
Requires: gcc = %{version}-%{release}

%description -n libitm-devel
This package contains headers and support files for the
GNU Transactional Memory library.

%package -n libitm-static
Summary: The GNU Transactional Memory static library
Requires: libitm-devel = %{version}-%{release}

%description -n libitm-static
This package contains GNU Transactional Memory static libraries.
%endif

%if %{build_libatomic}
%package -n libatomic
Summary: The GNU Atomic library

%description -n libatomic
This package contains the GNU Atomic library
which is a GCC support runtime library for atomic operations not supported
by hardware.

%package -n libatomic-static
Summary: The GNU Atomic static library
Requires: libatomic = %{version}-%{release}

%description -n libatomic-static
This package contains GNU Atomic static libraries.
%endif

%if %{build_libasan}
%package -n libasan
Summary: The Address Sanitizer runtime library

%description -n libasan
This package contains the Address Sanitizer library
which is used for -fsanitize=address instrumented programs.

%package -n libasan-static
Summary: The Address Sanitizer static library
Requires: libasan = %{version}-%{release}

%description -n libasan-static
This package contains Address Sanitizer static runtime library.
%endif

%if %{build_libtsan}
%package -n libtsan
Summary: The Thread Sanitizer runtime library

%description -n libtsan
This package contains the Thread Sanitizer library
which is used for -fsanitize=thread instrumented programs.

%package -n libtsan-static
Summary: The Thread Sanitizer static library
Requires: libtsan = %{version}-%{release}

%description -n libtsan-static
This package contains Thread Sanitizer static runtime library.
%endif

%if %{build_libubsan}
%package -n libubsan
Summary: The Undefined Behavior Sanitizer runtime library

%description -n libubsan
This package contains the Undefined Behavior Sanitizer library
which is used for -fsanitize=undefined instrumented programs.

%package -n libubsan-static
Summary: The Undefined Behavior Sanitizer static library
Requires: libubsan = %{version}-%{release}

%description -n libubsan-static
This package contains Undefined Behavior Sanitizer static runtime library.
%endif

%if %{build_liblsan}
%package -n liblsan
Summary: The Leak Sanitizer runtime library

%description -n liblsan
This package contains the Leak Sanitizer library
which is used for -fsanitize=leak instrumented programs.

%package -n liblsan-static
Summary: The Leak Sanitizer static library
Requires: liblsan = %{version}-%{release}

%description -n liblsan-static
This package contains Leak Sanitizer static runtime library.
%endif

%package -n cpp
Summary: The C Preprocessor
Provides: /lib/cpp
Requires: libgcc = %{version}-%{release}
Requires: libstdc++ = %{version}-%{release}

%description -n cpp
Cpp is the GNU C-Compatible Compiler Preprocessor.
Cpp is a macro processor which is used automatically
by the C compiler to transform your program before actual
compilation. It is called a macro processor because it allows
you to define macros, abbreviations for longer
constructs.

The C preprocessor provides four separate functionalities: the
inclusion of header files (files of declarations that can be
substituted into your program); macro expansion (you can define macros,
and the C preprocessor will replace the macros with their definitions
throughout the program); conditional compilation (using special
preprocessing directives, you can include or exclude parts of the
program according to various conditions); and line control (if you use
a program to combine or rearrange source files into an intermediate
file which is then compiled, you can use line control to inform the
compiler about where each source line originated).

You should install this package if you are a C programmer and you use
macros.

%if %{build_ada}
%package gnat
Summary: Ada 83, 95, 2005 and 2012 support for GCC
Requires: gcc = %{version}-%{release}
Requires: libgnat = %{version}-%{release}, libgnat-devel = %{version}-%{release}

%description gnat
GNAT is a GNU Ada 83, 95, 2005 and 2012 front-end to GCC. This package includes
development tools, the documents and Ada compiler.

%package -n libgnat
Summary: GNU Ada 83, 95, 2005 and 2012 runtime shared libraries

%description -n libgnat
GNAT is a GNU Ada 83, 95, 2005 and 2012 front-end to GCC. This package includes
shared libraries, which are required to run programs compiled with the GNAT.

%package -n libgnat-devel
Summary: GNU Ada 83, 95, 2005 and 2012 libraries

%description -n libgnat-devel
GNAT is a GNU Ada 83, 95, 2005 and 2012 front-end to GCC. This package includes
libraries, which are required to compile with the GNAT.

%package -n libgnat-static
Summary: GNU Ada 83, 95, 2005 and 2012 static libraries
Requires: libgnat-devel = %{version}-%{release}

%description -n libgnat-static
GNAT is a GNU Ada 83, 95, 2005 and 2012 front-end to GCC. This package includes
static libraries.
%endif

%if %{build_go}
%package go
Summary: Go support
Requires: gcc = %{version}-%{release}
Requires: libgo = %{version}-%{release}
Requires: libgo-devel = %{version}-%{release}
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives
Provides: gccgo = %{version}-%{release}

%description go
The gcc-go package provides support for compiling Go programs
with the GNU Compiler Collection.

%package -n libgo
Summary: Go runtime

%description -n libgo
This package contains Go shared library which is needed to run
Go dynamically linked programs.

%package -n libgo-devel
Summary: Go development libraries
Requires: libgo = %{version}-%{release}

%description -n libgo-devel
This package includes libraries and support files for compiling
Go programs.

%package -n libgo-static
Summary: Static Go libraries
Requires: libgo = %{version}-%{release}
Requires: gcc = %{version}-%{release}

%description -n libgo-static
This package contains static Go libraries.
%endif

%if %{enable_plugin}
%package plugin-devel
Summary: Support for compiling GCC plugins
Requires: gcc = %{version}-%{release}
Requires: gmp-devel >= 4.1.2-8, mpfr-devel >= 2.2.1, libmpc-devel >= 0.8.1

%description plugin-devel
This package contains header files and other support files
for compiling GCC plugins.  The GCC plugin ABI is currently
not stable, so plugins must be rebuilt any time GCC is updated.
%endif

%package wlink
Summary: GCC configuration changes for Watcom linker support.
Group: Development/Languages
Requires: watcom-wlink-hll
Requires: gcc = %{version}-%{release}

%description wlink
This package triggers the required CONFIG.SYS settings to allow use of Watcom
Linker instead of ld.

%package wrc
Summary: GCC configuration changes for Watcom resource compiler support.
Group: Development/Languages
Requires: watcom-wrc
Requires: gcc = %{version}-%{release}

%description wrc
This package triggers the required CONFIG.SYS settings to allow use of Watcom
resource compiler instead of IBM one.

%debug_package

%prep
#setup -q -n gcc-%{version}-%{DATE} -a 1 -a 2
%scm_setup

# Move relevant sources to build subdir to reference them by name instead of SOURCEx
for src in %{sources}; do
  case $src in
  *.zip) ;;
  *) %{__cp} -a $src .;;
  esac
done

echo 'OS/2 RPM build %{version}-%{release}' > gcc/DEV-PHASE

# TODO not sure if we need this given that we run autoreconf.
#./contrib/gcc_update --touch

LC_ALL=C sed -i -e 's/\xa0/ /' gcc/doc/options.texi

sed -i -e 's/Common Driver Var(flag_report_bug)/& Init(1)/' gcc/common.opt

# This test causes fork failures, because it spawns way too many threads
rm -f gcc/testsuite/go.test/test/chan/goroutines.go

# Cook all generated stuff (our Git doesn't store it).
autogen.sh

# TODO hack around gcc1.dll BLDLEVEL string (temporary, should go away
# once https://github.com/bitwiseworks/gcc-os2/issues/9 is done).
sed -i -e 's/GNU GCC Runtime Version $(gcc_version)-$(RPM_PACKAGE_RELEASE)/$(LT_BUILDLEVEL)@@GNU GCC Runtime/' libgcc/config/i386/t-emx

%build

OPT_FLAGS=`echo %{optflags}|sed -e 's/\(-Wp,\)\?-D_FORTIFY_SOURCE=[12]//g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-m64//g;s/-m32//g;s/-m31//g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-mfpmath=sse/-mfpmath=sse -msse2/g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/ -pipe / /g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-Werror=format-security/-Wformat-security/g'`
# TODO not sure if we need this
#ifarch %{ix86}
#OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-march=i.86//g'`
#endif
OPT_FLAGS=`echo "$OPT_FLAGS" | sed -e 's/[[:blank:]]\+/ /g'`
case "$OPT_FLAGS" in
  *-fasynchronous-unwind-tables*)
    sed -i -e 's/-fno-exceptions /-fno-exceptions -fno-asynchronous-unwind-tables /' \
      libgcc/Makefile.in
    ;;
esac

rm -rf obj-%{gcc_target_platform}
mkdir obj-%{gcc_target_platform}
cd obj-%{gcc_target_platform}

enablelgo=
enablelada=
enablelobjc=
enableld=
enablegfortran=
%if %{build_objc}
enablelobjc=,objc,obj-c++
%endif
%if %{build_ada}
enablelada=,ada
%endif
%if %{build_go}
enablelgo=,go
%endif
%if %{build_d}
enableld=,d
%endif
%if %{build_gfortran}
enablegfortran=,fortran
%endif

CONFIGURE_OPTS="\
	--build=%{gcc_target_platform} \
	--with-sysroot=/@unixroot \
	--prefix=%{_prefix} --mandir=%{_mandir} --infodir=%{_infodir} \
	--with-bugurl=https://github.com/bitwiseworks/gcc-os2/issues \
	--enable-shared --enable-threads --enable-checking=release \
	--disable-multilib \
	--with-system-zlib \
	--with-gcc-major-version-only \
%if %{enable_plugin}
	--enable-plugin \
%endif
%if %{build_isl}
	--with-isl \
%else
	--without-isl \
%endif
%if %{attr_ifunc}
	--enable-gnu-indirect-function \
%endif
%if 0
	--enable-cet \
%endif
	--with-tune=generic \
	--with-arch=i686 \
	--with-gnu-as \
	--disable-libstdcxx-pch \
"

# Make sure newly built DLLs are picked up when needed.
objdir=%{_topdir}/BUILD/%{name}-%{version}/obj-%{gcc_target_platform}
export PATH="$objdir/gcc${PATH:+;$PATH}"
export BEGINLIBPATH="$objdir/gcc${BEGINLIBPATH:+;$BEGINLIBPATH}"
export LIBPATHSTRICT=T

# Note: set LDFLAGS_FOR_TARGET below to make sure target DLLs such
# as libstdc++ will get the right link flags.

CC="$CC" CXX="$CXX" CFLAGS="$OPT_FLAGS" \
	CXXFLAGS="`echo " $OPT_FLAGS " | sed 's/ -Wall / /g;s/ -fexceptions / /g' \
		  | sed 's/ -Wformat-security / -Wformat -Wformat-security /'`" \
	XCFLAGS="$OPT_FLAGS" TCFLAGS="$OPT_FLAGS" \
	LDFLAGS="-g -Zomf -Zmap -Zargs-wild -Zhigh-mem" \
	LDFLAGS_FOR_TARGET="$LDFLAGS" \
	../configure --disable-bootstrap \
	--enable-languages=c,c++${enablegfortran}${enablelobjc}${enablelada}${enablelgo}${enableld} \
	$CONFIGURE_OPTS

# Set BUILDLEVEL to be embedded to all DLLs built with Libtool.
export LT_BUILDLEVEL="@#%{vendor}:%{version}-%{release}#@##1## `LANG=C date +'%%d %%b %%Y %%H:%%M:%%S'`     `uname -n`::::0::"

# TODO we don't use bootstrap ATM: BOOT_CFLAGS="$OPT_FLAGS" profiledbootstrap
make %{?_smp_mflags}

CC="`%{gcc_target_platform}/libstdc++-v3/scripts/testsuite_flags --build-cc`"
CXX="`%{gcc_target_platform}/libstdc++-v3/scripts/testsuite_flags --build-cxx` `%{gcc_target_platform}/libstdc++-v3/scripts/testsuite_flags --build-includes`"

# Make generated man pages even if Pod::Man is not new enough
perl -p -i.bak -e 's/head3/head2/' ../contrib/texi2pod.pl
for i in ../gcc/doc/*.texi; do
  cp -a $i $i.orig; sed 's/ftable/table/' $i.orig > $i
done
make -C gcc generated-manpages
for i in ../gcc/doc/*.texi; do mv -f $i.orig $i; done

# Make generated doxygen pages.
%if %{build_libstdcxx_docs}
cd %{gcc_target_platform}/libstdc++-v3
make doc-html-doxygen
make doc-man-doxygen
cd ../..
%endif

# Copy various doc files here and there
cd ..
mkdir -p rpm.doc/gfortran rpm.doc/objc rpm.doc/gdc rpm.doc/libphobos
mkdir -p rpm.doc/go rpm.doc/libgo rpm.doc/libquadmath rpm.doc/libitm
for i in gcc/cp gcc/ada gcc/jit libstdc++-v3 libobjc libgomp libcc1 libatomic libsanitizer; do
	mkdir -p rpm.doc/changelogs/$i
done

for i in gcc gcc/cp gcc/ada gcc/jit libstdc++-v3 libobjc libgomp libcc1 libatomic libsanitizer; do
	cp -p $i/ChangeLog* rpm.doc/changelogs/$i
done

%if %{build_gfortran}
(cd gcc/fortran; for i in ChangeLog*; do
	cp -p $i ../../rpm.doc/gfortran/$i
done)
(cd libgfortran; for i in ChangeLog*; do
	cp -p $i ../rpm.doc/gfortran/$i.libgfortran
done)
%endif
%if %{build_objc}
(cd libobjc; for i in README*; do
	cp -p $i ../rpm.doc/objc/$i.libobjc
done)
%endif
%if %{build_d}
(cd gcc/d; for i in ChangeLog*; do
	cp -p $i ../../rpm.doc/gdc/$i.gdc
done)
(cd libphobos; for i in ChangeLog*; do
	cp -p $i ../rpm.doc/libphobos/$i.libphobos
done
cp -a src/LICENSE*.txt libdruntime/LICENSE ../rpm.doc/libphobos/)
%endif
%if %{build_libquadmath}
(cd libquadmath; for i in ChangeLog* COPYING.LIB; do
	cp -p $i ../rpm.doc/libquadmath/$i.libquadmath
done)
%endif
%if %{build_libitm}
(cd libitm; for i in ChangeLog*; do
	cp -p $i ../rpm.doc/libitm/$i.libitm
done)
%endif
%if %{build_go}
(cd gcc/go; for i in README* ChangeLog*; do
	cp -p $i ../../rpm.doc/go/$i
done)
(cd libgo; for i in LICENSE* PATENTS* README; do
	cp -p $i ../rpm.doc/libgo/$i.libgo
done)
%endif

rm -f rpm.doc/changelogs/gcc/ChangeLog.[1-9]
find rpm.doc -name \*ChangeLog\* | xargs bzip2 -9

%install
rm -rf %{buildroot}

cd obj-%{gcc_target_platform}

# TODO need?
## There are some MP bugs in libstdc++ Makefiles
#make -C %{gcc_target_platform}/libstdc++-v3
#
#make prefix=%{buildroot}%{_prefix} mandir=%{buildroot}%{_mandir} \
#  infodir=%{buildroot}%{_infodir} install

make DESTDIR=%{buildroot} install

%if %{build_ada}
chmod 644 %{buildroot}%{_infodir}/gnat*
%endif

FULLPATH=%{buildroot}%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
FULLEPATH=%{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}

# fix some things
ln -sf gcc.exe %{buildroot}%{_prefix}/bin/cc.exe
rm -f %{buildroot}%{_prefix}/lib/cpp.exe
ln -sf ../bin/cpp.exe %{buildroot}/%{_prefix}/lib/cpp.exe
%if %{build_gfortran}
ln -sf gfortran.exe %{buildroot}%{_prefix}/bin/f95.exe
%endif
rm -f %{buildroot}%{_infodir}/dir
gzip -9 %{buildroot}%{_infodir}/*.info*
%if %{build_ada}
ln -sf gc.exec %{buildroot}%{_prefix}/bin/gnatgcc.exe
%endif
%if %{build_gfortran}
mkdir -p %{buildroot}%{_fmoddir}
%endif

%if %{build_go}
mv %{buildroot}%{_prefix}/bin/go{,.gcc}
mv %{buildroot}%{_prefix}/bin/gofmt{,.gcc}
ln -sf /etc/alternatives/go %{buildroot}%{_prefix}/bin/go
ln -sf /etc/alternatives/gofmt %{buildroot}%{_prefix}/bin/gofmt
%endif

# TODO need?
%if 0
for f in `find %{buildroot}%{_prefix}/include/c++/%{gcc_major}/%{gcc_target_platform}/ -name c++config.h`; do
  for i in 1 2 4 8; do
    sed -i -e 's/#define _GLIBCXX_ATOMIC_BUILTINS_'$i' 1/#ifdef __GCC_HAVE_SYNC_COMPARE_AND_SWAP_'$i'\
&\
#endif/' $f
  done
done
%endif

# Nuke bits/*.h.gch dirs
# 1) there is no bits/*.h header installed, so when gch file can't be
#    used, compilation fails
# 2) sometimes it is hard to match the exact options used for building
#    libstdc++-v3 or they aren't desirable
# 3) there are multilib issues, conflicts etc. with this
# 4) it is huge
# People can always precompile on their own whatever they want, but
# shipping this for everybody is unnecessary.
rm -rf %{buildroot}%{_prefix}/include/c++/%{gcc_major}/%{gcc_target_platform}/bits/*.h.gch

%if %{build_libstdcxx_docs}
libstdcxx_doc_builddir=%{gcc_target_platform}/libstdc++-v3/doc/doxygen
mkdir -p ../rpm.doc/libstdc++-v3
cp -r -p ../libstdc++-v3/doc/html ../rpm.doc/libstdc++-v3/html
cp -r -p $libstdcxx_doc_builddir/html ../rpm.doc/libstdc++-v3/html/api
mkdir -p %{buildroot}%{_mandir}/man3
cp -r -p $libstdcxx_doc_builddir/man/man3/* %{buildroot}%{_mandir}/man3/
find ../rpm.doc/libstdc++-v3 -name \*~ | xargs rm
%endif

FULLLSUBDIR=
FULLLPATH=$FULLPATH

find %{buildroot} -name \*.la | xargs rm -f

%if %{build_gfortran}
mv %{buildroot}%{_prefix}/%{_lib}/libgfortran.spec $FULLPATH/
%endif
%if %{build_d}
mv %{buildroot}%{_prefix}/%{_lib}/libgphobos.spec $FULLPATH/
%endif
%if %{build_libitm}
mv %{buildroot}%{_prefix}/%{_lib}/libitm.spec $FULLPATH/
%endif
%if %{build_libasan}
mv %{buildroot}%{_prefix}/%{_lib}/libsanitizer.spec $FULLPATH/
%endif

%if %{build_libgomp}
mv -f %{buildroot}%{_prefix}/%{_lib}/libgomp.spec $FULLPATH/
%endif

%if %{build_ada}
mv -f $FULLPATH/adalib/libgnarl-*.so %{buildroot}%{_prefix}/%{_lib}/
mv -f $FULLPATH/adalib/libgnat-*.so %{buildroot}%{_prefix}/%{_lib}/
rm -f $FULLPATH/adalib/libgnarl.so* $FULLPATH/adalib/libgnat.so*
%endif

%if %{enable_gdb}
mkdir -p %{buildroot}%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}
mv -f %{buildroot}%{_prefix}/%{_lib}/libstdc++*gdb.py* \
      %{buildroot}%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/
pushd ../libstdc++-v3/python
for i in `find . -name \*.py`; do
  touch -r $i %{buildroot}%{_prefix}/share/gcc-%{gcc_major}/python/$i
done
touch -r hook.in %{buildroot}%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/libstdc++*gdb.py
popd
for f in `find %{buildroot}%{_prefix}/share/gcc-%{gcc_major}/python/ \
	       %{buildroot}%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/ -name \*.py`; do
  r=${f/$RPM_BUILD_ROOT/}
  %{__python3} -c 'import py_compile; py_compile.compile("'$f'", dfile="'$r'")'
  %{__python3} -O -c 'import py_compile; py_compile.compile("'$f'", dfile="'$r'")'
done
%else
rm -f %{buildroot}%{_prefix}/%{_lib}/*gdb.py
%endif

%if %{build_libgccjit}
rm -f $FULLEPATH/libgccjit.so
cp -a objlibgccjit/gcc/libgccjit.so* %{buildroot}%{_prefix}/%{_lib}/
cp -a ../gcc/jit/libgccjit*.h %{buildroot}%{_prefix}/include/
/usr/bin/install -c -m 644 objlibgccjit/gcc/doc/libgccjit.info %{buildroot}/%{_infodir}/
gzip -9 %{buildroot}/%{_infodir}/libgccjit.info
%endif

# If we are building a debug package then copy all of the static archives
# into the debug directory to keep them as unstripped copies.
%if 0%{?_enable_debug_packages}
for d in . $FULLLSUBDIR; do
  mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/debug%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/$d
  for f in `find $d -maxdepth 1 -a \
		\( -name libasan.a -o -name libatomic.a \
		-o -name libcaf_single.a \
		-o -name libgcc.a -o -name libgcc_eh.a \
		-o -name libgcov.a -o -name libgfortran.a \
		-o -name libgo.a -o -name libgobegin.a \
		-o -name libgolibbegin.a -o -name libgomp.a \
		-o -name libitm.a -o -name liblsan.a \
		-o -name libobjc.a -o -name libgdruntime.a -o -name libgphobos.a \
		-o -name libquadmath.a -o -name libstdc++.a \
		-o -name libstdc++fs.a -o -name libsupc++.a \
		-o -name libtsan.a -o -name libubsan.a \) -a -type f`; do
    cp -a $f $RPM_BUILD_ROOT%{_prefix}/lib/debug%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/$d/
  done
done
%endif

# TODO remove? We provide a complete include-fixed dir on OS/2
%if 0
mv $FULLPATH/include-fixed/syslimits.h $FULLPATH/include/syslimits.h
mv $FULLPATH/include-fixed/limits.h $FULLPATH/include/limits.h
for h in `find $FULLPATH/include -name \*.h`; do
  if grep -q 'It has been auto-edited by fixincludes from' $h; then
    rh=`grep -A2 'It has been auto-edited by fixincludes from' $h | tail -1 | sed 's|^.*"\(.*\)".*$|\1|'`
    diff -up $rh $h || :
    rm -f $h
  fi
done
%endif

# Remove fixed includes belonging to other RPMs
# TODO better fix fixincludes makefiles
rm -rf $FULLPATH/include-fixed/os2tk45

cat > %{buildroot}%{_prefix}/bin/c89 <<"EOF"
#!/bin/sh
fl="-std=c89"
for opt; do
  case "$opt" in
    -ansi|-std=c89|-std=iso9899:1990) fl="";;
    -std=*) echo "`basename $0` called with non ANSI/ISO C option $opt" >&2
	    exit 1;;
  esac
done
exec gcc $fl ${1+"$@"}
EOF
cat > %{buildroot}%{_prefix}/bin/c99 <<"EOF"
#!/bin/sh
fl="-std=c99"
for opt; do
  case "$opt" in
    -std=c99|-std=iso9899:1999) fl="";;
    -std=*) echo "`basename $0` called with non ISO C99 option $opt" >&2
	    exit 1;;
  esac
done
exec gcc $fl ${1+"$@"}
EOF
chmod 755 %{buildroot}%{_prefix}/bin/c?9

cd ..
%find_lang %{name}
%find_lang cpplib

# Remove binaries we will not be including, so that they don't end up in
# gcc-debuginfo
rm -f %{buildroot}%{_prefix}/%{_lib}/libffi* || :
rm -f %{buildroot}%{_prefix}/%{_lib}/libiberty.a || :
rm -f $FULLEPATH/install-tools/mkheaders
rm -f $FULLEPATH/install-tools/fixincl.exe
# We provide SSP on OS/2
#rm -f %{buildroot}%{_prefix}/%{_lib}/ssp*
rm -f %{buildroot}%{_prefix}/%{_lib}/vtv* || :
rm -f %{buildroot}%{_prefix}/bin/%{gcc_target_platform}-gfortran.exe || :
rm -f %{buildroot}%{_prefix}/bin/%{gcc_target_platform}-gccgo.exe || :
rm -f %{buildroot}%{_prefix}/bin/%{gcc_target_platform}-gcj.exe  | :
rm -f %{buildroot}%{_prefix}/bin/%{gcc_target_platform}-gcc-ar.exe || :
rm -f %{buildroot}%{_prefix}/bin/%{gcc_target_platform}-gcc-nm.exe || :
rm -f %{buildroot}%{_prefix}/bin/%{gcc_target_platform}-gcc-ranlib.exe || :
rm -f %{buildroot}%{_prefix}/bin/%{gcc_target_platform}-gdc.exe || :

rm -f %{buildroot}%{mandir}/man3/ffi* || :

# Remove the rest of install-tools as we don't include them either.
rm -rf $FULLEPATH/install-tools
rm -rf $FULLPATH/install-tools

# Help plugins find out nvra.
echo gcc-%{version}-%{release}.%{_arch} > $FULLPATH/rpmver

# Build gccXXX forwarders
for bld in 335 432 433 434 435 440 441 442 444 445 446 452 453 454 464 473 474 482 483 490 491 492; do
  sed -i 's/Forwarder/Forwarder %{version}-%{release}/' gcc${bld}.def
  gcc -s -Zomf -Zmap -Zdll -nostdlib -o gcc${bld}.dll gcc${bld}.def fwdstub.s obj-%{gcc_target_platform}/gcc/libgcc_so_d.a -llibc
  cp -a gcc${bld}.dll %{buildroot}%{_libdir}
done

# Build ssp forwarder for GCC 4.x
sed -i 's/Forwarder/Forwarder %{version}-%{release}/' ssp.def
gcc -s -Zomf -Zmap -Zdll -nostdlib -lend -o ssp.dll ssp.def  obj-%{gcc_target_platform}/%{gcc_target_platform}/libssp/.libs/ssp0_dll.a
cp -a ssp.dll %{buildroot}%{_libdir}

# Build stdcpp forwarder for GCC 4.4.x
sed -i 's/Forwarder/Forwarder %{version}-%{release}/' stdcpp.def
gcc -s -Zomf -Zmap -Zdll -nostdlib -lend -o stdcpp.dll stdcpp.def  obj-%{gcc_target_platform}/%{gcc_target_platform}/libstdc++-v3/src/.libs/stdc++_dll.a -l%{_libdir}/libc066.dll
cp -a stdcpp.dll %{buildroot}%{_libdir}

# Provide .lib versions of static libraries to speed up compilation times.
for f in `find %{buildroot} -name \*.a`; do
  f_lib=${f%.a}.lib
  [ -f $f_lib ] || emxomf $f -o $f_lib
done

echo dummy for virtual package > gcc-wrc.txt
echo dummy for virtual package > gcc-wlink.txt

# TODO deal with tests later
%if 0
%check
cd obj-%{gcc_target_platform}

# run the tests.
LC_ALL=C make %{?_smp_mflags} -k check ALT_CC_UNDER_TEST=gcc ALT_CXX_UNDER_TEST=g++ \
%if 0%{?fedora} >= 20 || 0%{?rhel} > 7
     RUNTESTFLAGS="--target_board=unix/'{,-fstack-protector-strong}'" || :
%else
     RUNTESTFLAGS="--target_board=unix/'{,-fstack-protector}'" || :
%endif
echo ====================TESTING=========================
( LC_ALL=C ../contrib/test_summary || : ) 2>&1 | sed -n '/^cat.*EOF/,/^EOF/{/^cat.*EOF/d;/^EOF/d;/^LAST_UPDATED:/d;p;}'
echo ====================TESTING END=====================
mkdir testlogs-%{_target_platform}-%{version}-%{release}
for i in `find . -name \*.log | grep -F testsuite/ | grep -v 'config.log\|acats.*/tests/'`; do
  ln $i testlogs-%{_target_platform}-%{version}-%{release}/ || :
done
tar cf - testlogs-%{_target_platform}-%{version}-%{release} | xz -9e \
  | uuencode testlogs-%{_target_platform}.tar.xz || :
rm -rf testlogs-%{_target_platform}-%{version}-%{release}
%endif

%if %{build_go}
%post go
%{_sbindir}/update-alternatives --install \
  %{_prefix}/bin/go go %{_prefix}/bin/go.gcc 92 \
  --slave %{_prefix}/bin/gofmt gofmt %{_prefix}/bin/gofmt.gcc

%preun go
if [ $1 = 0 ]; then
  %{_sbindir}/update-alternatives --remove go %{_prefix}/bin/go.gcc
fi
%endif

%post wrc -e
if [ "$1" = 1 ] ; then
#execute only on first install
%cube {DELLINE "SET EMXOMFLD_RC="} %%{os2_config_sys}  > NUL
%cube {DELLINE "SET EMXOMFLD_RC_TYPE="} %%{os2_config_sys}> NUL
%cube {ADDLINE "SET EMXOMFLD_RC=wrc.exe"} %%{os2_config_sys} > NUL
%cube {ADDLINE "SET EMXOMFLD_RC_TYPE=WRC"} %%{os2_config_sys} > NUL
fi

%postun wrc -e
if [ "$1" = 0 ] ; then
# execute only on last uninstall
%cube {DELLINE "SET EMXOMFLD_RC="} %%{os2_config_sys} > NUL
%cube {DELLINE "SET EMXOMFLD_RC_TYPE="} %%{os2_config_sys} > NUL
fi

%post wlink -e
if [ "$1" = 1 ] ; then
# execute only on first install
%cube {DELLINE "SET EMXOMFLD_LINKER="} %%{os2_config_sys} > NUL
%cube {DELLINE "SET EMXOMFLD_TYPE="} %%{os2_config_sys} > NUL
%cube {ADDLINE "SET EMXOMFLD_LINKER=wl.exe"} %%{os2_config_sys} > NUL
%cube {ADDLINE "SET EMXOMFLD_TYPE=WLINK"} %%{os2_config_sys} > NUL
fi

%postun wlink -e
if [ "$1" = 0 ] ; then
# execute only on last uninstall
%cube {DELLINE "SET EMXOMFLD_LINKER="} %%{os2_config_sys} > NUL
%cube {DELLINE "SET EMXOMFLD_TYPE="} %%{os2_config_sys} > NUL
fi

%files -f %{name}.lang
%{_prefix}/bin/cc.exe
%{_prefix}/bin/c89
%{_prefix}/bin/c99
%{_prefix}/bin/gcc.exe
%{_prefix}/bin/gcov.exe
%{_prefix}/bin/gcov-tool.exe
%{_prefix}/bin/gcov-dump.exe
%{_prefix}/bin/gcc-ar.exe
%{_prefix}/bin/gcc-nm.exe
%{_prefix}/bin/gcc-ranlib.exe
%{_prefix}/bin/%{gcc_target_platform}-gcc.exe
%{_prefix}/bin/%{gcc_target_platform}-gcc-%{gcc_major}.exe
%{_mandir}/man1/gcc.1*
%{_mandir}/man1/gcov.1*
%{_mandir}/man1/gcov-tool.1*
%{_mandir}/man1/gcov-dump.1*
%{_mandir}/man7/fsf-funding.7*
%{_mandir}/man7/gfdl.7*
%{_mandir}/man7/gpl.7*
%{_infodir}/gcc*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/lto1.exe
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/lto-wrapper.exe
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/lto_plu*.dll
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/lto_plu*.a
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/lto_plu*.lib
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/rpmver
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stdarg.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stdfix.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/varargs.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stdbool.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/iso646.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/unwind.h
%if %{build_libgomp}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/omp.h
%endif
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stdalign.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stdnoreturn.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stdatomic.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/gcov.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/mmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/xmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/emmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/pmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/tmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/ammintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/smmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/nmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/bmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/wmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/immintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avxintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/x86intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/fma4intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/xopintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/lwpintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/popcntintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/bmiintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/tbmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/ia32intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx2intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/bmi2intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/f16cintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/fmaintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/lzcntintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/rtmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/xtestintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/adxintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/prfchwintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/rdseedintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/fxsrintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/xsaveintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/xsaveoptintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512cdintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512erintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512fintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512pfintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/shaintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/mm_malloc.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/mm3dnow.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/cpuid.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/cross-stdarg.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512bwintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512dqintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512ifmaintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512ifmavlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vbmiintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vbmivlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vlbwintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vldqintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/clflushoptintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/clwbintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/mwaitxintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/xsavecintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/xsavesintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/clzerointrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/pkuintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx5124fmapsintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx5124vnniwintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vpopcntdqintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/sgxintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/gfniintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/cetintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/cet.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vbmi2intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vbmi2vlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vnniintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vnnivlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/vaesintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/vpclmulqdqintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vpopcntdqvlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512bitalgintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/pconfigintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/wbnoinvdintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/movdirintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/waitpkgintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/cldemoteintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/tgmath.h
%if %{build_libasan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/sanitizer
%endif
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include-fixed
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include-fixed/limits.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include-fixed/README
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include-fixed/stddef.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include-fixed/stdio.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include-fixed/stdlib.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include-fixed/syslimits.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include-fixed/unistd.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include-fixed/wchar.h
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include-fixed/386
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include-fixed/386/ansi.h
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include-fixed/sys
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include-fixed/sys/types.h
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/collect2.exe
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/emx*.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgcc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgcc.lib
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgcov.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgcov.lib
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgcc_eh.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgcc_eh.lib
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgcc_so_d.*
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/gcc1.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/gcc1.lib
%if %{build_libgomp}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgomp.spec
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgomp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgomp.so
%endif
%if %{build_libitm}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libitm.spec
%endif
%if %{build_libasan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libsanitizer.spec
%endif
%if %{build_libtsan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libtsan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libtsan_preinit.o
%endif
%if %{build_liblsan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/liblsan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/liblsan_preinit.o
%endif
%doc gcc/README* rpm.doc/changelogs/gcc/ChangeLog* 
%doc README.md ChangeLog.md
%{!?_licensedir:%global license %%doc}
%license gcc/COPYING* COPYING.RUNTIME

%files -n cpp -f cpplib.lang
%{_prefix}/lib/cpp.exe
%{_prefix}/bin/cpp.exe
%{_mandir}/man1/cpp.1*
%{_infodir}/cpp*
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/cc1.exe

%files -n libgcc
%{_prefix}/%{_lib}/gcc1.dll
%{!?_licensedir:%global license %%doc}
%license gcc/COPYING* COPYING.RUNTIME

%files -n libgcc-fwd
%{_prefix}/%{_lib}/gcc???.dll

%files -n libssp
%{_prefix}/%{_lib}/ssp0.dll
%{!?_licensedir:%global license %%doc}
%license gcc/COPYING* COPYING.RUNTIME

%files -n libssp-fwd
%{_prefix}/%{_lib}/ssp.dll

%files -n libssp-devel
%{_prefix}/%{_lib}/ssp*_dll.a
%{_prefix}/%{_lib}/ssp*_dll.lib
%{_prefix}/%{_lib}/ssp.a
%{_prefix}/%{_lib}/ssp.lib
%{_prefix}/%{_lib}/ssp_nonshared.a
%{_prefix}/%{_lib}/ssp_nonshared.lib
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/ssp

%files c++
%{_prefix}/bin/%{gcc_target_platform}-*++.exe
%{_prefix}/bin/g++.exe
%{_prefix}/bin/c++.exe
%{_mandir}/man1/g++.1*
%{_prefix}/lib/supc++.a
%{_prefix}/lib/supc++.lib
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/cc1plus.exe
%doc rpm.doc/changelogs/gcc/cp/ChangeLog*

%files -n libstdc++
%{_prefix}/%{_lib}/stdcpp6.dll
%if %{enable_gdb}
%dir %{_datadir}/gdb
%dir %{_datadir}/gdb/auto-load
%dir %{_datadir}/gdb/auto-load/%{_prefix}
%dir %{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/
%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/libstdc*gdb.py*
%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/__pycache__
%endif
%dir %{_prefix}/share/gcc-%{gcc_major}
%dir %{_prefix}/share/gcc-%{gcc_major}/python
%{_prefix}/share/gcc-%{gcc_major}/python/libstdcxx

%files -n libstdc++-fwd
%{_prefix}/%{_lib}/stdcpp.dll

%files -n libstdc++-devel
%dir %{_prefix}/include/c++
%{_prefix}/include/c++/%{gcc_major}
%{_prefix}/lib/stdc++*_dll.a
%{_prefix}/lib/stdc++*_dll.lib
%doc rpm.doc/changelogs/libstdc++-v3/ChangeLog* libstdc++-v3/README*

%files -n libstdc++-static
%{_prefix}/lib/stdc++.a
%{_prefix}/lib/stdc++.lib

%if %{build_libstdcxx_docs}
%files -n libstdc++-docs
%{_mandir}/man3/*
%doc rpm.doc/libstdc++-v3/html
%endif

%if %{build_objc}
%files objc
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/objc
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/cc1obj
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libobjc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libobjc.so
%doc rpm.doc/objc/*
%doc libobjc/THREADS* rpm.doc/changelogs/libobjc/ChangeLog*

%files objc++
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/cc1objplus

%files -n libobjc
%{_prefix}/%{_lib}/libobjc.so.4*
%endif

%if %{build_gfortran}
%files gfortran
%{_prefix}/bin/gfortran
%{_prefix}/bin/f95
%{_mandir}/man1/gfortran.1*
%{_infodir}/gfortran*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/ISO_Fortran_binding.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/omp_lib.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/omp_lib.f90
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/omp_lib.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/omp_lib_kinds.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/openacc.f90
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/openacc.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/openacc_kinds.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/openacc_lib.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/ieee_arithmetic.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/ieee_exceptions.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/ieee_features.mod
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/f951
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgfortran.spec
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libcaf_single.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgfortran.so
%dir %{_fmoddir}
%doc rpm.doc/gfortran/*

%files -n libgfortran
%{_prefix}/%{_lib}/libgfortran.so.5*

%files -n libgfortran-static
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgfortran.a
%endif

%if %{build_d}
%files gdc
%{_prefix}/bin/gdc
%{_mandir}/man1/gdc.1*
%{_infodir}/gdc*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/d
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/d21
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgphobos.spec
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgdruntime.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgphobos.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgdruntime.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgphobos.so
%doc rpm.doc/gdc/*

%files -n libgphobos
%{_prefix}/%{_lib}/libgdruntime.so.76*
%{_prefix}/%{_lib}/libgphobos.so.76*
%doc rpm.doc/libphobos/*

%files -n libgphobos-static
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgdruntime.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgphobos.a
%endif

%if %{build_ada}
%files gnat
%{_prefix}/bin/gnat
%{_prefix}/bin/gnat[^i]*
%{_infodir}/gnat*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/adalib
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/gnat1
%doc rpm.doc/changelogs/gcc/ada/ChangeLog*

%files -n libgnat
%{_prefix}/%{_lib}/libgnat-*.so
%{_prefix}/%{_lib}/libgnarl-*.so

%files -n libgnat-devel
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/adalib
%exclude %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/adalib/libgnat.a
%exclude %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/adalib/libgnarl.a

%files -n libgnat-static
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/adalib
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/adalib/libgnat.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/adalib/libgnarl.a
%endif

%if %{build_libgomp}
%files -n libgomp
%{_prefix}/%{_lib}/libgomp.so.1*
%{_infodir}/libgomp.info*
%doc rpm.doc/changelogs/libgomp/ChangeLog*
%endif

%if %{build_libquadmath}
%files -n libquadmath
%{_prefix}/%{_lib}/quadmat0.dll
%{_infodir}/libquadmath.info*
%{!?_licensedir:%global license %%doc}
%license rpm.doc/libquadmath/COPYING*

%files -n libquadmath-devel
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/quadmath.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/quadmath_weak.h
%{_prefix}/lib/quadmath*_dll.a
%{_prefix}/lib/quadmath*_dll.lib
%doc rpm.doc/libquadmath/ChangeLog*

%files -n libquadmath-static
%{_prefix}/lib/quadmath.a
%{_prefix}/lib/quadmath.lib
%endif

%if %{build_libitm}
%files -n libitm
%{_prefix}/%{_lib}/libitm.so.1*
%{_infodir}/libitm.info*

%files -n libitm-devel
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include
#%%{_prefix}/lib/gcc/%%{gcc_target_platform}/%%{gcc_major}/include/itm.h
#%%{_prefix}/lib/gcc/%%{gcc_target_platform}/%%{gcc_major}/include/itm_weak.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libitm.so
%doc rpm.doc/libitm/ChangeLog*

%files -n libitm-static
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libitm.a
%endif

%if %{build_libatomic}
%files -n libatomic
%{_prefix}/%{_lib}/libatomic.so.1*

%files -n libatomic-static
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libatomic.a
%doc rpm.doc/changelogs/libatomic/ChangeLog*
%endif

%if %{build_libasan}
%files -n libasan
%{_prefix}/%{_lib}/libasan.so.5*

%files -n libasan-static
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libasan.a
%doc rpm.doc/changelogs/libsanitizer/ChangeLog*
%{!?_licensedir:%global license %%doc}
%license libsanitizer/LICENSE.TXT
%endif

%if %{build_libubsan}
%files -n libubsan
%{_prefix}/%{_lib}/libubsan.so.1*

%files -n libubsan-static
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libubsan.a
%doc rpm.doc/changelogs/libsanitizer/ChangeLog*
%{!?_licensedir:%global license %%doc}
%license libsanitizer/LICENSE.TXT
%endif

%if %{build_libtsan}
%files -n libtsan
%{_prefix}/%{_lib}/libtsan.so.0*

%files -n libtsan-static
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libtsan.a
%doc rpm.doc/changelogs/libsanitizer/ChangeLog*
%{!?_licensedir:%global license %%doc}
%license libsanitizer/LICENSE.TXT
%endif

%if %{build_liblsan}
%files -n liblsan
%{_prefix}/%{_lib}/liblsan.so.0*

%files -n liblsan-static
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/liblsan.a
%doc rpm.doc/changelogs/libsanitizer/ChangeLog*
%{!?_licensedir:%global license %%doc}
%license libsanitizer/LICENSE.TXT
%endif

%if %{build_go}
%files go
%ghost %{_prefix}/bin/go
%attr(755,root,root) %{_prefix}/bin/go.gcc
%{_prefix}/bin/gccgo
%ghost %{_prefix}/bin/gofmt
%attr(755,root,root) %{_prefix}/bin/gofmt.gcc
%{_mandir}/man1/gccgo.1*
%{_mandir}/man1/go.1*
%{_mandir}/man1/gofmt.1*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/go1
%attr(755,root,root) %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/cgo
%attr(755,root,root) %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/buildid
%attr(755,root,root) %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/test2json
%attr(755,root,root) %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/vet
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgo.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgo.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgobegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgolibbegin.a
%doc rpm.doc/go/*

%files -n libgo
%attr(755,root,root) %{_prefix}/%{_lib}/libgo.so.14*
%doc rpm.doc/libgo/*

%files -n libgo-devel
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/%{_lib}/go
%dir %{_prefix}/%{_lib}/go/%{gcc_major}
%{_prefix}/%{_lib}/go/%{gcc_major}/%{gcc_target_platform}
%dir %{_prefix}/lib/go
%dir %{_prefix}/lib/go/%{gcc_major}
%{_prefix}/lib/go/%{gcc_major}/%{gcc_target_platform}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgobegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgolibbegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgo.so

%files -n libgo-static
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgo.a
%endif

%if %{build_libgccjit}
%files -n libgccjit
%{_prefix}/%{_lib}/libgccjit.so.*
%doc rpm.doc/changelogs/gcc/jit/ChangeLog*

%files -n libgccjit-devel
%{_prefix}/%{_lib}/libgccjit.so
%{_prefix}/include/libgccjit*.h
%{_infodir}/libgccjit.info*
%doc rpm.doc/libgccjit-devel/*
%doc gcc/jit/docs/examples
%endif

%if %{enable_plugin}
%files plugin-devel
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin/gtype.state
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin/include
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/plugin

%if %{enable_gdb}
%files gdb-plugin
%{_prefix}/%{_lib}/libcc1.so*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin/libcc1plugin.so*
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin/libcp1plugin.so*
%doc rpm.doc/changelogs/libcc1/ChangeLog*
%endif
%endif

%files wlink
%doc gcc-wlink.txt

%files wrc
%doc gcc-wrc.txt

%changelog
* Sat May 9 2020 Dmitriy Kuminov <coding@dmik.org> - 9.2.0-4
- Require gettext-devel when building to avoid GCC own intl usage [gcc-os2#24].
- Fix forwarders for GCC runtime 4.4.0-4.4.2, 4.4.4 and 4.4.5 [gcc-os2#25].

* Fri Mar 27 2020 Dmitriy Kuminov <coding@dmik.org> - 9.2.0-3
- Release version 9.2.0 OS/2 Beta 2.
  (https://github.com/bitwiseworks/gcc-os2/blob/gcc-9_2_0-release-os2-b2/ChangeLog.md).
- Provide libgcc1 and libstdc++6 as aliasses for libgcc and libstdc++6 as some
  .spec may use Require them directly.
- Change mpc-devel dependency to libmpc-devel (remaned according to Fedora).

* Wed Jan 15 2020 Dmitriy Kuminov <coding@dmik.org> - 9.2.0-2
- Use os2_config_sys macro (with -e and %%) instead of hard-coded c:\config.sys.
- Fix gcc1.dll BLDLEVEL string.

* Tue Jan 14 2020 Dmitriy Kuminov <coding@dmik.org> - 9.2.0-1
- Initial RPM release of GCC 9
  (https://github.com/bitwiseworks/gcc-os2/blob/gcc-9_2_0-release-os2-b1/ChangeLog.md).
