# devel is not buildable due to unresolved externals
%define build_devel 0

Summary: A tool for creating scanners (text pattern recognizers)
Name: flex
Version: 2.6.4
Release: 1%{?dist}
# parse.c and parse.h are under GPLv3+ with exception which allows
#	relicensing.  Since flex is shipped under BDS-style license,
#	let's  assume that the relicensing was done.
# gettext.h (copied from gnulib) is under LGPLv2+
License: BSD and LGPLv2+
URL: https://github.com/westes/flex
Group: Development/Tools
%scm_source github https://github.com/bitwiseworks/%{name}-os2 %{version}-os2

Requires: m4
BuildRequires: gettext gettext-devel bison m4 help2man gcc automake libtool

%description
The flex program generates scanners.  Scanners are programs which can
recognize lexical patterns in text.  Flex takes pairs of regular
expressions and C code as input and generates a C source file as
output.  The output file is compiled and linked with a library to
produce an executable.  The executable searches through its input for
occurrences of the regular expressions.  When a match is found, it
executes the corresponding C code.  Flex was designed to work with
both Yacc and Bison, and is used by many programs as part of their
build process.

You should install flex if you are going to use your system for
application development.

# We keep the libraries in separate sub-package to allow for multilib
# installations of flex.
%if %{build_devel}
%package devel
Summary: Libraries for flex scanner generator
Obsoletes: flex-static < 2.5.35-15
Provides: flex-static

%description devel

This package contains the library with default implementations of
`main' and `yywrap' functions that the client binary can choose to use
instead of implementing their own.
%endif

%package doc
Summary: Documentation for flex scanner generator
	
%description doc

This package contains documentation for flex scanner generator in
plain text and PDF formats.

%debug_package

%prep
%scm_setup

%build
autoreconf -fvi

export LDFLAGS="-Zbin-files -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
%if %{build_devel}
%global conf_flags ""
%else
%global conf_flags "--disable-libfl"
%endif
%configure --docdir=%{_pkgdocdir} %{conf_flags}
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT/%{_infodir}/dir
rm -f $RPM_BUILD_ROOT/%{_pkgdocdir}/README.cvs
rm -f $RPM_BUILD_ROOT/%{_pkgdocdir}/TODO
# For now, excluding the new .la and .so files as we haven't had
# any requests for them and adding them will require a new subpackage.
# The .so files contain 2 optional implementations of main and yywrap
# for developer convenience. They are also available in the .a file
# provided in flex-devel.
find %{buildroot} -name '*.la' -delete
find %{buildroot} -name '*.dll' -delete

( cd ${RPM_BUILD_ROOT}
  rm -f .%{_bindir}/flex++.exe
  ln -sf flex.exe .%{_bindir}/lex
  ln -sf flex.exe .%{_bindir}/flex++
  ln -s flex.1 .%{_mandir}/man1/lex.1
  ln -s flex.1 .%{_mandir}/man1/flex++.1
%if %{build_devel}
  ln -s libfl.a .%{_libdir}/libl.a
%endif
)

%find_lang flex

%check
echo ============TESTING===============
make check
echo ============END TESTING===========

%files  -f flex.lang
%dir %{_pkgdocdir}
%license COPYING
%{_pkgdocdir}/NEWS
%{_pkgdocdir}/README.md
%{_bindir}/*
%exclude %{_bindir}/*.dbg
%{_mandir}/man1/*
%{_includedir}/FlexLexer.h
%{_infodir}/flex.info*

%if %{build_devel}
%files devel
%dir %{_pkgdocdir}
%license COPYING
%{_libdir}/*.a
%endif

%files doc	
%{_pkgdocdir}
%exclude %{_pkgdocdir}/NEWS
%exclude %{_pkgdocdir}/README.md

%changelog
* Wed Jun 12 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.6.4-1
- update to version 2.6.4
- use scm_ macros
- moved source to github

* Tue Feb 28 2012 yd
- fixed m4 executable location.

* Fri Jan 06 2012 yd
- initial unixroot build.
