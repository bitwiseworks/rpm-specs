#define svn_url     e:/trees/coreutils/trunk
%define svn_url     http://svn.netlabs.org/repos/ports/coreutils/trunk
%define svn_rev     1954

Summary: A set of basic GNU tools commonly used in shell scripts
Name:    coreutils
Version: 8.26
Release: 1%{?dist}
License: GPLv3+
Group:   System Environment/Base
Url:     http://www.gnu.org/software/coreutils/

Vendor:  bww bitwise works GmbH
Source:  %{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip

#BuildRequires: libselinux-devel
#BuildRequires: libacl-devel
BuildRequires: gettext bison
BuildRequires: texinfo
BuildRequires: autoconf
BuildRequires: automake
#BuildRequires: libcap-devel
#BuildRequires: libattr-devel
BuildRequires: openssl-devel
BuildRequires: gmp-devel
#BuildRequires: attr
#BuildRequires: strace

Requires: %{name}-common = %{version}-%{release}
#Requires(pre): /sbin/install-info
#Requires(preun): /sbin/install-info
#Requires(post): /sbin/install-info
Requires(post): grep
Requires:       ncurses

Provides: fileutils = %{version}-%{release}
Provides: sh-utils = %{version}-%{release}
Provides: stat = %{version}-%{release}
Provides: textutils = %{version}-%{release}
#old mktemp package had epoch 3, so we have to use 4 for coreutils
Provides: mktemp = 4:%{version}-%{release}
Provides: bundled(gnulib)
Obsoletes: mktemp < 4:%{version}-%{release}
Obsoletes: fileutils <= 4.1.9
Obsoletes: sh-utils <= 2.0.12
Obsoletes: stat <= 3.3
Obsoletes: textutils <= 2.0.21
Obsoletes: %{name} < 8.24-100

%description
These are the GNU core utilities.  This package is the combination of
the old GNU fileutils, sh-utils, and textutils packages.

%package common
# yum obsoleting rules explained at:
# https://bugzilla.redhat.com/show_bug.cgi?id=1107973#c7
Obsoletes: %{name} < 8.24-100
Summary:  coreutils common optional components

%description common
Optional though recommended components,
including documentation and translations.

%debug_package

%prep
%if %{?svn_rev:%(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')}%{!?svn_rev):0}
%setup -q
%else
%setup -n "%{name}-%{version}" -Tc
svn export %{?svn_rev:-r %{svn_rev}} %{svn_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip" "%{name}-%{version}")
%endif

#chmod a+x tests/misc/sort-mb-tests.sh tests/df/direct.sh || :

#fix typos/mistakes in localized documentation(#439410, #440056)
#find ./po/ -name "*.p*" | xargs \
# sed -i \
# -e 's/-dpR/-cdpR/'

%build

export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lintl -lcx"
%{expand:%%global optflags %{optflags} -D_GNU_SOURCE=1}
# we do autoreconf even fedora doesn't do it
autoreconf -i -v

# we only do a separate build
#for type in separate single; do
for type in separate; do
  mkdir $type && \
  (cd $type && ln -s ../configure || exit 1
  if test $type = 'single'; then
    config_single='--enable-single-binary'
    config_single="$config_single --without-openssl"  # smaller/slower sha*sum
    config_single="$config_single --without-gmp"      # expr/factor machine ints
  else
    config_single='--with-openssl'  # faster sha*sum
  fi
  %configure $config_single \
             --cache-file=../config.cache \
             --enable-largefile \
             --enable-install-program=arch \
             --with-tty-group \
             DEFAULT_POSIX2_VERSION=200112 alternative=199209 || :

  make all %{?_smp_mflags})
done


#%check
#for type in separate single; do
#  test $type = 'single' && subdirs='SUBDIRS=.' # Only check gnulib once
#  (cd $type && make check %{?_smp_mflags} $subdirs)
#done

%install
#for type in separate single; do
for type in separate; do
  install=install
  if test $type = 'single'; then
    subdir=%{_libexecdir}/%{name}; install=install-exec
  fi
  (cd $type && make DESTDIR=$RPM_BUILD_ROOT/$subdir $install)

  # chroot was in /usr/sbin :
  mkdir -p $RPM_BUILD_ROOT/$subdir/%{_bindir}
  mkdir -p $RPM_BUILD_ROOT/$subdir/%{_sbindir}
  mv $RPM_BUILD_ROOT/$subdir/%{_bindir}/chroot.exe $RPM_BUILD_ROOT/$subdir/%{_sbindir}/chroot.exe

  # Move multicall variants to *.single.
  # RemovePathPostfixes will strip that later.
  if test $type = 'single'; then
    for dir in %{_bindir} %{_sbindir} %{_libexecdir}/%{name}; do
      for bin in $RPM_BUILD_ROOT/%{_libexecdir}/%{name}/$dir/*; do
        basebin=$(basename $bin)
        mv $bin $RPM_BUILD_ROOT/$dir/$basebin.single
      done
    done
  fi
done

# fix japanese catalog file
if [ -d $RPM_BUILD_ROOT%{_datadir}/locale/ja_JP.EUC/LC_MESSAGES ]; then
   mkdir -p $RPM_BUILD_ROOT%{_datadir}/locale/ja/LC_MESSAGES
   mv $RPM_BUILD_ROOT%{_datadir}/locale/ja_JP.EUC/LC_MESSAGES/*mo \
      $RPM_BUILD_ROOT%{_datadir}/locale/ja/LC_MESSAGES
   rm -rf $RPM_BUILD_ROOT%{_datadir}/locale/ja_JP.EUC
fi

bzip2 -9f ChangeLog

# {env,cut,readlink} were previously moved from /usr/bin to /bin and linked into
# this is os/2 specific
for i in env cut readlink; do ln -sf /@unixroot/usr/bin/$i.exe $RPM_BUILD_ROOT/@unixroot/usr/bin/$i; done

# yd move conflicting tools to libexec/bin and place a symlink for script compatibility
mkdir -p $RPM_BUILD_ROOT%{_libexecdir}/bin
for i in dir date sort hostid; do
  mv $RPM_BUILD_ROOT%{_bindir}/$i.exe $RPM_BUILD_ROOT%{_libexecdir}/bin/$i.exe
  ln -s %{_libexecdir}/bin/$i.exe $RPM_BUILD_ROOT%{_bindir}/$i
done

# These come from util-linux and/or procps.
# With coreutils > 8.24 one can just add to --enable-no-install-program
# rather than manually removing here, since tests depending on
# built utilities are correctly skipped if not present.
#for i in kill ; do
#    rm -f $RPM_BUILD_ROOT{%{_bindir}/$i,%{_mandir}/man1/$i.1}
#    rm -f $RPM_BUILD_ROOT%{_bindir}/$i.single
#done

# Compress ChangeLogs from before the fileutils/textutils/etc merge
bzip2 -f9 old/*/C*

# Use hard links instead of symbolic links for LC_TIME files (bug #246729).
#find %{buildroot}%{_datadir}/locale -type l | \
#(while read link
# do
#   target=$(readlink "$link")
#   rm -f "$link"
#   ln "$(dirname "$link")/$target" "$link"
# done)

%find_lang %name

# (sb) Deal with Installed (but unpackaged) file(s) found
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
rm -f $RPM_BUILD_ROOT%{_usr}/lib/charset.alias

%clean
rm -rf $RPM_BUILD_ROOT

%pre
# We must deinstall these info files since they're merged in
# coreutils.info. else their postun'll be run too late
# and install-info will fail badly because of duplicates
#for file in sh-utils textutils fileutils; do
#  if [ -f %{_infodir}/$file.info.gz ]; then
#    /sbin/install-info --delete %{_infodir}/$file.info.gz --dir=%{_infodir}/dir &> /dev/null || :
#  fi
#done

%preun
#if [ $1 = 0 ]; then
#  if [ -f %{_infodir}/%{name}.info.gz ]; then
#    /sbin/install-info --delete %{_infodir}/%{name}.info.gz %{_infodir}/dir || :
#  fi
#fi

%post
#%{_bindir}/grep -v '(sh-utils)\|(fileutils)\|(textutils)' %{_infodir}/dir > \
#  %{_infodir}/dir.rpmmodify || exit 0
#    /bin/mv -f %{_infodir}/dir.rpmmodify %{_infodir}/dir
#if [ -f %{_infodir}/%{name}.info.gz ]; then
#  /sbin/install-info %{_infodir}/%{name}.info.gz %{_infodir}/dir || :
#fi

%files
%defattr(-,root,root,-)
%_bindir/*
%_sbindir/chroot.exe
%{_libexecdir}/*
%exclude %{_bindir}/*.dbg
%exclude %{_sbindir}/*.dbg
%exclude %{_libexecdir}/bin/*.dbg

%files common -f %{name}.lang
%defattr(-,root,root,-)
#%config(noreplace) %{_sysconfdir}/DIR_COLORS*
#%config(noreplace) %{_sysconfdir}/profile.d/*
%{_infodir}/coreutils*
%{_mandir}/man*/*
# The following go to /usr/share/doc/coreutils-common
%doc ABOUT-NLS COPYING NEWS README THANKS TODO

%changelog
* Fri Jan 27 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> - 8.26-1
- update coreutils to version 8.26
- set stdout to binary in base64

* Mon Dec 05 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 8.25-4
- fix a rm break with deep directories

* Mon Sep 12 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 8.25-3
- remove -ZBin-files

* Tue Sep 06 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 8.25-2
- fix scriplet errors when using dash as shell

* Tue Jul 12 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 8.25-1
- updated coreutils to version 8.25
- changed debug handling
- added direct svn export

* Sat Mar 15 2014 yd
- fixed libexec dir for symlinks.
- added debug package with symbolic info for exceptq.

* Wed Jul 24 2013 yd
- move conflicting tools to libexec/bin.

* Mon Feb 18 2013 yd
- same change for sort/hostid tools.

* Wed Jan 30 2013 yd
- rename sort.exe to sort-unix.exe and add symlink.

* Thu Feb 02 2012 yd
- Remove symlinks from /bin.

* Sun Nov 20 2011 yd
- fixed chown/chgrp, wildcard expansion for ls/touch.

* Fri Nov 18 2011 yd
- restored env symlink and others (python wants them).

* Wed Nov 16 2011 yd
- rename dir.exe to dir-unix.exe and add symlink
- keep all executables to /usr/bin and place symlinks in /bin
