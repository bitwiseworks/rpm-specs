#define svn_url     F:/rd/ports/ghostscript/trunk
%define svn_url     http://svn.netlabs.org/repos/ports/ghostscript/trunk
%define svn_rev     941

%define _with_freetype 1
%define gs_ver 9.10
%define gs_dot_ver 9.10
%{expand: %%define build_with_freetype %{?_with_freetype:1}%{!?_with_freetype:0}}

Summary: A PostScript interpreter and renderer
Name: ghostscript
Version: %{gs_ver}

Release: 3%{?dist}

# Included CMap data is Redistributable, no modification permitted,
# see http://bugzilla.redhat.com/487510
License: GPLv3+ and Redistributable, no modification permitted
URL: http://www.ghostscript.com/
Group: Applications/Publishing

Source: %{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip

Requires: urw-fonts >= 1.1, ghostscript-fonts
Requires: poppler-data
BuildRequires: xz
BuildRequires: libjpeg-devel
BuildRequires: zlib-devel, libpng-devel, unzip
BuildRequires: glib2-devel
# Omni requires libxml
BuildRequires: libxml2-devel
BuildRequires: libtiff-devel
#BuildRequires: cups-devel >= 1.1.13
BuildRequires: libtool
#BuildRequires: jasper-devel, gnutls-devel
#BuildRequires: dbus-devel
BuildRequires: poppler-data
#BuildRequires: lcms2-devel
#BuildRequires: openjpeg-devel
%{?_with_freetype:BuildRequires: freetype-devel}
BuildRoot: %{_tmppath}/%{name}-%{gs_ver}-root

# See bug #83516.
Conflicts: ttfonts-ja < 1.2-23
Conflicts: ttfonts-ko < 1.0.11-27
Conflicts: ttfonts-zh_CN < 2.12-2
Conflicts: ttfonts-zh_TW < 2.11-20

%description
Ghostscript is a set of software that provides a PostScript
interpreter, a set of C procedures (the Ghostscript library, which
implements the graphics capabilities in the PostScript language) and
an interpreter for Portable Document Format (PDF) files. Ghostscript
translates PostScript code into many common, bitmapped formats, like
those understood by your printer or screen. Ghostscript is normally
used to display PostScript files and to print PostScript files to
non-PostScript printers.

If you need to display PostScript files or print them to
non-PostScript printers, you should install ghostscript. If you
install ghostscript, you also need to install the ghostscript-fonts
package.

%package devel
Summary: Files for developing applications that use ghostscript
Requires: %{name} = %{version}-%{release}
Group: Development/Libraries

%description devel
The header files for developing applications that use ghostscript.

%package doc
Summary: Documentation for ghostscript
Requires: %{name} = %{version}-%{release}
Group: Documentation
BuildArch: noarch

%description doc
The documentation files that come with ghostscript.

%package gtk
Summary: A GTK-enabled PostScript interpreter and renderer
Requires: %{name} = %{version}-%{release}
Group: Applications/Publishing

%description gtk
A GTK-enabled version of Ghostscript, called 'gsx'.

%package cups
Summary: CUPS filter for interpreting PostScript and PDF
Requires: %{name} = %{version}-%{release}
Requires: cups
Group: System Environment/Daemons

%description cups
CUPS filter and conversion rules for interpreting PostScript and PDF.

%package debug
Summary: HLL debug data for exception handling support.

%description debug
HLL debug data for exception handling support.

%prep
%if %{?svn_rev:%(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')}%{!?svn_rev):0}
%setup -q
%else
%setup -n "%{name}-%{version}" -Tc
svn export %{?svn_rev:-r %{svn_rev}} %{svn_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip" "%{name}-%{version}")
%endif

#rm -rf expat freetype icclib jasper jpeg lcms2 libpng openjpeg zlib cups/libs
rm -rf expat freetype jpeg libpng zlib cups/libs



# Convert manual pages to UTF-8
#from8859_1() {
#        iconv -f iso-8859-1 -t utf-8 < "$1" > "${1}_"
#        mv "${1}_" "$1"
#}
#for i in man/de/*.1; do
#  if [ "$(file --brief --mime-encoding "$i")" = iso-8859-1 ]; then
#    from8859_1 "$i"
#  fi
#done

# Convert ps files to UTF-8
#for i in examples/cjk/gsc*.ps; do from8859_1 "$i"; done

%build
# Compile without strict aliasing opts due to these files:
# gdevescv.c gdevl4v.c gdevopvp.c gdevbbox.c gdevdbit.c gdevddrw.c 
# gdevp14.c gdevpdfd.c gdevpdfi.c gdevpdfo.c gdevpdft.c gdevpdfv.c 
# gdevpdte.c gdevpdtt.c gdevps.c gdevpx.c gscoord.c gscparam.c gscrd.c 
# gsdps1.c gsimage.c gspath1.c gsptype1.c gsptype2.c gstype2.c 
# gstype42.c gxccache.c gxchar.c gxclimag.c gxclpath.c gxfcopy.c 
# gximag3x.c gximage3.c gxipixel.c gxshade1.c gxstroke.c gxtype1.c 
# ibnum.c iscanbin.c zchar1.c zchar.c zcharx.c zfapi.c zfont32.c 
# zfunc0.c zfunc3.c zfunc4.c zpcolor.c zshade.c
EXTRACFLAGS="-fno-strict-aliasing"

FONTPATH=
for path in \
        /@system_drive/psfonts \
        /@system_drive/os2/psfonts \
        %{_datadir}/fonts/default/%{name} \
        %{_datadir}/fonts/default/Type1 \
        %{_datadir}/fonts/default/amspsfnt/pfb \
        %{_datadir}/fonts/default/cmpsfont/pfb \
        %{_datadir}/fonts \
        %{_datadir}/%{name}/conf.d \
        %{_sysconfdir}/%{name} \
        %{_sysconfdir}/%{name}/%{gs_dot_ver} \
        %{_datadir}/poppler/cMap/*
do
  FONTPATH="$FONTPATH${FONTPATH:+;}$path"
done

#autoconf --force
# --with-ijs --enable-dynamic
export CONFIG_SITE="/@unixroot/usr/share/config.legacy";
export CONFIG_SHELL="/@unixroot/usr/bin/sh.exe";
%configure --with-fontpath="$FONTPATH" \
        --with-drivers=ALL --disable-compile-inits \
        CFLAGS="$CFLAGS $EXTRACFLAGS"

# Build IJS
#cd ijs
#./autogen.sh
#configure --enable-shared --disable-static
#make
#cd ..

%if %{build_with_freetype}
FT_CFLAGS=$(pkg-config --cflags freetype2)
make so RPM_OPT_FLAGS="$RPM_OPT_FLAGS $EXTRACFLAGS" prefix=%{_prefix} \
        FT_BRIDGE=1 FT_CFLAGS="$FT_CFLAGS" FT_LIB=freetype
%else
make so RPM_OPT_FLAGS="$RPM_OPT_FLAGS $EXTRACFLAGS" prefix=%{_prefix}
%endif
#make cups

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_mandir}
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
mkdir -p $RPM_BUILD_ROOT/%{_datadir}
mkdir -p $RPM_BUILD_ROOT/%{_docdir}
mkdir -p $RPM_BUILD_ROOT/%{_libdir}
mkdir -p $RPM_BUILD_ROOT/%{_includedir}/ijs

make soinstall \
%{?_with_freetype:FT_BRIDGE=1} \
        prefix=$RPM_BUILD_ROOT%{_prefix} \
        mandir=$RPM_BUILD_ROOT%{_mandir} \
        datadir=$RPM_BUILD_ROOT%{_datadir} \
        gsincludedir=$RPM_BUILD_ROOT%{_includedir}/ghostscript/ \
        bindir=$RPM_BUILD_ROOT%{_bindir} \
        libdir=$RPM_BUILD_ROOT%{_libdir} \
        docdir=$RPM_BUILD_ROOT%{_docdir}/%{name}-%{gs_dot_ver} \
        gsdir=$RPM_BUILD_ROOT%{_datadir}/%{name} \
        gsdatadir=$RPM_BUILD_ROOT%{_datadir}/%{name}/%{gs_dot_ver} \
        gssharedir=$RPM_BUILD_ROOT%{_libdir}/%{name}/%{gs_dot_ver} \
        CUPSSERVERROOT=$RPM_BUILD_ROOT`cups-config --serverroot` \
        CUPSSERVERBIN=$RPM_BUILD_ROOT`cups-config --serverbin` \
        CUPSDATA=$RPM_BUILD_ROOT`cups-config --datadir`

mv -f $RPM_BUILD_ROOT%{_bindir}/gsc.exe $RPM_BUILD_ROOT%{_bindir}/gsos2.exe
# add symlink for scripts
ln -s %{_bindir}/gsos2.exe %{buildroot}%{_bindir}/gs.exe
rm -f $RPM_BUILD_ROOT%{_libdir}/gsdll2.%{gs_dot_ver}.dll

#cd ijs
#makeinstall
#cd ..

echo ".so man1/gs.1" > $RPM_BUILD_ROOT/%{_mandir}/man1/ghostscript.1
ln -sf gs $RPM_BUILD_ROOT%{_bindir}/ghostscript

# Rename an original cidfmap to cidfmap.GS
#mv $RPM_BUILD_ROOT%{_datadir}/%{name}/%{gs_dot_ver}/Resource/Init/cidfmap $RPM_BUILD_ROOT%{_datadir}/%{name}/%{gs_dot_ver}/Resource/Init/cidfmap.GS
# Install our own cidfmap to allow the separated
# cidfmap which the font packages own.
#install -m0644 %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/%{name}/%{gs_dot_ver}/Resource/Init/CIDFnmap
#install -m0644 %{SOURCE4} $RPM_BUILD_ROOT%{_datadir}/%{name}/%{gs_dot_ver}/Resource/Init/cidfmap

# Documentation
install -m0644 doc/COPYING $RPM_BUILD_ROOT%{_docdir}/%{name}-%{gs_dot_ver}

# Don't ship libtool la files.
rm -f $RPM_BUILD_ROOT%{_libdir}/libijs.la

# Don't ship ijs example client or server
rm -f $RPM_BUILD_ROOT%{_bindir}/ijs_{client,server}_example

# Don't ship URW fonts; we already have them.
#rm -rf $RPM_BUILD_ROOT%{_datadir}/ghostscript/%{gs_dot_ver}/Resource/Font

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/ghostscript/%{gs_dot_ver}
touch $RPM_BUILD_ROOT%{_sysconfdir}/ghostscript/%{gs_dot_ver}/Fontmap.local
touch $RPM_BUILD_ROOT%{_sysconfdir}/ghostscript/%{gs_dot_ver}/cidfmap.local
touch $RPM_BUILD_ROOT%{_sysconfdir}/ghostscript/%{gs_dot_ver}/CIDFnmap.local

# The man/de/man1 symlinks are broken (bug #66238).
find $RPM_BUILD_ROOT%{_mandir}/de/man1 -type l | xargs rm -f

# Don't ship fixmswrd.pl as it pulls in perl (bug #463948).
rm -f $RPM_BUILD_ROOT%{_bindir}/fixmswrd.pl

# Don't ship CMaps (instead poppler-data paths are in search path).
rm -f $RPM_BUILD_ROOT%{_datadir}/ghostscript/%{gs_dot_ver}/Resource/CMap/*

MAIN_PWD=`pwd`
(cd $RPM_BUILD_ROOT; find .%{_datadir}/ghostscript/%{gs_dot_ver}/Resource -type f | \
                sed -e 's/\.//;' | grep -v Fontmap | grep -v gs_init.ps > $MAIN_PWD/rpm.sharelist
 find .%{_bindir}/ | sed -e 's/\.//;' | \
                grep -v '/$\|/hpijs$\|/gsx$\|/ijs-config$' \
                >> $MAIN_PWD/rpm.sharelist)


%clean
rm -rf $RPM_BUILD_ROOT

#%post -p /sbin/ldconfig

#%postun -p /sbin/ldconfig

%files -f rpm.sharelist
%defattr(-,root,root)
%dir %{_sysconfdir}/ghostscript
%dir %{_sysconfdir}/ghostscript/%{gs_dot_ver}
%dir %{_datadir}/ghostscript/%{gs_dot_ver}
%dir %{_datadir}/ghostscript/%{gs_dot_ver}/Resource
%dir %{_datadir}/ghostscript/%{gs_dot_ver}/Resource/Init
%config %{_datadir}/ghostscript/%{gs_dot_ver}/Resource/Init/gs_init.ps
%config %{_datadir}/ghostscript/%{gs_dot_ver}/Resource/Init/Fontmap*
%dir %{_datadir}/ghostscript/%{gs_dot_ver}/Resource/CMap
%dir %{_datadir}/ghostscript/%{gs_dot_ver}/Resource/ColorSpace
%dir %{_datadir}/ghostscript/%{gs_dot_ver}/Resource/Decoding
%dir %{_datadir}/ghostscript/%{gs_dot_ver}/Resource/Encoding
%dir %{_datadir}/ghostscript/%{gs_dot_ver}/Resource/SubstCID
%{_datadir}/ghostscript/%{gs_dot_ver}/lib
%{_datadir}/ghostscript/%{gs_dot_ver}/iccprofiles
%{_mandir}/man*/*
%lang(de) %{_mandir}/de/man*/*
%{_libdir}/gsdll2.dll
#%{_libdir}/libijs-*.so*
#%dir %{_libdir}/%{name}
#%{_libdir}/%{name}/%{gs_dot_ver}
%config(noreplace) %{_sysconfdir}/ghostscript/%{gs_dot_ver}/*

%files doc
%defattr(-,root,root)
%doc %{_datadir}/ghostscript/%{gs_dot_ver}/examples
%doc %{_docdir}/%{name}-%{gs_dot_ver}

%files gtk
%defattr(-,root,root)
%{_bindir}/gsx.exe

%files cups
%defattr(-,root,root)
#%{_datadir}/cups/model/pxl*
#%{_datadir}/cups/mime/*.convs
#%{_cups_serverbin}/filter/*

%files devel
%defattr(-,root,root)
%dir %{_includedir}/ghostscript
%{_includedir}/ghostscript/*.h
#%dir %{_includedir}/ijs
#%{_includedir}/ijs/*
#%{_bindir}/ijs-config
#%{_libdir}/pkgconfig/ijs.pc
#%{_libdir}/libijs.so
%{_libdir}/gs.a
%{_libdir}/gs.lib

%files debug
%defattr(-,root,root)
%{_bindir}/*.dbg
%{_libdir}/*.dbg

%changelog
* Tue Dec 16 2014 yd
- r937, r941, fix FONTPATH handling, add PSFONTS dir.

* Fri Dec 12 2014 yd
- initial unixroot build.