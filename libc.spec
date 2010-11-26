
Name:           libc
License:        BSD; GPL v2 or later; LGPL v2.1 or later
Summary:        Standard Shared Libraries
Group:          System/Libraries
Version:        0.6.3
Release:        2%{?dist}
Url:            http://svn.netlabs.org/libc

BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Source:         libc-%{version}.zip

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


%prep
%setup -q -n libc-%{version}

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p %{buildroot}%{_usr}
cp -r "*" %{buildroot}%{_usr}
mkdir -p %{buildroot}%{_datadir}/doc/libc-0.6.3
mv %{buildroot}%{_usr}/doc/gcc-3.3.5 %{buildroot}%{_datadir}/doc/libc-0.6.3
#mv %{buildroot}%{_datadir}/doc/gcc-3.3.5 libc-0.6.3

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%doc %{_datadir}/doc/*
/%{_libdir}/libc06*.dll


%files devel
%defattr(-,root,root)
%doc %{_prefix}/man/man1/*
%{_usr}/bin
%{_usr}/i386-pc-os2-elf
%{_usr}/i386-pc-os2-emx
%{_usr}/include
%{_usr}/info
%{_usr}/lib
%{_usr}/share

%changelog
