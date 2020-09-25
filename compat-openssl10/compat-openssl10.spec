%global _lto_cflags %{nil}
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
%global soversion 10
# Number of threads to spawn when testing some threading fixes.
%global thread_test_threads %{?threads:%{threads}}%{!?threads:1}

# Arches on which we need to prevent arch conflicts on opensslconf.h, must
# also be handled in opensslconf-new.h.
%global multilib_arches %{ix86} ia64 %{mips} ppc %{power64} s390 s390x sparcv9 sparc64 x86_64

%global _performance_build 1

Summary: Compatibility version of the OpenSSL library
Name: compat-openssl10
Version: 1.0.2u
Release: 1%{?dist}
Epoch: 1

License: OpenSSL
URL: http://www.openssl.org/
Vendor: bww bitwise works GmbH
%scm_source github http://github.com/bitwiseworks/openssl-os2 %{version}-os2

BuildRequires: gcc
%if !0%{?os2_version}
BuildRequires: coreutils, perl-interpreter, perl-generators, sed, zlib-devel, /usr/bin/cmp
BuildRequires: perl-FileHandle
BuildRequires: perl-File-Find-Rule, perl-File-Compare
BuildRequires: lksctp-tools-devel
BuildRequires: /usr/bin/rename
BuildRequires: /usr/bin/pod2man
%else
BuildRequires: coreutils, perl, perl-generators, sed, zlib-devel, diffutils
BuildRequires: /@unixroot/usr/bin/pod2man
%endif
Requires: coreutils
%if !0%{?os2_version}
Requires: coreutils, make
Requires: crypto-policies
%else
Requires: coreutils
%endif
Conflicts: openssl < 1:1.1.0, openssl-libs < 1:1.1.0

%description
The OpenSSL toolkit provides support for secure communications between
machines. This version of OpenSSL package contains only the libraries
and is provided for compatibility with previous releases and software
that does not support compilation with OpenSSL-1.1.


%package devel
Summary: Files for development of applications which have to use OpenSSL-1.0.2
Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: zlib-devel
Requires: pkgconfig
# The devel subpackage intentionally conflicts with main openssl-devel
# as simultaneous use of both openssl package cannot be encouraged.
# Making the packages non-conflicting would also require further
# changes in the dependent packages.
Conflicts: openssl-devel

%description devel
The OpenSSL toolkit provides support for secure communications between
machines. This version of OpenSSL package contains only the libraries
and is provided for compatibility with previous releases and software
that does not support compilation with OpenSSL-1.1. This package
contains include files needed to develop applications which
support various cryptographic algorithms and protocols.


%debug_package

%prep
%scm_setup

sed -i 's/SHLIB_VERSION_NUMBER "1.0.0"/SHLIB_VERSION_NUMBER "%{version}"/' crypto/opensslv.h

# Modify the various perl scripts to reference perl in the right location.
perl util/perlpath.pl `dirname %{__perl}`

# Generate a table with the compile settings for my perusal.
%if !0%{?os2_version}
touch Makefile
make TABLE PERL=%{__perl}
%endif

cp apps/openssl.cnf apps/openssl10.cnf

%build
# Figure out which flags we want to use.
# default
%if 0%{?os2_version}
sslarch=OS2-KNIX
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

# ia64, x86_64, ppc are OK by default
# Configure the build tree.  Override OpenSSL defaults with known-good defaults
# usable on all platforms.  The Configure script already knows to use -fPIC and
# RPM_OPT_FLAGS, so we can skip specifiying them here.

libs=-lcx
export CFLAGS="${CFLAGS:-%optflags}"
export VENDOR="%{vendor}"
export PERL="%{__perl}"

./Configure \
    --prefix=%{_prefix} --openssldir=%{_sysconfdir}/pki/tls ${sslflags} \
%if 0%{?os2_version}
    zlib enable-camellia enable-seed enable-tlsext enable-rfc3779 \
    experimental-jpake \
%else
    --system-ciphers-file=%{_sysconfdir}/crypto-policies/back-ends/openssl.config \
    zlib sctp enable-camellia enable-seed enable-tlsext enable-rfc3779 \
%endif
    enable-cms enable-md2 enable-rc5 \
    no-mdc2 no-ec2m no-gost no-srp no-krb5 \
%if 0%{?os2_version}
    shared  ${sslarch}
%else
    --enginesdir=%{_libdir}/openssl/engines \
    shared  ${sslarch} %{?!nofips:fips}
%endif

# Add -Wa,--noexecstack here so that libcrypto's assembler modules will be
# marked as not requiring an executable stack.
# Also add -DPURIFY to make using valgrind with openssl easier as we do not
# want to depend on the uninitialized memory as a source of entropy anyway.
%if !0%{?os2_version}
RPM_OPT_FLAGS="$RPM_OPT_FLAGS -Wa,--noexecstack -Wa,--generate-missing-build-notes=yes -DPURIFY"
%endif
make depend
make all

# Generate hashes for the included certs.
make rehash

# Clean up the .pc files
for i in libcrypto.pc libssl.pc openssl.pc ; do
  sed -i '/^Libs.private:/{s/-L[^ ]* //;s/-Wl[^ ]* //}' $i
done

%check
# Verify that what was compiled actually works.

%if !0%{?os2_version}
# We must revert patch33 before tests otherwise they will fail
patch -p1 -R < %{PATCH33}
cp apps/openssl.cnf apps/openssl10.cnf

LD_LIBRARY_PATH=`pwd`${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
export LD_LIBRARY_PATH
OPENSSL_ENABLE_MD5_VERIFY=
export OPENSSL_ENABLE_MD5_VERIFY
make -C test apps tests
%{__cc} -o openssl-thread-test \
    -I./include \
    $RPM_OPT_FLAGS \
    %{SOURCE8} \
    -L. \
    -lssl -lcrypto \
    -lpthread -lz -ldl
./openssl-thread-test --threads %{thread_test_threads}

# Add generation of HMAC checksum of the final stripped library
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
%if 0%{?os2_version}
install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_includedir}
install -d $RPM_BUILD_ROOT%{_libdir}
install -d $RPM_BUILD_ROOT%{_mandir}
install -d $RPM_BUILD_ROOT%{_libdir}/openssl
%else
install -d $RPM_BUILD_ROOT{%{_bindir},%{_includedir},%{_libdir},%{_mandir},%{_libdir}/openssl}
%endif
make INSTALL_PREFIX=$RPM_BUILD_ROOT install
%if !0%{?os2_version}
make INSTALL_PREFIX=$RPM_BUILD_ROOT install_docs
%else
cp ssl%{soversion}.dll $RPM_BUILD_ROOT%{_libdir}
cp crypto%{soversion}.dll $RPM_BUILD_ROOT%{_libdir}
# Remove duplicate DLLs with lib* prefix (todo: fix it in Makefiles)
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*%{soversion}.dll
%endif

mv $RPM_BUILD_ROOT%{_libdir}/engines $RPM_BUILD_ROOT%{_libdir}/openssl
mv $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/man/* $RPM_BUILD_ROOT%{_mandir}/
rmdir $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/man
%if !0%{?os2_version}
rename so.%{soversion} so.%{version} $RPM_BUILD_ROOT%{_libdir}/*.so.%{soversion}
for lib in $RPM_BUILD_ROOT%{_libdir}/*.so.%{version} ; do
    chmod 755 ${lib}
    ln -s -f `basename ${lib}` $RPM_BUILD_ROOT%{_libdir}/`basename ${lib} .%{version}`.%{soversion}
done
%endif

# Delete static library
rm -f $RPM_BUILD_ROOT%{_libdir}/*_s.a || :

# Rename man pages so that they don't conflict with other system man pages.
%if !0%{?os2_version}
pushd $RPM_BUILD_ROOT%{_mandir}
%else
pwd_save=`pwd`
cd $RPM_BUILD_ROOT%{_mandir}
%endif
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
popd
%else
cd $pwd_save
%endif

# Delete non-devel man pages in the compat package
%if !0%{?os2_version}
rm -rf $RPM_BUILD_ROOT%{_mandir}/man[157]*
%else
rm -rf $RPM_BUILD_ROOT%{_mandir}/man1*
rm -rf $RPM_BUILD_ROOT%{_mandir}/man5*
rm -rf $RPM_BUILD_ROOT%{_mandir}/man7*
%endif

# Delete configuration files
rm -rf  $RPM_BUILD_ROOT%{_sysconfdir}/pki/*

# Remove binaries
rm -rf $RPM_BUILD_ROOT/%{_bindir}

# Remove engines
rm -rf $RPM_BUILD_ROOT/%{_libdir}/openssl

# Install compat config file
%if 0%{?os2_version}
mkdir $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls
%endif
install -m 644 apps/openssl10.cnf $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/openssl10.cnf


%files
%license LICENSE
%doc FAQ NEWS README
%if !0%{?os2_version}
%doc README.FIPS
%doc README.legacy-settings
%endif

%attr(0755,root,root) %{_libdir}/crypto%{soversion}.dll
%attr(0755,root,root) %{_libdir}/ssl%{soversion}.dll

%if 0%{?os2_version}
%dir %{_sysconfdir}/pki/tls
%config(noreplace) %{_sysconfdir}/pki/tls/openssl10.cnf
%else
%dir %{_sysconfdir}/pki
%attr(0644,root,root) %{_sysconfdir}/pki/openssl10.cnf
%endif

%files devel
%doc doc/c-indentation.el doc/openssl.txt CHANGES
%{_prefix}/include/openssl
%attr(0755,root,root) %{_libdir}/lib*.a
%attr(0644,root,root) %{_mandir}/man3*/*
%attr(0644,root,root) %{_libdir}/pkgconfig/*.pc

%if !0%{?os2_version}
%ldconfig_scriptlets
%endif

%changelog
* Fri Sep 25 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> 1:1.0.2u-1
- Update to version 1.0.2u.
- rename to compat-openssl10, like fedora to have openssl1.1 in parallel
- adjusted the spec heavily

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
