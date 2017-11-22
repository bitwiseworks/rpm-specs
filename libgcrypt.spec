# Note: this .spec is borrowed from https://src.fedoraproject.org/git/rpms/libgcrypt.git

Name: libgcrypt
Version: 1.9.0
Release: 1%{?dist}
URL: http://www.gnupg.org/

%define gcrylibdir %{_libdir}

# Technically LGPLv2.1+, but Fedora's table doesn't draw a distinction.
# Documentation and some utilities are GPLv2+ licensed. These files
# are in the devel subpackage.
License: LGPLv2+
Summary: A general-purpose cryptography library

Vendor:		bww bitwise works GmbH
%scm_source     github https://github.com/ydario/libgcrypt OS2-BRANCH
#scm_source git file://f:/rd/ports/keepassx/libgpg-error OS2-BRANCH

BuildRequires: gawk, libgpg-error-devel >= 1.11, pkgconfig
#BuildRequires: fipscheck
# This is needed only when patching the .texi doc.
#BuildRequires: texinfo
Group: System Environment/Libraries

%package devel
Summary: Development files for the %{name} package
License: LGPLv2+ and GPLv2+
Group: Development/Libraries
Requires: libgpg-error-devel
Requires: %{name} = %{version}-%{release}

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
libtoolize
autogen.sh --force

%build
%configure --disable-static \
     --disable-doc \
     --enable-pubkey-ciphers='dsa elgamal rsa ecc'
make %{?_smp_mflags}

%check

%install
make install DESTDIR=$RPM_BUILD_ROOT

# replace my_host with none.
sed -i -e 's,^my_host=".*"$,my_host="none",g' $RPM_BUILD_ROOT/%{_bindir}/libgcrypt-config

rm -f ${RPM_BUILD_ROOT}/%{_infodir}/dir ${RPM_BUILD_ROOT}/%{_libdir}/*.la

%files
%defattr(-,root,root,-)
#%dir /etc/gcrypt
#%config(noreplace) /etc/gcrypt/random.conf
%{gcrylibdir}/gcrypt*.dll
#%{gcrylibdir}/.libgcrypt.so.*.hmac
%{!?_licensedir:%global license %%doc}
%license COPYING.LIB
%doc AUTHORS NEWS THANKS

%files devel
%defattr(-,root,root,-)
%{_bindir}/%{name}-config
%{_bindir}/dumpsexp.exe
%{_bindir}/hmac256.exe
%{_bindir}/mpicalc.exe
%{_includedir}/*
%{_libdir}/*.a
%{_datadir}/aclocal/*
#%{_mandir}/man1/*
#%{_infodir}/gcrypt.info*
#%{!?_licensedir:%global license %%doc}
%license COPYING

%changelog
* Tue Nov 22 2017 yd <yd@os2power.com> 1.8.1-1
- first public rpm build.
