# This package depends on automagic byte compilation
# https://fedoraproject.org/wiki/Changes/No_more_automagic_Python_bytecompilation_phase_2
%global _python_bytecompile_extra 1

%global _changelog_trimtime %(date +%s -d "1 year ago")

# See https://fedoraproject.org/wiki/Packaging:Python_Appendix#Manual_byte_compilation
%global __python %{__python3}

Name: glib2
Version: 2.58.3
Release: 1%{?dist}
Summary: A library of handy utility functions

License: LGPLv2+
URL: http://www.gtk.org
%if !0%{?os2_version}
Source0: http://download.gnome.org/sources/glib/2.58/glib-%{version}.tar.xz
%else
Vendor: bww bitwise works GmbH
%scm_source github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2
%endif

%if !0%{?os2_version}
BuildRequires: chrpath
%endif
BuildRequires: gettext
%if !0%{?os2_version}
BuildRequires: perl-interpreter
%else
BuildRequires: perl
%endif
%if !0%{?os2_version}
# for sys/inotify.h
BuildRequires: glibc-devel
BuildRequires: libattr-devel
BuildRequires: libselinux-devel
# for sys/sdt.h
BuildRequires: systemtap-sdt-devel
BuildRequires: pkgconfig(libelf)
%endif
BuildRequires: pkgconfig(libffi)
BuildRequires: pkgconfig(libpcre)
%if !0%{?os2_version}
BuildRequires: pkgconfig(mount)
%endif
BuildRequires: pkgconfig(zlib)
# Bootstrap build requirements
BuildRequires: automake autoconf libtool
%if !0%{?os2_version}
BuildRequires: gtk-doc
%endif
BuildRequires: python3-devel

%if !0%{?os2_version}
# for GIO content-type support
Recommends: shared-mime-info
%endif

%if 0%{?os2_version}
Provides:  libglib-2_0-0 = %{version}-%{release}
Obsoletes: libglib-2_0-0 < %{version}-%{release}
Provides:  libgmodule-2_0-0 = %{version}-%{release}
Obsoletes: libgmodule-2_0-0 < %{version}-%{release}
Provides:  libgthread-2_0-0 = %{version}-%{release}
Obsoletes: libgthread-2_0-0 < %{version}-%{release}
Provides:  libgobject-2_0-0 = %{version}-%{release}
Obsoletes: libgobject-2_0-0 < %{version}-%{release}
Provides:  libgio-2_0-0 = %{version}-%{release}
Obsoletes: libgio-2_0-0 < %{version}-%{release}
%endif

%description
GLib is the low-level core library that forms the basis for projects
such as GTK+ and GNOME. It provides data structure handling for C,
portability wrappers, and interfaces for such runtime functionality
as an event loop, threads, dynamic loading, and an object system.


%package devel
Summary: A library of handy utility functions
%if !0%{?os2_version}
Requires: %{name}%{?_isa} = %{version}-%{release}
%else
Requires: %{name} = %{version}-%{release}
%endif

%description devel
The glib2-devel package includes the header files for the GLib library.

%package doc
Summary: A library of handy utility functions
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
The glib2-doc package includes documentation for the GLib library.

%if !0%{?os2_version}
%package fam
Summary: FAM monitoring module for GIO
Requires: %{name}%{?_isa} = %{version}-%{release}
BuildRequires: gamin-devel

%description fam
The glib2-fam package contains the FAM (File Alteration Monitor) module for GIO.
%endif

%package static
Summary: glib static
Requires: %{name}-devel = %{version}-%{release}

%description static
The %{name}-static subpackage contains static libraries for %{name}.

%package tests
Summary: Tests for the glib2 package
%if !0%{?os2_version}
Requires: %{name}%{?_isa} = %{version}-%{release}
%else
Requires: %{name} = %{version}-%{release}
%endif

%description tests
The glib2-tests package contains tests that can be used to verify
the functionality of the installed glib2 package.

%if 0%{?os2_version}
%debug_package
%endif

%prep
%if !0%{?os2_version}
%autosetup -n glib-%{version} -p1
%else
%scm_setup
%endif

%build
# Bug 1324770: Also explicitly remove PCRE sources since we use --with-pcre=system
rm glib/pcre/*.[ch]
%if !0%{?os2_version}
# Support builds of both git snapshots and tarballs packed with autogoo
(if ! test -x configure; then NOCONFIGURE=1 ./autogen.sh; CONFIGFLAGS=--enable-gtk-doc; fi;
 %configure $CONFIGFLAGS \
           --disable-silent-rules \
           --with-python=%{__python3} \
           --with-pcre=system \
           --enable-systemtap \
           --enable-static \
           --enable-installed-tests
)
%else
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lpthread -lcx"
export VENDOR="%{vendor}"
export NOCONFIGURE=1
autogen.sh
export BEGINLIBPATH="%{_builddir}/%{buildsubdir}/glib/.libs;%{_builddir}/%{buildsubdir}/gobject/.libs;%{_builddir}/%{buildsubdir}/gio/.libs;%{_builddir}/%{buildsubdir}/gthread/.libs;%{_builddir}/%{buildsubdir}/gmodule/.libs"
%configure \
           --with-python=%{__python3} \
           --with-pcre=system \
           --enable-shared --enable-static \
           --enable-installed-tests
%endif

%make_build

%install
%make_install
# Since this is a generated .py file, set it to a known timestamp,
# otherwise it will vary by build time, and thus break multilib -devel
# installs.
touch -r gio/gdbus-2.0/codegen/config.py.in $RPM_BUILD_ROOT/%{_datadir}/glib-2.0/codegen/config.py
%if !0%{?os2_version}
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/*.so
%endif

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
%if !0%{?os2_version}
rm -f $RPM_BUILD_ROOT%{_libdir}/gio/modules/*.{a,la}
%else
rm -f $RPM_BUILD_ROOT%{_libdir}/gio/modules/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/gio/modules/*.la
%endif
# Remove python files bytecompiled by the build system. rpmbuild regenerates
# them again later in a brp script using the timestamps set above.
%if !0%{?os2_version}
rm -f $RPM_BUILD_ROOT%{_datadir}/glib-2.0/gdb/*.{pyc,pyo}
%else
rm -f $RPM_BUILD_ROOT%{_datadir}/glib-2.0/gdb/*.pyc
rm -f $RPM_BUILD_ROOT%{_datadir}/glib-2.0/gdb/*.pyo
rm -f $RPM_BUILD_ROOT%{_libdir}/charset.alias
%endif
rm -f $RPM_BUILD_ROOT%{_datadir}/glib-2.0/gdb/__pycache__/
%if !0%{?os2_version}
rm -f $RPM_BUILD_ROOT%{_datadir}/glib-2.0/codegen/*.{pyc,pyo}
%else
rm -f $RPM_BUILD_ROOT%{_datadir}/glib-2.0/codegen/*.pyc
rm -f $RPM_BUILD_ROOT%{_datadir}/glib-2.0/codegen/*.pyo
%endif
rm -rf $RPM_BUILD_ROOT%{_datadir}/glib-2.0/codegen/__pycache__/

%if !0%{?os2_version}
mv  $RPM_BUILD_ROOT%{_bindir}/gio-querymodules $RPM_BUILD_ROOT%{_bindir}/gio-querymodules-%{__isa_bits}
%endif

touch $RPM_BUILD_ROOT%{_libdir}/gio/modules/giomodule.cache

# bash-completion scripts need not be executable
chmod 644 $RPM_BUILD_ROOT%{_datadir}/bash-completion/completions/*

%find_lang glib20

%if !0%{?os2_version}
%transfiletriggerin -- %{_libdir}/gio/modules
gio-querymodules-%{__isa_bits} %{_libdir}/gio/modules &> /dev/null || :

%transfiletriggerpostun -- %{_libdir}/gio/modules
gio-querymodules-%{__isa_bits} %{_libdir}/gio/modules &> /dev/null || :

%transfiletriggerin -- %{_datadir}/glib-2.0/schemas
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%transfiletriggerpostun -- %{_datadir}/glib-2.0/schemas
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
%endif

%files -f glib20.lang
%license COPYING
%doc AUTHORS NEWS README
%if !0%{?os2_version}
%{_libdir}/libglib-2.0.so.*
%{_libdir}/libgthread-2.0.so.*
%{_libdir}/libgmodule-2.0.so.*
%{_libdir}/libgobject-2.0.so.*
%{_libdir}/libgio-2.0.so.*
%else
%{_libdir}/glib2*.dll
%{_libdir}/gthr2*.dll
%{_libdir}/gmod2*.dll
%{_libdir}/gobj2*.dll
%{_libdir}/gio2*.dll
%endif
%dir %{_datadir}/bash-completion
%dir %{_datadir}/bash-completion/completions
%{_datadir}/bash-completion/completions/gapplication
%{_datadir}/bash-completion/completions/gdbus
%{_datadir}/bash-completion/completions/gio
%{_datadir}/bash-completion/completions/gsettings
%dir %{_datadir}/glib-2.0
%dir %{_datadir}/glib-2.0/schemas
%dir %{_libdir}/gio
%dir %{_libdir}/gio/modules
%ghost %{_libdir}/gio/modules/giomodule.cache
%if !0%{?os2_version}
%{_bindir}/gio
%{_bindir}/gio-launch-desktop
%{_bindir}/gio-querymodules*
%{_bindir}/glib-compile-schemas
%{_bindir}/gsettings
%{_bindir}/gdbus
%{_bindir}/gapplication
%else
%{_bindir}/gio.exe
%{_bindir}/gio-launch-desktop.exe
%{_bindir}/gio-querymodules.exe
%{_bindir}/glib-compile-schemas.exe
%{_bindir}/gsettings.exe
%{_bindir}/gdbus.exe
%{_bindir}/gapplication.exe
%endif
%{_mandir}/man1/gio.1*
%{_mandir}/man1/gio-querymodules.1*
%{_mandir}/man1/glib-compile-schemas.1*
%{_mandir}/man1/gsettings.1*
%{_mandir}/man1/gdbus.1*
%{_mandir}/man1/gapplication.1*

%files devel
%if !0%{?os2_version}
%{_libdir}/lib*.so
%else
%{_libdir}/*_dll.a
%endif
%{_libdir}/glib-2.0
%{_includedir}/*
%{_datadir}/aclocal/*
%{_libdir}/pkgconfig/*
%{_datadir}/glib-2.0/gdb
%{_datadir}/glib-2.0/gettext
%{_datadir}/glib-2.0/schemas/gschema.dtd
%{_datadir}/glib-2.0/valgrind/glib.supp
%{_datadir}/bash-completion/completions/gresource
%{_bindir}/glib-genmarshal
%{_bindir}/glib-gettextize
%{_bindir}/glib-mkenums
%if !0%{?os2_version}
%{_bindir}/gobject-query
%{_bindir}/gtester
%else
%{_bindir}/gobject-query.exe
%{_bindir}/gtester.exe
%endif
%{_bindir}/gdbus-codegen
%if !0%{?os2_version}
%{_bindir}/glib-compile-resources
%{_bindir}/gresource
%else
%{_bindir}/glib-compile-resources.exe
%{_bindir}/gresource.exe
%endif
%{_datadir}/glib-2.0/codegen
%attr (0755, root, root) %{_bindir}/gtester-report
%{_mandir}/man1/glib-genmarshal.1*
%{_mandir}/man1/glib-gettextize.1*
%{_mandir}/man1/glib-mkenums.1*
%{_mandir}/man1/gobject-query.1*
%{_mandir}/man1/gtester-report.1*
%{_mandir}/man1/gtester.1*
%{_mandir}/man1/gdbus-codegen.1*
%{_mandir}/man1/glib-compile-resources.1*
%{_mandir}/man1/gresource.1*
%{_datadir}/gdb/
%{_datadir}/gettext/
%if !0%{?os2_version}
%{_datadir}/systemtap/
%endif

%files doc
%if !0%{?os2_version}
%doc %{_datadir}/gtk-doc/html/*
%endif

%if !0%{?os2_version}
%files fam
%{_libdir}/gio/modules/libgiofam.so
%endif

%files static
%if !0%{?os2_version}
%{_libdir}/libgio-2.0.a
%{_libdir}/libglib-2.0.a
%{_libdir}/libgmodule-2.0.a
%{_libdir}/libgobject-2.0.a
%{_libdir}/libgthread-2.0.a
%else
%{_libdir}/gio-2.0.a
%{_libdir}/glib-2.0.a
%{_libdir}/gmodule-2.0.a
%{_libdir}/gobject-2.0.a
%{_libdir}/gthread-2.0.a
%endif

%files tests
%{_libexecdir}/installed-tests
%if 0%{?os2_version}
%exclude %{_libexecdir}/installed-tests/glib/*.dbg
%exclude %{_libexecdir}/installed-tests/glib/modules/*.dbg
%exclude %{_libexecdir}/installed-tests/glib/x-content/*/*.dbg
%endif
%{_datadir}/installed-tests

%changelog
* Mon Oct 27 2025 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.58.3-1
- update to version 2.58.3

* Thu Nov 11 2021 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.46.2-2
- provide libgio to force update as well

* Wed Nov 10 2021 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.46.2-1
- update to version 2.46.2
- resync with fedora spec

* Tue Aug 21 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.33.12-3
- rebuild with latest tool chain
- use new scm_ macros
- use libcx
- remove legacy package

* Tue Jul 05 2016 yd <yd@os2power.com> 2.33.12-2
- r1643, use gettext code to embed codepage aliases. ticket#14.

* Sat Jun 18 2016 yd <yd@os2power.com> 2.33.12-1
- r1605, use ISO8859-1 as default mapping, added _EURO locales.
- add legacy package for 2.25 compatibility.
- build public version.

* Wed Jan 27 2016 Dmitriy Kuminov <coding@dmik.org> 2.25.15-5
- Remove .la files from distribution.
- Build with gcc-4.9.2 against libc-0.6.6.
- Switch to downloading sources from SVN.

* Wed Jul 18 2012 yd
- include Dmitry's changes for OpenJDK build.
