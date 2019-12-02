%global with_check 0

Summary: The GNU macro processor
Name: m4
Version: 1.4.18
Release: 1%{?dist}
License: GPLv3+
URL: http://www.gnu.org/software/m4/

Vendor: bww bitwise works GmbH
%scm_source github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2

BuildRequires: gcc autoconf automake
%ifarch ppc ppc64
BuildRequires: texinfo
%endif

%description
A GNU implementation of the traditional UNIX macro processor.  M4 is
useful for writing text files which can be logically parsed, and is used
by many programs as part of their build process.  M4 has built-in
functions for including files, running shell commands, doing arithmetic,
etc.  The autoconf program needs m4 for generating configure scripts, but
not for running configure scripts.

Install m4 if you need a macro processor.

%debug_package

%prep
%scm_setup

#chmod 644 COPYING

%build
export LDFLAGS="-Zomf -Zhigh-mem -Zargs-wild -Zargs-resp"
export LIBS="-lcx -lintl"
export VENDOR="%{vendor}"

autoreconf -ivf

%configure

make %{?_smp_mflags}

%install
%make_install
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%check
%if %{with_check}
make %{?_smp_mflags} check
%endif

%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README THANKS TODO
%{_bindir}/m4.exe
%{_infodir}/*
%{_mandir}/man1/m4.1*


%changelog
* Mon Dec 02 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.4.18-1
- updated to version 1.4.18
- cleanup of the spec and use scm_* macros

* Wed Sep 03 2014 yd
- added debug package with symbolic info for exceptq.

* Wed Sep 3 2014 Dmitriy Kuminov <coding@dmik.org> 1.4.17-2
- Rebuild with autoconf 2.69-2.

* Fri Aug 29 2014 Dmitriy Kuminov <coding@dmik.org> 1.4.17-1
- Updated to version 1.4.17.
- Rebuilt with LIBC 0.6.5 and GCC 4.7.3 in attempt to fix some problems (see #28).

* Fri Jan 06 2012 yd
- update trunk to 1.4.16










