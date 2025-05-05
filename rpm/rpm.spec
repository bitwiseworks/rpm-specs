# build against xz?
%bcond_without xz
# just for giggles, option to build with internal Berkeley DB
%bcond_with int_bdb
# run internal testsuite?
%if !0%{?os2_version}
%bcond_without check
%else
%bcond_with check
%endif
# build with plugins?
%bcond_without plugins
# build with libarchive? (needed for rpm2archive)
%bcond_without libarchive
# build with libimaevm.so
%if !0%{?os2_version}
%bcond_without libimaevm
%else
%bcond_with libimaevm
%endif
# build with new db format
%bcond_with ndb
# build with zstd support?
%bcond_without zstd
# build with lmdb support?
%bcond_with lmdb

%if !0%{?os2_version}
%define rpmhome /usr/lib/rpm
%else
%define rpmhome %{_libdir}/rpm
%endif

%global rpmver 4.15.1
#global snapver rc1
%global rel 3

%global srcver %{version}%{?snapver:-%{snapver}}
%global srcdir %{?snapver:testing}%{!?snapver:%{name}-%(echo %{version} | cut -d'.' -f1-2).x}

%define bdbver 5.3.15

# Build-dependency on systemd for the sake of one macro would be a bit much...
%{!?_tmpfilesdir:%global _tmpfilesdir /usr/lib/tmpfiles.d}

Summary: The RPM package management system
Name: rpm
Version: %{rpmver}
Release: %{?snapver:0.%{snapver}.}%{rel}%{?dist}
Url: http://www.rpm.org/
%if !0%{?os2_version}
Source0: http://ftp.rpm.org/releases/%{srcdir}/%{name}-%{srcver}.tar.bz2
%if %{with int_bdb}
Source1: db-%{bdbver}.tar.gz
%endif

# Disable autoconf config.site processing (#962837)
Patch1: rpm-4.15.x-siteconfig.patch
# In current Fedora, man-pages pkg owns all the localized man directories
Patch3: rpm-4.9.90-no-man-dirs.patch
# Temporary band-aid for rpm2cpio whining on payload size mismatch (#1142949)
Patch5: rpm-4.12.0-rpm2cpio-hack.patch
# https://github.com/rpm-software-management/rpm/pull/473
Patch6: 0001-find-debuginfo.sh-decompress-DWARF-compressed-ELF-se.patch

# Patches already upstream:

# These are not yet upstream
Patch906: rpm-4.7.1-geode-i686.patch
# Probably to be upstreamed in slightly different form
Patch907: rpm-4.15.x-ldflags.patch
%else
Vendor: bww bitwise works GmbH
%scm_source github http://github.com/bitwiseworks/%{name}-os2new v%{version}-os2-1
%endif

# Partially GPL/LGPL dual-licensed and some bits with BSD
# SourceLicense: (GPLv2+ and LGPLv2+ with exceptions) and BSD
License: GPLv2+

Requires: coreutils
%if %{without int_bdb}
# db recovery tools, rpmdb_util symlinks
%if !0%{?os2_version}
Requires: %{_bindir}/db_stat
%else
Requires: %{_bindir}/db_stat.exe
%endif
%endif
%if !0%{?os2_version}
Requires: popt%{_isa} >= 1.10.2.1
%else
Requires: popt >= 1.10.2.1
%endif
Requires: curl

%if %{without int_bdb}
%if !0%{?os2_version}
BuildRequires: libdb-devel
%else
BuildRequires: db4-devel
%endif
%endif

%if %{with check}
BuildRequires: fakechroot gnupg2
%endif

# XXX generally assumed to be installed but make it explicit as rpm
# is a bit special...
%if !0%{?os2_version}
BuildRequires: redhat-rpm-config >= 94
%endif
BuildRequires: gcc make
BuildRequires: gawk
%if !0%{?os2_version}
BuildRequires: elfutils-devel >= 0.112
BuildRequires: elfutils-libelf-devel
%endif
BuildRequires: readline-devel zlib-devel
BuildRequires: openssl-devel
# The popt version here just documents an older known-good version
BuildRequires: popt-devel >= 1.10.2
BuildRequires: file-devel
BuildRequires: gettext-devel
BuildRequires: ncurses-devel
BuildRequires: bzip2-devel >= 0.9.0c-2
BuildRequires: lua-devel >= 5.1
%if !0%{?os2_version}
BuildRequires: libcap-devel
BuildRequires: libacl-devel
%endif
%if %{with xz}
BuildRequires: xz-devel >= 4.999.8
%endif
%if %{with libarchive}
BuildRequires: libarchive-devel
%endif
%if %{with zstd}
BuildRequires: libzstd-devel
%endif
%if %{with lmdb}
BuildRequires: lmdb-devel
%endif
# Couple of patches change makefiles so, require for now...
BuildRequires: automake libtool

%if %{with plugins}
%if !0%{?os2_version}
BuildRequires: libselinux-devel
%endif
BuildRequires: dbus-devel
%if !0%{?os2_version}
BuildRequires: audit-libs-devel
%endif
%endif

%if %{with libimaevm}
BuildRequires: ima-evm-utils-devel >= 1.0
%endif

%description
The RPM Package Manager (RPM) is a powerful command line driven
package management system capable of installing, uninstalling,
verifying, querying, and updating software packages. Each software
package consists of an archive of files along with information about
the package like its version, a description, etc.

%package libs
Summary:  Libraries for manipulating RPM packages
License: GPLv2+ and LGPLv2+ with exceptions
Requires: %{name} = %{version}-%{release}
%if 0%{?os2_version}
# We need a fork-friendly PR_LoadLibrary on OS/2
Requires: nspr >= 4.12.0-2
%endif

%description libs
This package contains the RPM shared libraries.

%package build-libs
Summary:  Libraries for building RPM packages
License: GPLv2+ and LGPLv2+ with exceptions
%if !0%{?os2_version}
Requires: rpm-libs%{_isa} = %{version}-%{release}
%else
Requires: rpm-libs = %{version}-%{release}
%endif

%description build-libs
This package contains the RPM shared libraries for building packages.

%package sign-libs
Summary:  Libraries for signing RPM packages
License: GPLv2+ and LGPLv2+ with exceptions
%if !0%{?os2_version}
Requires: rpm-libs%{_isa} = %{version}-%{release}
Requires: %{_bindir}/gpg2
%else
Requires: rpm-libs = %{version}-%{release}
%endif

%description sign-libs
This package contains the RPM shared libraries for signing packages.

%package devel
Summary:  Development files for manipulating RPM packages
License: GPLv2+ and LGPLv2+ with exceptions
Requires: %{name} = %{version}-%{release}
%if !0%{?os2_version}
Requires: %{name}-libs%{_isa} = %{version}-%{release}
Requires: %{name}-build-libs%{_isa} = %{version}-%{release}
Requires: %{name}-sign-libs%{_isa} = %{version}-%{release}
Requires: popt-devel%{_isa}
%else
Requires: %{name}-libs = %{version}-%{release}
Requires: %{name}-build-libs = %{version}-%{release}
Requires: %{name}-sign-libs = %{version}-%{release}
Requires: popt-devel
%endif

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
Requires: rpm = %{version}-%{release}
%if !0%{?os2_version}
Requires: elfutils >= 0.128 binutils
%endif
Requires: findutils sed grep gawk diffutils file patch >= 2.5
Requires: tar unzip gzip bzip2 cpio xz
%if %{with zstd}
Requires: zstd
%endif
Requires: pkgconfig >= 1:0.24
%if !0%{?os2_version}
Requires: /usr/bin/gdb-add-index
# https://fedoraproject.org/wiki/Changes/Minimal_GDB_in_buildroot
Suggests: gdb-minimal
%endif
# Technically rpmbuild doesn't require any external configuration, but
# creating distro-compatible packages does. To make the common case
# "just work" while allowing for alternatives, depend on a virtual
# provide, typically coming from redhat-rpm-config.
%if !0%{?os2_version}
Requires: system-rpm-config
%endif

%description build
The rpm-build package contains the scripts and executable programs
that are used to build packages using the RPM Package Manager.

%package sign
Summary: Package signing support
%if !0%{?os2_version}
Requires: rpm-sign-libs%{_isa} = %{version}-%{release}
%else
Requires: rpm-sign-libs = %{version}-%{release}
%endif

%description sign
This package contains support for digitally signing RPM packages.

%package -n python2-%{name}
Summary: Python 2 bindings for apps which will manipulate RPM packages
BuildRequires: python2-devel
%{?python_provide:%python_provide python2-%{name}}
%if !0%{?os2_version}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
%else
Requires: %{name}-libs = %{version}-%{release}
%endif
Provides: %{name}-python = %{version}-%{release}
Obsoletes: %{name}-python < %{version}-%{release}

%description -n python2-%{name}
The python2-rpm package contains a module that permits applications
written in the Python programming language to use the interface
supplied by RPM Package Manager libraries.

This package should be installed if you want to develop Python 2
programs that will manipulate RPM packages and databases.

%package -n python3-%{name}
Summary: Python 3 bindings for apps which will manipulate RPM packages
BuildRequires: python3-devel
%{?python_provide:%python_provide python3-%{name}}
%if !0%{?os2_version}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
%else
Requires: %{name}-libs = %{version}-%{release}
%endif
Provides: %{name}-python3 = %{version}-%{release}
Obsoletes: %{name}-python3 < %{version}-%{release}
Obsoletes: platform-python-%{name} < %{version}-%{release}

%description -n python3-%{name}
The python3-rpm package contains a module that permits applications
written in the Python programming language to use the interface
supplied by RPM Package Manager libraries.

This package should be installed if you want to develop Python 3
programs that will manipulate RPM packages and databases.

%package apidocs
Summary: API documentation for RPM libraries
BuildArch: noarch

%description apidocs
This package contains API documentation for developing applications
that will manipulate RPM packages and databases.

%if !0%{?os2_version}
%package cron
Summary: Create daily logs of installed packages.
BuildArch: noarch
Requires: crontabs logrotate rpm = %{version}-%{release}

%description cron
This package contains a cron job which creates daily logs of installed
packages on a system.
%endif

%if %{with plugins}
%if !0%{?os2_version}
%package plugin-selinux
Summary: Rpm plugin for SELinux functionality
Requires: rpm-libs%{_isa} = %{version}-%{release}
Requires: selinux-policy-base

%description plugin-selinux
%{summary}.
%endif

%package plugin-syslog
Summary: Rpm plugin for syslog functionality
%if !0%{?os2_version}
Requires: rpm-libs%{_isa} = %{version}-%{release}
%else
Requires: rpm-libs = %{version}-%{release}
%endif

%description plugin-syslog
%{summary}.

%if !0%{?os2_version}
%package plugin-systemd-inhibit
Summary: Rpm plugin for systemd inhibit functionality
Requires: rpm-libs%{_isa} = %{version}-%{release}

%description plugin-systemd-inhibit
This plugin blocks systemd from entering idle, sleep or shutdown while an rpm
transaction is running using the systemd-inhibit mechanism.
%endif

%if !0%{?os2_version}
%package plugin-ima
Summary: Rpm plugin ima file signatures
Requires: rpm-libs%{_isa} = %{version}-%{release}

%description plugin-ima
%{summary}.
%endif

%package plugin-prioreset
Summary: Rpm plugin for resetting scriptlet priorities for SysV init
%if !0%{?os2_version}
Requires: rpm-libs%{_isa} = %{version}-%{release}
%else
Requires: rpm-libs = %{version}-%{release}
%endif

%description plugin-prioreset
%{summary}.

Useful on legacy SysV init systems if you run rpm transactions with
nice/ionice priorities. Should not be used on systemd systems.

%if !0%{?os2_version}
%package plugin-audit
Summary: Rpm plugin for logging audit events on package operations
Requires: rpm-libs%{_isa} = %{version}-%{release}

%description plugin-audit
%{summary}.
%endif

# with plugins
%endif

%if 0%{?os2_version}
%debug_package
%endif

%prep
%if !0%{?os2_version}
%autosetup -n %{name}-%{srcver} %{?with_int_bdb:-a 1} -p1
%else
%scm_setup
%endif

%if %{with int_bdb}
ln -s db-%{bdbver} db
%endif

%build
%set_build_flags

%if 0%{?os2_version}
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
%endif

autoreconf -i -f

%if !0%{?os2_version}
# Hardening hack taken from macro %%configure defined in redhat-rpm-config
for i in $(find . -name ltmain.sh) ; do
     %{__sed} -i.backup -e 's~compiler_flags=$~compiler_flags="%{_hardened_ldflags}"~' $i
done;

# Using configure macro has some unwanted side-effects on rpm platform
# setup, use the old-fashioned way for now only defining minimal paths.
./configure \
    --prefix=%{_usr} \
    --sysconfdir=%{_sysconfdir} \
    --localstatedir=%{_var} \
    --sharedstatedir=%{_var}/lib \
    --libdir=%{_libdir} \
    --build=%{_target_platform} \
    --host=%{_target_platform} \
    --with-vendor=redhat \
    %{!?with_int_bdb: --with-external-db} \
    %{!?with_plugins: --disable-plugins} \
    --with-lua \
    --with-selinux \
    --with-cap \
    --with-acl \
    %{?with_ndb: --with-ndb} \
    %{?with_libimaevm: --with-imaevm} \
    %{?with_zstd: --enable-zstd} \
    %{?with_lmdb: --enable-lmdb} \
    --enable-python \
    --with-crypto=openssl
%else
%configure \
    --enable-shared --disable-static \
    %{!?with_int_bdb: --with-external-db} \
    %{!?with_plugins: --disable-plugins} \
    --with-lua \
    %{?with_ndb: --with-ndb} \
    %{?with_libimaevm: --with-imaevm} \
    %{?with_zstd: --enable-zstd} \
    %{?with_lmdb: --enable-lmdb} \
    --enable-python \
    --with-crypto=openssl
%endif

%make_build

%if !0%{?os2_version}
pushd python
%else
cd python
%endif
%py2_build
%py3_build
%if !0%{?os2_version}
popd
%else
cd ..
%endif

%install
%make_install

# We need to build with --enable-python for the self-test suite, but we
# actually package the bindings built with setup.py (#531543#c26)
%if !0%{?os2_version}
pushd python
%else
cd python
%endif
%py2_install
%py3_install
%if !0%{?os2_version}
popd
%else
cd ..
%endif

%if 0%{?os2_version}
# Remove OS/2 import libraries from plugins
rm ${RPM_BUILD_ROOT}%{_libdir}/rpm-plugins/*_dll.a

# Remove all dll and import libraries from python sitearch, as we
# deliver the pyd anyway
rm -f ${RPM_BUILD_ROOT}%{python2_sitearch}/%{name}/*_dll.a
rm -f ${RPM_BUILD_ROOT}%{python2_sitearch}/%{name}/*.dll
rm -f ${RPM_BUILD_ROOT}%{python3_sitearch}/%{name}/*_dll.a
rm -f ${RPM_BUILD_ROOT}%{python3_sitearch}/%{name}/*.dll

# Remove mkinstalldirs, as we dont install it for now
rm -f ${RPM_BUILD_ROOT}%{rpmhome}/mkinstalldirs

# Remove elf attr magic (makes no sense on OS/2)
rm ${RPM_BUILD_ROOT}%{rpmhome}/fileattrs/elf.attr

# Remove systemd plugin manpage
rm -f ${RPM_BUILD_ROOT}%{_mandir}/man8/rpm-plugin-systemd-inhibit.8*

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
%endif

%if !0%{?os2_version}
# Save list of packages through cron
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/cron.daily
install -m 755 scripts/rpm.daily ${RPM_BUILD_ROOT}%{_sysconfdir}/cron.daily/rpm

mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d
install -m 644 scripts/rpm.log ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d/rpm

mkdir -p ${RPM_BUILD_ROOT}%{_tmpfilesdir}
echo "r /var/lib/rpm/__db.*" > ${RPM_BUILD_ROOT}%{_tmpfilesdir}/rpm.conf
%endif

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rpm
mkdir -p $RPM_BUILD_ROOT%{rpmhome}/macros.d

# init an empty database for %ghost'ing
%if !0%{?os2_version}
./rpmdb --dbpath=$RPM_BUILD_ROOT/var/lib/rpm --initdb
%else
export BEGINLIBPATH="%{_builddir}/%{buildsubdir}/rpmio/.libs;%{_builddir}/%{buildsubdir}/lib/.libs;$BEGINLIBPATH"
./rpmdb --dbpath=$RPM_BUILD_ROOT/%{_var}/lib/rpm --initdb
rm -f $RPM_BUILD_ROOT/%{_var}/lib/rpm/.rpm.lock
touch $RPM_BUILD_ROOT/%{_var}/.rpm.lock
%endif

# plant links to relevant db utils as rpmdb_foo for documention compatibility
%if %{without int_bdb}
for dbutil in dump load recover stat upgrade verify
do
    ln -s %{_bindir}/db_${dbutil}.exe $RPM_BUILD_ROOT/%{rpmhome}/rpmdb_${dbutil}
done
%endif

%find_lang %{name}

find $RPM_BUILD_ROOT -name "*.la"|xargs rm -f

%if !0%{?os2_version}
# These live in perl-generators and python-rpm-generators now
rm -f $RPM_BUILD_ROOT/%{rpmhome}/{perldeps.pl,perl.*,pythond*}
rm -f $RPM_BUILD_ROOT/%{_fileattrsdir}/{perl*,python*}
%else
rm -f $RPM_BUILD_ROOT/%{rpmhome}/pythond*
rm -f $RPM_BUILD_ROOT/%{_fileattrsdir}/python*
%endif

%if %{with check}
%check
# https://github.com/rpm-software-management/rpm/issues/741
make check || (cat tests/rpmtests.log; exit 0)
%endif

%files -f %{name}.lang
%license COPYING
%doc CREDITS doc/manual/[a-z]*

%if !0%{?os2_version}
%{_tmpfilesdir}/rpm.conf
%endif
%dir %{_sysconfdir}/rpm

%if !0%{?os2_version}
%attr(0755, root, root) %dir /var/lib/rpm
%attr(0644, root, root) %ghost %config(missingok,noreplace) /var/lib/rpm/*
%attr(0644, root, root) %ghost /var/lib/rpm/.*.lock
%else
%attr(0755, root, root) %dir %{_var}/lib/rpm
%attr(0644, root, root) %ghost %config(missingok,noreplace) %{_var}/lib/rpm/*
%attr(0644, root, root) %ghost %{_var}/.*.lock
%endif

%if !0%{?os2_version}
%{_bindir}/rpm
%{_bindir}/rpm2archive
%{_bindir}/rpm2cpio
%{_bindir}/rpmdb
%{_bindir}/rpmkeys
%else
%{_bindir}/rpm.exe
%{_bindir}/rpm2archive.exe
%{_bindir}/rpm2cpio.exe
%{_bindir}/rpmdb.exe
%{_bindir}/rpmkeys.exe
%endif
%{_bindir}/rpmquery
%{_bindir}/rpmverify

%{_mandir}/man8/rpm.8*
%{_mandir}/man8/rpmdb.8*
%{_mandir}/man8/rpmkeys.8*
%{_mandir}/man8/rpm2cpio.8*
%{_mandir}/man8/rpm-misc.8*

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
%{rpmhome}/lua
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
%if !0%{?os2_version}
%{_libdir}/librpmio.so.*
%{_libdir}/librpm.so.*
%else
%{_libdir}/rpmio[0-9].dll
%{_libdir}/rpm[0-9].dll
%endif
%if %{with plugins}
%dir %{_libdir}/rpm-plugins

%files plugin-syslog
%if !0%{?os2_version}
%{_libdir}/rpm-plugins/syslog.so
%else
%{_libdir}/rpm-plugins/syslog.dll
%endif

%if !0%{?os2_version}
%files plugin-selinux
%{_libdir}/rpm-plugins/selinux.so
%endif

%if !0%{?os2_version}
%files plugin-systemd-inhibit
%{_libdir}/rpm-plugins/systemd_inhibit.so
%{_mandir}/man8/rpm-plugin-systemd-inhibit.8*
%endif

%if !0%{?os2_version}
%files plugin-ima
%{_libdir}/rpm-plugins/ima.so
%endif

%files plugin-prioreset
%if !0%{?os2_version}
%{_libdir}/rpm-plugins/prioreset.so
%else
%{_libdir}/rpm-plugins/priorese.dll
%endif

%if !0%{?os2_version}
%files plugin-audit
%{_libdir}/rpm-plugins/audit.so
%endif

# with plugins
%endif

%files build-libs
%if !0%{?os2_version}
%{_libdir}/librpmbuild.so.*
%else
%{_libdir}/rpmbuil[0-9].dll
%endif

%files sign-libs
%if !0%{?os2_version}
%{_libdir}/librpmsign.so.*
%else
%{_libdir}/rpmsign[0-9].dll
%endif

%files build
%if !0%{?os2_version}
%{_bindir}/rpmbuild
%else
%{_bindir}/rpmbuild.exe
%endif
%{_bindir}/gendiff
%if !0%{?os2_version}
%{_bindir}/rpmspec
%else
%{_bindir}/rpmspec.exe
%endif

%{_mandir}/man1/gendiff.1*
%{_mandir}/man8/rpmbuild.8*
%{_mandir}/man8/rpmdeps.8*
%{_mandir}/man8/rpmspec.8*

%{rpmhome}/brp-*
%{rpmhome}/check-*
%if !0%{?os2_version}
%{rpmhome}/debugedit
%{rpmhome}/sepdebugcrcfix
%{rpmhome}/find-debuginfo.sh
%endif
%{rpmhome}/find-lang.sh
%{rpmhome}/*provides*
%{rpmhome}/*requires*
%{rpmhome}/*deps*
%{rpmhome}/*.prov
%{rpmhome}/*.req
%{rpmhome}/config.*
%if !0%{?os2_version}
%{rpmhome}/mkinstalldirs
%endif
%{rpmhome}/fileattrs/*
%if 0%{?os2_version}
%exclude %{rpmhome}/*.dbg
%endif

%files sign
%if !0%{?os2_version}
%{_bindir}/rpmsign
%else
%{_bindir}/rpmsign.exe
%endif
%{_mandir}/man8/rpmsign.8*

%files -n python2-%{name}
%{python2_sitearch}/%{name}/
%{python2_sitearch}/%{name}-%{version}*.egg-info

%files -n python3-%{name}
%{python3_sitearch}/%{name}/
%{python3_sitearch}/%{name}-%{version}*.egg-info

%files devel
%{_mandir}/man8/rpmgraph.8*
%if !0%{?os2_version}
%{_bindir}/rpmgraph
%{_libdir}/librp*[a-z].so
%else
%{_bindir}/rpmgraph.exe
%{_libdir}/rp*_dll.a
%endif
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/%{name}/

%if !0%{?os2_version}
%files cron
%{_sysconfdir}/cron.daily/rpm
%config(noreplace) %{_sysconfdir}/logrotate.d/rpm
%endif

%files apidocs
%license COPYING
%doc doc/librpm/html/*

%changelog
* Mon Mai 05 2025 Silvan Scherrer <silvan.scherrer@aroa.ch> 4.15.1-3
- fix a annoying macro parameter bug
- fix a forgotten change

* Mon Apr 28 2025 Silvan Scherrer <silvan.scherrer@aroa.ch> 4.15.1-2
- move .rpm.lock out of /var/lib/rpm, as else rebuilddb is not working

* Fri Apr 25 2025 Silvan Scherrer <silvan.scherrer@aroa.ch> 4.15.1-1
- update to version 4.15
- resync spec with fedora version

* Wed Apr 23 2025 Silvan Scherrer <silvan.scherrer@aroa.ch> 4.13.0-21
- use a new branch for building. Should be equivalent
- enable python3

* Wed Sep 15 2021 Silvan Scherrer <silvan.scherrer@aroa.ch> 4.13.0-20
- force proper sse2 alignment in optflags on x86 platforms
- cherry pick some lua changes from upstream, fixes lua path handling

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
