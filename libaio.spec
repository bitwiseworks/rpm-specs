%define svn_url     http://svn.netlabs.org/repos/ports/libaio/trunk
%define svn_rev     1329

Summary: Port of Asynchronous I/O support from glibc.
Name: libaio
Version: 0.0.1
Release: 4%{?dist}
License: GPLv2, LGPL 2.1
URL: https://ftp.gnu.org/gnu/libc/
Group: Development/Libraries
Source: %{name}-%{version}-r%{svn_rev}.zip
Requires:      libgcc1 pthread
BuildRequires: gcc
BuildRequires: libc-devel pthread-devel

%description
Asynchronous I/O support library does the support of
asynchronous I/O requests executing, e.g., read/write/list i/o. The 
requests are queued and are executed in background, with consequent
further signal delivery or thread creation.

%package devel
License:        GPLv2, LGPL 2.1
Summary:        Asynchronous I/O support library
Group:          Development/Libraries
BuildRequires:  pthread-devel
Requires:       %name = %version-%release

%description devel
Asynchronous I/O support library does the support of
asynchronous I/O requests executing, e.g., read/write/list i/o. The 
requests are queued and are executed in background, with consequent
further signal delivery or thread creation.

%debug_package

%prep
%if %{?svn_rev:%(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')}%{!?svn_rev):0}
%setup -q
%else
%setup -q -n "%{name}-%{version}" -Tc
svn export %{?svn_rev:-r %{svn_rev}} %{svn_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip" "%{name}-%{version}")
%endif

%build
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_includedir}
install -m 644 aio.h %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_libdir}
install -m 755 aio_dll.* libaio.* aio.dll %{buildroot}%{_libdir}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYING COPYING.LIB LICENSES README.OS2
%{_libdir}/aio.dll

%files devel
%defattr(-,root,root)
%{_includedir}/aio.h
%{_libdir}/libaio.a
%{_libdir}/aio_dll.a
%{_libdir}/libaio.lib
%{_libdir}/aio_dll.lib

%changelog
* Mon Feb 29 2016 Valery Sedletski <_valerius@mail.ru> - 0.0.1-4
- Added needed Requires and BuildRequires directives

* Thu Feb 25 2016 Valery Sedletski <_valerius@mail.ru> - 0.0.1-3
- changed aio.dll -> aio in .def file

* Thu Feb 18 2016 Valery Sedletski <_valerius@mail.ru> - 0.0.1-2
- changed libs format from a.out to OMF
- added *-debug package

* Sun Feb 14 2016 Valery V.Sedletski <_valerius@mail.ru> - 0.0.1-1
- Initial package for version 0.0.1.
