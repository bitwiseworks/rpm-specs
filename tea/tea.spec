Name:          tea
Version:       63.0.1
Release:       1%{?dist}
Summary:       A powerful and easy-to-use Qt4-based editor with many useful features for HTML, Docbook, and LaTeX editing
Group:         Graphical Desktop/Applications/Development
%if 0%{?os2_version}
Vendor:        TeLLie OS2 forever
Distribution:  OS/2
Packager:      TeLLie
%endif 
URL:           http://semiletov.org/tea/
%if !0%{?os2_version}
Source:       http://downloads.sourceforge.net/project/tea-editor/tea-editor/%{version}/tea-%{version}.tar.bz2
%else
%scm_source github https://github.com/Tellie/%{name}-os2 %{version}-os2
%endif

License:       GPL
# AUTOBUILDREQ-BEGIN
%if !0%{?os2_version}
BuildRequires: glibc-devel
BuildRequires: libGL-devel
%endif
BuildRequires: bww-resources-rpm
BuildRequires: hunspell-devel
BuildRequires: qt5-qtbase-devel
BuildRequires: poppler-devel
BuildRequires: zlib-devel
BuildRequires: aspell-devel

## AUTOBUILDREQ-END
BuildRoot:     %{_tmppath}/%{name}-%{version}-root

%description
TEA is a powerful and easy-to-use Qt4-based editor with many useful features for HTML, Docbook, and LaTeX editing.
It features a small footprint, a tabbed layout engine, support for multiple encodings, code snippets, templates, customizable hotkeys,
an "open at cursor" function for HTML files and images, miscellaneous HTML tools, preview in external browser, string manipulation functions,
Morse-code tools, bookmarks, syntax highlighting, and more.

%prep
%scm_setup

%build
%cmake -DUSE_ASPELL=ON -DUSE_PRINTER=ON -DUSE_PDF=ON -DUSE_DJVU=ON 
%cmake_build

%install
%cmake_install

%if 0%{?os2_version}     
mkdir -p %{buildroot}%{_datadir}/os2/icons/
cp -a icons/%{name}.ico %{buildroot}%{_datadir}/os2/icons/%{name}.ico
%endif


%files
%doc AUTHORS COPYING README.md NEWS NEWS-RU TODO 
%exclude %{_datadir}/applications/%{name}.desktop
%if !0%{?os2_version}
%{_bindir}/tea
%else
%doc README-OS2.txt CHANGES-OS2.txt
%{_bindir}/tea.exe
%{_datadir}/os2/icons/%{name}.ico
%endif
%{_datadir}/icons/hicolor/32x32/apps/tea.png
%{_datadir}/icons/hicolor/48x48/apps/tea.png
%{_datadir}/icons/hicolor/64x64/apps/tea.png
%{_datadir}/icons/hicolor/128x128/apps/tea.png
%{_datadir}/icons/hicolor/scalable/apps/tea.svg

%if 0%{?os2_version}
%global wps_folder_title Tea

%post -e
if [ "$1" -ge 1 ]; then # (upon update)
    %wps_object_delete_all
fi
%global wps_app_title Tea
%bww_folder -t %{wps_folder_title}
%bww_app -f %{_bindir}/%{name}.exe -t %{wps_app_title} -i ${name}.ico
%bww_app_shadow
%bww_file TODO -f %_defaultdocdir/%{name}-%{version}/TODO
%bww_file README-OS2.txt -f %_defaultdocdir/%{name}-%{version}/README-os2.txt
%bww_file CHANGES-OS2.txt -f %_defaultdocdir/%{name}-%{version}/CHANGES-os2.txt
%bww_file README.md -f %_defaultdocdir/%{name}-%{version}/README.md

%postun
if [ "$1" -eq 0 ]; then # (upon removal)
    %wps_object_delete_all
fi
%endif

%changelog
* Mon May 13 2024 Elbert Pol ,elbert.pol@gmail.com> 63.0.1-1
- Updated to latest version

* Sat May 11 2024 Elbert Pol <elbert.pol@gmail.com> 63.0.0-1
- Updated to latest version

* Sun Mar 10 2024 Elbert Pol <elbert.pol@gmail.com> 62.4.0-1
- U[dated to latest version

* Tue Dec 19 2023 Elbert Pol <elbert.pol@gmail.com> 62.1.2-4
- Tweaked the spec file some more.
- Add some BuildRequires

* Wed Dec 13 2023 Elbert Pol <elbert.pol@gmail.com> 62.1.2-3
- Updated spec and add desktop map and icon
- Add spec file to BWW reposito

* Mon Dec 11 2023 Elbert Pol <elbert.pol@gmail.com> 62.1.2-2
- Update the spec file more to os2 specifications

* Sat Dec 09 2023 Elbert Pol <elbert.pol@gmail.com> 62.1.2-1
- Updated to latest version

* Sun Nov 05 2023 Elbert Pol <elbert.pol@gmail.com> 62.1.0-1
- Updated to latest version

* Sun Nov 13 2022 Elbert Pol <elbert.pol@gmail.com> 62.0.1-1
- Updated to latest version

* Mon Oct 31 2022 Elbert Pol <elbert.pol@gmail.com> 61-2.0-1
- Updated to latest version
 
* Mon Sep 26 2022 Elbert Pol <elbert.pol@gmail.com> 61.1.0-1
- Updated to latest version.

* Fri Jul 22 2022 Elbert Pol <elbert.pol@gmail.com> 61.0.0-1
- Updated to latest version

* Wed Jan 19 2022 Elbert Pol <elbert.pol@gmail.com> 60-7.0-1
- Updated to latest version

* Tue Oct 19 2021 Elbert Pol <elbert.pol@gmail.com> 60-6.1-1
- Updated to latest version

* Thu Sep 30 2021 Elbert Pol <elbert.pol@gmail.com> 60-5.1-1
- Updated to latest version

* Thu Jul 15 2021 Elbert Pol <elbert.pol@gmail.com> 60.4.0-1
- Updated to latest version

* Thu Jun 03 2021 Elbert Pol <elbert.pol@gmail.com> 60.3.0-1
- Updated to latest version

* Thu May 06 2021 Elbert Pol <elbert.pol@gmail.com> 60.1.0-1
- Updated to latest version

* Mon Apr 12 2021 Elbert Pol <elbert.pol@gmail.com> 60.0.3-1
- Updated to latest version

* Tue Apr 06 2021 Elbert Pol <elbert.pol@gmail.com> 60.0.2-1
- Updated to latest version

* Sat Oct 03 2020 Elbert Pol <elbert.pol@gmail.com> 50.1.0-1
- Updated to latest source

* Thu Apr 02 2020 Elbert Pol <elbert.pol@gmail.com> 50.0.4-2
- Requirement from some files not needed and build with gcc 9.2.0
- Also fix some other definitions for OS2 

* Tue Dec 10 2019 Elbert Pol <elbert.pol@gmail.com> 50.0.4-1
- Updated to latest source
- Some more OS/2 fixes

* Sat Dec 07 2019 Elbert Pol <elbert.pol@gmail.com> 50.0.3-1
- Updated to latest source
- Some OS/2 fix

* Fri Nov 29 2019 Elbert Pol <elbert.pol@gmail.com> 50.0.0-1
- Updated to latest source

* Sun Sep 22 2019 Elbert Pol <elbert.pol@gmail.com> 48.0.0-1
- Updated to latest source

* Mon May 06 2019 Elbert Pol <elbert.pol@gmail.com> 47.1.0-1
- Updated to latest source

* Sun Dec 02 2018 Elbert Pol <elbert.pol@gmail.com> 47.0.0-1
- Update to latest source

* Sun Sep 30 2018 Elbert Pol <elbert.pol@gmail.com> 46.3.0-1
- Some OS2 fixes to enable PDF and DJVU
- First OS/2 rpm release
