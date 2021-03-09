%define kmk_dist out/os2.x86/release/dist

Summary: A posix pthread emulation for OS/2 and OS/2 based systems
Name: pthread
Version: 0.2.4
Release: 1%{?dist}
License: unknown
Vendor:  bww bitwise works GmbH
Epoch: 2

%scm_source github http://github.com/bitwiseworks/pthread-os2 %{version}
#scm_source git file://D:/Coding/pthread/master %{version}

# Due to fixed _fmutex_request loop break.
Requires: libc >= 1:0.1.7

BuildRequires: gcc make

Source1: pthread-legacy-os2.zip

%description
A posix pthread emulation library.

%package devel
Summary: Header files developing apps which will use pthread
Requires: %{name} = %{epoch}:%{version}-%{release}

%description devel
Header files and a library of pthread functions, for developing apps
which will use the library.

%package legacy
Summary: The previous posix pthread emulation library.

%description legacy
The previous posix pthread emulation library.

%debug_package

%prep
%scm_setup
unzip %SOURCE1 -d .

%build
export KCFLAGS="%{optflags}"
kmk -C src
kmk -C src install

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}

cp pthread.dll %{buildroot}%{_libdir}
cp %{kmk_dist}/lib/pthr01.dll %{buildroot}%{_libdir}
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

%changelog
* Tue Mar 9 2021 Dmitriy Kuminov <coding@dmik.org> 2:0.2.4-1
- Make PTHREAD_RECURSIVE_MUTEX_INITIALIZER actually work [#11].
- Add support for kLIBC fork [#12].
- pthread_join: Fix possible race [#7].

* Fri Feb 26 2021 Dmitriy Kuminov <coding@dmik.org> 2:0.2.3-1
- Return proper POSIX errors in 'key' APIs (try 2).
- Retry waiting after DOS wait APIs fail with ERROR_INTERRUPT.
- pthread_mutex_trylock: Return EBUSY when mutex is locked instead of ETIMEDOUT.
- pthread_join: Don't call DosWaitThread twice.
- Use _fmutex for pthread_mutex [#9].

* Wed Aug 12 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> 2:0.2.2-1
- fix ticket #8

* Tue Mar 31 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> 2:0.2.1-1
- fix a regression of 0.2.0 (Dmitriy Kuminov)
- fix wrong dates in spec file

* Fri Mar 27 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> 2:0.2.0-1
- fix compiler warnings (Dmitriy Kuminov)
- make pthread_key_creation thread safe (Dmitriy Kuminov)
- make pthread_key_t integer for compatibility with POSIX (Dmitriy Kuminov)

* Mon Jan 06 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> 2:0.1.1-1
- add a real pthread_sigmask, so returncode is correct
- move source to github and clean it a bit

* Fri Mar 29 2019 Dmitriy Kuminov <coding@dmik.org> 2:0.1-1
- Bump epoch to 2 to replace bulky versioning scheme with normal one.
- Implement key destructors [#182].
- Make pthread_join survive kLIBC signal delivery.
- Build against LIBCn (kLIBC successor).

* Wed Jan 30 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> 20190130-23
- fix ticket #205 (code by KO Myung-Hun)
- fix ticket #204 (code by kO Myung-Hun)
- remove exceptq
- link against libcx
- add buildlevel info

* Wed Dec 27 2017 Dmitriy Kuminov <coding@dmik.org> 20171227-22
- Remove dangerous DosEnterCritSec usage.
- Use scm_source macro and friends.

* Tue Dec 29 2015 yd <yd@os2power.com> 20151229-21
- r1234, enable EXAPIS and mappings for fork() registration.

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

* Fri Apr 25 2014 Dmitriy Kuminov <coding@dmik.org>
- r720, Return proper POSIX errors in 'key' APIs. Fix pthread_key_delete() return code.

* Thu Apr 24 2014 Dmitriy Kuminov <coding@dmik.org>
- r718, fix invalid dereference in TlsAlloc and TlsFree.

* Wed Feb 26 2014 komh
- r704, pthread_mutex_destroy() crashs if a variable with PTHREAD_MUTEX_INITIALIZER is passed.

* Sun Nov 17 2013 yd
- r684, fix initializer for mutex destroy, fixes AOO i123001.

* Mon Sep 24 2012 yd
- added stubs for pthread_rwlock_* functions.

* Tue Mar 13 2012 yd
- added missing prototypes and exports (detach and kill).

* Wed Nov 02 2011 yd
- added -Zdll to build system
- improved build system

* Tue Oct 11 2011 yd
- exception record must be on stack
- always uninstall record from running thread
- use new LibLoadExceptq to enable exceptq only if main app loads it. Code by Rich Walsh.

* Thu Sep 22 2011 yd
- enable high memory access for library, otherwise every app using it is forced to use low memory (see git).
