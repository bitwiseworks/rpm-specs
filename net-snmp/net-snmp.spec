# use nestnmp_check 0 to speed up packaging by disabling 'make test'
%if !0%{?os2_version}
%{!?netsnmp_check: %global netsnmp_check 1}
%else
%global netsnmp_check 0
%endif

# Arches on which we need to prevent arch conflicts on net-snmp-config.h
%if !0%{?os2_version}
%global multilib_arches %{ix86} ia64 ppc ppc64 s390 s390x x86_64 sparc sparcv9 sparc64 aarch64
%else
%global multilib_arches ia64 ppc ppc64 s390 s390x x86_64 sparc sparcv9 sparc64 aarch64
%endif

# actual soname version
%global soname  40

Summary:    A collection of SNMP protocol tools and libraries
Name:       net-snmp
Version:    5.9.4
Release:    1%{?dist}
Epoch:      1

License:    MIT-CMU AND BSD-3-Clause AND MIT
URL:        http://net-snmp.sourceforge.net/
%if !0%{?os2_version}
Source0:    https://downloads.sourceforge.net/project/net-snmp/net-snmp/%{version}/net-snmp-%{version}.tar.gz
Source1:    net-snmp.redhat.conf
Source2:    net-snmp-config.h
Source3:    net-snmp-config
Source4:    net-snmp-trapd.redhat.conf
Source5:    net-snmpd.sysconfig
Source6:    net-snmptrapd.sysconfig
Source7:    net-snmp-tmpfs.conf
Source8:    snmpd.service
Source9:    snmptrapd.service
Source10:   IETF-MIB-LICENSE.txt

Patch1:     net-snmp-5.9-pie.patch
Patch2:     net-snmp-5.9-dir-fix.patch
Patch3:     net-snmp-5.9-multilib.patch
Patch4:     net-snmp-5.9-test-debug.patch
Patch5:     net-snmp-5.7.2-cert-path.patch
Patch6:     net-snmp-5.9-cflags.patch
Patch7:     net-snmp-5.8-Remove-U64-typedef.patch
Patch8:     net-snmp-5.7.3-iterator-fix.patch
Patch9:     net-snmp-5.9-autofs-skip.patch
Patch10:    net-snmp-5.9-coverity.patch
Patch11:    net-snmp-5.8-expand-SNMPCONFPATH.patch
Patch12:    net-snmp-5.8-duplicate-ipAddress.patch
Patch13:    net-snmp-5.9-memory-reporting.patch
Patch14:    net-snmp-5.8-man-page.patch
Patch15:    net-snmp-5.8-ipAddress-faster-load.patch
Patch16:    net-snmp-5.8-rpm-memory-leak.patch
Patch17:    net-snmp-5.9-aes-config.patch
Patch18:    net-snmp-5.8-clientaddr-error-message.patch
Patch19:    net-snmp-5.9-intermediate-certs.patch
Patch20:    net-snmp-5.9.1-remove-des.patch
Patch21:    net-snmp-libs-misunderstanding.patch
Patch22:    net-snmp-5.9-ipv6-disable-leak.patch
Patch23:    net-snmp-5.9-rpmdb.patch
Patch24:    net-snmp-5.9.4-autoconf.patch
Patch25:    net-snmp-5.9.4-kernel-6.7.patch

# Modern RPM API means at least EL6
Patch101:   net-snmp-5.8-modern-rpm-api.patch

#disable this patch due compatibility issues
Patch102:   net-snmp-5.9-python3.patch
%else
Vendor:     bww bitwise works GmbH
%scm_source github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2
%endif

%if !0%{?os2_version}
Requires:        %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
Requires:        %{name}-agent-libs%{?_isa} = %{epoch}:%{version}-%{release}
%else
Requires:        %{name}-libs = %{epoch}:%{version}-%{release}
Requires:        %{name}-agent-libs = %{epoch}:%{version}-%{release}
%endif
# This is actually needed for the %%triggerun script but Requires(triggerun)
# is not valid.  We can use %%post because this particular %%triggerun script
# should fire just after this package is installed.
%if !0%{?os2_version}
%{?systemd_requires}
%endif
BuildRequires: make
%if !0%{?os2_version}
BuildRequires: libxcrypt-devel
BuildRequires:   systemd
%endif
BuildRequires:   gcc
%if !0%{?os2_version}
BuildRequires:   openssl-devel, bzip2-devel, elfutils-devel
BuildRequires:   libselinux-devel, elfutils-libelf-devel, rpm-devel
%else
BuildRequires:   openssl-devel, bzip2-devel
BuildRequires:   rpm-devel
%endif
%if !0%{?os2_version}
BuildRequires:   perl-devel, perl(ExtUtils::Embed), procps
%else
BuildRequires:   perl-devel, perl(ExtUtils::Embed)
%endif
BuildRequires:   python3-devel, python3-setuptools
%if !0%{?os2_version}
BuildRequires:   chrpath
BuildRequires:   mariadb-connector-c-devel
# for netstat, needed by 'make test'
BuildRequires:   net-tools
%endif
# for make test
BuildRequires:   perl(:VERSION) >= 5.6
BuildRequires:   perl(AutoLoader)
BuildRequires:   perl(blib)
BuildRequires:   perl(Carp)
BuildRequires:   perl(DynaLoader)
BuildRequires:   perl(Exporter)
BuildRequires:   perl(overload)
BuildRequires:   perl(strict)
BuildRequires:   perl(TAP::Harness)
BuildRequires:   perl(vars)
BuildRequires:   perl(warnings)
%if !0%{?os2_version}
%ifnarch s390 s390x ppc64le
BuildRequires:   lm_sensors-devel >= 3
%endif
%endif
BuildRequires:   autoconf, automake

%description
SNMP (Simple Network Management Protocol) is a protocol used for
network management. The NET-SNMP project includes various SNMP tools:
an extensible agent, an SNMP library, tools for requesting or setting
information from SNMP agents, tools for generating and handling SNMP
traps, a version of the netstat command which uses SNMP, and a Tk/Perl
mib browser. This package contains the snmpd and snmptrapd daemons,
documentation, etc.

You will probably also want to install the net-snmp-utils package,
which contains NET-SNMP utilities.

%package utils
Summary:  Network management utilities using SNMP, from the NET-SNMP project
%if !0%{?os2_version}
Requires: %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
%else
Requires: %{name}-libs = %{epoch}:%{version}-%{release}
%endif

%description utils
The net-snmp-utils package contains various utilities for use with the
NET-SNMP network management project.

Install this package if you need utilities for managing your network
using the SNMP protocol. You will also need to install the net-snmp
package.

%package devel
Summary:  The development environment for the NET-SNMP project
%if !0%{?os2_version}
Requires: %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
Requires: %{name}-agent-libs%{?_isa} = %{epoch}:%{version}-%{release}
%else
Requires: %{name}-libs = %{epoch}:%{version}-%{release}
Requires: %{name}-agent-libs = %{epoch}:%{version}-%{release}
%endif
%if !0%{?os2_version}
Requires: elfutils-devel, rpm-devel, elfutils-libelf-devel, openssl-devel
Requires: redhat-rpm-config
%ifnarch s390 s390x ppc64le
Requires: lm_sensors-devel
%endif
%else
Requires: rpm-devel, openssl-devel
%endif
# pull perl development libraries, net-snmp agent libraries may link to them
%if !0%{?os2_version}
Requires: perl-devel%{?_isa}
%else
Requires: perl-devel
%endif

%description devel
The net-snmp-devel package contains the development libraries and
header files for use with the NET-SNMP project's network management
tools.

Install the net-snmp-devel package if you would like to develop
applications for use with the NET-SNMP project's network management
tools. You'll also need to have the net-snmp and net-snmp-utils
packages installed.

%package perl-module
Summary:       The perl NET-SNMP module
%if !0%{?os2_version}
Requires:      %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}, perl-interpreter
%else
Requires:      %{name}-libs = %{epoch}:%{version}-%{release}, perl
%endif
BuildRequires: perl-interpreter
BuildRequires: perl-generators

%description perl-module
The net-snmp-perl package contains the perl files to use SNMP from within
Perl.

Install the net-snmp-perl package, if you want to use SNMP with perl.


%package perl
Summary:       The perl-based utilities and the mib2c tool
%if !0%{?os2_version}
Requires:      %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}, perl-interpreter
Requires:      %{name}-agent-libs%{?_isa} = %{epoch}:%{version}-%{release}
Requires:      %{name}-devel%{?_isa} = %{epoch}:%{version}-%{release}
%else
Requires:      %{name}-libs = %{epoch}:%{version}-%{release}, perl
Requires:      %{name}-agent-libs = %{epoch}:%{version}-%{release}
Requires:      %{name}-devel = %{epoch}:%{version}-%{release}
%endif
BuildRequires: perl-interpreter
BuildRequires: perl-generators

%description perl
The net-snmp-perl package contains the utilities written in perl.

Install the net-snmp-perl package, if you want to use mib2c or other
perl utilities. Use the net-snmp-perl-module package instead to get the
SNMP perl module.

%package gui
Summary:  An interactive graphical MIB browser for SNMP
%if !0%{?os2_version}
Requires: perl-Tk, %{name}-perl-module%{?_isa} = %{epoch}:%{version}-%{release}
%else
Requires: perl-Tk, %{name}-perl-module = %{epoch}:%{version}-%{release}
%endif
BuildRequires: perl-interpreter
BuildRequires: perl-generators

%description gui
The net-snmp-gui package contains tkmib utility, which is a graphical user 
interface for browsing the Message Information Bases (MIBs). It is also 
capable of sending or retrieving the SNMP management information to/from 
the remote agents interactively.

Install the net-snmp-gui package, if you want to use this interactive utility.

%package libs
Summary: The NET-SNMP runtime client libraries

%description libs
The net-snmp-libs package contains the runtime client libraries for shared
binaries and applications.

%package agent-libs
Summary:   The NET-SNMP runtime agent libraries
# the libs link against libperl.so:
%if !0%{?os2_version}
Requires:  %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
%else
Requires:  %{name}-libs = %{epoch}:%{version}-%{release}
%endif

%description agent-libs
The net-snmp-agent-libs package contains the runtime agent libraries for shared
binaries and applications.

%package -n python3-net-snmp
%{?python_provide:%python_provide python3-net-snmp}
# Remove before F30
Provides:  %{name}-python = %{version}-%{release}
%if !0%{?os2_version}
Provides:  %{name}-python%{?_isa} = %{version}-%{release}
%endif
Obsoletes: %{name}-python < %{version}-%{release}
Summary:   The Python 'netsnmp' module for the Net-SNMP
%if !0%{?os2_version}
Requires:  %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
%else
Requires:  %{name}-libs = %{epoch}:%{version}-%{release}
%endif

%description -n python3-net-snmp
The 'netsnmp' module provides a full featured, tri-lingual SNMP (SNMPv3, 
SNMPv2c, SNMPv1) client API. The 'netsnmp' module internals rely on the
Net-SNMP toolkit library.

%if !0%{?os2_version}
%debug_package
%endif

%prep
%if !0%{?os2_version}
%setup -q
cp %{SOURCE10} .

%ifnarch ia64
%patch 1 -p1 -b .pie
%endif

%patch 2 -p1 -b .dir-fix
%patch 3 -p1 -b .multilib
%patch 4 -p1
%patch 5 -p1 -b .cert-path
%patch 6 -p1 -b .cflags
%patch 7 -p1 -b .u64-remove
%patch 8 -p1 -b .iterator-fix
%patch 9 -p1 -b .autofs-skip
%patch 10 -p1 -b .coverity
%patch 11 -p1 -b .expand-SNMPCONFPATH
%patch 12 -p1 -b .duplicate-ipAddress
%patch 13 -p1 -b .memory-reporting
%patch 14 -p1 -b .man-page
%patch 15 -p1 -b .ipAddress-faster-load
%patch 16 -p1 -b .rpm-memory-leak
%patch 17 -p1 -b .aes-config
%patch 18 -p1 -b .clientaddr-error-message
%patch 19 -p1 -b .intermediate-certs
%patch 20 -p1 -b .remove-des
%patch 21 -p1
%patch 22 -p1 -b .ipv6-disable-leak
%patch 23 -p1 -b .rpmdbpatch
%patch 24 -p1 
%patch 25 -p1 -b .kernel-6.7

%patch 101 -p1 -b .modern-rpm-api
%patch 102 -p1
%else
%scm_setup
%endif

# disable failing test - see https://bugzilla.redhat.com/show_bug.cgi?id=680697
rm testing/fulltests/default/T200*

%build

# Autoreconf to get autoconf 2.69 for ARM (#926223)
%if !0%{?os2_version}
autoreconf
%else
autoreconf -fvi

RPM_LD_FLAGS="$RPM_LD_FLAGS -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"
export LDFLAGS="$RPM_LD_FLAGS"
export LIBS="-lcx -ltinfo"
# Set BUILDLEVEL to be embedded to all DLLs built with Libtool.
export LT_BUILDLEVEL="@#%{vendor}:%{version}-%{release}#@##1## `LANG=C date +'%%d %%b %%Y %%H:%%M:%%S'`     `uname -n`::::0::"
%endif

%if !0%{?os2_version}
MIBS="host agentx smux \
     ucd-snmp/diskio tcp-mib udp-mib mibII/mta_sendmail \
     ip-mib/ipv4InterfaceTable ip-mib/ipv6InterfaceTable \
     ip-mib/ipAddressPrefixTable/ipAddressPrefixTable \
     ip-mib/ipDefaultRouterTable/ipDefaultRouterTable \
     ip-mib/ipv6ScopeZoneIndexTable ip-mib/ipIfStatsTable \
     sctp-mib rmon-mib etherlike-mib"

%ifnarch s390 s390x ppc64le
# there are no lm_sensors on s390
MIBS="$MIBS ucd-snmp/lmsensorsMib"
%endif
%endif

%configure \
    --disable-static --enable-shared \
    --enable-as-needed \
    --enable-blumenthal-aes \
    --enable-embedded-perl \
%if !0%{?os2_version}
    --enable-ipv6 \
%else
    --enable-ipv6=no \
%endif
    --enable-local-smux \
    --enable-mfd-rewrites \
    --enable-ucd-snmp-compatibility \
    --disable-des \
    --sysconfdir=%{_sysconfdir} \
    --with-cflags="$RPM_OPT_FLAGS -fPIE" \
    --with-ldflags="$RPM_LD_FLAGS -lm" \
%if !0%{?os2_version}
    --with-logfile="/var/log/snmpd.log" \
    --with-mib-modules="$MIBS" \
    --with-mysql \
%else
    --with-logfile="/@unixroot/var/log/snmpd.log" \
%endif
    --with-openssl \
%if !0%{?os2_version}
    --with-persistent-directory="/var/lib/net-snmp" \
%else
    --with-persistent-directory="/@unixroot/var/lib/net-snmp" \
%endif
    --with-perl-modules="INSTALLDIRS=vendor" \
    --with-pic \
    --with-security-modules=tsm  \
    --with-sys-location="Unknown" \
%if !0%{?os2_version}
    --with-systemd \
    --with-temp-file-pattern=/run/net-snmp/snmp-tmp-XXXXXX \
%else
    --with-temp-file-pattern=/@unixroot/run/net-snmp/snmp-tmp-XXXXXX \
%endif
    --with-transports="DTLSUDP TLSTCP" \
    --with-sys-contact="root@localhost" \
    --without-pcre <<EOF
EOF

# store original libtool file, we will need it later
cp libtool libtool.orig
# remove rpath from libtool
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

# the package is not %%_smp_mflags safe
%{__make}

%if !0%{?os2_version}
# remove rpath from compiled perl libs
find perl/blib -type f -name "*.so" -print -exec chrpath --delete {} \;
%endif

# compile python module
%if !0%{?os2_version}
pushd python
%else
cd python
%endif
%{__python3} setup.py --basedir="../" build
%if !0%{?os2_version}
popd
%else
cd ..
%endif


%install
make install DESTDIR=%{buildroot}

# Determine which arch net-snmp-config.h is going to try to #include.
basearch=%{_arch}
%ifarch %{ix86}
basearch=i386
%endif

%ifarch %{multilib_arches}
# Do an net-snmp-config.h switcheroo to avoid file conflicts on systems where you
# can have both a 32- and 64-bit version of the library, as they each need
# their own correct-but-different versions of net-snmp-config.h to be usable.
mv %{buildroot}/%{_bindir}/net-snmp-config %{buildroot}/%{_bindir}/net-snmp-config-${basearch}
install -m 755 %SOURCE3 %{buildroot}/%{_bindir}/net-snmp-config
mv %{buildroot}/%{_includedir}/net-snmp/net-snmp-config.h %{buildroot}/%{_includedir}/net-snmp/net-snmp-config-${basearch}.h
install -m644 %SOURCE2 %{buildroot}/%{_includedir}/net-snmp/net-snmp-config.h
%endif

install -d %{buildroot}%{_sysconfdir}/snmp
%if !0%{?os2_version}
install -m 644 %SOURCE1 %{buildroot}%{_sysconfdir}/snmp/snmpd.conf
install -m 644 %SOURCE4 %{buildroot}%{_sysconfdir}/snmp/snmptrapd.conf
%endif

install -d %{buildroot}%{_sysconfdir}/sysconfig
%if !0%{?os2_version}
install -m 644 %SOURCE5 %{buildroot}%{_sysconfdir}/sysconfig/snmpd
install -m 644 %SOURCE6 %{buildroot}%{_sysconfdir}/sysconfig/snmptrapd
%endif

# prepare /var/lib/net-snmp
install -d %{buildroot}%{_localstatedir}/lib/net-snmp
install -d %{buildroot}%{_localstatedir}/lib/net-snmp/mib_indexes
install -d %{buildroot}%{_localstatedir}/lib/net-snmp/cert_indexes
install -d %{buildroot}%{_localstatedir}/run/net-snmp

# remove things we don't want to distribute
%if !0%{?os2_version}
rm -f %{buildroot}%{_bindir}/snmpinform
ln -s snmptrap %{buildroot}/usr/bin/snmpinform
%else
rm -f %{buildroot}%{_bindir}/snmpinform.exe
ln -s snmptrap.exe %{buildroot}/%{_bindir}/snmpinform
%endif
rm -f %{buildroot}%{_bindir}/snmpcheck
rm -f %{buildroot}/%{_bindir}/fixproc
rm -f %{buildroot}/%{_mandir}/man1/fixproc*
rm -f %{buildroot}/%{_bindir}/ipf-mod.pl
rm -f %{buildroot}/%{_libdir}/*.la
%if !0%{?os2_version}
rm -f %{buildroot}/%{_libdir}/libsnmp*
%else
rm -f %{buildroot}/%{_libdir}/snmp*
%endif
rm -f %{buildroot}/%{_libdir}/perl5/vendor_perl/Bundle/MakefileSubs.pm

# remove special perl files
find %{buildroot} -name perllocal.pod \
    -o -name .packlist \
    -o -name "*.bs" \
    -o -name Makefile.subs.pl \
    | xargs -ri rm -f {}
# remove docs that do not apply to Linux
rm -f README.aix README.hpux11 README.osX README.Panasonic_AM3X.txt README.solaris README.win32

# copy missing mib2c.conf files
install -m 644 local/mib2c.*.conf %{buildroot}%{_datadir}/snmp

# install python module
%if !0%{?os2_version}
pushd python
%else
cd python
%endif
%{__python3} setup.py --basedir=.. install -O1 --skip-build --root %{buildroot} 
%if !0%{?os2_version}
popd
%else
cd ..
%endif

%if !0%{?os2_version}
find %{buildroot} -name '*.so' | xargs chmod 0755
%else
find %{buildroot} -name '*.dll' | xargs chmod 0755
%endif

# trim down massive ChangeLog
dd bs=1024 count=250 if=ChangeLog of=ChangeLog.trimmed

# convert files to UTF-8
%if !0%{?os2_version}
for file in README COPYING; do
    iconv -f 8859_1 -t UTF-8 <$file >$file.utf8
    mv $file.utf8 $file
done
%endif

# remove executable bit from documentation samples
chmod 644 local/passtest local/ipf-mod.pl

# systemd stuff
%if !0%{?os2_version}
install -m 755 -d %{buildroot}/%{_tmpfilesdir}
install -m 644 %SOURCE7 %{buildroot}/%{_tmpfilesdir}/net-snmp.conf
install -m 755 -d %{buildroot}/%{_unitdir}
install -m 644 %SOURCE8 %SOURCE9 %{buildroot}/%{_unitdir}/
%endif

%check
%if %{netsnmp_check}
%ifarch ppc ppc64
rm -vf testing/fulltests/default/T200snmpv2cwalkall_simple
%endif
# restore libtool, for unknown reason it does not work with the one without rpath
cp -f libtool.orig libtool
# temporary workaround to make test "extending agent functionality with pass" working
chmod 755 local/passtest

%if !0%{?os2_version}
LD_LIBRARY_PATH=%{buildroot}/%{_libdir} make test
%else
BEGINLIBPATH=%{buildroot}/%{_libdir} make test
%endif
%endif


%post
%if !0%{?os2_version}
%systemd_post snmpd.service snmptrapd.service
%endif

%preun
%if !0%{?os2_version}
%systemd_preun snmpd.service snmptrapd.service
%endif


%postun
%if !0%{?os2_version}
%systemd_postun_with_restart snmpd.service snmptrapd.service
%endif

%if !0%{?os2_version}
%ldconfig_scriptlets libs
%ldconfig_scriptlets agent-libs
%endif

%files
%doc COPYING ChangeLog.trimmed EXAMPLE.conf FAQ NEWS TODO
%doc README README.agent-mibs README.agentx README.krb5 README.snmpv3
%doc local/passtest local/ipf-mod.pl
%doc README.thread AGENT.txt PORTING local/README.mib2c
%if !0%{?os2_version}
%doc IETF-MIB-LICENSE.txt
%endif
%dir %{_sysconfdir}/snmp
%if !0%{?os2_version}
%config(noreplace) %attr(0600,root,root) %{_sysconfdir}/snmp/snmpd.conf
%config(noreplace) %attr(0600,root,root) %{_sysconfdir}/snmp/snmptrapd.conf
%endif
%{_bindir}/snmpconf
%{_bindir}/net-snmp-create-v3-user
%if !0%{?os2_version}
%{_sbindir}/snmpd
%{_sbindir}/snmptrapd
%else
%{_sbindir}/snmpd.exe
%{_sbindir}/snmptrapd.exe
%endif
%attr(0644,root,root) %{_mandir}/man[58]/snmp*d*
%attr(0644,root,root) %{_mandir}/man5/snmp_config.5.gz
%attr(0644,root,root) %{_mandir}/man5/variables*
%attr(0644,root,root) %{_mandir}/man1/net-snmp-create-v3-user*
%attr(0644,root,root) %{_mandir}/man1/snmpconf.1.gz
%dir %{_datadir}/snmp
%{_datadir}/snmp/snmpconf-data
%dir %{_localstatedir}/run/net-snmp
%if !0%{?os2_version}
%{_tmpfilesdir}/net-snmp.conf
%{_unitdir}/snmp*
%config(noreplace) %{_sysconfdir}/sysconfig/snmpd
%config(noreplace) %{_sysconfdir}/sysconfig/snmptrapd
%endif
%if !0%{?os2_version}
%{_bindir}/agentxtrap
%else
%{_bindir}/agentxtrap.exe
%endif
%attr(0644,root,root) %{_mandir}/man1/agentxtrap.1*

%files utils
%if !0%{?os2_version}
%{_bindir}/encode_keychange
%else
%{_bindir}/encode_keychange.exe
%endif
%{_bindir}/snmp[^c-]*
%if 0%{?os2_version}
%exclude %{_bindir}/*.dbg
%endif
%attr(0644,root,root) %{_mandir}/man1/snmp[^-]*.1*
%attr(0644,root,root) %{_mandir}/man1/encode_keychange*.1*
%attr(0644,root,root) %{_mandir}/man5/snmp.conf.5.gz
%attr(0644,root,root) %{_mandir}/man5/variables.5.gz

%files devel
%if !0%{?os2_version}
%{_libdir}/lib*.so
%else
%{_libdir}/*_dll.a
%endif
%{_libdir}/pkgconfig/*
%{_includedir}/*
%attr(0644,root,root) %{_mandir}/man3/*.3.*
%attr(0755,root,root) %{_bindir}/net-snmp-config*
%attr(0644,root,root) %{_mandir}/man1/net-snmp-config*.1.*

%files perl-module
%attr(0644,root,root) %{_mandir}/man3/*.3pm.*
%{perl_vendorarch}/*SNMP*
%if 0%{?os2_version}
%exclude %{perl_vendorarch}/*.dbg
%endif
%{perl_vendorarch}/auto/*SNMP*
%if 0%{?os2_version}
%exclude %{perl_vendorarch}/auto/*SNMP*.dbg
%endif
%{perl_vendorarch}/auto/Bundle/*SNMP*

%files perl
%{_bindir}/mib2c-update
%{_bindir}/mib2c
%{_bindir}/snmp-bridge-mib
%{_bindir}/net-snmp-cert
%{_bindir}/checkbandwidth
%dir %{_datadir}/snmp
%{_datadir}/snmp/mib2c*
%{_datadir}/snmp/*.pl
%{_bindir}/traptoemail
%attr(0644,root,root) %{_mandir}/man[15]/mib2c*
%attr(0644,root,root) %{_mandir}/man1/traptoemail*.1*
%attr(0644,root,root) %{_mandir}/man1/snmp-bridge-mib.1*

%files -n python3-net-snmp
%doc README
%{python3_sitearch}/*

%files gui
%{_bindir}/tkmib
%attr(0644,root,root) %{_mandir}/man1/tkmib.1*

%files libs
%doc COPYING README ChangeLog.trimmed FAQ NEWS TODO
%if !0%{?os2_version}
%doc IETF-MIB-LICENSE.txt
%{_libdir}/libnetsnmp.so.%{soname}*
%else
%{_libdir}/netsnm*.dll
%endif
%dir %{_datadir}/snmp
%dir %{_datadir}/snmp/mibs
%{_datadir}/snmp/mibs/*
%dir %{_localstatedir}/lib/net-snmp
%dir %{_localstatedir}/lib/net-snmp/mib_indexes
%dir %{_localstatedir}/lib/net-snmp/cert_indexes

%files agent-libs
%if !0%{?os2_version}
%{_libdir}/libnetsnmpagent*.so.%{soname}*
%{_libdir}/libnetsnmphelpers*.so.%{soname}*
%{_libdir}/libnetsnmpmibs*.so.%{soname}*
%{_libdir}/libnetsnmptrapd*.so.%{soname}*
%else
%{_libdir}/netsag*.dll
%{_libdir}/netshl*.dll
%{_libdir}/netsmi*.dll
%{_libdir}/netstr*.dll
%endif

%changelog
* Fri Feb 21 2025 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1:5.9.4-1
- update to version 5.9.4
- resync with fedory spec

* Wed Aug 26 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1:5.8-1
- first OS/2 rpm version
