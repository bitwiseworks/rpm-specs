
Name:           libc
License:        BSD; GPL v2 or later; LGPL v2.1 or later
Summary:        Standard Shared Libraries
Group:          System/Libraries
Version:        0.6.4
Release:        8%{?dist}
Url:            http://svn.netlabs.org/libc

BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Source:         libc-%{version}.zip
Source1:        libc-os2.tar.gz

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


%package -n gettext-devel
License:        BSD; GPL v2 or later; LGPL v2.1 or later
Summary:        Include Files and Libraries Mandatory for Development (gettext headers)
Group:          Development/Libraries/C and C++

%description -n gettext-devel
These libraries are needed to develop programs which use the standard C
library (gettext headers).


%prep
%setup -q -c -a 1

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_usr}/i386-pc-os2-elf
mkdir -p %{buildroot}%{_usr}/i386-pc-os2-emx
mkdir -p %{buildroot}%{_usr}/man
mkdir -p %{buildroot}%{_usr}/info

cp -p -r "usr/bin/*" %{buildroot}%{_bindir}
cp -p -r "usr/include/*" %{buildroot}%{_includedir}
cp -p -r "usr/lib/*" %{buildroot}%{_libdir}
cp -p -r "usr/man/*" %{buildroot}%{_usr}/i386-pc-os2-elf
cp -p -r "usr/man/*" %{buildroot}%{_usr}/i386-pc-os2-emx
cp -p -r "usr/man/*" %{buildroot}%{_usr}/man
cp -p -r "usr/man/*" %{buildroot}%{_usr}/info

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

%files -n gettext-devel
%defattr(-,root,root)
%{_includedir}/libintl.h

%changelog
* Tue Sep 04 2011 yd
- update to csd4
