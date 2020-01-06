Name: libdaemon
Version: 0.14
Release: 1%{?dist}
Summary: Library for writing UNIX daemons
License: LGPLv2+
URL: http://0pointer.de/lennart/projects/libdaemon/
Vendor: bww bitwise works GmbH
%scm_source github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2 

# Requires lynx to build the docs
BuildRequires:  gcc
#BuildRequires:  lynx

%description
libdaemon is a lightweight C library which eases the writing of UNIX daemons.
It consists of the following parts:
* A wrapper around fork() which does the correct daemonization
  procedure of a process
* A wrapper around syslog() for simpler and compatible log output to
  Syslog or STDERR
* An API for writing PID files
* An API for serializing UNIX signals into a pipe for usage with
  select() or poll()
* An API for running subprocesses with STDOUT and STDERR redirected
  to syslog.

%package devel
Summary: Libraries and header files for libdaemon development
Requires: libdaemon = %{version}-%{release}

%description devel
The libdaemon-devel package contains the header files and libraries
necessary for developing programs using libdaemon.

%prep
%scm_setup
autoreconf -fvi

%build
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
export VENDOR="%{vendor}"

%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

# remove not installed files
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

rm -f $RPM_BUILD_ROOT/%{_datadir}/doc/libdaemon/README
rm -f $RPM_BUILD_ROOT/%{_datadir}/doc/libdaemon/README.html
rm -f $RPM_BUILD_ROOT/%{_datadir}/doc/libdaemon/style.css

#ldconfig_scriptlets

%files
%defattr(-,root,root)
%doc LICENSE README
%{_libdir}/*.dll

%files devel
%defattr(-,root,root)
%doc doc/README.html doc/style.css
%{_includedir}/*
%{_libdir}/*_dll.a
%{_libdir}/pkgconfig/*.pc

%changelog
* Mon Jan 06 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.14-1
- first rpm version
