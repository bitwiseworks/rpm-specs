# See the bug #429880
%global gcc_major  %(gcc -dumpversion || echo "666")
# See rhbz#1193591
%global automake_version %(set -- `automake --version | head -n 1` ; echo ${4-unknown})

%if !0%{?os2_version}
%bcond_without check
%else
# TODO make check takes insanely long when run by rpmbuild on OS/2.
%bcond_with check
%endif

Summary: The GNU Portable Library Tool
Name:    libtool
Version: 2.4.7
Release: 1%{?dist}

# To help future rebase, the following licenses were seen in the following files/folders:
# '*' is anything that was not explicitly listed earlier in the folder
#
# From libtool package:
# usr/bin/:
#  libtool - GPL-2.0-or-later WITH Libtool-exception AND MIT
#  libtoolize - GPL-2.0-or-later AND MIT
# usr/share/:
#  aclocal/* - FSFULLR
#  doc/libtool:
#    AUTHORS - GPL-2.0-or-later
#    * - FSFAP
#  info/* - GFDL-1.3-or-later
#  libtool/build-aux/:
#    {compile,depcomp,missing} - GPL-2.0-or-later WITH Autoconf-exception-generic
#    config.{guess,sub} - GPL-3.0-or-later WITH Autoconf-exception-generic-3.0
#    install-sh - X11 AND LicenseRef-Fedora-public-domain
#    ltmain.sh - GPL-2.0-or-later WITH Libtool-exception AND MIT
# usr/share/man/man1/*: generated from usr/bin/libtool{,ize} using help2man
#
# From libtool-ltdl package:
# usr/lib64/
#  * - LGPL-2.0-or-later WITH Libtool-exception
#
# From libtool-ltdl-devel package:
# usr/include/* - LGPL-2.0-or-later WITH Libtool-exception
# usr/share/:
#  README - FSFAP
#  {*.c,*.h,Makefile.am,configure.ac,ltdl.mk} - LGPL-2.0-or-later WITH Libtool-exception
#  Makefile.in - FSFULLRWD
#  aclocal.m4 - FSFULLR AND FSFULLRWD
#  configure - FSFUL
License: GPL-2.0-or-later AND GPL-2.0-or-later WITH Autoconf-exception-generic AND GPL-2.0-or-later WITH Libtool-exception AND LGPL-2.0-or-later WITH Libtool-exception AND GPL-3.0-or-later WITH Autoconf-exception-generic-3.0 AND MIT AND FSFAP AND FSFULLR AND FSFULLRWD AND GFDL-1.3-or-later AND X11 AND LicenseRef-Fedora-public-domain
URL:     http://www.gnu.org/software/libtool/

%if !0%{?os2_version}
Source:  http://ftp.gnu.org/gnu/libtool/libtool-%{version}.tar.xz

# ~> downstream
# ~> remove possibly once #1158915 gets fixed somehow
Patch0:  libtool-2.4.5-rpath.patch

# See the rhbz#1289759 and rhbz#1214506.  We disable hardening namely because
# that bakes the CFLAGS/LDFLAGS into installed /bin/libtool and ltmain.sh files.
# At the same time we want to have libltdl.so hardened.  Downstream-only patch.
%undefine _hardened_build
Patch1: libtool-2.4.6-hardening.patch

# The testsuite seems to not properly handle template instantiation and as
# a result fails.  libtool itself appears to be OK from my by-hand testing. (by Jeff Law)
# Disable LTO for link-order2 test (Related: #1988112)
Patch2: libtool-2.4.6-disable-lto-link-order2.patch

# non-PIC libraries are not supported on ARMv7
# Since we removed "-fPIC" from global CFLAGS this test fails on this arch (as expected)
# Please refer to the following ticket regarding PIC support on ARM:
# https://bugs.launchpad.net/ubuntu/+source/gcc-4.4/+bug/503448
Patch3: libtool-2.4.6-disable_non-pic_arm.patch

# rhbz#2047389, patch sent upstream
# https://lists.gnu.org/archive/html/libtool-patches/2022-02/msg00000.html
Patch4: libtool-2.4.6-keep-compiler-deps.patch

# Patch sent upstream
# https://lists.gnu.org/archive/html/libtool-patches/2022-12/msg00004.html
Patch5: 0001-tests-Fix-grep-warning-about-stray-before.patch

%if ! 0%{?_module_build}
Patch100: libtool-nodocs.patch
%endif

Patch101: libtool-c99.patch
%else
Vendor:  bww bitwise works GmbH

%scm_source github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2
%endif

# /usr/bin/libtool includes paths within gcc's versioned directories
# Libtool must be rebuilt whenever a new upstream gcc is built
# Starting with gcc 7 gcc in Fedora is packaged so that only major
# number changes need libtool rebuilding.
Requires: gcc(major) = %{gcc_major}
Requires: autoconf, automake, sed, tar, findutils

%if ! 0%{?_module_build}
BuildRequires: texinfo
%endif
BuildRequires: autoconf, automake
BuildRequires: help2man

# make sure we can configure all supported langs
%if !0%{?os2_version}
BuildRequires: libstdc++-devel, gcc-gfortran
%else
BuildRequires: libstdc++-devel
%endif

BuildRequires: gcc, gcc-c++
BuildRequires: make


%description
GNU Libtool is a set of shell scripts which automatically configure UNIX and
UNIX-like systems to generically build shared libraries. Libtool provides a
consistent, portable interface which simplifies the process of using shared
libraries.

If you are developing programs which will use shared libraries, but do not use
the rest of the GNU Autotools (such as GNU Autoconf and GNU Automake), you
should install the libtool package.

The libtool package also includes all files needed to integrate the GNU
Portable Library Tool (libtool) and the GNU Libtool Dynamic Module Loader
(ltdl) into a package built using the GNU Autotools (including GNU Autoconf
and GNU Automake).


%package ltdl
Summary:  Runtime libraries for GNU Libtool Dynamic Module Loader
Provides: %{name}-libs = %{version}-%{release}
License:  LGPLv2+


%description ltdl
The libtool-ltdl package contains the GNU Libtool Dynamic Module Loader, a
library that provides a consistent, portable interface which simplifies the
process of using dynamic modules.

These runtime libraries are needed by programs that link directly to the
system-installed ltdl libraries; they are not needed by software built using
the rest of the GNU Autotools (including GNU Autoconf and GNU Automake).


%package ltdl-devel
Summary: Tools needed for development using the GNU Libtool Dynamic Module Loader
Requires: automake = %automake_version
Requires: %{name}-ltdl = %{version}-%{release}
License:  LGPLv2+


%description ltdl-devel
Static libraries and header files for development with ltdl.


%if !0%{?os2_version}
%debug_package
%endif

%prep
%if !0%{?os2_version}
%autosetup -n libtool-%{version} -p1

autoreconf -v
%else
%scm_setup

# Make sure configure is updated to properly support OS/2
# (slashes in PATH are needed for the bootstrap script itself)
export PATH=`echo $PATH | tr '\\\\' /`
./bootstrap --copy --force --skip-git

# Restore .version and ChangeLog as they are not properly regenerated (they need .git)
rm -f .version ChangeLog
mv .version~ .version
mv ChangeLog~ ChangeLog
%endif

%build

%if 0%{?os2_version}
export CC=gcc
export CXX=g++
export F77=gfortran
export CFLAGS="$RPM_OPT_FLAGS"

# These are for LTDL DLL
export LDFLAGS="-Zomf -Zmap -Zhigh-mem"
%endif

%configure

%make_build \
    CUSTOM_LTDL_CFLAGS="%_hardening_cflags" \
    CUSTOM_LTDL_LDFLAGS="%_hardening_ldflags"


%check
%if %{with check}
make check VERBOSE=yes || { cat tests/testsuite.dir/*/testsuite.log ; false ; }
%endif


%install
%make_install
# info's TOP dir (by default owned by info)
rm -f %{buildroot}%{_infodir}/dir
# *.la *.a files generated by libtool shouldn't be distributed (and the
# `./configure --disable-static' breaks testsuite)
%if !0%{?os2_version}
rm -f %{buildroot}%{_libdir}/libltdl.{a,la}
%else
rm -f %{buildroot}%{_libdir}/libltdl.la
rm -f %{buildroot}%{_libdir}/ltdl.a
%endif


%files
%license COPYING
%doc AUTHORS NEWS README THANKS TODO ChangeLog*
%{_infodir}/libtool.info*.gz
%{_mandir}/man1/libtool.1*
%{_mandir}/man1/libtoolize.1*
%{_bindir}/libtool
%{_bindir}/libtoolize
%{_datadir}/aclocal/*.m4
%dir %{_datadir}/libtool
%{_datadir}/libtool/build-aux


%files ltdl
%license libltdl/COPYING.LIB
%if !0%{?os2_version}
%{_libdir}/libltdl.so.*
%else
%{_libdir}/ltdl*.dll
%endif


%files ltdl-devel
%license libltdl/COPYING.LIB
%doc libltdl/README
%{_datadir}/libtool
%exclude %{_datadir}/libtool/build-aux
%{_includedir}/ltdl.h
%{_includedir}/libltdl
# .so files without version must be in -devel subpackage
%if !0%{?os2_version}
%{_libdir}/libltdl.so
%else
%{_libdir}/ltdl*_dll.a
%endif


%changelog
* Fri Jan 26 2024 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.4.7-1
- update to version 2.4.7
- resync with latest Fedora spec

* Tue Jan 14 2020 Dmitriy Kuminov <coding@dmik.org> 2.4.6-4
- Use scm_ macros.
- Resync with latest Fedora spec (11bb551).
- Rebuild for GCC 9.
- Add support for LT_BUILDLEVEL [#1].

* Mon Nov 28 2016 Dmitriy Kuminov <coding@dmik.org> 2.4.6-3
- Add -buildlevel command line option to pass BUILDLEVEL signature
  for DLL creation.
- Fix NEED_USCORE detection in ltdl (LT_FUNC_DLSYM_USCORE) on OS/2.
- Build LTDL DLL with high memory support (-Zhigh-mem).

* Tue Feb 2 2016 Dmitriy Kuminov <coding@dmik.org> 2.4.6-2
- Fix missing DLL exports when -export-symbols-regex is given.
- Fix broken -os2dllname compatiblity.
- Set libext to lib when AR is emxomfar.
- Make SYMBOL_UNDERSCORE correctly defined.

* Tue Feb 17 2015 Dmitriy Kuminov <coding@dmik.org> 2.4.6-1
- Update to version 2.4.6 from vendor.

* Fri Jan 23 2015 yd
- rebuild for gcc 4.9.2.

* Tue Jan 13 2015 Dmitriy Kuminov <coding@dmik.org> 2.4.2-8
- Support -release option on OS/2.
- Use response files for long command lines when linking DLLs on OS/2.

* Fri Oct 31 2014 Dmitriy Kuminov <coding@dmik.org> 2.4.2-7
- Rename -os2dllname switch to -shortname (old one is still
  supported for backward compatibility).
- Always set allow_undefined to no on OS/2.
- Fix setting BEGINLIBPATH in execute mode on OS/2.
- Support -version-number on OS/2.

* Tue Oct 3 2014 Dmitriy Kuminov <coding@dmik.org> 2.4.2-6
- Generate proper DLL version suffix (CURRNENT - AGE).

* Tue Sep 30 2014 Dmitriy Kuminov <coding@dmik.org> 2.4.2-5
- Fix weird typo breaking correct OS/2 DLL name generation
  in some cases.

* Thu Sep 04 2014 yd
- added debug package with symbolic info for exceptq.

* Wed Sep 3 2014 Dmitriy Kuminov <coding@dmik.org> 2.4.2-3
- Rebuild with autoconf 2.69-2.
- Use /@unixroot in generated files instead of absolute paths to
  compiler files.

* Mon Sep 1 2014 Dmitriy Kuminov <coding@dmik.org> 2.4.2-2
- Fix PATH_SEPARATOR detection in libtoolize.

* Sun Aug 31 2014 Dmitriy Kuminov <coding@dmik.org> 2.4.2-1
- Initial package for version 2.4.2.
