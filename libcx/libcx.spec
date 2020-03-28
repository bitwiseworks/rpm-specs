Name: libcx
Summary: kLIBC Extension Library
Version: 0.6.7
Release: 1%{?dist}
License: LGPLv2.1+
Group: System/Libraries
Vendor: bww bitwise works GmbH
URL: https://github.com/bitwiseworks/libcx

%scm_source github https://github.com/bitwiseworks/libcx %{version}
#scm_source git file://D:/Coding/libcx/master %{version}

BuildRequires: sed

Obsoletes: libpoll
Provides: libpoll

# Due to patch from kLIBC #366
Requires: libc >= 0.6.6-35
# Due to LIBCn #62 (socklen_t)
BuildRequires: libc-devel >= 1:0.1.4

%description
The kLIBC Extension Library extends the functionality of the kLIBC library
by adding a number of high demand features required by modern applications.

%package devel
Summary: Development package for %{name}
Requires: %{name} = %{version}-%{release}
Requires: libc-devel exceptq-devel
Requires: pkgconfig

Obsoletes: libpoll-devel
Provides: libpoll-devel

%description devel
Libraries, header files and documentation for %{name}.

%debug_package

%prep
%scm_setup

%global kmk_flags CFLAGS="%{optflags}" LDFLAGS=-Zhigh-mem KBUILD_VERBOSE=2 BUILD_TYPE=release INST_PREFIX="%{_prefix}"

%build
kmk %{kmk_flags}

%install
%{__rm}  -rf %{buildroot}
kmk %{kmk_flags} DESTDIR="%{buildroot}" install
# Remove tests as we don't need them now
%{__rm} -rf %{buildroot}%{_bindir}/tst-*.exe
# Copy headers (@todo move it to Makefile.kmk)
%{__mkdir_p} %{buildroot}%{_includedir}/sys %{buildroot}%{_includedir}/libcx
echo "#include <sys/poll.h>" > nosys_poll.h
%{__install} -m 644 nosys_poll.h %{buildroot}%{_includedir}/poll.h
%{__install} -m 644 src/poll/poll.h %{buildroot}%{_includedir}/sys
%{__install} -m 644 src/mmap/sys/mman.h %{buildroot}%{_includedir}/sys
%{__install} -m 644 src/exeinfo/libcx/exeinfo.h %{buildroot}%{_includedir}/libcx
%{__install} -m 644 src/net/libcx/net.h %{buildroot}%{_includedir}/libcx
%{__install} -m 644 src/net/ifaddrs.h %{buildroot}%{_includedir}
%{__install} -m 644 src/spawn/libcx/spawn2.h %{buildroot}%{_includedir}/libcx
# Dir for LIBCx assertion logs
%{__mkdir_p} %{buildroot}%{_var}/log/libcx

%check
kmk  %{kmk_flags} test

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc LICENSE README.md CHANGELOG.md
%{_libdir}/libcx*.dll
%{_libdir}/libcx-spawn2.wrp
%dir %{_var}/log/libcx

%files devel
%defattr(-,root,root)
%{_libdir}/libcx*.a
%{_bindir}/libcx-stats.exe
%{_includedir}/poll.h
%{_includedir}/ifaddrs.h
%{_includedir}/sys/poll.h
%{_includedir}/sys/mman.h
%{_includedir}/libcx/exeinfo.h
%{_includedir}/libcx/net.h
%{_includedir}/libcx/spawn2.h

%changelog
* Fri Mar 27 2020 Dmitriy Kuminov <coding@dmik.org> 0.6.7-1
- Release version 0.6.7
  (https://github.com/bitwiseworks/libcx/blob/0.6.7/CHANGELOG.md).

* Mon Jul 15 2019 Dmitriy Kuminov <coding@dmik.org> 0.6.6-1
- Release version 0.6.6
  (https://github.com/bitwiseworks/libcx/blob/0.6.6/CHANGELOG.md).

* Fri Mar 29 2019 Dmitriy Kuminov <coding@dmik.org> 0.6.5-1
- Release version 0.6.5
  (https://github.com/bitwiseworks/libcx/blob/0.6.5/CHANGELOG.md).
- Build against LIBCn (kLIBC successor).

* Mon Dec 31 2018 Dmitriy Kuminov <coding@dmik.org> 0.6.4-1
- Release version 0.6.4
  (https://github.com/bitwiseworks/libcx/blob/0.6.4/CHANGELOG.md).

* Tue Sep 11 2018 Dmitriy Kuminov <coding@dmik.org> 0.6.3-1
- Release version 0.6.3
  (https://github.com/bitwiseworks/libcx/blob/0.6.3/CHANGELOG.md).

* Tue Apr 17 2018 Dmitriy Kuminov <coding@dmik.org> 0.6.2-1
- Release version 0.6.2
  (https://github.com/bitwiseworks/libcx/blob/0.6.2/CHANGELOG.md).

* Mon Jan 8 2018 Dmitriy Kuminov <coding@dmik.org> 0.6.1-2
- Add missing header libcx/spawn2.h.
- Enable tests at build time (fixed).

* Wed Dec 27 2017 Dmitriy Kuminov <coding@dmik.org> 0.6.1-1
- Release version 0.6.1
  (https://github.com/bitwiseworks/libcx/blob/0.6.1/CHANGELOG.md).
- Add check section to run tests.

* Tue Aug 29 2017 Dmitriy Kuminov <coding@dmik.org> 0.6.0-1
- Release version 0.6.0
  (https://github.com/bitwiseworks/libcx/blob/0.6.0/CHANGELOG.md).
- Add check section to run tests.

* Fri Jun 2 2017 Dmitriy Kuminov <coding@dmik.org> 0.5.3-1
- Release version 0.5.3
  (https://github.com/bitwiseworks/libcx/blob/0.5.3/CHANGELOG.md).

* Mon Mar 27 2017 Dmitriy Kuminov <coding@dmik.org> 0.5.2-1
- Release version 0.5.2
  (https://github.com/bitwiseworks/libcx/blob/0.5.2/CHANGELOG.md).

* Fri Mar 24 2017 Dmitriy Kuminov <coding@dmik.org> 0.5.1-1
- Release version 0.5.1
  (https://github.com/bitwiseworks/libcx/blob/0.5.1/CHANGELOG.md).

* Fri Mar 10 2017 Dmitriy Kuminov <coding@dmik.org> 0.5.0-1
- Release version 0.5.0
  (https://github.com/bitwiseworks/libcx/blob/0.5.0/CHANGELOG.md).

* Wed Jan 18 2017 Dmitriy Kuminov <coding@dmik.org> 0.4.1-1
- Release version 0.4.1
  (https://github.com/bitwiseworks/libcx/blob/0.4.1/CHANGELOG.md).

* Thu Nov 24 2016 Dmitriy Kuminov <coding@dmik.org> 0.4-1
- Release version 0.4
  (https://github.com/bitwiseworks/libcx/blob/0.4/CHANGELOG.md).

* Mon Sep 26 2016 Dmitriy Kuminov <coding@dmik.org> 0.3.1-1
- Release version 0.3.1
  (https://github.com/bitwiseworks/libcx/blob/0.3.1/CHANGELOG.md).

* Thu Sep 22 2016 Dmitriy Kuminov <coding@dmik.org> 0.3-1
- Release version 0.3
  (https://github.com/bitwiseworks/libcx/blob/0.3/CHANGELOG.md).

* Fri Aug 19 2016 Dmitriy Kuminov <coding@dmik.org> 0.2.1-1
- Release version 0.2.1
  (https://github.com/bitwiseworks/libcx/blob/0.2.1/CHANGELOG.md).

* Mon Jul 18 2016 Dmitriy Kuminov <coding@dmik.org> 0.2-1
- Release version 0.2
  (https://github.com/bitwiseworks/libcx/blob/0.2/CHANGELOG.md).

* Fri Jun 10 2016 Dmitriy Kuminov <coding@dmik.org> 0.1-1
- Initial package for version 0.1.
