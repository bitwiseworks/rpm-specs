Name:           clipgrab
Version:        3.9.10
Release:        1%{?dist}

License:        GPLv3 and Non-Commercial Use Only (Artwork and Trademark)
Summary:        A free video downloader and converter
URL:            http://clipgrab.de/en
%if !0%{?os2_version}
Source0:        https://download.clipgrab.org/%{name}-%{version}.tar.gz
Source1:        %{name}.desktop
%else
%scm_source github https://github.com/Tellie/%{name}-os2 %{version}-os2
%endif
ExcludeArch:    ppc64le ppc64

%if 0%{os2_version}
Vendor:         TeLLie OS2 forever
Distribution:   OS/2
Packager:       TeLLeRBoP

Source100:      %{name}-os2.ico
Source101:      %{name}-os2.rc

# For scm macros
BuildRequires:  curl zip

# for WPS macros
BuildRequires:  bww-resources-rpm-build
Requires:       bww-resources-rpm
%endif

%if !0%{?os2_version}
BuildRequires:  ImageMagick
BuildRequires:  desktop-file-utils
BuildRequires:  pkgconfig(Qt5WebKit)
BuildRequires:  pkgconfig(Qt5WebKitWidgets)
%endif
BuildRequires:  pkgconfig(Qt5WebEngineWidgets)
BuildRequires:  pkgconfig(Qt5Xml)
# Work around https://bugzilla.redhat.com/show_bug.cgi?id=1909195
BuildRequires: nss nspr

%if !0%{?os2_version}
Requires:       hicolor-icon-theme
%endif
Requires:       ffmpeg

%description
ClipGrab is a free downloader and converter for YouTube, Vimeo, Dailymotion
and many other online video sites.

%prep
%if !0%{?os2_version}
#setup -q
%autosetup -p 1 -n %{name}-%{version}
%else
%scm_setup
chmod 0644 *.cpp *.h icon.png COPYING README license.odt
# Fix build with Qt 5.12: https://aur.archlinux.org/packages/clipgrab-qt5/
sed -i 's|QtWebKit/QWebView|QtWebKitWidgets/QWebView|' mainwindow.ui
cp -a %{SOURCE100} %{SOURCE101} .
%endif

%build
%{qmake_qt5} clipgrab.pro QMAKE_CXXFLAGS="%{optflags}"
%make_build
%if 0%{?os2_version}
wrc -bt=os2 -zm -r %{name}-os2.rc
wrc -bt=os2 -zm %{name}-os2.res %{name}.exe
%endif

%install
%if !0%{?os2_version}
install -Dm755 %{name} %{buildroot}%{_bindir}/%{name}
desktop-file-install --dir %{buildroot}%{_datadir}/applications %{SOURCE1}
%else
install -Dm755 %{name}.exe %{buildroot}%{_bindir}/%{name}.exe
mkdir -p %{buildroot}%{_datadir}/os2/icons/
cp -a %{name}-os2.ico %{buildroot}%{_datadir}/os2/icons/%{name}.ico
%endif
mkdir -p %{buildroot}%{_datadir}/applications
install -Dm 644 icon.png %{buildroot}%{_datadir}/pixmaps/%{name}.png

%files
%license COPYING
%doc README README-os2.txt CHANGES-os2.txt
%if !0%{?os2_version}
%{_bindir}/%{name}
%{_datadir}/applications/clipgrab.desktop
%else
%{_bindir}/%{name}.exe
%{_datadir}/os2/icons/%{name}.ico
%endif
%{_datadir}/pixmaps/*.png

%if 0%{?os2_version}
%global wps_folder_title Clipgrab

%post -e
if [ "$1" -ge 1 ]; then # (upon update)
    %wps_object_delete_all
fi
%global wps_app_title Clipgrab
%bww_folder -t %{wps_folder_title}
%bww_app -f %{_bindir}/%{name}.exe -t %{wps_app_title} -i ${name}.ico
%bww_app_shadow
%bww_readme -f %_defaultdocdir/%{name}-%{version}/README
%bww_license -f %_defaultlicensedir/%{name}-%{version}/COPYING
%bww_file README-OS2.txt -f %_defaultdocdir/%{name}-%{version}/README-os2.txt
%bww_file CHANGES-OS2.txt -f %_defaultdocdir/%{name}-%{version}/CHANGES-os2.txt


%postun
if [ "$1" -eq 0 ]; then # (upon removal)
    %wps_object_delete_all
fi
%endif

%changelog

* Sun Feb 04 2024 Elbert Pol <elbert.pol@gmail.com> - 3.9.10-1
- Update to latest version
- Add support for python3
- resync with fedora spec

* Tue Feb 22 2022 Elbert Pol <elbert.pol@gmail.com> - 3.9.7-1
- Updated to latest version

* Sun Feb 03 2019 Elbert Pol <elbert.pol@gmail.com> - 3.7.2-1
- Updated to latest QT4 version of clipgrab

* Fri Nov 09 2018 Elbert Pol <elbert.pol@gmail.com> - 3.7.1-1
- first clipgrab rpm for OS/2

