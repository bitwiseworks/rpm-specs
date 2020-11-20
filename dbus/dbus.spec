%global _hardened_build 1
%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

%global gettext_package         dbus-1

%global libselinux_version      2.0.86

# fedora-release-30-0.2 and generic-release-0.1 added required presets to enable systemd-unit symlinks
%if !0%{?os2_version}
%global fedora_release_version  30-0.2
%global generic_release_version 30-0.1
%endif

%global dbus_user_uid           81

%if !0%{?os2_version}
%global dbus_common_config_opts --enable-libaudit --enable-selinux=yes --with-system-socket=/run/dbus/system_bus_socket --with-dbus-user=dbus --libexecdir=/%{_libexecdir}/dbus-1 --enable-user-session --docdir=%{_pkgdocdir} --enable-installed-tests

# Allow extra dependencies required for some tests to be disabled.
%bcond_without tests
# Disabled in June 2014: http://lists.freedesktop.org/archives/dbus/2014-June/016223.html
%bcond_with check
%else
%bcond_with tests
%bcond_with check
%endif
# Allow cmake support to be disabled. #1497257
%bcond_without cmake

Name:    dbus
Epoch:   1
Version: 1.13.12
Release: 1%{?dist}
Summary: D-BUS message bus

# The effective license of the majority of the package, including the shared
# library, is "GPL-2+ or AFL-2.1". Certain utilities are "GPL-2+" only.
License: (GPLv2+ or AFL) and GPLv2+
URL:     http://www.freedesktop.org/Software/dbus/
#VCS:    git:git://git.freedesktop.org/git/dbus/dbus
%if !0%{?os2_version}
Source0: https://dbus.freedesktop.org/releases/%{name}/%{name}-%{version}.tar.gz
Source1: https://dbus.freedesktop.org/releases/%{name}/%{name}-%{version}.tar.gz.asc
# gpg --keyserver keyring.debian.org --recv-keys 36EC5A6448A4F5EF79BEFE98E05AE1478F814C4F
# gpg --export --export-options export-minimal > gpgkey-36EC5A6448A4F5EF79BEFE98E05AE1478F814C4F.gpg
Source2: gpgkey-36EC5A6448A4F5EF79BEFE98E05AE1478F814C4F.gpg
Source3: 00-start-message-bus.sh
Source4: dbus.socket
Source5: dbus-daemon.service
Source6: dbus.user.socket
Source7: dbus-daemon.user.service
Patch0: 0001-tools-Use-Python3-for-GetAllMatchRules.patch
%else
Vendor:  bww bitwise works GmbH
#scm_source    github https://github.com/bitwiseworks/%{name}-os2 %{version}-os2
%scm_source    git e:/trees/dbus/git master-os2
%endif

BuildRequires: autoconf-archive
BuildRequires: libtool
%if !0%{?os2_version}
BuildRequires: audit-libs-devel >= 0.9
BuildRequires: gnupg2
BuildRequires: libX11-devel
BuildRequires: libcap-ng-devel
%endif
BuildRequires: pkgconfig(expat)
%if !0%{?os2_version}
BuildRequires: pkgconfig(libselinux) >= %{libselinux_version}
BuildRequires: pkgconfig(libsystemd)
BuildRequires: pkgconfig(systemd)
%endif
BuildRequires: doxygen
# For Ducktype documentation.
%if !0%{?os2_version}
BuildRequires: /usr/bin/ducktype
BuildRequires: /usr/bin/yelp-build
# For building XML documentation.
BuildRequires: /usr/bin/xsltproc
%else
BuildRequires: /@unixroot/usr/bin/xsltproc.exe
%endif
BuildRequires: xmlto
%if %{with cmake}
# For AutoReq cmake-filesystem.
BuildRequires: cmake
%endif

#For macroized scriptlets.
%if !0%{?os2_version}
BuildRequires:    systemd
%endif

# Note: These is only required for --with-tests; when bootstrapping, you can
# pass --without-tests.
%if %{with tests}
BuildRequires: pkgconfig(gio-2.0) >= 2.40.0
BuildRequires: python3-dbus
BuildRequires: python3-gobject
%endif
%if %{with check}
BuildRequires: /usr/bin/Xvfb
%endif

# Since F30 the default implementation is dbus-broker over dbus-daemon
%if !0%{?os2_version}
Requires: dbus-broker >= 16-4
%endif

%description
D-BUS is a system for sending messages between applications. It is
used both for the system-wide message bus service, and as a
per-user-login-session messaging facility.

%package common
Summary:        D-BUS message bus configuration
BuildArch:      noarch
%{?systemd_requires}
%if !0%{?os2_version}
Conflicts:      fedora-release < %{fedora_release_version}
Conflicts:      generic-release < %{generic_release_version}
Requires:       /usr/bin/systemctl
%endif

%description common
The %{name}-common package provides the configuration and setup files for D-Bus
implementations to provide a System and User Message Bus.

%package daemon
Summary:        D-BUS message bus
%if !0%{?os2_version}
%{?systemd_requires}
Conflicts:      fedora-release < %{fedora_release_version}
Conflicts:      generic-release < %{generic_release_version}
Requires:       libselinux%{?_isa} >= %{libselinux_version}
%endif
Requires:       dbus-common = %{epoch}:%{version}-%{release}
Requires:       dbus-libs = %{epoch}:%{version}-%{release}
Requires:       dbus-tools = %{epoch}:%{version}-%{release}
%if !0%{?os2_version}
Requires(pre):  /usr/sbin/useradd
Requires:       /usr/bin/systemctl
%else
Requires(pre):  /@unixroot/usr/bin/useradd
%endif

%description daemon
D-BUS is a system for sending messages between applications. It is
used both for the system-wide message bus service, and as a
per-user-login-session messaging facility.

%package tools
Summary:        D-BUS Tools and Utilities
Requires:       dbus-libs = %{epoch}:%{version}-%{release}

%description tools
Tools and utilities to interact with a running D-Bus Message Bus, provided by
the reference implementation.

%package libs
Summary: Libraries for accessing D-BUS

%description libs
This package contains lowlevel libraries for accessing D-BUS.

%package doc
Summary: Developer documentation for D-BUS
Requires: %{name}-daemon = %{epoch}:%{version}-%{release}
BuildArch: noarch

%description doc
This package contains developer documentation for D-Bus along with
other supporting documentation such as the introspect dtd file.

%package devel
Summary: Development files for D-BUS
Requires: dbus-libs = %{epoch}:%{version}-%{release}
# For xml directory ownership.
Requires: xml-common

%description devel
This package contains libraries and header files needed for
developing software that uses D-BUS.

%package tests
Summary: Tests for the %{name}-daemon package
Requires: %{name}-daemon = %{epoch}:%{version}-%{release}

%description tests
The %{name}-tests package contains tests that can be used to verify
the functionality of the installed %{name}-daemon package.

%if !0%{?os2_version}
%package x11
Summary: X11-requiring add-ons for D-BUS
# The server package can be a different architecture.
Requires: %{name}-daemon = %{epoch}:%{version}-%{release}

%description x11
D-BUS contains some tools that require Xlib to be installed, those are
in this separate package so server systems need not install X.
%endif

%debug_package

%prep
%if !0%{?os2_version}
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -p1
%else
%scm_setup
%endif


%build
# Avoid rpath.
%if !0%{?os2_version}
if test -f autogen.sh; then env NOCONFIGURE=1 ./autogen.sh; else autoreconf --verbose --force --install; fi
%else
autoreconf -fvi
%endif

# Call configure here (before the extra directories for the multiple builds
# have been created) to ensure that the hardening flag hack is applied to
# ltmain.sh
%if !0%{?os2_version}
%configure %{dbus_common_config_opts} --enable-doxygen-docs --enable-ducktype-docs --enable-xml-docs --disable-asserts
make distclean

mkdir build
pushd build
# See /usr/lib/rpm/macros
%global _configure ../configure
%configure %{dbus_common_config_opts} --enable-doxygen-docs --enable-ducktype-docs --enable-xml-docs --disable-asserts
make V=1 %{?_smp_mflags}
popd

%if %{with check}
mkdir build-check
pushd build-check
%configure %{dbus_common_config_opts} --enable-asserts --enable-verbose-mode --enable-tests
make V=1 %{?_smp_mflags}
popd
%endif
%else
export LDFLAGS='-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx'
export LIBS='-lcx'
# Set BUILDLEVEL to be embedded to all DLLs built with Libtool.
export LT_BUILDLEVEL="@#%{vendor}:%{version}-%{release}#@##1## `LANG=C date +'%%d %%b %%Y %%H:%%M:%%S'`     `uname -n`::::0::"
%configure --disable-static \
 --with-dbus-user=dbus --libexecdir=%{_libexecdir}/dbus-1 \
 --enable-user-session --docdir=%{_pkgdocdir} --enable-installed-tests \
 --enable-doxygen-docs --enable-xml-docs --disable-asserts
make V=1 %{?_smp_mflags}
%endif


%install
%if !0%{?os2_version}
pushd build
%endif
make install DESTDIR=%{buildroot} INSTALL="install -p"
%if !0%{?os2_version}
popd
%endif

# Delete python2 code
rm -f %{buildroot}/%{_pkgdocdir}/examples/GetAllMatchRules.py

%if !0%{?os2_version}
find %{buildroot} -name '*.a' -type f -delete
%endif
find %{buildroot} -name '*.la' -type f -delete

%if ! %{with cmake}
rm -rf %{buildroot}%{_libdir}/cmake
%endif

# Delete upstream units
%if !0%{?os2_version}
rm -f %{buildroot}%{_unitdir}/dbus.{socket,service}
rm -f %{buildroot}%{_unitdir}/sockets.target.wants/dbus.socket
rm -f %{buildroot}%{_unitdir}/multi-user.target.wants/dbus.service
rm -f %{buildroot}%{_userunitdir}/dbus.{socket,service}
rm -f %{buildroot}%{_userunitdir}/sockets.target.wants/dbus.socket
%else
rm -f %{buildroot}%{_libdir}/systemd/dbus.socket
rm -f %{buildroot}%{_libdir}/systemd/dbus.service
rm -f %{buildroot}%{_libdir}/systemd/sockets.target.wants/dbus.socket
rm -f %{buildroot}%{_libdir}/systemd/multi-user.target.wants/dbus.service
rm -f %{buildroot}%{_libdir}/systemd/user/dbus.socket
rm -f %{buildroot}%{_libdir}/systemd/user/dbus.service
rm -f %{buildroot}%{_libdir}/systemd/user/sockets.target.wants/dbus.socket
rm -f %{buildroot}%{_bindir}/dbus-launch.exe
rm -f %{buildroot}%{_mandir}/man1/dbus-launch.1*
%endif

# Install downstream units
%if !0%{?os2_version}
install -Dp -m755 %{SOURCE3} %{buildroot}%{_sysconfdir}/X11/xinit/xinitrc.d/00-start-message-bus.sh
install -Dp -m644 %{SOURCE4} %{buildroot}%{_unitdir}/dbus.socket
install -Dp -m644 %{SOURCE5} %{buildroot}%{_unitdir}/dbus-daemon.service
install -Dp -m644 %{SOURCE6} %{buildroot}%{_userunitdir}/dbus.socket
install -Dp -m644 %{SOURCE7} %{buildroot}%{_userunitdir}/dbus-daemon.service
%endif

# Obsolete, but still widely used, for drop-in configuration snippets.
install --directory %{buildroot}%{_sysconfdir}/dbus-1/session.d
install --directory %{buildroot}%{_sysconfdir}/dbus-1/system.d

install --directory %{buildroot}%{_datadir}/dbus-1/interfaces

## %find_lang %{gettext_package}

%if !0%{?os2_version}
install --directory %{buildroot}/var/lib/dbus
install --directory %{buildroot}/run/dbus
%else
install --directory %{buildroot}/@unixroot/var/lib/dbus
install --directory %{buildroot}/@unixroot/var/run/dbus
%endif

install -pm 644 -t %{buildroot}%{_pkgdocdir} \
    doc/introspect.dtd doc/introspect.xsl doc/system-activation.txt

# Make sure that the documentation shows up in Devhelp.
%if !0%{?os2_version}
install --directory %{buildroot}%{_datadir}/gtk-doc/html
ln -s %{_pkgdocdir} %{buildroot}%{_datadir}/gtk-doc/html/dbus
%endif

# Shell wrapper for installed tests, modified from Debian package.
cat > dbus-run-installed-tests <<EOF
#!/bin/sh
# installed-tests wrapper for dbus. Outputs TAP format because why not

set -e

timeout="timeout 300s"
ret=0
i=0
tmpdir=\$(mktemp --directory --tmpdir dbus-run-installed-tests.XXXXXX)

for t in %{_libexecdir}/dbus-1/installed-tests/dbus/test-*; do
    i=\$(( \$i + 1 ))
    echo "# \$i - \$t ..."
    echo "x" > "\$tmpdir/result"
    ( set +e; \$timeout \$t; echo "\$?" > "\$tmpdir/result" ) 2>&1 | sed 's/^/# /'
    e="\$(cat "\$tmpdir/result")"
    case "\$e" in
        (0)
            echo "ok \$i - \$t"
            ;;
        (77)
            echo "ok \$i # SKIP \$t"
            ;;
        (*)
            echo "not ok \$i - \$t (\$e)"
            ret=1
            ;;
    esac
done

rm -rf tmpdir
echo "1..\$i"
exit \$ret
EOF

install -pm 755 -t %{buildroot}%{_libexecdir}/dbus-1 dbus-run-installed-tests


%if %{with check}
%check
pushd build-check

# TODO: better script for this...
export DISPLAY=42
{ Xvfb :${DISPLAY} -nolisten tcp -auth /dev/null >/dev/null 2>&1 &
  trap "kill -15 $! || true" 0 HUP INT QUIT TRAP TERM; };
if ! env DBUS_TEST_SLOW=1 make check; then
    echo "Tests failed, finding all Automake logs..." 1>&2;
    find . -type f -name '*.trs' | while read trs; do cat ${trs}; cat ${trs%%.trs}.log; done
    echo  "Exiting abnormally due to make check failure above" 1>&2;
    exit 1;
fi
popd
%endif


%pre daemon
# Add the "dbus" user and group
%if !0%{?os2_version}
getent group dbus >/dev/null || groupadd -f -g %{dbus_user_uid} -r dbus
if ! getent passwd dbus >/dev/null ; then
    if ! getent passwd %{dbus_user_uid} >/dev/null ; then
      useradd -r -u %{dbus_user_uid} -g %{dbus_user_uid} -d '/' -s /sbin/nologin -c "System message bus" dbus
    else
      useradd -r -g %{dbus_user_uid} -d '/' -s /sbin/nologin -c "System message bus" dbus
    fi
fi
%else
groupadd -g %{dbus_user_uid} -r dbus
useradd -r -g %{dbus_user_uid} -d '/' -s /sbin/nologin -c "System message bus" dbus
%endif
exit 0

%post common
%if !0%{?os2_version}
%systemd_post dbus.socket
%systemd_user_post dbus.socket
%endif

%post daemon
%if !0%{?os2_version}
%systemd_post dbus-daemon.service
%systemd_user_post dbus-daemon.service
%endif

%preun common
%if !0%{?os2_version}
%systemd_preun dbus.socket
%systemd_user_preun dbus.socket
%endif

%preun daemon
%if !0%{?os2_version}
%systemd_preun dbus-daemon.service
%systemd_user_preun dbus-daemon.service
%endif

%postun common
%if !0%{?os2_version}
%systemd_postun dbus.socket
%systemd_user_postun dbus.socket
%endif

%postun daemon
%if !0%{?os2_version}
%systemd_postun dbus-daemon.service
%systemd_user_postun dbus-daemon.service
%endif

%if !0%{?os2_version}
%triggerpostun common -- dbus-common < 1:1.12.10-4
systemctl --no-reload preset dbus.socket &>/dev/null || :
systemctl --no-reload --global preset dbus.socket &>/dev/null || :

%triggerpostun daemon -- dbus-daemon < 1:1.12.10-7
systemctl --no-reload preset dbus-daemon.service &>/dev/null || :
systemctl --no-reload --global preset dbus-daemon.service &>/dev/null || :
%endif

%files
# The 'dbus' package is only retained for compatibility purposes. It will
# eventually be removed and then replaced by 'Provides: dbus' in the
# dbus-daemon package. It will then exclusively be used for other packages to
# describe their dependency on a system and user bus. It does not pull in any
# particular dbus *implementation*, nor any libraries. These should be pulled
# in, if required, via explicit dependencies.

%files common
%dir %{_sysconfdir}/dbus-1
%dir %{_sysconfdir}/dbus-1/session.d
%dir %{_sysconfdir}/dbus-1/system.d
%config %{_sysconfdir}/dbus-1/session.conf
%config %{_sysconfdir}/dbus-1/system.conf
%dir %{_datadir}/dbus-1
%dir %{_datadir}/dbus-1/session.d
%dir %{_datadir}/dbus-1/system.d
%{_datadir}/dbus-1/session.conf
%{_datadir}/dbus-1/system.conf
%{_datadir}/dbus-1/services
%{_datadir}/dbus-1/system-services
%{_datadir}/dbus-1/interfaces
%if !0%{?os2_version}
%{_sysusersdir}/dbus.conf
%{_unitdir}/dbus.socket
%{_userunitdir}/dbus.socket
%endif

%files daemon
# Strictly speaking, we could remove the COPYING from this subpackage and 
# just have it be in libs, because dbus Requires dbus-libs.
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc AUTHORS CONTRIBUTING.md NEWS README
%exclude %{_pkgdocdir}/api
%exclude %{_pkgdocdir}/dbus.devhelp
%exclude %{_pkgdocdir}/diagram.*
%exclude %{_pkgdocdir}/introspect.*
%exclude %{_pkgdocdir}/system-activation.txt
%exclude %{_pkgdocdir}/*.html
%if !0%{?os2_version}
%ghost %dir /run/%{name}
%else
%dir /@unixroot/var/run/%{name}
%endif
%dir %{_localstatedir}/lib/dbus/
%if !0%{?os2_version}
%{_bindir}/dbus-daemon
%{_bindir}/dbus-cleanup-sockets
%{_bindir}/dbus-run-session
%{_bindir}/dbus-test-tool
%else
%{_bindir}/dbus-daemon.exe
%{_bindir}/dbus-cleanup-sockets.exe
%{_bindir}/dbus-run-session.exe
%{_bindir}/dbus-test-tool.exe
%endif
%{_mandir}/man1/dbus-cleanup-sockets.1*
%{_mandir}/man1/dbus-daemon.1*
%{_mandir}/man1/dbus-run-session.1*
%{_mandir}/man1/dbus-test-tool.1*
%dir %{_libexecdir}/dbus-1
# See doc/system-activation.txt in source tarball for the rationale
# behind these permissions
%if !0%{?os2_version}
%attr(4750,root,dbus) %{_libexecdir}/dbus-1/dbus-daemon-launch-helper
%else
%attr(4750,root,dbus) %{_libexecdir}/dbus-1/dbus-daemon-launch-helper.exe
%endif
%exclude %{_libexecdir}/dbus-1/dbus-run-installed-tests
%if !0%{?os2_version}
%{_tmpfilesdir}/dbus.conf
%{_unitdir}/dbus-daemon.service
%{_userunitdir}/dbus-daemon.service
%endif

%files tools
%{!?_licensedir:%global license %%doc}
%license COPYING
%if !0%{?os2_version}
%{_bindir}/dbus-send
%{_bindir}/dbus-monitor
%{_bindir}/dbus-update-activation-environment
%{_bindir}/dbus-uuidgen
%else
%{_bindir}/dbus-send.exe
%{_bindir}/dbus-monitor.exe
%{_bindir}/dbus-update-activation-environment.exe
%{_bindir}/dbus-uuidgen.exe
%endif
%{_mandir}/man1/dbus-monitor.1*
%{_mandir}/man1/dbus-send.1*
%{_mandir}/man1/dbus-update-activation-environment.1*
%{_mandir}/man1/dbus-uuidgen.1*

%files libs
%{!?_licensedir:%global license %%doc}
%license COPYING
%if !0%{?os2_version}
%{_libdir}/*dbus-1*.so.*
%else
%{_libdir}/dbus*.dll
%endif

%files tests
%{_libexecdir}/dbus-1/installed-tests
%if 0%{?os2_version}
%exclude %{_libexecdir}/dbus-1/installed-tests/dbus/*.dbg
%endif
%{_libexecdir}/dbus-1/dbus-run-installed-tests
%{_datadir}/installed-tests

%if !0%{?os2_version}
%files x11
%{_bindir}/dbus-launch
%{_mandir}/man1/dbus-launch.1*
%{_sysconfdir}/X11/xinit/xinitrc.d/00-start-message-bus.sh
%endif

%files doc
%{_pkgdocdir}/*
%if !0%{?os2_version}
%{_datadir}/gtk-doc
%endif
%exclude %{_pkgdocdir}/AUTHORS
%exclude %{_pkgdocdir}/ChangeLog
%exclude %{_pkgdocdir}/HACKING
%exclude %{_pkgdocdir}/NEWS
%exclude %{_pkgdocdir}/README

%files devel
%{_datadir}/xml/dbus-1
%if !0%{?os2_version}
%{_libdir}/lib*.so
%else
%{_libdir}/*_dll.a
%endif
%dir %{_libdir}/dbus-1.0
%if %{with cmake}
%{_libdir}/cmake/DBus1
%endif
%{_libdir}/dbus-1.0/include/
%{_libdir}/pkgconfig/dbus-1.pc
%{_includedir}/*


%changelog
* Wed Nov 11 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.13.12-1
- first OS/2 rpm

