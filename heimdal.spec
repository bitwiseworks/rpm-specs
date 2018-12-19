
Name: heimdal
Version: 7.5.0
Release: 1%{?dist}
Summary: A Kerberos 5 implementation without export restrictions
License: BSD and MIT
URL: http://www.h5l.org/
Group: System Environment/Libraries
Vendor: bww bitwise works GmbH
%scm_source  github https://github.com/bitwiseworks/heimdal-os2 master-os2

BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  readline-devel
BuildRequires:  libtool
BuildRequires:  ncurses-devel
#BuildRequires:  openldap-devel
#Required for tests/ldap
#BuildRequires:  openldap-servers
#BuildRequires:  pam-devel
BuildRequires:  perl(JSON)
BuildRequires:  sqlite-devel
BuildRequires:  texinfo
BuildRequires:  db4-devel
BuildRequires:  python2


# Bundled libtommath (https://bugzilla.redhat.com/1118462)
Provides: bundled(libtommath) = 0.42.0

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
Group:      System Environment/Base

%description workstation
This package contains Heimdal Kerberos 5 programs and utilities for
use on workstations (kinit, klist, kdestroy, kpasswd)


%package server
Summary:  Heimdal kerberos server
Group:    System Environment/Daemons
#Requires: logrotate
Provides: heimdal-kdc = %{version}-%{release}
Obsoletes: heimdal-kdc < 1.5

%description server
This package contains the master Heimdal kerberos Key Distribution
Center (KDC), admin interface server (admind) and master-slave
synchronisation daemons. Install this package if you intend to
set up Kerberos server.


%package libs
Summary: Heimdal kerberos shared libraries
Group:   System Environment/Libraries
Requires(post): info
Requires(preun): info

%description libs
This package contains shared libraries required by several of the other
Heimdal packages.


%package devel
Summary:  Header and other development files for Heimdal kerberos
Group:    System Environment/Libraries
Provides: %{name}-static = %{version}-%{release}

%description devel
Contains files needed to compile and link software using the Heimdal
kerberos headers/libraries.


%debug_package


%prep
%scm_setup
autoreconf -fvi


%build
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx -ltinfo"
export VENDOR="%{vendor}"

%ifarch i386
%global build_fix "-march=i686"
%else
%global build_fix ""
%endif
%configure \
        --prefix=%{_prefix} \
        --includedir=%{_includedir}/%{name} \
        --enable-shared \
        --enable-pthread-support \
        --enable-kcm \
        --enable-pk-init \
        --with-sqlite3=%{_prefix} \
        --with-readline=%{_prefix} \
        --with-libintl=/@unixroot/usr \
        CFLAGS="%{optflags} %{build_fix}"

export BEGINLIBPATH=%{_builddir}/%{buildsubdir}/lib/roken/.libs
make %{?_smp_mflags}
make %{?_smp_mflags} -C doc html


%check
# Several intermittent test failures here, so make this non-fatal:
#make check || :


%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
mkdir -p %{buildroot}%{_localstatedir}/heimdal/
mkdir -p %{buildroot}%{_sysconfdir}
echo "# see man heimdal-kadmind(8)" > %{buildroot}%{_sysconfdir}/heimdal-kadmind.acl
ln -s %{_sysconfdir}/heimdal-kadmind.acl %{buildroot}%{_localstatedir}/heimdal/kadmind.acl
touch    %{buildroot}%{_sysconfdir}/heimdal-slaves
ln -s %{_sysconfdir}/heimdal-slaves %{buildroot}%{_localstatedir}/heimdal/slaves
install -d -m 700 %{buildroot}%{_localstatedir}/log/heimdal
install -d -m 755 %{buildroot}/%{_pkgdocdir}
install -p -D -m 644 LICENSE    %{buildroot}/%{_pkgdocdir}/LICENSE
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

ln -s %{_bindir}/kinit.exe %{buildroot}%{_bindir}/kauth

rm %{buildroot}%{_mandir}/man5/qop.5
ln -s mech.5.gz %{buildroot}%{_mandir}/man5/qop.5.gz

if find %{buildroot} -name '*.mo' | grep .; then
   %find_lang %{name} --all-name
else
   touch %{name}.lang
fi


%post server


%preun server


%postun server


%post libs
#  %{_sbindir}/ldconfig
  %{_sbindir}/install-info %{_infodir}/%{name}.info %{_infodir}/dir || :


%preun libs
if [ $1 = 0 ] ; then
    %{_sbindir}/install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir || :
fi


%postun libs
#  %{_sbindir}/ldconfig


%files libs -f %{name}.lang
%{_libdir}/*.dll
%{_infodir}/heimdal.info*
%{_infodir}/hx509.info*
%{_mandir}/man5/krb5.conf.5*
%{_mandir}/man5/qop.5*
%{_mandir}/man5/mech.5*
%{_mandir}/man8/kerberos.8*
%{_bindir}/string2key.exe
%{_mandir}/man8/string2key.8*
%{_libexecdir}/kdigest.exe
%{_mandir}/man8/kdigest.8*
%{_bindir}/verify_krb5_conf.exe
%{_mandir}/man8/verify_krb5_conf.8*
%{_libexecdir}/digest-service.exe
%doc %{_pkgdocdir}


%files server
%dir %attr(700,root,root) %{_localstatedir}/heimdal
%dir %attr(700,root,root) %{_localstatedir}/log/heimdal
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
%{_libexecdir}/kadmind.exe
%{_mandir}/man8/kadmind.8*
%{_libexecdir}/kdc.exe
%{_mandir}/man8/kdc.8*
%{_libexecdir}/kpasswdd.exe
%{_mandir}/man8/kpasswdd.8*
%{_sbindir}/kstash.exe
%{_mandir}/man8/kstash.8*


%files workstation
%{_bindir}/afslog.exe
%{_mandir}/man1/afslog.1*
%{_bindir}/bsearch.exe
%{_mandir}/man1/bsearch.1*
%{_bindir}/pagsh.exe
%{_mandir}/man1/pagsh.1*
%{_bindir}/gsstool.exe
%{_bindir}/heimtools.exe
%{_bindir}/hxtool.exe
%{_bindir}/idn-lookup.exe
%{_bindir}/kdestroy.exe
%{_mandir}/man1/kdestroy.1*
%{_bindir}/kf.exe
%{_mandir}/man1/kf.1*
%{_bindir}/kgetcred.exe
%{_mandir}/man1/kgetcred.1*
%{_libexecdir}/kimpersonate.exe
%{_mandir}/man8/kimpersonate.8*
%{_bindir}/kinit.exe
%{_bindir}/kauth
%{_mandir}/man1/kinit.1*
%{_bindir}/klist
%{_mandir}/man1/klist.1*
%{_bindir}/kpasswd.exe
%{_mandir}/man1/kpasswd.1*
%{_bindir}/kswitch
%{_mandir}/man1/kswitch.1*
%{_bindir}/otp.exe
%{_mandir}/man1/otp.1*
%{_bindir}/otpprint.exe
%{_mandir}/man1/otpprint.1*
%{_bindir}/kadmin.exe
%{_mandir}/man1/kadmin.1*
%{_libexecdir}/kcm.exe
%{_mandir}/man8/kcm.8*
%{_libexecdir}/kfd.exe
%{_mandir}/man8/kfd.8*
%{_bindir}/ktutil.exe
%{_mandir}/man1/ktutil.1*
%attr(04550,root,root) %{_bindir}/su.exe
%{_mandir}/man1/su.1*


%files devel
%dir %{_libexecdir}/%{name}
%{_bindir}/krb5-config
%{_mandir}/man1/krb5-config.1*
%{_includedir}/*
%{_libdir}/*.a
%{_mandir}/man3/*
%{_mandir}/man7/*
%{_libexecdir}/%{name}/asn1_compile.exe
%{_libexecdir}/%{name}/asn1_print.exe
%{_libexecdir}/%{name}/slc.exe
%{_libdir}/pkgconfig/*.pc


%changelog
* Fri Apr 20 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> 7.5.0-1
- first public build
