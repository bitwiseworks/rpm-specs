# use nestnmp_check 0 to speed up packaging by disabling 'make test'
%if 0%{?os2_version}
%global netsnmp_check 0
%else
%{!?netsnmp_check: %global netsnmp_check 1}
%endif

# Arches on which we need to prevent arch conflicts on net-snmp-config.h
%if 0%{?os2_version}
%global multilib_arches ia64 ppc ppc64 s390 s390x x86_64 sparc sparcv9 sparc64 aarch64
%else
%global multilib_arches %{ix86} ia64 ppc ppc64 s390 s390x x86_64 sparc sparcv9 sparc64 aarch64
%endif

# actual soname version
%global soname  35

Summary:    A collection of SNMP protocol tools and libraries
Name:       net-snmp
Version:    5.8
Release:    1%{?dist}
Epoch:      1

License:    BSD
URL:        http://net-snmp.sourceforge.net/
Vendor:     bww bitwise works GmbH
%scm_source github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2

Requires:        %{name}-libs = %{epoch}:%{version}-%{release}
Requires:        %{name}-agent-libs = %{epoch}:%{version}-%{release}
# This is actually needed for the %%triggerun script but Requires(triggerun)
# is not valid.  We can use %%post because this particular %triggerun script
# should fire just after this package is installed.
%if !0%{?os2_version}
%{?systemd_requires}
BuildRequires:   systemd
%endif
BuildRequires:   gcc
%if 0%{?os2_version}
BuildRequires:   openssl-devel, bzip2-devel
%else
BuildRequires:   openssl-devel, bzip2-devel, elfutils-devel
%endif
%if 0%{?os2_version}
BuildRequires:   rpm-devel
%else
BuildRequires:   libselinux-devel, elfutils-libelf-devel, rpm-devel
%endif
%if 0%{?os2_version}
BuildRequires:   perl-devel, perl(ExtUtils::Embed)
%else
BuildRequires:   perl-devel, perl(ExtUtils::Embed), procps
%endif
%if 0%{?os2_version}
BuildRequires:   python-devel, python-setuptools
%else
BuildRequires:   python3-devel, python3-setuptools
BuildRequires:   chrpath
BuildRequires:   mariadb-connector-c-devel
# for netstat, needed by 'make test'
BuildRequires:   net-tools
%endif
# for make test
%if 0%{?os2_version}
BuildRequires:   perl >= 5.6
%else
BuildRequires:   perl(:VERSION) >= 5.6
%endif
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
Requires: %{name}-libs = %{epoch}:%{version}-%{release}

%description utils
The net-snmp-utils package contains various utilities for use with the
NET-SNMP network management project.

Install this package if you need utilities for managing your network
using the SNMP protocol. You will also need to install the net-snmp
package.

%package devel
Summary:  The development environment for the NET-SNMP project
Requires: %{name}-libs = %{epoch}:%{version}-%{release}
Requires: %{name}-agent-libs = %{epoch}:%{version}-%{release}
%if 0%{?os2_version}
Requires: rpm-devel, openssl-devel
%else
Requires: elfutils-devel, rpm-devel, elfutils-libelf-devel, openssl-devel
%ifnarch s390 s390x ppc64le
Requires: lm_sensors-devel
%endif
%endif
# pull perl development libraries, net-snmp agent libraries may link to them
Requires: perl-devel

%description devel
The net-snmp-devel package contains the development libraries and
header files for use with the NET-SNMP project's network management
tools.

Install the net-snmp-devel package if you would like to develop
applications for use with the NET-SNMP project's network management
tools. You'll also need to have the net-snmp and net-snmp-utils
packages installed.

%package perl
Summary:       The perl NET-SNMP module and the mib2c tool
%if 0%{?os2_version}
Requires:      %{name}-libs = %{epoch}:%{version}-%{release}, perl
%else
Requires:      %{name}-libs = %{epoch}:%{version}-%{release}, perl-interpreter
%endif
Requires:      %{name}-agent-libs = %{epoch}:%{version}-%{release}
Requires:      %{name}-devel = %{epoch}:%{version}-%{release}
%if 0%{?os2_version}
BuildRequires: perl
%else
BuildRequires: perl-interpreter
%endif
BuildRequires: perl-generators

%description perl
The net-snmp-perl package contains the perl files to use SNMP from within
Perl.

Install the net-snmp-perl package, if you want to use mib2c or SNMP 
with perl.

%package gui
Summary:  An interactive graphical MIB browser for SNMP
Requires: perl-Tk, net-snmp-perl = %{epoch}:%{version}-%{release}

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
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:  %{name}-libs = %{epoch}:%{version}-%{release}

%description agent-libs
The net-snmp-agent-libs package contains the runtime agent libraries for shared
binaries and applications.

%package -n python2-net-snmp
%{?python_provide:%python_provide python2-net-snmp}
#%%{?python_obsolete:%%python_obsolete python3-net-snmp}
# Remove before F30
Provides:  %{name}-python = %{version}-%{release}
Provides:  %{name}-python = %{version}-%{release}
Obsoletes: %{name}-python < %{version}-%{release}
Summary:   The Python 'netsnmp' module for the Net-SNMP
Requires:  %{name}-libs = %{epoch}:%{version}-%{release}
#
%description -n python2-net-snmp
The 'netsnmp' module provides a full featured, tri-lingual SNMP (SNMPv3,
SNMPv2c, SNMPv1) client API. The 'netsnmp' module internals rely on the
Net-SNMP toolkit library.

%if !0%{?os2_version}
%package -n python3-net-snmp
%{?python_provide:%python_provide python3-net-snmp}
# Remove before F30
Provides:  %{name}-python = %{version}-%{release}
Provides:  %{name}-python = %{version}-%{release}
Obsoletes: %{name}-python < %{version}-%{release}
Summary:   The Python 'netsnmp' module for the Net-SNMP
Requires:  %{name}-libs = %{epoch}:%{version}-%{release}

%description -n python3-net-snmp
The 'netsnmp' module provides a full featured, tri-lingual SNMP (SNMPv3, 
SNMPv2c, SNMPv1) client API. The 'netsnmp' module internals rely on the
Net-SNMP toolkit library.
%endif

%debug_package

%prep
%scm_setup

# disable failing test - see https://bugzilla.redhat.com/show_bug.cgi?id=680697
rm testing/fulltests/default/T200*

%build

# Autoreconf to get autoconf 2.69 for ARM (#926223)
autoreconf -fvi

RPM_LD_FLAGS="$RPM_LD_FLAGS -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"
export LDFLAGS="$RPM_LD_FLAGS"
export LIBS="-lcx -ltinfo"
# Set BUILDLEVEL to be embedded to all DLLs built with Libtool.
export LT_BUILDLEVEL="@#%{vendor}:%{version}-%{release}#@##1## `LANG=C date +'%%d %%b %%Y %%H:%%M:%%S'`     `uname -n`::::0::"

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
%if 0%{?os2_version}
    --enable-ipv6=no \
%else
    --enable-ipv6 \
%endif
    --enable-local-smux \
    --enable-mfd-rewrites \
    --enable-ucd-snmp-compatibility \
    --sysconfdir=%{_sysconfdir} \
    --with-cflags="$RPM_OPT_FLAGS -fPIE" \
    --with-ldflags="$RPM_LD_FLAGS -lm" \
%if 0%{?os2_version}
    --with-logfile="/@unixroot/var/log/snmpd.log" \
%else
    --with-logfile="/var/log/snmpd.log" \
    --with-mib-modules="$MIBS" \
    --with-mysql \
%endif
    --with-openssl \
%if 0%{?os2_version}
    --with-persistent-directory="/@unixroot/var/lib/net-snmp" \
%else
    --with-persistent-directory="/var/lib/net-snmp" \
%endif
    --with-perl-modules="INSTALLDIRS=vendor" \
    --with-pic \
    --with-security-modules=tsm  \
    --with-sys-location="Unknown" \
%if 0%{?os2_version}
    --with-temp-file-pattern=/@unixroot/run/net-snmp/snmp-tmp-XXXXXX \
%else
    --with-systemd \
    --with-temp-file-pattern=/run/net-snmp/snmp-tmp-XXXXXX \
%endif
    --with-transports="DTLSUDP TLSTCP" \
    --with-sys-contact="root@localhost" <<EOF
EOF

# store original libtool file, we will need it later
cp libtool libtool.orig
# remove rpath from libtool
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

# the package is not %%_smp_mflags safe
make

%if 0%{?os2_version}
# we need to manify all subdir by hand
cd perl
make manifypods
for i in default_store ASN OID agent SNMP TrapReceiver; do
  cd $i
  make manifypods
  cd ..
done
cd ..
%endif

%if !0%{?os2_version}
# remove rpath from compiled perl libs
find perl/blib -type f -name "*.so" -print -exec chrpath --delete {} \;
%endif

# compile python module
%if 0%{?os2_version}
cd python
%{__python2} setup.py --basedir="../" build
cd ..
%else
pushd python
%{__python3} setup.py --basedir="../" build
popd
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
rm -f %{buildroot}%{_bindir}/snmpinform.exe
ln -s snmptrap.exe %{buildroot}/%{_bindir}/snmpinform
rm -f %{buildroot}/%{_bindir}/snmpcheck
rm -f %{buildroot}/%{_bindir}/fixproc
rm -f %{buildroot}/%{_mandir}/man1/fixproc*
rm -f %{buildroot}/%{_bindir}/ipf-mod.pl
rm -f %{buildroot}/%{_libdir}/*.la
rm -f %{buildroot}/%{_libdir}/snmp*

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
%if 0%{?os2_version}
cd python
%{__python2} setup.py --basedir=.. install -O1 --skip-build --root %{buildroot} 
cd ..
%else
pushd python
%{__python3} setup.py --basedir=.. install -O1 --skip-build --root %{buildroot} 
popd
%endif

find %{buildroot} -name '*.dll' | xargs chmod 0755

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

# dirty hack for #603243, until it's fixed properly upstream
install -m 755 -d %{buildroot}/%{_includedir}/net-snmp/agent/util_funcs
install -m 644  agent/mibgroup/util_funcs/*.h %{buildroot}/%{_includedir}/net-snmp/agent/util_funcs

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

BEGINLIBPATH=%{buildroot}/%{_libdir} make test

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
%{_sbindir}/*
%exclude %{_sbindir}/*.dbg
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
%{_bindir}/agentxtrap.exe
%attr(0644,root,root) %{_mandir}/man1/agentxtrap.1*

%files utils
%{_bindir}/encode_keychange.exe
%{_bindir}/snmp[^c-]*
%exclude %{_bindir}/*.dbg
%attr(0644,root,root) %{_mandir}/man1/snmp[^-]*.1*
%attr(0644,root,root) %{_mandir}/man1/encode_keychange*.1*
%attr(0644,root,root) %{_mandir}/man5/snmp.conf.5.gz
%attr(0644,root,root) %{_mandir}/man5/variables.5.gz

%files devel
%{_libdir}/*_dll.a
%{_includedir}/*
%attr(0644,root,root) %{_mandir}/man3/*.3.*
%attr(0755,root,root) %{_bindir}/net-snmp-config*
%attr(0644,root,root) %{_mandir}/man1/net-snmp-config*.1.*

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
%attr(0644,root,root) %{_mandir}/man3/*.3pm.*
%attr(0644,root,root) %{_mandir}/man1/traptoemail*.1*
%attr(0644,root,root) %{_mandir}/man1/snmp-bridge-mib.1*
%{perl_vendorarch}/*SNMP*
%exclude %{perl_vendorarch}/*.dbg
%{perl_vendorarch}/auto/*SNMP*
%exclude %{perl_vendorarch}/auto/*SNMP*.dbg
%{perl_vendorarch}/auto/Bundle/*SNMP*
%{perl_vendorarch}/Bundle/MakefileSubs.pm

%if 0%{?os2_version}
%files -n python2-net-snmp
%doc README
%{python2_sitearch}/*
%else
%files -n python3-net-snmp
%doc README
%{python3_sitearch}/*
%endif

%files gui
%{_bindir}/tkmib
%attr(0644,root,root) %{_mandir}/man1/tkmib.1*

%files libs
%doc COPYING README ChangeLog.trimmed FAQ NEWS TODO
%if !0%{?os2_version}
%doc IETF-MIB-LICENSE.txt
%endif
%{_libdir}/netsnm*.dll
%dir %{_datadir}/snmp
%dir %{_datadir}/snmp/mibs
%{_datadir}/snmp/mibs/*
%dir %{_localstatedir}/lib/net-snmp
%dir %{_localstatedir}/lib/net-snmp/mib_indexes
%dir %{_localstatedir}/lib/net-snmp/cert_indexes

%files agent-libs
%{_libdir}/netsag*.dll
%{_libdir}/netshl*.dll
%{_libdir}/netsmi*.dll
%{_libdir}/netstr*.dll

%changelog
* Wed Aug 26 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1:5.8-1
- first OS/2 rpm version
