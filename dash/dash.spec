# Note: this .spec is borrowed from dash-0.5.8-2.fc23.src.rpm

Name:           dash
Version:        0.5.10.2
Release:        1%{?dist}
Summary:        Small and fast POSIX-compliant shell
Group:          System Environment/Shells
# BSD: DASH in general
# GPLv2+: From src/mksignames.c
# Public Domain: From src/bltin/test.c
# Copyright only: From src/hetio.h
License:        BSD and GPLv2+ and Public Domain and Copyright only
URL:            http://gondor.apana.org.au/~herbert/%{name}/
Vendor:         bww bitwise works GmbH

%scm_source github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2

BuildRequires: gcc make git zip

BuildRequires: automake
BuildRequires: exceptq-devel

%description
DASH is a POSIX-compliant implementation of /bin/sh that aims to be as small as
possible. It does this without sacrificing speed where possible. In fact, it is
significantly faster than bash (the GNU Bourne-Again SHell) for most tasks.

%package sh
Summary:  Installs DASH as the system default POSIX shell.
Requires: dash
# @todo See http://trac.netlabs.org/rpm/ticket/137.
Provides: /@unixroot/bin/sh
Provides: sh
Obsoletes: ash-sh

%description sh
Virtual package that installs DASH as the system default POSIX shell.

%debug_package

%prep
%scm_setup

# Generate configure and friends
autogen.sh

%build

# Disable job control, OS/2 tty doesn't allow this
export CFLAGS="$RPM_OPT_FLAGS -DJOBS=0"

# Usual link options
export LDFLAGS="-Zomf -Zmap -Zhigh-mem -Zargs-wild -Zargs-resp"

# Use LIBCx for EXCEPTQ handler
export LIBS="-lcx"

# We install dash into /usr/bin, so no --bindir=/bin
%configure

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

# Create a symlink for the default shell
ln -s %{_bindir}/%{name}.exe %{buildroot}%{_bindir}/sh
cp -p %{buildroot}%{_bindir}/%{name}.exe %{buildroot}%{_bindir}/sh.exe
ln -s %{_mandir}/man1/%{name}.1 %{buildroot}%{_mandir}/man1/sh.1

#%post
#grep -q '^/bin/dash$' %{_sysconfdir}/shells || \
#    echo '/bin/dash' >> %{_sysconfdir}/shells

#%postun
#if [ $1 -eq 0 ]; then
#    sed -i '/^\/bin\/dash$/d' %{_sysconfdir}/shells
#fi

%files
%doc COPYING ChangeLog
%{_bindir}/%{name}.exe
%{_mandir}/man1/%{name}.1*

%files sh
%{_bindir}/sh
%{_bindir}/sh.exe
%{_mandir}/man1/sh.1*

%changelog
* Mon Nov 11 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> 0.5.10.2-1
- Update to version 0.5.10.2
- Use scm_ macros
- dash-sh now provides sh as well

* Fri Aug 17 2018 Dmitriy Kuminov <coding@dmik.org> 0.5.9.1-2
- Add support for BEGINLIBPATH and friends (#161).
- Fix broken `cd x:` command (#163).

* Mon Nov 28 2016 Dmitriy Kuminov <coding@dmik.org> 0.5.9.1-1
- Update to version 0.5.9.1.
- Increase stack size to 8 MB to fix crashes with too big here-docs.
- Link against LIBCx 0.4.
- Build with standard platform-specific optimization (also improves
  debug symbols due to -g when compiling).

* Tue Sep 6 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> 0.5.9-2
- rebuilt with new libc (paths.h changes)

* Mon Aug 8 2016 Dmitriy Kuminov <coding@dmik.org> 0.5.9-1
- Update to version 0.5.9.
- Make cd builtin handle paths like /@unixroot correctly.
- Convert backslashes to forward ones in PATH-like variables
  (PATHLIKE_VARS may be used to extend list of recognized ones).
- Be more verbose on fork failures.
- Add support for EXCEPTQ and debug info package.
- The dash-sh package now obsoletes ash-sh for easy update
  (ash is deprecated from now on).

* Mon Apr 6 2015 Dmitriy Kuminov <coding@dmik.org> 0.5.8-1
- Initial package for version 0.5.8.
