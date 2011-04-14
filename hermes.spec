Summary:        An anti-spam SMTP proxy
Name:           hermes
Version:        1.6
Release:        2%{?dist}
License:        GPL
Group:          System Environment/Daemons
Packager:       Veit Wahlich <cru@zodia.de>
URL:            http://www.hermes-project.com/
Source0:        http://www.iteisa.com/files/%{name}-%{version}.tar.gz
Source1:        %{name}-os2.zip

Buildroot:      %{_tmppath}/%{name}-%{version}-%{release}-root

Patch1: 	hermes-os2.diff

%description
hermes is a generic, lightweight, portable and fast anti-spam smtp proxy.
Supports greylisting, dns blacklisting/whitelisting, protocol throttling, banner delaying, spf and some
other tricks to reject most spam before it even enters your system.

%prep
%setup -q -a1
%patch001 -p1 -b .os2~

%build
export CONFIG_SHELL="/bin/sh" ; \
export LDFLAGS="-Zbin-files -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp" ; \
export LIBS="-lurpo -lmmap -lpthread" ; \
%configure --docdir=%{_datadir}/doc/%{name}-%{version} \
    --disable-dependency-tracking \
    --enable-spf --with-logger-module=file \
    --enable-shared --disable-static \
    "--cache-file=%{_topdir}/cache/%{name}.cache"

%__make %{?_smp_mflags}

%install
%__rm -rf %{buildroot}
%__make DESTDIR=%{buildroot} install
%__mkdir_p %{buildroot}%{_sysconfdir}/rc.d/init.d
%__mkdir_p %{buildroot}%{_sysconfdir}/hermes
%__mkdir_p %{buildroot}%{_localstatedir}/hermes
%__install -m 0755 dists/fc_init %{buildroot}%{_sysconfdir}/rc.d/init.d/hermes
%__install -m 0600 dists/hermesrc.example %{buildroot}%{_sysconfdir}/hermes/hermesrc

%clean
%__rm -rf %{buildroot}

#%post
#/sbin/chkconfig --add hermes

#%preun
#if [ $1 = 0 ]; then	# execute this only if we are NOT doing an upgrade
#    %{_sysconfdir}/rc.d/init.d/hermes stop >/dev/null 2>&1
#    /sbin/chkconfig --del hermes
#fi
#exit 0

%post
%wps_object_create_begin
HERMES_FOLDER:WPFolder|Hermes %version|<WP_DESKTOP>|TITLE=Hermes %version;
HERMES_README:WPShadow|Readme 1st|<HERMES_FOLDER>|SHADOWID=((%_defaultdocdir/%name-%version/ReadMe.txt))
HERMES_OPTIONS:WPShadow|Options|<HERMES_FOLDER>|SHADOWID=((%_defaultdocdir/%name-%version/hermes-options.html))
HERMES_CONFIG:WPShadow|Options|<HERMES_FOLDER>|SHADOWID=((%_sysconfdir/hermes/hermesrc))
HERMES_DAEMON:WPProgram|Hermes daemon|<HERMES_FOLDER>|EXENAME=((%_bindir/hermes.exe));STARTUPDIR=((%_bindir));ICONFILE=((%_defaultdocdir/%name-%version/hermes.ico));TITLE=Hermes daemon;
%wps_object_create_end

%postun
%wps_object_delete_all

%files
%defattr(-, root, root, 0755)
%doc ChangeLog TODO AUTHORS dists/hermesrc.example docs/hermes-options.html docs/installing-hermes.txt docs/gpl.txt
%doc ReadMe.txt rotate.cmd white_host.cmd white_ips.cmd hermes.ico
%{_bindir}/hermes.exe
%{_sysconfdir}/rc.d/init.d/hermes
%config %{_sysconfdir}/hermes/hermesrc
%dir %attr(0700,nobody,nobody) %{_localstatedir}/hermes

%changelog
