#%define PATCHVER P4
#%define PREVER rc1
#%define VERSION %{version}%{PREVER}
#%define VERSION %{version}-%{PATCHVER}
%define VERSION %{version}

%{?!SDB:       %define SDB       0}
%{?!test:      %define test      0}
%{?!bind_uid:  %define bind_uid  25}
%{?!bind_gid:  %define bind_gid  25}
%{?!GSSTSIG:   %define GSSTSIG   0}
%{?!PKCS11:    %define PKCS11    0}
%{?!DEVEL:     %define DEVEL     1}
%define        bind_dir          /@unixroot/var/named
%define        chroot_prefix     %{bind_dir}/chroot

#
Summary:  The Berkeley Internet Name Domain (BIND) DNS (Domain Name System) server
Name:     bind
License:  ISC
Version:  9.8.1
Release:  1%{?dist}
Url:      http://www.isc.org/products/BIND/
Buildroot:%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Group:    System Environment/Daemons
#
Source:   ftp://ftp.isc.org/isc/bind9/%{VERSION}/bind-%{VERSION}.tar.gz

#Source8:  dnszone.schema
Source25: named.conf.sample
Source28: config-8.tar.bz2
Source35: bind.tmpfiles.d
Source36: trusted-key.key

Patch0:  bind-os2.patch

#
#Requires:       mktemp
#Requires:       systemd-units
#Requires:       bind-libs = %{version}-%{release}
Obsoletes:      bind-config < 30:9.3.2-34.fc6
Provides:       bind-config = 30:9.3.2-34.fc6
Obsoletes:      caching-nameserver < 31:9.4.1-7.fc8
Provides:       caching-nameserver = 31:9.4.1-7.fc8
Obsoletes:      dnssec-conf < 1.27-2
Provides:       dnssec-conf = 1.27-1
BuildRequires:  openssl-devel, autoconf, pkgconfig, libxml2-devel
#BuildRequires:  libidn-devel, libcap-devel, libtool
%if %{SDB}
BuildRequires:  openldap-devel, postgresql-devel, sqlite-devel, mysql-devel
%endif
%if %{test}
BuildRequires:  net-tools
%endif
%if %{GSSTSIG}
BuildRequires:  krb5-devel
%endif

# Comment from atkac:
#
# Don't extract provides for the following libraries. Non-BIND9
# applications should not use them, they should use libraries
# from bind-libs-lite package.
#
# Since bind-libs-lite doesn't contain some libraries used by all
# BIND9 programs (like liblwres) use those "internal" libraries for
# dependency resolution. If, for example, bind package requires
# libdns.so then it will automatically pull in both bind-libs
# and bind-libs-lite (which is incorrect, only bind-libs is needed)
%{?filter_setup:
%filter_provides_in %{_libdir}/bind9/libdns\.so.*
%filter_provides_in %{_libdir}/bind9/libisc\.so.*
%filter_provides_in %{_libdir}/bind9/libisccfg\.so.*
%filter_from_requires /libdns\.so.*/d
%filter_from_requires /libisc\.so.*/d
%filter_from_requires /libisccfg\.so.*/d
%filter_setup
}

%description
BIND (Berkeley Internet Name Domain) is an implementation of the DNS
(Domain Name System) protocols. BIND includes a DNS server (named),
which resolves host names to IP addresses; a resolver library
(routines for applications to use when interfacing with DNS); and
tools for verifying that the DNS server is operating properly.

%if %{PKCS11}
%package pkcs11
Summary: Bind PKCS#11 tools for using DNSSEC
Group:   System Environment/Daemons
Requires: engine_pkcs11 opensc
#BuildRequires: opensc-devel

%description pkcs11
This is a set of PKCS#11 utilities that when used together create rsa
keys in a PKCS11 keystore, such as provided by opencryptoki. The keys
will have a label of "zone,zsk|ksk,xxx" and an id of the keytag in hex.
%endif

%if %{SDB}
%package sdb
Summary: BIND server with database backends and DLZ support
Group:   System Environment/Daemons
Requires: bind

%description sdb
BIND (Berkeley Internet Name Domain) is an implementation of the DNS
(Domain Name System) protocols. BIND includes a DNS server (named-sdb)
which has compiled-in SDB (Simplified Database Backend) which includes
support for using alternative Zone Databases stored in an LDAP server
(ldapdb), a postgreSQL database (pgsqldb), an sqlite database (sqlitedb),
or in the filesystem (dirdb), in addition to the standard in-memory RBT
(Red Black Tree) zone database. It also includes support for DLZ
(Dynamic Loadable Zones)
%endif

%package libs-lite
Summary:  Libraries for working with the DNS protocol
Group:    Applications/System
Obsoletes:bind-libbind-devel < 31:9.3.3-4.fc7
Provides: bind-libbind-devel = 31:9.3.3-4.fc7
Requires: bind-license = %{version}-%{release}

%description libs-lite
Contains lite version of BIND suite libraries which are used by various
programs to work with DNS protocol.

%package libs
Summary: Libraries used by the BIND DNS packages
Group:    Applications/System
Requires: bind-license = %{version}-%{release}

%description libs
Contains heavyweight version of BIND suite libraries used by both named DNS
server and utilities in bind-utils package.

%package license
Summary:  License of the BIND DNS suite
Group:    Applications/System
BuildArch:noarch

%description license
Contains license of the BIND DNS suite.

%package utils
Summary: Utilities for querying DNS name servers
Group:   Applications/System

%description utils
Bind-utils contains a collection of utilities for querying DNS (Domain
Name System) name servers to find out information about Internet
hosts. These tools will provide you with the IP addresses for given
host names, as well as other information about registered domains and
network addresses.

You should install bind-utils if you need to get information from DNS name
servers.

%if %{DEVEL}
%package devel
Summary:  Header files and libraries needed for BIND DNS development
Group:    Development/Libraries
Obsoletes:bind-libbind-devel < 31:9.3.3-4.fc7
Provides: bind-libbind-devel = 31:9.3.3-4.fc7
Requires: bind-libs = %{version}-%{release}

%description devel
The bind-devel package contains full version of the header files and libraries
required for development with ISC BIND 9
%endif

%package lite-devel
Summary:  Lite version of header files and libraries needed for BIND DNS development
Group:    Development/Libraries
Requires: bind-libs-lite = %{version}-%{release}

%description lite-devel
The bind-lite-devel package contains lite version of the header
files and libraries required for development with ISC BIND 9

%package chroot
Summary:        A chroot runtime environment for the ISC BIND DNS server, named(8)
Group:          System Environment/Daemons
Prefix:         %{chroot_prefix}
Requires:       bind = %{version}-%{release}

%description chroot
This package contains a tree of files which can be used as a
chroot(2) jail for the named(8) program from the BIND package.
Based on the code from Jan "Yenya" Kasprzak <kas@fi.muni.cz>

%prep
%setup -q -n %{name}-%{VERSION}

# Common patches
%patch0 -p1 -b .os2
:;

%build
export CFLAGS="$CFLAGS $RPM_OPT_FLAGS"
export CPPFLAGS="$CPPFLAGS -DDIG_SIGCHASE"
export STD_CDEFINES="$CPPFLAGS"
export CONFIG_SHELL="/@unixroot/usr/bin/sh.exe"
# YD -Zhigh-mem is not compatible with some tcpip libc functions
export LDFLAGS="-Zexe -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lurpo -lmmap -lpthread"

sed -i -e \
's/RELEASEVER=\(.*\)/RELEASEVER=\1-OS2-%{version}-%{release}/' \
version

%configure \
  --with-libtool \
  --enable-threads \
  --disable-ipv6 \
  --with-pic \
  --disable-static \
  --disable-openssl-version-check \
  --with-openssl=%{_prefix} \
  --enable-exportlib \
  --with-export-libdir=%{_libdir} \
  --with-export-includedir=%{_includedir} \
  --includedir=%{_includedir}/bind9 \
%if %{PKCS11}
  --with-pkcs11=%{_libdir}/pkcs11/PKCS11_API.so \
%endif
%if %{SDB}
  --with-dlz-ldap=yes \
  --with-dlz-postgres=yes \
  --with-dlz-mysql=yes \
  --with-dlz-filesystem=yes \
%endif
%if %{GSSTSIG}
  --with-gssapi=yes \
  --disable-isc-spnego \
%endif
 "--cache-file=%{_topdir}/cache/%{name}-%{_target_cpu}.cache"

make %{?_smp_mflags}

%if %{test}
%check
if [ "`whoami`" = 'root' ]; then
  set -e
  chmod -R a+rwX .
  pushd bin/tests
  pushd system
  ./ifconfig.sh up
  popd
  make test
  e=$?
  pushd system
  ./ifconfig.sh down
  popd
  popd
  if [ "$e" -ne 0 ]; then
    echo "ERROR: this build of BIND failed 'make test'. Aborting."
    exit $e;
  fi;
else
  echo 'only root can run the tests (they require an ifconfig).'
%endif

%install
rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

install -m 755 lib/bind9/bind9.dll $RPM_BUILD_ROOT/%{_libdir}

gzip -9 doc/rfc/*

# Build directory hierarchy
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/rc.d/init.d
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/NetworkManager/dispatcher.d
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/bind
mkdir -p ${RPM_BUILD_ROOT}%{_var}/named/slaves
mkdir -p ${RPM_BUILD_ROOT}%{_var}/named/data
mkdir -p ${RPM_BUILD_ROOT}%{_var}/named/dynamic
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man1
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man5
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man8
mkdir -p ${RPM_BUILD_ROOT}%{_var}/run/named
mkdir -p ${RPM_BUILD_ROOT}%{_var}/log

#chroot
mkdir -p ${RPM_BUILD_ROOT}/%{chroot_prefix}/dev
mkdir -p ${RPM_BUILD_ROOT}/%{chroot_prefix}/etc
mkdir -p ${RPM_BUILD_ROOT}/%{chroot_prefix}/var
mkdir -p ${RPM_BUILD_ROOT}/%{chroot_prefix}/var/log
mkdir -p ${RPM_BUILD_ROOT}/%{chroot_prefix}/var/named
mkdir -p ${RPM_BUILD_ROOT}/%{chroot_prefix}/var/run/named
mkdir -p ${RPM_BUILD_ROOT}/%{chroot_prefix}/var/tmp
mkdir -p ${RPM_BUILD_ROOT}/%{chroot_prefix}/etc/pki/dnssec-keys
mkdir -p ${RPM_BUILD_ROOT}/%{chroot_prefix}/etc/named
mkdir -p ${RPM_BUILD_ROOT}/%{chroot_prefix}/%{_libdir}/bind
# these are required to prevent them being erased during upgrade of previous
# versions that included them (bug #130121):
touch ${RPM_BUILD_ROOT}/%{chroot_prefix}/dev/null
touch ${RPM_BUILD_ROOT}/%{chroot_prefix}/dev/random
touch ${RPM_BUILD_ROOT}/%{chroot_prefix}/dev/zero
touch ${RPM_BUILD_ROOT}/%{chroot_prefix}/etc/localtime

touch ${RPM_BUILD_ROOT}/%{chroot_prefix}/etc/named.conf
#end chroot

# Remove unwanted files
rm -f ${RPM_BUILD_ROOT}%{_sysconfdir}/bind.keys

#install -m 755 %SOURCE2 ${RPM_BUILD_ROOT}%{_sysconfdir}/rc.d/init.d/named
#install -m 644 %SOURCE3 ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d/named
#install -m 755 %SOURCE4 ${RPM_BUILD_ROOT}%{_sysconfdir}/NetworkManager/dispatcher.d/13-named
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig
#install -m 644 %{SOURCE1} ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig/named
%if %{SDB}
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/openldap/schema
install -m 644 %{SOURCE8} ${RPM_BUILD_ROOT}%{_sysconfdir}/openldap/schema/dnszone.schema
install -m 644 %{SOURCE12} contrib/sdb/pgsql/
%endif

# Files required to run test-suite outside of build tree:
cp -fp config.h ${RPM_BUILD_ROOT}/%{_includedir}/bind9
cp -fp lib/dns/include/dns/forward.h ${RPM_BUILD_ROOT}/%{_includedir}/dns
cp -fp lib/isc/unix/include/isc/keyboard.h ${RPM_BUILD_ROOT}/%{_includedir}/isc

# Remove libtool .la files:
rm -f ${RPM_BUILD_ROOT}/%{_libdir}/*.la

# Remove -devel files out of buildroot if not needed
%if !%{DEVEL}
rm -f ${RPM_BUILD_ROOT}/%{_libdir}/bind9/*so
rm -rf ${RPM_BUILD_ROOT}/%{_includedir}/bind9
rm -f ${RPM_BUILD_ROOT}/%{_mandir}/man1/isc-config.sh.1*
rm -f ${RPM_BUILD_ROOT}/%{_mandir}/man3/lwres*
rm -f ${RPM_BUILD_ROOT}/%{_bindir}/isc-config.sh
%endif

# SDB manpages
%if %{SDB}
install -m 644 %{SOURCE31} ${RPM_BUILD_ROOT}%{_mandir}/man1/ldap2zone.1
install -m 644 %{SOURCE32} ${RPM_BUILD_ROOT}%{_mandir}/man8/named-sdb.8
install -m 644 %{SOURCE33} ${RPM_BUILD_ROOT}%{_mandir}/man1/zonetodb.1
install -m 644 %{SOURCE34} ${RPM_BUILD_ROOT}%{_mandir}/man1/zone2sqlite.1
%endif

# Ghost config files:
touch ${RPM_BUILD_ROOT}%{_localstatedir}/log/named.log

# configuration files:
tar -xjf %{SOURCE28}
cp -r etc ${RPM_BUILD_ROOT}/@unixroot
cp -r var ${RPM_BUILD_ROOT}/@unixroot
touch ${RPM_BUILD_ROOT}%{_sysconfdir}/rndc.key
touch ${RPM_BUILD_ROOT}%{_sysconfdir}/rndc.conf
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/named

install -m 644 bind.keys ${RPM_BUILD_ROOT}%{_sysconfdir}/named.iscdlv.key
install -m 644 %{SOURCE36} ${RPM_BUILD_ROOT}%{_sysconfdir}/trusted-key.key

# sample bind configuration files for %%doc:
mkdir -p sample%{_sysconfdir} sample%{_var}/named/data
mkdir -p sample%{_sysconfdir} sample%{_var}/named/slaves
install -m 644 %{SOURCE25} sample%{_sysconfdir}/named.conf
# Copy default configuration to %%doc to make it usable from system-config-bind
install -m 644 ${RPM_BUILD_ROOT}%{_sysconfdir}/named.conf named.conf.default
install -m 644 ${RPM_BUILD_ROOT}%{_sysconfdir}/named.rfc1912.zones sample%{_sysconfdir}/named.rfc1912.zones
install -m 644 ${RPM_BUILD_ROOT}%{_var}/named/named.ca sample%{_var}/named
install -m 644 ${RPM_BUILD_ROOT}%{_var}/named/named.localhost  sample%{_var}/named
install -m 644 ${RPM_BUILD_ROOT}%{_var}/named/named.loopback  sample%{_var}/named
install -m 644 ${RPM_BUILD_ROOT}%{_var}/named/named.empty  sample%{_var}/named
for f in my.internal.zone.db slaves/my.slave.internal.zone.db slaves/my.ddns.internal.zone.db my.external.zone.db; do 
  echo '@ in soa localhost. root 1 3H 15M 1W 1D
  ns localhost.' > sample%{_var}/named/$f; 
done
:;

mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/tmpfiles.d
install -m 644 %{SOURCE35} ${RPM_BUILD_ROOT}%{_sysconfdir}/tmpfiles.d/named.conf

%pre
if [ "$1" -eq 1 ]; then
  /usr/sbin/groupadd -g %{bind_gid} -f -r named >/dev/null 2>&1 || :;
  /usr/sbin/useradd  -u %{bind_uid} -r -N -M -g named -s /sbin/nologin -d /var/named -c Named named >/dev/null 2>&1 || :;
fi;
:;

%post
#/sbin/ldconfig
#/sbin/chkconfig --add named
if [ "$1" -eq 1 ]; then
  if [ ! -e %{_sysconfdir}/rndc.key ]; then
    /usr/sbin/rndc-confgen -a > /dev/null 2>&1
  fi
  [ -x /sbin/restorecon ] && /sbin/restorecon %{_sysconfdir}/rndc.* %{_sysconfdir}/named.* >/dev/null 2>&1 ;
  # rndc.key has to have correct perms and ownership, CVE-2007-6283
  [ -e %{_sysconfdir}/rndc.key ] && chown root:named %{_sysconfdir}/rndc.key
  [ -e %{_sysconfdir}/rndc.key ] && chmod 0640 %{_sysconfdir}/rndc.key
fi
:;

%preun
#if [ "$1" -eq 0 ]; then
#  /sbin/service named stop >/dev/null 2>&1 || :;
#  /sbin/chkconfig --del named || :;
#fi;
:;

%postun
#/sbin/ldconfig
#if [ "$1" -ge 1 ]; then
#  /sbin/service named try-restart >/dev/null 2>&1 || :;
#fi;
:;

%if %{SDB}
%post sdb
/sbin/service named try-restart > /dev/null 2>&1 || :;

%postun sdb
/sbin/service named try-restart > /dev/null 2>&1 || :;
%endif

%triggerpostun -n bind -- bind <= 32:9.5.0-20.b1
if [ "$1" -gt 0 ]; then
  [ -e %{_sysconfdir}/rndc.key ] && chown root:named %{_sysconfdir}/rndc.key
  [ -e %{_sysconfdir}/rndc.key ] && chmod 0640 %{_sysconfdir}/rndc.key
fi
:;


# Automatically update configuration from "dnssec-conf-based" to "BIND-based"
%triggerpostun -n bind -- dnssec-conf
if [ -r '%{_sysconfdir}/named.conf' ]; then
cp -fp %{_sysconfdir}/named.conf %{_sysconfdir}/named.conf.rpmsave
if grep -Eq '%{_sysconfdir}/(named.dnssec.keys|pki/dnssec-keys)' %{_sysconfdir}/named.conf; then
  if grep -q 'dlv.isc.org.conf' %{_sysconfdir}/named.conf; then
    # DLV is configured, reconfigure it to new configuration
    sed -i -e 's/.*dnssec-lookaside.*dlv\.isc\.org\..*/dnssec-lookaside auto;\
bindkeys-file "\%{_sysconfdir}\/named.iscdlv.key";\
managed-keys-directory "\/var\/named\/dynamic";/' %{_sysconfdir}/named.conf
  fi
  sed -i -e '/.*named\.dnssec\.keys.*/d' -e '/.*pki\/dnssec-keys.*/d' \
    %{_sysconfdir}/named.conf
  /sbin/service named try-restart > /dev/null 2>&1 || :;
fi
fi

# Ditto for chroot
if [ -r '/var/named/chroot%{_sysconfdir}/named.conf' ]; then
cp -fp /var/named/chroot%{_sysconfdir}/named.conf /var/named/chroot%{_sysconfdir}/named.conf.rpmsave
if grep -Eq '%{_sysconfdir}/(named.dnssec.keys|pki/dnssec-keys)' /var/named/chroot%{_sysconfdir}/named.conf; then
  if grep -q 'dlv.isc.org.conf' /var/named/chroot%{_sysconfdir}/named.conf; then
    # DLV is configured, reconfigure it to new configuration
    sed -i -e 's/.*dnssec-lookaside.*dlv\.isc\.org\..*/dnssec-lookaside auto;\
bindkeys-file "\/etc\/named.iscdlv.key";\
managed-keys-directory "\/var\/named\/dynamic";/' /var/named/chroot/etc/named.conf
  fi
  sed -i -e '/.*named\.dnssec\.keys.*/d' -e '/.*pki\/dnssec-keys.*/d' \
    /var/named/chroot/etc/named.conf
  /sbin/service named try-restart > /dev/null 2>&1 || :;
fi
fi

%post chroot
if [ "$1" -gt 0 ]; then
  [ -e %{chroot_prefix}/dev/random ] || \
    /bin/mknod %{chroot_prefix}/dev/random c 1 8
  [ -e %{chroot_prefix}/dev/zero ] || \
    /bin/mknod %{chroot_prefix}/dev/zero c 1 5
  [ -e %{chroot_prefix}/dev/zero ] || \
    /bin/mknod %{chroot_prefix}/dev/null c 1 3
  rm -f %{chroot_prefix}/etc/localtime
  cp /etc/localtime %{chroot_prefix}/etc/localtime
  if ! grep -q '^ROOTDIR=' /etc/sysconfig/named; then
    echo 'ROOTDIR=/var/named/chroot' >> /etc/sysconfig/named
    /sbin/service named try-restart > /dev/null 2>&1 || :;
  fi
fi;
:;

%posttrans chroot
if [ -x /usr/sbin/selinuxenabled ] && /usr/sbin/selinuxenabled; then
  [ -x /sbin/restorecon ] && /sbin/restorecon %{chroot_prefix}/dev/* > /dev/null 2>&1;
fi;
:;

%preun chroot
if [ "$1" -eq 0 ]; then
  rm -f %{chroot_prefix}/dev/{random,zero,null}
  rm -f %{chroot_prefix}/etc/localtime
  if grep -q '^ROOTDIR=' /etc/sysconfig/named; then
    # NOTE: Do NOT call `service named try-restart` because chroot
    # files will remain mounted.
    START=no
    [ -e /var/lock/subsys/named ] && START=yes
    /sbin/service named stop > /dev/null 2>&1 || :;
    sed -i -e '/^ROOTDIR=.*/d' /etc/sysconfig/named
    if [ "x$START" = xyes ]; then
      /sbin/service named start > /dev/null 2>&1 || :;
    fi
  fi
fi
:;

%clean
rm -rf ${RPM_BUILD_ROOT}
:;

%files
%defattr(-,root,root,-)
%{_libdir}/bind
#%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/sysconfig/named
%config(noreplace) %attr(0644,root,named) %{_sysconfdir}/named.iscdlv.key
%config(noreplace) %attr(0644,root,named) %{_sysconfdir}/named.root.key
%{_sysconfdir}/tmpfiles.d/named.conf
#%{_sysconfdir}/rc.d/init.d/named
#%{_sysconfdir}/NetworkManager/dispatcher.d/13-named
%{_sbindir}/arpaname.exe
%{_sbindir}/ddns-confgen.exe
%{_sbindir}/genrandom.exe
%{_sbindir}/named-journalprint.exe
%{_sbindir}/nsec3hash.exe
%{_sbindir}/dnssec*.exe
%{_sbindir}/named-check*.exe
%{_sbindir}/lwresd.exe
%{_sbindir}/named.exe
%{_sbindir}/rndc*.exe
%{_sbindir}/named-compilezone.exe
%{_sbindir}/isc-hmac-fixup.exe
%{_mandir}/man1/arpaname.1*
%{_mandir}/man5/named.conf.5*
%{_mandir}/man5/rndc.conf.5*
%{_mandir}/man8/rndc.8*
%{_mandir}/man8/named.8*
%{_mandir}/man8/lwresd.8*
%{_mandir}/man8/dnssec*.8*
%{_mandir}/man8/named-checkconf.8*
%{_mandir}/man8/named-checkzone.8*
%{_mandir}/man8/named-compilezone.8*
%{_mandir}/man8/rndc-confgen.8*
%{_mandir}/man8/ddns-confgen.8*
%{_mandir}/man8/genrandom.8*
%{_mandir}/man8/named-journalprint.8*
%{_mandir}/man8/nsec3hash.8*
%{_mandir}/man8/isc-hmac-fixup.8*
%doc CHANGES README named.conf.default
%doc doc/arm doc/misc doc/draft doc/rfc
%doc sample/

# Hide configuration
%defattr(0640,root,named,0750)
%dir %{_sysconfdir}/named
%dir %{_localstatedir}/named
%config(noreplace) %verify(not link) %{_sysconfdir}/named.conf
%config(noreplace) %verify(not link) %{_sysconfdir}/named.rfc1912.zones
%config %verify(not link) %{_localstatedir}/named/named.ca
%config %verify(not link) %{_localstatedir}/named/named.localhost
%config %verify(not link) %{_localstatedir}/named/named.loopback
%config %verify(not link) %{_localstatedir}/named/named.empty
%defattr(0660,named,named,0770)
%dir %{_localstatedir}/named/slaves
%dir %{_localstatedir}/named/data
%dir %{_localstatedir}/named/dynamic
%ghost %{_localstatedir}/log/named.log
%defattr(0640,root,named,0750)
%ghost %config(noreplace) %{_sysconfdir}/rndc.key
# ^- rndc.key now created on first install only if it does not exist
# %verify(not size,not md5) %config(noreplace) %attr(0640,root,named) /etc/rndc.conf
# ^- Let the named internal default rndc.conf be used -
#    rndc.conf not required unless it differs from default.
%ghost %config(noreplace) %{_sysconfdir}/rndc.conf
# ^- The default rndc.conf which uses rndc.key is in named's default internal config -
#    so rndc.conf is not necessary.
#%config(noreplace) %{_sysconfdir}/logrotate.d/named
%defattr(-,named,named,-)
%dir %{_localstatedir}/run/named

%if %{SDB}
%files sdb
%defattr(-,root,root,-)
%{_mandir}/man1/zone2ldap.1*
%{_mandir}/man1/ldap2zone.1*
%{_mandir}/man1/zonetodb.1*
%{_mandir}/man1/zone2sqlite.1*
%{_mandir}/man8/named-sdb.8*
%doc contrib/sdb/ldap/README.ldap contrib/sdb/ldap/INSTALL.ldap contrib/sdb/pgsql/README.sdb_pgsql
%dir %{_sysconfdir}/openldap/schema
%config(noreplace) %{_sysconfdir}/openldap/schema/dnszone.schema
%{_sbindir}/named-sdb
%{_sbindir}/zone2ldap
%{_sbindir}/ldap2zone
%{_sbindir}/zonetodb
%{_sbindir}/zone2sqlite
%endif

%files libs
%defattr(-,root,root,-)
%{_libdir}/*.dll

%files libs-lite
%defattr(-,root,root,-)
#%{_libdir}/*export.a

%files license
%defattr(-,root,root,-)
%doc COPYRIGHT

%files utils
%defattr(-,root,root,-)
%{_bindir}/dig.exe
%{_bindir}/host.exe
%{_bindir}/nslookup.exe
%{_bindir}/nsupdate.exe
%{_mandir}/man1/host.1*
%{_mandir}/man1/nsupdate.1*
%{_mandir}/man1/dig.1*
%{_mandir}/man1/nslookup.1*
%{_sysconfdir}/trusted-key.key

%if %{DEVEL}
%files devel
%defattr(-,root,root,-)
%{_libdir}/*.a
#%exclude %{_libdir}/*export.so
%{_includedir}/bind9
%{_mandir}/man1/isc-config.sh.1*
%{_mandir}/man3/lwres*
%{_bindir}/isc-config.sh
%endif

%files lite-devel
%defattr(-,root,root,-)
#%{_libdir}/*export.a
%{_includedir}/dns
%{_includedir}/dst
%{_includedir}/irs
%{_includedir}/isc
%{_includedir}/isccfg

%files chroot
%defattr(-,root,root,-)
%ghost %{chroot_prefix}/dev/null
%ghost %{chroot_prefix}/dev/random
%ghost %{chroot_prefix}/dev/zero
%ghost %{chroot_prefix}/etc/localtime
%defattr(0640,root,named,0750)
%dir %{chroot_prefix}
%dir %{chroot_prefix}/dev
%dir %{chroot_prefix}/etc
%dir %{chroot_prefix}/etc/named
%dir %{chroot_prefix}/etc/pki/dnssec-keys
%dir %{chroot_prefix}/var
%dir %{chroot_prefix}/var/run
%dir %{chroot_prefix}/var/named
%dir %{chroot_prefix}/%{_libdir}/bind
%ghost %config(noreplace) %{chroot_prefix}/etc/named.conf
%defattr(0660,named,named,0770)
%dir %{chroot_prefix}/var/run/named
%dir %{chroot_prefix}/var/tmp
%dir %{chroot_prefix}/var/log

%if %{PKCS11}
%files pkcs11
%defattr(-,root,root,-)
%doc COPYRIGHT
%{_sbindir}/pkcs11-destroy
%{_sbindir}/pkcs11-keygen
%{_sbindir}/pkcs11-list
%{_mandir}/man8/pkcs11*
%endif

%changelog
* Mon Jan 30 2012 yd
- multiprocessor support.
- thread support.
- initial unixroot build.
