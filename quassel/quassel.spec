%global quassel_user        quassel
%global quassel_data_dir    %{_var}/lib/quassel
%global title A modern distributed IRC system

%global no_systemd 1
%global no_webkit 1
%global no_multimedia 1

Name:    quassel
Summary: A modern distributed IRC system
Version: 0.14
Release: 1.pre%{?dist}

License: GPLv2 or GPLv3
URL:     http://quassel-irc.org/
Vendor:  bww bitwise works GmbH
%scm_source github http://github.com/bitwiseworks/%{name}-os2 master-os2

Requires: bww-resources-rpm
BuildRequires: cmake
#BuildRequires: dbusmenu-qt5-devel
#BuildRequires: desktop-file-utils
#BuildRequires: extra-cmake-modules
BuildRequires: openssl-devel
BuildRequires: perl-generators
#BuildRequires: phonon-qt5-devel
BuildRequires: qca-qt5-devel
BuildRequires: qt5-linguist
BuildRequires: qt5-qtbase-devel
%if !0%{?no_webkit}
BuildRequires: qt5-qtwebkit-devel
%endif
%if !0%{?no_multimedia}
BuildRequires: qt5-qtmultimedia-devel
%endif
BuildRequires: qt5-rpm-macros
#BuildRequires: openldap-devel

%if !0%{?no_systemd}
BuildRequires: systemd
%endif

#BuildRequires: libappstream-glib

Requires: oxygen-icon-theme

Provides: %{name}-gui = %{version}-%{release}

Requires: %{name}-common = %{version}-%{release}

# Systemd service file and configuration script.
%if !0%{?no_systemd}
Source1: quasselcore.service
%endif
Source2: quassel.conf

%description
Quassel IRC is a modern, distributed IRC client,
meaning that one (or multiple) client(s) can attach
to and detach from a central core --
much like the popular combination of screen and a
text-based IRC client such as WeeChat, but graphical

%package common
Summary: Quassel common/shared files
# not strictly required, but helps this get pulled out when
# someone removes %%name or %%name-client
Requires: %{name}-gui = %{version}-%{release}
# put here for convenience, instead of all subpkgs which
# provide %%{name}-gui
BuildArch: noarch
%description common
%{summary}.

%package core
Summary: Quassel core component

# Required for the quassel user.
#Requires(pre): shadow-utils

# Weak dependency on qt5 postgresql bindings.
# We use a weak dependency here so they can be uninstalled if necessary.
Recommends: qt5-qtbase-postgresql

%description core
The Quassel IRC Core maintains a connection with the
server, and allows for multiple clients to connect

%package client
Summary: Quassel client
Provides: %{name}-gui = %{version}-%{release}
Requires: %{name}-common = %{version}-%{release}
%description client
Quassel client

%debuglevel

%prep
%scm_setup

%build
# !!the below values need to be adjusted and when we have a boost rpm those !! #
# !! are obsolete (if we ever get a boost rpm) !! #
export BOOST_CPPFLAGS="-IE:/Trees/boost/trunk"
export BOOST_ROOT="E:/Trees/boost/trunk"
export BOOST_LDFLAGS="-LE:/Trees/boost/trunk/stage/lib"

export LDFLAGS="-Zomf -Zhigh-mem -lcx -lssp %{?__global_ldflags}"
export VENDOR="%{vendor}"

mkdir build
cd build
%{cmake} .. -DWANT_MONO=1 -DUSE_QT5=1 -DHAVE_SSL=1 \
  -DENABLE_SHARED=OFF
cd ..

make %{?_smp_mflags} -C build

%install
make install/fast DESTDIR=%{buildroot} -C build

# unpackaged files
rm -f %{buildroot}/%{_datadir}/pixmaps/quassel.png

# Install quassel.conf for systemd file
mkdir -p %{buildroot}/%{_sysconfdir}
install -m 0644 %{SOURCE2} %{buildroot}/%{_sysconfdir}/

# Install systemd service file
%if !0%{?no_systemd}
install -d -m 0755 %{buildroot}/%{_unitdir}
install -p -m 0644 %{SOURCE1} %{buildroot}/%{_unitdir}/
%endif

# Home directory for quassel user
install -d -m 0750 %{buildroot}/%{quassel_data_dir}

# Core pre/post macros.

%pre core
groupadd -r %{quassel_user}
useradd -r -g %{quassel_user} -d %{quassel_data_dir} -s /sbin/nologin \
    -c "Account to own and run the quasselcore daemon from." %{quassel_user}
exit 0

%post core
# Install quassel service.
%if !0%{?no_systemd}
%systemd_post quasselcore.service
%endif

%preun core
%if !0%{?no_systemd}
%systemd_preun quasselcore.service
%endif

%postun core
%if !0%{?no_systemd}
%systemd_postun_with_restart quasselcore.service
%endif

%post
if [ "$1" -ge 1 ]; then # (upon update)
    %wps_object_delete_all
fi
# for the definition of the parameters see macros.bww
%bww_folder -t %{title} -s %{name}-apps
%bww_app -f %{_bindir}/%{name}.exe -t %{title}
%bww_app_shadow
%bww_readme -f %_defaultdocdir/%{name}-common-%{version}/README.md


%postun
if [ "$1" -eq 0 ]; then # (upon removal)
    %wps_object_delete_all
fi


%post client
if [ "$1" -ge 1 ]; then # (upon update)
    %wps_object_delete_all
fi
# for the definition of the parameters see macros.bww
%bww_folder -t %{title} -s %{name}-apps
%bww_app -f %{_bindir}/%{name}client.exe -t %{title}


%postun client
if [ "$1" -eq 0 ]; then # (upon removal)
    %wps_object_delete_all
fi

%files
%{_bindir}/quassel.exe

%files common
%doc README.md
%license COPYING gpl-2.0.txt gpl-3.0.txt
#{_datadir}/knotifications5/quassel.notifyrc
%{_datadir}/quassel/
#{_datadir}/icons/hicolor/*/*/*

%files core
%doc README.md
%license COPYING gpl-2.0.txt gpl-3.0.txt
%{_bindir}/quasselcore.exe
%dir %attr(-,quassel,quassel) %{quassel_data_dir}
%if !0%{?no_systemd}
%{_unitdir}/quasselcore.service
%endif
%config(noreplace) %{_sysconfdir}/quassel.conf

%files client
%{_bindir}/quasselclient.exe


%changelog
* Wed Jan 22 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.14-1.pre
- initial OS/2 rpm

