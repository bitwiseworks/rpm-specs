# ======================================================
# Conditionals and other variables controlling the build
# ======================================================

# Note that the bcond macros are named for the CLI option they create.
# "%%bcond_without" means "ENABLE by default and create a --without option"

# Whether to use RPM build wheels from the python-{pip,setuptools}-wheel package
# Uses upstream bundled prebuilt wheels otherwise
# setuptools >= 45.0 no longer support Python 2.7, hence disabled
%bcond_with rpmwheels

# Run the test suite in %%check
%if !0%{?os2_version}
%bcond_without tests
%else
%bcond_with tests
%endif

# By default, we build with tkinter, but e.g. the GIMP flatpak can turn this off
%if !0%{?os2_version}
%bcond_without tkinter
%else
%bcond_with tkinter
%endif

%global unicode ucs4
%global pybasever 2.7
%global pyshortver 27
%global pylibdir %{_libdir}/python%{pybasever}
%global tools_dir %{pylibdir}/Tools
%global demo_dir %{pylibdir}/Demo
%global doc_tools_dir %{pylibdir}/Doc/tools
%global dynload_dir %{pylibdir}/lib-dynload
%global site_packages %{pylibdir}/site-packages

%if 0%{?os2_version}
# Place rpm-macros into proper location
%global rpmmacrodir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)
# Exclude Windows installer stubs from debug info stripping
%define _strip_opts --debuginfo -x "wininst-*.exe"
%endif

# Python's configure script defines SOVERSION, and this is used in the Makefile
# to determine INSTSONAME, the name of the libpython DSO:
#   LDLIBRARY='libpython$(VERSION).so'
#   INSTSONAME="$LDLIBRARY".$SOVERSION
# We mirror this here in order to make it easier to add the -gdb.py hooks.
# (if these get out of sync, the payload of the libs subpackage will fail
# and halt the build)
%global py_SOVERSION 1.0
%global py_INSTSONAME_optimized libpython%{pybasever}.so.%{py_SOVERSION}
%global py_INSTSONAME_debug     libpython%{pybasever}_d.so.%{py_SOVERSION}

%global with_huntrleaks 0
%if !0%{?os2_version}
%global with_gdb_hooks 1
%global with_systemtap 1
%else
%global with_gdb_hooks 0
%global with_systemtap 0
%endif
%global with_valgrind 0
%if !0%{?os2_version}
%global with_gdbm 1
%else
%global with_gdbm 0
%endif

# Disable automatic bytecompilation. The python2.7 binary is not yet
# available in /usr/bin when Python is built. Also, the bytecompilation fails
# on files that test invalid syntax.
%global __brp_python_bytecompile %{nil}
%global regenerate_autotooling_patch 0

# ==================
# Top-level metadata
# ==================
Summary: Version %{pybasever} of the Python interpreter
Name: python%{pybasever}
URL: https://www.python.org/
%if 0%{?os2_version}
Vendor: bww bitwise works GmbH
%endif

%global general_version %{pybasever}.18
#global prerel ...
%global upstream_version %{general_version}%{?prerel}
Version: %{general_version}%{?prerel:~%{prerel}}
Release: 3%{?dist}
%if %{with rpmwheels}
License: Python
%else
# Python is Python
# setuptools is MIT and bundles:
#   packaging: BSD or ASL 2.0
#   pyparsing: MIT
#   six: MIT
# pip is MIT and bundles:
#   appdirs: MIT
#   distlib: Python
#   distro: ASL 2.0
#   html5lib: MIT
#   six: MIT
#   colorama: BSD
#   CacheControl: ASL 2.0
#   msgpack-python: ASL 2.0
#   lockfile: MIT
#   progress: ISC
#   ipaddress: Python
#   packaging: ASL 2.0 or BSD
#   pep517: MIT
#   pyparsing: MIT
#   pytoml: MIT
#   retrying: ASL 2.0
#   requests: ASL 2.0
#   chardet: LGPLv2
#   idna: BSD
#   urllib3: MIT
#   certifi: MPLv2.0
#   setuptools: MIT
#   webencodings: BSD
License: Python and MIT and ASL 2.0 and BSD and ISC and LGPLv2 and MPLv2.0 and (ASL 2.0 or BSD)
%endif


# Python 2 is deprecated in Fedora 30+, see:
#   https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal
# This means that new packages MUST NOT depend on python2, even transitively
#   see: https://fedoraproject.org/wiki/Packaging:Deprecating_Packages
# Python 2 will not be supported after 2019. Use the python3 package instead
# if possible.
Provides: deprecated()

# This package was renamed from python27 in Fedora 33
Provides:  python%{pyshortver} = %{version}-%{release}
Obsoletes: python%{pyshortver} < %{version}-%{release}

# People might want to dnf install python2 instead of pythonXY
Provides: python2 = %{version}-%{release}

# We want to be nice for the packages that still remain, so we keep providing this
# TODO stop doing this in undefined future
Provides: python(abi) = %{pybasever}

# To test the python27 without disrupting everything, we keep providing the devel part until mid September 2019
Provides: python2-devel = %{version}-%{release}
%if %{with tkinter}
Provides: python2-tkinter = %{version}-%{release}
%endif


# =======================
# Build-time requirements
# =======================

# (keep this list alphabetized)

BuildRequires: autoconf
%if !0%{?os2_version}
BuildRequires: bluez-libs-devel
%endif
BuildRequires: bzip2
BuildRequires: bzip2-devel
BuildRequires: expat-devel
BuildRequires: findutils
BuildRequires: gcc-c++
%if !0%{?os2_version}
BuildRequires: glibc-all-langpacks
BuildRequires: glibc-devel
%endif
BuildRequires: gmp-devel
%if !0%{?os2_version}
BuildRequires: libGL-devel
BuildRequires: libX11-devel
BuildRequires: libdb-devel
BuildRequires: libffi-devel
BuildRequires: libnsl2-devel
BuildRequires: libtirpc-devel
%endif
BuildRequires: make
BuildRequires: ncurses-devel
BuildRequires: openssl-devel
%if !0%{?os2_version}
BuildRequires: pkgconf-pkg-config
%endif
BuildRequires: readline-devel
BuildRequires: sqlite-devel
BuildRequires: tar
%if %{with tkinter}
BuildRequires: tcl-devel
BuildRequires: tix-devel
BuildRequires: tk-devel
%endif
BuildRequires: zlib-devel
%if !0%{?os2_version}
BuildRequires: gnupg2
%endif
BuildRequires: git-core

%if %{with_gdbm}
# ABI change without soname bump, reverted
BuildRequires: gdbm-devel >= 1:1.13
%endif

%if 0%{?with_systemtap}
BuildRequires: systemtap-sdt-devel
# (this introduces a circular dependency, in that systemtap-sdt-devel's
# /usr/bin/dtrace is a python script)
%global tapsetdir      /usr/share/systemtap/tapset
%endif # with_systemtap

%if 0%{?with_valgrind}
BuildRequires: valgrind-devel
%endif

%if %{with rpmwheels}
BuildRequires: python-setuptools-wheel < 45
BuildRequires: python-pip-wheel
Requires: python-setuptools-wheel < 45
Requires: python-pip-wheel
%else
Provides: bundled(python2dist(setuptools)) = 41.2.0
Provides: bundled(python2dist(packaging)) = 16.8
Provides: bundled(python2dist(pyparsing)) = 2.2.1
Provides: bundled(python2dist(six)) = 1.10.0

Provides: bundled(python2dist(pip)) = 19.2.3
Provides: bundled(python2dist(appdirs)) = 1.4.3
Provides: bundled(python2dist(CacheControl)) = 0.12.5
Provides: bundled(python2dist(certifi)) = 2019.6.16
Provides: bundled(python2dist(chardet)) = 3.0.4
Provides: bundled(python2dist(colorama)) = 0.4.1
Provides: bundled(python2dist(distlib)) = 0.2.9.post0
Provides: bundled(python2dist(distro)) = 1.4.0
Provides: bundled(python2dist(html5lib)) = 1.0.1
Provides: bundled(python2dist(idna)) = 2.8
Provides: bundled(python2dist(ipaddress)) = 1.0.22
Provides: bundled(python2dist(lockfile)) = 0.12.2
Provides: bundled(python2dist(msgpack)) = 0.6.1
Provides: bundled(python2dist(packaging)) = 19.0
Provides: bundled(python2dist(pep517)) = 0.5.0
Provides: bundled(python2dist(progress)) = 1.5
Provides: bundled(python2dist(pyparsing)) = 2.4.0
Provides: bundled(python2dist(pytoml)) = 0.1.20
Provides: bundled(python2dist(requests)) = 2.22.0
Provides: bundled(python2dist(retrying)) = 1.3.3
Provides: bundled(python2dist(setuptools)) = 41.0.1
Provides: bundled(python2dist(six)) = 1.12.0
Provides: bundled(python2dist(urllib3)) = 1.25.3
Provides: bundled(python2dist(webencodings)) = 0.5.1
%endif

# For /usr/lib64/pkgconfig/
%if !0%{?os2_version}
Requires: pkgconf-pkg-config
%endif

# The RPM related dependencies bring nothing to a non-RPM Python developer
# But we want them when packages BuildRequire python2-devel
%if !0%{?os2_version}
Requires: (python-rpm-macros if rpm-build)
Requires: (python-srpm-macros if rpm-build)
%else
Requires: python-rpm-macros
Requires: python-srpm-macros
%endif
# Remove this no sooner than Fedora 36:
Provides: python2-rpm-macros = 3.9-34
Obsoletes: python2-rpm-macros < 3.9-34

# https://bugzilla.redhat.com/show_bug.cgi?id=1217376
# https://bugzilla.redhat.com/show_bug.cgi?id=1496757
# https://bugzilla.redhat.com/show_bug.cgi?id=1218294
# TODO change to a specific subpackage once available (#1218294)
%if !0%{?os2_version}
Requires: (redhat-rpm-config if gcc)
%endif

Obsoletes: python2 < %{version}-%{release}
Obsoletes: python2-debug < %{version}-%{release}
Obsoletes: python2-devel < %{version}-%{release}
Obsoletes: python2-libs < %{version}-%{release}
Obsoletes: python2-test < %{version}-%{release}
Obsoletes: python2-tkinter < %{version}-%{release}
Obsoletes: python2-tools < %{version}-%{release}


# =======================
# Source code and patches
# =======================

%if !0%{?os2_version}
Source0: %{url}ftp/python/%{general_version}/Python-%{upstream_version}.tar.xz
Source1: %{url}ftp/python/%{general_version}/Python-%{upstream_version}.tar.xz.asc
Source2: %{url}static/files/pubkeys.txt

# Systemtap tapset to make it easier to use the systemtap static probes
# (actually a template; LIBRARY_PATH will get fixed up during install)
# Written by dmalcolm; not yet sent upstream
Source3: libpython.stp

# Example systemtap script using the tapset
# Written by wcohen, mjw, dmalcolm; not yet sent upstream
Source4: systemtap-example.stp

# Another example systemtap script that uses the tapset
# Written by dmalcolm; not yet sent upstream
Source5: pyfuntop.stp
%endif

Source6: macros.python2

# (Patches taken from github.com/fedora-python/cpython)

%if !0%{?os2_version}
# 00000 # eb41a89085f19eab30c9e1f22d09102f3dcab7f0
# Modules/Setup.dist is ultimately used by the "makesetup" script to construct
# the Makefile and config.c
#
# Upstream leaves many things disabled by default, to try to make it easy as
# possible to build the code on as many platforms as possible.
#
# TODO: many modules can also now be built by setup.py after the python binary
# has been built; need to assess if we should instead build things there
#
# We patch it downstream as follows:
#   - various modules are built by default by upstream as static libraries;
#   we built them as shared libraries
#   - build the "readline" module (appears to also be handled by setup.py now)
#   - build the nis module (which needs the tirpc library since glibc 2.26)
#   - enable the build of the following modules:
#     - array arraymodule.c     # array objects
#     - cmath cmathmodule.c # -lm # complex math library functions
#     - math mathmodule.c # -lm # math library functions, e.g. sin()
#     - _struct _struct.c       # binary structure packing/unpacking
#     - time timemodule.c # -lm # time operations and variables
#     - operator operator.c     # operator.add() and similar goodies
#     - _weakref _weakref.c     # basic weak reference support
#     - _testcapi _testcapimodule.c    # Python C API test module
#     - _random _randommodule.c # Random number generator
#     - _collections _collectionsmodule.c # Container types
#     - itertools itertoolsmodule.c
#     - strop stropmodule.c
#     - _functools _functoolsmodule.c
#     - _bisect _bisectmodule.c # Bisection algorithms
#     - unicodedata unicodedata.c    # static Unicode character database
#     - _locale _localemodule.c
#     - fcntl fcntlmodule.c     # fcntl(2) and ioctl(2)
#     - spwd spwdmodule.c               # spwd(3)
#     - grp grpmodule.c         # grp(3)
#     - select selectmodule.c   # select(2); not on ancient System V
#     - mmap mmapmodule.c  # Memory-mapped files
#     - _csv _csv.c  # CSV file helper
#     - _socket socketmodule.c  # Socket module helper for socket(2)
#     - _ssl _ssl.c
#     - crypt cryptmodule.c -lcrypt     # crypt(3)
#     - termios termios.c       # Steen Lumholt's termios module
#     - resource resource.c     # Jeremy Hylton's rlimit interface
#     - audioop audioop.c       # Operations on audio samples
#     - imageop imageop.c       # Operations on images
#     - _md5 md5module.c md5.c
#     - _sha shamodule.c
#     - _sha256 sha256module.c
#     - _sha512 sha512module.c
#     - linuxaudiodev linuxaudiodev.c
#     - timing timingmodule.c
#     - _tkinter _tkinter.c tkappinit.c
#     - dl dlmodule.c
#     - gdbm gdbmmodule.c
#     - _bsddb _bsddb.c
#     - binascii binascii.c
#     - parser parsermodule.c
#     - cStringIO cStringIO.c
#     - cPickle cPickle.c
#     - zlib zlibmodule.c
#     - _multibytecodec cjkcodecs/multibytecodec.c
#     - _codecs_cn cjkcodecs/_codecs_cn.c
#     - _codecs_hk cjkcodecs/_codecs_hk.c
#     - _codecs_iso2022 cjkcodecs/_codecs_iso2022.c
#     - _codecs_jp cjkcodecs/_codecs_jp.c
#     - _codecs_kr cjkcodecs/_codecs_kr.c
#     - _codecs_tw cjkcodecs/_codecs_tw.c
Patch0: python-2.7.1-config.patch

# 00001 # 4cc17cbeaa6c5320d44494c14fe4abe479bf186b
# Removes the "-g" option from "pydoc", for some reason; I believe
# (dmalcolm 2010-01-29) that this was introduced in this change:
# - fix pydoc (#68082)
# in 2.2.1-12 as a response to the -g option needing TkInter installed
# (Red Hat Linux 8)
Patch1: 00001-pydocnogui.patch

# 00004 # 81b93bf369d9d67c71beb5449ff0870f8ac15c7d
# Add $(CFLAGS) to the linker arguments when linking the "python" binary
# since some architectures (sparc64) need this (rhbz:199373).
# Not yet filed upstream
Patch4: python-2.5-cflags.patch

# 00006 # bebaf146393db2eb55ea494243a4095ae32eb50d
# Work around a bug in Python' gettext module relating to the "Plural-Forms"
# header (rhbz:252136)
# Related to upstream issues:
#   http://bugs.python.org/issue1448060 and http://bugs.python.org/issue1475523
# though the proposed upstream patches are, alas, different
Patch6: python-2.5.1-plural-fix.patch

# 00007 # 824c01cf0f2ee2f66cdd8373295431c16b809c5c
# This patch was listed in the changelog as:
#  * Fri Sep 14 2007 Jeremy Katz <katzj@redhat.com> - 2.5.1-11
#  - fix encoding of sqlite .py files to work around weird encoding problem
#  in Turkish (#283331)
# A traceback attached to rhbz 244016 shows the problem most clearly: a
# traceback on attempting to import the sqlite module, with:
#   "SyntaxError: encoding problem: with BOM (__init__.py, line 1)"
# This seems to come from Parser/tokenizer.c:check_coding_spec
# Our patch changes two source files within sqlite3, removing the
# "coding: ISO-8859-1" specs and character E4 = U+00E4 =
# LATIN SMALL LETTER A WITH DIAERESIS from in ghaering's surname.
#
# It may be that the conversion of "ISO-8859-1" to "iso-8859-1" is thwarted
# by the implementation of "tolower" in the Turkish locale; see:
#   https://bugzilla.redhat.com/show_bug.cgi?id=191096#c9
#
# TODO: Not yet sent upstream, and appears to me (dmalcolm 2010-01-29) that
# it may be papering over a symptom
Patch7: python-2.5.1-sqlite-encoding.patch

# 00010 # 4a21749202ce4e7b8ea716d38c194a997bcf5baa
# FIXME: Lib/ctypes/util.py posix implementation defines a function
# _get_soname(f).  Upstreams's implementation of this uses objdump to read the
# SONAME from a library; we avoid this, apparently to minimize space
# requirements on the live CD:
# (rhbz:307221)
Patch10: 00010-2.7.13-binutils-no-dep.patch

# 00013 # 4f2f7b3152a8c3d28441877567051384f23b3e4b
# Add various constants to the socketmodule (rhbz#436560):
# TODO: these patches were added in 2.5.1-22 and 2.5.1-24 but appear not to
# have been sent upstream yet:
Patch13: python-2.7rc1-socketmodule-constants.patch

# 00014 # 250d635a8481bc3bf729567e135d6d9cb4698199
# Add various constants to the socketmodule (rhbz#436560):
# TODO: these patches were added in 2.5.1-22 and 2.5.1-24 but appear not to
# have been sent upstream yet:
Patch14: python-2.7rc1-socketmodule-constants2.patch

# 00016 # 7ac402c3d2d7f6cd9b98deb0b7138765d31d105a
# Remove an "-rpath $(LIBDIR)" argument from the linkage args in configure.in:
# FIXME: is this for OSF, not Linux?
Patch16: python-2.6-rpath.patch

# 00017 # c30c4e768942a54dd3a5020c820935f9e2e9fa80
# Fixup distutils/unixccompiler.py to remove standard library path from rpath:
# Adapted from Patch0 in ivazquez' python3000 specfile, removing usage of
# super() as it's an old-style class
Patch17: python-2.6.4-distutils-rpath.patch

# 00055 # 4cde34923ef71a8c32f8fae50630c90645170500
# Systemtap support: add statically-defined probe points
# Patch based on upstream bug: http://bugs.python.org/issue4111
# fixed up by mjw and wcohen for 2.6.2, then fixed up by dmalcolm for 2.6.4
# then rewritten by mjw (attachment 390110 of rhbz 545179), then reformatted
# for 2.7rc1 by dmalcolm:
Patch55: 00055-systemtap.patch

# 00102 # 2242f5aa671eb490b5487dc46dcb05266decfe02
# Only used when "%%%%{_lib}" == "lib64"
# Fixup various paths throughout the build and in distutils from "lib" to "lib64",
# and add the /usr/lib64/pythonMAJOR.MINOR/site-packages to sitedirs, in front of
# /usr/lib/pythonMAJOR.MINOR/site-packages
# Not upstream
Patch102: 00102-2.7.13-lib64.patch

# 00103 # ccade12a68954f5bac4d00153ac92e7eee9c2b34
# Python 2.7 split out much of the path-handling from distutils/sysconfig.py to
# a new sysconfig.py (in r77704).
# We need to make equivalent changes to that new file to ensure that the stdlib
# and platform-specific code go to /usr/lib64 not /usr/lib, on 64-bit archs:
Patch103: python-2.7-lib64-sysconfig.patch

# 00104 # dc327f751c4f4ad6c2e7ad338e97a8a1e0650b60
# Only used when "%%%%{_lib}" == "lib64"
# Another lib64 fix, for distutils/tests/test_install.py; not upstream:
Patch104: 00104-lib64-fix-for-test_install.patch

# 00111 # 3dd8cb916b10ea83c0c7d690cf3c7512394a7f66
# Patch the Makefile.pre.in so that the generated Makefile doesn't try to build
# a libpythonMAJOR.MINOR.a (bug 550692):
# Downstream only: not appropriate for upstream
Patch111: 00111-no-static-lib.patch

# 00112 # 1676b155da8dcacc21fd20006105e3c164a6c5de
# Patch to support building both optimized vs debug stacks DSO ABIs, sharing
# the same .py and .pyc files, using "_d.so" to signify a debug build of an
# extension module.
#
# Based on Debian's patch for the same,
#  http://patch-tracker.debian.org/patch/series/view/python2.6/2.6.5-2/debug-build.dpatch
#
# (which was itself based on the upstream Windows build), but with some
# changes:
#
#   * Debian's patch to dynload_shlib.c looks for module_d.so, then module.so,
# but this can potentially find a module built against the wrong DSO ABI.  We
# instead search for just module_d.so in a debug build
#
#   * We remove this change from configure.in's build of the Makefile:
#   SO=$DEBUG_EXT.so
# so that sysconfig.py:customize_compiler stays with shared_lib_extension='.so'
# on debug builds, so that UnixCCompiler.find_library_file can find system
# libraries (otherwise "make sharedlibs" fails to find system libraries,
# erroneously looking e.g. for "libffi_d.so" rather than "libffi.so")
#
#   * We change Lib/distutils/command/build_ext.py:build_ext.get_ext_filename
# to add the _d there, when building an extension.  This way, "make sharedlibs"
# can build ctypes, by finding the sysmtem libffi.so (rather than failing to
# find "libffi_d.so"), and builds the module as _ctypes_d.so
#
#   * Similarly, update build_ext:get_libraries handling of Py_ENABLE_SHARED by
# appending "_d" to the python library's name for the debug configuration
#
#   * We modify Modules/makesetup to add the "_d" to the generated Makefile
# rules for the various Modules/*.so targets
#
# This may introduce issues when building an extension that links directly
# against another extension (e.g. users of NumPy?), but seems more robust when
# searching for external libraries
#
#   * We don't change Lib/distutils/command/build.py: build.build_purelib to
# embed plat_specifier, leaving it as is, as pure python builds should be
# unaffected by these differences (we'll be sharing the .py and .pyc files)
#
#   * We introduce DEBUG_SUFFIX as well as DEBUG_EXT:
#     - DEBUG_EXT is used by ELF files (names and SONAMEs); it will be "_d" for
# a debug build
#     - DEBUG_SUFFIX is used by filesystem paths; it will be "-debug" for a
# debug build
#
#   Both will be empty in an optimized build.  "_d" contains characters that
# are valid ELF metadata, but this leads to various ugly filesystem paths (such
# as the include path), and DEBUG_SUFFIX allows these paths to have more natural
# names.  Changing this requires changes elsewhere in the distutils code.
#
#   * We add DEBUG_SUFFIX to PYTHON in the Makefile, so that the two
# configurations build parallel-installable binaries with different names
# ("python-debug" vs "python").
#
#   * Similarly, we add DEBUG_SUFFIX within python-config and
#  python$(VERSION)-config, so that the two configuration get different paths
#  for these.
#
#  See also patch 130 below
Patch112: 00112-2.7.13-debug-build.patch

# 00113 # 9dd9dbc52d40c76002245bdc718f2d09590615bf
# Add configure-time support for the COUNT_ALLOCS and CALL_PROFILE options
# described at http://svn.python.org/projects/python/trunk/Misc/SpecialBuilds.txt
# so that if they are enabled, they will be in that build's pyconfig.h, so that
# extension modules will reliably use them
# Not yet sent upstream
Patch113: 00113-more-configuration-flags.patch

# 00114 # 3cfc26f24a13732fe602a47e389152714b757fd7
# Add flags for statvfs.f_flag to the constant list in posixmodule (i.e. "os")
# (rhbz:553020); partially upstream as http://bugs.python.org/issue7647
# Not yet sent upstream
Patch114: 00114-statvfs-f_flag-constants.patch

# 00121 # 15d7dd7ccf99e88ddc9d858cef57b1c91f6871b2
# Upstream r79310 removed the "Modules" directory from sys.path when Python is
# running from the build directory on POSIX to fix a unit test (issue #8205).
# This seems to have broken the compileall.py done in "make install": it cannot
# find shared library extension modules at this point in the build (sys.path
# does not contain DESTDIR/usr/lib(64)/python-2.7/lib-dynload for some reason),
# leading to the build failing with:
# Traceback (most recent call last):
#   File "/home/david/rpmbuild/BUILDROOT/python-2.7-0.1.rc2.fc14.x86_64/usr/lib64/python2.7/compileall.py", line 17, in <module>
#     import struct
#   File "/home/david/rpmbuild/BUILDROOT/python-2.7-0.1.rc2.fc14.x86_64/usr/lib64/python2.7/struct.py", line 1, in <module>
#    from _struct import *
# ImportError: No module named _struct
# This patch adds the build Modules directory to build path.
Patch121: 00121-add-Modules-to-build-path.patch

# 00128 # cf4b30b7664a016ba6ee399aad8f65588a7efd79
# 2.7.1 (in r84230) added a test to test_abc which fails if python is
# configured with COUNT_ALLOCS, which is the case for our debug build
# (the COUNT_ALLOCS instrumentation keeps "C" alive).
# Not yet sent upstream
Patch128: python-2.7.1-fix_test_abc_with_COUNT_ALLOCS.patch

# 00130 # a1595a504aa3fc712856b20bd0850a13b5755762
# Add "--extension-suffix" option to python-config and python-debug-config
# (rhbz#732808)
#
# This is adapted from 3.2's PEP-3149 support.
#
# Fedora's debug build has some non-standard features (see also patch 112
# above), though largely shared with Debian/Ubuntu and Windows
#
# In particular, SO in the Makefile is currently always just ".so" for our
# python 2 optimized builds, but for python 2 debug it should be '_d.so', to
# distinguish the debug vs optimized ABI, following the pattern in the above
# patch.
#
# Not yet sent upstream
Patch130: python-2.7.2-add-extension-suffix-to-python-config.patch

# 00131 # aa81f736a8d7cc4315e920bcec3cb5883c67034b
# The four tests in test_io built on top of check_interrupted_write_retry
# fail when built in Koji, for ppc and ppc64; for some reason, the SIGALRM
# handlers are never called, and the call to write runs to completion
# (rhbz#732998)
Patch131: 00131-disable-tests-in-test_io.patch

# 00132 # 1ec40c78e547fc449ee22a4dbc52562b89115f40
# Add non-standard hooks to unittest for use in the "check" phase below, when
# running selftests within the build:
#   @unittest._skipInRpmBuild(reason)
# for tests that hang or fail intermittently within the build environment, and:
#   @unittest._expectedFailureInRpmBuild
# for tests that always fail within the build environment
#
# The hooks only take effect if WITHIN_PYTHON_RPM_BUILD is set in the
# environment, which we set manually in the appropriate portion of the "check"
# phase below (and which potentially other python-* rpms could set, to reuse
# these unittest hooks in their own "check" phases)
Patch132: 00132-add-rpmbuild-hooks-to-unittest.patch

# 00133 # 434fef9eec3c579fd1ecc956136c1b7cc0b2ea3f
# "dl" is deprecated, and test_dl doesn't work on 64-bit builds:
Patch133: 00133-skip-test_dl.patch

# 00136 # 2f7c096e92687ca4ab771802f866588242ba9184
# Some tests try to seek on sys.stdin, but don't work as expected when run
# within Koji/mock; skip them within the rpm build:
Patch136: 00136-skip-tests-of-seeking-stdin-in-rpmbuild.patch

# 00137 # ddb14da3b15a1f6cfda5ab94919f624c91294e00
# Some tests within distutils fail when run in an rpmbuild:
Patch137: 00137-skip-distutils-tests-that-fail-in-rpmbuild.patch

# 00138 # c955cda1742fcfc632c8eaf0b50e4bffb199d33a
# Fixup some tests within distutils to work with how debug builds are set up:
Patch138: 00138-fix-distutils-tests-in-debug-build.patch

# 00139 # 38a2e2222cf61623fa5519a652a28537b5cd005d
# ARM-specific: skip known failure in test_float:
#  http://bugs.python.org/issue8265 (rhbz#706253)
Patch139: 00139-skip-test_float-known-failure-on-arm.patch

# 00140 # e5095acfe56937839f02013f9c46cb188784a5b2
# Sparc-specific: skip known failure in test_ctypes:
#  http://bugs.python.org/issue8314 (rhbz#711584)
# which appears to be a libffi bug
Patch140: 00140-skip-test_ctypes-known-failure-on-sparc.patch

# 00142 # bcd487be7de5823edd0017bf6778d5e2a0b06c8d
# Some pty tests fail when run in mock (rhbz#714627):
Patch142: 00142-skip-failing-pty-tests-in-rpmbuild.patch

# 00143 # 87bf5bbe4f0c89ec249ee9707bc03ccc9103406c
# Fix the --with-tsc option on ppc64, and rework it on 32-bit ppc to avoid
# aliasing violations (rhbz#698726)
# Sent upstream as http://bugs.python.org/issue12872
Patch143: 00143-tsc-on-ppc.patch

# 00144 # 7a99684f18ea9fc4c00cd2235c623658af36fc97
# (Optionally) disable the gdbm module:
Patch144: 00144-no-gdbm.patch

# 00146 # 310ca3207145a5ce6cf414a14650dbafcd7ad215
# Support OpenSSL FIPS mode (e.g. when OPENSSL_FORCE_FIPS_MODE=1 is set)
# - handle failures from OpenSSL (e.g. on attempts to use MD5 in a
#   FIPS-enforcing environment)
# - add a new "usedforsecurity" keyword argument to the various digest
#   algorithms in hashlib so that you can whitelist a callsite with
#   "usedforsecurity=False"
# (sent upstream for python 3 as http://bugs.python.org/issue9216; this is a
# backport to python 2.7; see RHEL6 patch 119)
# - enforce usage of the _hashlib implementation: don't fall back to the _md5
#   and _sha* modules (leading to clearer error messages if fips selftests
#   fail)
# - don't build the _md5 and _sha* modules; rely on the _hashlib implementation
#   of hashlib (for example, md5.py will use _hashlib's implementation of MD5,
#   if permitted by the FIPS setting)
# (rhbz#563986)
Patch146: 00146-hashlib-fips.patch

# 00147 # c77e8f43adbfb44f0a843f06869a36a37415d389
# Add a sys._debugmallocstats() function
# Based on patch 202 from RHEL 5's python.spec, with updates from rhbz#737198
# Sent upstream as http://bugs.python.org/issue14785
Patch147: 00147-add-debug-malloc-stats.patch

# 00155 # a154c44f2dfb60419cecaa193ef13e7613dbd488
# Avoid allocating thunks in ctypes unless absolutely necessary, to avoid
# generating SELinux denials on "import ctypes" and "import uuid" when
# embedding Python within httpd (rhbz#814391)
Patch155: 00155-avoid-ctypes-thunks.patch

# 00156 # a8d1c46e2ab627c493fdcea6d6ba752d9a7bfa2e
# Recent builds of gdb will only auto-load scripts from certain safe
# locations.  Turn off this protection when running test_gdb in the selftest
# suite to ensure that it can load our -gdb.py script (rhbz#817072):
# Not yet sent upstream
Patch156: 00156-gdb-autoload-safepath.patch

# 00165 # 38fdabaaa8c5d1576a372a22cdae1f17b65a215f
# Backport to Python 2 from Python 3.3 of improvements to the "crypt" module
# adding precanned ways of salting a password (rhbz#835021)
# Based on r88500 patch to py3k from Python 3.3
# plus 6482dd1c11ed, 0586c699d467, 62994662676a, 74a1110a3b50, plus edits
# to docstrings to note that this additional functionality is not standard
# within 2.7
Patch165: 00165-crypt-module-salt-backport.patch

# 00167 # 76aea104d5c20527ea08936fb6f2edbb52a07a46
# Don't run any of the stack navigation tests in test_gdb when Python is
# optimized, since there appear to be many different ways in which gdb can
# fail to read the PyFrameObject* for arbitrary places in the callstack,
# presumably due to compiler optimization (rhbz#912025)
#
# Not yet sent upstream
Patch167: 00167-disable-stack-navigation-tests-when-optimized-in-test_gdb.patch

# 00169 # 8d99c73e801c185674c7aee473d3466a118b566a
# Use SHA-256 rather than implicitly using MD5 within the challenge handling
# in multiprocessing.connection
#
# Sent upstream as http://bugs.python.org/issue17258
# (rhbz#879695)
Patch169: 00169-avoid-implicit-usage-of-md5-in-multiprocessing.patch

# 00170 # 029de09ec004fb47f8cbd978f68759e7b4267a38
# In debug builds, try to print repr() when a C-level assert fails in the
# garbage collector (typically indicating a reference-counting error
# somewhere else e.g in an extension module)
# Backported to 2.7 from a patch I sent upstream for py3k
#   http://bugs.python.org/issue9263  (rhbz#614680)
# hiding the proposed new macros/functions within gcmodule.c to avoid exposing
# them within the extension API.
# (rhbz#850013)
Patch170: 00170-gc-assertions.patch

# 00174 # 149dca2c7ba69102e681d9834ac13c153ca53afc
# Workaround for failure to set up prefix/exec_prefix when running
# an embededed libpython that sets Py_SetProgramName() to a name not
# on $PATH when run from the root directory due to
#   https://fedoraproject.org/wiki/Features/UsrMove
# e.g. cmpi-bindings under systemd (rhbz#817554):
Patch174: 00174-fix-for-usr-move.patch

# 00180 # 7199dba788cff67117e091f6ea84a8e7a98d39fe
# Enable building on ppc64p7
# Not appropriate for upstream, Fedora-specific naming
Patch180: 00180-python-add-support-for-ppc64p7.patch

# 00181 # 4034653bd9e53ead4d73f263d12acf20497b6155
# Allow arbitrary timeout for Condition.wait, as reported in
# https://bugzilla.redhat.com/show_bug.cgi?id=917709
# Upstream doesn't want this: http://bugs.python.org/issue17748
# But we have no better solution downstream yet, and since there is
# no API breakage, we apply this patch.
# Doesn't apply to Python 3, where this is fixed otherwise and works.
Patch181: 00181-allow-arbitrary-timeout-in-condition-wait.patch

# 00185 # b104ec8a02f122cfc5c1bdfe923dfe94a6b5079e
# Makes urllib2 honor "no_proxy" enviroment variable for "ftp:" URLs
# when ftp_proxy is set
Patch185: 00185-urllib2-honors-noproxy-for-ftp.patch

# 00189 # 038b390c478fe336a8ea350972785d317bdbbd53
# Instead of bundled wheels, use our RPM packaged wheels from
# /usr/share/python-wheels
Patch189: 00189-use-rpm-wheels.patch

# 00191 # d6f8cb42773c48c480e0639cc8a57aebbf3a4c76
# Disabling NOOP test as it fails without internet connection
Patch191: 00191-disable-NOOP.patch

# 00193 # 31a84748ead0945648369d3520369cdd508815e8
# Enable loading sqlite extensions. This patch isn't needed for
# python3.spec, since Python 3 has a configuration option for this.
# rhbz#1066708
# Patch provided by John C. Peterson
Patch193: 00193-enable-loading-sqlite-extensions.patch

# 00289 # a923413277ad6331772a93b9daeb85a842ddfc00
# Disable automatic detection for the nis module
# (we handle it it in Setup.dist, see Patch0)
Patch289: 00289-disable-nis-detection.patch

# 00351 # 1ae2a3db6d7af4ea973d1aee285e5fb9f882fdd0
# Avoid infinite loop when reading specially crafted TAR files using the tarfile module
# (CVE-2019-20907).
# See: https://bugs.python.org/issue39017
Patch351: 00351-cve-2019-20907-fix-infinite-loop-in-tarfile.patch

# 00354 # 9e9d2c6106446ad107ca1bb6729883c76fefc6eb
# Reject control chars in HTTP method in httplib.putrequest to prevent
# HTTP header injection
#
# Backported from Python 3.5-3.10 (and adjusted for py2's single-module httplib):
# - https://bugs.python.org/issue39603
# - https://github.com/python/cpython/pull/18485 (3.10)
# - https://github.com/python/cpython/pull/21946 (3.5)
#
# Co-authored-by: AMIR <31338382+amiremohamadi@users.noreply.github.com>
Patch354: 00354-cve-2020-26116-http-request-method-crlf-injection-in-httplib.patch

# 00357 # c4b8cabe4e772e4b8eea3e4dab5de12a3e9b5bc2
# CVE-2021-3177: Replace snprintf with Python unicode formatting in ctypes param reprs
#
# Backport of Python3 commit 916610ef90a0d0761f08747f7b0905541f0977c7:
# https://bugs.python.org/issue42938
# https://github.com/python/cpython/pull/24239
Patch357: 00357-CVE-2021-3177.patch

# (New patches go here ^^^)
#
# When adding new patches to "python2" and "python3" in Fedora, EL, etc.,
# please try to keep the patch numbers in-sync between all specfiles.
#
# More information, and a patch number catalog, is at:
#
#     https://fedoraproject.org/wiki/SIGs/Python/PythonPatches

# Disable tk, applied conditionally if %%{without tkinter}
Patch4000: 04000-disable-tk.patch

# This is the generated patch to "configure"; see the description of
#   %%{regenerate_autotooling_patch}
# above:

Patch5000: 05000-autotool-intermediates.patch
%else
%scm_source github http://github.com/bitwiseworks/python-os2 v%{version}-os2-2
%endif

# ======================================================
# Additional metadata
# ======================================================

%description
Python 2 is an old version of the language that is incompatible with the 3.x
line of releases. The language is mostly the same, but many details, especially
how built-in objects like dictionaries and strings work, have changed
considerably, and a lot of deprecated features have finally been removed in the
3.x line.

Note that Python 2 is not supported upstream after 2020-01-01, please use the
python3 package instead if you can.

This package also provides the "python2" executable.

# remove this part when we are sure everything works with python3
%if 0%{?os2_version}
%package -n python%{pybasever}-unversioned-command
Summary: The "python" command that runs Python 2

# In theory this could require any python2 version
Requires: python2 == %{version}-%{release}
# But since we want to provide versioned python, we require exact version
Provides: python = %{version}-%{release}
# This also save us an explicit conflict for older python2 builds

%description -n python%{pybasever}-unversioned-command
This package contains python.exe - the "python" command that runs Python 2.

%endif # os2_version

%if 0%{?os2_version}
%debug_package
%endif

# ======================================================
# The prep phase of the build:
# ======================================================

%prep
%if !0%{?os2_version}
%gpgverify -k2 -s1 -d0
%setup -q -n Python-%{upstream_version}
%else
%scm_setup
%endif

%if 0%{?with_systemtap}
# Provide an example of usage of the tapset:
cp -a %{SOURCE4} .
cp -a %{SOURCE5} .
%endif # with_systemtap

# Ensure that we're using the system copy of various libraries, rather than
# copies shipped by upstream in the tarball:
#   Remove embedded copy of expat:
rm -r Modules/expat || exit 1

#   Remove embedded copy of libffi:
for SUBDIR in darwin libffi libffi_arm_wince libffi_msvc libffi_osx ; do
  rm -r Modules/_ctypes/$SUBDIR || exit 1 ;
done

#   Remove embedded copy of zlib:
rm -r Modules/zlib || exit 1

## Disabling hashlib patch for now as it needs to be reimplemented
## for OpenSSL 1.1.0.
# Don't build upstream Python's implementation of these crypto algorithms;
# instead rely on _hashlib and OpenSSL.
#
# For example, in our builds md5.py uses always uses hashlib.md5 (rather than
# falling back to _md5 when hashlib.md5 is not available); hashlib.md5 is
# implemented within _hashlib via OpenSSL (and thus respects FIPS mode)
#for f in md5module.c md5.c shamodule.c sha256module.c sha512module.c; do
#    rm Modules/$f
#done

#
# Apply patches:
#
%if !0%{?os2_version}
%patch0 -p1 -b .rhconfig
%patch1 -p1 -b .no_gui
%patch4 -p1 -b .cflags
%patch6 -p1 -b .plural
%patch7 -p1

%if "%{_lib}" == "lib64"
%patch102 -p1 -b .lib64
%patch103 -p1 -b .lib64-sysconfig
%patch104 -p1
%endif

%patch10 -p1 -b .binutils-no-dep
%patch13 -p1 -b .socketmodule
%patch14 -p1 -b .socketmodule2
%patch16 -p1 -b .rpath
%patch17 -p1 -b .distutils-rpath

%if 0%{?with_systemtap}
%patch55 -p1 -b .systemtap
%endif

%patch111 -p1 -b .no-static-lib

%patch112 -p1 -b .debug-build

%patch113 -p1 -b .more-configuration-flags

%patch114 -p1 -b .statvfs-f-flag-constants


%patch121 -p1
%patch128 -p1

%patch130 -p1

%ifarch ppc %{power64}
%patch131 -p1
%endif

%patch132 -p1
%patch133 -p1
%patch136 -p1 -b .stdin-test
%patch137 -p1
%patch138 -p1
%ifarch %{arm}
%patch139 -p1
%endif
%ifarch %{sparc}
%patch140 -p1
%endif
%patch142 -p1 -b .tty-fail
%patch143 -p1 -b .tsc-on-ppc
%if !%{with_gdbm}
%patch144 -p1
%endif
#patch146 -p1
%patch147 -p1
%patch155 -p1
%patch156 -p1
%patch165 -p1
mv Modules/cryptmodule.c Modules/_cryptmodule.c
%patch167 -p1
%patch169 -p1
%patch170 -p1
%patch174 -p1 -b .fix-for-usr-move
%patch180 -p1
%patch181 -p1
%patch185 -p1

%if %{with rpmwheels}
%patch189 -p1
rm Lib/ensurepip/_bundled/*.whl
%endif

%patch191 -p1
%patch193 -p1
%patch289 -p1

# Patch 351 adds binary file for testing. We need to apply it using Git.
git apply %{PATCH351}

%patch354 -p1
%patch357 -p1

%if %{without tkinter}
%patch4000 -p1
%endif
%endif

# This shouldn't be necesarry, but is right now (2.2a3)
find -name "*~" |xargs rm -f

%if !0%{?os2_version}
%if ! 0%{regenerate_autotooling_patch}
# Normally we apply the patch to "configure"
# We don't apply the patch if we're working towards regenerating it
%patch5000 -p0 -b .autotool-intermediates
%endif
%else
# generate configure & friends
autoreconf -fvi
%endif

# ======================================================
# Configuring and building the code:
# ======================================================

%build
topdir=$(pwd)
%if !0%{?os2_version}
export CFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE -fPIC -fwrapv"
export CXXFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE -fPIC -fwrapv"
export CPPFLAGS="$(pkg-config --cflags-only-I libffi)"
export OPT="$RPM_OPT_FLAGS -D_GNU_SOURCE -fPIC -fwrapv"
export LINKCC="gcc"
export LDFLAGS="$RPM_LD_FLAGS"
if pkg-config openssl ; then
  export CFLAGS="$CFLAGS $(pkg-config --cflags openssl)"
  export LDFLAGS="$LDFLAGS $(pkg-config --libs-only-L openssl)"
fi
# Force CC
export CC=gcc
%else
# NOTE: Put -lcx to LDFLAGS instead of LIBS to have LIBCx linked to all shared
# (.pyd) modules in addition to the python DLL and EXE itself
export LDFLAGS="-g -Zbin-files -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx $LDFLAGS"
export LIBS="-lssl -lcrypto -lintl -lcx"
export VENDOR="%{vendor}"
export BOOTSTRAP_TIME="`LANG=C date +'%%d %%b %%Y %%H:%%M:%%S'`"
export LIBPATHSTRICT=T
%endif

%if 0%{regenerate_autotooling_patch}
# If enabled, this code regenerates the patch to "configure", using a
# local copy of autoconf-2.65, then exits the build
#
# The following assumes that the copy is installed to ~/autoconf-2.65/bin
# as per these instructions:
#   http://bugs.python.org/issue7997

for f in pyconfig.h.in configure ; do
    cp $f $f.autotool-intermediates ;
done

# Rerun the autotools:
PATH=~/autoconf-2.65/bin:$PATH autoconf
autoheader

# Regenerate the patch:
gendiff . .autotool-intermediates > %{PATCH5000}


# Exit the build
exit 1
%endif

# Define a function, for how to perform a "build" of python for a given
# configuration:
BuildPython() {
  ConfName=$1
  BinaryName=$2
  SymlinkName=$3
  ExtraConfigArgs=$4
  PathFixWithThisBinary=$5

  ConfDir=build/$ConfName

  echo STARTING: BUILD OF PYTHON FOR CONFIGURATION: $ConfName - %{_bindir}/$BinaryName
  mkdir -p $ConfDir

%if !0%{?os2_version}
  pushd $ConfDir
%else
  cd $ConfDir
%endif
  # Use the freshly created "configure" script, but in the directory two above:
  %global _configure $topdir/configure

%configure \
%if !0%{?os2_version}
  --enable-ipv6 \
%else
  --enable-ipv6=no \
%endif
  --enable-shared \
  --enable-unicode=%{unicode} \
%if !0%{?os2_version}
  --with-dbmliborder=gdbm:ndbm:bdb \
%endif
  --with-system-expat \
  --with-system-ffi \
%if 0%{?with_systemtap}
  --with-dtrace \
  --with-tapset-install-dir=%{tapsetdir} \
%endif
%if 0%{?with_valgrind}
  --with-valgrind \
%endif
  $ExtraConfigArgs \
  %{nil}

%if !0%{?os2_version}
%make_build EXTRA_CFLAGS="$CFLAGS"
%else
make EXTRA_CFLAGS="$CFLAGS"
%endif

# We need to fix shebang lines across the full source tree.
#
# We do this using the pathfix.py script, which requires one of the
# freshly-built Python binaries.
#
# We use the optimized python binary, and make the shebangs point at that same
# optimized python binary:
if $PathFixWithThisBinary
then
  # pathfix.py currently only works with files matching ^[a-zA-Z0-9_]+\.py$
  # when crawling through directories, so we handle the special cases manually
%if !0%{?os2_version}
  LD_LIBRARY_PATH="$topdir/$ConfDir" ./$BinaryName \
%else
  BEGINLIBPATH="$topdir/$ConfDir" ./$BinaryName \
%endif
    $topdir/Tools/scripts/pathfix.py \
      -i "%{_bindir}/python%{pybasever}" \
      $topdir \
      $topdir/Tools/pynche/pynche \
%if !0%{?os2_version}
      $topdir/Demo/pdist/{rcvs,rcsbump,rrcs} \
%else
      $topdir/Demo/pdist/rcvs \
      $topdir/Demo/pdist/rcsbump \
      $topdir/Demo/pdist/rrcs \
%endif
      $topdir/Demo/scripts/find-uname.py \
      $topdir/Tools/scripts/reindent-rst.py
fi

# Rebuild with new python
# We need a link to a versioned python in the build directory
ln -s $BinaryName $SymlinkName
%if !0%{?os2_version}
LD_LIBRARY_PATH="$topdir/$ConfDir" PATH=$PATH:$topdir/$ConfDir make -s EXTRA_CFLAGS="$CFLAGS" %{?_smp_mflags}
%else
BEGINLIBPATH="$topdir/$ConfDir" PATH="$PATH;$topdir/$ConfDir" make -s EXTRA_CFLAGS="$CFLAGS" %{?_smp_mflags}
%endif

%if !0%{?os2_version}
  popd
%else
  cd $topdir
%endif
  echo FINISHED: BUILD OF PYTHON FOR CONFIGURATION: $ConfDir
}

# Use "BuildPython" to support building with different configurations:

BuildPython optimized \
  python \
  python%{pybasever} \
  "" \
  true


# ======================================================
# Installing the built code:
# ======================================================

%install
%if 0%{?os2_version}
export LIBPATHSTRICT=T
%endif
topdir=$(pwd)
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_prefix} %{buildroot}%{_mandir}

# Clean up patched .py files that are saved as .lib64
for f in distutils/command/install distutils/sysconfig; do
    rm -f Lib/$f.py.lib64
done

InstallPython() {

  ConfName=$1
  BinaryName=$2
  PyInstSoName=$3

  ConfDir=build/$ConfName

  echo STARTING: INSTALL OF PYTHON FOR CONFIGURATION: $ConfName - %{_bindir}/$BinaryName
  mkdir -p $ConfDir

%if !0%{?os2_version}
  pushd $ConfDir
%else
  cd $ConfDir
%endif

%make_install

# We install a collection of hooks for gdb that make it easier to debug
# executables linked against libpython (such as /usr/lib/python itself)
#
# These hooks are implemented in Python itself
#
# gdb-archer looks for them in the same path as the ELF file, with a -gdb.py suffix.
# We put them in the debuginfo package by installing them to e.g.:
#  /usr/lib/debug/usr/lib/libpython2.6.so.1.0.debug-gdb.py
# (note that the debug path is /usr/lib/debug for both 32/64 bit)
#
# See https://fedoraproject.org/wiki/Features/EasierPythonDebugging for more
# information
#
# Initially I tried:
#  /usr/lib/libpython2.6.so.1.0-gdb.py
# but doing so generated noise when ldconfig was rerun (rhbz:562980)
#
%if 0%{?with_gdb_hooks}
DirHoldingGdbPy=%{_usr}/lib/debug/%{_libdir}
PathOfGdbPy=$DirHoldingGdbPy/$PyInstSoName-%{version}-%{release}.%{_arch}.debug-gdb.py

mkdir -p %{buildroot}$DirHoldingGdbPy
cp $topdir/Tools/gdb/libpython.py %{buildroot}$PathOfGdbPy

# Manually byte-compile the file, in case find-debuginfo.sh is run before
# brp-python-bytecompile, so that the .pyc/.pyo files are properly listed in
# the debuginfo manifest:
LD_LIBRARY_PATH="$topdir/$ConfDir" $topdir/$ConfDir/$BinaryName \
  -c "import compileall; import sys; compileall.compile_dir('%{buildroot}$DirHoldingGdbPy', ddir='$DirHoldingGdbPy')"

LD_LIBRARY_PATH="$topdir/$ConfDir" $topdir/$ConfDir/$BinaryName -O \
  -c "import compileall; import sys; compileall.compile_dir('%{buildroot}$DirHoldingGdbPy', ddir='$DirHoldingGdbPy')"
%endif # with_gdb_hooks

%if !0%{?os2_version}
  popd
%else
  cd $topdir
%endif

  echo FINISHED: INSTALL OF PYTHON FOR CONFIGURATION: $ConfName
}

# Use "InstallPython" to support building with different configurations:

# Now the optimized build:
InstallPython optimized \
  python%{pybasever} \
  %{py_INSTSONAME_optimized}


# Fix the interpreter path in binaries installed by distutils
# (which changes them by itself)
# Make sure we preserve the file permissions
for fixed in %{buildroot}%{_bindir}/pydoc; do
%if !0%{?os2_version}
    sed 's,#!.*/python$,#!/usr/bin/env python%{pybasever},' $fixed > $fixed- \
        && cat $fixed- > $fixed && rm -f $fixed-
%else
    sed 's,#!.*/python$,#!/@unixroot/usr/bin/env python%{pybasever},' $fixed > $fixed- \
        && cat $fixed- > $fixed && rm -f $fixed-
%endif
done

# Junk, no point in putting in -test sub-pkg
rm -f %{buildroot}/%{pylibdir}/idlelib/testcode.py*

# don't include tests that are run at build time in the package
# This is documented, and used: rhbz#387401
if /bin/false; then
 # Move this to -test subpackage.
mkdir save_bits_of_test
for i in test_support.py __init__.py; do
  cp -a %{buildroot}/%{pylibdir}/test/$i save_bits_of_test
done
rm -rf %{buildroot}/%{pylibdir}/test
mkdir %{buildroot}/%{pylibdir}/test
cp -a save_bits_of_test/* %{buildroot}/%{pylibdir}/test
fi

# tools

mkdir -p ${RPM_BUILD_ROOT}%{site_packages}

#pynche
rm -f Tools/pynche/*.pyw
cp -rp Tools/pynche \
  ${RPM_BUILD_ROOT}%{site_packages}/

mv Tools/pynche/README Tools/pynche/README.pynche

#gettext
install -m755  Tools/i18n/pygettext.py %{buildroot}%{_bindir}/
install -m755  Tools/i18n/msgfmt.py %{buildroot}%{_bindir}/

# Useful development tools
install -m755 -d %{buildroot}%{tools_dir}/scripts
install Tools/README %{buildroot}%{tools_dir}/
install Tools/scripts/*py %{buildroot}%{tools_dir}/scripts/

# Documentation tools
install -m755 -d %{buildroot}%{doc_tools_dir}
#install -m755 Doc/tools/mkhowto %{buildroot}%{doc_tools_dir}

# Useful demo scripts
install -m755 -d %{buildroot}%{demo_dir}
cp -ar Demo/* %{buildroot}%{demo_dir}

# Get rid of crap
find %{buildroot}/ -name "*~"|xargs rm -f
find %{buildroot}/ -name ".cvsignore"|xargs rm -f
find %{buildroot}/ -name "*.bat"|xargs rm -f
find . -name "*~"|xargs rm -f
find . -name ".cvsignore"|xargs rm -f


# Provide binaries in the form of bin2 and bin2.7, thus implementing
# (and expanding) the recommendations of PEP 394.
# Do NOT provide unversioned binaries
# https://fedoraproject.org/wiki/Changes/Python_means_Python3
mv %{buildroot}%{_bindir}/idle %{buildroot}%{_bindir}/idle%{pybasever}
ln -s ./idle%{pybasever} %{buildroot}%{_bindir}/idle2

mv %{buildroot}%{_bindir}/pydoc %{buildroot}%{_bindir}/pydoc%{pybasever}
ln -s ./pydoc%{pybasever} %{buildroot}%{_bindir}/pydoc2

mv %{buildroot}%{_bindir}/pygettext.py %{buildroot}%{_bindir}/pygettext%{pybasever}.py
ln -s ./pygettext%{pybasever}.py %{buildroot}%{_bindir}/pygettext2.py

mv %{buildroot}%{_bindir}/msgfmt.py %{buildroot}%{_bindir}/msgfmt%{pybasever}.py
ln -s ./msgfmt%{pybasever}.py %{buildroot}%{_bindir}/msgfmt2.py

mv %{buildroot}%{_bindir}/smtpd.py %{buildroot}%{_bindir}/smtpd%{pybasever}.py
ln -s ./smtpd%{pybasever}.py %{buildroot}%{_bindir}/smtpd2.py

%if 0%{?os2_version}
ln -s ./python%{pybasever}.exe %{buildroot}%{_bindir}/python%{pybasever}
%endif

# Link the unversioned stuff
%if 0%{?os2_version}
ln -s ./python%{pybasever}.exe %{buildroot}%{_bindir}/python
cp -p %{buildroot}%{_bindir}/python%{pybasever}.exe %{buildroot}%{_bindir}/python.exe
%endif

# Fix for bug #136654
rm -f %{buildroot}%{pylibdir}/email/test/data/audiotest.au %{buildroot}%{pylibdir}/test/audiotest.au

# Fix bug #143667: python should own /usr/lib/python2.x on 64-bit machines
%if "%{_lib}" == "lib64"
install -d %{buildroot}/%{_prefix}/lib/python%{pybasever}/site-packages
%endif

# Make python-devel multilib-ready (bug #192747, #139911)
%if !0%{?os2_version}
%global _pyconfig32_h pyconfig-32.h
%global _pyconfig64_h pyconfig-64.h

%ifarch %{power64} s390x x86_64 ia64 alpha sparc64 aarch64 %{mips64} riscv64
%global _pyconfig_h %{_pyconfig64_h}
%else
%global _pyconfig_h %{_pyconfig32_h}
%endif
%else
%global _pyconfig_h pyconfig.h
%endif

%global PyIncludeDirs python%{pybasever}

%if !0%{?os2_version}
for PyIncludeDir in %{PyIncludeDirs} ; do
  mv %{buildroot}%{_includedir}/$PyIncludeDir/pyconfig.h \
     %{buildroot}%{_includedir}/$PyIncludeDir/%{_pyconfig_h}
  cat > %{buildroot}%{_includedir}/$PyIncludeDir/pyconfig.h << EOF
#include <bits/wordsize.h>

#if __WORDSIZE == 32
#include "%{_pyconfig32_h}"
#elif __WORDSIZE == 64
#include "%{_pyconfig64_h}"
#else
#error "Unknown word size"
#endif
EOF
done
ln -s ../../libpython%{pybasever}.so %{buildroot}%{pylibdir}/config/libpython%{pybasever}.so
%endif

# Fix for bug 201434: make sure distutils looks at the right pyconfig.h file
# Similar for sysconfig: sysconfig.get_config_h_filename tries to locate
# pyconfig.h so it can be parsed, and needs to do this at runtime in site.py
# when python starts up.
#
# Split this out so it goes directly to the pyconfig-32.h/pyconfig-64.h
# variants:
sed -i -e "s/'pyconfig.h'/'%{_pyconfig_h}'/" \
  %{buildroot}%{pylibdir}/distutils/sysconfig.py \
  %{buildroot}%{pylibdir}/sysconfig.py

# Ensure that the curses module was linked against libncursesw.so, rather than
# libncurses.so (bug 539917)
%if !0%{?os2_version}
ldd %{buildroot}/%{dynload_dir}/_curses*.so \
    | grep curses \
    | grep libncurses.so && (echo "_curses.so linked against libncurses.so" ; exit 1)

# Ensure that the debug modules are linked against the debug libpython, and
# likewise for the optimized modules and libpython:
for Module in %{buildroot}/%{dynload_dir}/*.so ; do
    case $Module in
    *_d.so)
        ldd $Module | grep %{py_INSTSONAME_optimized} &&
            (echo Debug module $Module linked against optimized %{py_INSTSONAME_optimized} ; exit 1)

        ;;
    *)
        ldd $Module | grep %{py_INSTSONAME_debug} &&
            (echo Optimized module $Module linked against debug %{py_INSTSONAME_optimized} ; exit 1)
        ;;
    esac
done
%endif

#
# Systemtap hooks:
#
%if 0%{?with_systemtap}
# Install a tapset for this libpython into tapsetdir, fixing up the path to the
# library:
mkdir -p %{buildroot}%{tapsetdir}
%ifarch %{power64} s390x x86_64 ia64 alpha sparc64 aarch64 %{mips64}
%global libpython_stp_optimized libpython%{pybasever}-64.stp
%global libpython_stp_debug     libpython%{pybasever}-debug-64.stp
%else
%global libpython_stp_optimized libpython%{pybasever}-32.stp
%global libpython_stp_debug     libpython%{pybasever}-debug-32.stp
%endif

sed \
   -e "s|LIBRARY_PATH|%{_libdir}/%{py_INSTSONAME_optimized}|" \
   %{SOURCE3} \
   > %{buildroot}%{tapsetdir}/%{libpython_stp_optimized}

%endif # with_systemtap

# Do bytecompilation with the newly installed interpreter.
# compile *.pyo
find %{buildroot} -type f -a -name "*.py" -print0 | \
%if !0%{?os2_version}
    LD_LIBRARY_PATH="%{buildroot}%{dynload_dir}/:%{buildroot}%{_libdir}" \
%else
    BEGINLIBPATH="%{buildroot}%{dynload_dir}/;%{buildroot}%{_libdir}" \
%endif
    PYTHONPATH="%{buildroot}%{_libdir}/python%{pybasever} %{buildroot}%{_libdir}/python%{pybasever}/site-packages" \
    xargs -0 %{buildroot}%{_bindir}/python%{pybasever} -O -c 'import py_compile, sys; [py_compile.compile(f, dfile=f.partition("%{buildroot}")[2]) for f in sys.argv[1:]]' || :
# compile *.pyc
find %{buildroot} -type f -a -name "*.py" -print0 | \
%if !0%{?os2_version}
    LD_LIBRARY_PATH="%{buildroot}%{dynload_dir}/:%{buildroot}%{_libdir}" \
%else
    BEGINLIBPATH="%{buildroot}%{dynload_dir}/;%{buildroot}%{_libdir}" \
%endif
    PYTHONPATH="%{buildroot}%{_libdir}/python%{pybasever} %{buildroot}%{_libdir}/python%{pybasever}/site-packages" \
    xargs -0 %{buildroot}%{_bindir}/python%{pybasever} -c 'import py_compile, sys; [py_compile.compile(f, dfile=f.partition("%{buildroot}")[2]) for f in sys.argv[1:]]' || :


# Make library-files user writable
%if !0%{?os2_version}
/usr/bin/chmod 755 %{buildroot}%{dynload_dir}/*.so
/usr/bin/chmod 755 %{buildroot}%{_libdir}/libpython%{pybasever}.so.1.0
%else
chmod 755 %{buildroot}%{dynload_dir}/*.pyd
chmod 755 %{buildroot}%{_libdir}/*.dll
%endif

# Remove pyc/pyo files from /usr/bin
# They are not needed, and due to them, the resulting RPM is not multilib-clean
# https://bugzilla.redhat.com/show_bug.cgi?id=1703575
%if !0%{?os2_version}
rm %{buildroot}%{_bindir}/*.py{c,o}
%else
rm %{buildroot}%{_bindir}/*.pyc
rm %{buildroot}%{_bindir}/*.pyo
%endif
# Remove all remaining unversioned commands
# https://fedoraproject.org/wiki/Changes/Python_means_Python3
%if !0%{?os2_version}
rm %{buildroot}%{_bindir}/python
%else
rm -f %{buildroot}%{_bindir}/python%{pyshortver}.dll
%endif
rm %{buildroot}%{_bindir}/python-config
rm %{buildroot}%{_mandir}/*/python.1*
rm %{buildroot}%{_libdir}/pkgconfig/python.pc

# RPM macros
mkdir -p %{buildroot}%{rpmmacrodir}
cp -a %{SOURCE6} %{buildroot}%{rpmmacrodir}

# ======================================================
# Running the upstream test suite
# ======================================================

%check
topdir=$(pwd)
CheckPython() {
  ConfName=$1
  BinaryName=$2
  ConfDir=$(pwd)/build/$ConfName

  export OPENSSL_CONF=/non-existing-file

  echo STARTING: CHECKING OF PYTHON FOR CONFIGURATION: $ConfName

  # Note that we're running the tests using the version of the code in the
  # builddir, not in the buildroot.

  pushd $ConfDir

  EXTRATESTOPTS="--verbose"

%ifarch s390 s390x %{power64} %{arm} aarch64 %{mips}
    EXTRATESTOPTS="$EXTRATESTOPTS -x test_gdb"
%endif
%ifarch %{mips64}
    EXTRATESTOPTS="$EXTRATESTOPTS -x test_ctypes"
%endif

%if 0%{?with_huntrleaks}
  # Try to detect reference leaks on debug builds.  By default this means
  # running every test 10 times (6 to stabilize, then 4 to watch):
  if [ "$ConfName" = "debug"  ] ; then
    EXTRATESTOPTS="$EXTRATESTOPTS --huntrleaks : "
  fi
%endif

  # Run the upstream test suite, setting "WITHIN_PYTHON_RPM_BUILD" so that the
  # our non-standard decorators take effect on the relevant tests:
  #   @unittest._skipInRpmBuild(reason)
  #   @unittest._expectedFailureInRpmBuild
  WITHIN_PYTHON_RPM_BUILD= EXTRATESTOPTS="$EXTRATESTOPTS" make test

  popd

  echo FINISHED: CHECKING OF PYTHON FOR CONFIGURATION: $ConfName

}

%if %{with tests}

# no locale coercion in python2
# test_ssl:test_load_dh_params shutil.copies into unicode filename
export LC_ALL=C.utf-8

# Check each of the configurations:
CheckPython \
  optimized \
  python%{pybasever}

%endif # with tests


# ======================================================
# Cleaning up
# ======================================================

%if 0%{?os2_version}
%post -e
if [ "$1" = 1 ] ; then
#execute only on first install
%cube {DELLINE "SET PYTHONPATH="} %%{os2_config_sys} > NUL
%cube {DELLINE "SET PYTHONHOME="} %%{os2_config_sys} > NUL
fi
%endif

%if 0%{?os2_version}
%files -n python%{pybasever}-unversioned-command
%{_bindir}/python
%{_bindir}/python.exe
%endif

%files
%doc README
%license %{pylibdir}/LICENSE.txt
%{_bindir}/pydoc2*
%{_bindir}/python2
%{_bindir}/python%{pybasever}
%if 0%{?os2_version}
%{_bindir}/python%{pybasever}.exe
%endif
%{_mandir}/*/python2*

%dir %{pylibdir}
%dir %{dynload_dir}

%if !0%{?os2_version}
%{dynload_dir}/_md5module.so
%{dynload_dir}/_sha256module.so
%{dynload_dir}/_sha512module.so
%{dynload_dir}/_shamodule.so
%endif

%{dynload_dir}/Python-%{upstream_version}-py%{pybasever}.egg-info
%if !0%{?os2_version}
%{dynload_dir}/_bisectmodule.so
%{dynload_dir}/_bsddb.so
%{dynload_dir}/_codecs_cn.so
%{dynload_dir}/_codecs_hk.so
%{dynload_dir}/_codecs_iso2022.so
%{dynload_dir}/_codecs_jp.so
%{dynload_dir}/_codecs_kr.so
%{dynload_dir}/_codecs_tw.so
%{dynload_dir}/_collectionsmodule.so
%{dynload_dir}/_csv.so
%{dynload_dir}/_ctypes.so
%{dynload_dir}/_curses.so
%{dynload_dir}/_curses_panel.so
%{dynload_dir}/_elementtree.so
%{dynload_dir}/_functoolsmodule.so
%{dynload_dir}/_hashlib.so
%{dynload_dir}/_heapq.so
%{dynload_dir}/_hotshot.so
%{dynload_dir}/_io.so
%{dynload_dir}/_json.so
%{dynload_dir}/_localemodule.so
%{dynload_dir}/_lsprof.so
%{dynload_dir}/_multibytecodecmodule.so
%{dynload_dir}/_multiprocessing.so
%{dynload_dir}/_randommodule.so
%{dynload_dir}/_socketmodule.so
%{dynload_dir}/_sqlite3.so
%{dynload_dir}/_ssl.so
%{dynload_dir}/_struct.so
%{dynload_dir}/arraymodule.so
%{dynload_dir}/audioop.so
%{dynload_dir}/binascii.so
%{dynload_dir}/bz2.so
%{dynload_dir}/cPickle.so
%{dynload_dir}/cStringIO.so
%{dynload_dir}/cmathmodule.so
%{dynload_dir}/_cryptmodule.so
%{dynload_dir}/datetime.so
%{dynload_dir}/dbm.so
%{dynload_dir}/dlmodule.so
%{dynload_dir}/fcntlmodule.so
%{dynload_dir}/future_builtins.so
%if %{with_gdbm}
%{dynload_dir}/gdbmmodule.so
%endif
%{dynload_dir}/grpmodule.so
%{dynload_dir}/imageop.so
%{dynload_dir}/itertoolsmodule.so
%{dynload_dir}/linuxaudiodev.so
%{dynload_dir}/math.so
%{dynload_dir}/mmapmodule.so
%{dynload_dir}/nismodule.so
%{dynload_dir}/operator.so
%{dynload_dir}/ossaudiodev.so
%{dynload_dir}/parsermodule.so
%{dynload_dir}/pyexpat.so
%{dynload_dir}/readline.so
%{dynload_dir}/resource.so
%{dynload_dir}/selectmodule.so
%{dynload_dir}/spwdmodule.so
%{dynload_dir}/stropmodule.so
%{dynload_dir}/syslog.so
%{dynload_dir}/termios.so
%{dynload_dir}/timemodule.so
%{dynload_dir}/timingmodule.so
%{dynload_dir}/unicodedata.so
%{dynload_dir}/xxsubtype.so
%{dynload_dir}/zlibmodule.so
%else
%{dynload_dir}/*.pyd
%endif

%dir %{site_packages}
%{site_packages}/README
%{pylibdir}/*.py*
%{pylibdir}/*.doc
%{pylibdir}/wsgiref.egg-info
%dir %{pylibdir}/bsddb
%{pylibdir}/bsddb/*.py*
%{pylibdir}/compiler
%dir %{pylibdir}/ctypes
%{pylibdir}/ctypes/*.py*
%{pylibdir}/ctypes/macholib
%{pylibdir}/curses
%dir %{pylibdir}/distutils
%{pylibdir}/distutils/*.py*
%{pylibdir}/distutils/README
%{pylibdir}/distutils/command
%exclude %{pylibdir}/distutils/command/wininst-*.exe
%dir %{pylibdir}/email
%{pylibdir}/email/*.py*
%{pylibdir}/email/mime
%{pylibdir}/encodings
%{pylibdir}/hotshot
%{pylibdir}/idlelib
%{pylibdir}/importlib
%dir %{pylibdir}/json
%{pylibdir}/json/*.py*
%{pylibdir}/lib2to3
%{pylibdir}/logging
%{pylibdir}/multiprocessing
%if !0%{?os2_version}
%{pylibdir}/plat-linux2
%else
%{pylibdir}/plat-os2knix
%endif
%{pylibdir}/pydoc_data
%dir %{pylibdir}/sqlite3
%{pylibdir}/sqlite3/*.py*

%{pylibdir}/unittest
%{pylibdir}/wsgiref
%{pylibdir}/xml
%if "%{_lib}" == "lib64"
%attr(0755,root,root) %dir %{_prefix}/lib/python%{pybasever}
%attr(0755,root,root) %dir %{_prefix}/lib/python%{pybasever}/site-packages
%endif

%if !0%{?os2_version}
%{_libdir}/%{py_INSTSONAME_optimized}
%else
%{_libdir}/python%{pyshortver}.dll
%endif
%if 0%{?with_systemtap}
%dir %(dirname %{tapsetdir})
%dir %{tapsetdir}
%{tapsetdir}/%{libpython_stp_optimized}
%doc systemtap-example.stp pyfuntop.stp
%endif

%dir %{pylibdir}/ensurepip/
%{pylibdir}/ensurepip/*.py*
%if %{with rpmwheels}
%exclude %{pylibdir}/ensurepip/_bundled
%else
%dir %{pylibdir}/ensurepip/_bundled
%{pylibdir}/ensurepip/_bundled/*.whl
%endif


#files devel
%{_libdir}/pkgconfig/python-%{pybasever}.pc
%{_libdir}/pkgconfig/python2.pc
%{pylibdir}/config/
%{pylibdir}/distutils/command/wininst-*.exe
%dir %{_includedir}/python%{pybasever}/
%{_includedir}/python%{pybasever}/*.h

%doc Misc/README.valgrind Misc/valgrind-python.supp Misc/gdbinit
%{_bindir}/python2-config
%{_bindir}/python%{pybasever}-config
%if !0%{?os2_version}
%{_libdir}/libpython%{pybasever}.so
%else
%{_libdir}/python%{pybasever}_dll.a
%endif

#files tools
%doc Tools/pynche/README.pynche
%{site_packages}/pynche
%{_bindir}/smtpd2*.py

# https://bugzilla.redhat.com/show_bug.cgi?id=1111275
%exclude %{_bindir}/2to3*

%{_bindir}/idle2*
%{_bindir}/pygettext2*.py
%{_bindir}/msgfmt2*.py
%{tools_dir}
%{demo_dir}
%{pylibdir}/Doc

#files tkinter
%{pylibdir}/lib-tk
%if %{with tkinter}
%{dynload_dir}/_tkinter.so
%endif

#files test
%{pylibdir}/bsddb/test
%{pylibdir}/ctypes/test
%{pylibdir}/distutils/tests
%{pylibdir}/email/test
%{pylibdir}/json/tests
%{pylibdir}/sqlite3/test
%{pylibdir}/test/

%if !0%{?os2_version}
%{dynload_dir}/_ctypes_test.so
%{dynload_dir}/_testcapimodule.so
%endif

# RPM macros, dir co-owned to avoid the dependency
%dir %{rpmmacrodir}
%{rpmmacrodir}/macros.python2

# Workaround for rhbz#1476593
%undefine _debuginfo_subpackages

# ======================================================
# Finally, the changelog:
# ======================================================

%changelog
* Mon Dec 27 2021 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.7.18-3
- Fix issue #7

* Wed May 26 2021 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.7.18-2
- Add a symlink for python2.7
- Add python2.7-unversioned-command files
- Fix issue #5

* Mon May 10 2021 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.7.18-1
- Add python2-rpm-macros content here
- Rename package to python2.7
- update to latest version 2.7.18
- resync with fedora spec

* Sat May 16 2020 Dmitriy Kuminov <coding@dmik.org> 2.7.6-25
- Move OS/2 port from Trac to GitHub.
- Build with GCC 9 and latest toolchain.
- Provide built-in dbm and bsddb modules.
- Make python distutils recognize FOO_dll.a libraries in EMX mode.
- Make sys.getfilesystemencoding() never return None [#1].
- Properly restore BEGINLIBPATH and friends after execve/spawnve.

* Wed Jan 23 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.7.6-24
- fix ticket #328

* Mon Jan 14 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.7.6-23
- fix ticket #326

* Fri Dec 21 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.7.6-22
- adjust getaddrinfo and friends to latest libcx
- don't add .exe to symlinks

* Mon Jun 18 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.7.6-21
- use %{os2_config_sys} macro instead of fixed c:\config.sys

* Wed Apr 18 2018 Dmitriy Kuminov <coding@dmik.org> 2.7.6-20.
- Understand `*module.pyd` and `*module.dll` extensions for Python modules.
- Improve handling of BEGINLIBPATH and other pseudo-env vars (#299).

* Mon Jan 8 2018 Dmitriy Kuminov <coding@dmik.org> 2.7.6-19
- Make sys.executable work for fancy python exe names on OS/2.
- Enable real os.spawnv* implementation on OS/2.
- Use LIBCx spawn2 instead of fork in subprocess module to improve performance.
- Don't flatten case of tempdir (fixes file name comparison in some apps).
- Support NUMBER_OF_PROCESSORS in multitasking.cpu_count() on OS/2.
- Fix handling drive letters in urllib.url2pathname and pathname2url on OS/2.
- Bring pthread dependency back (it's still used).

* Sat Jun 3 2017 Dmitriy Kuminov <coding@dmik.org> 2.7.6-18
- Put the LIBCx library to LDFLAGS rather than LIBS to have all module DLLs
  linked against it as well.
- Rebuild against LIBCx 0.5.3 to incorporate DosRead JFS workaround for fread.
- Remove urpo as it conflicts with LIBCx.
- Remove pthread from libraries as not needed any more.
- Remove .pyo files (needed only in python -O mode which is rarely used).
- Remove .dbg files for Windows stubs (wininst-*.exe).
- Use scm_source/scm_setup for downloading sources.

* Mon Apr 24 2017 yd <yd@os2power.com> 2.7.6-17
- add new requirements and move unittest files. ticket#248.

* Fri Feb 17 2017 yd <yd@os2power.com> 2.7.6-16
- force db4 minimal version (libcx req).

* Thu Feb 09 2017 yd <yd@os2power.com> 2.7.6-15
- link with libcx for memory mapping support.

* Fri Jun 10 2016 yd <yd@os2power.com> 2.7.6-14
- fixed Obsoletes vs Conflicts.
- fixed python2-devel and -tools version.

* Thu Jun 09 2016 yd <yd@os2power.com> 2.7.6-13
- enable support for ucs4 unicode set. ticket#182.
- r780, fix file deletion. ticket#185.
- r779, remove 8.3 file name truncation, use opendir() to avoid resolving symlinks. ticket#185.
- r775, generate both 8.3 and long names for pyd dynamic libraries. fixes ticket#185.

* Sat Dec 12 2015 Dmitriy Kuminov <coding@dmik.org> 2.7.6-12
- r611, Add dummy plat-os2knix directory.
- r610, Fix silly typo.
- r609, Fix a typo in r529.
- r608, Make os.path.defpath return '$UNIXROOT/usr/bin' on OS/2 when it is set.
- r607, Replace altsep to sep in paths returned by os.path.join.
- r606, Add ignore patterns for *.pyc and generated files.
- r605, configure: Generate correct OS/2 defs and remove pre-built configure.
- r604, Fix building with no OS/2 Toolkit headers in include paths.
- r603, Use configured SHELL in subprocess module.
- Provide dummy _dlopen in ctypes to make colorama package happy.
- Use configured SHELL for subprocess.Popen(shell=True) instead of
  hardcoded '/bin/sh'.
- Make os.path.join replace all altsep (\) with sep (/) on return (to
  fix joining names with components of PATH-like env. vars and passing
  the results to a unix shell).
- Make os.path.defpath return '$UNIXROOT\\usr\\bin'.
- r568, build mmap module, by psmedley.

* Thu Feb 26 2015 yd <yd@os2power.com> 2.7.6-11
- r560, -O3 breaks the build, at least for pentium4 march.
- r529, use unixroot path for script path replacement. Fixes ticket#114.

* Mon Apr 07 2014 yd
- build for python 2.7.

* Sat Mar 15 2014 yd
- r385 and others, added support for virtualenv.
- added debug package with symbolic info for exceptq.

* Wed Jun 05 2013 yd
- r348, add samefile, sameopenfile, samestat to os.path module.

* Thu Dec 27 2012 yd
- fix local/bin requirements for python-tools.

* Mon Jan 16 2012 yd
- rebuild with libc 0.6.4 runtime.
