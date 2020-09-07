# we don't want to provide private python extension libs
%{?filter_setup:
%filter_provides_in %{python2_sitearch}/.*\.so$
%filter_setup
}

%define without_dbus 1
%define without_fax 1

Summary: HP Linux Imaging and Printing Project
Name: hplip
Version: 3.19.8
Release: 3%{?dist}
License: GPLv2+ and MIT and BSD and IJG and Public Domain and GPLv2+ with exceptions and ISC

Url: https://developers.hp.com/hp-linux-imaging-and-printing
Vendor: bww bitwise works GmbH
#scm_source github  https://github.com/bitwiseworks/%{name}-os2 %{version}-os2-2
%scm_source git e:/trees/hplip/git master

# @todo: decide if we need that to
# if we do it as well, also remove the comment in the post section
%if !0%{?os2_version}
Source1: hpcups-update-ppds.sh
%endif

Requires: %{name}-libs = %{version}-%{release}
#Requires: python3-pillow
Requires: cups
Requires: wget
%if 0%{!?without_dbus:1}
Requires: python3-dbus
%endif
# set require directly to /usr/bin/gpg, because gnupg2 and gnupg ships it,
# but gnupg will be deprecated in the future
%if !0%{?os2_version}
Requires: %{_bindir}/gpg
# /usr/lib/udev/rules.d
Requires: systemd
%endif
# 1733449 - Scanner on an HP AIO printer is not detected unless libsane-hpaio is installed
Requires: libsane-hpaio
# require coreutils, because timeout binary is needed in post scriptlet,
# because hpcups-update-ppds script can freeze in certain situation and
# stop the update
Requires(post): coreutils

# gcc and gcc-c++ are no longer in buildroot by default

# gcc is needed for compilation of HPAIO scanning backend, HP implementation of
# IPP and MDNS protocols, hpps driver, hp backend, hpip (image processing 
# library), multipoint transport driver hpmud
BuildRequires: gcc
# gcc-c++ is needed for hpijs, hpcups drivers
BuildRequires: gcc-c++

BuildRequires: autoconf automake libtool
BuildRequires: net-snmp-devel
BuildRequires: cups-devel
BuildRequires: python-devel
BuildRequires: libjpeg-devel
%if !0%{?os2_version}
BuildRequires: desktop-file-utils
%endif
BuildRequires: libusb1-devel
BuildRequires: openssl-devel
BuildRequires: sane-backends-devel
%if 0%{!?without_dbus:1}
BuildRequires: pkgconfig(dbus-1)
%endif

# Make sure we get postscriptdriver tags - need cups and python3-cups.
BuildRequires: cups
%if !0%{?os2_version}
BuildRequires: python3-cups
%endif

# macros: %%{_tmpfilesdir}, %%{_udevrulesdir}
%if !0%{?os2_version}
BuildRequires: systemd
%endif

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

%description libs
Libraries needed by HPLIP.

%package gui
Summary: HPLIP graphical tools
License: BSD
%if !0%{?os2_version}
BuildRequires: libappstream-glib
%endif
Requires: python2-PyQt4
%if !0%{?os2_version}
Requires: python3-reportlab
# hpssd.py
Requires: python3-gobject
%endif
Requires: %{name} = %{version}-%{release}
Requires: libsane-hpaio = %{version}-%{release}

%description gui
HPLIP graphical tools.

%package -n libsane-hpaio
Summary: SANE driver for scanners in HP's multi-function devices
License: GPLv2+
Requires: sane-backends
Requires: %{name}-libs = %{version}-%{release}

%description -n libsane-hpaio
SANE driver for scanners in HP's multi-function devices (from HPOJ).

%debug_package

%prep
%scm_setup

sed -i.duplex-constraints \
    -e 's,\(UIConstraints.* \*Duplex\),//\1,' \
    prnt/drv/hpcups.drv.in

# Change shebang /usr/bin/env python -> /usr/bin/python3 (bug #618351).
find -name '*.py' -print0 | xargs -0 \
    sed -i.env-python -e 's,^#!/usr/bin/env python,#!%{__python2},'
sed -i.env-python -e 's,^#!/usr/bin/env python,#!%{__python2},' \
    prnt/filters/hpps \
    fax/filters/pstotiff

rm locatedriver

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
        --enable-scan-build \
        --enable-gui-build \
%if 0%{!?without_fax:1}
        --enable-fax-build \
%else
        --enable-fax-build=no \
%endif
        --disable-foomatic-rip-hplip-install \
        --enable-qt4 \
        --enable-hpcups-install --enable-cups-drv-install \
        --enable-foomatic-drv-install \
        --enable-hpijs-install \
%if 0%{?without_dbus:1}
        --enable-dbus-build=no \
%endif
        --disable-policykit --with-mimedir=%{_datadir}/cups/mime \
        --enable-shared --disable-static \
        --with-cupsbackenddir=%{_cups_serverbin}/backend \
        --with-cupsfilterdir=%{_cups_serverbin}/filter \
        --with-icondir=%{_datadir}/applications \
        --with-systraydir=%{_sysconfdir}/xdg/autostart

make %{?_smp_mflags}


%install
mkdir -p %{buildroot}%{_bindir}
make install DESTDIR=%{buildroot}

# Create /run/hplip & /var/lib/hp
mkdir -p %{buildroot}%{_localstatedir}/run/hplip
mkdir -p %{buildroot}%{_localstatedir}/lib/hp

# Remove unpackaged files
rm -rf  %{buildroot}%{_sysconfdir}/sane.d \
        %{buildroot}%{_docdir} \
        %{buildroot}%{_datadir}/hal \
        %{buildroot}%{_datadir}/hplip/pkservice.py \
        %{buildroot}%{_bindir}/hp-pkservice \
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
        %{buildroot}%{_datadir}/applications/hplip.desktop \
        %{buildroot}%{_datadir}/ppd/HP/*.ppd


# Regenerate hpcups PPDs on upgrade if necessary (bug #579355).
%if !0%{?os2_version}
install -p -m755 %{SOURCE1} %{buildroot}%{_bindir}/hpcups-update-ppds
%endif

%{__mkdir_p} %{buildroot}%{_sysconfdir}/sane.d/dll.d
echo hpaio > %{buildroot}%{_sysconfdir}/sane.d/dll.d/hpaio

# Images in docdir should not be executable (bug #440552).
find doc/images -type f -exec chmod 644 {} \;

# Create an empty plugins directory to make sure it gets the right
# SELinux file context (bug #564551).
%{__mkdir_p} %{buildroot}%{_datadir}/hplip/prnt/plugins

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
rm -f %{buildroot}%{_unitdir}/hplip-printer@.service
rm -rf %{buildroot}%{_libdir}/systemd
rm -rf %{buildroot}%{_datadir}/applications
# we don't need the exe and the python version of hpps, we remove the python version
rm -f %{buildroot}%{_cups_serverbin}/filter/hpps

# The systray applet doesn't work properly (displays icon as a
# window), so don't ship the launcher yet.
rm -rf %{buildroot}%{_sysconfdir}/xdg/autostart/hplip-systray.desktop

# as there is no devel package we don't ship the *.a files either
rm -f  %{buildroot}%{_libdir}/*.a \
       %{buildroot}%{_libdir}/sane/*.a \
       %{buildroot}%{python_sitearch}/*.a

# hp-setup needs to have cups service enabled and running for setups of queues
%pre
%if !0%{?os2_version}
%{_bindir}/systemctl start cups &>/dev/null ||:
%{_bindir}/systemctl enable cups &>/dev/null ||:
%endif

%post
# timeout is to prevent possible freeze during update
%if !0%{?os2_version}
%{_bindir}/timeout 10m -k 15m %{_bindir}/hpcups-update-ppds &>/dev/null ||:
%endif

%if !0%{?os2_version}
ldconfig_scriptlets libs
%endif

%files
%doc COPYING doc/*
# ex-hpijs
%{_bindir}/hpijs.exe
# ex-hpijs
%if !0%{?os2_version}
%{_bindir}/hpcups-update-ppds
%endif
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
%{_cups_serverbin}/backend/hp.exe
%if 0%{!?without_fax:1}
%{_cups_serverbin}/backend/hpfax.exe
%endif
# ex-hpijs
%{_cups_serverbin}/filter/hpcups.exe
%if 0%{!?without_fax:1}
%{_cups_serverbin}/filter/hpcupsfax.exe
%endif
%{_cups_serverbin}/filter/hpps.exe
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
%{_datadir}/hplip/scan
%{_datadir}/ppd
%{_localstatedir}/lib/hp
%dir %attr(0775,root,lp) %{_localstatedir}/run/hplip
%if !0%{?os2_version}
%{_tmpfilesdir}/hplip.conf
%endif
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
%{_libdir}/hpdis*.dll
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
%{_bindir}/hp-uiscan
%{_bindir}/hp-wificonfig
%if !0%{?os2_version}
%{_datadir}/applications/*.desktop
%endif
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
%{_datadir}/hplip/uiscan.py*
%{_datadir}/hplip/wificonfig.py*
# Directories
%{_datadir}/hplip/data/images
%{_datadir}/hplip/ui4

%files -n libsane-hpaio
%{_libdir}/sane/hpaio*.dll
%config(noreplace) %{_sysconfdir}/sane.d/dll.d/hpaio

%changelog
* Wed Sep 02 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.19.8-3
- enable net-snmp

* Wed Jan 15 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.19.8-2
- enable sane-backends

* Wed Oct 02 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.19.8-1
- update to version 3.19.8

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
