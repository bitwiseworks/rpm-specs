%bcond_with bootstrap

%if %{without bootstrap}
%{?!WITH_MONO:          %global WITH_MONO 1}
%else
%{?!WITH_MONO:          %global WITH_MONO 0}
%endif

%{?!WITH_COMPAT_DNSSD:  %global WITH_COMPAT_DNSSD 1}
%{?!WITH_COMPAT_HOWL:   %global WITH_COMPAT_HOWL  1}
%{?!WITH_QT3:           %global WITH_QT3 1}
%{?!WITH_QT4:           %global WITH_QT4 1}

%if %{without bootstrap}
%{?!WITH_QT5:           %global WITH_QT5 1}
%else
%{?!WITH_QT5:           %global WITH_QT5 0}
%endif

%{?!WITH_PYTHON:        %global WITH_PYTHON 1}

%ifnarch %{mono_arches}
%define WITH_MONO 0
%endif

# https://bugzilla.redhat.com/show_bug.cgi?id=1751484
%if 0%{?fedora} > 30 || 0%{?rhel} > 8
%global WITH_PYTHON 0
%endif

%if 0%{?rhel}
%define WITH_MONO 0
  %if 0%{?rhel} >= 6
    %define WITH_QT4 0
    %define WITH_QT5 0
  %endif
  %if 0%{?rhel} > 7
    %define WITH_QT3 0
  %endif
%endif
%if 0%{?os2_version}
%define WITH_MONO 0
%define WITH_QT3 0
%define WITH_PYTHON 0
%endif

# http://bugzilla.redhat.com/1008395 - no hardened build
%global _hardened_build 1

# trim changelog included in binary rpms
%global _changelog_trimtime %(date +%s -d "1 year ago")

Name:             avahi
Version:          0.7
Release:          1%{?dist}
Summary:          Local network service discovery
License:          LGPLv2+
URL:              http://avahi.org
Requires:         dbus
Requires:         expat
Requires:         libdaemon >= 0.11
# For /usr/bin/dbus-send
Requires(post):   dbus
%if !0%{?os2_version}
Requires(pre):    shadow-utils
%endif
Requires(pre):    coreutils
Requires:         %{name}-libs = %{version}-%{release}
BuildRequires:    automake
BuildRequires:    libtool
BuildRequires:    dbus-devel >= 0.90
%if !0%{?os2_version}
BuildRequires:    dbus-glib-devel >= 0.70
BuildRequires:    desktop-file-utils
%if %{without bootstrap}
BuildRequires:    gtk2-devel
BuildRequires:    gtk3-devel >= 2.99.0
%endif
%endif
#BuildRequires:    gobject-introspection-devel
%if %{WITH_QT3}
BuildRequires:    qt3-devel
%endif
%if %{WITH_QT4}
%if !0%{?os2_version}
BuildRequires:    qt4-devel
%else
BuildRequires:    qt4-devel-kit
%endif
%endif
%if %{WITH_QT5}
BuildRequires:    qt5-qtbase-devel
%endif
BuildRequires:    libdaemon-devel >= 0.11
BuildRequires:    glib2-devel
%if !0%{?os2_version}
BuildRequires:    libcap-devel
%endif
BuildRequires:    expat-devel
%if %{WITH_PYTHON}
%if 0%{?fedora} > 27
%global python2_dbus python2-dbus
%global python2_libxml2 python2-libxml2
%else
%global python2_dbus dbus-python
%global python2_libxml2 libxml2-python
%endif
BuildRequires:    %{python2_dbus}
BuildRequires:    %{python2_libxml2}
# really only need interpreter + rpm-macros -- rex
BuildRequires:    python2-devel
BuildRequires:    python3-devel
%else
Obsoletes: python2-avahi < %{version}-%{release}
Obsoletes: python3-avahi < %{version}-%{release}
%if %{without bootstrap}
%if !0%{?os2_version}
BuildRequires:    pygtk2
%endif
%endif
%endif
%if !0%{?os2_version}
BuildRequires:    gdbm-devel
BuildRequires:    pkgconfig(pygobject-3.0)
%endif
BuildRequires:    pkgconfig(libevent) >= 2.0.21
%if !0%{?os2_version}
BuildRequires:    intltool
%endif
BuildRequires:    perl-XML-Parser
BuildRequires:    xmltoman
%if %{WITH_MONO}
BuildRequires:    mono-devel
BuildRequires:    monodoc-devel
%endif
%if !0%{?os2_version}
BuildRequires:    systemd
%{?systemd_requires}
%endif
BuildRequires:    gcc
BuildRequires:    gcc-c++

%if !0%{?os2_version}
%if 0%{?beta:1}
Source0:          https://github.com/lathiat/avahi/archive/%{version}-%{beta}.tar.gz#/%{name}-%{version}-%{beta}.tar.gz
%else
Source0:          https://github.com/lathiat/avahi/releases/download/v%{version}/avahi-%{version}.tar.gz
#Source0:         http://avahi.org/download/avahi-%{version}.tar.gz
%endif

## upstream patches
Patch6: 0006-avahi-dnsconfd.service-Drop-Also-avahi-daemon.socket.patch
Patch7: 0007-man-add-missing-bshell.1-symlink.patch
Patch8: 0008-Ship-avahi-discover-1-bssh-1-and-bvnc-1-also-for-GTK.patch
Patch9: 0009-fix-requires-in-pc-file.patch
Patch10: 0010-fix-bytestring-decoding-for-proper-display.patch
Patch11: 0011-avahi_dns_packet_consume_uint32-fix-potential-undefi.patch

## downstream patches
Patch100:         avahi-0.6.30-mono-libdir.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1897925
# https://github.com/lathiat/avahi/pull/312
Patch101: 0016-fix-QT3-build.patch
Patch102: avahi-0.8-no_undefined.patch
%else
Vendor:           bww bitwise works GmbH
#scm_source       github https://github.com/bitwiseworks/%{name}-os2 %{version}-os2
%scm_source       git e:/trees/avahi/git master-os2
%endif

%description
Avahi is a system which facilitates service discovery on
a local network -- this means that you can plug your laptop or
computer into a network and instantly be able to view other people who
you can chat with, find printers to print to or find files being
shared. This kind of technology is already found in MacOS X (branded
'Rendezvous', 'Bonjour' and sometimes 'ZeroConf') and is very
convenient.

%package tools
Summary:          Command line tools for mDNS browsing and publishing
Requires:         %{name} = %{version}-%{release}
Requires:         %{name}-libs = %{version}-%{release}

%description tools
Command line tools that use avahi to browse and publish mDNS services.

%if !0%{?os2_version}
%package ui-tools
Summary:          UI tools for mDNS browsing
Requires:         %{name} = %{version}-%{release}
Requires:         %{name}-libs = %{version}-%{release}
Requires:         %{name}-glib = %{version}-%{release}
Requires:         %{name}-ui-gtk3 = %{version}-%{release}
Requires:         tigervnc
Requires:         openssh-clients
%if %{WITH_PYTHON}
Requires:         gdbm
Requires:         pygtk2
Requires:         pygtk2-libglade
Requires:         python2-avahi = %{version}-%{release}
Requires:         %{python2_dbus}
Requires:         python2-gobject-base
%endif

%description ui-tools
Graphical user interface tools that use Avahi to browse for mDNS services.
%endif

%package glib
Summary:          Glib libraries for avahi
Requires:         %{name}-libs = %{version}-%{release}

%description glib
Libraries for easy use of avahi from glib applications.

%package glib-devel
Summary:          Libraries and header files for avahi glib development
Requires:         %{name}-devel = %{version}-%{release}
Requires:         %{name}-glib = %{version}-%{release}
Requires:         glib2-devel

%description glib-devel
The avahi-devel package contains the header files and libraries
necessary for developing programs using avahi with glib.

%package gobject
Summary:          GObject wrapper library for Avahi
Requires:         %{name}-libs = %{version}-%{release}
Requires:         %{name}-glib = %{version}-%{release}

%description gobject
This library contains a GObject wrapper for the Avahi API

%package gobject-devel
Summary:          Libraries and header files for Avahi GObject development
Requires:         %{name}-devel = %{version}-%{release}
Requires:         %{name}-gobject = %{version}-%{release}
#Requires:         %{name}-glib-devel = %{version}-%{release}

%description gobject-devel
The avahi-gobject-devel package contains the header files and libraries
necessary for developing programs using avahi-gobject.

%if !0%{?os2_version}
%if %{without bootstrap}
%package ui
Summary:          Gtk user interface library for Avahi (Gtk+ 2 version)
Requires:         %{name}-libs = %{version}-%{release}
Requires:         %{name}-glib = %{version}-%{release}
Requires:         gtk2

%description ui
This library contains a Gtk 2.x widget for browsing services.

%package ui-gtk3
Summary:          Gtk user interface library for Avahi (Gtk+ 3 version)
Requires:         %{name}-libs = %{version}-%{release}
Requires:         %{name}-glib = %{version}-%{release}
Requires:         gtk3

%description ui-gtk3
This library contains a Gtk 3.x widget for browsing services.

%package ui-devel
Summary:          Libraries and header files for Avahi UI development
Requires:         %{name}-devel = %{version}-%{release}
Requires:         %{name}-ui = %{version}-%{release}
Requires:         %{name}-ui-gtk3 = %{version}-%{release}
#Requires:         %{name}-glib-devel = %{version}-%{release}

%description ui-devel
The avahi-ui-devel package contains the header files and libraries
necessary for developing programs using avahi-ui.
%endif
%endif

%if %{WITH_QT3}
%package qt3
Summary:          Qt3 libraries for avahi
Requires:         %{name}-libs = %{version}-%{release}

%description qt3
Libraries for easy use of avahi from Qt3 applications.

%package qt3-devel
Summary:          Libraries and header files for avahi Qt3 development
Requires:         %{name}-devel = %{version}-%{release}
Requires:         %{name}-qt3 = %{version}-%{release}

%description qt3-devel
The avahi-qt3-devel package contains the header files and libraries
necessary for developing programs using avahi with Qt3.
%endif

%if %{WITH_QT4}
%package qt4
Summary:          Qt4 libraries for avahi
Requires:         %{name}-libs = %{version}-%{release}

%description qt4
Libraries for easy use of avahi from Qt4 applications.

%package qt4-devel
Summary:          Libraries and header files for avahi Qt4 development
Requires:         %{name}-devel = %{version}-%{release}
Requires:         %{name}-qt4 = %{version}-%{release}

%description qt4-devel
Th avahi-qt4-devel package contains the header files and libraries
necessary for developing programs using avahi with Qt4.
%endif

%if %{WITH_QT5}
%package qt5
Summary:          Qt5 libraries for avahi
Requires:         %{name}-libs = %{version}-%{release}

%description qt5
Libraries for easy use of avahi from Qt5 applications.

%package qt5-devel
Summary:          Libraries and header files for avahi Qt5 development
Requires:         %{name}-devel = %{version}-%{release}
Requires:         %{name}-qt5 = %{version}-%{release}

%description qt5-devel
Th avahi-qt5-devel package contains the header files and libraries
necessary for developing programs using avahi with Qt5.
%endif

%if %{WITH_MONO}
%package sharp
Summary:          Mono language bindings for avahi mono development
Requires:         mono-core >= 1.1.13
Requires:         %{name}-libs = %{version}-%{release}

%description sharp
The avahi-sharp package contains the files needed to develop
mono programs that use avahi.

%package ui-sharp
Summary:          Mono language bindings for avahi-ui
Requires:         %{name}-libs = %{version}-%{release}
Requires:         %{name}-ui = %{version}-%{release}
Requires:         %{name}-sharp = %{version}-%{release}
Requires:         mono-core >= 1.1.13
Requires:         gtk-sharp2
BuildRequires:    gtk-sharp2-devel

%description ui-sharp
The avahi-sharp package contains the files needed to run
Mono programs that use avahi-ui.

%package ui-sharp-devel
Summary:          Mono language bindings for developing with avahi-ui
Requires:         %{name}-ui-sharp = %{version}-%{release}

%description ui-sharp-devel
The avahi-sharp-ui-devel package contains the files needed to develop
Mono programs that use avahi-ui.
%endif

%package libs
Summary:          Libraries for avahi run-time use

%description libs
The avahi-libs package contains the libraries needed
to run programs that use avahi.

%package devel
Summary:          Libraries and header files for avahi development
Requires:         %{name}-libs = %{version}-%{release}
# for libavahi-core
Requires:         %{name} = %{version}-%{release}

%description devel
The avahi-devel package contains the header files and libraries
necessary for developing programs using avahi.

%if %{WITH_COMPAT_HOWL}
%package compat-howl
Summary:          Libraries for howl compatibility
Requires:         %{name}-libs = %{version}-%{release}
Obsoletes:        howl-libs
Provides:         howl-libs

%description compat-howl
Libraries that are compatible with those provided by the howl package.

%package compat-howl-devel
Summary:          Header files for development with the howl compatibility libraries
Requires:         %{name}-compat-howl = %{version}-%{release}
Requires:         %{name}-devel = %{version}-%{release}
Obsoletes:        howl-devel
Provides:         howl-devel

%description compat-howl-devel
Header files for development with the howl compatibility libraries.
%endif

%if %{WITH_COMPAT_DNSSD}
%package compat-libdns_sd
Summary:          Libraries for Apple Bonjour mDNSResponder compatibility
Requires:         %{name}-libs = %{version}-%{release}

%description compat-libdns_sd
Libraries for Apple Bonjour mDNSResponder compatibility.

%package compat-libdns_sd-devel
Summary:          Header files for the Apple Bonjour mDNSResponder compatibility libraries
Requires:         %{name}-compat-libdns_sd = %{version}-%{release}
Requires:         %{name}-devel = %{version}-%{release}

%description compat-libdns_sd-devel
Header files for development with the Apple Bonjour mDNSResponder compatibility
libraries.
%endif

%if !0%{?os2_version}
%package autoipd
Summary:          Link-local IPv4 address automatic configuration daemon (IPv4LL)
Requires(pre):    shadow-utils
Requires:         %{name}-libs = %{version}-%{release}

%description autoipd
avahi-autoipd implements IPv4LL, "Dynamic Configuration of IPv4
Link-Local Addresses"  (IETF RFC3927), a protocol for automatic IP address
configuration from the link-local 169.254.0.0/16 range without the need for a
central server. It is primarily intended to be used in ad-hoc networks which
lack a DHCP server.
%endif

%package dnsconfd
Summary:          Configure local unicast DNS settings based on information published in mDNS
Requires:         %{name} = %{version}-%{release}
Requires:         %{name}-libs = %{version}-%{release}

%description dnsconfd
avahi-dnsconfd connects to a running avahi-daemon and runs the script
/etc/avahi/dnsconfd.action for each unicast DNS server that is announced on the
local LAN. This is useful for configuring unicast DNS servers in a DHCP-like
fashion with mDNS.

%if %{WITH_PYTHON}
%package -n python2-avahi
Summary:          Python2 Avahi bindings
Obsoletes:        python-avahi < 0.7
Provides:         python-avahi = %{version}-%{release}
Requires:         %{name} = %{version}-%{release}
Requires:         %{name}-libs = %{version}-%{release}

%description -n python2-avahi
%{summary}.

%package -n python3-avahi
Summary:          Python3 Avahi bindings
Requires:         %{name} = %{version}-%{release}
Requires:         %{name}-libs = %{version}-%{release}

%description -n python3-avahi
%{summary}.
%endif

%debug_package

%prep
%if !0%{?os2_version}
%autosetup -n %{name}-%{version}%{?beta:-%{beta}} -p1
%else
%scm_setup
%endif

rm -fv docs/INSTALL


%build
# patch100/101/102 requires autogen
# and kills rpaths a bonus
rm -fv missing
NOCONFIGURE=1 ./autogen.sh

%if 0%{?os2_version}
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
export QT4_LIBS="-lQtCore4"
export QT4_CFLAGS="-std=gnu++11 -I/@unixroot/usr/include/QtCore"
export MOC_QT4=/@unixroot/usr/lib/qt4/bin/moc.exe
export CPPFLAGS="-std=gnu++11"
# Set BUILDLEVEL to be embedded to all DLLs built with Libtool.
export LT_BUILDLEVEL="@#%{vendor}:%{version}-%{release}#@##1## `LANG=C date +'%%d %%b %%Y %%H:%%M:%%S'`     `uname -n`::::0::"
%endif

%configure \
%if !0%{?os2_version}
        --with-distro=fedora \
%endif
        --disable-monodoc \
        --with-avahi-user=avahi \
        --with-avahi-group=avahi \
        --with-avahi-priv-access-group=avahi \
        --with-autoipd-user=avahi-autoipd \
        --with-autoipd-group=avahi-autoipd \
%if !0%{?os2_version}
        --with-systemdsystemunitdir=%{_unitdir} \
%endif
        --enable-introspection=no \
        --enable-shared=yes \
        --enable-static=no \
        --disable-silent-rules \
%if !0%{?os2_version}
%if %{without bootstrap}
        --enable-gtk \
%else
	--disable-gtk \
	--disable-gtk3 \
%endif
%else
	--disable-gtk \
	--disable-gtk3 \
	--disable-gdbm \
	--disable-autoipd \
%endif
%if ! %{WITH_PYTHON}
	--disable-python \
%endif
%if %{WITH_COMPAT_DNSSD}
        --enable-compat-libdns_sd \
%endif
%if %{WITH_COMPAT_HOWL}
        --enable-compat-howl \
%endif
%if %{WITH_QT3}
        --enable-qt3 \
%endif
%if %{WITH_QT4}
        --enable-qt4 \
%endif
%if ! %{WITH_QT5}
        --disable-qt5 \
%endif
%if ! %{WITH_MONO}
        --disable-mono \
%endif
;

# workaround parallel build issues (aarch64 only so far, bug #1564553)
%if !0%{?os2_version}
%make_build -k V=1 || make V=1
%else
make V=1
%endif

%install
%make_install

# omit libtool .la files
rm -fv %{buildroot}%{_libdir}/lib*.la

# remove example
rm -fv %{buildroot}%{_sysconfdir}/avahi/services/ssh.service
rm -fv %{buildroot}%{_sysconfdir}/avahi/services/sftp-ssh.service

# create /var/run/avahi-daemon to ensure correct selinux policy for it:
mkdir -p %{buildroot}%{_localstatedir}/run/avahi-daemon
%if !0%{?os2_version}
mkdir -p %{buildroot}%{_localstatedir}/lib/avahi-autoipd
%endif

# remove the documentation directory - let % doc handle it:
rm -rfv %{buildroot}%{_datadir}/%{name}-%{version}

# Make /etc/avahi/etc/localtime owned by avahi:
%if !0%{?os2_version}
mkdir -p %{buildroot}/etc/avahi/etc
touch %{buildroot}/etc/avahi/etc/localtime
%else
mkdir -p %{buildroot}/@unixroot/etc/avahi/etc
touch %{buildroot}/@unixroot/etc/avahi/etc/localtime
%endif

# fix bug 197414 - add missing symlinks for avahi-compat-howl and avahi-compat-dns-sd
%if %{WITH_COMPAT_HOWL}
ln -s avahi-compat-howl.pc  %{buildroot}/%{_libdir}/pkgconfig/howl.pc
%endif
%if %{WITH_COMPAT_DNSSD}
ln -s avahi-compat-libdns_sd.pc %{buildroot}/%{_libdir}/pkgconfig/libdns_sd.pc
ln -s avahi-compat-libdns_sd/dns_sd.h %{buildroot}/%{_includedir}/
%endif

%if %{WITH_PYTHON}
# Add python3 support
mkdir -p %{buildroot}%{python3_sitelib}/avahi/
cp -r %{buildroot}%{python2_sitelib}/avahi/* %{buildroot}%{python3_sitelib}/avahi/
rm -fv %{buildroot}%{buildroot}%{python3_sitelib}/avahi/*.py{c,o}
sed -i 's!/usr/bin/python2!/usr/bin/python3!' %{buildroot}%{python3_sitelib}/avahi/ServiceTypeDatabase.py

# avoid empty GenericName keys from .desktop files
for i in %{buildroot}%{_datadir}/applications/*.desktop ; do
if [ -n "$(grep '^GenericName=$' $i)" ]; then
  desktop-file-edit --copy-name-to-generic-name $i
fi
done
%else
# unpackaged files
rm -fv  %{buildroot}%{_datadir}/applications/{bssh,bvnc}.desktop
rm -fv  %{buildroot}%{_datadir}/avahi/interfaces/avahi-discover.ui
%endif

rm -fv %{buildroot}%{_sysconfdir}/rc.d/init.d/avahi-daemon
rm -fv %{buildroot}%{_sysconfdir}/rc.d/init.d/avahi-dnsconfd

%find_lang %{name}


%check
%if %{WITH_PYTHON}
for i in %{buildroot}%{_datadir}/applications/*.desktop ; do
desktop-file-validate $i
done
%endif


%pre
%if !0%{?os2_version}
getent group avahi >/dev/null || groupadd -f -g 70 -r avahi
if ! getent passwd avahi > /dev/null ; then
  if ! getent passwd 70 > /dev/null ; then
    useradd -r -l -u 70 -g avahi -d %{_localstatedir}/run/avahi-daemon -s /sbin/nologin -c "Avahi mDNS/DNS-SD Stack" avahi
  else
    useradd -r -l -g avahi -d %{_localstatedir}/run/avahi-daemon -s /sbin/nologin -c "Avahi mDNS/DNS-SD Stack" avahi
  fi
fi
%else
groupadd -f -g 70 -r avahi
useradd -r -l -u 70 -g avahi -d %{_localstatedir}/run/avahi-daemon -s /sbin/nologin -c "Avahi mDNS/DNS-SD Stack" avahi
%endif
exit 0

%post
%if !0%{?os2_version}
%{?ldconfig}
/usr/bin/dbus-send --system --type=method_call --dest=org.freedesktop.DBus / org.freedesktop.DBus.ReloadConfig >/dev/null 2>&1 || :
if [ "$1" -eq 1 -a -s /etc/localtime ]; then
        /usr/bin/cp -cfp /etc/localtime /etc/avahi/etc/localtime >/dev/null 2>&1 || :
fi
%systemd_post avahi-daemon.socket avahi-daemon.service
%endif

%preun
%if !0%{?os2_version}
%systemd_preun avahi-daemon.socket avahi-daemon.service
%endif

%postun
%if !0%{?os2_version}
%{?ldconfig}
%systemd_postun_with_restart avahi-daemon.socket avahi-daemon.service
%endif

%if !0%{?os2_version}
%pre autoipd
getent group avahi-autoipd >/dev/null || groupadd -f -g 170 -r avahi-autoipd
if ! getent passwd avahi-autoipd > /dev/null ; then
  if ! getent passwd 170 > /dev/null; then
    useradd -r -u 170 -l -g avahi-autoipd -d %{_localstatedir}/lib/avahi-autoipd -s /sbin/nologin -c "Avahi IPv4LL Stack" avahi-autoipd
  else
    useradd -r -l -g avahi-autoipd -d %{_localstatedir}/lib/avahi-autoipd -s /sbin/nologin -c "Avahi IPv4LL Stack" avahi-autoipd
  fi
fi
exit 0
%endif

%post dnsconfd
%if !0%{?os2_version}
%systemd_post avahi-dnsconfd.service
%endif

%preun dnsconfd
%if !0%{?os2_version}
%systemd_preun avahi-dnsconfd.service
%endif

%postun dnsconfd
%if !0%{?os2_version}
%systemd_postun_with_restart avahi-dnsconfd.service
%endif

%if !0%{?os2_version}
%ldconfig_scriptlets glib

%ldconfig_scriptlets compat-howl

%ldconfig_scriptlets compat-libdns_sd

%ldconfig_scriptlets libs

%ldconfig_scriptlets ui

%ldconfig_scriptlets ui-gtk3

%ldconfig_scriptlets gobject
%endif

%files -f %{name}.lang
%doc docs/* avahi-daemon/example.service avahi-daemon/sftp-ssh.service avahi-daemon/ssh.service
%dir %{_sysconfdir}/avahi
%dir %{_sysconfdir}/avahi/etc
%ghost %{_sysconfdir}/avahi/etc/localtime
%config(noreplace) %{_sysconfdir}/avahi/hosts
%dir %{_sysconfdir}/avahi/services
%ghost %dir %{_localstatedir}/run/avahi-daemon
%config(noreplace) %{_sysconfdir}/avahi/avahi-daemon.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/avahi-dbus.conf
%if !0%{?os2_version}
%{_sbindir}/avahi-daemon
%else
%{_sbindir}/avahi-daemon.exe
%endif
%dir %{_datadir}/avahi
%{_datadir}/avahi/*.dtd
%dir %{_libdir}/avahi
%if %{WITH_PYTHON}
%{_libdir}/avahi/service-types.db
%endif
%{_mandir}/man5/*
%{_mandir}/man8/avahi-daemon.*
%if !0%{?os2_version}
%{_unitdir}/avahi-daemon.service
%{_unitdir}/avahi-daemon.socket
%endif
%{_datadir}/dbus-1/interfaces/*.xml
%{_datadir}/dbus-1/system-services/org.freedesktop.Avahi.service
%if !0%{?os2_version}
%{_libdir}/libavahi-core.so.*
%else
%{_libdir}/avahcor*.dll
%endif

%if !0%{?os2_version}
%files autoipd
%{_sbindir}/avahi-autoipd
%config(noreplace) %{_sysconfdir}/avahi/avahi-autoipd.action
%attr(1770,avahi-autoipd,avahi-autoipd) %dir %{_localstatedir}/lib/avahi-autoipd/
%{_mandir}/man8/avahi-autoipd.*
%endif

%files dnsconfd
%config(noreplace) %{_sysconfdir}/avahi/avahi-dnsconfd.action
%if !0%{?os2_version}
%{_sbindir}/avahi-dnsconfd
%else
%{_sbindir}/avahi-dnsconfd.exe
%endif
%{_mandir}/man8/avahi-dnsconfd.*
%if !0%{?os2_version}
%{_unitdir}/avahi-dnsconfd.service
%endif

%files tools
%if !0%{?os2_version}
%{_bindir}/avahi-browse
%else
%{_bindir}/avahi-browse.exe
%endif
%{_bindir}/avahi-browse-domains
%if !0%{?os2_version}
%{_bindir}/avahi-publish
%else
%{_bindir}/avahi-publish.exe
%endif
%{_bindir}/avahi-publish-address
%{_bindir}/avahi-publish-service
%if !0%{?os2_version}
%{_bindir}/avahi-resolve
%else
%{_bindir}/avahi-resolve.exe
%endif
%{_bindir}/avahi-resolve-address
%{_bindir}/avahi-resolve-host-name
%if !0%{?os2_version}
%{_bindir}/avahi-set-host-name
%else
%{_bindir}/avahi-set-host-name.exe
%endif

%{_mandir}/man1/avahi-browse.1*
%{_mandir}/man1/avahi-browse-domains.1*
%{_mandir}/man1/avahi-publish.1*
%{_mandir}/man1/avahi-publish-address.1*
%{_mandir}/man1/avahi-publish-service.1*
%{_mandir}/man1/avahi-resolve.1*
%{_mandir}/man1/avahi-resolve-address.1*
%{_mandir}/man1/avahi-resolve-host-name.1*
%{_mandir}/man1/avahi-set-host-name.1*

%if !0%{?os2_version}
%files ui-tools
%{_bindir}/bshell
%{_bindir}/bssh
%{_bindir}/bvnc
%{_bindir}/avahi-discover-standalone
%{_mandir}/man1/bshell.1*
%{_mandir}/man1/bssh.1*
%{_mandir}/man1/bvnc.1*
%if %{WITH_PYTHON}
# avahi-bookmarks is not really a UI tool, but I won't create a seperate package for it...
%{_bindir}/avahi-bookmarks
%{_mandir}/man1/avahi-discover*
%{_mandir}/man1/avahi-bookmarks*
%{_datadir}/applications/b*.desktop
%{_datadir}/applications/avahi-discover.desktop
%{_datadir}/avahi/interfaces/
%{python2_sitelib}/avahi_discover/
%endif
%endif

%files devel
%if !0%{?os2_version}
%{_libdir}/libavahi-common.so
%{_libdir}/libavahi-core.so
%{_libdir}/libavahi-client.so
%{_libdir}/libavahi-libevent.so
%else
%{_libdir}/avahi-common*_dll.a
%{_libdir}/avahi-core*_dll.a
%{_libdir}/avahi-client*_dll.a
%{_libdir}/avahi-libevent*_dll.a
%endif
%{_includedir}/avahi-client
%{_includedir}/avahi-common
%{_includedir}/avahi-core
%{_includedir}/avahi-libevent
%{_libdir}/pkgconfig/avahi-core.pc
%{_libdir}/pkgconfig/avahi-client.pc
%{_libdir}/pkgconfig/avahi-libevent.pc

%files libs
%doc README
%license LICENSE
%if !0%{?os2_version}
%{_libdir}/libavahi-common.so.*
%{_libdir}/libavahi-client.so.*
%{_libdir}/libavahi-libevent.so.*
%else
%{_libdir}/avahcom*.dll
%{_libdir}/avahcln*.dll
%{_libdir}/avahevt*.dll
%endif

%files glib
%if !0%{?os2_version}
%{_libdir}/libavahi-glib.so.*
%else
%{_libdir}/avahgli*.dll
%endif

%files glib-devel
%if !0%{?os2_version}
%{_libdir}/libavahi-glib.so
%else
%{_libdir}/avahi-glib*_dll.a
%endif
%{_includedir}/avahi-glib
%{_libdir}/pkgconfig/avahi-glib.pc

%files gobject
%if !0%{?os2_version}
%{_libdir}/libavahi-gobject.so.*
%else
%{_libdir}/avahgob*.dll
%endif
#%{_libdir}/girepository-1.0/Avahi-0.6.typelib
#%{_libdir}/girepository-1.0/AvahiCore-0.6.typelib

%files gobject-devel
%if !0%{?os2_version}
%{_libdir}/libavahi-gobject.so
%else
%{_libdir}/avahi-gobject*_dll.a
%endif
%{_includedir}/avahi-gobject
%{_libdir}/pkgconfig/avahi-gobject.pc
#%{_datadir}/gir-1.0/Avahi-0.6.gir
#%{_datadir}/gir-1.0/AvahiCore-0.6.gir

%if !0%{?os2_version}
%if %{without bootstrap}
%files ui
%{_libdir}/libavahi-ui.so.*

%files ui-gtk3
%{_libdir}/libavahi-ui-gtk3.so.*

%files ui-devel
%{_libdir}/libavahi-ui.so
%{_libdir}/libavahi-ui-gtk3.so
%{_includedir}/avahi-ui
%{_libdir}/pkgconfig/avahi-ui.pc
%{_libdir}/pkgconfig/avahi-ui-gtk3.pc
%endif
%endif

%if %{WITH_QT3}
%ldconfig_scriptlets qt3

%files qt3
%{_libdir}/libavahi-qt3.so.*

%files qt3-devel
%{_libdir}/libavahi-qt3.so
%{_includedir}/avahi-qt3/
%{_libdir}/pkgconfig/avahi-qt3.pc
%endif

%if %{WITH_QT4}
%if !0%{?os2_version}
%ldconfig_scriptlets qt4
%endif

%files qt4
%if !0%{?os2_version}
%{_libdir}/libavahi-qt4.so.*
%else
%{_libdir}/avahqt4*.dll
%endif

%files qt4-devel
%if !0%{?os2_version}
%{_libdir}/libavahi-qt4.so
%else
%{_libdir}/avahi-qt4*_dll.a
%endif
%{_includedir}/avahi-qt4/
%{_libdir}/pkgconfig/avahi-qt4.pc
%endif

%if %{WITH_QT5}
%if !0%{?os2_version}
%ldconfig_scriptlets qt5
%endif

%files qt5
%if !0%{?os2_version}
%{_libdir}/libavahi-qt5.so.*
%else
%{_libdir}/avahqt5*.dll
%endif

%files qt5-devel
%if !0%{?os2_version}
%{_libdir}/libavahi-qt5.so
%else
%{_libdir}/avahi-qt5*_dll.a
%endif
%{_includedir}/avahi-qt5/
%{_libdir}/pkgconfig/avahi-qt5.pc
%endif

%if %{WITH_MONO}
%files sharp
%{_prefix}/lib/mono/avahi-sharp
%{_prefix}/lib/mono/gac/avahi-sharp
%{_libdir}/pkgconfig/avahi-sharp.pc

%files ui-sharp
%{_prefix}/lib/mono/avahi-ui-sharp
%{_prefix}/lib/mono/gac/avahi-ui-sharp

%files ui-sharp-devel
%{_libdir}/pkgconfig/avahi-ui-sharp.pc
%endif

%if %{WITH_COMPAT_HOWL}
%files compat-howl
%if !0%{?os2_version}
%{_libdir}/libhowl.so.*
%else
%{_libdir}/howl*.dll
%endif

%files compat-howl-devel
%if !0%{?os2_version}
%{_libdir}/libhowl.so
%else
%{_libdir}/howl*_dll.a
%endif
%{_includedir}/avahi-compat-howl
%{_libdir}/pkgconfig/avahi-compat-howl.pc
%{_libdir}/pkgconfig/howl.pc
%endif

%if %{WITH_COMPAT_DNSSD}
%files compat-libdns_sd
%if !0%{?os2_version}
%{_libdir}/libdns_sd.so.*
%else
%{_libdir}/dns_sd*.dll
%endif

%files compat-libdns_sd-devel
%if !0%{?os2_version}
%{_libdir}/libdns_sd.so
%else
%{_libdir}/dns_sd*_dll.a
%endif
%{_includedir}/avahi-compat-libdns_sd
%{_includedir}/dns_sd.h
%{_libdir}/pkgconfig/avahi-compat-libdns_sd.pc
%{_libdir}/pkgconfig/libdns_sd.pc
%endif

%if %{WITH_PYTHON}
%files -n python2-avahi
%{python2_sitelib}/avahi/

%files -n python3-avahi
%{python3_sitelib}/avahi/
%endif


%changelog
* Wed Nov 18 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.7-1
- first OS/2 rpm
