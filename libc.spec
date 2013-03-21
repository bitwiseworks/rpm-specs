
Name:           libc
License:        BSD; GPL v2 or later; LGPL v2.1 or later
Summary:        Standard Shared Libraries
Group:          System/Libraries
Version:        0.6.5
Release:        17%{?dist}
Url:            http://svn.netlabs.org/libc

BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Source:         libc-%{version}.zip
Source1:        libc-emxomf.zip
Patch0:         libc.patch

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
Requires:       libc = %{version}

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

%description gettext-devel
These libraries are needed to develop programs which use the standard C
library (gettext headers).


%prep
%setup -q -c -a 1
%patch0 

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_usr}/i386-pc-os2-elf
mkdir -p %{buildroot}%{_usr}/i386-pc-os2-emx
mkdir -p %{buildroot}%{_usr}/man
mkdir -p %{buildroot}%{_usr}/info

cp -p -r usr/bin/* %{buildroot}%{_bindir}
cp -p -r usr/include/* %{buildroot}%{_includedir}
cp -p -r emxomf.exe %{buildroot}%{_bindir}
cp -p -r usr/lib/* %{buildroot}%{_libdir}
cp -p -r usr/man/* %{buildroot}%{_usr}/i386-pc-os2-elf
cp -p -r usr/man/* %{buildroot}%{_usr}/i386-pc-os2-emx
cp -p -r usr/man/* %{buildroot}%{_usr}/man
cp -p -r usr/man/* %{buildroot}%{_usr}/info

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

rexx2vio $RPM_BUILD_ROOT%{_bindir}/dllar.cmd $RPM_BUILD_ROOT%{_bindir}/dllar.exe

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%doc usr/doc/gcc-3.3.5/*
%{_libdir}/libc06*.dll

%files devel
%defattr(-,root,root)
%doc %{_prefix}/man/man1/*
%{_usr}/bin
%{_usr}/i386-pc-os2-elf
%{_usr}/i386-pc-os2-emx
%{_includedir}
%exclude %{_includedir}/db.h
%exclude %{_includedir}/ndbm.h
%exclude %{_includedir}/libintl.h
%{_usr}/info
%{_libdir}

%files -n db1-devel
%defattr(-,root,root)
%{_includedir}/db.h
%{_includedir}/ndbm.h

%files gettext-devel
%defattr(-,root,root)
%{_includedir}/libintl.h

%changelog
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
