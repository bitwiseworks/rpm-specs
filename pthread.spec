%define kmk_dist out/os2.x86/release/dist

Summary: A posix pthread emulation for OS/2-eComStation
Name: pthread
Version: 20131117
Release: 12%{?dist}
License: unknown
Group: Development/Libraries
Source: pthread-%{version}-os2.zip
Source1: pthread-legacy-os2.zip


%description
A posix pthread emulation library.

%package devel
Summary: Header files developing apps which will use pthread
Group: Development/Libraries

%description devel
Header files and a library of pthread functions, for developing apps
which will use the library.

%package legacy
Summary: The previous posix pthread emulation library.

%description legacy
The previous posix pthread emulation library.

%package debug
Summary: HLL debug data for exception handling support.

%description debug
HLL debug data for exception handling support.

%prep
%setup -q -c -a 1


%build
export KCFLAGS="%{optflags}"
kmk -C src
kmk -C src install

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}

cp pthread.dll %{buildroot}%{_libdir}
cp %{kmk_dist}/bin/pthr01.dll %{buildroot}%{_libdir}
cp %{kmk_dist}/include/pthread.h %{buildroot}%{_includedir}
cp %{kmk_dist}/lib/pthread*.a %{buildroot}%{_libdir}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/pthr??.dll
%exclude %{_libdir}/*.dbg

%files devel
%defattr(-,root,root)
%{_libdir}/*.a
%{_includedir}/*

%files legacy
%defattr(-,root,root)
%{_libdir}/pthread.dll

%files debug
%defattr(-,root,root)
%{_libdir}/*.dbg

%changelog
* Sat Nov 17 2013 yd
- r684, fix initializer for mutex destroy, fixes AOO i123001.

* Mon Sep 24 2012 yd
- added stubs for pthread_rwlock_* functions.

* Tue Mar 13 2012 yd
- added missing prototypes and exports (detach and kill).

* Wed Nov 02 2011 yd
- added -Zdll to build system
- improved build system

* Thu Oct 11 2011 yd
- exception record must be on stack
- always uninstall record from running thread
- use new LibLoadExceptq to enable exceptq only if main app loads it. Code by Rich Walsh.

* Thu Sep 22 2011 yd
- enable high memory access for library, otherwise every app using it is forced to use low memory (see git).
