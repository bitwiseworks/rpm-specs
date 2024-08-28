Name:           media-downloader
Version:        5.0.1
Release:        1%{?dist}
Summary:        GUI frontend to multiple CLI based downloading programs
License:        GPL-2.0-or-later
%if 0%{?os2_version}
Vendor:        TeLLie OS2 forever
Distribution:  OS/2
Packager:      TeLLie
%endif 
URL:            https://github.com/mhogomchungu/media-downloader
%if !0%{?os2_version}
Source0:        %url/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz
%else
%scm_source github https://github.com/Tellie/media-downloader-os2 %{version}-os2
%endif
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  qt5-qtbase-devel
%if !0%{?os2_version}
BuildRequires:  desktop-file-utils
Requires: aria2
Requires: yt-dlp
%endif



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
%if !0%{?os2_version}
%autosetup -p0 -n %{name}-%{version}
%else
%scm_setup
%endif

%build
%if !0%{?os2_version}
mkdir build && pushd build
%cmake -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=release ..
%else
%cmake -DCMAKE_INSTALL_PREFIX=/@unixroot/usr -DCMAKE_BUILD_TYPE=release 
%endif

%cmake_build
cd src
wrc -bt=os2 -zm -r os2app.rc
wrc -bt=os2 -zm os2app.res ../pc-os2-emx-build/media-downloader.exe
%if !0%{?os2_version}
popd
%endif

%install
%if 0%{?os2_version}     
mkdir -p %{buildroot}%{_datadir}/os2/icons/
cp -a src/%{name}-os2.ico %{buildroot}%{_datadir}/os2/icons/%{name}.ico
%endif
%if !0%{?os2_version}
pushd build
%endif
%cmake_install
%if !0%{?os2_version}
popd
%endif

%find_lang %{name} --all-name --with-qt

%check
%if !0%{?os2_version}
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
%endif

%files -f %{name}.lang
%doc README.md changelog
%license LICENSE
%if !0%{?os2_version}
%{_bindir}/%{name}
%else
%doc README-os2.txt
%{_bindir}/%{name}.exe
%{_datadir}/os2/icons/%{name}.ico
%endif
%dir %{_datadir}/%{name}/
%dir %{_datadir}/%{name}/translations/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png

%if 0%{?os2_version}
%global wps_folder_title Media-downloader

%post -e
if [ "$1" -ge 1 ]; then # (upon update)
    %wps_object_delete_all
fi
%global wps_app_title Media-downloader
%bww_folder -t %{wps_folder_title}
%bww_app -f %{_bindir}/%{name}.exe -t %{wps_app_title} -i ${name}.ico
%bww_app_shadow
%bww_file changelog -f %_defaultdocdir/%{name}-%{version}/CHANGELOG
%bww_file README-OS2.txt -f %_defaultdocdir/%{name}-%{version}/README-os2.txt
%bww_file README.md -f %_defaultdocdir/%{name}-%{version}/README.md

%postun
if [ "$1" -eq 0 ]; then # (upon removal)
    %wps_object_delete_all
fi
%endif

%changelog
* Wed Aug 28 2024 Elbert Pol <elbert.pol@gmail.com> - 5.0.1-1
- Updated to latest version

* Tue Aug 06 2024 Elbert Pol <elbert.pol@gmail.com> - 4.9.0-1
- Updated to latest version

* Sat Jul 06 2024 Elbert Pol <elbert.pol@gmail.com> - 4.8.0-1
- Update to latest version.
- Add icon and add a map on desktop
- Add ico to exe file

* Sun Jun 16 2024 Elbert Pol <elbert.pol@gmail.com> - 4.7.0-1
- First Rpm for os2
