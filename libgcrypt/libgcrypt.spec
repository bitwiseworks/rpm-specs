Name: libgcrypt
Version: 1.8.6
Release: 1%{?dist}
URL: http://www.gnupg.org/

%global gcrylibdir %{_libdir}
%global gcrysoname libgcrypt.so.20
%global hmackey orboDeJITITejsirpADONivirpUkvarP

# Technically LGPLv2.1+, but Fedora's table doesn't draw a distinction.
# Documentation and some utilities are GPLv2+ licensed. These files
# are in the devel subpackage.
License: LGPLv2+
Summary: A general-purpose cryptography library

Vendor:  bww bitwise works GmbH
%scm_source    github https://github.com/bitwiseworks/%{name}-os2 %{name}-%{version}-os2

BuildRequires: gcc
BuildRequires: gawk, libgpg-error-devel >= 1.11, pkgconfig
# This is needed only when patching the .texi doc.
BuildRequires: texinfo
BuildRequires: transfig
BuildRequires: autoconf, automake, libtool

%package devel
Summary: Development files for the %{name} package
License: LGPLv2+ and GPLv2+
Requires: libgpg-error-devel
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description
Libgcrypt is a general purpose crypto library based on the code used
in GNU Privacy Guard.  This is a development version.

%description devel
Libgcrypt is a general purpose crypto library based on the code used
in GNU Privacy Guard.  This package contains files needed to develop
applications using libgcrypt.

%debug_package

%prep
%scm_setup

%build
# This package has a configure test which uses ASMs, but does not link the
# resultant .o files.  As such the ASM test is always successful, even on
# architectures were the ASM is not valid when compiling with LTO.
#
# -ffat-lto-objects is sufficient to address this issue.  It is the default
# for F33, but is expected to only be enabled for packages that need it in
# F34, so we use it here explicitly
%define _lto_cflags -flto=auto -ffat-lto-objects

autoreconf -fvi

%if 0%{?os2_version}
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"
# Set BUILDLEVEL to be embedded to all DLLs built with Libtool.
export LT_BUILDLEVEL="@#%{vendor}:%{version}-%{release}#@##1## `LANG=C date +'%%d %%b %%Y %%H:%%M:%%S'`     `uname -n`::::0::"
%endif

%configure --disable-static \
%ifarch sparc64
     --disable-asm \
%endif
     --enable-noexecstack \
%if !0%{?os2_version}
     --enable-hmac-binary-check \
%endif
     --enable-pubkey-ciphers='dsa elgamal rsa ecc' \
     --disable-O-flag-munging
sed -i -e '/^sys_lib_dlsearch_path_spec/s,/lib /usr/lib,/usr/lib /lib64 /usr/lib64 /lib,g' libtool
make %{?_smp_mflags}

%check
%if !0%{?os2_version}
src/hmac256 %{hmackey} src/.libs/%{gcrysoname} | cut -f1 -d ' ' >src/.libs/.%{gcrysoname}.hmac
%else
export BEGINLIBPATH=%{_builddir}/%{buildsubdir}/src/.libs
%endif

make check

# Add generation of HMAC checksums of the final stripped binaries 
%if !0%{?os2_version}
%define __spec_install_post \
    %{?__debug_package:%{__debug_install_post}} \
    %{__arch_install_post} \
    %{__os_install_post} \
    src/hmac256 %{hmackey} $RPM_BUILD_ROOT%{gcrylibdir}/%{gcrysoname} | cut -f1 -d ' ' >$RPM_BUILD_ROOT%{gcrylibdir}/.%{gcrysoname}.hmac \
%{nil}
%endif

%install
%make_install

# Change /usr/lib64 back to /usr/lib.  This saves us from having to patch the
# script to "know" that -L/usr/lib64 should be suppressed, and also removes
# a file conflict between 32- and 64-bit versions of this package.
# Also replace my_host with none.
%if !0%{?os2_version}
sed -i -e 's,^libdir="/usr/lib.*"$,libdir="/usr/lib",g' $RPM_BUILD_ROOT/%{_bindir}/libgcrypt-config
%endif
sed -i -e 's,^my_host=".*"$,my_host="none",g' $RPM_BUILD_ROOT/%{_bindir}/libgcrypt-config

rm -f ${RPM_BUILD_ROOT}/%{_infodir}/dir ${RPM_BUILD_ROOT}/%{_libdir}/*.la
%if !0%{?os2_version}
/sbin/ldconfig -n $RPM_BUILD_ROOT/%{_libdir}

%if "%{gcrylibdir}" != "%{_libdir}"
# Relocate the shared libraries to %{gcrylibdir}.
mkdir -p $RPM_BUILD_ROOT%{gcrylibdir}
for shlib in $RPM_BUILD_ROOT%{_libdir}/*.so* ; do
	if test -L "$shlib" ; then
		rm "$shlib"
	else
		mv "$shlib" $RPM_BUILD_ROOT%{gcrylibdir}/
	fi
done

# Add soname symlink.
/sbin/ldconfig -n $RPM_BUILD_ROOT/%{_lib}/
%endif

# Overwrite development symlinks.
pushd $RPM_BUILD_ROOT/%{gcrylibdir}
for shlib in lib*.so.?? ; do
	target=$RPM_BUILD_ROOT/%{_libdir}/`echo "$shlib" | sed -e 's,\.so.*,,g'`.so
%if "%{gcrylibdir}" != "%{_libdir}"
	shlib=%{gcrylibdir}/$shlib
%endif
	ln -sf $shlib $target
done
popd

# Create /etc/gcrypt (hardwired, not dependent on the configure invocation) so
# that _someone_ owns it.
mkdir -p -m 755 $RPM_BUILD_ROOT/etc/gcrypt
install -m644 %{SOURCE7} $RPM_BUILD_ROOT/etc/gcrypt/random.conf

%ldconfig_scriptlets
%endif

%files
%if !0%{?os2_version}
%dir /etc/gcrypt
%config(noreplace) /etc/gcrypt/random.conf
%{gcrylibdir}/libgcrypt.so.*.*
%{gcrylibdir}/%{gcrysoname}
%{gcrylibdir}/.%{gcrysoname}.hmac
%else
%{gcrylibdir}/gcrypt*.dll
%endif
%{!?_licensedir:%global license %%doc}
%license COPYING.LIB
%doc AUTHORS NEWS THANKS

%files devel
%{_bindir}/%{name}-config
%if !0%{?os2_version}
%{_bindir}/dumpsexp
%{_bindir}/hmac256
%{_bindir}/mpicalc
%else
%{_bindir}/dumpsexp.exe
%{_bindir}/hmac256.exe
%{_bindir}/mpicalc.exe
%endif
%{_includedir}/*
%if !0%{?os2_version}
%{_libdir}/*.so
%else
%{_libdir}/*_dll.a
%endif
%{_libdir}/pkgconfig/libgcrypt.pc
%{_datadir}/aclocal/*
%{_mandir}/man1/*

%{_infodir}/gcrypt.info*
%{!?_licensedir:%global license %%doc}
%license COPYING

%changelog
* Wed Sep 30 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.8.6-1
- update to version 1.8.6
- resync spec with fedora

* Wed Nov 22 2017 yd <yd@os2power.com> 1.8.1-1
- first public rpm build.
