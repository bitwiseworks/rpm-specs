# Do we add appdata-files? (disabled)
# consider conditional on whether %%_metainfodir is defined or not instead -- rex
%bcond_with appdata

# Set to bcond_without or use --with bootstrap if bootstrapping a new release
# or architecture
%bcond_without bootstrap

# Build with Emacs support (disabled)
%bcond_with emacs

# Run git tests (disabled)
%bcond_with git_test

# Set to bcond_with or use --without gui to disable qt4 gui build
%bcond_without gui

# Use ncurses for colorful output
%bcond_without ncurses

# Setting the Python-version used by default
%bcond_with python3

# Enable RPM dependency generators for cmake files written in Python
%bcond_without rpm

# enable this when we have Sphinx-build (disabled)
%bcond_with sphinx

# Run tests (disabled)
%bcond_with test

# Enable X11 tests (disabled)
%bcond_with X11_test

# Place rpm-macros into proper location
%global rpm_macros_dir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)

# Setup _pkgdocdir if not defined already
%{!?_pkgdocdir:%global _pkgdocdir %{_docdir}/%{name}-%{version}}

%global major_version 3
%global minor_version 10
# Set to RC version if building RC, else %%{nil}
#global rcsuf rc3
%{?rcsuf:%global relsuf .%{rcsuf}}
%{?rcsuf:%global versuf -%{rcsuf}}

# Uncomment if building for EPEL
#global name_suffix %%{major_version}
%global orig_name cmake


Name:           %{orig_name}%{?name_suffix}
Version:        %{major_version}.%{minor_version}.3
Release:        1%{?dist}
Summary:        Cross-platform make system

# most sources are BSD
# Source/CursesDialog/form/ a bunch is MIT
# Source/kwsys/MD5.c is zlib
# some GPL-licensed bison-generated files, which all include an
# exception granting redistribution under terms of your choice
License:        BSD and MIT and zlib
URL:            http://www.cmake.org
Vendor:         bww bitwise works GmbH
%scm_source github http://github.com/bitwiseworks/cmake-os2 %{version}-os2
Source2:        macros.%{name}
# See https://bugzilla.redhat.com/show_bug.cgi?id=1202899
Source3:        %{name}.attr
Source4:        %{name}.prov
Source5:        %{name}.req

BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
#BuildRequires:  gcc-gfortran
BuildRequires:  sed
BuildRequires:  git
%if %{with X11_test}
BuildRequires:  libX11-devel
%endif
%if %{with ncurses}
BuildRequires:  ncurses-devel
%endif
%if %{with sphinx}
BuildRequires:  %{_bindir}/sphinx-build
%endif
%if %{without bootstrap}
BuildRequires:  bzip2-devel
BuildRequires:  curl-devel
BuildRequires:  expat-devel
#BuildRequires:  jsoncpp-devel
#BuildRequires:  libarchive-devel
#BuildRequires:  libuv-devel
#BuildRequires:  rhash-devel
BuildRequires:  xz-devel
BuildRequires:  zlib-devel
%endif
%if %{with emacs}
BuildRequires:  emacs
%endif
%if %{with rpm}
%if %{with python3}
%{!?python3_pkgversion: %global python3_pkgversion 3}
BuildRequires:  python%{python3_pkgversion}-devel
%else
BuildRequires:  python2-devel
%endif
%endif
%if %{with gui}
BuildRequires: pkgconfig(Qt5Widgets)
%if %{with appdata}
BuildRequires: desktop-file-utils
%endif
%endif

%if %{without bootstrap}
# Ensure we have our own rpm-macros in place during build.
BuildRequires:  %{name}-rpm-macros
%endif

Requires:       %{name}-data = %{version}-%{release}
Requires:       %{name}-rpm-macros = %{version}-%{release}
Requires:       %{name}-filesystem = %{version}-%{release}

# Provide the major version name
Provides: %{orig_name}%{major_version} = %{version}-%{release}


%description
CMake is used to control the software compilation process using simple
platform and compiler independent configuration files. CMake generates
native makefiles and workspaces that can be used in the compiler
environment of your choice. CMake is quite sophisticated: it is possible
to support complex environments requiring system configuration, preprocessor
generation, code generation, and template instantiation.


%package        data
Summary:        Common data-files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-filesystem = %{version}-%{release}
Requires:       %{name}-rpm-macros = %{version}-%{release}
%if %{with emacs}
Requires:       emacs-filesystem%{?_emacs_version: >= %{_emacs_version}}
%endif

BuildArch:      noarch

%description    data
This package contains common data-files for %{name}.


%package        doc
Summary:        Documentation for %{name}
BuildArch:      noarch

%description    doc
This package contains documentation for %{name}.


%package        filesystem
Summary:        Directories used by CMake modules

%description    filesystem
This package owns all directories used by CMake modules.


%if %{with gui}
%package        gui
Summary:        Qt GUI for %{name}

Requires:       %{name} = %{version}-%{release}
%if %{with appdata}
Requires:       hicolor-icon-theme
Requires:       shared-mime-info
%endif

%description    gui
The %{name}-gui package contains the Qt based GUI for %{name}.
%endif


%package        rpm-macros
Summary:        Common RPM macros for %{name}
Requires:       rpm
# when subpkg introduced
Conflicts:      cmake-data < 3.10.1-2

BuildArch:      noarch

%description    rpm-macros
This package contains common RPM macros for %{name}.


%debug_package


%prep
%scm_setup

%if %{with rpm}
%if %{with python3}
echo '#!%{__python3}' > %{name}.prov
echo '#!%{__python3}' > %{name}.req
%else
echo '#!%{__python2}' > %{name}.prov
echo '#!%{__python2}' > %{name}.req
%endif
tail -n +2 %{SOURCE4} >> %{name}.prov
tail -n +2 %{SOURCE5} >> %{name}.req
%endif


%build
export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"
export LDFLAGS="-Zomf -Zhigh-mem -lcx %{?__global_ldflags}"
export VENDOR="%{vendor}"
mkdir build
cd build
#             --%{?with_bootstrap:no-}system-libs \
#             --parallel=`/usr/bin/getconf _NPROCESSORS_ONLN` \
../bootstrap --prefix=%{_prefix} --datadir=/share/%{name} \
             --docdir=/share/doc/%{name} --mandir=/share/man \
             --verbose --system-bzip2 --system-curl --system-expat \
             --system-liblzma --system-zlib \
%if %{with sphinx}
             --sphinx-man --sphinx-html} \
%else
             --sphinx-build=%{_bindir}/false \
%endif
             --%{!?with_gui:no-}qt-gui \
             -- -DCMAKE_USE_OPENSSL:BOOL=ON \
;
make VERBOSE=1


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_pkgdocdir}
%make_install -C build CMAKE_DOC_DIR=%{buildroot}%{_pkgdocdir}
find %{buildroot}/%{_datadir}/%{name}/Modules -type f | xargs chmod -x
[ -n "$(find %{buildroot}/%{_datadir}/%{name}/Modules -name \*.orig)" ] &&
  echo "Found .orig files in %{_datadir}/%{name}/Modules, rebase patches" &&
  exit 1
# Install major_version name links
%{!?name_suffix:for f in ccmake cmake cpack ctest; do ln -s ${f}.exe %{buildroot}%{_bindir}/${f}%{major_version}; done}
# Install bash completion symlinks
#mkdir -p %{buildroot}%{_datadir}/bash-completion/completions
#for f in %{buildroot}%{_datadir}/%{name}/completions/*
#do
#  ln -s ../../%{name}/completions/$(basename $f) %{buildroot}%{_datadir}/bash-completion/completions
#done
%if %{with emacs}
# Install emacs cmake mode
mkdir -p %{buildroot}%{_emacs_sitelispdir}/%{name}
install -p -m 0644 Auxiliary/cmake-mode.el %{buildroot}%{_emacs_sitelispdir}/%{name}/%{name}-mode.el
%{_emacs_bytecompile} %{buildroot}%{_emacs_sitelispdir}/%{name}/%{name}-mode.el
mkdir -p %{buildroot}%{_emacs_sitestartdir}
install -p -m 0644 %SOURCE1 %{buildroot}%{_emacs_sitestartdir}
%endif
# RPM macros
install -p -m0644 -D %{SOURCE2} %{buildroot}%{rpm_macros_dir}/macros.%{name}
sed -i -e "s|@@CMAKE_VERSION@@|%{version}|" -e "s|@@CMAKE_MAJOR_VERSION@@|%{major_version}|" %{buildroot}%{rpm_macros_dir}/macros.%{name}
touch -r %{SOURCE2} %{buildroot}%{rpm_macros_dir}/macros.%{name}
%if %{with rpm} && 0%{?_rpmconfigdir:1}
# RPM auto provides
install -p -m0644 -D %{SOURCE3} %{buildroot}%{_prefix}/lib/rpm/fileattrs/%{name}.attr
install -p -m0755 -D %{name}.prov %{buildroot}%{_prefix}/lib/rpm/%{name}.prov
install -p -m0755 -D %{name}.req %{buildroot}%{_prefix}/lib/rpm/%{name}.req
%endif
mkdir -p %{buildroot}%{_libdir}/%{orig_name}
# Install copyright files for main package
find Source Utilities -type f -iname copy\* | while read f
do
  fname=$(basename $f)
  dir=$(dirname $f)
  dname=$(basename $dir)
  cp -p $f ./${fname}_${dname}
done
# Cleanup pre-installed documentation
%if %{with sphinx}
mv %{buildroot}%{_docdir}/%{name}/html .
%endif
rm -rf %{buildroot}%{_docdir}/%{name}
# Install documentation to _pkgdocdir
mkdir -p %{buildroot}%{_pkgdocdir}
cp -pr %{buildroot}%{_datadir}/%{name}/Help %{buildroot}%{_pkgdocdir}
mv %{buildroot}%{_pkgdocdir}/Help %{buildroot}%{_pkgdocdir}/rst
%if %{with sphinx}
mv html %{buildroot}%{_pkgdocdir}
%endif

%if %{with gui}
# Desktop file
%if %{with appdata}
desktop-file-install --delete-original \
  --dir=%{buildroot}%{_datadir}/applications \
  %{buildroot}%{_datadir}/applications/%{name}-gui.desktop

# Register as an application to be visible in the software center
#
# NOTE: It would be *awesome* if this file was maintained by the upstream
# project, translated and installed into the right place during `make install`.
#
# See http://www.freedesktop.org/software/appstream/docs/ for more details.
#
mkdir -p %{buildroot}%{_metainfodir}
cat > %{buildroot}%{_metainfodir}/cmake-gui.appdata.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!-- Copyright 2014 Ryan Lerch <rlerch@redhat.com> -->
<!--
EmailAddress: kitware@kitware.com
SentUpstream: 2014-09-17
-->
<application>
  <id type="desktop">cmake-gui.desktop</id>
  <metadata_license>CC0-1.0</metadata_license>
  <name>CMake GUI</name>
  <summary>Create new CMake projects</summary>
  <description>
    <p>
      CMake is an open source, cross platform build system that can build, test,
      and package software. CMake GUI is a graphical user interface that can
      create and edit CMake projects.
    </p>
  </description>
  <url type="homepage">http://www.cmake.org</url>
  <screenshots>
    <screenshot type="default">https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/CMake/a.png</screenshot>
  </screenshots>
  <!-- FIXME: change this to an upstream email address for spec updates
  <updatecontact>someone_who_cares@upstream_project.org</updatecontact>
   -->
</application>
EOF
%endif
%endif

# create manifests for splitting files and directories for filesystem-package
find %{buildroot}%{_datadir}/%{name} -type d | \
  sed -e 's!^%{buildroot}!%%dir "!g' -e 's!$!"!g' > data_dirs.mf
find %{buildroot}%{_datadir}/%{name} -type f | \
  sed -e 's!^%{buildroot}!"!g' -e 's!$!"!g' > data_files.mf
find %{buildroot}%{_libdir}/%{orig_name} -type d | \
  sed -e 's!^%{buildroot}!%%dir "!g' -e 's!$!"!g' > lib_dirs.mf
find %{buildroot}%{_libdir}/%{orig_name} -type f | \
  sed -e 's!^%{buildroot}!"!g' -e 's!$!"!g' > lib_files.mf
find %{buildroot}%{_bindir} -type f -or -type l -or -xtype l | \
  sed -e '/.*-gui.exe$/d' -e '/^$/d' -e 's!^%{buildroot}!"!g' -e 's!$!"!g' >> lib_files.mf


%if %{with test}
%check
cd build
#CMake.FileDownload, CTestTestUpload, and curl require internet access
# RunCMake.CPack_RPM is broken if disttag contains "+", bug #1499151
NO_TEST="CMake.FileDownload|CTestTestUpload|curl|RunCMake.CPack_RPM"
NO_TEST="$NO_TEST|CPackComponentsForAll-RPM-IgnoreGroup"
# RunCMake.File_Generate fails on S390X
%ifarch s390x
NO_TEST="$NO_TEST|RunCMake.File_Generate"
%endif
export NO_TEST
bin/ctest%{?name_suffix} -V -E "$NO_TEST" %{?_smp_mflags}
cd ..
%endif


%files -f lib_files.mf
%doc %dir %{_pkgdocdir}
%license Copyright.txt*
%license COPYING*
%if %{with sphinx}
%{_mandir}/man1/c%{name}.1.*
%{_mandir}/man1/%{name}.1.*
%{_mandir}/man1/cpack%{?name_suffix}.1.*
%{_mandir}/man1/ctest%{?name_suffix}.1.*
%{_mandir}/man7/*.7.*
%endif


%files data -f data_files.mf
%{_datadir}/aclocal/%{name}.m4
#%{_datadir}/bash-completion
%if %{with emacs}
%{_emacs_sitelispdir}
%{_emacs_sitestartdir}
%endif


%files doc
# Pickup license-files from main-pkg's license-dir
# If there's no license-dir they are picked up by %%doc previously
#%{?_licensedir:%license %{_datadir}/licenses/%{name}*}
%doc %{_pkgdocdir}


%files filesystem -f data_dirs.mf -f lib_dirs.mf


%if %{with gui}
%files gui
%{_bindir}/%{name}-gui.exe
%if %{with appdata}
%{_metainfodir}/*.appdata.xml
%{_datadir}/applications/CMake%{?name_suffix}.desktop
%{_datadir}/mime/packages/
%{_datadir}/icons/hicolor/*/apps/CMake%{?name_suffix}Setup.png
%endif
%if %{with sphinx}
%{_mandir}/man1/%{name}-gui.1.*
%endif
%endif


%files rpm-macros
%{rpm_macros_dir}/macros.%{name}
%if %{with rpm} && 0%{?_rpmconfigdir:1}
%{_rpmconfigdir}/fileattrs/%{name}.attr
%{_rpmconfigdir}/%{name}.prov
%{_rpmconfigdir}/%{name}.req
%endif


%changelog
* Mon Sep 16 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> 3.10.3-1
- update to vendor version 3.10.3

* Wed Jan 25 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 3.7.0-2
- adjust def file creation

* Mon Dec 05 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> 3.7.0-1
- initial rpm version
