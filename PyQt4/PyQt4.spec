%if 0%{?os2_version}
%define _qt4_plugindir %{_libdir}/qt4/plugins
%define _qt4_datadir %{_datadir}/qt4
%endif

%if 0%{?fedora} || 0%{?rhel} > 7 || 0%{?os2_version}
%global with_python3 1
%global webkit 1
%endif

%if 0%{?fedora} < 32 && 0%{?rhel} < 8 || 0%{?os2_version}
%global with_python2 1
%endif

%if 0%{?fedora} && 0%{?fedora} < 30
%global qtassistant 1
%endif

%if 0%{?with_python3}
%{!?python3_inc:%global python3_inc %(%{__python3} -c "from distutils.sysconfig import get_python_inc; print(get_python_inc(1))")}
%if !0%{?os2_version}
%global python3_dbus_dir %(%{__python3} -c "import dbus.mainloop; print(dbus.mainloop.__path__[0])")
%endif
%endif

%if 0%{?with_python2}
%if !0%{?os2_version}
%{!?__python2:%global __python2 /usr/bin/python2}
%else
%{!?__python2:%global __python2 /@unixroot/usr/bin/python2}
%endif
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch:%global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%{!?python2_inc:%global python2_inc %(%{__python2} -c "from distutils.sysconfig import get_python_inc; print get_python_inc(1)")}
%if !0%{?os2_version}
%global python2_dbus_dir %(%{__python2} -c "import dbus.mainloop; print(dbus.mainloop.__path__[0])")
%if 0%{?fedora} > 27
%global python2_dbus python2-dbus
%else
%global python2_dbus dbus-python
%endif
%endif
%endif

## f29+ no longer using separate sipdir for python3
%global py3_sipdir %{_datadir}/sip/PyQt4
%dnl %if 0%{?fedora} < 29
%dnl %global py3_sipdir %{_datadir}/python3-sip/PyQt4
%dnl %endif

Summary: Python bindings for Qt4
Name: 	 PyQt4
Version: 4.12.3
Release: 2%{?dist}

# GPLv2 exceptions(see GPL_EXCEPTIONS*.txt)
License: (GPLv3 or GPLv2 with exceptions) and BSD
Url:     http://www.riverbankcomputing.com/software/pyqt/
%if !0%{?os2_version}
%if 0%{?snap:1}
Source0:  http://www.riverbankcomputing.com/static/Downloads/PyQt4/PyQt-x11-gpl-%{version}%{?snap:-snapshot-%{snap}}.tar.gz
%else
Source0:  http://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-%{version}/PyQt4_gpl_x11-%{version}.tar.gz
%endif
%else
Vendor: bww bitwise works GmbH
%scm_source github http://github.com/bitwiseworks/%{name}-os2 v%{version}-os2-1
%endif

Source2: pyuic4.sh

## upstreamable patches

## upstream patches
%if !0%{?os2_version}
# fix FTBFS on ARM
Patch60:  qreal_float_support.diff

# Fix Python 3.10 support (rhbz#1895298)
Patch61:  python310-pyobj_ascharbuf.patch

# rhel patches
Patch300: PyQt-x11-gpl-4.11-webkit.patch
%endif

BuildRequires: make
%if !0%{?os2_version}
BuildRequires: chrpath
%endif
BuildRequires: findutils
BuildRequires: gcc-c++
%if !0%{?os2_version}
BuildRequires: pkgconfig(dbus-1)
BuildRequires: pkgconfig(dbus-python)
BuildRequires: pkgconfig(phonon)
BuildRequires: pkgconfig(QtDBus) pkgconfig(QtDeclarative) pkgconfig(QtDesigner)
BuildRequires: pkgconfig(QtGui) pkgconfig(QtHelp) pkgconfig(QtMultimedia)
BuildRequires: pkgconfig(QtNetwork) pkgconfig(QtOpenGL)
BuildRequires: pkgconfig(QtScript) pkgconfig(QtScriptTools)
BuildRequires: pkgconfig(QtSql) pkgconfig(QtSvg) pkgconfig(QtTest)
BuildRequires: pkgconfig(QtXml) pkgconfig(QtXmlPatterns)
%else
BuildRequires: libqt4-devel >= 4.7.3
%endif
%global sip_ver 4.19.25

%if 0%{?with_python3}
%if !0%{?os2_version}
BuildRequires: python3-dbus
%endif
BuildRequires: python3-devel 
BuildRequires: python3-pyqt4-sip >= %{sip_ver}
BuildRequires: python3-sip-devel >= %{sip_ver}
%endif # with_python3

%if 0%{?with_python2}
%if !0%{?os2_version}
BuildRequires: %{python2_dbus}
%endif
BuildRequires: python2-devel
BuildRequires: python2-pyqt4-sip >= %{sip_ver}
BuildRequires: python2-sip-devel >= %{sip_ver}

%if !0%{?os2_version}
Requires: %{python2_dbus}
%{?_qt4_version:Requires: qt4%{?_isa} >= %{_qt4_version}}
%else
Requires: libqt4 >= 4.7.3
%endif
%{?_sip_api:Requires: python2-pyqt4-sip-api(%{_sip_api_major}) >= %{_sip_api}}

%if !0%{?qtassistant}
Obsoletes: PyQt4-assistant < %{version}-%{release}
Obsoletes: python3-PyQt4-assistant < %{version}-%{release}
%endif

%if 0%{?webkit}
# when -webkit was split out
Obsoletes: PyQt4 < 4.11.4-8
%endif

Provides: python-qt4 = %{version}-%{release}
Provides: python2-qt4 = %{version}-%{release}
Provides: python2-PyQt4 = %{version}-%{release}
Provides: pyqt4 = %{version}-%{release}
Provides: python%{python2_version}dist(pyqt4) = %{version}
%endif

%global __provides_exclude_from ^(%{?python2_sitearch:%{python2_sitearch}/.*\\.so|}%{?python3_sitearch:%{python3_sitearch}/.*\\.so|}%{_qt4_plugindir}/.*\\.so)$

%description
These are Python bindings for Qt4.

%package devel
Summary: Files needed to build other bindings based on Qt4
%if 0%{?webkit}
Obsoletes: %{name}-webkit-devel < %{version}-%{release}
Provides: %{name}-webkit-devel = %{version}-%{release}
Obsoletes: PyQt4 < 4.11.4-8
%endif
Provides: python-qt4-devel = %{version}-%{release}
Provides: python2-qt4-doc = %{version}-%{release}
Provides: python2-PyQt4-doc = %{version}-%{release}
Provides: pyqt4-devel = %{version}-%{release}
Requires: %{name} = %{version}-%{release}
%if !0%{?os2_version}
Requires: qt4-devel
%else
Requires: libqt4-devel
%endif
Requires: sip-devel
# when split happened, upgrade path
Obsoletes: PyQt4-devel < 4.10.3-6
%description devel
Files needed to build other bindings for C++ classes that inherit from any
of the Qt4 classes (e.g. KDE or your own).

%package doc
Summary: PyQt4 developer documentation and examples
BuildArch: noarch
# when split happened, upgrade path
Obsoletes: PyQt4-devel < 4.10.3-6
Obsoletes: python3-PyQt4-devel < 4.10.3-6
Provides: python-qt4-doc = %{version}-%{release}
Provides: python2-qt4-doc = %{version}-%{release}
Provides: python2-PyQt4-doc = %{version}-%{release}
%description doc
%{summary}.

# split-out arch'd subpkg, since (currently) %%_qt4_datadir = %%_qt4_libdir
%package qsci-api
Summary: Qscintilla API file support
# when split happened, upgrade path
Obsoletes: PyQt4-devel < 4.10.3-6
Obsoletes: python3-PyQt4-devel < 4.10.3-6
Provides: python-qt4-qsci-api = %{version}-%{release}
Provides: python2-qt4-qsci-api = %{version}-%{release}
Provides: python2-PyQt4-qsci-api = %{version}-%{release}
%description qsci-api
%{summary}.

%if 0%{?qtassistant}
%package assistant
Summary: Python bindings for QtAssistant
%if !0%{?os2_version}
BuildRequires: pkgconfig(QtAssistantClient)
%else
BuildRequires: qt4-assistant >= 4.7.3
%endif
Provides: python-qt4-assistant = %{version}-%{release}
Provides: python2-qt4-assistant = %{version}-%{release}
Provides: python2-PyQt4-assistant = %{version}-%{release}
Requires: %{name} = %{version}-%{release}
%description assistant
%{summary}.

%package -n python3-%{name}-assistant
Summary: Python 3 bindings for QtAssistant
Provides: python3-qt4-assistant = %{version}-%{release}
Requires: python3-%{name} = %{version}-%{release}
%description -n python3-%{name}-assistant
%{summary}.
%endif

%if 0%{?webkit}
%package webkit
Summary: Python bindings for Qt4 Webkit
%if !0%{?os2_version}
BuildRequires: pkgconfig(QtWebKit)
%else
BuildRequires: libqt4-webkit-devel >= 4.7.3
%endif
# when -webkit was split out
Obsoletes: PyQt4 < 4.11.4-8
Provides: python-qt4-webkit = %{version}-%{release}
Provides: python2-qt4-webkit = %{version}-%{release}
Provides: python2-PyQt4-webkit = %{version}-%{release}
Provides: pyqt4-webkit = %{version}-%{release}
Requires: %{name} = %{version}-%{release}
%description webkit
%{summary}.

%package -n python3-%{name}-webkit
Summary: Python3 bindings for Qt4 Webkit
Obsoletes: python3-PyQt4 < 4.11.4-8
Provides: python3-qt4-webkit = %{version}-%{release}
Requires:  python3-PyQt4 = %{version}-%{release}
%description -n python3-%{name}-webkit
%{summary}.
%endif

# The bindings are imported as "PyQt4", hence it's reasonable to name the
# Python 3 subpackage "python3-PyQt4", despite the apparent tautology
%package -n python3-%{name}
Summary: Python 3 bindings for Qt4
%if !0%{?os2_version}
Requires: python3-dbus
%endif
%if !0%{?os2_version}
%{?_qt4_version:Requires: qt4%{?_isa} >= %{_qt4_version}}
%else
%{?_qt4_version:Requires: libqt4 >= %{_qt4_version}}
%endif
%{?_sip_api:Requires: python3-pyqt4-sip-api(%{_sip_api_major}) >= %{_sip_api}}
%if 0%{?webkit}
Obsoletes: python3-PyQt4 < 4.11.4-8
%endif
Provides: python3-qt4 = %{version}-%{release}
Provides: python%{python3_version}dist(pyqt4) = %{version}
%description -n python3-%{name}
These are Python 3 bindings for Qt4.

%package -n python3-%{name}-devel
Summary: Python 3 bindings for Qt4
%if 0%{?webkit}
Provides: python3-%{name}-webkit-devel = %{version}-%{release}
%endif
Provides: python3-qt4-devel = %{version}-%{release}
Requires: python3-%{name} = %{version}-%{release}
Requires: python3-sip-devel
# when split happened, upgrade path
Obsoletes: python3-PyQt4-devel < 4.10.3-6
%description -n python3-%{name}-devel
Files needed to build other Python 3 bindings for C++ classes that inherit
from any of the Qt4 classes (e.g. KDE or your own).


%prep
%if !0%{?os2_version}
%setup -q -n PyQt4_gpl_x11-%{version}%{?snap:-snapshot-%{snap}}
%else
%scm_setup
%endif

# save orig for comparison later
cp -a ./sip/QtGui/opengl_types.sip ./sip/QtGui/opengl_types.sip.orig
%if !0%{?os2_version}
%patch60 -p1 -b .arm
%patch61 -p1
%if ! 0%{?webkit}
%patch300 -p1 -b .webkit
%endif
%endif

# permissions, mark examples non-executable
find examples/ -name "*.py" | xargs chmod a-x


%build

%if !0%{?os2_version}
QT4DIR=%{_qt4_prefix}
PATH=%{_qt4_bindir}:$PATH ; export PATH
%else
# !!! permanent restriction of qt4 !!!
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
# fourth you need to garde QMAKE_MOC with isEmpty(QMAKE_SH) and add the below block
#} else {
#QMAKE_MOC       = $$[QT_INSTALL_BINS]/moc.exe
#QMAKE_UIC       = $$[QT_INSTALL_BINS]/uic.exe
#QMAKE_IDC       = $$[QT_INSTALL_BINS]/idc.exe
#}

export QMAKE_SH=$SHELL
# do a fast qt build, as runmapsym and wmapsym is not needed here
export FAST_BUILD=1
export VENDOR="%{vendor}"
export VERSION="%{version}"
%global __global_ldflags -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp
%endif

%if 0%{?with_python2}
# Python 2 build:
%if !0%{?os2_version}
mkdir %{_target_platform}
pushd %{_target_platform}
%else
mkdir -p os2
cd os2
%endif
%{__python2} ../configure.py \
  --assume-shared \
  --confirm-license \
  --no-timestamp \
%if !0%{?os2_version}
  --qmake=%{_qt4_qmake} \
%endif
  --qsci-api-destdir=%{_qt4_datadir}/qsci \
  --verbose \
  CFLAGS="%{optflags}" CXXFLAGS="%{optflags}" LFLAGS="%{?__global_ldflags}"

%if 0%{?os2_version}
# fix our qt4 make issue
sed -i -e "s|mkdir -p|\|\| mkdir -p|g" designer/Makefile
%endif
%make_build
%if !0%{?os2_version}
popd
%else
cd ..
%endif
%endif

# Python 3 build:
%if 0%{?with_python3}

%if !0%{?os2_version}
mkdir %{_target_platform}-python3
pushd %{_target_platform}-python3
%else
mkdir os2-python3
cd os2-python3
%endif
%{__python3} ../configure.py \
  --assume-shared \
  --confirm-license \
  --no-timestamp \
%if !0%{?os2_version}
  --qmake=%{_qt4_qmake} \
%endif
  --qsci-api-destdir=%{_qt4_datadir}/qsci \
  %{?py3_sipdir:--sipdir=%{py3_sipdir}} \
  --verbose \
  CFLAGS="%{optflags}" CXXFLAGS="%{optflags}" LFLAGS="%{?__global_ldflags}"

%if 0%{?os2_version}
# fix our qt4 make issue
sed -i -e "s|mkdir -p|\|\| mkdir -p|g" designer/Makefile
%endif
%make_build
%if !0%{?os2_version}
popd
%else
cd ..
%endif
%endif # with_python3


%install
# Install Python 3 first, and move aside any executables, to avoid clobbering
# the Python 2 installation:
%if 0%{?with_python3}
%if !0%{?os2_version}
make install DESTDIR=%{buildroot} INSTALL_ROOT=%{buildroot} -C %{_target_platform}-python3
%else
make install DESTDIR=%{buildroot} INSTALL_ROOT=%{buildroot} -C os2-python3
%endif
%if "%py3_sipdir" == "%{_datadir}/sip/PyQt4"
# copy files to old location for compat purposes temporarily
mkdir -p %{buildroot}%{_datadir}/python3-sip
%if !0%{?os2_version}
cp -alf %{buildroot}%{py3_sipdir} \
        %{buildroot}%{_datadir}/python3-sip/PyQt4
%else
cp -af %{buildroot}%{py3_sipdir} \
        %{buildroot}%{_datadir}/python3-sip/PyQt4
rm -fv %{buildroot}/pyqt4.lib
%endif
%endif
mkdir %{buildroot}%{python3_sitearch}/PyQt4/__pycache__/ ||:
%endif

%if 0%{?with_python2}
%if !0%{?os2_version}
make install DESTDIR=%{buildroot} INSTALL_ROOT=%{buildroot} -C %{_target_platform}
%else
make install DESTDIR=%{buildroot} INSTALL_ROOT=%{buildroot} -C os2
rm -fv %{buildroot}/pyqt4.lib
%endif
%endif

# remove Python 3 code from Python 2.6 directory, fixes FTBFS (#564633)
rm -rfv %{buildroot}%{python2_sitearch}/PyQt4/uic/port_v3/

# likewise, remove Python 2 code from the Python 3.1 directory:
rm -rfv %{buildroot}%{python3_sitearch}/PyQt4/uic/port_v2/

# install pyuic4 wrapper to support both python2/python3
rm -fv %{buildroot}%{_bindir}/pyuic4
install -p -m755 -D %{SOURCE2} \
  %{buildroot}%{_bindir}/pyuic4
sed -i \
  -e "s|@PYTHON3@|%{__python3}|g" \
  -e "s|@PYTHON2@|%{__python2}|g" \
  %{buildroot}%{_bindir}/pyuic4


%check
# verify opengl_types.sip sanity
diff -u ./sip/QtGui/opengl_types.sip.orig \
        ./sip/QtGui/opengl_types.sip ||:


%if 0%{?with_python2}
%files
%doc NEWS README
%license LICENSE
%if !0%{?os2_version}
%{python2_dbus_dir}/qt.so
%endif
%dir %{python2_sitearch}/PyQt4/
%{python2_sitearch}/PyQt4/__init__.py*
%{python2_sitearch}/PyQt4/pyqtconfig.py*
%if !0%{?os2_version}
%{python2_sitearch}/PyQt4/phonon.so
%{python2_sitearch}/PyQt4/Qt.so
%{python2_sitearch}/PyQt4/QtCore.so
%{python2_sitearch}/PyQt4/QtDBus.so
%{python2_sitearch}/PyQt4/QtDeclarative.so
%{python2_sitearch}/PyQt4/QtDesigner.so
%{python2_sitearch}/PyQt4/QtGui.so
%{python2_sitearch}/PyQt4/QtHelp.so
%{python2_sitearch}/PyQt4/QtMultimedia.so
%{python2_sitearch}/PyQt4/QtNetwork.so
%{python2_sitearch}/PyQt4/QtOpenGL.so
%{python2_sitearch}/PyQt4/QtScript.so
%{python2_sitearch}/PyQt4/QtScriptTools.so
%{python2_sitearch}/PyQt4/QtSql.so
%{python2_sitearch}/PyQt4/QtSvg.so
%{python2_sitearch}/PyQt4/QtTest.so
%{python2_sitearch}/PyQt4/QtXml.so
%{python2_sitearch}/PyQt4/QtXmlPatterns.so
%else
%{python2_sitearch}/PyQt4/Qt.pyd
%{python2_sitearch}/PyQt4/QtCore.pyd
%{python2_sitearch}/PyQt4/QtDecl.pyd
%{python2_sitearch}/PyQt4/QtDeclarative.pyd
%{python2_sitearch}/PyQt4/QtDsgn.pyd
%{python2_sitearch}/PyQt4/QtDesigner.pyd
%{python2_sitearch}/PyQt4/QtGui.pyd
%{python2_sitearch}/PyQt4/QtHelp.pyd
%{python2_sitearch}/PyQt4/QtNet.pyd
%{python2_sitearch}/PyQt4/QtNetwork.pyd
%{python2_sitearch}/PyQt4/QtScri.pyd
%{python2_sitearch}/PyQt4/QtScript.pyd
%{python2_sitearch}/PyQt4/QtScTl.pyd
%{python2_sitearch}/PyQt4/QtScriptTools.pyd
%{python2_sitearch}/PyQt4/QtSql.pyd
%{python2_sitearch}/PyQt4/QtSvg.pyd
%{python2_sitearch}/PyQt4/QtTest.pyd
%{python2_sitearch}/PyQt4/QtXml.pyd
%{python2_sitearch}/PyQt4/QtXmlP.pyd
%{python2_sitearch}/PyQt4/QtXmlPatterns.pyd
%endif
%{python2_sitearch}/PyQt4/uic/
%{_qt4_plugindir}/designer/*

%if 0%{?qtassistant}
%files assistant
%if !0%{?os2_version}
%{python2_sitearch}/PyQt4/QtAssistant.so
%else
%{python2_sitearch}/PyQt4/QtAsst.pyd
%{python2_sitearch}/PyQt4/QtAssistant.pyd
%endif
%endif

%if 0%{?webkit}
%files webkit
%if !0%{?os2_version}
%{python2_sitearch}/PyQt4/QtWebKit.so
%else
%{python2_sitearch}/PyQt4/QtWebK.pyd
%{python2_sitearch}/PyQt4/QtWebKit.pyd
%endif
%endif

%files devel
%if !0%{?os2_version}
%{_bindir}/pylupdate4
%{_bindir}/pyrcc4
%{_bindir}/pyuic4
%else
%{_bindir}/pylupdate4.exe
%{_bindir}/pyrcc4.exe
%{_bindir}/pyuic4
%endif
%{_datadir}/sip/PyQt4/
%endif

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
%license LICENSE
%if !0%{?os2_version}
%{python3_dbus_dir}/qt.so
%endif
%dir %{python3_sitearch}/PyQt4/
%{python3_sitearch}/PyQt4/__init__.py*
%{python3_sitearch}/PyQt4/__pycache__/
%{python3_sitearch}/PyQt4/pyqtconfig.py*
%if !0%{?os2_version}
%{python3_sitearch}/PyQt4/phonon.so
%{python3_sitearch}/PyQt4/Qt.so
%{python3_sitearch}/PyQt4/QtCore.so
%{python3_sitearch}/PyQt4/QtDBus.so
%{python3_sitearch}/PyQt4/QtDeclarative.so
%{python3_sitearch}/PyQt4/QtDesigner.so
%{python3_sitearch}/PyQt4/QtGui.so
%{python3_sitearch}/PyQt4/QtHelp.so
%{python3_sitearch}/PyQt4/QtMultimedia.so
%{python3_sitearch}/PyQt4/QtNetwork.so
%{python3_sitearch}/PyQt4/QtOpenGL.so
%{python3_sitearch}/PyQt4/QtScript.so
%{python3_sitearch}/PyQt4/QtScriptTools.so
%{python3_sitearch}/PyQt4/QtSql.so
%{python3_sitearch}/PyQt4/QtSvg.so
%{python3_sitearch}/PyQt4/QtTest.so
%{python3_sitearch}/PyQt4/QtXml.so
%{python3_sitearch}/PyQt4/QtXmlPatterns.so
%else
%{python3_sitearch}/PyQt4/Qt.pyd
%{python3_sitearch}/PyQt4/QtCore.pyd
%{python3_sitearch}/PyQt4/QtDecl.pyd
%{python3_sitearch}/PyQt4/QtDeclarative.pyd
%{python3_sitearch}/PyQt4/QtDsgn.pyd
%{python3_sitearch}/PyQt4/QtDesigner.pyd
%{python3_sitearch}/PyQt4/QtGui.pyd
%{python3_sitearch}/PyQt4/QtHelp.pyd
%{python3_sitearch}/PyQt4/QtNet.pyd
%{python3_sitearch}/PyQt4/QtNetwork.pyd
%{python3_sitearch}/PyQt4/QtScri.pyd
%{python3_sitearch}/PyQt4/QtScript.pyd
%{python3_sitearch}/PyQt4/QtScTl.pyd
%{python3_sitearch}/PyQt4/QtScriptTools.pyd
%{python3_sitearch}/PyQt4/QtSql.pyd
%{python3_sitearch}/PyQt4/QtSvg.pyd
%{python3_sitearch}/PyQt4/QtTest.pyd
%{python3_sitearch}/PyQt4/QtXml.pyd
%{python3_sitearch}/PyQt4/QtXmlP.pyd
%{python3_sitearch}/PyQt4/QtXmlPatterns.pyd
%endif
%{python3_sitearch}/PyQt4/uic/
%if !0%{?with_python2}
%{_qt4_plugindir}/designer/*
%endif

%if 0%{?qtassistant}
%files -n python3-%{name}-assistant
%if !0%{?os2_version}
%{python3_sitearch}/PyQt4/QtAssistant.so
%else
%{python3_sitearch}/PyQt4/QtAsst.pyd
%{python3_sitearch}/PyQt4/QtAssistant.pyd
%endif
%endif

%if 0%{?webkit}
%files -n python3-%{name}-webkit
%if !0%{?os2_version}
%{python3_sitearch}/PyQt4/QtWebKit.so
%else
%{python3_sitearch}/PyQt4/QtWebK.pyd
%{python3_sitearch}/PyQt4/QtWebKit.pyd
%endif
%endif

%files -n python3-%{name}-devel
%if !0%{?os2_version}
%{_bindir}/pylupdate4
%{_bindir}/pyrcc4
%{_bindir}/pyuic4
%else
%{_bindir}/pylupdate4.exe
%{_bindir}/pyrcc4.exe
%{_bindir}/pyuic4
%endif
%{py3_sipdir}/
# compat location
%dir %{_datadir}/python3-sip/
%{_datadir}/python3-sip/PyQt4/
%endif


%changelog
* Wed May 14 2025 Silvan Scherrer <silvan.scherrer@aroa.ch> - 4.12.3-2
- rebuild with python 3.13

* Fri Feb 04 2022 Silvan Scherrer <silvan.scherrer@aroa.ch> - 4.12.3-1
- update to latest PyQt4 version
- rebuild with later sip
- enable python3

* Fri Jul 01 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 4.11.4-4
- workaround the absolute path bug in Qt4

* Tue Jun 14 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 4.11.4-3
- rebuilt because of python ucs2/ucs4 change

* Fri Jun 3 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 4.11.4-2
- add symlink for long names
- add nameshort tag, as inplemented in sip

* Thu May 26 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 4.11.4-1
- initial version
