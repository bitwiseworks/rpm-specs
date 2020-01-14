%global with_single 0
%global with_colors 0
%global with_tests  0

%if %{with_single}
%global types separate single
%else
%global types separate
%endif

Summary: A set of basic GNU tools commonly used in shell scripts
Name:    coreutils
Version: 8.31
Release: 1%{?dist}
License: GPLv3+
Url:     https://www.gnu.org/software/coreutils/

Vendor:  bww bitwise works GmbH

%scm_source github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2

%if %{with_single}
# do not make coreutils-single depend on /usr/bin/coreutils
%global __requires_exclude ^%{_bindir}/coreutils$
%endif

Conflicts: filesystem < 3
# To avoid clobbering installs
%if %{with_single}
Conflicts: coreutils-single
%endif

#BuildRequires: attr
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: gcc
BuildRequires: gettext-devel
BuildRequires: gmp-devel
#BuildRequires: hostname
#BuildRequires: libacl-devel
#BuildRequires: libattr-devel
#BuildRequires: libcap-devel
#BuildRequires: libselinux-devel
#BuildRequires: libselinux-utils
BuildRequires: openssl-devel
#BuildRequires: strace
BuildRequires: texinfo

%if 23 < 0%{?fedora} || 7 < 0%{?rhel}
# needed by i18n test-cases
BuildRequires: glibc-langpack-en
%endif

Requires: %{name}-common = %{version}-%{release}
Requires: ncurses

Provides: coreutils-full = %{version}-%{release}
Obsoletes: %{name} < 8.24-100

%description
These are the GNU core utilities.  This package is the combination of
the old GNU fileutils, sh-utils, and textutils packages.

%if %{with_single}
%package single
Summary:  coreutils multicall binary
Suggests: coreutils-common
Provides: coreutils = %{version}-%{release}
Provides: coreutils%{?_isa} = %{version}-%{release}
# To avoid clobbering installs
Conflicts: coreutils < 8.24-100
# Note RPM doesn't support separate buildroots for %files
# http://rpm.org/ticket/874 so use RemovePathPostfixes
# (new in rpm 4.13) to support separate file sets.
RemovePathPostfixes: .single

%description single
These are the GNU core utilities,
packaged as a single multicall binary.
%endif


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
%scm_setup
%if %{with_colors}
# will be modified by coreutils-8.25-DIR_COLORS.patch
tee DIR_COLORS{,.256color,.lightbgcolor} <src/dircolors.hin >/dev/null
# git add DIR_COLORS{,.256color,.lightbgcolor}
# git commit -m "clone DIR_COLORS before patching"
%endif


%if %{with_tests}
(echo ">>> Fixing permissions on tests") 2>/dev/null
find tests -name '*.sh' -perm 0644 -print -exec chmod 0755 '{}' '+'
(echo "<<< done") 2>/dev/null
%endif

autoreconf -fiv


%build
export VENDOR="%{vendor}"
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lintl -lcx"
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
%{expand:%%global optflags %{optflags} -D_GNU_SOURCE=1}

# we only do a separate build
for type in %{types}; do
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


%check
%if %{with_tests}
for type in separate single; do
  test $type = 'single' && subdirs='SUBDIRS=.' # Only check gnulib once
  (cd $type && make check %{?_smp_mflags} $subdirs)
done
%endif

%install
for type in %{types}; do
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

%if %{with_colors}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
install -p -c -m644 DIR_COLORS{,.256color,.lightbgcolor} \
    $RPM_BUILD_ROOT%{_sysconfdir}
install -p -c -m644 %SOURCE105 $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/colorls.sh
install -p -c -m644 %SOURCE106 $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/colorls.csh
%endif

# {env,cut,readlink} were previously moved from /usr/bin to /bin and linked into
# this is os/2 specific
for i in env cut readlink; do ln -sf /@unixroot/usr/bin/$i.exe $RPM_BUILD_ROOT/@unixroot/usr/bin/$i; done

# yd move conflicting tools to libexec/bin and place a symlink for script compatibility
mkdir -p $RPM_BUILD_ROOT%{_libexecdir}/bin
for i in dir date sort hostid; do
  mv $RPM_BUILD_ROOT%{_bindir}/$i.exe $RPM_BUILD_ROOT%{_libexecdir}/bin/$i.exe
  ln -s %{_libexecdir}/bin/$i.exe $RPM_BUILD_ROOT%{_bindir}/$i
done

%find_lang %name
# Add the %%lang(xyz) ownership for the LC_TIME dirs as well...
grep LC_TIME %name.lang | cut -d'/' -f1-6 | sed -e 's/) /) %%dir /g' >>%name.lang

# (sb) Deal with Installed (but unpackaged) file(s) found
rm -f $RPM_BUILD_ROOT%{_infodir}/dir


%files
%_bindir/*
%_sbindir/chroot.exe
%{_libexecdir}/*
%exclude %{_bindir}/*.dbg
%exclude %{_sbindir}/*.dbg
%exclude %{_libexecdir}/bin/*.dbg


%if %{with_single}
%files single
%{_bindir}/*.single
%{_sbindir}/chroot.single
%dir %{_libexecdir}/coreutils
%{_libexecdir}/coreutils/*.so.single
# duplicate the license because coreutils-common does not need to be installed
%{!?_licensedir:%global license %%doc}
%license COPYING
%endif


%files common -f %{name}.lang
%if %{with_colors}
%config(noreplace) %{_sysconfdir}/DIR_COLORS*
%config(noreplace) %{_sysconfdir}/profile.d/*
%endif
%{_infodir}/coreutils*
%{_mandir}/man*/*
# The following go to /usr/share/doc/coreutils-common
%doc ABOUT-NLS NEWS README THANKS TODO
%license COPYING


%changelog
* Mon Dec 09 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> - 8.31-1
- update to version 8.31
- fix ticket #1
- merge spec with fedora one

* Wed Jan 23 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> - 8.26-3
- enable install-info
- remove Work around sort stdn close failure (#145), as fixed in libc now

* Thu Feb 23 2017 Dmitriy Kuminov <coding@dmik.org> - 8.26-2
- Use scm_source and friends.
- Work around sort stdn close failure (#145).

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
