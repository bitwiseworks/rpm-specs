%global nspr_version 4.8.6
%global nss_util_version 3.12.8
%global nss_softokn_version 3.12.8
%global unsupported_tools_directory %{_libdir}/nss/unsupported-tools

Summary:          Network Security Services
Name:             nss
Version:          3.12.8
Release:          2%{?dist}
License:          MPLv1.1 or GPLv2+ or LGPLv2+
URL:              http://www.mozilla.org/projects/security/pki/nss/
Group:            System Environment/Libraries
Requires:         nspr >= %{nspr_version}
Requires:         nss-util >= %{nss_util_version}
Requires:         nss-softokn%{_isa} >= %{nss_softokn_version}
#Requires:         nss-system-init
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:    nspr-devel >= %{nspr_version}
#BuildRequires:    nss-softokn-devel >= %{nss_softokn_version}
#BuildRequires:    nss-util-devel >= %{nss_util_version}
BuildRequires:    sqlite-devel
BuildRequires:    zlib-devel
BuildRequires:    pkgconfig
#BuildRequires:    gawk
#BuildRequires:    psmisc
#BuildRequires:    perl

Source0:          %{name}-%{version}.tar.gz

Source1:          nss.pc.in
Source2:          nss-config.in

#Source3:          blank-cert8.db
#Source4:          blank-key3.db
#Source5:          blank-secmod.db
#Source6:          blank-cert9.db
#Source7:          blank-key4.db
#Source8:          system-pkcs11.txt
#Source9:          setup-nsssysinit.sh
#Source10:         PayPalEE.cert
#Source12:         %{name}-pem-20100809.tar.bz2

Source21:          nss-util.pc.in
Source22:          nss-util-config.in

Source31:          nss-softokn.pc.in
Source32:          nss-softokn-config.in

Patch0:           nss-os2.diff
#Patch3:           renegotiate-transitional.patch
#Patch6:           nss-enable-pem.patch
#Patch7:           nsspem-596674.patch
#Patch8:           nss-sysinit-userdb-first.patch
#Patch9:           0001-Add-support-for-PKCS-8-encoded-private-keys.patch
#Patch10:          0001-Do-not-define-SEC_SkipTemplate.patch

%description
Network Security Services (NSS) is a set of libraries designed to
support cross-platform development of security-enabled client and
server applications. Applications built with NSS can support SSL v2
and v3, TLS, PKCS #5, PKCS #7, PKCS #11, PKCS #12, S/MIME, X.509
v3 certificates, and other security standards.

%package tools
Summary:          Tools for the Network Security Services
Group:            System Environment/Base
Requires:         nss = %{version}-%{release}
Requires:         zlib

%description tools
Network Security Services (NSS) is a set of libraries designed to
support cross-platform development of security-enabled client and
server applications. Applications built with NSS can support SSL v2
and v3, TLS, PKCS #5, PKCS #7, PKCS #11, PKCS #12, S/MIME, X.509
v3 certificates, and other security standards.

Install the nss-tools package if you need command-line tools to
manipulate the NSS certificate and key database.

%package sysinit
Summary:          System NSS Initilization
Group:            System Environment/Base
# providing nss-system-init without version so that it can
# be replaced by a better one, e.g. supplied by the os vendor
Provides:         nss-system-init
Requires:         nss = %{version}-%{release}
Requires(post):   coreutils, sed

%description sysinit
Default Operating System module that manages applications loading
NSS globally on the system. This module loads the system defined
PKCS #11 modules for NSS and chains with other NSS modules to load
any system or user configured modules.

%package devel
Summary:          Development libraries for Network Security Services
Group:            Development/Libraries
Requires:         nss = %{version}-%{release}
Requires:         nss-util-devel
Requires:         nss-softokn-devel 
Requires:         nspr-devel >= %{nspr_version}
Requires:         pkgconfig

%description devel
Header and Library files for doing development with Network Security Services.


%package pkcs11-devel
Summary:          Development libraries for PKCS #11 (Cryptoki) using NSS
Group:            Development/Libraries
Provides:         nss-pkcs11-devel-static = %{version}-%{release}
Requires:         nss-devel = %{version}-%{release}

%description pkcs11-devel
Library files for developing PKCS #11 modules using basic NSS 
low level services.

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
Requires:         nss-util = %{version}-%{release}
Requires:         nspr-devel >= %{nspr_version}
Requires:         pkgconfig

%description util-devel
Header and library files for doing development with Network Security Services.


%package softokn
Summary:          Network Security Services Soktoken Module
Group:            System Environment/Libraries
Requires:         nspr >= %{nspr_version}
Requires:         nss-util >= %{nss_util_version}
Requires:         nss-softokn-freebl%{_isa} >= %{version}

%description softokn
Network Security Services Softoken Cryptographic Module

%package softokn-freebl
Summary:          Freebl library for the Network Security Services
Group:            System Environment/Base
Conflicts:        nss < 3.12.2.99.3-5
Conflicts:        Prelink < 0.4.3

%description softokn-freebl
Network Security Services Softoken Cryptographic Module Freelb Library.

Install the nss-softokn-freebl package if you need the freebl 
library.

%package softokn-freebl-devel
Summary:          Header and Library files for doing development with the Freebl library for NSS
Group:            System Environment/Base
Requires:         nss-softokn-freebl = %{version}-%{release}

%description softokn-freebl-devel
Network Security Services Softoken Cryptographic Module Freelb Library Development Tools.

%package softokn-devel
Summary:          Development libraries for Network Security Services
Group:            Development/Libraries
Requires:         nss-softokn = %{version}-%{release}
Requires:         nspr-devel >= %{nspr_version}
Requires:         nss-util-devel >= %{version}
Requires:         pkgconfig
BuildRequires:    nspr-devel >= %{nspr_version}
#BuildRequires:    nss-util-devel >= %{version}
# require nss at least the version when we split via subpackages
#BuildRequires:    nss-devel >= 3.12.2.99.3-11

%description softokn-devel
Header and Library files for doing development with Network Security Services.


%prep
%setup -q
#%{__cp} %{SOURCE10} -f ./mozilla/security/nss/tests/libpkix/certs
%setup -q -T -D -n %{name}-%{version}
# -a 12

%patch0 -p1 -b .os2~

#%patch3 -p0 -b .transitional
#%patch6 -p0 -b .libpem
#%patch7 -p0 -b .596674
#%patch8 -p0 -b .603313
#%patch9 -p1 -b .pkcs8privatekey
#%patch10 -p1 -b .noskiptemplate

cp mozilla/security/nss/lib/util/nssutil.def mozilla/security/nss/lib/util/nssuti.def
cp mozilla/security/nss/lib/softoken/softokn.def mozilla/security/nss/lib/softoken/softok.def

# yd convert LF to CRLF in cmd files
sed -i '#\n#\r\n#g' mozilla/security/nss/cmd/shlibsign/sign.cmd

%build

#ecs compatibility
PROGRAMS=
export PROGRAMS
export MAKESHELL="/bin/sh"

#FREEBL_NO_DEPEND=1
#export FREEBL_NO_DEPEND

# Enable compiler optimizations and disable debugging code
BUILD_OPT=1
export BUILD_OPT

# Generate symbolic info for debuggers
XCFLAGS=$RPM_OPT_FLAGS
export XCFLAGS

PKG_CONFIG_ALLOW_SYSTEM_LIBS=1
PKG_CONFIG_ALLOW_SYSTEM_CFLAGS=1

export PKG_CONFIG_ALLOW_SYSTEM_LIBS
export PKG_CONFIG_ALLOW_SYSTEM_CFLAGS

NSPR_INCLUDE_DIR=`/@unixroot/usr/bin/pkg-config --cflags-only-I nspr | sed 's/-I//'`
NSPR_LIB_DIR=`/@unixroot/usr/bin/pkg-config --libs-only-L nspr | sed 's/[[:space:]]*$//' | sed 's/-L//'`

export NSPR_INCLUDE_DIR
export NSPR_LIB_DIR

NSS_INCLUDE_DIR=`/@unixroot/usr/bin/pkg-config --cflags-only-I nss-util | sed 's/-I//'`
NSS_LIB_DIR=`/@unixroot/usr/bin/pkg-config --libs-only-L nss-util| sed 's/[[:space:]]*$//' | sed 's/-L//'`

NSS_USE_SYSTEM_SQLITE=1
export NSS_USE_SYSTEM_SQLITE
USE_SYSTEM_ZLIB=1
export USE_SYSTEM_ZLIB

%ifarch x86_64 ppc64 ia64 s390x sparc64
USE_64=1
export USE_64
%endif

# We only ship the nss proper libraries, no softoken nor util, yet                                   
# we must compile with the entire source tree because nss needs                               
# private exports from util. The install section will ensure not
# to override nss-util and nss-softoken headers already installed.
#     

# yd smp build not safe
make -C ./mozilla/security/coreconf
# %{?_smp_mflags}
make -C ./mozilla/security/dbm
# %{?_smp_mflags}
make -C ./mozilla/security/nss
# %{?_smp_mflags}

%install

%{__rm} -rf $RPM_BUILD_ROOT


# Set up our package file
# The nspr_version and nss_{util|softokn}_version globals used
# here match the ones nss has for its Requires. 
%{__mkdir_p} ./mozilla/dist/pkgconfig
%{__cat} %{SOURCE1} | sed -e "s,%%libdir%%,%{_libdir},g" \
                          -e "s,%%prefix%%,%{_prefix},g" \
                          -e "s,%%exec_prefix%%,%{_prefix},g" \
                          -e "s,%%includedir%%,%{_includedir}/nss3,g" \
                          -e "s,%%NSS_VERSION%%,%{version},g" \
                          -e "s,%%NSPR_VERSION%%,%{nspr_version},g" \
                          -e "s,%%NSSUTIL_VERSION%%,%{nss_util_version},g" \
                          -e "s,%%SOFTOKEN_VERSION%%,%{nss_softokn_version},g" > \
                          ./mozilla/dist/pkgconfig/nss.pc

# util-Set up our package file
%{__cat} %{SOURCE21} | sed -e "s,%%libdir%%,%{_libdir},g" \
                          -e "s,%%prefix%%,%{_prefix},g" \
                          -e "s,%%exec_prefix%%,%{_prefix},g" \
                          -e "s,%%includedir%%,%{_includedir}/nss3,g" \
                          -e "s,%%NSPR_VERSION%%,%{nspr_version},g" \
                          -e "s,%%NSSUTIL_VERSION%%,%{version},g" > \
                          ./mozilla/dist/pkgconfig/nss-util.pc

# softokn-Set up our package file
%{__cat} %{SOURCE31} | sed -e "s,%%libdir%%,%{_libdir},g" \
                          -e "s,%%prefix%%,%{_prefix},g" \
                          -e "s,%%exec_prefix%%,%{_prefix},g" \
                          -e "s,%%includedir%%,%{_includedir}/nss3,g" \
                          -e "s,%%NSPR_VERSION%%,%{nspr_version},g" \
                          -e "s,%%NSSUTIL_VERSION%%,%{nss_util_version},g" \
                          -e "s,%%SOFTOKEN_VERSION%%,%{version},g" > \
                          ./mozilla/dist/pkgconfig/nss-softokn.pc

NSS_VMAJOR=`cat mozilla/security/nss/lib/nss/nss.h | grep "#define.*NSS_VMAJOR" | awk '{print $3}'`
NSS_VMINOR=`cat mozilla/security/nss/lib/nss/nss.h | grep "#define.*NSS_VMINOR" | awk '{print $3}'`
NSS_VPATCH=`cat mozilla/security/nss/lib/nss/nss.h | grep "#define.*NSS_VPATCH" | awk '{print $3}'`

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
                          > ./mozilla/dist/pkgconfig/nss-config
%{__cat} %{SOURCE22} | sed -e "s,@libdir@,%{_libdir},g" \
                          -e "s,@prefix@,%{_prefix},g" \
                          -e "s,@exec_prefix@,%{_prefix},g" \
                          -e "s,@includedir@,%{_includedir}/nss3,g" \
                          -e "s,@MOD_MAJOR_VERSION@,$NSS_VMAJOR,g" \
                          -e "s,@MOD_MINOR_VERSION@,$NSS_VMINOR,g" \
                          -e "s,@MOD_PATCH_VERSION@,$NSS_VPATCH,g" \
                          > ./mozilla/dist/pkgconfig/nss-util-config
%{__cat} %{SOURCE32} | sed -e "s,@libdir@,%{_libdir},g" \
                          -e "s,@prefix@,%{_prefix},g" \
                          -e "s,@exec_prefix@,%{_prefix},g" \
                          -e "s,@includedir@,%{_includedir}/nss3,g" \
                          -e "s,@MOD_MAJOR_VERSION@,$NSS_VMAJOR,g" \
                          -e "s,@MOD_MINOR_VERSION@,$NSS_VMINOR,g" \
                          -e "s,@MOD_PATCH_VERSION@,$NSS_VPATCH,g" \
                          > ./mozilla/dist/pkgconfig/nss-softokn-config

chmod 755 ./mozilla/dist/pkgconfig/nss-config

#%{__cat} %{SOURCE9} > ./mozilla/dist/pkgconfig/setup-nsssysinit.sh
#chmod 755 ./mozilla/dist/pkgconfig/setup-nsssysinit.sh


# There is no make install target so we'll do it ourselves.

%{__mkdir_p} $RPM_BUILD_ROOT/%{_includedir}/nss3
%{__mkdir_p} $RPM_BUILD_ROOT/%{_bindir}
%{__mkdir_p} $RPM_BUILD_ROOT/%{_libdir}
%{__mkdir_p} $RPM_BUILD_ROOT/%{unsupported_tools_directory}
%{__mkdir_p} $RPM_BUILD_ROOT/%{_libdir}/pkgconfig

# Copy the binary libraries we want nsspemk.dll libnsssysinitk.dll 
for file in nss3k.dll nssckbik.dll smime3k.dll ssl3k.dll nssuti3k.dll softok3k.dll nssdbm3k.dll freebl3k.dll
do
  %{__install} -p -m 755 mozilla/dist/*.OBJ/lib/$file $RPM_BUILD_ROOT/%{_libdir}
done
# Copy the import libraries we want
for file in nss3.a smime3.a ssl3.a nssdbm3.a
do
  %{__install} -p -m 755 mozilla/dist/*.OBJ/lib/$file $RPM_BUILD_ROOT/%{_libdir}
done
%{__install} -p -m 755 mozilla/dist/*.OBJ/lib/nssuti3.a $RPM_BUILD_ROOT/%{_libdir}/nssutil3.a
%{__install} -p -m 755 mozilla/dist/*.OBJ/lib/softok3.a $RPM_BUILD_ROOT/%{_libdir}/softokn3.a

# Install the empty NSS db files
# Legacy db
#%{__mkdir_p} $RPM_BUILD_ROOT/%{_sysconfdir}/pki/nssdb
#%{__install} -p -m 644 %{SOURCE3} $RPM_BUILD_ROOT/%{_sysconfdir}/pki/nssdb/cert8.db
#%{__install} -p -m 644 %{SOURCE4} $RPM_BUILD_ROOT/%{_sysconfdir}/pki/nssdb/key3.db
#%{__install} -p -m 644 %{SOURCE5} $RPM_BUILD_ROOT/%{_sysconfdir}/pki/nssdb/secmod.db
# Shared db
#%{__install} -p -m 644 %{SOURCE6} $RPM_BUILD_ROOT/%{_sysconfdir}/pki/nssdb/cert9.db
#%{__install} -p -m 644 %{SOURCE7} $RPM_BUILD_ROOT/%{_sysconfdir}/pki/nssdb/key4.db
#%{__install} -p -m 644 %{SOURCE8} $RPM_BUILD_ROOT/%{_sysconfdir}/pki/nssdb/pkcs11.txt
     
# Copy the development libraries we want
for file in crmf.a nssb.a nssckfw.a freebl.a
do
  %{__install} -p -m 644 mozilla/dist/*.OBJ/lib/$file $RPM_BUILD_ROOT/%{_libdir}
done

# Copy the binaries we want
for file in certutil cmsutil crlutil modutil pk12util signtool signver ssltap
do
  %{__install} -p -m 755 mozilla/dist/*.OBJ/bin/$file.exe $RPM_BUILD_ROOT/%{_bindir}
done

# Copy the binaries we ship as unsupported
for file in atob btoa derdump ocspclnt pp selfserv strsclnt symkeyutil tstclnt vfyserv vfychain shlibsign
do
  %{__install} -p -m 755 mozilla/dist/*.OBJ/bin/$file.exe $RPM_BUILD_ROOT/%{unsupported_tools_directory}
done

# Copy the include files we want
for file in mozilla/dist/public/nss/*.h
do
  %{__install} -p -m 644 $file $RPM_BUILD_ROOT/%{_includedir}/nss3
done

# Copy a freebl include file we also want
for file in mozilla/dist/private/nss/blapi.h
do
  %{__install} -p -m 644 $file $RPM_BUILD_ROOT/%{_includedir}/nss3
done

# Copy the package configuration files
%{__install} -p -m 644 ./mozilla/dist/pkgconfig/nss.pc $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/nss.pc
%{__install} -p -m 755 ./mozilla/dist/pkgconfig/nss-config $RPM_BUILD_ROOT/%{_bindir}/nss-config
# Copy the pkcs #11 configuration script
#%{__install} -p -m 755 ./mozilla/dist/pkgconfig/setup-nsssysinit.sh $RPM_BUILD_ROOT/%{_bindir}/setup-nsssysinit.sh

# util-Copy the package configuration files
%{__install} -p -m 644 ./mozilla/dist/pkgconfig/nss-util.pc $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/nss-util.pc
%{__install} -p -m 755 ./mozilla/dist/pkgconfig/nss-util-config $RPM_BUILD_ROOT/%{_bindir}/nss-util-config

# softokn-Copy the package configuration files
%{__install} -p -m 644 ./mozilla/dist/pkgconfig/nss-softokn.pc $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/nss-softokn.pc
%{__install} -p -m 755 ./mozilla/dist/pkgconfig/nss-softokn-config $RPM_BUILD_ROOT/%{_bindir}/nss-softokn-config

# Copy the digital signatures
for file in freebl3k nssdbm3k softok3k
do
  %{__install} -p -m 644 mozilla/dist/*.OBJ/lib/$file.chk $RPM_BUILD_ROOT/%{_libdir}
done


%clean
%{__rm} -rf $RPM_BUILD_ROOT

#%triggerpostun -n nss-sysinit -- nss-sysinit < 3.12.8-3
# Reverse unwanted disabling of sysinit by faulty preun sysinit scriplet
# from previous versions of nss.spec
#/@unixroot/usr/bin/setup-nsssysinit.sh on

#%post -p /sbin/ldconfig

#%postun -p /sbin/ldconfig


%files
%defattr(-,root,root)
%{_libdir}/nss3k.dll
%{_libdir}/ssl3k.dll
%{_libdir}/smime3k.dll
%{_libdir}/nssckbik.dll
#%{_libdir}/nsspemk.dll
#%dir %{_sysconfdir}/pki/nssdb
#%config(noreplace) %{_sysconfdir}/pki/nssdb/cert8.db
#%config(noreplace) %{_sysconfdir}/pki/nssdb/key3.db
#%config(noreplace) %{_sysconfdir}/pki/nssdb/secmod.db

#%files sysinit
#%defattr(-,root,root)
#%{_libdir}/libnsssysinitk.dll
#%config(noreplace) %{_sysconfdir}/pki/nssdb/cert9.db
#%config(noreplace) %{_sysconfdir}/pki/nssdb/key4.db
#%config(noreplace) %{_sysconfdir}/pki/nssdb/pkcs11.txt
#%{_bindir}/setup-nsssysinit.sh

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
%{unsupported_tools_directory}/ocspclnt.exe
%{unsupported_tools_directory}/pp.exe
%{unsupported_tools_directory}/selfserv.exe
%{unsupported_tools_directory}/strsclnt.exe
%{unsupported_tools_directory}/symkeyutil.exe
%{unsupported_tools_directory}/tstclnt.exe
%{unsupported_tools_directory}/vfyserv.exe
%{unsupported_tools_directory}/vfychain.exe

%files devel
%defattr(-,root,root)
%{_libdir}/nss3.a
%{_libdir}/smime3.a
%{_libdir}/ssl3.a
%{_libdir}/crmf.a
%{_libdir}/pkgconfig/nss.pc
%{_bindir}/nss-config

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
%{_libdir}/nssb.a
%{_libdir}/nssckfw.a

%files util
%defattr(-,root,root)
%{_libdir}/nssuti3k.dll

%files util-devel
%defattr(-,root,root)
# package configuration files
%{_libdir}/pkgconfig/nss-util.pc
%{_bindir}/nss-util-config
%{_libdir}/nssutil3.a
# co-owned with nss
%dir %{_includedir}/nss3
# these are marked as public export in
# mozilla/security/nss/lib/util/manifest.mk
%{_includedir}/nss3/base64.h
%{_includedir}/nss3/ciferfam.h
%{_includedir}/nss3/nssb64.h
%{_includedir}/nss3/nssb64t.h
%{_includedir}/nss3/nsslocks.h
%{_includedir}/nss3/nssilock.h
%{_includedir}/nss3/nssilckt.h
%{_includedir}/nss3/nssrwlk.h
%{_includedir}/nss3/nssrwlkt.h
%{_includedir}/nss3/nssutil.h
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
%{_includedir}/nss3/utilrename.h

%files softokn
%defattr(-,root,root)
%{_libdir}/nssdbm3k.dll
%{_libdir}/nssdbm3k.chk
%{_libdir}/softok3k.dll
%{_libdir}/softok3k.chk
# shared with nss-tools
%dir %{_libdir}/nss
#%dir %{saved_files_dir}
%dir %{unsupported_tools_directory}
%{unsupported_tools_directory}/shlibsign.exe

%files softokn-freebl
%defattr(-,root,root)
%{_libdir}/freebl3k.dll
%{_libdir}/freebl3k.chk
# and these symbolic links
#%{_libdir}/libfreebl3.so
#%{_libdir}/libfreebl3.chk

%files softokn-freebl-devel
%defattr(-,root,root)
%{_libdir}/freebl.a
%{_includedir}/nss3/blapi.h

%files softokn-devel
%defattr(-,root,root)
%{_libdir}/pkgconfig/nss-softokn.pc
%{_libdir}/nssdbm3.a
%{_libdir}/softokn3.a
%{_bindir}/nss-softokn-config
# co-owned with nss
%dir %{_includedir}/nss3
#
# The following headers are those exported public in
# mozilla/security/nss/lib/freebl/manifest.mn and
# mozilla/security/nss/lib/softoken/manifest.mn
#
# The following list is short because many headers, such as
# the pkcs #11 ones, have been provided by nss-util-devel
# which installed them before us.
#
%{_includedir}/nss3/blapit.h
%{_includedir}/nss3/ecl-exp.h
%{_includedir}/nss3/hasht.h
%{_includedir}/nss3/sechash.h
#%{_includedir}/nss3/nsslowhash.h
%{_includedir}/nss3/secmodt.h
%{_includedir}/nss3/shsign.h

%changelog
