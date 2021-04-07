# Add readline edditing in pcre2test tool
%bcond_without pcre2_enables_readline

# Disable SELinux-frindly JIT allocator because it seems not to be fork-safe,
# https://bugs.exim.org/show_bug.cgi?id=1749#c45
%bcond_with pcre2_enables_sealloc

# This is stable release:
#%%global rcversion RC1
Name:       pcre2
Version:    10.36
Release:    %{?rcversion:0.}1%{?rcversion:.%rcversion}%{?dist}
%global     myversion %{version}%{?rcversion:-%rcversion}
Summary:    Perl-compatible regular expression library
# the library:                          BSD with exceptions
# pcre2test (linked to GNU readline):   BSD (linked to GPLv3+)
# COPYING:                              see LICENCE file
# LICENSE:                              BSD text with exceptions and
#                                       Public Domain declaration
#                                       for testdata
#Bundled
# src/sljit:                            BSD
#Not distributed in any binary package
# aclocal.m4:                           FSFULLR and GPLv2+ with exception
# ar-lib:                               GPLv2+ with exception
# cmake/COPYING-CMAKE-SCRIPTS:          BSD
# compile:                              GPLv2+ with exception
# config.guess:                         GPLv3+ with exception
# config.sub:                           GPLv3+ with exception
# configure:                            FSFUL and GPLv2+ with exception
# depcomp:                              GPLv2+ with exception
# INSTALL:                              FSFAP
# install-sh:                           MIT
# ltmain.sh:                            GPLv2+ with exception and (MIT or GPLv3+)
# m4/ax_pthread.m4:                     GPLv3+ with exception
# m4/libtool.m4:                        FSFUL and FSFULLR and
#                                       GPLv2+ with exception
# m4/ltoptions.m4:                      FSFULLR
# m4/ltsugar.m4:                        FSFULLR
# m4/ltversion.m4:                      FSFULLR
# m4/lt~obsolete.m4:                    FSFULLR
# m4/pcre2_visibility.m4:               FSFULLR
# Makefile.in:                          FSFULLR
# missing:                              GPLv2+ with exception
# test-driver:                          GPLv2+ with exception
# testdata:                             Public Domain
License:    BSD
URL:        https://www.pcre.org/
%if !0%{?os2_version}
Source0:    https://ftp.pcre.org/pub/pcre/%{?rcversion:Testing/}%{name}-%{myversion}.tar.bz2
Source1:    https://ftp.pcre.org/pub/pcre/%{?rcversion:Testing/}%{name}-%{myversion}.tar.bz2.sig
Source2:    https://ftp.pcre.org/pub/pcre/Public-Key
# Do no set RPATH if libdir is not /usr/lib
Patch0:     pcre2-10.10-Fix-multilib.patch
# Fix a possible NULL pointer dereference in auto_possessify(),
# upstream bug #2686, in upstream after 10.36
Patch1:     pcre2-10.36-Get-rid-of-gcc-fanalyzer-error-though-it-was-probabl.patch
# Fix misparsing long numbers as a backreference and a number without
# a closing bracket as a quantifier, upstream bug #2690, in upstream after
# 10.36
Patch2:     pcre2-10.36-Fix-some-numerical-checking-bugs-Bugzilla-2690.patch
# Fix a mismatch if \K was involved in a recursion, in upstream after 10.36
Patch3:     pcre2-10.36-Fix-K-within-recursion-bug-in-interpreter.patch
# Restore single character repetition optimization in JIT, upstream bug #2698,
# in upstream after 10.36
Patch4:     pcre2-10.36-Restore-single-character-repetition-optimization-in-.patch
%else
Vendor:         bww bitwise works GmbH
%scm_source     github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2
%endif
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  coreutils
BuildRequires:  gcc
BuildRequires:  gnupg2
BuildRequires:  libtool
BuildRequires:  make
%if %{with pcre2_enables_readline}
BuildRequires:  readline-devel
%endif
BuildRequires:  sed
Requires:       %{name}-syntax = %{version}-%{release}
%if !0%{?os2_version}
Provides:       bundled(sljit)
%endif

%description
PCRE2 is a re-working of the original PCRE (Perl-compatible regular
expression) library to provide an entirely new API.

PCRE2 is written in C, and it has its own API. There are three sets of
functions, one for the 8-bit library, which processes strings of bytes, one
for the 16-bit library, which processes strings of 16-bit values, and one for
the 32-bit library, which processes strings of 32-bit values. There are no C++
wrappers. This package provides support for strings in 8-bit and UTF-8
encodings. Install %{name}-utf16 or %{name}-utf32 packages for the other ones.

The distribution does contain a set of C wrapper functions for the 8-bit
library that are based on the POSIX regular expression API (see the pcre2posix
man page). These can be found in a library called libpcre2posix. Note that
this just provides a POSIX calling interface to PCRE2; the regular expressions
themselves still follow Perl syntax and semantics. The POSIX API is
restricted, and does not give full access to all of PCRE2's facilities.

%package utf16
Summary:    UTF-16 variant of PCRE2
%if !0%{?os2_version}
Provides:   bundled(sljit)
%endif
Requires:   %{name}-syntax = %{version}-%{release}
Conflicts:  %{name} < 10.21-4

%description utf16
This is PCRE2 library working on UTF-16 strings.

%package utf32
Summary:    UTF-32 variant of PCRE2
%if !0%{?os2_version}
Provides:   bundled(sljit)
%endif
Requires:   %{name}-syntax = %{version}-%{release}
Conflicts:  %{name} < 10.21-4

%description utf32
This is PCRE2 library working on UTF-32 strings.

%package devel
Summary:    Development files for %{name}
Requires:   %{name} = %{version}-%{release}
Requires:   %{name}-utf16 = %{version}-%{release}
Requires:   %{name}-utf32 = %{version}-%{release}

%description devel
Development files (headers, libraries for dynamic linking, documentation)
for %{name}.  The header file for the POSIX-style functions is called
pcre2posix.h.

%package static
Summary:    Static library for %{name}
Requires:   %{name}-devel = %{version}-%{release}
%if !0%{?os2_version}
Provides:   bundled(sljit)
%endif

%description static
Library for static linking for %{name}.

%package syntax
Summary:    Documentation for PCRE2 regular expressions
BuildArch:  noarch
Conflicts:  %{name}-devel < 10.34-8

%description syntax
This is a set of manual pages that document a syntax of the regular
expressions implemented by the PCRE2 library.

%package tools
Summary:    Auxiliary utilities for %{name}
# pcre2test (linked to GNU readline):   BSD (linked to GPLv3+)
License:    BSD and GPLv3+
Requires:   %{name} = %{version}-%{release}

%description tools
Utilities demonstrating PCRE2 capabilities like pcre2grep or pcre2test.

%if 0%{?os2_version}
%debug_package
%endif

%prep
%if !0%{?os2_version}
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -n %{name}-%{myversion} -p1
# Because of multilib patch
libtoolize --copy --force
%else
%scm_setup
%endif
autoreconf -vif

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
    --disable-pcre2grep-jit \
%else
    --enable-jit \
    --enable-pcre2grep-jit \
%endif
%endif
    --disable-bsr-anycrlf \
    --disable-coverage \
    --disable-ebcdic \
    --disable-fuzz-support \
%if %{with pcre2_enables_sealloc}
    --enable-jit-sealloc \
%else
    --disable-jit-sealloc \
%endif
    --disable-never-backslash-C \
%if !0%{?os2_version}
    --enable-newline-is-lf \
%else
    --enable-newline-is-any \
%endif
    --enable-pcre2-8 \
    --enable-pcre2-16 \
    --enable-pcre2-32 \
    --enable-pcre2grep-callout \
    --enable-pcre2grep-callout-fork \
    --disable-pcre2grep-libbz2 \
    --disable-pcre2grep-libz \
    --disable-pcre2test-libedit \
%if %{with pcre2_enables_readline}
    --enable-pcre2test-libreadline \
%else
    --disable-pcre2test-libreadline \
%endif
    --enable-percent-zt \
    --disable-rebuild-chartables \
    --enable-shared \
    --disable-silent-rules \
    --enable-static \
    --enable-unicode \
    --disable-valgrind
make %{?_smp_mflags}

%install
%{make_install}
# Get rid of unneeded *.la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
# These are handled by %%doc in %%files
rm -rf $RPM_BUILD_ROOT%{_docdir}/pcre2

%check
%if !0%{?os2_version}
make %{?_smp_mflags} check VERBOSE=yes
%endif

%files
%if !0%{?os2_version}
%{_libdir}/libpcre2-8.so.0*
%{_libdir}/libpcre2-posix.so.2*
%else
%{_libdir}/pcre28*.dll
%{_libdir}/pcre2p*.dll
%endif

%files utf16
%if !0%{?os2_version}
%{_libdir}/libpcre2-16.so.0*
%else
%{_libdir}/pcre26*.dll
%endif

%files utf32
%if !0%{?os2_version}
%{_libdir}/libpcre2-32.so.0*
%else
%{_libdir}/pcre23*.dll
%endif

%files devel
%if !0%{?os2_version}
%{_libdir}/*.so
%else
%{_libdir}/*_dll.a
%endif
%{_libdir}/pkgconfig/*
%{_includedir}/*.h
%{_mandir}/man1/pcre2-config.*
%{_mandir}/man3/pcre2_*
%{_mandir}/man3/pcre2api.*
%{_mandir}/man3/pcre2build.*
%{_mandir}/man3/pcre2callout.*
%{_mandir}/man3/pcre2convert.*
%{_mandir}/man3/pcre2demo.*
%{_mandir}/man3/pcre2jit.*
%{_mandir}/man3/pcre2posix.*
%{_mandir}/man3/pcre2sample.*
%{_mandir}/man3/pcre2serialize*
%{_bindir}/pcre2-config
%doc doc/*.txt doc/html
%doc README HACKING ./src/pcre2demo.c

%files static
%{_libdir}/*.a
%if 0%{?os2_version}
%exclude %{_libdir}/*_dll.a
%endif
%license COPYING LICENCE

%files syntax
%license COPYING LICENCE
%doc AUTHORS ChangeLog NEWS
%{_mandir}/man3/pcre2.*
%{_mandir}/man3/pcre2compat.*
%{_mandir}/man3/pcre2limits.*
%{_mandir}/man3/pcre2matching.*
%{_mandir}/man3/pcre2partial.*
%{_mandir}/man3/pcre2pattern.*
%{_mandir}/man3/pcre2perform.*
%{_mandir}/man3/pcre2syntax.*
%{_mandir}/man3/pcre2unicode.*

%files tools
%if !0%{?os2_version}
%{_bindir}/pcre2grep
%{_bindir}/pcre2test
%else
%{_bindir}/pcre2grep.exe
%{_bindir}/pcre2test.exe
%endif
%{_mandir}/man1/pcre2grep.*
%{_mandir}/man1/pcre2test.*

%changelog
* Fri Apr 02 2021 Silvan Scherrer <silvan.scherrer@aroa.ch> - 10.36-1
- First OS/2 rpm

