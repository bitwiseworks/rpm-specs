# Do we want SELinux & Audit
%define WITH_SELINUX 0

# OpenSSH privilege separation requires a user & group ID
%define sshd_uid    74
%define sshd_gid    74

# Do we want to disable building of gnome-askpass? (1=yes 0=no)
%define no_gnome_askpass 1

# Do we want to link against a static libcrypto? (1=yes 0=no)
%define static_libcrypto 0

# Do we want smartcard support (1=yes 0=no)
#Smartcard support is broken from 5.4p1
%define scard 0

# Use GTK2 instead of GNOME in gnome-ssh-askpass
%define gtk2 0

# Build position-independent executables (requires toolchain support)?
%define pie 0

# Do we want kerberos5 support (1=yes 0=no)
%define kerberos5 0

# Do we want libedit support
%define libedit 0

# Do we want NSS tokens support
#NSS support is broken from 5.4p1
%define nss 0

# Whether or not /sbin/nologin exists.
%define nologin 1

# Whether to build pam_ssh_agent_auth
%define pam_ssh_agent 0

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

# Options for Smartcard support: (needs libsectok and openssl-engine)
# rpm -ba|--rebuild --define "smartcard 1"
%{?smartcard:%global scard 1}

# Is this a build for the rescue CD (without PAM, with MD5)? (1=yes 0=no)
%define rescue 0
%{?build_rescue:%global rescue 1}
%{?build_rescue:%global rescue_rel rescue}

# Turn off some stuff for resuce builds
%if %{rescue}
%define kerberos5 0
%define libedit 0
%define pam_ssh_agent 0
%endif

# Do not forget to bump pam_ssh_agent_auth release if you rewind the main package release to 1
%define openssh_rel 1
%define pam_ssh_agent_rel 24
%define pam_ssh_agent_ver 0.9.2

Summary: An open source implementation of SSH protocol versions 1 and 2
Name: openssh
Version: 5.9p1
Release: %{openssh_rel}%{?dist}%{?rescue_rel}
URL: http://www.openssh.com/portable.html

Source0: ftp://ftp.openbsd.org/pub/OpenBSD/OpenSSH/portable/openssh-%{version}.tar.gz

Patch1: openssh-os2.diff

License: BSD
Group: Applications/Internet
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%if %{nologin}
#Requires: /sbin/nologin
%endif

#Requires: initscripts >= 5.20

%if ! %{no_gnome_askpass}
%if %{gtk2}
BuildRequires: gtk2-devel
BuildRequires: libX11-devel
%else
BuildRequires: gnome-libs-devel
%endif
%endif

%if %{scard}
BuildRequires: sharutils
%endif
BuildRequires: perl, zlib-devel
#BuildRequires: audit-libs-devel
#BuildRequires: util-linux, groff, man
#BuildRequires: pam-devel
#BuildRequires: tcp_wrappers-devel
#BuildRequires: fipscheck-devel
BuildRequires: openssl-devel >= 0.9.8j

%if %{kerberos5}
BuildRequires: krb5-devel
%endif

%if %{libedit}
BuildRequires: libedit-devel ncurses-devel
%endif

%if %{nss}
BuildRequires: nss-devel
%endif

%if %{WITH_SELINUX}
Requires: libselinux >= 1.27.7
BuildRequires: libselinux-devel >= 1.27.7
Requires: audit-libs >= 1.0.8
BuildRequires: audit-libs >= 1.0.8
%endif

#BuildRequires: xauth
BuildRequires: curl-devel ncurses-devel

%package clients
Summary: An open source SSH client applications
Requires: openssh = %{version}-%{release}
Group: Applications/Internet

%package server
Summary: An open source SSH server daemon
Group: System Environment/Daemons
Requires: openssh = %{version}-%{release}
Requires(post): chkconfig >= 0.9, /sbin/service
Requires(pre): /usr/sbin/useradd
Requires: pam >= 1.0.1-3

%package askpass
Summary: A passphrase dialog for OpenSSH and X
Group: Applications/Internet
Requires: openssh = %{version}-%{release}
Obsoletes: openssh-askpass-gnome
Provides: openssh-askpass-gnome

%package -n pam_ssh_agent_auth
Summary: PAM module for authentication with ssh-agent
Group: System Environment/Base
Version: %{pam_ssh_agent_ver}
Release: %{pam_ssh_agent_rel}.%{openssh_rel}%{?dist}%{?rescue_rel}
License: BSD

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

%description askpass
OpenSSH is a free version of SSH (Secure SHell), a program for logging
into and executing commands on a remote machine. This package contains
an X11 passphrase dialog for OpenSSH.

%description -n pam_ssh_agent_auth
This package contains a PAM module which can be used to authenticate
users using ssh keys stored in a ssh-agent. Through the use of the
forwarding of ssh-agent connection it also allows to authenticate with
remote ssh-agent instance.

The module is most useful for su and sudo service stacks.

%prep
%setup -q
%patch1 -p1 -b .os2~


%build
export CONFIG_SHELL="/bin/sh" 
export LIBS="-lurpo -lpthread"

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
	--disable-utmp \
	--disable-utmpx \
	--disable-wtmp \
	--disable-wtmpx \
	--disable-libutil \
	--disable-pututline \
	--disable-pututxline \
%if %{nss}
	--with-nss \
%endif
%if %{scard}
	--with-smartcard \
%endif
%if %{rescue}
	--without-pam \
%else
	--without-pam \
%endif
%if %{WITH_SELINUX}
	--with-selinux --with-linux-audit \
%endif
%if %{kerberos5}
	--with-kerberos5${krb5_prefix:+=${krb5_prefix}} \
%else
	--without-kerberos5 \
%endif
%if %{libedit}
	--with-libedit \
%else
	--without-libedit \
%endif
	"--cache-file=%{_topdir}/cache/%{name}-%{_target_cpu}.cache"

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
	make gnome-ssh-askpass2
	mv gnome-ssh-askpass2 gnome-ssh-askpass
else
	make gnome-ssh-askpass1
	mv gnome-ssh-askpass1 gnome-ssh-askpass
fi
popd
%endif

%if %{pam_ssh_agent}
pushd pam_ssh_agent_auth-%{pam_ssh_agent_ver}
LDFLAGS="$SAVE_LDFLAGS"
%configure --with-selinux --libexecdir=/%{_lib}/security
make
popd
%endif

# Add generation of HMAC checksums of the final stripped binaries
%define __spec_install_post_000 \
    %{?__debug_package:%{__debug_install_post}} \
    %{__arch_install_post} \
    %{__os_install_post} \
    fipshmac $RPM_BUILD_ROOT%{_bindir}/ssh \
    fipshmac $RPM_BUILD_ROOT%{_sbindir}/sshd \
%{nil}

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p -m755 $RPM_BUILD_ROOT%{_sysconfdir}/ssh
mkdir -p -m755 $RPM_BUILD_ROOT%{_libexecdir}/openssh
mkdir -p -m755 $RPM_BUILD_ROOT%{_var}/empty/sshd
make install DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/
install -d $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d
install -d $RPM_BUILD_ROOT%{_libexecdir}/openssh
#install -m644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/sshd
#install -m755 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/sshd
install -m755 contrib/ssh-copy-id $RPM_BUILD_ROOT%{_bindir}/
mkdir -p -m755 $RPM_BUILD_ROOT%{_mandir}/man1
install contrib/ssh-copy-id.1 $RPM_BUILD_ROOT%{_mandir}/man1/

%if ! %{no_gnome_askpass}
install -s contrib/gnome-ssh-askpass $RPM_BUILD_ROOT%{_libexecdir}/openssh/gnome-ssh-askpass
%endif

%if ! %{scard}
	rm -f $RPM_BUILD_ROOT%{_datadir}/openssh/Ssh.bin
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

rm -f README.nss.nss-keys
%if ! %{nss}
rm -f README.nss
%endif

%if %{pam_ssh_agent}
pushd pam_ssh_agent_auth-%{pam_ssh_agent_ver}
make install DESTDIR=$RPM_BUILD_ROOT
popd
%endif
%clean
rm -rf $RPM_BUILD_ROOT

%pre server
%if %{nologin}
/usr/sbin/useradd -c "Privilege-separated SSH" -u %{sshd_uid} \
	-s /sbin/nologin -r -d /var/empty/sshd sshd 2> /dev/null || :
%else
/usr/sbin/useradd -c "Privilege-separated SSH" -u %{sshd_uid} \
	-s /dev/null -r -d /var/empty/sshd sshd 2> /dev/null || :
%endif

%post server
/sbin/chkconfig --add sshd

%postun server
/sbin/service sshd condrestart > /dev/null 2>&1 || :

%preun server
if [ "$1" = 0 ]
then
	/sbin/service sshd stop > /dev/null 2>&1 || :
	/sbin/chkconfig --del sshd
fi

%files
%defattr(-,root,root)
%doc CREDITS ChangeLog INSTALL LICENCE OVERVIEW PROTOCOL* README* TODO
#WARNING*
%attr(0755,root,root) %dir %{_sysconfdir}/ssh
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/ssh/moduli
%if ! %{rescue}
%attr(0755,root,root) %{_bindir}/ssh-keygen.exe
%attr(0644,root,root) %{_mandir}/cat1/ssh-keygen.1*
%attr(0755,root,root) %dir %{_libexecdir}/openssh
%attr(4755,root,root) %{_libexecdir}/openssh/ssh-keysign.exe
%attr(0644,root,root) %{_mandir}/cat8/ssh-keysign.8*
%endif
%if %{scard}
%attr(0755,root,root) %dir %{_datadir}/openssh
%attr(0644,root,root) %{_datadir}/openssh/Ssh.bin
%endif

%files clients
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/ssh.exe
#%attr(0644,root,root) %{_bindir}/.ssh.hmac
%attr(0644,root,root) %{_mandir}/cat1/ssh.1*
%attr(0755,root,root) %{_bindir}/scp.exe
%attr(0644,root,root) %{_mandir}/cat1/scp.1*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/ssh/ssh_config
%attr(0755,root,root) %{_bindir}/slogin.exe
%attr(0644,root,root) %{_mandir}/cat1/slogin.1*
%attr(0644,root,root) %{_mandir}/cat5/ssh_config.5*
%if ! %{rescue}
%attr(2755,root,nobody) %{_bindir}/ssh-agent.exe
%attr(0755,root,root) %{_bindir}/ssh-add.exe
%attr(0755,root,root) %{_bindir}/ssh-keyscan.exe
%attr(0755,root,root) %{_bindir}/sftp.exe
%attr(0755,root,root) %{_bindir}/ssh-copy-id
%attr(0755,root,root) %{_libexecdir}/openssh/ssh-pkcs11-helper.exe
%attr(0644,root,root) %{_mandir}/cat1/ssh-agent.1*
%attr(0644,root,root) %{_mandir}/cat1/ssh-add.1*
%attr(0644,root,root) %{_mandir}/cat1/ssh-keyscan.1*
%attr(0644,root,root) %{_mandir}/cat1/sftp.1*
%attr(0644,root,root) %{_mandir}/man1/ssh-copy-id.1*
%attr(0644,root,root) %{_mandir}/cat8/ssh-pkcs11-helper.8*
%endif

%if ! %{rescue}
%files server
%defattr(-,root,root)
%dir %attr(0711,root,root) %{_var}/empty/sshd
%attr(0755,root,root) %{_sbindir}/sshd.exe
#%attr(0644,root,root) %{_sbindir}/.sshd.hmac
%attr(0755,root,root) %{_libexecdir}/openssh/sftp-server.exe
%attr(0644,root,root) %{_mandir}/cat5/sshd_config.5*
%attr(0644,root,root) %{_mandir}/cat5/moduli.5*
%attr(0644,root,root) %{_mandir}/cat8/sshd.8*
%attr(0644,root,root) %{_mandir}/cat8/sftp-server.8*
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/ssh/sshd_config
#%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/pam.d/sshd
#%attr(0755,root,root) %{_sysconfdir}/rc.d/init.d/sshd
%endif

%if ! %{no_gnome_askpass}
%files askpass
%defattr(-,root,root)
%attr(0644,root,root) %{_sysconfdir}/profile.d/gnome-ssh-askpass.*
%attr(0755,root,root) %{_libexecdir}/openssh/gnome-ssh-askpass
%attr(0755,root,root) %{_libexecdir}/openssh/ssh-askpass
%endif

%if %{pam_ssh_agent}
%files -n pam_ssh_agent_auth
%defattr(-,root,root)
%doc pam_ssh_agent_auth-%{pam_ssh_agent_ver}/OPENSSH_LICENSE
%attr(0755,root,root) /%{_lib}/security/pam_ssh_agent_auth.so
%attr(0644,root,root) %{_mandir}/cat8/pam_ssh_agent_auth.8*
%endif

%changelog
