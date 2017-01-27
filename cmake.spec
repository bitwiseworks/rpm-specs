#define svn_url     e:/trees/cmake/trunk
%define svn_url     http://svn.netlabs.org/repos/ports/cmake/trunk
%define svn_rev     1949


# Set to bcond_with or use --without gui to disable qt4 gui build
%bcond_without gui

# Set to bcond_without or use --with desktop to enable desktopn stuff
%bcond_with desktop

# Place rpm-macros into proper location
%global rpm_macros_dir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)

# Setup _pkgdocdir if not defined already
%{!?_pkgdocdir:%global _pkgdocdir %{_docdir}/%{name}-%{version}}

# enable this when we have Sphinx-build
%bcond_with sphinx

%global major_version 3
%global minor_version 7
%global orig_name cmake


Name:           %{orig_name}%{?name_suffix}
Version:        %{major_version}.%{minor_version}.0
Release:        2%{?dist}
Summary:        Cross-platform make system

# most sources are BSD
# Source/CursesDialog/form/ a bunch is MIT
# Source/kwsys/MD5.c is zlib
# some GPL-licensed bison-generated files, which all include an
# exception granting redistribution under terms of your choice
License:        BSD and MIT and zlib
URL:            http://www.cmake.org
Vendor:         bww bitwise works GmbH
Source:         %{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip
Source2:        macros.%{name}


#BuildRequires:  gcc-gfortran
#BuildRequires:  ncurses-devel, libX11-devel
BuildRequires:  bzip2-devel
BuildRequires:  curl-devel
BuildRequires:  expat-devel
#BuildRequires:  jsoncpp-devel
#BuildRequires:  libarchive-devel
#BuildRequires:  libuv-devel
%if 0%{?with_sphinx:1}
BuildRequires:  /@unixroot/usr/bin/sphinx-build
%endif
BuildRequires:  xz-devel
BuildRequires:  zlib-devel
#BuildRequires:  emacs
BuildRequires:  python2-devel
%if %{with gui}
BuildRequires: libqt4-devel
#BuildRequires: desktop-file-utils
%global qt_gui --qt-gui
%endif

Requires:       %{name}-data = %{version}-%{release}
Requires:       rpm

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
BuildArch:      noarch

%description    data
This package contains common data-files for %{name}.


%package        doc
Summary:        Documentation for %{name}
BuildArch:      noarch

%description    doc
This package contains documentation for %{name}.


%package        gui
Summary:        Qt GUI for %{name}

Requires:       %{name} = %{version}-%{release}
#Requires:       hicolor-icon-theme
#Requires:       shared-mime-info

%description    gui
The %{name}-gui package contains the Qt based GUI for %{name}.


%debug_package


%prep
%if %{?svn_rev:%(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')}%{!?svn_rev):0}
%setup -q
%else
%setup -n "%{name}-%{version}" -Tc
svn export %{?svn_rev:-r %{svn_rev}} %{svn_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip" "%{name}-%{version}")
%endif


%build
export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"
export LDFLAGS="-Zomf -Zhigh-mem -lcx %{?__global_ldflags}"
export VENDOR="%{vendor}"
mkdir build
cd build
#             --%{?with_bootstrap:no-}system-libs \
../bootstrap --prefix=%{_prefix} --datadir=/share/%{name} \
             --docdir=/share/doc/%{name} --mandir=/share/man \
             --verbose --system-bzip2 --system-curl --system-expat \
             --system-liblzma --system-zlib \
             %{?with_sphinx:--sphinx-man --sphinx-html} \
             %{?qt_gui} -- \
             -DCMAKE_USE_OPENSSL:BOOL=ON 

make


%install
cd build
make install DESTDIR=%{buildroot}
find %{buildroot}/%{_datadir}/%{name}/Modules -type f | xargs chmod -x
[ -n "$(find %{buildroot}/%{_datadir}/%{name}/Modules -name \*.orig)" ] &&
  echo "Found .orig files in %{_datadir}/%{name}/Modules, rebase patches" &&
  exit 1
cd ..

# RPM macros
install -p -m0644 -D %{SOURCE2} %{buildroot}%{rpm_macros_dir}/macros.%{name}
sed -i -e "s|@@CMAKE_VERSION@@|%{version}|" -e "s|@@CMAKE_MAJOR_VERSION@@|%{major_version}|" %{buildroot}%{rpm_macros_dir}/macros.%{name}
touch -r %{SOURCE2} %{buildroot}%{rpm_macros_dir}/macros.%{name}

mkdir -p %{buildroot}%{_libdir}/%{name}
# Install copyright files for main package
find Source Utilities -type f -iname copy\* | while read f
do
  fname=$(basename $f)
  dir=$(dirname $f)
  dname=$(basename $dir)
  cp -p $f ./${fname}_${dname}
done

# Cleanup pre-installed documentation
%if 0%{?with_sphinx:1}
mv %{buildroot}%{_docdir}/%{name}/html .
%endif
rm -rf %{buildroot}%{_docdir}/%{name}
# Install documentation to _pkgdocdir
mkdir -p %{buildroot}%{_pkgdocdir}
cp -pr %{buildroot}%{_datadir}/%{name}/Help %{buildroot}%{_pkgdocdir}
mv %{buildroot}%{_pkgdocdir}/Help %{buildroot}%{_pkgdocdir}/rst
%if 0%{?with_sphinx:1}
mv html %{buildroot}%{_pkgdocdir}
%endif

%if %{with desktop}
# Desktop file
desktop-file-install --delete-original \
  --dir=%{buildroot}%{_datadir}/applications \
  %{buildroot}/%{_datadir}/applications/CMake%{?name_suffix}.desktop
%endif


%check
#cd build
#CMake.FileDownload, and CTestTestUpload require internet access
#bin/ctest%{?name_suffix} -V -E 'CMake.FileDownload|CTestTestUpload' %{?_smp_mflags}
#cd ..


%if %{with desktop}
%post gui
update-desktop-database &> /dev/null || :
/bin/touch --no-create %{_datadir}/mime || :
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun gui
update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/mime || :
    update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans gui
update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
%endif


%files
%doc %dir %{_pkgdocdir}
%license Copyright.txt*
%license COPYING*
#%{_bindir}/c%{name}.exe
%{_bindir}/%{name}.exe
%{_bindir}/cpack.exe
%{_bindir}/ctest.exe
%if 0%{?with_sphinx:1}
#%{_mandir}/man1/c%{name}.1.*
%{_mandir}/man1/%{name}.1.*
%{_mandir}/man1/cpack.1.*
%{_mandir}/man1/ctest.1.*
%{_mandir}/man7/*.7.*
%endif
%{_libdir}/%{name}/


%files data
%{_datadir}/aclocal/%{name}.m4
%{_datadir}/%{name}/
%{rpm_macros_dir}/macros.%{name}


%files doc
# Pickup license-files from main-pkg's license-dir
# If there's no license-dir they are picked up by %%doc previously
%{?_licensedir:%license %{_datadir}/licenses/%{name}*}
%doc %{_pkgdocdir}/


%if %{with gui}
%files gui
%{_bindir}/%{name}-gui.exe
%if %{with desktop}
%{_datadir}/applications/CMake%{?name_suffix}.desktop
%{_datadir}/mime/packages/
%{_datadir}/icons/hicolor/*/apps/CMake%{?name_suffix}Setup.png
%endif
%if 0%{?with_sphinx:1}
%{_mandir}/man1/%{name}-gui.1.*
%endif
%endif


%changelog
* Wed Jan 25 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 3.7.0-2
- adjust def file creation

* Mon Dec 05 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> 3.7.0-1
- initial rpm version
