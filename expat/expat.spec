%global unversion 2_7_1

Summary: An XML parser library
Name: expat
Version: %(echo %{unversion} | sed 's/_/./g')
Release: 1%{?dist}
%if !0%{?os2_version}
Source0: https://github.com/libexpat/libexpat/releases/download/R_%{unversion}/expat-%{version}.tar.gz
Source1: https://github.com/libexpat/libexpat/releases/download/R_%{unversion}/expat-%{version}.tar.gz.asc
# Sebastian Pipping's PGP public key
Source2: https://keys.openpgp.org/vks/v1/by-fingerprint/3176EF7DB2367F1FCA4F306B1F9B0E909AF37285
%else
Vendor: bww bitwise works GmbH
%scm_source github  http://github.com/bitwiseworks/%{name}-os2 %{version}-os2

# DEF files to create forwarders to the old name
Source10:       expat7.def
%endif

URL: https://libexpat.github.io/
License: MIT
BuildRequires: autoconf, libtool, xmlto, gcc-c++
BuildRequires: make
%if !0%{?os2_version}
BuildRequires: gnupg2
%endif

%description
This is expat, the C library for parsing XML, written by James Clark. Expat
is a stream oriented XML parser. This means that you register handlers with
the parser prior to starting the parse. These handlers are called when the
parser discovers the associated structures in the document being parsed. A
start tag is an example of the kind of structures for which you may
register handlers.

%package devel
Summary: Libraries and header files to develop applications using expat
%if !0%{?os2_version}
Requires: expat%{?_isa} = %{version}-%{release}
%else
Requires: expat = %{version}-%{release}
%endif

%description devel
The expat-devel package contains the libraries, include files and documentation
to develop XML applications with expat.

%package static
Summary: expat XML parser static library
%if !0%{?os2_version}
Requires: expat-devel%{?_isa} = %{version}-%{release}
%else
Requires: expat-devel = %{version}-%{release}
%endif

%description static
The expat-static package contains the static version of the expat library.
Install it if you need to link statically with expat.

%if 0%{?os2_version}
%debug_package
%endif

%prep
%if !0%{?os2_version}
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup
%else
%scm_setup

# Prepare forwarder DLLs.
for m in %{SOURCE10}; do
  cp ${m} .
done
%endif
sed -i 's/install-data-hook/do-nothing-please/' lib/Makefile.am
./buildconf.sh

%build
%if !0%{?os2_version}
export CFLAGS="$RPM_OPT_FLAGS -fPIC"
%else
export CFLAGS="$RPM_OPT_FLAGS"
export LDFLAGS="-Zomf -Zhigh-mem -Zargs-wild -Zargs-resp -lcx"
%endif
export DOCBOOK_TO_MAN="xmlto man"
%configure

%if 0%{?os2_version}
# Set BUILDLEVEL to be embedded to all DLLs built with Libtool.
export LT_BUILDLEVEL="@#%{vendor}:%{version}-%{release}#@##1## `LANG=C date +'%%d %%b %%Y %%H:%%M:%%S'`     `uname -n`::::0::"
%endif
%make_build

%install
%make_install

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%if 0%{?os2_version}
# remove Authors and Changes
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/expat

# Generate & install forwarder DLLs.
gcc -Zomf -Zdll -nostdlib expat7.def -l$RPM_BUILD_ROOT/%{_libdir}/expat1.dll -lend -o $RPM_BUILD_ROOT/%{_libdir}/expat7.dll
%endif

%check
%if 0%{?os2_version}
export LIBPATHSTRICT=t
export BEGINLIBPATH=%{_builddir}/%{buildsubdir}/lib/.libs
%endif
make check

%if !0%{?os2_version}
%ldconfig_scriptlets
%endif

%files
%doc AUTHORS Changes
%license COPYING
%if !0%{?os2_version}
%{_bindir}/*
%{_libdir}/libexpat.so.1
%{_libdir}/libexpat.so.1.*
%else
%{_bindir}/*.exe
%{_libdir}/expat1.dll
%{_libdir}/expat7.dll
%endif
%{_mandir}/*/*

%files devel
%doc doc/reference.html doc/*.css examples/*.c
%if !0%{?os2_version}
%{_libdir}/libexpat.so
%else
%{_libdir}/*_dll.a
%endif
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*.h
%{_libdir}/cmake/expat-%{version}

%files static
%if !0%{?os2_version}
%{_libdir}/libexpat.a
%else
%{_libdir}/expat.a
%endif

%changelog
* Tue May 06 2025 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.7.1-1
- update to version 2.7.1

* Tue May 05 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.2.9-1
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
