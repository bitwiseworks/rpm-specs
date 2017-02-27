### remark: as soon as setuptools is done, enable it here also !!!


%global srcname pyparsing
%global sum Python package with an object-oriented approach to text processing

%global build_wheel 0
%global with_python3 0

%global python2_wheelname %{srcname}-%{version}-py2.py3-none-any.whl
%global python3_wheelname %python2_wheelname

Summary:        %{sum}
Name:           pyparsing
Version:        2.1.10
Release:        1%{?dist}

License:        MIT
URL:            http://pyparsing.wikispaces.com/
Vendor:         bww bitwise works GmbH
%scm_source  svn http://svn.netlabs.org/repos/ports/pyparsing/trunk 2076

BuildArch:      noarch
BuildRequires:  dos2unix
BuildRequires:  python2-devel
#BuildRequires:  python2-setuptools
%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif

%if 0%{?build_wheel}
BuildRequires:  python2-pip
BuildRequires:  python-wheel
BuildRequires:  python%{python3_pkgversion}-pip
BuildRequires:  python%{python3_pkgversion}-wheel
%endif

Requires:      python-%{srcname} = %{version}-%{release}

%description
pyparsing is a module that can be used to easily and directly configure syntax
definitions for any number of text parsing applications.


%package        doc
Summary:        Documentation for pyparsing python package

%description    doc
The package contains documentation for pyparsing.


%package -n python2-%{srcname}
Summary:       %{sum}
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-pyparsing
pyparsing is a module that can be used to easily and directly configure syntax
definitions for any number of text parsing applications.


%if 0%{?with_python3}
%package -n python3-pyparsing
Summary:        %{sum}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-pyparsing
pyparsing is a module that can be used to easily and directly configure syntax
definitions for any number of text parsing applications.

This is the Python 3 version.
%endif


%prep
%scm_setup
#mv docs/pyparsingClassDiagram.PNG docs/pyparsingClassDiagram.png
rm docs/pyparsingClassDiagram.JPG
dos2unix -k CHANGES LICENSE README

%build
%if 0%{?build_wheel}
%py2_build_wheel
%else
%py2_build
%endif
%if 0%{?with_python3}
%if 0%{?build_wheel}
%py3_build_wheel
%else
%py3_build
%endif
%endif

%install
%if 0%{?build_wheel}
%py2_install_wheel %{python2_wheelname}
%else
%py2_install
%endif
%if 0%{?with_python3}
%if 0%{?build_wheel}
%py3_install_wheel %{python3_wheelname}
%else
%py3_install
%endif
%endif

%files

%files -n python2-pyparsing
%license LICENSE
%doc CHANGES README
%{python2_sitelib}/*

%if 0%{?with_python3}
%files -n python3-pyparsing
%license LICENSE
%doc CHANGES README LICENSE
%{python3_sitelib}/pyparsing.py
%{python3_sitelib}/__pycache__/*
%{python3_sitelib}/pyparsing-*dist-info/
%endif

%files doc
%license LICENSE
%doc CHANGES README HowToUsePyparsing.html docs examples htmldoc

%changelog
* Mon Feb 27 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.1.10-1
- first rpm version
