%global libname solv

%if !0%{?os2_version}
%bcond_without python_bindings
%bcond_without perl_bindings
%bcond_without ruby_bindings
%else
%bcond_with python_bindings
%bcond_with perl_bindings
%bcond_with ruby_bindings
%endif
# Creates special prefixed pseudo-packages from appdata metadata
%bcond_without appdata
# Creates special prefixed "group:", "category:" pseudo-packages
%bcond_without comps
# For rich dependencies
%bcond_without complex_deps
%bcond_without helix_repo
%bcond_without suse_repo
%bcond_without debian_repo
%bcond_without arch_repo
# For handling deb + rpm at the same time
%bcond_without multi_semantics
%if !0%{?os2_version}
%bcond_without zchunk
%bcond_without zstd
%else
%bcond_with zchunk
%bcond_with zstd
%endif

%define __cmake_switch(b:) %[%{expand:%%{?with_%{-b*}}} ? "ON" : "OFF"]

Name:           lib%{libname}
Version:        0.7.16
Release:        1%{?dist}
Summary:        Package dependency solver

License:        BSD
URL:            https://github.com/openSUSE/libsolv
%if !0%{?os2_version}
Source:         %{url}/archive/%{version}/%{name}-%{version}.tar.gz
%else
Vendor:         bww bitwise works GmbH
%scm_source github http://github.com/bitwiseworks/libsolv-os2 %{version}-os2
%endif

BuildRequires:  cmake
BuildRequires:  gcc-c++
%if !0%{?os2_version}
BuildRequires:  ninja-build
%endif
BuildRequires:  pkgconfig(rpm)
BuildRequires:  zlib-devel
# -DWITH_LIBXML2=ON
BuildRequires:  libxml2-devel
# -DENABLE_LZMA_COMPRESSION=ON
BuildRequires:  xz-devel
# -DENABLE_BZIP2_COMPRESSION=ON
BuildRequires:  bzip2-devel
%if %{with zstd}
# -DENABLE_ZSTD_COMPRESSION=ON
BuildRequires:  libzstd-devel
%endif
%if %{with zchunk}
# -DENABLE_ZCHUNK_COMPRESSION=ON
BuildRequires:  pkgconfig(zck)
%endif
# https://bugzilla.redhat.com/show_bug.cgi?id=1830346
%if !0%{?os2_version}
Requires:       rpm%{?_isa} >= 4.16.0
%else
# as soon as we have the rpm version 4.16 we can enable the %[] expression as well
Requires:       rpm >= 4.13.0
%endif

%description
A free package dependency solver using a satisfiability algorithm. The
library is based on two major, but independent, blocks:

- Using a dictionary approach to store and retrieve package
  and dependency information.

- Using satisfiability, a well known and researched topic, for
  resolving package dependencies.

%package devel
Summary:        Development files for %{name}
%if !0%{?os2_version}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       rpm-devel%{?_isa}
%else
Requires:       %{name} = %{version}-%{release}
Requires:       rpm-devel
%endif

%description devel
Development files for %{name}.

%package tools
Summary:        Package dependency solver tools
%if !0%{?os2_version}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%else
Requires:       %{name} = %{version}-%{release}
%endif
# repo2solv dependencies. Used as execl()
Requires:       %{_bindir}/find

%description tools
Package dependency solver tools.

%package demo
Summary:        Applications demoing the %{name} library
%if !0%{?os2_version}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%else
Requires:       %{name} = %{version}-%{release}
%endif
# solv dependencies. Used as execlp() and system()
Requires:       %{_bindir}/curl
%if !0%{?os2_version}
Requires:       %{_bindir}/gpg2
%endif

%description demo
Applications demoing the %{name} library.

%if %{with perl_bindings}
%package -n perl-%{libname}
Summary:        Perl bindings for the %{name} library
BuildRequires:  swig
BuildRequires:  perl-devel
BuildRequires:  perl-generators
%if !0%{?os2_version}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%else
Requires:       %{name} = %{version}-%{release}
%endif

%description -n perl-%{libname}
Perl bindings for the %{name} library.
%endif

%if %{with ruby_bindings}
%package -n ruby-%{libname}
Summary:        Ruby bindings for the %{name} library
BuildRequires:  swig
BuildRequires:  ruby-devel
%if !0%{?os2_version}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%else
Requires:       %{name} = %{version}-%{release}
%endif

%description -n ruby-%{libname}
Ruby bindings for the %{name} library.
%endif

%if %{with python_bindings}
%package -n python3-%{libname}
Summary:        Python bindings for the %{name} library
%{?python_provide:%python_provide python3-%{libname}}
BuildRequires:  swig
BuildRequires:  python3-devel
%if !0%{?os2_version}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%else
Requires:       %{name} = %{version}-%{release}
%endif

%description -n python3-%{libname}
Python bindings for the %{name} library.

Python 3 version.
%endif

%if 0%{?os2_version}
%debug_package
%endif

%prep
%if !0%{?os2_version}
%autosetup -p1
%else
%scm_setup
%endif

%build
%if 0%{?os2_version}
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"
export VENDOR="%{vendor}"
%endif

%if !0%{?os2_version}
%cmake -GNinja                                            \
  -DFEDORA=1                                              \
%else
%cmake                                                    \
  -DOS2=1                                                 \
  -DWITHOUT_COOKIEOPEN=1                                  \
%endif
  -DENABLE_RPMDB=ON                                       \
  -DENABLE_RPMDB_BYRPMHEADER=ON                           \
  -DENABLE_RPMDB_LIBRPM=ON                                \
  -DENABLE_RPMPKG_LIBRPM=ON                               \
  -DENABLE_RPMMD=ON                                       \
%if !0%{?os2_version}
  -DENABLE_COMPS=%{__cmake_switch -b comps}               \
%else
  -DENABLE_COMPS=ON                                       \
%endif
%if !0%{?os2_version}
  -DENABLE_APPDATA=%{__cmake_switch -b appdata}           \
%else
  -DENABLE_APPDATA=ON                                     \
%endif
  -DUSE_VENDORDIRS=ON                                     \
  -DWITH_LIBXML2=ON                                       \
  -DENABLE_LZMA_COMPRESSION=ON                            \
  -DENABLE_BZIP2_COMPRESSION=ON                           \
%if !0%{?os2_version}
  -DENABLE_ZSTD_COMPRESSION=%{__cmake_switch -b zstd}     \
  -DENABLE_ZCHUNK_COMPRESSION=%{__cmake_switch -b zchunk} \
%else
  -DENABLE_ZSTD_COMPRESSION=OFF                           \
  -DENABLE_ZCHUNK_COMPRESSION=OFF                         \
%endif
%if %{with zchunk}
  -DWITH_SYSTEM_ZCHUNK=ON                                 \
%endif
%if !0%{?os2_version}
  -DENABLE_HELIXREPO=%{__cmake_switch -b helix_repo}      \
  -DENABLE_SUSEREPO=%{__cmake_switch -b suse_repo}        \
  -DENABLE_DEBIAN=%{__cmake_switch -b debian_repo}        \
  -DENABLE_ARCHREPO=%{__cmake_switch -b arch_repo}        \
  -DMULTI_SEMANTICS=%{__cmake_switch -b multi_semantics}  \
  -DENABLE_COMPLEX_DEPS=%{__cmake_switch -b complex_deps} \
  -DENABLE_PERL=%{__cmake_switch -b perl_bindings}        \
  -DENABLE_RUBY=%{__cmake_switch -b ruby_bindings}        \
  -DENABLE_PYTHON=%{__cmake_switch -b python_bindings}    \
%else
  -DENABLE_HELIXREPO=ON    \
  -DENABLE_SUSEREPO=ON     \
  -DENABLE_DEBIAN=ON       \
  -DENABLE_ARCHREPO=ON     \
  -DMULTI_SEMANTICS=ON     \
  -DENABLE_COMPLEX_DEPS=ON \
  -DENABLE_PERL=OFF        \
  -DENABLE_RUBY=OFF        \
  -DENABLE_PYTHON=OFF      \
%endif
%if %{with python_bindings}
  -DPYTHON_EXECUTABLE=%{python3}                          \
%endif
  %{nil}
%if !0%{?os2_version}
%cmake_build
%else
make
%endif

%install
%if !0%{?os2_version}
%cmake_install
%else
%make_install
%endif

%check
%if 0%{?os2_version}
export BEGINLIBPATH="%{_builddir}/%{buildsubdir}/src;%{_builddir}/%{buildsubdir}/ext"
%endif
%if !0%{?os2_version}
%ctest
%else
make test
%endif

%files
%license LICENSE*
%doc README
%if !0%{?os2_version}
%{_libdir}/%{name}.so.*
%{_libdir}/%{name}ext.so.*
%else
%{_libdir}/solv*.dll
%endif

%files devel
%if !0%{?os2_version}
%{_libdir}/%{name}.so
%{_libdir}/%{name}ext.so
%else
%{_libdir}/solv*_dll.a
%endif
%{_includedir}/%{libname}/
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/pkgconfig/%{name}ext.pc
# Own directory because we don't want to depend on cmake
%dir %{_datadir}/cmake/Modules/
%{_datadir}/cmake/Modules/FindLibSolv.cmake
%{_mandir}/man3/%{name}*.3*

# Some small macro to list tools with mans
%if !0%{?os2_version}
%global solv_tool() \
%{_bindir}/%{1}\
%{_mandir}/man1/%{1}.1*
%else
%global solv_tool() \
%{_bindir}/%{1}.exe \
%{_mandir}/man1/%{1}.1*
%endif

%files tools
%solv_tool deltainfoxml2solv
%solv_tool dumpsolv
%solv_tool installcheck
%solv_tool mergesolv
%solv_tool repomdxml2solv
%solv_tool rpmdb2solv
%solv_tool rpmmd2solv
%solv_tool rpms2solv
%solv_tool testsolv
%solv_tool updateinfoxml2solv
%solv_tool repo2solv
%if %{with comps}
  %solv_tool comps2solv
%endif
%if %{with appdata}
  %solv_tool appdata2solv
%endif
%if %{with debian_repo}
  %solv_tool deb2solv
%endif
%if %{with arch_repo}
  %solv_tool archpkgs2solv
  %solv_tool archrepo2solv
%endif
%if %{with helix_repo}
  %solv_tool helix2solv
%endif
%if %{with suse_repo}
  %solv_tool susetags2solv
%endif

%files demo
%solv_tool solv

%if %{with perl_bindings}
%files -n perl-%{libname}
%{perl_vendorarch}/%{libname}.pm
%{perl_vendorarch}/%{libname}.so
%endif

%if %{with ruby_bindings}
%files -n ruby-%{libname}
%{ruby_vendorarchdir}/%{libname}.so
%endif

%if %{with python_bindings}
%files -n python3-%{libname}
%{python3_sitearch}/_%{libname}.so
%{python3_sitearch}/%{libname}.py
%{python3_sitearch}/__pycache__/%{libname}.*
%endif

%changelog
* Tue Apr 20 2021 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.7.16-1
- first rpm version

