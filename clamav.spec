#define svn_url     F:/rd/ports/clamav/trunk
%define svn_url     http://svn.netlabs.org/repos/ports/clamav/trunk
%define svn_rev     1841

Summary:	End-user tools for the Clam Antivirus scanner
Name:		clamav
Version:	0.99.2
Release:        1%{?dist}

License:	proprietary
Group:		Applications/File
URL:		http://www.clamav.net

Source:		%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip

BuildRoot:	%_tmppath/%name-%version-%release-root

Requires:	clamav-lib = %version-%release
#Requires:	data(clamav)

BuildRequires:	curl-devel
BuildRequires:	zlib-devel bzip2-devel
BuildRequires:	ncurses-devel
BuildRequires:	json-c-devel pcre-devel openssl-devel libxml2-devel
BuildRequires:	libtool libtool-ltdl-devel
#BuildRequires:	bc

%package lib
Summary:	Dynamic libraries for the Clam Antivirus scanner
Group:		System Environment/Libraries
#Requires:	data(clamav)

%package devel
Summary:	Header files and libraries for the Clam Antivirus scanner
Group:		Development/Libraries
Requires:	clamav-lib        = %version-%release
#Requires:	clamav-filesystem = %version-%release

%package data
Summary:	Virus signature data for the Clam Antivirus scanner
Group:		Applications/File
#Requires(pre):		clamav-filesystem = %version-%release
#Requires(postun):	clamav-filesystem = %version-%release
Provides:		data(clamav) = full
Conflicts:		data(clamav) < full
Conflicts:		data(clamav) > full
%{?noarch}

%package update
Summary:	Auto-updater for the Clam Antivirus scanner data-files
Group:		Applications/File
#Source200:	freshclam-sleep
#Source201:	freshclam.sysconfig
#Source202:	clamav-update.cron
#Requires:		clamav-filesystem = %version-%release
#Requires(pre):		/etc/cron.d
#Requires(postun):	/etc/cron.d
#Requires(post):		%__chown %__chmod
#Requires(post):		group(%username)

%package server
Summary:	Clam Antivirus scanner server
Group:		System Environment/Daemons
Requires:	data(clamav)
#Requires:	clamav-filesystem = %version-%release
Requires:	clamav-lib        = %version-%release

%package server-sysvinit
Summary:	SysV initscripts for clamav server
Group:		System Environment/Daemons
Provides:	init(clamav-server) = sysv
Requires:	clamav-server = %version-%release
#Requires(pre):		%_initrddir
#Requires(postun):	%_initrddir
Provides:	clamav-server-sysv = %version-%release
Obsoletes:	clamav-server-sysv < %version-%release
%{?noarch}


%package scanner
Summary:	Clamav scanner daemon
Group:		System Environment/Daemons
Requires:	init(clamav-scanner)
Provides:	user(%scanuser)  = 49
Provides:	group(%scanuser) = 49
Requires:	clamav-server = %version-%release
%{?noarch}

%package scanner-sysvinit
Summary:	SysV initscripts for clamav scanner daemon
Group:		System Environment/Daemons
Provides:	init(clamav-scanner) = sysv
Requires:	clamav-server-sysvinit = %version-%release
Requires:	clamav-scanner = %version-%release
#Requires(pre):		%_initrddir
#Requires(postun):	%_initrddir initscripts
#Requires(post):		chkconfig
#Requires(preun):	chkconfig initscripts
%{?noarch}

#%package scanner-upstart
#Summary:	Upstart initscripts for clamav scanner daemon
#Group:		System Environment/Daemons
#Source410:	clamd.scan.upstart
#Provides:	init(clamav-scanner) = upstart
#Requires:	clamav-scanner = %version-%release
#Requires(pre):		/etc/init
#Requires(post):		/usr/bin/killall
#Requires(postun):	/sbin/initctl
#%{?noarch}


%description
Clam AntiVirus is an anti-virus toolkit for UNIX. The main purpose of this
software is the integration with mail servers (attachment scanning). The
package provides a flexible and scalable multi-threaded daemon, a command
line scanner, and a tool for automatic updating via Internet. The programs
are based on a shared library distributed with the Clam AntiVirus package,
which you can use with your own software. The virus database is based on
the virus database from OpenAntiVirus, but contains additional signatures
(including signatures for popular polymorphic viruses, too) and is KEPT UP
TO DATE.

%description lib
This package contains dynamic libraries shared between applications
using the Clam Antivirus scanner.

%description devel
This package contains headerfiles and libraries which are needed to
build applications using clamav.


%description data
This is an empty package to fulfill inter-package dependencies of the
clamav suite. 


%description update
This package contains programs which can be used to update the clamav
anti-virus database automatically. It uses the freshclam(1) utility for
this task. To activate it, uncomment the entry in /etc/cron.d/clamav-update.

%description server
ATTENTION: most users do not need this package; the main package has
everything (or depends on it) which is needed to scan for virii on
workstations.

This package contains files which are needed to execute the clamd-daemon.
This daemon does not provide a system-wide service. Instead of, an instance
of this daemon should be started for each service requiring it.

See the README file how this can be done with a minimum of effort.


%description server-sysvinit
SysV initscripts template for the clamav server


%description scanner
This package contains a generic system wide clamd service which is
e.g. used by the clamav-milter package.

%description scanner-sysvinit
The SysV initscripts for clamav-scanner.


%debug_package


## ------------------------------------------------------------

%prep
%if %{?svn_rev:%(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')}%{!?svn_rev):0}
%setup -q
%else
%setup -n "%{name}-%{version}" -Tc
svn export %{?svn_rev:-r %{svn_rev}} %{svn_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip" "%{name}-%{version}")
%endif

sed -i -e 's!_VERSION_!%version!g;' \
    -e 's!_BUILD_!%release!g;' \
    ReadMe.txt

#sed -ri \
#    -e 's!^#?(LogFile ).*!#\1/var/log/clamd.<SERVICE>!g' \
#    -e 's!^#?(LocalSocket ).*!#\1/var/run/clamd.<SERVICE>/clamd.sock!g' \
#    -e 's!^(#?PidFile ).*!\1/var/run/clamd.<SERVICE>/clamd.pid!g' \
#    -e 's!^#?(User ).*!\1<USER>!g' \
#    -e 's!^#?(AllowSupplementaryGroups|LogSyslog).*!\1 yes!g' \
#    -e 's! /usr/local/share/clamav,! %homedir,!g' \
#    etc/clamd.conf

#sed -ri \
#    -e 's!^#?(UpdateLogFile )!#\1!g;' \
#    -e 's!^#?(LogSyslog).*!\1 yes!g' \
#    -e 's!(DatabaseOwner *)clamav$!\1%username!g' etc/freshclam.conf


## ------------------------------------------------------------

%build
export CFLAGS="$RPM_OPT_FLAGS -Wall -W -Wmissing-prototypes -Wmissing-declarations"
export LDFLAGS="-Zomf -Zmap -Zbin-files -Zhigh-mem -Zargs-wild -Zargs-resp"
export LIBS="-lurpo -lcx0 -lpthread"
# YD this is required for make llvm configure to work...
export PATH_SEPARATOR=";"

autoreconf -fvi

%configure \
    --disable-milter \
    --disable-rpath \
    --with-dbdir=/@unixroot/var/lib/clamav \
    --with-xml=/@unixroot/usr \
    --with-openssl=/@unixroot/usr \
    --with-libcurl=/@unixroot/usr \
    --with-zlib=/@unixroot/usr \
    --with-libjson=/@unixroot/usr \
    --enable-languages=c --disable-ltdl-install --disable-fdpassing \
    --disable-clamav \
    --disable-check \
    --disable-llvm \
    --enable-shared --disable-static

# TODO: check periodically that CLAMAVUSER is used for freshclam only

make %{?_smp_mflags}


## ------------------------------------------------------------

%install
rm -rf "$RPM_BUILD_ROOT" _doc*
make DESTDIR="$RPM_BUILD_ROOT" install

#cp libclamav/clamav.dll $RPM_BUILD_ROOT%{_libdir}
cp clamd/clamd.ico $RPM_BUILD_ROOT%{_sbindir}

#LogFile must be readable to submit stats
sed -i 's!#LogFileUnlock yes!LogFileUnlock yes!g;' \
    $RPM_BUILD_ROOT%{_sysconfdir}/clamd.conf.sample


rm $RPM_BUILD_ROOT%{_mandir}/man8/clamav-milter.8

#install -d -m755 \
#	${RPM_BUILD_ROOT}%_sysconfdir/{mail,clamd.d,cron.d,logrotate.d,sysconfig,init} \
#	${RPM_BUILD_ROOT}%_var/log \
#	${RPM_BUILD_ROOT}%milterstatedir \
#	${RPM_BUILD_ROOT}%pkgdatadir/template \
#	${RPM_BUILD_ROOT}%_initrddir \
#	${RPM_BUILD_ROOT}%homedir \
#	${RPM_BUILD_ROOT}%scanstatedir

#rm -f	${RPM_BUILD_ROOT}%_sysconfdir/clamd.conf \
#	${RPM_BUILD_ROOT}%_libdir/*.la

rm -f	${RPM_BUILD_ROOT}%_libdir/*.la
rm -f	${RPM_BUILD_ROOT}%_libdir/clamunrar*

mkdir -p $RPM_BUILD_ROOT%{_var}/lib/clamav
touch $RPM_BUILD_ROOT%{_var}/lib/clamav/daily.cld
touch $RPM_BUILD_ROOT%{_var}/lib/clamav/daily.cvd
touch $RPM_BUILD_ROOT%{_var}/lib/clamav/main.cld
touch $RPM_BUILD_ROOT%{_var}/lib/clamav/main.cvd
touch $RPM_BUILD_ROOT%{_var}/lib/clamav/bytecode.cld
touch $RPM_BUILD_ROOT%{_var}/lib/clamav/bytecode.cvd
touch $RPM_BUILD_ROOT%{_var}/lib/clamav/mirrors.dat


## prepare the server-files
#mkdir _doc_server
#install -m644 -p %SOURCE2	_doc_server/clamd.sysconfig
#install -m644 -p %SOURCE3       _doc_server/clamd.logrotate
#install -m755 -p %SOURCE7	_doc_server/clamd.init
#install -m644 -p %SOURCE5	_doc_server/README
#install -m644 -p etc/clamd.conf _doc_server/clamd.conf

#install -m644 -p %SOURCE1	$RPM_BUILD_ROOT%pkgdatadir
#install -m755 -p %SOURCE100     $RPM_BUILD_ROOT%pkgdatadir
#cp -pa _doc_server/*            $RPM_BUILD_ROOT%pkgdatadir/template
#ln -s %pkgdatadir/clamd-wrapper $RPM_BUILD_ROOT%_initrddir/clamd-wrapper

#smartsubst 's!/usr/share/clamav!%pkgdatadir!g' $RPM_BUILD_ROOT%pkgdatadir/clamd-wrapper


## prepare the update-files
#install -m644 -p %SOURCE6	${RPM_BUILD_ROOT}%_sysconfdir/logrotate.d/clamav-update
#install -m755 -p %SOURCE8	${RPM_BUILD_ROOT}%_sbindir/clamav-notify-servers
#touch ${RPM_BUILD_ROOT}%freshclamlog

#install -p -m0755 %SOURCE200	$RPM_BUILD_ROOT%pkgdatadir/freshclam-sleep
#install -p -m0644 %SOURCE201	$RPM_BUILD_ROOT%_sysconfdir/sysconfig/freshclam
#install -p -m0600 %SOURCE202	$RPM_BUILD_ROOT%_sysconfdir/cron.d/clamav-update

#smartsubst 's!webmaster,clamav!webmaster,%username!g;
#	    s!/usr/share/clamav!%pkgdatadir!g;
#	    s!/usr/bin!%_bindir!g;
#            s!/usr/sbin!%_sbindir!g;' \
#   $RPM_BUILD_ROOT%_sysconfdir/cron.d/clamav-update \
#   $RPM_BUILD_ROOT%pkgdatadir/freshclam-sleep


### The scanner stuff
#sed -e 's!<SERVICE>!scan!g;s!<USER>!%scanuser!g' \
#    etc/clamd.conf > $RPM_BUILD_ROOT%_sysconfdir/clamd.d/scan.conf

#sed -e 's!<SERVICE>!scan!g;' $RPM_BUILD_ROOT%pkgdatadir/template/clamd.init \
#    > $RPM_BUILD_ROOT%_initrddir/clamd.scan

#install -p -m 644 %SOURCE410 $RPM_BUILD_ROOT%_sysconfdir/init/clamd.scan.conf

#touch $RPM_BUILD_ROOT%scanstatedir/clamd.sock


%{!?with_upstart:rm -rf $RPM_BUILD_ROOT%_sysconfdir/init}

## ------------------------------------------------------------

%clean
rm -rf "$RPM_BUILD_ROOT"

%post
%wps_object_create_begin
CLAMAV_README:WPShadow|Readme 1st|<CLAMAV_FOLDER>|SHADOWID=((%_defaultdocdir/%name-%version/ReadMe.txt))
%wps_object_create_end

%postun
%wps_object_delete_all

# -lib is installed first/uninstalled last, create folder here
%post lib
%wps_object_create_begin -n %{name}-lib
CLAMAV_FOLDER:WPFolder|ClamAV %version|<WP_DESKTOP>|TITLE=ClamAV %version;
%wps_object_create_end

%postun lib
%wps_object_delete_all -n %{name}-lib

%post server
%wps_object_create_begin -n %{name}-server
CLAMAV_CLAMD:WPProgram|ClamAV daemon|<CLAMAV_FOLDER>|EXENAME=((%_sbindir/clamd.exe));STARTUPDIR=((%_sbindir));ICONFILE=((%_sbindir/clamd.ico));TITLE=ClamAV daemon;
CLAMAV_CLAMD_CONF:WPShadow|clamd.conf|<CLAMAV_FOLDER>|SHADOWID=((%_sysconfdir/clamd.conf))
%wps_object_create_end

%postun server
%wps_object_delete_all -n %{name}-server

%post update
%wps_object_create_begin -n %{name}-update
CLAMAV_FRESHCLAM:WPProgram|Freshclam|<CLAMAV_FOLDER>|EXENAME=((%_bindir/freshclam.exe));STARTUPDIR=((%_bindir));TITLE=Freshclam;NOAUTOCLOSE=YES;
CLAMAV_FRESHCLAM_CONF:WPShadow|freshclam.conf|<CLAMAV_FOLDER>|SHADOWID=((%_sysconfdir/freshclam.conf))
%wps_object_create_end

%postun update
%wps_object_delete_all -n %{name}-update

## ------------------------------------------------------------

%files
%defattr(-,root,root,-)
%doc AUTHORS BUGS COPYING ChangeLog FAQ NEWS README UPGRADE
%doc ReadMe.txt
%doc docs/*.pdf
%_bindir/*.exe
%_mandir/man[15]/*
%exclude %_bindir/clamav-config
%exclude %_bindir/freshclam.exe
%exclude %_mandir/*/freshclam*

## -----------------------

%files lib
%defattr(-,root,root,-)
%_libdir/*.dll

## -----------------------

%files devel
%defattr(-,root,root,-)
%_includedir/*
%_libdir/*.a
#%pkgdatadir/template
#%pkgdatadir/clamd-gen
%_libdir/pkgconfig/*
%_bindir/clamav-config

## -----------------------

%files data
%defattr(-,%username,%username,-)
%ghost %attr(0664,%username,%username) %{_var}/lib/clamav/*.cvd
%ghost %attr(0664,%username,%username) %{_var}/lib/clamav/*.cld
%ghost %attr(0664,%username,%username) %{_var}/lib/clamav/*.dat


## -----------------------

%files update
%defattr(-,root,root,-)
%_bindir/freshclam.exe
%_mandir/*/freshclam*
#%pkgdatadir/freshclam-sleep
%config(noreplace) %verify(not mtime)    %_sysconfdir/freshclam.conf.sample
#%config(noreplace) %verify(not mtime)    %_sysconfdir/logrotate.d/*
#%config(noreplace) %_sysconfdir/cron.d/*
#%config(noreplace) %_sysconfdir/sysconfig/freshclam

#%ghost %attr(0664,root,%username) %verify(not size md5 mtime) %freshclamlog
%ghost %attr(0664,%username,%username) %{_var}/lib/clamav/*.cld
%ghost %attr(0664,%username,%username) %{_var}/lib/clamav/*.cvd
%ghost %attr(0664,%username,%username) %{_var}/lib/clamav/*.dat


## -----------------------

%files server
%defattr(-,root,root,-)
#%doc _doc_server/*
%_mandir/man[58]/clamd*
%_sbindir/*.exe
%_sbindir/*.ico
#%pkgdatadir/clamd-wrapper
#%dir %_sysconfdir/clamd.d
%config(noreplace) %verify(not mtime)    %_sysconfdir/clamd.conf.sample


%files server-sysvinit
%defattr(-,root,root,-)
#%_initrddir/clamd-wrapper


## -----------------------

%files scanner
%defattr(-,root,root,-)
#%dir %attr(0710,%scanuser,%scanuser) %scanstatedir
#%config(noreplace) %_sysconfdir/clamd.d/scan.conf
#%ghost %scanstatedir/clamd.sock

%files scanner-sysvinit
#%attr(0755,root,root) %config %_initrddir/clamd.scan

%if 0%{?with_upstart:1}
%files scanner-upstart
%defattr(-,root,root,-)
%config(noreplace) %_sysconfdir/init/clamd.scan*
%endif

%changelog
* Mon Nov 28 2016 yd <yd@os2power.com> 0.99.2-1
- use libcx0 mmap code, new libtool generation.
- r1834, update of source code to 0.99.21.

* Thu Feb 05 2015 yd <yd@os2power.com> 0.98.6-6
- r1001, update of source code to 0.98.6.

* Thu Nov 24 2011 yd
- fixed missing mmap check in build
