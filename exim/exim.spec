# SA-Exim has long since been obsoleted by the proper built-in ACL support
# from exiscan. Disable it for FC6 unless people scream.
%if 0%{?fedora} < 6
%define buildsa 1
%endif
%define buildsa 0

# Build clamav subpackage for FC5 and above.
#%if 0%{?fedora} >= 5
%define buildclam 1
#%endif

Summary: The exim mail transfer agent
Name: exim
Version: 4.73
Release: 0.4%{?dist}
License: GPLv2+
Url: http://www.exim.org/
Group: System Environment/Daemons
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides: MTA smtpd smtpdaemon server(smtp)

#Requires(post): /sbin/chkconfig /sbin/service %{_sbindir}/alternatives
#Requires(preun): /sbin/chkconfig /sbin/service %{_sbindir}/alternatives
#Requires(pre): %{_sbindir}/groupadd, %{_sbindir}/useradd
%if 0%{?buildclam}
#BuildRequires: clamav-devel
%endif
Source: ftp://ftp.exim.org/pub/exim/exim4/exim-%{version}.tar.gz

Source1: exim-Makefile-OS2
Source2: exim-os.h-OS2
#Source2: exim.init
#Source3: exim.sysconfig
#Source4: exim.logrotate
#Source5: exim-tidydb.sh
#Source11: exim.pam
%if 0%{?buildsa}
#Source13: http://marc.merlins.org/linux/exim/files/sa-exim-4.2.tar.gz
%endif
Source20: exim-greylist.conf.inc
Source21: exim-mk-greylist-db.sql
Source22: exim-greylist-tidy.sh

Patch1: exim-os2.diff
Patch4: exim-rhl.patch
Patch6: exim-4.50-config.patch
#Patch8: exim-4.24-libdir.patch
#Patch12: exim-4.33-cyrus.patch
#Patch13: exim-4.43-pamconfig.patch
#Patch14: exim-4.50-spamdconf.patch
#Patch18: exim-4.71-dlopen-localscan.patch
#Patch19: exim-4.63-procmail.patch
#Patch20: exim-4.63-allow-filter.patch
Patch21: exim-4.63-localhost-is-local.patch
#Patch22: exim-4.66-greylist-conf.patch
#Patch23: exim-4.67-smarthost-config.patch
#Patch24: exim-4.71-dynlookup.patch
#Patch25: exim-4.69-dynlookup-config.patch
#Patch26: exim-4.69-strictaliasing.patch

#Requires: /etc/pki/tls/certs /etc/pki/tls/private
#Requires: /etc/aliases
#Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildRequires: db4-devel openssl-devel
#BuildRequires: openldap-devel pam-devel
%if 0%{?buildsa}
#BuildRequires: lynx
%endif
BuildRequires: pcre-devel sqlite-devel
#BuildRequires: tcp_wrappers-devel cyrus-sasl-devel
#BuildRequires: openldap-devel openssl-devel mysql-devel postgresql-devel
#BuildRequires: libXaw-devel libXmu-devel libXext-devel libX11-devel libSM-devel
#BuildRequires: libICE-devel libXpm-devel libXt-devel perl(ExtUtils::Embed)

%description 
Exim is a message transfer agent (MTA) developed at the University of
Cambridge for use on Unix systems connected to the Internet. It is
freely available under the terms of the GNU General Public Licence. In
style it is similar to Smail 3, but its facilities are more
general. There is a great deal of flexibility in the way mail can be
routed, and there are extensive facilities for checking incoming
mail. Exim can be installed in place of sendmail, although the
configuration of exim is quite different to that of sendmail.

%package mysql
Summary: MySQL lookup support for Exim
Group: System Environment/Daemons
Requires: exim = %{version}-%{release}

%description mysql
This package contains the MySQL lookup module for Exim

%package pgsql
Summary: PostgreSQL lookup support for Exim
Group: System Environment/Daemons
Requires: exim = %{version}-%{release}

%description pgsql
This package contains the PostgreSQL lookup module for Exim

%package mon
Summary: X11 monitor application for Exim
Group: Applications/System

%description mon
The Exim Monitor is an optional supplement to the Exim package. It
displays information about Exim's processing in an X window, and an
administrator can perform a number of control actions from the window
interface.

%package sa
Summary: Exim SpamAssassin at SMTP time - d/l plugin
Group: System Environment/Daemons
Requires: exim = %{version}-%{release}

%description sa
The exim-sa package is an old method for allowing SpamAssassin to be run on
incoming mail at SMTP time. It is deprecated in favour of the built-in ACL
support for content scanning.

%package clamav
Summary: Clam Antivirus scanner dæmon configuration for use with Exim
Group: System Environment/Daemons
Requires: clamav-server exim
Obsoletes: clamav-exim <= 0.86.2
#Requires(post): /sbin/chkconfig /sbin/service
#Requires(preun): /sbin/chkconfig /sbin/service

%description clamav
This package contains configuration files which invoke a copy of the
clamav dæmon for use with Exim. It can be activated by adding (or
uncommenting)

   av_scanner = clamd:%{_var}/run/clamd.exim/clamd.sock

in your exim.conf, and using the 'malware' condition in the DATA ACL,
as follows:

   deny message = This message contains malware ($malware_name)
      malware = *

For further details of Exim content scanning, see chapter 41 of the Exim
specification:
http://www.exim.org/exim-html-%{version}/doc/html/spec_html/ch41.html

%package greylist
Summary: Example configuration for greylisting using Exim
Group: System Environment/Daemons
Requires: sqlite exim %{_sysconfdir}/cron.daily

%description greylist
This package contains a simple example of how to do greylisting in Exim's
ACL configuration. It contains a cron job to remove old entries from the
greylisting database, and an ACL subroutine which needs to be included
from the main exim.conf file.

To enable greylisting, install this package and then uncomment the lines
in Exim's configuration /etc/exim.conf which enable it. You need to
uncomment at least two lines -- the '.include' directive which includes
the new ACL subroutine, and the line which invokes the new subroutine.

By default, this implementation only greylists mails which appears
'suspicious' in some way. During normal processing of the ACLs we collect
a list of 'offended' which it's committed, which may include having
SpamAssassin points, lacking a Message-ID: header, coming from a blacklisted
host, etc. There are examples of these in the default configuration file,
mostly commented out. These should be sufficient for you to you trigger
greylisting for whatever 'offences' you can dream of, or even to make 
greylisting unconditional.

%prep
%setup -q
%if 0%{?buildsa}
#%setup -q -T -D -a 13
%endif

%patch1 -p1 -b .os2~
%patch4 -p1 -b .rhl
#YD included into main diff: %patch6 -p1 -b .config
#%patch8 -p1 -b .libdir
#%patch12 -p1 -b .cyrus
#%patch13 -p1 -b .pam
#%patch14 -p1 -b .spamd
#%patch18 -p1 -b .dl
#%patch19 -p1 -b .procmail
#%patch20 -p1 -b .filter
%patch21 -p1 -b .localhost
#%patch22 -p1 -b .grey
#%patch23 -p1 -b .smarthost
#%patch24 -p1 -b .dynlookup
#%patch25 -p1 -b .dynconfig
#%patch26 -p1 -b .strictaliasing

cp %{SOURCE1} OS/Makefile-OS2
cp %{SOURCE2} OS/os.h-OS2

cp src/EDITME Local/Makefile
sed -i 's!^# LOOKUP_MODULE_DIR=.*!LOOKUP_MODULE_DIR=%{_libdir}/exim/%{version}-%{release}/lookups!' Local/Makefile
#sed -i 's!^# AUTH_LIBS=-lsasl2!AUTH_LIBS=-lsasl2!' Local/Makefile
sed -i 's!^EXIM_USER=.*!EXIM_USER=root!' Local/Makefile
cp exim_monitor/EDITME Local/eximon.conf


%build

export CONFIG_SHELL="/@unixroot/usr/bin/sh.exe"
export MAKESHELL="/@unixroot/usr/bin/sh.exe"
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp" 
export  LFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp" 
export CFLAGS="$RPM_OPT_FLAGS -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE"

%ifnarch s390 s390x sparc sparcv9 sparcv9v sparc64 sparc64v
	export PIE=-fpie
%else
	export PIE=-fPIE
%endif
make _lib=%{_lib} SHELL="/@unixroot/usr/bin/sh.exe" FULLECHO=

%if 0%{?buildsa}
# build sa-exim
cd sa-exim*
perl -pi -e 's|\@lynx|HOME=/ /usr/bin/lynx|g;' Makefile
make SACONF=%{_sysconfdir}/exim/sa-exim.conf CFLAGS="$RPM_OPT_FLAGS -fPIC"
%endif

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_sbindir}
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pam.d
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/exim

cd build-`scripts/os-type`-`scripts/arch-type`
install -m 4775 exim.exe $RPM_BUILD_ROOT%{_sbindir}

# eximon eximon.bin
for i in exim_dumpdb.exe exim_fixdb.exe exim_tidydb.exe \
	exinext exiwhat exim_dbmbuild.exe exicyclog exim_lock.exe \
	exigrep eximstats exipick exiqgrep exiqsumm \
	exim_checkaccess convert4r4
do
	install -m 0755 $i $RPM_BUILD_ROOT%{_sbindir}
done

mkdir -p $RPM_BUILD_ROOT%{_libdir}/exim/%{version}-%{release}/lookups
#for i in mysql.so pgsql.so
#do 
#	install -m755 lookups/$i \
#	 $RPM_BUILD_ROOT%{_libdir}/exim/%{version}-%{release}/lookups
#done

cd ..

install -m 0644 src/configure.default $RPM_BUILD_ROOT%{_sysconfdir}/exim/exim.conf
#install -m 0644 %SOURCE11 $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/exim

mkdir -p $RPM_BUILD_ROOT/usr/lib
#pushd $RPM_BUILD_ROOT/usr/lib
#ln -sf ../sbin/exim sendmail.exim
#popd

#pushd $RPM_BUILD_ROOT%{_sbindir}/
#ln -sf exim sendmail.exim
#popd

#pushd $RPM_BUILD_ROOT%{_bindir}/
#ln -sf ../sbin/exim mailq.exim
#ln -sf ../sbin/exim runq.exim
#ln -sf ../sbin/exim rsmtp.exim
#ln -sf ../sbin/exim rmail.exim
#ln -sf ../sbin/exim newaliases.exim
#popd

install -d -m 0750 $RPM_BUILD_ROOT%{_var}/spool/exim
install -d -m 0750 $RPM_BUILD_ROOT%{_var}/spool/exim/db
install -d -m 0750 $RPM_BUILD_ROOT%{_var}/spool/exim/input
install -d -m 0750 $RPM_BUILD_ROOT%{_var}/spool/exim/msglog
install -d -m 0750 $RPM_BUILD_ROOT%{_var}/log/exim

mkdir -p $RPM_BUILD_ROOT%{_mandir}/man8
install -m644 doc/exim.8 $RPM_BUILD_ROOT%{_mandir}/man8/exim.8
pod2man --center=EXIM --section=8 \
	$RPM_BUILD_ROOT%{_sbindir}/eximstats > \
	$RPM_BUILD_ROOT%{_mandir}/man8/eximstats.8

#mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
#install -m 644 %SOURCE3 $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/exim

#mkdir -p $RPM_BUILD_ROOT%{_initrddir}
#install %SOURCE2 $RPM_BUILD_ROOT%{_initrddir}/exim

#mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
#install -m 0644 %SOURCE4 $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/exim

#mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/cron.daily
#install -m 0755 %SOURCE5 $RPM_BUILD_ROOT%{_sysconfdir}/cron.daily/exim-tidydb

%if 0%{?buildsa}
# install sa
cd sa-exim*
mkdir -p $RPM_BUILD_ROOT%{_libexecdir}/exim
install *.so  $RPM_BUILD_ROOT%{_libexecdir}/exim
install -m 644 *.conf $RPM_BUILD_ROOT%{_sysconfdir}/exim
ln -s sa-exim*.so $RPM_BUILD_ROOT%{_libexecdir}/exim/sa-exim.so
%endif

# generate ghost .pem file
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/certs
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/private
touch $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/certs/exim.pem
touch $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/private/exim.pem
chmod 600 $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/certs/exim.pem
chmod 600 $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/private/exim.pem

# generate alternatives ghosts
#mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
#for i in %{_sbindir}/sendmail %{_bindir}/{mailq,runq,rsmtp,rmail,newaliases} \
#	/usr/lib/sendmail %{_sysconfdir}/pam.d/smtp %{_mandir}/man1/mailq.1.gz
#do
#	touch $RPM_BUILD_ROOT$i
#done

%if 0%{?buildclam}
# Munge the clamav init and config files from clamav-devel. This really ought
# to be a subpackage of clamav, but this hack will have to do for now.
%define clamsubst(n1:n2:n3:n3:n5) sed -e "s!<SERVICE>!%3!g;s!<USER>!%4!g;%5" %{_datadir}/clamav/template/%1 > $RPM_BUILD_ROOT%2


mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/clamd.d
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig

#%clamsubst clamd.conf %{_sysconfdir}/clamd.d/exim.conf exim exim \
#       s!^##*\(\(LogFile\|LocalSocket\|PidFile\|User\)\s\|\(StreamSaveToDisk\|ScanMail\|LogTime\|ScanArchive\)$\)!\1!;s!^Example!#Example!;
#
#%clamsubst clamd.init %{_initrddir}/clamd.exim exim exim
#%clamsubst clamd.logrotate %{_sysconfdir}/logrotate.d/clamd.exim exim exim


cat <<EOF > $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/clamd.exim
CLAMD_CONFIG='%_sysconfdir/clamd.d/exim.conf'
CLAMD_SOCKET=%{_var}/run/clamd.exim/clamd.sock
EOF
#ln -sf clamd $RPM_BUILD_ROOT/usr/sbin/clamd.exim

mkdir -p $RPM_BUILD_ROOT%{_var}/run/clamd.exim
mkdir -p $RPM_BUILD_ROOT%{_var}/log
touch $RPM_BUILD_ROOT%{_var}/log/clamd.exim

%endif

# Set up the greylist subpackage
install -m644 %{SOURCE20} $RPM_BUILD_ROOT/%_sysconfdir/exim/exim-greylist.conf.inc
install -m644 %{SOURCE21} $RPM_BUILD_ROOT/%_sysconfdir/exim/mk-greylist-db.sql
mkdir -p $RPM_BUILD_ROOT/%_sysconfdir/cron.daily
install -m755 %{SOURCE22} $RPM_BUILD_ROOT/%_sysconfdir/cron.daily/greylist-tidy.sh
touch $RPM_BUILD_ROOT/%_var/spool/exim/db/greylist.db

%clean
rm -rf $RPM_BUILD_ROOT

#%pre
#%{_sbindir}/groupadd -g 93 exim 2>/dev/null
#%{_sbindir}/useradd -d %{_var}/spool/exim -s /sbin/nologin -G mail -M -r -u 93 -g exim exim 2>/dev/null
## Copy TLS certs from old location to new -- don't move them, because the
## config file may be modified and may be pointing to the old location.
#if [ ! -f /etc/pki/tls/certs/exim.pem -a -f %{_datadir}/ssl/certs/exim.pem ] ; then
#   cp %{_datadir}/ssl/certs/exim.pem /etc/pki/tls/certs/exim.pem
#   cp %{_datadir}/ssl/private/exim.pem /etc/pki/tls/private/exim.pem
#fi
#exit 0

#%post
#/sbin/chkconfig --add exim
#%{_sbindir}/alternatives --install %{_sbindir}/sendmail mta %{_sbindir}/sendmail.exim 10 \
#	--slave %{_bindir}/mailq mta-mailq %{_bindir}/mailq.exim \
#	--slave %{_bindir}/runq mta-runq %{_bindir}/runq.exim \
#	--slave %{_bindir}/rsmtp mta-rsmtp %{_bindir}/rsmtp.exim \
#	--slave %{_bindir}/rmail mta-rmail %{_bindir}/rmail.exim \
#	--slave /etc/pam.d/smtp mta-pam /etc/pam.d/exim \
#	--slave %{_bindir}/newaliases mta-newaliases %{_bindir}/newaliases.exim \
#	--slave /usr/lib/sendmail mta-sendmail /usr/lib/sendmail.exim \
#	--slave %{_mandir}/man1/mailq.1.gz mta-mailqman %{_mandir}/man8/exim.8.gz \
#	--initscript exim

#%preun
#if [ $1 = 0 ]; then
#	/sbin/service exim stop > /dev/null 2>&1
#	/sbin/chkconfig --del exim
#	%{_sbindir}/alternatives --remove mta %{_sbindir}/sendmail.exim
#fi

#%postun
#if [ "$1" -ge "1" ]; then
#	/sbin/service exim  condrestart > /dev/null 2>&1
#	mta=`readlink /etc/alternatives/mta`
#	if [ "$mta" == "%{_sbindir}/sendmail.exim" ]; then
#		/usr/sbin/alternatives --set mta %{_sbindir}/sendmail.exim
#	fi
#fi

#%post greylist
#if [ ! -r %{_var}/spool/exim/db/greylist.db ]; then
#   sqlite3 %{_var}/spool/exim/db/greylist.db < %{_sysconfdir}/exim/mk-greylist-db.sql
#   chown exim.exim %{_var}/spool/exim/db/greylist.db
#   chmod 0660 %{_var}/spool/exim/db/greylist.db
#fi

%post
%wps_object_create_begin
EXIM4_FOLDER:WPFolder|Exim %version|<WP_DESKTOP>|TITLE=Exim %version;
EXIM4_EXIMD:WPProgram|Exim daemon|<EXIM4_FOLDER>|EXENAME=((%_sbindir/exim.exe));STARTUPDIR=((%_sbindir));PARAMETERS=-bd -q5m;TITLE=Exim4 daemon;
EXIM4_EXIM_CONF:WPShadow|exim.conf|<EXIM4_FOLDER>|SHADOWID=((%_sysconfdir/exim/exim.conf))
%wps_object_create_end

%postun
%wps_object_delete_all

%files
%defattr(-,root,root)
%attr(4755,root,root) %{_sbindir}/exim.exe
%{_sbindir}/exim_dumpdb.exe
%{_sbindir}/exim_fixdb.exe
%{_sbindir}/exim_tidydb.exe
%{_sbindir}/exinext
%{_sbindir}/exiwhat
%{_sbindir}/exim_dbmbuild.exe
%{_sbindir}/exicyclog
%{_sbindir}/exigrep
%{_sbindir}/eximstats
%{_sbindir}/exipick
%{_sbindir}/exiqgrep
%{_sbindir}/exiqsumm
%{_sbindir}/exim_lock.exe
%{_sbindir}/exim_checkaccess
%{_sbindir}/convert4r4
#%{_sbindir}/sendmail.exim
#%{_bindir}/mailq.exim
#%{_bindir}/runq.exim
#%{_bindir}/rsmtp.exim
#%{_bindir}/rmail.exim
#%{_bindir}/newaliases.exim
#/usr/lib/sendmail.exim
%{_mandir}/*/*
%dir %{_libdir}/exim
%dir %{_libdir}/exim/%{version}-%{release}
%dir %{_libdir}/exim/%{version}-%{release}/lookups

%defattr(-,exim,exim)
%dir %{_var}/spool/exim
%dir %{_var}/spool/exim/db
%dir %{_var}/spool/exim/input
%dir %{_var}/spool/exim/msglog
%dir %{_var}/log/exim

%defattr(-,root,mail)
%dir %{_sysconfdir}/exim
%config(noreplace) %{_sysconfdir}/exim/exim.conf

%defattr(-,root,root)
#%config(noreplace) %{_sysconfdir}/sysconfig/exim
#%{_sysconfdir}/rc.d/init.d/exim
#%config(noreplace) %{_sysconfdir}/logrotate.d/exim
#%config(noreplace) %{_sysconfdir}/pam.d/exim
#%{_sysconfdir}/cron.daily/exim-tidydb

%doc ACKNOWLEDGMENTS LICENCE NOTICE README.UPDATING README 
%doc doc util/unknownuser.sh

%attr(0600,root,root) %ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{_sysconfdir}/pki/tls/certs/exim.pem
%attr(0600,root,root) %ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{_sysconfdir}/pki/tls/private/exim.pem

%attr(0755,root,root) %ghost %{_sbindir}/sendmail
%attr(0755,root,root) %ghost %{_bindir}/mailq
%attr(0755,root,root) %ghost %{_bindir}/runq
%attr(0755,root,root) %ghost %{_bindir}/rsmtp
%attr(0755,root,root) %ghost %{_bindir}/rmail
%attr(0755,root,root) %ghost %{_bindir}/newaliases
%attr(0755,root,root) %ghost /usr/lib/sendmail
#%ghost %{_sysconfdir}/pam.d/smtp
#%ghost %{_mandir}/man1/mailq.1.gz

#%files mysql
#%defattr(-,root,root,-)
#%{_libdir}/exim/%{version}-%{release}/lookups/mysql.so

#%files pgsql
#%defattr(-,root,root,-)
#%{_libdir}/exim/%{version}-%{release}/lookups/pgsql.so

#%files mon
#%defattr(-,root,root)
#%{_sbindir}/eximon
#%{_sbindir}/eximon.bin

%if 0%{?buildsa}
%files sa
%defattr(-,root,root)
%{_libexecdir}/exim
%config(noreplace) %{_sysconfdir}/exim/sa-*.conf
%doc sa-exim*/*.html
%doc sa-exim*/{ACKNOWLEDGEMENTS,INSTALL,LICENSE,TODO}
%endif

%if 0%{?buildclam}
#%post clamav
#/bin/touch %{_var}/log/clamd.exim
#/bin/chown exim.exim %{_var}/log/clamd.exim
#/sbin/chkconfig --add clamd.exim

#%preun clamav
#test "$1" != 0 || %{_initrddir}/clamd.exim stop &>/dev/null || :
#test "$1" != 0 || /sbin/chkconfig --del clamd.exim

#%postun clamav
#test "$1"  = 0 || %{_initrddir}/clamd.exim condrestart >/dev/null || :

%files clamav
%defattr(-,root,root,-)
#%{_sbindir}/clamd.exim
#%attr(0755,root,root) %config %{_initrddir}/clamd.exim
#%config(noreplace) %verify(not mtime) %{_sysconfdir}/clamd.d/exim.conf
%config(noreplace) %verify(not mtime) %{_sysconfdir}/sysconfig/clamd.exim
#%config(noreplace) %verify(not mtime) %{_sysconfdir}/logrotate.d/clamd.exim
%attr(0750,exim,exim) %dir %{_var}/run/clamd.exim
%ghost %attr(0644,exim,exim) %{_var}/log/clamd.exim
%endif

%files greylist
%defattr(-,root,root,-)
%config %{_sysconfdir}/exim/exim-greylist.conf.inc
%ghost %{_var}/spool/exim/db/greylist.db
%{_sysconfdir}/exim/mk-greylist-db.sql
%{_sysconfdir}/cron.daily/greylist-tidy.sh

%changelog

