# For the curious:
# 0.9.5a soversion = 0
# 0.9.6  soversion = 1
# 0.9.6a soversion = 2
# 0.9.6c soversion = 3
# 0.9.7a soversion = 4
# 0.9.7ef soversion = 5
# 0.9.8ab soversion = 6
# 0.9.8g soversion = 7
# 0.9.8jk + EAP-FAST soversion = 8
# 1.0.0 soversion = 10
# 1.1.0 soversion = 1.1 (same as upstream although presence of some symbols
#                        depends on build configuration options)
%define soversion 1.1
%if 0%{?os2_version}
%define dllversion 11
%endif

# Arches on which we need to prevent arch conflicts on opensslconf.h, must
# also be handled in opensslconf-new.h.
%define multilib_arches %{ix86} ia64 %{mips} ppc ppc64 s390 s390x sparcv9 sparc64 x86_64

%global _performance_build 1

Summary: Utilities from the general purpose cryptography library with TLS implementation
Name: openssl
Version: 1.1.1l
Release: 1%{?dist}
Epoch: 1

License: OpenSSL and ASL 2.0
URL: http://www.openssl.org/
BuildRequires: make
BuildRequires: gcc
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
BuildRequires: perl(Time::HiRes)
BuildRequires: perl(FindBin), perl(lib), perl(File::Compare), perl(File::Copy)
Requires: coreutils
Requires: %{name}-libs = %{epoch}:%{version}-%{release}

Vendor: bww bitwise works GmbH
%scm_source github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2

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
Recommends: openssl-pkcs11
Provides: openssl-fips = %{epoch}:%{version}-%{release}

%description libs
OpenSSL is a toolkit for supporting cryptography. The openssl-libs
package contains the libraries that are used by various applications which
support cryptographic algorithms and protocols.

%package devel
Summary: Files for development of applications which will use OpenSSL
Requires: %{name}-libs = %{epoch}:%{version}-%{release}
Requires: pkgconfig

%description devel
OpenSSL is a toolkit for supporting cryptography. The openssl-devel
package contains include files needed to develop applications which
support various cryptographic algorithms and protocols.

%package static
Summary:  Libraries for static linking of applications which will use OpenSSL
Requires: %{name}-devel = %{epoch}:%{version}-%{release}

%description static
OpenSSL is a toolkit for supporting cryptography. The openssl-static
package contains static libraries needed for static linking of
applications which support various cryptographic algorithms and
protocols.

%package perl
Summary: Perl scripts provided with OpenSSL
Requires: perl
Requires: %{name} = %{epoch}:%{version}-%{release}

%description perl
OpenSSL is a toolkit for supporting cryptography. The openssl-perl
package provides Perl scripts for converting certificates and keys
from other formats to the formats used by the OpenSSL toolkit.

%debug_package

%prep
%scm_setup


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
sslarch=linux-generic64
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
export HASHBANGPERL=/@unixroot/usr/bin/perl
%endif

# ia64, x86_64, ppc are OK by default
# Configure the build tree.  Override OpenSSL defaults with known-good defaults
# usable on all platforms.  The Configure script already knows to use -fPIC and
# RPM_OPT_FLAGS, so we can skip specifiying them here.

%if 0%{?os2_version}
libs=-lcx
export CFLAGS="${CFLAGS:-%optflags}"
export VENDOR="%{vendor}"
mkdir build
cd build
../Configure \
%else
./Configure \
%endif
	--prefix=%{_prefix} --openssldir=%{_sysconfdir}/pki/tls ${sslflags} \
%if !0%{?os2_version}
	--system-ciphers-file=%{_sysconfdir}/crypto-policies/back-ends/openssl.config \
	zlib enable-camellia enable-seed enable-rfc3779 enable-sctp \
%else
	zlib enable-camellia enable-seed enable-rfc3779 \
%endif
	enable-cms enable-md2 enable-rc5 enable-ssl3 enable-ssl3-method \
	enable-weak-ssl-ciphers \
	no-mdc2 no-ec2m no-sm2 no-sm4 \
%if !0%{?os2_version}
	shared  ${sslarch} $RPM_OPT_FLAGS '-DDEVRANDOM="\"/dev/urandom\""'
%else
	shared  ${sslarch} ${libs}
%endif

# Do not run this in a production package the FIPS symbols must be patched-in
#util/mkdef.pl crypto update

%if 0%{?os2_version}
# patch Makefile, as our perl has a bug :(
sed -i 's/BLDDIR=/BLDDIR=./' Makefile
%endif

make all

# Clean up the .pc files
for i in libcrypto.pc libssl.pc openssl.pc ; do
  sed -i '/^Libs.private:/{s/-L[^ ]* //;s/-Wl[^ ]* //}' $i
done
%if 0%{?os2_version}
cd ..
%endif

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
 sed '/"zlib-dynamic" => "default",/a\ \ "sctp" => "default",' configdata.pm > configdata.pm.new && \
 touch -r configdata.pm configdata.pm.new && \
 mv -f configdata.pm.new configdata.pm)

LD_LIBRARY_PATH=`pwd`${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
export LD_LIBRARY_PATH
crypto/fips/fips_standalone_hmac libcrypto.so.%{soversion} >.libcrypto.so.%{soversion}.hmac
ln -s .libcrypto.so.%{soversion}.hmac .libcrypto.so.hmac
crypto/fips/fips_standalone_hmac libssl.so.%{soversion} >.libssl.so.%{soversion}.hmac
ln -s .libssl.so.%{soversion}.hmac .libssl.so.hmac
OPENSSL_ENABLE_MD5_VERIFY=
export OPENSSL_ENABLE_MD5_VERIFY
OPENSSL_SYSTEM_CIPHERS_OVERRIDE=xyz_nonexistent_file
export OPENSSL_SYSTEM_CIPHERS_OVERRIDE
make test
%endif

# Add generation of HMAC checksum of the final stripped library
%if !0%{?os2_version}
%define __spec_install_post \
    %{?__debug_package:%{__debug_install_post}} \
    %{__arch_install_post} \
    %{__os_install_post} \
    crypto/fips/fips_standalone_hmac $RPM_BUILD_ROOT%{_libdir}/libcrypto.so.%{version} >$RPM_BUILD_ROOT%{_libdir}/.libcrypto.so.%{version}.hmac \
    ln -sf .libcrypto.so.%{version}.hmac $RPM_BUILD_ROOT%{_libdir}/.libcrypto.so.%{soversion}.hmac \
    crypto/fips/fips_standalone_hmac $RPM_BUILD_ROOT%{_libdir}/libssl.so.%{version} >$RPM_BUILD_ROOT%{_libdir}/.libssl.so.%{version}.hmac \
    ln -sf .libssl.so.%{version}.hmac $RPM_BUILD_ROOT%{_libdir}/.libssl.so.%{soversion}.hmac \
%{nil}
%endif

%define __provides_exclude_from %{_libdir}/openssl

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
# Install OpenSSL.
%if !0%{?os2_version}
install -d $RPM_BUILD_ROOT{%{_bindir},%{_includedir},%{_libdir},%{_mandir},%{_libdir}/openssl,%{_pkgdocdir}}
%else
cd build
install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_includedir}
install -d $RPM_BUILD_ROOT%{_libdir}
install -d $RPM_BUILD_ROOT%{_mandir}
install -d $RPM_BUILD_ROOT%{_libdir}/openssl
%endif
%make_install
%if !0%{?os2_version}
rename so.%{soversion} so.%{version} $RPM_BUILD_ROOT%{_libdir}/*.so.%{soversion}
for lib in $RPM_BUILD_ROOT%{_libdir}/*.so.%{version} ; do
	chmod 755 ${lib}
	ln -s -f `basename ${lib}` $RPM_BUILD_ROOT%{_libdir}/`basename ${lib} .%{version}`
	ln -s -f `basename ${lib}` $RPM_BUILD_ROOT%{_libdir}/`basename ${lib} .%{version}`.%{soversion}
done
else
cd ..
%endif

# Install a makefile for generating keys and self-signed certs, and a script
# for generating them on the fly.
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/certs
%if !0%{?os2_version}
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
ln -s -f config.5 man5/openssl.cnf.5
for manpage in man*/* ; do
	if [ -L ${manpage} ]; then
		TARGET=`ls -l ${manpage} | awk '{ print $NF }'`
		ln -snf ${TARGET}ssl ${manpage}ssl
		rm -f ${manpage}
	else
		mv ${manpage} ${manpage}ssl
	fi
done
%if !0%{?os2_version}
for conflict in passwd rand ; do
	rename ${conflict} ssl${conflict} man*/${conflict}*
# Fix dangling symlinks
	manpage=man1/openssl-${conflict}.*
	if [ -L ${manpage} ] ; then
		ln -snf ssl${conflict}.1ssl ${manpage}
	fi
done
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

# Next step of gradual disablement of SSL3.
# Make SSL3 disappear to newly built dependencies.
sed -i '/^\#ifndef OPENSSL_NO_SSL_TRACE/i\
#ifndef OPENSSL_NO_SSL3\
# define OPENSSL_NO_SSL3\
#endif' $RPM_BUILD_ROOT/%{_prefix}/include/openssl/opensslconf.h

%ifarch %{multilib_arches}
# Do an opensslconf.h switcheroo to avoid file conflicts on systems where you
# can have both a 32- and 64-bit version of the library, and they each need
# their own correct-but-different versions of opensslconf.h to be usable.
install -m644 %{SOURCE10} \
	$RPM_BUILD_ROOT/%{_prefix}/include/openssl/opensslconf-${basearch}.h
cat $RPM_BUILD_ROOT/%{_prefix}/include/openssl/opensslconf.h >> \
	$RPM_BUILD_ROOT/%{_prefix}/include/openssl/opensslconf-${basearch}.h
install -m644 %{SOURCE9} \
	$RPM_BUILD_ROOT/%{_prefix}/include/openssl/opensslconf.h
%endif
LD_LIBRARY_PATH=`pwd`${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
export LD_LIBRARY_PATH
%endif


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc FAQ NEWS README README.FIPS
%if !0%{?os2_version}
%{_bindir}/make-dummy-cert
%{_bindir}/renew-dummy-cert
%{_bindir}/openssl
%else
%{_bindir}/openssl.exe
%endif
%{_mandir}/man1*/*
%{_mandir}/man5*/*
%{_mandir}/man7*/*
%if !0%{?os2_version}
%{_pkgdocdir}/Makefile.certificate
%endif
%exclude %{_mandir}/man1*/*.pl*
%exclude %{_mandir}/man1*/c_rehash*
%exclude %{_mandir}/man1*/openssl-c_rehash*
%exclude %{_mandir}/man1*/tsget*
%exclude %{_mandir}/man1*/openssl-tsget*

%files libs
%{!?_licensedir:%global license %%doc}
%license LICENSE
%dir %{_sysconfdir}/pki/tls
%dir %{_sysconfdir}/pki/tls/certs
%dir %{_sysconfdir}/pki/tls/misc
%dir %{_sysconfdir}/pki/tls/private
%config(noreplace) %{_sysconfdir}/pki/tls/openssl.cnf
%config(noreplace) %{_sysconfdir}/pki/tls/ct_log_list.cnf
%if !0%{?os2_version}
%attr(0755,root,root) %{_libdir}/libcrypto.so.%{version}
%attr(0755,root,root) %{_libdir}/libcrypto.so.%{soversion}
%attr(0755,root,root) %{_libdir}/libssl.so.%{version}
%attr(0755,root,root) %{_libdir}/libssl.so.%{soversion}
%attr(0644,root,root) %{_libdir}/.libcrypto.so.*.hmac
%attr(0644,root,root) %{_libdir}/.libssl.so.*.hmac
%else
%attr(0755,root,root) %{_libdir}/crypto%{dllversion}.dll
%attr(0755,root,root) %{_libdir}/ssl%{dllversion}.dll
%endif
%attr(0755,root,root) %{_libdir}/engines-%{soversion}
%if 0%{?os2_version}
%exclude %{_libdir}/engines-%{soversion}/*.dbg
%endif

%files devel
%doc CHANGES doc/dir-locals.example.el doc/openssl-c-indent.el
%{_prefix}/include/openssl
%if !0%{?os2_version}
%{_libdir}/*.so
%else
%{_libdir}/*_dll.a
%endif
%{_mandir}/man3*/*
%{_libdir}/pkgconfig/*.pc

%files static
%defattr(-,root,root)
%if !0%{?os2_version}
%{_libdir}/*.a
%else
%{_libdir}/*_s.a
%endif

%files perl
%{_bindir}/c_rehash
%{_bindir}/*.pl
%{_bindir}/tsget
%{_mandir}/man1*/*.pl*
%{_mandir}/man1*/c_rehash*
%{_mandir}/man1*/openssl-c_rehash*
%{_mandir}/man1*/tsget*
%{_mandir}/man1*/openssl-tsget*
%dir %{_sysconfdir}/pki/CA
%dir %{_sysconfdir}/pki/CA/private
%dir %{_sysconfdir}/pki/CA/certs
%dir %{_sysconfdir}/pki/CA/crl
%dir %{_sysconfdir}/pki/CA/newcerts

%if !0%{?os2_version}
%ldconfig_scriptlets libs
%endif

%changelog
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
