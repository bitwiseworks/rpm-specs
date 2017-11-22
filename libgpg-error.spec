# Note: this .spec is borrowed from https://src.fedoraproject.org/git/rpms/libgpg-error.git

Summary: Library for error values used by GnuPG components
Name: libgpg-error
Version: 1.28
Release: 1%{?dist}
URL: https://www.gnupg.org/related_software/libgpg-error/
Group: System Environment/Libraries
License: LGPLv2+

Vendor:		bww bitwise works GmbH
%scm_source     github https://github.com/ydario/libgpg-error master-os2
#scm_source git file://f:/rd/ports/keepassx/libgpg-error master-os2

BuildRequires: gawk, gettext, autoconf, automake, gettext-devel, libtool
#BuildRequires: texinfo
%if 0%{?fedora} > 13
BuildRequires: gettext-autopoint
%endif

%description
This is a library that defines common error values for all GnuPG
components.  Among these are GPG, GPGSM, GPGME, GPG-Agent, libgcrypt,
pinentry, SmartCard Daemon and possibly more in the future.

%package devel
Summary: Development files for the %{name} package
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
This is a library that defines common error values for all GnuPG
components.  Among these are GPG, GPGSM, GPGME, GPG-Agent, libgcrypt,
pinentry, SmartCard Daemon and possibly more in the future. This package
contains files necessary to develop applications using libgpg-error.

%debug_package

%prep
%scm_setup
libtoolize
autogen.sh --force

%build
%configure \
	--disable-static --disable-rpath --disable-languages \
	--disable-doc --disable-tests
make %{?_smp_mflags}

%install
rm -fr $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT/%{_infodir}/dir

%find_lang %{name}

%check
make check

%clean
rm -fr $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root)
%{!?_licensedir:%global license %%doc}
%license COPYING COPYING.LIB
%doc AUTHORS README NEWS ChangeLog
%{_bindir}/gpg-error.exe
%{_libdir}/gpg-err0.dll
#%{_datadir}/libgpg-error

%files devel
%defattr(-,root,root)
%{_bindir}/gpg-error-config
%{_libdir}/gpg-error*.a
%{_includedir}/gpg-error.h
%{_includedir}/gpgrt.h
%{_datadir}/aclocal/gpg-error.m4
#%{_infodir}/gpgrt.info*
#%{_mandir}/man1/gpg-error-config.*

%changelog
* Tue Nov 22 2017 yd <yd@os2power.com> 1.28-1
- first public rpm build.
