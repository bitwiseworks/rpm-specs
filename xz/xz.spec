# Not needed for f21+ and probably RHEL8+
%{!?_licensedir:%global license %%doc}

Summary:	LZMA compression utilities
Name:		xz
Version:	5.2.3
Release:	3%{?dist}

# Scripts xz{grep,diff,less,more} and symlinks (copied from gzip) are
# GPLv2+, binaries are Public Domain (linked against LGPL getopt_long but its
# OK), documentation is Public Domain.
License:	GPLv2+ and Public Domain
%if !0%{?os2_version}
# official upstream release
Source0:	https://tukaani.org/%{name}/%{name}-%{version}.tar.xz

Source100:	colorxzgrep.sh
Source101:	colorxzgrep.csh

Patch1:   xz-5.2.5-enable_CET.patch
%else
Vendor:		bww bitwise works GmbH
%scm_source	github https://github.com/bitwiseworks/%{name}-os2 v%{version}-os2
%endif

URL:		https://tukaani.org/%{name}/
Requires:	%{name}-libs = %{version}-%{release}

# For /usr/libexec/grepconf.sh (RHBZ#1189120).
# Unfortunately F21 has a newer version of grep which doesn't
# have grepconf, but we're only concerned with F22 here.
Requires:	grep >= 2.20-5

BuildRequires:  make
BuildRequires:	gcc
%if !0%{?os2_version}
BuildRequires:	perl-interpreter
%else
BuildRequires:	perl
%endif

%description
XZ Utils are an attempt to make LZMA compression easy to use on free (as in
freedom) operating systems. This is achieved by providing tools and libraries
which are similar to use than the equivalents of the most popular existing
compression algorithms.

LZMA is a general purpose compression algorithm designed by Igor Pavlov as
part of 7-Zip. It provides high compression ratio while keeping the
decompression speed fast.


%package 	libs
Summary:	Libraries for decoding LZMA compression
License:	Public Domain
Obsoletes:	%{name}-compat-libs < %{version}-%{release}

%description 	libs
Libraries for decoding files compressed with LZMA or XZ utils.


%package 	static
Summary:	Statically linked library for decoding LZMA compression
License:	Public Domain

%description 	static
Statically linked library for decoding files compressed with LZMA or
XZ utils.  Most users should *not* install this.


%package 	devel
Summary:	Devel libraries & headers for liblzma
License:	Public Domain
Requires:	%{name}-libs = %{version}-%{release}

%description	devel
Devel libraries and headers for liblzma.


%package 	lzma-compat
Summary:	Older LZMA format compatibility binaries
# Just a set of symlinks to 'xz' + two Public Domain binaries.
License:	Public Domain
Requires:	%{name} = %{version}-%{release}
Obsoletes:	lzma < %{version}
Provides:	lzma = %{version}

%description	lzma-compat
The lzma-compat package contains compatibility links for older
commands that deal with the older LZMA format.

%if 0%{?os2_version}
%legacy_runtime_packages
%debug_package
%endif

%prep
%if !0%{?os2_version}
%autosetup -p1
%else
%scm_setup
autoreconf -fvi
%endif


%build
%if !0%{?os2_version}
export CFLAGS="%optflags"

%ifarch %ix86
  # rhbz#1630650, annocheck reports the following message because liblzma uses
  # crc*_x86.S asm code on i686:
  CFLAGS="$CFLAGS -Wa,--generate-missing-build-notes=yes"
%endif
%else
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx -lpthread"
export VENDOR="%{vendor}"
%endif

%configure
%if !0%{?os2_version}
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%make_build
%else
make %{?_smp_mflags}
%endif


%install
%make_install
rm -f %{buildroot}%{_libdir}/*.la

%if !0%{?os2_version}
# xzgrep colorization
%global profiledir %{_sysconfdir}/profile.d
mkdir -p %{buildroot}%{profiledir}
install -p -m 644 %{SOURCE100} %{buildroot}%{profiledir}
install -p -m 644 %{SOURCE101} %{buildroot}%{profiledir}
%endif

%find_lang %name


%check
%if !0%{?os2_version}
LD_LIBRARY_PATH=$PWD/src/liblzma/.libs make check
%endif

%if !0%{?os2_version}
%ldconfig_scriptlets libs
%endif


%files -f %{name}.lang
%license COPYING*
%if !0%{?os2_version}
%doc %{_pkgdocdir}
%exclude %_pkgdocdir/examples*
%else
%doc %{_docdir}/xz
%exclude %_docdir/xz/examples*
%endif
%{_bindir}/*xz*
%if 0%{?os2_version}
%exclude %{_bindir}/*.dbg
%endif
%{_mandir}/man1/*xz*
%if !0%{?os2_version}
%{_mandir}/de/man1/*xz*
%{profiledir}/*
%endif


%files libs
%license COPYING
%if !0%{?os2_version}
%{_libdir}/lib*.so.5*
%else
%{_libdir}/*.dll
%exclude %{_libdir}/lzma.dll
%endif


%files static
%license COPYING
%if !0%{?os2_version}
%{_libdir}/liblzma.a
%else
%{_libdir}/lzma.a
%endif


%files devel
%dir %{_includedir}/lzma
%{_includedir}/lzma/*.h
%{_includedir}/lzma.h
%if !0%{?os2_version}
%{_libdir}/*.so
%else
%{_libdir}/*_dll.a
%endif
%{_libdir}/pkgconfig/liblzma.pc
%if !0%{?os2_version}
%doc %_pkgdocdir/examples*
%else
%doc %_docdir/xz/examples*
%endif


%files lzma-compat
%{_bindir}/*lz*
%if 0%{?os2_version}
%exclude %{_bindir}/*.dbg
%endif
%{_mandir}/man1/*lz*
%if !0%{?os2_version}
%{_mandir}/de/man1/*lz*
%endif


%changelog
* Mon Jan 17 2022 Silvan Scherrer <silvan.scherrer@aroa.ch> 5.2.3-3
- resync with fedora spec
- moved source to github
- added static part

* Tue Feb 14 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 5.2.3-2
- rebuild with changed legacy_runtime_packages macro

* Wed Feb 08 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 5.2.3-1
- update to version 5.2.3
- use the new scm_source and scm_setup macros
- don't use a forwarder, use the legacy script

* Fri Nov 25 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> 5.2.2-1
- update to version 5.2.2

* Mon Jun 13 2016 yd <yd@os2power.com> 4.999.9beta-5
- rebuild package, fixes ticket#183.
- added debug package.
