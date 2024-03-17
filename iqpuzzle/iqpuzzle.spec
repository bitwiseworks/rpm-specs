Name:           iqpuzzle
Version:        1.2.10
Release:        1%{?dist}
Summary:        A diverting I.Q. challenging pentomino puzzle
Group:          Games/Puzzles
License:        GPLv3
URL:            https://github.com/ElTh0r0/iqpuzzle
%if 0%{?os2_version}
Vendor:        TeLLie OS2 forever
Distribution:  OS/2
Packager:      TeLLie
%endif 

%if !0%{?os2_version}
URL:           http://semiletov.org/tea/
Source0:        https://github.com/ElTh0r0/iqpuzzle/archive/v%{version}/%{name}-%{version}.tar.gz
%else
%scm_source github https://github.com/tellie/%{name}-os2 %{version}-os2
%endif
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Widgets)

# for WPS macros
%if 0%{os2_version}
BuildRequires:  bww-resources-rpm-build
Requires:       bww-resources-rpm
%endif

%description
iQPuzzle is a diverting I.Q. challenging pentomino puzzle.
Pentominos are used as puzzle pieces and more than 300 different board shapes
are available, which have to be filled with them.

%prep
%if !0%{?os2_version}
%autosetup
%else
%scm_setup
%endif

%build
%qmake_qt5 PREFIX=%{buildroot}%{_prefix}
%make_build
%if 0%{?os2_version}
wrc -bt=os2 -zm -r %{name}-os2.rc
wrc -bt=os2 -zm %{name}-os2.res %{name}.exe
%endif
 
%install
%make_install
%if 0%{?os2_version}
install -Dm755 %{name}.exe %{buildroot}%{_bindir}/%{name}.exe
mkdir -p %{buildroot}%{_datadir}/os2/icons/
cp -a icons/%{name}_os2.ico %{buildroot}%{_datadir}/os2/icons/%{name}.ico
mkdir -p %{buildroot}%{_datadir}/iqpuzzle/boards
cp -a data/boards/* %{buildroot}%{_datadir}/iqpuzzle/boards/
# install man pages
mkdir -p %{buildroot}/%{_mandir}/man6
cp man/man6/* %{buildroot}/%{_mandir}/man6/
%endif
%if !0%{?os2_version}
%find_lang %{name} --with-man

%files -f %{name}.lang
%else
%files
%license COPYING
%doc README.md README-OS2.txt CHANGES-OS2.txt
%endif
%if !0%{?os2_version}
%{_bindir}/%{name}
%{_datadir}/applications/com.github.elth0r0.iqpuzzle.desktop
%{_datadir}/icons/hicolor/*/apps/iqpuzzle.png
%{_datadir}/icons/hicolor/scalable/apps/iqpuzzle.svg
%{_datadir}/metainfo/com.github.elth0r0.iqpuzzle.metainfo.xml
%{_datadir}/%{name}/
%else
%{_bindir}/%{name}.exe
%{_datadir}/os2/icons/%{name}.ico
%{_datadir}/%{name}/boards/
%endif
%{_mandir}/man6/*

%if 0%{?os2_version}
%global wps_folder_title iqpuzzle

%post -e
if [ "$1" -ge 1 ]; then # (upon update)
    %wps_object_delete_all
fi
%global wps_app_title iqpuzzle
%bww_folder -t %{wps_folder_title}
%bww_app -f %{_bindir}/%{name}.exe -t %{wps_app_title} -i %{name}.ico
%bww_app_shadow
%bww_license -f %_defaultlicensedir/%{name}-%{version}/COPYING
%bww_file README-OS2.txt -f %_defaultdocdir/%{name}-%{version}/README-os2.txt
%bww_file CHANGES-OS2.txt -f %_defaultdocdir/%{name}-%{version}/CHANGES-os2.txt


%postun
if [ "$1" -eq 0 ]; then # (upon removal)
    %wps_object_delete_all
fi
%endif

%changelog
* Sun Mar 17 2024 Elbert Pol <elbert.pol@gmail.com> 1.2.10-1
- Update source to build 14-03-2024
- Make a WPS desktop map for iqpuzzle
- Add ico to exe file