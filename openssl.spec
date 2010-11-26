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
%define soversion 10

# Number of threads to spawn when testing some threading fixes.
%define thread_test_threads %{?threads:%{threads}}%{!?threads:1}

# Arches on which we need to prevent arch conflicts on opensslconf.h, must
# also be handled in opensslconf-new.h.
%define multilib_arches %{ix86} ia64 ppc ppc64 s390 s390x sparcv9 sparc64 x86_64

Summary: A general purpose cryptography library with TLS implementation
Name: openssl
Version: 1.0.0a
Release: 2%{?dist}

Source: openssl-%{version}.tar.gz

# Build changes
Patch0: openssl-os2.diff
Patch1: openssl-os2-engines.diff

License: OpenSSL
Group: System Environment/Libraries
URL: http://www.openssl.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-root

#BuildRequires: mktemp, krb5-devel, perl, sed, zlib-devel, /usr/bin/cmp
BuildRequires: zlib-devel
#BuildRequires: /usr/bin/rename
#Requires: mktemp, ca-certificates >= 2008-5

%description
The OpenSSL toolkit provides support for secure communications between
machines. OpenSSL includes a certificate management tool and shared
libraries which provide various cryptographic algorithms and
protocols.

%package devel
Summary: Files for development of applications which will use OpenSSL
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}, zlib-devel
Requires: pkgconfig

%description devel
OpenSSL is a toolkit for supporting cryptography. The openssl-devel
package contains include files needed to develop applications which
support various cryptographic algorithms and protocols.

%package static
Summary:  Libraries for static linking of applications which will use OpenSSL
Group: Development/Libraries
Requires: %{name}-devel = %{version}-%{release}

%description static
OpenSSL is a toolkit for supporting cryptography. The openssl-static
package contains static libraries needed for static linking of
applications which support various cryptographic algorithms and
protocols.

%package perl
Summary: Perl scripts provided with OpenSSL
Group: Applications/Internet
Requires: perl
Requires: %{name} = %{version}-%{release}

%description perl
OpenSSL is a toolkit for supporting cryptography. The openssl-perl
package provides Perl scripts for converting certificates and keys
from other formats to the formats used by the OpenSSL toolkit.

%prep
%setup -q -n %{name}-%{version}

%patch0 -p1 -b .os2~
%patch1 -p1 -b .os2engines~

# Modify the various perl scripts to reference perl in the right location.
perl util/perlpath.pl `dirname %{__perl}`

# Generate a table with the compile settings for my perusal.
touch Makefile
make TABLE PERL=%{__perl}

%build
# Figure out which flags we want to use.
# default
sslarch=OS2-KNIX

# Configure the build tree.  Override OpenSSL defaults with known-good defaults
# usable on all platforms.  The Configure script already knows to use -fPIC and
# RPM_OPT_FLAGS, so we can skip specifiying them here.
export MAKESHELL="/bin/sh" ; \
export CFLAGS="${CFLAGS:-%optflags}" ; \
./Configure \
	--prefix=%{_usr} --openssldir=%{_sysconfdir}/pki/tls ${sslflags} \
	zlib enable-camellia enable-seed enable-tlsext enable-rfc3779 \
	enable-cms no-idea no-mdc2 no-rc5 no-ec no-ecdh no-ecdsa \
        no-krb5 \
	${sslarch} shared

# Add -Wa,--noexecstack here so that libcrypto's assembler modules will be
# marked as not requiring an executable stack.
#RPM_OPT_FLAGS="$RPM_OPT_FLAGS -Wa,--noexecstack"
make depend
# YD smp build not supported
make all

# Generate hashes for the included certs.
make rehash

# Overwrite FIPS README
#cp -f %{SOURCE11} .

%check
# Verify that what was compiled actually works.

# We must revert patch33 before tests otherwise they will fail
#patch -p1 -R < %{PATCH33}

#LD_LIBRARY_PATH=`pwd`${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
#export LD_LIBRARY_PATH
#make -C test apps tests
#%{__cc} -o openssl-thread-test \
#	`krb5-config --cflags` \
#	-I./include \
#	$RPM_OPT_FLAGS \
#	%{SOURCE8} \
#	-L. \
#	-lssl -lcrypto \
#	`krb5-config --libs` \
#	-lpthread -lz -ldl
#./openssl-thread-test --threads %{thread_test_threads}

# Add generation of HMAC checksum of the final stripped library
#%define __spec_install_post \
#    %{?__debug_package:%{__debug_install_post}} \
#    %{__arch_install_post} \
#    %{__os_install_post} \
#    crypto/fips/fips_standalone_sha1 $RPM_BUILD_ROOT/%{_lib}/libcrypto.so.%{version} >$RPM_BUILD_ROOT/%{_lib}/.libcrypto.so.%{version}.hmac \
#    ln -sf .libcrypto.so.%{version}.hmac $RPM_BUILD_ROOT/%{_lib}/.libcrypto.so.%{soversion}.hmac \
#    crypto/fips/fips_standalone_sha1 $RPM_BUILD_ROOT%{_libdir}/libssl.so.%{version} >$RPM_BUILD_ROOT%{_libdir}/.libssl.so.%{version}.hmac \
#    ln -sf .libssl.so.%{version}.hmac $RPM_BUILD_ROOT%{_libdir}/.libssl.so.%{soversion}.hmac \
#%{nil}

%install
export MAKESHELL="/bin/sh" 
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

# Install OpenSSL.
install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_includedir}
install -d $RPM_BUILD_ROOT%{_libdir}
install -d $RPM_BUILD_ROOT%{_mandir}
install -d $RPM_BUILD_ROOT%{_libdir}/openssl
make INSTALL_PREFIX=$RPM_BUILD_ROOT install
make INSTALL_PREFIX=$RPM_BUILD_ROOT install_docs

cp ssl_s.a $RPM_BUILD_ROOT%{_libdir}
cp ssl%{soversion}.dll $RPM_BUILD_ROOT%{_libdir}
cp crypto_s.a $RPM_BUILD_ROOT%{_libdir}
cp crypto%{soversion}.dll $RPM_BUILD_ROOT%{_libdir}

mv $RPM_BUILD_ROOT%{_libdir}/engines $RPM_BUILD_ROOT%{_libdir}/openssl
mv $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/man/* $RPM_BUILD_ROOT%{_mandir}/
rmdir $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/man

#rename so.%{soversion} so.%{version} $RPM_BUILD_ROOT%{_libdir}/*.so.%{soversion}
#mkdir $RPM_BUILD_ROOT/%{_lib}
#mv $RPM_BUILD_ROOT%{_libdir}/libcrypto.so.%{version} $RPM_BUILD_ROOT/%{_lib}
#for lib in $RPM_BUILD_ROOT%{_libdir}/*.so.%{version} ; do
#	chmod 755 ${lib}
#	ln -s -f `basename ${lib}` $RPM_BUILD_ROOT%{_libdir}/`basename ${lib} .%{version}`
#	ln -s -f `basename ${lib}` $RPM_BUILD_ROOT%{_libdir}/`basename ${lib} .%{version}`.%{soversion}
#done
#for lib in $RPM_BUILD_ROOT/%{_lib}/*.so.%{version} ; do
#	chmod 755 ${lib}
#	ln -s -f ../../%{_lib}/`basename ${lib}` $RPM_BUILD_ROOT%{_libdir}/`basename ${lib} .%{version}`
#	ln -s -f `basename ${lib}` $RPM_BUILD_ROOT/%{_lib}/`basename ${lib} .%{version}`.%{soversion}
#done

# Install a makefile for generating keys and self-signed certs, and a script
# for generating them on the fly.
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/certs
#install -m644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/certs/Makefile
#install -m755 %{SOURCE6} $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/certs/make-dummy-cert

# Make sure we actually include the headers we built against.
for header in $RPM_BUILD_ROOT%{_includedir}/openssl/* ; do
	if [ -f ${header} -a -f include/openssl/$(basename ${header}) ] ; then
		install -m644 include/openssl/`basename ${header}` ${header}
	fi
done

# Rename man pages so that they don't conflict with other system man pages.
#pushd $RPM_BUILD_ROOT%{_mandir}
for manpage in $RPM_BUILD_ROOT%{_mandir}/man*/* ; do
	if [ -L ${manpage} ]; then
		TARGET=`ls -l ${manpage} | awk '{ print $NF }'`
		ln -snf ${TARGET}ssl ${manpage}ssl
		rm -f ${manpage}
	else
		mv ${manpage} ${manpage}ssl
	fi
done
#for conflict in passwd rand ; do
#	rename ${conflict} ssl${conflict} man*/${conflict}*
#done
#popd

# Pick a CA script.
#pushd  $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/misc
mv $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/misc/CA.sh $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/misc/CA
#popd

mkdir -m755 $RPM_BUILD_ROOT%{_sysconfdir}/pki/CA
mkdir -m700 $RPM_BUILD_ROOT%{_sysconfdir}/pki/CA/private
mkdir -m755 $RPM_BUILD_ROOT%{_sysconfdir}/pki/CA/certs
mkdir -m755 $RPM_BUILD_ROOT%{_sysconfdir}/pki/CA/crl
mkdir -m755 $RPM_BUILD_ROOT%{_sysconfdir}/pki/CA/newcerts

# Ensure the openssl.cnf timestamp is identical across builds to avoid
# mulitlib conflicts and unnecessary renames on upgrade
#touch -r %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/openssl.cnf

# Determine which arch opensslconf.h is going to try to #include.
#basearch=i386
#%ifarch %{multilib_arches}
# Do an opensslconf.h switcheroo to avoid file conflicts on systems where you
# can have both a 32- and 64-bit version of the library, and they each need
# their own correct-but-different versions of opensslconf.h to be usable.
#install -m644 %{SOURCE10} \
#	$RPM_BUILD_ROOT/%{_prefix}/include/openssl/opensslconf-${basearch}.h
#cat $RPM_BUILD_ROOT/%{_prefix}/include/openssl/opensslconf.h >> \
#	$RPM_BUILD_ROOT/%{_prefix}/include/openssl/opensslconf-${basearch}.h
#install -m644 %{SOURCE9} \
#	$RPM_BUILD_ROOT/%{_prefix}/include/openssl/opensslconf.h
#%endif

# Remove unused files from upstream fips support
rm -rf $RPM_BUILD_ROOT/%{_bindir}/openssl_fips_fingerprint
rm -rf $RPM_BUILD_ROOT/%{_libdir}/fips_premain.*
rm -rf $RPM_BUILD_ROOT/%{_libdir}/fipscanister.*

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc FAQ LICENSE CHANGES NEWS INSTALL README
%doc doc/c-indentation.el doc/openssl.txt
%doc doc/openssl_button.html doc/openssl_button.gif
%doc doc/ssleay.txt
#%doc README.FIPS
%dir %{_sysconfdir}/pki/tls
%dir %{_sysconfdir}/pki/tls/certs
#%{_sysconfdir}/pki/tls/certs/make-dummy-cert
#%{_sysconfdir}/pki/tls/certs/Makefile
%dir %{_sysconfdir}/pki/tls/misc
%{_sysconfdir}/pki/tls/misc/CA
%dir %{_sysconfdir}/pki/CA
%dir %{_sysconfdir}/pki/CA/private
%dir %{_sysconfdir}/pki/CA/certs
%dir %{_sysconfdir}/pki/CA/crl
%dir %{_sysconfdir}/pki/CA/newcerts
%{_sysconfdir}/pki/tls/misc/c_*
%{_sysconfdir}/pki/tls/private

%config(noreplace) %{_sysconfdir}/pki/tls/openssl.cnf

%attr(0755,root,root) %{_bindir}/openssl.exe
%attr(0755,root,root) %{_libdir}/crypto%{soversion}.dll
%attr(0755,root,root) %{_libdir}/ssl%{soversion}.dll
#%attr(0644,root,root) /%{_lib}/.libcrypto.so.*.hmac
#%attr(0644,root,root) %{_libdir}/.libssl.so.*.hmac
%attr(0755,root,root) %{_libdir}/openssl
%attr(0644,root,root) %{_mandir}/man1*/[ABD-Zabcd-z]*
%attr(0644,root,root) %{_mandir}/man5*/*
%attr(0644,root,root) %{_mandir}/man7*/*

%files devel
%defattr(-,root,root)
%{_prefix}/include/openssl
%attr(0755,root,root) %{_libdir}/*%{soversion}.dll
%attr(0755,root,root) %{_libdir}/lib*.a
%attr(0644,root,root) %{_mandir}/man3*/*
%attr(0644,root,root) %{_libdir}/pkgconfig/*.pc

%files static
%defattr(-,root,root)
%attr(0644,root,root) %{_libdir}/*_s.a

%files perl
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/c_rehash
%attr(0644,root,root) %{_mandir}/man1*/*.pl*
%{_sysconfdir}/pki/tls/misc/*.pl
%{_sysconfdir}/pki/tls/misc/tsget

#%post -p /sbin/ldconfig

#%postun -p /sbin/ldconfig

%changelog
