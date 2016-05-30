#define svn_url     e:/trees/pyqt4/trunk
%define svn_url     http://svn.netlabs.org/repos/ports/pyqt4/trunk
%define svn_rev     1579

%define target os2
# remove the below 2 settings, as soon as we deliver qt macros
%define _qt4_plugindir %{_libdir}/qt4/plugins
%define _qt4_datadir %{_datadir}/qt4

# switch this on when we have python3
#global with_python3 1

#global qtassistant 1
%global webkit 1

%if 0%{?with_python3}
%{!?python3_inc:%global python3_inc %(%{__python3} -c "from distutils.sysconfig import get_python_inc; print(get_python_inc(1))")}
#global python3_dbus_dir %(%{__python3} -c "import dbus.mainloop; print(dbus.mainloop.__path__[0])")
%endif

%{!?__python2:%global __python2 /@unixroot/usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch:%global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%{!?python2_inc:%global python2_inc %(%{__python2} -c "from distutils.sysconfig import get_python_inc; print get_python_inc(1)")}
# we don't have dbus atm
#global python2_dbus_dir %(%{__python2} -c "import dbus.mainloop; print(dbus.mainloop.__path__[0])")

Summary: Python bindings for Qt4
Name: 	 PyQt4
Version: 4.11.4
Release: 1%{?dist}

# GPLv2 exceptions(see GPL_EXCEPTIONS*.txt)
License: (GPLv3 or GPLv2 with exceptions) and BSD
Url:     http://www.riverbankcomputing.com/software/pyqt/
Vendor: bww bitwise works GmbH
Source: %{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip

#BuildRequires: dbus-python
#BuildRequires: pkgconfig(dbus-1) pkgconfig(dbus-python)
#BuildRequires: pkgconfig(phonon)
#BuildRequires: pkgconfig(QtDBus)
BuildRequires: libqt4-devel >= 4.7.3
BuildRequires: python2-devel
BuildRequires: sip-devel >= 4.16.8

%if 0%{?with_python3}
BuildRequires: python3-dbus
BuildRequires: python3-devel 
BuildRequires: python3-sip-devel >= 4.16.8
%endif # with_python3

#Requires: dbus-python
Requires: qt4 >= 4.7.3
%{?_sip_api:Requires: sip-api(%{_sip_api_major}) >= %{_sip_api}}

Provides: python-qt4 = %{version}-%{release}
Provides: python2-qt4 = %{version}-%{release}
Provides: python2-PyQt4 = %{version}-%{release}
Provides: pyqt4 = %{version}-%{release}

%description
These are Python bindings for Qt4.

%package devel
Summary: Files needed to build other bindings based on Qt4
%if 0%{?webkit}
Obsoletes: %{name}-webkit-devel < %{version}-%{release}
Provides: %{name}-webkit-devel = %{version}-%{release}
Obsoletes: PyQt4 < %{version}-%{release}
Requires: %{name}-webkit = %{version}-%{release}
%endif
Provides: python-qt4-devel = %{version}-%{release}
Provides: python2-qt4-doc = %{version}-%{release}
Provides: python2-PyQt4-doc = %{version}-%{release}
Provides: pyqt4-devel = %{version}-%{release}
Requires: %{name} = %{version}-%{release}
Requires: qt4-devel
Requires: sip-devel

%description devel
Files needed to build other bindings for C++ classes that inherit from any
of the Qt4 classes (e.g. KDE or your own).

%package doc
Summary: PyQt4 developer documentation and examples
BuildArch: noarch
Provides: python-qt4-doc = %{version}-%{release}
Provides: python2-qt4-doc = %{version}-%{release}
Provides: python2-PyQt4-doc = %{version}-%{release}

%description doc
%{summary}.

# split-out arch'd subpkg, since (currently) %%_qt4_datadir = %%_qt4_libdir
%package qsci-api
Summary: Qscintilla API file support
# when split happened, upgrade path
Provides: python-qt4-qsci-api = %{version}-%{release}
Provides: python2-qt4-qsci-api = %{version}-%{release}
Provides: python2-PyQt4-qsci-api = %{version}-%{release}

%description qsci-api
%{summary}.

%if 0%{?qtassistant}
%package assistant
Summary: Python bindings for QtAssistant
BuildRequires: qt4-assistant >= 4.7.3
Provides: python-qt4-assistant = %{version}-%{release}
Provides: python2-qt4-assistant = %{version}-%{release}
Provides: python2-PyQt4-assistant = %{version}-%{release}
Requires: %{name} = %{version}-%{release}

%description assistant
%{summary}.

%if 0%{?with_python3}
%package -n python3-%{name}-assistant
Summary: Python 3 bindings for QtAssistant
Provides: python3-qt4-assistant = %{version}-%{release}
Requires: python3-%{name} = %{version}-%{release}

%description -n python3-%{name}-assistant
%{summary}.
%endif
%endif

%if 0%{?webkit}
%package webkit
Summary: Python bindings for Qt4 Webkit
BuildRequires: libqt4-webkit-devel >= 4.7.3
Provides: python-qt4-webkit = %{version}-%{release}
Provides: python2-qt4-webkit = %{version}-%{release}
Provides: python2-PyQt4-webkit = %{version}-%{release}
Provides: pyqt4-webkit = %{version}-%{release}
Requires: %{name} = %{version}-%{release}

%description webkit
%{summary}.

%if 0%{?with_python3}
%package -n python3-%{name}-webkit
Summary: Python3 bindings for Qt4 Webkit
Provides: python3-qt4-webkit = %{version}-%{release}
Requires:  python3-PyQt4 = %{version}-%{release}

%description -n python3-%{name}-webkit
%{summary}.
%endif
%endif

%if 0%{?with_python3}
# The bindings are imported as "PyQt4", hence it's reasonable to name the
# Python 3 subpackage "python3-PyQt4", despite the apparent tautology
%package -n python3-%{name}
Summary: Python 3 bindings for Qt4
Requires: python3-dbus
%{?_qt4_version:Requires: qt4 >= %{_qt4_version}}
%{?_sip_api:Requires: python3-sip-api(%{_sip_api_major}) >= %{_sip_api}}
Provides: python3-qt4 = %{version}-%{release}

%description -n python3-%{name}
These are Python 3 bindings for Qt4.

%package -n python3-%{name}-devel
Summary: Python 3 bindings for Qt4
%if 0%{?webkit}
Provides: python3-%{name}-webkit-devel = %{version}-%{release}
Requires: python3-%{name}-webkit = %{version}-%{release}
%endif
Provides: python3-qt4-devel = %{version}-%{release}
Requires: python3-%{name} = %{version}-%{release}
Requires: python3-sip-devel

%description -n python3-%{name}-devel
Files needed to build other Python 3 bindings for C++ classes that inherit
from any of the Qt4 classes (e.g. KDE or your own).
%endif

# no debug package at the moment, as all is already built with -s
#debug_package


%prep
%if %{?svn_rev:%(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')}%{!?svn_rev):0}
%setup -q
%else
%setup -n "%{name}-%{version}" -Tc
svn export %{?svn_rev:-r %{svn_rev}} %{svn_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip" "%{name}-%{version}")
%endif

# save orig for comparison later
cp -a ./sip/QtGui/opengl_types.sip ./sip/QtGui/opengl_types.sip.orig

# permissions, mark examples non-executable
find examples/ -name "*.py" | xargs chmod a-x


%build
# !!!!!!!! remove the below instructions, when switched to shell based qmake
# 
# configure needs qmake_sh, as else install will never work
# adjust qmake.conf to the following
# first before the first isEmpty(QMAKE_SH) you need to add QMAKE_SH=$$(QMAKE_SH)
# second you need to flip all !isEmpty(QMAKE_SH) as else sip will not work ok
# third you need to exchange the current QMAKE_RUN_GENDEF with the below block
#isEmpty(QMAKE_SH) {
#QMAKE_RUN_GENDEF            = \
#    $(QMAKESPECDIR)\\emxexpw.cmd -name $(basename $(TARGET)) \
#        -def $(DEF_FILE) \
#        $(if $(DEF_FILE_VERSION),-version \"$(DEF_FILE_VERSION)\") \
#        $(if $(DEF_FILE_DESCRIPTION),-desc \"$(DEF_FILE_DESCRIPTION)\") \
#        $(if $(DEF_FILE_VENDOR),-vendor \"$(DEF_FILE_VENDOR)\") \
#        $(if $(DEF_FILE_TEMPLATE),-template \"$(DEF_FILE_TEMPLATE)\")
#} else {
#QMAKE_RUN_GENDEF            = \
#    $(QMAKESPECDIR)/emxexpw.cmd -name $(basename $(TARGET)) \
#        -def $(DEF_FILE) \
#        $(if $(DEF_FILE_VERSION),-version \"$(DEF_FILE_VERSION)\") \
#        $(if $(DEF_FILE_DESCRIPTION),-desc \"$(DEF_FILE_DESCRIPTION)\") \
#        $(if $(DEF_FILE_VENDOR),-vendor \"$(DEF_FILE_VENDOR)\") \
#        $(if $(DEF_FILE_TEMPLATE),-template \"$(DEF_FILE_TEMPLATE)\")
#}

export QMAKE_SH=$SHELL
# do a fast qt build, as runmapsym and wmapsym is not needed here
export FAST_BUILD=1
LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"

# Python 2 build:
mkdir -p %{target}
cd %{target}
%{__python2} ../configure.py \
  --assume-shared \
  --confirm-license \
  --no-timestamp \
  --qsci-api --qsci-api-destdir=%{_qt4_datadir}/qsci \
  --verbose \
  CFLAGS="%{optflags}" CXXFLAGS="%{optflags}" LFLAGS="$LDFLAGS"

make %{?_smp_mflags}
cd ..

# Python 3 build:
%if 0%{?with_python3}
mkdir %{target}-python3
pushd %{target}-python3
%{__python3} ../configure.py \
  --assume-shared \
  --confirm-license \
  --no-timestamp \
  --qmake=%{_qt4_qmake} \
  --no-qsci-api \
  --sipdir=%{_datadir}/python3-sip/PyQt4 \
  --verbose \
  CFLAGS="%{optflags}" CXXFLAGS="%{optflags}" LFLAGS="%{?__global_ldflags}"

make %{?_smp_mflags}
popd
%endif # with_python3


%install

# Install Python 3 first, and move aside any executables, to avoid clobbering
# the Python 2 installation:
%if 0%{?with_python3}
make install DESTDIR=%{buildroot} INSTALL_ROOT=%{buildroot} -C %{target}-python3
%endif # with_python3

make install DESTDIR=%{buildroot} INSTALL_ROOT=%{buildroot} -C %{target}

# remove Python 3 code from Python 2.6 directory, fixes FTBFS (#564633)
rm -rfv %{buildroot}%{python2_sitearch}/PyQt4/uic/port_v3/

# likewise, remove Python 2 code from the Python 3.1 directory:
rm -rfv %{buildroot}%{python3_sitearch}/PyQt4/uic/port_v2/

# copy designer plugin by hand, as install target isn't working atm
mkdir -p %{buildroot}%{_qt4_plugindir}/designer
cp %{target}/designer/pyqt4.dll %{buildroot}%{_qt4_plugindir}/designer

%check
# verify opengl_types.sip sanity
diff -u ./sip/QtGui/opengl_types.sip.orig \
        ./sip/QtGui/opengl_types.sip ||:


%files
%doc NEWS README
%doc LICENSE
#{python2_dbus_dir}/qt.dll
%dir %{python2_sitearch}/PyQt4/
%{python2_sitearch}/PyQt4/__init__.py*
%{python2_sitearch}/PyQt4/pyqtconfig.py*
#{python2_sitearch}/PyQt4/phonon.pyd
%{python2_sitearch}/PyQt4/Qt.pyd
%{python2_sitearch}/PyQt4/QtCore.pyd
#{python2_sitearch}/PyQt4/QtDBus.pyd
%{python2_sitearch}/PyQt4/QtDecl.pyd
%{python2_sitearch}/PyQt4/QtDsgn.pyd
%{python2_sitearch}/PyQt4/QtGui.pyd
%{python2_sitearch}/PyQt4/QtHelp.pyd
#%{python2_sitearch}/PyQt4/QtMultimedia.pyd
%{python2_sitearch}/PyQt4/QtNet.pyd
#%{python2_sitearch}/PyQt4/QtOpenGL.pyd
%{python2_sitearch}/PyQt4/QtScri.pyd
%{python2_sitearch}/PyQt4/QtScTl.pyd
%{python2_sitearch}/PyQt4/QtSql.pyd
%{python2_sitearch}/PyQt4/QtSvg.pyd
%{python2_sitearch}/PyQt4/QtTest.pyd
%{python2_sitearch}/PyQt4/QtXml.pyd
%{python2_sitearch}/PyQt4/QtXmlP.pyd
%{python2_sitearch}/PyQt4/uic/
%{_qt4_plugindir}/designer/*

%if 0%{?qtassistant}
%files assistant
%{python2_sitearch}/PyQt4/QtAssistant.pyd
%endif

%if 0%{?webkit}
%files webkit
%{python2_sitearch}/PyQt4/QtWebK.pyd
%endif

%files devel
%{_bindir}/pylupdate4.exe
%{_bindir}/pyrcc4.exe
%{_bindir}/pyuic4
%{_datadir}/sip/PyQt4/

%files doc
%doc doc/*
%doc examples/

%files qsci-api
# avoid dep on qscintilla-python, own %%_qt4_datadir/qsci/... here for now
%dir %{_qt4_datadir}/qsci/
%dir %{_qt4_datadir}/qsci/api/
%dir %{_qt4_datadir}/qsci/api/python/
%{_qt4_datadir}/qsci/api/python/PyQt4.api

%if 0%{?with_python3}
%files -n python3-%{name}
%doc NEWS README
%doc LICENSE
%{python3_dbus_dir}/qt.so
%dir %{python3_sitearch}/PyQt4/
%{python3_sitearch}/PyQt4/__init__.py*
%{python3_sitearch}/PyQt4/__pycache__/
%{python3_sitearch}/PyQt4/pyqtconfig.py*
%{python3_sitearch}/PyQt4/phonon.pyd
%{python3_sitearch}/PyQt4/Qt.pyd
%{python3_sitearch}/PyQt4/QtCore.pyd
%{python3_sitearch}/PyQt4/QtDBus.pyd
%{python3_sitearch}/PyQt4/QtDecl.pyd
%{python3_sitearch}/PyQt4/QtDsgn.pyd
%{python3_sitearch}/PyQt4/QtGui.pyd
%{python3_sitearch}/PyQt4/QtHelp.pyd
%{python3_sitearch}/PyQt4/QtMultimedia.pyd
%{python3_sitearch}/PyQt4/QtNet.pyd
%{python3_sitearch}/PyQt4/QtOpenGL.pyd
%{python3_sitearch}/PyQt4/QtScri.pyd
%{python3_sitearch}/PyQt4/QtScTl.pyd
%{python3_sitearch}/PyQt4/QtSql.pyd
%{python3_sitearch}/PyQt4/QtSvg.pyd
%{python3_sitearch}/PyQt4/QtTest.pyd
%{python3_sitearch}/PyQt4/QtXml.pyd
%{python3_sitearch}/PyQt4/QtXmlP.pyd
%{python3_sitearch}/PyQt4/uic/

%if 0%{?qtassistant}
%files -n python3-%{name}-assistant
%{python3_sitearch}/PyQt4/QtAssistant.pyd
%endif

%if 0%{?webkit}
%files -n python3-%{name}-webkit
%{python3_sitearch}/PyQt4/QtWebKit.pyd
%endif

%files -n python3-%{name}-devel
%{_bindir}/pylupdate4.exe
%{_bindir}/pyrcc4.exe
%{_bindir}/pyuic4
%{_datadir}/python3-sip/PyQt4/
%endif


%changelog
* Thu May 26 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 4.11.4-1
- initial version
