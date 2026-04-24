%global perl_version    5.42.2
%global perl_epoch      4
%global perl_arch_stem -thread-multi
%global perl_archname %{_arch}-%{_os}%{perl_arch_stem}

%global multilib_64_archs aarch64 %{power64} s390x sparc64 x86_64 
%global parallel_tests 1
%global tapsetdir   %{_datadir}/systemtap/tapset

%global dual_life 0
%if !0%{?os2_version}
%global rebuild_from_scratch %{defined perl_bootstrap}
%else
%global rebuild_from_scratch 1
%global perl_bootstrap 1
%endif

# This overrides filters from build root (/usr/lib/rpm/macros.d/macros.perl)
# intentionally (unversioned perl(DB) is removed and versioned one is kept).
# Filter provides from *.pl files, bug #924938
%global __provides_exclude_from .*%{_docdir}
%if %{defined perl_archlib}
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}.*%{perl_archlib}/.*\\.pl$|.*%{perl_privlib}/.*\\.pl$
%endif
%if 0%{?os2_version}
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}.*/auto/.*\\.dll$|.*%{perl_archlib}/.*\\.dll$
%endif
%global __requires_exclude_from %{_docdir}
%global __provides_exclude perl\\((VMS|Win32|BSD::|DB\\)$)
%global __requires_exclude perl\\((VMS|BSD::|Win32|Tk|Mac::|Your::Module::Here)
# same as we provide in /usr/lib/rpm/macros.d/macros.perl
%global perl5_testdir   %{_libexecdir}/perl5-tests

# Optional features
# Run C++ tests
%bcond_without perl_enables_cplusplus_test
# We can build without libdb (BerkeleyDB)
%if 0%{?rhel} || 0%{?os2_version}
%bcond_with bdb
%else
%bcond_without bdb
%endif
# We can bootstrap without gdbm
%if !0%{?os2_version}
%bcond_without gdbm
else
%bcond_with gdbm
%endif
# Support for groff, bug #135101
%bcond_without perl_enables_groff
# Run Turkish locale tests
%bcond_without perl_enables_turkish_test
# Run syslog tests
%bcond_with perl_enables_syslog_test
# SystemTap support
%if !0%{?os2_version}
%bcond_without perl_enables_systemtap
%else
%bcond_with perl_enables_systemtap
%endif
# <> operator uses File::Glob nowadays. CSH is not needed.
%bcond_with perl_enables_tcsh
# We can skip %%check phase
%if !0%{?os2_version}
%bcond_without test
%else
%bcond_with test
%endif

# The additional linker flags break binary perl- packages.
# https://bugzilla.redhat.com/show_bug.cgi?id=2043092
%undefine _package_note_file

Name:           perl
# These are all found licenses. They are distributed among various
# subpackages.
# dist/Tie-File/lib/Tie/File.pm:        GPL-2.0-or-later OR Artistic-1.0-Perl
# cpan/Getopt-Long/lib/Getopt/Long.pm:  GPL-2.0-or-later OR Artistic-1.0-Perl
# cpan/Compress-Raw-Zlib/Zlib.xs:       (GPL-1.0-or-later OR Artistic-1.0-Perl) AND Zlib
# RSA-MD does not have to be recorded in the License
# cpan/Digest-MD5/MD5.xs:               (GPL-1.0-or-later OR Artistic-1.0-Perl)
#                                        AND RSA-MD
# cpan/Time-Piece/Piece.xs:             (GPL-1.0-or-later OR Artistic-1.0-Perl)
#                                        AND BSD-2-Clause-Views
# dist/PathTools/Cwd.xs:                (GPL-1.0-or-later OR Artistic-1.0-Perl)
#                                        AND BSD-3-Clause
# util.c:                               (GPL-1.0-or-later OR Artistic-1.0-Perl) AND Martin-Birgmeier
# cpan/perlfaq/lib/perlfaq4.pod:        (GPL-1.0-or-later OR Artistic-1.0-Perl) AND LicenseRef-Fedora-Public-Domain
# cpan/Test-Simple/lib/Test/Tutorial.pod:   (GPL-1.0-or-later OR Artistic-1.0-Perl)
#                                            AND LicenseRef-Fedora-Public-Domain
# cpan/MIME-Base64/Base64.xs:           (GPL-1.0-or-later OR Artistic-1.0-Perl)
#                                        AND MIT (Bellcore)
# cpan/Test-Simple/lib/ok.pm:           CC0-1.0
# cpan/Text-Tabs/lib/Text/Wrap.pm:      TTWL
# cpan/Encode/bin/encguess:             Artistic-2.0
# cpan/Unicode-Collate/Collate/allkeys.txt:     Unicode-DFS-2015
# inline.h:                             MIT
# lib/unicore:                          Unicode-3.0
# ext/SDBM_File/sdbm.{c,h}:             Public domain
# regexec.c, regcomp.c:                 Spencer-86
# cpan/Locale-Maketext-Simple/lib/Locale/Maketext/Simple.pm:    MIT (with
#                                       exception for Perl)
# time64.c:                             MIT
# perly.h:                              GPL-3.0-or-later WITH Bison-exception-2.2
# pod/perlpodstyle.pod:                 MIT
# pod/perlunicook.pod:                  (GPL-1.0-or-later OR Artistic-1.0-Perl) AND LicenseRef-Fedora-UltraPermissive
# pod/perlgpl.pod:                      GPL text
# pod/perlartistic.pod:                 Artistic text
# ext/File-Glob/bsd_glob.{c,h}:         BSD-3-Clause
# Other files:                          GPL-1.0-or-later OR Artistic-1.0-Perl
## Not in a binary package
# ebcdic_tables.h:                                  MIT
# cpan/podlators/t/docs/pod.t:                      MIT
# cpan/podlators/t/docs/pod-spelling.t:             MIT
# cpan/podlators/t/docs/spdx-license.t:             MIT
# cpan/podlators/t/docs/synopsis.t:                 MIT
# cpan/podlators/t/docs/urls.t :                    MIT
# cpan/podlators/t/lib/Test/RRA.pm:                 MIT
# cpan/podlators/t/lib/Test/RRA/Config.pm:          MIT
# cpan/podlators/t/lib/Test/RRA/ModuleVersion.pm:   MIT
# cpan/podlators/t/style/minimum-version.t:         MIT
# cpan/podlators/t/style/module-version.t:          MIT
# cpan/podlators/t/style/strict.t:                  MIT
# cpan/Term-ANSIColor/t/lib/Test/RRA/Config.pm:     MIT
## Unbundled
# cpan/Compress-Raw-Bzip2/bzip2-src:    bzip2-1.0.6
# cpan/Compress-Raw-Zlib/zlib-src:      Zlib
# perl.h (EBDIC parts)                              MIT
## perl sub-package notice
# perluniprops.pod is generated from lib/unicore sources:   Unicode-3.0
# uni_keywords.h is generated from lib/unicore sources:     Unicode-3.0
#
# This sub-subpackage doesn't contain any copyrightable material.
# Nevertheless, it needs a License tag, so we'll use the generic
# "perl" license.
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          %{perl_epoch}
Version:        %{perl_version}
# release number must be even higher, because dual-lived modules will be broken otherwise
Release:        14%{?dist}
Summary:        Practical Extraction and Report Language
Url:            https://www.perl.org/
%if !0%{?os2_version}
Source0:        https://www.cpan.org/src/5.0/perl-%{perl_version}.tar.xz
%else
Vendor:         bww bitwise works GmbH
%scm_source     github https://github.com/bitwiseworks/%{name}-os2 %{perl_version}-os2
%global main_version %{perl_version}
%endif
Source3:        macros.perl
%if !0%{?os2_version}
#Systemtap tapset and example that make use of systemtap-sdt-devel
# build requirement. Written by lberk; Not yet upstream.
Source4:        perl.stp
Source5:        perl-example.stp
%endif
# Tom Christiansen confirms Pod::Html uses the same license as perl
Source6:        Pod-Html-license-clarification

# Pregenerated dependencies for bootstrap.
# If your RPM tool fails on including the source file, then you forgot to
# define _sourcedir macro to point to the directory with the sources.
Source7:        gendep.macros
%if %{defined perl_bootstrap}
%include %{SOURCE7}
%endif
%if !0%{?os2_version}
# Use config.over to make build of perl reproducible
Source8:        config.over

# Removes date check, Fedora/RHEL specific
Patch1:         perl-perlbug-tag.patch

# Fedora/RHEL only (64bit only)
Patch2:         perl-5.8.0-libdir64.patch

# Fedora/RHEL specific (use libresolv instead of libbind), bug #151127
Patch3:         perl-5.10.0-libresolv.patch

# FIXME: May need the "Fedora" references removed before upstreaming
# patches ExtUtils-MakeMaker
Patch4:         perl-USE_MM_LD_RUN_PATH.patch

# Provide maybe_command independently, bug #1129443
Patch5:         perl-5.22.1-Provide-ExtUtils-MM-methods-as-standalone-ExtUtils-M.patch

# The Fedora builders started randomly failing this futime test
# only on x86_64, so we just don't run it. Works fine on normal
# systems.
Patch6:         perl-5.10.0-x86_64-io-test-failure.patch

# switch off test, which is failing only on koji (fork)
Patch7:         perl-5.14.1-offtest.patch

# Define SONAME for libperl.so
Patch8:         perl-5.16.3-create_libperl_soname.patch

# Install libperl.so to -Dshrpdir value
Patch9:         perl-5.22.0-Install-libperl.so-to-shrpdir-on-Linux.patch

# Make *DBM_File desctructors thread-safe, bug #1107543, RT#61912
Patch10:        perl-5.34.0-Destroy-GDBM-NDBM-ODBM-SDBM-_File-objects-only-from-.patch

# Replace ExtUtils::MakeMaker dependency with ExtUtils::MM::Utils.
# This allows not to require perl-devel. Bug #1129443
Patch11:        perl-5.22.1-Replace-EU-MM-dependnecy-with-EU-MM-Utils-in-IPC-Cmd.patch

# Link XS modules to pthread library to fix linking with -z defs,
# <https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/message/3RHZEHLRUHJFF2XGHI5RB6YPDNLDR4HG/>
Patch12:        perl-5.27.8-hints-linux-Add-lphtread-to-lddlflags.patch

# Pass the correct CFLAGS to dtrace
Patch13:        perl-5.28.0-Pass-CFLAGS-to-dtrace.patch

# Link XS modules to libperl.so with EU::CBuilder on Linux, bug #960048
Patch200:       perl-5.16.3-Link-XS-modules-to-libperl.so-with-EU-CBuilder-on-Li.patch

# Link XS modules to libperl.so with EU::MM on Linux, bug #960048
Patch201:       perl-5.16.3-Link-XS-modules-to-libperl.so-with-EU-MM-on-Linux.patch

# If optimizing -O is used, add the definition to .ph files, bug #2152012
Patch202:       perl-5.36.0-Add-definition-of-OPTIMIZE-to-.ph-files.patch
%endif

# Update some of the bundled modules
# see http://fedoraproject.org/wiki/Perl/perl.spec for instructions

BuildRequires:  bash
BuildRequires:  bzip2-devel
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
%if %{with gdbm}
BuildRequires:  gdbm-devel
%endif
# glibc-common for iconv
%if !0%{?os2_version}
BuildRequires:  glibc-common
%endif
%if %{with perl_enables_groff}
# Build-require groff tools for populating %%Config correctly, bug #135101
BuildRequires:  groff-base
%endif
%if %{with bdb}
BuildRequires:  libdb-devel
%endif
BuildRequires:  make
%if !%{defined perl_bootstrap}
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
%endif
BuildRequires:  sed
%if %{with perl_enables_systemtap}
BuildRequires:  systemtap-sdt-devel
BuildRequires:  systemtap-sdt-dtrace
%endif
BuildRequires:  tar
%if %{with perl_enables_tcsh}
BuildRequires:  tcsh
%endif
BuildRequires:  zlib-devel

# For tests
%if %{with test}
%if %{with perl_enables_cplusplus_test}
# An optional ExtUtils-CBuilder's test
BuildRequires:  gcc-c++
%endif
BuildRequires:  procps
%if %{with perl_enables_turkish_test}
# An optional t/re/fold_grind_T.t test
BuildRequires:  glibc-langpack-tr
%endif
%if %{with perl_enables_syslog_test}
BuildRequires:  rsyslog
%endif
%endif


# compat macro needed for rebuild
%global perl_compat perl(:MODULE_COMPAT_5.42.2)

Requires:       %perl_compat
%if !0%{?os2_version}
Requires:       perl-interpreter%{?_isa} = %{perl_epoch}:%{perl_version}-%{release}
Requires:       perl-libs%{?_isa} = %{perl_epoch}:%{perl_version}-%{release}
Requires:       perl-devel%{?_isa} = %{perl_epoch}:%{perl_version}-%{release}
%else
Requires:       perl-interpreter = %{perl_epoch}:%{perl_version}-%{release}
Requires:       perl-libs = %{perl_epoch}:%{perl_version}-%{release}
Requires:       perl-devel = %{perl_epoch}:%{perl_version}-%{release}
%endif
Requires:       perl-macros
Requires:       perl-utils
%if %{defined perl_bootstrap}
%gendep_perl
%endif

Requires:       perl-Archive-Tar, perl-Attribute-Handlers, perl-autodie,
Requires:       perl-AutoLoader, perl-AutoSplit, perl-autouse,
Requires:       perl-B, perl-base, perl-Benchmark, perl-bignum, perl-blib,
Requires:       perl-Carp, perl-Class-Struct,
Requires:       perl-Compress-Raw-Bzip2, perl-Compress-Raw-Zlib,
Requires:       perl-Config-Extensions, perl-Config-Perl-V, perl-constant,
Requires:       perl-CPAN, perl-CPAN-Meta, perl-CPAN-Meta-Requirements,
Requires:       perl-CPAN-Meta-YAML, perl-Data-Dumper,
%if %{with bdb}
Requires:       perl-DB_File,
%endif
Requires:       perl-DBM_Filter, perl-debugger, perl-deprecate,
Requires:       perl-Devel-Peek, perl-Devel-PPPort, perl-Devel-SelfStubber,
Requires:       perl-diagnostics, perl-Digest, perl-Digest-MD5, perl-Digest-SHA,
Requires:       perl-DirHandle,
Requires:       perl-doc,
Requires:       perl-Dumpvalue,
Requires:       perl-DynaLoader,
Requires:       perl-Encode, perl-Encode-devel, perl-encoding,
Requires:       perl-encoding-warnings, perl-English,
Requires:       perl-Env, perl-Errno, perl-experimental, perl-Exporter,
Requires:       perl-ExtUtils-CBuilder, perl-ExtUtils-Constant,
Requires:       perl-ExtUtils-Command,
Requires:       perl-ExtUtils-Embed, perl-ExtUtils-Install,
Requires:       perl-ExtUtils-MakeMaker, perl-ExtUtils-Manifest,
%if !0%{?os2_version}
Requires:       perl-ExtUtils-Miniperl, perl-ExtUtils-MM-Utils,
%else
Requires:       perl-ExtUtils-Miniperl,
%endif
Requires:       perl-ExtUtils-ParseXS,
Requires:       perl-Fcntl, perl-fields,
Requires:       perl-File-Basename, perl-File-Compare, perl-File-Copy,
Requires:       perl-File-DosGlob, perl-File-Fetch,
Requires:       perl-File-Find, perl-File-Path, perl-File-stat, perl-File-Temp,
Requires:       perl-FileCache, perl-FileHandle, perl-filetest,
Requires:       perl-Filter, perl-Filter-Simple,
Requires:       perl-FindBin,
%if %{with gdbm}
Requires:       perl-GDBM_File,
%endif
Requires:       perl-Getopt-Long, perl-Getopt-Std,
Requires:       perl-Hash-Util, perl-Hash-Util-FieldHash, perl-HTTP-Tiny,
Requires:       perl-if, perl-IO, perl-IO-Compress, perl-IO-Socket-IP,
Requires:       perl-IO-Zlib, perl-IPC-Cmd, perl-IPC-Open3, perl-IPC-SysV,
Requires:       perl-I18N-Collate, perl-I18N-Langinfo, perl-I18N-LangTags,
Requires:       perl-JSON-PP,
Requires:       perl-less,
Requires:       perl-lib, perl-libnet, perl-libnetcfg,
Requires:       perl-locale, perl-Locale-Maketext, perl-Locale-Maketext-Simple,
Requires:       perl-Math-BigInt, perl-Math-BigInt-FastCalc,
Requires:       perl-Math-Complex, perl-Memoize, perl-meta-notation,
Requires:       perl-MIME-Base64,
Requires:       perl-Module-CoreList, perl-Module-CoreList-tools,
Requires:       perl-Module-Load, perl-Module-Load-Conditional,
Requires:       perl-Module-Loaded, perl-Module-Metadata,
Requires:       perl-mro,
%if %{with gdbm}
Requires:       perl-NDBM_File,
%endif
Requires:       perl-Net, perl-Net-Ping, perl-NEXT,
%if %{with gdbm}
Requires:       perl-ODBM_File,
%endif
Requires:       perl-Opcode, perl-open, perl-overload, perl-overloading,
Requires:       perl-parent, perl-PathTools, perl-Params-Check, perl-perlfaq,
Requires:       perl-PerlIO-via-QuotedPrint, perl-Perl-OSType,
Requires:       perl-ph,
Requires:       perl-Pod-Checker, perl-Pod-Escapes, perl-Pod-Functions,
Requires:       perl-Pod-Html, perl-Pod-Perldoc,
Requires:       perl-Pod-Simple, perl-Pod-Usage, perl-podlators, perl-POSIX,
Requires:       perl-Safe, perl-Scalar-List-Utils,
Requires:       perl-Search-Dict, perl-SelectSaver,
Requires:       perl-SelfLoader, perl-sigtrap, perl-Socket, perl-sort,
Requires:       perl-Storable,
Requires:       perl-subs,
Requires:       perl-Symbol, perl-Sys-Hostname, perl-Sys-Syslog,
Requires:       perl-Term-ANSIColor, perl-Term-Cap, perl-Term-Complete,
Requires:       perl-Term-ReadLine, perl-Term-Table,
Requires:       perl-Test, perl-Test-Harness, perl-Test-Simple,
Requires:       perl-Text-Abbrev, perl-Text-Balanced, perl-Text-ParseWords,
Requires:       perl-Text-Tabs+Wrap,
Requires:       perl-Thread, perl-Thread-Queue, perl-Thread-Semaphore,
Requires:       perl-threads, perl-threads-shared,
Requires:       perl-Tie, perl-Tie-File, perl-Tie-Memoize, perl-Tie-RefHash,
Requires:       perl-Time, perl-Time-HiRes, perl-Time-Local, perl-Time-Piece,
Requires:       perl-Unicode-Collate, perl-Unicode-Normalize, perl-Unicode-UCD,
Requires:       perl-User-pwent,
Requires:       perl-vars, perl-version, perl-vmsish,

# Full EVR is for compatibility with systems that swapped perl and perl-core
# <https://fedoraproject.org/wiki/Changes/perl_Package_to_Install_Core_Modules>,
# bug #1464903.
Provides:       perl-core = %{perl_version}-%{release}
%if !0%{?os2_version}
Provides:       perl-core%{?_isa} = %{perl_version}-%{release}
%endif
# perl was renamed to perl-interpreter and perl-core renamed to perl
Obsoletes:      perl-core < 5.26.0-395


%description
Perl is a high-level programming language with roots in C, sed, awk and shell
scripting. Perl is good at handling processes and files, and is especially
good at handling text. Perl's hallmarks are practicality and efficiency.
While it is used to do a lot of different things, Perl's most common
applications are system administration utilities and web programming.

This is a metapackage with all the Perl bits and core modules that can be
found in the upstream tarball from perl.org.

If you need only a specific feature, you can install a specific package
instead. E.g. to handle Perl scripts with %{_bindir}/perl interpreter,
install perl-interpreter package. See perl-interpreter description for more
details on the Perl decomposition into packages.


%package interpreter
Summary:        Standalone executable Perl interpreter
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
# perl-interpreter denotes a package with the perl executable.
# Full EVR is for compatibility with systems that swapped perl and perl-core
# <https://fedoraproject.org/wiki/Changes/perl_Package_to_Install_Core_Modules>,
# bug #1464903.
Version:        %{perl_version}
Epoch:          %{perl_epoch}

%if !0%{?os2_version}
Requires:       perl-libs%{?_isa} = %{perl_epoch}:%{perl_version}-%{release}
%else
Requires:       perl-libs = %{perl_epoch}:%{perl_version}-%{release}
%endif
Suggests:       perl-doc = %{perl_version}-%{release}
%if %{defined perl_bootstrap}
# Require this till perl-interpreter sub-package provides any modules
Requires:       %perl_compat
%gendep_perl_interpreter
%endif

# We need this to break the dependency loop, and ensure that perl-libs 
# gets installed before perl-interpreter.
Requires(post): perl-libs

# suidperl isn't created by upstream since 5.12.0
Obsoletes:      perl-suidperl <= 4:5.12.2
# perl was renamed to perl-interpreter and perl-core renamed to perl
# <https://fedoraproject.org/wiki/Changes/perl_Package_to_Install_Core_Modules>,
# bug #1464903.
Obsoletes:      perl < 4:5.26.0-395

%description interpreter
This is a Perl interpreter as a standalone executable %{_bindir}/perl
required for handling Perl scripts. It does not provide all the other Perl
modules or tools.

Install this package if you want to program in Perl or enable your system to
handle Perl scripts with %{_bindir}/perl interpreter.

If your script requires some Perl modules, you can install them with
"perl(MODULE)" where "MODULE" is a name of required module. E.g. install
"perl(Test::More)" to make Test::More Perl module available.

If you need all the Perl modules that come with upstream Perl sources, so
called core modules, install perl package.

If you only need perl run-time as a shared library, i.e. Perl interpreter
embedded into another application, the only essential package is perl-libs.

Perl header files can be found in perl-devel package.

Perl utils like "h2ph" or "perlbug" can be found in perl-utils package.

Perl debugger, usually invoked with "perl -d", is available in perl-debugger
package.


%package libs
Summary:        The libraries for the perl run-time
License:        (GPL-1.0-or-later OR Artistic-1.0-Perl) AND Martin-Birgmeier AND Spencer-86 AND MIT AND Unicode-3.0 AND LicenseRef-Fedora-Public-Domain
# Compat provides
Provides:       %perl_compat
Provides:       perl(:MODULE_COMPAT_5.42.1)
Provides:       perl(:MODULE_COMPAT_5.42.0)
# Interpreter version to fulfil required genersted from "require 5.006;"
Provides:       perl(:VERSION) = %{perl_version}
# Integeres are 64-bit on all platforms
Provides:       perl(:WITH_64BIT)
# Threading provides
Provides:       perl(:WITH_ITHREADS)
Provides:       perl(:WITH_THREADS)
# Largefile provides
Provides:       perl(:WITH_LARGEFILES)
# PerlIO provides
Provides:       perl(:WITH_PERLIO)
# Loaded by charnames, unicore/Name.pm does not declare unicore::Name module
Provides:       perl(unicore::Name)
# Keep utf8 modules in perl-libs because a sole regular expression like /\pN/
# causes loading utf8 and unicore/Heave.pl and unicore/lib files.
Provides:       perl(utf8_heavy.pl)
# utf8 and utf8_heavy.pl require Carp, re, strict, warnings, XSLoader
# For AnyDBM_File
%if %{with bdb}
Suggests:       perl(DB_File)
%endif
# XSLoader requires DynaLoder
Requires:       perl(DynaLoader)
# Encode is loaded in BOOT section of PerlIO::encoding
Requires:       perl(Encode)
# File::Spec loaded by _charnames.pm that is loaded by \N{}
Requires:       perl(File::Spec)
%if %{with gdbm}
# For AnyDBM_File
Suggests:       perl(GDBM_File)
Recommends:     perl(NDBM_File)
Suggests:       perl(ODBM_File)
%endif
# Term::Cap is optional
%if %{defined perl_bootstrap}
%gendep_perl_libs
%endif

# Remove private redefinitions
# XSLoader redefines DynaLoader name space for compatibility, but it still
# loads DynaLoader.pm (though DynaLoader.xs is compiled into libperl).
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\((charnames|DynaLoader)\\)$

%description libs
The is a perl run-time (interpreter as a shared library and include
directories).


%package devel
Summary:        Header files for use in perl development
# l1_char_class_tab.h is generated from lib/unicore sources:    Unicode-3.0
License:        (GPL-1.0-or-later OR Artistic-1.0-Perl) AND Unicode-3.0
%if %{with perl_enables_systemtap}
Requires:       systemtap-sdt-devel
Requires:       systemtap-sdt-dtrace
%endif
Requires:       perl(ExtUtils::ParseXS)
# Match library and header files when downgrading releases
%if !0%{?os2_version}
Requires:       perl-libs%{?_isa} = %{perl_epoch}:%{perl_version}-%{release}
%else
Requires:       perl-libs = %{perl_epoch}:%{perl_version}-%{release}
%endif
Recommends:     perl-doc = %{perl_version}-%{release}
# Devel::PPPort for h2xs script
Requires:       perl(Devel::PPPort)
# Compiler and linker options stored into perl and used when building XS
# modules refer to hardering profiles like
# /usr/lib/rpm/redhat/redhat-hardened-cc1 that are delivered by
# redhat-rpm-config. Bug #1557667.
%if !0%{?os2_version}
Requires:       redhat-rpm-config
# ExtUtils::Embed -e ldopts include libcrypt, bug #1666098
Requires:       libxcrypt-devel%{?_isa}
%endif

%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_devel
%endif

%description devel
This package contains header files and development modules.
Most perl packages will need to install perl-devel to build.


%package macros
Summary:        Macros for rpmbuild
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
BuildArch:      noarch
Requires:       perl-interpreter
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_macros
%endif

%description macros
RPM macros that are handy when building binary RPM packages.


%package tests
Summary:        The Perl test suite
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
# right?
AutoReqProv:    0
# FIXME - note this will need to change when doing the core/minimal swizzle
Requires:       perl
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_tests
%endif

%description tests
This package contains the test suite included with Perl %{perl_version}.

Install this if you want to test your Perl installation (binary and core
modules).


%package utils
Summary:        Utilities packaged with the Perl distribution
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        %{perl_version}
BuildArch:      noarch
# Match library exactly for perlbug version string
Requires:       perl-libs = %{perl_epoch}:%{perl_version}-%{release}
# Keep /usr/sbin/sendmail and Module::CoreList optional for the perlbug tool
%if %{defined perl_bootstrap}
%gendep_perl_utils
%endif
Conflicts:      perl < 4:5.22.0-351

%description utils
Several utilities which come with Perl distribution like h2ph, perlbug,
perlthanks, and pl2pm. Some utilities are provided by more specific
packages like perldoc by perl-Pod-Perldoc and splain by perl-diagnostics.

%if %{dual_life} || %{rebuild_from_scratch}
%package Archive-Tar
Summary:        A module for Perl manipulation of .tar files
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        3.04
BuildArch:      noarch
Requires:       perl(IO::Zlib) >= 1.01
# Optional run-time:
Requires:       perl(IO::Compress::Bzip2) >= 2.015
# IO::String not used if perl supports useperlio which is true
# Use Compress::Zlib's version for IO::Uncompress::Bunzip2
Requires:       perl(IO::Uncompress::Bunzip2) >= 2.015
%if !%{defined perl_bootstrap}
Requires:       perl(Text::Diff)
%endif
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Archive_Tar
%endif

%description Archive-Tar
Archive::Tar provides an object oriented mechanism for handling tar files.  It
provides class methods for quick and easy files handling while also allowing
for the creation of tar file objects for custom manipulation.  If you have the
IO::Zlib module installed, Archive::Tar will also support compressed or
gzipped tar files.
%endif

%package Attribute-Handlers
Summary:        Simpler definition of attribute handlers
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.03
BuildArch:      noarch
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Attribute_Handlers
%endif
Conflicts:      perl < 4:5.22.0-351

%description Attribute-Handlers
This Perl module, when inherited by a package, allows that package's class to
define attribute handler subroutines for specific attributes. Variables and
subroutines subsequently defined in that package, or in packages derived from
that package may be given attributes with the same names as the attribute
handler subroutines, which will then be called in one of the compilation
phases (i.e. in a "BEGIN", "CHECK", "INIT", or "END" block).

%if %{dual_life} || %{rebuild_from_scratch}
%package autodie
Summary:        Replace functions with ones that succeed or die
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        2.37
BuildArch:      noarch
Requires:       perl(B)
Requires:       perl(Fcntl)
Requires:       perl(overload)
Requires:       perl(POSIX)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_autodie
%endif
Conflicts:      perl < 4:5.16.2-259

%description autodie
The "autodie" and "Fatal" pragma provides a convenient way to replace
functions that normally return false on failure with equivalents that throw an
exception on failure.

However "Fatal" has been obsoleted by the new autodie pragma. Please use
autodie in preference to "Fatal".
%endif

%package AutoLoader
Summary:        Load subroutines only on demand
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        5.74
BuildArch:      noarch
Requires:       perl(Carp)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_AutoLoader
%endif
Conflicts:      perl < 4:5.30.1-451

%description AutoLoader
The AutoLoader module works with the AutoSplit module and the "__END__" token
to defer the loading of some subroutines until they are used rather than
loading them all at once.

%package AutoSplit
Summary:        Split a package for automatic loading
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
# Real version 1.06
Version:        5.74
BuildArch:      noarch
Requires:       perl(Carp)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_AutoSplit
%endif
Conflicts:      perl < 4:5.30.1-451

%description AutoSplit
Split up your program into files that the AutoLoader module can handle. It is
used by both the standard Perl libraries and by the ExtUtils::MakeMaker
utility, to automatically configure libraries for automatic loading.

%package autouse
Summary:        Postpone load of modules until a function is used
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.11
BuildArch:      noarch
Requires:       perl(Carp)
Requires:       perl(warnings)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_autouse
%endif
Conflicts:      perl < 4:5.30.1-451

%description autouse
If a module is not loaded yet, then the autouse declaration declares functions
in the current package. When these functions are called, they load the package
and substitute themselves with the correct definitions.

%package B
Summary:        Perl compiler backend
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.89
Requires:       perl(Data::Dumper)
Requires:       perl(overloading)
Requires:       perl(XSLoader)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_B
%endif
Conflicts:      perl-interpreter < 4:5.30.1-451

%description B
The "B" module supplies classes which allow a Perl program to delve into its
own innards. It is the module used to implement the backends of the Perl
compiler.

%package base
Summary:        Establish an ISA relationship with base classes at compile time
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        2.27
BuildArch:      noarch
Requires:       perl(Carp)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_base
%endif
Conflicts:      perl < 4:5.30.1-451

%description base
"base" module allows you to both load one or more modules, while setting up
inheritance from those modules at the same time.  Unless you are using the
"fields" pragma, consider this module discouraged in favor of the
lighter-weight "parent".

%package Benchmark
Summary:        Benchmark running times of Perl code
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.27
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Benchmark
%endif
BuildArch:      noarch
Conflicts:      perl-interpreter < 4:5.30.1-451

%description Benchmark
The Benchmark module encapsulates a number of routines to help you figure out
how long it takes to execute some code.

%if %{dual_life} || %{rebuild_from_scratch}
%package bignum
Summary:        Transparent big number support for Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        0.67
Requires:       perl(Carp)
# Math::BigInt::Lite is optional
Requires:       perl(Math::BigRat)
Requires:       perl(warnings)
BuildArch:      noarch
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_bignum
%endif
Conflicts:      perl < 4:5.22.0-348

%description bignum
This package attempts to make it easier to write scripts that use BigInts and
BigFloats in a transparent way.
%endif

%package blib
Summary:        Use uninstalled version of a package
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.07
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_blib
%endif
BuildArch:      noarch
Conflicts:      perl-interpreter < 4:5.30.1-451

%description blib
This module looks for MakeMaker-like "blib" directory structure starting in
given or current directory and working back up to five levels of directories.
It is intended for use on command line with -M option as a way of testing
arbitrary scripts against an uninstalled version of a package.

%if %{dual_life} || %{rebuild_from_scratch}
%package Carp
Summary:        Alternative warn and die for modules
Epoch:          0
# Real version 1.54
Version:        1.54
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Carp
%endif
BuildArch:      noarch

# Do not export unversioned module
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(Carp\\)\\s*$

%description Carp
The Carp routines are useful in your own modules because they act like
die() or warn(), but with a message which is more likely to be useful to a
user of your module. In the case of cluck, confess, and longmess that
context is a summary of every call in the call-stack. For a shorter message
you can use carp or croak which report the error as being from where your
module was called. There is no guarantee that that is where the error was,
but it is a good educated guess.
%endif

%package Class-Struct
Summary:        Declare struct-like data types as Perl classes
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        0.68
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Class_Struct
%endif
BuildArch:      noarch
Conflicts:      perl-interpreter < 4:5.30.1-451

%description Class-Struct
Class::Struct module exports a single function struct(). Given a list of
element names and types, and optionally a class name, struct() creates a
Perl 5 class that implements a struct-like data structure.

%if %{dual_life} || %{rebuild_from_scratch}
%package Compress-Raw-Bzip2
Summary:        Low-Level Interface to bzip2 compression library
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        2.213
Requires:       perl(Exporter), perl(File::Temp)
%if %{defined perl_bootstrap}
%gendep_perl_Compress_Raw_Bzip2
%endif

%description Compress-Raw-Bzip2
This module provides a Perl interface to the bzip2 compression library.
It is used by IO::Compress::Bzip2.

%package Compress-Raw-Zlib
Summary:        Low-Level Interface to the zlib compression library
License:        (GPL-1.0-or-later OR Artistic-1.0-Perl) AND Zlib
Epoch:          0
Version:        2.222
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Compress_Raw_Zlib
%endif

%description Compress-Raw-Zlib
This module provides a Perl interface to the zlib compression library.
It is used by IO::Compress::Zlib.
%endif

%package Config-Extensions
Summary:        Hash lookup of which Perl core extensions were built
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        0.03
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Config_Extensions
%endif
BuildArch:      noarch
Conflicts:      perl-interpreter < 4:5.30.1-451

%description Config-Extensions
The Config::Extensions module provides a hash %%Extensions containing all the
core extensions that were enabled for this perl.

%if %{dual_life} || %{rebuild_from_scratch}
%package Config-Perl-V
Summary:        Structured data retrieval of perl -V output
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        0.38
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Config_Perl_V
%endif
BuildArch:      noarch
Conflicts:      perl < 4:5.22.0-347

%description Config-Perl-V
The command "perl -V" will return you an excerpt from the %%Config::Config
hash combined with the output of "perl -V" that is not stored inside the hash,
but only available to the perl binary itself. This package provides Perl
module that will return you the output of "perl -V" in a structure.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package constant
Summary:        Perl pragma to declare constants
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.33
Requires:       perl(Carp)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_constant
%endif
BuildArch:      noarch
Conflicts:      perl < 4:5.16.3-264

%description constant
This pragma allows you to declare constants at compile-time:

use constant PI => 4 * atan2(1, 1);

When you declare a constant such as "PI" using the method shown above,
each machine your script runs upon can have as many digits of accuracy
as it can use. Also, your program will be easier to read, more likely
to be maintained (and maintained correctly), and far less likely to
send a space probe to the wrong planet because nobody noticed the one
equation in which you wrote 3.14195.

When a constant is used in an expression, Perl replaces it with its
value at compile time, and may then optimize the expression further.
In particular, any code in an "if (CONSTANT)" block will be optimized
away if the constant is false.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package CPAN
Summary:        Query, download and build perl modules from CPAN sites
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        2.38
Requires:       make
# Some subpackaged modules are not dual-lived. E.g. "open". If a distribution
# on CPAN declares a dependency on such module, CPAN client will fail,
# because the only provider is a perl distribution.
# Another issue is with dual-lived modules whose distribution actually does
# not declare all needed core dependencies and the installation would also
# fail.
# As a result, any CPAN client must run-require the complete perl.
Requires:       perl
# Prefer Archive::Tar and Compress::Zlib over tar and gzip
Requires:       perl(Archive::Tar) >= 1.50
Requires:       perl(base)
Requires:       perl(Data::Dumper)
%if !%{defined perl_bootstrap}
Requires:       perl(Devel::Size)
%endif
Requires:       perl(ExtUtils::Manifest)
%if !%{defined perl_bootstrap}
Requires:       perl(File::HomeDir) >= 0.65
%endif
Requires:       perl(File::Temp) >= 0.16
Requires:       perl(lib)
Requires:       perl(Net::Config)
Requires:       perl(Net::FTP)
Requires:       perl(POSIX)
Requires:       perl(Term::ReadLine)
%if !%{defined perl_bootstrap}
Requires:       perl(URI)
Requires:       perl(URI::Escape)
%endif
Requires:       perl(User::pwent)
# Optional but higly recommended:
%if !%{defined perl_bootstrap}
Requires:       perl(Archive::Zip)
Requires:       perl(Compress::Bzip2)
Requires:       perl(CPAN::Meta) >= 2.110350
%endif
Requires:       perl(Compress::Zlib)
Requires:       perl(Digest::MD5)
# CPAN encourages Digest::SHA strongly because of integrity checks
Requires:       perl(Digest::SHA)
Requires:       perl(Dumpvalue)
Requires:       perl(ExtUtils::CBuilder)
%if ! %{defined perl_bootstrap}
# Avoid circular deps local::lib -> Module::Install -> CPAN when bootstraping
# local::lib recommended by CPAN::FirstTime default choice, bug #1122498
Requires:       perl(local::lib)
%endif
Requires:       perl(Module::Build)
%if ! %{defined perl_bootstrap}
Requires:       perl(Text::Glob)
%endif
Provides:       cpan = %{version}
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_CPAN
%endif
BuildArch:      noarch

%description CPAN
The CPAN module automates or at least simplifies the make and install of
perl modules and extensions. It includes some primitive searching
capabilities and knows how to use LWP, HTTP::Tiny, Net::FTP and certain
external download clients to fetch distributions from the net.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package CPAN-Meta
Summary:        Distribution metadata for a CPAN dist
Epoch:          0
Version:        2.150010
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Requires:       perl(CPAN::Meta::YAML) >= 0.011
Requires:       perl(Encode)
Requires:       perl(JSON::PP) >= 2.27300
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_CPAN_Meta
%endif
BuildArch:      noarch

%description CPAN-Meta
Software distributions released to the CPAN include a META.json or, for
older distributions, META.yml, which describes the distribution, its
contents, and the requirements for building and installing the
distribution. The data structure stored in the META.json file is described
in CPAN::Meta::Spec.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package CPAN-Meta-Requirements
Summary:        Set of version requirements for a CPAN dist
Epoch:          0
# Real version 2.140
Version:        2.140
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
BuildArch:      noarch
# CPAN-Meta-Requirements used to have six decimal places
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(CPAN::Meta::Requirements\\)
Provides:       perl(CPAN::Meta::Requirements) = %{version}000
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_CPAN_Meta_Requirements
%endif

%description CPAN-Meta-Requirements
A CPAN::Meta::Requirements object models a set of version constraints like
those specified in the META.yml or META.json files in CPAN distributions.
It can be built up by adding more and more constraints, and it will reduce
them to the simplest representation.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package CPAN-Meta-YAML
Version:        0.020
Epoch:          0
Summary:        Read and write a subset of YAML for CPAN Meta files
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
BuildArch:      noarch
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_CPAN_Meta_YAML
%endif

%description CPAN-Meta-YAML
This module implements a subset of the YAML specification for use in reading
and writing CPAN metadata files like META.yml and MYMETA.yml. It should not be
used for any other general YAML parsing or generation task.
%endif


%if %{dual_life} || %{rebuild_from_scratch}
%package Data-Dumper
Summary:        Stringify perl data structures, suitable for printing and eval
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        2.192
Requires:       perl(B::Deparse)
Requires:       perl(bytes)
Requires:       perl(Scalar::Util)
Requires:       perl(XSLoader)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Data_Dumper
%endif

%description Data-Dumper
Given a list of scalars or reference variables, writes out their contents
in perl syntax. The references can also be objects. The content of each
variable is output in a single Perl statement. Handles self-referential
structures correctly.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%if %{with bdb}
%package DB_File
Summary:        Perl5 access to Berkeley DB version 1.x
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.859
Requires:       perl(Fcntl)
Requires:       perl(XSLoader)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_DB_File
%endif
Conflicts:      perl < 4:5.16.3-264

%description DB_File
DB_File is a module which allows Perl programs to make use of the facilities
provided by Berkeley DB version 1.x (if you have a newer version of DB, you
will be limited to functionality provided by interface of version 1.x). The
interface defined here mirrors the Berkeley DB interface closely.
%endif
%endif

%package DBM_Filter
Summary:        Filter DBM keys and values
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        0.07
Requires:       perl(Compress::Zlib)
Requires:       perl(Encode)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_DBM_Filter
%endif
BuildArch:      noarch
Conflicts:      perl-interpreter < 4:5.30.1-451

# Remove private redefinitions
# DBM_Filter redefines Tie::Hash, but does not load it.
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(Tie::Hash\\)$

%description DBM_Filter
This module provides an interface that allows filters to be applied to tied
hashes associated with DBM files.

%package debugger
Summary:        Perl debugger
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.60
BuildArch:      noarch
# File provides
Provides:       perl(dumpvar.pl) = %{perl_version}
Provides:       perl(perl5db.pl) = %{version}
Recommends:     perl(Carp)
Recommends:     perl(Config)
Requires:       perl(Cwd)
Recommends:     perl(Devel::Peek)
Requires:       perl(feature)
Recommends:     perl(IO::Handle)
Recommends:     perl(File::Basename)
Recommends:     perl(File::Path)
Requires:       perl(IO::Socket)
Requires:       perl(meta_notation) = %{perl_version}
Requires:       perl(mro)
%if !%{defined perl_bootstrap}
Suggests:       perl(PadWalker) >= 0.08
%endif
Recommends:     perl(POSIX)
Requires:       perl(Term::ReadLine)
# ??? Term::Rendezvous
Requires:       perl(threads)
Requires:       perl(threads::shared)
Requires:       perl(vars)
Requires:       perl(warnings)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_debugger
%endif
Conflicts:      perl < 4:5.30.1-451

%description debugger
This is the perl debugger. It is loaded automatically by Perl when you invoke
a script with "perl -d". There is also "DB" module contained for
a programmatic interface to the debugging API.

%package deprecate
Summary:        Perl pragma for deprecating the inclusion of a module in core
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        0.04
Requires:       perl(Carp)
Requires:       perl(Config)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_deprecate
%endif
BuildArch:      noarch
Conflicts:      perl-interpreter < 4:5.30.1-451

%description deprecate
"deprecate" pragma simplifies the maintenance of dual-life modules that will no
longer be included in the Perl core in a future Perl release, but are
still included currently. The purpose of the pragma is to alert users to the
status of such a module by issuing a warning that encourages them to install
the module from CPAN, so that a future upgrade to a perl which omits the
module will not break their code.

%package Devel-Peek
Summary:        A data debugging tool for the XS programmer
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.36
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Devel_Peek
%endif
Conflicts:      perl < 4:5.22.0-351

%description Devel-Peek
Devel::Peek contains functions which allows raw Perl data types to be
manipulated from a Perl script. This is used by those who do XS programming to
check that the data they are sending from C to Perl looks as they think it
should look.

%if %{dual_life} || %{rebuild_from_scratch}
%package Devel-PPPort
Summary:        Perl Pollution Portability header generator
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        3.73
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Devel_PPPort
%endif
Conflicts:      perl < 4:5.20.1-310

%description Devel-PPPort
Perl's API has changed over time, gaining new features, new functions,
increasing its flexibility, and reducing the impact on the C name space
environment (reduced pollution). The header file written by this module,
typically ppport.h, attempts to bring some of the newer Perl API features
to older versions of Perl, so that you can worry less about keeping track
of old releases, but users can still reap the benefit.
%endif

%package Devel-SelfStubber
Summary:        Generate stubs for a SelfLoading module
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.06
BuildArch:      noarch
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Devel_SelfStubber
%endif
Conflicts:      perl < 4:5.22.0-351

%description Devel-SelfStubber
Devel::SelfStubber prints the stubs you need to put in the module before the
__DATA__ token (or you can get it to print the entire module with stubs
correctly placed). The stubs ensure that if a method is called, it will get
loaded. They are needed specifically for inherited autoloaded methods.

%package diagnostics
Summary:        Produce verbose warning diagnostics
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.40
BuildArch:      noarch
# Match library exactly for diagnostics messages
Requires:       perl-libs = %{perl_epoch}:%{perl_version}-%{release}
Requires:       perl(Getopt::Std)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_diagnostics
%endif
Conflicts:      perl-utils < 5.30.1-451
Conflicts:      perl-interpreter < 4:5.30.1-451

%description diagnostics
The diagnostics module extends the terse diagnostics normally emitted by both
the perl compiler and the perl interpreter (from running perl with a -w switch
or "use warnings"), augmenting them with the more explicative and endearing
descriptions found in perldiag. splain tool explains perl messages found on
standard input.

%if %{dual_life} || %{rebuild_from_scratch}
%package Digest
Summary:        Modules that calculate message digests
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
# Epoch bump for clean upgrade over old standalone package
Epoch:          0
Version:        1.20
BuildArch:      noarch
Requires:       perl(MIME::Base64)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Digest
%endif

%description Digest
The Digest:: modules calculate digests, also called "fingerprints" or
"hashes", of some data, called a message. The digest is (usually)
some small/fixed size string. The actual size of the digest depend of
the algorithm used. The message is simply a sequence of arbitrary
bytes or bits.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Digest-MD5
Summary:        Perl interface to the MD5 Algorithm
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
# Epoch bump for clean upgrade over old standalone package
Epoch:          0
# Real version 2.59
Version:        2.59
Requires:       perl(XSLoader)
# Recommended
Requires:       perl(Digest::base) >= 1.00
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Digest_MD5
%endif

%description Digest-MD5
The Digest::MD5 module allows you to use the RSA Data Security Inc. MD5
Message Digest algorithm from within Perl programs. The algorithm takes as
input a message of arbitrary length and produces as output a 128-bit
"fingerprint" or "message digest" of the input.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Digest-SHA
Summary:        Perl extension for SHA-1/224/256/384/512
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        6.04
Requires:       perl(Carp)
# Recommended
Requires:       perl(Digest::base)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Digest_SHA
%endif

%description Digest-SHA
Digest::SHA is a complete implementation of the NIST Secure Hash
Standard.  It gives Perl programmers a convenient way to calculate
SHA-1, SHA-224, SHA-256, SHA-384, and SHA-512 message digests.  The
module can handle all types of input, including partial-byte data.
%endif

%package DirHandle
Summary:        Supply object methods for directory handles
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.05
BuildArch:      noarch
Requires:       perl(warnings)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_DirHandle
%endif
Conflicts:      perl < 4:5.30.1-451

%description DirHandle
There is no reason to use this module nowadays. The DirHandle module provides
an alternative interface to the opendir(), closedir(), readdir(), and
rewinddir() functions. Since Perl 5.6, opendir() alone has been all you need
for lexical handles.

%package doc
Summary:        Perl language documentation
License:        (GPL-1.0-or-later OR Artistic-1.0-Perl) AND Unicode-3.0 AND LicenseRef-Fedora-UltraPermissive
Epoch:          0
Version:        %{perl_version}
BuildArch:      noarch
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%endif
# For perldoc tool
Recommends:     perl-Pod-Perldoc
Conflicts:      perl < 4:5.30.1-451

%description doc
This is a documentation for Perl language. It's provided in POD and manual
page format.

%package Dumpvalue
Summary:        Screen dump of Perl data
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
# Real version 1.21
Version:        2.27
BuildArch:      noarch
Recommends:     perl(Devel::Peek)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Dumpvalue
%endif
Conflicts:      perl < 4:5.30.1-451

%description Dumpvalue
Dumpvalue module enables you to print a content of variables and other Perl
data structures.

%package DynaLoader
Summary:        Dynamically load C libraries into Perl code
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.57
Requires:       perl(Carp)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_DynaLoader
%endif
Conflicts:      perl < 4:5.30.1-451

%description DynaLoader
The DynaLoader module defines a standard generic interface to the dynamic
linking mechanisms available on many platforms. Its primary purpose is to
implement automatic dynamic loading of Perl modules. For a simpler interface,
see XSLoader module.

%if %{dual_life} || %{rebuild_from_scratch}
%package Encode
Summary:        Character encodings in Perl
License:        (GPL-1.0-or-later OR Artistic-1.0-Perl) AND Artistic-2.0
Epoch:          4
Version:        3.21
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Encode
%endif
Conflicts:      perl < 4:5.16.2-256

%description Encode
The Encode module provides the interface between Perl strings and the rest
of the system. Perl strings are sequences of characters.

%package encoding
Summary:        Write your Perl script in non-ASCII or non-UTF-8
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          4
Version:        3.00
# Keeping this sub-package arch-specific because it installs files into
# arch-specific directories.
Requires:       perl(Carp)
# Config not needed on perl ≥ 5.008
# Consider Filter::Util::Call as mandatory, bug #1165183, CPAN RT#100427
Requires:       perl(Filter::Util::Call)
# I18N::Langinfo is optional
# PerlIO::encoding is optional
Requires:       perl(utf8)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_encoding
%endif
Conflicts:      perl-Encode < 2:2.60-314

%description encoding
With the encoding pragma, you can write your Perl script in any encoding you
like (so long as the Encode module supports it) and still enjoy Unicode
support.

However, this encoding module is deprecated under perl 5.18. It uses
a mechanism provided by perl that is deprecated under 5.18 and higher, and may
be removed in a future version.GPL-1.0-or-later OR Artistic-1.0-Perl

The easiest and the best alternative is to write your script in UTF-8.

%package Encode-devel
Summary:        Character encodings in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          4
Version:        3.21
Requires:       %{name}-Encode = %{epoch}:%{version}-%{release}
Recommends:     perl-devel
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Encode_devel
%endif
BuildArch:      noarch

%description Encode-devel
enc2xs builds a Perl extension for use by Encode from either Unicode Character
Mapping files (.ucm) or Tcl Encoding Files (.enc). You can use enc2xs to add
your own encoding to perl. No knowledge of XS is necessary.
%endif

%package encoding-warnings
Summary:        Warn on implicit encoding conversions
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        0.14
BuildArch:      noarch
Requires:       perl(Carp)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_encoding_warnings
%endif
Conflicts:      perl < 4:5.30.1-451

%description encoding-warnings
As of Perl 5.26.0, this module has no effect. The internal Perl feature that
was used to implement this module has been removed.  Hence, if you load this
module on Perl 5.26.0, you will get one warning that the module is no longer
supported; and the module will do nothing thereafter.

%package English
Summary:        Nice English or awk names for ugly punctuation variables
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.11
Requires:       perl(Carp)
Requires:       perl(warnings)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_English
%endif
BuildArch:      noarch
Conflicts:      perl-interpreter < 4:5.30.1-451

%description English
This module provides aliases for the built-in variables whose names no one
seems to like to read.

%if %{dual_life} || %{rebuild_from_scratch}
%package Env
Summary:        Perl module that imports environment variables as scalars or arrays
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.06
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Env
%endif
BuildArch:      noarch
Conflicts:      perl < 4:5.16.2-265

%description Env
Perl maintains environment variables in a special hash named %%ENV. For when
this access method is inconvenient, the Perl module Env allows environment
variables to be treated as scalar or array variables.
%endif

%package Errno
Summary:        System errno constants
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.38
# Errno.pm bakes in kernel version at build time and compares it against
# $Config{osvers} at run time. Match exact interpreter build. Bug #1393421.
%if !0%{?os2_version}
Requires:       perl-libs%{?_isa} = %{perl_epoch}:%{perl_version}-%{release}
%else
Requires:       perl-libs = %{perl_epoch}:%{perl_version}-%{release}
%endif
Requires:       perl(Carp)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Errno
%endif
Conflicts:      perl < 4:5.22.0-351

%description Errno
"Errno" defines and conditionally exports all the error constants defined in
your system "errno.h" include file. It has a single export tag, ":POSIX",
which will export all POSIX defined error numbers.

%if %{dual_life} || %{rebuild_from_scratch}
%package experimental
Summary:        Experimental features made easy
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        0.035
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_experimental
%endif
BuildArch:      noarch
Conflicts:      perl < 4:5.20.0-303

%description experimental
This pragma provides an easy and convenient way to enable or disable
experimental features.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Exporter
Summary:        Implements default import method for modules
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        5.79
Requires:       perl(Carp) >= 1.05
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Exporter
%endif
BuildArch:      noarch
Conflicts:      perl < 4:5.16.2-265

%description Exporter
The Exporter module implements an import method which allows a module to
export functions and variables to its users' name spaces. Many modules use
Exporter rather than implementing their own import method because Exporter
provides a highly flexible interface, with an implementation optimized for
the common case.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package ExtUtils-CBuilder
Summary:        Compile and link C code for Perl modules
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        0.280242
BuildArch:      noarch
# C and C++ compilers are highly recommended because compiling code is the
# purpose of ExtUtils::CBuilder, bug #1547165
Requires:       gcc
Requires:       gcc-c++
Requires:       perl-devel
Requires:       perl(DynaLoader)
Requires:       perl(ExtUtils::Mksymlists)
Requires:       perl(File::Spec) >= 3.13
Requires:       perl(Perl::OSType) >= 1
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_ExtUtils_CBuilder
%endif

%description ExtUtils-CBuilder
This module can build the C portions of Perl modules by invoking the
appropriate compilers and linkers in a cross-platform manner. It was motivated
by the Module::Build project, but may be useful for other purposes as well.
%endif

%package ExtUtils-Constant
Summary:        Generate XS code to import C header constants
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        0.25
BuildArch:      noarch
Requires:       perl(Data::Dumper)
# ExtUtils::Constant::Aaargh56Hash not used on recent Perls
# FileHandle not used on recent Perls
# POSIX not used on recent Perls
Conflicts:      perl-interpreter < 4:5.30.1-451
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_ExtUtils_Constant
%endif

%description ExtUtils-Constant
ExtUtils::Constant facilitates generating C and XS wrapper code to allow
Perl modules to AUTOLOAD constants defined in C library header files.

%if %{dual_life} || %{rebuild_from_scratch}
%package ExtUtils-Command
Summary:        Perl routines to replace common UNIX commands in Makefiles
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          2
Version:        7.76
BuildArch:      noarch
Conflicts:      perl < 4:5.20.1-312
Requires:       perl(File::Find)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_ExtUtils_Command
%endif

%description ExtUtils-Command
This Perl module is used to replace common UNIX commands. In all cases the
functions work with @ARGV rather than taking arguments. This makes them
easier to deal with in Makefiles.
%endif

%package ExtUtils-Embed
Summary:        Utilities for embedding Perl in C/C++ applications
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.35
Requires:       perl-devel
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_ExtUtils_Embed
%endif
BuildArch:      noarch

%description ExtUtils-Embed
Utilities for embedding Perl in C/C++ applications.


%if %{dual_life} || %{rebuild_from_scratch}
%package ExtUtils-Install
Summary:        Install files from here to there
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        2.22
BuildArch:      noarch
Requires:       perl(AutoSplit)
Requires:       perl(File::Compare)
Requires:       perl(Data::Dumper)
Recommends:     perl(POSIX)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_ExtUtils_Install
%endif

%description ExtUtils-Install
Handles the installing and uninstalling of perl modules, scripts, man
pages, etc.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package ExtUtils-MakeMaker
Summary:        Create a module Makefile
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          2
Version:        7.76
# These dependencies are weak in order to relieve building noarch
# packages from perl-devel and gcc. See bug #1547165.
# If an XS module is built, the generated Makefile executes gcc.
Recommends:     gcc
# If an XS module is built, code generated from XS will be compiled and it
# includes Perl header files.
Recommends:     perl-devel
Requires:       perl(Data::Dumper)
Requires:       perl(DynaLoader)
Requires:       perl(ExtUtils::Command)
Requires:       perl(ExtUtils::Install)
Requires:       perl(ExtUtils::Manifest)
Requires:       perl(File::Find)
Requires:       perl(Getopt::Long)
# Optional Pod::Man is needed for generating manual pages from POD
Requires:       perl(Pod::Man)
Requires:       perl(POSIX)
Requires:       perl(Test::Harness)
Requires:       perl(version)
# If an XS module is compiled, xsubpp(1) is needed
Requires:       perl-ExtUtils-ParseXS
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_ExtUtils_MakeMaker
%endif
BuildArch:      noarch

# Filter false DynaLoader provides. Versioned perl(DynaLoader) keeps
# unfiltered on perl package, no need to reinject it.
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(DynaLoader\\)\\s*$
%global __provides_exclude %__provides_exclude|^perl\\(ExtUtils::MakeMaker::_version\\)

%description ExtUtils-MakeMaker
Create a module Makefile.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package ExtUtils-Manifest
Summary:        Utilities to write and check a MANIFEST file
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          1
Version:        1.75
Requires:       perl(File::Path)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_ExtUtils_Manifest
%endif
BuildArch:      noarch

%description ExtUtils-Manifest
%{summary}.
%endif

%package ExtUtils-Miniperl
Summary:        Write the C code for perlmain.c
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.14
Requires:       perl-devel
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_ExtUtils_Miniperl
%endif
BuildArch:      noarch

%description ExtUtils-Miniperl
writemain() takes an argument list of directories containing archive libraries
that relate to perl modules and should be linked into a new perl binary. It
writes a corresponding perlmain.c file that is a plain C file containing all
the bootstrap code to make the If the first argument to writemain() is a
reference to a scalar it is used as the file name to open for output. Any other
reference is used as the file handle to write to. Otherwise output defaults to
STDOUT.

%if %{dual_life} || %{rebuild_from_scratch}
%if !0%{?os2_version}
%package ExtUtils-MM-Utils
Summary:        ExtUtils::MM methods without dependency on ExtUtils::MakeMaker
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          1
# Real version 7.11
# Dual-life ExtUtils-MakeMaker generate it with its version
Version:        7.44
BuildArch:      noarch
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_ExtUtils_MM_Utils
%endif

%description ExtUtils-MM-Utils
This is a collection of ExtUtils::MM subroutines that are used by many
other modules but that do not need full-featured ExtUtils::MakeMaker. The
issue with ExtUtils::MakeMaker is it pulls in Perl header files and that
is an overkill for small subroutines.
%endif
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package ExtUtils-ParseXS
Summary:        Module and a script for converting Perl XS code into C code
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        3.57
Requires:       perl(fields)
Requires:       perl(Hash::Util)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_ExtUtils_ParseXS
%endif
Conflicts:      perl-interpreter < 4:5.30.1-451
BuildArch:      noarch

%description ExtUtils-ParseXS
ExtUtils::ParseXS will compile XS code into C code by embedding the constructs
necessary to let C functions manipulate Perl values and creates the glue
necessary to let Perl access those functions.
%endif

%package Fcntl
Summary:        File operation options
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.20
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Fcntl
%endif
Conflicts:      perl-interpreter < 4:5.30.1-451

%description Fcntl
Fcntl module provides file operation related options.

%package fields
Summary:        Compile-time class fields
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
# Real version 2.25
Version:        2.27
BuildArch:      noarch
Requires:       perl(base)
Requires:       perl(Carp)
Requires:       perl(Hash::Util)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_fields
%endif
Conflicts:      perl < 4:5.30.1-451

%description fields
The "fields" pragma enables compile-time and run-time verified class fields.

%package File-Basename
Summary:        Parse file paths into directory, file name, and suffix
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        2.86
BuildArch:      noarch
Requires:       perl(Carp)
Requires:       perl(re)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_File_Basename
%endif
Conflicts:      perl < 4:5.30.1-451

%description File-Basename
These routines allow you to parse file paths into their directory, file name,
and suffix.

%package File-Compare
Summary:        Compare files or file handles
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
# Normalized version
Version:        1.100.800
BuildArch:      noarch
Requires:       perl(Carp)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_File_Compare
%endif
Conflicts:      perl < 4:5.30.1-451

%description File-Compare
A File::Compare Perl module provides functions for comparing a content of two
files specified by a file name or a file handle.

%package File-Copy
Summary:        Copy files or file handles
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        2.41
BuildArch:      noarch
Requires:       perl(Carp)
Requires:       perl(File::Basename)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_File_Copy
%endif
Conflicts:      perl < 4:5.30.1-451

%description File-Copy
A File::Copy module provides two basic functions, copy and move, which are
useful for getting the contents of a file from one place to another.

%package File-DosGlob
Summary:        DOS-like globbing
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.12
Requires:       perl(Text::ParseWords)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_File_DosGlob
%endif
Conflicts:      perl-interpreter < 4:5.30.1-451

%description File-DosGlob
This Perl module implements DOS-like globbing with a few enhancements. It
is largely compatible with perlglob.exe in all but one respect--it understands
wild cards in directory components.

%if %{dual_life} || %{rebuild_from_scratch}
%package File-Fetch
Summary:        Generic file fetching mechanism
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.04
Requires:       perl(IPC::Cmd) >= 0.36
Requires:       perl(Module::Load::Conditional) >= 0.04
Requires:       perl(Params::Check) >= 0.07
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_File_Fetch
%endif
BuildArch:      noarch

%description File-Fetch
File::Fetch is a generic file fetching mechanism.
%endif

%package File-Find
Summary:        Traverse a directory tree
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.44
Recommends:     perl(Scalar::Util)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_File_Find
%endif
BuildArch:      noarch
Conflicts:      perl-interpreter < 4:5.30.1-451

%description File-Find
These are functions for searching through directory trees doing work on each
file found similar to the Unix find command.

%if %{dual_life} || %{rebuild_from_scratch}
%package File-Path
Summary:        Create or remove directory trees
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        2.18
Requires:       perl(Carp)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_File_Path
%endif
BuildArch:      noarch
Conflicts:      perl < 4:5.16.2-265

%description File-Path
This module provides a convenient way to create directories of arbitrary
depth and to delete an entire directory subtree from the file system.
%endif

%package File-stat
Summary:        By-name interface to Perl built-in stat functions
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.14
BuildArch:      noarch
Requires:       perl(Symbol)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_File_stat
%endif
Conflicts:      perl < 4:5.30.1-451

%description File-stat
This module overrides the core stat() and lstat() functions, replacing them
with versions that return File::stat objects. This object has methods that
return the similarly named structure field name from the stat(2) function.

%if %{dual_life} || %{rebuild_from_scratch}
%package File-Temp
Summary:        Return name and handle of a temporary file safely
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          1
# Normalized version
Version:        0.231.100
BuildArch:      noarch
Requires:       perl(File::Path) >= 2.06
Requires:       perl(POSIX)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_File_Temp
%endif
Conflicts:      perl < 4:5.16.2-265

%description File-Temp
File::Temp can be used to create and open temporary files in a safe way.
There is both a function interface and an object-oriented interface. The
File::Temp constructor or the tempfile() function can be used to return the
name and the open file handle of a temporary file. The tempdir() function
can be used to create a temporary directory.
%endif

%package FileCache
Summary:        Keep more files open than the system permits
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.10
BuildArch:      noarch
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_FileCache
%endif
Conflicts:      perl-interpreter < 4:5.30.1-451

%description FileCache
The "cacheout" function will make sure that there's a file handle open
for reading or writing available as the path name you give it. It
automatically closes and re-opens files if you exceed your system
maximum number of file descriptors, or the suggested maximum.

%package FileHandle
Summary:        Object methods for file handles
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        2.05
BuildArch:      noarch
Requires:       perl(Exporter)
Recommends:     perl(Fcntl)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_FileHandle
%endif
Conflicts:      perl-interpreter < 4:5.30.1-451

%description FileHandle
This is an object-oriented interface for opening files and performing
input/output operations on them.

%package filetest
Summary:        Perl pragma to control the filetest permission operators
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.03
BuildArch:      noarch
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_filetest
%endif
Conflicts:      perl < 4:5.30.1-451

%description filetest
The default behavior of file test operators (e.g. "-r") is to use the simple
mode bits as returned by the stat() family of system calls. However, many
operating systems have additional features to define more complex access
rights, for example ACLs (Access Control Lists). For such environments, "use
filetest" may help the permission operators to return results more consistent
with other tools.

%if %{dual_life} || %{rebuild_from_scratch}
# FIXME Filter-Simple? version?
%package Filter
Summary:        Perl source filters
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          2
Version:        1.64
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Filter
%endif

%description Filter
Source filters alter the program text of a module before Perl sees it, much as
a C preprocessor alters the source text of a C program before the compiler
sees it.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Filter-Simple
Summary:        Simplified Perl source filtering
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        0.96
BuildArch:      noarch
Conflicts:      perl < 4:5.20.1-312
Requires:       perl(Text::Balanced) >= 1.97
Requires:       perl(warnings)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Filter_Simple
%endif

%description Filter-Simple
The Filter::Simple Perl module provides a simplified interface to
Filter::Util::Call; one that is sufficient for most common cases.
%endif

%package FindBin
Summary:        Locate a directory of an original Perl script
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.54
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_FindBin
%endif
BuildArch:      noarch
Conflicts:      perl-interpreter < 4:5.30.1-451

%description FindBin
Locates the full path to the script bin directory to allow the use of paths
relative to the bin directory.

%if %{with gdbm}
%package GDBM_File
Summary:        Perl5 access to the gdbm library
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          1
Version:        1.24
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_GDBM_File
%endif
Conflicts:      perl-interpreter < 4:5.30.1-451

%description GDBM_File
GDBM_File is a module which allows Perl programs to make use of the facilities
provided by the GNU gdbm library.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Getopt-Long
Summary:        Extended processing of command line options
License:        GPL-2.0-or-later OR Artistic-1.0-Perl
Epoch:          1
Version:        2.58
Requires:       perl(overload)
Requires:       perl(Text::ParseWords)
# Recommended:
Requires:       perl(Pod::Usage) >= 1.14
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Getopt_Long
%endif
BuildArch:      noarch
Conflicts:      perl < 4:5.16.3-268

%description Getopt-Long
The Getopt::Long module implements an extended getopt function called
GetOptions(). It parses the command line from @ARGV, recognizing and removing
specified options and their possible values.  It adheres to the POSIX syntax
for command line options, with GNU extensions. In general, this means that
options have long names instead of single letters, and are introduced with
a double dash "--". Support for bundling of command line options, as was the
case with the more traditional single-letter approach, is provided but not
enabled by default.
%endif

%package Getopt-Std
Summary:        Process single-character switches with switch clustering
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.14
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Getopt_Std
%endif
BuildArch:      noarch
Conflicts:      perl-interpreter < 4:5.30.1-451

%description Getopt-Std
The Getopt::Std module provides functions for processing single-character
switches with switch clustering. Pass one argument which is a string
containing all switches to be recognized.

%package Hash-Util
Summary:        General-utility hash subroutines
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        0.32
Requires:       perl(Hash::Util::FieldHash)
Requires:       perl(XSLoader)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Hash_Util
%endif
Conflicts:      perl-interpreter < 4:5.30.1-451

%description Hash-Util
Hash::Util contains special functions for manipulating hashes that don't
really warrant a keyword.

%package Hash-Util-FieldHash
Summary:        Support for inside-out classes
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.27
Requires:       perl(XSLoader)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Hash_Util_FieldHash
%endif
Conflicts:      perl-interpreter < 4:5.30.1-451

%description Hash-Util-FieldHash
Hash::Util::FieldHash offers a number of functions in support of the
inside-out technique of class construction.

%package if
Summary:        Use a Perl module if a condition holds
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
# Normalized 0.0610
Version:        0.61.000
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_if
%endif
BuildArch:      noarch
Conflicts:      perl-interpreter < 4:5.30.1-451

%description if
The "if" module is used to conditionally load another module.

%package IO
Summary:        Perl input/output modules
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.55
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_IO
%endif
Conflicts:      perl < 4:5.22.0-351

%description IO
This is a collection of Perl input/output modules.

%if %{dual_life} || %{rebuild_from_scratch}
%package IO-Compress
Summary:        IO::Compress wrapper for modules
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        2.213
Obsoletes:      perl-Compress-Zlib <= 2.020
Provides:       perl(IO::Uncompress::Bunzip2)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_IO_Compress
%endif
BuildArch:      noarch

%description IO-Compress
This module is the base class for all IO::Compress and IO::Uncompress modules.
This module is not intended for direct use in application code. Its sole
purpose is to to be sub-classed by IO::Compress modules.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package IO-Socket-IP
Summary:        Drop-in replacement for IO::Socket::INET supporting both IPv4 and IPv6
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        0.43
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_IO_Socket_IP
%endif
BuildArch:      noarch
Conflicts:      perl < 4:5.20.0-303

%description IO-Socket-IP
This module provides a protocol-independent way to use IPv4 and IPv6
sockets, as a drop-in replacement for IO::Socket::INET. Most constructor
arguments and methods are provided in a backward-compatible way.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package IO-Zlib
Summary:        Perl IO:: style interface to Compress::Zlib
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        1.15
BuildRequires:  gzip
# The code defaults to Compress::Zlib, but a user can override it to gzip by
# importing :gzip_external symbol
Requires:       gzip
Requires:       perl(Compress::Zlib) >= 2
# IO::Handle used if gzip backend is requested
Requires:       perl(IO::Handle)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_IO_Zlib
%endif
BuildArch:      noarch

%description IO-Zlib
IO::Zlib provides an IO:: style interface to Compress::Zlib and hence to
gzip/zlib-compressed files. It provides many of the same methods as the
IO::Handle interface.
%endif


%if %{dual_life} || %{rebuild_from_scratch}
%package IPC-Cmd
Summary:        Finding and running system commands made easy
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
# Epoch bump for clean upgrade over old standalone package
Epoch:          2
Version:        1.04
%if !0%{?os2_version}
Requires:       perl(ExtUtils::MM::Utils)
%endif
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_IPC_Cmd
%endif
BuildArch:      noarch

%description IPC-Cmd
IPC::Cmd allows you to run commands, interactively if desired, in a platform
independent way, but have them still work.
%endif

%package IPC-Open3
Summary:        Open a process for reading, writing, and error handling
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.24
Requires:       perl(Fcntl)
Requires:       perl(IO::Pipe)
Requires:       perl(POSIX)
Requires:       perl(warnings)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_IPC_Open3
%endif
BuildArch:      noarch
Conflicts:      perl-interpreter < 4:5.30.1-451

%description IPC-Open3
These are functions that spawn a given command and connects the standard
output of the command for reading, standard output for writing, and standard
error output for handling the errors.

%if %{dual_life} || %{rebuild_from_scratch}
%package IPC-SysV
Summary:        Object interface to System V IPC
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        2.09
Requires:       perl(DynaLoader)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_IPC_SysV
%endif
Conflicts:      perl < 4:5.22.0-351

%description IPC-SysV
This is an object interface for System V messages, semaphores, and
inter-process calls.
%endif

%package I18N-Collate
Summary:        Compare 8-bit scalar data according to the current locale
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.02
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_I18N_Collate
%endif
BuildArch:      noarch
Conflicts:      perl-interpreter < 4:5.30.1-451

%description I18N-Collate
This module provides you with objects that will collate according to your
national character set. This module is deprecated. See the perllocale manual
page for further information.

%package I18N-Langinfo
Summary:        Query locale information
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        0.24
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_I18N_Langinfo
%endif
Conflicts:      perl-interpreter < 4:5.30.1-451

%description I18N-Langinfo
The langinfo() function queries various locale information that can be used to
localize output and user interfaces. It uses the current underlying locale,
regardless of whether or not it was called from within the scope of "use
locale".

%package I18N-LangTags
Summary:        Functions for dealing with RFC 3066 language tags
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        0.45
Requires:       perl(integer)
Requires:       perl(warnings)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_I18N_LangTags
%endif
BuildArch:      noarch
Conflicts:      perl-interpreter < 4:5.30.1-451

%description I18N-LangTags
Language tags are a formalism, described in RFC 3066, for declaring what
language form (language and possibly dialect) a given chunk of information is
in. This library provides functions for common tasks involving language tags
as they are needed in a variety of protocols and applications.

%if %{dual_life} || %{rebuild_from_scratch}
%package HTTP-Tiny
Summary:        A small, simple, correct HTTP/1.1 client
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        0.090
Requires:       perl(bytes)
Requires:       perl(Carp)
Requires:       perl(IO::Socket)
Requires:       perl(Time::Local)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_HTTP_Tiny
%endif
BuildArch:      noarch

%description HTTP-Tiny
This is a very simple HTTP/1.1 client, designed primarily for doing simple GET 
requests without the overhead of a large framework like LWP::UserAgent.
It is more correct and more complete than HTTP::Lite. It supports proxies 
(currently only non-authenticating ones) and redirection. It also correctly 
resumes after EINTR.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package JSON-PP
Summary:        JSON::XS compatible pure-Perl module
Epoch:          1
Version:        4.16
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
BuildArch:      noarch
Requires:       perl(Data::Dumper)
Requires:       perl(Encode)
Requires:       perl(Math::BigFloat)
Requires:       perl(Math::BigInt)
Requires:       perl(Scalar::Util)
Requires:       perl(subs)
%if %{defined perl_bootstrap}
Requires:       %perl_compat 
%gendep_perl_JSON_PP
%endif
Conflicts:      perl-JSON < 2.50

%description JSON-PP
JSON::XS is the fastest and most proper JSON module on CPAN. It is written by
Marc Lehmann in C, so must be compiled and installed in the used environment.
JSON::PP is a pure-Perl module and is compatible with JSON::XS.
%endif

%package less
Summary:        Perl pragma to request less of something
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        0.03
BuildArch:      noarch
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_less
%endif
Conflicts:      perl < 4:5.30.1-451

%description less
"use less ...;" is a Perl user-pragma. If you're very lucky some code you're
using will know that you asked for less CPU usage or RAM or fat or... we just
can't know.

%package lib
Summary:        Manipulate @INC at compile time
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        0.65
Requires:       perl(Carp)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_lib
%endif
Conflicts:      perl-interpreter < 4:5.30.1-451

%description lib
This module simplifies the manipulation of @INC at compile time.

%if %{dual_life} || %{rebuild_from_scratch}
%package libnet
Summary:        Perl clients for various network protocols
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        3.15
Requires:       perl(File::Basename)
Requires:       perl(IO::Socket) >= 1.05
# Prefer IO::Socket::IP over IO::Socket::INET6 and IO::Socket::INET
Requires:       perl(IO::Socket::IP) >= 0.20
Requires:       perl(POSIX)
Requires:       perl(Socket) >= 2.016
Requires:       perl(utf8)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_libnet
%endif
BuildArch:      noarch
Conflicts:      perl < 4:5.22.0-347

%description libnet
This is a collection of Perl modules which provides a simple and
consistent programming interface (API) to the client side of various
protocols used in the internet community.
%endif

%package libnetcfg
Summary:        Configure libnet
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          %perl_epoch
Version:        %perl_version
# Net::Config is optional
BuildArch:      noarch
%if %{defined perl_bootstrap}
%gendep_perl_libnetcfg
%endif
Conflicts:      perl-devel < 4:5.22.0-347

%description libnetcfg
The libnetcfg utility can be used to configure the libnet.

%package locale
Summary:        Pragma to use or avoid POSIX locales for built-in operations
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.13
Requires:       perl(Carp)
Requires:       perl(POSIX)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_locale
%endif
BuildArch:      noarch
Conflicts:      perl-interpreter < 4:5.30.1-451

%description locale
This pragma tells the compiler to enable (or disable) the use of POSIX locales
for built-in operations (for example, LC_CTYPE for regular expressions,
LC_COLLATE for string comparison, and LC_NUMERIC for number formatting). Each
"use locale" or "no locale" affects statements to the end of the enclosing
block.

%if %{dual_life} || %{rebuild_from_scratch}
%package Locale-Maketext
Summary:        Framework for localization
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.33
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Locale_Maketext
%endif
BuildArch:      noarch
Conflicts:      perl < 4:5.16.3-268

%description Locale-Maketext
It is a common feature of applications (whether run directly, or via the Web)
for them to be "localized" -- i.e., for them to present an English interface
to an English-speaker, a German interface to a German-speaker, and so on for
all languages it's programmed with. Locale::Maketext is a framework for
software localization; it provides you with the tools for organizing and
accessing the bits of text and text-processing code that you need for
producing localized applications.
%endif

%package Locale-Maketext-Simple
Summary:        Simple interface to Locale::Maketext::Lexicon
License:        MIT
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        0.21
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Locale_Maketext_Simple
%endif
BuildArch:      noarch

%description Locale-Maketext-Simple
This module is a simple wrapper around Locale::Maketext::Lexicon, designed
to alleviate the need of creating Language Classes for module authors.

%if %{dual_life} || %{rebuild_from_scratch}
%package Math-BigInt
Summary:        Arbitrary-size integer and float mathematics
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          1
# Real version 2.005002
Version:        2.0050.02
Requires:       perl(Carp)
# File::Spec not used on recent perl
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Math_BigInt
%endif
BuildArch:      noarch
Conflicts:      perl < 4:5.22.0-347

# Do not export unversioned module
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(Math::BigInt\\)\\s*$

%description Math-BigInt
This provides Perl modules for arbitrary-size integer and float mathematics.

%package Math-BigInt-FastCalc
Summary:        Math::BigInt::Calc XS implementation
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
# Version normalized to dot format
# Real version 0.5020
Version:        0.502.000
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Math_BigInt_FastCalc
%endif
Conflicts:      perl < 4:5.22.0-348

%description Math-BigInt-FastCalc
This package provides support for faster big integer calculations.
%endif

%package Math-Complex
Summary:        Complex numbers and trigonometric functions
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.63
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Math_Complex
%endif
BuildArch:      noarch
Conflicts:      perl < 4:5.22.0-348

%description Math-Complex
This package lets you create and manipulate complex numbers. By default, Perl
limits itself to real numbers, but an extra "use" statement brings full
complex support, along with a full set of mathematical functions typically
associated with and/or extended to complex numbers.

%package Memoize
Summary:        Transparently speed up functions by caching return values
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.17
# Keep Time::HiRes optional
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Memoize
%endif
BuildArch:      noarch
Conflicts:      perl < 4:5.22.0-350

%description Memoize
Memoizing a function makes it faster by trading space for time. It does
this by caching the return values of the function in a table. If you call
the function again with the same arguments, memoize jumps in and gives
you the value out of the table, instead of letting the function compute
the value all over again.

%package meta-notation
Summary:        Change nonprintable characters below 0x100 into printables
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        %{perl_version}
BuildArch:      noarch
Provides:       perl(meta_notation) = %{perl_version}
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_meta_notation
%endif
Conflicts:      perl < 4:5.30.1-451

%description meta-notation
Returns a copy of the input string with the nonprintable characters below
0x100 changed into printables. Any ASCII printables or above 0xFF are
unchanged.

%if %{dual_life} || %{rebuild_from_scratch}
%package MIME-Base64
Summary:        Encoding and decoding of Base64 and quoted-printable strings
# cpan/MIME-Base64/Base64.xs:   (GPL-1.0-or-later OR Artistic-1.0-Perl) and MIT (Bellcore's part)
# Other files:                  GPL-1.0-or-later OR Artistic-1.0-Perl
License:        (GPL-1.0-or-later OR Artistic-1.0-Perl) AND MIT
Epoch:          0
Version:        3.16
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_MIME_Base64
%endif
Conflicts:      perl < 4:5.22.0-347

%description MIME-Base64
This package contains a Base64 encoder/decoder and a quoted-printable
encoder/decoder. These encoding methods are specified in RFC 2045 - MIME
(Multipurpose Internet Mail Extensions).
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Module-CoreList
Summary:        What modules are shipped with versions of perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          1
Version:        5.20260329
Requires:       perl(List::Util)
Requires:       perl(version) >= 0.88
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Module_CoreList
%endif
BuildArch:      noarch

%description Module-CoreList
Module::CoreList provides information on which core and dual-life modules
are shipped with each version of perl.

%package Module-CoreList-tools
Summary:        Tool for listing modules shipped with perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          1
Version:        5.20260329
Requires:       perl(feature)
Requires:       perl(version) >= 0.88
Requires:       perl-Module-CoreList = %{epoch}:%{version}-%{release}
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Module_CoreList_tools
%endif
# The files were distributed with perl.spec's subpackage
# perl-Module-CoreList <= 1:5.020001-309
Conflicts:      perl-Module-CoreList < 1:5.020001-310
BuildArch:      noarch

%description Module-CoreList-tools
This package provides a corelist(1) tool which can be used to query what
modules were shipped with given perl version.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Module-Load
Summary:        Runtime require of both modules and files
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        0.36
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Module_Load
%endif
BuildArch:      noarch

%description Module-Load
Module::Load eliminates the need to know whether you are trying to require
either a file or a module.
%endif


%if %{dual_life} || %{rebuild_from_scratch}
%package Module-Load-Conditional
Summary:        Looking up module information / loading at runtime
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        0.74
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Module_Load_Conditional
%endif
BuildArch:      noarch

%description Module-Load-Conditional
Module::Load::Conditional provides simple ways to query and possibly load any
of the modules you have installed on your system during runtime.
%endif


%package Module-Loaded
Summary:        Mark modules as loaded or unloaded
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        0.08
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Module_Loaded
%endif
BuildArch:      noarch

%description Module-Loaded
When testing applications, often you find yourself needing to provide
functionality in your test environment that would usually be provided by
external modules. Rather than munging the %%INC by hand to mark these external
modules as loaded, so they are not attempted to be loaded by perl, this module
offers you a very simple way to mark modules as loaded and/or unloaded.


%if %{dual_life} || %{rebuild_from_scratch}
%package Module-Metadata
Summary:        Gather package and POD information from perl module files
Epoch:          0
Version:        1.000038
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
BuildArch:      noarch
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Module_Metadata
%endif

%description Module-Metadata
Gather package and POD information from perl module files
%endif

%package mro
Summary:        Method resolution order
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.29
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_mro
%endif
Conflicts:      perl-interpreter < 4:5.30.1-451

%description mro
The "mro" name space provides several utilities for dealing with method
resolution order and method caching in general.

%if %{with gdbm}
%package NDBM_File
Summary:        Tied access to ndbm files
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.18
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_NDBM_File
%endif
Conflicts:      perl-interpreter < 4:5.30.1-451

%description NDBM_File
NDBM_File establishes a connection between a Perl hash variable and a file in
ndbm format. You can manipulate the data in the file just as if it were in
a Perl hash, but when your program exits, the data will remain in the file, to
be used the next time your program runs.
%endif

%package Net
Summary:        By-name interface to Perl built-in network resolver
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.04
BuildArch:      noarch
Requires:       perl(Socket)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Net
%endif
Conflicts:      perl-interpreter < 4:5.30.1-451

%description Net
This package provide object-oriented interface to Perl built-in gethost*(),
getnet*(), getproto*(), and getserv*() functions.

%if %{dual_life} || %{rebuild_from_scratch}
%package Net-Ping
Summary:        Check a remote host for reachability
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        2.76
Requires:       perl(IO::Socket::INET)
# Keep Net::Ping::External optional
Suggests:       perl(Net::Ping::External)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Net_Ping
%endif
BuildArch:      noarch
Conflicts:      perl < 4:5.22.0-350

%description Net-Ping
Net::Ping module contains methods to test the reachability of remote hosts on
a network.
%endif

%package NEXT
Summary:        Pseudo-class that allows method redispatch
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        0.69
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_NEXT
%endif
BuildArch:      noarch
Conflicts:      perl-interpreter < 4:5.30.1-451

%description NEXT
The NEXT module adds a pseudo-class named "NEXT" to any program that uses it.
If a method "m" calls "$self->NEXT::m()", the call to "m" is redispatched as
if the calling method had not originally been found.

%if %{with gdbm}
%package ODBM_File
Summary:        Tied access to odbm files
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.20
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_ODBM_File
%endif
Conflicts:      perl-interpreter < 4:5.30.1-451

%description ODBM_File
ODBM_File establishes a connection between a Perl hash variable and a file in
odbm format. You can manipulate the data in the file just as if it were in
a Perl hash, but when your program exits, the data will remain in the file, to
be used the next time your program runs.
%endif

%package Opcode
Summary:        Disable named opcodes when compiling a perl code
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.69
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Opcode
%endif
Conflicts:      perl-interpreter < 4:5.30.1-451

%description Opcode
The Opcode module allows you to define an operator mask to be in effect when
perl next compiles any code. Attempting to compile code which contains
a masked opcode will cause the compilation to fail with an error. The code
will not be executed.

%package open
Summary:        Perl pragma to set default PerlIO layers for input and output
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.13
Requires:       perl(Carp)
Requires:       perl(Encode)
Requires:       perl(encoding)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_open
%endif
Conflicts:      perl < 4:5.20.2-326
BuildArch:      noarch

%description open
The "open" pragma serves as one of the interfaces to declare default "layers"
(also known as "disciplines") for all I/O.

%package overload
Summary:        Overloading Perl operations
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.40
BuildArch:      noarch
Requires:       perl(mro)
Requires:       perl(Scalar::Util)
Requires:       perl(overloading)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_overload
%endif
Conflicts:      perl-interpreter < 4:5.30.1-451

%description overload
The "overload" pragma allows overloading of Perl operators for a class. To
overload built-in functions, see "Overriding Built-in Functions" in perlsub
POD instead.

%package overloading
Summary:        Perl pragma to lexically control overloading
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        0.02
BuildArch:      noarch
Requires:       perl(Carp)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_overloading
%endif
Conflicts:      perl-interpreter < 4:5.30.1-451

%description overloading
Overloading pragma allows you to lexically disable or enable overloading.

%if %{dual_life} || %{rebuild_from_scratch}
%package parent
Summary:        Establish an ISA relationship with base classes at compile time
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        0.244
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_parent
%endif
BuildArch:      noarch

%description parent
parent allows you to both load one or more modules, while setting up
inheritance from those modules at the same time. Mostly similar in effect to:

    package Baz;

    BEGIN {
        require Foo;
        require Bar;

        push @ISA, qw(Foo Bar);
    }
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Params-Check
Summary:        Generic input parsing/checking mechanism
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        0.38
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Params_Check
%endif
BuildArch:      noarch

%description Params-Check
Params::Check is a generic input parsing/checking mechanism.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package PathTools
Summary:        PathTools Perl module (Cwd, File::Spec)
License:        (GPL-1.0-or-later OR Artistic-1.0-Perl) AND BSD-3-Clause
Epoch:          0
Version:        3.94
Requires:       perl(Carp)
Requires:       perl(Errno)
Requires:       perl(Scalar::Util)
# XSLoader is optional only because miniperl does not support XS. With perl we
# almost certainly want it.
Recommends:     perl(XSLoader)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_PathTools
%endif

%description PathTools
PathTools Perl module (Cwd, File::Spec).
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package perlfaq
Summary:        Frequently asked questions about Perl
# Code examples are Public Domain
License:        (GPL-1.0-or-later OR Artistic-1.0-Perl) AND LicenseRef-Fedora-Public-Domain
Epoch:          0
Version:        5.20250619
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_perlfaq
%endif
BuildArch:      noarch
Conflicts:      perl < 4:5.22.0-347

%description perlfaq
The perlfaq comprises several documents that answer the most commonly asked
questions about Perl and Perl programming.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package PerlIO-via-QuotedPrint
Summary:        PerlIO layer for quoted-printable strings
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        0.10
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_PerlIO_via_QuotedPrint
%endif
BuildArch:      noarch
Conflicts:      perl < 4:5.22.0-347

%description PerlIO-via-QuotedPrint
This module implements a PerlIO layer that works on files encoded in the
quoted-printable format. It will decode from quoted-printable while
reading from a handle, and it will encode as quoted-printable while
writing to a handle.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Perl-OSType
Summary:        Map Perl operating system names to generic types
Version:        1.010
Epoch:          0
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Perl_OSType
%endif
BuildArch:      noarch

%description Perl-OSType
Modules that provide OS-specific behaviors often need to know if the current
operating system matches a more generic type of operating systems. For example,
'linux' is a type of 'Unix' operating system and so is 'freebsd'.
This module provides a mapping between an operating system name as given by $^O
and a more generic type. The initial version is based on the OS type mappings
provided in Module::Build and ExtUtils::CBuilder (thus, Microsoft operating
systems are given the type 'Windows' rather than 'Win32').
%endif

%package ph
Summary:        Selected system header files converted to Perl headers
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        %{perl_version}
# Match header files used when building perl.
%if !0%{?os2_version}
Requires:       perl-libs%{?_isa} = %{perl_epoch}:%{perl_version}-%{release}
%else
Requires:       perl-libs = %{perl_epoch}:%{perl_version}-%{release}
%endif
Requires:       perl(warnings)
# We deliver this package only for these three files mentioned in
# a documentation.
Provides:       perl(sys/ioctl.ph) = %{perl_version}
Provides:       perl(sys/syscall.ph) = %{perl_version}
Provides:       perl(syscall.ph) = %{perl_version}
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_ph
%endif
Conflicts:      perl < 4:5.30.1-451

%description ph
Contemporary Perl still refers to some Perl header (ph) files although it does
not build them anymore. This is a prebuilt collection of the referred files.
If you miss other ones, you can generate them with h2ph tool from perl-utils
package.

%if %{dual_life} || %{rebuild_from_scratch}
%package Pod-Checker
Summary:        Check POD documents for syntax errors
Epoch:          4
Version:        1.77
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Pod_Checker
%endif
BuildArch:      noarch

%description Pod-Checker
Module and tools to verify POD documentation contents for compliance with the
Plain Old Documentation format specifications.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Pod-Escapes
Summary:        Resolve POD escape sequences
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        1.07
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Pod_Escapes
%endif
BuildArch:      noarch

%description Pod-Escapes
This module provides things that are useful in decoding Pod E<...> sequences.
%endif

%package Pod-Functions
Summary:        Group Perl functions as in perlfunc POD
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.14
BuildArch:      noarch
# Match perl the functions come from
Requires:       perl-libs = %{perl_epoch}:%{perl_version}-%{release}
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Pod_Functions
%endif
Conflicts:      perl < 4:5.30.1-451

%description Pod-Functions
This module enumerates the Perl functions that are documented in perlfunc POD.

%package Pod-Html
Summary:        Convert POD files to HTML
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.35
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Pod_Html
%endif
BuildArch:      noarch
Conflicts:      perl < 4:5.22.0-350

%description Pod-Html
This package converts files from POD format (see perlpod) to HTML format. It
can automatically generate indexes and cross-references, and it keeps a cache
of things it knows how to cross-reference.

%if %{dual_life} || %{rebuild_from_scratch}
%package Pod-Perldoc
Summary:        Look up Perl documentation in Pod format
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
# Real version 3.2801
Version:        3.28.01
%if %{with perl_enables_groff}
# Pod::Perldoc::ToMan executes roff
Requires:       groff-base
%endif
Requires:       perl(File::Temp) >= 0.22
Requires:       perl(HTTP::Tiny)
Requires:       perl(IO::Handle)
Requires:       perl(IPC::Open3)
# POD2::Base is optional
# Pod::Checker is not needed if Pod::Simple::Checker is available
Requires:       perl(Pod::Simple::Checker)
Requires:       perl(Pod::Simple::RTF) >= 3.16
Requires:       perl(Pod::Simple::XMLOutStream) >= 3.16
Requires:       perl(Text::ParseWords)
# Tk is optional
Requires:       perl(Symbol)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Pod_Perldoc
%endif
BuildArch:      noarch

%description Pod-Perldoc
perldoc looks up a piece of documentation in .pod format that is embedded
in the perl installation tree or in a perl script, and displays it via
"groff -man | $PAGER". This is primarily used for the documentation for
the perl library modules.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Pod-Simple
Summary:        Framework for parsing POD documentation
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        3.45
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Pod_Simple
%endif
BuildArch:      noarch

%description Pod-Simple
Pod::Simple is a Perl library for parsing text in the Pod ("plain old
documentation") markup language that is typically used for writing
documentation for Perl and for Perl modules.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Pod-Usage
Summary:        Print a usage message from embedded pod documentation
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          4
Version:        2.05
# Pod::Usage executes perldoc from perl-Pod-Perldoc by default
Requires:       perl-Pod-Perldoc
Requires:       perl(Pod::Text)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Pod_Usage
%endif
BuildArch:      noarch

%description Pod-Usage
pod2usage will print a usage message for the invoking script (using its
embedded POD documentation) and then exit the script with the desired exit
status. The usage message printed may have any one of three levels of
"verboseness": If the verbose level is 0, then only a synopsis is printed.
If the verbose level is 1, then the synopsis is printed along with a
description (if present) of the command line options and arguments. If the
verbose level is 2, then the entire manual page is printed.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package podlators
Summary:        Format POD source into various output formats
License:        (GPL-1.0-or-later OR Artistic-1.0-Perl) AND FSFAP
Epoch:          1
Version:        6.0.2
BuildArch:      noarch
Requires:       perl(File::Spec) >= 0.8
Requires:       perl(Pod::Simple) >= 3.06
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_podlators
%endif
Conflicts:      perl < 4:5.16.1-234

%description podlators
This package contains Pod::Man and Pod::Text modules which convert POD input
to *roff source output, suitable for man pages, or plain text.  It also
includes several sub-classes of Pod::Text for formatted output to terminals
with various capabilities.
%endif

%package POSIX
Summary:        Perl interface to IEEE Std 1003.1
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        2.23
Requires:       perl(Carp)
Requires:       perl(locale)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_POSIX
%endif
Conflicts:      perl-interpreter < 4:5.30.1-451

%description POSIX
The POSIX module permits you to access all (or nearly all) the standard POSIX
1003.1 identifiers. Many of these identifiers have been given Perl interfaces.

%package Safe
Summary:        Compile and execute code in restricted compartments
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        2.47
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Safe
%endif
BuildArch:      noarch
Conflicts:      perl-interpreter < 4:5.30.1-451

%description Safe
The Safe extension module allows the creation of compartments in which Perl
code can be evaluated. Please note that the restriction is not suitable for
security purposes.

%if %{dual_life} || %{rebuild_from_scratch}
%package Scalar-List-Utils
Summary:        A selection of general-utility scalar and list subroutines
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          5
Version:        1.69
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Scalar_List_Utils
%endif

%description Scalar-List-Utils
Scalar::Util and List::Util contain a selection of subroutines that people have
expressed would be nice to have in the perl core, but the usage would not
really be high enough to warrant the use of a keyword, and the size so small
such that being individual extensions would be wasteful.
%endif

%package Search-Dict
Summary:        Search for a key in a dictionary file
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.08
Requires:       perl(feature)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Search_Dict
%endif
BuildArch:      noarch
Conflicts:      perl-interpreter < 4:5.30.1-451

%description Search-Dict
This module sets file position in a file handle to be first line greater than
or equal (string-wise) to a key.

%package SelectSaver
Summary:        Save and restore selected file handle
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.02
BuildArch:      noarch
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_SelectSaver
%endif
Conflicts:      perl < 4:5.30.1-451

%description SelectSaver
A "SelectSaver" object contains a reference to the file handle that was
selected when it was created. When the object is destroyed, it re-selects the
file handle that was selected when it was created.

%package SelfLoader
Summary:        Load functions only on demand
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.28
BuildArch:      noarch
Requires:       perl(Carp)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_SelfLoader
%endif
Conflicts:      perl < 4:5.22.0-351

%description SelfLoader
This Perl module tells its users that functions in a package are to be
autoloaded from after the "__DATA__" token. See also "Autoloading" in
perlsub.

%package sigtrap
Summary:        Perl pragma to enable simple signal handling
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.10
BuildArch:      noarch
Requires:       perl(meta_notation) = %{perl_version}
Requires:       perl(Symbol)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_sigtrap
%endif
Conflicts:      perl < 4:5.30.1-451

%description sigtrap
The sigtrap pragma is a simple interface for installing signal handlers.

%if %{dual_life} || %{rebuild_from_scratch}
%package Socket
Summary:        C socket.h defines and structure manipulators
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          4
Version:        2.038
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Socket
%endif

%description Socket
This module is just a translation of the C socket.h file.  Unlike the old
mechanism of requiring a translated socket.ph file, this uses the h2xs program
(see the Perl source distribution) and your native C compiler.  This means
that it has a far more likely chance of getting the numbers right.  This
includes all of the commonly used pound-defines like AF_INET, SOCK_STREAM, etc.
%endif

%package sort
Summary:        Perl pragma to control sort() behavior
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        2.06
BuildArch:      noarch
Requires:       perl(Carp)
Requires:       perl(warnings)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_sort
%endif
Conflicts:      perl < 4:5.30.1-451

%description sort
With the "sort" pragma you can control the behavior of the builtin "sort()"
function.

%if %{dual_life} || %{rebuild_from_scratch}
%package Storable
Summary:        Persistence for Perl data structures
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          1
Version:        3.37
# Carp substitutes missing Log::Agent
Requires:       perl(Carp)
Requires:       perl(Config)
# Fcntl is optional, but locking is good
Requires:       perl(Fcntl)
Requires:       perl(IO::File)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Storable
%endif
Conflicts:      perl < 4:5.16.3-274

%description Storable
The Storable package brings persistence to your Perl data structures
containing scalar, array, hash or reference objects, i.e. anything that
can be conveniently stored to disk and retrieved at a later time.
%endif

%package subs
Summary:        Perl pragma to predeclare subroutine names
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.04
BuildArch:      noarch
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_subs
%endif
Conflicts:      perl < 4:5.30.1-451

%description subs
This will predeclare all the subroutines whose names are in the list,
allowing you to use them without parentheses (as list operators) even
before they're declared.

%package Symbol
Summary:        Manipulate Perl symbols and their names
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.09
BuildArch:      noarch
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Symbol
%endif
Conflicts:      perl < 4:5.30.1-451

%description Symbol
The Symbol module provides functions for manipulating Perl symbols.

%package Sys-Hostname
Summary:        Try every conceivable way to get a hostname
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.25
Suggests:       perl(POSIX)
Requires:       perl(XSLoader)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Sys_Hostname
%endif
Conflicts:      perl-interpreter < 4:5.30.1-451

%description Sys-Hostname
It attempts several methods of getting the system hostname and then caches the
result.

%if %{dual_life} || %{rebuild_from_scratch}
%package Sys-Syslog
Summary:        Perl interface to the UNIX syslog(3) calls
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        0.36
Requires:       perl(XSLoader)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Sys_Syslog
%endif
Conflicts:      perl < 4:5.16.3-269

%description Sys-Syslog
Sys::Syslog is an interface to the UNIX syslog(3) function. Call syslog() with
a string priority and a list of printf() arguments just like at syslog(3).
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Term-ANSIColor
Summary:        Color screen output using ANSI escape sequences
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        5.01
Requires:       perl(Carp)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Term_ANSIColor
%endif
BuildArch:      noarch
Conflicts:      perl < 4:5.18.2-302

%description Term-ANSIColor
This module has two interfaces, one through color() and colored() and the
other through constants. It also offers the utility functions uncolor(),
colorstrip(), colorvalid(), and coloralias(), which have to be explicitly
imported to be used.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Term-Cap
Summary:        Perl termcap interface
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.18
# ncurses for infocmp tool
Requires:       ncurses
Requires:       perl(Carp)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Term_Cap
%endif
BuildArch:      noarch
Conflicts:      perl < 4:5.22.0-347

%description Term-Cap
These are low-level functions to extract and use capabilities from a terminal
capability (termcap) database.
%endif

%package Term-Complete
Summary:        Perl word completion
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.403
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Term_Complete
%endif
BuildArch:      noarch
Conflicts:      perl-interpreter < 4:5.30.1-451

%description Term-Complete
"Complete" routine provides word completion on a list of words in the array.

%package Term-ReadLine
Summary:        Perl interface to various read-line packages
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.17
Requires:       perl(Term::Cap)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Term_ReadLine
%endif
BuildArch:      noarch
Conflicts:      perl-interpreter < 4:5.30.1-451

%description Term-ReadLine
This package is just a front end to some other packages. It's a stub to
set up a common interface to the various read-line implementations found
on CPAN (under the "Term::ReadLine::*" name space).

%if %{dual_life} || %{rebuild_from_scratch}
%package Term-Table
Summary:        Format a header and rows into a table
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        0.024
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Term_Table
%endif
BuildArch:      noarch
Conflicts:      perl < 4:5.39.10-507

%description Term-Table
This Perl module is able to format rows of data into tables.
%endif

%package Test
Summary:        Simple framework for writing test scripts
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.31
# Algorithm::Diff 1.15 is optional
Requires:       perl(File::Temp)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Test
%endif
BuildArch:      noarch
Conflicts:      perl < 4:5.22.0-351

%description Test
The Test Perl module simplifies the task of writing test files for Perl modules,
such that their output is in the format that Test::Harness expects to see.

%if %{dual_life} || %{rebuild_from_scratch}
%package Test-Harness
Summary:        Run Perl standard test scripts with statistics
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          1
Version:        3.50
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Test_Harness
%endif
BuildArch:      noarch

%description Test-Harness
Run Perl standard test scripts with statistics.
Use TAP::Parser, Test::Harness package was whole rewritten.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Test-Simple
Summary:        Basic utilities for writing tests
License:        (GPL-1.0-or-later OR Artistic-1.0-Perl) AND CC0-1.0 AND LicenseRef-Fedora-Public-Domain
Epoch:          3
Version:        1.302210
Requires:       perl(Data::Dumper)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Test_Simple
%endif
BuildArch:      noarch

%description Test-Simple
Basic utilities for writing tests.
%endif

%package Text-Abbrev
Summary:        Create an abbreviation table from a list
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.02
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Text_Abbrev
%endif
BuildArch:      noarch
Conflicts:      perl-interpreter < 4:5.30.1-451

%description Text-Abbrev
It stores all unambiguous truncations of each element of a list as keys in
an associative array. The values are the original list elements.

%if %{dual_life} || %{rebuild_from_scratch}
%package Text-Balanced
Summary:        Extract delimited text sequences from strings
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        2.06
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Text_Balanced
%endif
BuildArch:      noarch
Conflicts:      perl < 4:5.22.0-347

%description Text-Balanced
These Perl subroutines may be used to extract a delimited substring, possibly
after skipping a specified prefix string.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Text-ParseWords
Summary:        Parse text into an array of tokens or array of arrays
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        3.31
Requires:       perl(Carp)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Text_ParseWords
%endif
BuildArch:      noarch
Conflicts:      perl < 4:5.16.2-256

%description Text-ParseWords
Parse text into an array of tokens or array of arrays.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Text-Tabs+Wrap
Summary:        Expand tabs and do simple line wrapping
License:        TTWL
Epoch:          0
Version:        2024.001
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Text_Tabs_Wrap
%endif
BuildArch:      noarch
Conflicts:      perl < 4:5.20.2-325

%description Text-Tabs+Wrap
Text::Tabs performs the same job that the UNIX expand(1) and unexpand(1)
commands do: adding or removing tabs from a document.

Text::Wrap::wrap() will reformat lines into paragraphs. All it does is break
up long lines, it will not join short lines together.
%endif

%package Thread
Summary:        Manipulate threads in Perl (for old code only)
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        3.06
BuildArch:      noarch
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Thread
%endif
Conflicts:      perl < 4:5.30.1-451

%description Thread
This Thread module served as the front end to the old-style thread model,
called 5005threads, that has been removed in version 5.10.

For old code and interim backwards compatibility, the Thread module has been
reworked to function as a front end for the new interpreter threads (ithreads)
model. However, some previous functionality is not available. Further, the
data sharing models between the two thread models are completely different,
and anything to do with data sharing has to be thought differently.

You are strongly encouraged to migrate any existing threaded code to the new
model (i.e., use the threads and threads::shared modules) as soon as possible.

%if %{dual_life} || %{rebuild_from_scratch}
%package Thread-Queue
Summary:        Thread-safe queues
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        3.14
Requires:       perl(Carp)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Thread_Queue
%endif
BuildArch:      noarch
Conflicts:      perl < 4:5.16.2-257

%description Thread-Queue
This module provides thread-safe FIFO queues that can be accessed safely by
any number of threads.
%endif

%package Tie
Summary:        Base classes for tying variables
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
# Version from Tie::StdHandle
Version:        4.6
BuildArch:      noarch
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Tie
%endif
Conflicts:      perl < 4:5.30.1-451

%description Tie
These are Perl modules that helps connecting classes with arrays, hashes,
handles, and scalars.

%package Tie-File
Summary:        Access the lines of a disk file via a Perl array
License:        GPL-2.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.10
# Symbol is not used on Perl >= 5.6.0
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Tie_File
%endif
BuildArch:      noarch
Conflicts:      perl-interpreter < 4:5.30.1-451

%description Tie-File
Tie::File represents a regular text file as a Perl array. Each element in the
array corresponds to a record in the file. The first line of the file is
element 0 of the array; the second line is element 1, and so on.  The file is
not loaded into memory, so this will work even for gigantic files.  Changes to
the array are reflected in the file immediately.

%package Tie-Memoize
Summary:        Add data to a hash when needed
License:        GPL-2.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.1
Requires:       perl(Carp)
Requires:       perl(Tie::ExtraHash)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Tie_Memoize
%endif
BuildArch:      noarch
Conflicts:      perl-interpreter < 4:5.30.1-451

%description Tie-Memoize
This package allows a tied hash to load its values automatically on the first
access, and to use the cached value on the following accesses.

%if %{dual_life} || %{rebuild_from_scratch}
%package Tie-RefHash
Summary:        Use references as hash keys
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.41
# Scalar::Util || overload
Requires:       perl(overload)
Suggests:       perl(Scalar::Util)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Tie_RefHash
%endif
BuildArch:      noarch
Conflicts:      perl-interpreter < 4:5.30.1-451

%description Tie-RefHash
This module provides the ability to use references as hash keys if you first
"tie" the hash variable to this module. Normally, only the keys of the tied
hash itself are preserved as references; to use references as keys in
hashes-of-hashes, use Tie::RefHash::Nestable, included as part of
Tie::RefHash.
%endif

%package Time
Summary:        By-name interface to Perl built-in time functions
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.04
BuildArch:      noarch
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Time
%endif
Conflicts:      perl-interpreter < 4:5.30.1-451

%description Time
This package provides an object-oriented interface to Perl built-in gmtime()
and localtime () functions.

%if %{dual_life} || %{rebuild_from_scratch}
%package Time-HiRes
Summary:        High resolution alarm, sleep, gettimeofday, interval timers
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          4
Version:        1.9778
Requires:       perl(Carp)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Time_HiRes
%endif
Conflicts:      perl < 4:5.16.3-271

%description Time-HiRes
The Time::HiRes module implements a Perl interface to the usleep, nanosleep,
ualarm, gettimeofday, and setitimer/getitimer system calls, in other words,
high resolution time and timers.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Time-Local
Summary:        Efficiently compute time from local and GMT time
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          2
# Real version 1.35
Version:        1.350
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Time_Local
%endif
BuildArch:      noarch
Conflicts:      perl < 4:5.16.3-262

%description Time-Local
This module provides functions that are the inverse of built-in perl functions
localtime() and gmtime(). They accept a date as a six-element array, and
return the corresponding time(2) value in seconds since the system epoch
(Midnight, January 1, 1970 GMT on Unix, for example). This value can be
positive or negative, though POSIX only requires support for positive values,
so dates before the system's epoch may not work on all operating systems.
%endif

%package Time-Piece
Summary:        Time objects from localtime and gmtime
License:        (GPL-1.0-or-later OR Artistic-1.0-Perl) AND BSD-2-Clause-Views
Epoch:          0
# Real version 1.36
Version:        1.3600
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Time_Piece
%endif

%description Time-Piece
The Time::Piece module replaces the standard localtime and gmtime functions
with implementations that return objects.  It does so in a backwards compatible
manner, so that using localtime or gmtime as documented in perlfunc still
behave as expected.

%package Thread-Semaphore
Summary:        Thread-safe semaphores
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        2.13
Requires:       perl(Carp)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Thread_Semaphore
%endif
BuildArch:      noarch
Conflicts:      perl-interpreter < 4:5.30.1-451

%description Thread-Semaphore
Semaphores provide a mechanism to regulate access to resources. Unlike locks,
semaphores aren't tied to particular scalars, and so may be used to control
access to anything you care to use them for. Semaphores don't limit their
values to zero and one, so they can be used to control access to some resource
that there may be more than one of (e.g., file handles). Increment and
decrement amounts aren't fixed at one either, so threads can reserve or return
multiple resources at once.

%if %{dual_life} || %{rebuild_from_scratch}
%package threads
Summary:        Perl interpreter-based threads
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          1
Version:        2.43
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_threads
%endif

%description threads
Since Perl 5.8, thread programming has been available using a model called
interpreter threads  which provides a new Perl interpreter for each thread,
and, by default, results in no data or state information being shared between
threads.

(Prior to Perl 5.8, 5005threads was available through the Thread.pm API. This
threading model has been deprecated, and was removed as of Perl 5.10.0.)

As just mentioned, all variables are, by default, thread local. To use shared
variables, you need to also load threads::shared.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package threads-shared
Summary:        Perl extension for sharing data structures between threads
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.70
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_threads_shared
%endif

%description threads-shared
By default, variables are private to each thread, and each newly created thread
gets a private copy of each existing variable. This module allows you to share
variables across different threads (and pseudo-forks on Win32). It is used
together with the threads module.  This module supports the sharing of the
following data types only: scalars and scalar refs, arrays and array refs, and
hashes and hash refs.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Unicode-Collate
Summary:        Unicode Collation Algorithm
License:        (GPL-1.0-or-later OR Artistic-1.0-Perl) AND Unicode-DFS-2015
Epoch:          0
Version:        1.31
Requires:       perl(Unicode::Normalize)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Unicode_Collate
%endif
Conflicts:      perl < 4:5.22.0-347

%description Unicode-Collate
This package is Perl implementation of Unicode Technical Standard #10 (Unicode
Collation Algorithm).
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Unicode-Normalize
Summary:        Unicode Normalization Forms
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.32
# unicore/CombiningClass.pl and unicore/Decomposition.pl from perl, perl is
# auto-detected.
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Unicode_Normalize
%endif
Conflicts:      perl < 4:5.22.0-347

%description Unicode-Normalize
This package provides Perl functions that can convert strings into various
Unicode normalization forms as defined in Unicode Standard Annex #15.
%endif

%package Unicode-UCD
Summary:        Unicode character database
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        0.81
BuildArch:      noarch
Requires:       perl(Storable)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_Unicode_UCD
%endif
Conflicts:      perl < 4:5.30.1-451

%description Unicode-UCD
The Unicode::UCD module offers a series of functions that provide a simple
interface to the Unicode Character Database.

%package User-pwent
Summary:        By-name interface to Perl built-in user name resolver
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
# Real versions - User::grent = 1.05, User::pwent = 1.03
Version:        1.05
BuildArch:      noarch
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_User_pwent
%endif
Conflicts:      perl-interpreter < 4:5.30.1-451

%description User-pwent
This package provides an object-oriented interface to Perl build-in getgr*()
and getpw*() functions.

%package vars
Summary:        Perl pragma to predeclare global variable names
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.05
BuildArch:      noarch
Requires:       perl(Carp)
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_vars
%endif
Conflicts:      perl < 4:5.30.1-451

%description vars
This pragma will predeclare all the variables whose names are in the
list, allowing you to use them under "use strict", and disabling any
typo warnings for them.

For use with variables in the current package for a single scope, the
functionality provided by this pragma has been superseded by "our"
declarations, available in Perl v5.6.0 or later, and use of this pragma is
discouraged.

%if %{dual_life} || %{rebuild_from_scratch}
%package version
Summary:        Perl extension for Version Objects
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
# Epoch bump for clean upgrade over old standalone package
Epoch:          9
# real version 0.9933
Version:        0.99.33
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_version
%endif
BuildArch:      noarch

%description version
Perl extension for Version Objects
%endif

%package vmsish
Summary:        Perl pragma to control VMS-specific language features
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Epoch:          0
Version:        1.04
BuildArch:      noarch
%if %{defined perl_bootstrap}
Requires:       %perl_compat
%gendep_perl_vmsish
%endif
Conflicts:      perl < 4:5.30.1-451

%description vmsish
The "vmsish" pragma control VMS-specific features of the Perl language. If
you're not running VMS, this module does nothing.

%if 0%{?os2_version}
%debug_package
%endif

%prep
%if !0%{?os2_version}
%setup -q -n perl-%{perl_version}
%patch -P1 -p1
%ifarch %{multilib_64_archs}
%patch -P2 -p1
%endif
%patch -P3 -p1
%patch -P4 -p1
%patch -P5 -p1
%patch -P6 -p1
%patch -P7 -p1
%patch -P8 -p1
%patch -P9 -p1
%patch -P10 -p1
%patch -P11 -p1
%patch -P12 -p1
%patch -P13 -p1
%patch -P200 -p1
%patch -P201 -p1
%patch -P202 -p1
%else
%scm_setup
%endif

%if !%{defined perl_bootstrap}
# Local patch tracking
perl -x patchlevel.h \
    'Fedora Patch1: Removes date check, Fedora/RHEL specific' \
%ifarch %{multilib_64_archs}
    'Fedora Patch2: support for libdir64' \
%endif
    'Fedora Patch3: use libresolv instead of libbind' \
    'Fedora Patch4: USE_MM_LD_RUN_PATH' \
    'Fedora Patch5: Provide MM::maybe_command independently (bug #1129443)' \
    'Fedora Patch6: Dont run one io test due to random builder failures' \
    'Fedora Patch8: Define SONAME for libperl.so' \
    'Fedora Patch9: Install libperl.so to -Dshrpdir value' \
    'Fedora Patch10: Make *DBM_File desctructors thread-safe (RT#61912)' \
    'Fedora Patch11: Replace EU::MakeMaker dependency with EU::MM::Utils in IPC::Cmd (bug #1129443)' \
    'Fedora Patch12: Link XS modules to pthread library to fix linking with -z defs' \
    'Fedora Patch13: Pass the correct CFLAGS to dtrace' \
    'Fedora Patch200: Link XS modules to libperl.so with EU::CBuilder on Linux' \
    'Fedora Patch201: Link XS modules to libperl.so with EU::MM on Linux' \
    'Fedora Patch202: Add definition of OPTIMIZE to .ph files' \
    %{nil}
%endif

%if !0%{?os2_version}
#copy the example script
install -m 0644 %{SOURCE5} .
%endif

#copy Pod-Html license clarification
cp %{SOURCE6} .

%if !0%{?os2_version}
# Copy config.over to override Configure's guesses.
cp %{SOURCE8} .
%endif

#
# Candidates for doc recoding (need case by case review):
# find . -name "*.pod" -o -name "README*" -o -name "*.pm" | xargs file -i | grep charset= | grep -v '\(us-ascii\|utf-8\)'
recode()
{
        iconv -f "${2:-iso-8859-1}" -t utf-8 < "$1" > "${1}_"
        touch -r "$1" "${1}_"
        mv -f "${1}_" "$1"
}
# TODO iconv fail on this one
##recode README.tw big5
#recode pod/perlebcdic.pod
#recode pod/perlhack.pod
#recode pod/perlhist.pod
#recode pod/perlthrtut.pod
#recode AUTHORS

find . -name \*.orig -exec rm -fv {} \;

# Configure Compress::Zlib to use system zlib
sed -i 's|BUILD_ZLIB      = True|BUILD_ZLIB      = False|
    s|INCLUDE         = ./zlib-src|INCLUDE         = %{_includedir}|
    s|LIB             = ./zlib-src|LIB             = %{_libdir}|' \
    cpan/Compress-Raw-Zlib/config.in

# Ensure that we never accidentally bundle zlib or bzip2
rm -rf cpan/Compress-Raw-Zlib/zlib-src
rm -rf cpan/Compress-Raw-Bzip2/bzip2-src
sed -i '/\(bzip2\|zlib\)-src/d' MANIFEST

%if !%{with gdbm}
# Do not install anything requiring NDBM_File if NDBM is not available.
rm -rf 'cpan/Memoize/Memoize/NDBM_File.pm'
sed -i '\|cpan/Memoize/Memoize/NDBM_File.pm|d' MANIFEST
%endif


%build
echo "RPM Build arch: %{_arch}"

# use "lib", not %%{_lib}, for privlib, sitelib, and vendorlib
# To build production version, we would need -DDEBUGGING=-g

# Perl INC path (perl -V) in search order:
# - /usr/local/share/perl5            -- for CPAN     (site lib)
# - /usr/local/lib[64]/perl5          -- for CPAN     (site arch)
# - /usr/share/perl5/vendor_perl      -- 3rd party    (vendor lib)
# - /usr/lib[64]/perl5/vendor_perl    -- 3rd party    (vendor arch)
# - /usr/share/perl5                  -- Fedora       (priv lib)
# - /usr/lib[64]/perl5                -- Fedora       (arch lib)

%global privlib     %{_prefix}/share/perl5
%global archlib     %{_libdir}/perl5

%if 0%{?flatpak_runtime}
%global perl_vendorlib  /app/%{_lib}/perl5/vendor_perl
%global perl_vendorarch /app/share/perl5/vendor_perl
%else
%global perl_vendorlib  %{privlib}/vendor_perl
%global perl_vendorarch %{archlib}/vendor_perl
%endif

%global perl_abi    %(echo '%{perl_version}' | sed 's/^\\([^.]*\\.[^.]*\\).*/\\1/')

# ldflags is not used when linking XS modules.
# Only ldflags is used when linking miniperl.
# Only ccflags and ldflags are used for Configure's compiler checks.
# Set optimize=none to prevent from injecting upstream's value.
%if !0%{?os2_version}
/bin/sh Configure -des \
%else
%{_bindir}/sh Configure -des \
%endif
        -Doptimize="none" \
%if !0%{?os2_version}
        -Dccflags="$RPM_OPT_FLAGS" \
        -Dldflags="$RPM_LD_FLAGS" \
%endif
%if !0%{?os2_version}
        -Dccdlflags="-Wl,--enable-new-dtags $RPM_LD_FLAGS" \
%else
        -Dccdlflags="$RPM_LD_FLAGS" \
%endif
%if !0%{?os2_version}
        -Dlddlflags="-shared $RPM_LD_FLAGS" \
%else
        -Dlddlflags="-Zdll -Zomf -Zhigh-mem $RPM_LD_FLAGS" \
%endif
        -Dshrpdir="%{_libdir}" \
        -DDEBUGGING=-g \
        -Dversion=%{perl_version} \
        -Dmyhostname=localhost \
        -Dperladmin=root@localhost \
        -Dcc='%{__cc}' \
%if !0%{?os2_version}
        -Dcf_by='Red Hat, Inc.' \
%else
        -Dcf_by='%{vendor}' \
%endif
        -Dprefix=%{_prefix} \
        -Dman1dir="%{_mandir}/man1" \
        -Dman3dir="%{_mandir}/man3" \
        -Dvendorprefix=%{_prefix} \
        -Dsiteprefix=%{_prefix}/local \
        -Dsitelib="%{_prefix}/local/share/perl5/%{perl_abi}" \
        -Dsitearch="%{_prefix}/local/%{_lib}/perl5/%{perl_abi}" \
        -Dprivlib="%{privlib}" \
        -Dvendorlib="%{perl_vendorlib}" \
        -Darchlib="%{archlib}" \
        -Dvendorarch="%{perl_vendorarch}" \
%if !0%{?os2_version}
        -Darchname=%{perl_archname} \
%endif
%if 0%{?flatpak}
        -Dotherlibdirs="/usr/share/perl5/vendor_perl:/usr/%{_lib}/perl5/vendor_perl:/usr/share/perl5:/usr/%{_lib}/perl5" \
%endif
%if 0%{?flatpak_runtime}
        -Dotherlibdirs=%{archlib}/vendor_perl:%{privlib}/vendor_perl \
        -Dvendorprefix=/app \
%endif
%ifarch %{multilib_64_archs}
        -Dlibpth="/usr/local/lib64 /lib64 %{_prefix}/lib64" \
%endif
%ifarch sparc sparcv9
        -Ud_longdbl \
%endif
        -Duseshrplib \
%if !0%{?os2_version}
        -Dusethreads \
        -Duseithreads \
%endif
%if %{with perl_enables_systemtap}
        -Dusedtrace='/usr/bin/dtrace' \
%else
        -Uusedtrace \
%endif
        -Duselargefiles \
%if !0%{?os2_version}
        -Dd_semctl_semun \
%endif
%if %{with bdb}
        -Di_db \
%endif
%if %{with gdbm}
        -Ui_ndbm \
        -Di_gdbm \
%endif
%if !0%{?os2_version}
        -Di_shadow \
        -Di_syslog \
%endif
        -Dman3ext=3pm \
        -Duseperlio \
        -Dinstallusrbinperl=n \
        -Ubincompat5005 \
        -Uversiononly \
%if !0%{?os2_version}
        -Dpager='/usr/bin/less -isr' \
%else
        -Dpager='%{_bindir}/less -isr' \
%endif
        -Dd_gethostent_r_proto -Ud_endhostent_r_proto -Ud_sethostent_r_proto \
        -Ud_endprotoent_r_proto -Ud_setprotoent_r_proto \
        -Ud_endservent_r_proto -Ud_setservent_r_proto \
        -Dscriptdir='%{_bindir}' \
        -Dusesitecustomize \
%if !0%{?os2_version}
        -Duse64bitint
%endif

# -Duseshrplib creates libperl.so, -Ubincompat5005 help create DSO -> libperl.so

BUILD_BZIP2=0
BZIP2_LIB=%{_libdir}
export BUILD_BZIP2 BZIP2_LIB

# Prepare a symlink from proper DSO name to libperl.so now so that new perl
# can be executed from make.
%if !0%{?os2_version}
%global soname libperl.so.%{perl_abi}
test -L %soname || ln -s libperl.so %soname
%endif

%if 0%{?os2_version}
# Fix /@unixroot paths
sed -i 's#.:/usr#%{_exec_prefix}#gi' config.sh
sed -i 's#.:/mptn#/@system_drive/mptn#gi' config.sh

make os2.o
%endif

%ifarch sparc64 %{arm}
make
%else
%if 0%{?os2_version}
make
%else
make %{?_smp_mflags}
%endif
%endif
%install
make install DESTDIR=$RPM_BUILD_ROOT

%global build_archlib $RPM_BUILD_ROOT%{archlib}
%global build_privlib $RPM_BUILD_ROOT%{privlib}
%global build_bindir  $RPM_BUILD_ROOT%{_bindir}
%if !0%{?os2_version}
%global new_perl LD_PRELOAD="%{build_archlib}/CORE/libperl.so" \\\
    LD_LIBRARY_PATH="%{build_archlib}/CORE" \\\
    PERL5LIB="%{build_archlib}:%{build_privlib}" \\\
    %{build_bindir}/perl
%else
%global new_perl BEGINLIBPATH="$RPM_BUILD_ROOT%{_libdir} LIBPATHSTRICT=T" \\\
    LD_LIBRARY_PATH="%{build_archlib}/CORE" \\\
    PERL5LIB="%{build_archlib};%{build_privlib}" \\\
    %{build_bindir}/perl
%endif

%if 0%{?os2_version}
# Symlink main executable for rpm scripts.
ln -s %{_bindir}/perl.exe %{build_bindir}/perl
ln -s %{_bindir}/perl.exe %{build_bindir}/perl%{perl_version}
# Remove .imp files.
rm -rf %{build_archlib}/CORE/*.imp
%endif

%if !0%{?os2_version}
# Make proper DSO names, move libperl to standard path.
mv "%{build_archlib}/CORE/libperl.so" \
    "$RPM_BUILD_ROOT%{_libdir}/libperl.so.%{perl_version}"
ln -s "libperl.so.%{perl_version}" "$RPM_BUILD_ROOT%{_libdir}/%{soname}"
ln -s "libperl.so.%{perl_version}" "$RPM_BUILD_ROOT%{_libdir}/libperl.so"
# XXX: Keep symlink from original location because various code glues
# $archlib/CORE/$libperl to get the DSO.
ln -s "../../libperl.so.%{perl_version}" "%{build_archlib}/CORE/libperl.so"
# XXX: Remove the soname named file from CORE directory that was created as
# a symlink in build section and installed as a regular file by perl build
# system.
rm -f "%{build_archlib}/CORE/%{soname}"
%else
# Make proper DSO names, move libperl to standard path.
mv "%{build_archlib}/CORE/libperl.a" \
    "$RPM_BUILD_ROOT%{_libdir}/libperl_dll.a"
# XXX: Keep symlink from original location because various code glues
# $archlib/CORE/$libperl to get the DSO.
ln -s "../../libperl_dll.a" "%{build_archlib}/CORE/libperl.a"
%endif

%if !0%{?os2_version}
install -p -m 755 utils/pl2pm %{build_bindir}/pl2pm
%endif

# perlfunc/ioctl() recommends sys/ioctl.ph.
# perlfaq5 recommends sys/syscall.ph.
# perlfunc/syscall() recommends syscall.ph.
for i in sys/ioctl.h sys/syscall.h syscall.h
do
    %{new_perl} %{build_bindir}/h2ph -a -d %{build_archlib} $i || true
done

# vendor directories (in this case for third party rpms)
# perl doesn't create the auto subdirectory, but modules put things in it,
# so we need to own it.

mkdir -p $RPM_BUILD_ROOT%{perl_vendorarch}/auto
mkdir -p $RPM_BUILD_ROOT%{perl_vendorlib}

#
# perl RPM macros
#
mkdir -p ${RPM_BUILD_ROOT}%{_rpmmacrodir}
install -p -m 644 %{SOURCE3} ${RPM_BUILD_ROOT}%{_rpmmacrodir}

#
# Core modules removal
#
# Dual-living binaries clashes on debuginfo files between perl and standalone
# packages. Excluding is not enough, we need to remove them. This is
# a work-around for rpmbuild bug #878863.
find $RPM_BUILD_ROOT -type f -name '*.bs' -empty -delete
chmod -R u+w $RPM_BUILD_ROOT/*

# miniperl? As an interpreter? How odd. Anyway, a symlink does it:
rm %{build_privlib}/ExtUtils/xsubpp
ln -s ../../../bin/xsubpp %{build_privlib}/ExtUtils/

# Don't need the .packlist
rm %{build_archlib}/.packlist

# Do not distribute File::Spec::VMS as it works on VMS only (bug #973713)
# We cannot remove it in %%prep because dist/Cwd/t/Spec.t test needs it.
rm %{build_archlib}/File/Spec/VMS.pm
%if !0%{?os2_version}
rm $RPM_BUILD_ROOT%{_mandir}/man3/File::Spec::VMS.3*
%else
rm $RPM_BUILD_ROOT%{_mandir}/man3/File.Spec.VMS.3*
%endif

# Do not distribute ExtUtils-PL2Bat, it is used only for Windows
rm %{build_privlib}/ExtUtils/PL2Bat.pm
%if !0%{?os2_version}
rm $RPM_BUILD_ROOT%{_mandir}/man3/ExtUtils::PL2Bat.3*
%else
rm $RPM_BUILD_ROOT%{_mandir}/man3/ExtUtils.PL2Bat.3*
%endif

# for now, remove Bzip2:
# Why? Now is missing Bzip2 files and provides
##find $RPM_BUILD_ROOT -name Bzip2 | xargs rm -r
##find $RPM_BUILD_ROOT -name '*B*zip2*'| xargs rm

# tests -- FIXME need to validate that this all works as expected
mkdir -p %{buildroot}%{perl5_testdir}/perl-tests

# "core"
tar -cf - t/ | ( cd %{buildroot}%{perl5_testdir}/perl-tests && tar -xf - )

# "dual-lifed"
for dir in `find ext/ -type d -name t -maxdepth 2` ; do

    tar -cf - $dir | ( cd %{buildroot}%{perl5_testdir}/perl-tests/t && tar -xf - )
done

# Normalize shell bangs in tests.
# brp-mangle-shebangs executed by rpm-build chokes on t/TEST.
%{new_perl} -MConfig -i -pn \
    -e 's"\A#!(?:perl|\./perl|/perl|/usr/bin/perl|/usr/bin/env perl)\b"$Config{startperl}"' \
    $(find %{buildroot}%{perl5_testdir}/perl-tests -type f)

%if %{with perl_enables_systemtap}
# Systemtap tapset install
mkdir -p %{buildroot}%{tapsetdir}
%ifarch %{multilib_64_archs}
%global libperl_stp libperl%{perl_version}-64.stp
%else
%global libperl_stp libperl%{perl_version}-32.stp
%endif

sed \
  -e "s|LIBRARY_PATH|%{_libdir}/%{soname}|" \
  %{SOURCE4} \
  > %{buildroot}%{tapsetdir}/%{libperl_stp}
%endif

%if ! %{dual_life} && ! %{rebuild_from_scratch}
# All dual_life files/directories are deleted here instead of %%exclude in
# %%files. So that debuginfo does not find unpacked binaries and blindly
# symlinks to them at random packages.

# Archive-Tar
rm %{buildroot}%{_bindir}/ptar
rm %{buildroot}%{_bindir}/ptardiff
rm %{buildroot}%{_bindir}/ptargrep
rm -rf %{buildroot}%{privlib}/Archive/Tar
rm %{buildroot}%{privlib}/Archive/Tar.pm
rm -rf %{buildroot}%{privlib}/Archive
rm %{buildroot}%{_mandir}/man1/ptar.1*
rm %{buildroot}%{_mandir}/man1/ptardiff.1*
rm %{buildroot}%{_mandir}/man1/ptargrep.1*
rm %{buildroot}%{_mandir}/man3/Archive::Tar*

# autodie
rm -rf %{buildroot}%{privlib}/autodie/
rm %{buildroot}%{privlib}/autodie.pm
rm %{buildroot}%{privlib}/Fatal.pm
rm %{buildroot}%{_mandir}/man3/autodie.3*
rm %{buildroot}%{_mandir}/man3/autodie::*
rm %{buildroot}%{_mandir}/man3/Fatal.3*

# bignum
rm %{buildroot}%{privlib}/bigfloat.pm
rm %{buildroot}%{privlib}/bigint.pm
rm %{buildroot}%{privlib}/bignum.pm
rm %{buildroot}%{privlib}/bigrat.pm
rm -rf %{buildroot}%{privlib}/Math/BigFloat
rm %{buildroot}%{privlib}/Math/BigInt/Trace.pm
rm %{buildroot}%{privlib}/Math/BigRat/Trace.pm
rm -rf %{buildroot}%{privlib}/Math/BigRat

rm %{buildroot}%{_mandir}/man3/bigfloat.*
rm %{buildroot}%{_mandir}/man3/bigint.*
rm %{buildroot}%{_mandir}/man3/bignum.*
rm %{buildroot}%{_mandir}/man3/bigrat.*

# Carp
rm -rf %{buildroot}%{privlib}/Carp
rm %{buildroot}%{privlib}/Carp.*
rm %{buildroot}%{_mandir}/man3/Carp.*

# Compress-Raw-Bzip2
rm %{buildroot}%{archlib}/Compress/Raw/Bzip2.pm
rm -rf %{buildroot}%{archlib}/auto/Compress/Raw/Bzip2
rm %{buildroot}%{_mandir}/man3/Compress::Raw::Bzip2*

# Compress-Raw-Zlib
rm %{buildroot}%{archlib}/Compress/Raw/Zlib.pm
rm -rf %{buildroot}%{archlib}/Compress/Raw
rm -rf %{buildroot}%{archlib}/Compress
rm -rf %{buildroot}%{archlib}/auto/Compress/Raw/Zlib
rm -rf %{buildroot}%{archlib}/auto/Compress/Raw
rm -rf %{buildroot}%{archlib}/auto/Compress
rm %{buildroot}%{_mandir}/man3/Compress::Raw::Zlib*

# Config-Perl-V
rm -rf %{buildroot}%{privlib}/Config/Perl
rm %{buildroot}%{_mandir}/man3/Config::Perl::V.*

# constant
rm %{buildroot}%{privlib}/constant.pm
rm %{buildroot}%{_mandir}/man3/constant.3*

# CPAN-Meta-Requirements
rm %{buildroot}%{privlib}/CPAN/Meta/Requirements.pm
rm %{buildroot}%{_mandir}/man3/CPAN::Meta::Requirements.3*

# CPAN-Meta-YAML
rm %{buildroot}%{privlib}/CPAN/Meta/YAML.pm
rm %{buildroot}%{_mandir}/man3/CPAN::Meta::YAML*

# CPAN-Meta
rm %{buildroot}%{privlib}/CPAN/Meta.pm
rm %{buildroot}%{privlib}/CPAN/Meta/Converter.pm
rm %{buildroot}%{privlib}/CPAN/Meta/Feature.pm
rm -rf %{buildroot}%{privlib}/CPAN/Meta/History
rm %{buildroot}%{privlib}/CPAN/Meta/History.pm
rm %{buildroot}%{privlib}/CPAN/Meta/Merge.pm
rm %{buildroot}%{privlib}/CPAN/Meta/Prereqs.pm
rm %{buildroot}%{privlib}/CPAN/Meta/Spec.pm
rm %{buildroot}%{privlib}/CPAN/Meta/Validator.pm
rm -rf %{buildroot}%{privlib}/CPAN/Meta
rm %{buildroot}%{privlib}/Parse/CPAN/Meta.pm
rm -rf %{buildroot}%{privlib}/Parse/CPAN
rm -rf %{buildroot}%{privlib}/Parse
rm %{buildroot}%{_mandir}/man3/CPAN::Meta*
rm %{buildroot}%{_mandir}/man3/Parse::CPAN::Meta.3*

# CPAN
rm %{buildroot}%{_bindir}/cpan
rm %{buildroot}%{privlib}/App/Cpan.pm
rm -rf %{buildroot}%{privlib}/CPAN
rm %{buildroot}%{privlib}/CPAN.pm
rm %{buildroot}%{_mandir}/man1/cpan.1*
rm %{buildroot}%{_mandir}/man3/App::Cpan.*
rm %{buildroot}%{_mandir}/man3/CPAN.*
rm %{buildroot}%{_mandir}/man3/CPAN:*

# Data-Dumper
rm %{buildroot}%{archlib}/auto/Data/Dumper/Dumper.so
rm %{buildroot}%{archlib}/Data/Dumper.pm
rm -rf %{buildroot}%{archlib}/auto/Data/Dumper
rm -rf %{buildroot}%{archlib}/auto/Data
rm -rf %{buildroot}%{archlib}/Data
rm %{buildroot}%{_mandir}/man3/Data::Dumper.3*

# DB_File
%if %{with bdb}
rm %{buildroot}%{archlib}/DB_File.pm
rm %{buildroot}%{archlib}/auto/DB_File/DB_File.so
rm -rf %{buildroot}%{archlib}/auto/DB_File
rm %{buildroot}%{_mandir}/man3/DB_File*
%endif

# Devel-PPPort
rm %{buildroot}%{archlib}/Devel/PPPort.pm
rm %{buildroot}%{_mandir}/man3/Devel::PPPort.3*

# Digest
rm %{buildroot}%{privlib}/Digest.pm
rm %{buildroot}%{privlib}/Digest/base.pm
rm %{buildroot}%{privlib}/Digest/file.pm
rm -rf %{buildroot}%{privlib}/Digest
rm %{buildroot}%{_mandir}/man3/Digest.3*
rm %{buildroot}%{_mandir}/man3/Digest::base.3*
rm %{buildroot}%{_mandir}/man3/Digest::file.3*

# Digest-MD5
rm %{buildroot}%{archlib}/Digest/MD5.pm
rm -rf %{buildroot}%{archlib}/auto/Digest/MD5
rm %{buildroot}%{_mandir}/man3/Digest::MD5.3*

# Digest-SHA
rm %{buildroot}%{_bindir}/shasum
rm %{buildroot}%{archlib}/Digest/SHA.pm
rm -rf %{buildroot}%{archlib}/Digest
rm -rf %{buildroot}%{archlib}/auto/Digest/SHA
rm -rf %{buildroot}%{archlib}/auto/Digest
rm %{buildroot}%{_mandir}/man1/shasum.1*
rm %{buildroot}%{_mandir}/man3/Digest::SHA.3*

# Encode
rm %{buildroot}%{_bindir}/encguess
rm %{buildroot}%{_bindir}/piconv
rm -rf %{buildroot}%{archlib}/Encode*
rm -rf %{buildroot}%{archlib}/auto/Encode*
rm %{buildroot}%{_mandir}/man1/encguess.1*
rm %{buildroot}%{_mandir}/man1/piconv.1*
rm %{buildroot}%{_mandir}/man3/Encode*.3*

# encoding
rm %{buildroot}%{archlib}/encoding.pm
rm %{buildroot}%{_mandir}/man3/encoding.3*

# Encode-devel
rm %{buildroot}%{_bindir}/enc2xs
rm %{buildroot}%{privlib}/Encode/*.e2x
rm %{buildroot}%{privlib}/Encode/encode.h
rm -rf %{buildroot}%{privlib}/Encode
rm %{buildroot}%{_mandir}/man1/enc2xs.1*

# Env
rm %{buildroot}%{privlib}/Env.pm
rm %{buildroot}%{_mandir}/man3/Env.3*

# Exporter
rm -rf %{buildroot}%{privlib}/Exporter*
rm %{buildroot}%{_mandir}/man3/Exporter*

# experimental
rm %{buildroot}%{privlib}/experimental*
rm %{buildroot}%{privlib}/stable*
rm %{buildroot}%{_mandir}/man3/experimental*
rm %{buildroot}%{_mandir}/man3/stable*

# ExtUtils-CBuilder
rm %{buildroot}%{privlib}/ExtUtils/CBuilder.pm
rm -rf %{buildroot}%{privlib}/ExtUtils/CBuilder
rm %{buildroot}%{_mandir}/man3/ExtUtils::CBuilder*

# ExtUtils-Command
rm %{buildroot}%{privlib}/ExtUtils/Command.pm
rm %{buildroot}%{_mandir}/man3/ExtUtils::Command.*

# ExtUtils-Install
rm %{buildroot}%{privlib}/ExtUtils/Install.pm
rm %{buildroot}%{privlib}/ExtUtils/Installed.pm
rm %{buildroot}%{privlib}/ExtUtils/Packlist.pm
rm %{buildroot}%{_mandir}/man3/ExtUtils::Install.3*
rm %{buildroot}%{_mandir}/man3/ExtUtils::Installed.3*
rm %{buildroot}%{_mandir}/man3/ExtUtils::Packlist.3*

# ExtUtils-Manifest
rm %{buildroot}%{privlib}/ExtUtils/Manifest.pm
rm %{buildroot}%{privlib}/ExtUtils/MANIFEST.SKIP
rm %{buildroot}%{_mandir}/man3/ExtUtils::Manifest.3*

# ExtUtils-MakeMaker
rm %{buildroot}%{_bindir}/instmodsh
rm -rf %{buildroot}%{privlib}/ExtUtils/Command
rm -rf %{buildroot}%{privlib}/ExtUtils/Liblist
rm %{buildroot}%{privlib}/ExtUtils/Liblist.pm
rm -rf %{buildroot}%{privlib}/ExtUtils/MakeMaker
rm %{buildroot}%{privlib}/ExtUtils/MakeMaker.pm
rm %{buildroot}%{privlib}/ExtUtils/MM.pm
rm %{buildroot}%{privlib}/ExtUtils/MM_*.pm
rm %{buildroot}%{privlib}/ExtUtils/MY.pm
rm %{buildroot}%{privlib}/ExtUtils/Mkbootstrap.pm
rm %{buildroot}%{privlib}/ExtUtils/Mksymlists.pm
rm %{buildroot}%{privlib}/ExtUtils/testlib.pm
rm %{buildroot}%{_mandir}/man1/instmodsh.1*
rm %{buildroot}%{_mandir}/man3/ExtUtils::Command::MM*
rm %{buildroot}%{_mandir}/man3/ExtUtils::Liblist.3*
rm %{buildroot}%{_mandir}/man3/ExtUtils::MM.3*
rm %{buildroot}%{_mandir}/man3/ExtUtils::MM_*
rm %{buildroot}%{_mandir}/man3/ExtUtils::MY.3*
rm %{buildroot}%{_mandir}/man3/ExtUtils::MakeMaker*
rm %{buildroot}%{_mandir}/man3/ExtUtils::Mkbootstrap.3*
rm %{buildroot}%{_mandir}/man3/ExtUtils::Mksymlists.3*
rm %{buildroot}%{_mandir}/man3/ExtUtils::testlib.3*

# ExtUtils-MM-Utils
rm %{buildroot}%{privlib}/ExtUtils/MM/Utils.pm
rm -rf %{buildroot}%{privlib}/ExtUtils/MM
rm %{buildroot}%{_mandir}/man3/ExtUtils::MM::Utils.*

# ExtUtils-ParseXS
rm %{buildroot}%{privlib}/ExtUtils/ParseXS.pm
rm %{buildroot}%{privlib}/ExtUtils/ParseXS.pod
rm %{buildroot}%{privlib}/ExtUtils/ParseXS/Constants.pm
rm %{buildroot}%{privlib}/ExtUtils/ParseXS/CountLines.pm
rm %{buildroot}%{privlib}/ExtUtils/ParseXS/Eval.pm
rm %{buildroot}%{privlib}/ExtUtils/ParseXS/Node.pm
rm %{buildroot}%{privlib}/ExtUtils/ParseXS/Utilities.pm
rm -rf %{buildroot}%{privlib}/ExtUtils/ParseXS
rm %{buildroot}%{privlib}/ExtUtils/Typemaps.pm
rm %{buildroot}%{privlib}/ExtUtils/Typemaps/Cmd.pm
rm %{buildroot}%{privlib}/ExtUtils/Typemaps/InputMap.pm
rm %{buildroot}%{privlib}/ExtUtils/Typemaps/OutputMap.pm
rm %{buildroot}%{privlib}/ExtUtils/Typemaps/Type.pm
rm -rf %{buildroot}%{privlib}/ExtUtils/Typemaps
rm %{buildroot}%{privlib}/ExtUtils/xsubpp
rm %{buildroot}%{privlib}/pod/perlxs.pod
rm %{buildroot}%{privlib}/pod/perlxstut.pod
rm %{buildroot}%{privlib}/pod/perlxstypemap.pod
rm %{buildroot}%{_bindir}/xsubpp
rm %{buildroot}%{_mandir}/man1/perlxs*
rm %{buildroot}%{_mandir}/man1/xsubpp*
rm %{buildroot}%{_mandir}/man3/ExtUtils::ParseXS.3*
rm %{buildroot}%{_mandir}/man3/ExtUtils::ParseXS::Constants.3*
rm %{buildroot}%{_mandir}/man3/ExtUtils::ParseXS::Eval.3*
rm %{buildroot}%{_mandir}/man3/ExtUtils::ParseXS::Node.3*
rm %{buildroot}%{_mandir}/man3/ExtUtils::ParseXS::Utilities.3*
rm %{buildroot}%{_mandir}/man3/ExtUtils::Typemaps.3*
rm %{buildroot}%{_mandir}/man3/ExtUtils::Typemaps::Cmd.3*
rm %{buildroot}%{_mandir}/man3/ExtUtils::Typemaps::InputMap.3*
rm %{buildroot}%{_mandir}/man3/ExtUtils::Typemaps::OutputMap.3*
rm %{buildroot}%{_mandir}/man3/ExtUtils::Typemaps::Type.3*

# File-Fetch
rm %{buildroot}%{privlib}/File/Fetch.pm
rm %{buildroot}%{_mandir}/man3/File::Fetch.3*

# File-Path
rm %{buildroot}%{privlib}/File/Path.pm
rm %{buildroot}%{_mandir}/man3/File::Path.3*

# File-Temp
rm %{buildroot}%{privlib}/File/Temp.pm
rm %{buildroot}%{_mandir}/man3/File::Temp.3*

# Filter
rm -rf %{buildroot}%{archlib}/auto/Filter/Util
rm -rf %{buildroot}%{archlib}/auto/Filter
rm -rf %{buildroot}%{archlib}/Filter/Util
rm -rf %{buildroot}%{archlib}/Filter
rm %{buildroot}%{privlib}/pod/perlfilter.pod
rm %{buildroot}%{_mandir}/man1/perlfilter.*
rm %{buildroot}%{_mandir}/man3/Filter::Util::*

# Filter-Simple
rm %{buildroot}%{privlib}/Filter/Simple.pm
rm -rf %{buildroot}%{privlib}/Filter
rm %{buildroot}%{_mandir}/man3/Filter::Simple.3*

# Getopt-Long
rm %{buildroot}%{privlib}/Getopt/Long.pm
rm %{buildroot}%{privlib}/Getopt/Long/Parser.pm
rm %{buildroot}%{_mandir}/man3/Getopt::Long.3*
rm %{buildroot}%{_mandir}/man3/Getopt::Long::Parser.3*

# IO-Compress
rm %{buildroot}%{_bindir}/streamzip
rm %{buildroot}%{_bindir}/zipdetails
rm %{buildroot}%{privlib}/IO/Compress.pm
rm %{buildroot}%{privlib}/IO/Compress/FAQ.pod
rm %{buildroot}%{_mandir}/man1/streamzip.*
rm %{buildroot}%{_mandir}/man1/zipdetails.*
rm %{buildroot}%{_mandir}/man3/IO::Compress.3*
rm %{buildroot}%{_mandir}/man3/IO::Compress::FAQ.*
# Compress-Zlib
rm %{buildroot}%{privlib}/Compress/Zlib.pm
rm -rf %{buildroot}%{privlib}/Compress
rm %{buildroot}%{_mandir}/man3/Compress::Zlib*
# IO-Compress-Base
rm %{buildroot}%{privlib}/File/GlobMapper.pm
rm %{buildroot}%{privlib}/IO/Compress/Base.pm
rm -rf %{buildroot}%{privlib}/IO/Compress/Base
rm %{buildroot}%{privlib}/IO/Uncompress/AnyUncompress.pm
rm %{buildroot}%{privlib}/IO/Uncompress/Base.pm
rm %{buildroot}%{_mandir}/man3/File::GlobMapper.*
rm %{buildroot}%{_mandir}/man3/IO::Compress::Base.*
rm %{buildroot}%{_mandir}/man3/IO::Uncompress::AnyUncompress.*
rm %{buildroot}%{_mandir}/man3/IO::Uncompress::Base.*
# IO-Compress-Zlib
rm %{buildroot}%{privlib}/IO/Compress/Bzip2.pm
rm %{buildroot}%{privlib}/IO/Compress/Deflate.pm
rm %{buildroot}%{privlib}/IO/Compress/Gzip.pm
rm %{buildroot}%{privlib}/IO/Compress/RawDeflate.pm
rm %{buildroot}%{privlib}/IO/Compress/Zip.pm
rm -rf %{buildroot}%{privlib}/IO/Compress/Adapter
rm -rf %{buildroot}%{privlib}/IO/Compress/Gzip
rm -rf %{buildroot}%{privlib}/IO/Compress/Zip
rm -rf %{buildroot}%{privlib}/IO/Compress/Zlib
rm -rf %{buildroot}%{privlib}/IO/Compress
rm %{buildroot}%{privlib}/IO/Uncompress/AnyInflate.pm
rm %{buildroot}%{privlib}/IO/Uncompress/Bunzip2.pm
rm %{buildroot}%{privlib}/IO/Uncompress/Gunzip.pm
rm %{buildroot}%{privlib}/IO/Uncompress/Inflate.pm
rm %{buildroot}%{privlib}/IO/Uncompress/RawInflate.pm
rm %{buildroot}%{privlib}/IO/Uncompress/Unzip.pm
rm -rf %{buildroot}%{privlib}/IO/Uncompress/Adapter
rm -rf %{buildroot}%{privlib}/IO/Uncompress
rm %{buildroot}%{_mandir}/man3/IO::Compress::Deflate*
rm %{buildroot}%{_mandir}/man3/IO::Compress::Bzip2*
rm %{buildroot}%{_mandir}/man3/IO::Compress::Gzip*
rm %{buildroot}%{_mandir}/man3/IO::Compress::RawDeflate*
rm %{buildroot}%{_mandir}/man3/IO::Compress::Zip*
rm %{buildroot}%{_mandir}/man3/IO::Uncompress::AnyInflate*
rm %{buildroot}%{_mandir}/man3/IO::Uncompress::Bunzip2*
rm %{buildroot}%{_mandir}/man3/IO::Uncompress::Gunzip*
rm %{buildroot}%{_mandir}/man3/IO::Uncompress::Inflate*
rm %{buildroot}%{_mandir}/man3/IO::Uncompress::RawInflate*
rm %{buildroot}%{_mandir}/man3/IO::Uncompress::Unzip*

# IO-Socket-IP
rm %{buildroot}%{privlib}/IO/Socket/IP.pm
rm -rf %{buildroot}%{privlib}/IO/Socket
rm %{buildroot}%{_mandir}/man3/IO::Socket::IP.*

# IO-Zlib
rm %{buildroot}%{privlib}/IO/Zlib.pm
rm -rf %{buildroot}%{privlib}/IO
rm %{buildroot}%{_mandir}/man3/IO::Zlib.*

# HTTP-Tiny
rm %{buildroot}%{privlib}/HTTP/Tiny.pm
rm -rf %{buildroot}%{privlib}/HTTP
rm %{buildroot}%{_mandir}/man3/HTTP::Tiny*

# IPC-Cmd
rm %{buildroot}%{privlib}/IPC/Cmd.pm
rm %{buildroot}%{_mandir}/man3/IPC::Cmd.3*

# IPC-SysV
rm -rf %{buildroot}%{archlib}/auto/IPC
rm %{buildroot}%{archlib}/IPC/Msg.pm
rm %{buildroot}%{archlib}/IPC/Semaphore.pm
rm %{buildroot}%{archlib}/IPC/SharedMem.pm
rm %{buildroot}%{archlib}/IPC/SysV.pm
rm -rf %{buildroot}%{archlib}/IPC
rm %{buildroot}%{_mandir}/man3/IPC::Msg.*
rm %{buildroot}%{_mandir}/man3/IPC::Semaphore.*
rm %{buildroot}%{_mandir}/man3/IPC::SharedMem.*
rm %{buildroot}%{_mandir}/man3/IPC::SysV.*

# JSON-PP
rm %{buildroot}%{_bindir}/json_pp
rm %{buildroot}%{privlib}/JSON/PP.pm
rm -rf %{buildroot}%{privlib}/JSON/PP
rm -rf %{buildroot}%{privlib}/JSON
rm %{buildroot}%{_mandir}/man1/json_pp.1*
rm %{buildroot}%{_mandir}/man3/JSON::PP.3*
rm %{buildroot}%{_mandir}/man3/JSON::PP::Boolean.3pm*

# libnet
rm %{buildroot}%{privlib}/Net/Cmd.pm
rm %{buildroot}%{privlib}/Net/Config.pm
rm %{buildroot}%{privlib}/Net/Domain.pm
rm %{buildroot}%{privlib}/Net/FTP.pm
rm -rf %{buildroot}%{privlib}/Net/FTP
rm %{buildroot}%{privlib}/Net/libnetFAQ.pod
rm %{buildroot}%{privlib}/Net/NNTP.pm
rm %{buildroot}%{privlib}/Net/Netrc.pm
rm %{buildroot}%{privlib}/Net/POP3.pm
rm %{buildroot}%{privlib}/Net/SMTP.pm
rm %{buildroot}%{privlib}/Net/Time.pm
rm %{buildroot}%{_mandir}/man3/Net::Cmd.*
rm %{buildroot}%{_mandir}/man3/Net::Config.*
rm %{buildroot}%{_mandir}/man3/Net::Domain.*
rm %{buildroot}%{_mandir}/man3/Net::FTP.*
rm %{buildroot}%{_mandir}/man3/Net::libnetFAQ.*
rm %{buildroot}%{_mandir}/man3/Net::NNTP.*
rm %{buildroot}%{_mandir}/man3/Net::Netrc.*
rm %{buildroot}%{_mandir}/man3/Net::POP3.*
rm %{buildroot}%{_mandir}/man3/Net::SMTP.*
rm %{buildroot}%{_mandir}/man3/Net::Time.*

# Locale-Maketext
rm %{buildroot}%{privlib}/Locale/Maketext.*
rm %{buildroot}%{privlib}/Locale/Maketext/Cookbook.*
rm %{buildroot}%{privlib}/Locale/Maketext/Guts.*
rm %{buildroot}%{privlib}/Locale/Maketext/GutsLoader.*
rm %{buildroot}%{privlib}/Locale/Maketext/TPJ13.*
rm %{buildroot}%{_mandir}/man3/Locale::Maketext.*
rm %{buildroot}%{_mandir}/man3/Locale::Maketext::Cookbook.*
rm %{buildroot}%{_mandir}/man3/Locale::Maketext::Guts.*
rm %{buildroot}%{_mandir}/man3/Locale::Maketext::GutsLoader.*
rm %{buildroot}%{_mandir}/man3/Locale::Maketext::TPJ13.*

# Math-BigInt
rm %{buildroot}%{privlib}/Math/BigFloat.pm
rm %{buildroot}%{privlib}/Math/BigInt.pm
rm %{buildroot}%{privlib}/Math/BigInt/Calc.pm
rm %{buildroot}%{privlib}/Math/BigInt/Lib.pm
rm %{buildroot}%{privlib}/Math/BigRat.pm
rm -rf %{buildroot}%{privlib}/Math/BigInt
rm %{buildroot}%{_mandir}/man3/Math::BigFloat.*
rm %{buildroot}%{_mandir}/man3/Math::BigInt.*
rm %{buildroot}%{_mandir}/man3/Math::BigInt::Calc.*
rm %{buildroot}%{_mandir}/man3/Math::BigInt::Lib.*
rm %{buildroot}%{_mandir}/man3/Math::BigRat.*

# Math-BigInt-FastCalc
rm -rf %{buildroot}%{archlib}/Math
rm -rf %{buildroot}%{archlib}/auto/Math
rm %{buildroot}%{_mandir}/man3/Math::BigInt::FastCalc.*

# MIME-Base64
rm -rf %{buildroot}%{archlib}/auto/MIME
rm -rf %{buildroot}%{archlib}/MIME
rm %{buildroot}%{_mandir}/man3/MIME::*

# Module-CoreList
rm -rf %{buildroot}%{privlib}/Module/CoreList
rm %{buildroot}%{privlib}/Module/CoreList.pm
rm %{buildroot}%{privlib}/Module/CoreList.pod
rm %{buildroot}%{_mandir}/man3/Module::CoreList*

# Module-CoreList-tools
rm %{buildroot}%{_bindir}/corelist
rm %{buildroot}%{_mandir}/man1/corelist*

# Module-Load
rm %{buildroot}%{privlib}/Module/Load.pm
rm %{buildroot}%{_mandir}/man3/Module::Load.*

# Module-Load-Conditional
rm -rf %{buildroot}%{privlib}/Module/Load
rm %{buildroot}%{_mandir}/man3/Module::Load::Conditional*

# Module-Metadata
rm %{buildroot}%{privlib}/Module/Metadata.pm
rm %{buildroot}%{_mandir}/man3/Module::Metadata.3pm*

# Net-Ping
rm %{buildroot}%{privlib}/Net/Ping.pm
rm %{buildroot}%{_mandir}/man3/Net::Ping.*

# parent
rm %{buildroot}%{privlib}/parent.pm
rm %{buildroot}%{_mandir}/man3/parent.3*

# Params-Check
rm -rf %{buildroot}%{privlib}/Params/
rm %{buildroot}%{_mandir}/man3/Params::Check*

# PathTools
rm %{buildroot}%{archlib}/Cwd.pm
rm -rf %{buildroot}%{archlib}/File/Spec*
rm -rf %{buildroot}%{archlib}/auto/Cwd/
rm %{buildroot}%{_mandir}/man3/Cwd*
rm %{buildroot}%{_mandir}/man3/File::Spec*

# Perl-OSType
rm %{buildroot}%{privlib}/Perl/OSType.pm
rm -rf %{buildroot}%{privlib}/Perl
rm %{buildroot}%{_mandir}/man3/Perl::OSType.3pm*

# perlfaq
rm %{buildroot}%{privlib}/perlfaq.pm
rm %{buildroot}%{privlib}/pod/perlfaq*
rm %{buildroot}%{privlib}/pod/perlglossary.pod
rm %{buildroot}%{_mandir}/man1/perlfaq*
rm %{buildroot}%{_mandir}/man1/perlglossary.*

# PerlIO-via-QuotedPrint
rm -rf %{buildroot}%{privlib}/PerlIO/via
rm %{buildroot}%{_mandir}/man3/PerlIO::via::QuotedPrint.*

# Pod-Checker
rm %{buildroot}%{_bindir}/podchecker
rm %{buildroot}%{privlib}/Pod/Checker.pm
rm %{buildroot}%{_mandir}/man1/podchecker.*
rm %{buildroot}%{_mandir}/man3/Pod::Checker.*

# Pod-Escapes
rm %{buildroot}%{privlib}/Pod/Escapes.pm
rm %{buildroot}%{_mandir}/man3/Pod::Escapes.*

# Pod-Perldoc
rm %{buildroot}%{_bindir}/perldoc
rm %{buildroot}%{privlib}/pod/perldoc.pod
rm %{buildroot}%{privlib}/Pod/Perldoc.pm
rm -rf %{buildroot}%{privlib}/Pod/Perldoc/
rm %{buildroot}%{_mandir}/man1/perldoc.1*
rm %{buildroot}%{_mandir}/man3/Pod::Perldoc*

# Pod-Usage
rm %{buildroot}%{_bindir}/pod2usage
rm %{buildroot}%{privlib}/Pod/Usage.pm
rm %{buildroot}%{_mandir}/man1/pod2usage.*
rm %{buildroot}%{_mandir}/man3/Pod::Usage.*

# podlators
rm %{buildroot}%{_bindir}/pod2man
rm %{buildroot}%{_bindir}/pod2text
rm %{buildroot}%{privlib}/pod/perlpodstyle.pod
rm %{buildroot}%{privlib}/Pod/Man.pm
rm %{buildroot}%{privlib}/Pod/ParseLink.pm
rm %{buildroot}%{privlib}/Pod/Text.pm
rm -rf %{buildroot}%{privlib}/Pod/Text
rm %{buildroot}%{_mandir}/man1/pod2man.1*
rm %{buildroot}%{_mandir}/man1/pod2text.1*
rm %{buildroot}%{_mandir}/man1/perlpodstyle.1*
rm %{buildroot}%{_mandir}/man3/Pod::Man*
rm %{buildroot}%{_mandir}/man3/Pod::ParseLink*
rm %{buildroot}%{_mandir}/man3/Pod::Text*

# Pod-Simple
rm %{buildroot}%{privlib}/Pod/Simple.pm
rm %{buildroot}%{privlib}/Pod/Simple.pod
rm -rf %{buildroot}%{privlib}/Pod/Simple/
rm %{buildroot}%{_mandir}/man3/Pod::Simple*

# Scalar-List-Utils
rm -rf %{buildroot}%{archlib}/List/
rm -rf %{buildroot}%{archlib}/Scalar/
rm -rf %{buildroot}%{archlib}/Sub/
rm -rf %{buildroot}%{archlib}/auto/List/
rm %{buildroot}%{_mandir}/man3/List::Util*
rm %{buildroot}%{_mandir}/man3/Scalar::Util*
rm %{buildroot}%{_mandir}/man3/Scalar::List::Utils*
rm %{buildroot}%{_mandir}/man3/Sub::Util*

# Socket
rm %{buildroot}%{archlib}/auto/Socket/Socket.*
rm -rf %{buildroot}%{archlib}/auto/Socket
rm %{buildroot}%{archlib}/Socket.pm
rm %{buildroot}%{_mandir}/man3/Socket.3*

# Storable
rm %{buildroot}%{archlib}/Storable.pm
rm -rf %{buildroot}%{archlib}/auto/Storable/
rm %{buildroot}%{_mandir}/man3/Storable.*

# Sys-Syslog
# %%dir %%{archlib}/Sys not excluded. It would be removed from the previous package.
rm %{buildroot}%{archlib}/Sys/Syslog.pm
# %%dir %%{archlib}/auto/Sys not excluded. It would be removed from the previous package.
rm -rf %{buildroot}%{archlib}/auto/Sys/Syslog/
rm %{buildroot}%{_mandir}/man3/Sys::Syslog.*

# Term-ANSIColor
rm %{buildroot}%{privlib}/Term/ANSIColor.pm
rm %{buildroot}%{_mandir}/man3/Term::ANSIColor*

# Term-Cap
rm %{buildroot}%{privlib}/Term/Cap.pm
rm %{buildroot}%{_mandir}/man3/Term::Cap.*

# Term-Table
rm %{buildroot}%{privlib}/Term/Table.pm
rm %{buildroot}%{privlib}/Term/Table//Cell.pm
rm %{buildroot}%{privlib}/Term/Table/CellStack.pm
rm %{buildroot}%{privlib}/Term/Table/HashBase.pm
rm %{buildroot}%{privlib}/Term/Table/LineBreak.pm
rm %{buildroot}%{privlib}/Term/Table/Spacer.pm
rm %{buildroot}%{privlib}/Term/Table/Util.pm
rm %{buildroot}%{_mandir}/man3/Term::Table*

# Test-Harness
rm %{buildroot}%{_bindir}/prove
rm -rf %{buildroot}%{privlib}/App/Prove*
rm -rf %{buildroot}%{privlib}/App
rm -rf %{buildroot}%{privlib}/TAP*
rm %{buildroot}%{privlib}/Test/Harness*
rm %{buildroot}%{_mandir}/man1/prove.1*
rm %{buildroot}%{_mandir}/man3/App::Prove*
rm %{buildroot}%{_mandir}/man3/TAP*
rm %{buildroot}%{_mandir}/man3/Test::Harness*

# Test-Simple
rm %{buildroot}%{privlib}/ok*
rm %{buildroot}%{privlib}/Test/More*
rm -rf %{buildroot}%{privlib}/Test/Builder*
rm -rf %{buildroot}%{privlib}/Test/Tester*
rm %{buildroot}%{privlib}/Test/Simple*
rm %{buildroot}%{privlib}/Test/Tutorial*
rm -rf %{buildroot}%{privlib}/Test/use
rm -rf %{buildroot}%{privlib}/Test
rm -rf %{buildroot}%{privlib}/Test2.pm
rm -rf %{buildroot}%{privlib}/Test2/API*
rm -rf %{buildroot}%{privlib}/Test2/Event.pm
rm -rf %{buildroot}%{privlib}/Test2/Event/*
rm -rf %{buildroot}%{privlib}/Test2/EventFacet*
rm -rf %{buildroot}%{privlib}/Test2/Formatter*
rm -rf %{buildroot}%{privlib}/Test2/Hub*
rm -rf %{buildroot}%{privlib}/Test2/IPC*
rm -rf %{buildroot}%{privlib}/Test2/Tools/Tiny.pm
rm -rf %{buildroot}%{privlib}/Test2/Transition.pod
rm %{buildroot}%{privlib}/Test2/Env.pm
rm %{buildroot}%{privlib}/Test2/Util.pm
rm %{buildroot}%{privlib}/Test2/Util/ExternalMeta.pm
rm %{buildroot}%{privlib}/Test2/Util/Facets2Legacy.pm
rm %{buildroot}%{privlib}/Test2/Util/HashBase.pm
rm %{buildroot}%{privlib}/Test2/Util/Sig.pm
rm %{buildroot}%{privlib}/Test2/Util/Trace.pm
rm %{buildroot}%{_mandir}/man3/ok*
rm %{buildroot}%{_mandir}/man3/Test::More*
rm %{buildroot}%{_mandir}/man3/Test::Builder*
rm %{buildroot}%{_mandir}/man3/Test::Tester*
rm %{buildroot}%{_mandir}/man3/Test::Simple*
rm %{buildroot}%{_mandir}/man3/Test::Tutorial*
rm %{buildroot}%{_mandir}/man3/Test::use::*
rm %{buildroot}%{_mandir}/man3/Test2.*
rm %{buildroot}%{_mandir}/man3/Test2::API*
rm %{buildroot}%{_mandir}/man3/Test2::Env.*
rm %{buildroot}%{_mandir}/man3/Test2::Event.*
rm %{buildroot}%{_mandir}/man3/Test2::Event::*
rm %{buildroot}%{_mandir}/man3/Test2::EventFacet*
rm %{buildroot}%{_mandir}/man3/Test2::Formatter*
rm %{buildroot}%{_mandir}/man3/Test2::Hub*
rm %{buildroot}%{_mandir}/man3/Test2::IPC*
rm %{buildroot}%{_mandir}/man3/Test2::Tools::Tiny*
rm %{buildroot}%{_mandir}/man3/Test2::Transition*
rm %{buildroot}%{_mandir}/man3/Test2::Util.*
rm %{buildroot}%{_mandir}/man3/Test2::Util::ExternalMeta.*
rm %{buildroot}%{_mandir}/man3/Test2::Util::Facets2Legacy.*
rm %{buildroot}%{_mandir}/man3/Test2::Util::HashBase.*
rm %{buildroot}%{_mandir}/man3/Test2::Util::Sig.*
rm %{buildroot}%{_mandir}/man3/Test2::Util::Trace.*

# Test2-Suite merged into perl-Test-Simple
rm -rf %{buildroot}%{privlib}/Test2/AsyncSubtest*
rm -rf %{buildroot}%{privlib}/Test2/Bundle*
rm -rf %{buildroot}%{privlib}/Test2/Compare*
rm -rf %{buildroot}%{privlib}/Test2/Manual*
rm %{buildroot}%{privlib}/Test2/Mock.pm
rm -rf %{buildroot}%{privlib}/Test2/Plugin*
rm -rf %{buildroot}%{privlib}/Test2/Require*
rm %{buildroot}%{privlib}/Test2/Suite.pm
rm %{buildroot}%{privlib}/Test2/Todo.pm
rm %{buildroot}%{privlib}/Test2/Tools.pm
rm -rf %{buildroot}%{privlib}/Test2/Tools
rm %{buildroot}%{privlib}/Test2/Util/Grabber.pm
rm %{buildroot}%{privlib}/Test2/Util/Guard.pm
rm %{buildroot}%{privlib}/Test2/Util/Importer.pm
rm %{buildroot}%{privlib}/Test2/Util/Ref.pm
rm %{buildroot}%{privlib}/Test2/Util/Stash.pm
rm %{buildroot}%{privlib}/Test2/Util/Sub.pm
rm -rf %{buildroot}%{privlib}/Test2/Util/Table
rm %{buildroot}%{privlib}/Test2/Util/Table.pm
rm %{buildroot}%{privlib}/Test2/Util/Term.pm
rm %{buildroot}%{privlib}/Test2/Util/Times.pm
rm -rf %{buildroot}%{privlib}/Test2/Util
rm %{buildroot}%{privlib}/Test2/V0.pm
rm -rf %{buildroot}%{privlib}/Test2/Workflow*
rm %{buildroot}%{_mandir}/man3/Test2::AsyncSubtest*
rm %{buildroot}%{_mandir}/man3/Test2::Bundle*
rm %{buildroot}%{_mandir}/man3/Test2::Compare*
rm %{buildroot}%{_mandir}/man3/Test2::Manual*
rm %{buildroot}%{_mandir}/man3/Test2::Mock.*
rm %{buildroot}%{_mandir}/man3/Test2::Plugin*
rm %{buildroot}%{_mandir}/man3/Test2::Require*
rm %{buildroot}%{_mandir}/man3/Test2::Suite.*
rm %{buildroot}%{_mandir}/man3/Test2::Todo.*
rm %{buildroot}%{_mandir}/man3/Test2::Tools.*
rm %{buildroot}%{_mandir}/man3/Test2::Tools::*
rm %{buildroot}%{_mandir}/man3/Test2::Util::Grabber.*
rm %{buildroot}%{_mandir}/man3/Test2::Util::Guard.*
rm %{buildroot}%{_mandir}/man3/Test2::Util::Importer.*
rm %{buildroot}%{_mandir}/man3/Test2::Util::Ref.*
rm %{buildroot}%{_mandir}/man3/Test2::Util::Stash.*
rm %{buildroot}%{_mandir}/man3/Test2::Util::Sub.*
rm %{buildroot}%{_mandir}/man3/Test2::Util::Table*
rm %{buildroot}%{_mandir}/man3/Test2::Util::Times.*
rm %{buildroot}%{_mandir}/man3/Test2::V0.*
rm %{buildroot}%{_mandir}/man3/Test2::Workflow*

# Text-Balanced
rm %{buildroot}%{privlib}/Text/Balanced.pm
rm %{buildroot}%{_mandir}/man3/Text::Balanced.*

# Text-ParseWords
rm %{buildroot}%{privlib}/Text/ParseWords.pm
rm %{buildroot}%{_mandir}/man3/Text::ParseWords.*

# Text-Tabs+Wrap
rm %{buildroot}%{privlib}/Text/Tabs.pm
rm %{buildroot}%{privlib}/Text/Wrap.pm
rm %{buildroot}%{_mandir}/man3/Text::Tabs.*
rm %{buildroot}%{_mandir}/man3/Text::Wrap.*

# Thread-Queue
rm %{buildroot}%{privlib}/Thread/Queue.pm
rm %{buildroot}%{_mandir}/man3/Thread::Queue.*

# Tie-RefHash
rm %{buildroot}%{privlib}/Tie/RefHash.pm
rm %{buildroot}%{_mandir}/man3/Tie::RefHash.*

# Time-HiRes
rm %{buildroot}%{archlib}/Time/HiRes.pm
rm -rf %{buildroot}%{archlib}/auto/Time/HiRes
rm %{buildroot}%{_mandir}/man3/Time::HiRes.*

# Time-Local
rm %{buildroot}%{privlib}/Time/Local.pm
rm %{buildroot}%{_mandir}/man3/Time::Local.*

# threads
rm %{buildroot}%{archlib}/auto/threads/threads*
rm %{buildroot}%{archlib}/threads.pm
rm %{buildroot}%{_mandir}/man3/threads.3*

# threads-shared
rm -rf %{buildroot}%{archlib}/auto/threads/shared*
rm -rf %{buildroot}%{archlib}/auto/threads
rm %{buildroot}%{archlib}/threads/shared*
rm -rf %{buildroot}%{archlib}/threads
rm %{buildroot}%{_mandir}/man3/threads::shared*

# Unicode-Collate
rm -rf %{buildroot}%{archlib}/auto/Unicode/Collate
rm -rf %{buildroot}%{archlib}/auto/Unicode
rm %{buildroot}%{archlib}/Unicode/Collate.pm
rm -rf %{buildroot}%{archlib}/Unicode/Collate
rm -rf %{buildroot}%{privlib}/Unicode/Collate
rm %{buildroot}%{_mandir}/man3/Unicode::Collate.*
rm %{buildroot}%{_mandir}/man3/Unicode::Collate::*

# Unicode-Normalize
rm -rf %{buildroot}%{archlib}/auto/Unicode/Normalize
rm %{buildroot}%{archlib}/Unicode/Normalize.pm
rm -rf %{buildroot}%{archlib}/Unicode
rm %{buildroot}%{_mandir}/man3/Unicode::Normalize.*

# version
rm %{buildroot}%{privlib}/version.pm
rm %{buildroot}%{privlib}/version.pod
rm -rf %{buildroot}%{privlib}/version/
rm %{buildroot}%{_mandir}/man3/version.3*
rm %{buildroot}%{_mandir}/man3/version::Internals.3*
%endif


# TODO: Canonicalize test files (rewrite intrerpreter path, fix permissions)
# XXX: We cannot rewrite ./perl before %%check phase. Otherwise the test
# would run against system perl at build-time.
# See __spec_check_pre global macro in macros.perl.
#T_FILES=`find %%{buildroot}%%{perl5_testdir} -type f -name '*.t'`
#%%fix_shbang_line $T_FILES
#%%{__chmod} +x $T_FILES
#%%{_fixperms} %%{buildroot}%%{perl5_testdir}
#
# lib/perl5db.t will fail if Term::ReadLine::Gnu is available
%check
%if %{with test}
%{new_perl} -I/lib regen/lib_cleanup.pl
pushd t
%{new_perl} -I../lib porting/customized.t --regen
popd
%if %{parallel_tests}
    JOBS=$(printf '%%s' "%{?_smp_mflags}" | sed 's/.*-j\([0-9][0-9]*\).*/\1/')
    LC_ALL=C TEST_JOBS=$JOBS make test_harness
%else
    LC_ALL=C make test
%endif
%endif

%if 0%{?flatpak}
# This symlink won't be included in the Flatpak, since it is outside of /app,
# but it is needed in the prefix=/app buildroot, since we need to be able to
# install modules that Require: /usr/bin/perl.
mkdir -p %{buildroot}/usr/bin
ln -s /app/bin/perl %{buildroot}/usr/bin/perl
%endif

%if !0%{?os2_version}
%ldconfig_scriptlets libs
%endif

%files
# Main perl package is an empty meta package.

%files interpreter
%{_bindir}/perl
%{_bindir}/perl%{perl_version}
%if 0%{?os2_version}
%{_bindir}/perl.exe
%{_bindir}/perl%{perl_version}.exe
%endif
%{_mandir}/man1/perl.1*
%{_mandir}/man1/perlrun.1*
%if !0%{?os2_version}
%dir %{privlib}/pod
%{privlib}/pod/perl.pod
%{privlib}/pod/perlrun.pod
%else
%dir %{privlib}/Pod
%{privlib}/Pod/perl.pod
%{privlib}/Pod/perlrun.pod
%endif
%if 0%{?flatpak}
/usr/bin/perl
%endif

%files libs
%license Artistic Copying
%doc AUTHORS README Changes
%dir %{archlib}
%{archlib}/attributes.pm
%dir %{archlib}/auto
%dir %{archlib}/auto/attributes
%if !0%{?os2_version}
%{archlib}/auto/attributes/attributes.so
%else
%{archlib}/auto/attributes/attribZU.dll
%endif
%dir %{archlib}/auto/File
%dir %{archlib}/auto/File/Glob
%if !0%{?os2_version}
%{archlib}/auto/File/Glob/Glob.so
%else
%{archlib}/auto/File/Glob/GlobAJ.dll
%endif
%{archlib}/auto/PerlIO
%{archlib}/auto/re
%{archlib}/auto/SDBM_File
%{archlib}/Config.*
%{archlib}/Config_git.pl
%{archlib}/Config_heavy.pl
%dir %{archlib}/CORE
%if !0%{?os2_version}
%{archlib}/CORE/libperl.so
%endif
%dir %{archlib}/File
%{archlib}/File/Glob.pm
%{archlib}/PerlIO
%{archlib}/re.pm
%{archlib}/SDBM_File.pm
%if !0%{?os2_version}
%{_libdir}/libperl.so.*
%else
%{_libdir}/perl8AF.dll
%endif
%dir %{perl_vendorarch}
%dir %{perl_vendorarch}/auto
%dir %{privlib}
%{privlib}/AnyDBM_File.pm
%{privlib}/builtin.pm
%{privlib}/bytes.pm
%{privlib}/_charnames.pm
%{privlib}/charnames.pm
%{privlib}/CORE.pod
%{privlib}/feature.pm
%{privlib}/integer.pm
%{privlib}/Internals.pod
%{privlib}/PerlIO.pm
%dir %{privlib}/PerlIO
%{privlib}/PerlIO/scalar.pm
%{privlib}/source/encoding.pm
%{privlib}/strict.pm
%{privlib}/unicore
%{privlib}/UNIVERSAL.pm
%{privlib}/utf8.pm
%{privlib}/warnings
%{privlib}/warnings.pm
%dir %{privlib}/Tie
%{privlib}/Tie/Hash.pm
%dir %{privlib}/Tie/Hash
%{privlib}/Tie/Hash/NamedCapture.pm
%{privlib}/XSLoader.pm
%dir %{perl_vendorlib}
%{_mandir}/man3/AnyDBM_File.*
%{_mandir}/man3/attributes.*
%{_mandir}/man3/builtin.*
%{_mandir}/man3/bytes.*
%{_mandir}/man3/charnames.*
%{_mandir}/man3/Config.*
%{_mandir}/man3/CORE.*
%{_mandir}/man3/feature.3*
%if !0%{?os2_version}
%{_mandir}/man3/File::Glob.*
%else
%{_mandir}/man3/File.Glob.*
%endif
%{_mandir}/man3/integer.*
%{_mandir}/man3/Internals.*
%{_mandir}/man3/PerlIO.*
%if !0%{?os2_version}
%{_mandir}/man3/PerlIO::encoding.*
%{_mandir}/man3/PerlIO::mmap.*
%{_mandir}/man3/PerlIO::scalar.*
%{_mandir}/man3/PerlIO::via.*
%endif
%{_mandir}/man3/re.*
%{_mandir}/man3/SDBM_File.3*
%if !0%{?os2_version}
%{_mandir}/man3/source::encoding.*
%else
%{_mandir}/man3/source.encoding.*
%endif
%{_mandir}/man3/strict.*
%if !0%{?os2_version}
%{_mandir}/man3/Tie::Hash.*
%{_mandir}/man3/Tie::Hash::*
%else
%{_mandir}/man3/Tie.Hash.*
%endif
#%%{_mandir}/man3/unicore*
%{_mandir}/man3/utf8.*
%{_mandir}/man3/warnings.*
%if !0%{?os2_version}
%{_mandir}/man3/warnings::*
%endif
%{_mandir}/man3/UNIVERSAL.*
%{_mandir}/man3/XSLoader.*
%if 0%{?os2_version}
%{archlib}/auto/OS2/DLL/*.dll
%{archlib}/auto/OS2/ExtAttr/*.dll
%{archlib}/auto/OS2/PrfDB/*.dll
%{archlib}/auto/OS2/Process/*.dll
%{archlib}/auto/OS2/REXX/*.dll
%{_mandir}/man3/OS2.*
%{archlib}/OS2
%{privlib}/OS2/DLL.pm
%endif

%files devel
%{_bindir}/h2xs
%{_mandir}/man1/h2xs*
%{_bindir}/perlivp
%{_mandir}/man1/perlivp*
%{archlib}/CORE/*.h
%if 0%{?os2_version}
%{archlib}/CORE/os2/*.h
%endif
%dir %{privlib}/ExtUtils
%{privlib}/ExtUtils/typemap
%if !0%{?os2_version}
%{_libdir}/libperl.so
%else
%{archlib}/CORE/libperl*.a
%{_libdir}/libperl_dll.a
%endif
%if %{with perl_enables_systemtap}
%dir %{_datadir}/systemtap
%dir %{_datadir}/systemtap/tapset
%{tapsetdir}/%{libperl_stp}
%doc perl-example.stp
%endif

%files macros
%{_rpmmacrodir}/macros.perl

%files tests
%{perl5_testdir}/

%files utils
%{_bindir}/h2ph
%{_bindir}/perlbug
%{_bindir}/perlthanks
%{_bindir}/pl2pm
%if !0%{?os2_version}
%dir %{privlib}/pod
%{privlib}/pod/perlutil.pod
%else
%dir %{privlib}/Pod
%{privlib}/Pod/perlutil.pod
%endif
%{_mandir}/man1/h2ph.*
%{_mandir}/man1/perlbug.*
%{_mandir}/man1/perlthanks.*
%{_mandir}/man1/perlutil.*
%{_mandir}/man1/pl2pm.*

%if %{dual_life} || %{rebuild_from_scratch}
%files Archive-Tar
%{_bindir}/ptar
%{_bindir}/ptardiff
%{_bindir}/ptargrep
%dir %{privlib}/Archive
%{privlib}/Archive/Tar 
%{privlib}/Archive/Tar.pm
%{_mandir}/man1/ptar.1*
%{_mandir}/man1/ptardiff.1*
%{_mandir}/man1/ptargrep.1*
%if !0%{?os2_version}
%{_mandir}/man3/Archive::Tar* 
%else
%{_mandir}/man3/Archive.Tar* 
%endif
%endif

%files Attribute-Handlers
%{privlib}/Attribute
%if !0%{?os2_version}
%{_mandir}/man3/Attribute::Handlers.*
%else
%{_mandir}/man3/Attribute.Handlers.*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files autodie
%{privlib}/autodie/
%{privlib}/autodie.pm
%{privlib}/Fatal.pm
%if !0%{?os2_version}
%{_mandir}/man3/autodie.3*
%{_mandir}/man3/autodie::*
%else
%{_mandir}/man3/autodie.*
%endif
%{_mandir}/man3/Fatal.3*
%endif

%files AutoLoader
%{privlib}/AutoLoader.pm
%{_mandir}/man3/AutoLoader.3*

%files AutoSplit
%{privlib}/AutoSplit.pm
%{_mandir}/man3/AutoSplit.3*

%files autouse
%{privlib}/autouse.pm
%{_mandir}/man3/autouse.3*

%files B
%{archlib}/auto/B
%{archlib}/B
%{archlib}/B.pm
%{archlib}/O.pm
%{privlib}/B
%{_mandir}/man3/B.*
%if !0%{?os2_version}
%{_mandir}/man3/B::*
%endif
%{_mandir}/man3/O.*

%files base
%{privlib}/base.pm
%{_mandir}/man3/base.3*

%files Benchmark
%{privlib}/Benchmark.pm
%{_mandir}/man3/Benchmark.*

%if %{dual_life} || %{rebuild_from_scratch}
%files bignum
%{privlib}/bigfloat.pm
%{privlib}/bigint.pm
%{privlib}/bignum.pm
%{privlib}/bigrat.pm
%dir %{privlib}/Math
%{privlib}/Math/BigFloat
%dir %{privlib}/Math/BigInt
%{privlib}/Math/BigInt/Trace.pm
%dir %{privlib}/Math/BigRat
%{privlib}/Math/BigRat/Trace.pm
%{_mandir}/man3/bigfloat.*
%{_mandir}/man3/bigint.*
%{_mandir}/man3/bignum.*
%{_mandir}/man3/bigrat.*
%endif

%files blib
%{privlib}/blib.pm
%{_mandir}/man3/blib.*

%if %{dual_life} || %{rebuild_from_scratch}
%files Carp
%{privlib}/Carp
%{privlib}/Carp.*
%{_mandir}/man3/Carp.*
%endif

%files Class-Struct
%{privlib}/Class
%if !0%{?os2_version}
%{_mandir}/man3/Class::Struct.*
%else
%{_mandir}/man3/Class.Struct.*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Compress-Raw-Bzip2
%dir %{archlib}/Compress
%dir %{archlib}/Compress/Raw
%{archlib}/Compress/Raw/Bzip2.pm
%dir %{archlib}/auto/Compress
%dir %{archlib}/auto/Compress/Raw
%{archlib}/auto/Compress/Raw/Bzip2
%if !0%{?os2_version}
%{_mandir}/man3/Compress::Raw::Bzip2*
%else
%{_mandir}/man3/Compress.Raw.Bzip2*
%endif
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Compress-Raw-Zlib
%dir %{archlib}/Compress
%dir %{archlib}/Compress/Raw
%{archlib}/Compress/Raw/Zlib.pm
%dir %{archlib}/auto/Compress
%dir %{archlib}/auto/Compress/Raw
%{archlib}/auto/Compress/Raw/Zlib
%if !0%{?os2_version}
%{_mandir}/man3/Compress::Raw::Zlib*
%else
%{_mandir}/man3/Compress.Raw.Zlib*
%endif
%endif

%files Config-Extensions
%dir %{privlib}/Config
%{privlib}/Config/Extensions.pm
%if !0%{?os2_version}
%{_mandir}/man3/Config::Extensions.*
%else
%{_mandir}/man3/Config.Extensions.*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Config-Perl-V
%dir %{privlib}/Config
%{privlib}/Config/Perl
%if !0%{?os2_version}
%{_mandir}/man3/Config::Perl::V.*
%else
%{_mandir}/man3/Config.Perl.V.*
%endif
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files constant
%{privlib}/constant.pm
%{_mandir}/man3/constant.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files CPAN
%{_bindir}/cpan
%dir %{privlib}/App
%{privlib}/App/Cpan.pm
%{privlib}/CPAN
%{privlib}/CPAN.pm
%{_mandir}/man1/cpan.1*
%if !0%{?os2_version}
%{_mandir}/man3/App::Cpan.*
%else
%{_mandir}/man3/App.Cpan.*
%endif
%{_mandir}/man3/CPAN.*
%if !0%{?os2_version}
%{_mandir}/man3/CPAN:*
%endif
%exclude %{privlib}/CPAN/Meta/
%exclude %{privlib}/CPAN/Meta.pm
%if !0%{?os2_version}
%exclude %{_mandir}/man3/CPAN::Meta*
%else
%exclude %{_mandir}/man3/CPAN.Meta*
%endif
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files CPAN-Meta
%dir %{privlib}/CPAN/Meta
%{privlib}/CPAN/Meta.pm
%{privlib}/CPAN/Meta/Converter.pm
%{privlib}/CPAN/Meta/Feature.pm
%dir %{privlib}/CPAN/Meta/History
%{privlib}/CPAN/Meta/History/Meta*
%{privlib}/CPAN/Meta/History.pm
%{privlib}/CPAN/Meta/Merge.pm
%{privlib}/CPAN/Meta/Prereqs.pm
%{privlib}/CPAN/Meta/Spec.pm
%{privlib}/CPAN/Meta/Validator.pm
%dir %{privlib}/Parse/
%dir %{privlib}/Parse/CPAN/
%{privlib}/Parse/CPAN/Meta.pm
%if !0%{?os2_version}
%{_mandir}/man3/CPAN::Meta*
%{_mandir}/man3/Parse::CPAN::Meta.3*
%exclude %{_mandir}/man3/CPAN::Meta::YAML*
%exclude %{_mandir}/man3/CPAN::Meta::Requirements*
%else
%{_mandir}/man3/CPAN.Meta*
%{_mandir}/man3/Parse.CPAN.Meta.3*
%exclude %{_mandir}/man3/CPAN.Meta.YAML*
%exclude %{_mandir}/man3/CPAN.Meta.Requirements*
%endif
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files CPAN-Meta-Requirements
%dir %{privlib}/CPAN
%dir %{privlib}/CPAN/Meta
%{privlib}/CPAN/Meta/Requirements.pm
%if !0%{?os2_version}
%{_mandir}/man3/CPAN::Meta::Requirements.3*
%else
%{_mandir}/man3/CPAN.Meta.Requirements.3*
%endif
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files CPAN-Meta-YAML
%dir %{privlib}/CPAN
%dir %{privlib}/CPAN/Meta
%{privlib}/CPAN/Meta/YAML.pm
%if !0%{?os2_version}
%{_mandir}/man3/CPAN::Meta::YAML*
%else
%{_mandir}/man3/CPAN.Meta.YAML*
%endif
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Data-Dumper
%dir %{archlib}/auto/Data
%dir %{archlib}/auto/Data/Dumper
%if !0%{?os2_version}
%{archlib}/auto/Data/Dumper/Dumper.so
%else
%{archlib}/auto/Data/Dumper/DumperTR.dll
%endif
%dir %{archlib}/Data
%{archlib}/Data/Dumper.pm
%if !0%{?os2_version}
%{_mandir}/man3/Data::Dumper.3*
%else
%{_mandir}/man3/Data.Dumper.3*
%endif
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%if %{with bdb}
%files DB_File
%{archlib}/DB_File.pm
%dir %{archlib}/auto/DB_File
%{archlib}/auto/DB_File/DB_File.so
%{_mandir}/man3/DB_File*
%endif
%endif

%files DBM_Filter
%{privlib}/DBM_Filter
%{privlib}/DBM_Filter.pm
%{_mandir}/man3/DBM_Filter.*
%if !0%{?os2_version}
%{_mandir}/man3/DBM_Filter::*
%endif

%files debugger
%{privlib}/DB.pm
%{privlib}/dumpvar.pl
%{privlib}/perl5db.pl
%if !0%{?os2_version}
%dir %{privlib}/pod
%{privlib}/pod/perldebug.pod
%else
%dir %{privlib}/Pod
%{privlib}/Pod/perldebug.pod
%endif
%{_mandir}/man1/perldebug.*
%{_mandir}/man3/DB.*

%files deprecate
%{privlib}/deprecate.pm
%{_mandir}/man3/deprecate.*

%files Devel-Peek
%dir %{archlib}/Devel
%{archlib}/Devel/Peek.pm
%dir %{archlib}/auto/Devel
%{archlib}/auto/Devel/Peek
%if !0%{?os2_version}
%{_mandir}/man3/Devel::Peek.*
%else
%{_mandir}/man3/Devel.Peek.*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Devel-PPPort
%dir %{archlib}/Devel
%{archlib}/Devel/PPPort.pm
%if !0%{?os2_version}
%{_mandir}/man3/Devel::PPPort.3*
%else
%{_mandir}/man3/Devel.PPPort.3*
%endif
%endif

%files Devel-SelfStubber
%dir %{privlib}/Devel
%{privlib}/Devel/SelfStubber.pm
%if !0%{?os2_version}
%{_mandir}/man3/Devel::SelfStubber.*
%else
%{_mandir}/man3/Devel.SelfStubber.*
%endif

%files diagnostics
%{_bindir}/splain
%{privlib}/diagnostics.pm
%if !0%{?os2_version}
%dir %{privlib}/pod
%{privlib}/pod/perldiag.pod
%else
%dir %{privlib}/Pod
%{privlib}/Pod/perldiag.pod
%endif
%{_mandir}/man1/perldiag.*
%{_mandir}/man1/splain.*
%{_mandir}/man3/diagnostics.*

%if %{dual_life} || %{rebuild_from_scratch}
%files Digest
%{privlib}/Digest.pm
%dir %{privlib}/Digest
%{privlib}/Digest/base.pm
%{privlib}/Digest/file.pm
%{_mandir}/man3/Digest.3*
%if !0%{?os2_version}
%{_mandir}/man3/Digest::base.3*
%{_mandir}/man3/Digest::file.3*
%else
%{_mandir}/man3/Digest.base.3*
%{_mandir}/man3/Digest.file.3*
%endif
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Digest-MD5
%dir %{archlib}/Digest
%{archlib}/Digest/MD5.pm
%dir %{archlib}/auto/Digest
%{archlib}/auto/Digest/MD5
%if !0%{?os2_version}
%{_mandir}/man3/Digest::MD5.3*
%else
%{_mandir}/man3/Digest.MD5.3*
%endif
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Digest-SHA
%{_bindir}/shasum
%dir %{archlib}/Digest
%{archlib}/Digest/SHA.pm
%dir %{archlib}/auto/Digest
%{archlib}/auto/Digest/SHA
%{_mandir}/man1/shasum.1*
%if !0%{?os2_version}
%{_mandir}/man3/Digest::SHA.3*
%else
%{_mandir}/man3/Digest.SHA.3*
%endif
%endif

%files DirHandle
%{privlib}/DirHandle.pm
%{_mandir}/man3/DirHandle.3*

%files doc
%if !0%{?os2_version}
%dir %{privlib}/pod
%{privlib}/pod/perl5*delta.pod
%{privlib}/pod/perlaix.pod
%{privlib}/pod/perlamiga.pod
%{privlib}/pod/perlandroid.pod
%{privlib}/pod/perlapi.pod
%{privlib}/pod/perlapio.pod
%{privlib}/pod/perlartistic.pod
%{privlib}/pod/perlbook.pod
%{privlib}/pod/perlboot.pod
%{privlib}/pod/perlbot.pod
%{privlib}/pod/perlbs2000.pod
%{privlib}/pod/perlcall.pod
%{privlib}/pod/perlcheat.pod
%{privlib}/pod/perlclass.pod
%{privlib}/pod/perlclassguts.pod
%{privlib}/pod/perlclib.pod
%{privlib}/pod/perlcn.pod
%{privlib}/pod/perlcommunity.pod
%{privlib}/pod/perlcygwin.pod
%{privlib}/pod/perldata.pod
%{privlib}/pod/perldbmfilter.pod
%{privlib}/pod/perldebguts.pod
%{privlib}/pod/perldebtut.pod
%{privlib}/pod/perldelta.pod
%{privlib}/pod/perldeprecation.pod
%{privlib}/pod/perldocstyle.pod
%{privlib}/pod/perldsc.pod
%{privlib}/pod/perldtrace.pod
%{privlib}/pod/perlebcdic.pod
%{privlib}/pod/perlembed.pod
%{privlib}/pod/perlexperiment.pod
%{privlib}/pod/perlfork.pod
%{privlib}/pod/perlform.pod
%{privlib}/pod/perlfreebsd.pod
%{privlib}/pod/perlfunc.pod
%{privlib}/pod/perlgit.pod
%{privlib}/pod/perlgov.pod
%{privlib}/pod/perlgpl.pod
%{privlib}/pod/perlguts.pod
%{privlib}/pod/perlhack.pod
%{privlib}/pod/perlhacktips.pod
%{privlib}/pod/perlhacktut.pod
%{privlib}/pod/perlhaiku.pod
%{privlib}/pod/perlhist.pod
%{privlib}/pod/perlhpux.pod
%{privlib}/pod/perlhurd.pod
%{privlib}/pod/perlintern.pod
%{privlib}/pod/perlinterp.pod
%{privlib}/pod/perlintro.pod
%{privlib}/pod/perliol.pod
%{privlib}/pod/perlipc.pod
%{privlib}/pod/perlirix.pod
%{privlib}/pod/perljp.pod
%{privlib}/pod/perlko.pod
%{privlib}/pod/perllexwarn.pod
%{privlib}/pod/perllinux.pod
%{privlib}/pod/perllocale.pod
%{privlib}/pod/perllol.pod
%{privlib}/pod/perlmacosx.pod
%{privlib}/pod/perlmod.pod
%{privlib}/pod/perlmodinstall.pod
%{privlib}/pod/perlmodlib.pod
%{privlib}/pod/perlmodstyle.pod
%{privlib}/pod/perlmroapi.pod
%{privlib}/pod/perlnewmod.pod
%{privlib}/pod/perlnumber.pod
%{privlib}/pod/perlobj.pod
%{privlib}/pod/perlootut.pod
%{privlib}/pod/perlop.pod
%{privlib}/pod/perlopenbsd.pod
%{privlib}/pod/perlopentut.pod
%{privlib}/pod/perlos2.pod
%{privlib}/pod/perlos390.pod
%{privlib}/pod/perlos400.pod
%{privlib}/pod/perlpacktut.pod
%{privlib}/pod/perlperf.pod
%{privlib}/pod/perlplan9.pod
%{privlib}/pod/perlpod.pod
%{privlib}/pod/perlpodspec.pod
%{privlib}/pod/perlpolicy.pod
%{privlib}/pod/perlport.pod
%{privlib}/pod/perlpragma.pod
%{privlib}/pod/perlqnx.pod
%{privlib}/pod/perlre.pod
%{privlib}/pod/perlreapi.pod
%{privlib}/pod/perlrebackslash.pod
%{privlib}/pod/perlrecharclass.pod
%{privlib}/pod/perlref.pod
%{privlib}/pod/perlreftut.pod
%{privlib}/pod/perlreguts.pod
%{privlib}/pod/perlrepository.pod
%{privlib}/pod/perlrequick.pod
%{privlib}/pod/perlreref.pod
%{privlib}/pod/perlretut.pod
%{privlib}/pod/perlriscos.pod
%{privlib}/pod/perlsec.pod
%{privlib}/pod/perlsecpolicy.pod
%{privlib}/pod/perlsolaris.pod
%{privlib}/pod/perlsource.pod
%{privlib}/pod/perlstyle.pod
%{privlib}/pod/perlsub.pod
%{privlib}/pod/perlsyn.pod
%{privlib}/pod/perlsynology.pod
%{privlib}/pod/perlthrtut.pod
%{privlib}/pod/perltie.pod
%{privlib}/pod/perltoc.pod
%{privlib}/pod/perltodo.pod
%{privlib}/pod/perltooc.pod
%{privlib}/pod/perltoot.pod
%{privlib}/pod/perltrap.pod
%{privlib}/pod/perltru64.pod
%{privlib}/pod/perltw.pod
%{privlib}/pod/perlunicode.pod
%{privlib}/pod/perlunicook.pod
%{privlib}/pod/perlunifaq.pod
%{privlib}/pod/perluniintro.pod
%{privlib}/pod/perluniprops.pod
%{privlib}/pod/perlunitut.pod
%{privlib}/pod/perlvar.pod
%{privlib}/pod/perlvms.pod
%{privlib}/pod/perlvos.pod
%{privlib}/pod/perlwin32.pod
%else
%dir %{privlib}/Pod
%{privlib}/Pod/perl5*delta.pod
%{privlib}/Pod/perlaix.pod
%{privlib}/Pod/perlamiga.pod
%{privlib}/Pod/perlandroid.pod
%{privlib}/Pod/perlapi.pod
%{privlib}/Pod/perlapio.pod
%{privlib}/Pod/perlartistic.pod
%{privlib}/Pod/perlbook.pod
%{privlib}/Pod/perlboot.pod
%{privlib}/Pod/perlbot.pod
%{privlib}/Pod/perlbs2000.pod
%{privlib}/Pod/perlcall.pod
%{privlib}/Pod/perlcheat.pod
%{privlib}/Pod/perlclass.pod
%{privlib}/Pod/perlclassguts.pod
%{privlib}/Pod/perlclib.pod
%{privlib}/Pod/perlcn.pod
%{privlib}/Pod/perlcommunity.pod
%{privlib}/Pod/perlcygwin.pod
%{privlib}/Pod/perldata.pod
%{privlib}/Pod/perldbmfilter.pod
%{privlib}/Pod/perldebguts.pod
%{privlib}/Pod/perldebtut.pod
%{privlib}/Pod/perldelta.pod
%{privlib}/Pod/perldeprecation.pod
%{privlib}/Pod/perldocstyle.pod
%{privlib}/Pod/perldsc.pod
%{privlib}/Pod/perldtrace.pod
%{privlib}/Pod/perlebcdic.pod
%{privlib}/Pod/perlembed.pod
%{privlib}/Pod/perlexperiment.pod
%{privlib}/Pod/perlfork.pod
%{privlib}/Pod/perlform.pod
%{privlib}/Pod/perlfreebsd.pod
%{privlib}/Pod/perlfunc.pod
%{privlib}/Pod/perlgit.pod
%{privlib}/Pod/perlgov.pod
%{privlib}/Pod/perlgpl.pod
%{privlib}/Pod/perlguts.pod
%{privlib}/Pod/perlhack.pod
%{privlib}/Pod/perlhacktips.pod
%{privlib}/Pod/perlhacktut.pod
%{privlib}/Pod/perlhaiku.pod
%{privlib}/Pod/perlhist.pod
%{privlib}/Pod/perlhpux.pod
%{privlib}/Pod/perlhurd.pod
%{privlib}/Pod/perlintern.pod
%{privlib}/Pod/perlinterp.pod
%{privlib}/Pod/perlintro.pod
%{privlib}/Pod/perliol.pod
%{privlib}/Pod/perlipc.pod
%{privlib}/Pod/perlirix.pod
%{privlib}/Pod/perljp.pod
%{privlib}/Pod/perlko.pod
%{privlib}/Pod/perllexwarn.pod
%{privlib}/Pod/perllinux.pod
%{privlib}/Pod/perllocale.pod
%{privlib}/Pod/perllol.pod
%{privlib}/Pod/perlmacosx.pod
%{privlib}/Pod/perlmod.pod
%{privlib}/Pod/perlmodinstall.pod
%{privlib}/Pod/perlmodlib.pod
%{privlib}/Pod/perlmodstyle.pod
%{privlib}/Pod/perlmroapi.pod
%{privlib}/Pod/perlnewmod.pod
%{privlib}/Pod/perlnumber.pod
%{privlib}/Pod/perlobj.pod
%{privlib}/Pod/perlootut.pod
%{privlib}/Pod/perlop.pod
%{privlib}/Pod/perlopenbsd.pod
%{privlib}/Pod/perlopentut.pod
%{privlib}/Pod/perlos2.pod
%{privlib}/Pod/perlos390.pod
%{privlib}/Pod/perlos400.pod
%{privlib}/Pod/perlpacktut.pod
%{privlib}/Pod/perlperf.pod
%{privlib}/Pod/perlplan9.pod
%{privlib}/Pod/perlpod.pod
%{privlib}/Pod/perlpodspec.pod
%{privlib}/Pod/perlpolicy.pod
%{privlib}/Pod/perlport.pod
%{privlib}/Pod/perlpragma.pod
%{privlib}/Pod/perlqnx.pod
%{privlib}/Pod/perlre.pod
%{privlib}/Pod/perlreapi.pod
%{privlib}/Pod/perlrebackslash.pod
%{privlib}/Pod/perlrecharclass.pod
%{privlib}/Pod/perlref.pod
%{privlib}/Pod/perlreftut.pod
%{privlib}/Pod/perlreguts.pod
%{privlib}/Pod/perlrepository.pod
%{privlib}/Pod/perlrequick.pod
%{privlib}/Pod/perlreref.pod
%{privlib}/Pod/perlretut.pod
%{privlib}/Pod/perlriscos.pod
%{privlib}/Pod/perlsec.pod
%{privlib}/Pod/perlsecpolicy.pod
%{privlib}/Pod/perlsolaris.pod
%{privlib}/Pod/perlsource.pod
%{privlib}/Pod/perlstyle.pod
%{privlib}/Pod/perlsub.pod
%{privlib}/Pod/perlsyn.pod
%{privlib}/Pod/perlsynology.pod
%{privlib}/Pod/perlthrtut.pod
%{privlib}/Pod/perltie.pod
%{privlib}/Pod/perltoc.pod
%{privlib}/Pod/perltodo.pod
%{privlib}/Pod/perltooc.pod
%{privlib}/Pod/perltoot.pod
%{privlib}/Pod/perltrap.pod
%{privlib}/Pod/perltru64.pod
%{privlib}/Pod/perltw.pod
%{privlib}/Pod/perlunicode.pod
%{privlib}/Pod/perlunicook.pod
%{privlib}/Pod/perlunifaq.pod
%{privlib}/Pod/perluniintro.pod
%{privlib}/Pod/perluniprops.pod
%{privlib}/Pod/perlunitut.pod
%{privlib}/Pod/perlvar.pod
%{privlib}/Pod/perlvms.pod
%{privlib}/Pod/perlvos.pod
%{privlib}/Pod/perlwin32.pod
%endif
%{_mandir}/man1/perl5*delta.*
%{_mandir}/man1/perlaix.*
%{_mandir}/man1/perlamiga.*
%{_mandir}/man1/perlandroid.*
%{_mandir}/man1/perlapi.*
%{_mandir}/man1/perlapio.*
%{_mandir}/man1/perlartistic.*
%{_mandir}/man1/perlbook.*
%{_mandir}/man1/perlboot.*
%{_mandir}/man1/perlbot.*
%{_mandir}/man1/perlbs2000.*
%{_mandir}/man1/perlcall.*
%{_mandir}/man1/perlcheat.*
%{_mandir}/man1/perlclass.*
%{_mandir}/man1/perlclassguts.*
%{_mandir}/man1/perlclib.*
%{_mandir}/man1/perlcn.*
%{_mandir}/man1/perlcommunity.*
%{_mandir}/man1/perlcygwin.*
%{_mandir}/man1/perldata.*
%{_mandir}/man1/perldbmfilter.*
%{_mandir}/man1/perldebguts.*
%{_mandir}/man1/perldebtut.*
%{_mandir}/man1/perldelta.*
%{_mandir}/man1/perldeprecation.*
%{_mandir}/man1/perldocstyle.*
%{_mandir}/man1/perldsc.*
%{_mandir}/man1/perldtrace.*
%{_mandir}/man1/perlebcdic.*
%{_mandir}/man1/perlembed.*
%{_mandir}/man1/perlexperiment.*
%{_mandir}/man1/perlfork.*
%{_mandir}/man1/perlform.*
%{_mandir}/man1/perlfreebsd.*
%{_mandir}/man1/perlfunc.*
%{_mandir}/man1/perlgit.*
%{_mandir}/man1/perlgov.*
%{_mandir}/man1/perlgpl.*
%{_mandir}/man1/perlguts.*
%{_mandir}/man1/perlhack.*
%{_mandir}/man1/perlhacktips.*
%{_mandir}/man1/perlhacktut.*
%{_mandir}/man1/perlhaiku.*
%{_mandir}/man1/perlhist.*
%{_mandir}/man1/perlhpux.*
%{_mandir}/man1/perlhurd.*
%{_mandir}/man1/perlintern.*
%{_mandir}/man1/perlinterp.*
%{_mandir}/man1/perlintro.*
%{_mandir}/man1/perliol.*
%{_mandir}/man1/perlipc.*
%{_mandir}/man1/perlirix.*
%{_mandir}/man1/perljp.*
%{_mandir}/man1/perlko.*
%{_mandir}/man1/perllexwarn.*
%{_mandir}/man1/perllinux.*
%{_mandir}/man1/perllocale.*
%{_mandir}/man1/perllol.*
%{_mandir}/man1/perlmacosx.*
%{_mandir}/man1/perlmod.*
%{_mandir}/man1/perlmodinstall.*
%{_mandir}/man1/perlmodlib.*
%{_mandir}/man1/perlmodstyle.*
%{_mandir}/man1/perlmroapi.*
%{_mandir}/man1/perlnewmod.*
%{_mandir}/man1/perlnumber.*
%{_mandir}/man1/perlobj.*
%{_mandir}/man1/perlootut.*
%{_mandir}/man1/perlop.*
%{_mandir}/man1/perlopenbsd.*
%{_mandir}/man1/perlopentut.*
%{_mandir}/man1/perlos2.*
%{_mandir}/man1/perlos390.*
%{_mandir}/man1/perlos400.*
%{_mandir}/man1/perlpacktut.*
%{_mandir}/man1/perlperf.*
%{_mandir}/man1/perlplan9.*
%{_mandir}/man1/perlpod.*
%{_mandir}/man1/perlpodspec.*
%{_mandir}/man1/perlpolicy.*
%{_mandir}/man1/perlport.*
%{_mandir}/man1/perlpragma.*
%{_mandir}/man1/perlqnx.*
%{_mandir}/man1/perlre.*
%{_mandir}/man1/perlreapi.*
%{_mandir}/man1/perlrebackslash.*
%{_mandir}/man1/perlrecharclass.*
%{_mandir}/man1/perlref.*
%{_mandir}/man1/perlreftut.*
%{_mandir}/man1/perlreguts.*
%{_mandir}/man1/perlrepository.*
%{_mandir}/man1/perlrequick.*
%{_mandir}/man1/perlreref.*
%{_mandir}/man1/perlretut.*
%{_mandir}/man1/perlriscos.*
%{_mandir}/man1/perlsec.*
%{_mandir}/man1/perlsecpolicy.*
%{_mandir}/man1/perlsolaris.*
%{_mandir}/man1/perlsource.*
%{_mandir}/man1/perlstyle.*
%{_mandir}/man1/perlsub.*
%{_mandir}/man1/perlsyn.*
%{_mandir}/man1/perlsynology.*
%{_mandir}/man1/perlthrtut.*
%{_mandir}/man1/perltie.*
%{_mandir}/man1/perltoc.*
%{_mandir}/man1/perltodo.*
%{_mandir}/man1/perltooc.*
%{_mandir}/man1/perltoot.*
%{_mandir}/man1/perltrap.*
%{_mandir}/man1/perltru64.*
%{_mandir}/man1/perltw.*
%{_mandir}/man1/perlunicode.*
%{_mandir}/man1/perlunicook.*
%{_mandir}/man1/perlunifaq.*
%{_mandir}/man1/perluniintro.*
%{_mandir}/man1/perluniprops.*
%{_mandir}/man1/perlunitut.*
%{_mandir}/man1/perlvar.*
%{_mandir}/man1/perlvms.*
%{_mandir}/man1/perlvos.*
%{_mandir}/man1/perlwin32.*

%files Dumpvalue
%{privlib}/Dumpvalue.pm
%{_mandir}/man3/Dumpvalue.3*

%files DynaLoader
%{archlib}/DynaLoader.pm
%{_mandir}/man3/DynaLoader.3*

%if %{dual_life} || %{rebuild_from_scratch}
%files Encode
%{_bindir}/encguess
%{_bindir}/piconv
%{archlib}/Encode*
%{archlib}/auto/Encode*
%{privlib}/Encode
%exclude %{privlib}/Encode/*.e2x
%exclude %{privlib}/Encode/encode.h
%{_mandir}/man1/encguess.1*
%{_mandir}/man1/piconv.1*
%{_mandir}/man3/Encode*.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files encoding
%{archlib}/encoding.pm
%{_mandir}/man3/encoding.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Encode-devel
%{_bindir}/enc2xs
%dir %{privlib}/Encode
%{privlib}/Encode/*.e2x
%{privlib}/Encode/encode.h
%{_mandir}/man1/enc2xs.1*
%endif

%files encoding-warnings
%dir %{privlib}/encoding
%{privlib}/encoding/warnings.pm
%if !0%{?os2_version}
%{_mandir}/man3/encoding::warnings.3*
%else
%{_mandir}/man3/encoding.warnings.3*
%endif

%files English
%{privlib}/English.pm
%{_mandir}/man3/English.3*

%if %{dual_life} || %{rebuild_from_scratch}
%files Env
%{privlib}/Env.pm
%{_mandir}/man3/Env.3*
%endif

%files Errno
%{archlib}/Errno.pm
%{_mandir}/man3/Errno.*

%if %{dual_life} || %{rebuild_from_scratch}
%files Exporter
%{privlib}/Exporter*
%{_mandir}/man3/Exporter*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files experimental
%{privlib}/experimental*
%{privlib}/stable*
%{_mandir}/man3/experimental*
%{_mandir}/man3/stable*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files ExtUtils-CBuilder
%dir %{privlib}/ExtUtils
%{privlib}/ExtUtils/CBuilder
%{privlib}/ExtUtils/CBuilder.pm
%if !0%{?os2_version}
%{_mandir}/man3/ExtUtils::CBuilder*
%else
%{_mandir}/man3/ExtUtils.CBuilder*
%endif
%endif

%files ExtUtils-Constant
%dir %{privlib}/ExtUtils
%{privlib}/ExtUtils/Constant
%{privlib}/ExtUtils/Constant.pm
%if !0%{?os2_version}
%{_mandir}/man3/ExtUtils::Constant::*
%{_mandir}/man3/ExtUtils::Constant.3*
%else
%{_mandir}/man3/ExtUtils.Constant.*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files ExtUtils-Command
%dir %{privlib}/ExtUtils
%{privlib}/ExtUtils/Command.pm
%if !0%{?os2_version}
%{_mandir}/man3/ExtUtils::Command.*
%else
%{_mandir}/man3/ExtUtils.Command.*
%endif
%endif

%files ExtUtils-Embed
%dir %{privlib}/ExtUtils
%{privlib}/ExtUtils/Embed.pm
%if !0%{?os2_version}
%{_mandir}/man3/ExtUtils::Embed*
%else
%{_mandir}/man3/ExtUtils.Embed*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files ExtUtils-Install
%dir %{privlib}/ExtUtils
%{privlib}/ExtUtils/Install.pm
%{privlib}/ExtUtils/Installed.pm
%{privlib}/ExtUtils/Packlist.pm
%if !0%{?os2_version}
%{_mandir}/man3/ExtUtils::Install.3*
%{_mandir}/man3/ExtUtils::Installed.3*
%{_mandir}/man3/ExtUtils::Packlist.3*
%else
%{_mandir}/man3/ExtUtils.Install.3*
%{_mandir}/man3/ExtUtils.Installed.3*
%{_mandir}/man3/ExtUtils.Packlist.3*
%endif
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files ExtUtils-Manifest
%dir %{privlib}/ExtUtils
%{privlib}/ExtUtils/Manifest.pm
%{privlib}/ExtUtils/MANIFEST.SKIP
%if !0%{?os2_version}
%{_mandir}/man3/ExtUtils::Manifest.3*
%else
%{_mandir}/man3/ExtUtils.Manifest.3*
%endif
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files ExtUtils-MakeMaker
%{_bindir}/instmodsh
%dir %{privlib}/ExtUtils
%{privlib}/ExtUtils/Command/
%{privlib}/ExtUtils/Liblist
%{privlib}/ExtUtils/Liblist.pm
%{privlib}/ExtUtils/MakeMaker
%{privlib}/ExtUtils/MakeMaker.pm
%{privlib}/ExtUtils/MM.pm
%{privlib}/ExtUtils/MM_*.pm
%{privlib}/ExtUtils/MY.pm
%{privlib}/ExtUtils/Mkbootstrap.pm
%{privlib}/ExtUtils/Mksymlists.pm
%{privlib}/ExtUtils/testlib.pm
%{_mandir}/man1/instmodsh.1*
%if !0%{?os2_version}
%{_mandir}/man3/ExtUtils::Command::MM*
%{_mandir}/man3/ExtUtils::Liblist.3*
%{_mandir}/man3/ExtUtils::MM.3*
%{_mandir}/man3/ExtUtils::MM_*
%{_mandir}/man3/ExtUtils::MY.3*
%{_mandir}/man3/ExtUtils::MakeMaker*
%{_mandir}/man3/ExtUtils::Mkbootstrap.3*
%{_mandir}/man3/ExtUtils::Mksymlists.3*
%{_mandir}/man3/ExtUtils::testlib.3*
%else
%{_mandir}/man3/ExtUtils.Command.MM*
%{_mandir}/man3/ExtUtils.Liblist.3*
%{_mandir}/man3/ExtUtils.MM.3*
%{_mandir}/man3/ExtUtils.MM_*
%{_mandir}/man3/ExtUtils.MY.3*
%{_mandir}/man3/ExtUtils.MakeMaker*
%{_mandir}/man3/ExtUtils.Mkbootstrap.3*
%{_mandir}/man3/ExtUtils.Mksymlists.3*
%{_mandir}/man3/ExtUtils.testlib.3*
%endif
%endif

%files ExtUtils-Miniperl
%dir %{privlib}/ExtUtils
%{privlib}/ExtUtils/Miniperl.pm
%if !0%{?os2_version}
%{_mandir}/man3/ExtUtils::Miniperl.3*
%else
%{_mandir}/man3/ExtUtils.Miniperl.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%if !0%{?os2_version}
%files ExtUtils-MM-Utils
%dir %{privlib}/ExtUtils
%dir %{privlib}/ExtUtils/MM
%{privlib}/ExtUtils/MM/Utils.pm
%if !0%{?os2_version}
%{_mandir}/man3/ExtUtils::MM::Utils.*
%else
%{_mandir}/man3/ExtUtils.MM.Utils.*
%endif
%endif
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files ExtUtils-ParseXS
%dir %{privlib}/ExtUtils
%dir %{privlib}/ExtUtils/ParseXS
%{privlib}/ExtUtils/ParseXS.pm
%{privlib}/ExtUtils/ParseXS.pod
%{privlib}/ExtUtils/ParseXS/Constants.pm
%{privlib}/ExtUtils/ParseXS/CountLines.pm
%{privlib}/ExtUtils/ParseXS/Eval.pm
%{privlib}/ExtUtils/ParseXS/Node.pm
%{privlib}/ExtUtils/ParseXS/Utilities.pm
%dir %{privlib}/ExtUtils/Typemaps
%{privlib}/ExtUtils/Typemaps.pm
%{privlib}/ExtUtils/Typemaps/Cmd.pm
%{privlib}/ExtUtils/Typemaps/InputMap.pm
%{privlib}/ExtUtils/Typemaps/OutputMap.pm
%{privlib}/ExtUtils/Typemaps/Type.pm
%{privlib}/ExtUtils/xsubpp
%if !0%{?os2_version}
%dir %{privlib}/pod
%{privlib}/pod/perlxs.pod
%{privlib}/pod/perlxstut.pod
%{privlib}/pod/perlxstypemap.pod
%else
%{privlib}/Pod/perlxs.pod
%{privlib}/Pod/perlxstut.pod
%{privlib}/Pod/perlxstypemap.pod
%endif
%{_bindir}/xsubpp
%{_mandir}/man1/perlxs*
%{_mandir}/man1/xsubpp*
%if !0%{?os2_version}
%{_mandir}/man3/ExtUtils::ParseXS.3*
%{_mandir}/man3/ExtUtils::ParseXS::Constants.3*
%{_mandir}/man3/ExtUtils::ParseXS::Eval.3*
%{_mandir}/man3/ExtUtils::ParseXS::Node.3*
%{_mandir}/man3/ExtUtils::ParseXS::Utilities.3*
%{_mandir}/man3/ExtUtils::Typemaps.3*
%{_mandir}/man3/ExtUtils::Typemaps::Cmd.3*
%{_mandir}/man3/ExtUtils::Typemaps::InputMap.3*
%{_mandir}/man3/ExtUtils::Typemaps::OutputMap.3*
%{_mandir}/man3/ExtUtils::Typemaps::Type.3*
%else
%{_mandir}/man3/ExtUtils.ParseXS.3*
%{_mandir}/man3/ExtUtils.ParseXS.Constants.3*
%{_mandir}/man3/ExtUtils.ParseXS.Eval.3*
%{_mandir}/man3/ExtUtils.ParseXS.Node.3*
%{_mandir}/man3/ExtUtils.ParseXS.Utilities.3*
%{_mandir}/man3/ExtUtils.Typemaps.3*
%{_mandir}/man3/ExtUtils.Typemaps.Cmd.3*
%{_mandir}/man3/ExtUtils.Typemaps.InputMap.3*
%{_mandir}/man3/ExtUtils.Typemaps.OutputMap.3*
%{_mandir}/man3/ExtUtils.Typemaps.Type.3*
%endif
%endif

%files Fcntl
%{archlib}/Fcntl.pm
%{archlib}/auto/Fcntl
%{_mandir}/man3/Fcntl.3*

%files fields
%{privlib}/fields.pm
%{_mandir}/man3/fields.3*

%files File-Basename
%dir %{privlib}/File
%{privlib}/File/Basename.pm
%if !0%{?os2_version}
%{_mandir}/man3/File::Basename.3*
%else
%{_mandir}/man3/File.Basename.3*
%endif

%files File-Compare
%dir %{privlib}/File
%{privlib}/File/Compare.pm
%if !0%{?os2_version}
%{_mandir}/man3/File::Compare.3*
%else
%{_mandir}/man3/File.Compare.3*
%endif

%files File-Copy
%dir %{privlib}/File
%{privlib}/File/Copy.pm
%if !0%{?os2_version}
%{_mandir}/man3/File::Copy.3*
%else
%{_mandir}/man3/File.Copy.3*
%endif

%files File-DosGlob
%dir %{archlib}/File
%{archlib}/File/DosGlob.pm
%dir %{archlib}/auto/File
%{archlib}/auto/File/DosGlob
%if !0%{?os2_version}
%{_mandir}/man3/File::DosGlob.3*
%else
%{_mandir}/man3/File.DosGlob.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files File-Fetch
%dir %{privlib}/File
%{privlib}/File/Fetch.pm
%if !0%{?os2_version}
%{_mandir}/man3/File::Fetch.3*
%else
%{_mandir}/man3/File.Fetch.3*
%endif
%endif

%files File-Find
%dir %{privlib}/File
%{privlib}/File/Find.pm
%if !0%{?os2_version}
%{_mandir}/man3/File::Find.3*
%else
%{_mandir}/man3/File.Find.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files File-Path
%dir %{privlib}/File
%{privlib}/File/Path.pm
%if !0%{?os2_version}
%{_mandir}/man3/File::Path.3*
%else
%{_mandir}/man3/File.Path.3*
%endif
%endif

%files File-stat
%dir %{privlib}/File
%{privlib}/File/stat.pm
%if !0%{?os2_version}
%{_mandir}/man3/File::stat.3*
%else
%{_mandir}/man3/File.stat.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files File-Temp
%dir %{privlib}/File
%{privlib}/File/Temp.pm
%if !0%{?os2_version}
%{_mandir}/man3/File::Temp.3*
%else
%{_mandir}/man3/File.Temp.3*
%endif
%endif

%files FileCache
%{privlib}/FileCache.pm
%{_mandir}/man3/FileCache.3*

%files FileHandle
%{privlib}/FileHandle.pm
%{_mandir}/man3/FileHandle.3*

%files filetest
%{privlib}/filetest.pm
%{_mandir}/man3/filetest.3*

%if %{dual_life} || %{rebuild_from_scratch}
%files Filter
%dir %{archlib}/auto/Filter
%{archlib}/auto/Filter/Util
%dir %{archlib}/Filter
%{archlib}/Filter/Util
%if !0%{?os2_version}
%{privlib}/pod/perlfilter.pod
%else
%{privlib}/Pod/perlfilter.pod
%endif
%{_mandir}/man1/perlfilter.*
%if !0%{?os2_version}
%{_mandir}/man3/Filter::Util::*
%else
%{_mandir}/man3/Filter.Util.*
%endif
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Filter-Simple
%dir %{privlib}/Filter
%{privlib}/Filter/Simple.pm
%if !0%{?os2_version}
%{_mandir}/man3/Filter::Simple.3*
%else
%{_mandir}/man3/Filter.Simple.3*
%endif
%endif

%files FindBin
%{privlib}/FindBin.pm
%{_mandir}/man3/FindBin.*

%if %{with gdbm}
%files GDBM_File
%{archlib}/GDBM_File.pm
%{archlib}/auto/GDBM_File
%{_mandir}/man3/GDBM_File.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Getopt-Long
%dir %{privlib}/Getopt
%dir %{privlib}/Getopt/Long
%{privlib}/Getopt/Long.pm
%{privlib}/Getopt/Long/Parser.pm
%if !0%{?os2_version}
%{_mandir}/man3/Getopt::Long.3*
%{_mandir}/man3/Getopt::Long::Parser.3*
%else
%{_mandir}/man3/Getopt.Long.3*
%{_mandir}/man3/Getopt.Long.Parser.3*
%endif
%endif

%files Getopt-Std
%dir %{privlib}/Getopt
%{privlib}/Getopt/Std.pm
%if !0%{?os2_version}
%{_mandir}/man3/Getopt::Std.3*
%else
%{_mandir}/man3/Getopt.Std.3*
%endif

%files Hash-Util
%dir %{archlib}/Hash
%{archlib}/Hash/Util.pm
%dir %{archlib}/auto/Hash
%dir %{archlib}/auto/Hash/Util
%if !0%{?os2_version}
%{archlib}/auto/Hash/Util/Util.so
%else
%{archlib}/auto/Hash/Util/UtilWX.dll
%endif
%if !0%{?os2_version}
%{_mandir}/man3/Hash::Util.3*
%else
%{_mandir}/man3/Hash.Util.3*
%endif

%files Hash-Util-FieldHash
%dir %{archlib}/auto/Hash
%dir %{archlib}/auto/Hash/Util
%{archlib}/auto/Hash/Util/FieldHash
%dir %{archlib}/Hash
%dir %{archlib}/Hash/Util
%{archlib}/Hash/Util/FieldHash.pm
%if !0%{?os2_version}
%{_mandir}/man3/Hash::Util::FieldHash.3*
%else
%{_mandir}/man3/Hash.Util.FieldHash.3*
%endif

%files if
%{privlib}/if.pm
%{_mandir}/man3/if.3*

%files IO
%dir %{archlib}/IO
%{archlib}/IO.pm
%{archlib}/IO/Dir.pm
%{archlib}/IO/File.pm
%{archlib}/IO/Handle.pm
%{archlib}/IO/Pipe.pm
%{archlib}/IO/Poll.pm
%{archlib}/IO/Seekable.pm
%{archlib}/IO/Select.pm
%dir %{archlib}/IO/Socket
%{archlib}/IO/Socket/INET.pm
%{archlib}/IO/Socket/UNIX.pm
%{archlib}/IO/Socket.pm
%dir %{archlib}/auto/IO
%if !0%{?os2_version}
%{archlib}/auto/IO/IO.so
%else
%{archlib}/auto/IO/IOGI.dll
%endif
%if !0%{?os2_version}
%{_mandir}/man3/IO.*
%{_mandir}/man3/IO::Dir.*
%{_mandir}/man3/IO::File.*
%{_mandir}/man3/IO::Handle.*
%{_mandir}/man3/IO::Pipe.*
%{_mandir}/man3/IO::Poll.*
%{_mandir}/man3/IO::Seekable.*
%{_mandir}/man3/IO::Select.*
%{_mandir}/man3/IO::Socket::INET.*
%{_mandir}/man3/IO::Socket::UNIX.*
%{_mandir}/man3/IO::Socket.*
%else
%{_mandir}/man3/IO.3*
%{_mandir}/man3/IO.Dir.*
%{_mandir}/man3/IO.File.*
%{_mandir}/man3/IO.Handle.*
%{_mandir}/man3/IO.Pipe.*
%{_mandir}/man3/IO.Poll.*
%{_mandir}/man3/IO.Seekable.*
%{_mandir}/man3/IO.Select.*
%{_mandir}/man3/IO.Socket.INET.*
%{_mandir}/man3/IO.Socket.UNIX.*
%{_mandir}/man3/IO.Socket.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files IO-Compress
# IO-Compress
%{_bindir}/streamzip
%{_bindir}/zipdetails
%dir %{privlib}/IO
%dir %{privlib}/IO/Compress
%{privlib}/IO/Compress.pm
%{privlib}/IO/Compress/FAQ.pod
%{_mandir}/man1/streamzip.*
%{_mandir}/man1/zipdetails.*
%if !0%{?os2_version}
%{_mandir}/man3/IO::Compress.3*
%{_mandir}/man3/IO::Compress::FAQ.*
%else
%{_mandir}/man3/IO.Compress.3*
%{_mandir}/man3/IO.Compress.FAQ.*
%endif
# Compress-Zlib
%dir %{privlib}/Compress
%{privlib}/Compress/Zlib.pm
%if !0%{?os2_version}
%{_mandir}/man3/Compress::Zlib*
%else
%{_mandir}/man3/Compress.Zlib*
%endif
#IO-Compress-Base
%dir %{privlib}/File
%{privlib}/File/GlobMapper.pm
%{privlib}/IO/Compress/Base
%{privlib}/IO/Compress/Base.pm
%dir %{privlib}/IO/Uncompress
%{privlib}/IO/Uncompress/AnyUncompress.pm
%{privlib}/IO/Uncompress/Base.pm
%if !0%{?os2_version}
%{_mandir}/man3/File::GlobMapper.*
%{_mandir}/man3/IO::Compress::Base.*
%{_mandir}/man3/IO::Uncompress::AnyUncompress.*
%{_mandir}/man3/IO::Uncompress::Base.*
%else
%{_mandir}/man3/File.GlobMapper.*
%{_mandir}/man3/IO.Compress.Base.*
%{_mandir}/man3/IO.Uncompress.AnyUncompress.*
%{_mandir}/man3/IO.Uncompress.Base.*
%endif
# IO-Compress-Zlib
%{privlib}/IO/Compress/Adapter
%{privlib}/IO/Compress/Deflate.pm
%{privlib}/IO/Compress/Bzip2.pm
%{privlib}/IO/Compress/Gzip
%{privlib}/IO/Compress/Gzip.pm
%{privlib}/IO/Compress/RawDeflate.pm
%{privlib}/IO/Compress/Zip
%{privlib}/IO/Compress/Zip.pm
%{privlib}/IO/Compress/Zlib
%{privlib}/IO/Uncompress/Adapter/
%{privlib}/IO/Uncompress/AnyInflate.pm
%{privlib}/IO/Uncompress/Bunzip2.pm
%{privlib}/IO/Uncompress/Gunzip.pm
%{privlib}/IO/Uncompress/Inflate.pm
%{privlib}/IO/Uncompress/RawInflate.pm
%{privlib}/IO/Uncompress/Unzip.pm
%if !0%{?os2_version}
%{_mandir}/man3/IO::Compress::Deflate*
%{_mandir}/man3/IO::Compress::Gzip*
%{_mandir}/man3/IO::Compress::Bzip2*
%{_mandir}/man3/IO::Compress::RawDeflate*
%{_mandir}/man3/IO::Compress::Zip*
%{_mandir}/man3/IO::Uncompress::AnyInflate*
%{_mandir}/man3/IO::Uncompress::Bunzip2*
%{_mandir}/man3/IO::Uncompress::Gunzip*
%{_mandir}/man3/IO::Uncompress::Inflate*
%{_mandir}/man3/IO::Uncompress::RawInflate*
%{_mandir}/man3/IO::Uncompress::Unzip*
%else
%{_mandir}/man3/IO.Compress.Deflate*
%{_mandir}/man3/IO.Compress.Gzip*
%{_mandir}/man3/IO.Compress.Bzip2*
%{_mandir}/man3/IO.Compress.RawDeflate*
%{_mandir}/man3/IO.Compress.Zip*
%{_mandir}/man3/IO.Uncompress.AnyInflate*
%{_mandir}/man3/IO.Uncompress.Bunzip2*
%{_mandir}/man3/IO.Uncompress.Gunzip*
%{_mandir}/man3/IO.Uncompress.Inflate*
%{_mandir}/man3/IO.Uncompress.RawInflate*
%{_mandir}/man3/IO.Uncompress.Unzip*
%endif
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files IO-Socket-IP
%dir %{privlib}/IO
%dir %{privlib}/IO/Socket
%{privlib}/IO/Socket/IP.pm
%if !0%{?os2_version}
%{_mandir}/man3/IO::Socket::IP.*
%else
%{_mandir}/man3/IO.Socket.IP.*
%endif
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files IO-Zlib
%dir %{privlib}/IO
%{privlib}/IO/Zlib.pm
%if !0%{?os2_version}
%{_mandir}/man3/IO::Zlib.*
%else
%{_mandir}/man3/IO.Zlib.*
%endif
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files HTTP-Tiny
%dir %{privlib}/HTTP
%{privlib}/HTTP/Tiny.pm
%if !0%{?os2_version}
%{_mandir}/man3/HTTP::Tiny*
%else
%{_mandir}/man3/HTTP.Tiny*
%endif
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files IPC-Cmd
%dir %{privlib}/IPC
%{privlib}/IPC/Cmd.pm
%if !0%{?os2_version}
%{_mandir}/man3/IPC::Cmd.3*
%else
%{_mandir}/man3/IPC.Cmd.3*
%endif
%endif

%files IPC-Open3
%dir %{privlib}/IPC
%{privlib}/IPC/Open2.pm
%{privlib}/IPC/Open3.pm
%if !0%{?os2_version}
%{_mandir}/man3/IPC::Open2.3*
%{_mandir}/man3/IPC::Open3.3*
%else
%{_mandir}/man3/IPC.Open2.3*
%{_mandir}/man3/IPC.Open3.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files IPC-SysV
%{archlib}/auto/IPC
%dir %{archlib}/IPC
%{archlib}/IPC/Msg.pm
%{archlib}/IPC/Semaphore.pm
%{archlib}/IPC/SharedMem.pm
%{archlib}/IPC/SysV.pm
%if !0%{?os2_version}
%{_mandir}/man3/IPC::Msg.*
%{_mandir}/man3/IPC::Semaphore.*
%{_mandir}/man3/IPC::SharedMem.*
%{_mandir}/man3/IPC::SysV.*
%else
%{_mandir}/man3/IPC.Msg.*
%{_mandir}/man3/IPC.Semaphore.*
%{_mandir}/man3/IPC.SharedMem.*
%{_mandir}/man3/IPC.SysV.*
%endif
%endif

%files I18N-Collate
%dir %{privlib}/I18N
%{privlib}/I18N/Collate.pm
%if !0%{?os2_version}
%{_mandir}/man3/I18N::Collate.*
%else
%{_mandir}/man3/I18N.Collate.*
%endif

%files I18N-Langinfo
%{archlib}/auto/I18N
%{archlib}/I18N
%if !0%{?os2_version}
%{_mandir}/man3/I18N::Langinfo.*
%else
%{_mandir}/man3/I18N.Langinfo.*
%endif

%files I18N-LangTags
%dir %{privlib}/I18N
%{privlib}/I18N/LangTags
%{privlib}/I18N/LangTags.pm
%if !0%{?os2_version}
%{_mandir}/man3/I18N::LangTags.*
%{_mandir}/man3/I18N::LangTags::*
%else
%{_mandir}/man3/I18N.LangTags.*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files JSON-PP
%{_bindir}/json_pp
%dir %{privlib}/JSON
%{privlib}/JSON/PP
%{privlib}/JSON/PP.pm
%{_mandir}/man1/json_pp.1*
%if !0%{?os2_version}
%{_mandir}/man3/JSON::PP.3*
%{_mandir}/man3/JSON::PP::Boolean.3pm*
%else
%{_mandir}/man3/JSON.PP.3*
%{_mandir}/man3/JSON.PP.Boolean.3pm*
%endif
%endif

%files less
%{privlib}/less.pm
%{_mandir}/man3/less.*

%files lib
%{archlib}/lib.pm
%{_mandir}/man3/lib.*

%if %{dual_life} || %{rebuild_from_scratch}
%files libnet
%dir %{privlib}/Net
%{privlib}/Net/Cmd.pm
%{privlib}/Net/Config.pm
%{privlib}/Net/Domain.pm
%{privlib}/Net/FTP
%{privlib}/Net/FTP.pm
%{privlib}/Net/libnetFAQ.pod
%{privlib}/Net/NNTP.pm
%{privlib}/Net/Netrc.pm
%{privlib}/Net/POP3.pm
%{privlib}/Net/SMTP.pm
%{privlib}/Net/Time.pm
%if !0%{?os2_version}
%{_mandir}/man3/Net::Cmd.*
%{_mandir}/man3/Net::Config.*
%{_mandir}/man3/Net::Domain.*
%{_mandir}/man3/Net::FTP.*
%{_mandir}/man3/Net::libnetFAQ.*
%{_mandir}/man3/Net::NNTP.*
%{_mandir}/man3/Net::Netrc.*
%{_mandir}/man3/Net::POP3.*
%{_mandir}/man3/Net::SMTP.*
%{_mandir}/man3/Net::Time.*
%else
%{_mandir}/man3/Net.Cmd.*
%{_mandir}/man3/Net.Config.*
%{_mandir}/man3/Net.Domain.*
%{_mandir}/man3/Net.FTP.*
%{_mandir}/man3/Net.libnetFAQ.*
%{_mandir}/man3/Net.NNTP.*
%{_mandir}/man3/Net.Netrc.*
%{_mandir}/man3/Net.POP3.*
%{_mandir}/man3/Net.SMTP.*
%{_mandir}/man3/Net.Time.*
%endif
%endif

%files libnetcfg
%{_bindir}/libnetcfg
%{_mandir}/man1/libnetcfg*

%files locale
%{privlib}/locale.pm
%{_mandir}/man3/locale.*

%if %{dual_life} || %{rebuild_from_scratch}
%files Locale-Maketext
%dir %{privlib}/Locale
%dir %{privlib}/Locale/Maketext
%{privlib}/Locale/Maketext.*
%{privlib}/Locale/Maketext/Cookbook.*
%{privlib}/Locale/Maketext/Guts.*
%{privlib}/Locale/Maketext/GutsLoader.*
%{privlib}/Locale/Maketext/TPJ13.*
%if !0%{?os2_version}
%{_mandir}/man3/Locale::Maketext.*
%{_mandir}/man3/Locale::Maketext::Cookbook.*
%{_mandir}/man3/Locale::Maketext::Guts.*
%{_mandir}/man3/Locale::Maketext::GutsLoader.*
%{_mandir}/man3/Locale::Maketext::TPJ13.*
%else
%{_mandir}/man3/Locale.Maketext.3*
%{_mandir}/man3/Locale.Maketext.Cookbook.*
%{_mandir}/man3/Locale.Maketext.Guts.*
%{_mandir}/man3/Locale.Maketext.GutsLoader.*
%{_mandir}/man3/Locale.Maketext.TPJ13.*
%endif
%endif

%files Locale-Maketext-Simple
%dir %{privlib}/Locale
%dir %{privlib}/Locale/Maketext
%{privlib}/Locale/Maketext/Simple.pm
%if !0%{?os2_version}
%{_mandir}/man3/Locale::Maketext::Simple.*
%else
%{_mandir}/man3/Locale.Maketext.Simple.*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Math-BigInt
%dir %{privlib}/Math
%{privlib}/Math/BigFloat.pm
%{privlib}/Math/BigInt.pm
%dir %{privlib}/Math/BigInt
%{privlib}/Math/BigInt/Calc.pm
%{privlib}/Math/BigInt/Lib.pm
%{privlib}/Math/BigRat.pm
%if !0%{?os2_version}
%{_mandir}/man3/Math::BigFloat.*
%{_mandir}/man3/Math::BigInt.*
%{_mandir}/man3/Math::BigInt::Calc.*
%{_mandir}/man3/Math::BigInt::Lib.*
%{_mandir}/man3/Math::BigRat.*
%else
%{_mandir}/man3/Math.BigFloat.*
%{_mandir}/man3/Math.BigInt.3*
%{_mandir}/man3/Math.BigInt.Calc.*
%{_mandir}/man3/Math.BigInt.Lib.*
%{_mandir}/man3/Math.BigRat.*
%endif
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Math-BigInt-FastCalc
%{archlib}/Math
%{archlib}/auto/Math
%if !0%{?os2_version}
%{_mandir}/man3/Math::BigInt::FastCalc.*
%else
%{_mandir}/man3/Math.BigInt.FastCalc.*
%endif
%endif

%files Math-Complex
%dir %{privlib}/Math
%{privlib}/Math/Complex.pm
%{privlib}/Math/Trig.pm
%if !0%{?os2_version}
%{_mandir}/man3/Math::Complex.*
%{_mandir}/man3/Math::Trig.*
%else
%{_mandir}/man3/Math.Complex.*
%{_mandir}/man3/Math.Trig.*
%endif

%files Memoize
%{privlib}/Memoize
%{privlib}/Memoize.pm
%if !0%{?os2_version}
%{_mandir}/man3/Memoize::*
%{_mandir}/man3/Memoize.*
%else
%{_mandir}/man3/Memoize.*
%endif

%files meta-notation
%{privlib}/meta_notation.pm

%if %{dual_life} || %{rebuild_from_scratch}
%files MIME-Base64
%{archlib}/auto/MIME
%{archlib}/MIME
%if !0%{?os2_version}
%{_mandir}/man3/MIME::*
%else
%{_mandir}/man3/MIME*
%endif
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Module-CoreList
%dir %{privlib}/Module
%{privlib}/Module/CoreList
%{privlib}/Module/CoreList.pm
%{privlib}/Module/CoreList.pod
%if !0%{?os2_version}
%{_mandir}/man3/Module::CoreList*
%else
%{_mandir}/man3/Module.CoreList*
%endif
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Module-CoreList-tools
%{_bindir}/corelist
%{_mandir}/man1/corelist*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Module-Load
%dir %{privlib}/Module
%{privlib}/Module/Load.pm
%if !0%{?os2_version}
%{_mandir}/man3/Module::Load.*
%else
%{_mandir}/man3/Module.Load.*
%endif
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Module-Load-Conditional
%dir %{privlib}/Module
%{privlib}/Module/Load
%if !0%{?os2_version}
%{_mandir}/man3/Module::Load::Conditional* 
%else
%{_mandir}/man3/Module.Load.Conditional* 
%endif
%endif

%files Module-Loaded
%dir %{privlib}/Module
%{privlib}/Module/Loaded.pm
%if !0%{?os2_version}
%{_mandir}/man3/Module::Loaded*
%else
%{_mandir}/man3/Module.Loaded*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Module-Metadata
%dir %{privlib}/Module
%{privlib}/Module/Metadata.pm
%if !0%{?os2_version}
%{_mandir}/man3/Module::Metadata.3pm*
%else
%{_mandir}/man3/Module.Metadata.3pm*
%endif
%endif

%files mro
%{archlib}/auto/mro
%{archlib}/mro.pm
%{_mandir}/man3/mro.3*

%if %{with gdbm}
%files NDBM_File
%{archlib}/NDBM_File.pm
%{archlib}/auto/NDBM_File
%{_mandir}/man3/NDBM_File.3*
%endif

%files Net
%dir %{privlib}/Net
%{privlib}/Net/hostent.pm
%{privlib}/Net/netent.pm
%{privlib}/Net/protoent.pm
%{privlib}/Net/servent.pm
%if !0%{?os2_version}
%{_mandir}/man3/Net::hostent.3*
%{_mandir}/man3/Net::netent.3*
%{_mandir}/man3/Net::protoent.3*
%{_mandir}/man3/Net::servent.3*
%else
%{_mandir}/man3/Net.hostent.3*
%{_mandir}/man3/Net.netent.3*
%{_mandir}/man3/Net.protoent.3*
%{_mandir}/man3/Net.servent.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Net-Ping
%dir %{privlib}/Net
%{privlib}/Net/Ping.pm
%if !0%{?os2_version}
%{_mandir}/man3/Net::Ping.*
%else
%{_mandir}/man3/Net.Ping.*
%endif
%endif

%files NEXT
%{privlib}/NEXT.pm
%{_mandir}/man3/NEXT.*

%if %{with gdbm}
%files ODBM_File
%{archlib}/ODBM_File.pm
%{archlib}/auto/ODBM_File
%{_mandir}/man3/ODBM_File.3*
%endif

%files open
%{privlib}/open.pm
%{_mandir}/man3/open.3*

%files Opcode
%{archlib}/auto/Opcode
%{archlib}/Opcode.pm
%{archlib}/ops.pm
%{_mandir}/man3/Opcode.3*
%{_mandir}/man3/ops.3*

%files overload
%{privlib}/overload.pm
%{_mandir}/man3/overload.3*

%files overloading
%dir %{privlib}/overload
%{privlib}/overload/numbers.pm
%{privlib}/overloading.pm
%{_mandir}/man3/overloading.3*

%if %{dual_life} || %{rebuild_from_scratch}
%files parent
%{privlib}/parent.pm
%{_mandir}/man3/parent.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Params-Check
%{privlib}/Params/
%if !0%{?os2_version}
%{_mandir}/man3/Params::Check*
%else
%{_mandir}/man3/Params.Check*
%endif
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files PathTools
%{archlib}/Cwd.pm
%dir %{archlib}/File
%{archlib}/File/Spec*
%{archlib}/auto/Cwd
%{_mandir}/man3/Cwd*
%if !0%{?os2_version}
%{_mandir}/man3/File::Spec*
%else
%{_mandir}/man3/File.Spec*
%endif
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Perl-OSType
%dir %{privlib}/Perl
%{privlib}/Perl/OSType.pm
%if !0%{?os2_version}
%{_mandir}/man3/Perl::OSType.3pm*
%else
%{_mandir}/man3/Perl.OSType.3pm*
%endif
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files perlfaq
%{privlib}/perlfaq.pm
%if !0%{?os2_version}
%dir %{privlib}/pod
%{privlib}/pod/perlfaq*
%{privlib}/pod/perlglossary.pod
%else
%dir %{privlib}/Pod
%{privlib}/Pod/perlfaq*
%{privlib}/Pod/perlglossary.pod
%endif
%{_mandir}/man1/perlfaq*
%{_mandir}/man1/perlglossary.*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files PerlIO-via-QuotedPrint
%{privlib}/PerlIO/via
%if !0%{?os2_version}
%{_mandir}/man3/PerlIO::via::QuotedPrint.*
%else
%{_mandir}/man3/PerlIO.via.QuotedPrint.*
%endif
%endif

%files ph
%if !0%{?os2_version}
%{archlib}/asm
%{archlib}/asm-generic
%{archlib}/bits
%endif
%{archlib}/features*.ph
%{archlib}/gnu
%{archlib}/_h2ph_pre.ph
%if !0%{?os2_version}
%{archlib}/linux
%{archlib}/stdc-predef.ph
%endif
%if !0%{?os2_version}
%{archlib}/sys
%{archlib}/syscall.ph
%else
%{archlib}/Sys
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Pod-Checker
%{_bindir}/podchecker
%dir %{privlib}/Pod
%{privlib}/Pod/Checker.pm
%{_mandir}/man1/podchecker.*
%if !0%{?os2_version}
%{_mandir}/man3/Pod::Checker.*
%else
%{_mandir}/man3/Pod.Checker.*
%endif
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Pod-Escapes
%dir %{privlib}/Pod
%{privlib}/Pod/Escapes.pm
%if !0%{?os2_version}
%{_mandir}/man3/Pod::Escapes.*
%else
%{_mandir}/man3/Pod.Escapes.*
%endif
%endif

%files Pod-Functions
%dir %{privlib}/Pod
%{privlib}/Pod/Functions.pm

%files Pod-Html
%license Pod-Html-license-clarification
%{_bindir}/pod2html
%dir %{privlib}/Pod
%{privlib}/Pod/Html
%{privlib}/Pod/Html.pm
%{_mandir}/man1/pod2html.1*
%if !0%{?os2_version}
%{_mandir}/man3/Pod::Html*
%else
%{_mandir}/man3/Pod.Html*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Pod-Perldoc
%{_bindir}/perldoc
%if !0%{?os2_version}
%{privlib}/pod/perldoc.pod
%else
%{privlib}/Pod/perldoc.pod
%endif
%dir %{privlib}/Pod
%{privlib}/Pod/Perldoc
%{privlib}/Pod/Perldoc.pm
%{_mandir}/man1/perldoc.1*
%if !0%{?os2_version}
%{_mandir}/man3/Pod::Perldoc*
%else
%{_mandir}/man3/Pod.Perldoc*
%endif
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Pod-Usage
%{_bindir}/pod2usage
%dir %{privlib}/Pod
%{privlib}/Pod/Usage.pm
%{_mandir}/man1/pod2usage.*
%if !0%{?os2_version}
%{_mandir}/man3/Pod::Usage.*
%else
%{_mandir}/man3/Pod.Usage.*
%endif
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files podlators
%{_bindir}/pod2man
%{_bindir}/pod2text
%if !0%{?os2_version}
%{privlib}/pod/perlpodstyle.pod
%else
%{privlib}/Pod/perlpodstyle.pod
%endif
%dir %{privlib}/Pod
%{privlib}/Pod/Man.pm
%{privlib}/Pod/ParseLink.pm
%{privlib}/Pod/Text
%{privlib}/Pod/Text.pm
%{_mandir}/man1/pod2man.1*
%{_mandir}/man1/pod2text.1*
%{_mandir}/man1/perlpodstyle.1*
%if !0%{?os2_version}
%{_mandir}/man3/Pod::Man*
%{_mandir}/man3/Pod::ParseLink*
%{_mandir}/man3/Pod::Text*
%else
%{_mandir}/man3/Pod.Man*
%{_mandir}/man3/Pod.ParseLink*
%{_mandir}/man3/Pod.Text*
%endif
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Pod-Simple
%dir %{privlib}/Pod
%{privlib}/Pod/Simple
%{privlib}/Pod/Simple.pm
%{privlib}/Pod/Simple.pod
%if !0%{?os2_version}
%{_mandir}/man3/Pod::Simple*
%else
%{_mandir}/man3/Pod.Simple*
%endif
%endif

%files POSIX
%{archlib}/auto/POSIX
%{archlib}/POSIX.*
%{_mandir}/man3/POSIX.*

%files Safe
%{privlib}/Safe.pm
%{_mandir}/man3/Safe.*

%if %{dual_life} || %{rebuild_from_scratch}
%files Scalar-List-Utils
%{archlib}/List
%{archlib}/Scalar
%{archlib}/Sub
%{archlib}/auto/List
%if !0%{?os2_version}
%{_mandir}/man3/List::Util*
%{_mandir}/man3/Scalar::List::Utils*
%{_mandir}/man3/Scalar::Util*
%{_mandir}/man3/Sub::Util*
%else
%{_mandir}/man3/List.Util*
%{_mandir}/man3/Scalar.List.Utils*
%{_mandir}/man3/Scalar.Util*
%{_mandir}/man3/Sub.Util*
%endif
%endif

%files Search-Dict
%{privlib}/Search
%if !0%{?os2_version}
%{_mandir}/man3/Search::*
%else
%{_mandir}/man3/Search.*
%endif

%files SelectSaver
%{privlib}/SelectSaver.pm
%{_mandir}/man3/SelectSaver.*

%files SelfLoader
%{privlib}/SelfLoader.pm
%{_mandir}/man3/SelfLoader.*

%files sigtrap
%{privlib}/sigtrap.pm
%{_mandir}/man3/sigtrap.*

%if %{dual_life} || %{rebuild_from_scratch}
%files Socket
%dir %{archlib}/auto/Socket
%if !0%{?os2_version}
%{archlib}/auto/Socket/Socket.*
%else
%{archlib}/auto/Socket/Socket*.dll
%endif
%{archlib}/Socket.pm
%{_mandir}/man3/Socket.3*
%endif

%files sort
%{privlib}/sort.pm
%{_mandir}/man3/sort.*

%if %{dual_life} || %{rebuild_from_scratch}
%files Storable
%{archlib}/Storable.pm
%{archlib}/auto/Storable
%if 0%{?os2_version}
%exclude %{archlib}/auto/Storable/Storab*.dbg
%endif
%{_mandir}/man3/Storable.*
%endif

%files subs
%{privlib}/subs.pm
%{_mandir}/man3/subs.*

%files Symbol
%{privlib}/Symbol.pm
%{_mandir}/man3/Symbol.*

%files Sys-Hostname
%dir %{archlib}/auto/Sys
%{archlib}/auto/Sys/Hostname
%if 0%{?os2_version}
%exclude %{archlib}/auto/Sys/Hostname/Hostna*.dbg
%endif
%dir %{archlib}/Sys
%{archlib}/Sys/Hostname.pm
%if !0%{?os2_version}
%{_mandir}/man3/Sys::Hostname.*
%else
%{_mandir}/man3/Sys.Hostname.*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Sys-Syslog
%dir %{archlib}/Sys
%{archlib}/Sys/Syslog.pm
%dir %{archlib}/auto/Sys
%{archlib}/auto/Sys/Syslog
%if 0%{?os2_version}
%exclude %{archlib}/auto/Sys/Syslog/Syslog*.dbg
%endif
%if !0%{?os2_version}
%{_mandir}/man3/Sys::Syslog.*
%else
%{_mandir}/man3/Sys.Syslog.*
%endif
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Term-ANSIColor
%dir %{privlib}/Term
%{privlib}/Term/ANSIColor.pm
%if !0%{?os2_version}
%{_mandir}/man3/Term::ANSIColor*
%else
%{_mandir}/man3/Term.ANSIColor*
%endif
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Term-Cap
%dir %{privlib}/Term
%{privlib}/Term/Cap.pm
%if !0%{?os2_version}
%{_mandir}/man3/Term::Cap.*
%else
%{_mandir}/man3/Term.Cap.*
%endif
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Term-Table
%dir %{privlib}/Term
%{privlib}/Term/Table*
%if !0%{?os2_version}
%{_mandir}/man3/Term::Table.*
%{_mandir}/man3/Term::Table::*
%else
%{_mandir}/man3/Term.Table.*
%endif
%endif

%files Term-Complete
%dir %{privlib}/Term
%{privlib}/Term/Complete.pm
%if !0%{?os2_version}
%{_mandir}/man3/Term::Complete.*
%else
%{_mandir}/man3/Term.Complete.*
%endif

%files Term-ReadLine
%dir %{privlib}/Term
%{privlib}/Term/ReadLine.pm
%if !0%{?os2_version}
%{_mandir}/man3/Term::ReadLine.*
%else
%{_mandir}/man3/Term.ReadLine.*
%endif

%files Test
%{privlib}/Test.pm
%{_mandir}/man3/Test.*

%if %{dual_life} || %{rebuild_from_scratch}
%files Test-Harness
%{_bindir}/prove
%dir %{privlib}/App
%{privlib}/App/Prove*
%{privlib}/TAP*
%dir %{privlib}/Test
%{privlib}/Test/Harness*
%{_mandir}/man1/prove.1*
%if !0%{?os2_version}
%{_mandir}/man3/App::Prove*
%{_mandir}/man3/TAP*
%{_mandir}/man3/Test::Harness*
%else
%{_mandir}/man3/App.Prove*
%{_mandir}/man3/TAP*
%{_mandir}/man3/Test.Harness*
%endif
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Test-Simple
%{privlib}/ok*
%dir %{privlib}/Test
%{privlib}/Test/More*
%{privlib}/Test/Builder*
%{privlib}/Test/Tester*
%{privlib}/Test/Simple*
%{privlib}/Test/Tutorial*
%{privlib}/Test/use
%dir %{privlib}/Test2
%{privlib}/Test2.pm
%{privlib}/Test2/API*
%{privlib}/Test2/Env*
%{privlib}/Test2/Event.pm
%{privlib}/Test2/Event/*
%{privlib}/Test2/EventFacet*
%{privlib}/Test2/Formatter*
%{privlib}/Test2/Hub*
%{privlib}/Test2/IPC*
%dir %{privlib}/Test2/Tools
%{privlib}/Test2/Tools/Tiny.pm
%{privlib}/Test2/Transition.pod
%{privlib}/Test2/Util.pm
%{privlib}/Test2/Util/ExternalMeta.pm
%{privlib}/Test2/Util/Facets2Legacy.pm
%{privlib}/Test2/Util/HashBase.pm
%{privlib}/Test2/Util/Sig.pm
%{privlib}/Test2/Util/Trace.pm
%{_mandir}/man3/ok*
%if !0%{?os2_version}
%{_mandir}/man3/Test::More*
%{_mandir}/man3/Test::Builder*
%{_mandir}/man3/Test::Tester*
%{_mandir}/man3/Test::Simple*
%{_mandir}/man3/Test::Tutorial*
%{_mandir}/man3/Test::use::*
%{_mandir}/man3/Test2.*
%{_mandir}/man3/Test2::API*
%{_mandir}/man3/Test2::Env.*
%{_mandir}/man3/Test2::Event.*
%{_mandir}/man3/Test2::Event::*
%{_mandir}/man3/Test2::EventFacet*
%{_mandir}/man3/Test2::Formatter*
%{_mandir}/man3/Test2::Hub*
%{_mandir}/man3/Test2::IPC*
%{_mandir}/man3/Test2::Tools::Tiny*
%{_mandir}/man3/Test2::Transition*
%{_mandir}/man3/Test2::Util.*
%{_mandir}/man3/Test2::Util::ExternalMeta.*
%{_mandir}/man3/Test2::Util::Facets2Legacy.*
%{_mandir}/man3/Test2::Util::HashBase.*
%{_mandir}/man3/Test2::Util::Sig.*
%{_mandir}/man3/Test2::Util::Trace.*
%else
%{_mandir}/man3/Test.More*
%{_mandir}/man3/Test.Builder*
%{_mandir}/man3/Test.Tester*
%{_mandir}/man3/Test.Simple*
%{_mandir}/man3/Test.Tutorial*
%{_mandir}/man3/Test.use.*
%{_mandir}/man3/Test2.3*
%{_mandir}/man3/Test2.API*
%{_mandir}/man3/Test2.Env.*
%{_mandir}/man3/Test2.Event.*
%{_mandir}/man3/Test2.EventFacet*
%{_mandir}/man3/Test2.Formatter*
%{_mandir}/man3/Test2.Hub*
%{_mandir}/man3/Test2.IPC*
%{_mandir}/man3/Test2.Tools.Tiny*
%{_mandir}/man3/Test2.Transition*
%{_mandir}/man3/Test2.Util.3*
%{_mandir}/man3/Test2.Util.ExternalMeta.*
%{_mandir}/man3/Test2.Util.Facets2Legacy.*
%{_mandir}/man3/Test2.Util.HashBase.*
%{_mandir}/man3/Test2.Util.Sig.*
%{_mandir}/man3/Test2.Util.Trace.*
%endif
%{privlib}/Test2/AsyncSubtest*
%{privlib}/Test2/Bundle*
%{privlib}/Test2/Compare*
%{privlib}/Test2/Manual*
%{privlib}/Test2/Mock.pm
%{privlib}/Test2/Plugin*
%{privlib}/Test2/Require*
%{privlib}/Test2/Suite.pm
%{privlib}/Test2/Todo.pm
%{privlib}/Test2/Tools.pm
%{privlib}/Test2/Tools/AsyncSubtest.pm
%{privlib}/Test2/Tools/Basic.pm
%{privlib}/Test2/Tools/Class.pm
%{privlib}/Test2/Tools/ClassicCompare.pm
%{privlib}/Test2/Tools/Compare.pm
%{privlib}/Test2/Tools/Defer.pm
%{privlib}/Test2/Tools/Encoding.pm
%{privlib}/Test2/Tools/Event.pm
%{privlib}/Test2/Tools/Exception.pm
%{privlib}/Test2/Tools/Exports.pm
%{privlib}/Test2/Tools/GenTemp.pm
%{privlib}/Test2/Tools/Grab.pm
%{privlib}/Test2/Tools/Mock.pm
%{privlib}/Test2/Tools/Ref.pm
%{privlib}/Test2/Tools/Refcount.pm
%{privlib}/Test2/Tools/Spec.pm
%{privlib}/Test2/Tools/Subtest.pm
%{privlib}/Test2/Tools/Target.pm
%{privlib}/Test2/Tools/Tester.pm
%{privlib}/Test2/Tools/Warnings.pm
%dir %{privlib}/Test2/Util
%{privlib}/Test2/Util/Grabber.pm
%{privlib}/Test2/Util/Guard.pm
%{privlib}/Test2/Util/Importer.pm
%{privlib}/Test2/Util/Ref.pm
%{privlib}/Test2/Util/Stash.pm
%{privlib}/Test2/Util/Sub.pm
%{privlib}/Test2/Util/Table.pm
%dir %{privlib}/Test2/Util/Table
%{privlib}/Test2/Util/Table/Cell.pm
%{privlib}/Test2/Util/Table/LineBreak.pm
%{privlib}/Test2/Util/Term.pm
%{privlib}/Test2/Util/Times.pm
%{privlib}/Test2/V0.pm
%{privlib}/Test2/Workflow*
%if !0%{?os2_version}
%{_mandir}/man3/Test2::AsyncSubtest*
%{_mandir}/man3/Test2::Bundle*
%{_mandir}/man3/Test2::Compare*
%{_mandir}/man3/Test2::Manual*
%{_mandir}/man3/Test2::Mock.*
%{_mandir}/man3/Test2::Plugin*
%{_mandir}/man3/Test2::Require*
%{_mandir}/man3/Test2::Suite.*
%{_mandir}/man3/Test2::Todo.*
%{_mandir}/man3/Test2::Tools.*
%{_mandir}/man3/Test2::Tools::AsyncSubtest.*
%{_mandir}/man3/Test2::Tools::Basic.*
%{_mandir}/man3/Test2::Tools::Class.*
%{_mandir}/man3/Test2::Tools::ClassicCompare.*
%{_mandir}/man3/Test2::Tools::Compare.*
%{_mandir}/man3/Test2::Tools::Defer.*
%{_mandir}/man3/Test2::Tools::Encoding.*
%{_mandir}/man3/Test2::Tools::Event.*
%{_mandir}/man3/Test2::Tools::Exception.*
%{_mandir}/man3/Test2::Tools::Exports.*
%{_mandir}/man3/Test2::Tools::GenTemp.*
%{_mandir}/man3/Test2::Tools::Grab.*
%{_mandir}/man3/Test2::Tools::Mock.*
%{_mandir}/man3/Test2::Tools::Ref.*
%{_mandir}/man3/Test2::Tools::Refcount.*
%{_mandir}/man3/Test2::Tools::Spec.*
%{_mandir}/man3/Test2::Tools::Subtest.*
%{_mandir}/man3/Test2::Tools::Target.*
%{_mandir}/man3/Test2::Tools::Tester.*
%{_mandir}/man3/Test2::Tools::Warnings.*
%{_mandir}/man3/Test2::Util::Grabber.*
%{_mandir}/man3/Test2::Util::Guard.*
%{_mandir}/man3/Test2::Util::Importer.*
%{_mandir}/man3/Test2::Util::Ref.*
%{_mandir}/man3/Test2::Util::Stash.*
%{_mandir}/man3/Test2::Util::Sub.*
%{_mandir}/man3/Test2::Util::Table*
%{_mandir}/man3/Test2::Util::Times.*
%{_mandir}/man3/Test2::V0.*
%{_mandir}/man3/Test2::Workflow*
%else
%{_mandir}/man3/Test2.AsyncSubtest*
%{_mandir}/man3/Test2.Bundle*
%{_mandir}/man3/Test2.Compare*
%{_mandir}/man3/Test2.Manual*
%{_mandir}/man3/Test2.Mock.*
%{_mandir}/man3/Test2.Plugin*
%{_mandir}/man3/Test2.Require*
%{_mandir}/man3/Test2.Suite.*
%{_mandir}/man3/Test2.Todo.*
%{_mandir}/man3/Test2.Tools.3*
%{_mandir}/man3/Test2.Tools.AsyncSubtest.*
%{_mandir}/man3/Test2.Tools.Basic.*
%{_mandir}/man3/Test2.Tools.Class.*
%{_mandir}/man3/Test2.Tools.ClassicCompare.*
%{_mandir}/man3/Test2.Tools.Compare.*
%{_mandir}/man3/Test2.Tools.Defer.*
%{_mandir}/man3/Test2.Tools.Encoding.*
%{_mandir}/man3/Test2.Tools.Event.*
%{_mandir}/man3/Test2.Tools.Exception.*
%{_mandir}/man3/Test2.Tools.Exports.*
%{_mandir}/man3/Test2.Tools.GenTemp.*
%{_mandir}/man3/Test2.Tools.Grab.*
%{_mandir}/man3/Test2.Tools.Mock.*
%{_mandir}/man3/Test2.Tools.Ref.*
%{_mandir}/man3/Test2.Tools.Refcount.*
%{_mandir}/man3/Test2.Tools.Spec.*
%{_mandir}/man3/Test2.Tools.Subtest.*
%{_mandir}/man3/Test2.Tools.Target.*
%{_mandir}/man3/Test2.Tools.Tester.*
%{_mandir}/man3/Test2.Tools.Warnings.*
%{_mandir}/man3/Test2.Util.Grabber.*
%{_mandir}/man3/Test2.Util.Guard.*
%{_mandir}/man3/Test2.Util.Importer.*
%{_mandir}/man3/Test2.Util.Ref.*
%{_mandir}/man3/Test2.Util.Stash.*
%{_mandir}/man3/Test2.Util.Sub.*
%{_mandir}/man3/Test2.Util.Table*
%{_mandir}/man3/Test2.Util.Times.*
%{_mandir}/man3/Test2.V0.*
%{_mandir}/man3/Test2.Workflow*
%endif
%endif

%files Text-Abbrev
%dir %{privlib}/Text
%{privlib}/Text/Abbrev.pm
%if !0%{?os2_version}
%{_mandir}/man3/Text::Abbrev.*
%else
%{_mandir}/man3/Text.Abbrev.*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Text-Balanced
%dir %{privlib}/Text
%{privlib}/Text/Balanced.pm
%if !0%{?os2_version}
%{_mandir}/man3/Text::Balanced.*
%else
%{_mandir}/man3/Text.Balanced.*
%endif
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Text-ParseWords
%dir %{privlib}/Text
%{privlib}/Text/ParseWords.pm
%if !0%{?os2_version}
%{_mandir}/man3/Text::ParseWords.*
%else
%{_mandir}/man3/Text.ParseWords.*
%endif
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Text-Tabs+Wrap
%dir %{privlib}/Text
%{privlib}/Text/Tabs.pm
%{privlib}/Text/Wrap.pm
%if !0%{?os2_version}
%{_mandir}/man3/Text::Tabs.*
%{_mandir}/man3/Text::Wrap.*
%else
%{_mandir}/man3/Text.Tabs.*
%{_mandir}/man3/Text.Wrap.*
%endif
%endif

%files Thread
%{privlib}/Thread.pm
%{_mandir}/man3/Thread.*

%if %{dual_life} || %{rebuild_from_scratch}
%files Thread-Queue
%dir %{privlib}/Thread
%{privlib}/Thread/Queue.pm
%if !0%{?os2_version}
%{_mandir}/man3/Thread::Queue.*
%else
%{_mandir}/man3/Thread.Queue.*
%endif
%endif

%files Thread-Semaphore
%dir %{privlib}/Thread
%{privlib}/Thread/Semaphore.pm
%if !0%{?os2_version}
%{_mandir}/man3/Thread::Semaphore.*
%else
%{_mandir}/man3/Thread.Semaphore.*
%endif

%files Tie
%dir %{privlib}/Tie
%{privlib}/Tie/Array.pm
%{privlib}/Tie/Handle.pm
%{privlib}/Tie/Scalar.pm
%{privlib}/Tie/StdHandle.pm
%{privlib}/Tie/SubstrHash.pm
%if !0%{?os2_version}
%{_mandir}/man3/Tie::Array.*
%{_mandir}/man3/Tie::Handle.*
%{_mandir}/man3/Tie::Scalar.*
%{_mandir}/man3/Tie::StdHandle.*
%{_mandir}/man3/Tie::SubstrHash.*
%else
%{_mandir}/man3/Tie.Array.*
%{_mandir}/man3/Tie.Handle.*
%{_mandir}/man3/Tie.Scalar.*
%{_mandir}/man3/Tie.StdHandle.*
%{_mandir}/man3/Tie.SubstrHash.*
%endif

%files Tie-File
%dir %{privlib}/Tie
%{privlib}/Tie/File.pm
%if !0%{?os2_version}
%{_mandir}/man3/Tie::File.*
%else
%{_mandir}/man3/Tie.File.*
%endif

%files Tie-Memoize
%dir %{privlib}/Tie
%{privlib}/Tie/Memoize.pm
%if !0%{?os2_version}
%{_mandir}/man3/Tie::Memoize.*
%else
%{_mandir}/man3/Tie.Memoize.*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Tie-RefHash
%dir %{privlib}/Tie
%{privlib}/Tie/RefHash.pm
%if !0%{?os2_version}
%{_mandir}/man3/Tie::RefHash.*
%else
%{_mandir}/man3/Tie.RefHash.*
%endif
%endif

%files Time
%dir %{privlib}/Time
%{privlib}/Time/gmtime.pm
%{privlib}/Time/localtime.pm
%{privlib}/Time/tm.pm
%if !0%{?os2_version}
%{_mandir}/man3/Time::gmtime.*
%{_mandir}/man3/Time::localtime.*
%{_mandir}/man3/Time::tm.*
%else
%{_mandir}/man3/Time.gmtime.*
%{_mandir}/man3/Time.localtime.*
%{_mandir}/man3/Time.tm.*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Time-HiRes
%dir %{archlib}/Time
%{archlib}/Time/HiRes.pm
%dir %{archlib}/auto/Time
%{archlib}/auto/Time/HiRes
%if !0%{?os2_version}
%{_mandir}/man3/Time::HiRes.*
%else
%{_mandir}/man3/Time.HiRes.*
%endif
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Time-Local
%dir %{privlib}/Time
%{privlib}/Time/Local.pm
%if !0%{?os2_version}
%{_mandir}/man3/Time::Local.*
%else
%{_mandir}/man3/Time.Local.*
%endif
%endif

%files Time-Piece
%dir %{archlib}/Time
%{archlib}/Time/Piece.pm 
%{archlib}/Time/Seconds.pm
%dir %{archlib}/auto/Time
%{archlib}/auto/Time/Piece
%if !0%{?os2_version}
%{_mandir}/man3/Time::Piece.3*
%{_mandir}/man3/Time::Seconds.3*
%else
%{_mandir}/man3/Time.Piece.3*
%{_mandir}/man3/Time.Seconds.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files threads
%dir %{archlib}/auto/threads
%if !0%{?os2_version}
%{archlib}/auto/threads/threads*
%else
%{archlib}/auto/threads/thread*.dll
%endif
%{archlib}/threads.pm
%{_mandir}/man3/threads.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files threads-shared
%dir %{archlib}/auto/threads
%{archlib}/auto/threads/shared*
%if 0%{?os2_version}
%{archlib}/auto/threads/shared/shared*.dbg
%endif
%dir %{archlib}/threads
%{archlib}/threads/shared*
%if !0%{?os2_version}
%{_mandir}/man3/threads::shared*
%else
%{_mandir}/man3/threads.shared*
%endif
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Unicode-Collate
%dir %{archlib}/auto/Unicode
%{archlib}/auto/Unicode/Collate
%if 0%{?os2_version}
%{archlib}/auto/Unicode/Collate/Collat*.dbg
%endif
%dir %{archlib}/Unicode
%{archlib}/Unicode/Collate
%{archlib}/Unicode/Collate.pm
%dir %{privlib}/Unicode
%{privlib}/Unicode/Collate
%if !0%{?os2_version}
%{_mandir}/man3/Unicode::Collate.*
%{_mandir}/man3/Unicode::Collate::*
%else
%{_mandir}/man3/Unicode.Collate.*
%endif
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Unicode-Normalize
%dir %{archlib}/auto/Unicode
%{archlib}/auto/Unicode/Normalize
%if 0%{?os2_version}
%{archlib}/auto/Unicode/Normalize/Normal*.dbg
%endif
%dir %{archlib}/Unicode
%{archlib}/Unicode/Normalize.pm
%if !0%{?os2_version}
%{_mandir}/man3/Unicode::Normalize.*
%else
%{_mandir}/man3/Unicode.Normalize.*
%endif
%endif

%files Unicode-UCD
%dir %{privlib}/Unicode
%{privlib}/Unicode/UCD.pm
%if !0%{?os2_version}
%{_mandir}/man3/Unicode::UCD.*
%else
%{_mandir}/man3/Unicode.UCD.*
%endif

%files User-pwent
%{privlib}/User
%if !0%{?os2_version}
%{_mandir}/man3/User::*
%else
%{_mandir}/man3/User.*
%endif

%files vars
%{privlib}/vars.pm
%{_mandir}/man3/vars.*

%if %{dual_life} || %{rebuild_from_scratch}
%files version
%{privlib}/version.pm
%{privlib}/version.pod
%{privlib}/version/
%{_mandir}/man3/version.3*
%if !0%{?os2_version}
%{_mandir}/man3/version::Internals.3*
%else
%{_mandir}/man3/version.Internals.3*
%endif
%endif

%files vmsish
%{privlib}/vmsish.pm
%{_mandir}/man3/vmsish.*

%changelog
* Fri Apr 24 2026 Silvan Scherrer <silvan.scherrer@aroa.ch> 5.42.2-14
- never start with rel 1 on a new version, because of dual-lived modules

* Mon Apr 20 2026 Silvan Scherrer <silvan.scherrer@aroa.ch> 5.42.2-1
- update to version 5.42.2
- resync with fedora spec

* Tue Mar 03 2026 Silvan Scherrer <silvan.scherrer@aroa.ch> 5.16.1-12
- update macros.perl

* Wed Mar 26 2025 Silvan Scherrer <silvan.scherrer@aroa.ch> 5.16.1-11
- use the right tag to build

* Mon Feb 17 2025 Silvan Scherrer <silvan.scherrer@aroa.ch> 5.16.1-10
- fix removing temp directories

* Wed Jan 13 2021 Silvan Scherrer <silvan.scherrer@aroa.ch> 5.16.1-9
- add libcx to the exe as well, so we get a nice trp on failures

* Fri Dec 11 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> 5.16.1-8
- fix a gcc 9 compiler regression while creating Errno.pm

* Wed Oct 14 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> 5.16.1-7
- enable libcx

* Thu Aug 27 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> 5.16.1-6
- preserve boot_DynaLoader export

* Wed Oct 24 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> 5.16.1-5
- readd zip functionality, which was lost in 5.16.1-4
- remove duplicate files
- fix for ticket #67
- fix for ticket #160

* Thu Apr 6 2017 Dmitriy Kuminov <coding@dmik.org> 5.16.1-4
- Merge Fedora perl.spec changes for 5.16.1 to generate proper perl(XXX)
  requires and provides and to bring more perl-XXX sub-packages.
- Bump epoch to 4 after Fedora to make automatic requires happy.
- Remove urpo dependency.
- Generate man files.
- Make build system recognize all library files kLIBC emxomfld recognizes.
- Remove .dbg files from normal RPMs.
- Use scm_source macros.
- Change vendor to bww bitwise works GmbH.

* Mon Mar 27 2017 yd <yd@os2power.com> 5.16.1-3
- package rebuild due to new perl() rpm macros.

* Fri Mar 11 2016 yd <yd@os2power.com> 5.16.1-2
- package rebuild due to broken hard links, ticket#172.

* Wed Aug 13 2014 yd
- first public release build.
- added debug package with symbolic info for exceptq.
- r745, Fix endless loop when calling shell script with invalid #! magic.
- r744, Support symlinked shells in scripts in system() and similar calls.
- r743, Fix building of minitperl on OS/2.
