# Note: this .spec is borrowed from python-lxml-3.4.4-2.fc24.src.rpm

%if 0%{?fedora} > 12
%global with_python3 1
%endif

%if 0%{?fedora} >= 20
%global with_python3_cssselect 1
%endif

%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           python-lxml
Version:        3.5.0
Release:        1%{?dist}
Summary:        ElementTree-like Python bindings for libxml2 and libxslt

Group:          Development/Libraries
License:        BSD
URL:            http://lxml.de
Source0:        http://lxml.de/files/lxml-%{version}.tgz
#Source1:        http://lxml.de/files/lxml-%{version}.tgz.asc

BuildRequires:  libxslt-devel

BuildRequires:  python-devel
#BuildRequires:  python-setuptools
#BuildRequires:  python-cssselect
#BuildRequires:  Cython >= 0.20

#Requires:       python-cssselect

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if 0%{?with_python3_cssselect}
BuildRequires:  python3-cssselect
%endif
%endif

%description
lxml provides a Python binding to the libxslt and libxml2 libraries.
It follows the ElementTree API as much as possible in order to provide
a more Pythonic interface to libxml2 and libxslt than the default
bindings.  In particular, lxml deals with Python Unicode strings
rather than encoded UTF-8 and handles memory management automatically,
unlike the default bindings.

%package docs
Summary:        Documentation for %{name}
Group:          Documentation
BuildArch:      noarch
%description docs
This package provides the documentation for %{name}, e.g. the API as html.


%if 0%{?with_python3}
%package -n python3-lxml
Summary:        ElementTree-like Python 3 bindings for libxml2 and libxslt
Group:          Development/Libraries
%if 0%{?with_python3_cssselect}
Requires:       python3-cssselect
%endif

%description -n python3-lxml
lxml provides a Python 3 binding to the libxslt and libxml2 libraries.
It follows the ElementTree API as much as possible in order to provide
a more Pythonic interface to libxml2 and libxslt than the default
bindings.  In particular, lxml deals with Python 3 Unicode strings
rather than encoded UTF-8 and handles memory management automatically,
unlike the default bindings.
%endif

%prep
%setup -q -n lxml-%{version}

## remove the C extension so that it will be rebuilt using the latest Cython
#rm -f src/lxml/lxml.etree.c
#rm -f src/lxml/lxml.etree.h
#rm -f src/lxml/lxml.etree_api.h
#rm -f src/lxml/lxml.objectify.c

chmod a-x doc/rest2html.py
sed -i 's/\r//' doc/s5/ui/default/print.css \
    doc/s5/ep2008/atom.rng \
    doc/s5/ui/default/iepngfix.htc

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -r . %{py3dir}
%endif

%build
CFLAGS="%{optflags}" %{__python} setup.py build
#--with-cython

%if 0%{?with_python3}
cp src/lxml/lxml.etree.c %{py3dir}/src/lxml
cp src/lxml/lxml.etree.h %{py3dir}/src/lxml
cp src/lxml/lxml.etree_api.h %{py3dir}/src/lxml
cp src/lxml/lxml.objectify.c %{py3dir}/src/lxml

pushd %{py3dir}
CFLAGS="%{optflags}" %{__python3} setup.py build --with-cython
popd
%endif

%install
%{__python} setup.py install --skip-build --no-compile --root %{buildroot}
#--with-cython

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --no-compile --with-cython --root %{buildroot}
popd
%endif

%check
# @todo enable once we got python-unittest
#BUILD_LIB_DIR=$(find $(pwd) -name "*.pyd" | head -n 1 | xargs dirname)
#cp $BUILD_LIB_DIR/*.pyd src/lxml
#export LANG=en_US.utf8
#%{__python} test.py -p -v
#export PYTHONPATH=src
#%{__python} selftest.py
#%{__python} selftest2.py

%if 0%{?with_python3}
pushd %{py3dir}

BUILD_LIB_DIR=$(find $(pwd) -name "*.pyd" | head -n 1 | xargs dirname)
cp $BUILD_LIB_DIR/*.pyd src/lxml
export LANG=en_US.utf8
%{__python3} test.py -p -v
export PYTHONPATH=src
%{__python3} selftest.py
%{__python3} selftest2.py

popd
%endif


%files
%{!?_licensedir:%global license %%doc}
%license LICENSES.txt
%doc PKG-INFO CREDITS.txt CHANGES.txt
%{python_sitearch}/lxml
%{python_sitearch}/lxml-*.egg-info

%files docs
%doc doc/*

%if 0%{?with_python3}
%files -n python3-lxml
%license LICENSES.txt
%doc PKG-INFO CREDITS.txt CHANGES.txt
%{python3_sitearch}/lxml-*.egg-info
%{python3_sitearch}/lxml
%endif

%changelog
* Thu Dec 12 2015 Dmitriy Kuminov <coding@dmik.org> 3.5.0-1
- Initial package for version 3.5.0.
