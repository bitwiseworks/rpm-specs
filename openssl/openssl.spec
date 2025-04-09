# For the curious:
# 0.9.8jk + EAP-FAST soversion = 8
# 1.0.0 soversion = 10
# 1.1.0 soversion = 1.1 (same as upstream although presence of some symbols
#                        depends on build configuration options)
# 3.0.0 soversion = 3 (same as upstream)
%define soversion 3

# Arches on which we need to prevent arch conflicts on opensslconf.h, must
# also be handled in opensslconf-new.h.
%define multilib_arches %{ix86} ia64 %{mips} ppc ppc64 s390 s390x sparcv9 sparc64 x86_64

%if !0%{?os2_version}
%define srpmhash() %{lua:
local files = rpm.expand("%_specdir/openssl.spec")
for i, p in ipairs(patches) do
   files = files.." "..p
end
for i, p in ipairs(sources) do
   files = files.." "..p
end
local sha256sum = assert(io.popen("cat "..files.." 2>/dev/null | sha256sum"))
local hash = sha256sum:read("*a")
sha256sum:close()
print(string.sub(hash, 0, 16))
}
%endif

%global _performance_build 1

Summary: Utilities from the general purpose cryptography library with TLS implementation
Name: openssl
Version: 3.4.1
Release: 1%{?dist}
Epoch: 1
%if !0%{?os2_version}
Source: openssl-%{version}-beta1.tar.gz
Source2: Makefile.certificate
Source3: genpatches
Source4: openssl.rpmlintrc
Source6: make-dummy-cert
Source7: renew-dummy-cert
Source9: configuration-switch.h
Source10: configuration-prefix.h

Patch0001: 0001-RH-Aarch64-and-ppc64le-use-lib64.patch
Patch0002: 0002-Add-a-separate-config-file-to-use-for-rpm-installs.patch
Patch0003: 0003-RH-Do-not-install-html-docs.patch
Patch0004: 0004-RH-Override-default-paths-for-the-CA-directory-tree.patch
Patch0005: 0005-RH-Instructions-to-load-legacy-provider.patch
Patch0006: 0006-RH-apps-ca-fix-md-option-help-text.patch-DROP.patch
Patch0007: 0007-RH-Disable-signature-verification-with-bad-digests-R.patch
Patch0008: 0008-RH-Add-support-for-PROFILE-SYSTEM-system-default-cip.patch
Patch0009: 0009-RH-Add-FIPS_mode-compatibility-macro.patch
Patch0010: 0010-RH-Add-Kernel-FIPS-mode-flag-support-FIXSTYLE.patch
Patch0011: 0011-RH-Drop-weak-curve-definitions-RENAMED-SQUASHED.patch
Patch0012: 0012-RH-Disable-explicit-ec-curves.patch
Patch0013: 0013-RH-skipped-tests-EC-curves.patch
Patch0014: 0014-RH-skip-quic-pairwise.patch
Patch0015: 0015-RH-version-aliasing.patch
Patch0016: 0016-RH-Export-two-symbols-for-OPENSSL_str-n-casecmp.patch
Patch0017: 0017-RH-TMP-KTLS-test-skip.patch
Patch0018: 0018-RH-Allow-disabling-of-SHA1-signatures.patch
Patch0019: 0019-RH-Set-default-certificate-digest-to-sha256.patch
Patch0020: 0020-FIPS-Red-Hat-s-FIPS-module-name-and-version.patch
Patch0021: 0021-FIPS-disable-fipsinstall.patch
Patch0022: 0022-FIPS-Force-fips-provider-on.patch
Patch0023: 0023-FIPS-INTEG-CHECK-Embed-hmac-in-fips.so-NOTE.patch
Patch0024: 0024-FIPS-INTEG-CHECK-Add-script-to-hmac-ify-fips.so.patch
Patch0025: 0025-FIPS-INTEG-CHECK-Execute-KATS-before-HMAC-REVIEW.patch
Patch0026: 0026-FIPS-RSA-encrypt-limits-REVIEW.patch
Patch0027: 0027-FIPS-RSA-PCTs.patch
Patch0028: 0028-FIPS-RSA-encapsulate-limits.patch
Patch0029: 0029-FIPS-RSA-Disallow-SHAKE-in-OAEP-and-PSS.patch
Patch0030: 0030-FIPS-RSA-size-mode-restrictions.patch
Patch0031: 0031-FIPS-RSA-Mark-x931-as-not-approved-by-default.patch
Patch0032: 0032-FIPS-RSA-Remove-X9.31-padding-signatures-tests.patch
Patch0033: 0033-FIPS-RSA-NEEDS-REWORK-FIPS-Use-OAEP-in-KATs-support-.patch
Patch0034: 0034-FIPS-Deny-SHA-1-signature-verification.patch
Patch0035: 0035-FIPS-RAND-FIPS-140-3-DRBG-NEEDS-REVIEW.patch
Patch0036: 0036-FIPS-RAND-Forbid-truncated-hashes-SHA-3.patch
Patch0037: 0037-FIPS-PBKDF2-Set-minimum-password-length.patch
Patch0038: 0038-FIPS-DH-PCT.patch
Patch0039: 0039-FIPS-DH-Disable-FIPS-186-4-type-parameters.patch
Patch0040: 0040-FIPS-TLS-Enforce-EMS-in-TLS-1.2-NOTE.patch
Patch0041: 0041-FIPS-CMS-Set-default-padding-to-OAEP.patch
Patch0042: 0042-FIPS-PKCS12-PBMAC1-defaults.patch
Patch0043: 0043-FIPS-Fix-encoder-decoder-negative-test.patch
Patch0044: 0044-FIPS-EC-DH-DSA-PCTs.patch
Patch0045: 0045-FIPS-EC-disable-weak-curves.patch
Patch0046: 0046-FIPS-NO-DSA-Support.patch
Patch0047: 0047-FIPS-NO-DES-support.patch
Patch0048: 0048-FIPS-NO-Kmac.patch
Patch0049: 0049-FIPS-NO-ECX-Ed-X-25519-448.patch
Patch0050: 0050-FIPS-NO-PQ-ML-SLH-DSA.patch
Patch0051: 0051-Revert-FIPS-NO-ECX-Ed-X-25519-448.patch
Patch0052: 0052-FIPS-Fix-some-tests-due-to-our-versioning-change.patch
Patch0053: 0053-Current-Rebase-status.patch
%else
Vendor: bww bitwise works GmbH
%scm_source github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2
%endif

License: Apache-2.0
URL: http://www.openssl.org/
BuildRequires: gcc g++
BuildRequires: make
%if !0%{?os2_version}
BuildRequires: coreutils, perl-interpreter, sed, zlib-devel, /usr/bin/cmp
BuildRequires: lksctp-tools-devel
BuildRequires: /usr/bin/rename
BuildRequires: /usr/bin/pod2man
BuildRequires: /usr/sbin/sysctl
%else
BuildRequires: coreutils, perl, sed, zlib-devel, /@unixroot/usr/bin/cmp.exe
BuildRequires: /@unixroot/usr/bin/pod2man
%endif
BuildRequires: perl(Test::Harness), perl(Test::More), perl(Math::BigInt)
BuildRequires: perl(Module::Load::Conditional), perl(File::Temp)
%if !0%{?os2_version}
BuildRequires: perl(Time::HiRes), perl(Time::Piece), perl(IPC::Cmd), perl(Pod::Html), perl(Digest::SHA)
%else
BuildRequires: perl(Time::HiRes), perl(IPC::Cmd), perl(Pod::Html), perl(Digest::SHA)
%endif
BuildRequires: perl(FindBin), perl(lib), perl(File::Compare), perl(File::Copy), perl(bigint)
BuildRequires: git-core
%if !0%{?os2_version}
BuildRequires: systemtap-sdt-devel
%endif
Requires: coreutils
%if !0%{?os2_version}
Requires: %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
%else
Requires: %{name}-libs = %{epoch}:%{version}-%{release}
%endif

%description
The OpenSSL toolkit provides support for secure communications between
machines. OpenSSL includes a certificate management tool and shared
libraries which provide various cryptographic algorithms and
protocols.

%package libs
Summary: A general purpose cryptography library with TLS implementation
Requires: ca-certificates >= 2008-5
%if !0%{?os2_version}
Requires: crypto-policies >= 20180730
%endif
%if 0%{?fedora} >= 40 || 0%{?rhel} >= 10
Recommends: pkcs11-provider%{?_isa}
%else
%if !0%{?os2_version}
Recommends: openssl-pkcs11%{?_isa}
%else
Recommends: openssl-pkcs11
%endif
%endif
%if ( %{defined rhel} && (! %{defined centos}) && (! %{defined eln}) )
Requires: openssl-fips-provider
%endif

%description libs
OpenSSL is a toolkit for supporting cryptography. The openssl-libs
package contains the libraries that are used by various applications which
support cryptographic algorithms and protocols.

%package devel
Summary: Files for development of applications which will use OpenSSL
%if !0%{?os2_version}
Requires: %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
%else
Requires: %{name}-libs = %{epoch}:%{version}-%{release}
%endif
Requires: pkgconfig

%description devel
OpenSSL is a toolkit for supporting cryptography. The openssl-devel
package contains include files needed to develop applications which
support various cryptographic algorithms and protocols.

%package devel-engine
Summary: Files for development of applications which will use OpenSSL and use deprecated ENGINE API.
%if !0%{?os2_version}
Requires: %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
Requires: %{name}-devel%{?_isa} = %{epoch}:%{version}-%{release}
%else
Requires: %{name}-libs = %{epoch}:%{version}-%{release}
Requires: %{name}-devel = %{epoch}:%{version}-%{release}
%endif
Requires: pkgconfig
Provides: deprecated()

%description devel-engine
OpenSSL is a toolkit for supporting cryptography. The openssl-devel-engine
package contains include files needed to develop applications which
use deprecated OpenSSL ENGINE functionality.

%package perl
Summary: Perl scripts provided with OpenSSL
%if !0%{?os2_version}
Requires: perl-interpreter
Requires: %{name}%{?_isa} = %{epoch}:%{version}-%{release}
%else
Requires: perl
Requires: %{name} = %{epoch}:%{version}-%{release}
%endif

%description perl
OpenSSL is a toolkit for supporting cryptography. The openssl-perl
package provides Perl scripts for converting certificates and keys
from other formats to the formats used by the OpenSSL toolkit.

%if 0%{?os2_version}
%legacy_runtime_packages

%debug_package
%endif

%prep
%if !0%{?os2_version}
%autosetup -S git -n %{name}-%{version}-beta1
%else
%scm_setup
%endif

%build
# Figure out which flags we want to use.
# default
%if 0%{?os2_version}
sslarch=os2
%else
sslarch=%{_os}-%{_target_cpu}
%ifarch %ix86
sslarch=linux-elf
if ! echo %{_target} | grep -q i686 ; then
	sslflags="no-asm 386"
fi
%endif
%ifarch x86_64
sslflags=enable-ec_nistp_64_gcc_128
%endif
%ifarch sparcv9
sslarch=linux-sparcv9
sslflags=no-asm
%endif
%ifarch sparc64
sslarch=linux64-sparcv9
sslflags=no-asm
%endif
%ifarch alpha alphaev56 alphaev6 alphaev67
sslarch=linux-alpha-gcc
%endif
%ifarch s390 sh3eb sh4eb
sslarch="linux-generic32 -DB_ENDIAN"
%endif
%ifarch s390x
sslarch="linux64-s390x"
%endif
%ifarch %{arm}
sslarch=linux-armv4
%endif
%ifarch aarch64
sslarch=linux-aarch64
sslflags=enable-ec_nistp_64_gcc_128
%endif
%ifarch sh3 sh4
sslarch=linux-generic32
%endif
%ifarch ppc64 ppc64p7
sslarch=linux-ppc64
%endif
%ifarch ppc64le
sslarch="linux-ppc64le"
sslflags=enable-ec_nistp_64_gcc_128
%endif
%ifarch mips mipsel
sslarch="linux-mips32 -mips32r2"
%endif
%ifarch mips64 mips64el
sslarch="linux64-mips64 -mips64r2"
%endif
%ifarch mips64el
sslflags=enable-ec_nistp_64_gcc_128
%endif
%ifarch riscv64
sslarch=linux64-riscv64
%endif
ktlsopt=enable-ktls
%ifarch armv7hl
ktlsopt=disable-ktls
%endif
%endif

# Add -Wa,--noexecstack here so that libcrypto's assembler modules will be
# marked as not requiring an executable stack.
# Also add -DPURIFY to make using valgrind with openssl easier as we do not
# want to depend on the uninitialized memory as a source of entropy anyway.
%if !0%{?os2_version}
RPM_OPT_FLAGS="$RPM_OPT_FLAGS -Wa,--noexecstack -Wa,--generate-missing-build-notes=yes -DPURIFY $RPM_LD_FLAGS"

export HASHBANGPERL=/usr/bin/perl
%else
RPM_OPT_FLAGS="$RPM_OPT_FLAGS $RPM_LD_FLAGS"

export HASHBANGPERL=/@unixroot/usr/bin/perl
%endif

%if !0%{?os2_version}
%define fips %{version}-%{srpmhash}
%endif
# ia64, x86_64, ppc are OK by default
# Configure the build tree.  Override OpenSSL defaults with known-good defaults
# usable on all platforms.  The Configure script already knows to use -fPIC and
# RPM_OPT_FLAGS, so we can skip specifiying them here.

%if 0%{?os2_version}
libs=-lcx
export CFLAGS="${CFLAGS:-%optflags}"
export VENDOR="%{vendor}"
%endif
./Configure \
	--prefix=%{_prefix} --openssldir=%{_sysconfdir}/pki/tls ${sslflags} \
%ifarch riscv64
        --libdir=%{_lib} \
%endif
%if !0%{?os2_version}
	--system-ciphers-file=%{_sysconfdir}/crypto-policies/back-ends/opensslcnf.config \
	zlib enable-camellia enable-seed enable-rfc3779 enable-sctp \
	enable-cms enable-md2 enable-rc5 ${ktlsopt} enable-fips -D_GNU_SOURCE\
%else
	zlib enable-camellia enable-seed enable-rfc3779 \
	enable-cms enable-md2 enable-rc5 -D_GNU_SOURCE\
%endif
	no-mdc2 no-ec2m no-sm2 no-sm4 no-atexit enable-buildtest-c++\
%if !0%{?os2_version}
	shared  ${sslarch} $RPM_OPT_FLAGS '-DDEVRANDOM="\"/dev/urandom\""' -DOPENSSL_PEDANTIC_ZEROIZATION\
	-DREDHAT_FIPS_VENDOR='"\"Red Hat Enterprise Linux OpenSSL FIPS Provider\""' -DREDHAT_FIPS_VERSION='"\"Rebase Testing\""'\
	-Wl,--allow-multiple-definition
%else
	shared  ${sslarch} $RPM_OPT_FLAGS ${libs}
%endif

# Do not run this in a production package the FIPS symbols must be patched-in
#util/mkdef.pl crypto update

make -s %{?_smp_mflags} all

# Clean up the .pc files
for i in libcrypto.pc libssl.pc openssl.pc ; do
  sed -i '/^Libs.private:/{s/-L[^ ]* //;s/-Wl[^ ]* //}' $i
done

%check
# Verify that what was compiled actually works.

%if 0%{?os2_version}
# this need to be set, as else it might use a already loaded one
export LIBPATHSTRICT=T
export BEGINLIBPATH=%{_builddir}/%{buildsubdir}
%else
# Hack - either enable SCTP AUTH chunks in kernel or disable sctp for check
(sysctl net.sctp.addip_enable=1 && sysctl net.sctp.auth_enable=1) || \
(echo 'Failed to enable SCTP AUTH chunks, disabling SCTP for tests...' &&
 sed '/"msan" => "default",/a\ \ "sctp" => "default",' configdata.pm > configdata.pm.new && \
 touch -r configdata.pm configdata.pm.new && \
 mv -f configdata.pm.new configdata.pm)

# We must revert patch4 before tests otherwise they will fail
#patch -p1 -R < %{PATCH4}
#We must disable default provider before tests otherwise they will fail
#patch -p1 < %{SOURCE14}

OPENSSL_ENABLE_MD5_VERIFY=
export OPENSSL_ENABLE_MD5_VERIFY
OPENSSL_ENABLE_SHA1_SIGNATURES=
export OPENSSL_ENABLE_SHA1_SIGNATURES
OPENSSL_SYSTEM_CIPHERS_OVERRIDE=xyz_nonexistent_file
export OPENSSL_SYSTEM_CIPHERS_OVERRIDE
#embed HMAC into fips provider for test run
dd if=/dev/zero bs=1 count=32 of=tmp.mac
objcopy --update-section .rodata1=tmp.mac providers/fips.so providers/fips.so.zeromac
mv providers/fips.so.zeromac providers/fips.so
rm tmp.mac
LD_LIBRARY_PATH=. apps/openssl dgst -binary -sha256 -mac HMAC -macopt hexkey:f4556650ac31d35461610bac4ed81b1a181b2d8a43ea2854cbae22ca74560813 < providers/fips.so > providers/fips.so.hmac
objcopy --update-section .rodata1=providers/fips.so.hmac providers/fips.so providers/fips.so.mac
mv providers/fips.so.mac providers/fips.so
#run tests itself
make test HARNESS_JOBS=8
#make test
%endif

# Add generation of HMAC checksum of the final stripped library
# We manually copy standard definition of __spec_install_post
# and add hmac calculation/embedding to fips.so
%if !0%{?os2_version}
%if ( %{defined rhel} && (! %{defined centos}) && (! %{defined eln}) )
%define __spec_install_post \
    rm -rf $RPM_BUILD_ROOT/%{_libdir}/ossl-modules/fips.so \
    %{?__debug_package:%{__debug_install_post}} \
    %{__arch_install_post} \
    %{__os_install_post} \
%{nil}
%else
%define __spec_install_post \
    %{?__debug_package:%{__debug_install_post}} \
    %{__arch_install_post} \
    %{__os_install_post} \
    dd if=/dev/zero bs=1 count=32 of=$RPM_BUILD_ROOT%{_libdir}/ossl-modules/tmp.mac \
    objcopy --update-section .rodata1=$RPM_BUILD_ROOT%{_libdir}/ossl-modules/tmp.mac $RPM_BUILD_ROOT%{_libdir}/ossl-modules/fips.so $RPM_BUILD_ROOT%{_libdir}/ossl-modules/fips.so.zeromac \
    mv $RPM_BUILD_ROOT%{_libdir}/ossl-modules/fips.so.zeromac $RPM_BUILD_ROOT%{_libdir}/ossl-modules/fips.so \
    rm $RPM_BUILD_ROOT%{_libdir}/ossl-modules/tmp.mac \
    OPENSSL_CONF=/dev/null LD_LIBRARY_PATH=. apps/openssl dgst -binary -sha256 -mac HMAC -macopt hexkey:f4556650ac31d35461610bac4ed81b1a181b2d8a43ea2854cbae22ca74560813 < $RPM_BUILD_ROOT%{_libdir}/ossl-modules/fips.so > $RPM_BUILD_ROOT%{_libdir}/ossl-modules/fips.so.hmac \
    objcopy --update-section .rodata1=$RPM_BUILD_ROOT%{_libdir}/ossl-modules/fips.so.hmac $RPM_BUILD_ROOT%{_libdir}/ossl-modules/fips.so $RPM_BUILD_ROOT%{_libdir}/ossl-modules/fips.so.mac \
    mv $RPM_BUILD_ROOT%{_libdir}/ossl-modules/fips.so.mac $RPM_BUILD_ROOT%{_libdir}/ossl-modules/fips.so \
    rm $RPM_BUILD_ROOT%{_libdir}/ossl-modules/fips.so.hmac \
%{nil}
%endif
%endif

%define __provides_exclude_from %{_libdir}/openssl

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
# Install OpenSSL.
%if !0%{?os2_version}
install -d $RPM_BUILD_ROOT{%{_bindir},%{_includedir},%{_libdir},%{_mandir},%{_libdir}/openssl,%{_pkgdocdir}}
%else
install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_includedir}
install -d $RPM_BUILD_ROOT%{_libdir}
install -d $RPM_BUILD_ROOT%{_mandir}
install -d $RPM_BUILD_ROOT%{_libdir}/openssl
install -d $RPM_BUILD_ROOT%{_pkgdocdir}
%endif
%make_install
%if !0%{?os2_version}
rename so.%{soversion} so.%{version} $RPM_BUILD_ROOT%{_libdir}/*.so.%{soversion}
for lib in $RPM_BUILD_ROOT%{_libdir}/*.so.%{version} ; do
	chmod 755 ${lib}
	ln -s -f `basename ${lib}` $RPM_BUILD_ROOT%{_libdir}/`basename ${lib} .%{version}`
	ln -s -f `basename ${lib}` $RPM_BUILD_ROOT%{_libdir}/`basename ${lib} .%{version}`.%{soversion}
done
mv rh-openssl.cnf $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/openssl.cnf

# Remove static libraries
for lib in $RPM_BUILD_ROOT%{_libdir}/*.a ; do
	rm -f ${lib}
done
%else

# Remove static libraries
for lib in $RPM_BUILD_ROOT%{_libdir}/*_s.a ; do
	rm -f ${lib}
done
%endif

# Install a makefile for generating keys and self-signed certs, and a script
# for generating them on the fly.
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/certs
%if !0%{?os2_version}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/openssl.d
install -m644 %{SOURCE2} $RPM_BUILD_ROOT%{_pkgdocdir}/Makefile.certificate
install -m755 %{SOURCE6} $RPM_BUILD_ROOT%{_bindir}/make-dummy-cert
install -m755 %{SOURCE7} $RPM_BUILD_ROOT%{_bindir}/renew-dummy-cert
%endif

# Move runable perl scripts to bindir
mv $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/misc/*.pl $RPM_BUILD_ROOT%{_bindir}
mv $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/misc/tsget $RPM_BUILD_ROOT%{_bindir}

# Rename man pages so that they don't conflict with other system man pages.
%if !0%{?os2_version}
pushd $RPM_BUILD_ROOT%{_mandir}
%else
pwd_save=`pwd`
cd $RPM_BUILD_ROOT%{_mandir}
%endif
mv man5/config.5ossl man5/openssl.cnf.5
%if !0%{?os2_version}
popd
%else
cd $pwd_save
%endif

mkdir -m755 $RPM_BUILD_ROOT%{_sysconfdir}/pki/CA
mkdir -m700 $RPM_BUILD_ROOT%{_sysconfdir}/pki/CA/private
mkdir -m755 $RPM_BUILD_ROOT%{_sysconfdir}/pki/CA/certs
mkdir -m755 $RPM_BUILD_ROOT%{_sysconfdir}/pki/CA/crl
mkdir -m755 $RPM_BUILD_ROOT%{_sysconfdir}/pki/CA/newcerts

# Ensure the config file timestamps are identical across builds to avoid
# mulitlib conflicts and unnecessary renames on upgrade
%if !0%{?os2_version}
touch -r %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/openssl.cnf
touch -r %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/ct_log_list.cnf
%endif

rm -f $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/openssl.cnf.dist
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/ct_log_list.cnf.dist
#we don't use native fipsmodule.cnf because FIPS module is loaded automatically
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/fipsmodule.cnf

# Determine which arch opensslconf.h is going to try to #include.
%if !0%{?os2_version}
basearch=%{_arch}
%ifarch %{ix86}
basearch=i386
%endif
%ifarch sparcv9
basearch=sparc
%endif
%ifarch sparc64
basearch=sparc64
%endif

# Next step of gradual disablement of ENGINE.
sed -i '/^\# ifndef OPENSSL_NO_STATIC_ENGINE/i\
# if !__has_include(<openssl/engine.h>) && !defined(OPENSSL_NO_ENGINE)\
#  define OPENSSL_NO_ENGINE\
# endif' $RPM_BUILD_ROOT/%{_prefix}/include/openssl/configuration.h

%ifarch %{multilib_arches}
# Do an configuration.h switcheroo to avoid file conflicts on systems where you
# can have both a 32- and 64-bit version of the library, and they each need
# their own correct-but-different versions of opensslconf.h to be usable.
install -m644 %{SOURCE10} \
	$RPM_BUILD_ROOT/%{_prefix}/include/openssl/configuration-${basearch}.h
cat $RPM_BUILD_ROOT/%{_prefix}/include/openssl/configuration.h >> \
	$RPM_BUILD_ROOT/%{_prefix}/include/openssl/configuration-${basearch}.h
install -m644 %{SOURCE9} \
	$RPM_BUILD_ROOT/%{_prefix}/include/openssl/configuration.h
%endif
ln -s /etc/crypto-policies/back-ends/openssl_fips.config $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/fips_local.cnf
%endif

%files
%{!?_licensedir:%global license %%doc}
%license LICENSE.txt
%doc NEWS.md README.md
%if !0%{?os2_version}
%{_bindir}/make-dummy-cert
%{_bindir}/renew-dummy-cert
%{_bindir}/openssl
%else
%{_bindir}/openssl.exe
%endif
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man7/*
%if !0%{?os2_version}
%{_pkgdocdir}/Makefile.certificate
%endif
%exclude %{_mandir}/man1/*.pl*
%exclude %{_mandir}/man1/tsget*

%files libs
%{!?_licensedir:%global license %%doc}
%license LICENSE.txt
%dir %{_sysconfdir}/pki/tls
%dir %{_sysconfdir}/pki/tls/certs
%dir %{_sysconfdir}/pki/tls/misc
%dir %{_sysconfdir}/pki/tls/private
%if !0%{?os2_version}
%dir %{_sysconfdir}/pki/tls/openssl.d
%endif
%config(noreplace) %{_sysconfdir}/pki/tls/openssl.cnf
%config(noreplace) %{_sysconfdir}/pki/tls/ct_log_list.cnf
%if !0%{?os2_version}
%config %{_sysconfdir}/pki/tls/fips_local.cnf
%attr(0755,root,root) %{_libdir}/libcrypto.so.%{version}
%{_libdir}/libcrypto.so.%{soversion}
%attr(0755,root,root) %{_libdir}/libssl.so.%{version}
%{_libdir}/libssl.so.%{soversion}
%else
%attr(0755,root,root) %{_libdir}/crypto%{soversion}.dll
%attr(0755,root,root) %{_libdir}/ssl%{soversion}.dll
%endif
%attr(0755,root,root) %{_libdir}/engines-%{soversion}
%attr(0755,root,root) %{_libdir}/ossl-modules
%if 0%{?os2_version}
%exclude %{_libdir}/engines-%{soversion}/*.dbg
%exclude %{_libdir}/ossl-modules/*.dbg
%endif

%files devel
%doc CHANGES.md doc/dir-locals.example.el doc/openssl-c-indent.el
%{_prefix}/include/openssl
%exclude %{_prefix}/include/openssl/engine*.h
%if !0%{?os2_version}
%{_libdir}/*.so
%else
%{_libdir}/*_dll.a
%endif
%{_mandir}/man3/*
%exclude %{_mandir}/man3/ENGINE*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/cmake/OpenSSL/OpenSSLConfig.cmake
%{_libdir}/cmake/OpenSSL/OpenSSLConfigVersion.cmake


%files devel-engine
%{_prefix}/include/openssl/engine*.h
%{_mandir}/man3/ENGINE*

%files perl
%{_bindir}/c_rehash
%{_bindir}/*.pl
%{_bindir}/tsget
%{_mandir}/man1/*.pl*
%{_mandir}/man1/tsget*
%dir %{_sysconfdir}/pki/CA
%dir %{_sysconfdir}/pki/CA/private
%dir %{_sysconfdir}/pki/CA/certs
%dir %{_sysconfdir}/pki/CA/crl
%dir %{_sysconfdir}/pki/CA/newcerts

%if !0%{?os2_version}
%ldconfig_scriptlets libs
%endif

%changelog
* Fri Apr 04 2025 Silvan Scherrer <silvan.scherrer@aroa.ch> 1:3.4.1-1
- Update to version 3.4.1.
- resync the spec with latest fedora

* Fri Mar 28 2025 Silvan Scherrer <silvan.scherrer@aroa.ch> 1:1.1.1w-1
- Update to version 1.1.1w.

* Wed Jan 11 2023 Silvan Scherrer <silvan.scherrer@aroa.ch> 1:1.1.1s-1
- Update to version 1.1.1s.

* Thu Jul 07 2022 Silvan Scherrer <silvan.scherrer@aroa.ch> 1:1.1.1q-1
- Update to version 1.1.1q.

* Thu Jun 16 2022 Silvan Scherrer <silvan.scherrer@aroa.ch> 1:1.1.1o-1
- Update to version 1.1.1o.

* Tue Aug 31 2021 Silvan Scherrer <silvan.scherrer@aroa.ch> 1:1.1.1l-1
- Update to version 1.1.1l.
- resync with fedora spec

* Tue Apr 13 2021 Silvan Scherrer <silvan.scherrer@aroa.ch> 1:1.1.1k-1
- Update to version 1.1.1k.

* Mon Nov 02 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> 1:1.1.1h-1
- Update to version 1.1.1h.

* Fri Sep 25 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> 1:1.1.1f-1
- Update to version 1.1.1f.
- resync the spec with latest fedora

* Wed Sep 18 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.0.2t-1
- Update to version 1.0.2t.

* Wed Nov 21 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.0.2q-1
- Update to version 1.0.2q.
- add a nice buildlevel string

* Wed May 02 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.0.2o-1
- Update to version 1.0.2o.
- moved source to github
- link against libcx

* Wed Mar 01 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.0.2k-1
- Update to version 1.0.2k.
- use new scm_ macros

* Wed Oct 26 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.0.2j-1
- Update to version 1.0.2j.

* Mon Jul 04 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.0.2h-3
- remove obsoletes tags from -libs
- add a requires tag to -libs

* Wed Jun 29 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.0.2h-2
- fix recursive symlink
- added debug package

* Wed Jun 29 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.0.2h-1
- Update to version 1.0.2h.

* Fri Apr 3 2015 Dmitriy Kuminov <coding@dmik.org> 1.0.0r-1
- Update to version 1.0.0r.
- Enable new algorithms: idea, md2, mdc2, ec, jpake.
- Rebuild with kLIBC 0.6.6 and GCC 4.9.2.

* Tue Sep 2 2014 Dmitriy Kuminov <coding@dmik.org> 1.0.0n-1
- Update to version 1.0.0n.
- Move find.pl to SVN repository.
- Remove DLLs from devel package.

* Wed Dec 05 2012 yd
- ca-certificates are required for proper ssl checks.
- added File::Find wrapper for find.pl.

* Mon Jan 16 2012 yd
- rebuild with libc 0.6.4 runtime.
