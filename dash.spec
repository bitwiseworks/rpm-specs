# Note: this .spec is borrowed from dash-0.5.8-2.fc23.src.rpm

# Disable debug symbols stuff - makes no sense w/o EXCEPTQ support
# (also depends on http://trac.netlabs.org/rpm/ticket/134)
%define _strip_no_debuginfo 1

Name:           dash
Version:        0.5.8
Release:        1%{?dist}
Summary:        Small and fast POSIX-compliant shell
Group:          System Environment/Shells
# BSD: DASH in general
# GPLv2+: From src/mksignames.c
# Public Domain: From src/bltin/test.c
# Copyright only: From src/hetio.h
License:        BSD and GPLv2+ and Public Domain and Copyright only
URL:            http://gondor.apana.org.au/~herbert/%{name}/
#Source0:        http://gondor.apana.org.au/~herbert/%{name}/files/%{name}-%{version}.tar.gz

%define svn_url     http://svn.netlabs.org/repos/ports/dash/trunk
%define svn_rev     1126

Source: %{name}-%{version}-r%{svn_rev}.zip

BuildRequires: gcc make subversion zip

BuildRequires: automake

%description
DASH is a POSIX-compliant implementation of /bin/sh that aims to be as small as
possible. It does this without sacrificing speed where possible. In fact, it is
significantly faster than bash (the GNU Bourne-Again SHell) for most tasks.

%package sh
Summary:  Installs DASH as the system default POSIX shell.
Requires: dash
# @todo See http://trac.netlabs.org/rpm/ticket/137.
Provides: /@unixroot/bin/sh

%description sh
Virtual package that installs DASH as the system default POSIX shell.

%prep
%if %{?svn_rev:%(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')}%{!?svn_rev):0}
%setup -q
%else
%setup -n "%{name}-%{version}" -Tc
svn export %{?svn_rev:-r %{svn_rev}} %{svn_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip" "%{name}-%{version}")
%endif

# Generate configure and friends
autogen.sh

%build

# Disable job control, OS/2 tty doesn't allow this
export CFLAGS='-DJOBS=0'

# Usual link options
export LDFLAGS='-Zomf -Zmap -Zhigh-mem -Zargs-wild -Zargs-resp' # -Zbin-files
export LD=emxomfld

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
%{_mandir}/man1/%{name}.1

%files sh
%{_bindir}/sh
%{_bindir}/sh.exe
%{_mandir}/man1/sh.1

%changelog
* Mon Apr 6 2015 Dmitriy Kuminov <coding@dmik.org> 0.5.8-1
- Initial package for version 0.5.8.
