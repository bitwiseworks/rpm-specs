# no demos atm
%global with_demos 0
# no mmap support atm, enable it with the next version again!!!
%global without_mmap 1

# no utf8 conversion
%global with_convert 0

Summary: A free and portable font rendering engine
Name: freetype
Version: 2.10.0
Release: 2%{?dist}
License: (FTL or GPLv2+) and BSD and MIT and Public Domain and zlib with acknowledgement
Group: System Environment/Libraries
URL: http://www.freetype.org

Vendor: bww bitwise works GmbH
%scm_source  github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2
Source1: http://download.savannah.gnu.org/releases/freetype/freetype-doc-%{version}.tar.bz2
%if %{with_demos}
Source2: http://download.savannah.gnu.org/releases/freetype/ft2demos-%{version}.tar.bz2
%endif

BuildRequires: gcc
BuildRequires: libpng-devel
BuildRequires: zlib-devel
BuildRequires: bzip2-devel
BuildRequires: pkgconfig

Provides: %{name}-bytecode
Provides: %{name}-subpixel

%description
The FreeType engine is a free and portable font rendering
engine, developed to provide advanced font support for a variety of
platforms and environments. FreeType is a library which can open and
manages font files as well as efficiently load, hint and render
individual glyphs. FreeType is not a font server or a complete
text-rendering library.


%if %{with_demos}
%package demos
Summary: A collection of FreeType demos
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}

%description demos
The FreeType engine is a free and portable font rendering
engine, developed to provide advanced font support for a variety of
platforms and environments.  The demos package includes a set of useful
small utilities showing various capabilities of the FreeType library.
%endif

%package devel
Summary: FreeType development libraries and header files
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
The freetype-devel package includes the static libraries and header files
for the FreeType font rendering engine.

Install freetype-devel if you want to develop programs which will use
FreeType.

%debug_package

%prep
%scm_setup
%setup -T -D -b 1
autogen.sh

%build
rm -f config.mk 
export LDFLAGS=" -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"
export VENDOR="%{vendor}"
%configure --disable-static \
%if %{without_mmap}
           --disable-mmap \
%endif
           --with-zlib=yes \
           --with-bzip2=yes \
           --with-png=yes \
           --with-harfbuzz=no \
           --enable-freetype-config

make %{?_smp_mflags}

%if %{with_demos}
# Build demos
pushd ft2demos-%{version}
make TOP_DIR=".."	
popd
%endif

%if %{with_convert}
# Convert FTL.txt and example3.cpp to UTF-8
cd docs	
iconv -f latin1 -t utf-8 < FTL.TXT > FTL.TXT.tmp && \	
touch -r FTL.TXT FTL.TXT.tmp && \
mv FTL.TXT.tmp FTL.TXT

iconv -f iso-8859-1 -t utf-8 < "tutorial/example3.cpp" > "tutorial/example3.cpp.utf8"
touch -r tutorial/example3.cpp tutorial/example3.cpp.utf8 && \
mv tutorial/example3.cpp.utf8 tutorial/example3.cpp
cd ..
%endif


%install

%make_install gnulocaledir=$RPM_BUILD_ROOT%{_datadir}/locale

%if %{with_demos}
{
  for ftdemo in ftbench ftchkwd ftmemchk ftpatchk fttimer ftdump ftlint ftmemchk ftvalid ; do
      builds/unix/libtool --mode=install install -m 755 ft2demos-%{version}/bin/$ftdemo $RPM_BUILD_ROOT/%{_bindir}
  done
}

{
  for ftdemo in ftdiff ftgamma ftgrid ftmulti ftstring fttimer ftview ; do
      builds/unix/libtool --mode=install install -m 755 ft2demos-%{version}/bin/$ftdemo $RPM_BUILD_ROOT/%{_bindir}
  done
}
%endif
	
# Don't package static a or .la files
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.la


%files
%{!?_licensedir:%global license %%doc}
%license docs/LICENSE.TXT docs/FTL.TXT docs/GPLv2.TXT
%{_libdir}/freetyp*.dll
%doc README
%doc docs/VERSIONS.TXT


%if %{with_demos}
%files demos
%{_bindir}/ftbench
%{_bindir}/ftchkwd
%{_bindir}/ftmemchk
%{_bindir}/ftpatchk
%{_bindir}/fttimer
%{_bindir}/ftdump
%{_bindir}/ftlint
%{_bindir}/ftvalid
%doc ChangeLog README
%endif


%files devel
%doc docs/CHANGES docs/formats.txt docs/ft2faq.html
%dir %{_includedir}/freetype2
%{_datadir}/aclocal/freetype2.m4
%{_includedir}/freetype2/*
%{_libdir}/freetype*_dll.a
%{_bindir}/freetype-config
%{_libdir}/pkgconfig/freetype2.pc
%doc docs/design
%doc docs/glyphs
%doc docs/reference
%doc docs/tutorial
%{_mandir}/man1/*


%changelog
* Fri May 24 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.10.0-2
- disable mmap for now, as there is still way to much dumb old software around

* Fri May 24 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.10.0-1
- updated source to 2.10.0
- moved source to github
- adjusted spec according to fedora
- deliver docs as well

* Wed Aug 09 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.8.0-1
- updated source to 2.8.0

* Wed Mar 01 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.7.1-1
- updated source to 2.7.1
- use new scm_ macros
- add bldlevel info

* Tue Oct 25 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.7.0-1
- updated source to 2.7.0
- as VERSION.DLL is renamed to VERSIONS.TXT its moved to primary package again

* Fri Feb 26 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.6.3-1
- updated source to 2.6.3
- added -Zhigh-mem

* Tue Dec 29 2015 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.6.2-1
- updated source to 2.6.2
- moved docs/version.dll to -devel
- adjusted debug package creation to latest rpm macros

* Wed Feb 11 2015 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.5.5-1
- updated source to 2.5.5
- added .dbg files

* Mon Oct 6 2014 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.5.3-1
- first version
