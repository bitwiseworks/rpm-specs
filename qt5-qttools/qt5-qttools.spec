%global qt_module qttools

# Only compress main Qt DLLs - plugins cannot be compressed as it destroys their QTMETADATA.
# TODO: Enhance _strip_opts to support masks with pathnames and to override LXLITE options for masks.
%global _strip_opts --compress -n "*.exe,Qt5*.dll"

# TODO: our make lacks -O flag, need to fix rpm macros for the time being...
%global make_build %{__make} %{?_smp_mflags}

# TODO: we don't have clang/devel on OS/2 and can't build qdoc for that reason
#global qdoc 1

#global bootstrap 1

%if ! 0%{?bootstrap}
## don't enable until crasher fixed: https://bugzilla.redhat.com/show_bug.cgi?id=1470778
#global webkit 1
%endif

Summary: Qt5 - QtTool components
Name:    qt5-qttools
Version: 5.13.1
Release: 1%{?dist}

License: LGPLv3 or LGPLv2
Url:     http://www.qt.io
%global majmin %(echo %{version} | cut -d. -f1-2)

# OS/2 is missing from official tarballs and has its own repo.
#Source0: https://download.qt.io/official_releases/qt/%{majmin}/%{version}/submodules/%{qt_module}-everywhere-src-%{version}.tar.xz

Vendor:  bww bitwise works GmbH

%scm_source github https://github.com/bitwiseworks/qttools-os2 v%{version}-os2-b1
#scm_source git file://D:/Coding/qt5/qt5/qttools xxxxxxx

# %%check needs cmake (and don't want to mess with cmake28)
BuildRequires: cmake
BuildRequires: qt5-rpm-macros >= %{version}

BuildRequires: qt5-qtbase-private-devel
BuildRequires: qt5-qtbase-static >= %{version}
BuildRequires: qt5-qtdeclarative-static >= %{version}
BuildRequires: pkgconfig(Qt5Qml)
# libQt5DBus.so.5(Qt_5_PRIVATE_API)
%{?_qt5:Requires: %{_qt5}%{?_isa} = %{_qt5_version}}

%if 0%{?bootstrap}
%global no_examples CONFIG-=compile_examples
Obsoletes: %{name}-examples < %{version}-%{release}
%else
%if 0%{?qdoc}
# for qdoc
BuildRequires: clang-devel llvm-devel
%endif
%endif

# To support github tags starting with `v` (nasty github bug!)
BuildRequires: os2-rpm-build >= 1-8

# To create WPS objects (with shared folder/object support)
BuildRequires: bww-resources-rpm-build >= 1.1.4

%if ! 0%{?no_examples:1}
%_qt5_examples_package_builddeps
%endif

Requires: %{name}-common = %{version}-%{release}

%description
%{summary}.

%package common
Summary: Common files for %{name}
BuildArch: noarch
Obsoletes: qt5-qttools-libs-clucene < 5.9.0
%if ! 0%{?webkit}
Obsoletes: qt5-designer-plugin-webkit < 5.9.0
%endif
# To create WPS objects (needed at runtime due to resource DLL)
Requires: bww-resources-rpm >= 1.1.4
%description common
%{summary}.

%package devel
Summary: Development files for %{name}
Requires: %{name} = %{version}-%{release}
Requires: %{name}-libs-designer%{?_isa} = %{version}-%{release}
Requires: %{name}-libs-designercomponents%{?_isa} = %{version}-%{release}
Requires: %{name}-libs-help%{?_isa} = %{version}-%{release}
Requires: qt5-doctools = %{version}-%{release}
Requires: qt5-designer = %{version}-%{release}
Requires: qt5-linguist = %{version}-%{release}
Requires: qt5-qtbase-devel%{?_isa}
%description devel
%{summary}.

%package static
Summary: Static library files for %{name}
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
%description static
%{summary}.

%package libs-designer
Summary: Qt5 Designer runtime library
Requires: %{name}-common = %{version}-%{release}
%description libs-designer
%{summary}.

%package libs-designercomponents
Summary: Qt5 Designer Components runtime library
Requires: %{name}-common = %{version}-%{release}
%description libs-designercomponents
%{summary}.

%package libs-help
Summary: Qt5 Help runtime library
Requires: %{name}-common = %{version}-%{release}
# when split happened
Conflicts: qt5-tools < 5.4.0-0.2
%description libs-help
%{summary}.

%package -n qt5-assistant
Summary: Documentation browser for Qt5
Requires: %{name}-common = %{version}-%{release}
%description -n qt5-assistant
%{summary}.

%package -n qt5-designer
Summary: Design GUIs for Qt5 applications
Requires: %{name}-libs-designer%{?_isa} = %{version}-%{release}
Requires: %{name}-libs-designercomponents%{?_isa} = %{version}-%{release}
%description -n qt5-designer
%{summary}.

%if 0%{?webkit}
%package -n qt5-designer-plugin-webkit
Summary: Qt5 designer plugin for WebKit
BuildRequires: pkgconfig(Qt5WebKitWidgets)
Requires: %{name}-libs-designer%{?_isa} = %{version}-%{release}
%description -n qt5-designer-plugin-webkit
%{summary}.
%endif

%package -n qt5-linguist
Summary: Qt5 Linguist Tools
Requires: %{name}-common = %{version}-%{release}
%description -n qt5-linguist
Tools to add translations to Qt5 applications.

%package -n qt5-qdbusviewer
Summary: D-Bus debugger and viewer
Requires: %{name}-common = %{version}-%{release}
%{?_qt5:Requires: %{_qt5}%{?_isa} >= %{_qt5_version}}
%description -n qt5-qdbusviewer
QDbusviewer can be used to inspect D-Bus objects of running programs
and invoke methods on those objects.

%package -n qt5-doctools
Summary: Qt5 doc tools package
%if 0%{?qdoc}
Provides: qt5-qdoc = %{version}
Obsoletes: qt5-qdoc < 5.8.0
%endif
Provides: qt5-qhelpgenerator = %{version}
Obsoletes: qt5-qhelpgenerator < 5.8.0
Provides: qt5-qtattributionsscanner = %{version}
Obsoletes: qt5-qtattributionsscanner < 5.8.0
Requires: qt5-qtattributionsscanner = %{version}

%description -n qt5-doctools
%{summary}.

%if ! 0%{?no_examples:1}
%package examples
Summary: Programming examples for %{name}
Requires: %{name}-common = %{version}-%{release}
%_qt5_examples_package_deps
%description examples
%{summary}.
%endif

%debug_package


%prep
#%setup -q -n %{qt_module}-everywhere-src-%{version}
%scm_setup


%build

# configure expects either a git clone w/o include dir or a source tarball with
# it but we are neither. Pretend we are the former.
test -d .git || mkdir .git

%{qmake_qt5} \
  %{?no_examples}

%make_build


%install
make install INSTALL_ROOT=%{buildroot}

# icons
# TODO: need?
#install -m644 -p -D src/assistant/assistant/images/assistant.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/assistant-qt5.png
#install -m644 -p -D src/assistant/assistant/images/assistant-128.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/assistant-qt5.png
#install -m644 -p -D src/designer/src/designer/images/designer.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/designer-qt5.png
#install -m644 -p -D src/qdbus/qdbusviewer/images/qdbusviewer.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/qdbusviewer-qt5.png
#install -m644 -p -D src/qdbus/qdbusviewer/images/qdbusviewer-128.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/qdbusviewer-qt5.png

# linguist icons
# TODO: need?
#for icon in src/linguist/linguist/images/icons/linguist-*-32.png ; do
#  size=$(echo $(basename ${icon}) | cut -d- -f2)
#  install -p -m644 -D ${icon} %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/linguist-qt5.png
#done

# hardlink files to {_bindir}, add -qt5 postfix to not conflict
# note that on OS/2 there is no hard linking so we move and symlink back instead
# (symlinking should be fine since _qt5_bindir is internal, not exposied in PATH
# so files from there are to be only operated by kLIBC which can read symlinks)
mkdir %{buildroot}%{_bindir}
PWD_SAVE=$PWD
cd %{buildroot}%{_qt5_bindir}
for i in * ; do
  case "${i}" in
   assistant.exe|designer.exe|lconvert.exe|linguist.exe|lrelease.exe|lupdate.exe|pixeltool.exe|qcollectiongenerator.exe|qdbus.exe|qdbusviewer.exe|qhelpconverter.exe|qhelpgenerator.exe|qtplugininfo.exe|qtattributionsscanner.exe)
      ext=${i##*.}
      targ=%{_bindir}/${i%%.${ext}}-qt5.${ext}
      mv     ${i} %{buildroot}${targ}
      ln -sv ${targ} ${i}
      ln -sv ${targ} ${i%%.${ext}}-qt5.${ext}
      ;;
    *)
      targ=%{_bindir}/${i}
      mv     ${i} %{buildroot}${targ}
      ln -sv ${targ} ${i}
      ;;
  esac
done
cd $PWD_SAVE

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot
PWD_SAVE=$PWD
cd %{buildroot}%{_qt5_libdir}
for prl_file in Qt5*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
done
cd $PWD_SAVE


%files -f %{debug_package_exclude_files}
%{_bindir}/qdbus-qt5.exe
%{_bindir}/qtpaths.exe
%{_qt5_bindir}/qdbus.exe
%{_qt5_bindir}/qdbus-qt5.exe
%{_qt5_bindir}/qtpaths.exe

%files common -f %{debug_package_exclude_files}
%doc README.md CHANGELOG.md
%license LICENSE.LGPL*

%files  libs-designer -f %{debug_package_exclude_files}
%{_qt5_libdir}/Qt5Dsgn.dll
%dir %{_qt5_libdir}/cmake/Qt5Designer/

%files  libs-designercomponents -f %{debug_package_exclude_files}
%{_qt5_libdir}/Qt5DsgC.dll

%files  libs-help -f %{debug_package_exclude_files}
%{_qt5_libdir}/Qt5Help.dll

%files -n qt5-assistant -f %{debug_package_exclude_files}
%{_bindir}/assistant-qt5.exe
%{_qt5_bindir}/assistant*

%files -n qt5-doctools -f %{debug_package_exclude_files}
%if 0%{?qdoc}
%{_bindir}/qdoc*
%{_qt5_bindir}/qdoc*
%endif
%{_bindir}/qdistancefieldgenerator*
%{_bindir}/qhelpgenerator*
%{_qt5_bindir}/qdistancefieldgenerator*
%{_qt5_bindir}/qhelpgenerator*
%{_bindir}/qtattributionsscanner-qt5.exe
%{_qt5_bindir}/qtattributionsscanner*

%files -n qt5-designer -f %{debug_package_exclude_files}
%{_bindir}/designer*
%{_qt5_bindir}/designer*

%if 0%{?webkit}
%files -n qt5-designer-plugin-webkit -f %{debug_package_exclude_files}
%{_qt5_plugindir}/designer/libqwebview.so
%{_qt5_libdir}/cmake/Qt5Designer/Qt5Designer_QWebViewPlugin.cmake
%endif

%files -n qt5-linguist -f %{debug_package_exclude_files}
%{_bindir}/linguist*
%{_qt5_bindir}/linguist*
# phrasebooks used by linguist
%{_qt5_datadir}/phrasebooks/
# linguist friends
%{_bindir}/lconvert*
%{_bindir}/lrelease*
%{_bindir}/lupdate*
%{_bindir}/lprodump*
%{_qt5_bindir}/lconvert*
%{_qt5_bindir}/lrelease*
%{_qt5_bindir}/lupdate*
%{_qt5_bindir}/lprodump*
# cmake config
%dir %{_qt5_libdir}/cmake/Qt5LinguistTools/
%{_qt5_libdir}/cmake/Qt5LinguistTools/Qt5LinguistToolsConfig*.cmake
%{_qt5_libdir}/cmake/Qt5LinguistTools/Qt5LinguistToolsMacros.cmake

%files -n qt5-qdbusviewer -f %{debug_package_exclude_files}
%{_bindir}/qdbusviewer*
%{_qt5_bindir}/qdbusviewer*

%files devel -f %{debug_package_exclude_files}
%{_bindir}/pixeltool*
%{_bindir}/qcollectiongenerator*
%{_bindir}/qdistancefieldgenerator*
#{_bindir}/qhelpconverter*
%{_bindir}/qtdiag*
%{_bindir}/qtplugininfo*
%{_qt5_bindir}/pixeltool*
%{_qt5_bindir}/qtdiag*
%{_qt5_bindir}/qcollectiongenerator*
%{_qt5_bindir}/qdistancefieldgenerator*
#{_qt5_bindir}/qhelpconverter*
%{_qt5_bindir}/qtplugininfo*
%{_qt5_headerdir}/QtDesigner/
%{_qt5_headerdir}/QtDesignerComponents/
%{_qt5_headerdir}/QtHelp/
%{_qt5_headerdir}/QtUiPlugin
%{_qt5_libdir}/Qt5Designer*.prl
%{_qt5_libdir}/Qt5Designer*.lib
%{_qt5_libdir}/Qt5Help.prl
%{_qt5_libdir}/Qt5Help.lib
%{_qt5_libdir}/Qt5UiPlugin.prl
%{_qt5_libdir}/cmake/Qt5Designer/Qt5DesignerConfig*.cmake
%{_qt5_libdir}/cmake/Qt5DesignerComponents/Qt5DesignerComponentsConfig*.cmake
%dir %{_qt5_libdir}/cmake/Qt5Help/
%{_qt5_libdir}/cmake/Qt5Help/Qt5HelpConfig*.cmake
%{_qt5_libdir}/cmake/Qt5UiPlugin/
%{_qt5_libdir}/pkgconfig/Qt5Designer.pc
%{_qt5_libdir}/pkgconfig/Qt5Help.pc
%{_qt5_libdir}/pkgconfig/Qt5UiPlugin.pc
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_designer.pri
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_designer_private.pri
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_designercomponents_private.pri
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_help.pri
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_help_private.pri
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_uiplugin.pri

%files static -f %{debug_package_exclude_files}
%{_qt5_headerdir}/QtUiTools/
%{_qt5_libdir}/Qt5UiTools.lib
%{_qt5_libdir}/Qt5UiTools.prl
%{_qt5_libdir}/cmake/Qt5UiTools/
%{_qt5_libdir}/pkgconfig/Qt5UiTools.pc
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_uitools.pri
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_uitools_private.pri

%if ! 0%{?no_examples:1}
%files examples -f %{debug_package_exclude_files}
%{_qt5_examplesdir}/
%{_qt5_plugindir}/designer/*
%dir %{_qt5_libdir}/cmake/Qt5Designer
%{_qt5_libdir}/cmake/Qt5Designer/Qt5Designer_*
%endif


%global wps_folder_title Qt 5 Tools


%post -n qt5-assistant
if [ "$1" -ge 1 ]; then # (upon update)
    %wps_object_delete_all -n qt5-assistant
fi
%global wps_app_title Qt Assistant
%bww_folder -t %{wps_folder_title} -n qt5-assistant -s %{name}-apps
%bww_app -f %{_bindir}/assistant-qt5.exe -t %{wps_app_title} -n qt5-assistant

%postun -n qt5-assistant
if [ "$1" -eq 0 ]; then # (upon removal)
    %wps_object_delete_all -n qt5-assistant
fi


%post -n qt5-designer
if [ "$1" -ge 1 ]; then # (upon update)
    %wps_object_delete_all -n qt5-designer
fi
%global wps_app_title Qt Designer
%bww_folder -t %{wps_folder_title} -n qt5-designer -s %{name}-apps
%bww_app -f %{_bindir}/designer-qt5.exe -t %{wps_app_title} -n qt5-designer

%postun -n qt5-designer
if [ "$1" -eq 0 ]; then # (upon removal)
    %wps_object_delete_all -n qt5-designer
fi


%post -n qt5-linguist
if [ "$1" -ge 1 ]; then # (upon update)
    %wps_object_delete_all -n qt5-linguist
fi
%global wps_app_title Qt Linguist
%bww_folder -t %{wps_folder_title} -n qt5-linguist -s %{name}-apps
%bww_app -f %{_bindir}/linguist-qt5.exe -t %{wps_app_title} -n qt5-linguist

%postun -n qt5-linguist
if [ "$1" -eq 0 ]; then # (upon removal)
    %wps_object_delete_all -n qt5-linguist
fi


# TODO: no app for qdbusviewer for now


%if ! 0%{?no_examples:1}
%_qt5_examples_package_post
%_qt5_examples_package_postun
%endif

%changelog
* Thu Oct 17 2019 Dmitriy Kuminov <coding@dmik.org> 5.13.1-1
- Initial release.
