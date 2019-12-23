# let -devel require drivers to make them available as multilib
%global needs_multilib_quirk 0

%if !0%{?fedora}%{?rhel} || 0%{?fedora} >= 16 || 0%{?rhel} >= 7
%global _hardened_build 1
%endif

%if !0%{?fedora}%{?rhel} || 0%{?fedora} >= 17 || 0%{?rhel} >= 7
%global udevdir %{_prefix}/lib/udev
%else
%global udevdir /lib/udev
%endif
%global udevrulesdir %{udevdir}/rules.d
%global udevhwdbdir %{udevdir}/hwdb.d

%if !0%{?fedora}%{?rhel} || 0%{?fedora} >= 18 || 0%{?rhel} >= 7
%global libusb1 1
%else
%global libusb1 0
%endif

%global __provides_exclude_from ^%{_libdir}/sane/.*\.so.*$
%global __requires_exclude ^libsane-.*\.so\.[0-9]*(\(\).*)?+$

%if ! 0%{?fedora}%{?rhel} || 0%{?fedora} >= 20 || 0%{?rhel} >= 8
%global _maindocdir %{_docdir}/%{name}
%global _docdocdir %{_docdir}/%{name}-doc
%else
%global _maindocdir %{_docdir}/%{name}-%{version}
%global _docdocdir %{_docdir}/%{name}-doc-%{version}
%endif

%global with_ieee1284 0
%global with_libv4l 0
%global with_gphoto2 0
%global with_systemd 0

Summary: Scanner access software
Name: sane-backends
Version: 1.0.28
Release: 1%{?dist}
# lib/ is LGPLv2+, backends are GPLv2+ with exceptions
# Tools are GPLv2+, docs are public domain
# see LICENSE for details
License: GPLv2+ and GPLv2+ with exceptions and Public Domain and IJG and LGPLv2+ and MIT
# Alioth Download URLs are amazing.
#scm_source github http://github.com/bitwiseworks/sane-backend-os2 %{version}-os2
%scm_source git e:/trees/libsane/git master-os2
Vendor: bww bitwise works GmbH

URL: http://www.sane-project.org

# gcc is no longer in buildroot by default
BuildRequires: gcc
# genesys backend is not written in C++, so it is needed as buildrequire
#BuildRequires: gcc-c++

#BuildRequires: %{_bindir}/latex
%if %libusb1
BuildRequires: libusb1-devel
%else
BuildRequires: libusb-devel
%endif
%if %{with_ieee1284}
BuildRequires: libieee1284-devel
%endif
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: libtiff-devel
%if %{with_libv4l}
BuildRequires: libv4l-devel
%endif
BuildRequires: gettext
%if %{with_gphoto2}
BuildRequires: gphoto2-devel
%endif
%if %{with_systemd}
BuildRequires: systemd-devel
BuildRequires: systemd
%endif
Requires: libpng
%if %{with_systemd}
Requires: systemd >= 196
Requires: systemd-udev >= 196
%endif
Requires: sane-backends-libs = %{?epoch:%{epoch}:}%{version}-%{release}
# Don't drag around obsoletes forever
%if ! (0%{?fedora} >= 27 || 0%{?rhel} >= 8)
Obsoletes: sane-backends < 1.0.25-3
Conflicts: sane-backends < 1.0.25-3
%endif

%description
Scanner Access Now Easy (SANE) is a universal scanner interface.  The
SANE application programming interface (API) provides standardized
access to any raster image scanner hardware (flatbed scanner,
hand-held scanner, video and still cameras, frame-grabbers, etc.).

%package doc
Summary: SANE backends documentation
BuildArch: noarch
# Don't drag around obsoletes forever
%if 0%{?fedora}%{?rhel} && (0%{?fedora} < 25 || 0%{?rhel} <= 8)
Obsoletes: sane-backends < 1.0.23-10
Conflicts: sane-backends < 1.0.23-10
%endif

%description doc
This package contains documentation for SANE backends.

%package libs
Summary: SANE libraries
Recommends: %{name}-drivers-cameras = %{?epoch:%{epoch}:}%{version}-%{release}
Recommends: %{name}-drivers-scanners = %{?epoch:%{epoch}:}%{version}-%{release}

%description libs
This package contains the SANE libraries which are needed by applications that
want to access scanners.

%package devel
Summary: SANE development toolkit
Requires: sane-backends = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: sane-backends-libs = %{?epoch:%{epoch}:}%{version}-%{release}
%if %needs_multilib_quirk
Requires: sane-backends-drivers-scanners = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: sane-backends-drivers-cameras = %{?epoch:%{epoch}:}%{version}-%{release}
%endif
%if %libusb1
Requires: libusb1-devel
%else
Requires: libusb-devel
%endif
%if %{with_ieee1284}
Requires: libieee1284-devel
%endif
Requires: libjpeg-devel
Requires: libtiff-devel
Requires: pkgconfig

%description devel
This package contains libraries and header files for writing Scanner Access Now
Easy (SANE) modules.

%package drivers-scanners
Summary: SANE backend drivers for scanners
Requires: sane-backends = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: sane-backends-libs = %{?epoch:%{epoch}:}%{version}-%{release}
# Don't drag around obsoletes forever
%if 0%{?rhel} && 0%{?rhel} < 8
Obsoletes: sane-backends < 1.0.22-4
Obsoletes: sane-backends-libs < 1.0.22-4
Conflicts: sane-backends < 1.0.22-4
Conflicts: sane-backends-libs < 1.0.22-4
%endif

%description drivers-scanners
This package contains backend drivers to access scanner hardware through SANE.

%if %{with_gphoto2}
%package drivers-cameras
Summary: Scanner backend drivers for digital cameras
Requires: sane-backends = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: sane-backends-libs = %{?epoch:%{epoch}:}%{version}-%{release}
# Don't drag around obsoletes forever
%if 0%{?rhel} && 0%{?rhel} < 8
Obsoletes: sane-backends-libs-gphoto2 < 1.0.22-4
Conflicts: sane-backends-libs-gphoto2 < 1.0.22-4
Provides: sane-libs-gphoto2 = %{?epoch:%{epoch}:}%{version}-%{release}
Provides: sane-libs-gphoto2 = %{?epoch:%{epoch}:}%{version}-%{release}
%endif

%description drivers-cameras
This package contains backend drivers to access digital cameras through SANE.
%endif

%package daemon
Summary: Scanner network daemon
Requires: sane-backends = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: sane-backends-libs = %{?epoch:%{epoch}:}%{version}-%{release}
#Requires(pre): shadow-utils
%{?systemd_requires}
# Split off saned from 1.0.25-3 on, don't drag around obsoletes forever
%if ! (0%{?fedora} >= 27 || 0%{?rhel} >= 8)
Obsoletes: sane-backends < 1.0.25-3
Conflicts: sane-backends < 1.0.25-3
%endif

%description daemon
This package contains saned which is the daemon that allows remote clients to
access image acquisition devices available on the local host.

%debug_package

%prep
%scm_setup
# we need to patch configure.ac here, as we are not in a git repo
sed -i "s/git describe --dirty/echo %{version}/" configure.ac
sh autogen.sh

%build
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx -lpthread"
export VENDOR="%{vendor}"

CFLAGS="%optflags -fno-strict-aliasing"
%if ! 0%{?_hardened_build}
# use PIC/PIE because SANE-enabled software is likely to deal with data coming
# from untrusted sources (client <-> saned via network)
CFLAGS="$CFLAGS -fPIC"
LDFLAGS="-pie"
%endif
%configure \
%if %{with_gphoto2}
    --with-gphoto2=%{_prefix} \
%endif
    --with-docdir=%{_maindocdir} \
%if %{with_systemd}
    --with-systemd \
%endif
    --disable-locking --disable-rpath \
%if %libusb1
    --with-usb \
%endif
    --enable-pthread \
    --disable-ipv6

make %{?_smp_mflags}

%if %{with_systemd}
# Write udev/hwdb files
_topdir="$PWD"
cd tools
./sane-desc -m udev+hwdb -s "${_topdir}/doc/descriptions;${_topdir}/doc/descriptions-external" -d0 > udev/sane-backends.rules
./sane-desc -m hwdb -s "${_topdir}/doc/descriptions;${_topdir}/doc/descriptions-external" -d0 > udev/sane-backends.hwdb

cd ..
%endif

%install
make DESTDIR="%{buildroot}" install

rm -f %{buildroot}%{_bindir}/gamma4scanimage.exe
rm -f %{buildroot}%{_mandir}/man1/gamma4scanimage.1*
#rm -f %{buildroot}%{_libdir}/sane/*.a %{buildroot}%{_libdir}/*.a
rm -f %{buildroot}%{_libdir}/sane/*.a
rm -f %{buildroot}%{_libdir}/libsane*.la %{buildroot}%{_libdir}/sane/*.la

%if %{with_systemd}
mkdir -p %{buildroot}%{udevrulesdir}
mkdir -p %{buildroot}%{udevhwdbdir}
install -m 0644 tools/udev/sane-backends.rules %{buildroot}%{udevrulesdir}/65-sane-backends.rules
install -m 0644 tools/udev/sane-backends.hwdb %{buildroot}%{udevhwdbdir}/20-sane-backends.hwdb
%endif

mkdir -p %{buildroot}%{_libdir}/pkgconfig
install -m 0644 tools/sane-backends.pc %{buildroot}%{_libdir}/pkgconfig/

_topdir="$PWD"
mkdir %{buildroot}%{_docdocdir}
cd %{buildroot}%{_maindocdir}
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
cd ${_topdir}

%find_lang %name

%post
%if %{with_systemd}
udevadm hwdb --update >/dev/null 2>&1 || :
%endif

%postun
%if %{with_systemd}
udevadm hwdb --update >/dev/null 2>&1 || :
%endif

#ldconfig_scriptlets libs

%pre daemon
#getent group saned >/dev/null || groupadd -r saned
groupadd -r saned
#getent passwd saned >/dev/null || \
    useradd -r -g saned -d %{_datadir}/sane -s /sbin/nologin \
		-c "SANE scanner daemon user" saned
exit 0

%post daemon
%if %{with_systemd}
%systemd_post saned.socket
%endif

%preun daemon
%if %{with_systemd}
%systemd_preun saned.socket
%endif

%postun daemon
%if %{with_systemd}
%systemd_postun saned.socket
%endif

%files -f %{name}.lang
%dir %{_maindocdir}
%doc %{_maindocdir}/AUTHORS
%doc %{_maindocdir}/ChangeLog
%doc %{_maindocdir}/NEWS
%doc %{_maindocdir}/PROBLEMS
%doc %{_maindocdir}/README*
%license %{_maindocdir}/COPYING
%license %{_maindocdir}/LICENSE
%dir /@unixroot/etc/sane.d
%dir /@unixroot/etc/sane.d/dll.d
%config(noreplace) /@unixroot/etc/sane.d/*.conf
%if %{with_systemd}
%{udevrulesdir}/65-sane-backends.rules
%{udevhwdbdir}/20-sane-backends.hwdb
%endif

%{_bindir}/sane-find-scanner.exe
%{_bindir}/scanimage.exe
%{_bindir}/umax_pp.exe

%exclude %{_mandir}/man1/sane-config.1*
%exclude %{_mandir}/man8/saned*
%{_mandir}/*/*

%dir %{_libdir}/sane
%dir %{_datadir}/sane

%files doc
%doc %{_docdocdir}

%files libs
%{_libdir}/sane*.dll

%files devel
%{_bindir}/sane-config
%{_mandir}/man1/sane-config.1*
%{_includedir}/sane
%{_libdir}/sane*_dll.a
%{_libdir}/pkgconfig/sane-backends.pc

%files drivers-scanners
# we need to specify all .so files for available backends because something like
# #1761145 can happen - genesys did not compile because of lack gcc-c++ in buildroot
# and configure printed only warning. So now we can figure out missing backend support
# during build
# not on os2, as too much hassle
# I'll leave here a wildcard record
%{_libdir}/sane/*.dll
%exclude %{_libdir}/sane*.dll

%exclude %{_libdir}/sane/gphoto2*.dll

%if %{with_gphoto2}
%files drivers-cameras
%{_libdir}/sane/gphoto2*.dll
%endif

%files daemon
%{_sbindir}/saned.exe
%{_mandir}/man8/saned*
%if %{with_systemd}
%{udevrulesdir}/66-saned.rules
%{_unitdir}/saned.socket
%{_unitdir}/saned@.service
%endif

%changelog
* Thu Oct 31 2019 Zdenek Dohnal <zdohnal@redhat.com> - 1.0.28-1
- 1761530 - apply upstream patch
