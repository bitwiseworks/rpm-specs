Summary: CMS and X.509 library
Name:    libksba
Version: 1.4.0
Release: 1%{?dist}

# The library is licensed under LGPLv3+ or GPLv2+,
# the rest of the package under GPLv3+
License: (LGPLv3+ or GPLv2+) and GPLv3+
URL:     http://www.gnupg.org/
%if !0%{?os2_version}
Source0: ftp://ftp.gnupg.org/gcrypt/libksba/libksba-%{version}.tar.bz2
Source1: ftp://ftp.gnupg.org/gcrypt/libksba/libksba-%{version}.tar.bz2.sig

Patch1: libksba-1.3.0-multilib.patch
%else
Vendor:  bww bitwise works GmbH
%scm_source    github https://github.com/bitwiseworks/%{name}-os2 %{name}-%{version}-os2
%endif

BuildRequires: gcc
BuildRequires: gawk
BuildRequires: libgpg-error-devel >= 1.8
BuildRequires: libgcrypt-devel >= 1.2.0

%description
KSBA (pronounced Kasbah) is a library to make X.509 certificates as
well as the CMS easily accessible by other applications.  Both
specifications are building blocks of S/MIME and TLS.

%package devel
Summary: Development headers and libraries for %{name}
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
%{summary}.

%debug_package

%prep
%if !0%{?os2_version}
%setup -q
%else
%scm_setup
%endif

%if !0%{?os2_version}
%patch1 -p1 -b .multilib
%else
autoreconf -fvi
%endif

# Convert to utf-8
for file in THANKS; do
    iconv -f ISO-8859-1 -t UTF-8 -o $file.new $file && \
    touch -r $file $file.new && \
    mv $file.new $file
done

%build
%if 0%{?os2_version}
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"
# Set BUILDLEVEL to be embedded to all DLLs built with Libtool.
export LT_BUILDLEVEL="@#%{vendor}:%{version}-%{release}#@##1## `LANG=C date +'%%d %%b %%Y %%H:%%M:%%S'`     `uname -n`::::0::"
%endif

%configure \
  --disable-dependency-tracking \
  --disable-static

%if !0%{?os2_version}
%make_build
%else
make %{?_smp_mflags}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%make_install

rm -f $RPM_BUILD_ROOT%{_infodir}/dir
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.la


%check
%if 0%{?os2_version}
export BEGINLIBPATH=%{_builddir}/%{buildsubdir}/src/.libs
%endif
make check


%if !0%{?os2_version}
%ldconfig_scriptlets
%endif

%files
%license COPYING COPYING.GPLv2 COPYING.GPLv3 COPYING.LGPLv3
%doc AUTHORS ChangeLog NEWS README* THANKS TODO
%if !0%{?os2_version}
%{_libdir}/libksba.so.8*
%else
%{_libdir}/ksba*.dll
%endif

%files devel
%{_bindir}/ksba-config
%if !0%{?os2_version}
%{_libdir}/libksba.so
%else
%{_libdir}/*_dll.a
%endif
%{_includedir}/ksba.h
%{_datadir}/aclocal/ksba.m4
%{_libdir}/pkgconfig/ksba.pc
%{_infodir}/ksba.info*


%changelog
* Mon Oct 26 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.4.0-1
- first OS/2 rpm
