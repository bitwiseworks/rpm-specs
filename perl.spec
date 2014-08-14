%global perl_version    5.16.1
%global perl_epoch      0
%global perl_arch_stem -thread-multi
%global perl_archname %{_arch}-%{_os}%{perl_arch_stem}

%global multilib_64_archs x86_64 s390x ppc64 sparc64
%global parallel_tests 1
%global tapsetdir   %{_datadir}/systemtap/tapset

# internal filter just for this spec
# XXX: %%global expands now, archlib must be pre-defined.
%global perl_default_filter %%{?filter_setup: %%{expand: \
%%filter_provides_in -P %%{archlib}/(?!CORE/libperl).*\\.so$ \
%%filter_setup \
}}

# same as we provide in /etc/rpm/macros.perl
%global perl5_testdir   %{_libexecdir}/perl5-tests

Name:           perl
Version:        %{perl_version}
# release number must be even higher, becase dual-lived modules will be broken otherwise
Release:        1%{?dist}
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
Source0:        http://www.cpan.org/src/5.0/perl-%{perl_version}.tar.gz

Patch1:         perl-os2.patch

# Update some of the bundled modules
# see http://fedoraproject.org/wiki/Perl/perl.spec for instructions

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:  db4-devel, zlib-devel
#BuildRequires:  gdbm-devel, groff, tcsh, systemtap-sdt-devel
# For tests
#BuildRequires:  procps, rsyslog

# The long line of Perl provides.

# These provides are needed by the perl pkg itself with auto-generated perl.req
Provides: perl(VMS::Filespec)
Provides: perl(VMS::Stdio)

# Compat provides
Provides: perl(:MODULE_COMPAT_5.12.4)
Provides: perl(:MODULE_COMPAT_5.12.3)
Provides: perl(:MODULE_COMPAT_5.12.2)
Provides: perl(:MODULE_COMPAT_5.12.1)
Provides: perl(:MODULE_COMPAT_5.12.0)

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
Provides: perl(syslog.pl)
Provides: perl(tainted.pl)
Provides: perl(termcap.pl)
Provides: perl(timelocal.pl)
Provides: perl(utf8_heavy.pl)
Provides: perl(validate.pl)
Provides: perl(Carp::Heavy)

# Long history in 3rd-party repositories:
Provides: perl-File-Temp = 0.22 
Obsoletes: perl-File-Temp < 0.20

# suidperl isn't created by upstream since 5.12.0
Obsoletes: perl-suidperl <= 4:5.12.2

Requires: perl-libs = %{perl_epoch}:%{perl_version}-%{release}

# We need this to break the dependency loop, and ensure that perl-libs 
# gets installed before perl.
Requires(post): perl-libs


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
#Requires:       systemtap-sdt-devel
Requires:       perl(ExtUtils::ParseXS)
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}

%description devel
This package contains header files and development modules.
Most perl packages will need to install perl-devel to build.

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
Version:        0.38
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
BuildArch:      noarch
# fix buggy rpm autodetection, remove once rpm is fixed.
Provides: perl(Archive::Extract)

%description Archive-Extract
Archive::Extract is a generic archive extraction mechanism.


%package Archive-Tar
Summary:        A module for Perl manipulation of .tar files
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        1.54 
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
Requires:       perl(Compress::Zlib)
Requires:       perl(IO::Zlib)
BuildArch:      noarch
# fix buggy rpm autodetection, remove once rpm is fixed.
Provides: perl(Archive::Tar)

%description Archive-Tar
Archive::Tar provides an object oriented mechanism for handling tar files.  It
provides class methods for quick and easy files handling while also allowing
for the creation of tar file objects for custom manipulation.  If you have the
IO::Zlib module installed, Archive::Tar will also support compressed or
gzipped tar files.


%package Class-ISA
Summary:        Report the search path for a class's ISA tree
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        0.36
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
BuildArch:      noarch
# fix buggy rpm autodetection, remove once rpm is fixed.
Provides: perl(Class::ISA)

%description Class-ISA
Suppose you have a class (like Food::Fish::Fishstick) that is derived, via
its @ISA, from one or more superclasses (as Food::Fish::Fishstick is from
Food::Fish, Life::Fungus, and Chemicals), and some of those superclasses
may themselves each be derived, via its @ISA, from one or more superclasses
(as above).


%package CGI
Summary:        Handle Common Gateway Interface requests and responses
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        3.49
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
BuildArch:      noarch
# fix buggy rpm autodetection, remove once rpm is fixed.
Provides: perl(CGI)

%description CGI
CGI.pm is a stable, complete and mature solution for processing and preparing
HTTP requests and responses. Major features including processing form
submissions, file uploads, reading and writing cookies, query string generation
and manipulation, and processing and preparing HTTP headers. Some HTML
generation utilities are included as well.

CGI.pm performs very well in in a vanilla CGI.pm environment and also comes
with built-in support for mod_perl and mod_perl2 as well as FastCGI.


%package Compress-Raw-Zlib
Summary:        Low-Level Interface to the zlib compression library
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        2.024
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
# fix buggy rpm autodetection, remove once rpm is fixed.
Provides: perl(Compress::Raw::Zlib)

%description Compress-Raw-Zlib
This module provides a Perl interface to the zlib compression library.
It is used by IO::Compress::Zlib.


%package CPAN
Summary:        Query, download and build perl modules from CPAN sites
Group:          Development/Languages
License:        GPL+ or Artistic
Epoch:          0
Version:        1.9402
# CPAN encourages Digest::SHA strongly because of integrity checks
Requires:       perl(Digest::SHA)
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
Provides:       cpan = %{version}
BuildArch:      noarch
# fix buggy rpm autodetection, remove once rpm is fixed.
Provides: perl(CPAN)
Requires: perl(PathTools), perl(ExtUtils::MakeMaker), perl(Scalar::List::Utils)

%description CPAN
Query, download and build perl modules from CPAN sites.


%package CPANPLUS
Summary:        API & CLI access to the CPAN mirrors
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        0.90
# CPANPLUS encourages Digest::SHA strongly because of integrity checks
Requires:       perl(Digest::SHA)
Requires:       perl(Module::Pluggable) >= 2.4
Requires:       perl(Module::CoreList)
#Requires:       perl(DBIx::Simple)
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
Provides:       perl-CPANPLUS-Dist-Build = 0.06
Obsoletes:      perl-CPANPLUS-Dist-Build <= 0.05
BuildArch:      noarch
# fix buggy rpm autodetection, remove once rpm is fixed.
Provides: perl(CPANPLUS)

%description CPANPLUS
The CPANPLUS library is an API to the CPAN mirrors and a collection of
interactive shells, commandline programs, etc, that use this API.


%package Digest-SHA
Summary:        Perl extension for SHA-1/224/256/384/512
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        5.47
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
# fix buggy rpm autodetection, remove once rpm is fixed.
Provides: perl(Digest::SHA)

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
Version:        0.27
Requires:       perl-devel
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
BuildArch:      noarch
# fix buggy rpm autodetection, remove once rpm is fixed.
Provides: perl(ExtUtils::CBuilder)

%description ExtUtils-CBuilder
This module can build the C portions of Perl modules by invoking the
appropriate compilers and linkers in a cross-platform manner. It was motivated
by the Module::Build project, but may be useful for other purposes as well.


%package ExtUtils-Embed
Summary:        Utilities for embedding Perl in C/C++ applications
Group:          Development/Languages
License:        GPL+ or Artistic
Epoch:          0
Version:        1.28
Requires:       perl-devel
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
BuildArch:      noarch
# fix buggy rpm autodetection, remove once rpm is fixed.
Provides: perl(ExtUtils::Embed)

%description ExtUtils-Embed
Utilities for embedding Perl in C/C++ applications.


%package ExtUtils-MakeMaker
Summary:        Create a module Makefile
Group:          Development/Languages
License:        GPL+ or Artistic
Epoch:          0
Version:        6.56
Requires:       perl-devel
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
Requires:       perl(Test::Harness)
BuildArch:      noarch
# fix buggy rpm autodetection, remove once rpm is fixed.
Provides: perl(ExtUtils::MakeMaker)

%description ExtUtils-MakeMaker
Create a module Makefile.


%package ExtUtils-ParseXS
Summary:        Module and a script for converting Perl XS code into C code
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
# We must preserve 4-digit precison since 2.2002 version
%global         ExtUtils_ParseXS_real_version 2.22
%global         ExtUtils_ParseXS_version %{ExtUtils_ParseXS_real_version}06
Version:        %{ExtUtils_ParseXS_version}
Requires:       perl-devel
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
BuildArch:      noarch
Provides:       perl(ExtUtils::ParseXS) = %{ExtUtils_ParseXS_version}

%description ExtUtils-ParseXS
ExtUtils::ParseXS will compile XS code into C code by embedding the constructs
necessary to let C functions manipulate Perl values and creates the glue
necessary to let Perl access those functions.


%package File-Fetch
Summary:        Generic file fetching mechanism
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        0.24 
Requires:       perl(IPC::Cmd) >= 0.36
Requires:       perl(Module::Load::Conditional) >= 0.04
Requires:       perl(Params::Check) >= 0.07
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
BuildArch:      noarch
# fix buggy rpm autodetection, remove once rpm is fixed.
Provides: perl(File::Fetch)

%description File-Fetch
File::Fetch is a generic file fetching mechanism.


%package IO-Compress
Summary:        IO::Compress wrapper for modules
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        2.026
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
Obsoletes:      perl-Compress-Zlib <= 2.020
Provides:       perl(IO::Uncompress::Bunzip2)
Provides:       perl(Compress::Zlib)
# fix buggy rpm autodetection, remove once rpm is fixed.
Provides: perl(IO::Compress)

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
# fix buggy rpm autodetection, remove once rpm is fixed.
Provides: perl(IO::Zlib)

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
Version:        0.54
Requires:       perl(ExtUtils::MakeMaker)
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
BuildArch:      noarch
# fix buggy rpm autodetection, remove once rpm is fixed.
Provides: perl(IPC::Cmd)

%description IPC-Cmd
IPC::Cmd allows you to run commands, interactively if desired, in a platform
independent way, but have them still work.


%package Locale-Maketext-Simple
Summary:        Simple interface to Locale::Maketext::Lexicon
Group:          Development/Libraries
License:        MIT
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        0.21
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
BuildArch:      noarch
# fix buggy rpm autodetection, remove once rpm is fixed.
Provides: perl(Locale::Maketext::Simple)

%description Locale-Maketext-Simple
This module is a simple wrapper around Locale::Maketext::Lexicon, designed
to alleviate the need of creating Language Classes for module authors.


%package Log-Message
Summary:        Generic message storage mechanism
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        0.02
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
# Add a versioned provides, since we pull the unversioned one out.
Provides:       perl(Log::Message::Handlers) = %{version}
BuildArch:      noarch
# fix buggy rpm autodetection, remove once rpm is fixed.
Provides: perl(Log::Message)

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
Version:        0.06
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
BuildArch:      noarch
# fix buggy rpm autodetection, remove once rpm is fixed.
Provides: perl(Log::Message::Simple)

%description Log-Message-Simple
This module provides standardized logging facilities using the
Log::Message module.


%package Module-Build
Summary:        Perl module for building and installing Perl modules
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        0.3603 
Requires:       perl(Archive::Tar) >= 1.08
Requires:       perl(ExtUtils::CBuilder) >= 0.15
Requires:       perl(ExtUtils::ParseXS) >= 1.02
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
BuildArch:      noarch
# fix buggy rpm autodetection, remove once rpm is fixed.
Provides: perl(Module::Build)

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
Epoch:          0
Version:        2.50 
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
#Requires:       perl(version)
BuildArch:      noarch
# fix buggy rpm autodetection, remove once rpm is fixed.
Provides: perl(Module::CoreList)

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
Version:        0.16
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
BuildArch:      noarch
# fix buggy rpm autodetection, remove once rpm is fixed.
Provides: perl(Module::Load)

%description Module-Load
Module::Load eliminates the need to know whether you are trying to require
either a file or a module.


%package Module-Load-Conditional
Summary:        Looking up module information / loading at runtime
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        0.34
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
BuildArch:      noarch
# fix buggy rpm autodetection, remove once rpm is fixed.
Provides: perl(Module::Load::Conditional)

%description Module-Load-Conditional
Module::Load::Conditional provides simple ways to query and possibly load any
of the modules you have installed on your system during runtime.


%package Module-Loaded
Summary:        Mark modules as loaded or unloaded
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        0.06
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
BuildArch:      noarch
# fix buggy rpm autodetection, remove once rpm is fixed.
Provides: perl(Module::Loaded)

%description Module-Loaded
When testing applications, often you find yourself needing to provide
functionality in your test environment that would usually be provided by
external modules. Rather than munging the %INC by hand to mark these external
modules as loaded, so they are not attempted to be loaded by perl, this module
offers you a very simple way to mark modules as loaded and/or unloaded.


%package Module-Pluggable
Summary:        Automatically give your module the ability to have plugins
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        3.90 
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
BuildArch:      noarch
# fix buggy rpm autodetection, remove once rpm is fixed.
Provides: perl(Module::Pluggable)

%description Module-Pluggable
Provides a simple but, hopefully, extensible way of having 'plugins' for your
module.


%package Object-Accessor
Summary:        Perl module that allows per object accessors
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        0.36
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
BuildArch:      noarch
# fix buggy rpm autodetection, remove once rpm is fixed.
Provides: perl(Object::Accessor)

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
# fix buggy rpm autodetection, remove once rpm is fixed.
Provides: perl(Package::Constants)

%description Package-Constants
Package::Constants lists all the constants defined in a certain package.  This
can be useful for, among others, setting up an autogenerated @EXPORT/@EXPORT_OK
for a Constants.pm file.


%package PathTools
Summary:        PathTools Perl module (Cwd, File::Spec)
Group:          Development/Libraries
License:        (GPL+ or Artistic) and BSD
Epoch:          0
Version:        3.31
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
# fix buggy rpm autodetection, remove once rpm is fixed.
Provides: perl(PathTools)

%description PathTools
PathTools Perl module (Cwd, File::Spec).


%package Params-Check
Summary:        Generic input parsing/checking mechanism
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        0.26
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
BuildArch:      noarch
# fix buggy rpm autodetection, remove once rpm is fixed.
Provides: perl(Params::Check)

%description Params-Check
Params::Check is a generic input parsing/checking mechanism.


%package Parse-CPAN-Meta
Summary:        Parse META.yml and other similar CPAN metadata files
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        1.40
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
BuildArch:      noarch
# FIXME it could be removed now?
Obsoletes:      perl-Parse-CPAN-Meta < 1.40
# fix buggy rpm autodetection, remove once rpm is fixed.
Provides: perl(Parse::CPAN::Meta)

%description Parse-CPAN-Meta 
Parse::CPAN::Meta is a parser for META.yml files, based on the parser half of
YAML::Tiny.


%package Pod-Escapes
Summary:        Perl module for resolving POD escape sequences
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        1.04
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
BuildArch:      noarch
# fix buggy rpm autodetection, remove once rpm is fixed.
Provides: perl(Pod::Escapes)

%description Pod-Escapes
This module provides things that are useful in decoding Pod E<...> sequences.
Presumably, it should be used only by Pod parsers and/or formatters.


%package Pod-Simple
Summary:        Framework for parsing POD documentation
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        3.13
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
BuildArch:      noarch
# fix buggy rpm autodetection, remove once rpm is fixed.
Provides: perl(Pod::Simple)

%description Pod-Simple
Pod::Simple is a Perl library for parsing text in the Pod ("plain old
documentation") markup language that is typically used for writing
documentation for Perl and for Perl modules.

%package Scalar-List-Utils
Summary:        A selection of general-utility scalar and list subroutines
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        1.22
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
# fix buggy rpm autodetection, remove once rpm is fixed.
Provides: perl(Scalar::List::Utils)

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
Version:        0.20
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
Requires:       perl(Log::Message::Simple)
BuildArch:      noarch
# fix buggy rpm autodetection, remove once rpm is fixed.
Provides: perl(Term::UI)

%description Term-UI
Term::UI is a transparent way of eliminating the overhead of having to format
a question and then validate the reply, informing the user if the answer was not
proper and re-issuing the question.


%package Test-Harness
Summary:        Run Perl standard test scripts with statistics
Group:          Development/Languages
License:        GPL+ or Artistic
Epoch:          0
Version:        3.17
Requires:       perl-devel
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
BuildArch:      noarch
# Use rewritten module perl-Test-Harness
Provides:       perl-TAP-Harness = 3.17
Obsoletes:      perl-TAP-Harness < 3.10
# fix buggy rpm autodetection, remove once rpm is fixed.
Provides: perl(Test::Harness)

%description Test-Harness
Run Perl standard test scripts with statistics.
Use TAP::Parser, Test::Harness package was whole rewritten.

%package Test-Simple
Summary:        Basic utilities for writing tests
Group:          Development/Languages
License:        GPL+ or Artistic
Epoch:          0
Version:        0.94
Requires:       perl-devel
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
BuildArch:      noarch
# fix buggy rpm autodetection, remove once rpm is fixed.
Provides: perl(Test::Simple)

%description Test-Simple
Basic utilities for writing tests.


%package Test-Simple-tests
Summary:        Test suite for package perl-Test-Simple
Group:          Development/Debug
License:        GPL+ or Artistic
Epoch:          0
Version:        0.94
Requires:       perl-Test-Simple = 0:0.94-%{release}
Requires:       /usr/bin/prove
AutoReqProv:    0
BuildArch:      noarch
# fix buggy rpm autodetection, remove once rpm is fixed.
Provides: perl(Test::Simple::tests)

%description Test-Simple-tests
This package provides the test suite for package perl-Test-Simple.


%package Time-Piece
Summary:        Time objects from localtime and gmtime
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        1.15
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
# fix buggy rpm autodetection, remove once rpm is fixed.
Provides: perl(Time::Piece)

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
Version:        0.223
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


%package threads
Summary:        Perl interpreter-based threads
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        1.75
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
Version:        1.32
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
Version:        0.82
Requires:       perl = %{perl_epoch}:%{perl_version}-%{release}
BuildArch:      noarch

%description version
Perl extension for Version Objects


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

Requires:       perl-Archive-Extract, perl-Archive-Tar, perl-Class-ISA,
Requires:       perl-Compress-Raw-Zlib, perl-CGI, perl-CPAN,
Requires:       perl-CPANPLUS, perl-Digest-SHA, perl-ExtUtils-CBuilder,
Requires:       perl-ExtUtils-Embed, perl-ExtUtils-MakeMaker, perl-ExtUtils-ParseXS,
Requires:       perl-File-Fetch, perl-IO-Compress, perl-IO-Zlib,
Requires:       perl-IPC-Cmd, perl-Locale-Maketext-Simple, perl-Log-Message, perl-Log-Message-Simple,
Requires:       perl-Module-Build, perl-Module-CoreList, perl-Module-Load,
Requires:       perl-Module-Load-Conditional, perl-Module-Loaded,
Requires:       perl-Module-Pluggable, perl-Object-Accessor, perl-Package-Constants, perl-PathTools
Requires:       perl-Params-Check, perl-Pod-Escapes, perl-Pod-Simple, perl-Scalar-List-Utils, perl-Term-UI
Requires:       perl-Test-Harness, perl-Test-Simple, perl-Time-Piece, perl-version
Requires:       perl-threads, perl-threads-shared, perl-parent, perl-Parse-CPAN-Meta

%description core
A metapackage which requires all of the perl bits and modules in the upstream
tarball from perl.org.


%package debug
Summary: HLL debug data for exception handling support.

%description debug
HLL debug data for exception handling support.


%{?perl_default_filter}
%prep
%setup -q -n perl-%{perl_version}
%patch1 -p1

attrib -s -h -r "*" /s

find . -name \*.orig -exec rm -fv {} \;

# Oh, the irony. Perl generates some non-versioned provides we don't need.
# Each of these has a versioned provide, which we keep.
%{?filter_setup:
%filter_from_provides /^perl(Carp)$/d
%filter_from_provides /^perl(DynaLoader)$/d
%filter_from_provides /^perl(Locale::Maketext)$/d
%filter_from_provides /^perl(Log::Message::Handlers)$/d
%filter_from_provides /^perl(Math::BigInt)$/d
%filter_from_provides /^perl(Net::Config)$/d 
%filter_from_provides /^perl(POSIX)$/d 
%filter_from_provides /^perl(Storable)$/d
%filter_from_provides /^perl(Tie::Hash)$/d
%filter_from_provides /^perl(bigint)$/d
%filter_from_provides /^perl(bigrat)$/d
%filter_from_provides /^perl(bytes)$/d 
%filter_from_provides /^perl(utf8)$/d 
%filter_from_provides /^perl(DB)$/d
# Filter the automatically generated dependencies.
%filter_from_requires /^perl(FCGI)/d
%filter_from_requires /^perl(Mac::/d
%filter_from_requires /^perl(Tk)/d
%filter_from_requires /^perl(Tk::/d
%filter_from_requires /^perl(Your::Module::Here)/d
# Filter less specific versions
%filter_from_provides /^perl(ExtUtils::ParseXS) = %{ExtUtils_ParseXS_real_version}$/d
%?perl_default_filter
}

# Configure Compress::Zlib to use system zlib
sed -i 's|BUILD_ZLIB      = True|BUILD_ZLIB      = False|
    s|INCLUDE         = ./zlib-src|INCLUDE         = %{_includedir}|
    s|LIB             = ./zlib-src|LIB             = %{_libdir}|' \
    cpan/Compress-Raw-Zlib/config.in

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

export CONFIG_SHELL="/@unixroot/usr/bin/sh.exe"
export LANG=""

sh Configure -des -Doptimize="$RPM_OPT_FLAGS" \
        -DDEBUGGING=-g \
        -Dversion=%{perl_version} \
        -Dmyhostname=localhost \
        -Dperladmin=root@localhost \
        -Dcc='%{__cc}' \
        -Dsh='/@unixroot/usr/bin/sh.exe' \
        -Dsed='sed' \
        -Dln='ln' \
        -Dcf_by='Netlabs.org' \
        -Dprefix=%{_prefix} \
        -Dvendorprefix=%{_prefix} \
        -Dsiteprefix=%{_prefix}/local \
        -Dsitelib="%{_prefix}/local/share/perl5" \
        -Dsitearch="%{_prefix}/local/%{_lib}/perl5" \
        -Dprivlib="%{privlib}" \
        -Dvendorlib="%{perl_vendorlib}" \
        -Darchlib="%{archlib}" \
        -Dvendorarch="%{perl_vendorarch}" \
%ifarch %{multilib_64_archs}
        -Dlibpth="/usr/local/lib64 /lib64 %{_prefix}/lib64" \
%endif
%ifarch sparc sparcv9
        -Ud_longdbl \
%endif
        -Duseshrplib \
        -Duselargefiles \
        -Dman3ext=3pm \
        -Duseperlio \
        -Dinstallusrbinperl=n \
        -Ubincompat5005 \
        -Uversiononly \
        -Dpager='/@unixroot/usr/bin/less -isr' \
        -Dd_gethostent_r_proto -Ud_endhostent_r_proto -Ud_sethostent_r_proto \
        -Ud_endprotoent_r_proto -Ud_setprotoent_r_proto \
        -Ud_endservent_r_proto -Ud_setservent_r_proto \
        -Dscriptdir='%{_bindir}' 

#        -Dd_semctl_semun \
#        -Di_db \
#        -Ui_ndbm \
#        -Di_gdbm \
#        -Di_syslog \
#        -Dccdlflags="-Wl,--enable-new-dtags" \
#        -Di_shadow \
#        -Dusethreads \
#        -Duseithreads \
#        -Darchname=%{perl_archname} \
# -Dusedtrace='/@unixroot/usr/bin/dtrace' \
# -Duseshrplib creates libperl.so, -Ubincompat5005 help create DSO -> libperl.so

# fix /@unixroot paths
sed -i 's#.:/usr#/@unixroot/usr#gi' config.sh
sed -i 's#.:/mptn#/@bootroot/mptn#gi' config.sh

make os2.o
perl make_patchnum.pl
# SMP build not working
make

%install
rm -rf $RPM_BUILD_ROOT

# YD install only binaries, man pages are failing.
./perl installperl --destdir=$RPM_BUILD_ROOT

# symlink main executable for rpm scripts
ln -s %{_bindir}/perl.exe %{buildroot}%{_bindir}/perl

%global build_archlib $RPM_BUILD_ROOT%{archlib}
%global build_privlib $RPM_BUILD_ROOT%{privlib}
%global build_bindir  $RPM_BUILD_ROOT%{_bindir}
%global new_perl LD_PRELOAD="%{build_archlib}/CORE/libperl.so" \\\
    LD_LIBRARY_PATH="%{build_archlib}/CORE" \\\
    PERL5LIB="%{build_archlib}:%{build_privlib}" \\\
    %{build_bindir}/perl

#install -p -m 755 utils/pl2pm %{build_bindir}/pl2pm

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
# libnet configuration file
#
#install -p -m 644 %{SOURCE2} %{build_privlib}/Net/libnet.cfg

#
# perl RPM macros
#
#mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/rpm
#install -p -m 644 %{SOURCE3} ${RPM_BUILD_ROOT}%{_sysconfdir}/rpm/

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

# Fix some manpages to be UTF-8
#mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1/
#pushd $RPM_BUILD_ROOT%{_mandir}/man1/
#  for i in perl588delta.1 perldelta.1 ; do
#    iconv -f MS-ANSI -t UTF-8 $i --output new-$i
#    rm $i
#    mv new-$i $i
#  done
#popd

# for now, remove Bzip2:
find $RPM_BUILD_ROOT -name Bzip2 | xargs rm -r
find $RPM_BUILD_ROOT -name '*B*zip2*'| xargs rm

# tests -- FIXME need to validate that this all works as expected
mkdir -p %{buildroot}%{perl5_testdir}/perl-tests

# "core"
tar -cf - t/ | ( cd %{buildroot}%{perl5_testdir}/perl-tests && tar -xf - )

# "dual-lifed"
for dir in `find ext/ -type d -name t -maxdepth 2` ; do

    tar -cf - $dir | ( cd %{buildroot}%{perl5_testdir}/perl-tests/t && tar -xf - )
done

# Selected "Dual-lifed cpan" packages
#pushd cpan
#for package in Test-Simple; do
#    for dir in `find ${package} -type d -name t -maxdepth 2` ; do
#        tar -cf - $dir | ( cd %{buildroot}%{perl5_testdir} && tar -xf - )
#    done
#done
#popd

# Systemtap tapset install
mkdir -p %{buildroot}%{tapsetdir}
%ifarch %{multilib_64_archs}
%global libperl_stp libperl%{perl_version}-64.stp
%else
%global libperl_stp libperl%{perl_version}-32.stp
%endif

#sed \
#  -e "s|LIBRARY_PATH|%{archlib}/CORE/libperl.so|" \
#  %{SOURCE4} \
#  > %{buildroot}%{tapsetdir}/%{libperl_stp}

# TODO: Canonicalize test files (rewrite intrerpreter path, fix permissions)
# XXX: We cannot rewrite ./perl before %%check phase. Otherwise the test
# would run against system perl at build-time.
# See __spec_check_pre global macro in macros.perl.
#T_FILES=`find %%{buildroot}%%{perl5_testdir} -type f -name '*.t'`
#%%fix_shbang_line $T_FILES
#%%{__chmod} +x $T_FILES
#%%{_fixperms} %%{buildroot}%%{perl5_testdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Artistic AUTHORS Copying README Changes
## {_mandir}/man1/*.1*
## {_mandir}/man3/*.3*
%{_bindir}/*
%{privlib}
%{archlib}
%{perl_vendorlib}


# libs
#%exclude %{archlib}/CORE/libperl.so
%exclude %{perl_vendorarch}

# devel
%exclude %{_bindir}/enc2xs
#%exclude ## {_mandir}/man1/enc2xs*
%exclude %{privlib}/Encode/
%exclude %{_bindir}/h2xs
#%exclude ## {_mandir}/man1/h2xs*
%exclude %{_bindir}/libnetcfg
#%exclude ## {_mandir}/man1/libnetcfg*
%exclude %{_bindir}/perlivp
#%exclude ## {_mandir}/man1/perlivp*
%exclude %{archlib}/CORE/*.h
#%exclude ## {_mandir}/man1/perlxs*

# Archive-Extract
%exclude %{privlib}/Archive/Extract.pm
#%exclude ## {_mandir}/man3/Archive::Extract.3*

# Archive-Tar
%exclude %{_bindir}/ptar
%exclude %{_bindir}/ptardiff
%exclude %{privlib}/Archive/Tar/
%exclude %{privlib}/Archive/Tar.pm
#%exclude ## {_mandir}/man1/ptar.1*
#%exclude ## {_mandir}/man1/ptardiff.1*
#%exclude ## {_mandir}/man3/Archive::Tar*

# Class-ISA
#%exclude %{privlib}/Class/ISA.pm
#%exclude ## {_mandir}/man3/Class::ISA.3*

# CGI
%exclude %{privlib}/CGI/
%exclude %{privlib}/CGI.pm
#%exclude ## {_mandir}/man3/CGI.3*
#%exclude ## {_mandir}/man3/CGI::*.3*

# CPAN
%exclude %{_bindir}/cpan
%exclude %{privlib}/CPAN/
%exclude %{privlib}/CPAN.pm
#%exclude ## {_mandir}/man1/cpan.1*
#%exclude ## {_mandir}/man3/CPAN.*
#%exclude ## {_mandir}/man3/CPAN:*

# Parse-CPAN-Meta
%exclude %dir %{privlib}/Parse/
%exclude %dir %{privlib}/Parse/CPAN/
%exclude %{privlib}/Parse/CPAN/Meta.pm
#%exclude ## {_mandir}/man3/Parse::CPAN::Meta.3*

# CPANPLUS
%exclude %{_bindir}/cpan2dist
%exclude %{_bindir}/cpanp
%exclude %{_bindir}/cpanp-run-perl
%exclude %{privlib}/CPANPLUS/
%exclude %{privlib}/CPANPLUS.pm
#%exclude ## {_mandir}/man1/cpan2dist.1*
#%exclude ## {_mandir}/man1/cpanp.1*
#%exclude ## {_mandir}/man3/CPANPLUS*

# Compress::Raw::Zlib
%exclude %{archlib}/Compress/Raw/
%exclude %{archlib}/auto/Compress
%exclude %{archlib}/auto/Compress/Raw/
%exclude %{archlib}/auto/Compress/Raw/Zlib/
#%exclude ## {_mandir}/man3/Compress::Raw::Zlib*

# Digest::SHA
%exclude %{_bindir}/shasum
%exclude %{archlib}/Digest/SHA.pm
%exclude %{archlib}/auto/Digest/SHA/
#%exclude ## {_mandir}/man1/shasum.1*
#%exclude ## {_mandir}/man3/Digest::SHA.3*

# ExtUtils::CBuilder
%exclude %{privlib}/ExtUtils/CBuilder/
%exclude %{privlib}/ExtUtils/CBuilder.pm
#%exclude ## {_mandir}/man3/ExtUtils::CBuilder*

# ExtUtils::Embed
%exclude %{privlib}/ExtUtils/Embed.pm
#%exclude ## {_mandir}/man3/ExtUtils::Embed*

# ExtUtils::MakeMaker
%exclude %{_bindir}/instmodsh
%exclude %{privlib}/ExtUtils/Command/
%exclude %{privlib}/ExtUtils/Install.pm
%exclude %{privlib}/ExtUtils/Installed.pm
%exclude %{privlib}/ExtUtils/Liblist/
%exclude %{privlib}/ExtUtils/Liblist.pm
%exclude %{privlib}/ExtUtils/MakeMaker/
%exclude %{privlib}/ExtUtils/MakeMaker.pm
%exclude %{privlib}/ExtUtils/MANIFEST.SKIP
%exclude %{privlib}/ExtUtils/MM*.pm
%exclude %{privlib}/ExtUtils/MY.pm
%exclude %{privlib}/ExtUtils/Manifest.pm
%exclude %{privlib}/ExtUtils/Mkbootstrap.pm
%exclude %{privlib}/ExtUtils/Mksymlists.pm
%exclude %{privlib}/ExtUtils/Packlist.pm
%exclude %{privlib}/ExtUtils/testlib.pm
#%exclude ## {_mandir}/man1/instmodsh.1*
#%exclude ## {_mandir}/man3/ExtUtils::Command::MM*
#%exclude ## {_mandir}/man3/ExtUtils::Install.3*
#%exclude ## {_mandir}/man3/ExtUtils::Installed.3*
#%exclude ## {_mandir}/man3/ExtUtils::Liblist.3*
#%exclude ## {_mandir}/man3/ExtUtils::MM*
#%exclude ## {_mandir}/man3/ExtUtils::MY.3*
#%exclude ## {_mandir}/man3/ExtUtils::MakeMaker*
#%exclude ## {_mandir}/man3/ExtUtils::Manifest.3*
#%exclude ## {_mandir}/man3/ExtUtils::Mkbootstrap.3*
#%exclude ## {_mandir}/man3/ExtUtils::Mksymlists.3*
#%exclude ## {_mandir}/man3/ExtUtils::Packlist.3*
#%exclude ## {_mandir}/man3/ExtUtils::testlib.3*

# ExtUtils::ParseXS
%exclude %{privlib}/ExtUtils/ParseXS.pm
%exclude %{privlib}/ExtUtils/xsubpp
%exclude %{_bindir}/xsubpp
#%exclude ## {_mandir}/man1/xsubpp*
#%exclude ## {_mandir}/man3/ExtUtils::ParseXS.3*

# File::Fetch
%exclude %{privlib}/File/Fetch.pm
#%exclude ## {_mandir}/man3/File::Fetch.3*

# IO::Compress

# Compress::Zlib
%exclude %{privlib}/Compress/Zlib.pm
#%exclude %{archlib}/auto/Compress/Zlib/
#%exclude ## {_mandir}/man3/Compress::Zlib*
# IO::Compress::Base
%exclude %{privlib}/File/GlobMapper.pm
%exclude %{privlib}/IO/Compress/Base/
%exclude %{privlib}/IO/Compress/Base.pm
%exclude %{privlib}/IO/Uncompress/AnyUncompress.pm
%exclude %{privlib}/IO/Uncompress/Base.pm
#%exclude ## {_mandir}/man3/File::GlobMapper.*
#%exclude ## {_mandir}/man3/IO::Compress::Base.*
#%exclude ## {_mandir}/man3/IO::Uncompress::AnyUncompress.*
#%exclude ## {_mandir}/man3/IO::Uncompress::Base.*
# IO::Compress::Zlib
%exclude %{privlib}/IO/Compress/Adapter/
%exclude %{privlib}/IO/Compress/Deflate.pm
%exclude %{privlib}/IO/Compress/Gzip/
%exclude %{privlib}/IO/Compress/Gzip.pm
%exclude %{privlib}/IO/Compress/RawDeflate.pm
%exclude %{privlib}/IO/Compress/Zip/
%exclude %{privlib}/IO/Compress/Zip.pm
%exclude %{privlib}/IO/Compress/Zlib/
%exclude %{privlib}/IO/Uncompress/Adapter/
%exclude %{privlib}/IO/Uncompress/AnyInflate.pm
%exclude %{privlib}/IO/Uncompress/Gunzip.pm
%exclude %{privlib}/IO/Uncompress/Inflate.pm
%exclude %{privlib}/IO/Uncompress/RawInflate.pm
%exclude %{privlib}/IO/Uncompress/Unzip.pm
#%exclude ## {_mandir}/man3/IO::Compress::Deflate*
#%exclude ## {_mandir}/man3/IO::Compress::Gzip*
#%exclude ## {_mandir}/man3/IO::Compress::RawDeflate*
#%exclude ## {_mandir}/man3/IO::Compress::Zip*
#%exclude ## {_mandir}/man3/IO::Uncompress::AnyInflate*
#%exclude ## {_mandir}/man3/IO::Uncompress::Gunzip*
#%exclude ## {_mandir}/man3/IO::Uncompress::Inflate*
#%exclude ## {_mandir}/man3/IO::Uncompress::RawInflate*
#%exclude ## {_mandir}/man3/IO::Uncompress::Unzip*

# IO::Zlib
%exclude %{privlib}/IO/Zlib.pm
#%exclude ## {_mandir}/man3/IO::Zlib.*

# IPC::Cmd
%exclude %{privlib}/IPC/Cmd.pm
#%exclude ## {_mandir}/man3/IPC::Cmd.3*

# Locale::Maketext::Simple
%exclude %{privlib}/Locale/Maketext/Simple.pm
#%exclude ## {_mandir}/man3/Locale::Maketext::Simple.*

# Log::Message
%exclude %{privlib}/Log/Message.pm
%exclude %{privlib}/Log/Message/Config.pm
%exclude %{privlib}/Log/Message/Handlers.pm
%exclude %{privlib}/Log/Message/Item.pm
#%exclude ## {_mandir}/man3/Log::Message.3*
#%exclude ## {_mandir}/man3/Log::Message::Config.3*
#%exclude ## {_mandir}/man3/Log::Message::Handlers.3*
#%exclude ## {_mandir}/man3/Log::Message::Item.3*

# Log::Message::Simple
%exclude %{privlib}/Log/Message/Simple.pm
#%exclude ## {_mandir}/man3/Log::Message::Simple.3*

# Module::Build
%exclude %{_bindir}/config_data
%exclude %{privlib}/inc/
%exclude %{privlib}/Module/Build/
%exclude %{privlib}/Module/Build.pm
#%exclude ## {_mandir}/man1/config_data.1*
#%exclude ## {_mandir}/man3/Module::Build*
#%exclude ## {_mandir}/man3/inc::latest.3*

# Module-CoreList
%exclude %{_bindir}/corelist
%exclude %{privlib}/Module/CoreList.pm
#%exclude ## {_mandir}/man1/corelist*
#%exclude ## {_mandir}/man3/Module::CoreList*

# Module-Load
%exclude %{privlib}/Module/Load.pm
#%exclude ## {_mandir}/man3/Module::Load.*

# Module-Load-Conditional
%exclude %{privlib}/Module/Load/
#%exclude ## {_mandir}/man3/Module::Load::Conditional*

# Module-Loaded
%exclude %{privlib}/Module/Loaded.pm
#%exclude ## {_mandir}/man3/Module::Loaded*

# Module-Pluggable
%exclude %{privlib}/Devel/InnerPackage.pm
%exclude %{privlib}/Module/Pluggable/
%exclude %{privlib}/Module/Pluggable.pm
#%exclude ## {_mandir}/man3/Devel::InnerPackage*
#%exclude ## {_mandir}/man3/Module::Pluggable*

# Object-Accessor
%exclude %{privlib}/Object/
#%exclude ## {_mandir}/man3/Object::Accessor*

# Package-Constants
%exclude %{privlib}/Package/
#%exclude ## {_mandir}/man3/Package::Constants*

# PathTools
%exclude %{archlib}/Cwd.pm
%exclude %{archlib}/File/Spec*
%exclude %{archlib}/auto/Cwd/
#%exclude ## {_mandir}/man3/Cwd*
#%exclude ## {_mandir}/man3/File::Spec*

# Params-Check
%exclude %{privlib}/Params/
#%exclude ## {_mandir}/man3/Params::Check*

# parent
%exclude %{privlib}/parent.pm
#%exclude ## {_mandir}/man3/parent.3*

# Pod-Escapes
%exclude %{privlib}/Pod/Escapes.pm
#%exclude ## {_mandir}/man3/Pod::Escapes.*

# Pod-Simple
%exclude %{privlib}/Pod/Simple/
%exclude %{privlib}/Pod/Simple.pm
%exclude %{privlib}/Pod/Simple.pod
#%exclude ## {_mandir}/man3/Pod::Simple*

# Scalar-List-Utils
%exclude %{archlib}/List/
%exclude %{archlib}/Scalar/
%exclude %{archlib}/auto/List/
#%exclude ## {_mandir}/man3/List::Util*
#%exclude ## {_mandir}/man3/Scalar::Util*

# Term-UI
%exclude %{privlib}/Term/UI.pm
%exclude %{privlib}/Term/UI/
#%exclude ## {_mandir}/man3/Term::UI*

# Test::Harness
%exclude %{_bindir}/prove
%exclude %{privlib}/App*
%exclude %{privlib}/TAP*
%exclude %{privlib}/Test/Harness*
#%exclude ## {_mandir}/man1/prove.1*
#%exclude ## {_mandir}/man3/App*
#%exclude ## {_mandir}/man3/TAP*
#%exclude ## {_mandir}/man3/Test::Harness*

# Test::Simple
%exclude %{privlib}/Test/More*
%exclude %{privlib}/Test/Builder*
%exclude %{privlib}/Test/Simple*
%exclude %{privlib}/Test/Tutorial*
#%exclude ## {_mandir}/man3/Test::More*
#%exclude ## {_mandir}/man3/Test::Builder*
#%exclude ## {_mandir}/man3/Test::Simple*
#%exclude ## {_mandir}/man3/Test::Tutorial*

# Time::Piece
%exclude %{archlib}/Time/Piece.pm
%exclude %{archlib}/Time/Seconds.pm
%exclude %{archlib}/auto/Time/Piece/
#%exclude ## {_mandir}/man3/Time::Piece.3*
#%exclude ## {_mandir}/man3/Time::Seconds.3*

# threads
#%dir %exclude %{archlib}/auto/threads
#%exclude %{archlib}/auto/threads/threads*
%exclude %{archlib}/threads.pm
#%exclude ## {_mandir}/man3/threads.3*

# threads-shared
%exclude %{archlib}/auto/threads/shared*
%exclude %dir %{archlib}/threads
%exclude %{archlib}/threads/shared*
#%exclude ## {_mandir}/man3/threads::shared*

# version
%exclude %{privlib}/version.pm
%exclude %{privlib}/version.pod
%exclude %{privlib}/version/
#%exclude ## {_mandir}/man3/version.3*
#%exclude ## {_mandir}/man3/version::Internals.3*

%files libs
%defattr(-,root,root)
%{_libdir}/*.dll
%dir %{archlib}
%dir %{perl_vendorarch}
%dir %{perl_vendorarch}/auto

%files devel
%defattr(-,root,root,-)
%{_bindir}/enc2xs
## {_mandir}/man1/enc2xs*
%{privlib}/Encode/
%{_bindir}/h2xs
## {_mandir}/man1/h2xs*
%{_bindir}/libnetcfg
## {_mandir}/man1/libnetcfg*
%{_bindir}/perlivp
## {_mandir}/man1/perlivp*
%{archlib}/CORE/*.h
## {_mandir}/man1/perlxs*
#%attr(0644,root,root) %{_sysconfdir}/rpm/macros.perl
#%{tapsetdir}/%{libperl_stp}
#%doc perl-example.stp

%files tests
%defattr(-,root,root,-)
%{perl5_testdir}/
#%exclude %{perl5_testdir}/Test-Simple

%files Archive-Extract
%defattr(-,root,root,-)
%{privlib}/Archive/Extract.pm
## {_mandir}/man3/Archive::Extract.3*

%files Archive-Tar
%defattr(-,root,root,-)
%{_bindir}/ptar
%{_bindir}/ptardiff
%{privlib}/Archive/Tar/ 
%{privlib}/Archive/Tar.pm
## {_mandir}/man1/ptar.1*
## {_mandir}/man1/ptardiff.1*
## {_mandir}/man3/Archive::Tar* 

%files Class-ISA
%defattr(-,root,root,-)
#%{privlib}/Class/ISA.pm
## {_mandir}/man3/Class::ISA.3*

%files CGI
%defattr(-,root,root,-)
%{privlib}/CGI/
%{privlib}/CGI.pm
## {_mandir}/man3/CGI.3*
## {_mandir}/man3/CGI::*.3*

%files Compress-Raw-Zlib
%defattr(-,root,root,-)
%dir %{archlib}/Compress
%{archlib}/Compress/Raw/
%dir %{archlib}/auto/Compress/
%dir %{archlib}/auto/Compress/Raw/
%{archlib}/auto/Compress/Raw/Zlib/
## {_mandir}/man3/Compress::Raw::Zlib*

%files CPAN
%defattr(-,root,root,-)
%{_bindir}/cpan
%{privlib}/CPAN/
%{privlib}/CPAN.pm
## {_mandir}/man1/cpan.1*
## {_mandir}/man3/CPAN.*
## {_mandir}/man3/CPAN:*

%files CPANPLUS
%defattr(-,root,root,-)
%{_bindir}/cpan2dist
%{_bindir}/cpanp
%{_bindir}/cpanp-run-perl
%{privlib}/CPANPLUS/
%{privlib}/CPANPLUS.pm
## {_mandir}/man1/cpan2dist.1*
## {_mandir}/man1/cpanp.1*
## {_mandir}/man3/CPANPLUS*

%files Digest-SHA
%defattr(-,root,root,-)
%{_bindir}/shasum
%dir %{archlib}/Digest/
%{archlib}/Digest/SHA.pm
%{archlib}/auto/Digest/SHA/
## {_mandir}/man1/shasum.1*
## {_mandir}/man3/Digest::SHA.3*

%files ExtUtils-CBuilder
%defattr(-,root,root,-)
%{privlib}/ExtUtils/CBuilder/
%{privlib}/ExtUtils/CBuilder.pm
## {_mandir}/man3/ExtUtils::CBuilder*

%files ExtUtils-Embed
%defattr(-,root,root,-)
%{privlib}/ExtUtils/Embed.pm
## {_mandir}/man3/ExtUtils::Embed*

%files ExtUtils-MakeMaker
%defattr(-,root,root,-)
%{_bindir}/instmodsh
%{privlib}/ExtUtils/Command/
%{privlib}/ExtUtils/Install.pm
%{privlib}/ExtUtils/Installed.pm
%{privlib}/ExtUtils/Liblist/
%{privlib}/ExtUtils/Liblist.pm
%{privlib}/ExtUtils/MakeMaker/
%{privlib}/ExtUtils/MakeMaker.pm
%{privlib}/ExtUtils/MANIFEST.SKIP
%{privlib}/ExtUtils/MM*.pm
%{privlib}/ExtUtils/MY.pm
%{privlib}/ExtUtils/Manifest.pm
%{privlib}/ExtUtils/Mkbootstrap.pm
%{privlib}/ExtUtils/Mksymlists.pm
%{privlib}/ExtUtils/Packlist.pm
%{privlib}/ExtUtils/testlib.pm
## {_mandir}/man1/instmodsh.1*
## {_mandir}/man3/ExtUtils::Command::MM*
## {_mandir}/man3/ExtUtils::Install.3*
## {_mandir}/man3/ExtUtils::Installed.3*
## {_mandir}/man3/ExtUtils::Liblist.3*
## {_mandir}/man3/ExtUtils::MM*
## {_mandir}/man3/ExtUtils::MY.3*
## {_mandir}/man3/ExtUtils::MakeMaker*
## {_mandir}/man3/ExtUtils::Manifest.3*
## {_mandir}/man3/ExtUtils::Mkbootstrap.3*
## {_mandir}/man3/ExtUtils::Mksymlists.3*
## {_mandir}/man3/ExtUtils::Packlist.3*
## {_mandir}/man3/ExtUtils::testlib.3*

%files ExtUtils-ParseXS
%defattr(-,root,root,-)
%{privlib}/ExtUtils/ParseXS.pm
%{privlib}/ExtUtils/xsubpp
%{_bindir}/xsubpp
## {_mandir}/man1/xsubpp*
## {_mandir}/man3/ExtUtils::ParseXS.3*

%files File-Fetch
%defattr(-,root,root,-)
%{privlib}/File/Fetch.pm
## {_mandir}/man3/File::Fetch.3*

%files IO-Compress
%defattr(-,root,root,-)
# Compress-Zlib
%{privlib}/Compress/Zlib.pm
#%{archlib}/auto/Compress/Zlib/
## {_mandir}/man3/Compress::Zlib*
#IO-Compress-Base
%{privlib}/File/GlobMapper.pm
%{privlib}/IO/Compress/Base/
%{privlib}/IO/Compress/Base.pm
%{privlib}/IO/Uncompress/AnyUncompress.pm
%{privlib}/IO/Uncompress/Base.pm
## {_mandir}/man3/File::GlobMapper.*
## {_mandir}/man3/IO::Compress::Base.*
## {_mandir}/man3/IO::Uncompress::AnyUncompress.*
## {_mandir}/man3/IO::Uncompress::Base.*

# IO-Compress-Zlib
%defattr(-,root,root,-)
%{privlib}/IO/Compress/Adapter/
%{privlib}/IO/Compress/Deflate.pm
%{privlib}/IO/Compress/Gzip/
%{privlib}/IO/Compress/Gzip.pm
%{privlib}/IO/Compress/RawDeflate.pm
%{privlib}/IO/Compress/Zip/
%{privlib}/IO/Compress/Zip.pm
%{privlib}/IO/Compress/Zlib/
%{privlib}/IO/Uncompress/Adapter/
%{privlib}/IO/Uncompress/AnyInflate.pm
%{privlib}/IO/Uncompress/Gunzip.pm
%{privlib}/IO/Uncompress/Inflate.pm
%{privlib}/IO/Uncompress/RawInflate.pm
%{privlib}/IO/Uncompress/Unzip.pm
## {_mandir}/man3/IO::Compress::Deflate*
## {_mandir}/man3/IO::Compress::Gzip*
## {_mandir}/man3/IO::Compress::RawDeflate*
## {_mandir}/man3/IO::Compress::Zip*
## {_mandir}/man3/IO::Uncompress::AnyInflate*
## {_mandir}/man3/IO::Uncompress::Gunzip*
## {_mandir}/man3/IO::Uncompress::Inflate*
## {_mandir}/man3/IO::Uncompress::RawInflate*
## {_mandir}/man3/IO::Uncompress::Unzip*

%files IO-Zlib
%defattr(-,root,root,-)
%{privlib}/IO/Zlib.pm
## {_mandir}/man3/IO::Zlib.*

%files IPC-Cmd
%defattr(-,root,root,-)
%{privlib}/IPC/Cmd.pm
## {_mandir}/man3/IPC::Cmd.3*

%files Locale-Maketext-Simple
%defattr(-,root,root,-)
%{privlib}/Locale/Maketext/Simple.pm
## {_mandir}/man3/Locale::Maketext::Simple.*

%files Log-Message
%defattr(-,root,root,-)
%{privlib}/Log/Message.pm
%{privlib}/Log/Message/Config.pm
%{privlib}/Log/Message/Handlers.pm
%{privlib}/Log/Message/Item.pm
## {_mandir}/man3/Log::Message.3*
## {_mandir}/man3/Log::Message::Config.3*
## {_mandir}/man3/Log::Message::Handlers.3*
## {_mandir}/man3/Log::Message::Item.3*

%files Log-Message-Simple
%defattr(-,root,root,-)
%{privlib}/Log/Message/Simple.pm
## {_mandir}/man3/Log::Message::Simple.3*

%files Module-Build
%defattr(-,root,root,-)
%{_bindir}/config_data
%{privlib}/inc/
%{privlib}/Module/Build/
%{privlib}/Module/Build.pm
## {_mandir}/man1/config_data.1*
## {_mandir}/man3/Module::Build*
## {_mandir}/man3/inc::latest.3*

%files Module-CoreList
%defattr(-,root,root,-)
%{_bindir}/corelist
%{privlib}/Module/CoreList.pm
## {_mandir}/man1/corelist*
## {_mandir}/man3/Module::CoreList*

%files Module-Load
%defattr(-,root,root,-)
%{privlib}/Module/Load.pm
## {_mandir}/man3/Module::Load.*

%files Module-Load-Conditional
%defattr(-,root,root,-)
%{privlib}/Module/Load/
## {_mandir}/man3/Module::Load::Conditional* 

%files Module-Loaded
%defattr(-,root,root,-)
%dir %{privlib}/Module/
%{privlib}/Module/Loaded.pm
## {_mandir}/man3/Module::Loaded*

%files Module-Pluggable
%defattr(-,root,root,-)
%{privlib}/Devel/InnerPackage.pm
%{privlib}/Module/Pluggable/
%{privlib}/Module/Pluggable.pm
## {_mandir}/man3/Devel::InnerPackage*
## {_mandir}/man3/Module::Pluggable*

%files Object-Accessor
%defattr(-,root,root,-)
%{privlib}/Object/
## {_mandir}/man3/Object::Accessor*

%files Package-Constants
%defattr(-,root,root,-)
%{privlib}/Package/
## {_mandir}/man3/Package::Constants*

%files PathTools
%defattr(-,root,root,-)
%{archlib}/Cwd.pm
%{archlib}/File/Spec*
%{archlib}/auto/Cwd/
## {_mandir}/man3/Cwd*
## {_mandir}/man3/File::Spec*

%files Params-Check
%defattr(-,root,root,-)
%{privlib}/Params/
## {_mandir}/man3/Params::Check*

%files Parse-CPAN-Meta
%defattr(-,root,root,-)
%dir %{privlib}/Parse/
%dir %{privlib}/Parse/CPAN/
%{privlib}/Parse/CPAN/Meta.pm
## {_mandir}/man3/Parse::CPAN::Meta.3*

%files Pod-Escapes
%defattr(-,root,root,-)
%{privlib}/Pod/Escapes.pm
## {_mandir}/man3/Pod::Escapes.*

%files Pod-Simple
%defattr(-,root,root,-)
%{privlib}/Pod/Simple/ 
%{privlib}/Pod/Simple.pm
%{privlib}/Pod/Simple.pod
## {_mandir}/man3/Pod::Simple*

%files Scalar-List-Utils
%defattr(-,root,root,-)
%{archlib}/List/
%{archlib}/Scalar/
%{archlib}/auto/List/
## {_mandir}/man3/List::Util*
## {_mandir}/man3/Scalar::Util*

%files Term-UI
%defattr(-,root,root,-)
%{privlib}/Term/UI/
%{privlib}/Term/UI.pm
## {_mandir}/man3/Term::UI*

%files Test-Harness
%defattr(-,root,root,-)
%{_bindir}/prove
%{privlib}/App*
%{privlib}/TAP*
%{privlib}/Test/Harness*
## {_mandir}/man1/prove.1*
## {_mandir}/man3/App*
## {_mandir}/man3/TAP*
## {_mandir}/man3/Test::Harness*

%files Test-Simple
%defattr(-,root,root,-)
%{privlib}/Test/More*
%{privlib}/Test/Builder*
%{privlib}/Test/Simple*
%{privlib}/Test/Tutorial*
## {_mandir}/man3/Test::More*
## {_mandir}/man3/Test::Builder*
## {_mandir}/man3/Test::Simple*
## {_mandir}/man3/Test::Tutorial*

%files Test-Simple-tests
%defattr(-,root,root,-)
%dir %{perl5_testdir}
#%{perl5_testdir}/Test-Simple

%files Time-Piece
%defattr(-,root,root,-)
%{archlib}/Time/Piece.pm 
%{archlib}/Time/Seconds.pm
%{archlib}/auto/Time/Piece/        
## {_mandir}/man3/Time::Piece.3*
## {_mandir}/man3/Time::Seconds.3*

%files parent 
%defattr(-,root,root,-)
%{privlib}/parent.pm
## {_mandir}/man3/parent.3*

%files threads
%defattr(-,root,root,-)
%dir %{archlib}/auto/threads
#%{archlib}/auto/threads/threads*
%{archlib}/threads.pm
## {_mandir}/man3/threads.3*

%files threads-shared
%defattr(-,root,root,-)
%{archlib}/auto/threads/shared*
%dir %{archlib}/threads
%{archlib}/threads/shared*
## {_mandir}/man3/threads::shared*

%files version
%defattr(-,root,root,-)
%{privlib}/version.pm
%{privlib}/version.pod
%{privlib}/version/
## {_mandir}/man3/version.3*
## {_mandir}/man3/version::Internals.3*

%files core
# Nothing. Nada. Zilch. Zarro. Uh uh. Nope. Sorry.

%files debug
%defattr(-,root,root)
%{_libdir}/*.dbg

%changelog
* Wed Aug 13 2014 yd
- first public release build.
- added debug package with symbolic info for exceptq.
- r745, Fix endless loop when calling shell script with invalid #! magic.
- r744, Support symlinked shells in scripts in system() and similar calls.
- r743, Fix building of minitperl on OS/2.
