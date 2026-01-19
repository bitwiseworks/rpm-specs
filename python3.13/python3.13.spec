# ======================
# Bootstrap conditionals
# ======================

# When bootstrapping python3, we need to build python3-packaging.
# but packaging BR python3-devel and that brings in python3-rpm-generators;
# python3-rpm-generators needs python3-packaging, so we cannot have it yet.
#
# We also use the previous build of Python in "make regen-all".
#
# Procedure: https://fedoraproject.org/wiki/SIGs/Python/UpgradingPython
#
# Bootstrap enabled:
# - disables regen-all with the same Python version
# - disables dependency on python3-rpm-generators if we build with main_python
# - disables rpmwheels, optimizations and tests by default
%if !0%{?os2_version}
%bcond bootstrap 0
%else
%bcond_without bootstrap
%endif

# Whether to use RPM build wheels from the python-{pip,setuptools,wheel}-wheel packages
# Uses upstream bundled prebuilt wheels otherwise
%if !0%{?os2_version}
%bcond rpmwheels %{without bootstrap}
%else
%bcond_with rpmwheels
%endif

# Expensive optimizations (mainly, profile-guided optimizations)
# We don't have to switch it off for bootstrap, but it speeds up the first build,
# so we opt to only run them during the "full" build
%if !0%{?os2_version}
%bcond optimizations %{without bootstrap}
%else
%bcond_with optimizations
%endif

# Run the test suite in %%check
# Technically, we can run the tests even during the bootstrap build, but since
# we build Python 2x, it's better to just run it once with the "full" build
%if !0%{?os2_version}
%bcond tests %{without bootstrap}
%else
%bcond_with tests
%endif

# ==================
# Top-level metadata
# ==================

%global pybasever 3.13

# pybasever without the dot:
%global pyshortver 313

Name: python%{pybasever}
Summary: Version %{pybasever} of the Python interpreter
URL: https://www.python.org/

#  WARNING  When rebasing to a new Python version,
#           remember to update the python3-docs package as well
%global general_version %{pybasever}.11
#global prerel ...
%global upstream_version %{general_version}%{?prerel}
Version: %{general_version}%{?prerel:~%{prerel}}
Release: 1%{?dist}
License: Python-2.0.1


# ==================================
# Conditionals controlling the build
# ==================================

# Main Python, i.e. whether this is the main Python version in the distribution
# that owns /usr/bin/python3 and other unique paths
# This also means the built subpackages are called python3 rather than python3X
# By default, this is determined by the %%__default_python3_pkgversion value
%if !0%{?os2_version}
%bcond main_python %["%{?__default_python3_pkgversion}" == "%{pybasever}"]
%else
%bcond_without main_python
%endif

# If this is *not* Main Python, should it contain `Provides: python(abi) ...`?
# In Fedora no package shall depend on an alternative Python via this tag, so we do not provide it.
# In ELN/RHEL/CentOS we want to allow building against alternative stacks, so the Provide is enabled.
%if !0%{?os2_version}
%bcond python_abi_provides_for_alt_pythons %{undefined fedora}
%else
%bcond_with python_abi_provides_for_alt_pythons
%endif


# Extra build for debugging the interpreter or C-API extensions
# (the -debug subpackages)
%if !0%{?os2_version}
%bcond debug_build 1
%else
%bcond_with debug_build
%endif

# Extra build without GIL, the freethreading PEP 703 provisional way
# (the -freethreading subpackage)
%if !0%{?os2_version}
%bcond freethreading_build 1
%else
%bcond_with freethreading_build
%endif

# PEP 744: JIT Compilation
# Whether to build with the experimental JIT compiler
# We can only have this on Fedora 40+, where clang 18+ is available
# And only on certain architectures: https://peps.python.org/pep-0744/#support
# The freethreading build (when enabled) does not support JIT yet
%if !0%{?os2_version}
%bcond jit %[(0%{?fedora} >= 40 || 0%{?epel} >= 10) && ("%{_arch}" == "x86_64" || "%{_arch}" == "aarch64")]
%else
%bcond_with jit
%endif
%if %{with jit}
# When built with JIT, it still needs to be enabled on runtime via PYTHON_JIT=1
%global jit_flag --enable-experimental-jit=yes-off
%endif

# Main interpreter loop optimization
%if !0%{?os2_version}
%bcond computed_gotos 1
%else
%bcond_without computed_gotos
%endif

# =====================
# General global macros
# =====================

%if %{with main_python}
%global pkgname python3
%global exename python3
%global python3_pkgversion 3
%else
%global pkgname python%{pybasever}
%global exename python%{pybasever}
%global python3_pkgversion %{pybasever}
%endif

# If the rpmwheels condition is disabled, we use the bundled wheel packages
# from Python with the versions below.
# This needs to be manually updated when we update Python.
# Explore the sources tarball (you need the version before %%prep is executed):
#  $ tar -tf Python-%%{upstream_version}.tar.xz | grep whl
%global pip_version 25.3
%global setuptools_version 79.0.1
# All of those also include a list of indirect bundled libs:
# pip
#  $ %%{_rpmconfigdir}/pythonbundles.py <(unzip -p Lib/ensurepip/_bundled/pip-*.whl pip/_vendor/vendor.txt)
%global pip_bundled_provides %{expand:
Provides: bundled(python3dist(cachecontrol)) = 0.14.3
Provides: bundled(python3dist(certifi)) = 2025.10.5
Provides: bundled(python3dist(dependency-groups)) = 1.3.1
Provides: bundled(python3dist(distlib)) = 0.4
Provides: bundled(python3dist(distro)) = 1.9
Provides: bundled(python3dist(idna)) = 3.10
Provides: bundled(python3dist(msgpack)) = 1.1.2
Provides: bundled(python3dist(packaging)) = 25
Provides: bundled(python3dist(platformdirs)) = 4.5
Provides: bundled(python3dist(pygments)) = 2.19.2
Provides: bundled(python3dist(pyproject-hooks)) = 1.2
Provides: bundled(python3dist(requests)) = 2.32.5
Provides: bundled(python3dist(resolvelib)) = 1.2.1
Provides: bundled(python3dist(rich)) = 14.2
Provides: bundled(python3dist(setuptools)) = 70.3
Provides: bundled(python3dist(tomli)) = 2.3
Provides: bundled(python3dist(tomli-w)) = 1.2
Provides: bundled(python3dist(truststore)) = 0.10.4
Provides: bundled(python3dist(urllib3)) = 1.26.20
}
# setuptools
# vendor.txt not in .whl
# %%{_rpmconfigdir}/pythonbundles.py <(unzip -l Lib/test/wheeldata/setuptools-*.whl | grep -E '_vendor/.+dist-info/RECORD' | sed -E 's@^.*/([^-]+)-([^-]+)\.dist-info/.*$@\1==\2@')
%global setuptools_bundled_provides %{expand:
Provides: bundled(python3dist(autocommand)) = 2.2.2
Provides: bundled(python3dist(backports-tarfile)) = 1.2
Provides: bundled(python3dist(importlib-metadata)) = 8
Provides: bundled(python3dist(inflect)) = 7.3.1
Provides: bundled(python3dist(jaraco-collections)) = 5.1
Provides: bundled(python3dist(jaraco-context)) = 5.3
Provides: bundled(python3dist(jaraco-functools)) = 4.0.1
Provides: bundled(python3dist(jaraco-text)) = 3.12.1
Provides: bundled(python3dist(more-itertools)) = 10.3
Provides: bundled(python3dist(packaging)) = 24.2
Provides: bundled(python3dist(platformdirs)) = 4.2.2
Provides: bundled(python3dist(tomli)) = 2.0.1
Provides: bundled(python3dist(typeguard)) = 4.3
Provides: bundled(python3dist(typing-extensions)) = 4.12.2
Provides: bundled(python3dist(wheel)) = 0.45.1
Provides: bundled(python3dist(zipp)) = 3.19.2
}

# ABIFLAGS, LDVERSION and SOABI are in the upstream configure.ac
# See PEP 3149 for some background: http://www.python.org/dev/peps/pep-3149/
%global ABIFLAGS_optimized           %{nil}
%global ABIFLAGS_debug               d
%global ABIFLAGS_freethreading       t
%global ABIFLAGS_freethreading_debug td

%global LDVERSION_optimized           %{pybasever}%{ABIFLAGS_optimized}
%global LDVERSION_debug               %{pybasever}%{ABIFLAGS_debug}
%global LDVERSION_freethreading       %{pybasever}%{ABIFLAGS_freethreading}
%global LDVERSION_freethreading_debug %{pybasever}%{ABIFLAGS_freethreading_debug}

%global pylibdir %{_libdir}/python%{pybasever}
%global dynload_dir %{pylibdir}/lib-dynload
# freethreading libraries are located in e.g. /usr/lib64/python3.13t/
# https://github.com/python/cpython/issues/121103
%global pylibdir_freethreading %{pylibdir}%{ABIFLAGS_freethreading}
%global dynload_dir_freethreading %{pylibdir_freethreading}/lib-dynload

# We use the upstream arch triplets, we convert them from %%{_arch}-linux%%{_gnu}
%global platform_triplet %{expand:%(echo %{_arch}-linux%{_gnu} | sed -E \\
    -e 's/^arm(eb)?-linux-gnueabi$/arm\\1-linux-gnueabihf/' \\
    -e 's/^mips64(el)?-linux-gnu$/mips64\\1-linux-gnuabi64/' \\
    -e 's/^ppc(64)?(le)?-linux-gnu$/powerpc\\1\\2-linux-gnu/')}

%global SOABI_optimized           cpython-%{pyshortver}%{ABIFLAGS_optimized}-%{platform_triplet}
%global SOABI_debug               cpython-%{pyshortver}%{ABIFLAGS_debug}-%{platform_triplet}
%global SOABI_freethreading       cpython-%{pyshortver}%{ABIFLAGS_freethreading}-%{platform_triplet}
%global SOABI_freethreading_debug cpython-%{pyshortver}%{ABIFLAGS_freethreading_debug}-%{platform_triplet}

# All bytecode files are in a __pycache__ subdirectory, with a name
# reflecting the version of the bytecode.
# See PEP 3147: http://www.python.org/dev/peps/pep-3147/
# For example,
#   foo/bar.py
# has bytecode at:
#   foo/__pycache__/bar.cpython-%%{pyshortver}.pyc
#   foo/__pycache__/bar.cpython-%%{pyshortver}.opt-1.pyc
#   foo/__pycache__/bar.cpython-%%{pyshortver}.opt-2.pyc
%global bytecode_suffixes .cpython-%{pyshortver}*.pyc

# Python's configure script defines SOVERSION, and this is used in the Makefile
# to determine INSTSONAME, the name of the libpython DSO:
#   LDLIBRARY='libpython$(VERSION).so'
#   INSTSONAME="$LDLIBRARY".$SOVERSION
# We mirror this here in order to make it easier to add the -gdb.py hooks.
# (if these get out of sync, the payload of the libs subpackage will fail
# and halt the build)
%global py_SOVERSION 1.0
%global py_INSTSONAME_optimized           libpython%{LDVERSION_optimized}.so.%{py_SOVERSION}
%global py_INSTSONAME_debug               libpython%{LDVERSION_debug}.so.%{py_SOVERSION}
%global py_INSTSONAME_freethreading       libpython%{LDVERSION_freethreading}.so.%{py_SOVERSION}
%global py_INSTSONAME_freethreading_debug libpython%{LDVERSION_freethreading_debug}.so.%{py_SOVERSION}

%if !0%{?os2_version}
# The -O flag for the compiler, optimized builds
# https://fedoraproject.org/wiki/Changes/Python_built_with_gcc_O3
%global optflags_optimized -O3
# The -O flag for the compiler, debug builds
# -Wno-cpp avoids some warnings with -O0
%global optflags_debug -O0 -Wno-cpp
# Remove the default -O2 flag, our flags are applied in %%build/%%install
%global __global_compiler_flags %(echo '%{__global_compiler_flags}' | sed 's/-O[[:digit:]]//')
%else
%global optflags_optimized ""
%endif

# Disable automatic bytecompilation. The python3 binary is not yet be
# available in /usr/bin when Python is built. Also, the bytecompilation fails
# on files that test invalid syntax.
%undefine py_auto_byte_compile

# When a main_python build is attempted despite the %%__default_python3_pkgversion value
# We undefine magic macros so the python3-... package does not provide wrong python3X-...
%if %{with main_python} && ("%{?__default_python3_pkgversion}" != "%{pybasever}")
%undefine __pythonname_provides
%{warn:Doing a main_python build with wrong %%__default_python3_pkgversion (0%{?__default_python3_pkgversion}, but this is %pyshortver)}
%endif

%if %{with main_python}
# To keep the upgrade path clean, we Obsolete python3.X from the python3
# package and python3.X-foo from individual subpackages.
# Note that using Obsoletes without package version is not standard practice.
# Here we assert that *any* version of the system's default interpreter is
# preferable to an "extra" interpreter. For example, python3-3.6.1 will
# replace python3.6-3.6.2.
%define unversioned_obsoletes_of_python3_X_if_main() %{expand:\
Obsoletes: python%{pybasever}%{?1:-%{1}}\
}
%else
%define unversioned_obsoletes_of_python3_X_if_main() %{nil}
%endif

# =======================
# Build-time requirements
# =======================

# (keep this list alphabetized within the %%if blocks)

BuildRequires: autoconf
%if !0%{?os2_version}
BuildRequires: bluez-libs-devel
%endif
BuildRequires: bzip2-devel
BuildRequires: expat-devel
BuildRequires: findutils
BuildRequires: gcc
%if !0%{?os2_version}
BuildRequires: gdbm-devel
%endif
BuildRequires: git-core
%if !0%{?os2_version}
BuildRequires: glibc-devel
%endif
%if !0%{?os2_version}
BuildRequires: gnupg2
BuildRequires: libX11-devel
%endif
BuildRequires: libffi-devel
%if !0%{?os2_version}
BuildRequires: libuuid-devel
%endif
BuildRequires: make
BuildRequires: mpdecimal-devel
BuildRequires: ncurses-devel
BuildRequires: openssl-devel
BuildRequires: pkgconfig
BuildRequires: python-rpm-macros
BuildRequires: readline-devel
%if !0%{?os2_version}
BuildRequires: redhat-rpm-config >= 127
%endif
BuildRequires: sqlite-devel
%if !0%{?os2_version}
BuildRequires: systemtap-sdt-devel
%endif
BuildRequires: tcl-devel < 1:9
%if !0%{?os2_version}
BuildRequires: tk-devel < 1:9
%endif
BuildRequires: xz-devel
BuildRequires: zlib-devel
%if !0%{?os2_version}
BuildRequires: /usr/bin/dtrace
%endif

%if %{undefined rhel} && !0%{?os2_version}
BuildRequires: libb2-devel
%endif

%if %{with tests}
BuildRequires: gcc-c++
BuildRequires: gdb
BuildRequires: glibc-all-langpacks
BuildRequires: tzdata
%endif

%if %{with jit}
BuildRequires: clang(major) = 18
BuildRequires: llvm(major) = 18
%endif

%ifarch %{valgrind_arches}
BuildRequires: valgrind-devel
%endif

%if %{with main_python} && !0%{?os2_version}
BuildRequires: desktop-file-utils
BuildRequires: libappstream-glib
%endif

%if %{with rpmwheels}
# Python 3.12 removed the deprecated imp module,
# the first compatible version of pip is 23.1.2.
BuildRequires: %{python_wheel_pkg_prefix}-pip-wheel >= 23.1.2
%if %{with tests}
BuildRequires: %{python_wheel_pkg_prefix}-setuptools-wheel
BuildRequires: (%{python_wheel_pkg_prefix}-wheel-wheel if %{python_wheel_pkg_prefix}-setuptools-wheel < 71)
%endif
%endif

%if %{without bootstrap}
# for make regen-all
# Note that we're not using the %%{pkgname} macro here on purpose, because when
# upgrading the main python3 to a new Python version, this would pull in the
# old version instead.
BuildRequires: python%{pybasever}
%endif

%if %{without bootstrap} || %{without main_python}
# for proper automatic provides
BuildRequires: python3-rpm-generators
%endif

# =======================
# Source code and patches
# =======================

%if !0%{?os2_version}
Source0: %{url}ftp/python/%{general_version}/Python-%{upstream_version}.tar.xz
Source1: %{url}ftp/python/%{general_version}/Python-%{upstream_version}.tar.xz.asc
# The release manager for Python 3.13 is Thomas Wouters
Source2: https://github.com/Yhg1s.gpg

# A simple script to check timestamps of bytecode files
# Run in check section with Python that is currently being built
# Originally written by bkabrda
Source8: check-pyc-timestamps.py

# Desktop menu entry for idle3
Source10: idle3.desktop

# AppData file for idle3
Source11: idle3.appdata.xml

# (Patches taken from github.com/fedora-python/cpython)

# 00251 # 5ac6e7781923cbb3e4606e3bca381a1167d322e5
# Change user install location
#
# Set values of base and platbase in sysconfig from /usr
# to /usr/local when RPM build is not detected
# to make pip and similar tools install into separate location.
#
# Fedora Change: https://fedoraproject.org/wiki/Changes/Making_sudo_pip_safe
# Downstream only.
#
# We've tried to rework in Fedora 36/Python 3.10 to follow https://bugs.python.org/issue43976
# but we have identified serious problems with that approach,
# see https://bugzilla.redhat.com/2026979 or https://bugzilla.redhat.com/2097183
#
# pypa/distutils integration: https://github.com/pypa/distutils/pull/70
Patch251: 00251-change-user-install-location.patch

# 00464 # 292acffec7a379cb6d1f3c47b9e5a2f170bbadb6
# Enable PAC and BTI protections for aarch64
#
# Apply protection against ROP/JOP attacks for aarch64 on asm_trampoline.S
#
# The BTI flag must be applied in the assembler sources for this class
# of attacks to be mitigated on newer aarch64 processors.
#
# Upstream PR: https://github.com/python/cpython/pull/130864/files
#
# The upstream patch is incomplete but only for the case where
# frame pointers are not used on 3.13+.
#
# Since on Fedora we always compile with frame pointers the BTI/PAC
# hardware protections can be enabled without losing Perf unwinding.
Patch464: 00464-enable-pac-and-bti-protections-for-aarch64.patch

# 00466 # e10760fb955ee33d2917f8a57bb4e24d71e5341c
# Downstream only: Skip tests not working with older expat version
#
# We want to run these tests in Fedora and EPEL 10, but not in EPEL 9,
# which has too old version of expat. We set the upper bound version
# in the conditionalized skip to a release available in CentOS Stream 10,
# which is tested as working.
Patch466: 00466-downstream-only-skip-tests-not-working-with-older-expat-version.patch

# (New patches go here ^^^)
#
# When adding new patches to "python" and "python3" in Fedora, EL, etc.,
# please try to keep the patch numbers in-sync between all specfiles.
#
# More information, and a patch number catalog, is at:
#
#     https://fedoraproject.org/wiki/SIGs/Python/PythonPatches
#
# The patches are stored and rebased at:
#
#     https://github.com/fedora-python/cpython
%else
Vendor: bww bitwise works GmbH
%scm_source github http://github.com/bitwiseworks/python-os2 v%{version}-os2
%endif


# ==========================================
# Descriptions, and metadata for subpackages
# ==========================================


%if %{with main_python}
# Description for the python3X SRPM only:
%description
Python %{pybasever} is an accessible, high-level, dynamically typed, interpreted
programming language, designed with an emphasis on code readability.
It includes an extensive standard library, and has a vast ecosystem of
third-party libraries.

%package -n %{pkgname}
Summary: Python %{pybasever} interpreter

# In order to support multiple Python interpreters for development purposes,
# packages with fully versioned naming scheme (e.g. python3.9*) exist for
# non-default versions of Python 3.
# For consistency, we provide python3.X from python3 as well.
Provides: python%{pybasever} = %{version}-%{release}
%if !0%{?os2_version}
Provides: python%{pybasever}%{?_isa} = %{version}-%{release}
%endif

%unversioned_obsoletes_of_python3_X_if_main

# https://fedoraproject.org/wiki/Changes/Move_usr_bin_python_into_separate_package
# https://fedoraproject.org/wiki/Changes/Python_means_Python3
# We recommend /usr/bin/python so users get it by default
# Versioned recommends are problematic, and we know that the package requires
# python3 back with fixed version, so we just use the path here:
Recommends: %{_bindir}/python
%endif

# Python interpreter packages used to be named (or provide) name pythonXY (e.g.
# python39). However, to align it with the executable names and to prepare for
# Python 3.10, they were renamed to pythonX.Y (e.g. python3.9, python3.10). We
# provide the previous names.
Provides: python%{pyshortver} = %{version}-%{release}

%if %{with main_python} || %{with python_abi_provides_for_alt_pythons}
# Packages with Python modules in standard locations automatically
# depend on python(abi). Provide that here.
Provides: python(abi) = %{pybasever}
%else
# We exclude the `python(abi)` Provides
%global __requires_exclude ^python\\(abi\\) = 3\\..+
%global __provides_exclude ^python\\(abi\\) = 3\\..+
%endif

%if !0%{?os2_version}
Requires: %{pkgname}-libs%{?_isa} = %{version}-%{release}
%else
Requires: %{pkgname}-libs = %{version}-%{release}
%endif

# This prevents ALL subpackages built from this spec to require
# /usr/bin/python3* or python(abi). Granularity per subpackage is impossible.
# It's intended for the libs package not to drag in the interpreter, see
# https://bugzilla.redhat.com/show_bug.cgi?id=1547131
# https://bugzilla.redhat.com/show_bug.cgi?id=1862082
# All other packages require %%{pkgname} explicitly.
%if !0%{?os2_version}
%global __requires_exclude ^(/usr/bin/python3|python\\(abi\\))
%else
%global __requires_exclude ^(/@unixroot/usr/bin/python3|python\\(abi\\))
%endif

%description -n %{pkgname}
Python %{pybasever} is an accessible, high-level, dynamically typed, interpreted
programming language, designed with an emphasis on code readability.
It includes an extensive standard library, and has a vast ecosystem of
third-party libraries.

The %{pkgname} package provides the "%{exename}" executable: the reference
interpreter for the Python language, version 3.
The majority of its standard library is provided in the %{pkgname}-libs package,
which should be installed automatically along with %{pkgname}.
The remaining parts of the Python standard library are broken out into the
%{pkgname}-tkinter and %{pkgname}-test packages, which may need to be installed
separately.

Documentation for Python is provided in the %{pkgname}-docs package.

Packages containing additional libraries for Python are generally named with
the "%{pkgname}-" prefix.


%if %{with main_python}
# https://fedoraproject.org/wiki/Changes/Move_usr_bin_python_into_separate_package
# https://fedoraproject.org/wiki/Changes/Python_means_Python3
%package -n python-unversioned-command
Summary: The "python" command that runs Python 3
%if !0%{?os2_version}
BuildArch: noarch
%else
Provides:  python = %{version}-%{release}
Obsoletes: python < %{pybasever}
%endif

# In theory this could require any python3 version
Requires: python3 == %{version}-%{release}
# But since we want to provide versioned python, we require exact version
Provides: python = %{version}-%{release}
# This also save us an explicit conflict for older python3 builds

# Also provide the name of the Ubuntu package with the same function,
# to be nice to people who temporarily forgot which distro they're on.
# C.f. https://packages.ubuntu.com/hirsute/all/python-is-python3/filelist
Provides: python-is-python3 = %{version}-%{release}

%description -n python-unversioned-command
This package contains /usr/bin/python - the "python" command that runs Python 3.

%endif # with main_python


%package -n %{pkgname}-libs
Summary:        Python runtime libraries

# Python is generally licensed as Python-2.0.1 but also includes incorporated software
# Combined manually from https://docs.python.org/3.13/license.html
# Hash of Doc/license.rst which is compared in %%prep, generated with:
# $ sha256sum Doc/license.rst | cut -f1 -d" "
%global license_file_hash 62f2c9c2c75d511170eb464ad5f83b78cc1f37eb2eb49c2846c9aa6c4557ee99
# Licenses of incorporated software:
# Mersenne Twister in _random C extension contains code under BSD-3-Clause
# socket.getaddrinfo() and socket.getnameinfo() are BSD-3-Clause
# test.support.asynchat and test.support.asyncore are MIT-CMU
# http.cookies is MIT-CMU
# trace is HPND-SMC
# uu is MIT-CMU
# xmlrpc.client is MIT-CMU
# test.test_epoll is MIT
# select kqueue interface is BSD-2-Clause
# SipHash algorithm in Python/pyhash.c is MIT
# strtod and dtoa are dtoa
# OpenSSL is not bundled
# expat is not bundled
# libffi is not bundled
# zlib is not bundled
# cfuhash used by tracemalloc is BSD-3-Clause
# libmpdec is not bundled
# C14N test suite in Lib/test/xmltestdata/c14n-20/ is BSD-3-Clause
# mimalloc is MIT
# parts of asyncio from uvloop are MIT
# Python/qsbr.c is adapted from code under BSD-2-Clause
# Bundled libb2 is not declared in the upstream document, but it's:
# CC0-1.0, covered by grandfathering exception
# We don't query upstream for changes, as 3.13 is the last Python version containing it.
%global libs_license Python-2.0.1 AND CC0-1.0 AND MIT AND BSD-3-Clause AND MIT-CMU AND HPND-SMC AND BSD-2-Clause AND dtoa
%if %{with rpmwheels}
Requires: %{python_wheel_pkg_prefix}-pip-wheel >= 23.1.2
License: %{libs_license}
%else
Provides: bundled(python3dist(pip)) = %{pip_version}
%pip_bundled_provides
# License combined from Python libs + pip
License: %{libs_license} AND Apache-2.0 AND ISC AND LGPL-2.1-only AND MPL-2.0 AND (Apache-2.0 OR BSD-2-Clause)
%endif

%unversioned_obsoletes_of_python3_X_if_main libs

%if !0%{?os2_version}
# Bundled internal headers are used even when building with system libb2
# last updated by https://github.com/python/cpython/pull/6286
Provides: bundled(libb2) = 0.98.1

# Bundled mimalloc version in Include/internal/mimalloc/mimalloc.h
# Python's version is modified, differences are listed in:
# https://github.com/python/cpython/issues/113141
Provides: bundled(mimalloc) = 2.12
%endif

# There are files in the standard library that have python shebang.
# We've filtered the automatic requirement out so libs are installable without
# the main package. This however makes it pulled in by default.
# See https://bugzilla.redhat.com/show_bug.cgi?id=1547131
%if !0%{?os2_version}
Recommends: %{pkgname}%{?_isa} = %{version}-%{release}
%else
Recommends: %{pkgname} = %{version}-%{release}
%endif

# tkinter is part of the standard library,
# but it is torn out to save an unwanted dependency on tk and X11.
# we recommend it when tk is already installed (for better UX)
%if !0%{?os2_version}
Recommends: (%{pkgname}-tkinter%{?_isa} = %{version}-%{release} if tk%{?_isa})
%endif

# The zoneinfo module needs tzdata
%if !0%{?os2_version}
Requires: tzdata
%endif

%if 0%{?os2_version} && %{with main_python}
Provides:  python-libs = %{version}-%{release}
Obsoletes: python-libs < %{pybasever}
%endif

# The requirement on libexpat is generated, but we need to version it.
# When built with a specific expat version, but installed with an older one,
# we sometimes get:
#   ImportError: /usr/lib64/python3.X/lib-dynload/pyexpat.cpython-....so:
#   undefined symbol: XML_...
# The pyexpat module has build-time checks for expat version to only use the
# available symbols. However, there is no runtime protection, so when the module
# is later installed with an older expat, it may error due to undefined symbols.
# This breaks many things, including python -m venv.
# We avoid this problem by requiring at least the same version of expat that
# was used during the build time.
# Other subpackages (like -debug) also need this, but they all depend on -libs.
%global expat_version %(LANG=C rpm -q --qf '%%{version}' expat.%{_target_cpu} | sed 's/.*not installed/0/')
%if !0%{?os2_version}
%global expat_version %(LANG=C rpm -q --qf '%%{version}' expat.%{_target_cpu} | sed 's/.*not installed/0/')
Requires: expat%{?_isa} >= %{expat_version}
%else
%global expat_version %(LANG=C rpm -q --qf '%%{version}' expat | sed 's/.*not installed/0/')
Requires: expat >= %{expat_version}
%endif


%description -n %{pkgname}-libs
This package contains runtime libraries for use by Python:
- the majority of the Python standard library
- a dynamically linked library for use by applications that embed Python as
  a scripting language, and by the main "%{exename}" executable


%package -n %{pkgname}-devel
Summary: Libraries and header files needed for Python development
# Bundled mimalloc header files are MIT
License: Python-2.0.1 AND MIT
Requires: %{pkgname} = %{version}-%{release}
%if !0%{?os2_version}
Requires: %{pkgname}-libs%{?_isa} = %{version}-%{release}
%else
Requires: %{pkgname}-libs = %{version}-%{release}
%endif
# The RPM related dependencies bring nothing to a non-RPM Python developer
# But we want them when packages BuildRequire python3-devel
%if !0%{?os2_version}
Requires: (python-rpm-macros if rpm-build)
Requires: (python3-rpm-macros if rpm-build)
%else
Requires: python-rpm-macros
Requires: python3-rpm-macros
%endif
# We omit this dependency on RHEL to avoid pulling the macros to AppStream:
# RHEL users can use the minimal implementation of %%pyproject_buildrequires
# from pyproject-srpm-macros instead.
# On Fedora, we keep this to avoid one additional round of %%generate_buildrequires.
%if !0%{?os2_version}
%{!?rhel:Requires: (pyproject-rpm-macros if rpm-build)}
%else
Requires: pyproject-rpm-macros
%endif

%unversioned_obsoletes_of_python3_X_if_main devel

%if %{with main_python}
# Python developers are very likely to need pip
Recommends: %{pkgname}-pip
%endif

# tox users are likely to need the devel subpackage
%if !0%{?os2_version}
Supplements: tox
%endif

%if %{without bootstrap} || %{without main_python}
# Generators run on the main Python 3 so we cannot require them when bootstrapping it
Requires: (python3-rpm-generators if rpm-build)
%endif

Conflicts: %{pkgname} < %{version}-%{release}

%if 0%{?os2_version} && %{with main_python}
Requires:  python3-rpm-generators
Provides:  python-devel = %{version}-%{release}
Obsoletes: python-devel < %{pybasever}
%endif

%description -n %{pkgname}-devel
This package contains the header files and configuration needed to compile
Python extension modules (typically written in C or C++), to embed Python
into other programs, and to make binary distributions for Python libraries.


%package -n %{pkgname}-idle
Summary: A basic graphical development environment for Python
Requires: %{pkgname} = %{version}-%{release}
Requires: %{pkgname}-tkinter = %{version}-%{release}

%unversioned_obsoletes_of_python3_X_if_main idle

%if %{with main_python}
Provides: idle3 = %{version}-%{release}
Provides: idle = %{version}-%{release}
%endif

Provides: %{pkgname}-tools = %{version}-%{release}
%if !0%{?os2_version}
Provides: %{pkgname}-tools%{?_isa} = %{version}-%{release}
%endif

%if 0%{?os2_version} && %{with main_python}
Provides:  python-tools = %{version}-%{release}
Obsoletes: python-tools < %{pybasever}
%endif

%description -n %{pkgname}-idle
IDLE is Python’s Integrated Development and Learning Environment.

IDLE has the following features: Python shell window (interactive
interpreter) with colorizing of code input, output, and error messages;
multi-window text editor with multiple undo, Python colorizing,
smart indent, call tips, auto completion, and other features;
search within any window, replace within editor windows, and
search through multiple files (grep); debugger with persistent
breakpoints, stepping, and viewing of global and local namespaces;
configuration, browsers, and other dialogs.


%package -n %{pkgname}-tkinter
Summary: A GUI toolkit for Python
Requires: %{pkgname} = %{version}-%{release}

%unversioned_obsoletes_of_python3_X_if_main tkinter

%if 0%{?os2_version} && %{with main_python}
Provides:  tkinter = %{version}-%{release}
Obsoletes: tkinter < %{pybasever}
%endif

# The importable module "turtle" is here, so provide python3-turtle.
# (We don't provide python3-turtledemo, that's not too useful when imported.)
%py_provides %{pkgname}-turtle

%description -n %{pkgname}-tkinter
The Tkinter (Tk interface) library is a graphical user interface toolkit for
the Python programming language.


%package -n %{pkgname}-test
Summary: The self-test suite for the main python3 package
Requires: %{pkgname} = %{version}-%{release}
%if !0%{?os2_version}
Requires: %{pkgname}-libs%{?_isa} = %{version}-%{release}
%else
Requires: %{pkgname}-libs = %{version}-%{release}
%endif

%if %{with rpmwheels}
Requires: %{python_wheel_pkg_prefix}-setuptools-wheel
Requires: (%{python_wheel_pkg_prefix}-wheel-wheel if %{python_wheel_pkg_prefix}-setuptools-wheel < 71)
%else
Provides: bundled(python3dist(setuptools)) = %{setuptools_version}
%setuptools_bundled_provides
# License manually combined from Python + setuptools + wheel
License: Python-2.0.1 AND MIT AND Apache-2.0 AND (Apache-2.0 OR BSD-2-Clause)
%endif

%unversioned_obsoletes_of_python3_X_if_main test

%if 0%{?os2_version} && %{with main_python}
Provides:  python-test = %{version}-%{release}
Obsoletes: python-test < %{pybasever}
%endif

%description -n %{pkgname}-test
The self-test suite for the Python interpreter.

This is only useful to test Python itself. For testing general Python code,
you should use the unittest module from %{pkgname}-libs, or a library such as
%{pkgname}-pytest.


%if %{with debug_build}
%package -n %{pkgname}-debug
Summary: Debug version of the Python runtime
License: %{libs_license}

# The debug build is an all-in-one package version of the regular build, and
# shares the same .py/.pyc files and directories as the regular build. Hence
# we depend on all of the subpackages of the regular build:
Requires: %{pkgname}%{?_isa} = %{version}-%{release}
Requires: %{pkgname}-libs%{?_isa} = %{version}-%{release}
Requires: %{pkgname}-devel%{?_isa} = %{version}-%{release}
Requires: %{pkgname}-test%{?_isa} = %{version}-%{release}
Requires: %{pkgname}-tkinter%{?_isa} = %{version}-%{release}
Requires: %{pkgname}-idle%{?_isa} = %{version}-%{release}

%unversioned_obsoletes_of_python3_X_if_main debug

%if 0%{?os2_version} && %{with main_python}
Provides:  python-debug = %{version}-%{release}
Obsoletes: python-debug < %{pybasever}
%endif

%description -n %{pkgname}-debug
python3-debug provides a version of the Python runtime with numerous debugging
features enabled, aimed at advanced Python users such as developers of Python
extension modules.

This version uses more memory and will be slower than the regular Python build,
but is useful for tracking down reference-counting issues and other bugs.

The debug build shares installation directories with the standard Python
runtime. Python modules -- source (.py), bytecode (.pyc), and C-API extensions
(.cpython*.so) -- are compatible between this and the standard version
of Python.

The debug runtime additionally supports debug builds of C-API extensions
(with the "d" ABI flag) for debugging issues in those extensions.
%endif # with debug_build


%if %{with freethreading_build}
# This deliberately does not use the %%{pkgname}- prefix,
# we want to call this python3.X-threading even when built as a main Python.
# At least until the PEP 703 build remains provisional.
%package -n python%{pybasever}-freethreading
Summary: Free Threading (PEP 703) version of the Python runtime

%if %{with rpmwheels}
Requires: %{python_wheel_pkg_prefix}-pip-wheel >= 23.1.2
Requires: %{python_wheel_pkg_prefix}-setuptools-wheel
Requires: (%{python_wheel_pkg_prefix}-wheel-wheel if %{python_wheel_pkg_prefix}-setuptools-wheel < 71)
License: %{libs_license}
%else
Provides: bundled(python3dist(pip)) = %{pip_version}
%pip_bundled_provides
Provides: bundled(python3dist(setuptools)) = %{setuptools_version}
%setuptools_bundled_provides
# License combined from Python libs + pip + setuptools
License: %{libs_license} AND Apache-2.0 AND ISC AND LGPL-2.1-only AND MPL-2.0 AND (Apache-2.0 OR BSD-2-Clause)
%endif

# This package doesn't depend on python3-libs, so we need to explicitly
# define the same Provides and Requires.
# See the comments in the definition of -libs subpackage for detailed explanations
Provides: bundled(libb2) = 0.98.1
Provides: bundled(mimalloc) = 2.12
Requires: tzdata
Requires: expat >= %{expat_version}

%description -n python%{pybasever}-freethreading
The provisional Free Threading (PEP 703) build of Python.

CPython’s global interpreter lock (“GIL”) prevents multiple threads from
executing Python code at the same time. The GIL is an obstacle to using
multi-core CPUs from Python efficiently.

This build of Python is built with the --disable-gil option.
It lets the interpreter run Python code without the global interpreter lock
and with the necessary changes needed to make the interpreter thread-safe.
%endif # with freethreading_build


%if %{with freethreading_build} && %{with debug_build}
%package -n python%{pybasever}-freethreading-debug
Summary: Free Threading (PEP 703) version of the Python runtime (debug build)
License: %{libs_license}

# This uses the pure Python modules from the freethreading package
Requires: python%{pybasever}-freethreading%{?_isa} = %{version}-%{release}

%description -n python%{pybasever}-freethreading-debug
The provisional Free Threading (PEP 703) build of Python. Debug build.

CPython’s global interpreter lock (“GIL”) prevents multiple threads from
executing Python code at the same time. The GIL is an obstacle to using
multi-core CPUs from Python efficiently.

This build of Python is built with the --disable-gil option.
It lets the interpreter run Python code without the global interpreter lock
and with the necessary changes needed to make the interpreter thread-safe.

This package provides a version of the Python runtime with numerous debugging
features enabled, aimed at advanced Python users such as developers of Python
extension modules.
%endif # with freethreading_build && debug_build

%if 0%{?os2_version}
%debug_package
%endif

# ======================================================
# The prep phase of the build:
# ======================================================

%prep
%if !0%{?os2_version}
%gpgverify -k2 -s1 -d0
%autosetup -S git_am -n Python-%{upstream_version}
%else
%scm_setup
%endif

# Verify the second level of bundled provides is up to date
# Arguably this should be done in %%check, but %%prep has a faster feedback loop
# setuptools.whl does not contain the vendored.txt files
%if !0%{?os2_version}
if [ -f %{_rpmconfigdir}/pythonbundles.py ]; then
  %{_rpmconfigdir}/pythonbundles.py <(unzip -p Lib/ensurepip/_bundled/pip-*.whl pip/_vendor/vendor.txt) --compare-with '%pip_bundled_provides'
  %{_rpmconfigdir}/pythonbundles.py <(unzip -l Lib/test/wheeldata/setuptools-*.whl | grep -E '_vendor/.+dist-info/RECORD' | sed -E 's@^.*/([^-]+)-([^-]+)\.dist-info/.*$@\1==\2@') --compare-with '%setuptools_bundled_provides'
fi
%endif

%if %{with rpmwheels}
rm Lib/ensurepip/_bundled/pip-%{pip_version}-py3-none-any.whl
rm Lib/test/wheeldata/setuptools-%{setuptools_version}-py3-none-any.whl
%endif

# check if there were any changes to Doc/license.rst
# if so, a review of %%libs_license and %%license_file_hash is needed
found_hash=$(sha256sum Doc/license.rst | cut -f1 -d" ")
if [ "$found_hash" != %{license_file_hash} ]; then
    echo "File hash mismatch: review Doc/license.rst for changes"
    exit 1
fi

# Remove all exe files to ensure we are not shipping prebuilt binaries
# note that those are only used to create Microsoft Windows installers
# and that functionality is broken on Linux anyway
find -name '*.exe' -print -delete

# Remove bundled libraries to ensure that we're using the system copy.
rm -r Modules/expat
rm -r Modules/_decimal/libmpdec

# Remove files that should be generated by the build
# (This is after patching, so that we can use patches directly from upstream)
%if !0%{?os2_version}
rm configure pyconfig.h.in
%endif

# Lower the minimal required version of autoconf to enable build for EPEL 9
sed -i "s/AC_PREREQ(\[2\.71\])/AC_PREREQ([2.69])/" configure.ac

# ======================================================
# Configuring and building the code:
# ======================================================

%build

# The build process embeds version info extracted from the Git repository
# into the Py_GetBuildInfo and sys.version strings.
# Our Git repository is artificial, so we don't want that.
# Tell configure to not use git.
export HAS_GIT=not-found

# Regenerate the configure script and pyconfig.h.in
%if !0%{?os2_version}
autoconf
autoheader
%else
autoreconf -fvi
%endif

# Remember the current directory (which has sources and the configure script),
# so we can refer to it after we "cd" elsewhere.
topdir=$(pwd)

# Get proper option names from bconds
%if %{with computed_gotos}
%global computed_gotos_flag yes
%else
%global computed_gotos_flag no
%endif

%if %{with optimizations}
%global optimizations_flag "--enable-optimizations"
%else
%global optimizations_flag "--disable-optimizations"
%endif

# Set common compiler/linker flags
# We utilize the %%extension_...flags macros here so users building C/C++
# extensions with our python won't get all the compiler/linker flags used
# in Fedora RPMs.
# Standard library built here will still use the %%build_...flags,
# Fedora packages utilizing %%py3_build will use them as well
# https://fedoraproject.org/wiki/Changes/Python_Extension_Flags
# https://fedoraproject.org/wiki/Changes/Python_Extension_Flags_Reduction
%if !0%{?os2_version}
export CFLAGS="%{extension_cflags}"
export CFLAGS_NODIST="%{build_cflags} -D_GNU_SOURCE -fPIC -fwrapv"
export CXXFLAGS="%{extension_cxxflags}"
export CPPFLAGS="$(pkg-config --cflags-only-I libffi)"
export OPT="%{extension_cflags}"
export LINKCC="gcc"
export CFLAGS="$CFLAGS $(pkg-config --cflags openssl)"
export LDFLAGS="%{extension_ldflags} $(pkg-config --libs-only-L openssl)"
export LDFLAGS_NODIST="%{build_ldflags} -g $(pkg-config --libs-only-L openssl)"
%else
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"
export LIBS="-lssl -lcrypto -lintl -lcx"
export VENDOR="%{vendor}"
export BOOTSTRAP_TIME="`LANG=C date +'%%d %%b %%Y %%H:%%M:%%S'`"
%endif

# We can build several different configurations of Python: regular and debug.
# Define a common function that does one build:
BuildPython() {
  ConfName=$1
  ExtraConfigArgs=$2
  MoreCFlags=$3

  # Each build is done in its own directory
  ConfDir=build/$ConfName
  echo STARTING: BUILD OF PYTHON FOR CONFIGURATION: $ConfName
  mkdir -p $ConfDir
%if !0%{?os2_version}
  pushd $ConfDir
%else
  cd $ConfDir
%endif

  # Normally, %%configure looks for the "configure" script in the current
  # directory.
  # Since we changed directories, we need to tell %%configure where to look.
  %global _configure $topdir/configure

  # A workaround for https://bugs.python.org/issue39761
  export DFLAGS=" "

%configure \
  --with-platlibdir=%{_lib} \
%if !0%{?os2_version}
  --enable-ipv6 \
%else
  --enable-ipv6=no \
  --with-mimalloc=no \
%endif
  --enable-shared \
  --with-computed-gotos=%{computed_gotos_flag} \
  --with-dbmliborder=gdbm:ndbm:bdb \
  --with-system-expat \
  --with-system-libmpdec \
  --enable-loadable-sqlite-extensions \
%if !0%{?os2_version}
  --with-dtrace \
  --with-lto \
%endif
  --with-ssl-default-suites=openssl \
  --without-static-libpython \
%if %{with rpmwheels}
  --with-wheel-pkg-dir=%{python_wheel_dir} \
%endif
%ifarch %{valgrind_arches}
  --with-valgrind \
%endif
  $ExtraConfigArgs \
  %{nil}

%if 0%{?fedora} && 0%{?fedora} < 42
  # Statically compile the _datetime module to mitigate:
  #  Segfault when updating from 3.13.0 to 3.13.1 while Python is running
  #  https://bugzilla.redhat.com/2333852
  # Note that this is an incomplete workaround for the case we know about,
  # we'd like to see the cause fixed properly in Python 3.14 upstream:
  #  https://github.com/python/cpython/issues/128341
  # This is only carried on Fedoras released before Python 3.13.1.
  echo -e '*static*\n_datetime _datetimemodule.c' > Modules/Setup.local
%endif

%global flags_override EXTRA_CFLAGS="$MoreCFlags" CFLAGS_NODIST="$CFLAGS_NODIST $MoreCFlags"

%if %{without bootstrap}
  # Regenerate generated files (needs python3)
  %make_build %{flags_override} regen-all PYTHON_FOR_REGEN="python%{pybasever}"
%endif

  # Invoke the build
  %make_build %{flags_override}

%if !0%{?os2_version}
  popd
%else
  cd $topdir
%endif
  echo FINISHED: BUILD OF PYTHON FOR CONFIGURATION: $ConfName
}

# Call the above to build each configuration.

%if %{with debug_build}
# The debug build is compiled with the lowest level of optimizations as to not optimize
# out frames. We also suppress the warnings as the default distro value of the FORTIFY_SOURCE
# option produces too many warnings when compiling at the O0 optimization level.
# See also: https://bugzilla.redhat.com/show_bug.cgi?id=1818857
BuildPython debug \
  "--without-ensurepip --with-pydebug %{?jit_flag}" \
  "%{optflags_debug}"
%endif # with debug_build

BuildPython optimized \
  "--without-ensurepip %{?jit_flag} %{optimizations_flag}" \
  "%{optflags_optimized}"

%if %{with freethreading_build} && %{with debug_build}
BuildPython freethreading-debug \
  "--without-ensurepip --with-pydebug --disable-gil" \
  "%{optflags_debug}"
%endif # with freethreading_build && debug_build

%if %{with freethreading_build}
BuildPython freethreading \
  "--without-ensurepip %{optimizations_flag} --disable-gil" \
  "%{optflags_optimized}"
%endif # with freethreading_build

# ======================================================
# Installing the built code:
# ======================================================

%install

# As in %%build, remember the current directory
topdir=$(pwd)

# We install a collection of hooks for gdb that make it easier to debug
# executables linked against libpython3* (such as /usr/bin/python3 itself)
#
# These hooks are implemented in Python itself (though they are for the version
# of python that gdb is linked with)
#
# gdb-archer looks for them in the same path as the ELF file or its .debug
# file, with a -gdb.py suffix.
# We put them next to the debug file, because ldconfig would complain if
# it found non-library files directly in /usr/lib/
# (see https://bugzilla.redhat.com/show_bug.cgi?id=562980)
#
# We'll put these files in the debuginfo package by installing them to e.g.:
#  /usr/lib/debug/usr/lib/libpython3.2.so.1.0.debug-gdb.py
# (note that the debug path is /usr/lib/debug for both 32/64 bit)
#
# See https://fedoraproject.org/wiki/Features/EasierPythonDebugging for more
# information

%if !0%{?os2_version}
DirHoldingGdbPy=%{_usr}/lib/debug/%{_libdir}
mkdir -p %{buildroot}$DirHoldingGdbPy
%endif

# When the actual %%{dynload_dir} exists (it does when python3.X is installed for regen-all)
# %%{buildroot}%%{dynload_dir} is not created by make install and the extension modules are missing
# Reported upstream as https://github.com/python/cpython/issues/98782
# A workaround is to create the directory before running make install
mkdir -p %{buildroot}%{dynload_dir}

# Multilib support for pyconfig.h
# 32- and 64-bit versions of pyconfig.h are different. For multilib support
# (making it possible to install 32- and 64-bit versions simultaneously),
# we need to install them under different filenames, and to make the common
# "pyconfig.h" include the right file based on architecture.
# See https://bugzilla.redhat.com/show_bug.cgi?id=192747
# Filanames are defined here:
%if !0%{?os2_version}
%global _pyconfig32_h pyconfig-32.h
%global _pyconfig64_h pyconfig-64.h
%global _pyconfig_h pyconfig-%{__isa_bits}.h
%else
%global _pyconfig_h pyconfig.h
%endif

# Use a common function to do an install for all our configurations:
InstallPython() {

  ConfName=$1
  PyInstSoName=$2
  MoreCFlags=$3
  LDVersion=$4

  # Switch to the directory with this configuration's built files
  ConfDir=build/$ConfName
  echo STARTING: INSTALL OF PYTHON FOR CONFIGURATION: $ConfName
  mkdir -p $ConfDir
%if !0%{?os2_version}
  pushd $ConfDir
%else
  cd $ConfDir
%endif

  %make_install EXTRA_CFLAGS="$MoreCFlags"

%if !0%{?os2_version}
  popd
%else
  cd $topdir
%endif

%if !0%{?os2_version}
  # See comment on $DirHoldingGdbPy above
  PathOfGdbPy=$DirHoldingGdbPy/$PyInstSoName-%{version}-%{release}.%{_arch}.debug-gdb.py
  cp Tools/gdb/libpython.py %{buildroot}$PathOfGdbPy

  # Rename the -devel script that differs on different arches to arch specific name
  mv %{buildroot}%{_bindir}/python${LDVersion}-{,`uname -m`-}config
  echo -e '#!/bin/sh\nexec %{_bindir}/python'${LDVersion}'-`uname -m`-config "$@"' > \
    %{buildroot}%{_bindir}/python${LDVersion}-config
    chmod +x %{buildroot}%{_bindir}/python${LDVersion}-config

  # Make python3-devel multilib-ready
  mv %{buildroot}%{_includedir}/python${LDVersion}/pyconfig.h \
     %{buildroot}%{_includedir}/python${LDVersion}/%{_pyconfig_h}
  cat > %{buildroot}%{_includedir}/python${LDVersion}/pyconfig.h << EOF
#include <bits/wordsize.h>

#if __WORDSIZE == 32
#include "%{_pyconfig32_h}"
#elif __WORDSIZE == 64
#include "%{_pyconfig64_h}"
#else
#error "Unknown word size"
#endif
EOF
%endif

  echo FINISHED: INSTALL OF PYTHON FOR CONFIGURATION: $ConfName
}

# Install the "freethreading" and "debug" builds first; any common files will be overridden with
# later builds
%if %{with freethreading_build} && %{with debug_build}
# Now the freethreading debug build:
InstallPython freethreading-debug \
  %{py_INSTSONAME_freethreading_debug} \
  "%{optflags_debug}" \
  %{LDVERSION_freethreading_debug}
%endif # with freethreading_build && debug_build

%if %{with debug_build}
InstallPython debug \
  %{py_INSTSONAME_debug} \
  "%{optflags_debug}" \
  %{LDVERSION_debug}
%endif # with debug_build

%if %{with freethreading_build}
# Now the freethreading optimized build:
InstallPython freethreading \
  %{py_INSTSONAME_freethreading} \
  "%{optflags_optimized}" \
  %{LDVERSION_freethreading}
%endif # with freethreading_build

# Now the optimized build:
InstallPython optimized \
  %{py_INSTSONAME_optimized} \
  "%{optflags_optimized}" \
  %{LDVERSION_optimized}

# Install directories for additional packages
install -d -m 0755 %{buildroot}%{pylibdir}/site-packages/__pycache__
%if "%{_lib}" == "lib64"
# The 64-bit version needs to create "site-packages" in /usr/lib/ (for
# pure-Python modules) as well as in /usr/lib64/ (for packages with extension
# modules).
# Note that rpmlint will complain about hardcoded library path;
# this is intentional.
install -d -m 0755 %{buildroot}%{_prefix}/lib/python%{pybasever}/site-packages/__pycache__
%if %{with freethreading_build}
install -d -m 0755 %{buildroot}%{_prefix}/lib/python%{pybasever}%{ABIFLAGS_freethreading}/site-packages/__pycache__
%endif # with freethreading_build
%endif

%if %{with main_python}
# add idle3 to menu
%if !0%{?os2_version}
install -D -m 0644 Lib/idlelib/Icons/idle_16.png %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/idle3.png
install -D -m 0644 Lib/idlelib/Icons/idle_32.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/idle3.png
install -D -m 0644 Lib/idlelib/Icons/idle_48.png %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/idle3.png
install -D -m 0644 Lib/idlelib/Icons/idle_256.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/idle3.png
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{SOURCE10}
%endif

# Install and validate appdata file
%if !0%{?os2_version}
mkdir -p %{buildroot}%{_metainfodir}
cp -a %{SOURCE11} %{buildroot}%{_metainfodir}
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/idle3.appdata.xml
%endif
%endif

# Make sure sysconfig looks at the right pyconfig-32.h/pyconfig-64.h file instead of pyconfig.h
# See https://bugzilla.redhat.com/show_bug.cgi?id=201434
# and https://bugzilla.redhat.com/show_bug.cgi?id=653058
sed -i -e "s/'pyconfig.h'/'%{_pyconfig_h}'/" \
  %{buildroot}%{pylibdir}/sysconfig/*.py

# Install i18n tools to bindir
# They are also in python2, so we version them
# https://bugzilla.redhat.com/show_bug.cgi?id=1571474
for tool in pygettext msgfmt; do
  cp -p Tools/i18n/${tool}.py %{buildroot}%{_bindir}/${tool}%{pybasever}.py
  ln -s ${tool}%{pybasever}.py %{buildroot}%{_bindir}/${tool}3.py
done

# Switch all shebangs to refer to the specific Python version.
# This currently only covers files matching ^[a-zA-Z0-9_]+\.py$,
# so handle files named using other naming scheme separately.
%if !0%{?os2_version}
LD_LIBRARY_PATH=./build/optimized ./build/optimized/python \
%else
BEGINLIBPATH=./build/optimized ./build/optimized/python \
%endif
  %{_rpmconfigdir}/redhat/pathfix.py \
  -i "%{_bindir}/python%{pybasever}" -pn \
  %{buildroot} \
  %{buildroot}%{_bindir}/*%{pybasever}.py \
%if !0%{?os2_version}
  %{buildroot}$DirHoldingGdbPy/*.py
%endif

# Remove shebang lines from .py files that aren't executable, and
# remove executability from .py files that don't have a shebang line:
find %{buildroot} -name \*.py \
  \( \( \! -perm /u+x,g+x,o+x -exec sed -e '/^#!/Q 0' -e 'Q 1' {} \; \
  -print -exec sed -i '1d' {} \; \) -o \( \
  -perm /u+x,g+x,o+x ! -exec grep -m 1 -q '^#!' {} \; \
  -exec chmod a-x {} \; \) \)

# Get rid of DOS batch files:
find %{buildroot} -name \*.bat -exec rm {} \;

# Get rid of backup files:
find %{buildroot}/ -name "*~" -exec rm -f {} \;
find . -name "*~" -exec rm -f {} \;

# Do bytecompilation with the newly installed interpreter.
# This is similar to the script in macros.pybytecompile
# compile *.pyc
# Python CMD line options:
# -s - don't add user site directory to sys.path
# -B - don't write .pyc files on import
# Clamp the source mtime first, see https://fedoraproject.org/wiki/Changes/ReproducibleBuildsClampMtimes
# The clamp_source_mtime module is only guaranteed to exist on Fedoras that enabled this option:
%if 0%{?clamp_mtime_to_source_date_epoch}
LD_LIBRARY_PATH="%{buildroot}%{dynload_dir}/:%{buildroot}%{_libdir}" \
PYTHONPATH="%{_rpmconfigdir}/redhat" \
%{buildroot}%{_bindir}/python%{pybasever} -s -B -m clamp_source_mtime %{buildroot}%{pylibdir} %{?with_freethreading_build:%{buildroot}%{pylibdir_freethreading}}
%endif
# compileall CMD line options:
# -f - force rebuild even if timestamps are up to date
# -o - optimization levels to run compilation with
# -s - part of path to left-strip from path to source file (buildroot)
# -p - path to add as prefix to path to source file (/ to make it absolute)
# --hardlink-dupes - hardlink different optimization level pycs together if identical (saves space)
# --invalidation-mode - we prefer the timestamp invalidation mode for performance reasons
# -x - skip test modules with SyntaxErrors (taken from the Makefile)
%if !0%{?os2_version}
LD_LIBRARY_PATH="%{buildroot}%{dynload_dir}/:%{buildroot}%{_libdir}" \
%else
BEGINLIBPATH="%{buildroot}%{dynload_dir}/;%{buildroot}%{_libdir}" \
%endif
%{buildroot}%{_bindir}/python%{pybasever} -s -B -m compileall \
-f %{_smp_mflags} -o 0 -o 1 -o 2 -s %{buildroot} -p / %{buildroot} --hardlink-dupes --invalidation-mode=timestamp \
-x 'bad_coding|badsyntax|site-packages'

# Turn this BRP off, it is done by compileall2 --hardlink-dupes above
%global __brp_python_hardlink %{nil}

# Since we have *.py files in bindir, this is created, but we don't want it
rm -rf %{buildroot}%{_bindir}/__pycache__

# Fixup permissions for shared libraries from non-standard 555 to standard 755:
find %{buildroot} -perm 555 -exec chmod 755 {} \;

# Create "/usr/bin/python3-debug", a symlink to the python3 debug binary, to
# avoid the user having to know the precise version and ABI flags.
# See e.g. https://bugzilla.redhat.com/show_bug.cgi?id=676748
%if %{with debug_build} && %{with main_python}
ln -s \
  %{_bindir}/python%{LDVERSION_debug} \
  %{buildroot}%{_bindir}/python3-debug
%endif

%if %{without main_python}
# Remove stuff that would conflict with python3 package
rm %{buildroot}%{_bindir}/python3
rm %{buildroot}%{_bindir}/pydoc3
rm %{buildroot}%{_bindir}/pygettext3.py
rm %{buildroot}%{_bindir}/msgfmt3.py
rm %{buildroot}%{_bindir}/idle3
rm %{buildroot}%{_bindir}/python3-*
rm %{buildroot}%{_libdir}/libpython3.so
rm %{buildroot}%{_mandir}/man1/python3.1
rm %{buildroot}%{_libdir}/pkgconfig/python3.pc
rm %{buildroot}%{_libdir}/pkgconfig/python3-embed.pc
%else
# Link the unversioned stuff
# https://fedoraproject.org/wiki/Changes/Python_means_Python3
ln -s ./python3 %{buildroot}%{_bindir}/python
ln -s ./pydoc3 %{buildroot}%{_bindir}/pydoc
ln -s ./pygettext3.py %{buildroot}%{_bindir}/pygettext.py
ln -s ./msgfmt3.py %{buildroot}%{_bindir}/msgfmt.py
ln -s ./idle3 %{buildroot}%{_bindir}/idle
ln -s ./python3-config %{buildroot}%{_bindir}/python-config
ln -s ./python3.1 %{buildroot}%{_mandir}/man1/python.1
ln -s ./python3.pc %{buildroot}%{_libdir}/pkgconfig/python.pc
%if %{with debug_build}
ln -s ./python3-debug %{buildroot}%{_bindir}/python-debug
%endif
%if 0%{?os2_version}
cp -p %{buildroot}%{_bindir}/python%{pybasever}.exe %{buildroot}%{_bindir}/python.exe
%endif
%endif

%if 0%{?os2_version}
ln -s ./python%{pybasever}.exe %{buildroot}%{_bindir}/python%{pybasever}
%endif

# Remove large, autogenerated sources and keep only the non-optimized pycache
%if !0%{?os2_version}
for file in %{buildroot}%{pylibdir}/pydoc_data/topics.py $(grep --include='*.py' -lr %{buildroot}%{pylibdir}/encodings -e 'Python Character Mapping Codec .* from .* with gencodec.py'); do
    directory=$(dirname ${file})
    module=$(basename ${file%%.py})
    mv ${directory}/{__pycache__/${module}.cpython-%{pyshortver}.pyc,${module}.pyc}
    rm ${directory}/{__pycache__/${module}.cpython-%{pyshortver}.opt-?.pyc,${module}.py}
done
%endif

%if %{without rpmwheels}
# Inject SBOM into the installed wheels (if the macro is available)
%{?python_wheel_inject_sbom:%python_wheel_inject_sbom %{buildroot}%{pylibdir}/ensurepip/_bundled/*.whl}
%endif

# ======================================================
# Checks for packaging issues
# ======================================================

%check

# first of all, check timestamps of bytecode files
%if !0%{?os2_version}
find %{buildroot} -type f -a -name "*.py" -print0 | \
    LD_LIBRARY_PATH="%{buildroot}%{dynload_dir}/:%{buildroot}%{_libdir}" \
    PYTHONPATH="%{buildroot}%{_libdir}/python%{pybasever} %{buildroot}%{_libdir}/python%{pybasever}/site-packages" \
    xargs -0 %{buildroot}%{_bindir}/python%{pybasever} %{SOURCE8}
%endif

# Ensure that the curses module was linked against libncursesw.so, rather than
# libncurses.so
# See https://bugzilla.redhat.com/show_bug.cgi?id=539917
%if !0%{?os2_version}
ldd %{buildroot}/%{dynload_dir}/_curses*.so \
    | grep curses \
    | grep libncurses.so && (echo "_curses.so linked against libncurses.so" ; exit 1)
%endif

# Ensure that the debug modules are linked against the debug libpython, and
# likewise for the optimized modules and libpython:
%if !0%{?os2_version}
for Module in %{buildroot}/%{dynload_dir}/*.so ; do
    case $Module in
    *.%{SOABI_debug})
        ldd $Module | grep %{py_INSTSONAME_optimized} &&
            (echo Debug module $Module linked against optimized %{py_INSTSONAME_optimized} ; exit 1)

        ;;
    *.%{SOABI_optimized})
        ldd $Module | grep %{py_INSTSONAME_debug} &&
            (echo Optimized module $Module linked against debug %{py_INSTSONAME_debug} ; exit 1)
        ;;
    esac
done
%endif


# ======================================================
# Running the upstream test suite
# ======================================================

topdir=$(pwd)
CheckPython() {
  ConfName=$1
  ConfDir=$(pwd)/build/$ConfName

  echo STARTING: CHECKING OF PYTHON FOR CONFIGURATION: $ConfName

  # Note that we're running the tests using the version of the code in the
  # builddir, not in the buildroot.

  # Show some info, helpful for debugging test failures
  LD_LIBRARY_PATH=$ConfDir $ConfDir/python -m test.pythoninfo

  # Run the upstream test suite
  # --timeout=2700: kill test running for longer than 45 minutes
  # test_freeze_simple_script is skipped, because it fails without bundled libs.
  #  the freeze tool is only usable from the source checkout anyway,
  #  we don't ship it in the RPM package.
  # test_check_probes is failing since it was introduced in 3.12.0rc1,
  # the test is skipped until it is fixed in upstream.
  # see: https://github.com/python/cpython/issues/104280#issuecomment-1669249980
  # test_signal is skipped due to https://github.com/python/cpython/issues/118989
  # test.test_concurrent_futures.test_deadlock tends to time out on s390x and ppc64le in
  # freethreading{,-debug} build, skipping it to shorten the build time
  # see: https://github.com/python/cpython/issues/121719
  LD_LIBRARY_PATH=$ConfDir $ConfDir/python -m test.regrtest \
    -wW --slowest %{_smp_mflags} \
    %ifarch riscv64
    --timeout=8100 \
    %else
    --timeout=2700 \
    %endif
    -i test_freeze_simple_script \
    -i test_check_probes \
    %ifarch %{mips64}
    -x test_ctypes \
    %endif
    %ifarch s390x ppc64le
    -x test_signal \
    -i test_deadlock \
    %endif

  echo FINISHED: CHECKING OF PYTHON FOR CONFIGURATION: $ConfName

}

%if %{with tests}

# Check each of the configurations:
%if %{with debug_build}
CheckPython debug
%endif # with debug_build
CheckPython optimized
%if %{with freethreading_build} && %{with debug_build}
CheckPython freethreading-debug
%endif # with freethreading_build && debug_build
%if %{with freethreading_build}
CheckPython freethreading
%endif # with freethreading_build

%endif # with tests


%files -n %{pkgname}
%doc README.rst

%if %{with main_python}
%{_bindir}/pydoc*
%{_bindir}/python3
%else
%{_bindir}/pydoc%{pybasever}
%endif

%{_bindir}/python%{pybasever}
%if !0%{?os2_version}
%{_bindir}/python%{LDVERSION_optimized}
%else
%{_bindir}/python%{pybasever}.exe
%endif
%{_mandir}/*/*3*


%if %{with main_python}
%files -n python-unversioned-command
%{_bindir}/python
%if 0%{?os2_version}
%{_bindir}/python.exe
%endif
%{_mandir}/*/python.1*
%endif

%files -n %{pkgname}-libs
%doc README.rst

%dir %{pylibdir}
%dir %{dynload_dir}

%license %{pylibdir}/LICENSE.txt

# Pure Python modules
# This is macronized for reuse in the -freethreading package
%define pure_python_modules() \
%{1}/*.py\
%dir %{1}/__pycache__/\
%{1}/__pycache__/*%{bytecode_suffixes}\
\
%{1}/_pyrepl/\
%{1}/asyncio/\
%{1}/collections/\
%{1}/concurrent/\
%{1}/ctypes/\
%{1}/curses/\
%{1}/dbm/\
%{1}/encodings/\
%{1}/html/\
%{1}/http/\
%{1}/importlib/\
%{1}/json/\
%{1}/logging/\
%{1}/multiprocessing/\
%{1}/pathlib/\
%{1}/pydoc_data/\
%{1}/re/\
%{1}/sqlite3/\
%{1}/sysconfig/\
%{1}/tomllib/\
%{1}/unittest/\
%{1}/urllib/\
%{1}/venv/\
%{1}/wsgiref/\
%{1}/xml/\
%{1}/xmlrpc/\
%{1}/zipfile/\
%{1}/zoneinfo/\
# Handle the email module in detail to mark architecture.rst as %%doc\
%dir %{1}/email/\
%dir %{1}/email/__pycache__/\
%{1}/email/*.py\
%{1}/email/__pycache__/*%{bytecode_suffixes}\
%{1}/email/mime/\
%doc %{1}/email/architecture.rst\
# Handle the ensurepip module in detail to not accidentally ship wheels\
%dir %{1}/ensurepip/\
%dir %{1}/ensurepip/__pycache__/\
%{1}/ensurepip/*.py\
%{1}/ensurepip/__pycache__/*%{bytecode_suffixes}\
%if %{with rpmwheels}\
%exclude %{1}/ensurepip/_bundled\
%else\
%dir %{1}/ensurepip/_bundled\
%{1}/ensurepip/_bundled/pip-%{pip_version}-py3-none-any.whl\
%endif

%pure_python_modules %{pylibdir}

# This will be in the tkinter package
%exclude %{pylibdir}/turtle.py
%exclude %{pylibdir}/__pycache__/turtle*%{bytecode_suffixes}

# This will be in the debug package
%if %{with debug_build}
%exclude %{pylibdir}/_sysconfigdata_%{ABIFLAGS_debug}_linux_%{platform_triplet}.py
%exclude %{pylibdir}/__pycache__/_sysconfigdata_%{ABIFLAGS_debug}_linux_%{platform_triplet}%{bytecode_suffixes}
%endif

# Extension modules
# This is macronized for reuse in the -debug package
%define extension_modules() \
%if !0%{?os2_version}\
%{1}/_asyncio.%{2}.so\
%{1}/_bisect.%{2}.so\
%{1}/_blake2.%{2}.so\
%{1}/_bz2.%{2}.so\
%{1}/_codecs_cn.%{2}.so\
%{1}/_codecs_hk.%{2}.so\
%{1}/_codecs_iso2022.%{2}.so\
%{1}/_codecs_jp.%{2}.so\
%{1}/_codecs_kr.%{2}.so\
%{1}/_codecs_tw.%{2}.so\
%{1}/_contextvars.%{2}.so\
%{1}/_csv.%{2}.so\
%{1}/_ctypes.%{2}.so\
%{1}/_curses.%{2}.so\
%{1}/_curses_panel.%{2}.so\
%if !(0%{?fedora} && 0%{?fedora} < 42)\
%{1}/_datetime.%{2}.so\
%endif\
%{1}/_dbm.%{2}.so\
%{1}/_gdbm.%{2}.so\
%{1}/_decimal.%{2}.so\
%{1}/_elementtree.%{2}.so\
%{1}/_hashlib.%{2}.so\
%{1}/_heapq.%{2}.so\
%{1}/_interpchannels.%{2}.so\
%{1}/_interpqueues.%{2}.so\
%{1}/_interpreters.%{2}.so\
%{1}/_json.%{2}.so\
%{1}/_lsprof.%{2}.so\
%{1}/_lzma.%{2}.so\
%{1}/_md5.%{2}.so\
%{1}/_multibytecodec.%{2}.so\
%{1}/_multiprocessing.%{2}.so\
%{1}/_opcode.%{2}.so\
%{1}/_pickle.%{2}.so\
%{1}/_posixshmem.%{2}.so\
%{1}/_posixsubprocess.%{2}.so\
%{1}/_queue.%{2}.so\
%{1}/_random.%{2}.so\
%{1}/_sha1.%{2}.so\
%{1}/_sha2.%{2}.so\
%{1}/_sha3.%{2}.so\
%{1}/_socket.%{2}.so\
%{1}/_sqlite3.%{2}.so\
%{1}/_ssl.%{2}.so\
%{1}/_statistics.%{2}.so\
%{1}/_struct.%{2}.so\
%{1}/_uuid.%{2}.so\
%{1}/_zoneinfo.%{2}.so\
%{1}/array.%{2}.so\
%{1}/binascii.%{2}.so\
%{1}/cmath.%{2}.so\
%{1}/fcntl.%{2}.so\
%{1}/grp.%{2}.so\
%{1}/math.%{2}.so\
%{1}/mmap.%{2}.so\
%{1}/pyexpat.%{2}.so\
%{1}/readline.%{2}.so\
%{1}/resource.%{2}.so\
%{1}/select.%{2}.so\
%{1}/syslog.%{2}.so\
%{1}/termios.%{2}.so\
%{1}/unicodedata.%{2}.so\
%{1}/zlib.%{2}.so\
%else\
%{1}/_asyncio.pyd\
%{1}/_bisect.pyd\
%{1}/_blake2.pyd\
%{1}/_bz2.pyd\
%{1}/_codecs_cn.pyd\
%{1}/_cod69f0.pyd\
%{1}/_codecs_hk.pyd\
%{1}/_codab2b.pyd\
%{1}/_codecs_iso2022.pyd\
%{1}/_cod5dc5.pyd\
%{1}/_codecs_jp.pyd\
%{1}/_codb1e5.pyd\
%{1}/_codecs_kr.pyd\
%{1}/_codd6c1.pyd\
%{1}/_codecs_tw.pyd\
%{1}/_codd595.pyd\
%{1}/_contextvars.pyd\
%{1}/_cond831.pyd\
%{1}/_csv.pyd\
%{1}/_ctypes.pyd\
%{1}/_curses.pyd\
%{1}/_curses_panel.pyd\
%{1}/_cur1cd0.pyd\
%{1}/_datetime.pyd\
%{1}/_dat0da0.pyd\
%{1}/_decimal.pyd\
%{1}/_elementtree.pyd\
%{1}/_elecf87.pyd\
%{1}/_hashlib.pyd\
%{1}/_heapq.pyd\
%{1}/_interpchannels.pyd\
%{1}/_int818c.pyd\
%{1}/_interpqueues.pyd\
%{1}/_inte010.pyd\
%{1}/_interpreters.pyd\
%{1}/_int46bc.pyd\
%{1}/_json.pyd\
%{1}/_lsprof.pyd\
%{1}/_lzma.pyd\
%{1}/_md5.pyd\
%{1}/_multibytecodec.pyd\
%{1}/_mulc0dc.pyd\
%{1}/_opcode.pyd\
%{1}/_pickle.pyd\
%{1}/_posixsubprocess.pyd\
%{1}/_pos58b3.pyd\
%{1}/_queue.pyd\
%{1}/_random.pyd\
%{1}/_sha1.pyd\
%{1}/_sha2.pyd\
%{1}/_sha3.pyd\
%{1}/_socket.pyd\
%{1}/_sqlite3.pyd\
%{1}/_ssl.pyd\
%{1}/_statistics.pyd\
%{1}/_sta0e5d.pyd\
%{1}/_struct.pyd\
%{1}/_zoneinfo.pyd\
%{1}/_zondbf1.pyd\
%{1}/array.pyd\
%{1}/binascii.pyd\
%{1}/cmath.pyd\
%{1}/fcntl.pyd\
%{1}/grp.pyd\
%{1}/math.pyd\
%{1}/mmap.pyd\
%{1}/pyexpat.pyd\
%{1}/readline.pyd\
%{1}/resource.pyd\
%{1}/select.pyd\
%{1}/syslog.pyd\
%{1}/termios.pyd\
%{1}/unicodedata.pyd\
%{1}/unic309a.pyd\
%{1}/zlib.pyd\
%endif\

%extension_modules %{dynload_dir} %{SOABI_optimized}

%dir %{pylibdir}/site-packages/
%dir %{pylibdir}/site-packages/__pycache__/
%{pylibdir}/site-packages/README.txt

%if "%{_lib}" == "lib64"
%attr(0755,root,root) %dir %{_prefix}/lib/python%{pybasever}/
%attr(0755,root,root) %dir %{_prefix}/lib/python%{pybasever}/site-packages/
%attr(0755,root,root) %dir %{_prefix}/lib/python%{pybasever}/site-packages/__pycache__/
%endif

# "Makefile" and the config-32/64.h file are needed by
# sysconfig.get_config_vars(), so we include them in the core
# package, along with their parent directories (bug 531901):
%if !0%{?os2_version}
%dir %{pylibdir}/config-%{LDVERSION_optimized}-%{platform_triplet}/
%{pylibdir}/config-%{LDVERSION_optimized}-%{platform_triplet}/Makefile
%else
%dir %{pylibdir}/config-%{LDVERSION_optimized}/
%{pylibdir}/config-%{LDVERSION_optimized}/Makefile
%endif
%dir %{_includedir}/python%{LDVERSION_optimized}/
%{_includedir}/python%{LDVERSION_optimized}/%{_pyconfig_h}

# Finally, libpython
%if !0%{?os2_version}
%{_libdir}/%{py_INSTSONAME_optimized}
%else
%{_libdir}/pytho%{pyshortver}.dll
%endif
%if %{with main_python}
%if !0%{?os2_version}
%{_libdir}/libpython3.so
%endif
%endif


%files -n %{pkgname}-devel
%if !0%{?os2_version}
%{pylibdir}/config-%{LDVERSION_optimized}-%{platform_triplet}/*
%exclude %{pylibdir}/config-%{LDVERSION_optimized}-%{platform_triplet}/Makefile
%else
%{pylibdir}/config-%{LDVERSION_optimized}/*
%exclude %{pylibdir}/config-%{LDVERSION_optimized}/Makefile
%endif
%exclude %{_includedir}/python%{LDVERSION_optimized}/%{_pyconfig_h}
%{_includedir}/python%{LDVERSION_optimized}/*.h
%{_includedir}/python%{LDVERSION_optimized}/internal/
%{_includedir}/python%{LDVERSION_optimized}/cpython/
%doc Misc/README.valgrind Misc/valgrind-python.supp

%if %{with main_python}
%{_bindir}/python3-config
%{_bindir}/python-config
%{_libdir}/pkgconfig/python3.pc
%{_libdir}/pkgconfig/python.pc
%{_libdir}/pkgconfig/python3-embed.pc
%{_bindir}/pygettext3.py
%{_bindir}/pygettext.py
%{_bindir}/msgfmt3.py
%{_bindir}/msgfmt.py
%endif

%{_bindir}/pygettext%{pybasever}.py
%{_bindir}/msgfmt%{pybasever}.py

%{_bindir}/python%{pybasever}-config
%{_bindir}/python%{LDVERSION_optimized}-config
%if !0%{?os2_version}
%{_bindir}/python%{LDVERSION_optimized}-*-config
%{_libdir}/libpython%{LDVERSION_optimized}.so
%else
%{_libdir}/python%{LDVERSION_optimized}_dll.a
%endif
%{_libdir}/pkgconfig/python-%{LDVERSION_optimized}.pc
%{_libdir}/pkgconfig/python-%{LDVERSION_optimized}-embed.pc
%{_libdir}/pkgconfig/python-%{pybasever}.pc
%{_libdir}/pkgconfig/python-%{pybasever}-embed.pc


%files -n %{pkgname}-idle
%if %{with main_python}
%{_bindir}/idle*
%else
%{_bindir}/idle%{pybasever}
%endif

%{pylibdir}/idlelib

%if %{with main_python}
%if !0%{?os2_version}
%{_metainfodir}/idle3.appdata.xml
%{_datadir}/applications/idle3.desktop
%{_datadir}/icons/hicolor/*/apps/idle3.*
%endif
%endif

%files -n %{pkgname}-tkinter
%{pylibdir}/tkinter
%if !0%{?os2_version}
%{dynload_dir}/_tkinter.%{SOABI_optimized}.so
%endif
%{pylibdir}/turtle.py
%{pylibdir}/__pycache__/turtle*%{bytecode_suffixes}
%dir %{pylibdir}/turtledemo
%{pylibdir}/turtledemo/*.py
%{pylibdir}/turtledemo/*.cfg
%dir %{pylibdir}/turtledemo/__pycache__/
%{pylibdir}/turtledemo/__pycache__/*%{bytecode_suffixes}


%files -n %{pkgname}-test
%{pylibdir}/test/

# Pure Python modules
%{pylibdir}/__phello__/

# Extension modules
# This is macronized for reuse in the -debug package
%define extension_modules_test() \
%if !0%{?os2_version}\
%{1}/_ctypes_test.%{2}.so\
%{1}/_testbuffer.%{2}.so\
%{1}/_testcapi.%{2}.so\
%{1}/_testclinic.%{2}.so\
%{1}/_testclinic_limited.%{2}.so\
%{1}/_testexternalinspection.%{2}.so\
%{1}/_testimportmultiple.%{2}.so\
%{1}/_testinternalcapi.%{2}.so\
%{1}/_testlimitedcapi.%{2}.so\
%{1}/_testmultiphase.%{2}.so\
%{1}/_testsinglephase.%{2}.so\
%{1}/_xxtestfuzz.%{2}.so\
%{1}/xxlimited.%{2}.so\
%{1}/xxlimited_35.%{2}.so\
%{1}/xxsubtype.%{2}.so\
%else\
%{1}/_ctypes_test.pyd\
%{1}/_cty1454.pyd\
%{1}/_testbuffer.pyd\
%{1}/_tesa271.pyd\
%{1}/_testcapi.pyd\
%{1}/_tes71aa.pyd\
%{1}/_testclinic.pyd\
%{1}/_tesc3bb.pyd\
%{1}/_testclinic_limited.pyd\
%{1}/_tesb8f3.pyd\
%{1}/_testexternalinspection.pyd\
%{1}/_tes7f5d.pyd\
%{1}/_testimportmultiple.pyd\
%{1}/_tes88af.pyd\
%{1}/_testinternalcapi.pyd\
%{1}/_tes574d.pyd\
%{1}/_testlimitedcapi.pyd\
%{1}/_tes16e0.pyd\
%{1}/_testmultiphase.pyd\
%{1}/_tesff79.pyd\
%{1}/_testsinglephase.pyd\
%{1}/_tesca66.pyd\
%{1}/_xxtestfuzz.pyd\
%{1}/_xxt68a5.pyd\
%{1}/xxlimited.pyd\
%{1}/xxli76c5.pyd\
%{1}/xxlimited_35.pyd\
%{1}/xxli7f82.pyd\
%{1}/xxsubtype.pyd\
%{1}/xxsu0974.pyd\
%endif\

%extension_modules_test %{dynload_dir} %{SOABI_optimized}


# We don't bother splitting the debug build out into further subpackages:
# if you need it, you're debugging and you probably don't mind having it all.

# Hence the manifest is the combination of analogous files in the manifests of
# all of the other subpackages
%if %{with debug_build}
%files -n %{pkgname}-debug
%if %{with main_python}
%{_bindir}/python3-debug
%{_bindir}/python-debug
%endif

# Analog of the core subpackage's files:
%{_bindir}/python%{LDVERSION_debug}

# Analog to the -libs subpackage's files:
%{_libdir}/%{py_INSTSONAME_debug}

# Analog of the libs, test, and tkinter extension modules:
%extension_modules %{dynload_dir} %{SOABI_debug}
%extension_modules_test %{dynload_dir} %{SOABI_debug}
%{dynload_dir}/_tkinter.%{SOABI_debug}.so

# Analog of the -devel subpackage's files:
%{pylibdir}/config-%{LDVERSION_debug}-%{platform_triplet}/
%{_includedir}/python%{LDVERSION_debug}/
%{_bindir}/python%{LDVERSION_debug}-config
%{_bindir}/python%{LDVERSION_debug}-*-config
%{_libdir}/libpython%{LDVERSION_debug}.so
%{_libdir}/pkgconfig/python-%{LDVERSION_debug}.pc
%{_libdir}/pkgconfig/python-%{LDVERSION_debug}-embed.pc

%{pylibdir}/_sysconfigdata_%{ABIFLAGS_debug}_linux_%{platform_triplet}.py
%{pylibdir}/__pycache__/_sysconfigdata_%{ABIFLAGS_debug}_linux_%{platform_triplet}%{bytecode_suffixes}

%endif # with debug_build

%if %{with freethreading_build}
%files -n python%{pybasever}-freethreading
%dir %{pylibdir_freethreading}
%dir %{dynload_dir_freethreading}

%license %{pylibdir_freethreading}/LICENSE.txt
%doc %{pylibdir_freethreading}/site-packages/README.txt

# Pure Python modules
%pure_python_modules %{pylibdir_freethreading}

# Modules that we separate from python3-libs, but want to ship in -freethreading
%{pylibdir_freethreading}/__phello__/
%{pylibdir_freethreading}/idlelib/
%{pylibdir_freethreading}/test/
%{pylibdir_freethreading}/tkinter/
%{pylibdir_freethreading}/turtledemo/

# This will be in the -freethreading-debug package
%if %{with debug_build}
%exclude %{pylibdir_freethreading}/_sysconfigdata_%{ABIFLAGS_freethreading_debug}_linux_%{platform_triplet}.py
%exclude %{pylibdir_freethreading}/__pycache__/_sysconfigdata_%{ABIFLAGS_freethreading_debug}_linux_%{platform_triplet}%{bytecode_suffixes}
%endif

# Analog of the core subpackage's files:
%{_bindir}/python%{LDVERSION_freethreading}

# Analog to the -libs subpackage's files:
%{_libdir}/%{py_INSTSONAME_freethreading}

%extension_modules %{dynload_dir_freethreading} %{SOABI_freethreading}
%extension_modules_test %{dynload_dir_freethreading} %{SOABI_freethreading}
%{dynload_dir_freethreading}/_tkinter.%{SOABI_freethreading}.so

# Analog of the -devel subpackage's files:
%{pylibdir_freethreading}/config-%{LDVERSION_freethreading}-%{platform_triplet}/
%{_includedir}/python%{LDVERSION_freethreading}/
%{_bindir}/python%{LDVERSION_freethreading}-config
%{_bindir}/python%{LDVERSION_freethreading}-*-config
%{_libdir}/libpython%{LDVERSION_freethreading}.so
%{_libdir}/pkgconfig/python-%{LDVERSION_freethreading}.pc
%{_libdir}/pkgconfig/python-%{LDVERSION_freethreading}-embed.pc

%endif # with freethreading_build

%if %{with freethreading_build} && %{with debug_build}
%files -n python%{pybasever}-freethreading-debug
# Analog of the core subpackage's files:
%{_bindir}/python%{LDVERSION_freethreading_debug}

# Analog to the -libs subpackage's files:
%{_libdir}/%{py_INSTSONAME_freethreading_debug}

# Analog of the libs, test, and tkinter extension modules:
%extension_modules %{dynload_dir_freethreading} %{SOABI_freethreading_debug}
%extension_modules_test %{dynload_dir_freethreading} %{SOABI_freethreading_debug}
%{dynload_dir_freethreading}/_tkinter.%{SOABI_freethreading_debug}.so

# Analog of the -devel subpackage's files:
%{pylibdir_freethreading}/config-%{LDVERSION_freethreading_debug}-%{platform_triplet}/
%{_includedir}/python%{LDVERSION_freethreading_debug}/
%{_bindir}/python%{LDVERSION_freethreading_debug}-config
%{_bindir}/python%{LDVERSION_freethreading_debug}-*-config
%{_libdir}/libpython%{LDVERSION_freethreading_debug}.so
%{_libdir}/pkgconfig/python-%{LDVERSION_freethreading_debug}.pc
%{_libdir}/pkgconfig/python-%{LDVERSION_freethreading_debug}-embed.pc

%{pylibdir_freethreading}/_sysconfigdata_%{ABIFLAGS_freethreading_debug}_linux_%{platform_triplet}.py
%{pylibdir_freethreading}/__pycache__/_sysconfigdata_%{ABIFLAGS_freethreading_debug}_linux_%{platform_triplet}%{bytecode_suffixes}

%endif # with freethreading_build && debug_build

# We put the debug-gdb.py file inside /usr/lib/debug to avoid noise from ldconfig
# See https://bugzilla.redhat.com/show_bug.cgi?id=562980
#
# The /usr/lib/rpm/redhat/macros defines %%__debug_package to use
# debugfiles.list, and it appears that everything below /usr/lib/debug and
# (/usr/src/debug) gets added to this file (via LISTFILES) in
# /usr/lib/rpm/find-debuginfo.sh
#
# Hence by installing it below /usr/lib/debug we ensure it is added to the
# -debuginfo subpackage
# (if it doesn't, then the rpmbuild ought to fail since the debug-gdb.py
# payload file would be unpackaged)

# Workaround for https://bugzilla.redhat.com/show_bug.cgi?id=1476593
%undefine _debuginfo_subpackages

# ======================================================
# Finally, the changelog:
# ======================================================

%changelog
* Fri Jan 16 2026 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.13.11-1
- updated to vendor version 3.13.11

* Fri May 16 2025 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.13.2-2
- fixed some issues 

* Mon May 05 2025 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.13.2-1
- update to version 3.13.2

* Fri Feb 28 2025 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.9.21-1
- update to version 3.9.21
- fix ticket #12
- fix ticket #13

* Tue Jul 04 2023 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.9.17-1
- update to version 3.9.17

* Fri Mar 03 2023 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.9.13-2
- fix ticket #9

* Mon Jul 04 2022 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.9.13-1
- update to version 3.9.13

* Fri Feb 18 2022 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.9.5-8
- fix several glitches in codepage handling
- enable os2 in bdist as well

* Mon Dec 27 2021 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.9.5-7
- fix ticket #7

* Thu Nov 25 2021 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.9.5-6
- fix reading pyc files
- fix isabs for in bootstrap
- fix spawn
- add HOME as ~ replacement

* Mon Jun 28 2021 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.9.5-5
- python-tkinter was tkinter, so name it right

* Fri Jun 18 2021 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.9.5-4
- obsolete/provide python-tools, python-tkinter

* Mon Jun 07 2021 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.9.5-3
- obsolete/provide python, python-libs, python-devel, python-test
- use pyd again instead of dll for modules. fixes some name clashes in anpm

* Wed May 26 2021 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.9.5-2
- Add a symlink for python3.9
- Add python.exe to unversioned-command
- Fix issue #5

* Wed May 12 2021 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.9.5-1
- fix several bugs from first 3.9.2
- update to version 3.9.5

* Wed Apr 14 2021 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.9.2-1
- first OS/2 python3 rpm
