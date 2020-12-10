# This spec file has been automatically updated
Version:	0.23.21
Release:	1%{?dist}
Name:           p11-kit
Summary:        Library for loading and sharing PKCS#11 modules

License:        BSD
URL:            http://p11-glue.freedesktop.org/p11-kit.html
%if !0%{?os2_version}
Source0:        https://github.com/p11-glue/p11-kit/releases/download/%{version}/p11-kit-%{version}.tar.xz
Source1:        https://github.com/p11-glue/p11-kit/releases/download/%{version}/p11-kit-%{version}.tar.xz.sig
Source2:        gpgkey-462225C3B46F34879FC8496CD605848ED7E69871.gpg
%endif
Source3:        trust-extract-compat
%if !0%{?os2_version}
Source4:        p11-kit-client.service
%else
Vendor:         bww bitwise works GmbH
%scm_source     github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2
%endif

BuildRequires:  gcc
BuildRequires:  libtasn1-devel >= 2.3
BuildRequires:  libffi-devel
BuildRequires:  gettext
%if !0%{?os2_version}
BuildRequires:  gtk-doc
%endif
%if !0%{?os2_version}
BuildRequires:  meson
BuildRequires:  systemd-devel
BuildRequires:  bash-completion
%endif
# Work around for https://bugzilla.redhat.com/show_bug.cgi?id=1497147
# Remove this once it is fixed
%if !0%{?os2_version}
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  gnupg2
BuildRequires:  /usr/bin/xsltproc
%else
BuildRequires:  /@unixroot/usr/bin/xsltproc.exe
%endif

%description
p11-kit provides a way to load and enumerate PKCS#11 modules, as well
as a standard configuration setup for installing PKCS#11 modules in
such a way that they're discoverable.


%package devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package trust
Summary:            System trust module from %{name}
Requires:           %{name} = %{version}-%{release}
%if !0%{?os2_version}
Requires(post):     %{_sbindir}/update-alternatives
Requires(postun):   %{_sbindir}/update-alternatives
%endif
Conflicts:          nss < 3.14.3-9

%description trust
The %{name}-trust package contains a system trust PKCS#11 module which
contains certificate anchors and black lists.


%package server
Summary:        Server and client commands for %{name}
Requires:       %{name} = %{version}-%{release}

%description server
The %{name}-server package contains command line tools that enable to
export PKCS#11 modules through a Unix domain socket.  Note that this
feature is still experimental.


%if !0%{?os2_version}
# solution taken from icedtea-web.spec
%define multilib_arches ppc64 sparc64 x86_64 ppc64le
%ifarch %{multilib_arches}
%define alt_ckbi  libnssckbi.so.%{_arch}
%else
%define alt_ckbi  libnssckbi.so
%endif
%endif


%debug_package


%prep
%if !0%{?os2_version}
gpgv2 --keyring %{SOURCE2} %{SOURCE1} %{SOURCE0}

%autosetup -p1
%else
%scm_setup
export NOCONFIGURE=1
autogen.sh
%endif

%build
%if !0%{?os2_version}
# These paths are the source paths that  come from the plan here:
# https://fedoraproject.org/wiki/Features/SharedSystemCertificates:SubTasks
%meson -Dgtk_doc=true -Dman=true -Dtrust_paths=%{_sysconfdir}/pki/ca-trust/source:%{_datadir}/pki/ca-trust-source
%meson_build
%else
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
export VENDOR="%{vendor}"
%configure --disable-static \
  --with-trust-paths="%{_sysconfdir}/pki/ca-trust/source;%{_datadir}/pki/ca-trust-source" --disable-silent-rules
make %{?_smp_mflags} V=1
%endif

%install
%if !0%{?os2_version}
%meson_install
%else
make install DESTDIR=$RPM_BUILD_ROOT
%endif
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pkcs11/modules
install -p -m 755 %{SOURCE3} $RPM_BUILD_ROOT%{_libexecdir}/p11-kit/
# Install the example conf with %%doc instead
mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{name}
mv $RPM_BUILD_ROOT%{_sysconfdir}/pkcs11/pkcs11.conf.example $RPM_BUILD_ROOT%{_docdir}/%{name}/pkcs11.conf.example
%if !0%{?os2_version}
mkdir -p $RPM_BUILD_ROOT%{_userunitdir}
install -p -m 644 %{SOURCE4} $RPM_BUILD_ROOT%{_userunitdir}
%endif
%if 0%{?os2_version}
# if we ever use meson, this is all gone
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/pkcs11/*.la
# never link to modules, so remove them here
rm $RPM_BUILD_ROOT%{_libdir}/pkcs11/*_dll.a
%endif
%find_lang %{name}

%check
%if !0%{?os2_version}
%meson_test
%endif


%post trust
%if !0%{?os2_version}
%{_sbindir}/update-alternatives --install %{_libdir}/libnssckbi.so \
        %{alt_ckbi} %{_libdir}/pkcs11/p11-kit-trust.so 30
%endif

%postun trust
%if !0%{?os2_version}
if [ $1 -eq 0 ] ; then
        # package removal
        %{_sbindir}/update-alternatives --remove %{alt_ckbi} %{_libdir}/pkcs11/p11-kit-trust.so
fi
%endif


%files -f %{name}.lang
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc AUTHORS NEWS README
%{_docdir}/%{name}/pkcs11.conf.example
%dir %{_sysconfdir}/pkcs11
%dir %{_sysconfdir}/pkcs11/modules
%dir %{_datadir}/p11-kit
%dir %{_datadir}/p11-kit/modules
%dir %{_libexecdir}/p11-kit
%if !0%{?os2_version}
%{_bindir}/p11-kit
%{_libdir}/libp11-kit.so.*
%{_libdir}/p11-kit-proxy.so
%{_libexecdir}/p11-kit/p11-kit-remote
%else
%{_bindir}/p11-kit.exe
%{_libdir}/p11kit*.dll
%{_libexecdir}/p11-kit/p11-kit-remote.exe
%endif
%if !0%{?os2_version}
%{_mandir}/man1/trust.1.gz
%{_mandir}/man8/p11-kit.8.gz
%{_mandir}/man5/pkcs11.conf.5.gz
%endif
%if !0%{?os2_version}
%{_datadir}/bash-completion/completions/p11-kit
%endif

%files devel
%{_includedir}/p11-kit-1/
%if !0%{?os2_version}
%{_libdir}/libp11-kit.so
%else
%{_libdir}/*_dll.a
%endif
%{_libdir}/pkgconfig/p11-kit-1.pc
%if !0%{?os2_version}
%doc %{_datadir}/gtk-doc/
%endif

%files trust
%if !0%{?os2_version}
%{_bindir}/trust
%else
%{_bindir}/trust.exe
%endif
%dir %{_libdir}/pkcs11
%if !0%{?os2_version}
%ghost %{_libdir}/libnssckbi.so
%{_libdir}/pkcs11/p11-kit-trust.so
%else
%{_libdir}/pkcs11/p11ktru*.dll
%endif
%{_datadir}/p11-kit/modules/p11-kit-trust.module
%{_libexecdir}/p11-kit/trust-extract-compat
%if !0%{?os2_version}
%{_datadir}/bash-completion/completions/trust
%endif

%files server
%if !0%{?os2_version}
%{_libdir}/pkcs11/p11-kit-client.so
%{_userunitdir}/p11-kit-client.service
%else
%{_libdir}/pkcs11/p11kcln*.dll
%endif
%if !0%{?os2_version}
%{_libexecdir}/p11-kit/p11-kit-server
%{_userunitdir}/p11-kit-server.service
%{_userunitdir}/p11-kit-server.socket
%else
%{_libexecdir}/p11-kit/p11-kit-server.exe
%endif


%changelog
* Wed Dec 09 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.23.21-1
- update to version 0.23.21
- resync spec with fedora

* Mon Nov 04 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.23.18.1-1
- initial OS/2 rpm
