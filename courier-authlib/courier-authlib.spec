
Name:           courier-authlib
Summary:        Courier authentication library
Version:        0.63.0
Release:        0%{?dist}
License:        GPLv2+
Group:          Productivity/Networking/Email/Servers
Url:            http://www.courier-mta.org/imap/
Source:         %{name}-%{version}.tar.bz2
#Source1:        courier-authdaemon.init
#Source2:        rpmlintrc
Patch1:         courier-authlib.diff

BuildRoot:      %{_tmppath}/%{name}-%{version}-build
#PreReq:         coreutils
#BuildRequires:  expect gcc-c++ gdbm-devel
#BuildRequires:  mysql-devel
#BuildRequires:  openldap2-devel pam-devel postgresql-devel
#BuildRequires:  procps
#Requires:       expect


%description
The Courier authentication library provides authentication services for
other Courier applications.

%package devel
Summary:        Development libraries for the Courier authentication library
License:        GPLv2+
Group:          Development/Libraries/Other
Requires:       %{name} = %{version}

%description devel
This package contains the development libraries and files needed to
compile Courier packages that use this authentication library.	Install
this package in order to build the rest of the Courier packages.  After
they are built and installed this package can be removed.  Files in
this package are not needed at runtime.


%package userdb
Summary:        Userdb support for the Courier authentication library
License:        GPLv2+
Group:          Productivity/Networking/Email/Servers

%description userdb
This package installs the userdb support for the Courier authentication
library.  Userdb is a simple way to manage virtual mail accounts using
a GDBM-based database file.

#%package ldap
#Summary:        LDAP support for the Courier authentication library
#License:        GPLv2+
#Group:          Productivity/Networking/Email/Servers

#%description ldap
#This package installs LDAP support for the Courier authentication
#library. Install this package in order to be able to authenticate using
#LDAP.

#%package mysql
#Summary:        MySQL support for the Courier authentication library
#License:        GPLv2+
#Group:          Productivity/Networking/Email/Servers

#%description mysql
#This package installs MySQL support for the Courier authentication
#library. Install this package in order to be able to authenticate using
#MySQL.

#%package pgsql
#Summary:        PostgreSQL support for the Courier authentication library
#License:        GPLv2+
#Group:          Productivity/Networking/Email/Servers

#%description pgsql
#This package installs PostgreSQL support for the Courier authentication
#library. Install this package in order to be able to authenticate using
#PostgreSQL.

#%package pipe
#Summary:        Pipe support for the Courier authentication library
#License:        GPLv2+
#Group:          Productivity/Networking/Email/Servers

#%description pipe
#This package installs Pipe support for the Courier authentication
#library. Install this package in order to be able to authenticate using
#Pipe.

%prep
%setup -q
%patch1 -p1 -b .os2~

%build

export CONFIG_SHELL="/bin/sh"
export CFLAGS="$RPM_OPT_FLAGS -DLDAP_DEPRECATED=1"
export LDFLAGS="-Zbin-files -Zhigh-mem -Zomf"
export LIBS="-lurpo"
%configure \
	--libexecdir=%{_prefix}/lib \
	--datadir=%{_datadir}/courier-imap \
	--sharedstatedir=%{_sharedstatedir}/%{name} \
	--with-piddir=/var/run \
	--disable-root-check \
	--enable-unicode \
	--with-authdaemonvar=%{_localstatedir}/run/authdaemon.courier-imap \
        "--cache-file=%{_topdir}/cache/%{name}-%{_target_cpu}.cache"

%{__make} %{?jobs:-j%jobs}

%install
%{__make} install DESTDIR=$RPM_BUILD_ROOT
#mv $RPM_BUILD_ROOT%{_libdir}/%{name}/lib*.so* $RPM_BUILD_ROOT%{_libdir}
%{__rm} -f $RPM_BUILD_ROOT%{_libdir}/%{name}/*.la
%{__install} -m 755 sysconftool $RPM_BUILD_ROOT%{_prefix}/lib/%{name}
%{__install} -m 755 authmigrate $RPM_BUILD_ROOT%{_prefix}/lib/%{name}
%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/init.d
#%{__install} -m 755 %{S:1} $RPM_BUILD_ROOT%{_sysconfdir}/init.d/courier-authdaemon
%{__ln_s} -f ../../%{_sysconfdir}/init.d/courier-authdaemon \
  $RPM_BUILD_ROOT%{_sbindir}/rccourier-authdaemon

%{__install} -m 755 authpwd.dll $RPM_BUILD_ROOT%{_prefix}/lib/%{name}

#%preun
#%stop_on_removal courier-authdaemon
#if [ "$1" = "0" ]; then
#  %{__rm} -f /var/run/authdaemon.courier-imap/{socket,pid,pid.lock}
#fi

#%post
#/sbin/ldconfig
#%{_prefix}/lib/%{name}/authmigrate >/dev/null
#%{_prefix}/lib/%{name}/sysconftool %{_sysconfdir}/authlib/*.dist >/dev/null
#if [ "$1" = "1" ]; then
#  %{fillup_and_insserv -f courier-authdaemon}
#fi

#%postun
#/sbin/ldconfig
#%restart_on_update courier-authdaemon
#%insserv_cleanup

#%post userdb -p /sbin/ldconfig

#%postun userdb -p /sbin/ldconfig

#%post ldap -p /sbin/ldconfig

#%postun ldap -p /sbin/ldconfig

#%post mysql -p /sbin/ldconfig

#%postun mysql -p /sbin/ldconfig

#%post pgsql -p /sbin/ldconfig

#%postun pgsql -p /sbin/ldconfig

#%post pipe -p /sbin/ldconfig

#%postun pipe -p /sbin/ldconfig

%post
%wps_object_create_begin
COURIER_FOLDER:WPFolder|Courier Daemons|<WP_DESKTOP>|TITLE=Courier Daemons;
COURIER_AUTHD:WPProgram|Courier Auth daemon|<COURIER_FOLDER>|EXENAME=((%{_prefix}/lib/%{name}/authdaemond.exe));STARTUPDIR=((%{_prefix}/lib/%{name}));PARAMETERS=;TITLE=Courier Auth daemon;
%wps_object_create_end

%postun
%wps_object_delete_all

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README README*html
%doc NEWS COPYING* AUTHORS ChangeLog authldap.schema
#%{_sysconfdir}/init.d/courier-authdaemon
%dir %{_sysconfdir}/authlib
%config %{_sysconfdir}/authlib/*
%dir %attr(700,root,root) %{_localstatedir}/run/authdaemon.courier-imap
%{_sbindir}/authdaemond
%{_sbindir}/authenumerate.exe
%{_sbindir}/authpasswd.exe
%{_sbindir}/authtest.exe
%{_sbindir}/courierlogger.exe
%{_sbindir}/rccourier-authdaemon
%dir %{_prefix}/lib/%{name}
%{_prefix}/lib/%{name}/authmigrate
%{_prefix}/lib/%{name}/sysconftool
%{_prefix}/lib/%{name}/authdaemond.exe
%{_prefix}/lib/%{name}/authsystem.passwd
%{_prefix}/lib/%{name}/makedatprog.exe
%{_prefix}/lib/%{name}/*.dll
%{_mandir}/man1/*

%files devel
%defattr(-,root,root,-)
#%doc authlib.html auth_*.html
%{_bindir}/courierauthconfig.exe
%{_includedir}/*
%{_mandir}/man3/*
%dir %{_prefix}/lib/%{name}/*.a

%files userdb
%defattr(-,root,root,-)
%{_sbindir}/makeuserdb
%{_sbindir}/pw2userdb
%{_sbindir}/userdb
%{_sbindir}/userdb-test-cram-md5
#%{_sbindir}/userdbpw
#%{_libdir}/libauthuserdb.so
#%{_libdir}/libauthuserdb.so.0*
%{_mandir}/man8/*userdb*

#%files ldap
#%defattr(-,root,root,-)
#%doc README.ldap authldap.schema
#%{_libdir}/libauthldap.so*

#%files mysql
#%defattr(-,root,root,-)
#%{_libdir}/libauthmysql.so*

#%files pgsql
#%defattr(-,root,root,-)
#%{_libdir}/libauthpgsql.so*

#%files pipe
#%defattr(-,root,root,-)
#%{_libdir}/libauthpipe.so*

%changelog
