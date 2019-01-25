Summary:         A library for handling different graphics file formats
Name:            netpbm
Version:         10.84.01
Release:         1%{?dist}
# See copyright_summary for details
License:         BSD and GPLv2 and IJG and MIT and Public Domain
URL: http://netpbm.sourceforge.net/

Vendor: bww bitwise works GmbH
%scm_source github https://github.com/bitwiseworks/%{name}-os2 %{version}-os2
# https://svn.code.sf.net/p/netpbm/code/advanced netpbm-%%{version}
# https://svn.code.sf.net/p/netpbm/code/userguide netpbm-%%{version}/userguide

BuildRequires:   libjpeg-devel, libpng-devel, libtiff-devel, flex, gcc
BuildRequires:   perl-generators, python, libxml2-devel
#BuildRequires:   libX11-devel, python3, jasper-devel
BuildRequires:   ghostscript
#Provides:        bundled(jasper), bundled(jbigkit)

%description
The netpbm package contains a library of functions which support
programs for handling various graphics file formats, including .pbm
(portable bitmaps), .pgm (portable graymaps), .pnm (portable anymaps),
.ppm (portable pixmaps) and others.

%package devel
Summary:         Development tools for programs which will use the netpbm libraries
Requires:        netpbm = %{version}-%{release}

%description devel
The netpbm-devel package contains the header files and static libraries,
etc., for developing programs which can handle the various graphics file
formats supported by the netpbm libraries.

Install netpbm-devel if you want to develop programs for handling the
graphics file formats supported by the netpbm libraries.  You'll also need
to have the netpbm package installed.

%package progs
Summary:         Tools for manipulating graphics files in netpbm supported formats
Requires:        ghostscript
Requires:        netpbm = %{version}-%{release}

%description progs
The netpbm-progs package contains a group of scripts for manipulating the
graphics files in formats which are supported by the netpbm libraries.  For
example, netpbm-progs includes the rasttopnm script, which will convert a
Sun rasterfile into a portable anymap.  Netpbm-progs contains many other
scripts for converting from one graphics file format to another.

If you need to use these conversion scripts, you should install
netpbm-progs.  You'll also need to install the netpbm package.

%package doc
Summary:         Documentation for tools manipulating graphics files in netpbm supported formats
Requires:        netpbm-progs = %{version}-%{release}

%description doc
The netpbm-doc package contains a documentation in HTML format for utilities
present in netpbm-progs package.

If you need to look into the HTML documentation, you should install
netpbm-doc.  You'll also need to install the netpbm-progs package.

%debug_package

%prep
%scm_setup

%build
./configure <<EOF

os2


n


jpeg8.dll

tiff5.dll

z.dll

none





EOF

TOP=`pwd`

make \
	LADD="-lcx" \
        VENDOR="%{vendor}"

# prepare man files
cd userguide
rm -f *.manual-pages
rm -f *.manfix
for i in *.html ; do
  ../buildtools/makeman ${i}
done
for i in 1 3 5 ; do
  mkdir -p man/man${i}
  mv *.${i} man/man${i}
done


%install
make package pkgdir=%{buildroot}/@unixroot/usr LINUXSVGALIB="NONE" XML2LIBS="NONE"

mkdir -p %{buildroot}%{_datadir}
mv userguide/man %{buildroot}%{_mandir}

# Get rid of the useless non-ascii character in pgmminkowski.1
sed -i 's/\xa0//' %{buildroot}%{_mandir}/man1/pgmminkowski.1

# Don't ship man pages for non-existent binaries and bogus ones
for i in hpcdtoppm \
	 ppmsvgalib vidtoppm picttoppm \
	 directory error extendedopacity \
	 pam pbm pgm pnm ppm index libnetpbm_dir \
	 liberror ppmtotga; do
	rm -f %{buildroot}%{_mandir}/man1/${i}.1
done
rm -f %{buildroot}%{_mandir}/man5/extendedopacity.5

mkdir -p %{buildroot}%{_datadir}/netpbm
mv %{buildroot}/@unixroot/usr/misc/*.map %{buildroot}%{_datadir}/netpbm/
mv %{buildroot}/@unixroot/usr/misc/rgb.txt %{buildroot}%{_datadir}/netpbm/
rm -rf %{buildroot}/@unixroot/usr/README
rm -rf %{buildroot}/@unixroot/usr/VERSION
rm -rf %{buildroot}/@unixroot/usr/link
rm -rf %{buildroot}/@unixroot/usr/misc
rm -rf %{buildroot}/@unixroot/usr/man
rm -rf %{buildroot}/@unixroot/usr/pkginfo
rm -rf %{buildroot}/@unixroot/usr/config_template
rm -rf %{buildroot}/@unixroot/usr/pkgconfig_template

#%ldconfig_scriptlets

%check
#pushd test
#export LD_LIBRARY_PATH=%{buildroot}%{_libdir}
#export PBM_TESTPREFIX=%{buildroot}%{_bindir}
#export PBM_BINPREFIX=%{buildroot}%{_bindir}
#./Execute-Tests && exit 0
#popd

%files
%doc doc/copyright_summary doc/COPYRIGHT.PATENT doc/HISTORY README
%license doc/GPL_LICENSE.txt
%{_libdir}/*.dll

%files devel
%dir %{_includedir}/netpbm
%{_includedir}/netpbm/*.h
%{_mandir}/man3/*
%{_libdir}/*_dll.a

%files progs
%{_bindir}/*
%exclude %{_bindir}/*.dbg
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_datadir}/netpbm/

%files doc
%doc userguide/*

%changelog
* Fri Oct 12 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> 10.84.01-1
- first rpm version
