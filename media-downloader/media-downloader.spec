Name:           media-downloader
Version:        4.7.0
Release:        1%{?dist}
Summary:        GUI frontend to multiple CLI based downloading programs
License:        GPL-2.0-or-later
URL:            https://github.com/mhogomchungu/media-downloader
Source0:        %url/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  qt5-qtbase-devel
BuildRequires:  desktop-file-utils
Requires: yt-dlp
Requires: aria2

%description
This project is a Qt/C++ based GUI frontend to CLI multiple CLI based tools that
deal with downloading online media.
yt-dlp CLI tool is the default supported tool and other tools can be added by
downloading their extension and a list of supported extensions is managed here.

Features offered:-
 1. The GUI can be used to download any media from any website supported by
    installed extensions.
 2. The GUI offers a configurable list of preset options that can be used to
     download media if they are provided in multiple formats.
 3. The GUI offers an ability to do unlimited number of parallel downloads.
    Be careful with this ability because doing too many parallel downloads may
    cause the host to ban you.
 4. The GUI offers an ability to do batch downloads by entering individual link
    in the UI or telling the app to read them from a local file.
 5. The GUI offers an ability to download playlist from websites that supports
    them like youtube.
 6. The GUI offers ability to manage links to playlist to easily monitor their
    activities(subscriptions).
 7. The GUI is offered in multiple languages and as of this writing, the
    supported languages are English, Chinese, Spanish, Polish, Turkish, Russian,
    Japanese, French and Italian.

%prep
%autosetup -p0 -n %{name}-%{version}

%build
mkdir build && pushd build
%cmake  -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=release ..
%cmake_build
popd

%install
pushd build
%cmake_install
popd
%find_lang %{name} --all-name --with-qt

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%files -f %{name}.lang
%doc README.md
%license LICENSE
%{_bindir}/%{name}
%dir %{_datadir}/%{name}/
%dir %{_datadir}/%{name}/translations/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png

%changelog
* Mon Jun 10 2024 Martin Gansser <martinkg@fedoraproject.org> - 4.7.0-1
- Update to 4.7.0

* Tue Apr 09 2024 Martin Gansser <martinkg@fedoraproject.org> - 4.5.0-1
- Update to 4.5.0

* Tue Mar 12 2024 Martin Gansser <martinkg@fedoraproject.org> - 4.4.0-1
- Update to 4.4.0

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 13 2024 Martin Gansser <martinkg@fedoraproject.org> - 4.2.0-2
- Remove RR youtube-dl

* Fri Jan 12 2024 Martin Gansser <martinkg@fedoraproject.org> - 4.2.0-1
- Update to 4.2.0
- Remove RR youtube-dl
- Add RR yt-dlp

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Mar 05 2023 Martin Gansser <martinkg@fedoraproject.org> - 2.9.0-1
- Update to 2.9.0

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 04 2023 Martin Gansser <martinkg@fedoraproject.org> - 2.8.0-1
- Update to 2.8.0

* Fri Dec 02 2022 Martin Gansser <martinkg@fedoraproject.org> - 2.7.0-2
- Remove unnecessary blank line above the first line
- Use new SPDX license format 

* Thu Nov 10 2022 Martin Gansser <martinkg@fedoraproject.org> - 2.7.0-1
- Update to 2.7.0

* Fri Oct 07 2022 Martin Gansser <martinkg@fedoraproject.org> - 2.6.0-1
- Initial package
