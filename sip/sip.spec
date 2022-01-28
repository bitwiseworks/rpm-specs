%bcond_without python3
%if (0%{?fedora} && 0%{?fedora} < 32) || (0%{?rhel} && 0%{?rhel} < 9) || 0%{?os2_version}
%bcond_without python2
%endif

%if %{with python3}
%{!?python3_inc:%global python3_inc %(%{__python3} -c "from distutils.sysconfig import get_python_inc; print(get_python_inc(1))")}
%endif
%if !0%{?os2_version}
%{!?__python2:%global __python2 /usr/bin/python2}
%else
%{!?__python2:%global __python2 /@unixroot/usr/bin/python2}
%endif
%{!?python2_sitearch:%global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%{!?python2_inc:%global python2_inc %(%{__python2} -c "from distutils.sysconfig import get_python_inc; print get_python_inc(1)")}

%if 0%{?fedora} > 31 || 0%{?rhel} > 8 || 0%{?os2_version}
%global PYINCLUDE %{_includedir}/python%{python3_version}
%else
%global PYINCLUDE %{_includedir}/python%{python3_version}m
%endif

%global rpm_macros_dir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)

# trim changelog included in binary rpms
%global _changelog_trimtime %(date +%s -d "1 year ago")

# see also https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/thread/JQQ66XJSIT2FGTK2YQY7AXMEH5IXMPUX/
%undefine _strict_symbol_defs_build

# provide non-namespace python modules
# needed by at least some legacy/non-qt consumers, e.g. pykde4
%if 0%{?fedora} && 0%{?fedora} < 31
%global no_namespace 1
%endif

# Stop building siplib for wx on F34+
%if 0%{?fedora} && 0%{?fedora} >= 34 || 0%{?os2_version}
%global wx_siplib 0
%else
%global wx_siplib 1
%endif

# Stop building PyQt5.sip on F35+
%if 0%{?fedora} && 0%{?fedora} >= 35
%global pyqt5_sip 0
%else
%global pyqt5_sip 1
%endif

Summary: SIP - Python/C++ Bindings Generator
Name: sip
Version: 4.19.25
Release: 1%{?dist}

# sipgen/parser.{c.h} is GPLv3+ with exceptions (bison)
License: GPLv2 or GPLv3 and (GPLv3+ with exceptions)
Url: https://riverbankcomputing.com/software/sip/intro
%if !0%{?os2_version}
Source0: https://riverbankcomputing.com/static/Downloads/sip/%{version}/sip-%{version}%{?snap:.%{snap}}.tar.gz
%else
Vendor: bww bitwise works GmbH
%scm_source github http://github.com/bitwiseworks/sip-os2 v%{version}-os2
%endif

Source10: sip-wrapper.sh

%if !0%{?os2_version}
## upstream patches

## upstreamable patches
# make install should not strip (by default), kills -debuginfo
Patch50: sip-4.18-no_strip.patch
# try not to rpath the world (I *think* this may not be required anymore, since sip-4.19 -- rex)
Patch51: sip-4.18-no_rpath.patch
# set sip_bin properly for python3 build (needswork to be upstreamable)
# no longer needed?  keep for a little while before dropping completely -- rex
#Patch52: sip-4.19.3-python3_sip_bin.patch
# Avoid hardcoding sip.so (needed for wxpython's siplib.so)
Patch53: sip-4.19.18-no_hardcode_sip_so.patch
# Recognize the py_ssize_t_clean directive to avoid FTBFS with PyQt 5.15.6
Patch54: sip-4.19.25-py_ssize_t_clean.patch
%endif

# extracted from sip.h, SIP_API_MAJOR_NR SIP_API_MINOR_NR defines
Source1: macros.sip
%global _sip_api_major 12
%global _sip_api_minor 7
%global _sip_api %{_sip_api_major}.%{_sip_api_minor}

BuildRequires: make
BuildRequires: gcc-c++
BuildRequires: sed
BuildRequires: bison
BuildRequires: flex

Obsoletes: sip-macros < %{version}-%{release}
Provides:  sip-macros = %{version}-%{release}

# upgrade path when no_namespace variants are dropped
%if ! 0%{?no_namespace}
Obsoletes: python2-sip < %{version}-%{release}
Obsoletes: python3-sip < %{version}-%{release}
%endif

%global _description\
SIP is a tool for generating bindings for C++ classes so that they can be\
accessed as normal Python classes. SIP takes many of its ideas from SWIG but,\
because it is specifically designed for C++ and Python, is able to generate\
tighter bindings. SIP is so called because it is a small SWIG.\
\
SIP was originally designed to generate Python bindings for KDE and so has\
explicit support for the signal slot mechanism used by the Qt/KDE class\
libraries. However, SIP can be used to generate Python bindings for any C++\
class library.

%description %_description

%package doc
Summary: Documentation for %summary
BuildArch: noarch
%description doc
This package contains HTML documentation for SIP.
%_description

%if %{with python2}
%if 0%{?no_namespace}
%package -n python2-sip
Summary: %summary
Provides: sip-api(%{_sip_api_major}) = %{_sip_api}
Provides: sip-api(%{_sip_api_major})%{?_isa} = %{_sip_api}
Provides: python2-sip-api(%{_sip_api_major}) = %{_sip_api}
Provides: python2-sip-api(%{_sip_api_major})%{?_isa} = %{_sip_api}
%{?python_provide:%python_provide python2-sip}
%description -n python2-sip %_description
%endif

%package -n python2-sip-devel
Summary: Files needed to generate Python bindings for any C++ class library
Requires: sip = %{version}-%{release}
#Requires: python2-sip%{?_isa} = %{version}-%{release}
BuildRequires: python2-devel
Requires:      python2-devel
# Remove before F30
Provides: sip-devel = %{version}-%{release}
Provides: sip-devel%{?_isa} = %{version}-%{release}
Obsoletes: sip-devel < %{version}-%{release}
%description -n python2-sip-devel
%{summary}.

%package -n python2-pyqt4-sip
Summary: %summary
Provides: python2-pyqt4-sip-api(%{_sip_api_major}) = %{_sip_api}
Provides: python2-pyqt4-sip-api(%{_sip_api_major})%{?_isa} = %{_sip_api}
%{?python_provide:%python_provide python2-pyqt4-sip}
%description -n python2-pyqt4-sip %_description

%package -n python2-pyqt5-sip
Summary: %summary
Provides: python2-pyqt5-sip-api(%{_sip_api_major}) = %{_sip_api}
Provides: python2-pyqt5-sip-api(%{_sip_api_major})%{?_isa} = %{_sip_api}
%{?python_provide:%python_provide python2-pyqt5-sip}
%description -n python2-pyqt5-sip %_description

%if %{?wx_siplib}
%package -n python2-wx-siplib
Summary: %summary
Provides: python2-wx-siplib-api(%{_sip_api_major}) = %{_sip_api}
Provides: python2-wx-siplib-api(%{_sip_api_major})%{?_isa} = %{_sip_api}
%{?python_provide:%python_provide python2-wx-siplib}
%description -n python2-wx-siplib %_description
%endif
%endif

%if %{with python3}
%if 0%{?no_namespace}
%package -n python%{python3_pkgversion}-sip
Summary: SIP - Python 3/C++ Bindings Generator
Provides: python%{python3_pkgversion}-sip-api(%{_sip_api_major}) = %{_sip_api}
Provides: python%{python3_pkgversion}-sip-api(%{_sip_api_major})%{?_isa} = %{_sip_api}
%description -n python%{python3_pkgversion}-sip
This is the Python 3 build of SIP.

%_description
%endif

%package -n python%{python3_pkgversion}-sip-devel
Summary: Files needed to generate Python bindings for any C++ class library
Requires: sip = %{version}-%{release}
#Requires: python3-sip%{?_isa} = %{version}-%{release}
BuildRequires: python%{python3_pkgversion}-devel
Requires:      python%{python3_pkgversion}-devel
%description -n python%{python3_pkgversion}-sip-devel
%{summary}.

%package -n python%{python3_pkgversion}-pyqt4-sip
Summary: SIP - Python 3/C++ Bindings Generator for pyqt4
BuildRequires: python%{python3_pkgversion}-devel
Provides: python%{python3_pkgversion}-pyqt4-sip-api(%{_sip_api_major}) = %{_sip_api}
Provides: python%{python3_pkgversion}-pyqt4-sip-api(%{_sip_api_major})%{?_isa} = %{_sip_api}
%description -n python%{python3_pkgversion}-pyqt4-sip
This is the Python 3 build of pyqt4-SIP.

%if %{?pyqt5_sip}
%package -n python%{python3_pkgversion}-pyqt5-sip
Summary: SIP - Python 3/C++ Bindings Generator for pyqt5
BuildRequires: python%{python3_pkgversion}-devel
Provides: python%{python3_pkgversion}-pyqt5-sip-api(%{_sip_api_major}) = %{_sip_api}
Provides: python%{python3_pkgversion}-pyqt5-sip-api(%{_sip_api_major})%{?_isa} = %{_sip_api}
%description -n python%{python3_pkgversion}-pyqt5-sip
This is the Python 3 build of pyqt5-SIP.
%endif

%if %{?wx_siplib}
%package -n python%{python3_pkgversion}-wx-siplib
Summary: SIP - Python 3/C++ Bindings Generator for wx
BuildRequires: python%{python3_pkgversion}-devel
Provides: python%{python3_pkgversion}-wx-siplib-api(%{_sip_api_major}) = %{_sip_api}
Provides: python%{python3_pkgversion}-wx-siplib-api(%{_sip_api_major})%{?_isa} = %{_sip_api}
%description -n python%{python3_pkgversion}-wx-siplib
This is the Python 3 build of wx-siplib.
%endif

%_description

%endif

%if 0%{?os2_version}
%debug_package
%endif


%prep

%if !0%{?os2_version}
%setup -q -n %{name}-%{version}%{?snap:.%{snap}}

%patch50 -p1 -b .no_strip
%patch51 -p1 -b .no_rpath
%patch53 -p1 -b .no_sip_so
%patch54 -p1 -b .py_ssize_t_clean
%else
%scm_setup
%endif


%build
%if 0%{?os2_version}
export VENDOR="%{vendor}"
export VERSION="%{version}"
%global __global_ldflags -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp
%endif
flex --outfile=sipgen/lexer.c sipgen/metasrc/lexer.l
bison --yacc --defines=sipgen/parser.h --output=sipgen/parser.c sipgen/metasrc/parser.y
%if %{with python2}
%if 0%{?no_namespace}
%if !0%{?os2_version}
mkdir %{_target_platform}-python2
pushd %{_target_platform}-python2
%else
mkdir python2
cd python2
%endif
%{__python2} ../configure.py \
  -b %{_bindir} -d %{python2_sitearch} -e %{_includedir}/python%{python2_version} \
  CFLAGS+="%{optflags}" CXXFLAGS+="%{optflags}" LFLAGS+="%{?__global_ldflags}"

%if !0%{?os2_version}
%make_build
popd
%else
make %{?_smp_mflags}
cd ..
%endif
%endif

%if !0%{?os2_version}
mkdir %{_target_platform}-python2-pyqt4
pushd %{_target_platform}-python2-pyqt4
%else
mkdir python2-pyqt4
cd python2-pyqt4
%endif
%{__python2} ../configure.py \
  --sip-module=PyQt4.sip \
  -b %{_bindir} -d %{python2_sitearch} -e %{_includedir}/python%{python2_version} \
  CFLAGS+="%{optflags}" CXXFLAGS+="%{optflags}" LFLAGS+="%{?__global_ldflags}"

%if !0%{?os2_version}
%make_build
popd
%else
make %{?_smp_mflags}
cd ..
%endif

%if !0%{?os2_version}
mkdir %{_target_platform}-python2-pyqt5
pushd %{_target_platform}-python2-pyqt5
%else
mkdir python2-pyqt5
cd python2-pyqt5
%endif
%{__python2} ../configure.py \
  --sip-module=PyQt5.sip \
  -b %{_bindir} -d %{python2_sitearch} -e %{_includedir}/python%{python2_version} \
  CFLAGS+="%{optflags}" CXXFLAGS+="%{optflags}" LFLAGS+="%{?__global_ldflags}"

%if !0%{?os2_version}
%make_build
popd
%else
make %{?_smp_mflags}
cd ..
%endif

sed -i -e 's|target = sip|target = siplib|g' siplib/siplib.sbf
%if %{?wx_siplib}
%if !0%{?os2_version}
mkdir %{_target_platform}-python2-wx
pushd %{_target_platform}-python2-wx
%else
mkdir python2-wx
cd python2-wx
%endif
%{__python2} ../configure.py \
  --sip-module=wx.siplib \
  -b %{_bindir} -d %{python2_sitearch} -e %{_includedir}/python%{python2_version} \
  CFLAGS+="%{optflags}" CXXFLAGS+="%{optflags}" LFLAGS+="%{?__global_ldflags}"

%if !0%{?os2_version}
%make_build
popd
%else
make %{?_smp_mflags}
cd ..
%endif
%endif
%endif
sed -i -e 's|target = siplib|target = sip|g' siplib/siplib.sbf

%if %{with python3}
%if 0%{?no_namespace}
%if !0%{?os2_version}
mkdir %{_target_platform}-python3
pushd %{_target_platform}-python3
%else
mkdir python3
cd python3
%endif
%{__python3} ../configure.py \
  -b %{_bindir} -d %{python3_sitearch} -e %{PYINCLUDE} \
  CXXFLAGS+="%{optflags}" CFLAGS+="%{optflags}" LFLAGS+="%{?__global_ldflags}"

%if !0%{?os2_version}
%make_build
popd
%else
make %{?_smp_mflags}
cd ..
%endif
%endif

%if !0%{?os2_version}
mkdir %{_target_platform}-python3-pyqt4
pushd %{_target_platform}-python3-pyqt4
%else
mkdir python3-pyqt4
cd python3-pyqt4
%endif
%{__python3} ../configure.py \
  --sip-module=PyQt4.sip \
  -b %{_bindir} -d %{python3_sitearch} -e %{PYINCLUDE} \
  CXXFLAGS+="%{optflags}" CFLAGS+="%{optflags}" LFLAGS+="%{?__global_ldflags}"

%if !0%{?os2_version}
%make_build
popd
%else
make %{?_smp_mflags}
cd ..
%endif

%if %{?pyqt5_sip}
%if !0%{?os2_version}
mkdir %{_target_platform}-python3-pyqt5
pushd %{_target_platform}-python3-pyqt5
%else
mkdir python3-pyqt5
cd python3-pyqt5
%endif
%{__python3} ../configure.py \
  --sip-module=PyQt5.sip \
  -b %{_bindir} -d %{python3_sitearch} -e %{PYINCLUDE} \
  CXXFLAGS+="%{optflags}" CFLAGS+="%{optflags}" LFLAGS+="%{?__global_ldflags}"

%if !0%{?os2_version}
%make_build
popd
%else
make %{?_smp_mflags}
cd ..
%endif
%endif

%if %{?wx_siplib}
sed -i -e 's|target = sip|target = siplib|g' siplib/siplib.sbf
%if !0%{?os2_version}
mkdir %{_target_platform}-python3-wx
pushd %{_target_platform}-python3-wx
%else
mkdir python3-wx
cd python3-wx
%endif
%{__python3} ../configure.py \
  --sip-module=wx.siplib \
  -b %{_bindir} -d %{python3_sitearch} -e %{PYINCLUDE} \
  CXXFLAGS+="%{optflags}" CFLAGS+="%{optflags}" LFLAGS+="%{?__global_ldflags}"

%if !0%{?os2_version}
%make_build
popd
%else
make %{?_smp_mflags}
cd ..
%endif
sed -i -e 's|target = siplib|target = sip|g' siplib/siplib.sbf
%endif

%endif


%install
# Perform the Python 3 installation first, to avoid stomping over the Python 2
# /usr/bin/sip:
%if %{with python3}
%if 0%{?no_namespace}
%if !0%{?os2_version}
%make_install -C %{_target_platform}-python3
%else
%make_install -C python3
%endif
%endif
%if !0%{?os2_version}
%make_install -C %{_target_platform}-python3-pyqt4
%else
%make_install -C python3-pyqt4
%endif
%if %{?pyqt5_sip}
%if !0%{?os2_version}
%make_install -C %{_target_platform}-python3-pyqt5
%else
%make_install -C python3-pyqt5
%endif
%endif
%if %{?wx_siplib}
%if !0%{?os2_version}
%make_install -C %{_target_platform}-python3-wx
%else
%make_install -C python3-wx
%endif
mv %{buildroot}%{python3_sitearch}/wx/sip.pyi %{buildroot}%{python3_sitearch}/wx/siplib.pyi
%endif
ln -s sip %{buildroot}%{_bindir}/python3-sip

## toplevel __pycache__ creation is ... inconsistent
## rawhide makes one, f23 local builds do not, so let's *make* it consistent
mkdir -p %{buildroot}%{python3_sitearch}/__pycache__/exclude_rpm_hack
%endif

# Python 2 installation:
%if %{with python2}
%if 0%{?no_namespace}
%if !0%{?os2_version}
%make_install -C %{_target_platform}-python2
%else
%make_install -C python2
%endif
%endif
%if !0%{?os2_version}
%make_install -C %{_target_platform}-python2-pyqt4
%make_install -C %{_target_platform}-python2-pyqt5
%else
%make_install -C python2-pyqt4
%make_install -C python2-pyqt5
%endif
%if %{?wx_siplib}
%if !0%{?os2_version}
%make_install -C %{_target_platform}-python2-wx
%else
%make_install -C python2-wx
%endif
mv %{buildroot}%{python2_sitearch}/wx/sip.pyi %{buildroot}%{python2_sitearch}/wx/siplib.pyi
%endif
%endif

# sip-wrapper
install %{SOURCE10} %{buildroot}%{_bindir}/sip-pyqt4
install %{SOURCE10} %{buildroot}%{_bindir}/sip-pyqt5
%if %{?wx_siplib}
install %{SOURCE10} %{buildroot}%{_bindir}/sip-wx
%endif
sed -i -e 's|@SIP_MODULE@|PyQt4.sip|g' %{buildroot}%{_bindir}/sip-pyqt4
sed -i -e 's|@SIP_MODULE@|PyQt5.sip|g' %{buildroot}%{_bindir}/sip-pyqt5
%if %{?wx_siplib}
sed -i -e 's|@SIP_MODULE@|wx.siplib|g' %{buildroot}%{_bindir}/sip-wx
%endif

mkdir -p %{buildroot}%{_datadir}/sip

# Macros used by -devel subpackages:
install -D -p -m644 %{SOURCE1} %{buildroot}%{rpm_macros_dir}/macros.sip

# Copy documentation from source dir
%if !0%{?os2_version}
pushd doc
%else
cd doc
%endif
find html/ -type f -exec install -m0644 -D {} %{buildroot}%{_pkgdocdir}/{} \;
%if !0%{?os2_version}
popd
%else
cd ..
%endif

%files
%doc README
%license LICENSE LICENSE-GPL2 LICENSE-GPL3
%if !0%{?os2_version}
%{_bindir}/sip
%else
%{_bindir}/sip.exe
%endif
# sip-wrappers
%{_bindir}/sip-pyqt4
%{_bindir}/sip-pyqt5
%if %{?wx_siplib}
%{_bindir}/sip-wx
%endif
# compat symlink
%{_bindir}/python3-sip
%dir %{_datadir}/sip/
%{rpm_macros_dir}/macros.sip

%files doc
%{_pkgdocdir}/html

%if %{with python2}
%files -n python2-sip-devel
%{_prefix}/include/python2.7/sip.h
%{python2_sitearch}/sipconfig.py*
%{python2_sitearch}/sipdistutils.py*

%if 0%{?no_namespace}
%files -n python2-sip
%doc NEWS README
%license LICENSE LICENSE-GPL2 LICENSE-GPL3
%{python2_sitearch}/sip.*
%{python2_sitearch}/sip-%{version}.dist-info/
%endif

%files -n python2-pyqt4-sip
%doc NEWS README
%license LICENSE LICENSE-GPL2 LICENSE-GPL3
%{python2_sitearch}/PyQt4/
%{python2_sitearch}/PyQt4_sip-%{version}.dist-info/

%files -n python2-pyqt5-sip
%doc NEWS README
%license LICENSE LICENSE-GPL2 LICENSE-GPL3
%dir %{python2_sitearch}/PyQt5/
%{python2_sitearch}/PyQt5/sip.*
%{python2_sitearch}/PyQt5_sip-%{version}.dist-info/

%if %{?wx_siplib}
%files -n python2-wx-siplib
%doc NEWS README
%license LICENSE LICENSE-GPL2 LICENSE-GPL3
%dir %{python2_sitearch}/wx/
%{python2_sitearch}/wx/siplib.*
%{python2_sitearch}/wx_siplib-%{version}.dist-info/
%endif
%endif

%if %{with python3}
%files -n python%{python3_pkgversion}-sip-devel
%{PYINCLUDE}/sip.h
%{python3_sitearch}/sipconfig.py*
%{python3_sitearch}/sipdistutils.py*
%{python3_sitearch}/__pycache__/*
%exclude %{python3_sitearch}/__pycache__/exclude_rpm_hack

%if 0%{?no_namespace}
%files -n python%{python3_pkgversion}-sip
%doc NEWS README
%license LICENSE LICENSE-GPL2 LICENSE-GPL3
%{python3_sitearch}/sip.*
%{python3_sitearch}/sip-%{version}.dist-info/
%endif

%files -n python%{python3_pkgversion}-pyqt4-sip
%doc NEWS README
%license LICENSE LICENSE-GPL2 LICENSE-GPL3
%dir %{python3_sitearch}/PyQt4/
%{python3_sitearch}/PyQt4/sip.*
%{python3_sitearch}/PyQt4_sip-%{version}.dist-info/

%if %{?pyqt5_sip}
%files -n python%{python3_pkgversion}-pyqt5-sip
%doc NEWS README
%license LICENSE LICENSE-GPL2 LICENSE-GPL3
%dir %{python3_sitearch}/PyQt5/
%{python3_sitearch}/PyQt5/sip.*
%{python3_sitearch}/PyQt5_sip-%{version}.dist-info/
%endif

%if %{?wx_siplib}
%files -n python%{python3_pkgversion}-wx-siplib
%doc NEWS README
%license LICENSE LICENSE-GPL2 LICENSE-GPL3
%dir %{python3_sitearch}/wx/
%{python3_sitearch}/wx/siplib.*
%{python3_sitearch}/wx_siplib-%{version}.dist-info/
%endif
%endif


%changelog
* Thu Jan 27 2022 Silvan Scherrer <silvan.scherrer@aroa.ch> - 4.19.25-1
- update to version 4.19.25
- resync with fedora spec

* Wed Jun 15 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 4.18.3-5
- fix signature handling 

* Tue Jun 14 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 4.18.3-4
- rebuilt because of python ucs2/ucs4 change

* Fri Jun 3 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 4.18-3
- truncate pyd files to max 8 char, if longer
- create a symlink, if the original pyd file is larger than 8 char
- add the possibility to have a nameshort tag in the %Module() section
- add a def file for pyd (header only)

* Fri May 20 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 4.18-2
- fix the Qt lib names (append the right version)
- enable GNUMAKE as make generator

* Thu May 19 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 4.18-1
- initial version
