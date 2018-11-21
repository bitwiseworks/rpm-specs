%global cache /@unixroot/var/cache/man
%global gnulib_ver 20140202
%global use_cron 0
%global systemdtmpfilesdir /@unixroot/usr/lib/tmpfiles.d

Summary: Tools for searching and reading man pages
Name: man-db
Version: 2.7.6.1
Release: 2%{?dist}
# GPLv2+ .. man-db
# GPLv3+ .. gnulib
License: GPLv2+ and GPLv3+
Group: System Environment/Base
URL: http://www.nongnu.org/man-db/

Vendor: bww bitwise works GmbH
%scm_source github https://github.com/bitwiseworks/%{name}-os2 %{version}-os2-2
#scm_source git file://e:/Trees/man-db/git master-os2

Obsoletes: man < 2.0
Provides: man = %{version}
Provides: man-pages-reader = %{version}
# FPC exception for gnulib - copylib - https://fedorahosted.org/fpc/ticket/174
#Provides: bundled(gnulib) = %{gnulib_ver}

Requires: coreutils, grep, groff-base, gzip, less
Requires: libiconv-utils
BuildRequires: db4-devel, gettext, groff, less, libpipeline-devel, zlib-devel
#BuildRequires: gdbm-devel
BuildRequires: po4a, perl, perl-version

%description
The man-db package includes five tools for browsing man-pages:
man, whatis, apropos, manpath and lexgrog. man formats and displays
manual pages. whatis searches the manual page names. apropos searches the
manual page names and descriptions. manpath determines search path
for manual pages. lexgrog directly reads header information in
manual pages.

%if %{use_cron}
%package cron
Summary: Periodic update of man-db cache
Group: System Environment/Base

Requires: %{name} = %{version}-%{release}
Requires: crontabs

BuildArch: noarch

%description cron
This package provides periodic update of man-db cache.
%endif

%debug_package

%prep
%scm_setup

# create the changelog
# is is a bit a nasty hack, but it's needed for now.
# the date will probably not change, but better check makefile.am
# the srcdir needs to be adjusted to the current build env
%define gen_start_date 2013-12-09 00:52
%define srcdir e:/Trees/man-db/git
build-aux/gitlog-to-changelog --format='%s%n%n%b%n' \
    --since="%{gen_start_date}" --srcdir=%{srcdir} > cl-t
rm -f ChangeLog
mv cl-t ChangeLog

autoreconf -fvi

%build
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
export VENDOR="%{vendor}"

%configure \
    --with-systemdtmpfilesdir=%{systemdtmpfilesdir} \
    --with-sections="1 1p 8 2 3 3p 4 5 6 7 9 0p n l p o 1x 2x 3x 4x 5x 6x 7x 8x" \
    --disable-setuid --enable-cache-owner=root \
    --with-browser=elinks --with-lzip=lzip \
    --with-override-dir=overrides
make CC="%{__cc} %{optflags}" %{?_smp_mflags} V=1

%check
#make check

%install
make install DESTDIR=$RPM_BUILD_ROOT prefix=%{_prefix} INSTALL='install -p'

# move the documentation to the relevant place
mv $RPM_BUILD_ROOT%{_datadir}/doc/man-db/* ./

# remove zsoelim man page - part of groff package
rm $RPM_BUILD_ROOT%{_datadir}/man/man1/zsoelim.1

# remove libtool archives
rm $RPM_BUILD_ROOT%{_libdir}/*.la
# remove archives
rm $RPM_BUILD_ROOT%{_libdir}/*.a

# install cache directory
install -d -m 0755  $RPM_BUILD_ROOT/%{cache}

%if %{use_cron}
# install cron script for man-db creation/update
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/cron.daily
install -D -p -m 0755 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/cron.daily/man-db.cron

# config for cron script
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
install -D -p -m 0644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/man-db
%endif

# config for tmpfiles.d
#install -D -p -m 0644 init/systemd/man-db.conf $RPM_BUILD_ROOT%{systemdtmpfilesdir}/.
rm -rf $RPM_BUILD_ROOT%{systemdtmpfilesdir}

# man-db-cache-update.service
#install -D -p -m 0644 %{SOURCE3} $RPM_BUILD_ROOT%{_unitdir}/man-db-cache-update.service

%find_lang %{name}
#find_lang %{name}-gnulib

# stop and disable timer from previous builds
%pre
#if [ -e /usr/lib/systemd/system/mandb.timer ]; then
#  if test -d /run/systemd; then
#	systemctl stop man-db.timer
#	systemctl -q disable man-db.timer
#  fi
#fi

# clear the old cache
%post
%{__rm} -rf %{cache}/*

# update cache
%transfiletriggerin -- %{_mandir}
MAN_NO_LOCALE_WARNING=1 /@unixroot/usr/bin/mandb -q

# update cache
%transfiletriggerpostun -- %{_mandir}
MAN_NO_LOCALE_WARNING=1 /@unixroot/usr/bin/mandb -q

%files -f %{name}.lang
# -f %{name}-gnulib.lang
%{!?_licensedir:%global license %%doc}
%license docs/COPYING
%doc README man-db-manual.txt man-db-manual.ps ChangeLog NEWS
%config(noreplace) %{_sysconfdir}/man_db.conf
%if %{use_cron}
%config(noreplace) %{_sysconfdir}/sysconfig/man-db
%endif
#%config(noreplace) %{systemdtmpfilesdir}/man-db.conf
%{_sbindir}/accessdb.exe
%{_bindir}/man.exe
%{_bindir}/whatis.exe
%{_bindir}/apropos
%{_bindir}/manpath.exe
%{_bindir}/lexgrog.exe
%{_bindir}/catman.exe
%{_bindir}/mandb.exe
%{_libdir}/*.dll
%dir %{_libexecdir}/man-db
%{_libexecdir}/man-db/globbing.exe
%{_libexecdir}/man-db/manconv.exe
%{_libexecdir}/man-db/zsoelim.exe
%attr(2755,root,man) %verify(not mtime) %dir %{cache}
# documentation and translation
%{_mandir}/man1/apropos.1*
%{_mandir}/man1/lexgrog.1*
%{_mandir}/man1/man.1*
%{_mandir}/man1/manconv.1*
%{_mandir}/man1/manpath.1*
%{_mandir}/man1/whatis.1*
%{_mandir}/man5/manpath.5*
%{_mandir}/man8/accessdb.8*
%{_mandir}/man8/catman.8*
%{_mandir}/man8/mandb.8*
%lang(da)   %{_datadir}/man/da/man*/*
%lang(de)   %{_datadir}/man/de/man*/*
%lang(es)   %{_datadir}/man/es/man*/*
%lang(fr)   %{_datadir}/man/fr/man*/*
%lang(id)   %{_datadir}/man/id/man*/*
%lang(it)   %{_datadir}/man/it/man*/*
%lang(ja)   %{_datadir}/man/ja/man*/*
%lang(nl)   %{_datadir}/man/nl/man*/*
%lang(pl)   %{_datadir}/man/pl/man*/*
%lang(ru)   %{_datadir}/man/ru/man*/*
%lang(sv)   %{_datadir}/man/sv/man*/*
%lang(zh_CN)   %{_datadir}/man/zh_CN/man*/*

%changelog
* Mon Nov 19 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.7.6.1-2
- fix a crlf issue

* Mon Nov 12 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.7.6.1-1
- Initial version
