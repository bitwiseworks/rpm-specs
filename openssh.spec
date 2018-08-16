# !!!! we need a way to deal with the sshd user. right now it needs to be added
# !!!! manually with klusrmgr


# Note: this .spec is borrowed from:
# https://src.fedoraproject.org/cgit/rpms/openssh.git/tree/openssh.spec

# Do we want SELinux & Audit
%global WITH_SELINUX 0

%global _hardened_build 1

# OpenSSH privilege separation requires a user & group ID
%global sshd_uid    74
%global sshd_gid    74

# Do we want to disable building of gnome-askpass? (1=yes 0=no)
%global no_gnome_askpass 1

# Do we want to link against a static libcrypto? (1=yes 0=no)
%global static_libcrypto 0

# Use GTK2 instead of GNOME in gnome-ssh-askpass
%global gtk2 0

# Build position-independent executables (requires toolchain support)?
%global pie 0

# Do we want kerberos5 support (1=yes 0=no)
%global kerberos5 0

# Do we want libedit support
%global libedit 0

# Do we want LDAP support
%global ldap 0

# Whether to build pam_ssh_agent_auth
%global pam_ssh_agent 0

# Reserve options to override askpass settings with:
# rpm -ba|--rebuild --define 'skip_xxx 1'
%{?skip_gnome_askpass:%global no_gnome_askpass 1}

# Add option to build without GTK2 for older platforms with only GTK+.
# Red Hat Linux <= 7.2 and Red Hat Advanced Server 2.1 are examples.
# rpm -ba|--rebuild --define 'no_gtk2 1'
%{?no_gtk2:%global gtk2 0}

# Options for static OpenSSL link:
# rpm -ba|--rebuild --define "static_openssl 1"
%{?static_openssl:%global static_libcrypto 1}

# Is this a build for the rescue CD (without PAM, with MD5)? (1=yes 0=no)
%define rescue 0
%{?build_rescue:%global rescue 1}
%{?build_rescue:%global rescue_rel rescue}

# Turn off some stuff for resuce builds
%if %{rescue}
%global kerberos5 0
%global libedit 0
%global pam_ssh_agent 0
%endif

# Do we want keycat package enabled
%global keycat 0

# Do we want cavs package enabled
%global cavs 0

# Do not forget to bump pam_ssh_agent_auth release if you rewind the main package release to 1
%global openssh_ver 7.7p1
%global openssh_rel 2
%global pam_ssh_agent_ver 0.10.3
%global pam_ssh_agent_rel 4

Summary: An open source implementation of SSH protocol versions 2
Name: openssh
Version: %{openssh_ver}
Release: %{openssh_rel}%{?dist}%{?rescue_rel}
URL: http://www.openssh.com/portable.html
Vendor: bww bitwise works GmbH

#scm_source github http://github.com/bitwiseworks/%{name}-os2 master-os2
%scm_source git e:/Trees/%{name}/git master-os2

License: BSD
Group: Applications/Internet
#Requires: /sbin/nologin

#Requires: initscripts >= 5.20

%if ! %{no_gnome_askpass}
%if %{gtk2}
BuildRequires: gtk2-devel
BuildRequires: libX11-devel
%else
BuildRequires: gnome-libs-devel
%endif
%endif

%if %{ldap}
BuildRequires: openldap-devel
%endif
BuildRequires: autoconf, automake, perl-generators, zlib-devel
#BuildRequires: perl-interpretor
#BuildRequires: audit-libs-devel >= 2.0.5
#BuildRequires: util-linux, groff
#BuildRequires: pam-devel
#BuildRequires: fipscheck-devel >= 1.3.0
BuildRequires: openssl-devel >= 0.9.8j
#BuildRequires: perl-podlators
#BuildRequires: systemd-devel
BuildRequires: gcc
#BuildRequires: p11-kit-devel
#Recommends: p11-kit

%if %{kerberos5}
BuildRequires: krb5-devel
%endif

%if %{libedit}
BuildRequires: libedit-devel ncurses-devel
%endif

%if %{WITH_SELINUX}
Requires: libselinux >= 2.3-5
BuildRequires: libselinux-devel >= 2.3-5
Requires: audit-libs >= 1.0.8
BuildRequires: audit-libs >= 1.0.8
%endif

#BuildRequires: xauth
# for tarball signature verification
#BuildRequires: gnupg2

%package clients
Summary: An open source SSH client applications
Requires: openssh = %{version}-%{release}
Group: Applications/Internet
#Requires: fipscheck-lib%{_isa} >= 1.3.0
#Requires: crypto-policies >= 20180306-1

%package server
Summary: An open source SSH server daemon
Group: System Environment/Daemons
Requires: openssh = %{version}-%{release}
Requires: klusrmgr >= 1.2.0
#Requires: pam >= 1.0.1-3
#Requires: fipscheck-lib%{_isa} >= 1.3.0
#Requires: crypto-policies >= 20180306-1
#%{?systemd_requires}

%if %{ldap}
%package ldap
Summary: A LDAP support for open source SSH server daemon
Requires: openssh = %{version}-%{release}
Group: System Environment/Daemons
%endif

%if %{keycat}
%package keycat
Summary: A mls keycat backend for openssh
Requires: openssh = %{version}-%{release}
Group: System Environment/Daemons
%endif

%package askpass
Summary: A passphrase dialog for OpenSSH and X
Group: Applications/Internet
Requires: openssh = %{version}-%{release}
Obsoletes: openssh-askpass-gnome
Provides: openssh-askpass-gnome

%if %{cavs}
%package cavs
Summary: CAVS tests for FIPS validation
Group: Applications/Internet
Requires: openssh = %{version}-%{release}
%endif

%if %{pam_ssh_agent}
%package -n pam_ssh_agent_auth
Summary: PAM module for authentication with ssh-agent
Group: System Environment/Base
Version: %{pam_ssh_agent_ver}
Release: %{pam_ssh_agent_rel}.%{openssh_rel}%{?dist}%{?rescue_rel}
License: BSD
%endif

%description
SSH (Secure SHell) is a program for logging into and executing
commands on a remote machine. SSH is intended to replace rlogin and
rsh, and to provide secure encrypted communications between two
untrusted hosts over an insecure network. X11 connections and
arbitrary TCP/IP ports can also be forwarded over the secure channel.

OpenSSH is OpenBSD's version of the last free version of SSH, bringing
it up to date in terms of security and features.

This package includes the core files necessary for both the OpenSSH
client and server. To make this package useful, you should also
install openssh-clients, openssh-server, or both.

%description clients
OpenSSH is a free version of SSH (Secure SHell), a program for logging
into and executing commands on a remote machine. This package includes
the clients necessary to make encrypted connections to SSH servers.

%description server
OpenSSH is a free version of SSH (Secure SHell), a program for logging
into and executing commands on a remote machine. This package contains
the secure shell daemon (sshd). The sshd daemon allows SSH clients to
securely connect to your SSH server.

%if %{ldap}
%description ldap
OpenSSH LDAP backend is a way how to distribute the authorized tokens
among the servers in the network.
%endif

%if %{keycat}
%description keycat
OpenSSH mls keycat is backend for using the authorized keys in the
openssh in the mls mode.
%endif

%description askpass
OpenSSH is a free version of SSH (Secure SHell), a program for logging
into and executing commands on a remote machine. This package contains
an X11 passphrase dialog for OpenSSH.

%if %{cavs}
%description cavs
This package contains test binaries and scripts to make FIPS validation
easier. Now contains CTR and KDF CAVS test driver.
%endif

%if %{pam_ssh_agent}
%description -n pam_ssh_agent_auth
This package contains a PAM module which can be used to authenticate
users using ssh keys stored in a ssh-agent. Through the use of the
forwarding of ssh-agent connection it also allows to authenticate with
remote ssh-agent instance.

The module is most useful for su and sudo service stacks.
%endif

%debug_package

%prep
%scm_setup

autoreconf -fvi

%build
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"

%if %{rescue}
CFLAGS="$CFLAGS -Os"
%endif
%if %{pie}
%ifarch s390 s390x sparc sparcv9 sparc64
CFLAGS="$CFLAGS -fPIC"
%else
CFLAGS="$CFLAGS -fpic"
%endif
SAVE_LDFLAGS="$LDFLAGS"
LDFLAGS="$LDFLAGS -pie -z relro -z now"

export CFLAGS
export LDFLAGS

%endif
%if %{kerberos5}
if test -r /@unixroot/etc/profile.d/krb5-devel.sh ; then
	source /@unixroot/etc/profile.d/krb5-devel.sh
fi
krb5_prefix=`krb5-config --prefix`
if test "$krb5_prefix" != "%{_prefix}" ; then
	CPPFLAGS="$CPPFLAGS -I${krb5_prefix}/include -I${krb5_prefix}/include/gssapi"; export CPPFLAGS
	CFLAGS="$CFLAGS -I${krb5_prefix}/include -I${krb5_prefix}/include/gssapi"
	LDFLAGS="$LDFLAGS -L${krb5_prefix}/%{_lib}"; export LDFLAGS
else
	krb5_prefix=
	CPPFLAGS="-I%{_includedir}/gssapi"; export CPPFLAGS
	CFLAGS="$CFLAGS -I%{_includedir}/gssapi"
fi
%endif

# not used configure switches 
#	--with-systemd \
#	--with-default-pkcs11-provider=yes \

%configure \
	--sysconfdir=%{_sysconfdir}/ssh \
	--libexecdir=%{_libexecdir}/openssh \
	--datadir=%{_datadir}/openssh \
	--with-pid-dir=%{_var}/run \
	--with-default-path=/@unixroot/usr/local/bin:/@unixroot/bin:/@unixroot/usr/bin \
	--with-superuser-path=/@unixroot/usr/local/sbin:/@unixroot/usr/local/bin:/@unixroot/sbin:/@unixroot/bin:/@unixroot/usr/sbin:/@unixroot/usr/bin \
	--with-privsep-path=%{_var}/empty/sshd \
	--disable-strip \
	--without-zlib-version-check \
	--with-ssl-engine \
	--with-ipaddr-display \
	--with-pie=no \
	--disable-utmp \
	--disable-utmpx \
	--disable-wtmp \
	--disable-wtmpx \
	--with-mantype=man \
%if %{ldap}
	--with-ldap \
%endif
%if %{rescue}
	--without-pam \
%else
	--without-pam \
%endif
%if %{WITH_SELINUX}
	--with-selinux --with-linux-audit \
	--with-sandbox=seccomp_filter \
%endif
%if %{kerberos5}
	--with-kerberos5${krb5_prefix:+=${krb5_prefix}} \
%else
	--without-kerberos5 \
%endif
%if %{libedit}
	--with-libedit
%else
	--without-libedit
%endif

%if %{static_libcrypto}
perl -pi -e "s|-lcrypto|%{_libdir}/libcrypto.a|g" Makefile
%endif

make

# Define a variable to toggle gnome1/gtk2 building.  This is necessary
# because RPM doesn't handle nested %if statements.
%if %{gtk2}
	gtk2=yes
%else
	gtk2=no
%endif

%if ! %{no_gnome_askpass}
pushd contrib
if [ $gtk2 = yes ] ; then
	CFLAGS="$CFLAGS %{?__global_ldflags}" \
	    make gnome-ssh-askpass2
	mv gnome-ssh-askpass2 gnome-ssh-askpass
else
	CFLAGS="$CFLAGS %{?__global_ldflags}"
	    make gnome-ssh-askpass1
	mv gnome-ssh-askpass1 gnome-ssh-askpass
fi
popd
%endif

# Add generation of HMAC checksums of the final stripped binaries
#%global __spec_install_post \
#    %{?__debug_package:%{__debug_install_post}} \
#    %{__arch_install_post} \
#    %{__os_install_post} \
#    fipshmac -d $RPM_BUILD_ROOT%{_libdir}/fipscheck $RPM_BUILD_ROOT%{_bindir}/ssh $RPM_BUILD_ROOT%{_sbindir}/sshd \
#%{nil}

%check
#to run tests use "--with check"
%if %{?_with_check:1}%{!?_with_check:0}
make tests
%endif

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p -m755 $RPM_BUILD_ROOT%{_sysconfdir}/ssh
mkdir -p -m755 $RPM_BUILD_ROOT%{_sysconfdir}/ssh/ssh_config.d
mkdir -p -m755 $RPM_BUILD_ROOT%{_libexecdir}/openssh
mkdir -p -m755 $RPM_BUILD_ROOT%{_var}/empty/sshd
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/ssh/ldap.conf

install -d $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/
install -d $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
install -d $RPM_BUILD_ROOT%{_libexecdir}/openssh
install -m755 contrib/ssh-copy-id $RPM_BUILD_ROOT%{_bindir}/
install contrib/ssh-copy-id.1 $RPM_BUILD_ROOT%{_mandir}/man1/

%if ! %{no_gnome_askpass}
install contrib/gnome-ssh-askpass $RPM_BUILD_ROOT%{_libexecdir}/openssh/gnome-ssh-askpass
%endif

%if ! %{no_gnome_askpass}
ln -s gnome-ssh-askpass $RPM_BUILD_ROOT%{_libexecdir}/openssh/ssh-askpass
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/
install -m 755 contrib/redhat/gnome-ssh-askpass.csh $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/
install -m 755 contrib/redhat/gnome-ssh-askpass.sh $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/
%endif

%if %{no_gnome_askpass}
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/gnome-ssh-askpass.*
%endif

sed -i -e "s|$RPM_BUILD_ROOT||g" $RPM_BUILD_ROOT%{_mandir}/man*/*

%if %{pam_ssh_agent}
pushd pam_ssh_agent_auth-%{pam_ssh_agent_ver}
make install DESTDIR=$RPM_BUILD_ROOT
popd
%endif

%pre
#getent group ssh_keys >/dev/null || groupadd -r ssh_keys || :
groupadd -r ssh_keys || :

%pre server
#getent group sshd >/dev/null || groupadd -g %{sshd_uid} -r sshd || :
groupadd -g %{sshd_uid} -r sshd || :
#getent passwd sshd >/dev/null || \
useradd -c "Privilege-separated SSH" -u %{sshd_uid} -g sshd \
  -s /usr/sbin/nologin -r -d /@unixroot/var/empty/sshd sshd 2> /dev/null || :

%post server
#%systemd_post sshd.service sshd.socket

%preun server
#%systemd_preun sshd.service sshd.socket

%postun server
#%systemd_postun_with_restart sshd.service

%files
%license LICENCE
%doc CREDITS INSTALL OVERVIEW PROTOCOL* README* TODO
#doc ChangeLog
%attr(0755,root,root) %dir %{_sysconfdir}/ssh
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/ssh/moduli
%if ! %{rescue}
%attr(0755,root,root) %{_bindir}/ssh-keygen.exe
%attr(0644,root,root) %{_mandir}/man1/ssh-keygen.1*
%attr(0755,root,root) %dir %{_libexecdir}/openssh
%attr(2555,root,ssh_keys) %{_libexecdir}/openssh/ssh-keysign.exe
%attr(0644,root,root) %{_mandir}/man8/ssh-keysign.8*
%endif

%files clients
%attr(0755,root,root) %{_bindir}/ssh.exe
#%attr(0644,root,root) %{_bindir}/.ssh.hmac
%attr(0644,root,root) %{_mandir}/man1/ssh.1*
%attr(0755,root,root) %{_bindir}/scp.exe
%attr(0644,root,root) %{_mandir}/man1/scp.1*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/ssh/ssh_config
%dir %attr(0755,root,root) %{_sysconfdir}/ssh/ssh_config.d/
%attr(0644,root,root) %{_mandir}/man5/ssh_config.5*
%if ! %{rescue}
%attr(0755,root,root) %{_bindir}/ssh-agent.exe
%attr(0755,root,root) %{_bindir}/ssh-add.exe
%attr(0755,root,root) %{_bindir}/ssh-keyscan.exe
%attr(0755,root,root) %{_bindir}/sftp.exe
%attr(0755,root,root) %{_bindir}/ssh-copy-id
%attr(0755,root,root) %{_libexecdir}/openssh/ssh-pkcs11-helper.exe
%attr(0644,root,root) %{_mandir}/man1/ssh-agent.1*
%attr(0644,root,root) %{_mandir}/man1/ssh-add.1*
%attr(0644,root,root) %{_mandir}/man1/ssh-keyscan.1*
%attr(0644,root,root) %{_mandir}/man1/sftp.1*
%attr(0644,root,root) %{_mandir}/man1/ssh-copy-id.1*
%attr(0644,root,root) %{_mandir}/man8/ssh-pkcs11-helper.8*
%endif

%if ! %{rescue}
%files server
%dir %attr(0711,root,root) %{_var}/empty/sshd
%attr(0755,root,root) %{_sbindir}/sshd.exe
#%attr(0644,root,root) %{_libdir}/fipscheck/.sshd.hmac
%attr(0755,root,root) %{_libexecdir}/openssh/sftp-server.exe
#%attr(0755,root,root) %{_libexecdir}/openssh/sshd-keygen.exe
%attr(0644,root,root) %{_mandir}/man5/sshd_config.5*
%attr(0644,root,root) %{_mandir}/man5/moduli.5*
%attr(0644,root,root) %{_mandir}/man8/sshd.8*
%attr(0644,root,root) %{_mandir}/man8/sftp-server.8*
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/ssh/sshd_config
#%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/pam.d/sshd
#%attr(0755,root,root) %{_sysconfdir}/rc.d/init.d/sshd
#%attr(0644,root,root) %{_unitdir}/sshd.service
#%attr(0644,root,root) %{_unitdir}/sshd@.service
#%attr(0644,root,root) %{_unitdir}/sshd.socket
#%attr(0644,root,root) %{_unitdir}/sshd-keygen@.service
#%attr(0644,root,root) %{_unitdir}/sshd-keygen.target
#%attr(0644,root,root) %{_tmpfilesdir}/openssh.conf
%endif

%if %{ldap}
%files ldap
%doc HOWTO.ldap-keys openssh-lpk-openldap.schema openssh-lpk-sun.schema ldap.conf
%doc openssh-lpk-openldap.ldif openssh-lpk-sun.ldif
%attr(0755,root,root) %{_libexecdir}/openssh/ssh-ldap-helper
%attr(0755,root,root) %{_libexecdir}/openssh/ssh-ldap-wrapper
%attr(0644,root,root) %{_mandir}/man8/ssh-ldap-helper.8*
%attr(0644,root,root) %{_mandir}/man5/ssh-ldap.conf.5*
%endif

%if %{keycat}
%files keycat
%doc HOWTO.ssh-keycat
%attr(0755,root,root) %{_libexecdir}/openssh/ssh-keycat.exe
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/pam.d/ssh-keycat
%endif

%if ! %{no_gnome_askpass}
%files askpass
%attr(0644,root,root) %{_sysconfdir}/profile.d/gnome-ssh-askpass.*
%attr(0755,root,root) %{_libexecdir}/openssh/gnome-ssh-askpass
%attr(0755,root,root) %{_libexecdir}/openssh/ssh-askpass
%endif

%if %{cavs}
%files cavs
%attr(0755,root,root) %{_libexecdir}/openssh/ctr-cavstest.exe
%attr(0755,root,root) %{_libexecdir}/openssh/ssh-cavs.exe
%attr(0755,root,root) %{_libexecdir}/openssh/ssh-cavs_driver.pl
%endif

%if %{pam_ssh_agent}
%files -n pam_ssh_agent_auth
%license pam_ssh_agent_auth-%{pam_ssh_agent_ver}/OPENSSH_LICENSE
%attr(0755,root,root) /%{_lib}/security/pam_ssh_agent_auth.so
%attr(0644,root,root) %{_mandir}/man8/pam_ssh_agent_auth.8*
%endif

%changelog
* Thu Aug 16 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> 7.7p1-2
- create the needed user and group 

* Fri Jul 27 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> 7.7p1-1
- Update to version 7.7.p1.
- moved source to github
