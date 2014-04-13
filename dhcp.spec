# Where dhcp configuration files are stored
%global dhcpconfdir %{_sysconfdir}/dhcp

# Base version number from ISC
%global basever 3.1
%global basedir %{basever}-ESV-R3

# LDAP patch version
%global ldappatchver %{basever}-2

Summary:  Dynamic host configuration protocol software
Name:     dhcp
Version:  %{basever}
Release:  3%{?dist}
License:  ISC
Group:    System Environment/Daemons
URL:      http://isc.org/products/DHCP/

Source0:  ftp://ftp.isc.org/isc/%{name}/%{name}-%{basedir}.tar.gz
Source1:  dhcp-os2.h
Source2:  dhconf.cmd

Patch0:   dhcp-os2.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
#BuildRequires: autoconf
#BuildRequires: automake
#BuildRequires: groff
#BuildRequires: libtool
#BuildRequires: openldap-devel
#BuildRequires: libcap-ng-devel

#Obsoletes: dhcpv6 <= 1.2.0-4

%description
DHCP (Dynamic Host Configuration Protocol) is a protocol which allows
individual devices on an IP network to get their own network
configuration information (IP address, subnetmask, broadcast address,
etc.) from a DHCP server. The overall purpose of DHCP is to make it
easier to administer a large network.  The dhcp package includes the
ISC DHCP service and relay agent.

To use DHCP on your network, install a DHCP service (or relay agent),
and on clients run a DHCP client daemon.  The dhcp package provides
the ISC DHCP service and relay agent.

%package -n dhclient
Summary: Provides the dhclient ISC DHCP client daemon and dhclient-script
Group: System Environment/Base
#Requires: initscripts >= 6.75
#Requires(post): coreutils
#Requires(post): grep

%description -n dhclient
DHCP (Dynamic Host Configuration Protocol) is a protocol which allows
individual devices on an IP network to get their own network
configuration information (IP address, subnetmask, broadcast address,
etc.) from a DHCP server. The overall purpose of DHCP is to make it
easier to administer a large network.

To use DHCP on your network, install a DHCP service (or relay agent),
and on clients run a DHCP client daemon.  The dhclient package
provides the ISC DHCP client daemon.

%package devel
Summary: Development headers and libraries for interfacing to the DHCP server
Group: Development/Libraries
Requires: %{name} = %{epoch}:%{version}-%{release}

%description devel
Header files and API documentation for using the ISC DHCP libraries.  The
libdhcpctl and libomapi static libraries are also included in this package.

%package debug
Summary: HLL debug data for exception handling support.

%description debug
HLL debug data for exception handling support.

%prep
%setup -q -n %{name}-%{basedir}
cp %{SOURCE1} includes/cf/os2.h

# Add in LDAP support
#%{__patch} -p1 < ldap-for-dhcp-%{ldappatchver}/%{name}-%{basever}-ldap.patch

%patch0 -p1 -b .os2~

# Update paths in all man pages
for page in client/dhclient.conf.5 client/dhclient.leases.5 \
            client/dhclient-script.8 client/dhclient.8 ; do
    %{__sed} -i -e 's|CLIENTBINDIR|/sbin|g' \
                -e 's|RUNDIR|%{_localstatedir}/run|g' \
                -e 's|DBDIR|%{_localstatedir}/lib/dhclient|g' \
                -e 's|ETCDIR|%{dhcpconfdir}|g' $page
done

for page in server/dhcpd.conf.5 server/dhcpd.leases.5 server/dhcpd.8 ; do
    %{__sed} -i -e 's|CLIENTBINDIR|/sbin|g' \
                -e 's|RUNDIR|%{_localstatedir}/run|g' \
                -e 's|DBDIR|%{_localstatedir}/lib/dhcpd|g' \
                -e 's|ETCDIR|%{dhcpconfdir}|g' $page
done

#aclocal
#libtoolize --copy --force
#autoconf
#autoheader
#automake --foreign --add-missing --copy

%build
export CONFIG_SHELL="/@unixroot/usr/bin/sh.exe"
export LDFLAGS="-Zomf"
CFLAGS="%{optflags} -D_GNU_SOURCE" \
./configure
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}

# Remove files we don't want
%{__rm} -f %{buildroot}%{_sysconfdir}/dhclient.conf
%{__rm} -f %{buildroot}%{_sysconfdir}/dhcpd.conf

# Install correct dhclient-script
#%{__mkdir} -p %{buildroot}/sbin
#%{__mv} %{buildroot}%{_sbindir}/dhclient %{buildroot}/sbin/dhclient
#%{__install} -p -m 0755 client/scripts/linux %{buildroot}/sbin/dhclient-script
%{__install} -p -m 0755 %{SOURCE2} %{buildroot}%{_sbindir}/dhconf.cmd

# Install init scripts
#%{__mkdir} -p %{buildroot}%{_initrddir}
#%{__install} -p -m 0755 %{SOURCE2} %{buildroot}%{_initrddir}/dhcpd
#%{__install} -p -m 0755 %{SOURCE8} %{buildroot}%{_initrddir}/dhcpd6
#%{__install} -p -m 0755 %{SOURCE3} %{buildroot}%{_initrddir}/dhcrelay

# Start empty lease databases
%{__mkdir} -p %{buildroot}%{_localstatedir}/lib/
touch %{buildroot}%{_localstatedir}/lib/dhcpd.leases
#touch %{buildroot}%{_localstatedir}/lib/dhcpd/dhcpd6.leases
%{__mkdir} -p %{buildroot}%{_localstatedir}/lib/

# Create default sysconfig files for dhcpd and dhcrelay
%{__mkdir} -p %{buildroot}%{_sysconfdir}/sysconfig

%{__cat} << EOF > %{buildroot}%{_sysconfdir}/sysconfig/dhcrelay
# Command line options here
INTERFACES=""
DHCPSERVERS=""
EOF

%{__cat} <<EOF > %{buildroot}%{_sysconfdir}/sysconfig/dhcpd
# Command line options here
DHCPDARGS=
EOF

#%{__cat} <<EOF > %{buildroot}%{_sysconfdir}/sysconfig/dhcpd6
# Command line options here
#DHCPDARGS=
#EOF

# Copy sample conf files into position (called by doc macro)
%{__cp} -p client/dhclient.conf dhclient.conf.sample
%{__cp} -p server/dhcpd.conf dhcpd.conf.sample
#%{__cp} -p doc/examples/dhclient-dhcpv6.conf dhclient6.conf.sample
#%{__cp} -p doc/examples/dhcpd-dhcpv6.conf dhcpd6.conf.sample

# Install default (empty) dhcpd.conf:
%{__mkdir} -p %{buildroot}%{dhcpconfdir}
%{__cat} << EOF > %{buildroot}%{dhcpconfdir}/dhcpd.conf
#
# DHCP Server Configuration file.
#   see /usr/share/doc/dhcp*/dhcpd.conf.sample
#   see 'man 5 dhcpd.conf'
#
EOF

# Install default (empty) dhcpd6.conf:
#%{__cat} << EOF > %{buildroot}%{dhcpconfdir}/dhcpd6.conf
#
# DHCP for IPv6 Server Configuration file.
#   see /usr/share/doc/dhcp*/dhcpd6.conf.sample
#   see 'man 5 dhcpd.conf'
#   run 'service dhcpd6 start' or 'dhcpd -6 -cf /etc/dhcp/dhcpd6.conf'
#
#EOF

# Install dhcp.schema for LDAP configuration
#%{__mkdir} -p %{buildroot}%{_sysconfdir}/openldap/schema
#%{__install} -p -m 0644 -D ldap-for-dhcp-%{ldappatchver}/dhcp.schema \
#    %{buildroot}%{_sysconfdir}/openldap/schema

# Install empty directory for dhclient.d scripts
#%{__mkdir} -p %{buildroot}%{dhcpconfdir}/dhclient.d

# Install NetworkManager dispatcher script
#%{__mkdir} -p %{buildroot}%{_sysconfdir}/NetworkManager/dispatcher.d
#%{__install} -p -m 0755 %{SOURCE6} %{buildroot}%{_sysconfdir}/NetworkManager/dispatcher.d

# Install pm-utils script to handle suspend/resume and dhclient leases
#%{__mkdir} -p %{buildroot}%{_libdir}/pm-utils/sleep.d
#%{__install} -p -m 0755 %{SOURCE7} %{buildroot}%{_libdir}/pm-utils/sleep.d

%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc LICENSE README 
#ldap-for-dhcp-%{ldappatchver}/README.ldap
%doc RELNOTES dhcpd.conf.sample doc/IANA-arp-parameters doc/api+protocol
#  dhcpd6.conf.sample
%doc doc/*.txt
# __fedora_contrib/* 
#ldap-for-dhcp-%{ldappatchver}/*.txt
%dir %{_localstatedir}/lib
%attr(0750,root,root) %dir %{dhcpconfdir}
%verify(not size md5 mtime) %config(noreplace) %{_localstatedir}/lib/dhcpd.leases
#%verify(not size md5 mtime) %config(noreplace) %{_localstatedir}/lib/dhcpd/dhcpd6.leases
%config(noreplace) %{_sysconfdir}/sysconfig/dhcpd
#%config(noreplace) %{_sysconfdir}/sysconfig/dhcpd6
%config(noreplace) %{_sysconfdir}/sysconfig/dhcrelay
%config(noreplace) %{dhcpconfdir}/dhcpd.conf
#%config(noreplace) %{dhcpconfdir}/dhcpd6.conf
#%config(noreplace) %{_sysconfdir}/openldap/schema/dhcp.schema
#%dir %{_sysconfdir}/NetworkManager
#%dir %{_sysconfdir}/NetworkManager/dispatcher.d
#%{_sysconfdir}/NetworkManager/dispatcher.d/10-dhclient
#%{_initrddir}/dhcpd
#%{_initrddir}/dhcpd6
#%{_initrddir}/dhcrelay
%{_bindir}/omshell.exe
%{_sbindir}/dhcpd.exe
%{_sbindir}/dhcrelay.exe
%attr(0644,root,root) %{_mandir}/man1/omshell.1
%attr(0644,root,root) %{_mandir}/man5/dhcpd.conf.5
%attr(0644,root,root) %{_mandir}/man5/dhcpd.leases.5
%attr(0644,root,root) %{_mandir}/man8/dhcpd.8
%attr(0644,root,root) %{_mandir}/man8/dhcrelay.8
%attr(0644,root,root) %{_mandir}/man5/dhcp-options.5
%attr(0644,root,root) %{_mandir}/man5/dhcp-eval.5

%files -n dhclient
%defattr(-,root,root,-)
%doc dhclient.conf.sample
# README.dhclient.d
# dhclient6.conf.sample
%attr(0750,root,root) %dir %{dhcpconfdir}
#%dir %{dhcpconfdir}/dhclient.d
%dir %{_localstatedir}/lib
%{_sbindir}/dhclient.exe
%{_sbindir}/dhconf.cmd
#%attr(0755,root,root) %{_libdir}/pm-utils/sleep.d/56dhclient
%attr(0644,root,root) %{_mandir}/man5/dhclient.conf.5
%attr(0644,root,root) %{_mandir}/man5/dhclient.leases.5
%attr(0644,root,root) %{_mandir}/man8/dhclient.8
%attr(0644,root,root) %{_mandir}/man8/dhclient-script.8
%attr(0644,root,root) %{_mandir}/man5/dhcp-options.5
%attr(0644,root,root) %{_mandir}/man5/dhcp-eval.5

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*.a
%attr(0644,root,root) %{_mandir}/man3/dhcpctl.3
%attr(0644,root,root) %{_mandir}/man3/omapi.3

%files debug
%defattr(-,root,root)
%{_bindir}/*.dbg
%{_sbindir}/*.dbg

%changelog
* Sun Apr 13 2014 yd
- r711, Add support for DHCLIENT_BEEP and DHCLIENT_LOGFILE env variables, by Andreas Buchinger.

* Mon Jan 30 2012 yd
- added dhconf.cmd.
- use spawn instead of fork().

* Tue Jan 24 2012 yd
- initial unixroot build.
