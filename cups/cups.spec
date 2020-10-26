%define _strip_opts --compress -i "*.cgi" --debuginfo -i "*.cgi"

%global use_alternatives 0
%global lspp 0
%global dbus 0
%global dnsds 0
%global gnutls 0
%global systemd 0
%global openldap 0
%global krb5 0
%global php 0
%global used_on_os2 0

# {_exec_prefix}/lib/cups is correct, even on x86_64.
# It is not used for shared objects but for executables.
# It's more of a libexec-style ({_libexecdir}) usage,
# but we use lib for compatibility with 3rd party drivers (at upstream request).
%global cups_serverbin %{_exec_prefix}/lib/cups

#%%global prever rc1
#%%global VERSION %%{version}%%{prever}
%global VERSION %{version}

Summary: CUPS printing system
Name: cups
Epoch: 1
Version: 2.2.12
Release: 1%{?dist}

License: GPLv2+ and LGPLv2+ with exceptions and AML
Url: http://www.cups.org

Vendor: bww bitwise works GmbH
%scm_source  github https://github.com/bitwiseworks/%{name}-os2 %{version}-os2
Source8:  macros.%{name}

Requires: %{name}-filesystem = %{epoch}:%{version}-%{release}
Requires: %{name}-libs = %{epoch}:%{version}-%{release}
Requires: %{name}-client = %{epoch}:%{version}-%{release}
Requires: %{name}-ipptool = %{epoch}:%{version}-%{release}

Provides: cupsddk, cupsddk-drivers

%if %{used_on_os2}
BuildRequires: pam-devel
%endif
#BuildRequires: pkgconf-pkg-config
BuildRequires: pkgconfig
%if %{gnutls}
BuildRequires: pkgconfig(gnutls)
%endif
%if %{openldap}
BuildRequires: libacl-devel
BuildRequires: openldap-devel
%endif
#BuildRequires: pkgconfig(libusb-1.0)
BuildRequires: libusb1 >= 1.0.16
%if %{krb5}
BuildRequires: krb5-devel
%endif
%if %{dnsds}
BuildRequires: pkgconfig(avahi-client)
%endif
%if %{systemd}
BuildRequires: systemd
BuildRequires: pkgconfig(libsystemd)
%endif
%if %{dbus}
BuildRequires: pkgconfig(dbus-1)
%endif
BuildRequires: automake
# needed for decompressing functions when reading from gzipped ppds
BuildRequires: zlib-devel

# gcc and gcc-c++ is no longer in buildroot by default
# gcc for most of files
BuildRequires: gcc
# gcc-c++ for ppdc and cups-driverd
#Buildrequires: gcc-c++

# Make sure we get postscriptdriver tags.
#BuildRequires: python3-cups

%if %{lspp}
BuildRequires: libselinux-devel
BuildRequires: audit-libs-devel
%endif

%if %{dbus}
Requires: dbus
%endif

# Requires working PrivateTmp (bug #807672)
%if %{systemd}
Requires(pre): systemd
Requires(post): systemd
%endif
Requires(post): grep, sed
%if %{systemd}
Requires(preun): systemd
Requires(postun): systemd
%endif

# We ship udev rules which use setfacl.
%if %{systemd}
Requires: systemd
Requires: acl
%endif

# Make sure we have some filters for converting to raster format.
Requires: cups-filters

%package client
Summary: CUPS printing system - client programs
License: GPLv2
Requires: %{name}-libs = %{epoch}:%{version}-%{release}
%if %{use_alternatives}
Provides: /@unixroot/usr/bin/lpq /@unixroot/usr/bin/lpr /@unixroot/usr/bin/lp /@unixroot/usr/bin/cancel /@unixroot/usr/bin/lprm /@unixroot/usr/bin/lpstat
Requires: /@unixroot/usr/sbin/alternatives
%endif
Provides: lpr

%package devel
Summary: CUPS printing system - development environment
License: LGPLv2
Requires: %{name}-libs = %{epoch}:%{version}-%{release}
%if %{gnutls}
Requires: gnutls-devel
%endif
%if %{krb5}
Requires: krb5-devel
%endif
Requires: zlib-devel
Provides: cupsddk-devel

%package libs
Summary: CUPS printing system - libraries
License: LGPLv2 and zlib

%package filesystem
Summary: CUPS printing system - directory layout
BuildArch: noarch

%package lpd
Summary: CUPS printing system - lpd emulation
Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: %{name}-libs = %{epoch}:%{version}-%{release}
Provides: lpd

%package ipptool
Summary: CUPS printing system - tool for performing IPP requests
Requires: %{name} = %{epoch}:%{version}-%{release}


%description
CUPS printing system provides a portable printing layer for
UNIX© operating systems. It has been developed by Apple Inc.
to promote a standard printing solution for all UNIX vendors and users.
CUPS provides the System V and Berkeley command-line interfaces.
CUPS was ported to OS/2 to have the same benefit as UNIX has.

%description client
CUPS printing system provides a portable printing layer for
UNIX© operating systems. This package contains command-line client
programs.

%description devel
CUPS printing system provides a portable printing layer for
UNIX© operating systems. This is the development package for creating
additional printer drivers, and other CUPS services.

%description libs
CUPS printing system provides a portable printing layer for
UNIX© operating systems. It has been developed by Apple Inc.
to promote a standard printing solution for all UNIX vendors and users.
CUPS provides the System V and Berkeley command-line interfaces.
CUPS was ported to OS/2 to have the same benefit as UNIX has.
The cups-libs package provides libraries used by applications to use CUPS
natively, without needing the lpp/lpr commands.

%description filesystem
CUPS printing system provides a portable printing layer for
UNIX© operating systems. This package provides some directories which are
required by other packages that add CUPS drivers (i.e. filters, backends etc.)

%description lpd
CUPS printing system provides a portable printing layer for
UNIX© operating systems. This is the package that provides standard
lpd emulation.

%description ipptool
Sends IPP requests to the specified URI and tests and/or displays the result.

%debug_package

%prep
%scm_setup

%if %{used_on_os2}
# if cupsd is set to log into /var/log/cups, then 'MaxLogSize 0' needs to be
# in cupsd.conf to disable cupsd logrotate functionality and use logrotated
sed -i -e '1iMaxLogSize 0' conf/cupsd.conf.in

# Log to the system journal by default (bug #1078781, bug #1519331).
sed -i -e 's,^ErrorLog .*$,ErrorLog syslog,' conf/cups-files.conf.in
sed -i -e 's,^AccessLog .*$,AccessLog syslog,' conf/cups-files.conf.in
sed -i -e 's,^PageLog .*,PageLog syslog,' conf/cups-files.conf.in

# Add comment text mentioning syslog is systemd journal (bug #1358589)
sed -i -e 's,\"syslog\",\"syslog\" \(syslog means systemd journal by default\),' conf/cups-files.conf.in

# Add group wheel to SystemGroups (bug #1405669)
sed -i -e 's,^SystemGroup .*$, SystemGroup sys root wheel,' conf/cups-files.conf.in

# Let's look at the compilation command lines.
perl -pi -e "s,^.SILENT:,," Makedefs.in

f=CREDITS.md
mv "$f" "$f"~
iconv -f MACINTOSH -t UTF-8 "$f"~ > "$f"
rm -f "$f"~
%endif

aclocal -I config-scripts
autoconf -f -I config-scripts

%build
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
export VENDOR="%{vendor}"

# cups can use different compiler if it is installed, so set to GCC for to be sure
export CC=gcc
export CXX=g++
export CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS"
export LDFLAGS="$LDFLAGS $RPM_OPT_FLAGS"
%configure --with-docdir=%{_datadir}/%{name}/www --enable-debug \
%if %{lspp}
	--enable-lspp \
%endif
	--with-exe-file-perm=0755 \
	--with-cupsd-file-perm=0755 \
	--with-log-file-perm=0600 \
	--enable-relro \
%if %{dbus}
	--with-dbusdir=%{_sysconfdir}/dbus-1 \
%endif
%if %{php}
	--with-php=/@unixroot/usr/bin/php-cgi \
%endif
%if %{dnsds}
	--enable-avahi \
%endif
	--enable-threads \
%if %{gnutls}
	--enable-gnutls \
%endif
	--enable-webif \
	--with-xinetd=no \
	--with-access-log-level=actions \
	--enable-page-logging \
	--with-system_groups=admin \
	--with-domainsocket=/socket/cups.sock \
	--enable-debug-printfs \
	localedir=%{_datadir}/locale

# If we got this far, all prerequisite libraries must be here.
make %{?_smp_mflags}

%install
make BUILDROOT=%{buildroot} install

rm -rf	%{buildroot}%{_initddir} \
	%{buildroot}%{_sysconfdir}/init.d \
	%{buildroot}%{_sysconfdir}/rc.d
%if %{systemd}
mkdir -p %{buildroot}%{_unitdir}
%endif

%if %{used_on_os2}
find %{buildroot}%{_datadir}/cups/model -name "*.ppd" |xargs gzip -n9f
%endif

%if %{use_alternatives}
pushd %{buildroot}%{_bindir}
for i in cancel lp lpq lpr lprm lpstat; do
	mv $i $i.cups
done

cd %{buildroot}%{_sbindir}
mv lpc lpc.cups
cd %{buildroot}%{_mandir}/man1
for i in cancel lp lpq lpr lprm lpstat; do
	mv $i.1 $i-cups.1
done
cd %{buildroot}%{_mandir}/man8

mv lpc.8 lpc-cups.8
popd
%endif

%if %{systemd}
mv %{buildroot}%{_unitdir}/org.cups.cupsd.path %{buildroot}%{_unitdir}/cups.path
mv %{buildroot}%{_unitdir}/org.cups.cupsd.service %{buildroot}%{_unitdir}/cups.service
mv %{buildroot}%{_unitdir}/org.cups.cupsd.socket %{buildroot}%{_unitdir}/cups.socket
mv %{buildroot}%{_unitdir}/org.cups.cups-lpd.socket %{buildroot}%{_unitdir}/cups-lpd.socket
mv %{buildroot}%{_unitdir}/org.cups.cups-lpd@.service %{buildroot}%{_unitdir}/cups-lpd@.service
sed -i -e "s,org.cups.cupsd,cups,g" %{buildroot}%{_unitdir}/cups.service
%endif

# Ship an rpm macro for where to put driver executables
mkdir -p %{buildroot}%{_rpmconfigdir}/macros.d
install -m 0644 %{SOURCE8} %{buildroot}%{_rpmconfigdir}/macros.d

# Ship a printers.conf file, and a client.conf file.  That way, they get
# their SELinux file contexts set correctly.
touch %{buildroot}%{_sysconfdir}/cups/printers.conf
touch %{buildroot}%{_sysconfdir}/cups/classes.conf
touch %{buildroot}%{_sysconfdir}/cups/client.conf
touch %{buildroot}%{_sysconfdir}/cups/subscriptions.conf
touch %{buildroot}%{_sysconfdir}/cups/lpoptions

# LSB 3.2 printer driver directory
mkdir -p %{buildroot}%{_datadir}/ppd

# Remove unshipped files.
rm -rf %{buildroot}%{_mandir}/cat? %{buildroot}%{_mandir}/*/cat?
rm -f %{buildroot}%{_datadir}/applications/cups.desktop
rm -rf %{buildroot}%{_datadir}/icons
# there are pdf-banners shipped with cups-filters (#919489)
rm -rf %{buildroot}%{_datadir}/cups/banners
rm -f %{buildroot}%{_datadir}/cups/data/testprint

%if %{used_on_os2}
# install /usr/lib/tmpfiles.d/cups.conf (bug #656566, bug #893834)
mkdir -p ${RPM_BUILD_ROOT}%{_tmpfilesdir}
cat > ${RPM_BUILD_ROOT}%{_tmpfilesdir}/cups.conf <<EOF
# See tmpfiles.d(5) for details

d /run/cups 0755 root lp -
d /run/cups/certs 0511 lp sys -

d /var/spool/cups/tmp - - - 30d
EOF

# /usr/lib/tmpfiles.d/cups-lp.conf (bug #812641)
cat > ${RPM_BUILD_ROOT}%{_tmpfilesdir}/cups-lp.conf <<EOF
# Legacy parallel port character device nodes, to trigger the
# auto-loading of the kernel module on access.
#
# See tmpfiles.d(5) for details

c /dev/lp0 0660 root lp - 6:0
c /dev/lp1 0660 root lp - 6:1
c /dev/lp2 0660 root lp - 6:2
c /dev/lp3 0660 root lp - 6:3
EOF
%endif

find %{buildroot} -type f -o -type l | sed '
s:.*\('%{_datadir}'/\)\([^/_]\+\)\(.*\.po$\):%lang(\2) \1\2\3:
/^%lang(C)/d
/^\([^%].*\)/d
' > %{name}.lang

%post
%if %{systemd}
%systemd_post %{name}.path %{name}.socket %{name}.service
%endif

# Remove old-style certs directory; new-style is /var/run
# (see bug #194581 for why this is necessary).
rm -rf %{_sysconfdir}/cups/certs
rm -f %{_localstatedir}/cache/cups/*.ipp %{_localstatedir}/cache/cups/*.cache

# Previous migration script unnecessarily put PageLogFormat into cups-files.conf
# (see bug #1148995)
FILE=%{_sysconfdir}/cups/cups-files.conf
for keyword in PageLogFormat; do
    sed -i -e "s,^$keyword,#$keyword,i" "$FILE" || :
done


exit 0

%post client
%if %{use_alternatives}
/@unixroot/usr/sbin/alternatives --install %{_bindir}/lpr print %{_bindir}/lpr.cups 40 \
	 --slave %{_bindir}/lp print-lp %{_bindir}/lp.cups \
	 --slave %{_bindir}/lpq print-lpq %{_bindir}/lpq.cups \
	 --slave %{_bindir}/lprm print-lprm %{_bindir}/lprm.cups \
	 --slave %{_bindir}/lpstat print-lpstat %{_bindir}/lpstat.cups \
	 --slave %{_bindir}/cancel print-cancel %{_bindir}/cancel.cups \
	 --slave %{_sbindir}/lpc print-lpc %{_sbindir}/lpc.cups \
	 --slave %{_mandir}/man1/cancel.1.gz print-cancelman %{_mandir}/man1/cancel-cups.1.gz \
	 --slave %{_mandir}/man1/lp.1.gz print-lpman %{_mandir}/man1/lp-cups.1.gz \
	 --slave %{_mandir}/man8/lpc.8.gz print-lpcman %{_mandir}/man8/lpc-cups.8.gz \
	 --slave %{_mandir}/man1/lpq.1.gz print-lpqman %{_mandir}/man1/lpq-cups.1.gz \
	 --slave %{_mandir}/man1/lpr.1.gz print-lprman %{_mandir}/man1/lpr-cups.1.gz \
	 --slave %{_mandir}/man1/lprm.1.gz print-lprmman %{_mandir}/man1/lprm-cups.1.gz \
	 --slave %{_mandir}/man1/lpstat.1.gz print-lpstatman %{_mandir}/man1/lpstat-cups.1.gz
%endif
exit 0

%post lpd
%if %{systemd}
%systemd_post cups-lpd.socket
%endif
exit 0

#ldconfig_scriptlets libs

%preun
%if %{systemd}
%systemd_preun %{name}.path %{name}.socket %{name}.service
%endif
exit 0

%preun client
%if %{use_alternatives}
if [ $1 -eq 0 ] ; then
	/@unixtool/usr/sbin/alternatives --remove print %{_bindir}/lpr.cups
fi
%endif
exit 0

%preun lpd
%if %{systemd}
%systemd_preun cups-lpd.socket
%endif
exit 0

%postun
%if %{systemd}
%systemd_postun_with_restart %{name}.path %{name}.socket %{name}.service
%endif
exit 0

%postun lpd
%if %{systemd}
%systemd_postun_with_restart cups-lpd.socket
%endif
exit 0


%files -f %{name}.lang
%doc README.md CREDITS.md CHANGES.md
%dir %attr(0755,root,lp) %{_sysconfdir}/cups
%dir %attr(0755,root,lp) %{_localstatedir}/run/cups
%dir %attr(0511,lp,sys) %{_localstatedir}/run/cups/certs
%if %{used_on_os2}
%{_tmpfilesdir}/cups.conf
%{_tmpfilesdir}/cups-lp.conf
%endif
%verify(not md5 size mtime) %config(noreplace) %attr(0640,root,lp) %{_sysconfdir}/cups/cupsd.conf
%attr(0640,root,lp) %{_sysconfdir}/cups/cupsd.conf.default
%verify(not md5 size mtime) %config(noreplace) %attr(0640,root,lp) %{_sysconfdir}/cups/cups-files.conf
%attr(0640,root,lp) %{_sysconfdir}/cups/cups-files.conf.default
%verify(not md5 size mtime) %config(noreplace) %attr(0644,root,lp) %{_sysconfdir}/cups/client.conf
%verify(not md5 size mtime) %config(noreplace) %attr(0600,root,lp) %{_sysconfdir}/cups/classes.conf
%verify(not md5 size mtime) %config(noreplace) %attr(0600,root,lp) %{_sysconfdir}/cups/printers.conf
%verify(not md5 size mtime) %config(noreplace) %attr(0644,root,lp) %{_sysconfdir}/cups/snmp.conf
%attr(0640,root,lp) %{_sysconfdir}/cups/snmp.conf.default
%verify(not md5 size mtime) %config(noreplace) %attr(0640,root,lp) %{_sysconfdir}/cups/subscriptions.conf
#%%{_sysconfdir}/cups/interfaces
%verify(not md5 size mtime) %config(noreplace) %attr(0644,root,lp) %{_sysconfdir}/cups/lpoptions
%dir %attr(0755,root,lp) %{_sysconfdir}/cups/ppd
%dir %attr(0700,root,lp) %{_sysconfdir}/cups/ssl
%if %{used_on_os2}
%config(noreplace) %{_sysconfdir}/pam.d/cups
%config(noreplace) %{_sysconfdir}/logrotate.d/cups
%endif
%dir %{_datadir}/%{name}/www
%dir %{_datadir}/%{name}/www/de
%dir %{_datadir}/%{name}/www/es
%dir %{_datadir}/%{name}/www/ja
%dir %{_datadir}/%{name}/www/ru
%{_datadir}/%{name}/www/images
%{_datadir}/%{name}/www/*.css
# 1658673 - html files cannot be docs, because CUPS web ui will not have
# introduction page on Fedora Docker image (because rpms are installed
# without docs there because of space reasons)
%{_datadir}/%{name}/www/index.html
%{_datadir}/%{name}/www/help
%{_datadir}/%{name}/www/robots.txt
%{_datadir}/%{name}/www/de/index.html
%{_datadir}/%{name}/www/es/index.html
%{_datadir}/%{name}/www/ja/index.html
%{_datadir}/%{name}/www/ru/index.html
%{_datadir}/%{name}/www/pt_BR/index.html
%{_datadir}/%{name}/www/apple-touch-icon.png
%dir %{_datadir}/%{name}/usb
%{_datadir}/%{name}/usb/org.cups.usb-quirks
%if %{systemd}
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}.socket
%{_unitdir}/%{name}.path
%endif
%{_bindir}/cupstestppd.exe
%{_bindir}/cupstestdsc.exe
%{_bindir}/ppd*.exe
%{cups_serverbin}/backend/*
%exclude %{cups_serverbin}/backend/*.dbg
%{cups_serverbin}/cgi-bin
%exclude %{cups_serverbin}/cgi-bin/*.dbg
%dir %{cups_serverbin}/daemon
%{cups_serverbin}/daemon/cups-deviced.exe
%{cups_serverbin}/daemon/cups-driverd.exe
%{cups_serverbin}/daemon/cups-exec.exe
%{cups_serverbin}/notifier
%exclude %{cups_serverbin}/notifier/*.dbg
%{cups_serverbin}/filter
%exclude %{cups_serverbin}/filter/*.dbg
%{cups_serverbin}/monitor/*.exe
%{_mandir}/man[1578]/*
# client subpackage
%exclude %{_mandir}/man1/lp*.1.gz
%if %{use_alternatives}
%exclude %{_mandir}/man1/cancel-cups.1.gz
%exclude %{_mandir}/man8/lpc-cups.8.gz
%else
%exclude %{_mandir}/man1/cancel.1.gz
%exclude %{_mandir}/man8/lpc.8.gz
%endif
# devel subpackage
%exclude %{_mandir}/man1/cups-config.1.gz
# ipptool subpackage
%exclude %{_mandir}/man1/ipptool.1.gz
%exclude %{_mandir}/man5/ipptoolfile.5.gz
# lpd subpackage
%exclude %{_mandir}/man8/cups-lpd.8.gz
%{_sbindir}/*
%exclude %{_sbindir}/*.dbg
# client subpackage
%if %{use_alternatives}
%exclude %{_sbindir}/lpc.cups.exe
%else
%exclude %{_sbindir}/lpc.exe
%endif
%dir %{_datadir}/cups/templates
%dir %{_datadir}/cups/templates/de
%dir %{_datadir}/cups/templates/es
%dir %{_datadir}/cups/templates/ja
%dir %{_datadir}/cups/templates/ru
%dir %{_datadir}/cups/templates/pt_BR
%{_datadir}/cups/templates/*.tmpl
%{_datadir}/cups/templates/de/*.tmpl
%{_datadir}/cups/templates/fr/*.tmpl
%{_datadir}/cups/templates/es/*.tmpl
%{_datadir}/cups/templates/ja/*.tmpl
%{_datadir}/cups/templates/ru/*.tmpl
%{_datadir}/cups/templates/pt_BR/*.tmpl
%dir %attr(1770,root,lp) %{_localstatedir}/spool/cups/tmp
%dir %attr(0710,root,lp) %{_localstatedir}/spool/cups
%dir %attr(0755,lp,sys) %{_localstatedir}/log/cups
%if %{dbus}
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/cups.conf
%endif
%{_datadir}/cups/drv/sample.drv
%{_datadir}/cups/examples
%{_datadir}/cups/mime/mime.types
%{_datadir}/cups/mime/mime.convs
%{_datadir}/cups/ppdc/*.defs
%{_datadir}/cups/ppdc/*.h

%files client
%{_sbindir}/lpc.exe
%{_bindir}/cancel.exe
%{_bindir}/lp*.exe
%if %{use_alternatives}
%{_mandir}/man1/lp*.1.gz
%{_mandir}/man1/cancel-cups*.1.gz
%{_mandir}/man8/lpc-cups.8.gz
%else
%{_mandir}/man1/lp*.1.gz
%{_mandir}/man1/cancel*.1.gz
%{_mandir}/man8/lpc.8.gz
%endif

%files libs
%doc LICENSE.txt
%{_libdir}/*.dll

%files filesystem
%dir %{cups_serverbin}
%dir %{cups_serverbin}/backend
%dir %{cups_serverbin}/driver
%dir %{cups_serverbin}/filter
%dir %{_datadir}/cups
%dir %{_datadir}/cups/data
%dir %{_datadir}/cups/drv
%dir %{_datadir}/cups/mime
%dir %{_datadir}/cups/model
%dir %{_datadir}/cups/ppdc
%dir %{_datadir}/ppd

%files devel
%{_bindir}/cups-config
%{_libdir}/*.a
%{_includedir}/cups/*
%{_mandir}/man1/cups-config.1.gz
%{_rpmconfigdir}/macros.d/macros.cups

%files lpd
%if %{systemd}
%{_unitdir}/cups-lpd.socket
%{_unitdir}/cups-lpd@.service
%endif
%{cups_serverbin}/daemon/cups-lpd.exe
%{_datadir}/man/man8/cups-lpd.8.gz

%files ipptool
%if %{dnsds}
%{_bindir}/ippfind.exe
%endif
%{_bindir}/ipptool.exe
%dir %{_datadir}/cups/ipptool
%{_datadir}/cups/ipptool/*
%{_mandir}/man1/ipptool.1.gz
%{_mandir}/man5/ipptoolfile.5.gz

%changelog
* Fri Oct 25 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.2.12-1
- update to version 2.2.12
- reworked spec file heavily

* Mon Nov 27 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.1.3-10
- add ETC to the env, as otherwise tcpip32.dll doesn't find any dns names

* Tue Oct 03 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.1.3-9
- moved source to github
- fixed a regression of the below /socket/cups.sock change

* Tue Aug 22 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.1.3-8
- add bldlevel to the dll
- fix search for ppd in cups-driver
- change LIBS
- change /@unixroot/var/run/cups/cups.sock to /socket/cups.sock
- adjust spec to scm_ macros usage

* Thu May 12 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.1.3-7
- fix timestamps absence in the jobs part of the webinterface

* Wed May 11 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.1.3-6
- disable the use of poll completely (fixes printing of large pdf)

* Fri Apr 29 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.1.3-5
- fix version info in german index.html (upstream bug)
- workaround for the webinterface issues (select() hack)
- remove .exe in httpSeperateURI
- don't deliver readonly cupsd

* Tue Apr 19 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.1.3-4
- add req for cups-filters
- don't use posix_spawn

* Wed Mar 16 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.1.3-3
- ship a rpm macro for cups_serverbin
- removed dbg packages from sbin dir in normal installation

* Fri Mar 11 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.1.3-2
- removed dbg packages from normal installation
- added SystemGroups value
- fixed some pipe() problems

* Mon Mar 07 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.1.3-1
- updated to version 2.1.3

* Fri Mar 04 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.4.8-5
- fixed lpd
- added more socketpair vs pipe changes
- also compress and strip debug info from cgi files

* Tue Jan 26 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.4.8-4
- poppler-utils needs to be at least 0.38.0-2
- remove wrong req for cups-lpr
- install all .a files for the dll

* Mon Jan 11 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.4.8-3
- rebuild with latest libraries
- adjusted debug package creation to latest rpm macros
- add poppler-utils as a requirement

* Sun Feb 15 2015 yd <yd@os2power.com> 1.4.8-1 1.4.8-2
- rebuild for new libpng release.

* Thu Dec 18 2014 yd
- r944, initial unixroot build.
