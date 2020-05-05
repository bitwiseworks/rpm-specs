%global unversion 2_2_9

Summary: An XML parser library
Name: expat
Version: %(echo %{unversion} | sed 's/_/./g')
Release: 1%{?dist}
URL: https://libexpat.github.io/
License: MIT
BuildRequires: autoconf, libtool, xmlto, gcc-c++

Vendor: bww bitwise works GmbH
%scm_source github  http://github.com/bitwiseworks/%{name}-os2 %{version}-os2

# DEF files to create forwarders to the old name
Source10:       expat7.def

%description
This is expat, the C library for parsing XML, written by James Clark. Expat
is a stream oriented XML parser. This means that you register handlers with
the parser prior to starting the parse. These handlers are called when the
parser discovers the associated structures in the document being parsed. A
start tag is an example of the kind of structures for which you may
register handlers.

%package devel
Summary: Libraries and header files to develop applications using expat
Requires: expat = %{version}-%{release}

%description devel
The expat-devel package contains the libraries, include files and documentation
to develop XML applications with expat.

%package static
Summary: expat XML parser static library
Requires: expat-devel = %{version}-%{release}

%description static
The expat-static package contains the static version of the expat library.
Install it if you need to link statically with expat.

%debug_package

%prep
%scm_setup

sed -i 's/install-data-hook/do-nothing-please/' lib/Makefile.am
autoreconf -fvi

# Prepare forwarder DLLs.
for m in %{SOURCE10}; do
  cp ${m} .
done

%build
export CFLAGS="$RPM_OPT_FLAGS"
export LDFLAGS="-Zomf -Zhigh-mem -Zargs-wild -Zargs-resp -lcx"
export DOCBOOK_TO_MAN="xmlto man --skip-validation"
%configure

# Set BUILDLEVEL to be embedded to all DLLs built with Libtool.
export LT_BUILDLEVEL="@#%{vendor}:%{version}-%{release}#@##1## `LANG=C date +'%%d %%b %%Y %%H:%%M:%%S'`     `uname -n`::::0::"
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/expat

# Generate & install forwarder DLLs.
gcc -Zomf -Zdll -nostdlib expat7.def -l$RPM_BUILD_ROOT/%{_libdir}/expat1.dll -lend -o $RPM_BUILD_ROOT/%{_libdir}/expat7.dll

%check
export LIBPATHSTRICT=t
export BEGINLIBPATH=%{_builddir}/%{buildsubdir}/lib/.libs
make check

%if !0%{?os2_version}
%ldconfig_scriptlets
%endif

%files
%{!?_licensedir:%global license %%doc}
%doc AUTHORS Changes
%license COPYING
%{_bindir}/*.exe
%{_libdir}/*.dll
%{_mandir}/*/*

%files devel
%doc doc/reference.html doc/*.png doc/*.css examples/*.c
%{_libdir}/*_dll.a
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*.h

%files static
%{_libdir}/*.a
%exclude %{_libdir}/*_dll.a

%changelog
* Thu Aug 10 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.2.9-1
- update to version 2.2.9
- built with latest tools
- remove -Zbin-files

* Thu Aug 10 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.1.0-13
- use scm_ macros
- add a forwarder, as the toolchain changes the name

* Mon Sep 08 2014 yd 2.1.0-12
- added debug package with symbolic info for exceptq.

* Wed Sep 3 2014 Dmitriy Kuminov <coding@dmik.org> 2.1.0-11
- Rebuild with high memory support.

* Mon Sep 1 2014 Dmitriy Kuminov <coding@dmik.org> 2.1.0-10
- Initial package for version 2.1.0.
