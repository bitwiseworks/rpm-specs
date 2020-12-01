%define __cmake_in_source_build 1

# Do not build python3 bindings for RHEL <= 7
%if 0%{?rhel} && 0%{?rhel} <= 7 || 0%{?os2_version}
%bcond_with python3
%else
%bcond_without python3
%endif

# Do not build python2 bindings for RHEL > 7 and Fedora > 29
%if 0%{?rhel} > 7 || 0%{?fedora} > 29
%bcond_with python2
%else
%bcond_without python2
%endif

Name:           libcomps
Version:        0.1.15
Release:        1%{?dist}
Summary:        Comps XML file manipulation library

License:        GPLv2+
URL:            https://github.com/rpm-software-management/libcomps
%if !0%{?os2_version}
Source0:        %{url}/archive/%{name}-%{version}/%{name}-%{version}.tar.gz
%else
Vendor:         bww bitwise works GmbH
%scm_source     github https://github.com/bitwiseworks/%{name}-os2 %{name}-%{version}-os2
%endif

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  libxml2-devel
BuildRequires:  check-devel
BuildRequires:  expat-devel
BuildRequires:  zlib-devel

%description
Libcomps is library for structure-like manipulation with content of
comps XML files. Supports read/write XML file, structure(s) modification.

%package devel
Summary:        Development files for libcomps library
Requires:       %{name} = %{version}-%{release}

%description devel
Development files for libcomps library.

%if !0%{?os2_version}
%package doc
Summary:        Documentation files for libcomps library
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch
BuildRequires:  doxygen

%description doc
Documentation files for libcomps library.

%package -n python-%{name}-doc
Summary:        Documentation files for python bindings libcomps library
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch
%if %{with python3}
BuildRequires:  python3-sphinx
%endif
%if %{with python2}
%if 0%{?rhel} && 0%{?rhel} <= 7
BuildRequires:  python-sphinx
%else
BuildRequires:  python2-sphinx
%endif
%endif

%description -n python-%{name}-doc
Documentation files for python bindings libcomps library.
%endif

%if %{with python2}
%package -n python2-%{name}
Summary:        Python 2 bindings for libcomps library
%{?python_provide:%python_provide python2-%{name}}
BuildRequires:  python2-devel
Requires:       %{name} = %{version}-%{release}

%description -n python2-%{name}
Python 2 bindings for libcomps library.
%endif

%if %{with python3}
%package -n python3-%{name}
Summary:        Python 3 bindings for libcomps library
BuildRequires:  python3-devel
%{?python_provide:%python_provide python3-%{name}}
Requires:       %{name} = %{version}-%{release}
Obsoletes:      platform-python-%{name} < %{version}-%{release}

%description -n python3-%{name}
Python3 bindings for libcomps library.
%endif

%debug_package

%prep
%if !0%{?os2_version}
%autosetup -p1 -n %{name}-%{name}-%{version}
%else
%scm_setup
%endif

%if %{with python2}
mkdir build-py2
%endif
%if %{with python3}
mkdir build-py3
%endif
mkdir build-doc

%build
%if 0%{?os2_version}
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"
export VENDOR="%{vendor}"
%endif

%if %{with python2}
%if !0%{?os2_version}
pushd build-py2
  %cmake ../libcomps/ -DPYTHON_DESIRED:STRING=2
  %make_build
popd
%else
cd build-py2
  %cmake ../libcomps/ -DPYTHON_DESIRED:STRING=2 -DENABLE_DOCS=0
  make
cd ..
%endif
%endif

%if %{with python3}
pushd build-py3
  %cmake ../libcomps/ -DPYTHON_DESIRED:STRING=3
  %make_build
popd
%endif

%if !0%{?os2_version}
pushd build-doc
%if %{with python2}
  %cmake ../libcomps/ -DPYTHON_DESIRED:STRING=2
%else
%if %{with python3}
  %cmake ../libcomps/ -DPYTHON_DESIRED:STRING=3
%endif
%endif
  make %{?_smp_mflags} docs
  make %{?_smp_mflags} pydocs
popd
%endif

%install
%if %{with python2}
%if !0%{?os2_version}
pushd build-py2
%else
cd build-py2
%endif
  %make_install
%if !0%{?os2_version}
popd
%else
cd ..
%endif
%endif

%if %{with python3}
pushd build-py3
  %make_install
popd
%endif

%check
%if %{with python2}
%if !0%{?os2_version}
pushd build-py2
%else
cd build-py2
%endif
  make test
  make pytest
%if !0%{?os2_version}
popd
%else
cd ..
%endif
%endif

%if %{with python3}
pushd build-py3
  make test
  make pytest
popd
%endif

%if !0%{?os2_version}
%if %{undefined ldconfig_scriptlets}
%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%else
%ldconfig_scriptlets
%endif
%endif

%files
%license COPYING
%doc README.md
%if !0%{?os2_version}
%{_libdir}/%{name}.so.*
%else
%{_libdir}/comps*.dll
%endif

%files devel
%if !0%{?os2_version}
%{_libdir}/%{name}.so
%else
%{_libdir}/*_dll.a
%endif
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/%{name}/

%if !0%{?os2_version}
%files doc
%doc build-doc/docs/libcomps-doc/html

%files -n python-%{name}-doc
%doc build-doc/src/python/docs/html
%endif

%if %{with python2}
%files -n python2-%{name}
%{python2_sitearch}/%{name}/
%if 0%{?os2_version}
%exclude %{python2_sitearch}/%{name}/*.dbg
%endif
%{python2_sitearch}/%{name}-%{version}-py%{python2_version}.egg-info
%endif

%if %{with python3}
%files -n python3-%{name}
%{python3_sitearch}/%{name}/
%if 0%{?os2_version}
%exclude %{python2_sitearch}/%{name}/*.dbg
%endif
%{python3_sitearch}/%{name}-%{version}-py%{python3_version}.egg-info
%endif

%changelog
* Mon Nov 30 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.1.15-1
- first OS/2 rpm
