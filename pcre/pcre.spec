# Is this a stable/testing release:
#%%global rcversion RC1
Name:       pcre
Version:    8.45
Release:    %{?rcversion:0.}1%{?rcversion:.%rcversion}%{?dist}.1
%global myversion %{version}%{?rcversion:-%rcversion}
Summary:    Perl-compatible regular expression library
## Source package only:
# INSTALL:                  FSFAP
# install-sh:               MIT and Public Domain
# ltmain.sh:                (GPLv2+ or BSD) and (GPLv3+ or MIT)
# missing:                  GPLv2+ or BSD
# compile:                  GPLv2+ or BSD
# config.sub:               GPLv3+ or BSD
# m4/ax_pthread.m4:         GPLv3+ with exception
# m4/libtool.m4:            GPLv2+ or BSD
# m4/ltversion.m4:          FSFULLR
# m4/pcre_visibility.m4:    FSFULLR
# m4/lt~obsolete.m4:        FSFULLR
# m4/ltsugar.m4:            FSFULLR
# m4/ltoptions.m4:          FSFULLR
# aclocal.m4:               (GPLv2+ or BSD) and FSFULLR 
# Makefile.in:              FSFULLR
# configure:                FSFUL
# test-driver:              GPLv2+ with exception
# testdata:                 Public Domain (see LICENSE file)
## Binary packages:
# other files:              BSD
License:    BSD
URL:        https://www.pcre.org/
%if !0%{?os2_version}
Source0:    https://ftp.pcre.org/pub/%{name}/%{?rcversion:Testing/}%{name}-%{myversion}.tar.bz2
Source1:    https://ftp.pcre.org/pub/%{name}/%{?rcversion:Testing/}%{name}-%{myversion}.tar.bz2.sig
Source2:    https://ftp.pcre.org/pub/pcre/Public-Key
# Do no set RPATH if libdir is not /usr/lib
Patch0:     pcre-8.21-multilib.patch
# Refused by upstream, bug #675477
Patch1:     pcre-8.32-refused_spelling_terminated.patch
# Fix recursion stack estimator, upstream bug #2173, refused by upstream
Patch2:     pcre-8.41-fix_stack_estimator.patch
# Link applications to PCRE-specific symbols when using POSIX API, bug #1667614,
# upstream bug 1830, partially borrowed from PCRE2, proposed to upstream,
# This amends ABI, application built with this patch cannot run with
# previous libpcreposix builds.
Patch3:     pcre-8.42-Declare-POSIX-regex-function-names-as-macros-to-PCRE.patch
# Fix reading an uninitialized memory when populating a name table,
# upstream bug #2661, proposed to the upstream
Patch4:     pcre-8.44-Inicialize-name-table-memory-region.patch
# Implement CET, bug #1909554, proposed to the upstream
# <https://lists.exim.org/lurker/message/20201220.222016.d8cd6d61.en.html>
Patch5:     pcre-8.44-JIT-compiler-update-for-Intel-CET.patch
Patch6:     pcre-8.44-Pass-mshstk-to-the-compiler-when-Intel-CET-is-enable.patch
%else
Vendor:         bww bitwise works GmbH
%scm_source     github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2
%endif
BuildRequires:  readline-devel
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  coreutils
BuildRequires:  gcc
BuildRequires:  gcc-c++
%if !0%{?os2_version}
# glibc-common for iconv
BuildRequires:  glibc-common
BuildRequires:  gnupg2
%endif
BuildRequires:  libtool
BuildRequires:  make
# perl not used because config.h.generic is pregenerated
# Tests:
BuildRequires:  bash
BuildRequires:  diffutils
BuildRequires:  grep

%description
PCRE, Perl-compatible regular expression, library has its own native API, but
a set of wrapper functions that are based on the POSIX API are also supplied
in the libpcreposix library. Note that this just provides a POSIX calling
interface to PCRE: the regular expressions themselves still follow Perl syntax
and semantics. This package provides support for strings in 8-bit and UTF-8
encodings. Detailed change log is provided by %{name}-doc package.

%package utf16
Summary:    UTF-16 variant of PCRE
%if !0%{?os2_version}
Conflicts:  %{name} < 8.38-12
%endif

%description utf16
This is Perl-compatible regular expression library working on UTF-16 strings.
Detailed change log is provided by %{name}-doc package.

%package utf32
Summary:    UTF-32 variant of PCRE
%if !0%{?os2_version}
Conflicts:  %{name} < 8.38-12
%endif

%description utf32
This is Perl-compatible regular expression library working on UTF-32 strings.
Detailed change log is provided by %{name}-doc package.

%package cpp
Summary:    C++ bindings for PCRE
Requires:   %{name} = %{version}-%{release}

%description cpp
This is C++ bindings for the Perl-compatible regular expression library.
Detailed change log is provided by %{name}-doc package.

%package doc
Summary:    Change log for %{name}
BuildArch:  noarch

%description doc
These are large documentation files about PCRE.

%package devel
Summary:    Development files for %{name}
Requires:   %{name} = %{version}-%{release}
Requires:   %{name}-cpp = %{version}-%{release}
Requires:   %{name}-utf16 = %{version}-%{release}
Requires:   %{name}-utf32 = %{version}-%{release}

%description devel
Development files (Headers, libraries for dynamic linking, etc) for %{name}.

%package static
Summary:    Static library for %{name}
Requires:   %{name}-devel%{_isa} = %{version}-%{release}

%description static
Library for static linking for %{name}.

%package tools
Summary:    Auxiliary utilities for %{name}
Requires:   %{name} = %{version}-%{release}

%description tools
Utilities demonstrating PCRE capabilities like pcregrep or pcretest.

%if 0%{?os2_version}
%legacy_runtime_packages

%debug_package
%endif

%prep
%if !0%{?os2_version}
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%setup -q -n %{name}-%{myversion}
%patch0 -p1
%patch1 -p1
%patch2 -p2
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
# Because of the multilib patch
libtoolize --copy --force
%else
%scm_setup
%endif
autoreconf -vif
%if !0%{?os2_version}
# One contributor's name is non-UTF-8
for F in ChangeLog; do
    iconv -f latin1 -t utf8 "$F" >"${F}.utf8"
    touch --reference "$F" "${F}.utf8"
    mv "${F}.utf8" "$F"
done
%endif

%build
%if 0%{?os2_version}
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"
export LIBS='-lcx -lpthread'
# Set BUILDLEVEL to be embedded to all DLLs built with Libtool.
export LT_BUILDLEVEL="@#%{vendor}:%{version}-%{release}#@##1## `LANG=C date +'%%d %%b %%Y %%H:%%M:%%S'`     `uname -n`::::0::"
%endif
# There is a strict-aliasing problem on PPC64, bug #881232
%ifarch ppc64
%global optflags %{optflags} -fno-strict-aliasing
%endif
%configure \
%if !0%{?os2_version}
%ifarch s390 s390x sparc64 sparcv9 riscv64
    --disable-jit \
%else
    --enable-jit \
%endif
%endif
    --enable-pcretest-libreadline \
    --enable-utf \
    --enable-unicode-properties \
    --enable-pcre8 \
    --enable-pcre16 \
    --enable-pcre32 \
%if 0%{?os2_version}
    --enable-stack-for-recursion=no \
    --enable-newline-is-any \
%endif
    --disable-silent-rules
make %{?_smp_mflags}

%install
%{make_install}
# Get rid of unneeded *.la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
# These are handled by %%doc in %%files
rm -rf $RPM_BUILD_ROOT%{_docdir}/pcre

%check
%ifarch s390 s390x ppc
# larger stack is needed on s390, ppc
ulimit -s 10240
%endif
%if !0%{?os2_version}
make %{?_smp_mflags} check VERBOSE=yes
%endif

%files
%if !0%{?os2_version}
%{_libdir}/libpcre.so.1
%{_libdir}/libpcre.so.1.*
%{_libdir}/libpcreposix.so.0
%{_libdir}/libpcreposix.so.0.*
%else
%{_libdir}/pcre1.dll
%{_libdir}/pcrepos0.dll
%endif
%license COPYING LICENCE
%doc AUTHORS NEWS

%files utf16
%if !0%{?os2_version}
%{_libdir}/libpcre16.so.0
%{_libdir}/libpcre16.so.0.*
%else
%{_libdir}/pcre160.dll
%endif
%license COPYING LICENCE
%doc AUTHORS NEWS

%files utf32
%if !0%{?os2_version}
%{_libdir}/libpcre32.so.0
%{_libdir}/libpcre32.so.0.*
%else
%{_libdir}/pcre320.dll
%endif
%license COPYING LICENCE
%doc AUTHORS NEWS

%files cpp
%if !0%{?os2_version}
%{_libdir}/libpcrecpp.so.0
%{_libdir}/libpcrecpp.so.0.*
%else
%{_libdir}/pcrecpp0.dll
%endif

%files doc
%doc ChangeLog

%files devel
%if !0%{?os2_version}
%{_libdir}/*.so
%else
%{_libdir}/*_dll.a
%endif
%{_libdir}/pkgconfig/*
%{_includedir}/*.h
%{_mandir}/man1/pcre-config.*
%{_mandir}/man3/*
%{_bindir}/pcre-config
%doc doc/*.txt doc/html
%doc README HACKING pcredemo.c

%files static
%{_libdir}/*.a
%if 0%{?os2_version}
%exclude %{_libdir}/*_dll.a
%endif
%license COPYING LICENCE

%files tools
%if !0%{?os2_version}
%{_bindir}/pcregrep
%{_bindir}/pcretest
%else
%{_bindir}/pcregrep.exe
%{_bindir}/pcretest.exe
%endif
%{_mandir}/man1/pcregrep.*
%{_mandir}/man1/pcretest.*

%changelog
* Fri Aug 03 2021 Silvan Scherrer <silvan.scherrer@aroa.ch> - 8.45-1.1
- update to version 8.45

* Thu Apr 08 2021 Silvan Scherrer <silvan.scherrer@aroa.ch> - 8.44-2.1
- disable a conflict, as this clashes with the old legacy package

* Fri Apr 02 2021 Silvan Scherrer <silvan.scherrer@aroa.ch> - 8.44-1.1
- update to version 8.44
- resync with fedora spec