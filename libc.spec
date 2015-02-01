#disable lxlite strip
%define __os_install_post	%{nil}

Name:           libc
License:        BSD; GPL v2 or later; LGPL v2.1 or later
Summary:        Standard Shared Libraries
Group:          System/Libraries
Version:        0.6.6
Release:        25%{?dist}
Url:            http://svn.netlabs.org/libc

BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Source:         libc-%{version}.zip
Source1:        libc-emxomf.zip
Patch0:         libc.patch

# These patches are not actually applied but they record what
# needs to be done to the stock LIBC 0.6 source in order to build
# emxomf.exe contained in libc-emxomf.zip 
Patch101:       libc-dmik-emxomf-02-remove-asterisk.diff
Patch102:       libc-yuri-emxomf-verbose-warnings-3.patch

BuildRequires:  rexx_exe

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
%setup -q -c -a 1
%patch0 

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

#remove (old) binutils headers/libs
rm -f %{buildroot}%{_includedir}/ansidecl.h
rm -f %{buildroot}%{_includedir}/bfd.h
rm -f %{buildroot}%{_includedir}/bfdlink.h
rm -f %{buildroot}%{_includedir}/dis-asm.h
rm -f %{buildroot}%{_includedir}/symcat.h
rm -f %{buildroot}%{_libdir}/libbfd.*
rm -f %{buildroot}%{_libdir}/libopcodes.*

#remove libstdc++/supc++ static libs (built with gcc 3.x)
rm -f %{buildroot}%{_libdir}/libstdc++.*
rm -f %{buildroot}%{_libdir}/libsupc++.*
rm -f %{buildroot}%{_libdir}/libiberty.*

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

%changelog
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
