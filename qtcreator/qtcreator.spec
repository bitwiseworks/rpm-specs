#
# http://github.com/dmik/qt-creator-os2
#
# If you are a packager, please read HowToDistribute.txt for general
# instructions.
#

Name:       qtcreator
Vendor:     netlabs.org
License:    LGPLv2 with exceptions
Url:        http://qt.nokia.com/products/developer-tools

%define ver_major   2
%define ver_minor   2
%define ver_patch   1

%define os2_release 0

%define rpm_release 1

%define git_url     http://github.com/dmik/qt-creator-os2/zipball/v%{version}-os2

%define descr_brief Qt Creator is a lightweight, cross-platform integrated \
development environment (IDE) designed to make development with the Qt \
application framework even faster and easier.

%define pkg_wps_base            QTCREATOR
%define pkg_wps_folder_id       <WP_DESKTOP>

%define pkg_docdir      %{_docdir}/%{name}

%if 0%{?os2_release}
Version:    %{ver_major}.%{ver_minor}.%{ver_patch}.%{os2_release}
%else
Version:    %{ver_major}.%{ver_minor}.%{ver_patch}
%endif
Release:    %{rpm_release}

Source:     %{name}-%{version}.zip

BuildRequires: libqt4-devel
BuildRequires: libqt4-webkit-devel
BuildRequires: qt4-devel-tools

#------------------------------------------------------------------------------
# commons
#------------------------------------------------------------------------------

# process command line arguments
%if "%{?SOURCE_TREE}" == ""
%define SOURCE_TREE .
%else
%define skip_prep_export 1
%endif

# disable lxlite compression (Qt EXEs and DLLs are already compressed)
%define __os_install_post	%{nil}

#------------------------------------------------------------------------------
# main package
#------------------------------------------------------------------------------

Summary:    Lightweight and cross-platform IDE for Qt
Group:      Development/Tools

Requires:   libqt4-gui
Requires:   libqt4-webkit
Requires:   libqt4-designer

%description
%{descr_brief}

# @todo see notes in %install
%files
%defattr(-,root,root,-)
%dir %{pkg_docdir}/
%docdir %{pkg_docdir}/
%{pkg_docdir}/*
%{_libdir}/qtcreator/
%exclude %{_libdir}/qtcreator/share/doc/qtcreator/qtcreator.qch

%post
%wps_object_create_begin -n %{name}
%{pkg_wps_base}:WPProgram|Qt Creator|%{pkg_wps_folder_id}|EXENAME=((%{_libdir}/qtcreator/bin/qtcreator.exe))
%wps_object_create_end

%postun
%wps_object_delete_all -n %{name}

#------------------------------------------------------------------------------
%package doc
#------------------------------------------------------------------------------

Summary:    Qt Creator documentation
Group:      Documentation
BuildArch:  noarch

Requires:   %{name} = %{version}-%{release}

%description doc
%{descr_brief}

# @todo see notes in %install
%files doc
%doc %{_libdir}/qtcreator/share/doc/qtcreator/qtcreator.qch

#------------------------------------------------------------------------------
%prep
#------------------------------------------------------------------------------

%if !0%{?skip_prep}

%if 0%{?master_mode}
%if !0%{?skip_prep_export}
# get clean source tree from github (both for building and for SRPM)
%setup -n "%{name}-%{version}" -Tc
rm -f "%{_sourcedir}/%{name}-%{version}.zip"
wget --no-check-certificate %{git_url} -O %{_sourcedir}/%{name}-%{version}.zip
unzip -qq "%{_sourcedir}/%{name}-%{version}.zip"
mv "./$(ls -fx1 | grep qt-creator)/*" "./"
%else
# use source tree in %{SOURCE_TREE} (e.g. shadow build)
%setup -n "%{name}-%{version}" -Tc%{?skip_prep_clean:D}
%endif
%else
# use source zip (the dir name in it is different, so unzip/rename manually too)
%setup -n "%{name}-%{version}" -Tc
unzip -qq "%{_sourcedir}/%{name}-%{version}.zip"
mv "./$(ls -fx1 | grep qt-creator)/*" "./"
%endif

%endif # if !0%{?skip_prep}

#------------------------------------------------------------------------------
%build
#------------------------------------------------------------------------------

%if !0%{?skip_build}

die() { echo "ERROR: $@"; exit 1; }
check_var() { eval "[ -n \"\$$1\" ] || die \"$1 variable is not set.\""; }

# Qt source tree (DOS format)
SOURCE_TREE_D=$(echo "%{SOURCE_TREE}" | tr '/' '\\')

[ -z "$MAKE_JOBS" ] && MAKE_JOBS=1

# CMD.EXE is required by the build process for now
export MAKESHELL=%{os2_boot_drive}\\OS2\\CMD.EXE

qmake $SOURCE_TREE_D

make -j$MAKE_JOBS

%endif # if !0%{?skip_build}

#------------------------------------------------------------------------------
%install
#------------------------------------------------------------------------------

# @todo make install creates three subdirs: bin/, lib/ and share/. We install
# them all to %{_libdir}/qtcreator/ instead of placing files to system bin/
# lib/ and share/ because we need to patch sources to make it work:
#   1. qtcreator.exe creates and uses private DLLs with very common names (eg.
#      ExtSys.dll) so they cannot live in %{_libdir}. We should:
#      - Move these private DLLs and EXEs to %{_libdir}/qtcreator/ (this requres
#        patching the sources to add the new directory relative to the new EXE
#        location to the plugin search list).
#      - Create EXE wrappers that will live in %{_prefix}/bin/ and, when started,
#        start their couterparts living in %{_libdir}/qtcreator/ after adding
#        this path to BEGINLIBPATH.
#   2. Place qtcreator.qch...


%if !0%{?skip_install}

rm -rf %{buildroot}

# CMD.EXE is required by the build process for now
export MAKESHELL=%{os2_boot_drive}\\OS2\\CMD.EXE

INSTALL_ROOT="%{buildroot}%{_libdir}/qtcreator"

make install INSTALL_ROOT=$(echo "$INSTALL_ROOT" | sed -re 's,/,\\,g')

# copy READMEs (make install doesn't do that)
mkdir -p "%{buildroot}%{pkg_docdir}/"
cp -dp \
    "%{SOURCE_TREE}/LICENSE.LGPL" \
    "%{SOURCE_TREE}/LGPL_EXCEPTION.TXT" \
    "%{SOURCE_TREE}/README" \
    "%{buildroot}%{pkg_docdir}/"

# share/pixmaps/qtcreator_*.png is of no use ATM
rm -rf "$INSTALL_ROOT/share/pixmaps/"


# @todo temporarily split out .sym files (until we generate -debuginfo packages)
rm -rf %{buildroot}.sym
for f in $(cd "%{buildroot}" && find -type f -name "*.sym"); do
    fd="${f%/*}"/
    [ "$fp" = "$f/" ] && fd=
    [ -d "%{buildroot}.sym/$fd" ] || mkdir -p "%{buildroot}.sym/$fd"
    mv "%{buildroot}/$f" "%{buildroot}.sym/$fd"
done

%endif # if !0%{?skip_install}

#------------------------------------------------------------------------------
%clean
#------------------------------------------------------------------------------

%if !0%{?skip_clean}

%if 0%{?master_mode}
%if "%{?create_zips_script}" != ""
# @todo put split out .sym files back
(cd "%{buildroot}.sym" && find . -type f -name '*.sym' -exec mv "{}" "../%{buildroot}/{}" \;)
rm -rf "%{buildroot}.sym"
%{create_zips_script} "%{buildroot}" "%{_topdir}"
%endif
%endif

rm -rf %{buildroot}

%endif # if !0%{?skip_clean}

#------------------------------------------------------------------------------
%changelog
* Thu Sep 17 2011 Dmitriy Kuminov <dmik/coding.org> 2.2.1-1
- New release 2.2.1. See %{pkg_docdir}/changes-4.7.3 and
  %{pkg_docdir}/CHANGES.OS2 for more information.
