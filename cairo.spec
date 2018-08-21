# Note: this .spec is borrowed from cairo-1.12.14-2.fc19.src.rpm

%define pixman_version 0.18.4
%define freetype_version 2.1.9
%define fontconfig_version 2.2.95

Summary:	A 2D graphics library
Name:		cairo
Version:	1.12.18
Release:	4%{?dist}
URL:		http://cairographics.org
#VCS:		git:git://git.freedesktop.org/git/cairo
#Source0:	http://cairographics.org/releases/%{name}-%{version}.tar.xz
License:	LGPLv2 or MPLv1.1
Group:		System Environment/Libraries
Vendor:         bww bitwise works GmbH

%scm_source  svn http://svn.netlabs.org/repos/ports/cairo/trunk 1578

BuildRequires: gcc make subversion zip

BuildRequires: pkgconfig
BuildRequires: libpng-devel
BuildRequires: libxml2-devel
BuildRequires: pixman-devel >= %{pixman_version}
BuildRequires: freetype-devel >= %{freetype_version}
BuildRequires: fontconfig-devel >= %{fontconfig_version}
BuildRequires: glib2-devel
#BuildRequires: librsvg2-devel
#BuildRequires: mesa-libGL-devel
#BuildRequires: mesa-libEGL-devel
BuildRequires: libcx-devel
BuildRequires: os2tk45-headers

%description
Cairo is a 2D graphics library designed to provide high-quality display
and print output. Currently supported output targets include the X Window
System, OpenGL (via glitz), in-memory image buffers, and image files (PDF,
PostScript, and SVG).

Cairo is designed to produce consistent output on all output media while
taking advantage of display hardware acceleration when available (e.g.
through the X Render Extension or OpenGL).

%package devel
Summary: Development files for cairo
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: libpng-devel
Requires: pixman-devel >= %{pixman_version}
Requires: freetype-devel >= %{freetype_version}
Requires: fontconfig-devel >= %{fontconfig_version}

%description devel
Cairo is a 2D graphics library designed to provide high-quality display
and print output.

This package contains libraries, header files and developer documentation
needed for developing software which uses the cairo graphics library.

%package gobject
Summary: GObject bindings for cairo
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}

%description gobject
Cairo is a 2D graphics library designed to provide high-quality display
and print output.

This package contains functionality to make cairo graphics library
integrate well with the GObject object system used by GNOME.

%package gobject-devel
Summary: Development files for cairo-gobject
Group: Development/Libraries
Requires: %{name}-devel = %{version}-%{release}
Requires: %{name}-gobject = %{version}-%{release}

%description gobject-devel
Cairo is a 2D graphics library designed to provide high-quality display
and print output.

This package contains libraries, header files and developer documentation
needed for developing software which uses the cairo Gobject library.

#%package tools
#Summary: Development tools for cairo
#Group: Development/Tools

#%description tools
#Cairo is a 2D graphics library designed to provide high-quality display
#and print output.
#
#This package contains tools for working with the cairo graphics library.
# * cairo-trace: Record cairo library calls for later playback

%debug_package

%prep
%scm_setup

# Generate confuigure and friends
NOCONFIGURE=1 autogen.sh

%build
# We can't add Toolkit includes in _INCS (it will casuse then to be searched
# before GCC headers and lead to conflicts), so use -idirafter.
export CPPFLAGS="-idirafter %{_includedir}/os2tk45 -DOS2EMX_PLAIN_CHAR"
export CPPFLAGS="$CPPFLAGS -DOS2_DYNAMIC_DIVE"
export LDFLAGS="-Zhigh-mem"
export LIBS="-lcx"
%configure --disable-static	\
	--enable-os2		\
	--enable-ft		\
	--enable-ps		\
	--enable-pdf		\
	--enable-svg		\
	--enable-tee		\
	--enable-gobject	\
	--disable-gtk-doc

#	--enable-gl

make V=1 %{?_smp_mflags}

%install
make install V=1 DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/*.la

%files
%doc AUTHORS BIBLIOGRAPHY BUGS COPYING COPYING-LGPL-2.1 COPYING-MPL-1.1 NEWS README
%{_libdir}/cairo?.dll
%{_libdir}/cairos?.dll
#%{_bindir}/cairo-sphinx

%files devel
%doc ChangeLog PORTING_GUIDE
%dir %{_includedir}/cairo/
%{_includedir}/cairo/cairo-deprecated.h
%{_includedir}/cairo/cairo-features.h
%{_includedir}/cairo/cairo-ft.h
%{_includedir}/cairo/cairo.h
%{_includedir}/cairo/cairo-pdf.h
%{_includedir}/cairo/cairo-ps.h
%{_includedir}/cairo/cairo-script-interpreter.h
%{_includedir}/cairo/cairo-svg.h
%{_includedir}/cairo/cairo-tee.h
%{_includedir}/cairo/cairo-version.h
%{_includedir}/cairo/cairo-os2.h
#%{_includedir}/cairo/cairo-gl.h
%{_includedir}/cairo/cairo-script.h
%{_libdir}/cairo_dll.a
%{_libdir}/cairo?_dll.a
%{_libdir}/cairo-script-interpreter_dll.a
%{_libdir}/cairo-script-interpreter?_dll.a
%{_libdir}/pkgconfig/cairo-fc.pc
%{_libdir}/pkgconfig/cairo-ft.pc
%{_libdir}/pkgconfig/cairo.pc
%{_libdir}/pkgconfig/cairo-pdf.pc
%{_libdir}/pkgconfig/cairo-png.pc
%{_libdir}/pkgconfig/cairo-ps.pc
%{_libdir}/pkgconfig/cairo-svg.pc
%{_libdir}/pkgconfig/cairo-tee.pc
%{_libdir}/pkgconfig/cairo-os2.pc
#%{_libdir}/pkgconfig/cairo-egl.pc
#%{_libdir}/pkgconfig/cairo-gl.pc
#%{_libdir}/pkgconfig/cairo-glx.pc
%{_libdir}/pkgconfig/cairo-script.pc
# @todo no docs for now as we need gtk-doc for them!
#%{_datadir}/gtk-doc/html/cairo

%files gobject
%{_libdir}/cairog?.dll

%files gobject-devel
%{_includedir}/cairo/cairo-gobject.h
%{_libdir}/cairo-gobject_dll.a
%{_libdir}/cairo-gobject?_dll.a
%{_libdir}/pkgconfig/cairo-gobject.pc

# @todo do we need it at all?
#%files tools
#%{_bindir}/cairo-trace
#%{_libdir}/cairo/

%changelog
* Tue Aug 21 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.12.18-4
- rebuild with latest tool chain
- use new scm_ macros
- use libcx

* Sat Jun 18 2016 yd <yd@os2power.com> 1.12.18-3
- rebuild for glib2 2.33.

* Thu May 26 2016 Dmitriy Kuminov <coding@dmik.org> 1.12.18-2
- Fix assertions and SIGABRT on application termination.

* Fri Feb 26 2016 Dmitriy Kuminov <coding@dmik.org> 1.12.18-1
- Update to version 1.12.18.

* Sat Feb 20 2016 Dmitriy Kuminov <coding@dmik.org> 1.12.0-1
- Initial package for version 1.12.0.
