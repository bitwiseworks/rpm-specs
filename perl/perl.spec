# Based on http://pkgs.fedoraproject.org/cgit/rpms/perl.git/tree/perl.spec?id=2b64acd23e71d8c12300bf0f61a40bf18ae25c0a

%global perl_version    5.16.1
%global perl_epoch      4
%global perl_arch_stem -thread-multi
%global perl_archname %{_arch}-%{_os}%{perl_arch_stem}

%global parallel_tests 1

# This overrides filters from build root (/etc/rpm/macros.perl)
# intentionally (unversioned perl(DB) is removed and versioned one is kept)
%global __provides_exclude_from .*/auto/.*\\.dll$|.*/%{perl_archlib}/.*\\.dll$|%{_docdir}
%global __requires_exclude_from %{_docdir}
%global __provides_exclude perl\\((VMS|Win32|BSD::|DB\\)$)
# unicore::Name - it's needed by perl, maybe problem of rpm
# FCGI is external dependency after install of perl-CGI, remove it during RC releases
%global __requires_exclude perl\\((VMS|BSD::|Win32|Tk|Mac::|Your::Module::Here|unicore::Name|FCGI)

# same as we provide in /etc/rpm/macros.perl
%global perl5_testdir   %{_libexecdir}/perl5-tests

# We can bootstrap without gdbm
%bcond_with gdbm
# We can skip %%check phase
%bcond_with test

Name:           perl
Version:        %{perl_version}
# release number must be even higher, because dual-lived modules will be broken otherwise
Release:        5%{?dist}
Epoch:          %{perl_epoch}
Summary:        Practical Extraction and Report Language
Group:          Development/Languages
# Modules Tie::File and Getopt::Long are licenced under "GPLv2+ or Artistic,"
# we have to reflect that in the sub-package containing them.
# under UCD are unicode tables
# Public domain: ext/SDBM_File/sdbm/*, ext/Compress-Raw-Bzip2/bzip2-src/dlltest.c
# MIT: ext/MIME-Base64/Base64.xs
# Copyright Only: for example ext/Text-Soundex/Soundex.xs
License:        (GPL+ or Artistic) and (GPLv2+ or Artistic) and Copyright Only and MIT and Public Domain and UCD
Url:            http://www.perl.org/
Vendor:         bww bitwise works GmbH

%scm_source     svn http://svn.netlabs.org/repos/ports/perl/trunk 2305
Source3:        macros.perl

# Update some of the bundled modules
# see http://fedoraproject.org/wiki/Perl/perl.spec for instructions

BuildRequires:  db4-devel, zlib-devel, bzip2-devel
#BuildRequires:  groff, tcsh
%if %{with gdbm}
BuildRequires: gdbm-devel
%endif

# For tests
%if %{with gdbm}
BuildRequires:  procps, rsyslog
%endif

# The long line of Perl provides.

# Compat provides
Provides: perl(:MODULE_COMPAT_5.16.1)
Provides: perl(:MODULE_COMPAT_5.16.0)

# Threading provides
Provides: perl(:WITH_ITHREADS)
Provides: perl(:WITH_THREADS)
# Largefile provides
Provides: perl(:WITH_LARGEFILES)
# PerlIO provides
Provides: perl(:WITH_PERLIO)
# File provides
Provides: perl(abbrev.pl)
Provides: perl(assert.pl)
Provides: perl(bigfloat.pl)
Provides: perl(bigint.pl)
Provides: perl(bigrat.pl)
Provides: perl(bytes_heavy.pl)
Provides: perl(cacheout.pl)
Provides: perl(complete.pl)
Provides: perl(ctime.pl)
Provides: perl(dotsh.pl)
Provides: perl(dumpvar.pl)
Provides: perl(exceptions.pl)
Provides: perl(fastcwd.pl)
Provides: perl(find.pl)
Provides: perl(finddepth.pl)
Provides: perl(flush.pl)
Provides: perl(ftp.pl)
Provides: perl(getcwd.pl)
Provides: perl(getopt.pl)
Provides: perl(getopts.pl)
Provides: perl(hostname.pl)
Provides: perl(importenv.pl)
Provides: perl(look.pl)
Provides: perl(newgetopt.pl)
Provides: perl(open2.pl)
Provides: perl(open3.pl)
Provides: perl(perl5db.pl)
Provides: perl(pwd.pl)
Provides: perl(shellwords.pl)
Provides: perl(stat.pl)
%if 0
Provides: perl(syslog.pl)
%endif
Provides: perl(tainted.pl)
Provides: perl(termcap.pl)
Provides: perl(timelocal.pl)
Provides: perl(utf8_heavy.pl)
Provides: perl(validate.pl)

# Long history in 3rd-party repositories:
Provides: perl-File-Temp = 0.22
Obsoletes: perl-File-Temp < 0.20

# suidperl isn't created by upstream since 5.12.0
Obsoletes: perl-suidperl <= 4:5.12.2

Requires: perl-libs = %{perl_epoch}:%{perl_version}-%{release}

# We need this to break the dependency loop, and ensure that perl-libs
# gets installed before perl.
Requires(post): perl-libs
# Same as perl-libs. We need macros in basic buildroot, where Perl is only
# because of git.
Requires(post): perl-macros


%description
Perl is a high-level programming language with roots in C, sed, awk and shell
scripting.  Perl is good at handling processes and files, and is especially
good at handling text.  Perl's hallmarks are practicality and efficiency.
While it is used to do a lot of different things, Perl's most common
applications are system administration utilities and web programming.  A large
proportion of the CGI scripts on the web are written in Perl.  You need the
perl package installed on your system so that your system can handle Perl
scripts.

Install this package if you want to program in Perl or enable your system to
handle Perl scripts.

%package libs
Summary:        The libraries for the perl runtime
Group:          Development/Languages
License:        GPL+ or Artistic
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}

%description libs
The libraries for the perl runtime


%package devel
Summary:        Header #files for use in perl development
Group:          Development/Languages
License:        GPL+ or Artistic
Requires:       perl(ExtUtils::ParseXS)
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}

%description devel
This package contains header files and development modules.
Most perl packages will need to install perl-devel to build.


%package macros
Summary:        Macros for rpmbuild
Group:          Development/Languages
License:        GPL+ or Artistic
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}

%description macros
Macros for rpmbuild are needed during build of srpm in koji. This
sub-package must be installed into buildroot, so it will be needed
by perl. Perl is needed because of git.


%package tests
Summary:        The Perl test suite
Group:          Development/Languages
License:        GPL+ or Artistic
# right?
AutoReqProv:    0
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
# FIXME - note this will need to change when doing the core/minimal swizzle
Requires:       perl-core

%description tests
This package contains the test suite included with Perl %{perl_version}.

Install this if you want to test your Perl installation (binary and core
modules).


%package Archive-Extract
Summary:        Generic archive extracting mechanism
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        0.58
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
BuildArch:      noarch

%description Archive-Extract
Archive::Extract is a generic archive extraction mechanism.


%package Archive-Tar
Summary:        A module for Perl manipulation of .tar files
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        1.82
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
Requires:       perl(Compress::Zlib), perl(IO::Zlib)
BuildArch:      noarch

%description Archive-Tar
Archive::Tar provides an object oriented mechanism for handling tar files.  It
provides class methods for quick and easy files handling while also allowing
for the creation of tar file objects for custom manipulation.  If you have the
IO::Zlib module installed, Archive::Tar will also support compressed or
gzipped tar files.


%package Carp
Summary:        Alternative warn and die for modules
Epoch:          0
Version:        1.26
License:        GPL+ or Artistic
Group:          Development/Libraries
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
Provides:       perl(Carp::Heavy) = %{version}
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


%package CGI
Summary:        Handle Common Gateway Interface requests and responses
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        3.59
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
Provides:       perl(CGI) = %{version}
BuildArch:      noarch

# Do not export unversioned module
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(CGI\\)\\s*$
# Do not export private modules
%global __provides_exclude %{__provides_exclude}|^perl\\(Fh\\)\\s*$
%global __provides_exclude %{__provides_exclude}|^perl\\(MultipartBuffer\\)\\s*$
%global __provides_exclude %{__provides_exclude}|^perl\\(utf8\\)\\s*$

%description CGI
CGI.pm is a stable, complete and mature solution for processing and preparing
HTTP requests and responses. Major features including processing form
submissions, file uploads, reading and writing cookies, query string generation
and manipulation, and processing and preparing HTTP headers. Some HTML
generation utilities are included as well.

CGI.pm performs very well in in a vanilla CGI.pm environment and also comes
with built-in support for mod_perl and mod_perl2 as well as FastCGI.


%package Compress-Raw-Bzip2
Summary:        Low-Level Interface to bzip2 compression library
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        2.048
Requires:       perl(Exporter), perl(File::Temp)

%description Compress-Raw-Bzip2
This module provides a Perl interface to the bzip2 compression library.
It is used by IO::Compress::Bzip2.


%package Compress-Raw-Zlib
Summary:        Low-Level Interface to the zlib compression library
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        2.048
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}

%description Compress-Raw-Zlib
This module provides a Perl interface to the zlib compression library.
It is used by IO::Compress::Zlib.


%package CPAN
Summary:        Query, download and build perl modules from CPAN sites
Group:          Development/Languages
License:        GPL+ or Artistic
Epoch:          0
Version:        1.9800
# CPAN encourages Digest::SHA strongly because of integrity checks
Requires:       perl(Digest::SHA)
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
Provides:       cpan = %{version}
BuildArch:      noarch

%description CPAN
Query, download and build perl modules from CPAN sites.

%package CPAN-Meta
Summary:        Distribution metadata for a CPAN dist
Epoch:          0
Version:        2.120630
License:        GPL+ or Artistic
Group:          Development/Libraries
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
BuildArch:      noarch

%description CPAN-Meta
Software distributions released to the CPAN include a META.json or, for
older distributions, META.yml, which describes the distribution, its
contents, and the requirements for building and installing the
distribution. The data structure stored in the META.json file is described
in CPAN::Meta::Spec.


%package CPAN-Meta-YAML
Version:        0.007
Epoch:          0
Summary:        Read and write a subset of YAML for CPAN Meta files
License:        GPL+ or Artistic
Group:          Development/Libraries
BuildArch:      noarch
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}

%description CPAN-Meta-YAML
This module implements a subset of the YAML specification for use in reading
and writing CPAN metadata files like META.yml and MYMETA.yml. It should not be
used for any other general YAML parsing or generation task.


%package CPANPLUS
Summary:        API & CLI access to the CPAN mirrors
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
# real version 0.9121
Version:        0.91.21
# CPANPLUS encourages Digest::SHA strongly because of integrity checks
Requires:       perl(Digest::SHA)
Requires:       perl(Module::Pluggable) >= 2.4
Requires:       perl(Module::CoreList)
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
Provides:       perl-CPANPLUS-Dist-Build = 0.54
Obsoletes:      perl-CPANPLUS-Dist-Build <= 0.05
BuildArch:      noarch

%description CPANPLUS
The CPANPLUS library is an API to the CPAN mirrors and a collection of
interactive shells, commandline programs, etc, that use this API.


%package Data-Dumper
Summary:        Stringify perl data structures, suitable for printing and eval
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        2.135.06
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
Requires:       perl(Scalar::Util)
Requires:       perl(XSLoader)

%description Data-Dumper
Given a list of scalars or reference variables, writes out their contents
in perl syntax. The references can also be objects. The content of each
variable is output in a single Perl statement. Handles self-referential
structures correctly.


%package Digest
Summary:        Modules that calculate message digests
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          0
Version:        1.17
BuildArch:      noarch
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
Requires:       perl(MIME::Base64)

%description Digest
The Digest:: modules calculate digests, also called "fingerprints" or
"hashes", of some data, called a message. The digest is (usually)
some small/fixed size string. The actual size of the digest depend of
the algorithm used. The message is simply a sequence of arbitrary
bytes or bits.


%package Digest-MD5
Summary:        Perl interface to the MD5 Algorithm
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          0
Version:        2.51
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
# Recommended
Requires:       perl(Digest::base) >= 1.00

%description Digest-MD5
The Digest::MD5 module allows you to use the RSA Data Security Inc. MD5
Message Digest algorithm from within Perl programs. The algorithm takes as
input a message of arbitrary length and produces as output a 128-bit
"fingerprint" or "message digest" of the input.


%package Digest-SHA
Summary:        Perl extension for SHA-1/224/256/384/512
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        5.71
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
# Recommended
Requires:       perl(Digest::base)
Requires:       perl(MIME::Base64)

%description Digest-SHA
Digest::SHA is a complete implementation of the NIST Secure Hash
Standard.  It gives Perl programmers a convenient way to calculate
SHA-1, SHA-224, SHA-256, SHA-384, and SHA-512 message digests.  The
module can handle all types of input, including partial-byte data.


%package ExtUtils-CBuilder
Summary:        Compile and link C code for Perl modules
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
# real version 0.280206 https://fedoraproject.org/wiki/Perl/Tips#Dot_approach
Version:        0.28.2.6
Requires:       perl-devel
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
BuildArch:      noarch

%description ExtUtils-CBuilder
This module can build the C portions of Perl modules by invoking the
appropriate compilers and linkers in a cross-platform manner. It was motivated
by the Module::Build project, but may be useful for other purposes as well.


%package ExtUtils-Embed
Summary:        Utilities for embedding Perl in C/C++ applications
Group:          Development/Languages
License:        GPL+ or Artistic
Epoch:          0
Version:        1.30
Requires:       perl-devel
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
BuildArch:      noarch

%description ExtUtils-Embed
Utilities for embedding Perl in C/C++ applications.


%package ExtUtils-Install
Summary:        Install files from here to there
Group:          Development/Languages
License:        GPL+ or Artistic
Epoch:          0
Version:        1.58
Requires:       perl-devel
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
BuildArch:      noarch

%description ExtUtils-Install
Handles the installing and uninstalling of perl modules, scripts, man
pages, etc.


%package ExtUtils-MakeMaker
Summary:        Create a module Makefile
Group:          Development/Languages
License:        GPL+ or Artistic
Epoch:          0
Version:        6.63.2
Requires:       perl-devel
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
Requires:       perl(ExtUtils::Install)
Requires:       perl(ExtUtils::Manifest)
Requires:       perl(Test::Harness)
BuildArch:      noarch

# Filter false DynaLoader provides. Versioned perl(DynaLoader) keeps
# unfiltered on perl package, no need to reinject it.
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(DynaLoader\\)\\s*$
%global __provides_exclude %__provides_exclude|^perl\\(ExtUtils::MakeMaker::_version\\)

%description ExtUtils-MakeMaker
Create a module Makefile.


%package ExtUtils-Manifest
Summary:        Utilities to write and check a MANIFEST file
Group:          Development/Languages
License:        GPL+ or Artistic
Epoch:          0
Version:        1.61
Requires:       perl-devel
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
BuildArch:      noarch

%description ExtUtils-Manifest
%{summary}.


%package ExtUtils-ParseXS
Summary:        Module and a script for converting Perl XS code into C code
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        3.16
Requires:       perl-devel
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
BuildArch:      noarch

%description ExtUtils-ParseXS
ExtUtils::ParseXS will compile XS code into C code by embedding the constructs
necessary to let C functions manipulate Perl values and creates the glue
necessary to let Perl access those functions.


%package File-Fetch
Summary:        Generic file fetching mechanism
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        0.32
Requires:       perl(IPC::Cmd) >= 0.36
Requires:       perl(Module::Load::Conditional) >= 0.04
Requires:       perl(Params::Check) >= 0.07
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
BuildArch:      noarch

%description File-Fetch
File::Fetch is a generic file fetching mechanism.

# FIXME Filter-Simple? version?
%package Filter
Summary:        Perl source filters
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        1.40
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}

%description Filter
Source filters alter the program text of a module before Perl sees it, much as
a C preprocessor alters the source text of a C program before the compiler
sees it.


%package IO-Compress
Summary:        IO::Compress wrapper for modules
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        2.048
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
Obsoletes:      perl-Compress-Zlib <= 2.020
Provides:       perl(IO::Uncompress::Bunzip2)

%description IO-Compress
This module is the base class for all IO::Compress and IO::Uncompress modules.
This module is not intended for direct use in application code. Its sole
purpose is to to be sub-classed by IO::Compress modules.


%package IO-Zlib
Summary:        Perl IO:: style interface to Compress::Zlib
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        1.10
Requires:       perl(Compress::Zlib)
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
BuildArch:      noarch

%description IO-Zlib
This modules provides an IO:: style interface to the Compress::Zlib package.
The main advantage is that you can use an IO::Zlib object in much the same way
as an IO::File object so you can have common code that doesn't know which sort
of file it is using.


%package IPC-Cmd
Summary:        Finding and running system commands made easy
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        0.76
Requires:       perl(ExtUtils::MakeMaker)
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
BuildArch:      noarch

%description IPC-Cmd
IPC::Cmd allows you to run commands, interactively if desired, in a platform
independent way, but have them still work.


%package HTTP-Tiny
Summary:        A small, simple, correct HTTP/1.1 client
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        0.017
Requires:       perl(Carp)
Requires:       perl(IO::Socket)
BuildArch:      noarch

%description HTTP-Tiny
This is a very simple HTTP/1.1 client, designed primarily for doing simple GET
requests without the overhead of a large framework like LWP::UserAgent.
It is more correct and more complete than HTTP::Lite. It supports proxies
(currently only non-authenticating ones) and redirection. It also correctly
resumes after EINTR.


%package JSON-PP
Summary:        JSON::XS compatible pure-Perl module
Epoch:          0
# 2.27150 version is a typo but we cannot fix it because it would break
# monotony
Version:        2.27200
License:        GPL+ or Artistic
Group:          Development/Libraries
BuildArch:      noarch
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
Conflicts:      perl-JSON < 2.50

%description JSON-PP
JSON::XS is the fastest and most proper JSON module on CPAN. It is written by
Marc Lehmann in C, so must be compiled and installed in the used environment.
JSON::PP is a pure-Perl module and is compatible with JSON::XS.


%package Locale-Codes
Summary:        Distribution of modules to handle locale codes
Epoch:          0
Version:        3.21
License:        GPL+ or Artistic
Group:          Development/Libraries
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
Requires:       perl(constant)
Provides:       perl(Locale::Codes) = %{version}
BuildArch:      noarch

# Do not export unversioned module
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(Locale::Codes\\)\\s*$

%description Locale-Codes
Locale-Codes is a distribution containing a set of modules. The modules
each deal with different types of codes which identify parts of the locale
including languages, countries, currency, etc.


%package Locale-Maketext-Simple
Summary:        Simple interface to Locale::Maketext::Lexicon
Group:          Development/Libraries
License:        MIT
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        0.21
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
BuildArch:      noarch

%description Locale-Maketext-Simple
This module is a simple wrapper around Locale::Maketext::Lexicon, designed
to alleviate the need of creating Language Classes for module authors.


%package Log-Message
Summary:        Generic message storage mechanism
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        0.04
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
# Add a versioned provides, since we pull the unversioned one out.
Provides:       perl(Log::Message::Handlers) = %{version}
BuildArch:      noarch

%description Log-Message
Log::Message is a generic message storage mechanism. It allows you to store
messages on a stack -- either shared or private -- and assign meta-data to it.
Some meta-data will automatically be added for you, like a timestamp and a
stack trace, but some can be filled in by the user, like a tag by which to
identify it or group it, and a level at which to handle the message (for
example, log it, or die with it).


%package Log-Message-Simple
Summary:        Simplified frontend to Log::Message
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        0.08
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
BuildArch:      noarch

%description Log-Message-Simple
This module provides standardized logging facilities using the
Log::Message module.


%package Module-Build
Summary:        Perl module for building and installing Perl modules
Group:          Development/Libraries
License:        GPL+ or Artistic
# Check epoch with standalone package
Epoch:          2
# real version 0.39_01
Version:        0.39.01
Requires:       perl(Archive::Tar) >= 1.08
Requires:       perl(CPAN::Meta) >= 2.110420
Requires:       perl(ExtUtils::CBuilder) >= 0.15
Requires:       perl(ExtUtils::ParseXS) >= 1.02
Requires:       perl-devel
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
BuildArch:      noarch

%description Module-Build
Module::Build is a system for building, testing, and installing Perl modules.
It is meant to be an alternative to ExtUtils::MakeMaker.  Developers may alter
the behavior of the module through subclassing in a much more straightforward
way than with MakeMaker. It also does not require a make on your system - most
of the Module::Build code is pure-perl and written in a very cross-platform
way. In fact, you don't even need a shell, so even platforms like MacOS
(traditional) can use it fairly easily. Its only prerequisites are modules that
are included with perl 5.6.0, and it works fine on perl 5.005 if you can
install a few additional modules.


%package Module-CoreList
Summary:        Perl core modules indexed by perl versions
Group:          Development/Languages
License:        GPL+ or Artistic
Epoch:          1
Version:        2.70

Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
Requires:       perl(version)
BuildArch:      noarch

%description Module-CoreList
Module::CoreList contains the hash of hashes %%Module::CoreList::version, this
is keyed on perl version as indicated in $].  The second level hash is module
=> version pairs.


%package Module-Load
Summary:        Runtime require of both modules and files
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        0.22
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
BuildArch:      noarch

%description Module-Load
Module::Load eliminates the need to know whether you are trying to require
either a file or a module.


%package Module-Load-Conditional
Summary:        Looking up module information / loading at runtime
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        0.46
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
BuildArch:      noarch

%description Module-Load-Conditional
Module::Load::Conditional provides simple ways to query and possibly load any
of the modules you have installed on your system during runtime.


%package Module-Loaded
Summary:        Mark modules as loaded or unloaded
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        0.08
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
BuildArch:      noarch

%description Module-Loaded
When testing applications, often you find yourself needing to provide
functionality in your test environment that would usually be provided by
external modules. Rather than munging the %INC by hand to mark these external
modules as loaded, so they are not attempted to be loaded by perl, this module
offers you a very simple way to mark modules as loaded and/or unloaded.


%package Module-Metadata
Summary:        Gather package and POD information from perl module files
Epoch:          0
Version:        1.000009
License:        GPL+ or Artistic
Group:          Development/Libraries
BuildArch:      noarch
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}

%description Module-Metadata
Gather package and POD information from perl module files

%package Module-Pluggable
Summary:        Automatically give your module the ability to have plugins
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
# Keep two digit decimal part
Version:        4.00
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
BuildArch:      noarch

%description Module-Pluggable
Provides a simple but, hopefully, extensible way of having 'plugins' for your
module.


%package Object-Accessor
Summary:        Perl module that allows per object accessors
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        0.42
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
BuildArch:      noarch

%description Object-Accessor
Object::Accessor provides an interface to create per object accessors (as
opposed to per Class accessors, as, for example, Class::Accessor provides).


%package Package-Constants
Summary:        List all constants declared in a package
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        0.02
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
BuildArch:      noarch

%description Package-Constants
Package::Constants lists all the constants defined in a certain package.  This
can be useful for, among others, setting up an autogenerated @EXPORT/@EXPORT_OK
for a Constants.pm file.


%package PathTools
Summary:        PathTools Perl module (Cwd, File::Spec)
# PathTools aka File::Spec
Group:          Development/Libraries
License:        (GPL+ or Artistic) and BSD
Epoch:          0
Version:        3.39.2
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}

%description PathTools
PathTools Perl module (Cwd, File::Spec).


%package Params-Check
Summary:        Generic input parsing/checking mechanism
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        0.32
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
BuildArch:      noarch

%description Params-Check
Params::Check is a generic input parsing/checking mechanism.


%package Parse-CPAN-Meta
Summary:        Parse META.yml and other similar CPAN metadata files
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        1.4402
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
BuildArch:      noarch
Requires:       perl(CPAN::Meta::YAML) >= 0.002
Requires:       perl(JSON::PP) >= 2.27103
# FIXME it could be removed now?
Obsoletes:      perl-Parse-CPAN-Meta < 1.40

%description Parse-CPAN-Meta
Parse::CPAN::Meta is a parser for META.yml files, based on the parser half of
YAML::Tiny.


%package Perl-OSType
Summary:        Map Perl operating system names to generic types
Version:        1.002
Epoch:          0
License:        GPL+ or Artistic
Group:          Development/Libraries
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
BuildArch:      noarch

%description Perl-OSType
Modules that provide OS-specific behaviors often need to know if the current
operating system matches a more generic type of operating systems. For example,
'linux' is a type of 'Unix' operating system and so is 'freebsd'.
This module provides a mapping between an operating system name as given by $^O
and a more generic type. The initial version is based on the OS type mappings
provided in Module::Build and ExtUtils::CBuilder (thus, Microsoft operating
systems are given the type 'Windows' rather than 'Win32').


%package Pod-Escapes
Summary:        Perl module for resolving POD escape sequences
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        1.04
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
BuildArch:      noarch

%description Pod-Escapes
This module provides things that are useful in decoding Pod E<...> sequences.
Presumably, it should be used only by Pod parsers and/or formatters.


%package Pod-Parser
Summary:        Basic perl modules for handling Plain Old Documentation (POD)
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        1.51
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
# Pod::Usage executes perldoc from perl-Pod-Perldoc by default
Requires:       perl-Pod-Perldoc
BuildArch:      noarch

%description Pod-Parser
This software distribution contains the packages for using Perl5 POD (Plain
Old Documentation). See the "perlpod" and "perlsyn" manual pages from your
Perl5 distribution for more information about POD.


%package Pod-Perldoc
Summary:        Look up Perl documentation in Pod format
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        3.17.00
# Pod::Perldoc::ToMan executes roff
# TODO no groff on OS/2 yet.
#Requires:       groff-base
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
BuildArch:      noarch

%description Pod-Perldoc
perldoc looks up a piece of documentation in .pod format that is embedded
in the perl installation tree or in a perl script, and displays it via
"groff -man | $PAGER". This is primarily used for the documentation for
the perl library modules.


%package Pod-Simple
Summary:        Framework for parsing POD documentation
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        3.20
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
BuildArch:      noarch

%description Pod-Simple
Pod::Simple is a Perl library for parsing text in the Pod ("plain old
documentation") markup language that is typically used for writing
documentation for Perl and for Perl modules.

%package Scalar-List-Utils
Summary:        A selection of general-utility scalar and list subroutines
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        1.25
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}

%description Scalar-List-Utils
Scalar::Util and List::Util contain a selection of subroutines that people have
expressed would be nice to have in the perl core, but the usage would not
really be high enough to warrant the use of a keyword, and the size so small
such that being individual extensions would be wasteful.


%package Term-UI
Summary:        Term::ReadLine UI made easy
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        0.30
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
Requires:       perl(Log::Message::Simple)
BuildArch:      noarch

%description Term-UI
Term::UI is a transparent way of eliminating the overhead of having to format
a question and then validate the reply, informing the user if the answer was not
proper and re-issuing the question.


%package Test-Harness
Summary:        Run Perl standard test scripts with statistics
Group:          Development/Languages
License:        GPL+ or Artistic
Epoch:          0
Version:        3.23
Requires:       perl-devel
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
BuildArch:      noarch
# Use rewritten module perl-Test-Harness
Provides:       perl-TAP-Harness = 3.17
Obsoletes:      perl-TAP-Harness < 3.10

%description Test-Harness
Run Perl standard test scripts with statistics.
Use TAP::Parser, Test::Harness package was whole rewritten.

%package Test-Simple
Summary:        Basic utilities for writing tests
Group:          Development/Languages
License:        GPL+ or Artistic
Epoch:          0
Version:        0.98
Requires:       perl-devel
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
Requires:       perl(Data::Dumper)
BuildArch:      noarch

%description Test-Simple
Basic utilities for writing tests.


%package Test-Simple-tests
Summary:        Test suite for package perl-Test-Simple
Group:          Development/Debug
License:        GPL+ or Artistic
Epoch:          0
Version:        0.98
Requires:       perl-Test-Simple = %{epoch}:%{version}-%{release}
Requires:       /usr/bin/prove
AutoReqProv:    0
BuildArch:      noarch

%description Test-Simple-tests
This package provides the test suite for package perl-Test-Simple.


%package Time-Piece
Summary:        Time objects from localtime and gmtime
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
# real 1.20_01
Version:        1.20.1
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}

%description Time-Piece
The Time::Piece module replaces the standard localtime and gmtime functions
with implementations that return objects.  It does so in a backwards compatible
manner, so that using localtime or gmtime as documented in perlfunc still
behave as expected.


%package parent
Summary:        Establish an ISA relationship with base classes at compile time
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        0.225
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
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


%package Socket
Summary:        C socket.h defines and structure manipulators
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        2.001
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}

%description Socket
This module is just a translation of the C socket.h file.  Unlike the old
mechanism of requiring a translated socket.ph file, this uses the h2xs program
(see the Perl source distribution) and your native C compiler.  This means
that it has a far more likely chance of getting the numbers right.  This
includes all of the commonly used pound-defines like AF_INET, SOCK_STREAM, etc.


%package threads
Summary:        Perl interpreter-based threads
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        1.86
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}

%description threads
Since Perl 5.8, thread programming has been available using a model called
interpreter threads  which provides a new Perl interpreter for each thread,
and, by default, results in no data or state information being shared between
threads.

(Prior to Perl 5.8, 5005threads was available through the Thread.pm API. This
threading model has been deprecated, and was removed as of Perl 5.10.0.)

As just mentioned, all variables are, by default, thread local. To use shared
variables, you need to also load threads::shared.


%package threads-shared
Summary:        Perl extension for sharing data structures between threads
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        1.40
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}

%description threads-shared
By default, variables are private to each thread, and each newly created thread
gets a private copy of each existing variable. This module allows you to share
variables across different threads (and pseudo-forks on Win32). It is used
together with the threads module.  This module supports the sharing of the
following data types only: scalars and scalar refs, arrays and array refs, and
hashes and hash refs.


%package version
Summary:        Perl extension for Version Objects
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          3
Version:        0.99
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
BuildArch:      noarch

%description version
Perl extension for Version Objects


%package Version-Requirements
Summary:        Set of version requirements for a CPAN dist
License:        GPL+ or Artistic
Group:          Development/Libraries
Version:        0.101022
Epoch:          0
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
BuildArch:      noarch

%description Version-Requirements
A Version::Requirements object models a set of version constraints like
those specified in the META.yml or META.json files in CPAN distributions.
It can be built up by adding more and more constraints, and it will reduce
them to the simplest representation.


%package core
Summary:        Base perl metapackage
Group:          Development/Languages
# This rpm doesn't contain any copyrightable material.
# Nevertheless, it needs a License tag, so we'll use the generic
# "perl" license.
License:        GPL+ or Artistic
Epoch:          0
Version:        %{perl_version}
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
Requires:       perl-libs = %{perl_epoch}:%{perl_version}-%{release}
Requires:       perl-devel = %{perl_epoch}:%{perl_version}-%{release}
Requires:       perl-macros

Requires:       perl-Archive-Extract, perl-Archive-Tar, perl-Compress-Raw-Bzip2
Requires:       perl-Carp, perl-Compress-Raw-Zlib, perl-CGI, perl-CPAN,
Requires:       perl-CPAN-Meta, perl-CPAN-Meta-YAML, perl-CPANPLUS,
Requires:       perl-Data-Dumper, perl-Digest, perl-Digest-MD5, perl-Digest-SHA,
Requires:       perl-ExtUtils-CBuilder, perl-ExtUtils-Embed,
Requires:       perl-ExtUtils-Install, perl-ExtUtils-MakeMaker
Requires:       perl-ExtUtils-Manifest
Requires:       perl-ExtUtils-ParseXS, perl-File-Fetch, perl-Filter,
Requires:       perl-HTTP-Tiny
Requires:       perl-IO-Compress, perl-IO-Zlib, perl-IPC-Cmd, perl-JSON-PP
Requires:       perl-Locale-Codes, perl-Locale-Maketext-Simple
Requires:       perl-Log-Message, perl-Log-Message-Simple, perl-Module-Build
Requires:       perl-Module-CoreList, perl-Module-Load
Requires:       perl-Module-Load-Conditional, perl-Module-Loaded, perl-Module-Metadata
Requires:       perl-Module-Pluggable, perl-Object-Accessor, perl-Package-Constants, perl-PathTools
Requires:       perl-Params-Check, perl-Parse-CPAN-Meta, perl-Perl-OSType
Requires:       perl-Pod-Escapes, perl-Pod-Parser, perl-Pod-Perldoc
Requires:       perl-Pod-Simple
Requires:       perl-Socket, perl-Term-UI, perl-Test-Harness, perl-Test-Simple
Requires:       perl-Time-Piece, perl-Version-Requirements, perl-version
Requires:       perl-threads, perl-threads-shared, perl-parent

%description core
A metapackage which requires all of the perl bits and modules in the upstream
tarball from perl.org.

%debug_package

%prep
%scm_setup

# TODO No iconv on OS/2 yet.
%if 0
#
# Candidates for doc recoding (need case by case review):
# find . -name "*.pod" -o -name "README*" -o -name "*.pm" | xargs file -i | grep charset= | grep -v '\(us-ascii\|utf-8\)'
recode()
{
        iconv -f "${2:-iso-8859-1}" -t utf-8 < "$1" > "${1}_"
        touch -r "$1" "${1}_"
        mv -f "${1}_" "$1"
}
recode README.cn euc-cn
recode README.jp euc-jp
recode README.ko euc-kr
# TODO iconv fail on this one
##recode README.tw big5
recode pod/perlebcdic.pod
recode pod/perlhack.pod
recode pod/perlhist.pod
recode pod/perlthrtut.pod
recode AUTHORS
%endif

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

%global perl_vendorlib  %{privlib}/vendor_perl
%global perl_vendorarch %{archlib}/vendor_perl

# For perl-5.14.2-large-repeat-heap-abuse.patch
perl regen.pl -v

%{_bindir}/sh Configure -des -Doptimize="$RPM_OPT_FLAGS" \
%if 0
        -Dccdlflags="-Wl,--enable-new-dtags" \
%endif
        -Dlddlflags="-shared $RPM_OPT_FLAGS $RPM_LD_FLAGS" \
        -DDEBUGGING=-g \
        -Dversion=%{perl_version} \
        -Dmyhostname=localhost \
        -Dperladmin=root@localhost \
        -Dcc='%{__cc}' \
        -Dsh='%{_bindir}/sh.exe' \
        -Dcf_by='bww bitwise works GmbH' \
        -Dprefix=%{_prefix} \
        -Dvendorprefix=%{_prefix} \
        -Dsiteprefix=%{_prefix}/local \
        -Dsitelib="%{_prefix}/local/share/perl5" \
        -Dsitearch="%{_prefix}/local/%{_lib}/perl5" \
        -Dprivlib="%{privlib}" \
        -Dvendorlib="%{perl_vendorlib}" \
        -Darchlib="%{archlib}" \
        -Dvendorarch="%{perl_vendorarch}" \
%if 0
        -Darchname=%{perl_archname} \
%endif
        -Duseshrplib \
%if 0
        -Dusethreads \
        -Duseithreads \
        -Dusedtrace='%{_bindir}/dtrace' \
%endif
        -Duselargefiles \
%if 0
        -Dd_semctl_semun \
        -Di_db \
%endif
%if %{with gdbm}
        -Ui_ndbm \
        -Di_gdbm \
%endif
%if 0
        -Di_shadow \
        -Di_syslog \
%endif
        -Dman3ext=3pm \
        -Duseperlio \
        -Dinstallusrbinperl=n \
        -Ubincompat5005 \
        -Uversiononly \
        -Dpager='%{_bindir}less -isr' \
        -Dd_gethostent_r_proto -Ud_endhostent_r_proto -Ud_sethostent_r_proto \
        -Ud_endprotoent_r_proto -Ud_setprotoent_r_proto \
        -Ud_endservent_r_proto -Ud_setservent_r_proto \
        -Dscriptdir='%{_bindir}' \
        -Dusesitecustomize

BUILD_BZIP2=0
BZIP2_LIB=%{_libdir}
export BUILD_BZIP2 BZIP2_LIB

# Fix /@unixroot paths
sed -i 's#.:/usr#%{_exec_prefix}#gi' config.sh
sed -i 's#.:/mptn#/@system_drive/mptn#gi' config.sh

make os2.o
perl make_patchnum.pl

%if 1
# SMP build does not work for now.
make
%else
make %{?_smp_mflags}
%endif

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# Symlink main executable for rpm scripts.
ln -s %{_bindir}/perl.exe %{buildroot}%{_bindir}/perl

# Remove .imp files.
rm -rf %{buildroot}%{archlib}/CORE/*.imp

%global build_archlib $RPM_BUILD_ROOT%{archlib}
%global build_privlib $RPM_BUILD_ROOT%{privlib}
%global build_bindir  $RPM_BUILD_ROOT%{_bindir}
%global new_perl BEGINLIBPATH="$RPM_BUILD_ROOT%{_libdir} LIBPATHSTRICT=T" \\\
    LD_LIBRARY_PATH="%{build_archlib}/CORE" \\\
    PERL5LIB="%{build_archlib}:%{build_privlib}" \\\
    %{build_bindir}/perl

for i in asm/termios.h syscall.h syslimits.h syslog.h \
    sys/ioctl.h sys/socket.h sys/time.h wait.h
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
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/rpm
install -p -m 644 %{SOURCE3} ${RPM_BUILD_ROOT}%{_sysconfdir}/rpm/

#
# Core modules removal
#
find $RPM_BUILD_ROOT -type f -name '*.bs' -empty | xargs rm -f

chmod -R u+w $RPM_BUILD_ROOT/*

# miniperl? As an interpreter? How odd. Anyway, a symlink does it:
rm %{build_privlib}/ExtUtils/xsubpp
ln -s ../../../bin/xsubpp %{build_privlib}/ExtUtils/

# Don't need the .packlist
rm %{build_archlib}/.packlist

# TODO No iconv on OS/2 yet.
%if 0
# Fix some manpages to be UTF-8
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1/
pushd $RPM_BUILD_ROOT%{_mandir}/man1/
  for i in perl588delta.1 perldelta.1 ; do
    iconv -f MS-ANSI -t UTF-8 $i --output new-$i
    rm $i
    mv new-$i $i
  done
popd
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

%if 0
# Selected "Dual-lifed cpan" packages
pushd cpan
for package in Test-Simple; do
    for dir in `find ${package} -type d -name t -maxdepth 2` ; do
        tar -cf - $dir | ( cd %{buildroot}%{perl5_testdir} && tar -xf - )
    done
done
popd
%endif

# TODO: Canonicalize test files (rewrite intrerpreter path, fix permissions)
# XXX: We cannot rewrite ./perl before %%check phase. Otherwise the test
# would run against system perl at build-time.
# See __spec_check_pre global macro in macros.perl.
#T_FILES=`find %%{buildroot}%%{perl5_testdir} -type f -name '*.t'`
#%%fix_shbang_line $T_FILES
#%%{__chmod} +x $T_FILES
#%%{_fixperms} %%{buildroot}%%{perl5_testdir}

%check
%if %{with test}
%if %{parallel_tests}
    JOBS=$(printf '%%s' "%{?_smp_mflags}" | sed 's/.*-j\([0-9][0-9]*\).*/\1/')
    LC_ALL=C TEST_JOBS=$JOBS make test_harness
%else
    LC_ALL=C make test
%endif
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{debug_package_exclude_files}
%doc Artistic AUTHORS Copying README Changes
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3*
%{_bindir}/*
%{privlib}
%{archlib}
%{perl_vendorlib}

# libs
%exclude %{perl_vendorarch}

# devel
%exclude %{_bindir}/enc2xs
%exclude %{_mandir}/man1/enc2xs*
%exclude %{privlib}/Encode/
%exclude %{_bindir}/h2xs
%exclude %{_mandir}/man1/h2xs*
%exclude %{_bindir}/libnetcfg
%exclude %{_mandir}/man1/libnetcfg*
%exclude %{_bindir}/perlivp
%exclude %{_mandir}/man1/perlivp*
%exclude %{archlib}/CORE/*.h
%exclude %{archlib}/CORE/os2/*.h
%exclude %{archlib}/CORE/libperl*.a
%exclude %{_mandir}/man1/perlxs*

# Archive-Extract
%exclude %{privlib}/Archive/Extract.pm
%exclude %{_mandir}/man3/Archive.Extract.3*

# Archive-Tar
%exclude %{_bindir}/ptar
%exclude %{_bindir}/ptardiff
%exclude %{_bindir}/ptargrep
%exclude %{privlib}/Archive/Tar/
%exclude %{privlib}/Archive/Tar.pm
%exclude %{_mandir}/man1/ptar.1*
%exclude %{_mandir}/man1/ptardiff.1*
%exclude %{_mandir}/man1/ptargrep.1*
%exclude %{_mandir}/man3/Archive.Tar*

# Carp
%exclude %{privlib}/Carp
%exclude %{privlib}/Carp.*
%exclude %{_mandir}/man3/Carp.*

# CGI
%exclude %{privlib}/CGI/
%exclude %{privlib}/CGI.pm
%exclude %{_mandir}/man3/CGI.3*
%exclude %{_mandir}/man3/CGI.*.3*

# CPAN
%exclude %{_bindir}/cpan
%exclude %{privlib}/CPAN/
%exclude %{privlib}/CPAN.pm
%exclude %{_mandir}/man1/cpan.1*
%exclude %{_mandir}/man3/CPAN.*

# CPAN-Meta
%exclude %{privlib}/CPAN/Meta.pm
%exclude %{privlib}/CPAN/Meta/Converter.pm
%exclude %{privlib}/CPAN/Meta/Feature.pm
%exclude %{privlib}/CPAN/Meta/History.pm
%exclude %{privlib}/CPAN/Meta/Prereqs.pm
%exclude %{privlib}/CPAN/Meta/Spec.pm
%exclude %{privlib}/CPAN/Meta/Validator.pm
%exclude %{_mandir}/man3/CPAN.Meta*

# CPAN-Meta-YAML
%exclude %{privlib}/CPAN/Meta/YAML.pm
%exclude %{_mandir}/man3/CPAN.Meta.YAML*

# Parse-CPAN-Meta
%exclude %dir %{privlib}/Parse/
%exclude %dir %{privlib}/Parse/CPAN/
%exclude %{privlib}/Parse/CPAN/Meta.pm
%exclude %{_mandir}/man3/Parse.CPAN.Meta.3*

# CPANPLUS
%exclude %{_bindir}/cpan2dist
%exclude %{_bindir}/cpanp
%exclude %{_bindir}/cpanp-run-perl
%exclude %{privlib}/CPANPLUS/
%exclude %{privlib}/CPANPLUS.pm
%exclude %{_mandir}/man1/cpan2dist.1*
%exclude %{_mandir}/man1/cpanp.1*
%exclude %{_mandir}/man3/CPANPLUS*

# Compress-Raw-Bzip2
%exclude %dir %{archlib}/Compress
%exclude %{archlib}/Compress/Raw/Bzip2.pm
%exclude %{_mandir}/man3/Compress.Raw.Bzip2*

# Compress::Raw::Zlib
%exclude %{archlib}/Compress/Raw/
%exclude %{archlib}/auto/Compress
%exclude %{archlib}/auto/Compress/Raw/
%exclude %{archlib}/auto/Compress/Raw/Zlib/
%exclude %{_mandir}/man3/Compress.Raw.Zlib*

# Data::Dumper
%exclude %dir %{archlib}/auto/Data
%exclude %dir %{archlib}/auto/Data/Dumper
%exclude %{archlib}/auto/Data/Dumper/
%exclude %dir %{archlib}/Data
%exclude %{archlib}/Data/Dumper.pm
%exclude %{_mandir}/man3/Data.Dumper.3*

# Digest
%exclude %{privlib}/Digest.pm
%exclude %dir %{privlib}/Digest
%exclude %{privlib}/Digest/base.pm
%exclude %{privlib}/Digest/file.pm
%exclude %{_mandir}/man3/Digest.3*
%exclude %{_mandir}/man3/Digest.base.3*
%exclude %{_mandir}/man3/Digest.file.3*

# Digest::MD5
%exclude %{archlib}/Digest/MD5.pm
%exclude %{archlib}/auto/Digest/MD5/
%exclude %{_mandir}/man3/Digest.MD5.3*

# Digest::SHA
%exclude %{_bindir}/shasum
%exclude %{archlib}/Digest/SHA.pm
%exclude %{archlib}/auto/Digest/SHA/
%exclude %{_mandir}/man1/shasum.1*
%exclude %{_mandir}/man3/Digest.SHA.3*

# ExtUtils::CBuilder
%exclude %{privlib}/ExtUtils/CBuilder/
%exclude %{privlib}/ExtUtils/CBuilder.pm
%exclude %{_mandir}/man3/ExtUtils.CBuilder*

# ExtUtils::Embed
%exclude %{privlib}/ExtUtils/Embed.pm
%exclude %{_mandir}/man3/ExtUtils.Embed*

# ExtUtils::Install
%exclude %{privlib}/ExtUtils/Install.pm
%exclude %{privlib}/ExtUtils/Installed.pm
%exclude %{privlib}/ExtUtils/Packlist.pm
%exclude %{_mandir}/man3/ExtUtils.Install.3*
%exclude %{_mandir}/man3/ExtUtils.Installed.3*
%exclude %{_mandir}/man3/ExtUtils.Packlist.3*

# ExtUtils::Manifest
%exclude %{privlib}/ExtUtils/Manifest.pm
%exclude %{privlib}/ExtUtils/MANIFEST.SKIP
%exclude %{_mandir}/man3/ExtUtils.Manifest.3*

# ExtUtils::MakeMaker
%exclude %{_bindir}/instmodsh
%exclude %{privlib}/ExtUtils/Command/
%exclude %{privlib}/ExtUtils/Liblist/
%exclude %{privlib}/ExtUtils/Liblist.pm
%exclude %{privlib}/ExtUtils/MakeMaker/
%exclude %{privlib}/ExtUtils/MakeMaker.pm
%exclude %{privlib}/ExtUtils/MM*.pm
%exclude %{privlib}/ExtUtils/MY.pm
%exclude %{privlib}/ExtUtils/Mkbootstrap.pm
%exclude %{privlib}/ExtUtils/Mksymlists.pm
%exclude %{privlib}/ExtUtils/testlib.pm
%exclude %{_mandir}/man1/instmodsh.1*
%exclude %{_mandir}/man3/ExtUtils.Command.MM*
%exclude %{_mandir}/man3/ExtUtils.Liblist.3*
%exclude %{_mandir}/man3/ExtUtils.MM*
%exclude %{_mandir}/man3/ExtUtils.MY.3*
%exclude %{_mandir}/man3/ExtUtils.MakeMaker*
%exclude %{_mandir}/man3/ExtUtils.Mkbootstrap.3*
%exclude %{_mandir}/man3/ExtUtils.Mksymlists.3*
%exclude %{_mandir}/man3/ExtUtils.testlib.3*

# ExtUtils::ParseXS
%exclude %dir %{privlib}/ExtUtils/ParseXS/
%exclude %dir %{privlib}/ExtUtils/Typemaps/
%exclude %{privlib}/ExtUtils/ParseXS.pm
%exclude %{privlib}/ExtUtils/ParseXS.pod
%exclude %{privlib}/ExtUtils/ParseXS/Constants.pm
%exclude %{privlib}/ExtUtils/ParseXS/CountLines.pm
%exclude %{privlib}/ExtUtils/ParseXS/Utilities.pm
%exclude %{privlib}/ExtUtils/Typemaps.pm
%exclude %{privlib}/ExtUtils/Typemaps/Cmd.pm
%exclude %{privlib}/ExtUtils/Typemaps/InputMap.pm
%exclude %{privlib}/ExtUtils/Typemaps/OutputMap.pm
%exclude %{privlib}/ExtUtils/Typemaps/Type.pm
%exclude %{privlib}/ExtUtils/xsubpp
%exclude %{_bindir}/xsubpp
%exclude %{_mandir}/man1/xsubpp*
%exclude %{_mandir}/man3/ExtUtils.ParseXS.3*
%exclude %{_mandir}/man3/ExtUtils.ParseXS.Constants.3*
%exclude %{_mandir}/man3/ExtUtils.ParseXS.Utilities.3*
%exclude %{_mandir}/man3/ExtUtils.Typemaps.3*
%exclude %{_mandir}/man3/ExtUtils.Typemaps.Cmd.3*
%exclude %{_mandir}/man3/ExtUtils.Typemaps.InputMap.3*
%exclude %{_mandir}/man3/ExtUtils.Typemaps.OutputMap.3*
%exclude %{_mandir}/man3/ExtUtils.Typemaps.Type.3*

# File::Fetch
%exclude %{privlib}/File/Fetch.pm
%exclude %{_mandir}/man3/File.Fetch.3*

# Filter
%exclude %{archlib}/auto/Filter/Util
%exclude %{archlib}/Filter/Util
%exclude %{privlib}/Pod/perlfilter.pod
%exclude %{_mandir}/man1/perlfilter.*
%exclude %{_mandir}/man3/Filter.Util.*

# IO::Compress
%exclude %{_bindir}/zipdetails
%exclude %{privlib}/IO/Compress/FAQ.pod
%exclude %{_mandir}/man1/zipdetails.*
%exclude %{_mandir}/man3/IO.Compress.FAQ.*
# Compress::Zlib
%exclude %{privlib}/Compress/Zlib.pm
%exclude %{_mandir}/man3/Compress.Zlib*
# IO::Compress::Base
%exclude %{privlib}/File/GlobMapper.pm
%exclude %{privlib}/IO/Compress/Base/
%exclude %{privlib}/IO/Compress/Base.pm
%exclude %{privlib}/IO/Uncompress/AnyUncompress.pm
%exclude %{privlib}/IO/Uncompress/Base.pm
%exclude %{_mandir}/man3/File.GlobMapper.*
%exclude %{_mandir}/man3/IO.Compress.Base.*
%exclude %{_mandir}/man3/IO.Uncompress.AnyUncompress.*
%exclude %{_mandir}/man3/IO.Uncompress.Base.*
# IO::Compress::Zlib
%exclude %{privlib}/IO/Compress/Adapter/
%exclude %{privlib}/IO/Compress/Deflate.pm
%exclude %{privlib}/IO/Compress/Gzip/
%exclude %{privlib}/IO/Compress/Gzip.pm
%exclude %{privlib}/IO/Compress/RawDeflate.pm
%exclude %{privlib}/IO/Compress/Bzip2.pm
%exclude %{privlib}/IO/Compress/Zip/
%exclude %{privlib}/IO/Compress/Zip.pm
%exclude %{privlib}/IO/Compress/Zlib/
%exclude %{privlib}/IO/Uncompress/Adapter/
%exclude %{privlib}/IO/Uncompress/AnyInflate.pm
%exclude %{privlib}/IO/Uncompress/Bunzip2.pm
%exclude %{privlib}/IO/Uncompress/Gunzip.pm
%exclude %{privlib}/IO/Uncompress/Inflate.pm
%exclude %{privlib}/IO/Uncompress/RawInflate.pm
%exclude %{privlib}/IO/Uncompress/Unzip.pm
%exclude %{_mandir}/man3/IO.Compress.Deflate*
%exclude %{_mandir}/man3/IO.Compress.Bzip2*
%exclude %{_mandir}/man3/IO.Compress.Gzip*
%exclude %{_mandir}/man3/IO.Compress.RawDeflate*
%exclude %{_mandir}/man3/IO.Compress.Zip*
%exclude %{_mandir}/man3/IO.Uncompress.AnyInflate*
%exclude %{_mandir}/man3/IO.Uncompress.Bunzip2*
%exclude %{_mandir}/man3/IO.Uncompress.Gunzip*
%exclude %{_mandir}/man3/IO.Uncompress.Inflate*
%exclude %{_mandir}/man3/IO.Uncompress.RawInflate*
%exclude %{_mandir}/man3/IO.Uncompress.Unzip*

# IO::Zlib
%exclude %{privlib}/IO/Zlib.pm
%exclude %{_mandir}/man3/IO.Zlib.*

# HTTP::Tiny
%exclude %{privlib}/HTTP/Tiny.pm
%exclude %{_mandir}/man3/HTTP.Tiny*

# IPC::Cmd
%exclude %{privlib}/IPC/Cmd.pm
%exclude %{_mandir}/man3/IPC.Cmd.3*

# JSON::PP
%exclude %{_bindir}/json_pp
%exclude %{privlib}/JSON/PP
%exclude %{privlib}/JSON/PP.pm
%exclude %{_mandir}/man1/json_pp.1*
%exclude %{_mandir}/man3/JSON.PP.3*
%exclude %{_mandir}/man3/JSON.PP.Boolean.3pm*

# Locale::Codes
%exclude %{privlib}/Locale/Codes
%exclude %{privlib}/Locale/Codes.*
%exclude %{privlib}/Locale/Country.*
%exclude %{privlib}/Locale/Currency.*
%exclude %{privlib}/Locale/Language.*
%exclude %{privlib}/Locale/Script.*
%exclude %{_mandir}/man3/Locale.Codes.*
%exclude %{_mandir}/man3/Locale.Country.*
%exclude %{_mandir}/man3/Locale.Currency.*
%exclude %{_mandir}/man3/Locale.Language.*
%exclude %{_mandir}/man3/Locale.Script.*

# Locale::Maketext::Simple
%exclude %{privlib}/Locale/Maketext/Simple.pm
%exclude %{_mandir}/man3/Locale.Maketext.Simple.*

# Log::Message
%exclude %{privlib}/Log/Message.pm
%exclude %{privlib}/Log/Message/Config.pm
%exclude %{privlib}/Log/Message/Handlers.pm
%exclude %{privlib}/Log/Message/Item.pm
%exclude %{_mandir}/man3/Log.Message.3*
%exclude %{_mandir}/man3/Log.Message.Config.3*
%exclude %{_mandir}/man3/Log.Message.Handlers.3*
%exclude %{_mandir}/man3/Log.Message.Item.3*

# Log::Message::Simple
%exclude %{privlib}/Log/Message/Simple.pm
%exclude %{_mandir}/man3/Log.Message.Simple.3*

# Module::Build
%exclude %{_bindir}/config_data
%exclude %{privlib}/inc/
%exclude %{privlib}/Module/Build/
%exclude %{privlib}/Module/Build.pm
%exclude %{_mandir}/man1/config_data.1*
%exclude %{_mandir}/man3/Module.Build*
%exclude %{_mandir}/man3/inc.latest.3*

# Module-CoreList
%exclude %{_bindir}/corelist
%exclude %{privlib}/Module/CoreList.pm
%exclude %{_mandir}/man1/corelist*
%exclude %{_mandir}/man3/Module.CoreList*

# Module-Load
%exclude %{privlib}/Module/Load.pm
%exclude %{_mandir}/man3/Module.Load.*

# Module-Load-Conditional
%exclude %{privlib}/Module/Load/
%exclude %{_mandir}/man3/Module.Load.Conditional*

# Module-Loaded
%exclude %{privlib}/Module/Loaded.pm
%exclude %{_mandir}/man3/Module.Loaded*

# Module-Metadata
%exclude %{privlib}/Module/Metadata.pm
%exclude %{_mandir}/man3/Module.Metadata.3pm*

# Module-Pluggable
%exclude %{privlib}/Devel/InnerPackage.pm
%exclude %{privlib}/Module/Pluggable/
%exclude %{privlib}/Module/Pluggable.pm
%exclude %{_mandir}/man3/Devel.InnerPackage*
%exclude %{_mandir}/man3/Module.Pluggable*

# Object-Accessor
%exclude %{privlib}/Object/
%exclude %{_mandir}/man3/Object.Accessor*

# Package-Constants
%exclude %{privlib}/Package/
%exclude %{_mandir}/man3/Package.Constants*

# PathTools
%exclude %{archlib}/Cwd.pm
%exclude %{archlib}/File/Spec*
%exclude %{archlib}/auto/Cwd/
%exclude %{_mandir}/man3/Cwd*
%exclude %{_mandir}/man3/File.Spec*

# Params-Check
%exclude %{privlib}/Params/
%exclude %{_mandir}/man3/Params.Check*

# Perl-OSType
%exclude %{privlib}/Perl/OSType.pm
%exclude %{_mandir}/man3/Perl.OSType.3pm*

# parent
%exclude %{privlib}/parent.pm
%exclude %{_mandir}/man3/parent.3*

# Pod-Escapes
%exclude %{privlib}/Pod/Escapes.pm
%exclude %{_mandir}/man3/Pod.Escapes.*

# Pod-Parser
%exclude %{_bindir}/pod2usage
%exclude %{_bindir}/podchecker
%exclude %{_bindir}/podselect
%exclude %{privlib}/Pod/Checker.pm
%exclude %{privlib}/Pod/Find.pm
%exclude %{privlib}/Pod/InputObjects.pm
%exclude %{privlib}/Pod/ParseUtils.pm
%exclude %{privlib}/Pod/Parser.pm
%exclude %{privlib}/Pod/PlainText.pm
%exclude %{privlib}/Pod/Select.pm
%exclude %{privlib}/Pod/Usage.pm
%exclude %{_mandir}/man1/pod2usage.1*
%exclude %{_mandir}/man1/podchecker.1*
%exclude %{_mandir}/man1/podselect.1*
%exclude %{_mandir}/man3/Pod.Checker.*
%exclude %{_mandir}/man3/Pod.Find.*
%exclude %{_mandir}/man3/Pod.InputObjects.*
%exclude %{_mandir}/man3/Pod.ParseUtils.*
%exclude %{_mandir}/man3/Pod.Parser.*
%exclude %{_mandir}/man3/Pod.PlainText.*
%exclude %{_mandir}/man3/Pod.Select.*
%exclude %{_mandir}/man3/Pod.Usage.*

# Pod-Perldoc
%exclude %{_bindir}/perldoc
%exclude %{privlib}/Pod/perldoc.pod
%exclude %{privlib}/Pod/Perldoc.pm
%exclude %{privlib}/Pod/Perldoc/
%exclude %{_mandir}/man1/perldoc.1*
%exclude %{_mandir}/man3/Pod.Perldoc*

# Pod-Simple
%exclude %{privlib}/Pod/Simple/
%exclude %{privlib}/Pod/Simple.pm
%exclude %{privlib}/Pod/Simple.pod
%exclude %{_mandir}/man3/Pod.Simple*

# Scalar-List-Utils
%exclude %{archlib}/List/
%exclude %{archlib}/Scalar/
%exclude %{archlib}/auto/List/
%exclude %{_mandir}/man3/List.Util*
%exclude %{_mandir}/man3/Scalar.Util*

# Term-UI
%exclude %{privlib}/Term/UI.pm
%exclude %{privlib}/Term/UI/
%exclude %{_mandir}/man3/Term.UI*

# Test::Harness
%exclude %{_bindir}/prove
%exclude %{privlib}/App*
%exclude %{privlib}/TAP*
%exclude %{privlib}/Test/Harness*
%exclude %{_mandir}/man1/prove.1*
%exclude %{_mandir}/man3/App*
%exclude %{_mandir}/man3/TAP*
%exclude %{_mandir}/man3/Test.Harness*

# Test::Simple
%exclude %{privlib}/Test/More*
%exclude %{privlib}/Test/Builder*
%exclude %{privlib}/Test/Simple*
%exclude %{privlib}/Test/Tutorial*
%exclude %{_mandir}/man3/Test.More*
%exclude %{_mandir}/man3/Test.Builder*
%exclude %{_mandir}/man3/Test.Simple*
%exclude %{_mandir}/man3/Test.Tutorial*

# Time::Piece
%exclude %{archlib}/Time/Piece.pm
%exclude %{archlib}/Time/Seconds.pm
%exclude %{archlib}/auto/Time/Piece/
%exclude %{_mandir}/man3/Time.Piece.3*
%exclude %{_mandir}/man3/Time.Seconds.3*

# Version-Requirements
%exclude %{privlib}/version/Requirements.pm
%exclude %{_mandir}/man3/version.Requirements.3*

# Socket
%exclude %dir %{archlib}/auto/Socket
%exclude %{archlib}/auto/Socket/
%exclude %{archlib}/Socket.pm
%exclude %{_mandir}/man3/Socket.3*

# threads
%dir %exclude %{archlib}/auto/threads
%exclude %{archlib}/auto/threads/thread*
%exclude %{archlib}/threads.pm
%exclude %{_mandir}/man3/threads.3*

# threads-shared
%exclude %{archlib}/auto/threads/shared/
%exclude %dir %{archlib}/threads
%exclude %{archlib}/threads/shared*
%exclude %{_mandir}/man3/threads.shared*

# version
%exclude %{privlib}/version.pm
%exclude %{privlib}/version.pod
%exclude %{privlib}/version/
%exclude %{_mandir}/man3/version.3*
%exclude %{_mandir}/man3/version.Internals.3*

%files libs
%defattr(-,root,root)
%{_libdir}/*.dll
%dir %{archlib}
%dir %{perl_vendorarch}
%dir %{perl_vendorarch}/auto

%files devel
%{_bindir}/enc2xs
%{_mandir}/man1/enc2xs*
%{privlib}/Encode/
%{_bindir}/h2xs
%{_mandir}/man1/h2xs*
%{_bindir}/libnetcfg
%{_mandir}/man1/libnetcfg*
%{_bindir}/perlivp
%{_mandir}/man1/perlivp*
%{archlib}/CORE/*.h
%{archlib}/CORE/os2/*.h
%{archlib}/CORE/libperl*.a
%{_mandir}/man1/perlxs*

%files macros
%attr(0644,root,root) %{_sysconfdir}/rpm/macros.perl

%files tests
%{perl5_testdir}/
#exclude %{perl5_testdir}/Test-Simple

%files Archive-Extract
%{privlib}/Archive/Extract.pm
%{_mandir}/man3/Archive.Extract.3*

%files Archive-Tar
%{_bindir}/ptar
%{_bindir}/ptardiff
%{_bindir}/ptargrep
%{privlib}/Archive/Tar/
%{privlib}/Archive/Tar.pm
%{_mandir}/man1/ptar.1*
%{_mandir}/man1/ptardiff.1*
%{_mandir}/man1/ptargrep.1*
%{_mandir}/man3/Archive.Tar*

%files Carp
%{privlib}/Carp
%{privlib}/Carp.*
%{_mandir}/man3/Carp.*

%files CGI
%{privlib}/CGI/
%{privlib}/CGI.pm
%{_mandir}/man3/CGI.3*
%{_mandir}/man3/CGI.*.3*

%files Compress-Raw-Bzip2
%dir %{archlib}/Compress
%dir %{archlib}/Compress/Raw
%{archlib}/Compress/Raw/Bzip2.pm
%dir %{archlib}/auto/Compress/
%dir %{archlib}/auto/Compress/Raw/
%{archlib}/auto/Compress/Raw/Bzip2/
%exclude %{archlib}/auto/Compress/Raw/Bzip2/*.dbg
%{_mandir}/man3/Compress.Raw.Bzip2*

%files Compress-Raw-Zlib
%dir %{archlib}/Compress
%dir %{archlib}/Compress/Raw
%{archlib}/Compress/Raw/Zlib.pm
%dir %{archlib}/auto/Compress/
%dir %{archlib}/auto/Compress/Raw/
%{archlib}/auto/Compress/Raw/Zlib/
%exclude %{archlib}/auto/Compress/Raw/Zlib/*.dbg
%{_mandir}/man3/Compress.Raw.Zlib*

%files CPAN
%{_bindir}/cpan
%{privlib}/CPAN/
%{privlib}/CPAN.pm
%{_mandir}/man1/cpan.1*
%{_mandir}/man3/CPAN.*
%exclude %{privlib}/CPAN/Meta/
%exclude %{privlib}/CPAN/Meta.pm
%exclude %{_mandir}/man3/CPAN.Meta*

%files CPAN-Meta
%dir %{privlib}/CPAN/Meta
%{privlib}/CPAN/Meta.pm
%{privlib}/CPAN/Meta/Converter.pm
%{privlib}/CPAN/Meta/Feature.pm
%{privlib}/CPAN/Meta/History.pm
%{privlib}/CPAN/Meta/Prereqs.pm
# TODO We don't provide separate perl-CPAN-Meta-Requirements on OS/2 yet.
%if 1
%{privlib}/CPAN/Meta/Requirements.pm
%endif
%{privlib}/CPAN/Meta/Spec.pm
%{privlib}/CPAN/Meta/Validator.pm
%{_mandir}/man3/CPAN.Meta*
%exclude %{_mandir}/man3/CPAN.Meta.YAML*

%files CPAN-Meta-YAML
%{privlib}/CPAN/Meta/YAML.pm
%{_mandir}/man3/CPAN.Meta.YAML*

%files CPANPLUS
%{_bindir}/cpan2dist
%{_bindir}/cpanp
%{_bindir}/cpanp-run-perl
%{privlib}/CPANPLUS/
%{privlib}/CPANPLUS.pm
%{_mandir}/man1/cpan2dist.1*
%{_mandir}/man1/cpanp.1*
%{_mandir}/man3/CPANPLUS*

%files Data-Dumper
%dir %{archlib}/auto/Data
%dir %{archlib}/auto/Data/Dumper
%{archlib}/auto/Data/Dumper/
%exclude %{archlib}/auto/Data/Dumper/*.dbg
%dir %{archlib}/Data
%{archlib}/Data/Dumper.pm
%{_mandir}/man3/Data.Dumper.3*

%files Digest
%{privlib}/Digest.pm
%dir %{privlib}/Digest
%{privlib}/Digest/base.pm
%{privlib}/Digest/file.pm
%{_mandir}/man3/Digest.3*
%{_mandir}/man3/Digest.base.3*
%{_mandir}/man3/Digest.file.3*

%files Digest-MD5
%{archlib}/Digest/MD5.pm
%{archlib}/auto/Digest/MD5/
%exclude %{archlib}/auto/Digest/MD5/*.dbg
%{_mandir}/man3/Digest.MD5.3*

%files Digest-SHA
%{_bindir}/shasum
%dir %{archlib}/Digest/
%{archlib}/Digest/SHA.pm
%{archlib}/auto/Digest/SHA/
%exclude %{archlib}/auto/Digest/SHA/*.dbg
%{_mandir}/man1/shasum.1*
%{_mandir}/man3/Digest.SHA.3*

%files ExtUtils-CBuilder
%{privlib}/ExtUtils/CBuilder/
%{privlib}/ExtUtils/CBuilder.pm
%{_mandir}/man3/ExtUtils.CBuilder*

%files ExtUtils-Embed
%{privlib}/ExtUtils/Embed.pm
%{_mandir}/man3/ExtUtils.Embed*

%files ExtUtils-Install
%{privlib}/ExtUtils/Install.pm
%{privlib}/ExtUtils/Installed.pm
%{privlib}/ExtUtils/Packlist.pm
%{_mandir}/man3/ExtUtils.Install.3*
%{_mandir}/man3/ExtUtils.Installed.3*
%{_mandir}/man3/ExtUtils.Packlist.3*

%files ExtUtils-Manifest
%{privlib}/ExtUtils/Manifest.pm
%{privlib}/ExtUtils/MANIFEST.SKIP
%{_mandir}/man3/ExtUtils.Manifest.3*

%files ExtUtils-MakeMaker
%{_bindir}/instmodsh
%{privlib}/ExtUtils/Command/
%{privlib}/ExtUtils/Liblist/
%{privlib}/ExtUtils/Liblist.pm
%{privlib}/ExtUtils/MakeMaker/
%{privlib}/ExtUtils/MakeMaker.pm
%{privlib}/ExtUtils/MM*.pm
%{privlib}/ExtUtils/MY.pm
%{privlib}/ExtUtils/Mkbootstrap.pm
%{privlib}/ExtUtils/Mksymlists.pm
%{privlib}/ExtUtils/testlib.pm
%{_mandir}/man1/instmodsh.1*
%{_mandir}/man3/ExtUtils.Command.MM*
%{_mandir}/man3/ExtUtils.Liblist.3*
%{_mandir}/man3/ExtUtils.MM*
%{_mandir}/man3/ExtUtils.MY.3*
%{_mandir}/man3/ExtUtils.MakeMaker*
%{_mandir}/man3/ExtUtils.Mkbootstrap.3*
%{_mandir}/man3/ExtUtils.Mksymlists.3*
%{_mandir}/man3/ExtUtils.testlib.3*

%files ExtUtils-ParseXS
%dir %{privlib}/ExtUtils/ParseXS/
%dir %{privlib}/ExtUtils/Typemaps/
%{privlib}/ExtUtils/ParseXS.pm
%{privlib}/ExtUtils/ParseXS.pod
%{privlib}/ExtUtils/ParseXS/Constants.pm
%{privlib}/ExtUtils/ParseXS/CountLines.pm
%{privlib}/ExtUtils/ParseXS/Utilities.pm
%{privlib}/ExtUtils/Typemaps.pm
%{privlib}/ExtUtils/Typemaps/Cmd.pm
%{privlib}/ExtUtils/Typemaps/InputMap.pm
%{privlib}/ExtUtils/Typemaps/OutputMap.pm
%{privlib}/ExtUtils/Typemaps/Type.pm
%{privlib}/ExtUtils/xsubpp
%{_bindir}/xsubpp
%{_mandir}/man1/xsubpp*
%{_mandir}/man3/ExtUtils.ParseXS.3*
%{_mandir}/man3/ExtUtils.ParseXS.Constants.3*
%{_mandir}/man3/ExtUtils.ParseXS.Utilities.3*
%{_mandir}/man3/ExtUtils.Typemaps.3*
%{_mandir}/man3/ExtUtils.Typemaps.Cmd.3*
%{_mandir}/man3/ExtUtils.Typemaps.InputMap.3*
%{_mandir}/man3/ExtUtils.Typemaps.OutputMap.3*
%{_mandir}/man3/ExtUtils.Typemaps.Type.3*

%files File-Fetch
%{privlib}/File/Fetch.pm
%{_mandir}/man3/File.Fetch.3*

%files Filter
%{archlib}/auto/Filter/Util
%exclude %{archlib}/auto/Filter/Util/Call/*.dbg
%{archlib}/Filter/Util
%{privlib}/Pod/perlfilter.pod
%{_mandir}/man1/perlfilter.*
%{_mandir}/man3/Filter.Util.*

%files IO-Compress
# IO-Compress
%{_bindir}/zipdetails
%{privlib}/IO/Compress/FAQ.pod
%{_mandir}/man1/zipdetails.*
%{_mandir}/man3/IO.Compress.FAQ.*
# Compress-Zlib
%{privlib}/Compress/Zlib.pm
%{_mandir}/man3/Compress.Zlib*
#IO-Compress-Base
%{privlib}/File/GlobMapper.pm
%{privlib}/IO/Compress/Base/
%{privlib}/IO/Compress/Base.pm
%{privlib}/IO/Uncompress/AnyUncompress.pm
%{privlib}/IO/Uncompress/Base.pm
%{_mandir}/man3/File.GlobMapper.*
%{_mandir}/man3/IO.Compress.Base.*
%{_mandir}/man3/IO.Uncompress.AnyUncompress.*
%{_mandir}/man3/IO.Uncompress.Base.*

# IO-Compress-Zlib
%{privlib}/IO/Compress/Adapter/
%{privlib}/IO/Compress/Deflate.pm
%{privlib}/IO/Compress/Bzip2.pm
%{privlib}/IO/Compress/Gzip/
%{privlib}/IO/Compress/Gzip.pm
%{privlib}/IO/Compress/RawDeflate.pm
%{privlib}/IO/Compress/Zip/
%{privlib}/IO/Compress/Zip.pm
%{privlib}/IO/Compress/Zlib/
%{privlib}/IO/Uncompress/Adapter/
%{privlib}/IO/Uncompress/AnyInflate.pm
%{privlib}/IO/Uncompress/Bunzip2.pm
%{privlib}/IO/Uncompress/Gunzip.pm
%{privlib}/IO/Uncompress/Inflate.pm
%{privlib}/IO/Uncompress/RawInflate.pm
%{privlib}/IO/Uncompress/Unzip.pm
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

%files IO-Zlib
%{privlib}/IO/Zlib.pm
%{_mandir}/man3/IO.Zlib.*

%files HTTP-Tiny
%{privlib}/HTTP/Tiny.pm
%{_mandir}/man3/HTTP.Tiny*

%files IPC-Cmd
%{privlib}/IPC/Cmd.pm
%{_mandir}/man3/IPC.Cmd.3*

%files JSON-PP
%{_bindir}/json_pp
%{privlib}/JSON/PP
%{privlib}/JSON/PP.pm
%{_mandir}/man1/json_pp.1*
%{_mandir}/man3/JSON.PP.3*
%{_mandir}/man3/JSON.PP.Boolean.3pm*

%files Locale-Codes
%{privlib}/Locale/Codes
%{privlib}/Locale/Codes.*
%{privlib}/Locale/Country.*
%{privlib}/Locale/Currency.*
%{privlib}/Locale/Language.*
%{privlib}/Locale/Script.*
%{_mandir}/man3/Locale.Codes.*
%{_mandir}/man3/Locale.Country.*
%{_mandir}/man3/Locale.Currency.*
%{_mandir}/man3/Locale.Language.*
%{_mandir}/man3/Locale.Script.*

%files Locale-Maketext-Simple
%{privlib}/Locale/Maketext/Simple.pm
%{_mandir}/man3/Locale.Maketext.Simple.*

%files Log-Message
%{privlib}/Log/Message.pm
%{privlib}/Log/Message/Config.pm
%{privlib}/Log/Message/Handlers.pm
%{privlib}/Log/Message/Item.pm
%{_mandir}/man3/Log.Message.3*
%{_mandir}/man3/Log.Message.Config.3*
%{_mandir}/man3/Log.Message.Handlers.3*
%{_mandir}/man3/Log.Message.Item.3*

%files Log-Message-Simple
%{privlib}/Log/Message/Simple.pm
%{_mandir}/man3/Log.Message.Simple.3*

%files Module-Build
%{_bindir}/config_data
%{privlib}/inc/
%{privlib}/Module/Build/
%{privlib}/Module/Build.pm
%{_mandir}/man1/config_data.1*
%{_mandir}/man3/Module.Build*
%{_mandir}/man3/inc.latest.3*

%files Module-CoreList
%{_bindir}/corelist
%{privlib}/Module/CoreList.pm
%{_mandir}/man1/corelist*
%{_mandir}/man3/Module.CoreList*

%files Module-Load
%{privlib}/Module/Load.pm
%{_mandir}/man3/Module.Load.*
%exclude %{_mandir}/man3/Module.Load.Conditional*

%files Module-Load-Conditional
%{privlib}/Module/Load/
%{_mandir}/man3/Module.Load.Conditional*

%files Module-Loaded
%dir %{privlib}/Module/
%{privlib}/Module/Loaded.pm
%{_mandir}/man3/Module.Loaded*

%files Module-Metadata
%{privlib}/Module/Metadata.pm
%{_mandir}/man3/Module.Metadata.3pm*

%files Module-Pluggable
%{privlib}/Devel/InnerPackage.pm
%{privlib}/Module/Pluggable/
%{privlib}/Module/Pluggable.pm
%{_mandir}/man3/Devel.InnerPackage*
%{_mandir}/man3/Module.Pluggable*

%files Object-Accessor
%{privlib}/Object/
%{_mandir}/man3/Object.Accessor*

%files Package-Constants
%{privlib}/Package/
%{_mandir}/man3/Package.Constants*

%files PathTools
%{archlib}/Cwd.pm
%{archlib}/File/Spec*
%{archlib}/auto/Cwd/
%exclude %{archlib}/auto/Cwd/*.dbg
%{_mandir}/man3/Cwd*
%{_mandir}/man3/File.Spec*

%files Params-Check
%{privlib}/Params/
%{_mandir}/man3/Params.Check*

%files Parse-CPAN-Meta
%dir %{privlib}/Parse/
%dir %{privlib}/Parse/CPAN/
%{privlib}/Parse/CPAN/Meta.pm
%{_mandir}/man3/Parse.CPAN.Meta.3*

%files parent
%{privlib}/parent.pm
%{_mandir}/man3/parent.3*

%files Perl-OSType
%{privlib}/Perl/OSType.pm
%{_mandir}/man3/Perl.OSType.3pm*

%files Pod-Escapes
%{privlib}/Pod/Escapes.pm
%{_mandir}/man3/Pod.Escapes.*

%files Pod-Parser
%{_bindir}/pod2usage
%{_bindir}/podchecker
%{_bindir}/podselect
%{privlib}/Pod/Checker.pm
%{privlib}/Pod/Find.pm
%{privlib}/Pod/InputObjects.pm
%{privlib}/Pod/ParseUtils.pm
%{privlib}/Pod/Parser.pm
%{privlib}/Pod/PlainText.pm
%{privlib}/Pod/Select.pm
%{privlib}/Pod/Usage.pm
%{_mandir}/man1/pod2usage.1*
%{_mandir}/man1/podchecker.1*
%{_mandir}/man1/podselect.1*
%{_mandir}/man3/Pod.Checker.*
%{_mandir}/man3/Pod.Find.*
%{_mandir}/man3/Pod.InputObjects.*
%{_mandir}/man3/Pod.ParseUtils.*
%{_mandir}/man3/Pod.Parser.*
%{_mandir}/man3/Pod.PlainText.*
%{_mandir}/man3/Pod.Select.*
%{_mandir}/man3/Pod.Usage.*

%files Pod-Perldoc
%{_bindir}/perldoc
%{privlib}/Pod/perldoc.pod
%{privlib}/Pod/Perldoc.pm
%{privlib}/Pod/Perldoc/
%{_mandir}/man1/perldoc.1*
%{_mandir}/man3/Pod.Perldoc*

%files Pod-Simple
%{privlib}/Pod/Simple/
%{privlib}/Pod/Simple.pm
%{privlib}/Pod/Simple.pod
%{_mandir}/man3/Pod.Simple*

%files Scalar-List-Utils
%{archlib}/List/
%{archlib}/Scalar/
%{archlib}/auto/List/
%exclude %{archlib}/auto/List/Util/*.dbg
%{_mandir}/man3/List.Util*
%{_mandir}/man3/Scalar.Util*

%files Socket
%dir %{archlib}/auto/Socket
%{archlib}/auto/Socket/
%exclude %{archlib}/auto/Socket/*.dbg
%{archlib}/Socket.pm
%{_mandir}/man3/Socket.3*

%files Term-UI
%{privlib}/Term/UI/
%{privlib}/Term/UI.pm
%{_mandir}/man3/Term.UI*

%files Test-Harness
%{_bindir}/prove
%{privlib}/App*
%{privlib}/TAP*
%{privlib}/Test/Harness*
%{_mandir}/man1/prove.1*
%{_mandir}/man3/App*
%{_mandir}/man3/TAP*
%{_mandir}/man3/Test.Harness*

%files Test-Simple
%{privlib}/Test/More*
%{privlib}/Test/Builder*
%{privlib}/Test/Simple*
%{privlib}/Test/Tutorial*
%{_mandir}/man3/Test.More*
%{_mandir}/man3/Test.Builder*
%{_mandir}/man3/Test.Simple*
%{_mandir}/man3/Test.Tutorial*

%files Test-Simple-tests
%dir %{perl5_testdir}
#{perl5_testdir}/Test-Simple

%files Time-Piece
%{archlib}/Time/Piece.pm
%{archlib}/Time/Seconds.pm
%{archlib}/auto/Time/Piece/
%exclude %{archlib}/auto/Time/Piece/*.dbg
%{_mandir}/man3/Time.Piece.3*
%{_mandir}/man3/Time.Seconds.3*

%files Version-Requirements
%{privlib}/version/Requirements.pm
%{_mandir}/man3/version.Requirements.3*

%files threads
%dir %{archlib}/auto/threads
%{archlib}/auto/threads/thread*
%exclude %{archlib}/auto/threads/thread*.dbg
%{archlib}/threads.pm
%{_mandir}/man3/threads.3*

%files threads-shared
%{archlib}/auto/threads/shared/
%exclude %{archlib}/auto/threads/shared/*.dbg
%dir %{archlib}/threads
%{archlib}/threads/shared*
%{_mandir}/man3/threads.shared*

%files version
%{privlib}/version.pm
%{privlib}/version.pod
%{privlib}/version/
%exclude %{privlib}/version/Requirements.pm
%{_mandir}/man3/version.3*
%{_mandir}/man3/version.Internals.3*

%files core
# Nothing. Nada. Zilch. Zarro. Uh uh. Nope. Sorry.

%changelog
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
