# Note: http://pkgs.fedoraproject.org/cgit/rpms/rpm.git/tree/rpm.spec?id=cef3bf822054a87f8f8ae53a31f4af9b3d88359b

# build against xz?
%bcond_without xz
# just for giggles, option to build with internal Berkeley DB
%bcond_with int_bdb
# run internal testsuite?
%bcond_without check

%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%define rpmhome %{_libdir}/rpm

%define rpmver 4.13.0
%define snapver %{nil}
%define srcver %{rpmver}

%define bdbver 4.8.24
%define dbprefix db

Summary: The RPM package management system
Name: rpm
Version: %{rpmver}
Release: 13%{?dist}
Group: System Environment/Base
Url: http://www.rpm.org/

%scm_source svn http://svn.netlabs.org/repos/rpm/rpm/trunk 1027

# Partially GPL/LGPL dual-licensed and some bits with BSD
# SourceLicense: (GPLv2+ and LGPLv2+ with exceptions) and BSD
License: GPLv2+

Requires: coreutils
%if %{without int_bdb}
# db recovery tools, rpmdb_util symlinks
Requires: db4-utils
%endif
Requires: popt >= 1.10.2.1
Requires: curl
Requires: rpm-libs = %{version}-%{release}
Requires: pthread >= 20151207
Requires: cpio
Requires: cube
Requires: sed

Provides: rpm-macros-warpin
Provides: rpm-macros-wps

BuildRequires: rexx_exe

%if %{without int_bdb}
BuildRequires: db4-devel
%endif

%if %{with check}
#BuildRequires: fakechroot
%endif

# XXX generally assumed to be installed but make it explicit as rpm
# is a bit special...
#BuildRequires: gawk
BuildRequires: readline-devel zlib-devel
BuildRequires: nss-devel
# The popt version here just documents an older known-good version
BuildRequires: popt-devel >= 1.10.2
BuildRequires: file-devel
BuildRequires: gettext-devel gettext-common-devel
BuildRequires: ncurses-devel
BuildRequires: bzip2-devel >= 0.9.0c-2
# YD because of ucs4
BuildRequires: python-devel >= 2.7.6-13
BuildRequires: libcx-devel
#BuildRequires: lua-devel >= 5.1
%if ! %{without xz}
BuildRequires: xz-devel >= 4.999.8
%endif

%description
The RPM Package Manager (RPM) is a powerful command line driven
package management system capable of installing, uninstalling,
verifying, querying, and updating software packages. Each software
package consists of an archive of files along with information about
the package like its version, a description, etc.

%package libs
Summary:  Libraries for manipulating RPM packages
Group: Development/Libraries
License: GPLv2+ and LGPLv2+ with exceptions
Requires: rpm = %{version}-%{release}

# We need a fork-friendly PR_LoadLibrary on OS/2
Requires: nspr >= 4.12.0-2

%description libs
This package contains the RPM shared libraries.

%package devel
Summary:  Development files for manipulating RPM packages
Group: Development/Libraries
License: GPLv2+ and LGPLv2+ with exceptions
Requires: rpm = %{version}-%{release}
Requires: popt-devel
Requires: file-devel

%description devel
This package contains the RPM C library and header files. These
development files will simplify the process of writing programs that
manipulate RPM packages and databases. These files are intended to
simplify the process of creating graphical package managers or any
other tools that need an intimate knowledge of RPM packages in order
to function.

This package should be installed if you want to develop programs that
will manipulate RPM packages and databases.

%package build
Summary: Scripts and executable programs used to build packages
Group: Development/Tools
Requires: rpm = %{version}-%{release}
#Requires: elfutils >= 0.128 binutils
Requires: findutils sed grep gawk diffutils
Requires: file patch >= 2.5
Requires: unzip xz
Requires: gzip bzip2 cpio
Requires: pkgconfig >= 1:0.24
Requires: tar
#Conflicts: ocaml-runtime < 3.11.1-7

%description build
The rpm-build package contains the scripts and executable programs
that are used to build packages using the RPM Package Manager.

%package python
Summary: Python bindings for apps which will manipulate RPM packages
Group: Development/Libraries
Requires: rpm = %{version}-%{release}
# YD because of ucs4
Requires: python >= 2.7.6-13

%description python
The rpm-python package contains a module that permits applications
written in the Python programming language to use the interface
supplied by RPM Package Manager libraries.

This package should be installed if you want to develop Python
programs that will manipulate RPM packages and databases.

%package apidocs
Summary: API documentation for RPM libraries
Group: Documentation
BuildArch: noarch

%description apidocs
This package contains API documentation for developing applications
that will manipulate RPM packages and databases.

%package cron
Summary: Create daily logs of installed packages.
Group: System Environment/Base
BuildArch: noarch
Requires: crontabs logrotate rpm = %{version}-%{release}

%description cron
This package contains a cron job which creates daily logs of installed
packages on a system.

%debug_package

%prep
%scm_setup

%if %{with int_bdb}
ln -s db-%{bdbver} db
%endif

%build

# Make default paths to tools start with /@unixroot on OS/2
sed -i \
  -e '/AC_PATH_PROGS\?(/ {
    s#, \?/usr/#, /@unixroot/usr/# ;
    s#, \?/bin/#, /@unixroot/usr/bin/# ;
    s#, \?/sbin/#, /@unixroot/usr/sbin/# ;
  }' \
  configure.ac

autoreconf -i -f

# Make tools we don't yet have in OS/2 RPMs pathless
export ac_cv_path___SSH=ssh

# Using configure macro has some unwanted side-effects on rpm platform
# setup, use the old-fashioned way for now only defining minimal paths.
export LDFLAGS="-Zbin-files -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lintl -lcx"
export CPPFLAGS="$CPPFLAGS `pkg-config --cflags nss`"
%configure \
    --enable-shared --disable-static --without-lua \
    %{!?with_int_bdb: --with-external-db} \
    --without-archive \
    --enable-python

make %{?_smp_mflags} V=1

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR="$RPM_BUILD_ROOT" install

# Remove OS/2 import libraries from plugins
rm ${RPM_BUILD_ROOT}%{_libdir}/rpm-plugins/*_dll.a

# No /bin on OS/2
mv ${RPM_BUILD_ROOT}/@unixroot/bin/rpm.exe ${RPM_BUILD_ROOT}%{_bindir}/rpm.exe

# Remove elf attr magic (makes no sense on OS/2)
rm ${RPM_BUILD_ROOT}%{rpmhome}/fileattrs/elf.attr

# Replace OS/2 paths with /@unixroot and /@system_drive
sed -i \
  -e 's#[^a-zA-Z][a-zA-Z]:/ecs/#/@system_drive/ecs/#gi' \
  -e 's#[^a-zA-Z][a-zA-Z]:/tcpip/bin/#/@system_drive/tcpip/bin/#gi' \
  ${RPM_BUILD_ROOT}%{rpmhome}/macros

# Check there are no paths starting with drive letter or having usr/local
! grep -q \
  -e '[^a-zA-Z][a-zA-Z]:/' \
  -e '/usr/local' \
  ${RPM_BUILD_ROOT}%{rpmhome}/macros

# Pack OS/2 Rexx scripts
for f in wps-object warpin-conflicts ; do
  rexx2vio "${RPM_BUILD_ROOT}%{rpmhome}/$f.cmd" "${RPM_BUILD_ROOT}%{rpmhome}/$f.exe"
  rm "${RPM_BUILD_ROOT}%{rpmhome}/$f.cmd"
  sed -i "s#$f.cmd#$f.exe#gi" ${RPM_BUILD_ROOT}%{rpmhome}/macros
done

# Save list of packages through cron
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/cron.daily
install -m 755 scripts/rpm.daily ${RPM_BUILD_ROOT}%{_sysconfdir}/cron.daily/rpm

mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d
install -m 644 scripts/rpm.log ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d/rpm

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rpm

mkdir -p $RPM_BUILD_ROOT%{_var}/lib/rpm
for dbi in \
    Basenames Conflictname Dirnames Group Installtid Name Packages \
    Providename Provideversion Requirename Requireversion Triggername \
    Filedigests Pubkeys Sha1header Sigmd5 Obsoletename \
    __db.001 __db.002 __db.003 __db.004 __db.005 __db.006 __db.007 \
    __db.008 __db.009
do
    touch $RPM_BUILD_ROOT%{_var}/lib/rpm/$dbi
done

# plant links to db utils as rpmdb_foo so existing documantion is usable
%if %{without int_bdb}
for dbutil in \
    archive deadlock dump load printlog \
    recover stat upgrade verify
do
    ln -s ../../bin/%{dbprefix}_${dbutil} $RPM_BUILD_ROOT/%{rpmhome}/rpmdb_${dbutil}
done
%endif

%find_lang %{name}

find $RPM_BUILD_ROOT -name "*.la"|xargs rm -f

# avoid dragging in tonne of perl libs for an unused script
#chmod 0644 $RPM_BUILD_ROOT/%{rpmhome}/perldeps.pl

# compress our ChangeLog, it's fairly big...
bzip2 -9 ChangeLog

%clean
rm -rf $RPM_BUILD_ROOT

#%if %{with check}
#%check
#make check
#[ "$(ls -A tests/rpmtests.dir)" ] && cat tests/rpmtests.log
#%endif

#%post libs -p /sbin/ldconfig
#%postun libs -p /sbin/ldconfig

#%posttrans
# XXX this is klunky and ugly, rpm itself should handle this
#dbstat=/usr/lib/rpm/rpmdb_stat
#if [ -x "$dbstat" ]; then
#    if "$dbstat" -e -h %{_var}/lib/rpm 2>&1 | grep -q "doesn't match environment version \| Invalid argument"; then
#        rm -f %{_var}/lib/rpm/__db.*
#    fi
#fi
#exit 0

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc GROUPS COPYING CREDITS ChangeLog.bz2 doc/manual/[a-z]*
%dir %{_sysconfdir}/rpm

%attr(0755, root, root) %dir %{_var}/lib/rpm
%attr(0644, root, root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) %{_var}/lib/rpm/*
%attr(0755, root, root) %dir %{rpmhome}

%{_bindir}/rpm.exe
%{_bindir}/rpm2cpio.exe
%{_bindir}/rpmdb.exe
%{_bindir}/rpmkeys.exe
%{_bindir}/rpmsign.exe
%{_bindir}/rpmquery
%{_bindir}/rpmverify

%{_mandir}/man8/rpm.8*
%{_mandir}/man8/rpmdb.8*
%{_mandir}/man8/rpmkeys.8*
%{_mandir}/man8/rpm2cpio.8*

# XXX this places translated manuals to wrong package wrt eg rpmbuild
%lang(fr) %{_mandir}/fr/man[18]/*.[18]*
%lang(ko) %{_mandir}/ko/man[18]/*.[18]*
%lang(ja) %{_mandir}/ja/man[18]/*.[18]*
%lang(pl) %{_mandir}/pl/man[18]/*.[18]*
%lang(ru) %{_mandir}/ru/man[18]/*.[18]*
%lang(sk) %{_mandir}/sk/man[18]/*.[18]*

%{rpmhome}/macros
%{rpmhome}/rpmpopt*
%{rpmhome}/rpmrc

%{rpmhome}/rpmdb_*
%{rpmhome}/rpm.daily
%{rpmhome}/rpm.log
%{rpmhome}/rpm.supp
%{rpmhome}/rpm2cpio.sh
%{rpmhome}/tgpg

%{rpmhome}/platform

%{rpmhome}/wps-object.exe
%{rpmhome}/warpin-conflicts.exe

%files libs
%defattr(-,root,root)
%{_libdir}/rpm*.dll
%dir %{_libdir}/rpm-plugins
%{_libdir}/rpm-plugins/*.dll

%files build
%defattr(-,root,root)
%{_bindir}/rpmbuild.exe
%{_bindir}/gendiff
%{_bindir}/rpmspec.exe
%{_bindir}/rpmsign.exe

%{_mandir}/man1/gendiff.1*
%{_mandir}/man8/rpmbuild.8*
%{_mandir}/man8/rpmdeps.8*
%{_mandir}/man8/rpmspec.8*
%{_mandir}/man8/rpmsign.8*

%{rpmhome}/brp-*
%{rpmhome}/check-*
#{rpmhome}/debugedit
#{rpmhome}/find-debuginfo.sh
%{rpmhome}/find-lang.sh
%{rpmhome}/find-legacy-runtime.sh
%{rpmhome}/*provides*
%{rpmhome}/*requires*
%{rpmhome}/*deps*
%{rpmhome}/*.prov
%{rpmhome}/*.req
%{rpmhome}/config.*
%{rpmhome}/macros.p*
%{rpmhome}/fileattrs

%files python
%defattr(-,root,root)
%{_usr}/lib/python*.*/*

%files devel
%defattr(-,root,root)
%_includedir/*
%{_libdir}/rp*[a-z].a
%{_mandir}/man8/rpmgraph.8*
%{_bindir}/rpmgraph.exe
%{_libdir}/pkgconfig/rpm.pc

%files cron
%defattr(-,root,root)
%{_sysconfdir}/cron.daily/rpm
%config(noreplace) %{_sysconfdir}/logrotate.d/rpm

%files apidocs
%defattr(-,root,root)
%doc COPYING doc/librpm/html/*

%changelog
* Fri Feb 24 2017 Dmitriy Kuminov <coding@dmik.org> - 4.13.0-13
- Use proper SVN revision for the build.

* Fri Feb 24 2017 Dmitriy Kuminov <coding@dmik.org> - 4.13.0-12
- Fix install/uninstall scriptlet execution (regression of previous release).
- Make brp-compress support OS/2 (enables compression of man files).

* Thu Feb 23 2017 Dmitriy Kuminov <coding@dmik.org> - 4.13.0-11
- Use scm_source and friends.
- Use OS/2 autoconf instead of pre-generated configure (this also adds ABI suffix to all DLLs).
- Restore using fork (that was replaced by popen) to reduce the number of OS/2-specific hacks.
- Fix executing popt aliases with --pipe (like rpm -qa --last).
- Use common check-files instead of check-files.os2.
- Remove URPO dependency.
- Fix a lot of compiler warnings.
- Fix paths to Tools defined in macros.

* Fri Feb 10 2017 yd <yd@os2power.com> 4.13.0-10
- r978, need scriptlet to run upon uninstall to remove WPS objects. ticket#227.
- r957,969, Auto setup macros for SCM-hosted sources. ticket#232.
- r954, make brp-strip.os2 always create debugfiles.list in top build directory. ticket#230.
- r953,956,972 add legacy runtime packages support. ticket#228.
- r951, replace $RPM_BUILD_NCPUS macro with a better version. fixes ticket#201.
- link with libcx for memory mapping support.

* Tue Jun 14 2016 yd <yd@os2power.com> 4.13.0-9
- r759, remove read-only flag before unlocking modules. fixes ticket#180.

* Thu Jun 09 2016 yd <yd@os2power.com> 4.13.0-8
- rebuild for ucs4, ticket#182.

* Thu Mar 17 2016 yd <yd@os2power.com> 4.13.0-7
- r706, fix full paths in rpmbuild command line.

* Sun Mar 13 2016 yd <yd@os2power.com> 4.13.0-6
- r693, do not try to start NULL scripts. fixes ticket#178.
- r692, disable hard link table building, ticket#172.

* Fri Jan 08 2016 yd <yd@os2power.com> 4.13.0-5
- r639, rpm: check file handle before closing stuffs. ticket#143.

* Fri Jan 08 2016 yd <yd@os2power.com> 4.13.0-4
- add sed as requirement, fixes ticket#162.
- r636, remap /bin to /@unixroot/usr/bin. fixes ticket#137.
- r634-635, replace fork() with popen() when redirecting output. fixes ticket#143.

* Tue Dec 29 2015 yd <yd@os2power.com> 4.13.0-3
- r628, cleanup unused sqlite entries.
- r627, use popen() to replace forking on script execution.

* Tue Dec 15 2015 yd <yd@os2power.com> 4.13.0-2
- r615, standardize debug package creation, ticket#149.

* Tue Dec 08 2015 yd <yd@os2power.com> 4.13.0-1
- r596, ignore KDE macros in find-lang.
- r595, build fixes.
- r594, merge 4.13.0 changes into trunk, build fixes.
- r589, set DB_PRIVATE flag to avoid issues with BDB and incomplete mmapping support.

* Thu Nov 12 2015 yd <yd@os2power.com> 4.8.1-24
- r582, allow use of platform specific macros file. fixes ticket#135.
- r581, standardize debug package creation. fixes ticket#134.

* Wed Feb 25 2015 yd <yd@os2power.com> 4.8.1-23
- r557, backport r536, Make %find_lang macro work on OS/2.
- r558, add support for macros.d directory, fixes ticket#119.
- r536, Make %find_lang macro work on OS/2.

* Fri Jan 30 2015 yd <yd@os2power.com> 4.8.1-22
- r505, define SHELL/CONFIG_SHELL/MAKESHELL automatically for every build.
- r504, ignore colors, they are only used for X86_64 elf linux to mix 32/64 bit code.
- r503, trunk backport, backport, enable short circuit also for -bb build binary packages option.

* Thu Jan 08 2015 yd
- -Zbin-files is not optional...

* Thu Jan 01 2015 yd
- r486, use urpo renameForce() to rename locked databases. ticket#99.
- implement subversion sources checkout.

* Wed Dec 24 2014 yd
- r484, r485, ticket#99.

* Wed Apr 09 2014 yd
- r409, popen() does not recognize unixroot, fixes macro expansion.

* Mon Apr 07 2014 yd
- build for python 2.7.

* Mon Mar 03 2014 yd
- r378 and others, upgrade to vendor 4.11.1, build of debug info packages.

* Thu Mar 28 2013 yd
- r341, fix scripts symlinks.

* Thu Mar 14 2013 yd
- added tool requirements for build package.

* Tue Mar 13 2012 yd
- updated warpin-conflict.cmd, ticket #27, #31.

* Sun Nov 20 2011 yd
- use shell in /usr/bin.

* Fri Nov 18 2011 yd
- keep all executables to /usr/bin and place symlinks in /bin
