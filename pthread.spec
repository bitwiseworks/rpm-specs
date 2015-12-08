%define svn_url     http://svn.netlabs.org/repos/ports/pthread/trunk
%define svn_rev     1208

%define kmk_dist out/os2.x86/release/dist

Summary: A posix pthread emulation for OS/2-eComStation
Name: pthread
Version: 20151207
Release: 20%{?dist}
License: unknown
Group: Development/Libraries
Source: %{name}-%{version}-r%{svn_rev}.zip
Source1: pthread-legacy-os2.zip


%description
A posix pthread emulation library.

%package devel
Summary: Header files developing apps which will use pthread
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
Header files and a library of pthread functions, for developing apps
which will use the library.

%package legacy
Summary: The previous posix pthread emulation library.

%description legacy
The previous posix pthread emulation library.

%package debug
Summary: HLL debug data for exception handling support.
Requires: %{name} = %{version}-%{release}

%description debug
HLL debug data for exception handling support.

%prep
%if %(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')
%setup -q
%else
%setup -n "%{name}-%{version}" -T -c -a 1
svn export -r %{svn_rev} %{svn_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" "%{name}-%{version}")
%endif

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
* Mon Dec 07 2015 yd <yd@os2power.com> 20151207-20
- r1208, added add some basic rwlock support.

* Thu May 21 2015 yd <yd@os2power.com> 20150408-19
- force -devel and -debug to depend on main package, fixes ticket:138.

* Wed Apr 08 2015 yd <yd@os2power.com> 20150408-18
- r1137, add missing export _pthread_attr_setdetachstate(), fixes ticket:65.

* Fri Mar 27 2015 yd <yd@os2power.com> 20150327-17
- r1118, Change pthread_yield() return value to int, fixes ticket#63.

* Thu Aug 14 2014 yd
- r812-813, set stack to be at least 2MB for new threads.
- Pull sources directly from SVN/GIT, ticket#76.

* Fri Apr 25 2014 Dmitriy Kuminov <dmik/coding.org>
- r720, Return proper POSIX errors in 'key' APIs. Fix pthread_key_delete() return code.

* Thu Apr 24 2014 Dmitriy Kuminov <dmik/coding.org>
- r718, fix invalid dereference in TlsAlloc and TlsFree.

* Wed Feb 26 2014 komh
- r704, pthread_mutex_destroy() crashs if a variable with PTHREAD_MUTEX_INITIALIZER is passed.

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
