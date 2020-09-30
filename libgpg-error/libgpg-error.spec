Name: libgpg-error
Version: 1.39
Release: 1%{?dist}
Summary: Library for error values used by GnuPG components
URL: https://www.gnupg.org/related_software/libgpg-error/
License: LGPLv2+

Vendor:		bww bitwise works GmbH
%scm_source     github https://github.com/bitwiseworks/%{name}-os2 %{name}-%{version}-os2

BuildRequires: gcc
BuildRequires: gawk, gettext, autoconf, automake, gettext-devel, libtool
BuildRequires: texinfo
BuildRequires: gettext-autopoint

%description
This is a library that defines common error values for all GnuPG
components.  Among these are GPG, GPGSM, GPGME, GPG-Agent, libgcrypt,
pinentry, SmartCard Daemon and possibly more in the future.

%package devel
Summary: Development files for the %{name} package
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
This is a library that defines common error values for all GnuPG
components.  Among these are GPG, GPGSM, GPGME, GPG-Agent, libgcrypt,
pinentry, SmartCard Daemon and possibly more in the future. This package
contains files necessary to develop applications using libgpg-error.

%debug_package

%prep
%scm_setup

autoreconf -fvi

# The config script already suppresses the -L if it's /usr/lib, so cheat and
# set it to a value which we know will be suppressed.
sed -i -e 's|^libdir=@libdir@$|libdir=@exec_prefix@/lib|g;s|@GPG_ERROR_CONFIG_HOST@|none|g' src/gpg-error-config.in
sed -i -e '/--variable=host/d' src/gpg-error-config-test.sh.in

# Modify configure to drop rpath for /usr/lib64
sed -i -e 's|sys_lib_dlsearch_path_spec="/lib /usr/lib|sys_lib_dlsearch_path_spec="/lib /usr/lib %{_libdir}|g' configure

%build
%if 0%{?os2_version}
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"
# Set BUILDLEVEL to be embedded to all DLLs built with Libtool.
export LT_BUILDLEVEL="@#%{vendor}:%{version}-%{release}#@##1## `LANG=C date +'%%d %%b %%Y %%H:%%M:%%S'`     `uname -n`::::0::"
%endif

%configure --disable-static --disable-rpath --disable-languages
make %{?_smp_mflags}

%install
%make_install
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT/%{_infodir}/dir

%find_lang %{name}

%check
export BEGINLIBPATH=%{_builddir}/%{buildsubdir}/src/.libs
make check

%if !0%{?os2_version}
%ldconfig_scriptlets
%endif

%files -f %{name}.lang
%license COPYING COPYING.LIB
%doc AUTHORS README NEWS
%if !0%{?os2_version}
%{_bindir}/gpg-error
%{_libdir}/libgpg-error.so.0*
%else
%{_bindir}/gpg-error.exe
%{_libdir}/gpg-err0.dll
%endif
%{_datadir}/libgpg-error

%files devel
%{_bindir}/gpg-error-config
%{_bindir}/gpgrt-config
%if !0%{?os2_version}
%{_bindir}/yat2m
%{_libdir}/libgpg-error.so
%else
%{_bindir}/yat2m.exe
%{_libdir}/gpg-error*_dll.a
%endif
%{_libdir}/pkgconfig/gpg-error.pc
%{_includedir}/gpg-error.h
%{_includedir}/gpgrt.h
%{_datadir}/aclocal/gpg-error.m4
%{_datadir}/aclocal/gpgrt.m4
%{_infodir}/gpgrt.info*
%{_mandir}/man1/gpgrt-config.*

%changelog
* Wed Sep 30 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.39-1
- update to version 1.39
- resync spec with fedora

* Wed Nov 23 2017 yd <yd@os2power.com> 1.28-2
- disable weak symbols for pthread, fixes pthread locking.

* Tue Nov 22 2017 yd <yd@os2power.com> 1.28-1
- first public rpm build.
