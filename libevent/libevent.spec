%global develdocdir %{_docdir}/%{name}-devel

Name:           libevent
Version:        2.1.11
Release:        4%{?dist}
Summary:        Abstract asynchronous event notification library

# arc4random.c, which is used in build, is ISC. The rest is BSD.
License:        BSD and ISC
URL:            http://libevent.org/
Vendor:         bww bitwise works GmbH

%scm_source     github https://github.com/bitwiseworks/%{name}-os2 %{version}-3-os2

BuildRequires:  gcc
%if ! 0%{?_module_build}
BuildRequires:  doxygen
%endif
BuildRequires:  openssl-devel
BuildRequires:  python-devel

# Due to fixed socketpair (note: the fix is in static lib)
BuildRequires: libc-devel >= 1:0.1.7

%description
The libevent API provides a mechanism to execute a callback function
when a specific event occurs on a file descriptor or after a timeout
has been reached. libevent is meant to replace the asynchronous event
loop found in event driven network servers. An application just needs
to call event_dispatch() and can then add or remove events dynamically
without having to change the event loop.

%package devel
Summary: Development files for %{name}
License: BSD
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files and libraries for developing
with %{name}.

%package doc
Summary: Development documentation for %{name}
# The files sample/openssl_hostname_validation.{c,h} and sample/hostcheck.{c,h}
# are MIT. The rest is BSD.
License: BSD and MIT
BuildArch: noarch

%description doc
This package contains the development documentation for %{name}.

%prep
%scm_setup
autogen.sh

%build
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx -lpthread"

%configure \
    --disable-dependency-tracking --disable-static

# Set BUILDLEVEL to be embedded to all DLLs built with Libtool.
export LT_BUILDLEVEL="@#%{vendor}:%{version}-%{release}#@##1## `LANG=C date +'%%d %%b %%Y %%H:%%M:%%S'`     `uname -n`::::0::"

make %{?_smp_mflags} all

%if ! 0%{?_module_build}
# Create the docs
make doxygen
%endif

%install
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

# not on OS/2, so disabled
%if !0%{?os2_version}
# Fix multilib install of devel (bug #477685)
mv $RPM_BUILD_ROOT%{_includedir}/event2/event-config.h \
   $RPM_BUILD_ROOT%{_includedir}/event2/event-config-%{__isa_bits}.h
cat > $RPM_BUILD_ROOT%{_includedir}/event2/event-config.h << EOF
#include <bits/wordsize.h>

#if __WORDSIZE == 32
#include <event2/event-config-32.h>
#elif __WORDSIZE == 64
#include <event2/event-config-64.h>
#else
#error "Unknown word size"
#endif
EOF
%endif

%if ! 0%{?_module_build}
mkdir -p $RPM_BUILD_ROOT/%{develdocdir}/html
(cd doxygen/html; \
	install -p -m 644 *.* $RPM_BUILD_ROOT/%{develdocdir}/html)
%endif

mkdir -p $RPM_BUILD_ROOT/%{develdocdir}/sample
(cd sample; \
	install -p -m 644 *.c *.am $RPM_BUILD_ROOT/%{develdocdir}/sample)

%check
# Tests fail due to nameserver not running locally
# [msg] Nameserver 127.0.0.1:38762 has failed: request timed out.
# On some architects this error is ignored on others it is not.
#make check

#ldconfig_scriptlets

%files
%license LICENSE
%doc ChangeLog
%{_libdir}/evnt*.dll

%files devel
%{_includedir}/event.h
%{_includedir}/evdns.h
%{_includedir}/evhttp.h
%{_includedir}/evrpc.h
%{_includedir}/evutil.h
%dir %{_includedir}/event2
%{_includedir}/event2/*.h
%{_libdir}/event*_dll.a
%{_libdir}/pkgconfig/libevent.pc
%{_libdir}/pkgconfig/libevent_core.pc
%{_libdir}/pkgconfig/libevent_extra.pc
%{_libdir}/pkgconfig/libevent_openssl.pc
%{_libdir}/pkgconfig/libevent_pthreads.pc
%{_bindir}/event_rpcgen.*

%files doc
%doc %{develdocdir}/

%changelog
* Fri Feb 26 2021 Dmitriy Kuminov <coding@dmik.org> - 2.1.11-4
- Rebuild against libc 0.1.7 to fix faulty socketpair errors.

* Thu Dec 31 2020 Dmitriy Kuminov <coding@dmik.org> - 2.1.11-3
- Remove OS/2 specific EBADF hack from select_dispatch [#2].

* Wed Mar 11 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.1.11-2
- fix a wrong if in the spec

* Fri Feb 28 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.1.11-1
- first OS/2 rpm version
