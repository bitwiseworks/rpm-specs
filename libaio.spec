Summary: Port of Asynchronous I/O support from glibc.
Name: libaio
Version: 0.0.1
Release: 1%{?dist}
License: GPLv2, LGPL 2.1
URL: https://ftp.gnu.org/gnu/libc/
Group: Development/Libraries
Source: libaio-0.0.1.zip
BuildRequires: gcc
BuildRequires: libc-devel

%description
Asynchronous I/O support library does the support of
asynchronous I/O requests executing, e.g., read/write/list i/o. The 
requests are queued and are executed in background, with consequent
further signal delivery or thread creation.

%package devel
License:        GPLv2, LGPL 2.1
Summary:        Asynchronous I/O support library
Group:          Development/Libraries

%description devel
Asynchronous I/O support library does the support of
asynchronous I/O requests executing, e.g., read/write/list i/o. The 
requests are queued and are executed in background, with consequent
further signal delivery or thread creation.

%prep
%setup -q -n %{name}-%{version}

%build
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_includedir}
install -m 644 aio.h %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_libdir}
install -m 755 aio_dll.lib libaio.lib aio.dll %{buildroot}%{_libdir}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYING COPYING.LIB LICENSES README.OS2
%{_libdir}/aio.dll

%files devel
%defattr(-,root,root)
%{_includedir}/aio.h
%{_libdir}/libaio.lib
%{_libdir}/aio_dll.lib
%{_libdir}/aio.dbg

%changelog
* Sun Feb 14 2016 Valery V.Sedletski <_valerius@mail.ru> 0.0.1-1
- Initial package for version 0.0.1.
