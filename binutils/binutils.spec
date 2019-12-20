
Summary: A GNU collection of binary utilities
Name: %{?cross}binutils%{?_with_debug:-debug}
Version: 2.33.1
Release: 1%{?dist}
License: GPLv3+
URL: https://sourceware.org/binutils

#----------------------------------------------------------------------------

# Binutils SPEC file.  Can be invoked with the following parameters:

# --define "binutils_target arm-linux-gnu" to create arm-linux-gnu-binutils.
# --with=bootstrap      Build with minimal dependencies.
# --with=debug          Build without optimizations and without splitting
#                        the debuginfo into a separate file.
# --without=docs        Skip building documentation.
# --without=testsuite   Do not run the testsuite.  Default is to run it.
# --with=testsuite      Run the testsuite.  Default when --with=debug is not
#                        to run it.
# --without=gold        Disable building of the GOLD linker.

#---Start of Configure Options-----------------------------------------------

# Use clang as the build time compiler rather than gcc.
%define build_using_clang 0

# Create deterministic archives (ie ones without timestamps).
# Default is off because of BZ 1195883.
%define enable_deterministic_archives 0

# Enable support for GCC LTO compilation.
# Disable if it is necessary to work around bugs in LTO.
%define enable_lto 0

# Enable the compression of debug sections as default behaviour of the
# assembler and linker.  This option is disabled for now.  The assembler and
# linker have command line options to override the default behaviour.
%define default_compress_debug 0

# Default to read-only-relocations (relro) in shared binaries.
# This is enabled as a security feature.
%define default_relro 1

# Enable the default generation of GNU Build notes by the assembler.
# This option is disabled as it has turned out to be problematic for the i686
# architecture, although the exact reason has not been determined.  (See
# BZ 1572485).  It also breaks building EFI binaries on AArch64, as these
# cannot have relocations against absolute symbols.
%define default_generate_notes 0

# Enable thread support in the GOLD linker (if it is being built).  This is
# particularly important if plugins to the linker intend to use threads
# themselves.  See BZ 1636479 for more details.  This option is made
# configurable in case there is ever a need to disable thread support.
%define enable_threading 1

#----End of Configure Options------------------------------------------------

# Note - in the future the gold linker may become deprecated.
%ifnarch riscv64
# no gold for us
%bcond_with gold
%else
# RISC-V does not have ld.gold thus disable by default.
%bcond_with gold
%endif

# Default: Not bootstrapping.
%bcond_with bootstrap
# Default: Not debug
%bcond_with debug
# Default: Always build documentation.
%bcond_without docs
# Default: Never run the testsuite.
%bcond_with testsuite

%if %{with bootstrap}
%undefine with_docs
%undefine with_testsuite
%endif

%if %{with debug}
%undefine with_testsuite
%endif

%if 0%{!?binutils_target:1}
# we always use _build, as target_platform isn't recognised by configure
# define binutils_target %{_target_platform}
%define binutils_target %{_build}
%define isnative 1
%define enable_shared 1
%else
%define cross %{binutils_target}-
%define isnative 0
%define enable_shared 0
%endif

# The opcodes library needs a few functions defined in the bfd
# library, but these symbols are not defined in the stub bfd .so
# that is available at link time.  (They are present in the real
# .so that is used at run time).
%undefine _strict_symbol_defs_build

#----------------------------------------------------------------------------

%global with_alternatives 0

Vendor: bww bitwise works GmbH
%scm_source github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2

Provides: bundled(libiberty)

%if %{with gold}
# For now we make the binutils package require the gold sub-package.
# That way other packages that have a requirement on "binutils" but
# actually want gold will not have to be changed.  In the future, if
# we decide to deprecate gold, we can remove this requirement, and
# then update other packages as necessary.
Requires: binutils-gold >= %{version}
%endif

%if %{with debug}
# Define this if you want to skip the strip step and preserve debug info.
# Useful for testing.
%define __debug_install_post : > %{_builddir}/%{?buildsubdir}/debugfiles.list
%define debug_package %{nil}
%endif

# Perl, sed and touch are all used in the %%prep section of this spec file.
BuildRequires: perl, sed, coreutils

%if %{build_using_clang}
BuildRequires: clang
%else
BuildRequires: gcc
%endif

%if %{without bootstrap}
BuildRequires: gettext, flex, zlib-devel
%endif

%if %{with docs}
BuildRequires: texinfo >= 4.0
# BZ 920545: We need pod2man in order to build the manual pages.
BuildRequires: /@unixroot/usr/bin/pod2man
%else
BuildRequires: findutils
%endif

# Required for: ld-bootstrap/bootstrap.exp bootstrap with --static
# It should not be required for: ld-elf/elf.exp static {preinit,init,fini} array
%if %{with testsuite}
# relro_test.sh uses dc which is part of the bc rpm, hence its inclusion here.
BuildRequires: dejagnu, zlib-static, glibc-static, sharutils, bc
%endif

%if %{with_alternatives}
Requires(post): %{_sbindir}/alternatives
Requires(preun): %{_sbindir}/alternatives
%endif
# We also need rm.
Requires(post): coreutils

# On ARM EABI systems, we do want -gnueabi to be part of the
# target triple.
%ifnarch %{arm}
%define _gnu %{nil}
%endif

#----------------------------------------------------------------------------

%description
Binutils is a collection of binary utilities, including ar (for
creating, modifying and extracting from archives), as (a family of GNU
assemblers), gprof (for displaying call graph profile data), ld (the
GNU linker), nm (for listing symbols from object files), objcopy (for
copying and translating object files), objdump (for displaying
information from object files), ranlib (for generating an index for
the contents of an archive), readelf (for displaying detailed
information about binary files), size (for listing the section sizes
of an object or archive file), strings (for listing printable strings
from files), strip (for discarding symbols), and addr2line (for
converting addresses to file and line).

#----------------------------------------------------------------------------

%package devel
Summary: BFD and opcodes static and dynamic libraries and header files
Provides: binutils-static = %{version}-%{release}
Requires: zlib-devel
Requires: binutils = %{version}-%{release}
# BZ 1215242: We need touch...
Requires: coreutils

# To avoid header clashes (demangle.h etc)
Requires: libc-devel >= 0.6.6-40

%description devel
This package contains BFD and opcodes static and dynamic libraries.

The dynamic libraries are in this package, rather than a separate
base package because they are actually linker scripts that force
the use of the static libraries.  This is because the API of the
BFD library is too unstable to be used dynamically.

The static libraries are here because they are now needed by the
dynamic libraries.

Developers starting new projects are strongly encouraged to consider
using libelf instead of BFD.

#----------------------------------------------------------------------------

%if %{with gold}

%package gold
Summary: The GOLD linker, a faster alternative to the BFD linker
Provides: gold = %{version}-%{release}
Requires: binutils >= %{version}

%description gold
This package provides the GOLD linker, which can be used as an alternative to
the default binutils linker (ld.bfd).  The GOLD is generally faster than the
BFD linker, and it supports features such as Identical Code Folding and
Incremental linking.  Unfortunately it is not as well maintained as the BFD
linker, and it may become deprecated in the future.

# Gold needs bison in order to build gold/yyscript.c.
BuildRequires: bison, m4, gcc-c++
# The GOLD testsuite needs a static libc++
BuildRequires: libstdc++-static

%if ! %{build_using_clang}
BuildRequires: gcc-c++
Conflicts: gcc-c++ < 4.0.0
%endif

# The higher of these two numbers determines the default ld.
%{!?ld_gold_priority:%global ld_gold_priority   30}

%endif %%# with gold

%{!?ld_bfd_priority: %global ld_bfd_priority    50}

#----------------------------------------------------------------------------

%debug_package

%prep
%scm_setup

autogen.sh

%if 0
# We cannot run autotools as there is an exact requirement of autoconf-2.59.
# FIXME - this is no longer true.  Maybe try reinstating autotool use ?

# On ppc64 and aarch64, we might use 64KiB pages
sed -i -e '/#define.*ELF_COMMONPAGESIZE/s/0x1000$/0x10000/' bfd/elf*ppc.c
sed -i -e '/#define.*ELF_COMMONPAGESIZE/s/0x1000$/0x10000/' bfd/elf*aarch64.c
sed -i -e '/common_pagesize/s/4 /64 /' gold/powerpc.cc
sed -i -e '/pagesize/s/0x1000,/0x10000,/' gold/aarch64.cc
# LTP sucks
perl -pi -e 's/i\[3-7\]86/i[34567]86/g' */conf*
sed -i -e 's/%''{release}/%{release}/g' bfd/Makefile{.am,.in}
sed -i -e '/^libopcodes_la_\(DEPENDENCIES\|LIBADD\)/s,$, ../bfd/libbfd.la,' opcodes/Makefile.{am,in}
# Build libbfd.so and libopcodes.so with -Bsymbolic-functions if possible.
if gcc %{optflags} -v --help 2>&1 | grep -q -- -Bsymbolic-functions; then
sed -i -e 's/^libbfd_la_LDFLAGS = /&-Wl,-Bsymbolic-functions /' bfd/Makefile.{am,in}
sed -i -e 's/^libopcodes_la_LDFLAGS = /&-Wl,-Bsymbolic-functions /' opcodes/Makefile.{am,in}
fi
# $PACKAGE is used for the gettext catalog name.
sed -i -e 's/^ PACKAGE=/ PACKAGE=%{?cross}/' */configure
# Undo the name change to run the testsuite.
for tool in binutils gas ld
do
  sed -i -e "2aDEJATOOL = $tool" $tool/Makefile.am
  sed -i -e "s/^DEJATOOL = .*/DEJATOOL = $tool/" $tool/Makefile.in
done
touch */configure
%endif

# Touch the .info files so that they are newer then the .texi files and
# hence do not need to be rebuilt.  This eliminates the need for makeinfo.
# The -print is there just to confirm that the command is working.
%if %{without docs}
  find . -name *.info -print -exec touch {} \;
%endif

%ifarch %{power64}
%define _target_platform %{_arch}-%{_vendor}-%{_host_os}
%endif

#----------------------------------------------------------------------------

%build
echo target is %{binutils_target}

%if %{build_using_clang}
# Clang does not support the -fstack-clash-protection option.
%global optflags %(echo %{optflags} | sed 's/-fstack-clash-protection//')
%endif

%ifarch %{power64}
export CFLAGS="$RPM_OPT_FLAGS -Wno-error"
%else
export CFLAGS="$RPM_OPT_FLAGS"
%endif

CARGS=

case %{binutils_target} in i?86*|sparc*|ppc*|s390*|sh*|arm*|aarch64*)
  CARGS="$CARGS --enable-64-bit-bfd"
  ;;
esac

case %{binutils_target} in ia64*)
  CARGS="$CARGS --enable-targets=i386-linux"
  ;;
esac

case %{binutils_target} in ppc*|ppc64*)
  CARGS="$CARGS --enable-targets=spu"
  ;;
esac

case %{binutils_target} in ppc64-*)
  CARGS="$CARGS --enable-targets=powerpc64le-linux"
  ;;
esac

case %{binutils_target} in ppc64le*)
    CARGS="$CARGS --enable-targets=powerpc-linux"
    ;;
esac

# we are not elf
#case %{binutils_target} in x86_64*|i?86*|arm*|aarch64*)
#  CARGS="$CARGS --enable-targets=x86_64-pep"
#  ;;
#esac

%if %{default_relro}
  CARGS="$CARGS --enable-relro=yes"
%else
  CARGS="$CARGS --enable-relro=no"
%endif

%if 0%{?_with_debug:1}
export CFLAGS="$CFLAGS -O0 -ggdb2 -Wno-error -D_FORTIFY_SOURCE=0"
%define enable_shared 0
%endif

export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
export VENDOR="%{vendor}"

# We could optimize the cross builds size by --enable-shared but the produced
# binaries may be less convenient in the embedded environment.
# the below configure switchs we don't use
#  --build=%{_target_platform} --host=%{_target_platform} \
%configure \
%if %{build_using_clang}
   CC=clang \
   CXX=clang++ \
%endif
  --quiet \
  --with-system-zlib \
  --target=%{binutils_target} \
%if %{with gold}
  --enable-gold=default \
%endif
  --enable-ld \
%if %{isnative}
  --with-sysroot=/@unixroot \
%else
  --enable-targets=%{_host} \
  --with-sysroot=%{_prefix}/%{binutils_target}/sys-root \
  --program-prefix=%{cross} \
%endif
%if %{enable_shared}
  --enable-shared --disable-static \
%else
  --disable-shared \
%endif
%if %{enable_deterministic_archives}
  --enable-deterministic-archives \
%else
  --enable-deterministic-archives=no \
%endif
%if %{enable_lto}
  --enable-lto \
%endif
%if %{default_compress_debug}
  --enable-compressed-debug-sections=all \
%else
  --enable-compressed-debug-sections=none \
%endif
%if %{default_generate_notes}
  --enable-generate-build-notes=yes \
%else
  --enable-generate-build-notes=no \
%endif
%if %{enable_threading}
  --enable-threads=yes \
%else
  --enable-threads=no \
%endif
  $CARGS \
  --enable-plugins=no \
  --with-bugurl=http://github.com/bitwiseworks/binutils-os2

%if %{with docs}
make %{_smp_mflags} tooldir=%{_prefix} all
make %{_smp_mflags} tooldir=%{_prefix} info
%else
make %{_smp_mflags} tooldir=%{_prefix} MAKEINFO=true all
%endif

# Do not use %%check as it is run after %%install where libbfd.so is rebuilt
# with -fvisibility=hidden no longer being usable in its shared form.
%if %{without testsuite}
echo ====================TESTSUITE DISABLED=========================
%else
make -k check < /dev/null || :
echo ====================TESTING=========================
cat {gas/testsuite/gas,ld/ld,binutils/binutils}.sum
%if %{with gold}
if [ -f gold/test-suite.log ]; then
    cat gold/test-suite.log
fi
if [ -f gold/testsuite/test-suite.log ]; then
    cat gold/testsuite/*.log
fi
%endif
echo ====================TESTING END=====================
for file in {gas/testsuite/gas,ld/ld,binutils/binutils}.{sum,log}
do
  ln $file binutils-%{_target_platform}-$(basename $file) || :
done
tar cjf binutils-%{_target_platform}.tar.xz  binutils-%{_target_platform}-*.{sum,log}
uuencode binutils-%{_target_platform}.tar.xz binutils-%{_target_platform}.tar.xz
rm -f binutils-%{_target_platform}.tar.xz    binutils-%{_target_platform}-*.{sum,log}
%if %{with gold}
if [ -f gold/testsuite/test-suite.log ]; then
  tar cjf  binutils-%{_target_platform}-gold.log.tar.xz gold/testsuite/*.log
  uuencode binutils-%{_target_platform}-gold.log.tar.xz binutils-%{_target_platform}-gold.log.tar.xz
  rm -f    binutils-%{_target_platform}-gold.log.tar.xz
fi
%endif
%endif # with testsuite

#----------------------------------------------------------------------------

%install
%if %{with docs}  
make install DESTDIR=%{buildroot}
%else
make install DESTDIR=%{buildroot} MAKEINFO=true
%endif

%if %{isnative}
%if %{with docs}
make prefix=%{buildroot}%{_prefix} infodir=%{buildroot}%{_infodir} install-info
%endif

%if 0
# Rebuild libiberty.a with -fPIC.
# Future: Remove it together with its header file, projects should bundle it.
%make_build -C libiberty clean
%make_build CFLAGS="-g -fPIC $RPM_OPT_FLAGS" -C libiberty

# Rebuild libbfd.a with -fPIC.
# Without the hidden visibility the 3rd party shared libraries would export
# the bfd non-stable ABI.
%make_build -C bfd clean
%make_build CFLAGS="-g -fPIC $RPM_OPT_FLAGS -fvisibility=hidden" -C bfd

# Rebuild libopcodes.a with -fPIC.
%make_build -C opcodes clean
%make_build CFLAGS="-g -fPIC $RPM_OPT_FLAGS" -C opcodes
%endif

# Install libiberty stuff as we provide it
install -m 644 libiberty/libiberty.a %{buildroot}%{_libdir}
install -m 644 include/libiberty.h %{buildroot}%{_prefix}/include
install -m 644 include/demangle.h %{buildroot}%{_prefix}/include
install -m 644 include/dyn-string.h %{buildroot}%{_prefix}/include
install -m 644 include/fibheap.h %{buildroot}%{_prefix}/include
install -m 644 include/floatformat.h %{buildroot}%{_prefix}/include
install -m 644 include/hashtab.h %{buildroot}%{_prefix}/include
install -m 644 include/objalloc.h %{buildroot}%{_prefix}/include
install -m 644 include/partition.h %{buildroot}%{_prefix}/include
install -m 644 include/sort.h %{buildroot}%{_prefix}/include
install -m 644 include/splay-tree.h %{buildroot}%{_prefix}/include
#install -m 644 bfd/libbfd.a %{buildroot}%{_libdir}
#install -m 644 opcodes/libopcodes.a %{buildroot}%{_libdir}

# Remove Windows/Novell only man pages
rm -f %{buildroot}%{_mandir}/man1/dlltool*
rm -f %{buildroot}%{_mandir}/man1/nlmconv*
rm -f %{buildroot}%{_mandir}/man1/windres*
rm -f %{buildroot}%{_mandir}/man1/windmc*

%if %{without docs}
rm -f %{buildroot}%{_mandir}/man1/addr2line*
rm -f %{buildroot}%{_mandir}/man1/ar*
rm -f %{buildroot}%{_mandir}/man1/as*
rm -f %{buildroot}%{_mandir}/man1/c++filt*
rm -f %{buildroot}%{_mandir}/man1/elfedit*
rm -f %{buildroot}%{_mandir}/man1/gprof*
rm -f %{buildroot}%{_mandir}/man1/ld*
rm -f %{buildroot}%{_mandir}/man1/nm*
rm -f %{buildroot}%{_mandir}/man1/objcopy*
rm -f %{buildroot}%{_mandir}/man1/objdump*
rm -f %{buildroot}%{_mandir}/man1/ranlib*
rm -f %{buildroot}%{_mandir}/man1/readelf*
rm -f %{buildroot}%{_mandir}/man1/size*
rm -f %{buildroot}%{_mandir}/man1/strings*
rm -f %{buildroot}%{_mandir}/man1/strip*
rm -f %{buildroot}%{_infodir}/as*
rm -f %{buildroot}%{_infodir}/bfd*
rm -f %{buildroot}%{_infodir}/binutils*
rm -f %{buildroot}%{_infodir}/gprof*
rm -f %{buildroot}%{_infodir}/ld*
%endif

%if %{enable_shared}
chmod +x %{buildroot}%{_libdir}/*.dll
%endif

# Remove libtool files, which reference the .dll libs
rm -f %{buildroot}%{_libdir}/*.la

%if 0
# Sanity check --enable-64-bit-bfd really works.
grep '^#define BFD_ARCH_SIZE 64$' %{buildroot}%{_prefix}/include/bfd.h
# Fix multilib conflicts of generated values by __WORDSIZE-based expressions.
%ifarch %{ix86} x86_64 ppc %{power64} s390 s390x sh3 sh4 sparc sparc64 arm
sed -i -e '/^#include "ansidecl.h"/{p;s~^.*$~#include <bits/wordsize.h>~;}' \
    -e 's/^#define BFD_DEFAULT_TARGET_SIZE \(32\|64\) *$/#define BFD_DEFAULT_TARGET_SIZE __WORDSIZE/' \
    -e 's/^#define BFD_HOST_64BIT_LONG [01] *$/#define BFD_HOST_64BIT_LONG (__WORDSIZE == 64)/' \
    -e 's/^#define BFD_HOST_64_BIT \(long \)\?long *$/#if __WORDSIZE == 32\
#define BFD_HOST_64_BIT long long\
#else\
#define BFD_HOST_64_BIT long\
#endif/' \
    -e 's/^#define BFD_HOST_U_64_BIT unsigned \(long \)\?long *$/#define BFD_HOST_U_64_BIT unsigned BFD_HOST_64_BIT/' \
    %{buildroot}%{_prefix}/include/bfd.h
%endif
touch -r bfd/bfd-in2.h %{buildroot}%{_prefix}/include/bfd.h

# Generate .so linker scripts for dependencies; imported from glibc/Makerules:

# This fragment of linker script gives the OUTPUT_FORMAT statement
# for the configuration we are building.
OUTPUT_FORMAT="\
/* Ensure this .so library will not be used by a link for a different format
   on a multi-architecture system.  */
$(gcc $CFLAGS $LDFLAGS -shared -x c /dev/null -o /dev/null -Wl,--verbose -v 2>&1 | sed -n -f "%{SOURCE2}")"

tee %{buildroot}%{_libdir}/libbfd.so <<EOH
/* GNU ld script */

$OUTPUT_FORMAT

/* The libz dependency is unexpected by legacy build scripts.  */
/* The libdl dependency is for plugin support.  (BZ 889134)  */
INPUT ( %{_libdir}/libbfd.a -liberty -lz -ldl )
EOH

tee %{buildroot}%{_libdir}/libopcodes.so <<EOH
/* GNU ld script */

$OUTPUT_FORMAT

INPUT ( %{_libdir}/libopcodes.a -lbfd )
EOH
%endif

%else # !isnative
# For cross-binutils we drop the documentation.
rm -rf %{buildroot}%{_infodir}
# We keep these as one can have native + cross binutils of different versions.
#rm -rf {buildroot}%{_prefix}/share/locale
#rm -rf {buildroot}%{_mandir}
rm -rf %{buildroot}%{_libdir}/libiberty.a
%endif # !isnative

# This one comes from gcc
rm -f %{buildroot}%{_infodir}/dir
#rm -rf %{buildroot}%{_prefix}/%{binutils_target}

%find_lang %{?cross}binutils
%find_lang %{?cross}opcodes
%find_lang %{?cross}bfd
%find_lang %{?cross}gas
%find_lang %{?cross}gprof
cat %{?cross}opcodes.lang >> %{?cross}binutils.lang
cat %{?cross}bfd.lang >> %{?cross}binutils.lang
cat %{?cross}gas.lang >> %{?cross}binutils.lang
cat %{?cross}gprof.lang >> %{?cross}binutils.lang

if [ -x ld/ld-new ]; then
  %find_lang %{?cross}ld
  cat %{?cross}ld.lang >> %{?cross}binutils.lang
fi
if [ -x gold/ld-new ]; then
  %find_lang %{?cross}gold
  cat %{?cross}gold.lang >> %{?cross}binutils.lang
fi

#----------------------------------------------------------------------------

%post
%__rm -f %{_bindir}/%{?cross}ld
%if %{with_alternatives}
%{_sbindir}/alternatives --install %{_bindir}/%{?cross}ld %{?cross}ld \
  %{_bindir}/%{?cross}ld.bfd %{ld_bfd_priority}

%if %{with gold}
%{_sbindir}/alternatives --install %{_bindir}/%{?cross}ld %{?cross}ld \
  %{_bindir}/%{?cross}ld.gold %{ld_gold_priority}
%endif

# Do not run "alternatives --auto ld" here.  Leave the setting to
# however the user previously had it set.  See BZ 1592069 for more details.
%endif

%if %{isnative}
#ldconfig_post
%endif

exit 0

#----------------------------------------------------------------------------

%preun
%if %{with_alternatives}
if [ $1 = 0 ]; then
  %{_sbindir}/alternatives --remove %{?cross}ld %{_bindir}/%{?cross}ld.bfd
fi
%if %{with gold}
if [ $1 = 0 ]; then
  %{_sbindir}/alternatives --remove %{?cross}ld %{_bindir}/%{?cross}ld.gold
fi
%endif
%endif

exit 0

#----------------------------------------------------------------------------

%if %{isnative}
%postun
#ldconfig_postun
%endif

#----------------------------------------------------------------------------

%files -f %{?cross}binutils.lang
%license COPYING COPYING3 COPYING3.LIB COPYING.LIB
%doc README
%{_bindir}/%{?cross}[!l]*.exe
%{_prefix}/%{binutils_target}/bin/%{?cross}[!l]*.exe
# %%verify(symlink) does not work for some reason, so using "owner" instead.
#verify(owner) %{_bindir}/%{?cross}ld
#{_bindir}/%{?cross}ld.bfd

%if %{with docs}
%{_mandir}/man1/*
%{_infodir}/as.info.*
%{_infodir}/binutils.info.*
%{_infodir}/gprof.info.*
#{_infodir}/ld.info.*
%{_infodir}/bfd.info.*
%endif

%if %{enable_shared}
%{_libdir}/*.dll
%endif

%if %{isnative}

%files devel
%{_prefix}/include/*
%{_libdir}/*.a

%endif # isnative

%if %{with gold}
%files gold
%{_bindir}/%{?cross}ld.gold
%endif

# %%ghost %%{_bindir}/%%{?cross}ld

#----------------------------------------------------------------------------
%changelog
* Fri Dec 20 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.33.1-1
- update to version 2.33.1

* Tue Jan 15 2019 Dmitriy Kuminov <coding@dmik.org> 2.27-3
- Restore installation of libiberty.a (broken by 2.25-1).
- Install all libibetry headers.

* Thu Jun 15 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.27-2
- fix ticket #165 (needs to be reverted after gcc issue #27 fix)
- add bldlevel info to the dll

* Mon Mar 20 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.27-1
- update to version 2.27
- adjust spec to scm_ macros usage

* Tue May 31 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.25-1
- update to version 2.25

* Wed Oct 5 2011 yd <yd@os2power.com> 2.21-1
- Initial version
