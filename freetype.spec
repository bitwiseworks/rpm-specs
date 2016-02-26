Summary: A free and portable font rendering engine
Name: freetype
Version: 2.6.3
Release: 1%{?dist}
License: (FTL or GPLv2+) and BSD and MIT and Public Domain and zlib with acknowledgement
Group: System Environment/Libraries
URL: http://www.freetype.org
Vendor: bww bitwise works GmbH
#Source:  http://download.savannah.gnu.org/releases/freetype/freetype-%{version}.tar.bz2
#Source1: http://download.savannah.gnu.org/releases/freetype/freetype-doc-%{version}.tar.bz2
#Source2: http://download.savannah.gnu.org/releases/freetype/ft2demos-%{version}.tar.bz2
#define svn_url	    e:/trees/freetype/trunk
%define svn_url     http://svn.netlabs.org/repos/ports/freetype2/trunk
%define svn_rev     1338

Source: %{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip

BuildRoot: %{tmpdir}/%{name}-%{version}-root-%(id -u -n)

BuildRequires: libpng-devel
BuildRequires: zlib-devel

Provides: %{name}-bytecode

%description
The FreeType engine is a free and portable font rendering
engine, developed to provide advanced font support for a variety of
platforms and environments. FreeType is a library which can open and
manages font files as well as efficiently load, hint and render
individual glyphs. FreeType is not a font server or a complete
text-rendering library.


#%package demos
#Summary: A collection of FreeType demos
#Group: System Environment/Libraries
#Requires: %{name} = %{version}-%{release}

#%description demos
#The FreeType engine is a free and portable font rendering
#engine, developed to provide advanced font support for a variety of
#platforms and environments.  The demos package includes a set of useful
#small utilities showing various capabilities of the FreeType library.


%package devel
Summary: FreeType development libraries and header files
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: libpng-devel

%description devel
The freetype-devel package includes the static libraries and header files
for the FreeType font rendering engine.

Install freetype-devel if you want to develop programs which will use
FreeType.

%debug_package

%prep
%if %{?svn_rev:%(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')}%{?!svn_rev):0}
%setup -q
%else
%setup -n "%{name}-%{version}" -Tc
svn export %{?svn_rev:-r %{svn_rev}} %{svn_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip" "%{name}-%{version}")
%endif
autogen.sh

%build
rm -f config.mk 
export LDFLAGS=" -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
%configure --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

%makeinstall gnulocaledir=$RPM_BUILD_ROOT%{_datadir}/locale

# Don't package static a or .la files
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.la


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_libdir}/freetyp*.dll
%doc README
%doc docs/LICENSE.TXT docs/FTL.TXT docs/GPLv2.TXT
%doc docs/CHANGES docs/formats.txt


#%files demos
#%defattr(-,root,root)
#%{_bindir}/ftbench
#%{_bindir}/ftchkwd
#%{_bindir}/ftmemchk
#%{_bindir}/ftpatchk
#%{_bindir}/fttimer
#%{_bindir}/ftdump
#%{_bindir}/ftlint
#%{_bindir}/ftmemchk
#%{_bindir}/ftvalid
#%doc ChangeLog README


%files devel
%defattr(-,root,root)
%dir %{_includedir}/freetype2
%{_datadir}/aclocal/freetype2.m4
%{_includedir}/freetype2/*
%{_libdir}/freetype*.a
%{_bindir}/freetype-config
%{_libdir}/pkgconfig/freetype2.pc
%doc docs/reference
%doc docs/VERSION.DLL
%{_mandir}/man1/*


%changelog
* Fri Feb 26 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.6.3-1
- updated source to 2.6.3
- added -Zhigh-mem

* Thu Dec 29 2015 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.6.2-1
- updated source to 2.6.2
- moved docs/version.dll to -devel
- adjusted debug package creation to latest rpm macros

* Wed Feb 11 2015 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.5.5-1
- updated source to 2.5.5
- added .dbg files

* Mon Oct 6 2014 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.5.3-1
- first version
