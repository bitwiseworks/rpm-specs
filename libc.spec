
Name:           libc
License:        BSD; GPL v2 or later; LGPL v2.1 or later
Summary:        Standard Shared Libraries
Group:          System/Libraries
Version:        0.6.3
Release:        6%{?dist}
Url:            http://svn.netlabs.org/libc

BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Source:         libc-%{version}.zip

Source1:         libc-os2.zip


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
%setup -q -n libc-%{version} -a 1

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p %{buildroot}%{_usr}
cp -r "*" %{buildroot}%{_usr}

rm -r %{buildroot}%{_usr}/doc/gcc-3.3.5/*

rexx2vio bin/dllar.cmd $RPM_BUILD_ROOT%{_bindir}/dllar.exe

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%doc doc/gcc-3.3.5/*
/%{_libdir}/libc06*.dll

%files devel
%defattr(-,root,root)
%doc %{_prefix}/man/man1/*
%{_usr}/bin
%{_usr}/i386-pc-os2-elf
%{_usr}/i386-pc-os2-emx
%{_usr}/include
%exclude %{_usr}/include/db.h
%exclude %{_usr}/include/ndbm.h
%exclude %{_usr}/include/libintl.h
%{_usr}/info
%{_usr}/lib
%{_usr}/share

%files -n db1-devel
%defattr(-,root,root)
%{_usr}/include/db.h
%{_usr}/include/ndbm.h

%files -n gettext-devel
%defattr(-,root,root)
%{_usr}/include/libintl.h

%changelog
