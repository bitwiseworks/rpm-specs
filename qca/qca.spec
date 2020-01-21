
%global qt4 1
%global qt5 1

%global botan 0
%global gcrypt 0
%global sasl2 0
%global pkcs11 0
%global run_check 0

%if 0%{?qt4}
%global _qt4_prefix /@unixroot/usr/share/qt4
%global _qt4_headerdir /@unixroot/usr/include
%global _qt4_libdir /@unixroot/usr/lib
%global _qt4_plugindir /@unixroot/usr/lib/qt4/plugins
%endif

Name:    qca
Summary: Qt Cryptographic Architecture
Version: 2.2.1
Release: 1%{?dist}

License: LGPLv2+
URL:     https://userbase.kde.org/QCA
Vendor:  bww bitwise works GmbH
%scm_source  github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2

## upstream patches

## upstreamable patches

BuildRequires: cmake >= 3.10.3-2
BuildRequires: gcc
%if 0%{?gcrypt}
BuildRequires: libgcrypt-devel
%endif
%if 0%{?botan}
BuildRequires: pkgconfig(botan-2)
%else
Obsoletes: qca-botan < %{version}-%{release}
%endif
BuildRequires: pkgconfig(libcrypto) pkgconfig(libssl)
BuildRequires: pkgconfig(nss)
%if 0%{?pkcs11}
BuildRequires: pkgconfig(libpkcs11-helper-1)
%endif
%if 0%{?sasl2}
BuildRequires: pkgconfig(libsasl2)
%endif
%if 0%{?qt4}
BuildRequires: libqt4-devel
%endif
# apidocs
# may need to add some tex-related ones too -- rex
#BuildRequires: doxygen-latex
#BuildRequires: graphviz

# qca2 renamed qca
Obsoletes: qca2 < 2.1.0
Provides:  qca2 = %{version}-%{release}

# most runtime consumers seem to assume the ossl plugin be present
Recommends: %{name}-ossl

%description
Taking a hint from the similarly-named Java Cryptography Architecture,
QCA aims to provide a straightforward and cross-platform crypto API,
using Qt datatypes and conventions. QCA separates the API from the
implementation, using plugins known as Providers. The advantage of this
model is to allow applications to avoid linking to or explicitly depending
on any particular cryptographic library. This allows one to easily change
or upgrade crypto implementations without even needing to recompile the
application!

%package devel
Summary: Qt Cryptographic Architecture development files
# qca2 renamed qca
Obsoletes: qca2-devel < 2.1.0
Provides:  qca2-devel = %{version}-%{release}
Requires:  %{name} = %{version}-%{release}
%description devel
This packages contains the development files for QCA.

%package doc
Summary: QCA API documentation
BuildArch: noarch
%description doc
This package includes QCA API documentation in HTML

%if 0%{?botan}
%package botan
Summary: Botan plugin for the Qt Cryptographic Architecture
Requires: %{name} = %{version}-%{release}
%description botan
%{summary}.
%endif

%if 0%{?sasl2}
%package cyrus-sasl
Summary: Cyrus-SASL plugin for the Qt Cryptographic Architecture
Requires: %{name} = %{version}-%{release}
%description cyrus-sasl
%{summary}.
%endif

%if 0%{?gcrypt}
%package gcrypt
Summary: Gcrypt plugin for the Qt Cryptographic Architecture
Requires: %{name} = %{version}-%{release}
%description gcrypt
%{summary}.
%endif

%package gnupg
Summary: Gnupg plugin for the Qt Cryptographic Architecture
Requires: %{name} = %{version}-%{release}
Requires: gnupg
%description gnupg
%{summary}.

%package logger
Summary: Logger plugin for the Qt Cryptographic Architecture
Requires: %{name} = %{version}-%{release}
%description logger
%{summary}.

%package nss
Summary: Nss plugin for the Qt Cryptographic Architecture
Requires: %{name} = %{version}-%{release}
%description nss
%{summary}.

%package ossl
Summary: Openssl plugin for the Qt Cryptographic Architecture
Requires: %{name} = %{version}-%{release}
%description ossl
%{summary}.

%if 0%{?pkcs11}
%package pkcs11
Summary: Pkcs11 plugin for the Qt Cryptographic Architecture
Requires: %{name} = %{version}-%{release}
%description pkcs11
%{summary}.
%endif

%package softstore
Summary: Pkcs11 plugin for the Qt Cryptographic Architecture
Requires: %{name} = %{version}-%{release}
%description softstore
%{summary}.

%if 0%{?qt5}
%package qt5
Summary: Qt5 Cryptographic Architecture
BuildRequires: pkgconfig(Qt5Core)
%if ! 0%{?botan}
Obsoletes: qca-qt5-botan < %{version}-%{release}
%endif
# most runtime consumers seem to assume the ossl plugin be present
Recommends: %{name}-qt5-ossl
%description qt5
Taking a hint from the similarly-named Java Cryptography Architecture,
QCA aims to provide a straightforward and cross-platform crypto API,
using Qt datatypes and conventions. QCA separates the API from the
implementation, using plugins known as Providers. The advantage of this
model is to allow applications to avoid linking to or explicitly depending
on any particular cryptographic library. This allows one to easily change
or upgrade crypto implementations without even needing to recompile the
application!

%package qt5-devel
Summary: Qt5 Cryptographic Architecture development files
Requires:  %{name}-qt5 = %{version}-%{release}
%description qt5-devel
%{summary}.

%if 0%{?botan}
%package qt5-botan
Summary: Botan plugin for the Qt5 Cryptographic Architecture
Requires: %{name}-qt5 = %{version}-%{release}
%description qt5-botan
%{summary}.
%endif

%if 0%{?sasl2}
%package qt5-cyrus-sasl
Summary: Cyrus-SASL plugin for the Qt5 Cryptographic Architecture
Requires: %{name}-qt5 = %{version}-%{release}
%description qt5-cyrus-sasl
%{summary}.
%endif

%if 0%{?gcrypt}
%package qt5-gcrypt
Summary: Gcrypt plugin for the Qt5 Cryptographic Architecture
Requires: %{name}-qt5 = %{version}-%{release}
%description qt5-gcrypt
%{summary}.
%endif

%package qt5-gnupg
Summary: Gnupg plugin for the Qt Cryptographic Architecture
Requires: %{name}-qt5 = %{version}-%{release}
Requires: gnupg
%description qt5-gnupg
%{summary}.

%package qt5-logger
Summary: Logger plugin for the Qt5 Cryptographic Architecture
Requires: %{name}-qt5 = %{version}-%{release}
%description qt5-logger
%{summary}.

%package qt5-nss
Summary: Nss plugin for the Qt5 Cryptographic Architecture
Requires: %{name}-qt5 = %{version}-%{release}
%description qt5-nss
%{summary}.

%package qt5-ossl
Summary: Openssl plugin for the Qt5 Cryptographic Architecture
Requires: %{name}-qt5 = %{version}-%{release}
%description qt5-ossl
%{summary}.

%if 0%{?pkcs11}
%package qt5-pkcs11
Summary: Pkcs11 plugin for the Qt5 Cryptographic Architecture
Requires: %{name}-qt5 = %{version}-%{release}
%description qt5-pkcs11
%{summary}.
%endif

%package qt5-softstore
Summary: Pkcs11 plugin for the Qt5 Cryptographic Architecture
Requires: %{name}-qt5 = %{version}-%{release}
%description qt5-softstore
%{summary}.
%endif

%debuglevel

%prep
%scm_setup


%build
export LDFLAGS="-Zomf -Zhigh-mem -lcx %{?__global_ldflags}"
export VENDOR="%{vendor}"

%if 0%{?qt5}
mkdir %{_host}-qt5
cd %{_host}-qt5
%{cmake} .. \
  -DQCA_BINARY_INSTALL_DIR:STRING=%{_bindir} \
  -DQCA_FEATURE_INSTALL_DIR:PATH=%{_qt5_archdatadir}/mkspecs/features \
  -DQCA_INCLUDE_INSTALL_DIR:PATH=%{_qt5_headerdir} \
  -DQCA_LIBRARY_INSTALL_DIR:PATH=%{_qt5_libdir} \
  -DQCA_PLUGINS_INSTALL_DIR:PATH=%{_qt5_plugindir} \
  -DQCA_PRIVATE_INCLUDE_INSTALL_DIR:PATH=%{_qt5_headerdir} \
  -DQT4_BUILD:BOOL=OFF \
  -DOS2_USE_DECLSPEC=ON
cd ..

make -C %{_host}-qt5
%endif

%if 0%{?qt4}
mkdir %{_host}
cd %{_host}
%{cmake} .. \
  -DQCA_DOC_INSTALL_DIR:PATH=%{_docdir}/qca \
  -DQCA_BINARY_INSTALL_DIR:STRING=%{_bindir} \
  -DQCA_FEATURE_INSTALL_DIR:PATH=%{_qt4_prefix}/mkspecs/features \
  -DQCA_INCLUDE_INSTALL_DIR:PATH=%{_qt4_headerdir} \
  -DQCA_LIBRARY_INSTALL_DIR:PATH=%{_qt4_libdir} \
  -DQCA_PLUGINS_INSTALL_DIR:PATH=%{_qt4_plugindir} \
  -DQCA_PRIVATE_INCLUDE_INSTALL_DIR:PATH=%{_qt4_headerdir} \
  -DQT4_BUILD:BOOL=ON \
  -DOS2_USE_DECLSPEC=ON
cd ..

make -C %{_host}

make doc -C %{_host}
%endif


%install
%if 0%{?qt5}
make install/fast DESTDIR=%{buildroot} -C %{_host}-qt5
%endif
%if 0%{?qt4}
make install/fast DESTDIR=%{buildroot} -C %{_host}

# no make install target for docs yet
mkdir -p %{buildroot}%{_docdir}/qca
cp -a %{_host}/apidocs/html/ %{buildroot}%{_docdir}/qca/
%endif


%check
%if 0%{?run_check}
export CTEST_OUTPUT_ON_FAILURE=1
export PKG_CONFIG_PATH=%{buildroot}%{_libdir}/pkgconfig
# skip slow archs
%ifnarch %{arm} ppc64 s390x
%if 0%{?qt4}
test "$(pkg-config --modversion qca2)" = "%{version}"
make test ARGS="--timeout 180 --output-on-failure" -C %{_host} ||:
%endif
%if 0%{?qt5}
test "$(pkg-config --modversion qca2-qt5)" = "%{version}"
make test ARGS="--timeout 180 --output-on-failure" -C %{_host}-qt5
%endif
%endif
%endif


%if 0%{?qt4}
#ldconfig_scriptlets

%files
%doc README TODO
%license COPYING
%{_qt4_libdir}/qca*.dll
%{_bindir}/mozcerts.exe
%{_bindir}/qcatool.exe
%{_mandir}/man1/qcatool.1*
%dir %{_qt4_plugindir}/crypto/
## HACK alert, quirk of recycling default %%_docdir below in -doc subpkg -- rex
%exclude %{_docdir}/qca/html/

%files doc
%{_docdir}/qca/html/

%files devel
%{_qt4_headerdir}/QtCrypto
%{_qt4_libdir}/qca*_dll.a
%{_libdir}/pkgconfig/qca2.pc
%{_libdir}/cmake/Qca/
%{_qt4_prefix}/mkspecs/features/crypto.prf

%if 0%{?botan}
%files botan
%doc plugins/qca-botan/README
%{_qt4_plugindir}/crypto/qca-bot*.dll
%endif

%if 0%{?sasl2}
%files cyrus-sasl
%doc plugins/qca-gcrypt/README
%{_qt4_plugindir}/crypto/qca-cyr*.dll
%endif

%if 0%{?gcrypt}
%files gcrypt
%{_qt4_plugindir}/crypto/qca-gcr*.dll
%endif

%files gnupg
%doc plugins/qca-gnupg/README
%{_qt4_plugindir}/crypto/qca-gnu*.dll

%files logger
%doc plugins/qca-logger/README
%{_qt4_plugindir}/crypto/qca-log*.dll

%files nss
%doc plugins/qca-nss/README
%{_qt4_plugindir}/crypto/qca-nss*.dll

%files ossl
%doc plugins/qca-ossl/README
%{_qt4_plugindir}/crypto/qca-oss*.dll

%if 0%{?pkcs11}
%files pkcs11
%doc plugins/qca-pkcs11/README
%{_qt4_plugindir}/crypto/qca-pkc*.dll
%endif

%files softstore
%doc plugins/qca-softstore/README
%{_qt4_plugindir}/crypto/qca-sof*.dll
%endif

%if 0%{?qt5}
#ldconfig_scriptlets qt5

%files qt5
%doc README TODO
%license COPYING
%{_bindir}/mozcerts-qt5.exe
%{_bindir}/qcatool-qt5.exe
%{_mandir}/man1/qcatool-qt5.1*
%{_qt5_libdir}/qca-qt5*.dll
%dir %{_qt5_plugindir}/crypto/

%files qt5-devel
%{_qt5_headerdir}/QtCrypto
%{_qt5_libdir}/qca-qt5*_dll.a
%{_libdir}/pkgconfig/qca2-qt5.pc
%{_libdir}/cmake/Qca-qt5/
%{_qt5_archdatadir}/mkspecs/features/crypto.prf

%if 0%{?botan}
%files qt5-botan
%doc plugins/qca-botan/README
%{_qt5_plugindir}/crypto/qca-bot*.dll
%endif

%if 0%{?sasl2}
%files qt5-cyrus-sasl
%doc plugins/qca-gcrypt/README
%{_qt5_plugindir}/crypto/qca-cyr*.dll
%endif

%if 0%{?gcrypt}
%files qt5-gcrypt
%{_qt5_plugindir}/crypto/qca-gcr*.dll
%endif

%files qt5-gnupg
%doc plugins/qca-gnupg/README
%{_qt5_plugindir}/crypto/qca-gnu*.dll

%files qt5-logger
%doc plugins/qca-logger/README
%{_qt5_plugindir}/crypto/qca-log*.dll

%files qt5-nss
%doc plugins/qca-nss/README
%{_qt5_plugindir}/crypto/qca-nss*.dll

%files qt5-ossl
%doc plugins/qca-ossl/README
%{_qt5_plugindir}/crypto/qca-oss*.dll

%if 0%{?pkcs11}
%files qt5-pkcs11
%doc plugins/qca-pkcs11/README
%{_qt5_plugindir}/crypto/qca-pkc*.dll
%endif

%files qt5-softstore
%doc plugins/qca-softstore/README
%{_qt5_plugindir}/crypto/qca-sof*.dll
%endif


%changelog
* Sat Jan 18 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.2.1-1
- initial OS/2 rpm
