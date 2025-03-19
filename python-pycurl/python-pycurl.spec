# python3 is not available on RHEL <= 7
%if 0%{?fedora} || 0%{?rhel} > 7 || 0%{?os2_version}
%bcond_without python3
%else
%bcond_with python3
%endif

# python2 is not available on Fedora and el8+
%if 0%{?fedora} || 0%{?rhel} > 7
%bcond_with python2
%else
%bcond_without python2
%endif

# test dependencies are not available on el9+
%if 0%{?fedora}
%bcond_without tests
%else
%bcond_with tests
%endif

%global modname pycurl

Name:           python-%{modname}
Version:        7.44.1
Release:        3%{?dist}
Summary:        A Python interface to libcurl

License:        LGPLv2+ or MIT
URL:            http://pycurl.io/
%if !0%{?os2_version}
Source0:        https://files.pythonhosted.org/packages/47/f9/c41d6830f7bd4e70d5726d26f8564538d08ca3a7ac3db98b325f94cdcb7f/pycurl-%{version}.tar.gz

# drop link-time vs. run-time TLS backend check (#1446850)
Patch2:         0002-python-pycurl-7.43.0-tls-backend.patch
%else
Vendor:         bww bitwise works GmbH
%scm_source github http://github.com/bitwiseworks/pycurl-os2 REL_7_44_1-os2
%endif

BuildRequires:  gcc
BuildRequires:  libcurl-devel
BuildRequires:  make
BuildRequires:  openssl-devel
%if !0%{?os2_version}
BuildRequires:  vsftpd
%endif

# During its initialization, PycURL checks that the actual libcurl version
# is not lower than the one used when PycURL was built.
# Yes, that should be handled by library versioning (which would then get
# automatically reflected by rpm).
# For now, we have to reflect that dependency.
%global libcurl_sed '/^#define LIBCURL_VERSION "/!d;s/"[^"]*$//;s/.*"//;q'
%if !0%{?os2_version}
%global curlver_h /usr/include/curl/curlver.h
%else
%global curlver_h /@unixroot/usr/include/curl/curlver.h
%endif
%global libcurl_ver %(sed %{libcurl_sed} %{curlver_h} 2>/dev/null || echo 0)

%description
PycURL is a Python interface to libcurl. PycURL can be used to fetch
objects identified by a URL from a Python program, similar to the
urllib Python module. PycURL is mature, very fast, and supports a lot
of features.

%if %{with python2}
%package -n python2-%{modname}
Summary:        Python interface to libcurl for Python 2
%{?python_provide:%python_provide python2-%{modname}}
BuildRequires:  python2-devel
Requires:       libcurl >= %{libcurl_ver}

Provides:       %{modname} = %{version}-%{release}
%if 0%{?os2_version}
Provides:       python-%{modname} = %{version}-%{release}
Obsoletes:      python-%{modname} < %{version}-%{release}
%endif

%description -n python2-%{modname}
PycURL is a Python interface to libcurl. PycURL can be used to fetch
objects identified by a URL from a Python program, similar to the
urllib Python module. PycURL is mature, very fast, and supports a lot
of features.

Python 2 version.
%endif

%if %{with python3}
%package -n python3-%{modname}
Summary:        Python interface to libcurl for Python 3
%{?python_provide:%python_provide python3-%{modname}}
BuildRequires:  python3-devel
%if %{with tests}
BuildRequires:  python3-bottle
BuildRequires:  python3-pytest
%global pytest pytest
%else
%global pytest true
%endif
BuildRequires:  python3-setuptools
Requires:       libcurl >= %{libcurl_ver}

%description -n python3-%{modname}
PycURL is a Python interface to libcurl. PycURL can be used to fetch
objects identified by a URL from a Python program, similar to the
urllib Python module. PycURL is mature, very fast, and supports a lot
of features.

Python 3 version.
%endif

%prep
%if !0%{?os2_version}
%autosetup -n %{modname}-%{version} -p1
%setup0 -q -n pycurl-%{version}
%else
%scm_setup
%endif

# remove windows-specific build script
rm -fv winbuild.py
sed -e 's| winbuild.py||' -i Makefile

# remove a test-case that relies on sftp://web.sourceforge.net being available
rm -fv tests/ssh_key_cb_test.py

# remove a test-case that fails in Koji
rm -fv tests/seek_cb_test.py

# remove test-cases that depend on external network
%if !0%{?os2_version}
rm -fv examples/tests/test_{build_config,xmlrpc}.py
%else
rm -fv examples/tests/test_build_config.py
rm -fv examples/tests/test_xmlrpc.py
%endif

# remove a test-case that depends on pygtk
rm -fv examples/tests/test_gtk.py

# remove tests depending on the 'flaky' python module
grep '^import flaky' -r tests | cut -d: -f1 | xargs rm -fv

# use %%{python3} instead of python to invoke tests, to make them work on f34
sed -e 's|python |%{python3} |' -i tests/ext/test-suite.sh
sed -e 's|^#! */usr/bin/env python$|#! /usr/bin/env %{python3}|' \
    -i tests/*.py setup.py

%build
export VENDOR="%{vendor}"
%if %{with python2}
%py2_build -- --with-openssl
%endif
%if %{with python3}
%py3_build -- --with-openssl
%endif

%install
export PYCURL_SSL_LIBRARY=openssl
%if %{with python2}
%py2_install
%endif
%if %{with python3}
%py3_install
%endif
rm -rf %{buildroot}%{_datadir}/doc/pycurl

%if %{with python3} && %{with tests}
%check
# relax crypto policy for the test-suite to make it pass again (#1863711)
export OPENSSL_SYSTEM_CIPHERS_OVERRIDE=XXX
export OPENSSL_CONF=

export PYTHONPATH=%{buildroot}%{python3_sitearch}
export PYCURL_SSL_LIBRARY=openssl
export PYCURL_VSFTPD_PATH=vsftpd
make test PYTHON=%{__python3} PYTEST=%{pytest} PYFLAKES=true
rm -fv tests/fake-curl/libcurl/*.so
%endif

%if %{with python2}
%files -n python2-%{modname}
%license COPYING-LGPL COPYING-MIT
%doc ChangeLog README.rst examples doc tests
%{python2_sitearch}/curl/
%if !0%{?os2_version}
%{python2_sitearch}/%{modname}.so
%else
%{python2_sitearch}/%{modname}.pyd
%endif
%{python2_sitearch}/%{modname}-%{version}-*.egg-info
%endif

%if %{with python3}
%files -n python3-%{modname}
%license COPYING-LGPL COPYING-MIT
%doc ChangeLog README.rst examples doc tests
%{python3_sitearch}/curl/
%if !0%{?os2_version}
%{python3_sitearch}/%{modname}.*.so
%else
%{python3_sitearch}/%{modname}.pyd
%endif
%{python3_sitearch}/%{modname}-%{version}-*.egg-info
%endif

%changelog
* Wed Jan 12 2022 Silvan Scherrer <silvan.scherrer@aroa.ch> 7.44.1-3
- enable python3

* Mon Nov 08 2021 Silvan Scherrer <silvan.scherrer@aroa.ch> 7.44.1-2
- provide a python-pycurl and obsolete the old version

* Wed Nov 03 2021 Silvan Scherrer <silvan.scherrer@aroa.ch> 7.44.1-1
- update to 7.44.1
- resync spec with fedora version

* Thu Jun 09 2016 yd <yd@os2power.com> 7.19.5.1-2
- rebuild for ucs4, ticket#182.

* Thu Feb 05 2015 yd <yd@os2power.com> 7.19.5.1-1
- initial build.
