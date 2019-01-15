# rpmbuild parameters:
# --define "binutils_target arm-linux-gnu" to create arm-linux-gnu-binutils.
# --with=bootstrap: Build with minimal dependencies.
# --with=debug: Build without optimizations and without splitting the debuginfo.
# --without=docs: Skip building documentation.
# --without=testsuite: Do not run the testsuite.

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
# BZ 1124342: Provide a way to enable deterministic archives.
# BZ 1195883: But do not do this by default.
%define enable_deterministic_archives 0

# BZ 1342618: Enable support for GCC LTO compilation.
%define enable_lto 0
# Disable the default generation of compressed debug sections.
%define default_compress_debug 0

# Default: Not bootstrapping.
%bcond_with bootstrap
# Default: Not debug
%bcond_with debug
# Default: Always build documentation.
%bcond_without docs
# Default: don't run run the testsuite.
%bcond_with testsuite

%if %{with bootstrap}
%undefine with_docs
%undefine with_testsuite
%endif

%if %{with debug}
%undefine with_testsuite
%endif


Summary: A GNU collection of binary utilities
Name: %{?cross}binutils%{?_with_debug:-debug}
Version: 2.27
Release: 3%{?dist}
License: GPLv3+
Group: Development/Tools
URL: http://sources.redhat.com/binutils

Vendor: bww bitwise works GmbH
%scm_source svn http://svn.netlabs.org/repos/ports/binutils/trunk 2204

Provides: bundled(libiberty)

# BZ 1173780: Building GOLD for PPC is not working at the moment.
# %define gold_arches %ix86 x86_64 %arm aarch64 ppc* %{power64}
%define gold_arches %ix86 x86_64 %arm aarch64

%if %{with bootstrap}
%define build_gold	no
%else
%ifarch %gold_arches
# we don't build on elf, so no gold for us
#define build_gold	both
%define build_gold	no
%else
%define build_gold	no
%endif
%endif

%if %{with debug}
# Define this if you want to skip the strip step and preserve debug info.
# Useful for testing.
%define __debug_install_post : > %{_builddir}/%{?buildsubdir}/debugfiles.list
%define debug_package %{nil}
%endif

BuildRequires: gcc make autoconf automake libtool

# Gold needs bison in order to build gold/yyscript.c.
# Bison needs m4.
%if "%{build_gold}" == "both"
BuildRequires: bison, m4, gcc-c++
%endif

%if %{without bootstrap}
BuildRequires: gettext, flex, zlib-devel
%endif

%if %{with docs}
BuildRequires: texinfo >= 4.0
# BZ 920545: We need pod2man in order to build the manual pages.
BuildRequires: /@unixroot/usr/bin/pod2man
Requires(post): %{_sbindir}/install-info.exe
Requires(preun): %{_sbindir}/install-info.exe
%endif

# Required for: ld-bootstrap/bootstrap.exp bootstrap with --static
# It should not be required for: ld-elf/elf.exp static {preinit,init,fini} array
%if %{with testsuite}
# relro_test.sh uses dc which is part of the bc rpm, hence its inclusion here.
BuildRequires: dejagnu, zlib-static, glibc-static, sharutils, bc
%if "%{build_gold}" == "both"
# The GOLD testsuite needs a static libc++
BuildRequires: libstdc++-static
%endif
%endif

Conflicts: gcc-c++ < 4.0.0

# The higher of these two numbers determines the default ld.
%{!?ld_bfd_priority: %global ld_bfd_priority	50}
%{!?ld_gold_priority:%global ld_gold_priority	30}

%if "%{build_gold}" == "both"
Requires(post): coreutils
Requires(post): %{_sbindir}/alternatives
Requires(preun): %{_sbindir}/alternatives
%endif

# On ARM EABI systems, we do want -gnueabi to be part of the
# target triple.
%ifnarch %{arm}
%define _gnu %{nil}
%endif

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

%package devel
Summary: BFD and opcodes static and dynamic libraries and header files
Group: System Environment/Libraries
Provides: binutils-static = %{version}-%{release}
%if %{with docs}
Requires(post): %{_sbindir}/install-info.exe
Requires(preun): %{_sbindir}/install-info.exe
%endif
Requires: zlib-devel
Requires: binutils = %{version}-%{release}
# BZ 1215242: We need touch...
Requires: coreutils

# To avoid header clashes (demangle.h etc)
Requires: libc-devel >= 0.6.6-40

%description devel
This package contains BFD and opcodes static and dynamic libraries.

The dynamic libraries are in this package, rather than a seperate
base package because they are actually linker scripts that force
the use of the static libraries.  This is because the API of the
BFD library is too unstable to be used dynamically.

The static libraries are here because they are now needed by the
dynamic libraries.

Developers starting new projects are strongly encouraged to consider
using libelf instead of BFD.

%debug_package

%prep
%scm_setup

autogen.sh

%if %{without docs}
  find . -name *.info -print -exec touch {} \;
%endif

%build
echo target is %{binutils_target}
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

case %{binutils_target} in  ppc64le*)
    CARGS="$CARGS --enable-targets=powerpc-linux"
    ;;
esac

# we are not elf
#case %{binutils_target} in x86_64*|i?86*|arm*|aarch64*)
#  CARGS="$CARGS --enable-targets=x86_64-pep"
#  ;;
#esac


%if 0%{?_with_debug:1}
CFLAGS="$CFLAGS -O0 -ggdb2 -Wno-error -D_FORTIFY_SOURCE=0"
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
  --target=%{binutils_target} \
  --with-system-zlib \
%ifarch %gold_arches
%if "%{build_gold}" == "both"
  --enable-gold=default --enable-ld \
%else
  --enable-ld \
%endif
%endif
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
  $CARGS \
  --enable-plugins=no \
  --with-bugurl=http://trac.netlabs.org/ports/

%if %{with docs}  
make %{_smp_mflags} tooldir=%{_prefix} all
make %{_smp_mflags} tooldir=%{_prefix} info
%else
make %{_smp_mflags} tooldir=%{_prefix} MAKEINFO=true all
%endif

# Do not use %%check as it is run after %%install where libbfd.so is rebuild
# with -fvisibility=hidden no longer being usable in its shared form.
%if %{without testsuite}
echo ====================TESTSUITE DISABLED=========================
%else
make -k check < /dev/null || :
echo ====================TESTING=========================
cat {gas/testsuite/gas,ld/ld,binutils/binutils}.sum
echo ====================TESTING END=====================
for file in {gas/testsuite/gas,ld/ld,binutils/binutils}.{sum,log}
do
  ln $file binutils-%{_target_platform}-$(basename $file) || :
done
tar cjf binutils-%{_target_platform}.tar.bz2 binutils-%{_target_platform}-*.{sum,log}
uuencode binutils-%{_target_platform}.tar.bz2 binutils-%{_target_platform}.tar.bz2
rm -f binutils-%{_target_platform}.tar.bz2 binutils-%{_target_platform}-*.{sum,log}
%endif

%install
rm -rf %{buildroot}
%if %{with docs}  
make install DESTDIR=%{buildroot}
%else
make install DESTDIR=%{buildroot} MAKEINFO=true
%endif

%if %{isnative}
%if %{with docs}
make prefix=%{buildroot}%{_prefix} infodir=%{buildroot}%{_infodir} install-info
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

# Remove Windows/Novell only man pages
rm -f %{buildroot}%{_mandir}/man1/dlltool*
rm -f %{buildroot}%{_mandir}/man1/nlmconv*
rm -f %{buildroot}%{_mandir}/man1/windres*
rm -f %{buildroot}%{_mandir}/man1/windmc*

%if %{enable_shared}
chmod +x %{buildroot}%{_libdir}/*.dll
%endif

# Remove libtool files, which reference the .dll libs
rm -f %{buildroot}%{_libdir}/*.la

%else # !%{isnative}
# For cross-binutils we drop the documentation.
rm -rf %{buildroot}%{_infodir}
# We keep these as one can have native + cross binutils of different versions.
#rm -rf %{buildroot}%{_prefix}/share/locale
#rm -rf %{buildroot}%{_mandir}
rm -rf %{buildroot}%{_libdir}/libiberty.a
%endif # !%{isnative}

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

%clean
rm -rf %{buildroot}

%post
%if "%{build_gold}" == "both"
%__rm -f %{_bindir}/%{?cross}ld
%{_sbindir}/alternatives --install %{_bindir}/%{?cross}ld %{?cross}ld \
  %{_bindir}/%{?cross}ld.bfd %{ld_bfd_priority}
%{_sbindir}/alternatives --install %{_bindir}/%{?cross}ld %{?cross}ld \
  %{_bindir}/%{?cross}ld.gold %{ld_gold_priority}
%{_sbindir}/alternatives --auto %{?cross}ld 
%endif
%if %{isnative}
#/sbin/ldconfig
%if %{with docs}
  %{_sbindir}/install-info --info-dir=%{_infodir} %{_infodir}/as.info.gz
  %{_sbindir}/install-info --info-dir=%{_infodir} %{_infodir}/binutils.info.gz
  %{_sbindir}/install-info --info-dir=%{_infodir} %{_infodir}/gprof.info.gz
# %{_sbindir}/install-info --info-dir=%{_infodir} %{_infodir}/ld.info.gz
%endif
%endif # %{isnative}
exit 0

%preun
%if "%{build_gold}" == "both"
if [ $1 = 0 ]; then
  %{_sbindir}/alternatives --remove %{?cross}ld %{_bindir}/%{?cross}ld.bfd
  %{_sbindir}/alternatives --remove %{?cross}ld %{_bindir}/%{?cross}ld.gold
fi
%endif
%if %{isnative}
if [ $1 = 0 ]; then
  if [ -f %{_infodir}/binutils.info.gz ]
  then
   %{_sbindir}/install-info --delete --info-dir=%{_infodir} %{_infodir}/as.info.gz
   %{_sbindir}/install-info --delete --info-dir=%{_infodir} %{_infodir}/binutils.info.gz
   %{_sbindir}/install-info --delete --info-dir=%{_infodir} %{_infodir}/gprof.info.gz
#  %{_sbindir}/install-info --delete --info-dir=%{_infodir} %{_infodir}/ld.info.gz
  fi
fi
%endif
exit 0

%if %{isnative}
%postun 
#/sbin/ldconfig
  if [ -f %{_infodir}/binutils.info.gz ]
  then
   %{_sbindir}/install-info --delete --info-dir=%{_infodir} %{_infodir}/as.info.gz
   %{_sbindir}/install-info --delete --info-dir=%{_infodir} %{_infodir}/binutils.info.gz
   %{_sbindir}/install-info --delete --info-dir=%{_infodir} %{_infodir}/gprof.info.gz
#  %{_sbindir}/install-info --delete --info-dir=%{_infodir} %{_infodir}/ld.info.gz
  fi
%endif # %{isnative}

%files -f %{?cross}binutils.lang
%defattr(-,root,root,-)
%license COPYING COPYING3 COPYING3.LIB COPYING.LIB
%doc README
%{_bindir}/%{?cross}[!l]*.exe
%{_prefix}/%{binutils_target}/bin/%{?cross}[!l]*.exe
%if "%{build_gold}" == "both"
%{_bindir}/%{?cross}ld*.exe
%ghost %{_bindir}/%{?cross}ld
%else
#%{_bindir}/%{?cross}ld*.exe
%endif
%{_mandir}/man1/*
%if %{enable_shared}
%{_libdir}/*.dll
%endif

%if %{isnative}
%if %{with docs}
%{_infodir}/[^b]*info*
%{_infodir}/binutils*info*
%endif

%files devel
%defattr(-,root,root,-)
%{_prefix}/include/*
%{_libdir}/*.a
%if %{with docs}
%{_infodir}/bfd*info*
%endif # with docs

%endif # %{isnative}

%changelog
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
