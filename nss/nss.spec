%global nspr_version 4.23.0
%global nss_version 3.47.0
%global unsupported_tools_directory %{_libdir}/nss/unsupported-tools
%global saved_files_dir %{_libdir}/nss/saved

%global with_dracut 0
%global with_crypto_pol 0
%global with_sysinit 0
%global with_blankdb 0
# the lowhash functionality depends on freeblprivate and we don't build that
%global with_lowhash 0

%if %{with_dracut}
%global dracutlibdir %{_prefix}/lib/dracut
%global dracut_modules_dir %{dracutlibdir}/modules.d/05nss-softokn/
%global dracut_conf_dir %{dracutlibdir}/dracut.conf.d
%endif

%bcond_with tests

# Produce .chk files for the final stripped binaries
#
# NOTE: The LD_LIBRARY_PATH line guarantees shlibsign links
# against the freebl that we just built. This is necessary
# because the signing algorithm changed on 3.14 to DSA2 with SHA256
# whereas we previously signed with DSA and SHA1. We must Keep this line
# until all mock platforms have been updated.
# After %%{__os_install_post} we would add
# export LD_LIBRARY_PATH=$RPM_BUILD_ROOT/%%{_libdir}
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

# The upstream omits the trailing ".0", while we need it for
# consistency with the pkg-config version:
# https://bugzilla.redhat.com/show_bug.cgi?id=1578106
%{lua:
rpm.define(string.format("nss_archive_version %s",
           string.gsub(rpm.expand("%nss_version"), "(.*)%.0$", "%1")))
}

%{lua:
rpm.define(string.format("nss_release_tag NSS_%s_RTM",
           string.gsub(rpm.expand("%nss_archive_version"), "%.", "_")))
}

Summary:          Network Security Services
Name:             nss
Version:          %{nss_version}
Release:          1%{?dist}
License:          MPLv2.0
URL:              http://www.mozilla.org/projects/security/pki/nss/
Vendor:           bww bitwise works GmbH

Requires:         nspr >= %{nspr_version}
Requires:         %{name}-util >= %{nss_version}
# TODO: revert to same version as nss once we are done with the merge
Requires:         %{name}-softokn => %{version}-%{release}
%if %{with_sysinit}
Requires:         %{name}-system-init
%endif
Requires:         p11-kit-trust
%if %{with_crypto_pol}
Requires:         crypto-policies
%endif
BuildRequires:    nspr-devel >= %{nspr_version}
# for shlibsign
BuildRequires:    nss-softokn
BuildRequires:    sqlite-devel
BuildRequires:    zlib-devel
BuildRequires:    pkgconfig
BuildRequires:    gawk
#BuildRequires:    psmisc
BuildRequires:    perl
BuildRequires:    gcc
#BuildRequires:    quilt

%scm_source github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2

Source1:          nss-util.pc.in
Source2:          nss-util-config.in
Source3:          nss-softokn.pc.in
Source4:          nss-softokn-config.in
%if %{with_dracut}
Source6:          nss-softokn-dracut-module-setup.sh
Source7:          nss-softokn-dracut.conf
%endif
Source8:          nss.pc.in
Source9:          nss-config.in
%if %{with_blankdb}
Source10:         blank-cert8.db
Source11:         blank-key3.db
Source12:         blank-secmod.db
Source13:         blank-cert9.db
Source14:         blank-key4.db
Source15:         system-pkcs11.txt
%endif
%if %{with_sysinit}
Source16:         setup-nsssysinit.sh
%endif
Source20:         nss-config.xml
%if %{with_sysinit}
Source21:         setup-nsssysinit.xml
%endif
%if %{with_blankdb}
Source22:         pkcs11.txt.xml
Source23:         cert8.db.xml
Source24:         cert9.db.xml
Source25:         key3.db.xml
Source26:         key4.db.xml
Source27:         secmod.db.xml
%endif
%if %{with_crypto_pol}
Source28:         nss-p11-kit.config
%endif

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


%description
Network Security Services (NSS) is a set of libraries designed to
support cross-platform development of security-enabled client and
server applications. Applications built with NSS can support SSL v2
and v3, TLS, PKCS #5, PKCS #7, PKCS #11, PKCS #12, S/MIME, X.509
v3 certificates, and other security standards.

%package tools
Summary:          Tools for the Network Security Services
Requires:         %{name} = %{version}-%{release}

%description tools
Network Security Services (NSS) is a set of libraries designed to
support cross-platform development of security-enabled client and
server applications. Applications built with NSS can support SSL v2
and v3, TLS, PKCS #5, PKCS #7, PKCS #11, PKCS #12, S/MIME, X.509
v3 certificates, and other security standards.

Install the nss-tools package if you need command-line tools to
manipulate the NSS certificate and key database.

%if %{with_sysinit}
%package sysinit
Summary:          System NSS Initialization
# providing nss-system-init without version so that it can
# be replaced by a better one, e.g. supplied by the os vendor
Provides:         %{name}-system-init
Requires:         %{name} = %{version}-%{release}
Requires(post):   coreutils, sed

%description sysinit
Default Operating System module that manages applications loading
NSS globally on the system. This module loads the system defined
PKCS #11 modules for NSS and chains with other NSS modules to load
any system or user configured modules.
%endif

%package devel
Summary:          Development libraries for Network Security Services
Provides:         %{name}-static = %{version}-%{release}
Requires:         %{name} = %{version}-%{release}
Requires:         %{name}-util-devel
Requires:         %{name}-softokn-devel
Requires:         nspr-devel >= %{nspr_version}
Requires:         pkgconfig
BuildRequires:    xmlto

%description devel
Header and Library files for doing development with Network Security Services.


%package pkcs11-devel
Summary:          Development libraries for PKCS #11 (Cryptoki) using NSS
Provides:         %{name}-pkcs11-devel-static = %{version}-%{release}
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


%package util
Summary:          Network Security Services Utilities Library
Requires:         nspr >= %{nspr_version}

%description util
Utilities for Network Security Services and the Softoken module

%package util-devel
Summary:          Development libraries for Network Security Services Utilities
Requires:         %{name}-util = %{version}-%{release}
Requires:         nspr-devel >= %{nspr_version}
Requires:         pkgconfig

%description util-devel
Header and library files for doing development with Network Security Services.

%package util-legacy
Summary:        Legacy libraries for Netscape Security Services Utilities.
Requires:       %{name}-util = %{version}-%{release}

%description util-legacy
NSS Utilities forwarder libraries with old DLL names ending with 'k'.


%package softokn
Summary:          Network Security Services Softoken Module
Requires:         nspr >= %{nspr_version}
Requires:         %{name}-util >= %{version}-%{release}
Requires:         %{name}-softokn-freebl >= %{version}-%{release}

%description softokn
Network Security Services Softoken Cryptographic Module

%package softokn-freebl
Summary:          Freebl library for the Network Security Services
# For PR_GetEnvSecure() from nspr >= 4.12
Requires:         nspr >= 4.12
# For NSS_SecureMemcmpZero() from nss-util >= 3.33
Requires:         %{name}-util >= 3.33
Conflicts:        %{name} < 3.12.2.99.3-5
Conflicts:        filesystem < 3

%description softokn-freebl
NSS Softoken Cryptographic Module Freebl Library

Install the nss-softokn-freebl package if you need the freebl
library.

%package softokn-freebl-devel
Summary:          Header and Library files for doing development with the Freebl library for NSS
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
Requires:         %{name}-softokn = %{version}-%{release}
Requires:         %{name}-softokn-freebl-devel = %{version}-%{release}
Requires:         nspr-devel >= %{nspr_version}
Requires:         %{name}-util-devel >= %{version}-%{release}
Requires:         pkgconfig
BuildRequires:    nspr-devel >= %{nspr_version}

%description softokn-devel
Header and library files for doing development with Network Security Services.

%package softokn-legacy
Summary:        Legacy libraries for Netscape Security Services Softoken Cryptographic Modile.
Requires:       %{name}-softokn = %{version}-%{release}

%description softokn-legacy
NSS Softoken Cryptographic Modile forwarder libraries with old DLL names ending with 'k'.

%package softokn-freebl-legacy
Summary:        Legacy libraries for Netscape Security Services Freebl.
Requires:       %{name}-softokn-freebl = %{version}-%{release}

%description softokn-freebl-legacy
NSS Freebl forwarder libraries with old DLL names ending with 'k'.

%debug_package

# Makes no sense to provide .dbg files for forwarder DLLs
%define _strip_opts --debuginfo -x "*k.dll"

%prep
%scm_setup


# Prepare forwarder DLLs.
for m in %{SOURCE401} %{SOURCE402} %{SOURCE403} %{SOURCE404} %{SOURCE411} %{SOURCE421} %{SOURCE422} %{SOURCE431}; do
  cp ${m} .
done

%build

# enable if you want to build with no NSPR dependencies
#export FREEBL_NO_DEPEND=1

%if %{with_lowhash}
# Must export FREEBL_LOWHASH=1 for nsslowhash.h so that it gets
# copied to dist and the rpm install phase can find it
# This due of the upstream changes to fix
# https://bugzilla.mozilla.org/show_bug.cgi?id=717906
export FREEBL_LOWHASH=1
%endif

# uncomment if the iquote patch is activated
#export IN_TREE_FREEBL_HEADERS_FIRST=1

#export NSS_FORCE_FIPS=1

# Enable compiler optimizations and disable debugging code
export BUILD_OPT=1

# Uncomment to disable optimizations
#RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed -e 's/-O2/-O0/g'`
#export RPM_OPT_FLAGS

# Generate symbolic info for debuggers
export XCFLAGS="$RPM_OPT_FLAGS"

export LDFLAGS="$RPM_LD_FLAGS"

export DSO_LDOPTS="$RPM_LD_FLAGS"

export PKG_CONFIG_ALLOW_SYSTEM_LIBS=1
export PKG_CONFIG_ALLOW_SYSTEM_CFLAGS=1

export NSPR_INCLUDE_DIR=`/@unixroot/usr/bin/pkg-config --cflags-only-I nspr | sed 's/-I//'`
export NSPR_LIB_DIR=%{_libdir}

export NSS_USE_SYSTEM_SQLITE=1

export NSS_ALLOW_SSLKEYLOGFILE=1

%ifnarch noarch
%if 0%{__isa_bits} == 64
export USE_64=1
%endif
%endif

# Begin -- OS/2 specific settings

# Enable high memory support
export MOZ_OS2_HIGH_MEMORY=1

# Force debug symbols to make debug_package happy
export MOZ_DEBUG_SYMBOLS=1
# MOZ_DEBUG is necessary to shut up premature debug symbol extraction
export MOZ_DEBUG=1

# Make sure build output lands in ./dist
export BUILD_TREE=`echo "%{_builddir}/%{?buildsubdir}" | tr '\\\' /`

# Disable external google tests as we lack std::wcslen in the gcc RPM
export NSS_DISABLE_GTESTS=1
export VENDOR="%{vendor}"
# End -- OS/2 specific settings follow below 


%{__make} -C ./coreconf
%{__make} -C ./lib/dbm

# Set the policy file location
# if set NSS will always check for the policy file and load if it exists
#export POLICY_FILE="nss.config"
# location of the policy file
#export POLICY_PATH="/etc/crypto-policies/back-ends"

%{__make} -C .

# build the man pages clean
%{__make} clean_docs build_docs

# and copy them to the dist directory for %%install to find them
%{__mkdir_p} ./dist/docs/nroff
%{__cp} ./doc/nroff/* ./dist/docs/nroff

# Set up our package file
%{__mkdir_p} ./dist/pkgconfig

%{__cat} %{SOURCE1} | sed -e "s,%%libdir%%,%{_libdir},g" \
                          -e "s,%%prefix%%,%{_prefix},g" \
                          -e "s,%%exec_prefix%%,%{_prefix},g" \
                          -e "s,%%includedir%%,%{_includedir}/nss3,g" \
                          -e "s,%%NSPR_VERSION%%,%{nspr_version},g" \
                          -e "s,%%NSSUTIL_VERSION%%,%{version},g" > \
                          ./dist/pkgconfig/nss-util.pc

NSSUTIL_VMAJOR=`cat lib/util/nssutil.h | grep "#define.*NSSUTIL_VMAJOR" | awk '{print $3}'`
NSSUTIL_VMINOR=`cat lib/util/nssutil.h | grep "#define.*NSSUTIL_VMINOR" | awk '{print $3}'`
NSSUTIL_VPATCH=`cat lib/util/nssutil.h | grep "#define.*NSSUTIL_VPATCH" | awk '{print $3}'`

%{__cat} %{SOURCE2} | sed -e "s,@libdir@,%{_libdir},g" \
                          -e "s,@prefix@,%{_prefix},g" \
                          -e "s,@exec_prefix@,%{_prefix},g" \
                          -e "s,@includedir@,%{_includedir}/nss3,g" \
                          -e "s,@MOD_MAJOR_VERSION@,$NSSUTIL_VMAJOR,g" \
                          -e "s,@MOD_MINOR_VERSION@,$NSSUTIL_VMINOR,g" \
                          -e "s,@MOD_PATCH_VERSION@,$NSSUTIL_VPATCH,g" \
                          > ./dist/pkgconfig/nss-util-config

chmod 755 ./dist/pkgconfig/nss-util-config

%{__cat} %{SOURCE3} | sed -e "s,%%libdir%%,%{_libdir},g" \
                          -e "s,%%prefix%%,%{_prefix},g" \
                          -e "s,%%exec_prefix%%,%{_prefix},g" \
                          -e "s,%%includedir%%,%{_includedir}/nss3,g" \
                          -e "s,%%NSPR_VERSION%%,%{nspr_version},g" \
                          -e "s,%%NSSUTIL_VERSION%%,%{nss_version},g" \
                          -e "s,%%SOFTOKEN_VERSION%%,%{version},g" > \
                          ./dist/pkgconfig/nss-softokn.pc

SOFTOKEN_VMAJOR=`cat lib/softoken/softkver.h | grep "#define.*SOFTOKEN_VMAJOR" | awk '{print $3}'`
SOFTOKEN_VMINOR=`cat lib/softoken/softkver.h | grep "#define.*SOFTOKEN_VMINOR" | awk '{print $3}'`
SOFTOKEN_VPATCH=`cat lib/softoken/softkver.h | grep "#define.*SOFTOKEN_VPATCH" | awk '{print $3}'`

%{__cat} %{SOURCE4} | sed -e "s,@libdir@,%{_libdir},g" \
                          -e "s,@prefix@,%{_prefix},g" \
                          -e "s,@exec_prefix@,%{_prefix},g" \
                          -e "s,@includedir@,%{_includedir}/nss3,g" \
                          -e "s,@MOD_MAJOR_VERSION@,$SOFTOKEN_VMAJOR,g" \
                          -e "s,@MOD_MINOR_VERSION@,$SOFTOKEN_VMINOR,g" \
                          -e "s,@MOD_PATCH_VERSION@,$SOFTOKEN_VPATCH,g" \
                          > ./dist/pkgconfig/nss-softokn-config

chmod 755 ./dist/pkgconfig/nss-softokn-config

%{__cat} %{SOURCE8} | sed -e "s,%%libdir%%,%{_libdir},g" \
                          -e "s,%%prefix%%,%{_prefix},g" \
                          -e "s,%%exec_prefix%%,%{_prefix},g" \
                          -e "s,%%includedir%%,%{_includedir}/nss3,g" \
                          -e "s,%%NSS_VERSION%%,%{version},g" \
                          -e "s,%%NSPR_VERSION%%,%{nspr_version},g" \
                          -e "s,%%NSSUTIL_VERSION%%,%{nss_version},g" \
                          -e "s,%%SOFTOKEN_VERSION%%,%{nss_version},g" > \
                          ./dist/pkgconfig/nss.pc

NSS_VMAJOR=`cat lib/nss/nss.h | grep "#define.*NSS_VMAJOR" | awk '{print $3}'`
NSS_VMINOR=`cat lib/nss/nss.h | grep "#define.*NSS_VMINOR" | awk '{print $3}'`
NSS_VPATCH=`cat lib/nss/nss.h | grep "#define.*NSS_VPATCH" | awk '{print $3}'`

%{__cat} %{SOURCE9} | sed -e "s,@libdir@,%{_libdir},g" \
                          -e "s,@prefix@,%{_prefix},g" \
                          -e "s,@exec_prefix@,%{_prefix},g" \
                          -e "s,@includedir@,%{_includedir}/nss3,g" \
                          -e "s,@MOD_MAJOR_VERSION@,$NSS_VMAJOR,g" \
                          -e "s,@MOD_MINOR_VERSION@,$NSS_VMINOR,g" \
                          -e "s,@MOD_PATCH_VERSION@,$NSS_VPATCH,g" \
                          > ./dist/pkgconfig/nss-config

chmod 755 ./dist/pkgconfig/nss-config

%if %{with_sysinit}
%{__cat} %{SOURCE16} > ./dist/pkgconfig/setup-nsssysinit.sh
chmod 755 ./dist/pkgconfig/setup-nsssysinit.sh
%endif

%{__cp} ./lib/ckfw/nssck.api ./dist/private/nss/

date +"%e %B %Y" | tr -d '\n' > date.xml
echo -n %{version} > version.xml

# configuration files and setup script
for m in %{SOURCE20} %{SOURCE21} %{SOURCE22}; do
  test -f ${m} && \
  cp ${m} .
done
for m in nss-config.xml setup-nsssysinit.xml pkcs11.txt.xml; do
  test -f ${m} && \
  xmlto man ${m}
done

# nss databases considered to be configuration files
for m in %{SOURCE23} %{SOURCE24} %{SOURCE25} %{SOURCE26} %{SOURCE27}; do
  test -f ${m} && \
  cp ${m} .
done
for m in cert8.db.xml cert9.db.xml key3.db.xml key4.db.xml secmod.db.xml; do
  test -f ${m} && \
  xmlto man ${m}
done


%check
%if %{with tests}
# Begin -- copied from the build section

export FREEBL_NO_DEPEND=1

export BUILD_OPT=1

%ifnarch noarch
%if 0%{__isa_bits} == 64
export USE_64=1
%endif
%endif

# End -- copied from the build section

# This is necessary because the test suite tests algorithms that are
# disabled by the system policy.
export NSS_IGNORE_SYSTEM_POLICY=1

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

SPACEISBAD=`find ./nss/tests | grep -c ' '` ||:
if [ $SPACEISBAD -ne 0 ]; then
  echo "error: filenames containing space are not supported (xargs)"
  exit 1
fi
MYRAND=`perl -e 'print 9000 + int rand 1000'`; echo $MYRAND ||:
RANDSERV=selfserv_${MYRAND}; echo $RANDSERV ||:
DISTBINDIR=`ls -d ./dist/*.OBJ/bin`; echo $DISTBINDIR ||:
pushd "$DISTBINDIR"
ln -s selfserv $RANDSERV
popd
# man perlrun, man perlrequick
# replace word-occurrences of selfserv with selfserv_$MYRAND
find ./nss/tests -type f |\
  grep -v "\.db$" |grep -v "\.crl$" | grep -v "\.crt$" |\
  grep -vw CVS  |xargs grep -lw selfserv |\
  xargs -l perl -pi -e "s/\bselfserv\b/$RANDSERV/g" ||:

killall $RANDSERV || :

rm -rf ./tests_results
pushd nss/tests
# all.sh is the test suite script

#  don't need to run all the tests when testing packaging
#  nss_cycles: standard pkix upgradedb sharedb
#  the full list from all.sh is:
#  "cipher lowhash libpkix cert dbtests tools fips sdr crmf smime ssl ocsp merge pkits chains ec gtests ssl_gtests"
%define nss_tests "libpkix cert dbtests tools fips sdr crmf smime ssl ocsp merge pkits chains ec gtests ssl_gtests"
#  nss_ssl_tests: crl bypass_normal normal_bypass normal_fips fips_normal iopr policy
#  nss_ssl_run: cov auth stapling stress
#
# Uncomment these lines if you need to temporarily
# disable some test suites for faster test builds
# % define nss_ssl_tests "normal_fips"
# % define nss_ssl_run "cov"

HOST=localhost DOMSUF=localdomain PORT=$MYRAND NSS_CYCLES=%{?nss_cycles} NSS_TESTS=%{?nss_tests} NSS_SSL_TESTS=%{?nss_ssl_tests} NSS_SSL_RUN=%{?nss_ssl_run} ./all.sh
popd

killall $RANDSERV || :
%endif

%install

# There is no make install target so we'll do it ourselves.

%{__mkdir_p} $RPM_BUILD_ROOT/%{_includedir}/nss3
%{__mkdir_p} $RPM_BUILD_ROOT/%{_includedir}/nss3/templates
%{__mkdir_p} $RPM_BUILD_ROOT/%{_bindir}
%{__mkdir_p} $RPM_BUILD_ROOT/%{_libdir}
%{__mkdir_p} $RPM_BUILD_ROOT/%{unsupported_tools_directory}
%{__mkdir_p} $RPM_BUILD_ROOT/%{_libdir}/pkgconfig
%{__mkdir_p} $RPM_BUILD_ROOT/%{saved_files_dir}
%if %{with_dracut}
%{__mkdir_p} $RPM_BUILD_ROOT/%{dracut_modules_dir}
%{__mkdir_p} $RPM_BUILD_ROOT/%{dracut_conf_dir}
%endif
%if %{with_crypto_pol}
%{__mkdir_p} $RPM_BUILD_ROOT/%{_sysconfdir}/crypto-policies/local.d
%endif
%if %{defined rhel}
# not needed for rhel and its derivatives only fedora
%else
# because of the pp.1 conflict with perl-PAR-Packer
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/doc/nss-tools
%endif

%if %{with_dracut}
install -m 755 %{SOURCE6} $RPM_BUILD_ROOT/%{dracut_modules_dir}/module-setup.sh
install -m 644 %{SOURCE7} $RPM_BUILD_ROOT/%{dracut_conf_dir}/50-nss-softokn.conf
%endif

mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man5

# Copy the binary libraries we want
# not used ones libfreeblpriv3.so libnsssysinit.so
for file in nssckbi nssutil3 softokn3 nssdbm3 freebl3 nss3 smime3 ssl3
do
  %{__install} -p -m 755 dist/*.OBJ/lib/$file.dll $RPM_BUILD_ROOT/%{_libdir}
  test -f dist/*.OBJ/lib/$file.a && \
    %{__install} -p -m 644 dist/*.OBJ/lib/$file.a $RPM_BUILD_ROOT/%{_libdir}
done



# Install the empty NSS db files
# Legacy db
%if %{with_blankdb}
%{__mkdir_p} $RPM_BUILD_ROOT/%{_sysconfdir}/pki/nssdb
%{__install} -p -m 644 %{SOURCE10} $RPM_BUILD_ROOT/%{_sysconfdir}/pki/nssdb/cert8.db
%{__install} -p -m 644 %{SOURCE11} $RPM_BUILD_ROOT/%{_sysconfdir}/pki/nssdb/key3.db
%{__install} -p -m 644 %{SOURCE12} $RPM_BUILD_ROOT/%{_sysconfdir}/pki/nssdb/secmod.db
# Shared db
%{__install} -p -m 644 %{SOURCE13} $RPM_BUILD_ROOT/%{_sysconfdir}/pki/nssdb/cert9.db
%{__install} -p -m 644 %{SOURCE14} $RPM_BUILD_ROOT/%{_sysconfdir}/pki/nssdb/key4.db
%{__install} -p -m 644 %{SOURCE15} $RPM_BUILD_ROOT/%{_sysconfdir}/pki/nssdb/pkcs11.txt
%endif

# Copy the development libraries we want
for file in crmf.a nssb.a nssckfw.a
do
  %{__install} -p -m 644 dist/*.OBJ/lib/$file $RPM_BUILD_ROOT/%{_libdir}
done

# Copy the binaries we want
for file in certutil cmsutil crlutil modutil nss-policy-check pk12util signver ssltap
do
  %{__install} -p -m 755 dist/*.OBJ/bin/$file.exe $RPM_BUILD_ROOT/%{_bindir}
done

# Copy the binaries we ship as unsupported
for file in bltest ecperf fbectest fipstest shlibsign atob btoa derdump listsuites ocspclnt pp selfserv signtool strsclnt symkeyutil tstclnt vfyserv vfychain
do
  %{__install} -p -m 755 dist/*.OBJ/bin/$file.exe $RPM_BUILD_ROOT/%{unsupported_tools_directory}
done

# Copy the include files we want
for file in dist/public/nss/*.h
do
  %{__install} -p -m 644 $file $RPM_BUILD_ROOT/%{_includedir}/nss3
done

# Copy some freebl include files we also want
for file in blapi.h alghmac.h cmac.h
do
  %{__install} -p -m 644 dist/private/nss/$file $RPM_BUILD_ROOT/%{_includedir}/nss3
done

# Copy the static freebl library
for file in freebl.a
do
install -p -m 644 dist/*.OBJ/lib/$file $RPM_BUILD_ROOT/%{_libdir}
done

# Copy the template files we want
for file in dist/private/nss/templates.c dist/private/nss/nssck.api
do
  %{__install} -p -m 644 $file $RPM_BUILD_ROOT/%{_includedir}/nss3/templates
done

# Copy the package configuration files
%{__install} -p -m 644 ./dist/pkgconfig/nss-util.pc $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/nss-util.pc
%{__install} -p -m 755 ./dist/pkgconfig/nss-util-config $RPM_BUILD_ROOT/%{_bindir}/nss-util-config
%{__install} -p -m 644 ./dist/pkgconfig/nss-softokn.pc $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/nss-softokn.pc
%{__install} -p -m 755 ./dist/pkgconfig/nss-softokn-config $RPM_BUILD_ROOT/%{_bindir}/nss-softokn-config
%{__install} -p -m 644 ./dist/pkgconfig/nss.pc $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/nss.pc
%{__install} -p -m 755 ./dist/pkgconfig/nss-config $RPM_BUILD_ROOT/%{_bindir}/nss-config
%if %{with_sysinit}
# Copy the pkcs #11 configuration script
%{__install} -p -m 755 ./dist/pkgconfig/setup-nsssysinit.sh $RPM_BUILD_ROOT/%{_bindir}/setup-nsssysinit.sh
# install a symbolic link to it, without the ".sh" suffix,
# that matches the man page documentation
ln -r -s -f $RPM_BUILD_ROOT/%{_bindir}/setup-nsssysinit.sh $RPM_BUILD_ROOT/%{_bindir}/setup-nsssysinit
%endif

# Copy the man pages for scripts
for f in nss-config setup-nsssysinit; do
  test -f ${f}.1 && \
   install -c -m 644 ${f}.1 $RPM_BUILD_ROOT%{_mandir}/man1/${f}.1
done
# Copy the man pages for the nss tools
for f in certutil cmsutil crlutil derdump modutil pk12util signtool signver ssltap vfychain vfyserv; do
  install -c -m 644 ./dist/docs/nroff/${f}.1 $RPM_BUILD_ROOT%{_mandir}/man1/${f}.1
done
%if %{defined rhel}
install -c -m 644 ./dist/docs/nroff/pp.1 $RPM_BUILD_ROOT%{_mandir}/man1/pp.1
%else
install -c -m 644 ./dist/docs/nroff/pp.1 $RPM_BUILD_ROOT%{_datadir}/doc/nss-tools/pp.1
%endif

# Copy the man pages for the configuration files
%if %{with_blankdb}
for f in pkcs11.txt; do
   install -c -m 644 ${f}.5 $RPM_BUILD_ROOT%{_mandir}/man5/${f}.5
done
%endif
# Copy the man pages for the nss databases
%if %{with_blankdb}
for f in cert8.db cert9.db key3.db key4.db secmod.db; do
   install -c -m 644 ${f}.5 $RPM_BUILD_ROOT%{_mandir}/man5/${f}.5
done
%endif

# Copy the crypto-policies configuration file
%if %{with_crypto_pol}
install -p -m 644 %{SOURCE28} $RPM_BUILD_ROOT/%{_sysconfdir}/crypto-policies/local.d
%endif

# Generate & install forwarder DLLs.
for m in nss3 nssckbi smime3 ssl3 nssdbm3 freebl3 ; do
  gcc -Zomf -Zdll -nostdlib ${m}k.def -l${RPM_BUILD_ROOT}%{_libdir}/${m}.dll -lend -o ${RPM_BUILD_ROOT}%{_libdir}/${m}k.dll
done
# These are special due to one letter less
gcc -Zomf -Zdll -nostdlib nssuti3k.def -l${RPM_BUILD_ROOT}%{_libdir}/nssutil3.dll -lend -o ${RPM_BUILD_ROOT}%{_libdir}/nssuti3k.dll
gcc -Zomf -Zdll -nostdlib softok3k.def -l${RPM_BUILD_ROOT}%{_libdir}/softokn3.dll -lend -o ${RPM_BUILD_ROOT}%{_libdir}/softok3k.dll


%if %{with_sysinit}
%triggerpostun -n nss-sysinit -- nss-sysinit < 3.12.8-3
# Reverse unwanted disabling of sysinit by faulty preun sysinit scriplet
# from previous versions of nss.spec
/usr/bin/setup-nsssysinit.sh on
%endif

%post
%if %{with_sysinit}
update-crypto-policies &> /dev/null || :
%endif

%postun
%if %{with_sysinit}
update-crypto-policies &> /dev/null || :
%endif


%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_libdir}/nss3.dll
%{_libdir}/ssl3.dll
%{_libdir}/smime3.dll
%{_libdir}/nssckbi.dll
%if %{with_blankdb}
%dir %{_sysconfdir}/pki/nssdb
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/pki/nssdb/cert8.db
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/pki/nssdb/key3.db
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/pki/nssdb/secmod.db
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/pki/nssdb/cert9.db
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/pki/nssdb/key4.db
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/pki/nssdb/pkcs11.txt
%endif
%if %{with_crypto_pol}
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/crypto-policies/local.d/nss-p11-kit.config
%endif
%if %{with_blankdb}
%doc %{_mandir}/man5/cert8.db.5*
%doc %{_mandir}/man5/key3.db.5*
%doc %{_mandir}/man5/secmod.db.5*
%doc %{_mandir}/man5/cert9.db.5*
%doc %{_mandir}/man5/key4.db.5*
%doc %{_mandir}/man5/pkcs11.txt.5*
%endif

%if %{with_sysinit}
%files sysinit
%{_libdir}/libnsssysinit.so
%{_bindir}/setup-nsssysinit.sh
# symbolic link to setup-nsssysinit.sh
%{_bindir}/setup-nsssysinit
%doc %{_mandir}/man1/setup-nsssysinit.1*
%endif

%files tools
%{_bindir}/certutil.exe
%{_bindir}/cmsutil.exe
%{_bindir}/crlutil.exe
%{_bindir}/modutil.exe
%{_bindir}/nss-policy-check.exe
%{_bindir}/pk12util.exe
%{_bindir}/signver.exe
%{_bindir}/ssltap.exe
%{unsupported_tools_directory}/atob.exe
%{unsupported_tools_directory}/btoa.exe
%{unsupported_tools_directory}/derdump.exe
%{unsupported_tools_directory}/listsuites.exe
%{unsupported_tools_directory}/ocspclnt.exe
%{unsupported_tools_directory}/pp.exe
%{unsupported_tools_directory}/selfserv.exe
%{unsupported_tools_directory}/signtool.exe
%{unsupported_tools_directory}/strsclnt.exe
%{unsupported_tools_directory}/symkeyutil.exe
%{unsupported_tools_directory}/tstclnt.exe
%{unsupported_tools_directory}/vfyserv.exe
%{unsupported_tools_directory}/vfychain.exe
# instead of %%{_mandir}/man*/* let's list them explicitely
# supported tools
%doc %{_mandir}/man1/certutil.1*
%doc %{_mandir}/man1/cmsutil.1*
%doc %{_mandir}/man1/crlutil.1*
%doc %{_mandir}/man1/modutil.1*
%doc %{_mandir}/man1/pk12util.1*
%doc %{_mandir}/man1/signver.1*
# unsupported tools
%doc %{_mandir}/man1/derdump.1*
%doc %{_mandir}/man1/signtool.1*
%if %{defined rhel}
%doc %{_mandir}/man1/pp.1*
%else
%dir %{_datadir}/doc/nss-tools
%doc %{_datadir}/doc/nss-tools/pp.1
%endif
%doc %{_mandir}/man1/ssltap.1*
%doc %{_mandir}/man1/vfychain.1*
%doc %{_mandir}/man1/vfyserv.1*

%files devel
%{_libdir}/crmf.a
%{_libdir}/nss3.a
%{_libdir}/smime3.a
%{_libdir}/ssl3.a
%{_libdir}/pkgconfig/nss.pc
%{_bindir}/nss-config
%doc %{_mandir}/man1/nss-config.1*

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
%{_includedir}/nss3/sslexp.h
%{_includedir}/nss3/sslproto.h
%{_includedir}/nss3/sslt.h

%files pkcs11-devel
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
%{_libdir}/nss3k.dll
%{_libdir}/ssl3k.dll
%{_libdir}/smime3k.dll
%{_libdir}/nssckbik.dll

%files util
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_libdir}/nssutil3.dll

%files util-devel
%{_libdir}/nssutil3.a
# package configuration files
%{_libdir}/pkgconfig/nss-util.pc
%{_bindir}/nss-util-config

# co-owned with nss
%dir %{_includedir}/nss3
# these are marked as public export in nss/lib/util/manifest.mk
%{_includedir}/nss3/base64.h
%{_includedir}/nss3/ciferfam.h
%{_includedir}/nss3/eccutil.h
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
%{_includedir}/nss3/pkcs11uri.h
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
%{_libdir}/nssuti3k.dll

%files softokn
%{_libdir}/nssdbm3.dll
%{_libdir}/nssdbm3.chk
%{_libdir}/softokn3.dll
%{_libdir}/softokn3.chk
# shared with nss-tools
%dir %{_libdir}/nss
%dir %{saved_files_dir}
%dir %{unsupported_tools_directory}
%{unsupported_tools_directory}/bltest.exe
%{unsupported_tools_directory}/ecperf.exe
%{unsupported_tools_directory}/fbectest.exe
%{unsupported_tools_directory}/fipstest.exe
%{unsupported_tools_directory}/shlibsign.exe

%files softokn-freebl
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_libdir}/freebl3.dll
%{_libdir}/freebl3.chk
#shared
%if %{with_dracut}
%dir %{dracut_modules_dir}
%{dracut_modules_dir}/module-setup.sh
%{dracut_conf_dir}/50-nss-softokn.conf
%endif

%files softokn-freebl-devel
%{_libdir}/freebl.a
%{_includedir}/nss3/blapi.h
%{_includedir}/nss3/blapit.h
%{_includedir}/nss3/alghmac.h
%{_includedir}/nss3/cmac.h
%{_includedir}/nss3/lowkeyi.h
%{_includedir}/nss3/lowkeyti.h

%files softokn-freebl-legacy
%{_libdir}/freebl3k.dll
%{_libdir}/freebl3k.chk

%files softokn-devel
%{_libdir}/nssdbm3.a
%{_libdir}/softokn3.a
%{_libdir}/pkgconfig/nss-softokn.pc
%{_bindir}/nss-softokn-config

# co-owned with nss
%dir %{_includedir}/nss3
#
# The following headers are those exported public in
# nss/lib/freebl/manifest.mn and
# nss/lib/softoken/manifest.mn
#
# The following list is short because many headers, such as
# the pkcs #11 ones, have been provided by nss-util-devel
# which installed them before us.
#
%{_includedir}/nss3/ecl-exp.h
%if %{with_lowhash}
%{_includedir}/nss3/nsslowhash.h
%endif
%{_includedir}/nss3/shsign.h

%files softokn-legacy
%{_libdir}/nssdbm3k.dll
%{_libdir}/nssdbm3k.chk
%{_libdir}/softok3k.dll
%{_libdir}/softok3k.chk


%changelog
* Wed Nov 20 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.47.0-1
- update to version 3.47
- merge spec from fedora with our version
- fix a requires softokn vs softoken issue in legacy-packages

* Thu Feb 23 2017 Dmitriy Kuminov <coding@dmik.org> - 3.23.0-4
- Use scm_source and friends.
- Generate more compact forwarder DLLs with better memory footprint.

* Fri Apr 15 2016 Dmitriy Kuminov <coding@dmik.org> 3.23.0-3
- Remove erroneous -Wl,-rpath-link from nss-config and others.

* Fri Apr 1 2016 Dmitriy Kuminov <coding@dmik.org> 3.23.0-2
- Enable high memory support.

* Wed Mar 30 2016 Dmitriy Kuminov <coding@dmik.org> 3.23.0-1
- Update to version 3.23.
- Import OS/2-specific NSS fixes from Mozilla for OS/2 sources.
- Rebuild with GCC 4.9.2 and LIBC 0.6.6.

* Mon Jan 16 2012 yd
- rebuild with libc 0.6.4 runtime.
