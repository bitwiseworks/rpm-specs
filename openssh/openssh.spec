# Do we want SELinux & Audit
%if 0%{?!noselinux:1}
%global WITH_SELINUX 1
%else
%global WITH_SELINUX 0
%endif

%global _hardened_build 1

# OpenSSH privilege separation requires a user & group ID
%global sshd_uid    74
%global sshd_gid    74

# Do we want to disable building of gnome-askpass? (1=yes 0=no)
%global no_gnome_askpass 0

# Do we want to link against a static libcrypto? (1=yes 0=no)
%global static_libcrypto 0

# Use GTK2 instead of GNOME in gnome-ssh-askpass
%global gtk2 1

# Build position-independent executables (requires toolchain support)?
%global pie 1

# Do we want kerberos5 support (1=yes 0=no)
%global kerberos5 1

# Do we want libedit support
%global libedit 1

# Whether to build pam_ssh_agent_auth
%if 0%{?!nopam:1}
%global pam_ssh_agent 1
%else
%global pam_ssh_agent 0
%endif

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

%if 0%{?os2_version}
# Turn off some stuff for OS/2 builds
%global WITH_SELINUX 0
%global no_gnome_askpass 1
%global gtk2 0
%global pie 0
%global kerberos5 0
%global libedit 0
%global pam_ssh_agent 0
%endif

# Do not forget to bump pam_ssh_agent_auth release if you rewind the main package release to 1
%global openssh_ver 8.4p1
%global openssh_rel 4
%global pam_ssh_agent_ver 0.10.4
%global pam_ssh_agent_rel 1

Summary: An open source implementation of SSH protocol version 2
Name: openssh
Version: %{openssh_ver}
Release: %{openssh_rel}%{?dist}
URL: http://www.openssh.com/portable.html
#URL1: https://github.com/jbeverly/pam_ssh_agent_auth/
%if !0%{?os2_version}
Source0: ftp://ftp.openbsd.org/pub/OpenBSD/OpenSSH/portable/openssh-%{version}.tar.gz
Source1: ftp://ftp.openbsd.org/pub/OpenBSD/OpenSSH/portable/openssh-%{version}.tar.gz.asc
Source2: sshd.pam
Source3: DJM-GPG-KEY.gpg
Source4: https://github.com/jbeverly/pam_ssh_agent_auth/archive/pam_ssh_agent_auth-%{pam_ssh_agent_ver}.tar.gz
Source5: pam_ssh_agent-rmheaders
Source6: ssh-keycat.pam
Source7: sshd.sysconfig
Source9: sshd@.service
Source10: sshd.socket
Source11: sshd.service
Source12: sshd-keygen@.service
Source13: sshd-keygen
Source14: sshd.tmpfiles
Source15: sshd-keygen.target

#https://bugzilla.mindrot.org/show_bug.cgi?id=2581
Patch100: openssh-6.7p1-coverity.patch

#https://bugzilla.mindrot.org/show_bug.cgi?id=1402
# https://bugzilla.redhat.com/show_bug.cgi?id=1171248
# record pfs= field in CRYPTO_SESSION audit event
Patch200: openssh-7.6p1-audit.patch
# Audit race condition in forked child (#1310684)
Patch201: openssh-7.1p2-audit-race-condition.patch

# --- pam_ssh-agent ---
# make it build reusing the openssh sources
Patch300: pam_ssh_agent_auth-0.9.3-build.patch
# check return value of seteuid()
# https://sourceforge.net/p/pamsshagentauth/bugs/23/
Patch301: pam_ssh_agent_auth-0.10.3-seteuid.patch
# explicitly make pam callbacks visible
Patch302: pam_ssh_agent_auth-0.9.2-visibility.patch
# update to current version of agent structure
Patch305: pam_ssh_agent_auth-0.9.3-agent_structure.patch
# remove prefixes to be able to build against current openssh library
Patch306: pam_ssh_agent_auth-0.10.2-compat.patch
# Fix NULL dereference from getpwuid() return value
# https://sourceforge.net/p/pamsshagentauth/bugs/22/
Patch307: pam_ssh_agent_auth-0.10.2-dereference.patch

#https://bugzilla.mindrot.org/show_bug.cgi?id=1641 (WONTFIX)
Patch400: openssh-7.8p1-role-mls.patch
#https://bugzilla.redhat.com/show_bug.cgi?id=781634
Patch404: openssh-6.6p1-privsep-selinux.patch
#?
Patch502: openssh-6.6p1-keycat.patch

#https://bugzilla.mindrot.org/show_bug.cgi?id=1644
Patch601: openssh-6.6p1-allow-ip-opts.patch
#https://bugzilla.mindrot.org/show_bug.cgi?id=1893 (WONTFIX)
Patch604: openssh-6.6p1-keyperm.patch
#(drop?) https://bugzilla.mindrot.org/show_bug.cgi?id=1925
Patch606: openssh-5.9p1-ipv6man.patch
#?
Patch607: openssh-5.8p2-sigpipe.patch
#https://bugzilla.mindrot.org/show_bug.cgi?id=1789
Patch609: openssh-7.2p2-x11.patch

#?
Patch700: openssh-7.7p1-fips.patch
#?
Patch702: openssh-5.1p1-askpass-progress.patch
#https://bugzilla.redhat.com/show_bug.cgi?id=198332
Patch703: openssh-4.3p2-askpass-grab-info.patch
#https://bugzilla.mindrot.org/show_bug.cgi?id=1635 (WONTFIX)
Patch707: openssh-7.7p1-redhat.patch
# warn users for unsupported UsePAM=no (#757545)
Patch711: openssh-7.8p1-UsePAM-warning.patch
# make aes-ctr ciphers use EVP engines such as AES-NI from OpenSSL
Patch712: openssh-6.3p1-ctr-evp-fast.patch
# add cavs test binary for the aes-ctr
Patch713: openssh-6.6p1-ctr-cavstest.patch
# add SSH KDF CAVS test driver
Patch714: openssh-6.7p1-kdf-cavs.patch

# GSSAPI Key Exchange (RFC 4462 + RFC 8732)
# from https://github.com/openssh-gsskex/openssh-gsskex/tree/fedora/master
Patch800: openssh-8.0p1-gssapi-keyex.patch
#http://www.mail-archive.com/kerberos@mit.edu/msg17591.html
Patch801: openssh-6.6p1-force_krb.patch
# add new option GSSAPIEnablek5users and disable using ~/.k5users by default (#1169843)
# CVE-2014-9278
Patch802: openssh-6.6p1-GSSAPIEnablek5users.patch
# Improve ccache handling in openssh (#991186, #1199363, #1566494)
# https://bugzilla.mindrot.org/show_bug.cgi?id=2775
Patch804: openssh-7.7p1-gssapi-new-unique.patch
# Respect k5login_directory option in krk5.conf (#1328243)
Patch805: openssh-7.2p2-k5login_directory.patch


#https://bugzilla.mindrot.org/show_bug.cgi?id=1780
Patch901: openssh-6.6p1-kuserok.patch
# Use tty allocation for a remote scp (#985650)
Patch906: openssh-6.4p1-fromto-remote.patch
# privsep_preauth: use SELinux context from selinux-policy (#1008580)
Patch916: openssh-6.6.1p1-selinux-contexts.patch
# log via monitor in chroots without /dev/log (#2681)
Patch918: openssh-6.6.1p1-log-in-chroot.patch
# scp file into non-existing directory (#1142223)
Patch919: openssh-6.6.1p1-scp-non-existing-directory.patch
# apply upstream patch and make sshd -T more consistent (#1187521)
Patch922: openssh-6.8p1-sshdT-output.patch
# Add sftp option to force mode of created files (#1191055)
Patch926: openssh-6.7p1-sftp-force-permission.patch
# make s390 use /dev/ crypto devices -- ignore closefrom
Patch939: openssh-7.2p2-s390-closefrom.patch
# Move MAX_DISPLAYS to a configuration option (#1341302)
Patch944: openssh-7.3p1-x11-max-displays.patch
# Help systemd to track the running service
Patch948: openssh-7.4p1-systemd.patch
# Pass inetd flags for SELinux down to openbsd compat level
Patch949: openssh-7.6p1-cleanup-selinux.patch
# Sandbox adjustments for s390 and audit
Patch950: openssh-7.5p1-sandbox.patch
# PKCS#11 URIs (upstream #2817, 2nd iteration)
# https://github.com/Jakuje/openssh-portable/commits/jjelen-pkcs11
# git show > ~/devel/fedora/openssh/openssh-8.0p1-pkcs11-uri.patch
Patch951: openssh-8.0p1-pkcs11-uri.patch
# Unbreak scp between two IPv6 hosts (#1620333)
Patch953: openssh-7.8p1-scp-ipv6.patch
# ssh-copy-id is unmaintained: Aggreagete patches
# https://gitlab.com/phil_hands/ssh-copy-id/-/merge_requests/2
Patch958: openssh-7.9p1-ssh-copy-id.patch
# Mention crypto-policies in manual pages (#1668325)
Patch962: openssh-8.0p1-crypto-policies.patch
# Use OpenSSL high-level API to produce and verify signatures (#1707485)
Patch963: openssh-8.0p1-openssl-evp.patch
# Use OpenSSL KDF (#1631761)
Patch964: openssh-8.0p1-openssl-kdf.patch
# sk-dummy.so built with -fvisibility=hidden does not work
Patch965: openssh-8.2p1-visibility.patch
# Do not break X11 without IPv6
Patch966: openssh-8.2p1-x11-without-ipv6.patch
Patch967: openssh-8.4p1-ssh-copy-id.patch
# https://bugzilla.mindrot.org/show_bug.cgi?id=3232
Patch968: openssh-8.4p1-sandbox-seccomp.patch
# https://bugzilla.mindrot.org/show_bug.cgi?id=3213
Patch969: openssh-8.4p1-debian-compat.patch

%else
Vendor: bww bitwise works GmbH

#scm_source github http://github.com/bitwiseworks/%{name}-os2 master-os2
%scm_source git e:/Trees/%{name}/git master-os2
%endif

License: BSD
%if !0%{?os2_version}
Requires: /sbin/nologin
%endif

%if ! %{no_gnome_askpass}
%if %{gtk2}
BuildRequires: gtk2-devel
BuildRequires: libX11-devel
%else
BuildRequires: gnome-libs-devel
%endif
%endif

%if !0%{?os2_version}
BuildRequires: autoconf, automake, perl-interpreter, perl-generators, zlib-devel
BuildRequires: audit-libs-devel >= 2.0.5
BuildRequires: util-linux, groff
BuildRequires: pam-devel
%else
BuildRequires: autoconf, automake, perl, perl-generators, zlib-devel
BuildRequires: groff
%endif
BuildRequires: openssl-devel >= 0.9.8j
%if !0%{?os2_version}
BuildRequires: perl-podlators
BuildRequires: systemd-devel
%endif
BuildRequires: gcc make
BuildRequires: p11-kit-devel
%if !0%{?os2_version}
BuildRequires: libfido2-devel
%endif
Recommends: p11-kit
Obsoletes: openssh-ldap < 8.3p1-4

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

%if !0%{?os2_version}
BuildRequires: xauth
%endif
# for tarball signature verification
BuildRequires: gnupg2

%package clients
Summary: An open source SSH client applications
Requires: openssh = %{version}-%{release}
%if !0%{?os2_version}
Requires: crypto-policies >= 20200610-1
%endif

%package server
Summary: An open source SSH server daemon
Requires: openssh = %{version}-%{release}
%if !0%{?os2_version}
Requires(pre): /usr/sbin/useradd
Requires: pam >= 1.0.1-3
Requires: crypto-policies >= 20200610-1
%{?systemd_requires}
%else
Requires: klusrmgr >= 1.2.0
%endif

%if !0%{?os2_version}
%package keycat
Summary: A mls keycat backend for openssh
Requires: openssh = %{version}-%{release}
%endif

%package askpass
Summary: A passphrase dialog for OpenSSH and X
Requires: openssh = %{version}-%{release}

%if !0%{?os2_version}
%package cavs
Summary: CAVS tests for FIPS validation
Requires: openssh = %{version}-%{release}
%endif

%if %{pam_ssh_agent}
%package -n pam_ssh_agent_auth
Summary: PAM module for authentication with ssh-agent
Version: %{pam_ssh_agent_ver}
Release: %{pam_ssh_agent_rel}.%{openssh_rel}%{?dist}.2
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

%if !0%{?os2_version}
%description keycat
OpenSSH mls keycat is backend for using the authorized keys in the
openssh in the mls mode.
%endif

%description askpass
OpenSSH is a free version of SSH (Secure SHell), a program for logging
into and executing commands on a remote machine. This package contains
an X11 passphrase dialog for OpenSSH.

%if !0%{?os2_version}
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

%if 0%{?os2_version}
%debug_package
%endif

%prep
%if !0%{?os2_version}
gpgv2 --quiet --keyring %{SOURCE3} %{SOURCE1} %{SOURCE0}
%setup -q -a 4

%if %{pam_ssh_agent}
pushd pam_ssh_agent_auth-pam_ssh_agent_auth-%{pam_ssh_agent_ver}
%patch300 -p2 -b .psaa-build
%patch301 -p2 -b .psaa-seteuid
%patch302 -p2 -b .psaa-visibility
%patch306 -p2 -b .psaa-compat
%patch305 -p2 -b .psaa-agent
%patch307 -p2 -b .psaa-deref
# Remove duplicate headers and library files
rm -f $(cat %{SOURCE5})
popd
%endif

%patch400 -p1 -b .role-mls
%patch404 -p1 -b .privsep-selinux

%patch502 -p1 -b .keycat

%patch601 -p1 -b .ip-opts
%patch604 -p1 -b .keyperm
%patch606 -p1 -b .ipv6man
%patch607 -p1 -b .sigpipe
%patch609 -p1 -b .x11
%patch702 -p1 -b .progress
%patch703 -p1 -b .grab-info
%patch707 -p1 -b .redhat
%patch711 -p1 -b .log-usepam-no
%patch712 -p1 -b .evp-ctr
%patch713 -p1 -b .ctr-cavs
%patch714 -p1 -b .kdf-cavs
# 
%patch800 -p1 -b .gsskex
%patch801 -p1 -b .force_krb
%patch804 -p1 -b .ccache_name
%patch805 -p1 -b .k5login
# 
%patch901 -p1 -b .kuserok
%patch906 -p1 -b .fromto-remote
%patch916 -p1 -b .contexts
%patch918 -p1 -b .log-in-chroot
%patch919 -p1 -b .scp
%patch802 -p1 -b .GSSAPIEnablek5users
%patch922 -p1 -b .sshdt
%patch926 -p1 -b .sftp-force-mode
%patch939 -p1 -b .s390-dev
%patch944 -p1 -b .x11max
%patch948 -p1 -b .systemd
%patch949 -p1 -b .refactor
%patch950 -p1 -b .sandbox
%patch951 -p1 -b .pkcs11-uri
%patch953 -p1 -b .scp-ipv6
%patch958 -p1 -b .ssh-copy-id
%patch962 -p1 -b .crypto-policies
%patch963 -p1 -b .openssl-evp
%patch964 -p1 -b .openssl-kdf
%patch965 -p1 -b .visibility
%patch966 -p1 -b .x11-ipv6
%patch967 -p1 -b .ssh-copy-id
%patch968 -p1 -b .seccomp
%patch969 -p0 -b .debian

%patch200 -p1 -b .audit
%patch201 -p1 -b .audit-race
%patch700 -p1 -b .fips

%patch100 -p1 -b .coverity

autoreconf
pushd pam_ssh_agent_auth-pam_ssh_agent_auth-%{pam_ssh_agent_ver}
autoreconf
popd
%else
%scm_setup

autoreconf -fvi
# we create a dummy ChangeLog here
echo "please visit https://github.com/bitwiseworks/openssh-os2" > ChangeLog
%endif

%build
%if 0%{?os2_version}
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
%endif
# the -fvisibility=hidden is needed for clean build of the pam_ssh_agent_auth
# it is needed for lib(open)ssh build too since it is linked to the pam module too
%if !0%{?os2_version}
CFLAGS="$RPM_OPT_FLAGS -fvisibility=hidden"; export CFLAGS
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
if test -r /etc/profile.d/krb5-devel.sh ; then
	source /etc/profile.d/krb5-devel.sh
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

%configure \
	--sysconfdir=%{_sysconfdir}/ssh \
	--libexecdir=%{_libexecdir}/openssh \
	--datadir=%{_datadir}/openssh \
%if !0%{?os2_version}
	--with-default-path=/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin \
	--with-superuser-path=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin \
%else
	--with-default-path="/@unixroot/usr/local/bin;/@unixroot/bin;/@unixroot/usr/bin;/@unixroot/usr/local/sbin;/@unixroot/usr/sbin" \
	--with-superuser-path="/@unixroot/usr/local/sbin;/@unixroot/usr/local/bin;/@unixroot/usr/sbin;/@unixroot/usr/bin" \
	--disable-utmp \
	--disable-utmpx \
	--disable-wtmp \
	--disable-wtmpx \
	--with-pid-dir=%{_var}/run \
%endif
	--with-privsep-path=%{_var}/empty/sshd \
	--disable-strip \
	--without-zlib-version-check \
	--with-ssl-engine \
	--with-ipaddr-display \
	--with-pie=no \
	--without-hardening `# The hardening flags are configured by system` \
%if !0%{?os2_version}
	--with-systemd \
	--with-default-pkcs11-provider=yes \
	--with-security-key-builtin=yes \
	--with-pam \
%endif
%if %{WITH_SELINUX}
	--with-selinux --with-audit=linux \
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

%if !0%{?os2_version}
%make_build
%else
make
%endif

# Define a variable to toggle gnome1/gtk2 building.  This is necessary
# because RPM doesn't handle nested %%if statements.
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

%if %{pam_ssh_agent}
pushd pam_ssh_agent_auth-pam_ssh_agent_auth-%{pam_ssh_agent_ver}
LDFLAGS="$SAVE_LDFLAGS"
%configure --with-selinux \
	--libexecdir=/%{_libdir}/security \
	--with-mantype=man \
	--without-openssl-header-check `# The check is broken`
%make_build
popd
%endif

%check
#to run tests use "--with check"
%if %{?_with_check:1}%{!?_with_check:0}
make tests
%endif

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p -m755 $RPM_BUILD_ROOT%{_sysconfdir}/ssh
mkdir -p -m755 $RPM_BUILD_ROOT%{_sysconfdir}/ssh/ssh_config.d
mkdir -p -m755 $RPM_BUILD_ROOT%{_sysconfdir}/ssh/sshd_config.d
mkdir -p -m755 $RPM_BUILD_ROOT%{_libexecdir}/openssh
mkdir -p -m755 $RPM_BUILD_ROOT%{_var}/empty/sshd
%make_install

%if !0%{?os2_version}
install -d $RPM_BUILD_ROOT/etc/pam.d/
install -d $RPM_BUILD_ROOT/etc/sysconfig/
%else
install -d $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/
install -d $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/
%endif
install -d $RPM_BUILD_ROOT%{_libexecdir}/openssh
%if !0%{?os2_version}
install -m644 %{SOURCE2} $RPM_BUILD_ROOT/etc/pam.d/sshd
install -m644 %{SOURCE6} $RPM_BUILD_ROOT/etc/pam.d/ssh-keycat
install -m644 %{SOURCE7} $RPM_BUILD_ROOT/etc/sysconfig/sshd
install -m644 ssh_config_redhat $RPM_BUILD_ROOT/etc/ssh/ssh_config.d/50-redhat.conf
install -m644 sshd_config_redhat $RPM_BUILD_ROOT/etc/ssh/sshd_config.d/50-redhat.conf
install -d -m755 $RPM_BUILD_ROOT/%{_unitdir}
install -m644 %{SOURCE9} $RPM_BUILD_ROOT/%{_unitdir}/sshd@.service
install -m644 %{SOURCE10} $RPM_BUILD_ROOT/%{_unitdir}/sshd.socket
install -m644 %{SOURCE11} $RPM_BUILD_ROOT/%{_unitdir}/sshd.service
install -m644 %{SOURCE12} $RPM_BUILD_ROOT/%{_unitdir}/sshd-keygen@.service
install -m644 %{SOURCE15} $RPM_BUILD_ROOT/%{_unitdir}/sshd-keygen.target
install -m744 %{SOURCE13} $RPM_BUILD_ROOT/%{_libexecdir}/openssh/sshd-keygen
%endif
install -m755 contrib/ssh-copy-id $RPM_BUILD_ROOT%{_bindir}/
install contrib/ssh-copy-id.1 $RPM_BUILD_ROOT%{_mandir}/man1/
%if !0%{?os2_version}
install -m644 -D %{SOURCE14} $RPM_BUILD_ROOT%{_tmpfilesdir}/%{name}.conf
%endif

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
%if !0%{?os2_version}
rm -f $RPM_BUILD_ROOT/etc/profile.d/gnome-ssh-askpass.*
%else
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/gnome-ssh-askpass.*
%endif
%endif

%if !0%{?os2_version}
perl -pi -e "s|$RPM_BUILD_ROOT||g" $RPM_BUILD_ROOT%{_mandir}/man*/*
%else
perl -pi.bak -e "s|$RPM_BUILD_ROOT||g" $RPM_BUILD_ROOT%{_mandir}/man*/*
rm -f $RPM_BUILD_ROOT%{_mandir}/man*/*.bak
%endif

%if %{pam_ssh_agent}
pushd pam_ssh_agent_auth-pam_ssh_agent_auth-%{pam_ssh_agent_ver}
%make_install
popd
%endif
%pre
%if !0%{?os2_version}
getent group ssh_keys >/dev/null || groupadd -r ssh_keys || :
%else
groupadd -r ssh_keys || :
%endif

%pre server
%if !0%{?os2_version}
getent group sshd >/dev/null || groupadd -g %{sshd_uid} -r sshd || :
%else
groupadd -g %{sshd_uid} -r sshd || :
%endif
%if !0%{?os2_version}
getent passwd sshd >/dev/null || \
  useradd -c "Privilege-separated SSH" -u %{sshd_uid} -g sshd \
  -s /sbin/nologin -r -d /var/empty/sshd sshd 2> /dev/null || :
%else
  useradd -c "Privilege-separated SSH" -u %{sshd_uid} -g sshd \
  -s /usr/sbin/nologin -r -d /@unixroot/var/empty/sshd sshd 2> /dev/null || :
%endif

%post server
%if !0%{?os2_version}
%systemd_post sshd.service sshd.socket
# Migration scriptlet for Fedora 31 and 32 installations to sshd_config
# drop-in directory (in F32+).
# Do this only if the file generated by anaconda exists, contains our config
# directive and sshd_config contains include directive as shipped in our package
%global sysconfig_anaconda /etc/sysconfig/sshd-permitrootlogin
test -f %{sysconfig_anaconda} && \
  test ! -f /etc/ssh/sshd_config.d/01-permitrootlogin.conf && \
  grep -q '^PERMITROOTLOGIN="-oPermitRootLogin=yes"' %{sysconfig_anaconda} && \
  grep -q '^Include /etc/ssh/sshd_config.d/\*.conf' /etc/ssh/sshd_config && \
  echo "PermitRootLogin yes" >> /etc/ssh/sshd_config.d/25-permitrootlogin.conf && \
  rm %{sysconfig_anaconda} || :
%endif

%preun server
%if !0%{?os2_version}
%systemd_preun sshd.service sshd.socket
%endif

%postun server
%if !0%{?os2_version}
%systemd_postun_with_restart sshd.service
%endif

%files
%license LICENCE
%doc CREDITS ChangeLog OVERVIEW PROTOCOL* README README.platform README.privsep README.tun README.dns TODO
%attr(0755,root,root) %dir %{_sysconfdir}/ssh
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/ssh/moduli
%if !0%{?os2_version}
%attr(0755,root,root) %{_bindir}/ssh-keygen
%else
%attr(0755,root,root) %{_bindir}/ssh-keygen.exe
%endif
%attr(0644,root,root) %{_mandir}/man1/ssh-keygen.1*
%attr(0755,root,root) %dir %{_libexecdir}/openssh
%if !0%{?os2_version}
%attr(2555,root,ssh_keys) %{_libexecdir}/openssh/ssh-keysign
%else
%attr(2555,root,ssh_keys) %{_libexecdir}/openssh/ssh-keysign.exe
%endif
%attr(0644,root,root) %{_mandir}/man8/ssh-keysign.8*

%files clients
%if !0%{?os2_version}
%attr(0755,root,root) %{_bindir}/ssh
%else
%attr(0755,root,root) %{_bindir}/ssh.exe
%endif
%attr(0644,root,root) %{_mandir}/man1/ssh.1*
%if !0%{?os2_version}
%attr(0755,root,root) %{_bindir}/scp
%else
%attr(0755,root,root) %{_bindir}/scp.exe
%endif
%attr(0644,root,root) %{_mandir}/man1/scp.1*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/ssh/ssh_config
%dir %attr(0755,root,root) %{_sysconfdir}/ssh/ssh_config.d/
%if !0%{?os2_version}
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/ssh/ssh_config.d/50-redhat.conf
%endif
%attr(0644,root,root) %{_mandir}/man5/ssh_config.5*
%if !0%{?os2_version}
%attr(0755,root,root) %{_bindir}/ssh-agent
%attr(0755,root,root) %{_bindir}/ssh-add
%attr(0755,root,root) %{_bindir}/ssh-keyscan
%attr(0755,root,root) %{_bindir}/sftp
%else
%attr(0755,root,root) %{_bindir}/ssh-agent.exe
%attr(0755,root,root) %{_bindir}/ssh-add.exe
%attr(0755,root,root) %{_bindir}/ssh-keyscan.exe
%attr(0755,root,root) %{_bindir}/sftp.exe
%endif
%attr(0755,root,root) %{_bindir}/ssh-copy-id
%if !0%{?os2_version}
%attr(0755,root,root) %{_libexecdir}/openssh/ssh-pkcs11-helper
%attr(0755,root,root) %{_libexecdir}/openssh/ssh-sk-helper
%else
%attr(0755,root,root) %{_libexecdir}/openssh/ssh-pkcs11-helper.exe
%attr(0755,root,root) %{_libexecdir}/openssh/ssh-sk-helper.exe
%endif
%attr(0644,root,root) %{_mandir}/man1/ssh-agent.1*
%attr(0644,root,root) %{_mandir}/man1/ssh-add.1*
%attr(0644,root,root) %{_mandir}/man1/ssh-keyscan.1*
%attr(0644,root,root) %{_mandir}/man1/sftp.1*
%attr(0644,root,root) %{_mandir}/man1/ssh-copy-id.1*
%attr(0644,root,root) %{_mandir}/man8/ssh-pkcs11-helper.8*
%attr(0644,root,root) %{_mandir}/man8/ssh-sk-helper.8*

%files server
%dir %attr(0711,root,root) %{_var}/empty/sshd
%if !0%{?os2_version}
%attr(0755,root,root) %{_sbindir}/sshd
%attr(0755,root,root) %{_libexecdir}/openssh/sftp-server
%attr(0755,root,root) %{_libexecdir}/openssh/sshd-keygen
%else
%attr(0755,root,root) %{_sbindir}/sshd.exe
%attr(0755,root,root) %{_libexecdir}/openssh/sftp-server.exe
%endif
%attr(0644,root,root) %{_mandir}/man5/sshd_config.5*
%attr(0644,root,root) %{_mandir}/man5/moduli.5*
%attr(0644,root,root) %{_mandir}/man8/sshd.8*
%attr(0644,root,root) %{_mandir}/man8/sftp-server.8*
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/ssh/sshd_config
%if !0%{?os2_version}
%dir %attr(0700,root,root) %{_sysconfdir}/ssh/sshd_config.d/
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/ssh/sshd_config.d/50-redhat.conf
%attr(0644,root,root) %config(noreplace) /etc/pam.d/sshd
%attr(0640,root,root) %config(noreplace) /etc/sysconfig/sshd
%attr(0644,root,root) %{_unitdir}/sshd.service
%attr(0644,root,root) %{_unitdir}/sshd@.service
%attr(0644,root,root) %{_unitdir}/sshd.socket
%attr(0644,root,root) %{_unitdir}/sshd-keygen@.service
%attr(0644,root,root) %{_unitdir}/sshd-keygen.target
%attr(0644,root,root) %{_tmpfilesdir}/openssh.conf
%endif

%if !0%{?os2_version}
%files keycat
%doc HOWTO.ssh-keycat
%attr(0755,root,root) %{_libexecdir}/openssh/ssh-keycat
%attr(0644,root,root) %config(noreplace) /etc/pam.d/ssh-keycat
%endif

%if ! %{no_gnome_askpass}
%files askpass
%attr(0644,root,root) %{_sysconfdir}/profile.d/gnome-ssh-askpass.*
%attr(0755,root,root) %{_libexecdir}/openssh/gnome-ssh-askpass
%attr(0755,root,root) %{_libexecdir}/openssh/ssh-askpass
%endif

%if !0%{?os2_version}
%files cavs
%attr(0755,root,root) %{_libexecdir}/openssh/ctr-cavstest
%attr(0755,root,root) %{_libexecdir}/openssh/ssh-cavs
%attr(0755,root,root) %{_libexecdir}/openssh/ssh-cavs_driver.pl
%endif

%if %{pam_ssh_agent}
%files -n pam_ssh_agent_auth
%license pam_ssh_agent_auth-pam_ssh_agent_auth-%{pam_ssh_agent_ver}/OPENSSH_LICENSE
%attr(0755,root,root) %{_libdir}/security/pam_ssh_agent_auth.so
%attr(0644,root,root) %{_mandir}/man8/pam_ssh_agent_auth.8*
%endif

%changelog
* Mon Feb 01 2021 Silvan Scherrer <silvan.scherrer@aroa.ch> 8.4p1-1
- update to vendor version 8.4

* Tue Nov 27 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> 7.7p1-4
- don't echo password
- handle stdin/stdout in select()

* Fri Aug 17 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> 7.7p1-3
- use socketpair() instead of pipe()

* Thu Aug 16 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> 7.7p1-2
- create the needed user and group 

* Fri Jul 27 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> 7.7p1-1
- Update to version 7.7.p1.
- moved source to github
