# Note that this is NOT a relocatable package
%define _version     0.9.10
%define github_name libvncserver
%define github_url  https://github.com/LibVNC/%{github_name}/archive
%define github_rev  LibVNCServer-%{_version}

Name:    %{github_name}
Version: %{_version}
Release: 2%{?dist}
Summary: a library to make writing a vnc server easy
License: GPL
Group:  System/Libraries
#Group: Libraries/Network
Packager: Johannes.Schindelin <Johannes.Schindelin@gmx.de>
# Source: %{name}-%{version}.tar.bz2
Source: %{github_name}-%{github_rev}.zip
Patch0: %{name}.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot
BuildRequires: gcc make curl zip

%description
LibVNCServer makes writing a VNC server (or more correctly, a program
exporting a framebuffer via the Remote Frame Buffer protocol) easy.

It is based on OSXvnc, which in turn is based on the original Xvnc by
ORL, later AT&T research labs in UK.

It hides the programmer from the tedious task of managing clients and
compression schemata.

LibVNCServer was put together and is (actively ;-) maintained by
Johannes Schindelin <Johannes.Schindelin@gmx.de>

%package devel
Requires:     %{name} = %{version}
Summary:      Static Libraries and Header Files for LibVNCServer
Group:        Libraries/Network
Requires:     %{name} = %{version}

%description devel
Static Libraries and Header Files for LibVNCServer.

# %package x11vnc
%package applet
Requires:     %{name} = %{version}
Summary:      VNC server for the current X11 session
Group:        User Interface/X
Requires:     %{name} = %{version}

# %description x11vnc
%description applet
x11vnc is to X Window System what WinVNC is to Windows, i.e. a server
which serves the current X Window System desktop via RFB (VNC)
protocol to the user.

Based on the ideas of x0rfbserver and on LibVNCServer, it has evolved
into a versatile and performant while still easy to use program.

%prep
# %setup -n %{name}-%{version}
%if %(sh -c 'if test -f "%{_sourcedir}/%{github_name}-%{github_rev}.zip" ; then echo 1 ; else echo 0 ; fi')
%setup -n "%{github_name}-%{github_rev}" -q
%else
%setup -n "%{github_name}-%{github_rev}" -Tc
rm -f "%{_sourcedir}/%{github_name}-%{github_rev}.zip"
curl -sSL "%{github_url}/%{github_rev}.zip" -o "%{_sourcedir}/%{github_name}-%{github_rev}.zip"
unzip -oC "%{_sourcedir}/%{github_name}-%{github_rev}.zip" -d ..
%endif

autoreconf -fi

%patch0 -p1

%build
PATH=`echo $PATH | tr '\\\' '/'` \
PATHSEP=";" EXEEXT=".exe" IMPLIBPREF="" IMPLIBSUFF="_dll.a" \
LDFLAGS="-lsocket -lmmap" SORT=sort \
CC=gcc.exe CXX=g++.exe ECHO=echo RANLIB=echo \
AR=ar.exe LD=ld.exe PKG_CONFIG=pkg-config \
EMXOMFLD_TYPE="wlink" EMXOMFLD_LINKER="wl.exe" \
./configure --without-ipv6

%{__make} %{?_smp_mflags}

%install
# [ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
# make install prefix=%{buildroot}%{_prefix}
%makeinstall includedir="%{buildroot}%{_includedir}/rfb"

%{__install} -d -m0755 %{buildroot}%{_datadir}/x11vnc/classes
%{__install} webclients/java-applet/VncViewer.jar webclients/index.vnc \
  %{buildroot}%{_datadir}/x11vnc/classes

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%pre
%post
%preun
%postun

%files
%defattr(-,root,root)
%doc README INSTALL AUTHORS ChangeLog NEWS TODO 
# %{_bindir}/LinuxVNC
%{_bindir}/libvncserver-config
%{_libdir}/vncclie0.dll
%{_libdir}/vncserv0.dll

%files devel
%defattr(-,root,root)
%{_includedir}/rfb/*
%{_libdir}/pkgconfig/libvncclient.pc
%{_libdir}/pkgconfig/libvncserver.pc
%{_libdir}/vncclie0.dbg
%{_libdir}/vncserv0.dbg
%{_libdir}/vncclient*.a
%{_libdir}/vncserver*.a
%{_libdir}/libvncclient.la
%{_libdir}/libvncserver.la

# %files x11vnc
%files applet
%defattr(-,root,root)
# %{_bindir}/x11vnc
# %{_mandir}/man1/x11vnc.1*
%{_datadir}/x11vnc/classes

%changelog
* Tue Nov 17 2015 Valery Sedletski - <_valerius@mail.ru> first OS/2 build
- initial OS/2 build

* Fri Aug 19 2005 Alberto Lusiani <alusiani@gmail.com> release 2
- create separate package for x11vnc to prevent conflicts with x11vnc rpm
- create devel package, needed to compile but not needed for running

* Sun Feb 9 2003 Johannes Schindelin
- created libvncserver.spec.in

