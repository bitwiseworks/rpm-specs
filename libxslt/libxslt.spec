Name:           libxslt
Summary:        Library providing the Gnome XSLT engine
Version:        1.1.39
Release:        2%{?dist}

License:        MIT
URL:            https://gitlab.gnome.org/GNOME/libxslt
%if !0%{?os2_version}
Source0:        https://download.gnome.org/sources/%{name}/1.1/%{name}-%{version}.tar.xz
%else
Vendor:         bww bitwise works GmbH
%scm_source     github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2

# DEF files to create forwarders for the legacy package
Source10:       libxslt.def
Source11:       libexslt.def
%endif

Provides: xsltproc = %{version}-%{release}

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  pkgconfig(libxml-2.0) >= 2.6.27

%if !0%{?os2_version}
# Fedora specific patches
Patch0:         multilib.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1467435
Patch1:         multilib2.patch
%endif

%description
This C library allows to transform XML files into other XML files
(or HTML, text, ...) using the standard XSLT stylesheet transformation
mechanism. To use it you need to have a version of libxml2 >= 2.6.27
installed. The xsltproc command is a command line interface to the XSLT engine

%package devel
Summary:        Development libraries and header files for %{name}
%if !0%{?os2_version}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libgpg-error-devel%{?_isa}
%else
Requires:       %{name} = %{version}-%{release}
Requires:       libgpg-error-devel
%endif

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%if 1
# Upstream package has not been ported to Python 3.  I have
# converted this section so it could be used to compile the
# Python 3 bindings one day once that has happened, but
# commented it out.  - RWMJ 2019-09-10
%package -n python3-libxslt
Summary:        Python 3 bindings for %{name}
BuildRequires:  python3-devel
BuildRequires:  python3-libxml2
%if !0%{?os2_version}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%else
Requires:       %{name} = %{version}-%{release}
%endif
Requires:       python3-libxml2
%{?python_provide:%python_provide python3-%{name}}

%description -n python3-libxslt
The libxslt-python package contains a module that permits applications
written in the Python programming language to use the interface
supplied by the libxslt library to apply XSLT transformations.

This library allows to parse sytlesheets, uses the libxml2-python
to load and save XML and HTML files. Direct access to XPath and
the XSLT transformation context are possible to extend the XSLT language
with XPath functions written in Python.
%endif

%if 0%{?os2_version}
%debug_package
%endif

%prep
%if !0%{?os2_version}
%autosetup -p1
%else
%scm_setup
# Prepare forwarder DLLs.
for m in %{SOURCE10} %{SOURCE11}; do
  cp ${m} .
done
%endif
chmod 644 python/tests/*

%build
%if 0%{?os2_version}
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
export VENDOR="%{vendor}"
%endif
autoreconf -vfi
#export PYTHON=%{__python3}
#%configure --disable-static --disable-silent-rules --with-python
%configure --disable-static --disable-silent-rules --with-python=yes --with-crypto=no
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -print -delete
# multiarch crazyness on timestamp differences
touch -m --reference=%{buildroot}%{_includedir}/libxslt/xslt.h %{buildroot}%{_bindir}/xslt-config
rm -vrf %{buildroot}%{_docdir}

%if 0%{?os2_version}
rm -vf %{buildroot}%{python3_sitearch}/*.a
# Generate & install forwarder DLLs.
gcc -Zomf -Zdll -nostdlib libxslt.def -l$RPM_BUILD_ROOT/%{_libdir}/xslt1.dll -lend -o $RPM_BUILD_ROOT/%{_libdir}/xslt.dll
gcc -Zomf -Zdll -nostdlib libexslt.def -l$RPM_BUILD_ROOT/%{_libdir}/exslt0.dll -lend -o $RPM_BUILD_ROOT/%{_libdir}/exslt.dll

# create a symlink for the python binding, as the dll itself is named xml2mod.dll
ln -s xsltmod.dll %{buildroot}%{python3_sitearch}/libxsltmod.pyd
%endif

%check
%if !0%{?os2_version}
%make_build tests
%endif

%if !0%{?os2_version}
%ldconfig_scriptlets
%endif

%files
%license Copyright
%doc AUTHORS NEWS README.md FEATURES
%if !0%{?os2_version}
%{_bindir}/xsltproc
%{_libdir}/libxslt.so.*
%{_libdir}/libexslt.so.*
%else
%{_bindir}/xsltproc.exe
%{_libdir}/xslt*.dll
%{_libdir}/exslt*.dll
%endif
%{_libdir}/libxslt-plugins/
%{_mandir}/man1/xsltproc.1*

%files devel
%doc doc/libxslt-api.xml
%doc doc/EXSLT/libexslt-api.xml
%doc %{_mandir}/man3/libxslt.3*
%doc %{_mandir}/man3/libexslt.3*
#%doc doc/*.html doc/html doc/*.gif doc/*.png
#%doc doc/images
%doc doc/tutorial
%doc doc/tutorial2
#%%doc doc/EXSLT
%{_datadir}/gtk-doc/
%{_libdir}/cmake/libxslt/
%if !0%{?os2_version}
%{_libdir}/libxslt.so
%{_libdir}/libexslt.so
%else
%{_libdir}/*_dll.a
%endif
%{_libdir}/xsltConf.sh
%{_datadir}/aclocal/libxslt.m4
%{_includedir}/libxslt/
%{_includedir}/libexslt/
%{_libdir}/pkgconfig/libxslt.pc
%{_libdir}/pkgconfig/libexslt.pc
%{_bindir}/xslt-config

%if 1
%files -n python3-libxslt
%{python3_sitearch}/libxslt.py*
%if !0%{?os2_version}
%{python3_sitearch}/libxsltmod.so
%else
%{python3_sitearch}/libxsltmod*
%{python3_sitearch}/xsltmod.dll
%endif
%{python3_sitelib}/__pycache__/libxslt*
%doc python/libxsltclass.txt
%doc python/tests/*.py
%doc python/tests/*.xml
%doc python/tests/*.xsl
%endif

%changelog
* Tue May 13 2025 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.1.39-2
- rebuild with python 3.12
- don't create the symlink with absolute path

* Fri Jan 26 2024 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.1.39-1
- update to version 1.1.39
- resync with fedora spec
- remove python2 binding
- add python3 binding

* Mon Jan 17 2022 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.1.34-2
- resync with fedora spec

* Wed Feb 12 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.1.34-1
- update to vendor version 1.1.34

* Thu Jul 26 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.1.32-1
- update to vendor version 1.1.32
- moved source to github
- use the new scm_source and scm_setup macros

* Wed Nov 30 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.1.29-2
- add -nostdlib to forwarders, to need less heap

* Fri Nov 25 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.1.29-1
- update to version 1.1.29
- adjust to the current toolchain

* Mon Apr 07 2014 yd
- build for python 2.7.
- added debug package with symbolic info for exceptq.
