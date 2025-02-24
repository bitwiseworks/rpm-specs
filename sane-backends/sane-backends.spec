# let -devel require drivers to make them available as multilib
%if !0%{?os2_version}
%global needs_multilib_quirk 1
%else
%global needs_multilib_quirk 0
%endif

%global _hardened_build 1

%global libusb1 1

%global __provides_exclude_from ^%{_libdir}/sane/.*\.so.*$
%global __requires_exclude ^libsane-.*\.so\.[0-9]*(\(\).*)?+$

%global _maindocdir %{_docdir}/%{name}
%global _docdocdir %{_docdir}/%{name}-doc

%global scanner_backends_list abaton agfafocus apple artec artec_eplus48u as6e avision bh canon canon630u canon_dr canon_lide70 canon_pp cardscan coolscan coolscan2 coolscan3 dell1600n_net dll epjitsu epson epson2 epsonds fujitsu genesys gt68xx hp hp3500 hp3900 hp4200 hp5400 hp5590 hpljm1005 hpsj5s hs2p ibm kodak kodakaio kvs1025 kvs20xx kvs40xx leo lexmark lexmark_x2600 ma1509 magicolor matsushita microtek microtek2 mustek mustek_pp mustek_usb mustek_usb2 nec net niash p5 pie pieusb pixma plustek plustek_pp ricoh ricoh2 rts8891 s9036 sceptre sharp sm3600 sm3840 snapscan sp15c st400 tamarack teco1 teco2 teco3 test u12 umax umax1220u umax_pp xerox_mfp
%global camera_backends_list dc210 dc240 dc25 dmc gphoto2 qcam stv680 v4l
%global config_files_list abaton agfafocus apple artec artec_eplus48u avision bh canon canon630u canon_dr canon_lide70 canon_pp cardscan coolscan coolscan2 coolscan3 dell1600n_net dll epjitsu epson epson2 epsonds fujitsu genesys gt68xx hp hp3900 hp4200 hp5400 hpsj5s hs2p ibm kodak kodakaio kvs1025 leo lexmark lexmark_x2600 ma1509 magicolor matsushita microtek microtek2 mustek mustek_pp mustek_usb nec net p5 pie pieusb pixma plustek plustek_pp ricoh rts8891 s9036 sceptre sharp sm3840 snapscan sp15c st400 tamarack teco1 teco2 teco3 test u12 umax umax1220u umax_pp xerox_mfp dc210 dc240 dc25 dmc gphoto2 qcam stv680 v4l

%if 0%{?flatpak} || 0%{?os2_version}
%bcond_with runtimedep_systemd
%else
%bcond_without runtimedep_systemd
%endif

Summary: Scanner access software
Name: sane-backends
Version: 1.3.1
Release: 1%{?dist}
# backend/coolscan*, backend/epson2*, backend/epsonds*, backend/magicolor*, backend/kodakaio* -
# GPL-2.0-only
# backend/qcam* - MIT AND GPL-2.0-or-later WITH SANE-exception
# include/sane.h,sanei_net.h,sanei_tcp.h,sanei_udp.h - LicenseRef-Fedora-Public-Domain
# sanei/sanei_jpeg.c - IJG
# sanei/*, backend/*, include/*, japi/* - GPL-2.0-or-later WITH SANE-exception
# frontend/*, tools/* - GPL-2.0-or-later
# lib/* - LGPL-2.0-or-later, LGPL-2.1-or-later (copied from glibc, remove in the future...)
# !DISABLED DURING CONFIGURE, thus not in License tag! backend/escl* - GPL-3.0-or-later
License: GPL-2.0-or-later WITH SANE-exception AND GPL-2.0-or-later AND GPL-2.0-only AND LGPL-2.0-or-later AND LGPL-2.1-or-later AND LicenseRef-Fedora-Public-Domain AND IJG AND MIT
# GitLab Download URLs are amazing. But the source code link has different name and doesnt have generated autotools stuff
%if !0%{?os2_version}
Source0: https://gitlab.com/sane-project/backends/uploads/104f09c07d35519cc8e72e604f11643f/%{name}-%{version}.tar.gz

Source1: sane.png
Source2: saned.socket
Source3: saned@.service.in
Source4: README.Fedora
Source5: 66-saned.rules
Source6: sane-backends.sysusers

# Fedora-specific, probably not generally applicable:
Patch0: sane-backends-1.0.25-udev.patch
# Fedora-specific (for now): don't use the same SONAME for backend libs and
# main lib
Patch1: sane-backends-1.0.23-soname.patch
# Fedora-specific (for now): make installed sane-config multi-lib aware again
Patch2: sane-backends-1.0.23-sane-config-multilib.patch
# https://gitlab.com/sane-project/backends/-/merge_requests/862
Patch3: backends-gcc15-bool-kw.patch
%else
%scm_source github http://github.com/bitwiseworks/sane-backend-os2 %{version}-os2
Vendor: bww bitwise works GmbH
%endif

URL: http://www.sane-project.org

# we need autoconf during build
BuildRequires: autoconf
# AX_CXX_COMPILE_STDCXX_11 in configure
BuildRequires: autoconf-archive
# needs aclocal-1.16 during build
BuildRequires: automake
BuildRequires: gettext
# gcc is no longer in buildroot by default
BuildRequires: gcc
# genesys backend is written in C++, so it is needed as buildrequire
BuildRequires: gcc-c++
# for autosetup
BuildRequires: git-core
%if !0%{?os2_version}
BuildRequires: gphoto2-devel
BuildRequires: texlive-base
BuildRequires: libieee1284-devel
%endif
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: libtiff-devel
%if %libusb1
%if !0%{?os2_version}
BuildRequires: libusbx-devel
%else
BuildRequires: libusb1-devel
%endif
%else
BuildRequires: libusb-devel
%endif
%if !0%{?os2_version}
BuildRequires: libv4l-devel
%endif
# uses make
BuildRequires: make
# pixma backend generates header files during build via python script
BuildRequires: python3
%if !0%{?os2_version}
BuildRequires: systemd-devel
BuildRequires: systemd
# needed by macros in rpm scriptlets
BuildRequires: systemd-rpm-macros
%endif

Requires: libpng
%if !0%{?os2_version}
Requires: sane-airscan
Requires: sane-backends-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
%else
Requires: sane-backends-libs = %{?epoch:%{epoch}:}%{version}-%{release}
%endif
%if %{with runtimedep_systemd}
Requires: systemd >= 196
Requires: systemd-udev >= 196
%endif

# workaround for Brother scanners, which drivers are built with old libnsl
# it is ignored by DNF, but it seems GUI installation apps should offer it
# if it is not installed, it leads to crashes like #1778425
Suggests: libnsl

%description
Scanner Access Now Easy (SANE) is a universal scanner interface.  The
SANE application programming interface (API) provides standardized
access to any raster image scanner hardware (flatbed scanner,
hand-held scanner, video and still cameras, frame-grabbers, etc.).

%package doc
Summary: SANE backends documentation
BuildArch: noarch

%description doc
This package contains documentation for SANE backends.

%package libs
Summary: SANE libraries
%if !0%{?os2_version}
Recommends: %{name}-drivers-cameras%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Recommends: %{name}-drivers-scanners%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
%else
Recommends: %{name}-drivers-scanners = %{?epoch:%{epoch}:}%{version}-%{release}
%endif

%description libs
This package contains the SANE libraries which are needed by applications that
want to access scanners.

%package devel
Summary: SANE development toolkit
%if !0%{?os2_version}
Requires: libieee1284-devel
%endif
Requires: libjpeg-devel
Requires: libtiff-devel
%if %libusb1
%if !0%{?os2_version}
Requires: libusbx-devel
%else
Requires: libusb1-devel
%endif
%else
Requires: libusb-devel
%endif
Requires: pkgconfig
Requires: sane-backends = %{?epoch:%{epoch}:}%{version}-%{release}
%if %needs_multilib_quirk
Requires: sane-backends-drivers-scanners%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: sane-backends-drivers-cameras%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
%endif
%if !0%{?os2_version}
Requires: sane-backends-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
%else
Requires: sane-backends-libs = %{?epoch:%{epoch}:}%{version}-%{release}
%endif

%description devel
This package contains libraries and header files for writing Scanner Access Now
Easy (SANE) modules.

%package drivers-scanners
Summary: SANE backend drivers for scanners
# pixma backend now requires libxml2
BuildRequires: libxml2-devel
# due move of camera backends
Conflicts: %{name}-drivers-cameras < 1.1.1-4
Requires: sane-backends = %{?epoch:%{epoch}:}%{version}-%{release}
%if !0%{?os2_version}
Requires: sane-backends-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
%else
Requires: sane-backends-libs = %{?epoch:%{epoch}:}%{version}-%{release}
%endif

%description drivers-scanners
This package contains backend drivers to access scanner hardware through SANE.

%if !0%{?os2_version}
%package drivers-cameras
Summary: Scanner backend drivers for digital cameras
# due move of camera backends
Conflicts: %{name}-drivers-scanners < 1.1.1-4
Requires: sane-backends = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: sane-backends-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description drivers-cameras
This package contains backend drivers to access digital cameras through SANE.
%endif

%package daemon
Summary: Scanner network daemon
Requires: sane-backends = %{?epoch:%{epoch}:}%{version}-%{release}
%if !0%{?os2_version}
Requires: sane-backends-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
%else
Requires: sane-backends-libs = %{?epoch:%{epoch}:}%{version}-%{release}
%endif

%description daemon
This package contains saned which is the daemon that allows remote clients to
access image acquisition devices available on the local host.

%if 0%{?os2_version}
%debug_package
%endif


%prep
%if !0%{?os2_version}
%autosetup -S git
%else
%scm_setup
# create a .tarball-version file
echo %{version} >.tarball-version
sh autogen.sh
%endif

%build
%if 0%{?os2_version}
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -fstack-protector"
export LIBS="-lcx -lpthread"
export VENDOR="%{vendor}"
%endif

CFLAGS="%optflags -fno-strict-aliasing"
%if ! 0%{?_hardened_build}
# use PIC/PIE because SANE-enabled software is likely to deal with data coming
# from untrusted sources (client <-> saned via network)
CFLAGS="$CFLAGS -fPIC"
LDFLAGS="-pie"
%endif
%configure \
%if !0%{?os2_version}
    --with-gphoto2=%{_prefix} \
%endif
    --with-docdir=%{_maindocdir} \
%if !0%{?os2_version}
    --with-systemd \
%endif
    --disable-locking --disable-rpath \
%if %libusb1
    --with-usb \
%endif
%if 0%{?os2_version}
    --disable-ipv6 \
%endif
    --enable-pthread
%make_build

%if !0%{?os2_version}
# Write udev/hwdb files
_topdir="$PWD"
pushd tools
./sane-desc -m udev+hwdb -s "${_topdir}/doc/descriptions:${_topdir}/doc/descriptions-external" -d0 > udev/sane-backends.rules
./sane-desc -m hwdb -s "${_topdir}/doc/descriptions:${_topdir}/doc/descriptions-external" -d0 > udev/sane-backends.hwdb

popd
%endif

%install
%make_install

%if !0%{?os2_version}
mkdir -p %{buildroot}%{_datadir}/pixmaps
install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/pixmaps
rm -f %{buildroot}%{_bindir}/gamma4scanimage
%else
rm -f %{buildroot}%{_bindir}/gamma4scanimage.exe
%endif
rm -f %{buildroot}%{_mandir}/man1/gamma4scanimage.1*
%if !0%{?os2_version}
rm -f %{buildroot}%{_libdir}/sane/*.a %{buildroot}%{_libdir}/*.a
%else
rm -f %{buildroot}%{_libdir}/sane/*.a
%endif
rm -f %{buildroot}%{_libdir}/libsane*.la %{buildroot}%{_libdir}/sane/*.la

%if !0%{?os2_version}
mkdir -p %{buildroot}%{_udevrulesdir}
mkdir -p %{buildroot}%{_udevhwdbdir}
install -m 0644 tools/udev/sane-backends.rules %{buildroot}%{_udevrulesdir}/65-sane-backends.rules
install -m 0644 tools/udev/sane-backends.hwdb %{buildroot}%{_udevhwdbdir}/20-sane-backends.hwdb
install -m 0644 %{SOURCE5} %{buildroot}%{_udevrulesdir}/66-saned.rules
%endif

mkdir -p %{buildroot}%{_libdir}/pkgconfig
install -m 0644 tools/sane-backends.pc %{buildroot}%{_libdir}/pkgconfig/

%if 0%{?os2_version}
_topdir="$PWD"
%endif
mkdir %{buildroot}%{_docdocdir}
%if !0%{?os2_version}
pushd %{buildroot}%{_maindocdir}
%else
cd %{buildroot}%{_maindocdir}
%endif
for f in *; do
    if [ -d "$f" ]; then
        mv "$f" "%{buildroot}%{_docdocdir}/${f}"
    else
        case "$f" in
        AUTHORS|ChangeLog|COPYING|LICENSE|NEWS|PROBLEMS|README|README.linux)
            ;;
        backend-writing.txt|PROJECTS|sane-*.html)
            mv "$f" "%{buildroot}%{_docdocdir}/${f}"
            ;;
        *)
            rm -rf "$f"
            ;;
        esac
    fi
done
%if !0%{?os2_version}
popd
%else
cd ${_topdir}
%endif

%if !0%{?os2_version}
install -m 644 %{SOURCE4} %{buildroot}%{_maindocdir}

install -m 755 -d %{buildroot}%{_unitdir}
install -m 644 %{SOURCE2} %{buildroot}%{_unitdir}
sed 's|@CONFIGDIR@|%{_sysconfdir}/sane.d|g' < %{SOURCE3} > saned@.service
install -m 644 saned@.service %{buildroot}%{_unitdir}

install -p -D -m 0644 %{SOURCE6} %{buildroot}%{_sysusersdir}/sane-backends.conf
%endif

%ifarch armv7hl
rm -f %{buildroot}%{_libdir}/sane/libsane-qcam.so
%endif

%find_lang %name

%if !0%{?os2_version}
touch so_scanner_list
for backend in %scanner_backends_list
do
  echo "%{_libdir}/sane/libsane-${backend}.so" >> so_scanner_list
done

touch so_camera_list
for backend in %camera_backends_list
do
  if [ "$backend" == "qcam" ]
  then
    continue
  fi
  echo "%{_libdir}/sane/libsane-${backend}.so" >> so_camera_list
done

touch config_list
for config in %config_files_list
do
  if [ "$config" == "epsonds" ] || [ "$config" == "qcam" ]
  then
    continue
  fi
  echo "%config(noreplace) %{_sysconfdir}/sane.d/${config}.conf" >> config_list
done
%endif

%post
%if !0%{?os2_version}
udevadm hwdb --update >/dev/null 2>&1 || :

# check if there is autodiscovery enabled in epsonds.conf
autodiscovery=`%{_bindir}/grep -E '^[[:space:]]*net[[:space:]]*autodiscovery' /etc/sane.d/epsonds.conf`
if [ -n "$autodiscovery" ]
then
  # comment out 'net autodiscovery' if it is not commented out
  %{_bindir}/sed -i 's,^[[:space:]]*net[[:space:]]*autodiscovery,#net autodiscovery,g' /etc/sane.d/epsonds.conf
fi
%endif

%postun
%if !0%{?os2_version}
udevadm hwdb --update >/dev/null 2>&1 || :
%endif

%if !0%{?os2_version}
%ldconfig_scriptlets libs
%endif

%pre daemon
%if !0%{?os2_version}
%sysusers_create_compat %{SOURCE6}
%else
groupadd -r saned
useradd -r -g saned -d %{_datadir}/sane -s /sbin/nologin \
		-c "SANE scanner daemon user" saned
exit 0
%endif

%post daemon
%if !0%{?os2_version}
%systemd_post saned.socket
%endif

%preun daemon
%if !0%{?os2_version}
%systemd_preun saned.socket
%endif

%postun daemon
%if !0%{?os2_version}
%systemd_postun_with_restart saned.socket
%endif

%if !0%{?os2_version}
%files -f %{name}.lang -f config_list
%else
%files -f %{name}.lang
%endif
%dir %{_maindocdir}
%doc %{_maindocdir}/AUTHORS
%doc %{_maindocdir}/ChangeLog
%doc %{_maindocdir}/NEWS
%doc %{_maindocdir}/PROBLEMS
%doc %{_maindocdir}/README*
%license %{_maindocdir}/COPYING
%license %{_maindocdir}/LICENSE
%dir %{_sysconfdir}/sane.d
%dir %{_sysconfdir}/sane.d/dll.d
%if !0%{?os2_version}
# 2130997 - epsonds.conf is modified during %post scriptlet to disable autodiscovery for
# security reasons, so disable RPM verification of it for size, md5 and modification time
%config(noreplace) %verify(not size md5 mtime) %{_sysconfdir}/sane.d/epsonds.conf
%ifarch x86_64 i686
%config(noreplace) %{_sysconfdir}/sane.d/qcam.conf
%endif
%else
%config(noreplace) %{_sysconfdir}/sane.d/*.conf
%endif
%if !0%{?os2_version}
%{_udevrulesdir}/65-sane-backends.rules
%{_udevhwdbdir}/20-sane-backends.hwdb
%{_datadir}/pixmaps/sane.png
%endif

%if !0%{?os2_version}
%{_bindir}/sane-find-scanner
%{_bindir}/scanimage
%{_bindir}/umax_pp
%else
%{_bindir}/sane-find-scanner.exe
%{_bindir}/scanimage.exe
%{_bindir}/umax_pp.exe
%endif

%exclude %{_mandir}/man1/sane-config.1*
%exclude %{_mandir}/man8/saned*
%{_mandir}/*/*

%dir %{_libdir}/sane
%dir %{_datadir}/sane

%files doc
%doc %{_docdocdir}

%files libs
%if !0%{?os2_version}
%{_libdir}/libsane.so.1
%{_libdir}/libsane.so.1.*
%else
%{_libdir}/sane*.dll
%endif

%files devel
%{_bindir}/sane-config
%{_mandir}/man1/sane-config.1*
%{_includedir}/sane
%if !0%{?os2_version}
%{_libdir}/libsane.so
%else
%{_libdir}/sane*_dll.a
%endif
%{_libdir}/pkgconfig/sane-backends.pc

%if !0%{?os2_version}
%files drivers-scanners -f so_scanner_list
# #1761145 can happen - genesys did not compile because of lack gcc-c++ in buildroot
# and configure printed only warning. So now we can figure out missing backend support
# during build
%{_libdir}/sane/*.so.1
%{_libdir}/sane/*.so.1.*
%else
%files drivers-scanners
# we need to specify all .so files for available backends because something like
# not on os2, as too much hassle
# I'll leave here a wildcard record
%{_libdir}/sane/*.dll
%exclude %{_libdir}/sane*.dll
%endif

%if !0%{?os2_version}
%exclude %{_libdir}/sane/*dc210.so*
%exclude %{_libdir}/sane/*dc240.so*
%exclude %{_libdir}/sane/*dc25.so*
%exclude %{_libdir}/sane/*dmc.so*
%exclude %{_libdir}/sane/*gphoto2.so*
%exclude %{_libdir}/sane/*qcam.so*
%exclude %{_libdir}/sane/*stv680.so*
%exclude %{_libdir}/sane/*v4l.so*
%endif

%if !0%{?os2_version}
%files drivers-cameras -f so_camera_list
# qcam is not on aarch64, ppc64le and s390x. SANE needs
# ioperm, inb and outb functions or portaccess function
# to support qcam backend. Those functions are only in
# armv7hl (until F30), i686 and x86_64 architectures.
# Because qcam is missing on some archs and releases,
# I'll leave here a wildcard record
%ifarch x86_64 i686
%{_libdir}/sane/libsane-qcam.so
%endif
%{_libdir}/sane/*.so.1
%{_libdir}/sane/*.so.1.*
%endif

%files daemon
%if !0%{?os2_version}
%{_sbindir}/saned
%else
%{_sbindir}/saned.exe
%endif
%{_mandir}/man8/saned*
%if !0%{?os2_version}
%config(noreplace) %{_sysconfdir}/sane.d/saned.conf
%{_udevrulesdir}/66-saned.rules
%{_sysusersdir}/sane-backends.conf
%{_unitdir}/saned.socket
%{_unitdir}/saned@.service
%endif

%changelog
* Mon Dec 23 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.3.1-1
- upate to version 1.3.1
- resync with fedora spec

* Mon Dec 23 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.0.28-2
- rebuild with net-snmp enabled

* Mon Dec 23 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.0.28-1
- initial OS/2 rpm
