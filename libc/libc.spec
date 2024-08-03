# Defines the major version (used in the DLL name)
%define ver_maj 0

# Disable .dbg creation for forwaders and compression for the main DLL
# (will be done manually with special compression options)
%define _strip_opts --debuginfo -x "libc*.dll" --compress -x "libcn%{ver_maj}.dll"

# New Epoch to signify rebranding from kLIBC to LIBC Next with its own versioning
Epoch:          1

Name:           libc
License:        BSD; GPL v2 or later; LGPL v2.1 or later
Summary:        Standard Shared Libraries
Group:          System/Libraries
Version:        %{ver_maj}.1.13
Release:        1%{?dist}
Vendor:         bww bitwise works GmbH
Url:            https://github.com/bitwiseworks/libc

%scm_source github https://github.com/bitwiseworks/libc %{version}
#scm_source git file://D:/Coding/libc/master %{version}

BuildRequires:  rexx_exe kbuild
BuildRequires:  gcc unzip sed gawk

# we need ourselves for the build
BuildRequires:  libc-devel

# for libiberty (#49)
BuildRequires:  binutils-devel >= 2.33.1

# Require kLIBC user management to make programs using Unix user management API
# (getpwuid() and friends) work correctly.
# TODO remove this dependency once master.passwd init is moved from klusrmgr here.
# Also, move pwd_mkdb.exe to a separate subpackage (libc-tools?) and depend klusrmgr on it.
Requires:       klusrmgr >= 1.2.2

%description
kLIBC is a C runtime library in which the coder is exploring The Single Unix
Specification (SUS) and various *BSD, Sun and Linux interfaces used in 'portable'
software. While implementing SUS completely and providing a great range of special
BSD, Sun and Linux APIs is a kind of ultimate goal, the main focus is on what is
interesting to play with and what is requested by porters using kLIBC.


%package devel
License:        BSD; GPL v2 or later; LGPL v2.1 or later
Summary:        Include Files and Libraries Mandatory for Development
Group:          Development/Libraries/C and C++
Requires:       libc = %{epoch}:%{version}-%{release}
Obsoletes:      libc-kprofile < %{version}

%description devel
These libraries are needed to develop programs which use the standard C
library.


%package db1-devel
License:        BSD; GPL v2 or later; LGPL v2.1 or later
Summary:        Include Files and Libraries Mandatory for Development (db headers)
Group:          Development/Libraries/C and C++
Requires:       libc = %{epoch}:%{version}-%{release}
Provides:       db1-devel = %{epoch}:%{version}-%{release}
Obsoletes:      db1-devel < %{epoch}:%{version}-%{release}

%description db1-devel
These libraries are needed to develop programs which use the standard C
library (db headers).


%package gettext-devel
License:        BSD; GPL v2 or later; LGPL v2.1 or later
Summary:        Include Files and Libraries Mandatory for Development (gettext headers)
Group:          Development/Libraries/C and C++
Provides:       gettext-devel
Requires:       libc = %{epoch}:%{version}-%{release}

%description gettext-devel
These libraries are needed to develop programs which use the standard C
library (gettext headers).


%debug_package


%prep

%scm_setup

# Check that package version matches the version from the sources
test "`grep -P -o '(?<=(VH|VM|VL) = )([0-9]+)' < src/emx/version.smak | tr -d \\\r | tr \\\n .`" = "%{version}."


%build

# NOTE: OPTIMIZE_FLAGS below overrides -O2 with -O3 as LIBC wants this.

%define kmk_flags \\\
  NO_STRIP=1 \\\
  INS="%{buildroot}/@unixroot/usr/" \\\
  OUT=out/ \\\
  ASM="%{_builddir}/%{?buildsubdir}/bin/ml.exe -c" \\\
  SHELL=/@unixroot/usr/bin/sh.exe \\\
  BUILD_ID="%{lua: print(string.sub(rpm.expand('%{__source_rev}'), 1, 7))}-git" \\\
  OPTIMIZE_FLAGS="%{lua: print((string.gsub(rpm.expand('%{optflags}'), '-O2', '-O3')))}" \\\
  OFFICIAL_VERSION=1

# boostrap everything using the system LIBC build
kmk -C src/emx MODE=opt %{kmk_flags} tools
# NOTE: There is a bug in kmk's .NOTPARALLEL processing triggered by $(_STD_WILDWILD) deps for
# $.stmp-libc-std that causes it to generate libc-std.h out of order so that files including it
# build earlier. A workaround is to generate this file up front in a separate invocation.
kmk -C src/emx MODE=opt %{kmk_flags} -f libonly.gmk libc-std.h
kmk -C src/emx MODE=opt %{kmk_flags} libs
kmk -C src/emx MODE=opt %{kmk_flags} install

# check that install uses the right dirs
test -d "%{buildroot}%{_bindir}" -a -d "%{buildroot}%{_libdir}" -a -d "%{buildroot}%{_includedir}"

# build everything again from scratch using the bootstrap LIBC
%{__rm} -rf out/
export PATH="%{buildroot}%{_bindir};$PATH"
export LIBRARY_PATH="%{buildroot}%{_libdir};$LIBRARY_PATH"
export C_INCLUDE_PATH="%{buildroot}%{_includedir};$C_INCLUDE_PATH"
export BEGINLIBPATH="%{buildroot}%{_libdir};$BEGINLIBPATH"
# NOTE: we'd like to use LIBPATHSTRICT, but this will lead to problems because processes will end up
# having two LIBC DLLs in memory (the old one from the boot runtime dragged in by other dependent DLLs
# which are not also on BEGINLIBPATH) and the just-built one (which will lack calls from these other
# DLLs). This in turn will lead to a number of side effects and the execution will most likely fail.
# Therefore we just hope that the boot DLL has all necessary exports. If not, the newly-built one
# will have to be manually installed and rebooted with in order for the build to complete.
#export LIBPATHSTRICT=T
kmk -C src/emx MODE=opt %{kmk_flags} tools
kmk -C src/emx MODE=opt %{kmk_flags} -f libonly.gmk libc-std.h
kmk -C src/emx MODE=opt %{kmk_flags} libs

%install

%{__rm} -rf %{buildroot}
kmk -C src/emx MODE=opt %{kmk_flags} install

# use special lxlite flags for the main LIBC DLL (see LXLITE.FLAGS in
# Makefile.gmk for reasoning) - note that we have to strip ourselves too
# TODO: add a _strip_opts option to override compression options
emxomfstrip -D %{buildroot}%{_libdir}/libcn%{ver_maj}.dbg %{buildroot}%{_libdir}/libcn%{ver_maj}.dll
lxlite /F+ /AP:4096 /MRN /MLN /MF1 %{buildroot}%{_libdir}/libcn%{ver_maj}.dll

# don't need this (not used)
%{__rm} -rf %{buildroot}/@unixroot/usr/i386-pc-os2-emx

# don't need this (some Innotek helper DLL)
%{__rm} -f %{buildroot}%{_libdir}/innidm.dll

# remove .map files
%{__rm} -f %{buildroot}%{_libdir}/*.map
%{__rm} -f %{buildroot}%{_libdir}/log/*.map

# remove ELH and PRF DLLs due to missing kdbglib.dll and kprofile.dll
# (http://trac.netlabs.org/rpm/ticket/196)
%{__rm} -f %{buildroot}%{_libdir}/libc*.elh
%{__rm} -f %{buildroot}%{_libdir}/libc*.prf

# remove CHKLOG and PRF versions of utility libraries (not used)
%{__rm} -f %{buildroot}%{_libdir}/lib*_l.*
%{__rm} -f %{buildroot}%{_libdir}/tcpipv4/lib*_l.*
%{__rm} -f %{buildroot}%{_libdir}/lib*_p.*
%{__rm} -f %{buildroot}%{_libdir}/tcpipv4/lib*_p.*

# remove static versions of LIBC (not supported)
%{__rm} -f %{buildroot}%{_libdir}/lib*_s.*
%{__rm} -f %{buildroot}%{_libdir}/libc_app.*
%{__rm} -f %{buildroot}%{_libdir}/libc_app_*.*

# remove sys/mman.h (provided by libcx-devel)
%{__rm} -f %{buildroot}%{_includedir}/sys/mman.h

# convert & install dllar
rexx2vio src/misc/dllar.cmd %{buildroot}%{_bindir}/dllar.exe

# build omf libraries
src/misc/MakeOmfLibs.cmd %{buildroot}%{_libdir}


%clean

rm -rf "%{buildroot}"


%files
%doc README.md CHANGELOG.md
%doc doc/COPYING.* doc/*.os2
%{_libdir}/libc*.dll
%{_bindir}/pwd_mkdb.exe


%files devel -f %{debug_package_exclude_files}
%{_bindir}
%{_includedir}
%exclude %{_includedir}/db.h
%exclude %{_includedir}/ndbm.h
%exclude %{_includedir}/libintl.h
%{_libdir}
%exclude %{_libdir}/libc*.dll
%exclude %{_bindir}/pwd_mkdb.exe


%files db1-devel
%{_includedir}/db.h
%{_includedir}/ndbm.h


%files gettext-devel
%{_includedir}/libintl.h


%changelog
* Sat Aug 3 2024 Dmitriy Kuminov <coding@dmik.org> 1:0.1.13-1
- Release LIBC Next version 0.1.13
  (https://github.com/bitwiseworks/libc/blob/0.1.13/CHANGELOG.md).

* Mon Sep 11 2023 Dmitriy Kuminov <coding@dmik.org> 1:0.1.12-1
- Release LIBC Next version 0.1.12
  (https://github.com/bitwiseworks/libc/blob/0.1.12/CHANGELOG.md).

* Wed Aug 30 2023 Dmitriy Kuminov <coding@dmik.org> 1:0.1.11-1
- Release LIBC Next version 0.1.11
  (https://github.com/bitwiseworks/libc/blob/0.1.11/CHANGELOG.md).

* Tue Mar 22 2022 Dmitriy Kuminov <coding@dmik.org> 1:0.1.10-1
- Release LIBC Next version 0.1.10
  (https://github.com/bitwiseworks/libc/blob/0.1.10/CHANGELOG.md).

* Thu Aug 26 2021 Dmitriy Kuminov <coding@dmik.org> 1:0.1.9-1
- Release LIBC Next version 0.1.9
  (https://github.com/bitwiseworks/libc/blob/0.1.9/CHANGELOG.md).
- Use optflags which works well now (this will also enable removing RPMBUILD
  prefix from source files to make debuginfo references relocatable).

* Mon Aug 16 2021 Dmitriy Kuminov <coding@dmik.org> 1:0.1.8-1
- Release LIBC Next version 0.1.8
  (https://github.com/bitwiseworks/libc/blob/0.1.8/CHANGELOG.md).

* Fri Feb 26 2021 Dmitriy Kuminov <coding@dmik.org> 1:0.1.7-1
- Release LIBC Next version 0.1.7
  (https://github.com/bitwiseworks/libc/blob/0.1.7/CHANGELOG.md).

* Thu Dec 31 2020 Dmitriy Kuminov <coding@dmik.org> 1:0.1.6-1
- Release LIBC Next version 0.1.6
  (https://github.com/bitwiseworks/libc/blob/0.1.6/CHANGELOG.md).

* Wed Jul 22 2020 Dmitriy Kuminov <coding@dmik.org> 1:0.1.5-1
- Release LIBC Next version 0.1.5
  (https://github.com/bitwiseworks/libc/blob/0.1.5/CHANGELOG.md).
- Remove libc-db1-devel from BuildRequires (not needed any more).

* Fri Mar 27 2020 Dmitriy Kuminov <coding@dmik.org> 1:0.1.4-1
- Release LIBC Next version 0.1.4
  (https://github.com/bitwiseworks/libc/blob/0.1.4/CHANGELOG.md).
- Build with GCC 9 and for pentium4 as well as for i686.
- devel: Install logging version of DLL to /@unixroot/usr/lib/log/.

* Wed Dec 25 2019 Dmitriy Kuminov <coding@dmik.org> 1:0.1.3-1
- Release LIBC Next version 0.1.3
  (https://github.com/bitwiseworks/libc/blob/0.1.3/CHANGELOG.md).
- Rebuild with newer libiberty (binutils 2.33.1) to fix EMXOMF crash [#49].

* Mon Jul 15 2019 Dmitriy Kuminov <coding@dmik.org> 1:0.1.2-1
- Release LIBC Next version 0.1.2
  (https://github.com/bitwiseworks/libc/blob/0.1.2/CHANGELOG.md).
- Fix RPM/real version mismatch check (CRLF problems).

* Sun Feb 24 2019 Dmitriy Kuminov <coding@dmik.org> 1:0.1.1-1
- Release LIBC Next version 0.1.1
  (https://github.com/bitwiseworks/libc/blob/0.1.1/CHANGELOG.md).
- Disable setting LIBPATHSTRICT as it may screw up the build.

* Fri Feb 15 2019 Dmitriy Kuminov <coding@dmik.org> 1:0.1.0-1
- Fork kLIBC and rebrand it to LIBC Next with a new versioning scheme and epoch.
- Release LIBC Next version 0.1.0
  (https://github.com/bitwiseworks/libc/blob/0.1.0/CHANGELOG.md).
- Use scm_source macros.
- Remove a lot of (unused and unneeded) static libs from the devel package.

* Fri Jan 11 2019 Dmitriy Kuminov <coding@dmik.org> 0.6.6-40
- Remove (old) libiberty headers (provided by binutils-devel now).

* Mon Dec 31 2018 Dmitriy Kuminov <coding@dmik.org> 0.6.6-39
- Make readdir return DT_LNK for symlinks (GH #9).
- Make sure SIGCHLD is raised after a zombie for wait[pid] is created (GH #10).
- Make reaplath fail on non-existing paths (GH #11).
- Make stat succeed on file names with trailing spaces (GH #12).
- Make [f]close return 0 regardless of DosClose result if LIBC handle is freed.
- Fix typo in dlclose backend that would result in random return values (GH #14).
- Increase dlerror buffer to 260+64 chars.

* Tue Jun 5 2018 Dmitriy Kuminov <coding@dmik.org> 0.6.6-38
- Fix resetting file access mode to O_WRONLY if opened with O_NOINHERIT. GitHub #2.
- Define __LONG_LONG_SUPPORTED on modern C++ (C++11 and above). GitHub #6.

* Mon May 21 2018 Dmitriy Kuminov <coding@dmik.org> 0.6.6-37
- Make libc-devel not provide libXXX.dll (it's provided by libc).

* Tue Apr 17 2018 Dmitriy Kuminov <coding@dmik.org> 0.6.6-36
- Apply patch from ticket #384 to fix DosAllocMemEx(OBJ_LOCATION) bug.

* Tue Aug 29 2017 Dmitriy Kuminov <coding@dmik.org> 0.6.6-35
- Apply patch from ticket #366 to allow using LIBC in fork() callbacks.

* Sat Jun 10 2017 Dmitriy Kuminov <coding@dmik.org> 0.6.6-34
- Remove BSD defines from sys/param.h and types.h to avoid mistreating OS/2
  as BSD (e.g. by LIBICU's unicode/platform.h).

* Tue Jun 6 2017 Dmitriy Kuminov <coding@dmik.org> 0.6.6-33
- Provide patched emxomfld.exe that fixes Invalid WKEXT record errors.

* Fri Apr 7 2017 Dmitriy Kuminov <coding@dmik.org> 0.6.6-32
- Require kLIBC user management (klusrmgr) to make programs using Unix user
  management API (getpwuid() and friends) work correctly.
- Move debug libraries from libc-devel to libc-debug (saves a lot of space).

* Thu Sep 22 2016 Dmitriy Kuminov <coding@dmik.org> 0.6.6-31
- Remove sys/mman.h which is now provided by libcx-devel.

* Fri Sep 02 2016 yd <yd@os2power.com> 0.6.6-30
- Fix path definitions in paths.h header. ticket#200.

* Sat Aug 20 2016 Dmitriy Kuminov <coding@dmik.org> 0.6.6-29
- Remove libcXXX.elh and libcXXX.prf from libc-devel due to missing
  dependnencies (klibdbg.dll and kprofile.dll). This also obsoletes
  the libc-kprofile dummy package.

* Mon Aug 8 2016 Dmitriy Kuminov <coding@dmik.org> 0.6.6-28
- Apply patches from tickets #361-365 to make fork() work in dash
  and similar cases and other minor improvements.

* Tue Jun 14 2016 yd <yd@os2power.com> 0.6.6-27
- removed libiberty.h since it is already in binutils-devel. ticket#103 and ticket#188.

* Sat Feb 07 2015 yd 0.6.6-26
- r3946, readded SafeWinUpper.
- removed asterisk patch from emxomf.

* Fri Jan 23 2015 yd 0.6.6-25
- added builtin.h and stddef.h patches required for building gcc 4.9.x.

* Sun Jan 18 2015 yd
- added new SafeDos* wrappers from trunk r3944.

* Sun Jan 11 2015 yd
- removed ansidecl.h since it is already in binutils-devel. ticket#103.

* Fri Jan 09 2015 yd
- added new SafeDos* wrappers from trunk r3942 and r3943.
- added emxomfstrip binary from trunk.

* Tue Jan 06 2015 yd 0.6.6-21
- update to libc 0.6.6-csd6, added omf libraries.

* Tue Aug 19 2014 Dmitriy Kuminov <coding@dmik.org> 0.6.5-20
- Merged emxomf-remove-asterick.diff from libc ticket #220.
- Made libc-devel and libc-gettext-devel strictly depend on current libc.

* Wed Jun 25 2014 yd
- emxomf, merged libc tickets #251, #293, #295.

* Wed Sep 11 2013 yd
- ticket#63: remove gcc335.dll from devel distribution.

* Thu Mar 21 2013 yd
- renamed gettext-devel to libc-gettext-devel to make it more visible.

* Thu Dec 13 2012 yd
- remove gcc 3.x stdc++/supc++ static libraries.

* Fri May 11 2012 yd
- remove obsolete binutil headers/libs

* Tue Apr 17 2012 yd
- update to csd5

* Mon Jan 09 2012 yd
- commented out sbrk/_sbrk definitions in stdlib.h (use unistd.h ones).

* Fri Dec 16 2011 yd
- restored stdarg.h/cdefs.h from original libc distribution.

* Thu Oct 20 2011 yd
- included emxomf.exe by dmik to workaround gcc/wlink bugs.

* Wed Oct 12 2011 yd
- fixed mmap include

* Mon Sep 05 2011 yd
- removed binutils

* Sun Sep 04 2011 yd
- update to csd4
