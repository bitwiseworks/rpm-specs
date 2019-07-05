
%global gnulib_ver 20140202

Summary: A pipeline manipulation library
Name: libpipeline
Version: 1.4.1
Release: 1%{?dist}
License: GPLv3+
Group: Development/Libraries
URL: http://libpipeline.nongnu.org/

Vendor: bww bitwise works GmbH
%scm_source github https://github.com/bitwiseworks/libpipeline-os2 %{version}-os2

BuildRequires: libtool, check-devel

# FPC exception for gnulib - copylib - https://fedorahosted.org/fpc/ticket/174
#Provides: bundled(gnulib) = %{gnulib_ver}

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

%description devel
libpipeline-devel contains the header files and libraries needed
to develop programs that use libpipeline library.

%prep
%scm_setup

# create the changelog
# is is a bit a nasty hack, but it's needed for now.
# the date will probably not change, but better check makefile.am
# the srcdir needs to be adjusted to the current build env
%define gen_start_date 2013-11-30 21:08
%define srcdir e:/Trees/libpipeline/git
build-aux/gitlog-to-changelog --format='%s%n%n%b%n' \
    --since="%{gen_start_date}" --srcdir=%{srcdir} > cl-t
rm -f ChangeLog
mv cl-t ChangeLog

# Regenerate configure
autoreconf -ivf

%build
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
export VENDOR="%{vendor}"

%{configure}
make %{?_smp_mflags}

%check
#make check

%install
make install DESTDIR=$RPM_BUILD_ROOT prefix=%{_prefix} INSTALL='install -p'
rm $RPM_BUILD_ROOT/%{_libdir}/libpipeline.la

#%post -p /sbin/ldconfig

#%postun -p /sbin/ldconfig

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc README ChangeLog NEWS
%{_libdir}/*.dll

%files devel
%{_libdir}/*_dll.a
%{_libdir}/pkgconfig/libpipeline.pc
%{_includedir}/*.h
%{_mandir}/man3/*

%changelog
* Mon Apr 03 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.4.1-1
- first rpm version
