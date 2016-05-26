#define svn_url     e:/trees/sip/trunk
%define svn_url     http://svn.netlabs.org/repos/ports/sip/trunk
%define svn_rev     1576

# switch this on when we have python3
#global with_python3 1

%if 0%{?with_python3}
%{!?python3_inc:%global python3_inc %(%{__python3} -c "from distutils.sysconfig import get_python_inc; print(get_python_inc(1))")}
%endif
%{!?__python2:%global __python2 /@unixroot/usr/bin/python2}
%{!?python2_sitearch:%global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%{!?python2_inc:%global python2_inc %(%{__python2} -c "from distutils.sysconfig import get_python_inc; print get_python_inc(1)")}

Summary: SIP - Python/C++ Bindings Generator
Name: sip
Version: 4.18
Release: 2%{?dist}

# sipgen/parser.{c.h} is GPLv3+ with exceptions (bison)
License: GPLv2 or GPLv3 and (GPLv3+ with exceptions)
Url: http://www.riverbankcomputing.com/software/sip/intro 
Vendor: bww bitwise works GmbH
Source: %{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip

# extracted from sip.h, SIP_API_MAJOR_NR SIP_API_MINOR_NR defines
%global _sip_api_major 11
%global _sip_api_minor 3
%global _sip_api %{_sip_api_major}.%{_sip_api_minor}

Provides: sip-api(%{_sip_api_major}) = %{_sip_api}

BuildRequires: python2-devel
BuildRequires: sed

%if 0%{?with_python3}
BuildRequires:  python3-devel
%endif

%description
SIP is a tool for generating bindings for C++ classes so that they can be
accessed as normal Python classes. SIP takes many of its ideas from SWIG but,
because it is specifically designed for C++ and Python, is able to generate
tighter bindings. SIP is so called because it is a small SWIG.

SIP was originally designed to generate Python bindings for KDE and so has
explicit support for the signal slot mechanism used by the Qt/KDE class
libraries. However, SIP can be used to generate Python bindings for any C++
class library.

%package devel
Summary: Files needed to generate Python bindings for any C++ class library
Requires: %{name} = %{version}-%{release}
Requires: %{name}-macros = %{version}-%{release}
Requires: python2-devel
%description devel
This package contains files needed to generate Python bindings for any C++
classes library.

%package macros
Summary: RPM macros for use when working with SIP
Requires: rpm
# when arch->noarch happened
Obsoletes: sip-macros < 4.15.5
BuildArch: noarch
%description macros
This package contains RPM macros for use when working with SIP.
%if 0%{?with_python3}
It is used by both the sip-devel (python 2) and python3-sip-devel subpackages.
%endif

%if 0%{?with_python3}
%package -n python3-sip
Summary: SIP - Python 3/C++ Bindings Generator
Provides: python3-sip-api(%{_sip_api_major}) = %{_sip_api}
%description -n python3-sip
This is the Python 3 build of SIP.

SIP is a tool for generating bindings for C++ classes so that they can be
accessed as normal Python 3 classes. SIP takes many of its ideas from SWIG but,
because it is specifically designed for C++ and Python, is able to generate
tighter bindings. SIP is so called because it is a small SWIG.

SIP was originally designed to generate Python bindings for KDE and so has
explicit support for the signal slot mechanism used by the Qt/KDE class
libraries. However, SIP can be used to generate Python 3 bindings for any C++
class library.

%package -n python3-sip-devel
Summary: Files needed to generate Python 3 bindings for any C++ class library
Requires: %{name}-macros = %{version}-%{release}
Requires: python3-sip = %{version}-%{release}
Requires: python3-devel
%description -n python3-sip-devel
This package contains files needed to generate Python 3 bindings for any C++
classes library.
%endif

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

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif


%build
LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} configure.py \
  -d %{python3_sitearch} \
  --sipdir=%{_datadir}/python3-sip \
  CXXFLAGS="%{optflags}" CFLAGS="%{optflags}" LFLAGS="$LDFLAGS"

make %{?_smp_mflags} 
popd
%endif

%{__python2} configure.py \
  -d %{python2_sitearch} \
  CFLAGS="%{optflags}" CXXFLAGS="%{optflags}" LFLAGS="$LDFLAGS"

make %{?_smp_mflags}


%install
# Perform the Python 3 installation first, to avoid stomping over the Python 2
# /usr/bin/sip:
%if 0%{?with_python3}
pushd %{py3dir}
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}%{_datadir}/python3-sip
mv %{buildroot}%{_bindir}/sip %{buildroot}%{_bindir}/python3-sip
popd

## toplevel __pycache__ creation is ... inconsistent
## rawhide makes one, f23 local builds do not, so let's *make* it consistent
mkdir -p %{buildroot}%{python3_sitearch}/__pycache__/exclude_rpm_hack
%endif

# Python 2 installation:
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}%{_datadir}/sip

# Macros used by -devel subpackages:
mkdir -p %{buildroot}/%{_rpmconfigdir}/macros.d
install -m 0644 %{_builddir}/%{buildsubdir}/macros.sip %{buildroot}%{_rpmconfigdir}/macros.d


%files
%doc NEWS README
%license LICENSE LICENSE-GPL2 LICENSE-GPL3
%{python2_sitearch}/sip*.py*

%files devel
%{_bindir}/sip.exe
%{_datadir}/sip/
%{python2_inc}/*

%files macros
%{_rpmconfigdir}/macros.d/macros.sip

%if 0%{?with_python3}
%files -n python3-sip
%doc NEWS README
%license LICENSE LICENSE-GPL2 LICENSE-GPL3
%{python3_sitearch}/sip.so
%{python3_sitearch}/sip*.py*
%{python3_sitearch}/__pycache__/*
%exclude %{python3_sitearch}/__pycache__/exclude_rpm_hack

%files -n python3-sip-devel
# Note that the "sip" binary is invoked by name in a few places higher up
# in the KDE-Python stack; these will need changing to "python3-sip":
%{_bindir}/python3-sip.exe
%{_datadir}/python3-sip/
%{python3_inc}/*
%endif


%changelog
* Fri May 20 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 4.18-2
- fix the Qt lib names (append the right version)
- enable GNUMAKE as make generator

* Thu May 19 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 4.18-1
- initial version
