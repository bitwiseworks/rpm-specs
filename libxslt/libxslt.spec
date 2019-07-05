Summary: Library providing the Gnome XSLT engine
Name: libxslt
Version: 1.1.32
Release: 1%{?dist}%{?extra_release}
License: MIT
Group: Development/Libraries
URL: http://xmlsoft.org/XSLT/
Vendor: bww bitwise works GmbH

%scm_source  github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2

# DEF files to create forwarders for the legacy package
Source10:       libxslt.def
Source11:       libexslt.def

Requires: libxml2 >= 2.6.27
Requires: libcx >= 0.4

BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: libxml2-devel >= 2.6.27
BuildRequires: python2-devel
BuildRequires: libxml2-python
#BuildRequires: libgcrypt-devel
BuildRequires: automake autoconf

%description
This C library allows to transform XML files into other XML files
(or HTML, text, ...) using the standard XSLT stylesheet transformation
mechanism. To use it you need to have a version of libxml2 >= 2.6.27
installed. The xsltproc command is a command line interface to the XSLT engine

%package devel
Summary: Libraries, includes, etc. to embed the Gnome XSLT engine
Group: Development/Libraries
Requires: libxslt = %{version}-%{release}
Requires: libxml2-devel >= 2.6.27
#Requires: libgcrypt-devel
Requires: pkgconfig

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package python
Summary: Python bindings for the libxslt library
Group: Development/Libraries
Requires: libxslt = %{version}-%{release}
Requires: libxml2 >= 2.6.27
Requires: libxml2-python >= 2.6.27

%description python
The libxslt-python package contains a module that permits applications
written in the Python programming language to use the interface
supplied by the libxslt library to apply XSLT transformations.

This library allows to parse sytlesheets, uses the libxml2-python
to load and save XML and HTML files. Direct access to XPath and
the XSLT transformation context are possible to extend the XSLT language
with XPath functions written in Python.

%debug_package

%prep
%scm_setup

# Prepare forwarder DLLs.
for m in %{SOURCE10} %{SOURCE11}; do
  cp ${m} .
done

autoreconf -fvi

gzip -9 ChangeLog

%build
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
export VENDOR="%{vendor}"
%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# multiarch crazyness on timestamp differences
touch -m --reference=$RPM_BUILD_ROOT/%{_includedir}/libxslt/xslt.h $RPM_BUILD_ROOT/%{_bindir}/xslt-config

rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-%{version}
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-python-%{version}
rm -f $RPM_BUILD_ROOT%{python_sitearch}/*.a

# Generate & install forwarder DLLs.
gcc -Zomf -Zdll -nostdlib libxslt.def -l$RPM_BUILD_ROOT/%{_libdir}/xslt1.dll -lend -o $RPM_BUILD_ROOT/%{_libdir}/xslt.dll
gcc -Zomf -Zdll -nostdlib libexslt.def -l$RPM_BUILD_ROOT/%{_libdir}/exslt0.dll -lend -o $RPM_BUILD_ROOT/%{_libdir}/exslt.dll

# create a symlink for the python binding, as the dll itself is named xml2mod.dll
ln -s %{python_sitearch}/xsltmod.dll $RPM_BUILD_ROOT%{python_sitearch}/libxsltmod.pyd

%clean
rm -fr %{buildroot}

%check
#make tests

#post -p /sbin/ldconfig

#postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%doc AUTHORS ChangeLog.gz NEWS README Copyright FEATURES
%doc %{_mandir}/man1/xsltproc.1*
%{_libdir}/*.dll
%{_libdir}/libxslt-plugins
%{_bindir}/xsltproc.exe

%files devel
%defattr(-, root, root)
%doc doc/libxslt-api.xml
%doc doc/libxslt-refs.xml
%doc doc/EXSLT/libexslt-api.xml
%doc doc/EXSLT/libexslt-refs.xml
%doc %{_mandir}/man3/libxslt.3*
%doc %{_mandir}/man3/libexslt.3*
%doc doc/*.html doc/html doc/*.gif doc/*.png
%doc doc/images
%doc doc/tutorial
%doc doc/tutorial2
%doc doc/EXSLT
%{_libdir}/*_dll.a
%{_libdir}/*.sh
%{_datadir}/aclocal/libxslt.m4
%{_includedir}/*
%{_bindir}/xslt-config
%{_libdir}/pkgconfig/libxslt.pc
%{_libdir}/pkgconfig/libexslt.pc

%files python
%defattr(-, root, root)
%{python_sitearch}/libxslt.py*
%{python_sitearch}/libxsltmod*
%{python_sitearch}/xsltmod.dll
%doc python/libxsltclass.txt
%doc python/tests/*.py
%doc python/tests/*.xml
%doc python/tests/*.xsl

%changelog
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
