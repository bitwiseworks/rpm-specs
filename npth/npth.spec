Name:           npth
Version:        1.6
Release:        1%{?dist}
Summary:        The New GNU Portable Threads library
License:        LGPLv2+
URL:            https://git.gnupg.org/cgi-bin/gitweb.cgi?p=npth.git
%if !0%{?os2_version}
Source:         https://gnupg.org/ftp/gcrypt/npth/%{name}-%{version}.tar.bz2
#Source1:        ftp://ftp.gnupg.org/gcrypt/npth/npth-%{version}.tar.bz2.sig
# Manual page is re-used and changed pth-config.1 from pth-devel package
Source2:        npth-config.1
%else
Vendor:  bww bitwise works GmbH
%scm_source    github https://github.com/bitwiseworks/%{name}-os2 %{name}-%{version}-os2
%endif

BuildRequires:  make
BuildRequires:  gcc

%description
nPth is a non-preemptive threads implementation using an API very similar
to the one known from GNU Pth. It has been designed as a replacement of
GNU Pth for non-ancient operating systems. In contrast to GNU Pth is is
based on the system's standard threads implementation. Thus nPth allows
the use of libraries which are not compatible to GNU Pth.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
This package contains libraries and header files for
developing applications that use %{name}.

%debug_package

%prep
%if !0%{?os2_version}
%autosetup
%else
%scm_setup
autoreconf -fvi
%endif

%build
%if 0%{?os2_version}
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"
# Set BUILDLEVEL to be embedded to all DLLs built with Libtool.
export LT_BUILDLEVEL="@#%{vendor}:%{version}-%{release}#@##1## `LANG=C date +'%%d %%b %%Y %%H:%%M:%%S'`     `uname -n`::::0::"
%endif

%configure --disable-static
%if !0%{?os2_version}
%make_build
%else
make %{?_smp_mflags}
%endif

%install
%make_install
%if !0%{?os2_version}
install -Dpm0644 -t %{buildroot}%{_mandir}/man1 %{S:2}
%endif
find %{buildroot} -name '*.la' -delete -print

%check
%if 0%{?os2_version}
export BEGINLIBPATH=%{_builddir}/%{buildsubdir}/src/.libs
%endif
make check

%if !0%{?os2_version}
%ldconfig_scriptlets
%endif

%files
%license COPYING.LIB
%if !0%{?os2_version}
%{_libdir}/lib%{name}.so.*
%else
%{_libdir}/*.dll
%endif

%files devel
%doc AUTHORS ChangeLog NEWS README
%{_bindir}/%{name}-config
%if !0%{?os2_version}
%{_libdir}/lib%{name}.so
%else
%{_libdir}/*_dll.a
%endif
%{_includedir}/%{name}.h
%if !0%{?os2_version}
%{_mandir}/man1/%{name}-config.1*
%endif
%{_datadir}/aclocal/%{name}.m4

%changelog
* Mon Oct 26 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.6-1
- first OS/2 rpm
