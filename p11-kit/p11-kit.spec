%global with_systemd 0
%global with_server 0
%global with_alternatives 0
%global with_gtkdoc 0

Version:	0.23.18.1
Release:	1%{?dist}
Name:           p11-kit
Summary:        Library for loading and sharing PKCS#11 modules

License:        BSD
URL:            http://p11-glue.freedesktop.org/p11-kit.html
Vendor:         bww bitwise works GmbH
%scm_source     github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2

BuildRequires:  gcc
BuildRequires:  libtasn1-devel >= 2.3
BuildRequires:  libffi-devel
%if %{with_gtkdoc}
BuildRequires:  gtk-doc
%endif
%if %{with_systemd}
BuildRequires:  systemd-devel
%endif
# Work around for https://bugzilla.redhat.com/show_bug.cgi?id=1497147
# Remove this once it is fixed
#BuildRequires:  pkgconfig(glib-2.0)

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
%if %{with_alternatives}
Requires(post):     %{_sbindir}/update-alternatives
Requires(postun):   %{_sbindir}/update-alternatives
%endif
Conflicts:          nss < 3.14.3-9

%description trust
The %{name}-trust package contains a system trust PKCS#11 module which
contains certificate anchors and black lists.


%if %{with_server}
%package server
Summary:        Server and client commands for %{name}
Requires:       %{name} = %{version}-%{release}

%description server
The %{name}-server package contains command line tools that enable to
export PKCS#11 modules through a Unix domain socket.  Note that this
feature is still experimental.


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
%scm_setup
export NOCONFIGURE=1
autogen.sh

%build
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
export VENDOR="%{vendor}"
# These paths are the source paths that  come from the plan here:
# https://fedoraproject.org/wiki/Features/SharedSystemCertificates:SubTasks
%configure --disable-static \
%if %{with_gtkdoc}
  --enable-doc \
%endif
  --with-trust-paths="%{_sysconfdir}/pki/ca-trust/source;%{_datadir}/pki/ca-trust-source" --disable-silent-rules
make %{?_smp_mflags} V=1

%install
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pkcs11/modules
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/pkcs11/*.la
# Install the example conf with %%doc instead
rm $RPM_BUILD_ROOT%{_sysconfdir}/pkcs11/pkcs11.conf.example

# never link to modules, so remove them here
rm $RPM_BUILD_ROOT%{_libdir}/pkcs11/*_dll.a
%if !%{with_server}
rm $RPM_BUILD_ROOT%{_libdir}/pkcs11/p11kcln*.dll
rm $RPM_BUILD_ROOT%{_libexecdir}/p11-kit/p11-kit-server.exe
%endif

# copy readme
rm README
cp README.md README

%check
%if %{with_server}
make check
%endif

%post trust
%if %{with_alternatives}
%{_sbindir}/update-alternatives --install %{_libdir}/libnssckbi.so \
        %{alt_ckbi} %{_libdir}/pkcs11/p11-kit-trust.so 30
%endif

%postun trust
%if %{with_alternatives}
if [ $1 -eq 0 ] ; then
        # package removal
        %{_sbindir}/update-alternatives --remove %{alt_ckbi} %{_libdir}/pkcs11/p11-kit-trust.so
fi
%endif


%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc AUTHORS NEWS README
%doc p11-kit/pkcs11.conf.example
%dir %{_sysconfdir}/pkcs11
%dir %{_sysconfdir}/pkcs11/modules
%dir %{_datadir}/p11-kit
%dir %{_datadir}/p11-kit/modules
%dir %{_libexecdir}/p11-kit
%{_bindir}/p11-kit.exe
%{_libdir}/p11kit*.dll
%{_libexecdir}/p11-kit/p11-kit-remote.exe
%if %{with_gtkdoc}
%{_mandir}/man1/trust.1.gz
%{_mandir}/man8/p11-kit.8.gz
%{_mandir}/man5/pkcs11.conf.5.gz
%endif

%files devel
%{_includedir}/p11-kit-1/
%{_libdir}/*_dll.a
%{_libdir}/pkgconfig/p11-kit-1.pc
%if %{with_gtkdoc}
%doc %{_datadir}/gtk-doc/
%endif

%files trust
%{_bindir}/trust.exe
%dir %{_libdir}/pkcs11
#%ghost %{_libdir}/libnssckbi.so
%{_libdir}/pkcs11/p11ktru*.dll
%{_datadir}/p11-kit/modules/p11-kit-trust.module
%{_libexecdir}/p11-kit/trust-extract-compat

%if %{with_server}
%files server
%{_libdir}/pkcs11/p11kcln*.dll
%{_userunitdir}/p11-kit-client.service
%{_libexecdir}/p11-kit/p11-kit-server.exe
%{_userunitdir}/p11-kit-server.service
%{_userunitdir}/p11-kit-server.socket
%endif


%changelog
* Mon Nov 04 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.23.18.1-1
- initial OS/2 rpm
