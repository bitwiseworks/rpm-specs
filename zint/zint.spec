Name:      zint
Version:   2.15.0
Release:   1%{?dist}
Summary:   Barcode generator library
# Automatically converted from old format: GPLv3+ - review is highly recommended.
License:   GPL-3.0-or-later
URL:       http://www.zint.org.uk
%if 0%{os2_version}
Vendor:         TeLLie OS2 forever
Distribution:   OS/2
Packager:       TeLLeRBoP
%endif
%if !0%{os2_version}
Source:    http://downloads.sourceforge.net/%{name}/%{name}-%{version}-src.tar.gz
%else
%scm_source github https://github.com/Tellie/zint-os2 %{version}-os2
%endif
%if !0%{os2_version}
# patch to disable creation of rpaths
Patch0:    %{name}-rpath.patch
# create shared libQZint instead of static one
Patch1:    %{name}-shared.patch
%endif

BuildRequires: cmake
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: libpng-devel
BuildRequires: zlib-devel
%if !0%{os2_version}
BuildRequires: mesa-libGL-devel
BuildRequires: desktop-file-utils
%endif
BuildRequires: qt5-qtbase-devel
BuildRequires: qt5-qtsvg-devel
BuildRequires: qt5-qttools-devel
BuildRequires: qt5-qttools-static

# for WPS macros
%if 0%{os2_version}
BuildRequires:  bww-resources-rpm-build
Requires:       bww-resources-rpm
%endif

%description
Zint is a C library for encoding data in several barcode variants. The
bundled command-line utility provides a simple interface to the library.
Features of the library:
- Over 50 symbologies including all ISO/IEC standards, like QR codes.
- Unicode translation for symbologies which support Latin-1 and 
  Kanji character sets.
- Full GS1 support including data verification and automated insertion of 
  FNC1 characters.
- Support for encoding binary data including NULL (ASCII 0) characters.
- Health Industry Barcode (HIBC) encoding capabilities.
- Output in PNG, EPS and SVG formats with user adjustable sizes and colors.
- Verification stage for SBN, ISBN and ISBN-13 data.


%package devel
Summary:       Library and header files for %{name}
%if !0%{os2_version}
Requires:      %{name}%{?_isa} = %{version}-%{release}
%else
Requires:      %{name} = %{version}-%{release}
%endif
Requires:      cmake

%description devel 
C library and header files needed to develop applications that use 
the Zint library. The API documentation can be found on the project website:
http://www.zint.org.uk/zintSite/Manual.aspx


%package qt
Summary:       Zint Barcode Studio

%description qt
Zint Barcode Studio is a Qt-based GUI which allows desktop users to generate 
barcodes which can then be embedded in documents or HTML pages.


%package qt-devel
Summary:       Library and header files for %{name}-qt
%if !0%{os2_version}
Requires:      %{name}-devel%{?_isa} = %{version}-%{release}
%else
Requires:      %{name}-devel = %{version}-%{release}
%endif

%description qt-devel 
C library and header files needed to develop applications that use libQZint.

%package static
Summary: Libraries for applications using zint

%description static
Static libraries for applications using the zint compression format.

%prep
%if !0%{os2_version}
%setup -q -n %{name}-%{version}-src
%patch -P0 -p1
%patch -P1 -p1
%else
%scm_setup
%endif

# fix line endings
sed -i "s|\r||g" docs/manual.txt

# remove BSD-licensed file required for Windows only (just to ensure that this package is plain GPLv3+)
rm -f backend/ms_stdint.h

# remove bundled getopt sources (we use the corresponding Fedora package instead)
rm -f frontend/getopt*.*

find -type f -exec chmod 644 {} \;

%build
%cmake
%cmake_build


%install
%cmake_install
rm -rf %{buildroot}/%{_datadir}/apps
install -D -p -m 644 docs/%{name}.1 %{buildroot}%{_mandir}/man1/%{name}.1
install -D -p -m 644 cmake/modules/FindZint.cmake %{buildroot}%{_datadir}/cmake/Modules/FindZint.cmake
mv %{buildroot}%{_datadir}/%{name} %{buildroot}%{_datadir}/cmake/%{name}
%if 0%{?os2_version}     
mkdir -p %{buildroot}%{_datadir}/os2/icons/
cp -a frontend_qt/res/qtzint-os2.ico %{buildroot}%{_datadir}/os2/icons/qt%{name}.ico
cp -a frontend/zint-os2.ico %{buildroot}%{_datadir}/os2/icons/%{name}.ico
%endif
%if !0%{os2_version}
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}-qt.desktop
install -D -p -m 644 %{name}-qt.png %{buildroot}/usr/share/pixmaps/%{name}-qt.png
install -D -p -m 644 %{name}-qt.desktop %{buildroot}%{_datadir}/applications/%{name}-qt.desktop

%ldconfig_scriptlets
%ldconfig_scriptlets qt
%endif


%files
%doc docs/manual.txt README TODO
%license LICENSE
%if !0%{os2_version}
%{_bindir}/%{name}
%else
%doc README-OS2.txt CHANGES-OS2.txt
%{_bindir}/%{name}.exe
%{_datadir}/os2/icons/%{name}.ico
%endif
%{_mandir}/man1/%{name}.1*
%if !0%{os2_version}
%{_libdir}/libzint.so.*
%else
%{_libdir}/*.dll
%endif

%files devel
%{_includedir}/%{name}.h
%if !0%{os2_version}
%{_libdir}/libzint.so
%else
%{_libdir}/*_dll.a
%endif
%{_datadir}/cmake/%{name}/
%{_datadir}/cmake/Modules/*.cmake

%files qt
%if !0%{os2_version}
%{_bindir}/%{name}-qt
%{_libdir}/libQZint.so.*
%{_datadir}/applications/%{name}-qt.desktop
%{_datadir}/pixmaps/%{name}-qt.png
%else
%{_bindir}/%{name}-qt.exe
%{_libdir}/*.dll
%{_datadir}/os2/icons/qt%{name}.ico
%endif

%files qt-devel
%{_includedir}/qzint.h
%if !0%{os2_version}
%{_libdir}/libQZint.so
%else
%{_libdir}/*_dll.a
%endif

%files static
%{_libdir}/*.a

%if 0%{?os2_version}
%global wps_folder_title Zint

%post -e
if [ "$1" -ge 1 ]; then # (upon update)
    %wps_object_delete_all
fi
%global wps_app_title Zint
%bww_folder -t %{wps_folder_title}
%bww_app -f %{_bindir}/%{name}-qt.exe -t %{wps_app_title} -i $qt%{name}.ico
%bww_app -f %{_bindir}/%{name}.exe -t %{wps_app_title} -i $%{name}.ico
%bww_app_shadow
%bww_readme -f %_defaultdocdir/%{name}-%{version}/README
%bww_license -f %_defaultlicensedir/%{name}-%{version}/LICENSE
%bww_file README-OS2.txt -f %_defaultdocdir/%{name}-%{version}/README-os2.txt
%bww_file CHANGES-OS2.txt -f %_defaultdocdir/%{name}-%{version}/CHANGES-os2.txt


%postun
if [ "$1" -eq 0 ]; then # (upon removal)
    %wps_object_delete_all
fi
%endif

%changelog
* Tue Feb 25 2025 Elbert Pol <elbert.pol@gmail.com> - 2.15.0-1
- First RPM for OS2
- Updated to latest version
