#define svn_url     F:/rd/rpm/rpm/branches/rpm-4.8.1
%define svn_url     http://svn.netlabs.org/repos/rpm/rpm/branches/rpm-4.8.1
%define svn_rev     615

%define with_sqlite 1
%undefine int_bdb

# build against xz?
%bcond_without xz
# sqlite backend is pretty useless
%bcond_with sqlite
# just for giggles, option to build with internal Berkeley DB
%bcond_with int_bdb
# run internal testsuite?
%bcond_without check

%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%define rpmhome %{_libdir}/rpm

%define rpmver 4.8.1
%define snapver %{nil}
%define srcver %{rpmver}

%define bdbver 4.8.24
%define dbprefix db

Summary: The RPM package management system
Name: rpm
Version: %{rpmver}
Release: 25%{?dist}
Group: System Environment/Base
Url: http://www.rpm.org/
Source: %{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip

# Partially GPL/LGPL dual-licensed and some bits with BSD
# SourceLicense: (GPLv2+ and LGPLv2+ with exceptions) and BSD 
License: GPLv2+

Requires: coreutils
%if %{without int_bdb}
# db recovery tools, rpmdb_util symlinks
Requires: db4-utils
%endif
Requires: popt >= 1.10.2.1
Requires: sqlite
Requires: curl
Requires: rpm-libs = %{version}-%{release}
Requires: pthread
Requires: cpio
Requires: cube
Requires: urpo >= 20150101

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
#BuildRequires: redhat-rpm-config
#BuildRequires: gawk
#BuildRequires: elfutils-devel >= 0.112
#BuildRequires: elfutils-libelf-devel
BuildRequires: readline-devel zlib-devel
BuildRequires: nss-devel
# The popt version here just documents an older known-good version
BuildRequires: popt-devel >= 1.10.2
BuildRequires: file-devel
BuildRequires: gettext-devel
#BuildRequires: libselinux-devel
BuildRequires: ncurses-devel
BuildRequires: bzip2-devel >= 0.9.0c-2
BuildRequires: python-devel >= 2.6
#BuildRequires: lua-devel >= 5.1
#BuildRequires: libcap-devel
#BuildRequires: libacl-devel
%if ! %{without xz}
BuildRequires: xz-devel >= 4.999.8
%endif
%if %{with sqlite}
BuildRequires: sqlite-devel
%endif

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

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
# librpm uses cap_compare, introduced sometimes between libcap 2.10 and 2.16.
# A manual require is needed, see #505596
#Requires: libcap >= 2.16

%description libs
This package contains the RPM shared libraries.

%package devel
Summary:  Development files for manipulating RPM packages
Group: Development/Libraries
License: GPLv2+ and LGPLv2+ with exceptions
Requires: rpm = %{version}-%{release}
#Requires: popt-devel
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
#Requires: python

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

%package debug
Summary: HLL debug data for exception handling support.

%description debug
HLL debug data for exception handling support.

%prep
%if %{?svn_rev:%(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')}%{!?svn_rev):0}
%setup -q
%else
%setup -n "%{name}-%{version}" -Tc
svn export %{?svn_rev:-r %{svn_rev}} %{svn_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip" "%{name}-%{version}")
%endif

%if %{with int_bdb}
ln -s db-%{bdbver} db
%endif

%build
%if %{without int_bdb}
#CPPFLAGS=-I%{_includedir}/db%{bdbver} 
#LDFLAGS=-L%{_libdir}/db%{bdbver}
%endif
#CPPFLAGS="$CPPFLAGS `pkg-config --cflags nss`"
#CFLAGS="$RPM_OPT_FLAGS"
#export CPPFLAGS CFLAGS LDFLAGS

# Using configure macro has some unwanted side-effects on rpm platform
# setup, use the old-fashioned way for now only defining minimal paths.
export RPM_MKDIR="/@unixroot/usr/bin/mkdir.exe";
export CONFIG_SITE="/@unixroot/usr/share/config.legacy";
export CONFIG_SHELL="/@unixroot/usr/bin/sh";
export LDFLAGS="-Zbin-files -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp";
export LIBS="-lintl -lurpo -lmmap -lpoll";
CFLAGS="%{optflags} -I/@unixroot/usr/include/nss3 -I/@unixroot/usr/include/nspr4" ; \
%configure \
    --enable-shared --disable-static --without-lua \
    %{!?with_int_bdb: --with-external-db} \
    %{?with_sqlite: --enable-sqlite3} \
    --enable-python

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR="$RPM_BUILD_ROOT" install

# YD skip pkcconfig requirement
#rm ${RPM_BUILD_ROOT}%{_libdir}/pkgconfig/rpm.pc
install -m 755 scripts/check-files.os2 ${RPM_BUILD_ROOT}%{rpmhome}
install -m 755 scripts/brp-strip.os2 ${RPM_BUILD_ROOT}%{rpmhome}
mv ${RPM_BUILD_ROOT}/@unixroot/bin/rpm.exe ${RPM_BUILD_ROOT}%{_bindir}/rpm.exe

# YD remove paths from macros
sed -i 's#.:/usr/bin/#/@unixroot/usr/bin/#gi' ${RPM_BUILD_ROOT}%{rpmhome}/macros
sed -i 's#.:/bin/#/@unixroot/bin/#gi' ${RPM_BUILD_ROOT}%{rpmhome}/macros
sed -i 's#.:/tcpip/bin/#/@bootroot/tcpip/bin/#gi' ${RPM_BUILD_ROOT}%{rpmhome}/macros
sed -i 's#.:/bin/tool/##gi' ${RPM_BUILD_ROOT}%{rpmhome}/macros

# YD install dll
install -D -m0755 build/.libs/rpmbuild.dll $RPM_BUILD_ROOT/%{_libdir}/
install -D -m0755 build/.libs/rpmbuild.a $RPM_BUILD_ROOT/%{_libdir}/
install -D -m0755 build/.libs/rpmbuild_s.a $RPM_BUILD_ROOT/%{_libdir}/
install -D -m0755 build/.libs/rpmbuild.lib $RPM_BUILD_ROOT/%{_libdir}/

install -D -m0755 lib/.libs/rpm.dll $RPM_BUILD_ROOT/%{_libdir}/
install -D -m0755 lib/.libs/rpm.a $RPM_BUILD_ROOT/%{_libdir}/
install -D -m0755 lib/.libs/rpm_s.a $RPM_BUILD_ROOT/%{_libdir}/
install -D -m0755 lib/.libs/rpm.lib $RPM_BUILD_ROOT/%{_libdir}/

install -D -m0755 rpmio/.libs/rpmio.dll $RPM_BUILD_ROOT/%{_libdir}/
install -D -m0755 rpmio/.libs/rpmio.a $RPM_BUILD_ROOT/%{_libdir}/
install -D -m0755 rpmio/.libs/rpmio_s.a $RPM_BUILD_ROOT/%{_libdir}/
install -D -m0755 rpmio/.libs/rpmio.lib $RPM_BUILD_ROOT/%{_libdir}/

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

#%find_lang %{name}

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

%files
# -f %{name}.lang
%defattr(-,root,root,-)
%doc GROUPS COPYING CREDITS ChangeLog.bz2 doc/manual/[a-z]*

%dir                            %{_sysconfdir}/rpm

%attr(0755, root, root)   %dir %{_var}/lib/rpm
%attr(0644, root, root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) %{_var}/lib/rpm/*
%attr(0755, root, root) %dir %{rpmhome}

%{_bindir}/rpm.exe
%{_bindir}/rpm2cpio.exe
%{_bindir}/rpmdb
%{_bindir}/rpmsign
%{_bindir}/rpmquery
%{_bindir}/rpmverify

%{_mandir}/man8/rpm.8*
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
%{rpmhome}/rpm.xinetd
%{rpmhome}/rpm2cpio.sh
%{rpmhome}/tgpg

%{rpmhome}/platform

%{rpmhome}/wps-object.exe
%{rpmhome}/warpin-conflicts.exe

%files libs
%defattr(-,root,root)
%{_libdir}/rpm*.dll

%files build
%defattr(-,root,root)
%{_bindir}/rpmbuild.exe
%{_bindir}/gendiff

%{_mandir}/man1/gendiff.1*

%{rpmhome}/brp-*
%{rpmhome}/check-buildroot
%{rpmhome}/check-files
%{rpmhome}/check-files.os2
%{rpmhome}/check-prereqs
%{rpmhome}/check-rpaths*
#%{rpmhome}/debugedit
#%{rpmhome}/find-debuginfo.sh
%{rpmhome}/find-lang.sh
%{rpmhome}/find-provides
%{rpmhome}/find-requires
%{rpmhome}/javadeps.exe
%{rpmhome}/mono-find-provides
%{rpmhome}/mono-find-requires
%{rpmhome}/ocaml-find-provides.sh
%{rpmhome}/ocaml-find-requires.sh
%{rpmhome}/osgideps.pl
%{rpmhome}/perldeps.pl
%{rpmhome}/libtooldeps.sh
%{rpmhome}/pkgconfigdeps.sh
%{rpmhome}/perl.prov
%{rpmhome}/perl.req
%{rpmhome}/tcl.req
%{rpmhome}/pythondeps.sh
%{rpmhome}/rpmdeps.exe
%{rpmhome}/config.guess
%{rpmhome}/config.sub
%{rpmhome}/mkinstalldirs
%{rpmhome}/rpmdiff*
%{rpmhome}/desktop-file.prov
%{rpmhome}/fontconfig.prov
#%{rpmhome}/postscriptdriver.prov

%{rpmhome}/macros.perl
%{rpmhome}/macros.python
%{rpmhome}/macros.php

%{_mandir}/man8/rpmbuild.8*
%{_mandir}/man8/rpmdeps.8*

%{_usr}/share/locale/ca/LC_MESSAGES/rpm.mo
%{_usr}/share/locale/cs/LC_MESSAGES/rpm.mo
%{_usr}/share/locale/da/LC_MESSAGES/rpm.mo
%{_usr}/share/locale/de/LC_MESSAGES/rpm.mo
%{_usr}/share/locale/es/LC_MESSAGES/rpm.mo
%{_usr}/share/locale/fi/LC_MESSAGES/rpm.mo
%{_usr}/share/locale/fr/LC_MESSAGES/rpm.mo
%{_usr}/share/locale/is/LC_MESSAGES/rpm.mo
%{_usr}/share/locale/it/LC_MESSAGES/rpm.mo
%{_usr}/share/locale/ja/LC_MESSAGES/rpm.mo
%{_usr}/share/locale/ko/LC_MESSAGES/rpm.mo
%{_usr}/share/locale/ms/LC_MESSAGES/rpm.mo
%{_usr}/share/locale/nb/LC_MESSAGES/rpm.mo
%{_usr}/share/locale/nl/LC_MESSAGES/rpm.mo
%{_usr}/share/locale/pl/LC_MESSAGES/rpm.mo
%{_usr}/share/locale/pt/LC_MESSAGES/rpm.mo
%{_usr}/share/locale/pt_BR/LC_MESSAGES/rpm.mo
%{_usr}/share/locale/ru/LC_MESSAGES/rpm.mo
%{_usr}/share/locale/sk/LC_MESSAGES/rpm.mo
%{_usr}/share/locale/sl/LC_MESSAGES/rpm.mo
%{_usr}/share/locale/sr/LC_MESSAGES/rpm.mo
%{_usr}/share/locale/sr@latin/LC_MESSAGES/rpm.mo
%{_usr}/share/locale/sv/LC_MESSAGES/rpm.mo
%{_usr}/share/locale/tr/LC_MESSAGES/rpm.mo
%{_usr}/share/locale/zh_TW/LC_MESSAGES/rpm.mo

%files python
%defattr(-,root,root)
%{_usr}/lib/python*.*/*

%files devel
%defattr(-,root,root)
%_includedir/*
%{_libdir}/rp*[a-z].a
%{_libdir}/rp*[a-z].lib
%{_mandir}/man8/rpmgraph.8*
%{_bindir}/rpmgraph.exe
%{_libdir}/pkgconfig/rpm.pc

%files cron
%defattr(-,root,root)
%{_sysconfdir}/cron.daily/rpm
%config(noreplace) %{_sysconfdir}/logrotate.d/rpm

#%files apidocs
#%defattr(-,root,root)
#%doc doc/librpm/html/*

%files debug
%defattr(-,root,root)
%{_bindir}/*.dbg
%{_libdir}/*.dbg
%{_libdir}/rpm/*.dbg


%changelog
* Tue Dec 15 2015 yd <yd@os2power.com> 4.8.1-25
- r615, standardize debug package creation, ticket#149.

* Thu Nov 12 2015 yd <yd@os2power.com> 4.8.1-24
- r582, allow use of platform specific macros file. fixes ticket#135. 
- r581, standardize debug package creation. fixes ticket#134.

* Wed Feb 25 2015 yd <yd@os2power.com> 4.8.1-23
- r557, backport r536, Make %find_lang macro work on OS/2.
- r558, add support for macros.d directory, fixes ticket#119. 

Make %find_lang macro work on OS/2.
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

* Wed Sep 24 2014 yd
- r461, sideport r409, popen() does not recognize unixroot, fixes macro expansion.

* Wed Apr 09 2014 yd
- r409, popen() does not recognize unixroot, fixes macro expansion.

* Mon Apr 07 2014 yd
- build for python 2.7.

* Wed Mar 28 2013 yd
- r341, fix scripts symlinks.

* Tue Mar 14 2013 yd
- added tool requirements for build package.

* Tue Mar 13 2012 yd
- updated warpin-conflict.cmd, ticket #27, #31.

* Sun Nov 20 2011 yd
- use shell in /usr/bin.

* Fri Nov 18 2011 yd
- keep all executables to /usr/bin and place symlinks in /bin
