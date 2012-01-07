Summary: A tool for creating scanners (text pattern recognizers)
Name: flex
Version: 2.5.35
Release: 1%{?dist}
License: BSD
Group: Development/Tools
URL: http://flex.sourceforge.net/
Source: http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Patch0: flex-2.5.35-sign.patch
Patch1: flex-2.5.35-hardening.patch
Patch2: flex-2.5.35-gcc44.patch
Patch3: flex-2.5.35-missing-prototypes.patch
Patch4: flex-os2.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: m4
BuildRequires: gettext bison m4

# We need to pull in the static library package.  That's necessary so
# that packages that just do BuildRequires: flex can still use -lfl.
# I suspect that linking to -lfl is actually rare and those (few)
# packages that do use it could be taught to require the sub-package
# explicitly.  So at some point in future, this dependency may be
# dropped.
#Requires: flex-static = %{version}

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
#%package static
#Summary: Libraries for flex scanner generator
#Group: Development/Tools

#%description static
#This package contains the library with default implementations of
#`main' and `yywrap' functions that the client binary can choose to use
#instead of implementing their own.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
export CONFIG_SHELL="/@unixroot/usr/bin/sh.exe"
export LDFLAGS="-Zbin-files -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lurpo -lmmap"
%configure \
    --disable-dependency-tracking \
   "--cache-file=%{_topdir}/cache/%{name}-%{_target_cpu}.cache"

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT/%{_infodir}/dir
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.a

( cd ${RPM_BUILD_ROOT}
  ln -sf flex .%{_bindir}/lex
  ln -sf flex .%{_bindir}/flex++
  ln -s flex.1 .%{_mandir}/man1/lex.1
  ln -s flex.1 .%{_mandir}/man1/flex++.1
)

#%check
#echo ============TESTING===============
#make check
#echo ============END TESTING===========

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%doc COPYING NEWS README
%{_bindir}/*
%{_mandir}/man1/*
%{_includedir}/FlexLexer.h
%{_infodir}/flex.info*
%{_usr}/share/locale/*

#%files static
#%defattr(-,root,root)
#%{_libdir}/*.a

%changelog
* Fri Jan 06 2012 yd
- initial unixroot build.
