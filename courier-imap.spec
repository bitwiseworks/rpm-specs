#
# spec file for package courier-imap (Version 4.8.1)
#
# Copyright (c) 2010 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild


Name:           courier-imap
Summary:        An IMAP and POP3 Server for Maildir MTAs
Version:        4.8.1
Release:        0%{?dist}
License:        GPLv2+
Group:          Productivity/Networking/Email/Servers
Url:            http://www.courier-mta.org/imap/
Source:         %{name}-%{version}.tar.bz2

#Source1:        pop3.pamd
#Source2:        imap.pamd
#Source4:        courier-imap.init
#Source5:        courier-imap-ssl.init
#Source6:        courier-pop.init
#Source7:        courier-pop-ssl.init
#Source8:        %{name}.firewall
#Source9:        %{name}-ssl.firewall

Patch0:         %{name}.diff
#Patch2:         %{name}-ulimit_conf.diff

BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%if 0%{?suse_version} > 910
BuildRequires:  audit-libs
%endif
BuildRequires:  courier-authlib-devel
#BuildRequires: fam-devel gcc-c++ gdbm-devel libstdc++-devel
BuildRequires:  db4-devel
#BuildRequires:  postfix procps
BuildRequires:  ncurses-devel openssl-devel zlib-devel
# openssl itself for /usr/bin/openssl configure check
BuildRequires:  openssl
Conflicts:      imap qpopper cyrus-imapd
Requires:       courier-authlib
#Requires:       fam-server gdbm openssl
Requires:       openssl

%description
Courier-IMAP is a fast, scalable, enterprise IMAP server that uses
Maildirs. Many E-mail service providers use Courier-IMAP to easy handle
hundreds of thousands of mail accounts. With its built-in IMAP and POP3
aggregation proxy, Courier-IMAP has practically infinite horizontal
scalability. In a proxy configuration, a pool of Courier servers service
initial IMAP and POP3 connections from clients. They wait to receive the
client's log in request, look up the server that actually holds this mail
account's mailbox, and establish a proxy connection to the server, all in
a single, seamless process. Mail accounts can be moved between different
servers, to achieve optimum resource usage.

The only practical limitation on Courier-IMAP is available network and I/O
bandwidth. If you are new to Courier-IMAP, this may sound a bit
intimidating. But you do not need to tackle everything at once. Start by
taking small, easy steps. Your first step will be to set up a small
Courier-IMAP server, using it like any other traditional IMAP service, on
a single server. After you gain experience and become comfortable with
Courier, you can then begin exploring its advanced features.

This is the same IMAP server that's included in the Courier mail server,
but configured as a standalone IMAP server that can be used with other
mail servers - such as Qmail, Exim, or Postfix - that deliver to maildirs.
If you already have Courier installed, you do not need to download this
version. If you install this version, you must remove it if you later
install the entire Courier server.


%prep
%setup -q
%patch0 -p1 -b .os2~

%build

export CONFIG_SHELL="/bin/sh"
export LDFLAGS="-Zbin-files -Zhigh-mem -Zomf"
export LIBS="-lurpo"

%configure \
	--libexecdir=%{_prefix}/lib/%{name} \
	--datadir=%{_datadir}/%{name} \
	--sysconfdir=%{_sysconfdir}/%{name} \
	--sharedstatedir=%{_sharedstatedir}/%{name} \
	--with-piddir=%{_localstatedir}/run \
	--disable-static \
	--disable-root-check \
	--enable-unicode \
	--with-authdaemonvar=%{_localstatedir}/run/authdaemon.%{name} \
	--with-certdb=%{_sysconfdir}/ssl/certs \
	--with-certsdir=%{_sysconfdir}/ssl/private \
	--enable-workarounds-for-imap-client-bugs \
        "--cache-file=%{_topdir}/cache/%{name}-%{_target_cpu}.cache"

%{__make} %{?jobs:-j%jobs}

%install
%{__make} install DESTDIR=$RPM_BUILD_ROOT
# Move daemons into sbin
#%{__mv} $RPM_BUILD_ROOT%{_prefix}/bin/couriertls.exe $RPM_BUILD_ROOT%{_prefix}/sbin/
%{__mv} $RPM_BUILD_ROOT%{_prefix}/bin/imapd.exe $RPM_BUILD_ROOT%{_prefix}/sbin/
%{__mv} $RPM_BUILD_ROOT%{_prefix}/bin/pop3d.exe $RPM_BUILD_ROOT%{_prefix}/sbin/
# Rename imapd.8 to courier-imapd.8
%{__mv}  $RPM_BUILD_ROOT%{_mandir}/man8/imapd.8 $RPM_BUILD_ROOT%{_mandir}/man8/%{name}d.8
# Install PAM config files
#%{__install} -D -m 644 $RPM_SOURCE_DIR/pop3.pamd $RPM_BUILD_ROOT/etc/pam.d/pop3
#%{__install} -D -m 644 $RPM_SOURCE_DIR/imap.pamd $RPM_BUILD_ROOT/etc/pam.d/imap
# Install init scripts
#for i in imap imap-ssl pop pop-ssl ; do
#  %{__install} -D -m 0755 $RPM_SOURCE_DIR/courier-$i.init $RPM_BUILD_ROOT/etc/init.d/courier-$i
#  %{__ln_s} -f /etc/init.d/courier-$i $RPM_BUILD_ROOT%{_prefix}/sbin/rccourier-$i
#done
# Remove original init scripts, will not work longer
%{__rm} $RPM_BUILD_ROOT%{_prefix}/lib/%{name}/imapd.rc
%{__rm} $RPM_BUILD_ROOT%{_prefix}/lib/%{name}/imapd-ssl.rc
%{__rm} $RPM_BUILD_ROOT%{_prefix}/lib/%{name}/pop3d.rc
%{__rm} $RPM_BUILD_ROOT%{_prefix}/lib/%{name}/pop3d-ssl.rc
#
# Fix imapd.dist
#
%{__sed} -i -e 's/^IMAPDSTART=.*/IMAPDSTART=YES/' $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/imapd.dist
%{__sed} -i -e 's/^ADDRESS=.*/ADDRESS=127.0.0.1/' $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/imapd.dist
%{__sed} -i -e 's/^MAXPERIP=.*/MAXPERIP=20/' $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/imapd.dist
%{__sed} -i -e 's/^IMAPDSSLSTART=.*/IMAPDSSLSTART=YES/' $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/imapd-ssl.dist
%{__sed} -i -e 's/^#\ \+\(TLS_CIPHER_LIST=.*\)/\1/' $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/imapd-ssl.dist
%{__sed} -i -e 's/^POP3DSTART=.*/POP3DSTART=YES/' $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/pop3d.dist
%{__sed} -i -e 's/^POP3DSSLSTART=.*/POP3DSSLSTART=YES/' $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/pop3d-ssl.dist
%{__sed} -i -e 's/^#\ \+\(TLS_CIPHER_LIST=.*\)/\1/' $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/pop3d-ssl.dist
# For %doc macro
%{__install} -m 0644 imap/ChangeLog ChangeLog
%{__install} -m 0644 imap/README README.imap
%{__install} -m 0644 imap/README.proxy README.proxy
%{__install} -m 0644 maildir/README.maildirquota.txt README.maildirquota
%{__install} -m 0644 maildir/README.sharedfolders.txt README.sharedfolders
%{__install} -D -m 0755 sysconftool $RPM_BUILD_ROOT%{_datadir}/%{name}/sysconftool
%{__chmod} 755 $RPM_BUILD_ROOT%{_datadir}/%{name}/sysconftool
%{__cat} >$RPM_BUILD_ROOT%{_datadir}/%{name}/configlist <<EOF
%{_sysconfdir}/courier/imapd.dist
%{_sysconfdir}/courier/imapd-ssl.dist
%{_sysconfdir}/courier/pop3d.dist
%{_sysconfdir}/courier/pop3d-ssl.dist
EOF
#firewall script
#%{__install} -D -m 644 %{S:8} $RPM_BUILD_ROOT%{_sysconfdir}/SuSEfirewall2.d/services/%{name}
#%{__install} -D -m 644 %{S:9} $RPM_BUILD_ROOT%{_sysconfdir}/SuSEfirewall2.d/services/%{name}-ssl

#%preun
#for i in imap imap-ssl pop pop-ssl ; do  
#  %stop_on_removal courier-$i
#done
#if [ "$1" = "0" ]; then
#  %{__rm} -f %{_localstatedir}/couriersslcache
#  %{__rm} -f %{_localstatedir}/imapd.pid
#  %{__rm} -f %{_localstatedir}/imapd-ssl.pid
#  %{__rm} -f %{_localstatedir}/imapd.pid.lock
#  %{__rm} -f %{_localstatedir}/imapd-ssl.pid.lock
#  %{__rm} -f %{_localstatedir}/pop3d.pid
#  %{__rm} -f %{_localstatedir}/pop3d-ssl.pid
#  %{__rm} -f %{_localstatedir}/pop3d.pid.lock
#  %{__rm} -f %{_localstatedir}/pop3d-ssl.pid.lock
#fi

#%post
#%{_datadir}/%{name}/sysconftool `%{__cat} %{_datadir}/%{name}/configlist` >/dev/null

#%postun
#for i in imap imap-ssl pop pop-ssl ; do
#  %restart_on_update courier-$i
#done  
#%insserv_cleanup

%post
%wps_object_create_begin
COURIER_IMAPD:WPProgram|Courier Imap daemon|<COURIER_FOLDER>|EXENAME=((%{_prefix}/lib/%{name}/imapd.cmd));STARTUPDIR=((%{_prefix}/lib/%{name}));PARAMETERS=;TITLE=Courier Imap daemon;
COURIER_POP3D:WPProgram|Courier Pop3 daemon|<COURIER_FOLDER>|EXENAME=((%{_prefix}/lib/%{name}/imapd.cmd));STARTUPDIR=((%{_prefix}/lib/%{name}));PARAMETERS=;TITLE=Courier Pop3 daemon;
%wps_object_create_end

%postun
%wps_object_delete_all


%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,755)
%doc AUTHORS ChangeLog COPYING* imap/BUGS README README.imap README.maildirquota README.proxy
%doc README.sharedfolders
#%attr(755,root,root) /etc/init.d/courier-*
#%config %attr(644,root,root) /etc/pam.d/imap
#%config %attr(644,root,root) /etc/pam.d/pop3
%dir %{_sysconfdir}/%{name}
%config %attr(600,root,root) %{_sysconfdir}/%{name}/imap*
%config %attr(600,root,root) %{_sysconfdir}/%{name}/pop3*
%config %{_sysconfdir}/%{name}/quotawarnmsg.example
%dir %{_prefix}/lib/%{name}
%{_prefix}/lib/%{name}/makedatprog.exe
%{_prefix}/lib/%{name}/couriertcpd.exe
%{_bindir}/*
%{_sbindir}/*
%{_mandir}/man?/*
%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/*
#%dir %{_sysconfdir}/SuSEfirewall2.d
#%dir %{_sysconfdir}/SuSEfirewall2.d/services
#%config %{_sysconfdir}/SuSEfirewall2.d/services/%{name}
#%config %{_sysconfdir}/SuSEfirewall2.d/services/%{name}-ssl

%changelog
