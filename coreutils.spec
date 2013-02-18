%define nopam 1

Summary: A set of basic GNU tools commonly used in shell scripts
Name:    coreutils
Version: 8.6
Release: 9%{?dist}
License: GPLv3+
Group:   System Environment/Base
Url:     http://www.gnu.org/software/coreutils/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0: ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz
Source1: coreutils-chown-os2.c

Patch1: coreutils-os2.diff

#BuildRequires: libselinux-devel
#BuildRequires: libacl-devel
BuildRequires: gettext bison
#BuildRequires: texinfo
#BuildRequires: autoconf
#BuildRequires: automake
#%{?!nopam:BuildRequires: pam-devel}
#BuildRequires: libcap-devel
#BuildRequires: libattr-devel
BuildRequires: gmp-devel
#BuildRequires: attr
#BuildRequires: strace

#Requires:       libattr
#Requires(post): grep
%{?!nopam:Requires: pam }
#Requires(post): libcap
Requires:       ncurses
Requires:       gmp
#Requires: %{name}-libs = %{version}-%{release}

Provides: fileutils = %{version}-%{release}
Provides: sh-utils = %{version}-%{release}
Provides: stat = %{version}-%{release}
Provides: textutils = %{version}-%{release}
#old mktemp package had epoch 3, so we have to use 4 for coreutils
Provides: mktemp = 4:%{version}-%{release}
Obsoletes: mktemp < 4:%{version}-%{release}
Obsoletes: fileutils <= 4.1.9
Obsoletes: sh-utils <= 2.0.12
Obsoletes: stat <= 3.3
Obsoletes: textutils <= 2.0.21

%description
These are the GNU core utilities.  This package is the combination of
the old GNU fileutils, sh-utils, and textutils packages.

#%package libs
#Summary: Libraries for %{name}
#Group: System Environment/Libraries
#Requires: %{name} = %{version}-%{release}

#%description libs
#Libraries for coreutils package.

%prep
%setup -q

%patch1 -p1 -b .os2~

cp %{SOURCE1} lib/chown-os2.c

#chmod a+x tests/misc/sort-mb-tests

#fix typos/mistakes in localized documentation(#439410, #440056)
#find ./po/ -name "*.p*" | xargs \
# sed -i \
# -e 's/-dpR/-cdpR/'

%build

export CONFIG_SHELL="/@unixroot/usr/bin/sh"
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
export LDFLAGS="-Zbin-files -Zhigh-mem -Zomf"
export LIBS="-lintl -lurpo"

%{expand:%%global optflags %{optflags} -D_GNU_SOURCE=1}
#autoreconf -i -v
#touch aclocal.m4 configure config.hin Makefile.in */Makefile.in
#aclocal -I m4
#autoconf --force
#automake --copy --add-missing
%configure \
           --includedir=/usr/include \
           --without-gmp \
           --enable-largefile \
           --enable-install-program=su.exe,hostname.exe,arch \
           --with-tty-group \
           "--cache-file=%{_topdir}/cache/%{name}-%{_target_cpu}.cache" \
           DEFAULT_POSIX2_VERSION=200112 alternative=199209 || :

# Regenerate manpages
#touch man/*.x

make all %{?_smp_mflags} \
         %{?!nopam:CPPFLAGS="-DUSE_PAM"} \
         su_LDFLAGS="-pie %{?!nopam:-lpam -lpam_misc}"

# XXX docs should say /var/run/[uw]tmp not /etc/[uw]tmp
sed -i -e 's,/etc/utmp,/var/run/utmp,g;s,/etc/wtmp,/var/run/wtmp,g' doc/coreutils.texi

#%check
#make check

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

# man pages are not installed with make install
#make mandir=$RPM_BUILD_ROOT%{_mandir} install-man

# fix japanese catalog file
if [ -d $RPM_BUILD_ROOT%{_datadir}/locale/ja_JP.EUC/LC_MESSAGES ]; then
   mkdir -p $RPM_BUILD_ROOT%{_datadir}/locale/ja/LC_MESSAGES
   mv $RPM_BUILD_ROOT%{_datadir}/locale/ja_JP.EUC/LC_MESSAGES/*mo \
      $RPM_BUILD_ROOT%{_datadir}/locale/ja/LC_MESSAGES
   rm -rf $RPM_BUILD_ROOT%{_datadir}/locale/ja_JP.EUC
fi

bzip2 -9f ChangeLog

# let be compatible with old fileutils, sh-utils and textutils packages :
mkdir -p $RPM_BUILD_ROOT%{_sbindir}
%{?!nopam:mkdir -p $RPM_BUILD_ROOT%_sysconfdir/pam.d}

# chroot was in /usr/sbin :
mv $RPM_BUILD_ROOT%_bindir/chroot.exe $RPM_BUILD_ROOT%_sbindir/chroot.exe

# {env,cut,readlink} were previously moved from /usr/bin to /bin and linked into
for i in env cut readlink; do ln -sf /@unixroot/usr/bin/$i.exe $RPM_BUILD_ROOT/@unixroot/usr/bin/$i; done

#mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
#install -p -c -m644 %SOURCE101 $RPM_BUILD_ROOT%{_sysconfdir}/DIR_COLORS
#install -p -c -m644 %SOURCE102 $RPM_BUILD_ROOT%{_sysconfdir}/DIR_COLORS.lightbgcolor
#install -p -c -m644 %SOURCE103 $RPM_BUILD_ROOT%{_sysconfdir}/DIR_COLORS.256color
#install -p -c -m644 %SOURCE105 $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/colorls.sh
#install -p -c -m644 %SOURCE106 $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/colorls.csh

# yd rename dir.exe to dir-unix.exe and place a symlink for script compatibility
mv $RPM_BUILD_ROOT%_bindir/dir.exe $RPM_BUILD_ROOT%_bindir/dir-unix.exe
ln -s /@unixroot/usr/bin/dir-unix.exe $RPM_BUILD_ROOT%_bindir/dir

# yd rename date.exe to date-unix.exe and place a symlink for script compatibility
mv $RPM_BUILD_ROOT%_bindir/date.exe $RPM_BUILD_ROOT%_bindir/date-unix.exe
ln -s /@unixroot/usr/bin/date-unix.exe $RPM_BUILD_ROOT%_bindir/date

# yd rename sort.exe to sort-unix.exe and place a symlink for script compatibility
mv $RPM_BUILD_ROOT%_bindir/sort.exe $RPM_BUILD_ROOT%_bindir/sort-unix.exe
ln -s /@unixroot/usr/bin/sort-unix.exe $RPM_BUILD_ROOT%_bindir/sort

# yd rename hostid.exe to hostid-unix.exe and place a symlink for script compatibility
mv $RPM_BUILD_ROOT%_bindir/hostid.exe $RPM_BUILD_ROOT%_bindir/hostid-unix.exe
ln -s /@unixroot/usr/bin/hostid-unix.exe $RPM_BUILD_ROOT%_bindir/hostid

# su
install -m 4755 src/su.exe $RPM_BUILD_ROOT/@unixroot/usr/bin
#install -m 755 src/runuser $RPM_BUILD_ROOT/sbin
# do not ship runuser in /usr/bin/runuser
#rm -rf $RPM_BUILD_ROOT/usr/bin/runuser

# These come from util-linux and/or procps.
#for i in hostname uptime kill ; do
#    rm $RPM_BUILD_ROOT{%_bindir/$i,%_mandir/man1/$i.1}
#done

#%{?!nopam:install -p -m 644 %SOURCE200 $RPM_BUILD_ROOT%_sysconfdir/pam.d/su}
#%{?!nopam:install -p -m 644 %SOURCE202 $RPM_BUILD_ROOT%_sysconfdir/pam.d/su-l}
#%{?!nopam:install -p -m 644 %SOURCE201 $RPM_BUILD_ROOT%_sysconfdir/pam.d/runuser}
#%{?!nopam:install -p -m 644 %SOURCE203 $RPM_BUILD_ROOT%_sysconfdir/pam.d/runuser-l}

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

#%find_lang %name

# (sb) Deal with Installed (but unpackaged) file(s) found
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
rm -f $RPM_BUILD_ROOT%{_usr}/lib/charset.alias

%clean
rm -rf $RPM_BUILD_ROOT

%files
# -f %{name}.lang
%defattr(-,root,root,-)
#%config(noreplace) %{_sysconfdir}/DIR_COLORS*
#%config(noreplace) %{_sysconfdir}/profile.d/*
#%{?!nopam:%config(noreplace) %{_sysconfdir}/pam.d/su}
#%{?!nopam:%config(noreplace) %{_sysconfdir}/pam.d/su-l}
#%{?!nopam:%config(noreplace) %{_sysconfdir}/pam.d/runuser}
#%{?!nopam:%config(noreplace) %{_sysconfdir}/pam.d/runuser-l}
%doc COPYING ABOUT-NLS ChangeLog.bz2 NEWS README THANKS TODO old/*
%_bindir/*
%_infodir/coreutils*
#%_mandir/man*/*
%_sbindir/chroot.exe
#/@unixroot/sbin/runuser.exe
%{_datadir}/locale/*

#%files libs
#%defattr(-, root, root, -)
#%{_libdir}/coreutils

%changelog
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
