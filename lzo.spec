Name:           lzo
Version:        2.09
Release:        2%{?dist}
Summary:        Data compression library with very fast (de)compression
Group:          System Environment/Libraries
License:        GPLv2+
URL:            http://www.oberhumer.com/opensource/lzo/
Vendor: bww bitwise works GmbH

%define minilzo     mlzo22
#define svn_url     e:/trees/liblzo/trunk
%define svn_url     http://svn.netlabs.org/repos/ports/lzo/trunk
%define svn_rev     1084

Source: %{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip

BuildRequires:  zlib-devel

%description
LZO is a portable lossless data compression library written in ANSI C.
It offers pretty fast compression and very fast decompression.
Decompression requires no memory. In addition there are slower
compression levels achieving a quite competitive compression ratio
while still decompressing at this very high speed.


%package minilzo
Summary:        Mini version of lzo for apps which don't need the full version
Group:          System Environment/Libraries

%description minilzo
A small (mini) version of lzo for embedding into applications which don't need
full blown lzo compression support.


%package devel
Summary:        Development files for the lzo library
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-minilzo = %{version}-%{release}
Requires:       zlib-devel

%description devel
LZO is a portable lossless data compression library written in ANSI C.
It offers pretty fast compression and very fast decompression.
This package contains development files needed for lzo.


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

# hammer to nuke rpaths, recheck on new releases
autoreconf -f -i


%build
export LDFLAGS=" -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
%configure --disable-static --enable-shared

make %{?_smp_mflags}
# build minilzo too (bz 439979)
gcc -g -O2 -Iinclude/lzo -o minilzo/minilzo.o -c minilzo/minilzo.c
echo "LIBRARY %{minilzo} INITINSTANCE TERMINSTANCE" > %{minilzo}.def
echo "DATA MULTIPLE" >> %{minilzo}.def
echo "EXPORTS" >> %{minilzo}.def
emxexp minilzo/minilzo.o >> %{minilzo}.def
gcc -g -Zhigh-mem -Zomf -Zdll %{minilzo}.def -o %{minilzo}.dll minilzo/minilzo.o
emximp -o %{minilzo}.a %{minilzo}.def


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
install -m 755 %{minilzo}.dll $RPM_BUILD_ROOT%{_libdir}
install -p -m 644 minilzo/minilzo.h $RPM_BUILD_ROOT%{_includedir}/lzo

#Remove doc
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/lzo


%check
export BEGINLIBPATH="$RPM_BUILD_ROOT%{_libdir};$BEGINLIBPATH"
make check test


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc AUTHORS THANKS NEWS
%{_libdir}/lzo2*.dll

%files minilzo
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc minilzo/README.LZO
%{_libdir}/%{minilzo}.dll

%files devel
%defattr(-,root,root,-)
%doc doc/LZOAPI.TXT doc/LZO.FAQ doc/LZO.TXT
%{_includedir}/lzo
%{_libdir}/*lzo*.a

%changelog
* Tue Jun 14 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.09-2
- changed debug package to new scheme

* Fri Feb 27 2015 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.09-1
- Initial version
