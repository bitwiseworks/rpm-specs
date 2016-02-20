# Note: this .spec is borrowed from pango-1.28.4-1.fc15.src.rpm

%define glib2_base_version 2.17.3
%define glib2_version %{glib2_base_version}-1
%define pkgconfig_version 0.12
%define freetype_version 2.1.3-3
%define fontconfig_version 2.6
%define cairo_version 1.7.6
%define libthai_version 0.1.9

Summary: System for layout and rendering of internationalized text
Name: pango
Version: 1.28.4
Release: 1%{?dist}
License: LGPLv2+
Group: System Environment/Libraries
#VCS: git:git://git.gnome.org/pango
#Source: http://download.gnome.org/sources/pango/1.28/pango-%{version}.tar.bz2
URL: http://www.pango.org
Vendor:     bww bitwise works GmbH

%define svn_url     http://svn.netlabs.org/repos/ports/pango/trunk
%define svn_rev     1270

Source: %{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip

BuildRequires: gcc make subversion zip

Requires: glib2 >= %{glib2_version}
Requires: freetype >= %{freetype_version}
Requires: fontconfig >= %{fontconfig_version}
Requires: cairo >= %{cairo_version}
#Requires: libthai >= %{libthai_version}
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: pkgconfig >= %{pkgconfig_version}
BuildRequires: freetype-devel >= %{freetype_version}
BuildRequires: fontconfig-devel >= %{fontconfig_version}
BuildRequires: cairo-devel >= %{cairo_version}
#BuildRequires: libthai-devel >= %{libthai_version}
#BuildRequires: gobject-introspection-devel
BuildRequires: cairo-gobject-devel
# Bootstrap requirements
#BuildRequires: gnome-common intltool gtk-doc

%description
Pango is a library for laying out and rendering of text, with an emphasis
on internationalization. Pango can be used anywhere that text layout is needed,
though most of the work on Pango so far has been done in the context of the
GTK+ widget toolkit. Pango forms the core of text and font handling for GTK+.

Pango is designed to be modular; the core Pango layout engine can be used
with different font backends.

The integration of Pango with Cairo provides a complete solution with high
quality text handling and graphics rendering.

%package devel
Summary: Development files for pango
Group: Development/Libraries
Requires: pango = %{version}-%{release}
Requires: glib2-devel >= %{glib2_version}
Requires: freetype-devel >= %{freetype_version}
Requires: fontconfig-devel >= %{fontconfig_version}
Requires: cairo-devel >= %{cairo_version}
Requires: pkgconfig

%description devel
The pango-devel package includes the header files and developer documentation
for the pango package.

%prep
%if %{?svn_rev:%(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')}%{!?svn_rev):0}
%setup -q
%else
%setup -n "%{name}-%{version}" -Tc
svn export %{?svn_rev:-r %{svn_rev}} %{svn_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip" "%{name}-%{version}")
%endif


# Generate confuigure and friends
# @todo this requires gnome-autogen.sh from gnome-common, we won't have it soon
#NOCONFIGURE=1 autogen.sh
autoreconf -fvi

%build

export LDFLAGS="-Zhigh-mem"
export LIBS="-lurpo -lmmap -lpoll"
 %configure \
  --enable-man \
  --disable-gtk-doc
make %{?_smp_mflags}


%install

make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

# Remove files that should not be packaged
rm $RPM_BUILD_ROOT%{_libdir}/*.la
rm $RPM_BUILD_ROOT%{_libdir}/pango/*/modules/*.la


%files
%defattr(-, root, root,-)
%doc README AUTHORS COPYING NEWS
%doc pango-view/HELLO.txt
%{_libdir}/pang*.dll
%{_bindir}/pango-querymodules.exe
%{_bindir}/pango-view.exe
%{_mandir}/man1/pango-view.1.gz
%{_mandir}/man1/pango-querymodules.1.gz
%{_libdir}/pango
# @todo needs gobject-introspection
#%{_libdir}/girepository-1.0/Pango-1.0.typelib
#%{_libdir}/girepository-1.0/PangoCairo-1.0.typelib
#%{_libdir}/girepository-1.0/PangoFT2-1.0.typelib
#%{_libdir}/girepository-1.0/PangoXft-1.0.typelib


%files devel
%defattr(-, root, root,-)
%{_libdir}/pango*_dll.a
%{_includedir}/*
%{_libdir}/pkgconfig/*
# @todo no docs for now as we need gtk-doc for them!
#%doc %{_datadir}/gtk-doc/html/pango
# @todo needs gobject-introspection
#%{_datadir}/gir-1.0/Pango-1.0.gir
#%{_datadir}/gir-1.0/PangoCairo-1.0.gir
#%{_datadir}/gir-1.0/PangoFT2-1.0.gir
#%{_datadir}/gir-1.0/PangoXft-1.0.gir


%changelog
* Sat Feb 20 2016 Dmitriy Kuminov <coding@dmik.org> 1.28.4-1
- Initial package for version 1.28.4.
