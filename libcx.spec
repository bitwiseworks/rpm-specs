Name: libcx
Summary: kLIBC Extension Library
Version: 0.5.0
Release: 1%{?dist}
License: LGPLv2.1+
Group: System/Libraries
Vendor: bww bitwise works GmbH
URL: https://github.com/bitwiseworks/libcx

%scm_source github https://github.com/bitwiseworks/libcx %{version}

Obsoletes: libpoll
Provides: libpoll

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

%define kmk_env \
    KMK_FLAGS="\
        KBUILD_VERBOSE=2 \
        BUILD_TYPE=release \
        INST_PREFIX=%{_prefix}"

%build
CFLAGS="$RPM_OPT_FLAGS"
LDFLAGS="-Zhigh-mem"
%{kmk_env}
kmk $KMK_FLAGS CFLAGS="$CFLAGS" LDFLAGS="$LDFLAGS"

%install
rm -rf %{buildroot}
%{kmk_env}
kmk $KMK_FLAGS DESTDIR="%{buildroot}" install
# Remove tests as we don't need them now
rm -rf %{buildroot}%{_bindir}/tst-*.exe
# Copy headers (@todo move it to Makefile.kmk)
mkdir -p %{buildroot}%{_includedir}/sys
echo "#include <sys/poll.h>" > nosys_poll.h
install -m 644 nosys_poll.h %{buildroot}%{_includedir}/poll.h
install -m 644 src/poll/poll.h %{buildroot}%{_includedir}/sys
install -m 644 src/mmap/sys/mman.h %{buildroot}%{_includedir}/sys

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc LICENSE README.md CHANGELOG.md
%{_libdir}/libcx*.dll

%files devel
%defattr(-,root,root)
%{_libdir}/libcx*.a
%{_bindir}/libcx-stats.exe
%{_includedir}/poll.h
%{_includedir}/sys/poll.h
%{_includedir}/sys/mman.h

%changelog
* Fri Mar 10 2017 Dmitriy Kuminov <coding@dmik.org> 0.5.0-1
- Release version 0.4.1
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
