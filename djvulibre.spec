#define svn_url     e:/trees/djvulibre/trunk
%define svn_url     http://svn.netlabs.org/repos/ports/djvulibre/trunk
%define svn_rev     1685


Summary: DjVu viewers, encoders, and utilities
Name: djvulibre
Version: 3.5.27
Release: 3%{?dist}
License: GPLv2+
Group: Applications/Publishing
URL: http://djvu.sourceforge.net/
Vendor:         bww bitwise works GmbH
Source:         %{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip

#Requires(post): xdg-utils
#Requires(preun): xdg-utils
BuildRequires: libjpeg-devel
BuildRequires: libtiff-devel
#BuildRequires: xdg-utils chrpath
#BuildRequires: hicolor-icon-theme
#BuildRequires: inkscape 
Requires: %{name}-libs = %{version}-%{release}

#Provides: %{name}-mozplugin = %{version}
#Obsoletes: %{name}-mozplugin < 3.5.24

%description
DjVu is a web-centric format and software platform for distributing documents
and images. DjVu can advantageously replace PDF, PS, TIFF, JPEG, and GIF for
distributing scanned documents, digital documents, or high-resolution pictures.
DjVu content downloads faster, displays and renders faster, looks nicer on a
screen, and consume less client resources than competing formats. DjVu images
display instantly and can be smoothly zoomed and panned with no lengthy
re-rendering.

DjVuLibre is a free (GPL'ed) implementation of DjVu, including viewers,
decoders, simple encoders, and utilities. The browser plugin is in its own
separate sub-package.


%package libs
Summary: Library files for DjVuLibre
Group: System Environment/Libraries

%description libs
Library files for DjVuLibre.


%package devel
Summary: Development files for DjVuLibre
Group: Development/Libraries
Requires: %{name}-libs = %{version}-%{release}
Requires: pkgconfig

%description devel
Development files for DjVuLibre.


%debug_package


%prep
%if %{?svn_rev:%(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')}%{!?svn_rev):0}
%setup -q
%else
%setup -n "%{name}-%{version}" -Tc
svn export %{?svn_rev:-r %{svn_rev}} %{svn_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip" "%{name}-%{version}")
%endif


%build 
export CFLAGS="$RPM_OPT_FLAGS -mstackrealign"
export CXXFLAGS="$RPM_OPT_FLAGS -mstackrealign"
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx0"
export NOCONFIGURE=1
autogen.sh


%configure --enable-shared --disable-static --disable-desktopfiles

make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}

# Remove libtool files, which reference the .dll libs
rm -f %{buildroot}%{_libdir}/*.la


#post


#preun


#postun


#posttrans


#post libs -p /sbin/ldconfig


#postun libs -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%{_bindir}/*.exe
%{_bindir}/any2djvu
%{_bindir}/djvudigital
%{_mandir}/man1/*
%{_datadir}/djvu/


%files libs
%defattr(-,root,root,-)
%doc README COPYRIGHT COPYING NEWS
%{_libdir}/*.dll


%files devel
%defattr(-,root,root,-)
%doc doc/*.*
%{_includedir}/libdjvu/
%{_libdir}/pkgconfig/ddjvuapi.pc
%{_libdir}/*_dll.a


%changelog
* Thu Sep 08 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.5.27-3
- fix a crash in the P4 build
- djvulibre also requires djvulibre-libs

* Tue Sep 06 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.5.27-2
- change all #ifdef OS2 to #ifdef __OS2__
- init pthread structure to prevent a sigsegv

* Fri Sep 02 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.5.27-1
- first version
