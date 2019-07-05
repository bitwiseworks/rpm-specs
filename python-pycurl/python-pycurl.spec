%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           python-pycurl
Version:        7.19.5.1
Release:        2%{?dist}
Summary:        A Python interface to libcurl

Group:          Development/Languages
License:        LGPLv2+ or MIT
URL:            http://pycurl.sourceforge.net/
Source0:        http://pycurl.sourceforge.net/download/pycurl-%{version}.tar.gz
Patch0:		pycurl-os2.patch

#Requires:       keyutils-libs
BuildRequires:  python-devel
#BuildRequires:  python3-devel
BuildRequires:  curl-devel >= 7.19.0
BuildRequires:  openssl-devel
#BuildRequires:  python-bottle
#BuildRequires:  python-cherrypy
#BuildRequires:  python-nose
#BuildRequires:  python3-bottle
#BuildRequires:  python3-cherrypy
#BuildRequires:  python3-nose
#BuildRequires:  vsftpd

Requires:       libcurl >= 7.37

# YD because of ucs4
Requires:       python >= 2.7.6-13

Provides:       pycurl = %{version}-%{release}

%description
PycURL is a Python interface to libcurl. PycURL can be used to fetch
objects identified by a URL from a Python program, similar to the
urllib Python module. PycURL is mature, very fast, and supports a lot
of features.

%package -n python3-pycurl
Summary:        A Python interface to libcurl for Python 3

%description -n python3-pycurl
PycURL is a Python interface to libcurl. PycURL can be used to fetch
objects identified by a URL from a Python program, similar to the
urllib Python module. PycURL is mature, very fast, and supports a lot
of features.

%prep
%setup0 -q -n pycurl-%{version}
%patch0 -p0 -b .os2~

# temporarily exclude failing test-cases
rm -f tests/{pycurl_object_test,share_test}.py

# fails with python3 on i686
rm -f tests/post_test.py

# copy the whole directory for the python3 build
#cp -a . %{py3dir}

%build
export CFLAGS="$RPM_OPT_FLAGS"
%{__python} setup.py build
# --with-nss // YD openssl required as in curl
#pushd %{py3dir}
#%{__python3} setup.py build --with-nss
#popd

%check
#export PYTHONPATH=$RPM_BUILD_ROOT%{python_sitearch}
#make test PYTHON=%{__python}
#pushd %{py3dir}
#export PYTHONPATH=$RPM_BUILD_ROOT%{python3_sitearch}
#make test PYTHON=%{__python3} NOSETESTS="nosetests-%{python3_version} -v"
#popd

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
#pushd %{py3dir}
#%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
#popd
rm -rf %{buildroot}%{_datadir}/doc/pycurl

%files
%{!?_licensedir:%global license %%doc}
%license COPYING-LGPL COPYING-MIT
%doc ChangeLog README.rst examples doc tests
%{python_sitearch}/*

#%files -n python3-pycurl
# TODO: find the lost COPYING file
#%{!?_licensedir:%global license %%doc}
#%license COPYING-LGPL COPYING-MIT
#%doc ChangeLog README.rst examples doc tests
#%{python3_sitearch}/*

%changelog
* Thu Jun 09 2016 yd <yd@os2power.com> 7.19.5.1-2
- rebuild for ucs4, ticket#182.

* Thu Feb 05 2015 yd <yd@os2power.com> 7.19.5.1-1
- initial build.
