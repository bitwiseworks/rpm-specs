Summary: A GNU general-purpose parser generator
Name: bison
Version: 3.4.1
Release: 1%{?dist}
License: GPLv3+
Group: Development/Tools

%scm_source github https://github.com/bitwiseworks/%{name}-os2 %{version}-os2
Vendor: bww bitwise works GmbH

# testsuite dependency
BuildRequires: gcc
BuildRequires: autoconf
BuildRequires: flex

URL: http://www.gnu.org/software/bison/
BuildRequires: m4 >= 1.4
#BuildRequires: java-1.6.0-openjdk-devel
Requires: m4 >= 1.4


%description
Bison is a general purpose parser generator that converts a grammar
description for an LALR(1) context-free grammar into a C program to
parse that grammar. Bison can be used to develop a wide range of
language parsers, from ones used in simple desk calculators to complex
programming languages. Bison is upwardly compatible with Yacc, so any
correctly written Yacc grammar should work with Bison without any
changes. If you know Yacc, you shouldn't have any trouble using
Bison. You do need to be very proficient in C programming to be able
to use Bison. Bison is only needed on systems that are used for
development.

If your system will be used for C development, you should install
Bison.

%package devel
Summary: -ly library for development using Bison-generated parsers
Group: Development/Libraries
Provides: bison-static = %{version}-%{release}

%description devel
The bison-devel package contains the -ly library sometimes used by
programs using Bison-generated parsers.  If you are developing programs
using Bison, you might want to link with this library.  This library
is not required by all Bison-generated parsers, but may be employed by
simple programs to supply minimal support for the generated parsers.

# -ly is kept static.  It only contains two symbols: main and yyerror,
# and both of these are extremely simple (couple lines of C total).
# It doesn't really pay off to introduce a shared library for that.
#
# Therefore -devel subpackage could have been created as -static, but
# the split was done in Jan 2005, which predates current guidelines.
# Besides there is logic to that: the library is devel in the sense
# that the generated parser could be distributed together with other
# sources, and only bison-devel would be necessary to wrap the build.

%package runtime
Summary: Runtime support files used by Bison-generated parsers

%description runtime
The bison-runtime package contains files used at runtime by parsers
that Bison generates.  Packages whose binaries contain parsers
generated by Bison should depend on bison-runtime to ensure that
these files are available.  See the Internationalization in the
Bison manual section for more information.

%debug_package

%prep
%scm_setup

%build
autoreconf -fvi
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
%configure --docdir=%{_docdir}/%{name}-%{version}
make %{?_smp_mflags}

%check
# checks are still disabled, even all work
# but enabling it means a very long buildtime, as tests run slow 
#make check
#make maintainer-check

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

# Remove unpackaged files.
rm -f $RPM_BUILD_ROOT/%{_bindir}/yacc
rm -f $RPM_BUILD_ROOT/%{_infodir}/dir
rm -f $RPM_BUILD_ROOT/%{_mandir}/man1/yacc*
rm -rf $RPM_BUILD_ROOT/%{_docdir}/%{name}/examples/*
find $RPM_BUILD_ROOT/%{_datadir}/locale/* -type f -name "bison-gnulib.mo" -exec rm -f {} ';'

%find_lang %{name}
%find_lang %{name}-runtime

gzip -9nf ${RPM_BUILD_ROOT}%{_infodir}/bison.info*


# The distribution contains also source files. These are used by m4
# when the target parser file is generated.
%files -f %{name}.lang
%doc AUTHORS ChangeLog NEWS README THANKS TODO COPYING
%{_mandir}/*/bison*
%{_datadir}/bison
%{_infodir}/bison.info*
%{_bindir}/bison.exe
%{_datadir}/aclocal/bison*.m4

%files -f %{name}-runtime.lang runtime
%doc COPYING

%files devel
%{_libdir}/liby.a


%changelog
* Fri Jun 14 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> 3.4.1-1
- update to version 3.4.1

* Mon Jun 27 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> 3.0.4-1
- update to version 3.0.4
- add debug package

* Tue Feb 28 2012 yd
- fixed m4 executable location.

* Fri Jan 06 2012 yd
- initial unixroot build.