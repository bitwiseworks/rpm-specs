%global _hardened_build 1
%if !0%{?os2_version}
%global libdir %{_libdir}/heimdal
%global bindir %{_exec_prefix}/lib/heimdal
%else
%global libdir %{_libdir}
%global bindir %{_bindir}
%endif

# Use systemd unit files on RHEL 7 and above.
%if !0%{?os2_version}
%if ! (0%{?rhel} && 0%{?rhel} < 7)
  %global _with_systemd 1
%endif
%endif

Name: heimdal
Version: 7.7.0
Release: 1%{?dist}
Summary: A Kerberos 5 implementation without export restrictions
License: BSD and MIT
URL: http://www.heimdal.software/
Vendor: bww bitwise works GmbH
%scm_source  github https://github.com/bitwiseworks/%{name}-os2 %{name}-%{version}-os2

Source3:  %{name}.sysconfig
%if !0%{?os2_version}
Source4:  %{name}.sh
Source5:  %{name}.csh
%endif
Source9:  krb5.conf.sample
%if !0%{?os2_version}
Source10: %{name}.logrotate
Source11: %{name}-bashrc
Source20: %{name}-kdc.init
Source21: %{name}-ipropd-master.init
Source22: %{name}-ipropd-slave.init
Source23: %{name}-kadmind.init
Source24: %{name}-kpasswdd.init
%endif
Source25: %{name}-kdc.conf
%if !0%{?os2_version}
Source26: %{name}-kdc.service
Source27: %{name}-ipropd-master.service
Source28: %{name}-ipropd-slave.service
Source29: %{name}-kadmind.service
Source30: %{name}-kpasswdd.service
Source31: %{name}-ipropd-slave-wrapper
%endif

BuildRequires:  gettext
BuildRequires:  bison
BuildRequires:  flex
%if !0%{?os2_version}
BuildRequires:  libedit-devel
%endif
BuildRequires:  readline-devel
BuildRequires:  libtool
BuildRequires:  ncurses-devel
%if !0%{?os2_version}
BuildRequires:  openldap-devel
#Required for tests/ldap
%if (0%{?rhel} && 0%{?rhel} > 7)
# but not available on RHEL 8
%else
BuildRequires:  openldap-servers
%endif
BuildRequires:  pam-devel
%endif
BuildRequires:  perl(JSON)
BuildRequires:  sqlite-devel
BuildRequires:  texinfo
%if !0%{?os2_version}
BuildRequires:  libcom_err-devel
BuildRequires:  libcap-ng-devel
%endif
%if (0%{?rhel} && 0%{?rhel} < 7) || 0%{?os2_version}
BuildRequires:  db4-devel
%else
BuildRequires:  libdb-devel
%endif
BuildRequires:  doxygen
%if !0%{?os2_version}
BuildRequires:  graphviz
%endif
%if 0%{?os2_version}
BuildRequires:  python2
%else
BuildRequires:  python3
%endif
%if (0%{?rhel} && 0%{?rhel} < 7)
BuildRequires:  groff
%else
BuildRequires:  groff-base
%endif
%if 0%{?_with_systemd}
BuildRequires: systemd-units
%endif

# Bundled libtommath (https://bugzilla.redhat.com/1118462)
Provides: bundled(libtommath) = 0.42.0

# This macro was added in Fedora 20. Use the old version if it's undefined
# on older Fedoras and RHELs prior to RHEL 8.
# https://fedoraproject.org/wiki/Changes/UnversionedDocdirs
%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

%description
Kerberos 5 is a network authentication and single sign-on system.
Heimdal is a free Kerberos 5 implementation without export restrictions
written from the spec (rfc1510 and successors) including advanced features
like thread safety, IPv6, master-slave replication of Kerberos Key
Distribution Center server and support for ticket delegation (S4U2Self,
S4U2Proxy).
This package can coexist with MIT Kerberos 5 packages. Hesiod is disabled
by default since it is deemed too big a security risk by the packager.

%package    workstation
Summary:    Heimdal kerberos programs for use on workstations

%description workstation
This package contains Heimdal Kerberos 5 programs and utilities for
use on workstations (kinit, klist, kdestroy, kpasswd)

%package server
Summary:  Heimdal kerberos server
%if !0%{?os2_version}
Requires: logrotate
%endif
%if 0%{?_with_systemd}
Requires(preun): systemd
Requires(postun): systemd
Requires(post): systemd
%else
%if !0%{?os2_version}
Requires(post): chkconfig
Requires(preun): chkconfig
Requires(preun): initscripts
Requires(postun): initscripts
%endif
%endif
Provides: heimdal-kdc = %{version}-%{release}
Obsoletes: heimdal-kdc < 1.5

%description server
This package contains the master Heimdal kerberos Key Distribution
Center (KDC), admin interface server (admind) and master-slave
synchronisation daemons. Install this package if you intend to
set up Kerberos server.

%package libs
Summary: Heimdal kerberos shared libraries
Requires(post): info
Requires(preun): info

%description libs
This package contains shared libraries required by several of the other
Heimdal packages.

%package devel
Summary:  Header and other development files for Heimdal kerberos
Provides: %{name}-static = %{version}-%{release}

%description devel
Contains files needed to compile and link software using the Heimdal
kerberos headers/libraries.

%if !0%{?os2_version}
%package path
Summary: Heimdal kerberos PATH manipulation
Requires: %{name}-libs
# For /etc/profile.d
Requires: setup

%description path
This package prepends the Heimdal binary directory to the beginning of
PATH.
%endif

%debug_package

%prep
%scm_setup
./autogen.sh


%build
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx -ltinfo"
export VENDOR="%{vendor}"

%if !0%{?os2_version}
%ifarch i386
%global build_fix "-march=i686"
%else
%global build_fix ""
%endif
%else
%global build_fix ""
%endif
%configure \
        --prefix=%{_prefix} \
        --includedir=%{_includedir}/%{name} \
%if !0%{?os2_version}
        --libdir=%{libdir} \
        --enable-static \
%endif
        --enable-shared \
        --enable-pthread-support \
        --without-x \
        --without-hesiod \
%if !0%{?os2_version}
        --with-ipv6 \
%else
        --without-ipv6 \
%endif
        --enable-kcm \
        --enable-pk-init \
%if !0%{?os2_version}
        --with-openldap=%{_prefix} \
%endif
        --with-sqlite3=%{_prefix} \
        --with-readline=%{_prefix} \
%if !0%{?os2_version}
        --with-libedit=%{_prefix} \
%endif
%if 0%{?os2_version}
        --disable-mmap \
%endif
        CFLAGS="%{optflags} %{build_fix}"

export BEGINLIBPATH=%{_builddir}/%{buildsubdir}/lib/roken/.libs
make -C include krb5-types.h
make
make -C doc html

# po/localefiles is not in the tarball, which causes install to fail
touch po/localefiles
make -C po mo

%check
# Several intermittent test failures here, so make this non-fatal:
# (timeout to debug hard to reproduce stuck build)
%if !0%{?os2_version}
timeout 20m %make_build check || :
%endif

%install
%make_install
# install the init files
%if 0%{?_with_systemd}
  # install systemd service files
  mkdir -p %{buildroot}%{_unitdir}
  pushd %{buildroot}%{_unitdir}
    install -p -D -m 644 %{SOURCE26} heimdal-kdc.service
    install -p -D -m 644 %{SOURCE27} heimdal-ipropd-master.service
    install -p -D -m 644 %{SOURCE28} heimdal-ipropd-slave.service
    install -p -D -m 644 %{SOURCE29} heimdal-kadmind.service
    install -p -D -m 644 %{SOURCE30} heimdal-kpasswdd.service
  popd
  install -p -D -m 755 %{SOURCE31} %{buildroot}%{_libexecdir}/ipropd-slave-wrapper
%else
%if !0%{?os2_version}
  # install legacy SysV init scripts
  mkdir -p %{buildroot}%{_sysconfdir}/rc.d/init.d
  pushd %{buildroot}%{_sysconfdir}/rc.d/init.d
    install -p -D -m 755 %{SOURCE20} heimdal-kdc
    install -p -D -m 755 %{SOURCE21} heimdal-ipropd-master
    install -p -D -m 755 %{SOURCE22} heimdal-ipropd-slave
    install -p -D -m 755 %{SOURCE23} heimdal-kadmind
    install -p -D -m 755 %{SOURCE24} heimdal-kpasswdd
  popd
%endif
%endif
install -p -D -m 644 %{SOURCE3}  %{buildroot}%{_sysconfdir}/sysconfig/heimdal
%if !0%{?os2_version}
install -p -D -m 644 %{SOURCE4}  %{buildroot}%{_sysconfdir}/profile.d/heimdal.sh
install -p -D -m 644 %{SOURCE5}  %{buildroot}%{_sysconfdir}/profile.d/heimdal.csh
install -p -D -m 644 %{SOURCE10} %{buildroot}%{_sysconfdir}/logrotate.d/heimdal
%endif
mkdir -p %{buildroot}%{_localstatedir}/heimdal/
install -p -D -m 755 %{SOURCE25}  %{buildroot}%{_sysconfdir}/heimdal-kdc.conf
ln -s %{_sysconfdir}/heimdal-kdc.conf %{buildroot}%{_localstatedir}/heimdal/kdc.conf
echo "# see man heimdal-kadmind(8)" > %{buildroot}%{_sysconfdir}/heimdal-kadmind.acl
ln -s %{_sysconfdir}/heimdal-kadmind.acl %{buildroot}%{_localstatedir}/heimdal/kadmind.acl
touch    %{buildroot}%{_sysconfdir}/heimdal-slaves
ln -s %{_sysconfdir}/heimdal-slaves %{buildroot}%{_localstatedir}/heimdal/slaves
install -d -m 700 %{buildroot}%{_localstatedir}/log/heimdal
install -d -m 755 %{buildroot}/%{_pkgdocdir}
install -p -D -m 644 LICENSE    %{buildroot}/%{_pkgdocdir}/LICENSE
install -p -D -m 644 %{SOURCE9} %{buildroot}/%{_pkgdocdir}/krb5.conf.sample
%if !0%{?os2_version}
install -p -D -m 644 %{SOURCE11} %{buildroot}/%{_pkgdocdir}/bashrc
%endif
# we don't need pkgconfig file and info/dir
rm -rf %{buildroot}%{libdir}/pkgconfig
rm -rf %{buildroot}%{_infodir}/dir
# NOTICE: no support for X11
rm -f %{buildroot}%{_mandir}/man1/kx.1*
rm -f %{buildroot}%{_mandir}/man1/rxtelnet.1*
rm -f %{buildroot}%{_mandir}/man1/rxterm.1*
rm -f %{buildroot}%{_mandir}/man1/tenletxr.1*
rm -f %{buildroot}%{_mandir}/man1/xnlock.1*
rm -f %{buildroot}%{_mandir}/man8/kxd.8*
# Remove CAT files, they are not needed
rm -rf %{buildroot}%{_mandir}/cat*
# Remove libtool archives
find %{buildroot} -type f -name '*.la' -exec rm -f {} ';'

%if !0%{?os2_version}
mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d/
cat >> %{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf << EOF
%{_libdir}/%{name}
EOF

mkdir -p %{buildroot}%{bindir}/bin
mkdir -p %{buildroot}%{_mandir}/%{name}/man{1,5,8}

# rename clashes with other pkgs from <app> to heimdal-<app>
for prog in kadmin kadmind kdestroy kinit klist kpasswd krb5-config ktutil su pagsh compile_et
do
   if [ -e %{buildroot}%{_bindir}/${prog} ]; then
     mv %{buildroot}%{_bindir}/{,%{name}-}${prog}
     ln -s %{_bindir}/%{name}-${prog} %{buildroot}%{bindir}/bin/${prog}
   elif [ -e %{buildroot}%{_sbindir}/${prog} ]; then
     mv %{buildroot}%{_sbindir}/{,%{name}-}${prog}
     ln -s %{_sbindir}/%{name}-${prog} %{buildroot}%{bindir}/bin/${prog}
   elif [ -e %{buildroot}%{_libexecdir}/${prog} ]; then
     mv %{buildroot}%{_libexecdir}/{,%{name}-}${prog}
   fi

   if [ -e %{buildroot}%{_mandir}/man1/${prog}.1 ]; then
     mv %{buildroot}%{_mandir}/man1/{,%{name}-}${prog}.1
   elif [ -e %{buildroot}%{_mandir}/man8/${prog}.8 ]; then
     mv %{buildroot}%{_mandir}/man8/{,%{name}-}${prog}.8
   fi
done

# If we have the prefixed name in one pkg we want it in all.
mv %{buildroot}%{_bindir}/{,%{name}-}kswitch
ln -s %{_bindir}/%{name}-kswitch %{buildroot}%{bindir}/bin/kswitch
mv %{buildroot}%{_mandir}/man1/{,%{name}-}kswitch.1
%endif

ln -s %{_bindir}/kinit.exe %{buildroot}%{_bindir}/kauth

%if !0%{?os2_version}
mv %{buildroot}%{_mandir}/man5/{,%{name}-}krb5.conf.5
%endif

rm %{buildroot}%{_mandir}/man5/qop.5
ln -s mech.5.gz %{buildroot}%{_mandir}/man5/qop.5.gz

%find_lang %{name} --all-name

%post server
%if 0%{?_with_systemd}
  %systemd_post heimdal-kdc.service
  %systemd_post heimdal-ipropd-master.service
  %systemd_post heimdal-ipropd-slave.service
  %systemd_post heimdal-kadmind.service
  %systemd_post heimdal-kpasswdd.service
%else
%if !0%{?os2_version}
  /sbin/chkconfig --add heimdal-kdc
  /sbin/chkconfig --add heimdal-ipropd-master
  /sbin/chkconfig --add heimdal-ipropd-slave
  /sbin/chkconfig --add heimdal-kadmind
  /sbin/chkconfig --add heimdal-kpasswdd
%endif
%endif

%preun server
%if 0%{?_with_systemd}
  %systemd_preun heimdal-kdc.service
  %systemd_preun heimdal-ipropd-master.service
  %systemd_preun heimdal-ipropd-slave.service
  %systemd_preun heimdal-kadmind.service
  %systemd_preun heimdal-kpasswdd.service
%else
%if !0%{?os2_version}
  if [ $1 -eq 0 ] ; then
     /sbin/service heimdal-kdc stop >/dev/null 2>&1 || :
     /sbin/chkconfig --del heimdal-kdc
     /sbin/service heimdal-ipropd-master stop >/dev/null 2>&1 || :
     /sbin/chkconfig --del heimdal-ipropd-master
     /sbin/service heimdal-ipropd-slave stop >/dev/null 2>&1 || :
     /sbin/chkconfig --del heimdal-ipropd-slave
     /sbin/service heimdal-kadmind stop >/dev/null 2>&1 || :
     /sbin/chkconfig --del heimdal-kadmind
     /sbin/service heimdal-kpasswdd stop >/dev/null 2>&1 || :
     /sbin/chkconfig --del >/dev/null
  fi
%endif
%endif

%postun server
%if 0%{?_with_systemd}
  %systemd_postun heimdal-kdc.service
  %systemd_postun heimdal-ipropd-master.service
  %systemd_postun heimdal-ipropd-slave.service
  %systemd_postun heimdal-kadmind.service
  %systemd_postun heimdal-kpasswdd.service
%else
%if !0%{?os2_version}
  if [ $1 -eq 1 ] ; then
     /sbin/service heimdal-kdc condrestart >/dev/null 2>&1 || :
     /sbin/service heimdal-ipropd-master condrestart >/dev/null 2>&1 || :
     /sbin/service heimdal-ipropd-slave condrestart >/dev/null 2>&1 || :
     /sbin/service heimdal-kadmind condrestart >/dev/null 2>&1 || :
     /sbin/service heimdal-kpasswdd condrestart >/dev/null 2>&1 || :
  fi
%endif
%endif

%if (0%{?rhel} && 0%{?rhel} < 8)
%post libs
%{_sbindir}/ldconfig
%{_sbindir}/install-info %{_infodir}/%{name}.info %{_infodir}/dir || :


%preun libs
if [ $1 = 0 ] ; then
  %{_sbindir}/install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir || :
fi

%postun libs
%{_sbindir}/ldconfig
%endif

%files libs -f %{name}.lang
%if !0%{?os2_version}
%dir %{bindir}
%dir %{bindir}/bin
%dir %{libdir}
%endif
%if !0%{?os2_version}
%config(noreplace) %{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf
%{libdir}/lib*.so*
%{libdir}/windc.so*
%else
%{libdir}/*.dll
%endif
%{_infodir}/heimdal.info*
%{_infodir}/hx509.info*
%{_mandir}/man5/krb5.conf.5*
%{_mandir}/man5/qop.5*
%{_mandir}/man5/mech.5*
%{_mandir}/man8/kerberos.8*
%{_prefix}/bin/string2key.exe
%{_mandir}/man8/string2key.8*
%{_libexecdir}/kdigest.exe
%{_mandir}/man8/kdigest.8*
%{_prefix}/bin/verify_krb5_conf.exe
%{_mandir}/man8/verify_krb5_conf.8*
%{_libexecdir}/digest-service.exe
%doc %{_pkgdocdir}
%license LICENSE

%files server
%if 0%{?_with_systemd}
%{_unitdir}/*.service
%else
%if !0%{?os2_version}
%{_initrddir}/*
%endif
%endif
%if !0%{?os2_version}
%{_sysconfdir}/logrotate.d/heimdal
%endif
%config(noreplace) %{_sysconfdir}/sysconfig/heimdal
%dir %attr(700,root,root) %{_localstatedir}/heimdal
%dir %attr(700,root,root) %{_localstatedir}/log/heimdal
%config(noreplace) %attr(600,root,root) %{_sysconfdir}/heimdal-kdc.conf
%config(noreplace) %{_localstatedir}/heimdal/kdc.conf
%config(noreplace) %attr(600,root,root) %{_sysconfdir}/heimdal-kadmind.acl
%config(noreplace) %{_localstatedir}/heimdal/kadmind.acl
%config(noreplace) %attr(600,root,root) %{_sysconfdir}/heimdal-slaves
%config(noreplace) %{_localstatedir}/heimdal/slaves
%{_libexecdir}/hprop.exe
%{_mandir}/man8/hprop.8*
%{_libexecdir}/hpropd.exe
%{_mandir}/man8/hpropd.8*
%{_mandir}/man8/iprop.8*
%{_sbindir}/iprop-log.exe
%{_mandir}/man8/iprop-log.8*
%{_libexecdir}/ipropd-master.exe
%{_mandir}/man8/ipropd-master.8*
%{_libexecdir}/ipropd-slave.exe
%{_mandir}/man8/ipropd-slave.8*
%if 0%{?_with_systemd}
%{_libexecdir}/ipropd-slave-wrapper.exe
%endif
%{_libexecdir}/kadmind.exe
%{_mandir}/man8/kadmind.8*
%{_libexecdir}/kdc.exe
%{_mandir}/man8/kdc.8*
%{_libexecdir}/kpasswdd.exe
%{_mandir}/man8/kpasswdd.8*
%{_sbindir}/kstash.exe
%{_mandir}/man8/kstash.8*

%files workstation
%{_prefix}/bin/afslog.exe
%{_mandir}/man1/afslog.1*
%{_prefix}/bin/bsearch.exe
%{_mandir}/man1/bsearch.1*
%{_prefix}/bin/pagsh.exe
%{_mandir}/man1/pagsh.1*
%{_prefix}/bin/gsstool.exe
%{_prefix}/bin/heimtools.exe
%{_prefix}/bin/hxtool.exe
%{_prefix}/bin/idn-lookup.exe
%{_prefix}/bin/kdestroy.exe
%{_mandir}/man1/kdestroy.1*
%{_prefix}/bin/kf.exe
%{_mandir}/man1/kf.1*
%{_prefix}/bin/kgetcred.exe
%{_mandir}/man1/kgetcred.1*
%{_libexecdir}/kimpersonate.exe
%{_mandir}/man8/kimpersonate.8*
%{_prefix}/bin/kinit.exe
%{_prefix}/bin/kauth
%{_mandir}/man1/kinit.1*
%{_prefix}/bin/klist
%{_mandir}/man1/klist.1*
%{_prefix}/bin/kpasswd.exe
%{_mandir}/man1/kpasswd.1*
%{_prefix}/bin/kswitch
%{_mandir}/man1/kswitch.1*
%{_prefix}/bin/otp.exe
%{_mandir}/man1/otp.1*
%{_prefix}/bin/otpprint.exe
%{_mandir}/man1/otpprint.1*
%{_bindir}/kadmin.exe
%{_mandir}/man1/kadmin.1*
%{_libexecdir}/kcm.exe
%{_mandir}/man8/kcm.8*
%{_libexecdir}/kfd.exe
%{_mandir}/man8/kfd.8*
%{_bindir}/ktutil.exe
%{_mandir}/man1/ktutil.1*
# NOTICE: no support for X11
#%%{_libexecdir}/kxd
#%%{_mandir}/man8/kxd.8*
#%%{_mandir}/cat8/kxd.8*
%attr(04550,root,root) %{_prefix}/bin/su.exe
%{_mandir}/man1/su.1*

%files devel
%dir %{_libexecdir}/%{name}
%{_bindir}/krb5-config
%{_mandir}/man1/krb5-config.1*
%{_includedir}/*
%{libdir}/*.a
%{_mandir}/man3/*
%{_mandir}/man7/*
%{_libexecdir}/%{name}/asn1_compile.exe
%{_libexecdir}/%{name}/asn1_print.exe
%{_libexecdir}/%{name}/slc.exe

%if !0%{?os2_version}
%files path
%{_sysconfdir}/profile.d/%{name}.sh
%{_sysconfdir}/profile.d/%{name}.csh
%endif
 
%changelog
* Wed Jun 03 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> 7.7.0-1
- update to vendor version 7.7.0
- fix location of key files
- find config files in the right directory
- enable all features we need

* Fri Apr 20 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> 7.5.0-1
- first public build
