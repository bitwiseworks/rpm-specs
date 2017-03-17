Name:           qpdfview
Version:        0.4.17
Release:        1%{?dist}
License:        GPLv2+
Summary:        Tabbed PDF Viewer
Url:            https://launchpad.net/qpdfview

Vendor:         bww bitwise works GmbH
%scm_source github https://github.com/bitwiseworks/qpdfview %{version}

Requires:       libqt4
Requires:       cups
Requires:       poppler-qt4
Requires:       libspectre ghostscript
Requires:       zlib
Requires:       djvulibre
Requires:       libjpeg libtiff libpng

BuildRequires:  libqt4-devel
BuildRequires:  cups-devel
BuildRequires:  poppler-qt4-devel
BuildRequires:  libspectre-devel ghostscript-devel
BuildRequires:  zlib-devel
BuildRequires:  djvulibre-devel
BuildRequires:  libjpeg-devel libtiff-devel libpng-devel

%description
qpdfview is a tabbed PDF viewer.
It uses the Poppler library for rendering and CUPS for printing.
It provides a clear and simple graphical user interface using the Qt framework.


%prep
%scm_setup


%build
export QMAKE_SH=$SHELL
# do a fast qt build, as runmapsym and wmapsym is not needed here
export FAST_BUILD=1
LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"

/@unixroot/usr/lib/qt4/bin/lrelease qpdfview.pro
qmake \
    TARGET_INSTALL_PATH="%{_bindir}" \
    PLUGIN_INSTALL_PATH="%{_libdir}/%{name}" \
    DATA_INSTALL_PATH="%{_datadir}/%{name}" \
    MANUAL_INSTALL_PATH="%{_mandir}/man1" \
    ICON_INSTALL_PATH="%{_datadir}/icons/hicolor/scalable/apps" \
    LAUNCHER_INSTALL_PATH="%{_datadir}/applications" \
    APPDATA_INSTALL_PATH="%{_datadir}/appdata" \
    "CONFIG+=no_install_debuginfo" "CONFIG+=without_dbus" "CONFIG+=without_magic" \
    qpdfview.pro
make %{?_smp_mflags}


%install
make INSTALL_ROOT=%{buildroot} install
%find_lang %{name} --with-qt --without-mo
# unknown language
rm -f %{buildroot}/%{_datadir}/%{name}/%{name}_ast.qm
rm -rf %{buildroot}/%{_datadir}/appdata
rm -rf %{buildroot}/%{_datadir}/applications
rm -rf %{buildroot}/%{_datadir}/icons

sed -i -e "s|_VERSION_|%{version}|" -e "s|_BUILD_|%{release}|" %{_builddir}/%{buildsubdir}/install.os2


%post
if [ "$1" -ge 1 ]; then # (upon update)
    %wps_object_delete_all
fi
# for the definition of the parameters see macros.bww
%define title Tabbed PDF viewer
%bww_folder -e %{name} -t %{title} -r README -s Y -a *.pdf,*.ps,*.eps,*.djvu,*.djv


%postun
if [ "$1" -eq 0 ]; then # (upon removal)
    %wps_object_delete_all
fi


%files -f %{name}.lang
%doc CHANGES CONTRIBUTORS COPYING README TODO install.os2
%{_bindir}/%{name}.exe
%{_libdir}/%{name}/
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/help*.html
%{_mandir}/man?/*

%changelog
* Fri Mar 17 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.4.17-1
- initial version
