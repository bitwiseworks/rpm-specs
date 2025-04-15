# To be reversed as soon as we verify that majority of software compiles
# fine against 3.0 version
%bcond_without devel

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

Summary: Compatibility version of the OpenSSL library
Name: openssl1.1
Version: 1.1.1w
Release: 2%{?dist}
Epoch: 1
%if !0%{?os2_version}
# We have to remove certain patented algorithms from the openssl source
# tarball with the hobble-openssl script which is included below.
# The original openssl upstream tarball cannot be shipped in the .src.rpm.
Source: openssl-%{version}-hobbled.tar.xz
Source1: hobble-openssl
Source9: opensslconf-new.h
Source10: opensslconf-new-warning.h
Source12: ec_curve.c
Source13: ectest.c
# Build changes
Patch1: openssl-1.1.1-build.patch
Patch2: openssl-1.1.1-defaults.patch
Patch3: openssl-1.1.1-no-html.patch
Patch4: openssl-1.1.1-man-rename.patch

# Functionality changes
Patch31: openssl-1.1.1-conf-paths.patch
Patch32: openssl-1.1.1-version-add-engines.patch
Patch33: openssl-1.1.1-apps-dgst.patch
Patch36: openssl-1.1.1-no-brainpool.patch
Patch37: openssl-1.1.1-ec-curves.patch
Patch38: openssl-1.1.1-no-weak-verify.patch
Patch40: openssl-1.1.1-disable-ssl3.patch
Patch41: openssl-1.1.1-system-cipherlist.patch
Patch42: openssl-1.1.1-fips.patch
Patch44: openssl-1.1.1-version-override.patch
Patch45: openssl-1.1.1-weak-ciphers.patch
Patch46: openssl-1.1.1-seclevel.patch
Patch47: openssl-1.1.1-ts-sha256-default.patch
Patch48: openssl-1.1.1-fips-post-rand.patch
Patch49: openssl-1.1.1-evp-kdf.patch
Patch50: openssl-1.1.1-ssh-kdf.patch
Patch51: openssl-1.1.1-intel-cet.patch
Patch60: openssl-1.1.1-krb5-kdf.patch
Patch61: openssl-1.1.1-edk2-build.patch
Patch62: openssl-1.1.1-fips-curves.patch
Patch65: openssl-1.1.1-fips-drbg-selftest.patch
Patch66: openssl-1.1.1-fips-dh.patch
Patch67: openssl-1.1.1-kdf-selftest.patch
Patch69: openssl-1.1.1-alpn-cb.patch
Patch70: openssl-1.1.1-rewire-fips-drbg.patch
# Backported fixes including security fixes
Patch52: openssl-1.1.1-s390x-update.patch
Patch53: openssl-1.1.1-fips-crng-test.patch
Patch55: openssl-1.1.1-arm-update.patch
Patch56: openssl-1.1.1-s390x-ecc.patch
Patch57: openssl1.1-c99.patch
%else
Vendor: bww bitwise works GmbH
%scm_source github http://github.com/bitwiseworks/openssl-os2 %{version}-os2
%endif

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
Conflicts: openssl-libs < 1:3.0
Provides: deprecated()

%description
The OpenSSL toolkit provides support for secure communications between
machines. This version of OpenSSL package contains only the libraries
from the 1.1.1 version and is provided for compatibility with previous
releases.

%if %{with devel}
%package devel
Summary: Files for development of applications which will use OpenSSL
%if !0%{?os2_version}
Requires: %{name}%{?_isa} = %{epoch}:%{version}-%{release}
%else
Requires: %{name}-libs = %{epoch}:%{version}-%{release}
%endif
Requires: pkgconfig
# The devel subpackage intentionally conflicts with main openssl-devel
# as simultaneous use of both openssl package cannot be encouraged.
# Making the packages non-conflicting would also require further
# changes in the dependent packages.
Conflicts: openssl-devel
Provides: deprecated()

%description devel
OpenSSL is a toolkit for supporting cryptography. The openssl-devel
package contains include files needed to develop applications which
support various cryptographic algorithms and protocols.
%endif

%if 0%{?os2_version}
%debug_package
%endif

%prep
%if !0%{?os2_version}
%setup -q -n openssl-%{version}

# The hobble_openssl is called here redundantly, just to be sure.
# The tarball has already the sources removed.
%{SOURCE1} > /dev/null

cp %{SOURCE12} crypto/ec/
cp %{SOURCE13} test/

%patch1 -p1 -b .build   %{?_rawbuild}
%patch2 -p1 -b .defaults
%patch3 -p1 -b .no-html  %{?_rawbuild}
%patch4 -p1 -b .man-rename

%patch31 -p1 -b .conf-paths
%patch32 -p1 -b .version-add-engines
%patch33 -p1 -b .dgst
%patch36 -p1 -b .no-brainpool
%patch37 -p1 -b .curves
%patch38 -p1 -b .no-weak-verify
%patch40 -p1 -b .disable-ssl3
%patch41 -p1 -b .system-cipherlist
%patch42 -p1 -b .fips
%patch44 -p1 -b .version-override
%patch45 -p1 -b .weak-ciphers
%patch46 -p1 -b .seclevel
%patch47 -p1 -b .ts-sha256-default
%patch48 -p1 -b .fips-post-rand
%patch49 -p1 -b .evp-kdf
%patch50 -p1 -b .ssh-kdf
%patch51 -p1 -b .intel-cet
%patch52 -p1 -b .s390x-update
%patch53 -p1 -b .crng-test
%patch55 -p1 -b .arm-update
%patch56 -p1 -b .s390x-ecc
%patch57 -p1
%patch60 -p1 -b .krb5-kdf
%patch61 -p1 -b .edk2-build
%patch62 -p1 -b .fips-curves
%patch65 -p1 -b .drbg-selftest
%patch66 -p1 -b .fips-dh
%patch67 -p1 -b .kdf-selftest
%patch69 -p1 -b .alpn-cb
%patch70 -p1 -b .rewire-fips-drbg
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

# We must revert patch31 before tests otherwise they will fail
patch -p1 -R < %{PATCH31}

%define __provides_exclude_from %{_libdir}/openssl
%endif

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
else
cd ..
%endif

# Delete static library
%if !0%{?os2_version}
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a || :
%else
rm -f $RPM_BUILD_ROOT%{_libdir}/*_s.a || :
%endif

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

# Delete non-devel man pages in the compat package
rm -rf $RPM_BUILD_ROOT%{_mandir}/man[157]*

# Delete configuration files
rm -rf  $RPM_BUILD_ROOT%{_sysconfdir}/pki/*

# Remove binaries
rm -rf $RPM_BUILD_ROOT/%{_bindir}

# Remove useless capi engine
rm -f $RPM_BUILD_ROOT/%{_libdir}/engines-1.1/capi.so

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
%endif

%if %{without devel}
# Delete devel files
rm -rf $RPM_BUILD_ROOT%{_includedir}/openssl
rm -rf $RPM_BUILD_ROOT%{_mandir}/man3*
rm -rf $RPM_BUILD_ROOT%{_libdir}/*.so
rm -rf $RPM_BUILD_ROOT%{_libdir}/pkgconfig
%endif

%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc FAQ NEWS README README.FIPS
%if !0%{?os2_version}
%attr(0755,root,root) %{_libdir}/libcrypto.so.%{version}
%attr(0755,root,root) %{_libdir}/libcrypto.so.%{soversion}
%attr(0755,root,root) %{_libdir}/libssl.so.%{version}
%attr(0755,root,root) %{_libdir}/libssl.so.%{soversion}
%else
%attr(0755,root,root) %{_libdir}/crypto%{dllversion}.dll
%attr(0755,root,root) %{_libdir}/ssl%{dllversion}.dll
%endif
%attr(0755,root,root) %{_libdir}/engines-%{soversion}

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

%if !0%{?os2_version}
%ldconfig_scriptlets
%endif

%changelog
* Wed Apr 16 2025 Silvan Scherrer <silvan.scherrer@aroa.ch> 1:1.1.1w-2
- prepair for openssl 3.x
- resync the spec with latest fedora openssl1.1 version

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
