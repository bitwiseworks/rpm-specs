# Note: http://pkgs.fedoraproject.org/cgit/rpms/rpm.git/tree/rpm.spec?id=cef3bf822054a87f8f8ae53a31f4af9b3d88359b

# build against xz?
%bcond_without xz
# just for giggles, option to build with internal Berkeley DB
%bcond_with int_bdb
# run internal testsuite?
%bcond_with check
# build with plugins?
%bcond_without plugins
# build with sanitizers?
%bcond_with sanitizer
# build with libarchive? (needed for rpm2archive)
%bcond_with libarchive
# build with libimaevm.so
%bcond_with libimaevm
# build with new db format
%bcond_with ndb
# build with cron?
%global with_cron 0

%define rpmhome %{_libdir}/rpm

%global rpmver 4.13.0
#global snapver rc2
%global srcver %{version}%{?snapver:-%{snapver}}

%define bdbname db4
%define bdbver 5.3.15
%define dbprefix db

Summary: The RPM package management system
Name: rpm
Version: %{rpmver}
Release: %{?snapver:0.%{snapver}.}19%{?dist}
Group: System Environment/Base
Url: http://www.rpm.org/
Vendor: bww bitwise works GmbH

%scm_source svn http://svn.netlabs.org/repos/rpm/rpm/trunk 1657

%if %{with int_bdb}
Source1: db-%{bdbver}.tar.gz
%endif

# Partially GPL/LGPL dual-licensed and some bits with BSD
# SourceLicense: (GPLv2+ and LGPLv2+ with exceptions) and BSD
License: GPLv2+

Requires: coreutils
%if %{without int_bdb}
# db recovery tools, rpmdb_util symlinks
Requires: %{bdbname}-utils
%endif
Requires: popt >= 1.10.2.1
Requires: curl

Requires: rpm-libs = %{version}-%{release}
Requires: pthread >= 20151207

# Due to _fread (see #257) and until #259 is done.
Requires: libcx >= 0.5.3

%if %{without int_bdb}
BuildRequires: %{bdbname}-devel
%endif

%if %{with check}
BuildRequires: fakechroot
%endif

# XXX generally assumed to be installed but make it explicit as rpm
# is a bit special...
#BuildRequires: gawk
BuildRequires: readline-devel zlib-devel
BuildRequires: nss-devel
BuildRequires: nss-softokn-freebl-devel
# The popt version here just documents an older known-good version
BuildRequires: popt-devel >= 1.10.2
BuildRequires: file-devel
BuildRequires: gettext-devel gettext-common-devel
BuildRequires: ncurses-devel
BuildRequires: bzip2-devel >= 0.9.0c-2
# YD because of ucs4
BuildRequires: python-devel >= 2.7.6-13
BuildRequires: libcx-devel
BuildRequires: lua-devel >= 5.1
%if ! %{without xz}
BuildRequires: xz-devel >= 4.999.8
%endif
%if ! %{without libarchive}
BuildRequires: libarchive-devel
%endif
BuildRequires: autoconf automake libtool

%if %{with plugins}
#BuildRequires: dbus-devel
%endif

%if %{with sanitizer}
BuildRequires: libasan
BuildRequires: libubsan
#BuildRequires: liblsan
#BuildRequires: libtsan
%global sanitizer_flags -fsanitize=address -fsanitize=undefined
%endif

%if %{with libimaevm}
BuildRequires: ima-evm-utils
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
Requires: %{name} = %{version}-%{release}

# We need a fork-friendly PR_LoadLibrary on OS/2
Requires: nspr >= 4.12.0-2

%description libs
This package contains the RPM shared libraries.

%package build-libs
Summary:  Libraries for building and signing RPM packages
Group: Development/Libraries
License: GPLv2+ and LGPLv2+ with exceptions
Requires: %{name}-libs = %{version}-%{release}
#Requires: %{_bindir}/gpg2

%description build-libs
This package contains the RPM shared libraries for building and signing
packages.

%package devel
Summary:  Development files for manipulating RPM packages
Group: Development/Libraries
License: GPLv2+ and LGPLv2+ with exceptions
Requires: %{name} = %{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}
Requires: %{name}-build-libs = %{version}-%{release}
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
Requires: binutils
Requires: findutils sed grep gawk diffutils file patch >= 2.5
Requires: tar unzip gzip bzip2 cpio xz
Requires: pkgconfig >= 1:0.24
# Technically rpmbuild doesn't require any external configuration, but
# creating distro-compatible packages does. To make the common case
# "just work" while allowing for alternatives, depend on a virtual
# provide, typically coming from redhat-rpm-config.
#Requires: system-rpm-config
# Techincally rpmbuild doesn't require python3 (and setuptools), but
# pythondistdeps generator expects it.
# See: https://bugzilla.redhat.com/show_bug.cgi?id=1410631
#Requires: python3-setuptools
# TODO On OS/2 we don't provide a separate perl-generators RPM yet.
%if 1
Provides: perl-generators
%endif

%description build
The rpm-build package contains the scripts and executable programs
that are used to build packages using the RPM Package Manager.

%package sign
Summary: Package signing support
Group: System Environment/Base
Requires: rpm-build-libs = %{version}-%{release}

%description sign
This package contains support for digitally signing RPM packages.

%package -n python2-%{name}
Summary: Python 2 bindings for apps which will manipulate RPM packages
Group: Development/Libraries
BuildRequires: python2-devel
%{?python_provide:%python_provide python2-%{name}}
Requires: %{name}-libs = %{version}-%{release}
Provides: %{name}-python = %{version}-%{release}
Obsoletes: %{name}-python < %{version}-%{release}
# YD because of ucs4
Requires: python >= 2.7.6-13

%description -n python2-%{name}
The python2-rpm package contains a module that permits applications
written in the Python programming language to use the interface
supplied by RPM Package Manager libraries.

This package should be installed if you want to develop Python 2
programs that will manipulate RPM packages and databases.

#package -n python3-%{name}
#Summary: Python 3 bindings for apps which will manipulate RPM packages
#Group: Development/Libraries
#BuildRequires: python3-devel
#{?python_provide:%python_provide python3-%{name}}
#{?system_python_abi}
#Requires: %{name}-libs%{?_isa} = %{version}-%{release}
#Provides: %{name}-python3 = %{version}-%{release}
#Obsoletes: %{name}-python3 < %{version}-%{release}

#description -n python3-%{name}
#the python3-rpm package contains a module that permits applications
#written in the Python programming language to use the interface
#supplied by RPM Package Manager libraries.
#
#This package should be installed if you want to develop Python 3
#programs that will manipulate RPM packages and databases.

%package apidocs
Summary: API documentation for RPM libraries
Group: Documentation
BuildArch: noarch

%description apidocs
This package contains API documentation for developing applications
that will manipulate RPM packages and databases.

%if %{with_cron}
%package cron
Summary: Create daily logs of installed packages.
Group: System Environment/Base
BuildArch: noarch
Requires: crontabs logrotate rpm = %{version}-%{release}

%description cron
This package contains a cron job which creates daily logs of installed
packages on a system.
%endif

%debug_package

%if %{with plugins}

%package plugin-syslog
Summary: Rpm plugin for syslog functionality
Group: System Environment/Base
Requires: rpm-libs%{_isa} = %{version}-%{release}

%description plugin-syslog
%{summary}

%package plugin-ima
Summary: Rpm plugin ima file signatures
Group: System Environment/Base
Requires: rpm-libs%{_isa} = %{version}-%{release}

%description plugin-ima
%{summary}

%endif

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

CPPFLAGS="`pkg-config --cflags nss` -DLUA_COMPAT_APIINTCASTS"
CFLAGS="$RPM_OPT_FLAGS %{?sanitizer_flags} -DLUA_COMPAT_APIINTCASTS"
LDFLAGS="%{?__global_ldflags} -Zbin-files -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
LIBS="-lintl -lcx"
export CPPFLAGS CFLAGS LDFLAGS LIBS
export VENDOR="%{vendor}"

autoreconf -i -f

# Make tools we don't yet have in OS/2 RPMs pathless
export ac_cv_path___SSH=ssh

%configure \
    --enable-shared --disable-static \
    %{!?with_int_bdb: --with-external-db} \
    %{!?with_plugins: --disable-plugins} \
    --with-lua \
    %{!?with_libarchive: --without-archive} \
    %{?with_ndb: --with-ndb} \
    --enable-python

make %{?_smp_mflags}

#pushd python
#{__python2} setup.py build
#{__python3} setup.py build
#popd

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR="$RPM_BUILD_ROOT" install

# We need to build with --enable-python for the self-test suite, but we
# actually package the bindings built with setup.py (#531543#c26)
#pushd python
#{__python2} setup.py install --skip-build --root $RPM_BUILD_ROOT
#{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT
#popd

# Remove OS/2 import libraries from plugins
rm ${RPM_BUILD_ROOT}%{_libdir}/rpm-plugins/*_dll.a

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

%if %{with_cron}
# Save list of packages through cron
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/cron.daily
install -m 755 scripts/rpm.daily ${RPM_BUILD_ROOT}%{_sysconfdir}/cron.daily/rpm

mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d
install -m 644 scripts/rpm.log ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d/rpm
%endif

#mkdir -p ${RPM_BUILD_ROOT}/usr/lib/tmpfiles.d
#echo "r /var/lib/rpm/__db.*" > ${RPM_BUILD_ROOT}/usr/lib/tmpfiles.d/rpm.conf

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rpm
mkdir -p $RPM_BUILD_ROOT%{rpmhome}/macros.d

mkdir -p $RPM_BUILD_ROOT%{_var}/lib/rpm
for dbi in \
    Basenames Conflictname Dirnames Group Installtid Name Obsoletename \
    Packages Providename Requirename Triggername Sha1header Sigmd5 \
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
    ln -s %{_bindir}/%{dbprefix}_${dbutil}.exe $RPM_BUILD_ROOT/%{rpmhome}/rpmdb_${dbutil}
done
%endif

%find_lang %{name}

find $RPM_BUILD_ROOT -name "*.la"|xargs rm -f

# TODO On OS/2 we don't provide a separate perl-generators RPM yet.
%if 0
# These live in perl-generators now
rm -f $RPM_BUILD_ROOT/%{rpmhome}/{perldeps.pl,perl.*}
rm -f $RPM_BUILD_ROOT/%{_fileattrsdir}/perl*
%endif
# Axe unused cruft
rm -f $RPM_BUILD_ROOT/%{rpmhome}/{tcl.req,osgideps.pl}

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with check}
%check
make check
[ "$(ls -A tests/rpmtests.dir)" ] && cat tests/rpmtests.log
%endif

%files -f %{name}.lang
%license COPYING
%doc GROUPS CREDITS doc/manual/[a-z]*

#/usr/lib/tmpfiles.d/rpm.conf
%dir %{_sysconfdir}/rpm

%attr(0755, root, root) %dir %{_var}/lib/rpm
%attr(0644, root, root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) %{_var}/lib/rpm/*
%attr(0755, root, root) %dir %{rpmhome}

%{_bindir}/rpm.exe
%{?with_libarchive: %{_bindir}/rpm2archive.exe}
%{_bindir}/rpm2cpio.exe
%{_bindir}/rpmdb.exe
%{_bindir}/rpmkeys.exe
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

%attr(0755, root, root) %dir %{rpmhome}
%{rpmhome}/macros
%{rpmhome}/macros.d
%{rpmhome}/rpmpopt*
%{rpmhome}/rpmrc

%{rpmhome}/rpmdb_*
%{rpmhome}/rpm.daily
%{rpmhome}/rpm.log
%{rpmhome}/rpm.supp
%{rpmhome}/rpm2cpio.sh
%{rpmhome}/tgpg

%{rpmhome}/platform

%dir %{rpmhome}/fileattrs

%files libs
%{_libdir}/rpmio[0-9].dll
%{_libdir}/rpm[0-9].dll
%if %{with plugins}
%dir %{_libdir}/rpm-plugins

%files plugin-syslog
%{_libdir}/rpm-plugins/syslog.dll

%files plugin-ima
%{_libdir}/rpm-plugins/ima.dll
%endif

%files build-libs
%{_libdir}/rpmbuil[0-9].dll
%{_libdir}/rpmsign[0-9].dll

%files build
%{_bindir}/rpmbuild.exe
%{_bindir}/gendiff
%{_bindir}/rpmspec.exe

%{_mandir}/man1/gendiff.1*
%{_mandir}/man8/rpmbuild.8*
%{_mandir}/man8/rpmdeps.8*
%{_mandir}/man8/rpmspec.8*

%{rpmhome}/brp-*
%{rpmhome}/check-*
#{rpmhome}/debugedit
#{rpmhome}/sepdebugcrcfix
#{rpmhome}/find-debuginfo.sh
%{rpmhome}/find-lang.sh
%{rpmhome}/*provides*
%{rpmhome}/*requires*
%{rpmhome}/*deps*
%{rpmhome}/*.prov
%{rpmhome}/*.req
%{rpmhome}/config.*
%{rpmhome}/macros.p*
%{rpmhome}/fileattrs/*
%exclude %{rpmhome}/*.dbg

%files sign
%{_bindir}/rpmsign.exe
%{_mandir}/man8/rpmsign.8*

%files -n python2-%{name}
%{python_sitearch}/%{name}/
%exclude %{python_sitearch}/%{name}/*.dbg
#{python_sitearch}/%{name}_python-*.egg-info

#files -n python3-%{name}
#{python3_sitearch}/%{name}/
#{python3_sitearch}/%{name}_python-*.egg-info

%files devel
%{_mandir}/man8/rpmgraph.8*
%{_bindir}/rpmgraph.exe
%{_libdir}/rp*[a-z].a
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/%{name}/

%if %{with_cron}
%files cron
%{_sysconfdir}/cron.daily/rpm
%config(noreplace) %{_sysconfdir}/logrotate.d/rpm
%endif

%files apidocs
%license COPYING
%doc doc/librpm/html/*

%changelog
* Fri Jun 21 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> 4.13.0-19
- fix ticket #246 (symlinks)
- fix ticket #289 (no cron)
- fix location of rpm.exe

* Fri Mar 29 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> 4.13.0-18
- add buildlevel string
- fix ticket #333

* Mon Jul 10 2017 Dmitriy Kuminov <coding@dmik.org> 4.13.0-17
- Depend on LIBCx 0.5.3 due to _fread override.

* Fri Jun 9 2017 Dmitriy Kuminov <coding@dmik.org> 4.13.0-16
- Make pkgconfig dependency generator work on OS/2 and under [d]ash.
- Greatly simplify/speedup pythondeps.sh and make it pick up .pyd/.exe.
- Move scm_source/scm_setup macros from to os2-rpm-build sub-package.
- Move WPS/WarpIn macros to os2-rpm-build sub-package.
- Move config.sys macros to os2-rpm package.
- Move os2_boot_drive macro to os2-rpm package.
- Remove os2_unixroot_drive macro (superseded by os2_unixroot_path in os2-rpm).

* Thu Apr 6 2017 Dmitriy Kuminov <coding@dmik.org> - 4.13.0-15
- Enable lua scritping.
- Temporarily make rpm-build provide perl-generators for compatibility with Fedora.
- Move some OS/2 specific macros and scripts to a separate package os2-rpm-build.
- Make rpmbuild obey -v and -d options (to enable printing debug info).
- Change vendor to bww bitwise works GmbH.

* Sat Feb 25 2017 Dmitriy Kuminov <coding@dmik.org> - 4.13.0-14
- Update to version 4.13.0 GA.
- Fix sed warnings in find-lang.sh due to ':' in pats on OS/2.
- Bring .spec in sync with current Fedora .spec (this renames some packages
  and adds some more).

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
