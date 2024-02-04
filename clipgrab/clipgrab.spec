Name:           clipgrab
Version:        3.9.7
Release:        1%{?dist}

License:        GPLv3 and Non-Commercial Use Only (Artwork and Trademark)
Summary:        A free video downloader and converter
URL:            http://clipgrab.de/en
%if !0%{?os2_version}
Source0:        https://download.clipgrab.org/%{name}-%{version}.tar.gz
Source1:        %{name}.desktop
%else
%scm_source github http://github.com/TeLLie/%{name}-os2 %{version}-os2
%endif
ExcludeArch:    ppc64le ppc64

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
chmod 0644 *.cpp *.h icon.png COPYING README license.odt
# Fix build with Qt 5.12: https://aur.archlinux.org/packages/clipgrab-qt5/
sed -i 's|QtWebKit/QWebView|QtWebKitWidgets/QWebView|' mainwindow.ui
%else
%scm_setup
%endif

%build
export QMAKE_SH=$SHELL
# do a fast qt build, as runmapsym and wmapsym is not needed here
export FAST_BUILD=1
LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"

%{qmake_qt5} clipgrab.pro QMAKE_CXXFLAGS="%{optflags}"
%if !0%{?os2_version}
%make_build
%else
make %{?_smp_mflags}
%endif

%install
install -Dm755 %{name}.exe %{buildroot}%{_bindir}/%{name}.exe
mkdir -p %{buildroot}%{_datadir}/applications
install -Dm 644 icon.png %{buildroot}%{_datadir}/pixmaps/%{name}.png
%if !0%{?os2_version}
desktop-file-install --dir %{buildroot}%{_datadir}/applications %{SOURCE1}
%endif

%files
%license COPYING
%doc README
%if !0%{?os2_version}
%{_bindir}/%{name}
%else
%{_bindir}/%{name}.exe
%endif
%{_datadir}/pixmaps/*.png
%if !0%{?os2_version}
%{_datadir}/applications/clipgrab.desktop
%endif

%changelog
* Thu Feb 22 2022 Elbert Pol <elbert.pol@gmail.com> - 3.9.7-1
- Updated to latest version

* Sun Feb 03 2019 Elbert Pol <elbert.pol@gmail.com> - 3.7.2-1
- Updated to latest QT4 version of clipgrab

* Fri Nov 09 2018 Elbert Pol <elbert.pol@gmail.com> - 3.7.1-1
- first clipgrab rpm for OS/2

