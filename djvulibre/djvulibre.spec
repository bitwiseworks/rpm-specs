%define         _hardened_build 1

Summary: DjVu viewers, encoders, and utilities
Name: djvulibre
Version: 3.5.28
Release: 1%{?dist}
License: GPLv2+
URL: http://djvu.sourceforge.net/
%if !0%{?os2_version}
Source0: http://downloads.sourceforge.net/djvu/%{name}-%{version}.tar.gz
Patch0: djvulibre-3.5.22-cdefs.patch
#Patch1: djvulibre-3.5.25.3-cflags.patch
Patch2: djvulibre-3.5.27-buffer-overflow.patch
Patch3: djvulibre-3.5.27-infinite-loop.patch
Patch4: djvulibre-3.5.27-stack-overflow.patch
Patch5: djvulibre-3.5.27-zero-bytes-check.patch
Patch6: djvulibre-3.5.27-export-file.patch
Patch7: djvulibre-3.5.27-null-dereference.patch
Patch8: djvulibre-3.5.27-check-image-size.patch
Patch9: djvulibre-3.5.27-integer-overflow.patch
Patch10: djvulibre-3.5.27-check-input-pool.patch
Patch11: djvulibre-3.5.27-djvuport-stack-overflow.patch
Patch12: djvulibre-3.5.27-unsigned-short-overflow.patch
Patch13: djvulibre-3.5.27-out-of-bound-write.patch
Patch14: djvulibre-3.5.27-out-of-bound-write-2.patch
%else
Vendor:         bww bitwise works GmbH
%scm_source github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2
%endif

%if !0%{?os2_version}
Requires(post): xdg-utils
Requires(preun): xdg-utils
%endif
%if (0%{?fedora} > 15 || 0%{?rhel} > 6 || 0%{?os2_version})
BuildRequires:  gcc
BuildRequires: libjpeg-turbo-devel
%else
BuildRequires: libjpeg-devel
%endif
BuildRequires: libtiff-devel
%if !0%{?os2_version}
BuildRequires: xdg-utils chrpath
BuildRequires: hicolor-icon-theme
BuildRequires: inkscape
%endif
BuildRequires: gcc-c++
BuildRequires: make

Provides: %{name}-mozplugin = %{version}
Obsoletes: %{name}-mozplugin < 3.5.24

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

%description libs
Library files for DjVuLibre.


%package devel
Summary: Development files for DjVuLibre
Requires: %{name}-libs = %{version}-%{release}
Requires: pkgconfig

%description devel
Development files for DjVuLibre.


%if 0%{?os2_version}
%debug_package
%endif

%prep
%if !0%{?os2_version}
%setup -q 
%patch0 -p1 -b .cdefs
#%patch1 -p1 -b .cflags
%patch2 -p1 -b .buffer-overflow
%patch3 -p1 -b .infinite-loop
%patch4 -p1 -b .stack-overflow
%patch5 -p1 -b .zero-bytes-check
%patch6 -p1 -b .export-file
%patch7 -p1 -b .null-dereference
%patch8 -p1 -b .check-image-size
%patch9 -p1 -b .integer-overflow
%patch10 -p1 -b .check-input-pool
%patch11 -p1 -b .djvuport-stack-overflow
%patch12 -p1 -b .unsigned-short-overflow
%patch13 -p1 -b .out-of-bound-write
%patch14 -p1 -b .out-of-bound-write-2
%else
%scm_setup
%endif


%build 
%if !0%{?os2_version}
%configure --with-qt=%{_libdir}/qt-3.3 --enable-threads
# Disable rpath on 64bit - NOT! It makes the build fail (still as of 3.5.20-2)
#sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
#sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%else
# Set BUILDLEVEL to be embedded to all DLLs built with Libtool.
export LT_BUILDLEVEL="@#%{vendor}:%{version}-%{release}#@##1## `LANG=C date +'%%d %%b %%Y %%H:%%M:%%S'`     `uname -n`::::0::"
# mstackrealign is not needed anymore, as used always in rpmbuild
#export CFLAGS="$RPM_OPT_FLAGS -mstackrealign"
#export CXXFLAGS="$RPM_OPT_FLAGS -mstackrealign"
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
export NOCONFIGURE=1
autogen.sh

%configure --enable-shared --disable-static --disable-desktopfiles
%endif

make %{?_smp_mflags} V=1


%install
make install DESTDIR=%{buildroot}

%if !0%{?os2_version}
# Fix for the libs to get stripped correctly (still required in 3.5.20-2)
find %{buildroot}%{_libdir} -name '*.so*' | xargs %{__chmod} +x

# Remove rpath
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/djvutoxml
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/djvused
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/cjb2
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/csepdjvu
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/djvuserve
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/djvm
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/djvuxmlparser
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/djvutxt
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/ddjvu
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/djvumake
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/cpaldjvu
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/djvuextract
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/c44
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/djvups
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/djvudump
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/djvmcvt
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/bzz
%endif

# This XML file does not differentiate between DjVu Image and DjVu Document
# MIME types, the default one in shared-mime-info does.
rm -f $RPM_BUILD_ROOT%{_datadir}/mime/packages/djvulibre-mime.xml

%if !0%{?os2_version}
# MIME types (icons and desktop file) - this installs icon files under
# /usr/share/icons/hicolor/ and an xml file under /usr/share/mime/image/
# Taken from {_datadir}/djvu/osi/desktop/register-djvu-mime install
# See also the README file in the desktopfiles directory of the source distribution
pushd desktopfiles
for i in 22 32 48 64 ; do
    install -d $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${i}x${i}/mimetypes/
    cp -a ./prebuilt-hi${i}-djvu.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${i}x${i}/mimetypes/image-vnd.djvu.mime.png
#    cp -a ./hi${i}-djvu.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${i}x${i}/mimetypes/gnome-mime-image-vnd.djvu.png
done
popd
%endif


%post
# Unregister menu entry for djview3 if it is present as we no longer
# ship this in favour of the djview4 package. These files were
# installed in %post by the older djvulibre packages, but not actually
# owned by the package (packaging bug)
%if !0%{?os2_version}
rm -f %{_datadir}/applications/djvulibre-djview3.desktop || :
rm -f %{_datadir}/icons/hicolor/32x32/apps/djvulibre-djview3.png || :
%endif


%preun
# This is the legacy script, not compliant with current packaging
# guidelines. However, we leave it in, as the old packages didn't own
# the icon and xml files, so we want to be sure we remove them
%if !0%{?os2_version}
if [ $1 -eq 0 ]; then
    # MIME types (icons and desktop file)
    %{_datadir}/djvu/osi/desktop/register-djvu-mime uninstall || :
fi
%endif


%ldconfig_scriptlets libs


%files
%{_bindir}/*
%if 0%{?os2_version}
%exclude %{_bindir}/*.dbg
%endif
%{_mandir}/man1/*
%{_datadir}/djvu/
%if !0%{?os2_version}
%{_datadir}/icons/hicolor/16x16/mimetypes/*
%{_datadir}/icons/hicolor/20x20/mimetypes/*
%{_datadir}/icons/hicolor/22x22/mimetypes/*
%{_datadir}/icons/hicolor/24x24/mimetypes/*
%{_datadir}/icons/hicolor/32x32/mimetypes/*
%{_datadir}/icons/hicolor/48x48/mimetypes/*
%{_datadir}/icons/hicolor/64x64/mimetypes/*
%{_datadir}/icons/hicolor/72x72/mimetypes/*
%{_datadir}/icons/hicolor/96x96/mimetypes/*
%{_datadir}/icons/hicolor/128x128/mimetypes/*
%{_datadir}/icons/hicolor/scalable/mimetypes/*
%{_datadir}/icons/hicolor/256x256/mimetypes/*
%endif


%files libs
%doc README COPYRIGHT COPYING NEWS
%if !0%{?os2_version}
%{_libdir}/*.so.*
%else
%{_libdir}/*.dll
%endif


%files devel
%doc doc/*.*
%{_includedir}/libdjvu/
%{_libdir}/pkgconfig/ddjvuapi.pc
%exclude %{_libdir}/*.la
%if !0%{?os2_version}
%{_libdir}/*.so
%else
%{_libdir}/*_dll.a
%endif


%changelog
* Tue Nov 16 2021 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.5.28-1
- update to version 3.5.28
- resync with fedora spec

* Thu Sep 08 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.5.27-3
- fix a crash in the P4 build
- djvulibre also requires djvulibre-libs

* Tue Sep 06 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.5.27-2
- change all #ifdef OS2 to #ifdef __OS2__
- init pthread structure to prevent a sigsegv

* Fri Sep 02 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.5.27-1
- first version
