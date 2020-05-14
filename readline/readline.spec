Summary: A library for editing typed command lines
Name: readline
Version: 8.0
Release: 1%{?dist}
License: GPLv3+
URL: https://tiswww.case.edu/php/chet/readline/rltop.html
Vendor: bww bitwise works GmbH
%scm_source github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2

BuildRequires: gcc
BuildRequires: ncurses-devel

%description
The Readline library provides a set of functions that allow users to
edit command lines. Both Emacs and vi editing modes are available. The
Readline library includes additional functions for maintaining a list
of previously-entered command lines for recalling or editing those
lines, and for performing csh-like history expansion on previous
commands.

%package devel
Summary: Files needed to develop programs which use the readline library
Requires: %{name} = %{version}-%{release}

%description devel
The Readline library provides a set of functions that allow users to
edit typed command lines. If you want to develop programs that will
use the readline library, you need to have the readline-devel package
installed. You also need to have the readline package installed.

%package static
Summary: Static libraries for the readline library
Requires: %{name}-devel = %{version}-%{release}

%description static
The readline-static package contains the static version of the readline
library.

%legacy_runtime_packages

%debug_package

%prep
%scm_setup
autoreconf -fvi

%build
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"
export VENDOR="%{vendor}"
%configure --with-curses --disable-install-examples
make %{?_smp_mflags}

%install
%make_install

rm -vrf %{buildroot}%{_docdir}/readline
rm -vf %{buildroot}%{_infodir}/dir*

%if !0%{?os2_version}
%ldconfig_scriptlets
%endif

%files
%license COPYING USAGE
%{_libdir}/readln8.dll
%{_libdir}/histor8.dll
%{_infodir}/history.info*
%{_infodir}/rluserman.info*

%files devel
%doc CHANGES NEWS README
%doc examples/*.c examples/*.h examples/rlfe
%{_includedir}/readline/
%{_libdir}/libreadline_dll.a
%{_libdir}/libhistory_dll.a
%{_libdir}/pkgconfig/%{name}.pc
%{_mandir}/man3/readline.3*
%{_mandir}/man3/history.3*
%{_infodir}/readline.info*

%files static
%{_libdir}/libreadline.a
%{_libdir}/libhistory.a

%changelog
* Thu May 14 2020 Silvan Scherrer <silvan.scherrer@ara.ch> 8.0-1
- update to version 8.0
- sync with latest fedora spec
- use scm_macros
- add legacy package to the old version 6.1-4

* Mon Jan 16 2012 yd <yuri.dario@os2power.com> 6.1-4
- rebuild with libc 0.6.4 runtime.

