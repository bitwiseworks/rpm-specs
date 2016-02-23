# Note that this is NOT a relocatable package
%define _version     0.9.10
%define github_name  libvncserver
# whether to use Github, or Netlabs's svn
%define _github      0

%if %_github
%define github_url  https://github.com/LibVNC/%{github_name}/archive
%define github_rev  LibVNCServer-%{_version}
%else
%define github_url     http://svn.netlabs.org/repos/ports/libvncserver/trunk
%define github_rev     1315
%endif

Name:    %{github_name}
Version: %{_version}
Release: 2%{?dist}
Summary: a library to make writing a vnc server easy
License: GPL
Group:  System/Libraries
#Group: Libraries/Network
Packager: Johannes.Schindelin <Johannes.Schindelin@gmx.de>
# Source: %{name}-%{version}.tar.bz2
%if %_github
Source: %{github_name}-%{github_rev}.zip
Patch0: %{name}.patch
%else
Source: %{name}-%{version}%{?github_rev:-r%{github_rev}}.zip
%endif
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

%debug_package

# %package x11vnc
#Requires:     %{name} = %{version}
#Summary:      VNC server for the current X11 session
#Group:        User Interface/X
#Requires:     %{name} = %{version}

# %description x11vnc
#x11vnc is to X Window System what WinVNC is to Windows, i.e. a server
#which serves the current X Window System desktop via RFB (VNC)
#protocol to the user.

#Based on the ideas of x0rfbserver and on LibVNCServer, it has evolved
#into a versatile and performant while still easy to use program.

%prep
# %setup -n %{name}-%{version}

%if %_github

%if %(sh -c 'if test -f "%{_sourcedir}/%{github_name}-%{github_rev}.zip" ; then echo 1 ; else echo 0 ; fi')
%setup -n "%{github_name}-%{github_rev}" -q
%else
%setup -n "%{github_name}-%{github_rev}" -Tc
rm -f "%{_sourcedir}/%{github_name}-%{github_rev}.zip"
curl -sSL "%{github_url}/%{github_rev}.zip" -o "%{_sourcedir}/%{github_name}-%{github_rev}.zip"
unzip -oC "%{_sourcedir}/%{github_name}-%{github_rev}.zip" -d ..
%endif

%else

%if %{?github_rev:%(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{github_rev}.zip" ; then echo 1 ; else echo 0 ; fi')}%{!?github_rev):0}
%setup -q
%else
%setup -n "%{name}-%{version}" -Tc
svn export %{?github_rev:-r %{github_rev}} %{github_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}%{?github_rev:-r%{github_rev}}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}%{?github_rev:-r%{github_rev}}.zip" "%{name}-%{version}")
%endif

%endif

autoreconf -fi

%if %_github
%patch0 -p1
%endif

%build
export  LDFLAGS="-Zhigh-mem -lsocket -lmmap" RANLIB=echo

%configure --without-ipv6

%{__make} %{?_smp_mflags}

%install
# [ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
# make install prefix=%{buildroot}%{_prefix}
%makeinstall includedir="%{buildroot}%{_includedir}/rfb"
emxomf -o %{buildroot}%{_libdir}/vncserver.lib %{buildroot}%{_libdir}/vncserver.a
emximp -o %{buildroot}%{_libdir}/vncserver_dll.lib %{buildroot}%{_libdir}/vncsrv0.dll
emximp -o %{buildroot}%{_libdir}/vncserver0_dll.lib %{buildroot}%{_libdir}/vncsrv0.dll
emxomf -o %{buildroot}%{_libdir}/vncclient.lib %{buildroot}%{_libdir}/vncclient.a
emximp -o %{buildroot}%{_libdir}/vncclient_dll.lib %{buildroot}%{_libdir}/vnccli0.dll
emximp -o %{buildroot}%{_libdir}/vncclient0_dll.lib %{buildroot}%{_libdir}/vnccli0.dll
# change shell path in libvncserver-config
sed -e 's-\#\!\/bin\/sh-#! /@unixroot/usr/bin/sh-g' \
	<%{buildroot}%{_bindir}/libvncserver-config \
	>%{buildroot}%{_bindir}/libvncserver-config-1
rm -rf %{buildroot}%{_bindir}/libvncserver-config
mv -f %{buildroot}%{_bindir}/libvncserver-config-1 %{buildroot}%{_bindir}/libvncserver-config

#%{__install} -d -m0755 %{buildroot}%{_datadir}/x11vnc/classes
#%{__install} webclients/java-applet/VncViewer.jar webclients/index.vnc \
#  %{buildroot}%{_datadir}/x11vnc/classes

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
%{_libdir}/vnccli0.dll
%{_libdir}/vncsrv0.dll

%files devel
%defattr(-,root,root)
%{_includedir}/rfb/*
%{_libdir}/pkgconfig/libvncclient.pc
%{_libdir}/pkgconfig/libvncserver.pc
%{_libdir}/vncclient*.a
%{_libdir}/vncserver*.a
%{_libdir}/vncclient*.lib
%{_libdir}/vncserver*.lib
%exclude %{_libdir}/libvncclient.la*
%exclude %{_libdir}/libvncserver.la*

# %files x11vnc
#%defattr(-,root,root)
# %{_bindir}/x11vnc
# %{_mandir}/man1/x11vnc.1*
#%{_datadir}/x11vnc/classes

%changelog
* Thu Feb 18 2016 Valery Sedletski - <_valerius@mail.ru> 0.9.10-2
- changed libs format to both a.out and OMF
- added debug package
- added OS/2 DLL shortname

* Tue Nov 17 2015 Valery Sedletski - <_valerius@mail.ru> first OS/2 build
- initial OS/2 build
