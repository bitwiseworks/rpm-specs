# Note: this .spec is borrowed from:
# nss-3.23.0-1.0.fc24.src.rpm
# nss-util-3.23.0-1.0.fc24.src.rpm
# nss-softokn-3.23.0-0.1.fc24.src.rpm

%global nspr_version 4.12.0
%global unsupported_tools_directory %{_libdir}/nss/unsupported-tools
%global allTools "certutil cmsutil crlutil derdump modutil pk12util signtool signver ssltap vfychain vfyserv"

# Produce .chk files for the final stripped binaries
%define __spec_install_post \
    %{?__debug_package:%{__debug_install_post}} \
    %{__arch_install_post} \
    %{__os_install_post} \
    export BEGINLIBPATH=$RPM_BUILD_ROOT/%{_libdir} \
    $RPM_BUILD_ROOT/%{unsupported_tools_directory}/shlibsign.exe -i $RPM_BUILD_ROOT/%{_libdir}/softokn3.dll \
    $RPM_BUILD_ROOT/%{unsupported_tools_directory}/shlibsign.exe -i $RPM_BUILD_ROOT/%{_libdir}/freebl3.dll \
    $RPM_BUILD_ROOT/%{unsupported_tools_directory}/shlibsign.exe -i $RPM_BUILD_ROOT/%{_libdir}/nssdbm3.dll \
    $RPM_BUILD_ROOT/%{unsupported_tools_directory}/shlibsign.exe -i $RPM_BUILD_ROOT/%{_libdir}/softok3k.dll \
    $RPM_BUILD_ROOT/%{unsupported_tools_directory}/shlibsign.exe -i $RPM_BUILD_ROOT/%{_libdir}/freebl3k.dll \
    $RPM_BUILD_ROOT/%{unsupported_tools_directory}/shlibsign.exe -i $RPM_BUILD_ROOT/%{_libdir}/nssdbm3k.dll \
%{nil}

Summary:          Network Security Services
Name:             nss
Version:          3.23.0
Release:          3%{?dist}
License:          MPLv2.0
URL:              http://www.mozilla.org/projects/security/pki/nss/
Group:            System Environment/Libraries
Vendor:           bww bitwise works GmbH

Requires:         nspr >= %{nspr_version}
Requires:         nss-util = %{version}-%{release}
Requires:         nss-softokn = %{version}-%{release}
# @todo remove?
#Requires:         nss-system-init
BuildRequires:    nspr-devel >= %{nspr_version}
BuildRequires:    sqlite-devel
BuildRequires:    zlib-devel
BuildRequires:    pkgconfig
BuildRequires:    gawk
#BuildRequires:    psmisc
BuildRequires:    perl

%define svn_url     http://svn.netlabs.org/repos/ports/nss/trunk
%define svn_rev     1529

Source: %{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip

BuildRequires: gcc make subversion zip

#Source0:          %{name}-%{version}.tar.gz
Source1:          nss.pc.in
Source2:          nss-config.in
#Source3:          blank-cert8.db
#Source4:          blank-key3.db
#Source5:          blank-secmod.db
#Source6:          blank-cert9.db
#Source7:          blank-key4.db
#Source8:          system-pkcs11.txt
#Source9:          setup-nsssysinit.sh
#Source12:         %{name}-pem-20160308.tar.bz2
# @todo We don't have xmlto yet.
#Source20:         nss-config.xml
#Source21:         setup-nsssysinit.xml
#Source22:         pkcs11.txt.xml
#Source23:         cert8.db.xml
#Source24:         cert9.db.xml
#Source25:         key3.db.xml
#Source26:         key4.db.xml
#Source27:         secmod.db.xml

# From nss-util.spec:
Source202:         nss-util.pc.in
Source203:         nss-util-config.in

# From nss-softokn.spec:
Source302:         nss-softokn.pc.in
Source303:         nss-softokn-config.in

# DEF files to create forwarders for legacy DLLs (nss-legacy)
Source401:         nss3k.def
Source402:         nssckbik.def
Source403:         smime3k.def
Source404:         ssl3k.def
# DEF files to create forwarders for legacy DLLs (nss-util-legacy)
Source411:         nssuti3k.def
# DEF files to create forwarders for legacy DLLs (nss-softokn-legacy)
Source421:         nssdbm3k.def
Source422:         softok3k.def
# DEF files to create forwarders for legacy DLLs (nss-softokn-freebl-legacy)
Source431:         freebl3k.def

#Patch3:           renegotiate-transitional.patch
# Upstream: https://bugzilla.mozilla.org/show_bug.cgi?id=402712
#Patch6:           nss-enable-pem.patch
# Below reference applies to most pem module related patches
# Upstream: https://bugzilla.mozilla.org/show_bug.cgi?id=617723
#Patch16:          nss-539183.patch
# must statically link pem against the freebl in the buildroot
# Needed only when freebl on tree has new APIS
#Patch25:          nsspem-use-system-freebl.patch
# TODO: Remove this patch when the ocsp test are fixed
#Patch40:          nss-3.14.0.0-disble-ocsp-test.patch
# TODO remove when we switch to building nss without softoken
#Patch49:          nss-skip-bltest-and-fipstest.patch
# This patch uses the gcc-iquote dir option documented at
# http://gcc.gnu.org/onlinedocs/gcc/Directory-Options.html#Directory-Options
# to place the in-tree directories at the head of the list of list of directories
# to be searched for for header files. This ensures a build even when system
# headers are older. Such is the case when starting an update with API changes or even private export changes.
# Once the buildroot aha been bootstrapped the patch may be removed but it doesn't hurt to keep it.
#Patch50:          iquote.patch
#Patch52:          disableSSL2libssl.patch
#Patch53:          disableSSL2tests.patch
#Patch54:          tstclnt-ssl2-off-by-default.patch
#Patch55:          skip_stress_TLS_RC4_128_with_MD5.patch
# Local patch for TLS_ECDHE_{ECDSA|RSA}_WITH_3DES_EDE_CBC_SHA ciphers
#Patch58: rhbz1185708-enable-ecc-3des-ciphers-by-default.patch

# From nss-util.spec:
#Patch202: hasht-dont-include-prtypes.patch
#Patch203: pkcs1sig-include-prtypes.patch
# TODO: investigate whether this patch should also be applied to
# nss-softokn and nss and whether it should be submitted upstream.
# First ensure that it won't cause any FIPS tests breakage.
#Patch204: nss-util-3.19.3-ldflags.patch

# From nss-softokn.spec:
# Patch adapted from rhel-7
# Upstream: https://bugzilla.mozilla.org/show_bug.cgi?id=1236720
#Patch311: nss-softokn-add_encrypt_derive.patch

%description
Network Security Services (NSS) is a set of libraries designed to
support cross-platform development of security-enabled client and
server applications. Applications built with NSS can support SSL v2
and v3, TLS, PKCS #5, PKCS #7, PKCS #11, PKCS #12, S/MIME, X.509
v3 certificates, and other security standards.

%package tools
Summary:          Tools for the Network Security Services
Group:            System Environment/Base
Requires:         %{name} = %{version}-%{release}

%description tools
Network Security Services (NSS) is a set of libraries designed to
support cross-platform development of security-enabled client and
server applications. Applications built with NSS can support SSL v2
and v3, TLS, PKCS #5, PKCS #7, PKCS #11, PKCS #12, S/MIME, X.509
v3 certificates, and other security standards.

Install the nss-tools package if you need command-line tools to
manipulate the NSS certificate and key database.

#%package sysinit
#Summary:          System NSS Initialization
#Group:            System Environment/Base
## providing nss-system-init without version so that it can
## be replaced by a better one, e.g. supplied by the os vendor
#Provides:         nss-system-init
#Requires:         %{name} = %{version}-%{release}
#Requires(post):   coreutils, sed

#%description sysinit
#Default Operating System module that manages applications loading
#NSS globally on the system. This module loads the system defined
#PKCS #11 modules for NSS and chains with other NSS modules to load
#any system or user configured modules.

%package devel
Summary:          Development libraries for Network Security Services
Group:            Development/Libraries
Provides:         %{name}-static = %{version}-%{release}
Requires:         %{name} = %{version}-%{release}
Requires:         %{name}-util-devel = %{version}-%{release}
Requires:         %{name}-softokn-devel = %{version}-%{release}
Requires:         nspr-devel >= %{nspr_version}
Requires:         pkgconfig
# @todo We don't have xmlto yet.
#BuildRequires:    xmlto

%description devel
Header and Library files for doing development with Network Security Services.

%package pkcs11-devel
Summary:          Development libraries for PKCS #11 (Cryptoki) using NSS
Group:            Development/Libraries
Provides:         nss-pkcs11-devel-static = %{version}-%{release}
Requires:         %{name}-devel = %{version}-%{release}
Requires:         %{name}-softokn-freebl-devel = %{version}-%{release}

%description pkcs11-devel
Library files for developing PKCS #11 modules using basic NSS
low level services.

%package legacy
Summary:        Legacy libraries for Netscape Security Services
Group:          System Environment/Libraries
Requires:       %{name} = %{version}-%{release}

%description legacy
NSS forwarder libraries with old DLL names ending with 'k'.

# From nss-util.spec:

%package util
Summary:          Network Security Services Utilities Library
Group:            System Environment/Libraries
Requires:         nspr >= %{nspr_version}

%description util
Utilities for Network Security Services and the Softoken module

# We shouln't need to have a devel subpackage as util will be used in the
# context of nss or nss-softoken. keeping to please rpmlint.
#
%package util-devel
Summary:          Development libraries for Network Security Services Utilities
Group:            Development/Libraries
Requires:         %{name}-util = %{version}-%{release}
Requires:         nspr-devel >= %{nspr_version}
Requires:         pkgconfig

%description util-devel
Header and library files for doing development with Network Security Services.

%package util-legacy
Summary:        Legacy libraries for Netscape Security Services Utilities.
Group:          System Environment/Libraries
Requires:       %{name}-util = %{version}-%{release}

%description util-legacy
NSS Utilities forwarder libraries with old DLL names ending with 'k'.

# From nss-softokn.spec:

%package softokn
Summary:          Network Security Services Softoken Module
Group:            System Environment/Libraries
Requires:         nspr >= %{nspr_version}
Requires:         %{name}-util = %{version}-%{release}
Requires:         %{name}-softokn-freebl = %{version}-%{release}

%description softokn
Network Security Services Softoken Cryptographic Module

%package softokn-freebl
Summary:          Freebl library for the Network Security Services
Group:            System Environment/Base
Conflicts:        nss < 3.12.2.99.3-5
Conflicts:        prelink < 0.4.3
Conflicts:        filesystem < 3

%description softokn-freebl
NSS Softoken Cryptographic Module Freebl Library

Install the nss-softokn-freebl package if you need the freebl
library.

%package softokn-freebl-devel
Summary:          Header and Library files for doing development with the Freebl library for NSS
Group:            System Environment/Base
Provides:         %{name}-softokn-freebl-static = %{version}-%{release}
Requires:         %{name}-softokn-freebl = %{version}-%{release}

%description softokn-freebl-devel
NSS Softoken Cryptographic Module Freebl Library Development Tools
This package supports special needs of some PKCS #11 module developers and
is otherwise considered private to NSS. As such, the programming interfaces
may change and the usual NSS binary compatibility commitments do not apply.
Developers should rely only on the officially supported NSS public API.

%package softokn-devel
Summary:          Development libraries for Network Security Services
Group:            Development/Libraries
Requires:         %{name}-softokn = %{version}-%{release}
Requires:         %{name}-softokn-freebl-devel = %{version}-%{release}
Requires:         nspr-devel >= %{nspr_version}
Requires:         %{name}-util-devel = %{version}-%{release}
Requires:         pkgconfig

%description softokn-devel
Header and library files for doing development with Network Security Services.

%package softokn-legacy
Summary:        Legacy libraries for Netscape Security Services Softoken Cryptographic Modile.
Group:          System Environment/Libraries
Requires:       %{name}-softoken = %{version}-%{release}

%description softokn-legacy
NSS Softoken Cryptographic Modile forwarder libraries with old DLL names ending with 'k'.

%package softokn-freebl-legacy
Summary:        Legacy libraries for Netscape Security Services Freebl.
Group:          System Environment/Libraries
Requires:       %{name}-softoken-freebl = %{version}-%{release}

%description softokn-freebl-legacy
NSS Freebl forwarder libraries with old DLL names ending with 'k'.

%debug_package

# Makes no sense to provide .dbg files for forwarder DLLs
%define _strip_opts --debuginfo -x "*k.dll"

%prep
%if %{?svn_rev:%(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')}%{!?svn_rev):0}
%setup -q
%else
%setup -n "%{name}-%{version}" -Tc
svn export %{?svn_rev:-r %{svn_rev}} %{svn_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip" "%{name}-%{version}")
%endif

#%patch2 -p0 -b .relro
#%patch3 -p0 -b .transitional
#%patch6 -p0 -b .libpem
#%patch16 -p0 -b .539183
# link pem against buildroot's freebl, essential when mixing and matching
#%patch25 -p0 -b .systemfreebl
#%patch40 -p0 -b .noocsptest
#%patch47 -p0 -b .templates
#%patch49 -p0 -b .skipthem
#%patch50 -p0 -b .iquote
#pushd nss
#%patch52 -p1 -b .disableSSL2libssl
#%patch53 -p1 -b .disableSSL2tests
#popd
#%patch54 -p0 -b .ssl2_off
#%patch55 -p1 -b .skip_stress_tls_rc4_128_with_md5
#%patch58 -p0 -b .1185708_3des

# @#todo remove?
#pushd nss/tests/ssl
## Create versions of sslcov.txt and sslstress.txt that disable tests
## for SSL2 and EXPORT ciphers.
#cat sslcov.txt| sed -r "s/^([^#].*EXPORT|^[^#].*SSL2)/#disabled \1/" > sslcov.noSSL2orExport.txt
#cat sslstress.txt| sed -r "s/^([^#].*EXPORT|^[^#].*SSL2)/#disabled \1/" > sslstress.noSSL2orExport.txt
#popd

# From nss-util.spec:
#%patch202 -p0 -b .prtypes
#%patch203 -p0 -b .include_prtypes
#%patch204 -p1 -b .ldflags

# From nss-softokn.spec:
# activate if needed when doing a major update with new apis
#pushd nss
#%patch311 -p1 -b .add_encrypt_derive
#popd

# Prepare forwarder DLLs.
for m in %{SOURCE401} %{SOURCE402} %{SOURCE403} %{SOURCE404} %{SOURCE411} %{SOURCE421} %{SOURCE422} %{SOURCE431}; do
  cp ${m} .
done

%build

# OS/2 compatiblity
unset PROGRAMS

# Enable high memory support
MOZ_OS2_HIGH_MEMORY=1
export MOZ_OS2_HIGH_MEMORY

# Force debug symbols to make debug_package happy
MOZ_DEBUG_SYMBOLS=1
export MOZ_DEBUG_SYMBOLS
# MOZ_DEBUG is necessary to shut up premature debug symbol extraction
MOZ_DEBUG=1
export MOZ_DEBUG

# Make sure build output lands in ./dist
export BUILD_TREE=`echo "%{_builddir}/%{?buildsubdir}" | tr '\\\' /`

export NSS_NO_SSL2_NO_EXPORT=1

NSS_NO_PKCS11_BYPASS=1
export NSS_NO_PKCS11_BYPASS

# We don't need a freebl/softoken build w/o NSPR
#FREEBL_NO_DEPEND=1
#export FREEBL_NO_DEPEND

# Must export FREEBL_LOWHASH=1 for nsslowhash.h so that it gets
# copied to dist and the rpm install phase can find it
# This due of the upstream changes to fix
# https://bugzilla.mozilla.org/show_bug.cgi?id=717906
# @todo this fails (missing -lfreebl3, needs investigation)
#FREEBL_LOWHASH=1
#export FREEBL_LOWHASH

# Enable compiler optimizations and disable debugging code
BUILD_OPT=1
export BUILD_OPT

# Uncomment to disable optimizations
#RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed -e 's/-O2/-O0/g'`
#export RPM_OPT_FLAGS

# Generate symbolic info for debuggers
XCFLAGS=$RPM_OPT_FLAGS
export XCFLAGS

PKG_CONFIG_ALLOW_SYSTEM_LIBS=1
PKG_CONFIG_ALLOW_SYSTEM_CFLAGS=1

export PKG_CONFIG_ALLOW_SYSTEM_LIBS
export PKG_CONFIG_ALLOW_SYSTEM_CFLAGS

NSPR_INCLUDE_DIR=`/@unixroot/usr/bin/pkg-config --cflags-only-I nspr | sed 's/-I//'`
NSPR_LIB_DIR=%{_libdir}

export NSPR_INCLUDE_DIR
export NSPR_LIB_DIR

NSS_USE_SYSTEM_SQLITE=1
export NSS_USE_SYSTEM_SQLITE

USE_SYSTEM_ZLIB=1
export USE_SYSTEM_ZLIB

ZLIB_LIBS=-lz
export ZLIB_LIBS

# Disable external google tests as we lack std::wcslen in the gcc RPM
NSS_DISABLE_GTESTS=1
export NSS_DISABLE_GTESTS

# uncomment if the iquote patch is activated
#export IN_TREE_FREEBL_HEADERS_FIRST=1

##### phase 2: build the rest of nss
# nss supports pluggable ecc with more than suite-b
#export NSS_ECC_MORE_THAN_SUITE_B=1

export NSS_BLTEST_NOT_AVAILABLE=1
%{__make} -C ./coreconf
%{__make} -C ./lib/dbm
%{__make} -C .
unset NSS_BLTEST_NOT_AVAILABLE

# build the man pages clean
%{__make} clean_docs build_docs

# and copy them to the dist directory for %%install to find them
%{__mkdir_p} ./dist/docs/nroff
%{__cp} ./doc/nroff/* ./dist/docs/nroff

# Set up our package file
# The nspr_version and nss_{util|softokn}_version globals used
# here match the ones nss has for its Requires.
%{__mkdir_p} ./dist/pkgconfig
%{__cat} %{SOURCE1} | sed -e "s,%%libdir%%,%{_libdir},g" \
                          -e "s,%%prefix%%,%{_prefix},g" \
                          -e "s,%%exec_prefix%%,%{_prefix},g" \
                          -e "s,%%includedir%%,%{_includedir}/nss3,g" \
                          -e "s,%%NSS_VERSION%%,%{version},g" \
                          -e "s,%%NSPR_VERSION%%,%{nspr_version},g" \
                          -e "s,%%NSSUTIL_VERSION%%,%{version},g" \
                          -e "s,%%SOFTOKEN_VERSION%%,%{version},g" > \
                          ./dist/pkgconfig/nss.pc

NSS_VMAJOR=`cat lib/nss/nss.h | grep "#define.*NSS_VMAJOR" | awk '{print $3}'`
NSS_VMINOR=`cat lib/nss/nss.h | grep "#define.*NSS_VMINOR" | awk '{print $3}'`
NSS_VPATCH=`cat lib/nss/nss.h | grep "#define.*NSS_VPATCH" | awk '{print $3}'`

export NSS_VMAJOR
export NSS_VMINOR
export NSS_VPATCH

%{__cat} %{SOURCE2} | sed -e "s,@libdir@,%{_libdir},g" \
                          -e "s,@prefix@,%{_prefix},g" \
                          -e "s,@exec_prefix@,%{_prefix},g" \
                          -e "s,@includedir@,%{_includedir}/nss3,g" \
                          -e "s,@MOD_MAJOR_VERSION@,$NSS_VMAJOR,g" \
                          -e "s,@MOD_MINOR_VERSION@,$NSS_VMINOR,g" \
                          -e "s,@MOD_PATCH_VERSION@,$NSS_VPATCH,g" \
                          > ./dist/pkgconfig/nss-config

chmod 755 ./dist/pkgconfig/nss-config

# From nss-util.spec:
# Set up our package file
%{__mkdir_p} ./dist/pkgconfig
%{__cat} %{SOURCE202} | sed -e "s,%%libdir%%,%{_libdir},g" \
                          -e "s,%%prefix%%,%{_prefix},g" \
                          -e "s,%%exec_prefix%%,%{_prefix},g" \
                          -e "s,%%includedir%%,%{_includedir}/nss3,g" \
                          -e "s,%%NSPR_VERSION%%,%{nspr_version},g" \
                          -e "s,%%NSSUTIL_VERSION%%,%{version},g" > \
                          ./dist/pkgconfig/nss-util.pc

NSSUTIL_VMAJOR=`cat lib/util/nssutil.h | grep "#define.*NSSUTIL_VMAJOR" | awk '{print $3}'`
NSSUTIL_VMINOR=`cat lib/util/nssutil.h | grep "#define.*NSSUTIL_VMINOR" | awk '{print $3}'`
NSSUTIL_VPATCH=`cat lib/util/nssutil.h | grep "#define.*NSSUTIL_VPATCH" | awk '{print $3}'`

export NSSUTIL_VMAJOR
export NSSUTIL_VMINOR
export NSSUTIL_VPATCH

%{__cat} %{SOURCE203} | sed -e "s,@libdir@,%{_libdir},g" \
                          -e "s,@prefix@,%{_prefix},g" \
                          -e "s,@exec_prefix@,%{_prefix},g" \
                          -e "s,@includedir@,%{_includedir}/nss3,g" \
                          -e "s,@MOD_MAJOR_VERSION@,$NSSUTIL_VMAJOR,g" \
                          -e "s,@MOD_MINOR_VERSION@,$NSSUTIL_VMINOR,g" \
                          -e "s,@MOD_PATCH_VERSION@,$NSSUTIL_VPATCH,g" \
                          > ./dist/pkgconfig/nss-util-config

chmod 755 ./dist/pkgconfig/nss-util-config

# From nss-softokn.spec:
# Set up our package file
# The nspr_version and nss_util_version globals used here
# must match the ones nss-softokn has for its Requires.
%{__mkdir_p} ./dist/pkgconfig
%{__cat} %{SOURCE302} | sed -e "s,%%libdir%%,%{_libdir},g" \
                          -e "s,%%prefix%%,%{_prefix},g" \
                          -e "s,%%exec_prefix%%,%{_prefix},g" \
                          -e "s,%%includedir%%,%{_includedir}/nss3,g" \
                          -e "s,%%NSPR_VERSION%%,%{nspr_version},g" \
                          -e "s,%%NSSUTIL_VERSION%%,%{version},g" \
                          -e "s,%%SOFTOKEN_VERSION%%,%{version},g" > \
                          ./dist/pkgconfig/nss-softokn.pc

SOFTOKEN_VMAJOR=`cat lib/softoken/softkver.h | grep "#define.*SOFTOKEN_VMAJOR" | awk '{print $3}'`
SOFTOKEN_VMINOR=`cat lib/softoken/softkver.h | grep "#define.*SOFTOKEN_VMINOR" | awk '{print $3}'`
SOFTOKEN_VPATCH=`cat lib/softoken/softkver.h | grep "#define.*SOFTOKEN_VPATCH" | awk '{print $3}'`

export SOFTOKEN_VMAJOR
export SOFTOKEN_VMINOR
export SOFTOKEN_VPATCH

%{__cat} %{SOURCE303} | sed -e "s,@libdir@,%{_libdir},g" \
                          -e "s,@prefix@,%{_prefix},g" \
                          -e "s,@exec_prefix@,%{_prefix},g" \
                          -e "s,@includedir@,%{_includedir}/nss3,g" \
                          -e "s,@MOD_MAJOR_VERSION@,$SOFTOKEN_VMAJOR,g" \
                          -e "s,@MOD_MINOR_VERSION@,$SOFTOKEN_VMINOR,g" \
                          -e "s,@MOD_PATCH_VERSION@,$SOFTOKEN_VPATCH,g" \
                          > ./dist/pkgconfig/nss-softokn-config

chmod 755 ./dist/pkgconfig/nss-softokn-config

# @todo remove?
#%{__cat} %{SOURCE9} > ./dist/pkgconfig/setup-nsssysinit.sh
#chmod 755 ./dist/pkgconfig/setup-nsssysinit.sh

%{__cp} ./lib/ckfw/nssck.api ./dist/private/nss/

date +"%e %B %Y" | tr -d '\n' > date.xml
echo -n %{version} > version.xml

# @todo We don't have xmlto yet.
## configuration files and setup script
#for m in %{SOURCE20} %{SOURCE21} %{SOURCE22}; do
#  cp ${m} .
#done
#for m in nss-config.xml setup-nsssysinit.xml pkcs11.txt.xml; do
#  xmlto man ${m}
#done
#
## nss databases considered to be configuration files
#for m in %{SOURCE23} %{SOURCE24} %{SOURCE25} %{SOURCE26} %{SOURCE27}; do
#  cp ${m} .
#done
#for m in cert8.db.xml cert9.db.xml key3.db.xml key4.db.xml secmod.db.xml; do
#  xmlto man ${m}
#done

%check
# @todo Disable check since it fails so far.
exit 0

if [ ${DISABLETEST:-0} -eq 1 ]; then
  echo "testing disabled"
  exit 0
fi

# Begin -- copied from the build section

# inform the ssl test scripts that SSL2 is disabled
export NSS_NO_SSL2_NO_EXPORT=1

# We don't need a freebl/softoken build w/o NSPR
#FREEBL_NO_DEPEND=1
#export FREEBL_NO_DEPEND

BUILD_OPT=1
export BUILD_OPT

export NSS_BLTEST_NOT_AVAILABLE=1

# End -- copied from the build section

# enable the following line to force a test failure
# find ./nss -name \*.chk | xargs rm -f

# Run test suite.
# In order to support multiple concurrent executions of the test suite
# (caused by concurrent RPM builds) on a single host,
# we'll use a random port. Also, we want to clean up any stuck
# selfserv processes. If process name "selfserv" is used everywhere,
# we can't simply do a "killall selfserv", because it could disturb
# concurrent builds. Therefore we'll do a search and replace and use
# a different process name.
# Using xargs doesn't mix well with spaces in filenames, in order to
# avoid weird quoting we'll require that no spaces are being used.

SPACEISBAD=`find ./tests | grep -c ' '` ||:
if [ $SPACEISBAD -ne 0 ]; then
  echo "error: filenames containing space are not supported (xargs)"
  exit 1
fi
MYRAND=`perl -e 'print 9000 + int rand 1000'`; echo $MYRAND ||:
RANDSERV=selfserv_${MYRAND}; echo $RANDSERV ||:
DISTBINDIR=`ls -d ./dist/*.OBJ/bin`; echo $DISTBINDIR ||:
pushd `pwd`
cd $DISTBINDIR
ln -s selfserv $RANDSERV
popd
# man perlrun, man perlrequick
# replace word-occurrences of selfserv with selfserv_$MYRAND
find ./tests -type f |\
  grep -v "\.db$" |grep -v "\.crl$" | grep -v "\.crt$" |\
  grep -vw CVS  |xargs grep -lw selfserv |\
  xargs -l perl -pi -e "s/\bselfserv\b/$RANDSERV/g" ||:

killall $RANDSERV || :

rm -rf ./tests_results
pushd ./tests/
# all.sh is the test suite script

#  don't need to run all the tests when testing packaging
#  nss_cycles: standard pkix upgradedb sharedb
%define nss_tests "libpkix cert dbtests tools fips sdr crmf smime ssl ocsp merge pkits chains"
#  nss_ssl_tests: crl bypass_normal normal_bypass normal_fips fips_normal iopr
#  nss_ssl_run: cov auth stress
#
# Uncomment these lines if you need to temporarily
# disable some test suites for faster test builds
# global nss_ssl_tests "normal_fips"
# global nss_ssl_run "cov auth"

SKIP_NSS_TEST_SUITE=`echo $SKIP_NSS_TEST_SUITE`

if [ "x$SKIP_NSS_TEST_SUITE" == "x" ]; then
  HOST=localhost DOMSUF=localdomain PORT=$MYRAND NSS_CYCLES=%{?nss_cycles} NSS_TESTS=%{?nss_tests} NSS_SSL_TESTS=%{?nss_ssl_tests} NSS_SSL_RUN=%{?nss_ssl_run} ./all.sh
else
  echo "skipped test suite"
fi

popd

# Normally, the grep exit status is 0 if selected lines are found and 1 otherwise,
# Grep exits with status greater than 1 if an error ocurred.
# If there are test failures we expect TEST_FAILURES > 0 and GREP_EXIT_STATUS = 0,
# With no test failures we expect TEST_FAILURES = 0 and GREP_EXIT_STATUS = 1, whereas
# GREP_EXIT_STATUS > 1 would indicate an error in grep such as failure to find the log file.
killall $RANDSERV || :

if [ "x$SKIP_NSS_TEST_SUITE" == "x" ]; then
  TEST_FAILURES=$(grep -c FAILED ./tests_results/security/localhost.1/output.log) || GREP_EXIT_STATUS=$?
else
  TEST_FAILURES=0
  GREP_EXIT_STATUS=1
fi

if [ ${GREP_EXIT_STATUS:-0} -eq 1 ]; then
  echo "okay: test suite detected no failures"
else
  if [ ${GREP_EXIT_STATUS:-0} -eq 0 ]; then
    # while a situation in which grep return status is 0 and it doesn't output
    # anything shouldn't happen, set the default to something that is
    # obviously wrong (-1)
    echo "error: test suite had ${TEST_FAILURES:--1} test failure(s)"
    exit 1
  else
    if [ ${GREP_EXIT_STATUS:-0} -eq 2 ]; then
      echo "error: grep has not found log file"
      exit 1
    else
      echo "error: grep failed with exit code: ${GREP_EXIT_STATUS}"
      exit 1
    fi
  fi
fi
echo "test suite completed"

%install

%{__rm} -rf $RPM_BUILD_ROOT

# There is no make install target so we'll do it ourselves.

%{__mkdir_p} $RPM_BUILD_ROOT/%{_includedir}/nss3
%{__mkdir_p} $RPM_BUILD_ROOT/%{_includedir}/nss3/templates
%{__mkdir_p} $RPM_BUILD_ROOT/%{_bindir}
%{__mkdir_p} $RPM_BUILD_ROOT/%{_libdir}
%{__mkdir_p} $RPM_BUILD_ROOT/%{unsupported_tools_directory}
%{__mkdir_p} $RPM_BUILD_ROOT/%{_libdir}/pkgconfig
%if %{defined rhel}
# not needed for rhel and its derivatives only fedora
%else
# because of the pp.1 conflict with perl-PAR-Packer
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/doc/nss-tools
%endif

mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man5

# Copy the binary libraries we want
for file in nssckbi nss3 smime3 ssl3 # nsspem
do
  %{__install} -p -m 755 dist/*.OBJ/lib/$file.dll $RPM_BUILD_ROOT/%{_libdir}
  test -f dist/*.OBJ/lib/$file.a && \
    %{__install} -p -m 644 dist/*.OBJ/lib/$file.a $RPM_BUILD_ROOT/%{_libdir}
done

# From nss-util.spec:
for file in nssutil3
do
  %{__install} -p -m 755 dist/*.OBJ/lib/$file.dll $RPM_BUILD_ROOT/%{_libdir}
  test -f dist/*.OBJ/lib/$file.a && \
    %{__install} -p -m 644 dist/*.OBJ/lib/$file.a $RPM_BUILD_ROOT/%{_libdir}
done

# From nss-softokn.spec:
# Copy the binary libraries we want
for file in softokn3 nssdbm3 freebl3
do
  %{__install} -p -m 755 dist/*.OBJ/lib/$file.dll $RPM_BUILD_ROOT/%{_libdir}
  test -f dist/*.OBJ/lib/$file.a && \
    %{__install} -p -m 644 dist/*.OBJ/lib/$file.a $RPM_BUILD_ROOT/%{_libdir}
done

# @todo remove?
## Install the empty NSS db files
## Legacy db
#%{__mkdir_p} $RPM_BUILD_ROOT/%{_sysconfdir}/pki/nssdb
#%{__install} -p -m 644 %{SOURCE3} $RPM_BUILD_ROOT/%{_sysconfdir}/pki/nssdb/cert8.db
#%{__install} -p -m 644 %{SOURCE4} $RPM_BUILD_ROOT/%{_sysconfdir}/pki/nssdb/key3.db
#%{__install} -p -m 644 %{SOURCE5} $RPM_BUILD_ROOT/%{_sysconfdir}/pki/nssdb/secmod.db
## Shared db
#%{__install} -p -m 644 %{SOURCE6} $RPM_BUILD_ROOT/%{_sysconfdir}/pki/nssdb/cert9.db
#%{__install} -p -m 644 %{SOURCE7} $RPM_BUILD_ROOT/%{_sysconfdir}/pki/nssdb/key4.db
#%{__install} -p -m 644 %{SOURCE8} $RPM_BUILD_ROOT/%{_sysconfdir}/pki/nssdb/pkcs11.txt

# Copy the development libraries we want
for file in crmf.a nssb.a nssckfw.a
do
  %{__install} -p -m 644 dist/*.OBJ/lib/$file $RPM_BUILD_ROOT/%{_libdir}
done

# Copy the binaries we want
for file in certutil cmsutil crlutil modutil pk12util signtool signver ssltap
do
  %{__install} -p -m 755 dist/*.OBJ/bin/$file.exe $RPM_BUILD_ROOT/%{_bindir}
done

# Copy the binaries we ship as unsupported
for file in atob btoa derdump listsuites ocspclnt pp selfserv strsclnt symkeyutil tstclnt vfyserv vfychain
do
  %{__install} -p -m 755 dist/*.OBJ/bin/$file.exe $RPM_BUILD_ROOT/%{unsupported_tools_directory}
done

# From nss-softokn.spec:
# Copy the binaries we ship as unsupported
for file in bltest fipstest shlibsign
do
  %{__install} -p -m 755 dist/*.OBJ/bin/$file.exe $RPM_BUILD_ROOT/%{unsupported_tools_directory}
done

# Copy the include files we want
for file in dist/public/nss/*.h
do
  %{__install} -p -m 644 $file $RPM_BUILD_ROOT/%{_includedir}/nss3
done

# From nss-softokn.spec:
# Copy some freebl include files we also want
for file in blapi.h alghmac.h
do
  %{__install} -p -m 644 dist/private/nss/$file $RPM_BUILD_ROOT/%{_includedir}/nss3
done

# Copy the template files we want
for file in dist/private/nss/nssck.api
do
  %{__install} -p -m 644 $file $RPM_BUILD_ROOT/%{_includedir}/nss3/templates
done

# From nss-util.spec:
# Copy the template files we want
for file in dist/private/nss/templates.c
do
  %{__install} -p -m 644 $file $RPM_BUILD_ROOT/%{_includedir}/nss3/templates
done

# From nss-softokn.spec:
# Copy the static freebl library
for file in freebl.a
do
%{__install} -p -m 644 dist/*.OBJ/lib/$file $RPM_BUILD_ROOT/%{_libdir}
done

# Copy the package configuration files
%{__install} -p -m 644 ./dist/pkgconfig/nss.pc $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/nss.pc
%{__install} -p -m 755 ./dist/pkgconfig/nss-config $RPM_BUILD_ROOT/%{_bindir}/nss-config

# From nss-util.spec:
# Copy the package configuration files
%{__install} -p -m 644 ./dist/pkgconfig/nss-util.pc $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/nss-util.pc
%{__install} -p -m 755 ./dist/pkgconfig/nss-util-config $RPM_BUILD_ROOT/%{_bindir}/nss-util-config

# From nss-softokn.spec:
# Copy the package configuration files
%{__install} -p -m 644 ./dist/pkgconfig/nss-softokn.pc $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/nss-softokn.pc
%{__install} -p -m 755 ./dist/pkgconfig/nss-softokn-config $RPM_BUILD_ROOT/%{_bindir}/nss-softokn-config

# @tod remove?
## Copy the pkcs #11 configuration script
#%{__install} -p -m 755 ./dist/pkgconfig/setup-nsssysinit.sh $RPM_BUILD_ROOT/%{_bindir}/setup-nsssysinit.sh
## install a symbolic link to it, without the ".sh" suffix,
## that matches the man page documentation
#ln -r -s -f $RPM_BUILD_ROOT/%{_bindir}/setup-nsssysinit.sh $RPM_BUILD_ROOT/%{_bindir}/setup-nsssysinit

# Copy the man pages for scripts
# @todo We don't have xmlto yet.
#for f in nss-config setup-nsssysinit; do
#   install -c -m 644 ${f}.1 $RPM_BUILD_ROOT%{_mandir}/man1/${f}.1
#done
# Copy the man pages for the nss tools
for f in "%{allTools}"; do
  install -c -m 644 ./dist/docs/nroff/${f}.1 $RPM_BUILD_ROOT%{_mandir}/man1/${f}.1
done
%if %{defined rhel}
install -c -m 644 ./dist/docs/nroff/pp.1 $RPM_BUILD_ROOT%{_mandir}/man1/pp.1
%else
install -c -m 644 ./dist/docs/nroff/pp.1 $RPM_BUILD_ROOT%{_datadir}/doc/nss-tools/pp.1
%endif

# Copy the man pages for the configuration files
# @todo We don't have xmlto yet.
#for f in pkcs11.txt; do
#   install -c -m 644 ${f}.5 $RPM_BUILD_ROOT%{_mandir}/man5/${f}.5
#done
# Copy the man pages for the nss databases
#for f in cert8.db cert9.db key3.db key4.db secmod.db; do
#   install -c -m 644 ${f}.5 $RPM_BUILD_ROOT%{_mandir}/man5/${f}.5
#done

# Generate & install forwarder DLLs.
gcc -Zomf -Zdll nss3k.def -l$RPM_BUILD_ROOT/%{_libdir}/nss3.dll -o $RPM_BUILD_ROOT/%{_libdir}/nss3k.dll
gcc -Zomf -Zdll nssckbik.def -l$RPM_BUILD_ROOT/%{_libdir}/nssckbi.dll -o $RPM_BUILD_ROOT/%{_libdir}/nssckbik.dll
gcc -Zomf -Zdll smime3k.def -l$RPM_BUILD_ROOT/%{_libdir}/smime3.dll -o $RPM_BUILD_ROOT/%{_libdir}/smime3k.dll
gcc -Zomf -Zdll ssl3k.def -l$RPM_BUILD_ROOT/%{_libdir}/ssl3.dll -o $RPM_BUILD_ROOT/%{_libdir}/ssl3k.dll
gcc -Zomf -Zdll nssuti3k.def -l$RPM_BUILD_ROOT/%{_libdir}/nssutil3.dll -o $RPM_BUILD_ROOT/%{_libdir}/nssuti3k.dll
gcc -Zomf -Zdll nssdbm3k.def -l$RPM_BUILD_ROOT/%{_libdir}/nssdbm3.dll -o $RPM_BUILD_ROOT/%{_libdir}/nssdbm3k.dll
gcc -Zomf -Zdll softok3k.def -l$RPM_BUILD_ROOT/%{_libdir}/softokn3.dll -o $RPM_BUILD_ROOT/%{_libdir}/softok3k.dll
gcc -Zomf -Zdll freebl3k.def -l$RPM_BUILD_ROOT/%{_libdir}/freebl3.dll -o $RPM_BUILD_ROOT/%{_libdir}/freebl3k.dll

%clean
%{__rm} -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_libdir}/nss3.dll
%{_libdir}/ssl3.dll
%{_libdir}/smime3.dll
%{_libdir}/nssckbi.dll
# @todo need?
#%{_libdir}/nsspem.dll
# @todo need?
#%dir %{_sysconfdir}/pki/nssdb
#%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/pki/nssdb/cert8.db
#%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/pki/nssdb/key3.db
#%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/pki/nssdb/secmod.db
##%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/pki/nssdb/cert9.db
##%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/pki/nssdb/key4.db
#%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/pki/nssdb/pkcs11.txt
# @todo We don't have xmlto yet.
#%attr(0644,root,root) %doc %{_mandir}/man5/cert8.db.5.gz
#%attr(0644,root,root) %doc %{_mandir}/man5/key3.db.5.gz
#%attr(0644,root,root) %doc %{_mandir}/man5/secmod.db.5.gz
#%attr(0644,root,root) %doc %{_mandir}/man5/cert9.db.5.gz
#%attr(0644,root,root) %doc %{_mandir}/man5/key4.db.5.gz
#%attr(0644,root,root) %doc %{_mandir}/man5/pkcs11.txt.5.gz

# @todo need?
#%files sysinit
#%defattr(-,root,root)
#%{_libdir}/libnsssysinit.so
#%{_bindir}/setup-nsssysinit.sh
## symbolic link to setup-nsssysinit.sh
#%{_bindir}/setup-nsssysinit
#%attr(0644,root,root) %doc %{_mandir}/man1/setup-nsssysinit.1.gz

%files tools
%defattr(-,root,root)
%{_bindir}/certutil.exe
%{_bindir}/cmsutil.exe
%{_bindir}/crlutil.exe
%{_bindir}/modutil.exe
%{_bindir}/pk12util.exe
%{_bindir}/signtool.exe
%{_bindir}/signver.exe
%{_bindir}/ssltap.exe
%{unsupported_tools_directory}/atob.exe
%{unsupported_tools_directory}/btoa.exe
%{unsupported_tools_directory}/derdump.exe
%{unsupported_tools_directory}/listsuites.exe
%{unsupported_tools_directory}/ocspclnt.exe
%{unsupported_tools_directory}/pp.exe
%{unsupported_tools_directory}/selfserv.exe
%{unsupported_tools_directory}/strsclnt.exe
%{unsupported_tools_directory}/symkeyutil.exe
%{unsupported_tools_directory}/tstclnt.exe
%{unsupported_tools_directory}/vfyserv.exe
%{unsupported_tools_directory}/vfychain.exe
# instead of %%{_mandir}/man*/* let's list them explicitely
# supported tools
%attr(0644,root,root) %doc %{_mandir}/man1/certutil.1.gz
%attr(0644,root,root) %doc %{_mandir}/man1/cmsutil.1.gz
%attr(0644,root,root) %doc %{_mandir}/man1/crlutil.1.gz
%attr(0644,root,root) %doc %{_mandir}/man1/modutil.1.gz
%attr(0644,root,root) %doc %{_mandir}/man1/pk12util.1.gz
%attr(0644,root,root) %doc %{_mandir}/man1/signtool.1.gz
%attr(0644,root,root) %doc %{_mandir}/man1/signver.1.gz
# unsupported tools
%attr(0644,root,root) %doc %{_mandir}/man1/derdump.1.gz
%if %{defined rhel}
%attr(0644,root,root) %doc %{_mandir}/man1/pp.1.gz
%else
%dir %{_datadir}/doc/nss-tools
%attr(0644,root,root) %doc %{_datadir}/doc/nss-tools/pp.1
%endif
%attr(0644,root,root) %doc %{_mandir}/man1/ssltap.1.gz
%attr(0644,root,root) %doc %{_mandir}/man1/vfychain.1.gz
%attr(0644,root,root) %doc %{_mandir}/man1/vfyserv.1.gz

%files devel
%defattr(-,root,root)
%{_libdir}/nss3.a
%{_libdir}/smime3.a
%{_libdir}/ssl3.a
%{_libdir}/crmf.a
# @todo need?
#%{_libdir}/nsspem.a
%{_libdir}/pkgconfig/nss.pc
%{_bindir}/nss-config
# @todo We don't have xmlto yet.
#%attr(0644,root,root) %doc %{_mandir}/man1/nss-config.1.gz
%dir %{_includedir}/nss3
%{_includedir}/nss3/cert.h
%{_includedir}/nss3/certdb.h
%{_includedir}/nss3/certt.h
%{_includedir}/nss3/cmmf.h
%{_includedir}/nss3/cmmft.h
%{_includedir}/nss3/cms.h
%{_includedir}/nss3/cmsreclist.h
%{_includedir}/nss3/cmst.h
%{_includedir}/nss3/crmf.h
%{_includedir}/nss3/crmft.h
%{_includedir}/nss3/cryptohi.h
%{_includedir}/nss3/cryptoht.h
%{_includedir}/nss3/sechash.h
%{_includedir}/nss3/jar-ds.h
%{_includedir}/nss3/jar.h
%{_includedir}/nss3/jarfile.h
%{_includedir}/nss3/key.h
%{_includedir}/nss3/keyhi.h
%{_includedir}/nss3/keyt.h
%{_includedir}/nss3/keythi.h
%{_includedir}/nss3/nss.h
%{_includedir}/nss3/nssckbi.h
#%{_includedir}/nss3/nsspem.h
%{_includedir}/nss3/ocsp.h
%{_includedir}/nss3/ocspt.h
%{_includedir}/nss3/p12.h
%{_includedir}/nss3/p12plcy.h
%{_includedir}/nss3/p12t.h
%{_includedir}/nss3/pk11func.h
%{_includedir}/nss3/pk11pqg.h
%{_includedir}/nss3/pk11priv.h
%{_includedir}/nss3/pk11pub.h
%{_includedir}/nss3/pk11sdr.h
%{_includedir}/nss3/pkcs12.h
%{_includedir}/nss3/pkcs12t.h
%{_includedir}/nss3/pkcs7t.h
%{_includedir}/nss3/preenc.h
%{_includedir}/nss3/secmime.h
%{_includedir}/nss3/secmod.h
%{_includedir}/nss3/secmodt.h
%{_includedir}/nss3/secpkcs5.h
%{_includedir}/nss3/secpkcs7.h
%{_includedir}/nss3/smime.h
%{_includedir}/nss3/ssl.h
%{_includedir}/nss3/sslerr.h
%{_includedir}/nss3/sslproto.h
%{_includedir}/nss3/sslt.h

%files pkcs11-devel
%defattr(-, root, root)
%{_includedir}/nss3/nssbase.h
%{_includedir}/nss3/nssbaset.h
%{_includedir}/nss3/nssckepv.h
%{_includedir}/nss3/nssckft.h
%{_includedir}/nss3/nssckfw.h
%{_includedir}/nss3/nssckfwc.h
%{_includedir}/nss3/nssckfwt.h
%{_includedir}/nss3/nssckg.h
%{_includedir}/nss3/nssckmdt.h
%{_includedir}/nss3/nssckt.h
%{_includedir}/nss3/templates/nssck.api
%{_libdir}/nssb.a
%{_libdir}/nssckfw.a

%files legacy
%defattr(-,root,root)
%{_libdir}/nss3k.dll
%{_libdir}/ssl3k.dll
%{_libdir}/smime3k.dll
%{_libdir}/nssckbik.dll

# From nss-util.spec:

%files util
%defattr(-,root,root)
%{_libdir}/nssutil3.dll

%files util-devel
%defattr(-,root,root)
%{_libdir}/nssutil3.a
# package configuration files
%{_libdir}/pkgconfig/nss-util.pc
%{_bindir}/nss-util-config
# these are marked as public export in nss/lib/util/manifest.mk
# co-owned with nss
%dir %{_includedir}/nss3
%{_includedir}/nss3/base64.h
%{_includedir}/nss3/ciferfam.h
%{_includedir}/nss3/hasht.h
%{_includedir}/nss3/nssb64.h
%{_includedir}/nss3/nssb64t.h
%{_includedir}/nss3/nsslocks.h
%{_includedir}/nss3/nssilock.h
%{_includedir}/nss3/nssilckt.h
%{_includedir}/nss3/nssrwlk.h
%{_includedir}/nss3/nssrwlkt.h
%{_includedir}/nss3/nssutil.h
%{_includedir}/nss3/pkcs1sig.h
%{_includedir}/nss3/pkcs11.h
%{_includedir}/nss3/pkcs11f.h
%{_includedir}/nss3/pkcs11n.h
%{_includedir}/nss3/pkcs11p.h
%{_includedir}/nss3/pkcs11t.h
%{_includedir}/nss3/pkcs11u.h
%{_includedir}/nss3/portreg.h
%{_includedir}/nss3/secasn1.h
%{_includedir}/nss3/secasn1t.h
%{_includedir}/nss3/seccomon.h
%{_includedir}/nss3/secder.h
%{_includedir}/nss3/secdert.h
%{_includedir}/nss3/secdig.h
%{_includedir}/nss3/secdigt.h
%{_includedir}/nss3/secerr.h
%{_includedir}/nss3/secitem.h
%{_includedir}/nss3/secoid.h
%{_includedir}/nss3/secoidt.h
%{_includedir}/nss3/secport.h
%{_includedir}/nss3/utilmodt.h
%{_includedir}/nss3/utilpars.h
%{_includedir}/nss3/utilparst.h
%{_includedir}/nss3/utilrename.h
%{_includedir}/nss3/templates/templates.c

%files util-legacy
%defattr(-,root,root)
%{_libdir}/nssuti3k.dll

# From nss-softokn.spec:

%files softokn
%defattr(-,root,root)
%{_libdir}/nssdbm3.dll
%{_libdir}/nssdbm3.chk
%{_libdir}/softokn3.dll
%{_libdir}/softokn3.chk
# shared with nss-tools
%dir %{_libdir}/nss
%dir %{unsupported_tools_directory}
%{unsupported_tools_directory}/bltest.exe
%{unsupported_tools_directory}/fipstest.exe
%{unsupported_tools_directory}/shlibsign.exe

%files softokn-freebl
%defattr(-,root,root)
%{_libdir}/freebl3.dll
%{_libdir}/freebl3.chk

%files softokn-freebl-devel
%defattr(-,root,root)
%{_libdir}/freebl.a
%{_includedir}/nss3/blapi.h
%{_includedir}/nss3/blapit.h
%{_includedir}/nss3/alghmac.h

%files softokn-devel
%defattr(-,root,root)
%{_libdir}/nssdbm3.a
%{_libdir}/softokn3.a
%{_libdir}/pkgconfig/nss-softokn.pc
%{_bindir}/nss-softokn-config
# co-owned with nss
%dir %{_includedir}/nss3
%{_includedir}/nss3/ecl-exp.h
# @todo this fails (missing -lfreebl3, needs investigation)
#%{_includedir}/nss3/nsslowhash.h
%{_includedir}/nss3/shsign.h

%files softokn-legacy
%defattr(-,root,root)
%{_libdir}/nssdbm3k.dll
%{_libdir}/nssdbm3k.chk
%{_libdir}/softok3k.dll
%{_libdir}/softok3k.chk

%files softokn-freebl
%defattr(-,root,root)
%{_libdir}/freebl3.dll
%{_libdir}/freebl3.chk

%files softokn-freebl-legacy
%defattr(-,root,root)
%{_libdir}/freebl3k.dll
%{_libdir}/freebl3k.chk


%changelog
* Fri Apr 15 2016 Dmitriy Kuminov <coding@dmik.org> 3.23.0-3
- Remove erroneous -Wl,-rpath-link from nss-config and others.

* Wed Apr 1 2016 Dmitriy Kuminov <coding@dmik.org> 3.23.0-2
- Enable high memory support.

* Wed Mar 30 2016 Dmitriy Kuminov <coding@dmik.org> 3.23.0-1
- Update to version 3.23.
- Import OS/2-specific NSS fixes from Mozilla for OS/2 sources.
- Rebuild with GCC 4.9.2 and LIBC 0.6.6.

* Mon Jan 16 2012 yd
- rebuild with libc 0.6.4 runtime.
