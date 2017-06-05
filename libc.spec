#disable lxlite strip & debug info generation
%define __os_install_post	%{nil}

Name:           libc
License:        BSD; GPL v2 or later; LGPL v2.1 or later
Summary:        Standard Shared Libraries
Group:          System/Libraries
Version:        0.6.6
Release:        33%{?dist}
Url:            http://svn.netlabs.org/libc

Source:         libc-%{version}.zip
Source1:        libc-emxomf.zip
# This contains binary build of LIBC with patches from tickets #361-365
Source2:        libc-hotfix.zip
# This contains binary build of emxomfld with patches from ticket #376
Source3:        libc-emxomfld.zip

Patch0:         libc.patch

# These patches are not actually applied but they record what
# needs to be done to the stock LIBC 0.6 source in order to build
# emxomf.exe contained in libc-emxomf.zip
Patch101:       libc-dmik-emxomf-02-remove-asterisk.diff
Patch102:       libc-yuri-emxomf-verbose-warnings-3.patch

BuildRequires:  rexx_exe

# Require kLIBC user management to make programs using Unix user management API
# (getpwuid() and friends) work correctly.
Requires:       klusrmgr

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
Requires:       libc = %{version}-%{release}
Obsoletes:      libc-kprofile < %{version}

%description devel
These libraries are needed to develop programs which use the standard C
library.


%package -n db1-devel
License:        BSD; GPL v2 or later; LGPL v2.1 or later
Summary:        Include Files and Libraries Mandatory for Development (db headers)
Group:          Development/Libraries/C and C++

%description -n db1-devel
These libraries are needed to develop programs which use the standard C
library (db headers).


%package gettext-devel
License:        BSD; GPL v2 or later; LGPL v2.1 or later
Summary:        Include Files and Libraries Mandatory for Development (gettext headers)
Group:          Development/Libraries/C and C++
Provides:       gettext-devel
Requires:       libc = %{version}-%{release}

%description gettext-devel
These libraries are needed to develop programs which use the standard C
library (gettext headers).


%package debug
Summary: HLL debug data for exception handling support.

%description debug
HLL debug data for exception handling support.


%prep
%setup -q -c -a 1 -a 2 -a 3
%patch0

#replace paths.h wrong macros
sed -i 's,"/@unixroot/bin,"/@unixroot/usr/bin,g' usr/include/paths.h

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_usr}/man
mkdir -p %{buildroot}%{_usr}/info

cp -p -r usr/bin/* %{buildroot}%{_bindir}
cp -p -r usr/include/* %{buildroot}%{_includedir}
cp -p -r usr/lib/* %{buildroot}%{_libdir}
cp -p -r usr/man/* %{buildroot}%{_usr}/man
cp -p -r usr/man/* %{buildroot}%{_usr}/info

# add new files
cp -p -r emxomf.exe %{buildroot}%{_bindir}
cp -p -r emxomfstrip.exe %{buildroot}%{_bindir}
cp -p -r os2safe.h %{buildroot}%{_includedir}
cp -p -r libos2.a %{buildroot}%{_libdir}

cp -p -r emxomfld.exe %{buildroot}%{_bindir}

# add hotfix DLLs
cp -p -r libc066.* %{buildroot}%{_libdir}

# remove ELH and PRF DLLs due to missing kdbglib.dll and kprofile.dll
# (http://trac.netlabs.org/rpm/ticket/196)
rm -f %{buildroot}%{_libdir}/libc*.elh
rm -f %{buildroot}%{_libdir}/libc*.elh.map
rm -f %{buildroot}%{_libdir}/libc*.prf
rm -f %{buildroot}%{_libdir}/libc*.prf.map

#remove (old) binutils headers/libs
rm -f %{buildroot}%{_includedir}/ansidecl.h
rm -f %{buildroot}%{_includedir}/bfd.h
rm -f %{buildroot}%{_includedir}/bfdlink.h
rm -f %{buildroot}%{_includedir}/dis-asm.h
rm -f %{buildroot}%{_includedir}/libiberty.h
rm -f %{buildroot}%{_includedir}/symcat.h
rm -f %{buildroot}%{_libdir}/libbfd.*
rm -f %{buildroot}%{_libdir}/libopcodes.*

#remove libstdc++/supc++ static libs (built with gcc 3.x)
rm -f %{buildroot}%{_libdir}/libstdc++.*
rm -f %{buildroot}%{_libdir}/libsupc++.*
rm -f %{buildroot}%{_libdir}/libiberty.*

#remove sys/mman.h (provided by libcx-devel)
rm -f %{buildroot}%{_includedir}/sys/mman.h

rexx2vio $RPM_BUILD_ROOT%{_bindir}/dllar.cmd $RPM_BUILD_ROOT%{_bindir}/dllar.exe

# build omf libraries
cd %{buildroot}%{_libdir}
cmd /c "@MakeOmfLibs.cmd"

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%doc usr/doc/gcc-3.3.5/*
%{_libdir}/libc06*.dll

%files devel
%defattr(-,root,root)
%doc %{_prefix}/man/man1/*
%doc %{_prefix}/man/man7/*
%{_bindir}
%exclude %{_bindir}/*.dbg
%{_includedir}
%exclude %{_includedir}/db.h
%exclude %{_includedir}/ndbm.h
%exclude %{_includedir}/libintl.h
%{_usr}/info
%{_libdir}
%exclude %{_libdir}/*.dbg
%exclude %{_libdir}/dbg
%exclude %{_libdir}/tcpipv4/dbg
%exclude %{_libdir}/gcc335.dll

%files -n db1-devel
%defattr(-,root,root)
%{_includedir}/db.h
%{_includedir}/ndbm.h

%files gettext-devel
%defattr(-,root,root)
%{_includedir}/libintl.h

%files debug
%defattr(-,root,root)
%{_bindir}/*.dbg
%{_libdir}/*.dbg
%{_libdir}/dbg
%{_libdir}/tcpipv4/dbg

%changelog
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

* Thu Jan 09 2015 yd
- added new SafeDos* wrappers from trunk r3942 and r3943.
- added emxomfstrip binary from trunk.

* Tue Jan 06 2015 yd 0.6.6-21
- update to libc 0.6.6-csd6, added omf libraries.

* Tue Aug 19 2014 Dmitriy Kuminov <coding@dmik.org> 0.6.5-20
- Merged emxomf-remove-asterick.diff from libc ticket #220.
- Made libc-devel and libc-gettext-devel strictly depend on current libc.

* Wed Jun 25 2014 yd
- emxomf, merged libc tickets #251, #293, #295.

* Thu Sep 11 2013 yd
- ticket#63: remove gcc335.dll from devel distribution.

* Thu Mar 21 2013 yd
- renamed gettext-devel to libc-gettext-devel to make it more visible.

* Thu Dec 13 2012 yd
- remove gcc 3.x stdc++/supc++ static libraries.

* Mon May 11 2012 yd
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

* Wed Sep 05 2011 yd
- removed binutils

* Tue Sep 04 2011 yd
- update to csd4
