%if !0%{?os2_version}
%global cache /var/cache/man
%else
%global cache %{_var}/cache/man
%endif
%global gnulib_ver 20140202

%if !0%{?os2_version}
%global use_cron 1
%global use_systemd 1
%global systemdtmpfilesdir /usr/lib/tmpfiles.d
%else
%global use_cron 0
%global use_systemd 0
%global systemdtmpfilesdir %{_usr}/lib/tmpfiles.d
%endif

Summary: Tools for searching and reading man pages
Name: man-db
Version: 2.7.6.1
Release: 4%{?dist}
# GPLv2+ .. man-db
# GPLv3+ .. gnulib
License: GPLv2+ and GPLv3+
Group: System Environment/Base
URL: http://www.nongnu.org/man-db/

%if !0%{?os2_version}
Source0: http://download.savannah.gnu.org/releases/%{name}/%{name}-%{version}.tar.xz
Source1: man-db.crondaily
Source2: man-db.sysconfig
Patch0: man-db-2.7.6.1-change-owner-of-man-cache.patch

# http://lists.nongnu.org/archive/html/man-db-devel/2017-01/msg00013.html
Patch1: man-db-2.7.6.1-fix-override-dir-handling.patch
%else
Vendor: bww bitwise works GmbH
%scm_source github https://github.com/bitwiseworks/%{name}-os2 %{version}-os2-3
%endif

Obsoletes: man < 2.0
Provides: man = %{version}
Provides: man-pages-reader = %{version}
%if !0%{?os2_version}
# FPC exception for gnulib - copylib - https://fedorahosted.org/fpc/ticket/174
Provides: bundled(gnulib) = %{gnulib_ver}
%endif

Requires: coreutils, grep, groff-base, gzip, less
Requires: libiconv-utils
%if !0%{?os2_version}
BuildRequires: gdbm-devel, gettext, groff, less, libpipeline-devel, zlib-devel
%else
BuildRequires: db4-devel, gettext, groff, less, libpipeline-devel, zlib-devel
Requires: db4 >= 4.8.30-8
Requires: libpipeline >= 1.4.1-2
BuildRequires: automake, autoconf, gcc
BuildRequires: os2-rpm >= 3.0
%endif
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

%if 0%{?os2_version}
%debug_package
%endif

%prep
%if !0%{?os2_version}
%autosetup -p1
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
# Raise stack to 8 MB to avoid SYS3171 (https://github.com/bitwiseworks/man-db-os2/issues/4)
#  -Zstack 8192
export LDFLAGS="$LDFLAGS -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
export VENDOR="%{vendor}"
%endif
%configure \
%if 0%{?os2_version}
    --enable-inprocess-manpages \
%endif    
    --with-systemdtmpfilesdir=%{systemdtmpfilesdir} \
    --with-sections="1 1p 8 2 3 3p 4 5 6 7 9 0p n l p o 1x 2x 3x 4x 5x 6x 7x 8x" \
    --disable-setuid --enable-cache-owner=root \
    --with-browser=elinks --with-lzip=lzip \
    --with-override-dir=overrides
make CC="%{__cc} %{optflags}" %{?_smp_mflags} V=1

%check
make check

%install
make install DESTDIR=$RPM_BUILD_ROOT prefix=%{_prefix} INSTALL='install -p'

# move the documentation to the relevant place
mv $RPM_BUILD_ROOT%{_datadir}/doc/man-db/* ./

# remove zsoelim man page - part of groff package
rm $RPM_BUILD_ROOT%{_datadir}/man/man1/zsoelim.1

# remove libtool archives
rm $RPM_BUILD_ROOT%{_libdir}/*.la
%if 0%{?os2_version}
rm $RPM_BUILD_ROOT%{_libdir}/*.a
%endif

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

%if %{use_systemd}
# config for tmpfiles.d
install -D -p -m 0644 init/systemd/man-db.conf $RPM_BUILD_ROOT%{systemdtmpfilesdir}/.

# man-db-cache-update.service
install -D -p -m 0644 %{SOURCE3} $RPM_BUILD_ROOT%{_unitdir}/man-db-cache-update.service
%else
rm -rf $RPM_BUILD_ROOT%{systemdtmpfilesdir}
%endif

%find_lang %{name}
%if !0%{?os2_version}
find_lang %{name}-gnulib
%endif

# stop and disable timer from previous builds
%pre
%if !0%{?os2_version}
if [ -e /usr/lib/systemd/system/mandb.timer ]; then
  if test -d /run/systemd; then
	systemctl stop man-db.timer
	systemctl -q disable man-db.timer
  fi
fi
%endif

# clear the old cache
%post
%{__rm} -rf %{cache}/*

# update cache
%transfiletriggerin -- %{_mandir}
MAN_NO_LOCALE_WARNING=1 %{_bindir}/mandb -q

# update cache
%transfiletriggerpostun -- %{_mandir}
MAN_NO_LOCALE_WARNING=1 %{_bindir}/mandb -q

%if !0%{?os2_version}
%files -f %{name}.lang -f %{name}-gnulib.lang
%else
%files -f %{name}.lang
%endif
%{!?_licensedir:%global license %%doc}
%license docs/COPYING
%doc README man-db-manual.txt man-db-manual.ps ChangeLog NEWS
%config(noreplace) %{_sysconfdir}/man_db.conf
%if %{use_cron}
%config(noreplace) %{_sysconfdir}/sysconfig/man-db
%endif
%if %{use_systemd}
%config(noreplace) %{systemdtmpfilesdir}/man-db.conf
%endif
%{_sbindir}/accessdb%{_exeext}
%{_bindir}/man%{_exeext}
%{_bindir}/whatis%{_exeext}
%{_bindir}/apropos
%{_bindir}/manpath%{_exeext}
%{_bindir}/lexgrog%{_exeext}
%{_bindir}/catman%{_exeext}
%{_bindir}/mandb%{_exeext}
%{_libdir}/*%{_shlibext}
%dir %{_libexecdir}/man-db
%{_libexecdir}/man-db/globbing%{_exeext}
%{_libexecdir}/man-db/manconv%{_exeext}
%{_libexecdir}/man-db/zsoelim%{_exeext}
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
* Thu Nov 26 2026 Dmitrii Kuminov <coding@dmik.org> - 2.7.6.1-4
- Build from tag 2.7.6.1-os2-3
- Resync with Fedora spec @ af41171 (2.7.6.1-5)
- Add proper OS/2 ifdefs for changed parts where appropriate
- Replace ChangeLog with a link to GitHub
- BuildRequire Automake and Autoconf for autoreconf
- BuildRequire os2-rpm >= 3.0 for various addons (also drags in newer rpm)
- Raise stack to 8 MB to avoid SYS3171
- Require libpipeline >= 1.4.1-2 for O_BINARY fixes
- Enable check (tests)

* Wed Dec 05 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.7.6.1-3
- add a require for at least db4 4.8.30-8 (ticket #322)

* Mon Nov 19 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.7.6.1-2
- fix a crlf issue

* Mon Nov 12 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.7.6.1-1
- Initial version
