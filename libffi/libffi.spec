%bcond_with bootstrap

%global multilib_arches %{ix86} x86_64

Name:		libffi
Version:	3.4.2
Release:	1%{?dist}
Summary:	A portable foreign function interface library
License:	MIT
URL:		http://sourceware.org/libffi

%if !0%{?os2_version}
Source0:	https://github.com/libffi/libffi/releases/download/v3.4.2/libffi-3.4.2.tar.gz
Source1:	ffi-multilib.h
Source2:	ffitarget-multilib.h
%else
Vendor:         bww bitwise works GmbH
%scm_source	github http://github.com/bitwiseworks/%{name}-os2 v%{version}-os2
%endif

BuildRequires: make
BuildRequires: gcc
%if %{without bootstrap}
BuildRequires: gcc-c++
%if !0%{?os2_version}
BuildRequires: dejagnu
%endif
%endif

%description
Compilers for high level languages generate code that follow certain
conventions.  These conventions are necessary, in part, for separate
compilation to work.  One such convention is the "calling convention".
The calling convention is a set of assumptions made by the compiler
about where function arguments will be found on entry to a function.  A
calling convention also specifies where the return value for a function
is found.  

Some programs may not know at the time of compilation what arguments
are to be passed to a function.  For instance, an interpreter may be
told at run-time about the number and types of arguments used to call a
given function.  `Libffi' can be used in such programs to provide a
bridge from the interpreter program to compiled code.

The `libffi' library provides a portable, high level programming
interface to various calling conventions.  This allows a programmer to
call any function specified by a call interface description at run time.

FFI stands for Foreign Function Interface.  A foreign function
interface is the popular name for the interface that allows code
written in one language to call code written in another language.  The
`libffi' library really only provides the lowest, machine dependent
layer of a fully featured foreign function interface.  A layer must
exist above `libffi' that handles type conversions for values passed
between the two languages.  

%package	devel
Summary:	Development files for %{name}
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig

%description	devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%if 0%{?os2_version}
%debug_package
%endif

%prep
%if !0%{?os2_version}
%setup -q
%else
%scm_setup
autoreconf -fvi
%endif

%build
%if 0%{?os2_version}
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
# Set BUILDLEVEL to be embedded to all DLLs built with Libtool.
export LT_BUILDLEVEL="@#%{vendor}:%{version}-%{release}#@##1## `LANG=C date +'%%d %%b %%Y %%H:%%M:%%S'`     `uname -n`::::0::"
%endif
# For now we disable the static templates to avoid ghc and
# gobject-introspection failures:
# https://gitlab.haskell.org/ghc/ghc/-/issues/20051
# https://gitlab.gnome.org/GNOME/gobject-introspection/-/merge_requests/283
# We need to get these fixes into Fedora before we can reeanble them.
%configure --disable-static --disable-exec-static-tramp
%make_build

%check
%if %{without bootstrap}
%make_build check
%endif

%install
%make_install

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%if !0%{?os2_version}
# Determine generic arch target name for multilib wrapper
basearch=%{_arch}
%ifarch %{ix86}
basearch=i386
%endif

mkdir -p $RPM_BUILD_ROOT%{_includedir}
%ifarch %{multilib_arches}
# Do header file switcheroo to avoid file conflicts on systems where you
# can have both a 32- and 64-bit version of the library, and they each need
# their own correct-but-different versions of the headers to be usable.
for i in ffi ffitarget; do
  mv $RPM_BUILD_ROOT%{_includedir}/$i.h $RPM_BUILD_ROOT%{_includedir}/$i-${basearch}.h
done
install -m644 %{SOURCE1} $RPM_BUILD_ROOT%{_includedir}/ffi.h
install -m644 %{SOURCE2} $RPM_BUILD_ROOT%{_includedir}/ffitarget.h
%endif
%endif

%if !0%{?os2_version}
%ldconfig_scriptlets
%endif

%files
%license LICENSE
%doc README.md
%if !0%{?os2_version}
%{_libdir}/libffi.so.8
%{_libdir}/libffi.so.8.1.0
%else
%{_libdir}/ffi*.dll
%endif

%files devel
%{_libdir}/pkgconfig/*.pc
%{_includedir}/ffi*.h
%if !0%{?os2_version}
%{_libdir}/*.so
%else
%{_libdir}/*_dll.a
%endif
%{_mandir}/man3/*.gz
%{_infodir}/libffi.info.*

%changelog
* Mon Dec 27 2021 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.4.2-1
- update to version 3.4.2

* Sat Oct 27 2012 yd
- initial unixroot build.
