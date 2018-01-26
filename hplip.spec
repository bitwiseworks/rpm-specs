# spec source :http://pkgs.fedoraproject.org/cgit/rpms/hplip.git/tree/hplip.spec

%define without_sane 1
%define without_dbus 1
%define without_fax 1

Summary: HP Linux Imaging and Printing Project
Name: hplip
Version: 3.17.11
Release: 1%{?dist}
License: GPLv2+ and MIT and BSD

Url: https://developers.hp.com/hp-linux-imaging-and-printing
Vendor: bww bitwise works GmbH
%scm_source github  https://github.com/bitwiseworks/%{name}-os2 3.17.11-os2

# @todo: decide if we need that to
# if we do it as well, also remove the coment in the post section
#Source1: hpcups-update-ppds.sh

Requires: %{name}-libs = %{version}-%{release}
#Requires: python-pillow
Requires: cups
Requires: wget
%if 0%{!?without_dbus:1}
Requires: python-dbus
%endif
#Requires: gnupg
# /etc/udev/rules.d
#Requires: systemd

BuildRequires: autoconf automake libtool
#BuildRequires: net-snmp-devel
BuildRequires: cups-devel
BuildRequires: python-devel
BuildRequires: libjpeg-devel
#BuildRequires: desktop-file-utils
BuildRequires: libusb1-devel
BuildRequires: openssl-devel
%if 0%{!?without_sane:1}
BuildRequires: sane-backends-devel
%endif
%if 0%{!?without_dbus:1}
BuildRequires: pkgconfig(dbus-1)
%endif

# Make sure we get postscriptdriver tags.
#BuildRequires: python-cups
BuildRequires: cups

# macros: %%{_tmpfilesdir}, %%{_udevrulesdir}
#BuildRequires: systemd

# hpijs was merged into main package in 3.15.7-2
Obsoletes: hpijs < 1:%{version}-%{release}
Provides:  hpijs = 1:%{version}-%{release}

%description
The Hewlett-Packard Linux Imaging and Printing Project provides
drivers for HP printers and multi-function peripherals.

%package common
Summary: Files needed by the HPLIP printer and scanner drivers
License: GPLv2+

%description common
Files needed by the HPLIP printer and scanner drivers.

%package libs
Summary: HPLIP libraries
License: GPLv2+ and MIT
Requires: %{name}-common = %{version}-%{release}
Requires: python
Obsoletes: %{name}-compat-libs < %{version}-%{release}

%description libs
Libraries needed by HPLIP.

%package gui
Summary: HPLIP graphical tools
License: BSD
#BuildRequires: libappstream-glib
Requires: python2-PyQt4
#Requires: python-reportlab
# hpssd.py
#Requires: python-gobject
Requires: %{name} = %{version}-%{release}
%if 0%{!?without_sane:1}
Requires: libsane-hpaio = %{version}-%{release}
%endif

%description gui
HPLIP graphical tools.

%if 0%{!?without_sane:1}
%package -n libsane-hpaio
Summary: SANE driver for scanners in HP's multi-function devices
License: GPLv2+
Obsoletes: libsane-hpoj < 0.91
Provides: libsane-hpoj = 0.91
Requires: sane-backends
Requires: %{name}-libs = %{version}-%{release}

%description -n libsane-hpaio
SANE driver for scanners in HP's multi-function devices (from HPOJ).
%endif

%debug_package

%prep
%scm_setup


%build
# Work-around Makefile.am imperfections.
sed -i 's|^AM_INIT_AUTOMAKE|AM_INIT_AUTOMAKE([foreign])|g' configure.in
# Upstream uses old libtool, which causes problems (due to libhpmud requiring
# libhpdiscovery) when we try to remove rpath from it.
# Regenerating all autotools files works-around these rpath issues.
autoreconf --verbose --force --install

export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
export VENDOR="%{vendor}"

%configure \
%if 0%{!?without_sane:1}
        --enable-scan-build \
%else
        --disable-scan-build \
%endif
        --enable-gui-build \
%if 0%{!?without_fax:1}
        --enable-fax-build \
%else
        --enable-fax-build=no \
%endif
        --disable-foomatic-rip-hplip-install  \
        --enable-qt4 \
        --enable-hpcups-install --enable-cups-drv-install \
        --enable-foomatic-drv-install \
        --enable-hpijs-install \
%if 0%{?without_dbus:1}
        --enable-dbus-build=no \
%endif
        --disable-policykit --with-mimedir=%{_datadir}/cups/mime \
        --disable-network-build --enable-shared --disable-static \
        --with-cupsbackenddir=%{_cups_serverbin}/backend \
        --with-cupsfilterdir=%{_cups_serverbin}/filter \
        --with-icondir=%{_datadir}/applications \
        --with-systraydir=%{_sysconfdir}/xdg/autostart

make %{?_smp_mflags}


%install
mkdir -p %{buildroot}%{_bindir}
make install DESTDIR=%{buildroot}

# Remove unpackaged files
rm -rf  %{buildroot}%{_sysconfdir}/sane.d \
        %{buildroot}%{_docdir} \
        %{buildroot}%{_datadir}/hal \
        %{buildroot}%{_datadir}/hplip/pkservice.py \
        %{buildroot}%{_bindir}/hp-pkservice \
        %{buildroot}%{_datadir}/applications \
        %{buildroot}%{_datadir}/hplip/locatedriver* \
        %{buildroot}%{_datadir}/hplip/dat2drv*

rm -f   %{buildroot}%{_bindir}/hp-logcapture \
        %{buildroot}%{_bindir}/hp-doctor \
        %{buildroot}%{_bindir}/hp-pqdiag \
        %{buildroot}%{_datadir}/hplip/logcapture.py \
        %{buildroot}%{_datadir}/hplip/doctor.py \
        %{buildroot}%{_datadir}/hplip/pqdiag.py

rm -f   %{buildroot}%{_bindir}/foomatic-rip \
        %{buildroot}%{_libdir}/cups/filter/foomatic-rip \
        %{buildroot}%{_libdir}/*.la \
        %{buildroot}%{python_sitearch}/*.la \
        %{buildroot}%{_libdir}/sane/*.la \
        %{buildroot}%{_datadir}/cups/model/foomatic-ppds \
        %{buildroot}%{_datadir}/ppd/HP/*.ppd


# Regenerate hpcups PPDs on upgrade if necessary (bug #579355).
#install -p -m755 %{SOURCE1} %{buildroot}%{_bindir}/hpcups-update-ppds

# Images in docdir should not be executable (bug #440552).
find doc/images -type f -exec chmod 644 {} \;

# Create an empty plugins directory to make sure it gets the right
# SELinux file context (bug #564551).
%{__mkdir_p} %{buildroot}%{_datadir}/hplip/prnt/plugins

# Create an empty var/run/hplip directory
%{__mkdir_p} %{buildroot}%{_localstatedir}/run/hplip

# Remove files we don't want to package.
rm -f %{buildroot}%{_datadir}/hplip/hpaio.desc
rm -f %{buildroot}%{_datadir}/hplip/hplip-install
rm -rf %{buildroot}%{_datadir}/hplip/install.*
rm -f %{buildroot}%{_datadir}/hplip/uninstall.*
rm -f %{buildroot}%{_bindir}/hp-uninstall
rm -f %{buildroot}%{_datadir}/hplip/upgrade.*
rm -f %{buildroot}%{_bindir}/hp-upgrade
rm -f %{buildroot}%{_datadir}/hplip/hpijs.drv.in.template
rm -f %{buildroot}%{_datadir}/cups/mime/pstotiff.types
rm -f %{buildroot}%{_datadir}/hplip/fax/pstotiff*
rm -rf %{buildroot}%{_libdir}/systemd

# we don't need the exe and the python version (use exe as newer)
rm -f %{buildroot}%{_cups_serverbin}/filter/hpps

# The systray applet doesn't work properly (displays icon as a
# window), so don't ship the launcher yet.
rm -rf %{buildroot}%{_sysconfdir}/xdg

# as there is no devel package we don't ship the *.a files either
rm -f  %{buildroot}%{_libdir}/*.a \
       %{buildroot}%{python_sitearch}/*.a

%files
%doc COPYING doc/*
# ex-hpijs
%{_bindir}/hpijs.exe
# ex-hpijs
#%{_bindir}/hpcups-update-ppds
%{_bindir}/hp-align
%{_bindir}/hp-clean
%{_bindir}/hp-colorcal
%{_bindir}/hp-config_usb_printer
%{_bindir}/hp-diagnose_plugin
%{_bindir}/hp-diagnose_queues
%{_bindir}/hp-fab
%{_bindir}/hp-firmware
%{_bindir}/hp-info
%{_bindir}/hp-levels
%{_bindir}/hp-makeuri
%{_bindir}/hp-plugin
%{_bindir}/hp-probe
%{_bindir}/hp-query
%{_bindir}/hp-scan
%{_bindir}/hp-sendfax
%{_bindir}/hp-setup
%{_bindir}/hp-testpage
%{_bindir}/hp-timedate
%{_bindir}/hp-unload
%{_cups_serverbin}/backend/*.exe
# ex-hpijs
%{_cups_serverbin}/filter/*.exe
%{_cups_serverbin}/filter/pstotiff
# ex-hpijs
%{_datadir}/cups/drv/*
%if 0%{!?without_fax:1}
%{_datadir}/cups/mime/pstotiff.convs
%endif
# Files
%{_datadir}/hplip/align.py*
%{_datadir}/hplip/check-plugin.py*
%{_datadir}/hplip/clean.py*
%{_datadir}/hplip/colorcal.py*
%{_datadir}/hplip/config_usb_printer.py*
%{_datadir}/hplip/diagnose_plugin.py*
%{_datadir}/hplip/diagnose_queues.py*
%{_datadir}/hplip/fab.py*
%if 0%{!?without_fax:1}
%{_datadir}/hplip/fax
%endif
%{_datadir}/hplip/firmware.py*
%{_datadir}/hplip/hpdio.py*
%{_datadir}/hplip/hplip_clean.sh
%{_datadir}/hplip/hpssd*
%{_datadir}/hplip/info.py*
%{_datadir}/hplip/__init__.py*
%{_datadir}/hplip/levels.py*
%{_datadir}/hplip/makeuri.py*
%{_datadir}/hplip/plugin.py*
%{_datadir}/hplip/probe.py*
%{_datadir}/hplip/query.py*
%{_datadir}/hplip/scan.py*
%{_datadir}/hplip/sendfax.py*
%{_datadir}/hplip/setup.py*
%{_datadir}/hplip/testpage.py*
%{_datadir}/hplip/timedate.py*
%{_datadir}/hplip/unload.py*
# Directories
%{_datadir}/hplip/base
%{_datadir}/hplip/copier
%{_datadir}/hplip/data/ldl
%{_datadir}/hplip/data/localization
%{_datadir}/hplip/data/pcl
%{_datadir}/hplip/data/ps
%{_datadir}/hplip/installer
%{_datadir}/hplip/pcard
%{_datadir}/hplip/prnt
%if 0%{!?without_sane:1}
%{_datadir}/hplip/scan
%endif
%{_datadir}/ppd
#%{_sharedstatedir}/hp
%dir %attr(0775,root,lp) %{_localstatedir}/run/hplip
#%{_tmpfilesdir}/hplip.conf
%{_sysconfdir}/udev/rules.d/56-hpmud.rules

%files common
%license COPYING
%dir %{_sysconfdir}/hp
%config(noreplace) %{_sysconfdir}/hp/hplip.conf
%dir %{_datadir}/hplip
%dir %{_datadir}/hplip/data
%{_datadir}/hplip/data/models

%files libs
%{_libdir}/hpip*.dll
#%{_libdir}/hpdis*.dll
%{_libdir}/hpmud*.dll
# Python extension
%{python_sitearch}/*.dll

%files gui
%{_bindir}/hp-check
%{_bindir}/hp-devicesettings
%{_bindir}/hp-faxsetup
%{_bindir}/hp-linefeedcal
%{_bindir}/hp-makecopies
%{_bindir}/hp-print
%{_bindir}/hp-printsettings
%{_bindir}/hp-systray
%{_bindir}/hp-toolbox
%{_bindir}/hp-wificonfig
#%{_datadir}/applications/*.desktop
# Files
%{_datadir}/hplip/check.py*
%{_datadir}/hplip/devicesettings.py*
%{_datadir}/hplip/faxsetup.py*
%{_datadir}/hplip/linefeedcal.py*
%{_datadir}/hplip/makecopies.py*
%{_datadir}/hplip/print.py*
%{_datadir}/hplip/printsettings.py*
%{_datadir}/hplip/systray.py*
%{_datadir}/hplip/toolbox.py*
%{_datadir}/hplip/wificonfig.py*
# Directories
%{_datadir}/hplip/data/images
%{_datadir}/hplip/ui4

%if 0%{!?without_sane:1}
%files -n libsane-hpaio
%{_libdir}/sane/sane-*.dll
%config(noreplace) %{_sysconfdir}/sane.d/dll.d/hpaio
%endif

%post
#%{_bindir}/hpcups-update-ppds &>/dev/null ||:

#%post libs -p /sbin/ldconfig

#%postun libs -p /sbin/ldconfig

%changelog
* Thu Jan 25 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.17.11-1
- changed the way python finds USER and HOME env
- moved source to github
- updated to version 3.17.11

* Tue Mar 21 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.16.11-1
- fix gui Requires
- use new scm_ macros
- update to version 3.16.11

* Mon Jun 13 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.16.3-1
- initial port
