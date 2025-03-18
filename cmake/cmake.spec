# Do we add appdata-files?
# consider conditional on whether %%_metainfodir is defined or not instead -- rex
%if 0%{?fedora} || 0%{?rhel} > 7
%bcond_without appdata
%else
%bcond_with appdata
%endif

# Set to bcond_without or use --with bootstrap if bootstrapping a new release
# or architecture
%if !0%{?os2_version}
%bcond_with bootstrap
%else
%bcond_without bootstrap
%endif

# Build with Emacs support
%if !0%{?os2_version}
%bcond_without emacs
%else
%bcond_with emacs
%global _emacs_sitelispdir %{_prefix}/share/emacs
%endif

# Run git tests
%if !0%{?os2_version}
%bcond_without git_test
%else
%bcond_with git_test
%endif

# Set to bcond_with or use --without gui to disable qt gui build
%bcond_without gui

# Use ncurses for colorful output
%bcond_without ncurses

# Setting the Python-version used by default
%if 0%{?rhel} && 0%{?rhel} < 8
%bcond_with python3
%else
%bcond_without python3
%endif

# Enable RPM dependency generators for cmake files written in Python
%bcond_without rpm

%if !0%{?os2_version}
%bcond_without sphinx
%else
%bcond_with sphinx
%endif

%if !0%{?rhel}
%bcond_with bundled_jsoncpp
%bcond_with bundled_rhash
%else
%bcond_without bundled_jsoncpp
%bcond_without bundled_rhash
%endif

# cppdap is currently shipped as a static lib from upstream,
# so we do not have it in the repos.
%if !0%{?os2_version}
%bcond_without bundled_cppdap
%else
%bcond_with bundled_cppdap
%endif

# Run tests
%if !0%{?os2_version}
%bcond_without test
%else
%bcond_with test
%endif

# Enable X11 tests
%if !0%{?os2_version}
%bcond_without X11_test
%else
%bcond_with X11_test
%endif

# Do not build non-lto objects to reduce build time significantly.
%global build_cflags   %(echo '%{build_cflags}'   | sed -e 's!-ffat-lto-objects!-fno-fat-lto-objects!g')
%global build_cxxflags %(echo '%{build_cxxflags}' | sed -e 's!-ffat-lto-objects!-fno-fat-lto-objects!g')
%global build_fflags   %(echo '%{build_fflags}' | sed -e 's!-ffat-lto-objects!-fno-fat-lto-objects!g')
%global build_fcflags  %(echo '%{build_fflags}' | sed -e 's!-ffat-lto-objects!-fno-fat-lto-objects!g')

# Place rpm-macros into proper location
%global rpm_macros_dir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)

# Setup _pkgdocdir if not defined already
%{!?_pkgdocdir:%global _pkgdocdir %{_docdir}/%{name}-%{version}}

# Setup _vpath_builddir if not defined already
%{!?_vpath_builddir:%global _vpath_builddir %{_target_platform}}

%global major_version 3
%global minor_version 31
%global patch_version 6

# For handling bump release by rpmdev-bumpspec and mass rebuild
%global baserelease 1

# Set to RC version if building RC, else comment out.
#%%global rcsuf rc3

%if 0%{?rcsuf:1}
%global pkg_version %{major_version}.%{minor_version}.%{patch_version}~%{rcsuf}
%global tar_version %{major_version}.%{minor_version}.%{patch_version}-%{rcsuf}
%else
%global pkg_version %{major_version}.%{minor_version}.%{patch_version}
%global tar_version %{major_version}.%{minor_version}.%{patch_version}
%endif

# Uncomment if building for EPEL
#global name_suffix %%{major_version}
%global orig_name cmake

Name:           %{orig_name}%{?name_suffix}
Version:        %{pkg_version}
Release:        %{baserelease}%{?dist}
Summary:        Cross-platform make system

# most sources are BSD
# Source/CursesDialog/form/ a bunch is MIT
# Source/kwsys/MD5.c is zlib
# some GPL-licensed bison-generated files, which all include an
# exception granting redistribution under terms of your choice
License:        BSD-3-Clause AND MIT-open-group AND Zlib%{?with_bundled_cppdap: AND Apache-2.0}
URL:            http://www.cmake.org
%if !0%{?os2_version}
Source0:        http://www.cmake.org/files/v%{major_version}.%{minor_version}/%{orig_name}-%{tar_version}.tar.gz
Source1:        %{name}-init.el
%else
Vendor:         bww bitwise works GmbH
%scm_source github http://github.com/bitwiseworks/cmake-os2 %{version}-os2
%endif
Source2:        macros.%{name}.in
# See https://bugzilla.redhat.com/show_bug.cgi?id=1202899
Source3:        %{name}.attr
Source4:        %{name}.prov
Source5:        %{name}.req

%if !0%{?os2_version}
# Always start regular patches with numbers >= 100.
# We need lower numbers for patches in compat package.
# And this enables us to use %%autosetup
#
# Patch to fix RindRuby vendor settings
# http://public.kitware.com/Bug/view.php?id=12965
# https://bugzilla.redhat.com/show_bug.cgi?id=822796
Patch100:       %{name}-findruby.patch

# Patch for renaming on EPEL
%if 0%{?name_suffix:1}
Patch1:         %{name}-rename.patch
%endif
%endif

BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc-c++
%if !0%{?os2_version}
BuildRequires:  gcc-gfortran
%endif
BuildRequires:  sed
%if !0%{?os2_version}
%if %{with git_test}
# Tests fail if only git-core is installed, bug #1488830
BuildRequires:  git
%else
BuildConflicts: git-core
%endif
%endif
%if %{with X11_test}
BuildRequires:  libX11-devel
%endif
%if %{with ncurses}
BuildRequires:  ncurses-devel
%endif
%if %{with sphinx}
BuildRequires:  %{_bindir}/sphinx-build
%endif
%if %{without bootstrap} || 0%{?os2_version}
BuildRequires:  bzip2-devel
BuildRequires:  curl-devel
%if !0%{?os2_version}
%if %{with bundled_cppdap}
Provides: bundled(cppdap)
%else
BuildRequires:  cppdap-devel
%endif
%endif
BuildRequires:  expat-devel
%if %{with bundled_jsoncpp}
Provides: bundled(jsoncpp)
%else
BuildRequires:  jsoncpp-devel
%endif
%if 0%{?fedora} || 0%{?rhel} >= 7 || 0%{?os2_version}
BuildRequires:  libarchive-devel
%else
BuildRequires:  libarchive3-devel
%endif
BuildRequires:  libuv-devel
%if %{with bundled_rhash}
Provides:  bundled(rhash)
%else
BuildRequires:  rhash-devel
%endif
BuildRequires:  xz-devel
BuildRequires:  zlib-devel
%if !0%{?os2_version}
BuildRequires:  vim-filesystem
%endif
%endif
%if %{with emacs}
BuildRequires:  emacs
%endif
BuildRequires:  openssl-devel
%if %{with rpm}
%if %{with python3}
%{!?python3_pkgversion: %global python3_pkgversion 3}
BuildRequires:  python%{python3_pkgversion}-devel
%else
BuildRequires:  python2-devel
%endif
%endif
%if %{with gui}
%if 0%{?fedora} || 0%{?rhel} > 9
BuildRequires: pkgconfig(Qt6Widgets)
%else
%if 0%{?rhel} > 7 || 0%{?os2_version}
BuildRequires: pkgconfig(Qt5Widgets)
%else
BuildRequires: pkgconfig(QtGui)
%endif
%endif
%if !0%{?os2_version}
BuildRequires: desktop-file-utils
%endif
%endif

%if !0%{?os2_version}
BuildRequires: pkgconfig(bash-completion)
%global bash_completionsdir %(pkg-config --variable=completionsdir bash-completion 2>/dev/null || echo '%{_datadir}/bash-completion/completions')
%endif

%if %{without bootstrap}
# Ensure we have our own rpm-macros in place during build.
BuildRequires:  %{name}-rpm-macros
%endif
BuildRequires: make

Requires:       %{name}-data = %{version}-%{release}
%if !0%{?os2_version}
Requires:       (%{name}-rpm-macros = %{version}-%{release} if rpm-build)
Requires:       %{name}-filesystem%{?_isa} = %{version}-%{release}
%else
Requires:       %{name}-rpm-macros = %{version}-%{release}
Requires:       %{name}-filesystem = %{version}-%{release}
%endif

# Explicitly require make.  (rhbz#1862014)
Requires:       make

# Provide the major version name
Provides: %{orig_name}%{major_version} = %{version}-%{release}

# Source/kwsys/MD5.c
# see https://fedoraproject.org/wiki/Packaging:No_Bundled_Libraries
Provides: bundled(md5-deutsch)

# https://fedorahosted.org/fpc/ticket/555
Provides: bundled(kwsys)

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
%if !0%{?os2_version}
Requires:       (%{name}-rpm-macros = %{version}-%{release} if rpm-build)
%else
Requires:       %{name}-rpm-macros = %{version}-%{release}
%endif
%if %{with emacs}
%if 0%{?fedora} || 0%{?rhel} >= 7
Requires:       emacs-filesystem%{?_emacs_version: >= %{_emacs_version}}
%endif
%endif
%if !0%{?os2_version}
Requires:       vim-filesystem
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

%if !0%{?os2_version}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       hicolor-icon-theme
Requires:       shared-mime-info%{?_isa}
%else
Requires:       %{name} = %{version}-%{release}
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


%package -n python3-cmake
Summary:        Python metadata for packages depending on %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
BuildArch:      noarch

%description -n python3-cmake
Package provides metadata for Python packages depending on cmake.
This is to make automatic dependency resolution work. The package is NOT
using anything from the PyPI package called cmake.


%if 0%{?os2_version} && 0
%debug_package
%endif

%prep
%if !0%{?os2_version}
%autosetup -n %{orig_name}-%{tar_version} -p 1
%else
%scm_setup
%endif

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
%if !0%{?os2_version}
%{set_build_flags}
%else
CFLAGS="$(echo ${CFLAGS:-%optflags} | sed -re "s/(^|\s)-g(\s|\$)/ /g") -s" ; export CFLAGS
CXXFLAGS="$(echo ${CFLAGS:-%optflags} | sed -re "s/(^|\s)-g(\s|\$)/ /g") -s" ; export CXXFLAGS
FFLAGS="${FFLAGS:-%optflags%{?_fmoddir: -I%_fmoddir}}" ; export FFLAGS
FCFLAGS="${FCFLAGS:-%optflags%{?_fmoddir: -I%_fmoddir}}" ; export FCFLAGS
export LDFLAGS="-Zomf -Zhigh-mem -lcx %{?__global_ldflags}"
export VENDOR="%{vendor}"
%endif
%if !0%{?os2_version}
SRCDIR="$(/usr/bin/pwd)"
%else
SRCDIR="$(/@unixroot/usr/bin/pwd)"
%endif
mkdir %{_vpath_builddir}
%if !0%{?os2_version}
pushd %{_vpath_builddir}
%else
cd %{_vpath_builddir}
%endif
$SRCDIR/bootstrap --prefix=%{_prefix} \
                  --datadir=/share/%{name} \
                  --docdir=/share/doc/%{name} \
                  --mandir=/share/man \
%if !0%{?os2_version}
                  --%{?with_bootstrap:no-}system-libs \
%else
                  --bootstrap-system-libuv \
                  --system-libs \
                  --no-system-nghttp2 \
%endif
                  --parallel="$(echo %{?_smp_mflags} | sed -e 's|-j||g')" \
%if %{with bundled_cppdap}
                  --no-system-cppdap \
%endif
%if %{with bundled_rhash}
                  --no-system-librhash \
%endif
%if %{with bundled_jsoncpp}
                  --no-system-jsoncpp \
%endif
%if %{with sphinx}
                  --sphinx-man --sphinx-html \
%else
                  --sphinx-build=%{_bindir}/false \
%endif
                  --%{!?with_gui:no-}qt-gui \
                  -- \
                  -DCMAKE_C_FLAGS_RELEASE:STRING="-O2 -g -DNDEBUG" \
                  -DCMAKE_CXX_FLAGS_RELEASE:STRING="-O2 -g -DNDEBUG" \
                  -DCMAKE_Fortran_FLAGS_RELEASE:STRING="-O2 -g -DNDEBUG" \
                  -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
                  -DCMAKE_INSTALL_DO_STRIP:BOOL=OFF \
                  -DCMake_TEST_NO_NETWORK:BOOL=ON
%if !0%{?os2_version}
popd
%else
cd ..
%endif
%make_build -C %{_vpath_builddir}

# Provide Python metadata
%global cmake_distinfo cmake-%{major_version}.%{minor_version}.%{patch_version}%{?rcsuf}.dist-info
mkdir %{cmake_distinfo}
cat > %{cmake_distinfo}/METADATA << EOF
Metadata-Version: 2.1
Name: cmake
Version: %{major_version}.%{minor_version}.%{patch_version}%{?rcsuf}
Summary: %{summary}
Description-Content-Type: text/plain

Metadata only package for automatic dependency resolution in the RPM
ecosystem. This package is separate from the PyPI package called cmake.
EOF
echo rpm > %{cmake_distinfo}/INSTALLER


%install
mkdir -p %{buildroot}%{_pkgdocdir}
%make_install -C %{_vpath_builddir} CMAKE_DOC_DIR=%{buildroot}%{_pkgdocdir}
find %{buildroot}%{_datadir}/%{name}/Modules -type f | xargs chmod -x
[ -n "$(find %{buildroot}%{_datadir}/%{name}/Modules -name \*.orig)" ] &&
  echo "Found .orig files in %{_datadir}/%{name}/Modules, rebase patches" &&
  exit 1
# Install major_version name links
%if !0%{?os2_version}
%{!?name_suffix:for f in ccmake cmake cpack ctest; do ln -s $f %{buildroot}%{_bindir}/${f}%{major_version}; done}
%else
%{!?name_suffix:for f in ccmake cmake cpack ctest; do ln -s ${f}.exe %{buildroot}%{_bindir}/${f}%{major_version}; done}
%endif

%if 0%{?os2_version}
rm -rf %{buildroot}%{_prefix}/share/vim
rm -rf %{buildroot}%{_prefix}/share/bash-completion
%endif
%if %{with emacs}
# Install emacs cmake mode
mkdir -p %{buildroot}%{_emacs_sitelispdir}/%{name} %{buildroot}%{_emacs_sitestartdir}
mv %{buildroot}%{_emacs_sitelispdir}/%{name}-mode.el %{buildroot}%{_emacs_sitelispdir}/%{name}
%{_emacs_bytecompile} %{buildroot}%{_emacs_sitelispdir}/%{name}/%{name}-mode.el
install -p -m 0644 %{SOURCE1} %{buildroot}%{_emacs_sitestartdir}
%else
rm -rf %{buildroot}%{_emacs_sitelispdir}
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
%if %{with bundled_cppdap}
cp -p Utilities/cmcppdap/LICENSE LICENSE.cppdap
cp -p Utilities/cmcppdap/NOTICE NOTICE.cppdap
%endif
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
%if !0%{?os2_version}
desktop-file-install --delete-original \
  --dir=%{buildroot}%{_datadir}/applications \
  %{buildroot}%{_datadir}/applications/%{name}-gui.desktop
%endif

%if %{with appdata}
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
%if !0%{?os2_version}
find %{buildroot}%{_bindir} -type f -or -type l -or -xtype l | \
  sed -e '/.*-gui$/d' -e '/^$/d' -e 's!^%{buildroot}!"!g' -e 's!$!"!g' >> lib_files.mf
%else
find %{buildroot}%{_bindir} -type f -or -type l -or -xtype l | \
  sed -e '/.*-gui.exe$/d' -e '/^$/d' -e 's!^%{buildroot}!"!g' -e 's!$!"!g' >> lib_files.mf
%endif

# Install Python metadata
mkdir -p %{buildroot}%{python3_sitelib}
cp -a %{cmake_distinfo} %{buildroot}%{python3_sitelib}


%if %{with test}
%check
%if !0%{?os2_version}
pushd %{_vpath_builddir}
%else
cd %{_vpath_builddir}
%endif
# CTestTestUpload requires internet access.
NO_TEST="CTestTestUpload"
# Likely failing for hardening flags from system.
NO_TEST="$NO_TEST|CustomCommand|RunCMake.PositionIndependentCode"
# Failing for rpm 4.19
NO_TEST="$NO_TEST|CPackComponentsForAll-RPM-default"
NO_TEST="$NO_TEST|CPackComponentsForAll-RPM-OnePackPerGroup"
NO_TEST="$NO_TEST|CPackComponentsForAll-RPM-AllInOne"
# curl test may fail during bootstrap
%if %{with bootstrap}
NO_TEST="$NO_TEST|curl"
%endif
%ifarch riscv64
# These three tests timeout on riscv64, skip them.
NO_TEST="$NO_TEST|Qt5Autogen.ManySources|Qt5Autogen.MocInclude|Qt5Autogen.MocIncludeSymlink|Qt6Autogen.MocIncludeSymlink"
%endif
%if 0%{?fedora} == 41
# Test failing on Fedora 41, only.
NO_TEST="$NO_TEST|RunCMake.Make|RunCMake.BuildDepends|Qt6Autogen.RerunMocBasic|Qt6Autogen.RerunRccDepends"
%endif
bin/ctest%{?name_suffix} %{?_smp_mflags} -V -E "$NO_TEST" --output-on-failure
## do this only periodically, not for every build -- besser82 20221102
# Keep an eye on failing tests
#bin/ctest%{?name_suffix} %{?_smp_mflags} -V -R "$NO_TEST" --output-on-failure || :
%if !0%{?os2_version}
popd
%else
cd ..
%endif
%endif


%files -f lib_files.mf
%doc %dir %{_pkgdocdir}
%license Copyright.txt*
%license COPYING*
%if %{with bundled_cppdap}
%license LICENSE.cppdap
%license NOTICE.cppdap
%endif
%if %{with sphinx}
%{_mandir}/man1/c%{name}.1.*
%{_mandir}/man1/%{name}.1.*
%{_mandir}/man1/cpack%{?name_suffix}.1.*
%{_mandir}/man1/ctest%{?name_suffix}.1.*
%{_mandir}/man7/*.7.*
%endif


%files data -f data_files.mf
%{_datadir}/aclocal/%{name}.m4
%if !0%{?os2_version}
%{bash_completionsdir}/c*
%endif
%if %{with emacs}
%if 0%{?fedora} || 0%{?rhel} >= 7
%{_emacs_sitelispdir}/%{name}
%{_emacs_sitestartdir}/%{name}-init.el
%else
%{_emacs_sitelispdir}
%{_emacs_sitestartdir}
%endif
%endif
%if !0%{?os2_version}
%{vimfiles_root}/indent/%{name}.vim
%{vimfiles_root}/syntax/%{name}.vim
%endif
%if 0%{?os2_version}
%ghost %{_datadir}/%{name}/Modules/Platform/os2.cmake
%endif


%files doc
# Pickup license-files from main-pkg's license-dir
# If there's no license-dir they are picked up by %%doc previously
%{?_licensedir:%license %{_datadir}/licenses/%{name}*}
%doc %{_pkgdocdir}


%files filesystem -f data_dirs.mf -f lib_dirs.mf


%if %{with gui}
%files gui
%if !0%{?os2_version}
%{_bindir}/%{name}-gui
%else
%{_bindir}/%{name}-gui.exe
%endif
%if %{with appdata}
%{_metainfodir}/*.appdata.xml
%endif
%if !0%{?os2_version}
%{_datadir}/applications/%{name}-gui.desktop
%{_datadir}/mime/packages
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


%files -n python3-cmake
%{python3_sitelib}/%{cmake_distinfo}


%changelog
* Fri Mar 14 2025 Silvan Scherrer <silvan.scherrer@aroa.ch> 3.31.6-1
- update to vendor version 3.31.6
- add external rhash lib
- resync spec file with fedora

* Wed Nov 29 2023 Silvan Scherrer <silvan.scherrer@aroa.ch> 3.25.2-1
- update to vendor version 3.25.2

* Wed Mar 22 2023 Dmitriy Kuminov <coding@dmik.org> 3.20.6-3
- Disable HLL debug info due to overflows in EMXOMF tools.
- Clean up BUILDROOT before and after installing.

* Fri Feb 24 2023 Silvan Scherrer <silvan.scherrer@aroa.ch> 3.20.6-2
- fix a crash
- enable system jsoncpp

* Fri Jan 27 2023 Silvan Scherrer <silvan.scherrer@aroa.ch> 3.20.6-1
- update to vendor version 3.20.6
- resync spec file with fedora

* Fri Jan 31 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> 3.15.3-1
- update to vendor version 3.15.3
- build with gcc9
- add rc file handling
- disable 1121 wlink messages
- don't use emxexp for c++ by default anymore, it relies on declspec
  if you want the old way use -DOS2_USE_CXX_EMXEXP=ON 

* Mon Sep 16 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> 3.10.3-1
- update to vendor version 3.10.3

* Wed Jan 25 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 3.7.0-2
- adjust def file creation

* Mon Dec 05 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> 3.7.0-1
- initial rpm version
