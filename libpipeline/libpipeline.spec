%global gnulib_ver 20140202

Summary: A pipeline manipulation library
Name: libpipeline
Version: 1.4.1
Release: 2%{?dist}
License: GPLv3+
Group: Development/Libraries
URL: http://libpipeline.nongnu.org/
%if !0%{?os2_version}
Source: http://download.savannah.gnu.org/releases/libpipeline/libpipeline-%{version}.tar.gz
%else
Vendor: bww bitwise works GmbH
%scm_source github https://github.com/bitwiseworks/libpipeline-os2 %{version}-os2-1
%endif

BuildRequires: libtool, check-devel

%if !0%{?os2_version}
# FPC exception for gnulib - copylib - https://fedorahosted.org/fpc/ticket/174
Provides: bundled(gnulib) = %{gnulib_ver}
%endif

%description
libpipeline is a C library for setting up and running pipelines of
processes, without needing to involve shell command-line parsing which is
often error-prone and insecure. This alleviates programmers of the need to
laboriously construct pipelines using lower-level primitives such as fork(2)
and execve(2).

%package devel
Summary: Header files and libraries for pipeline manipulation library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig
%if 0%{?os2_version}
BuildRequires: automake, autoconf, gcc
BuildRequires: os2-rpm >= 3.0
%endif

%description devel
libpipeline-devel contains the header files and libraries needed
to develop programs that use libpipeline library.

%prep
%if !0%{?os2_version}
%setup -q
%else
%scm_setup
%endif

%if 0%{?os2_version}
# Create a dummy ChangeLog with a GitHub link
echo "Please visit %{__source_url}/commits/%{__source_rev}" > ChangeLog
autoreconf -fvi
%endif

%build
%if 0%{?os2_version}
export LDFLAGS="$LDFLAGS -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
export VENDOR="%{vendor}"
%endif
%{configure}
make %{?_smp_mflags}

%check
make check

%install
make install DESTDIR=$RPM_BUILD_ROOT prefix=%{_prefix} INSTALL='install -p'
rm $RPM_BUILD_ROOT/%{_libdir}/libpipeline.la

%if !0%{?os2_version}
%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig
%endif

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc README ChangeLog NEWS
%{_libdir}/*%{_shlibextmask}

%files devel
%{_libdir}/*%{_implibext}
%{_libdir}/pkgconfig/libpipeline.pc
%{_includedir}/*.h
%{_mandir}/man3/*

%changelog
* Thu Nov 26 2026 Dmitrii Kuminov <coding@dmik.org> 1.4.1-2
- Build from tag 1.4.1-os2-1
- Resync with Fedora spec @ d34bc55 (1.4.1-3)
- Add proper OS/2 ifdefs for changed parts where appropriate
- Replace ChangeLog with a link to GitHub
- BuildRequire Automake and Autoconf for autoreconf
- BuildRequire os2-rpm >= 3.0 for various addons (also drags in newer rpm)
- Enable check (tests)

* Mon Apr 03 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.4.1-1
- first rpm version
