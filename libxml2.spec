# remove the comment below, when we have python3 support
#global with_python3 1

#define svn_url     e:/trees/libxml2/trunk
%define svn_url     http://svn.netlabs.org/repos/ports/xml2/trunk
%define svn_rev     1830

Summary: Library providing XML and HTML support
Name: libxml2
Version: 2.9.4
Release: 1%{?dist}
License: MIT
Group: Development/Libraries
URL: http://xmlsoft.org/
Vendor: bww bitwise works GmbH

Source: %{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip

# DEF files to create forwarders for the legacy package
Source10:       libxml2.def

BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: python-devel
%if 0%{?with_python3}
BuildRequires: python3-devel
%endif # with_python3
BuildRequires: zlib-devel
BuildRequires: pkgconfig
#BuildRequires: xz-devel
Requires: libcx >= 0.4

%description
This library allows to manipulate XML files. It includes support 
to read, modify and write XML and HTML files. There is DTDs support
this includes parsing and validation even with complex DtDs, either
at parse time or later once the document has been modified. The output
can be a simple SAX stream or and in-memory DOM like representations.
In this case one can use the built-in XPath and XPointer implementation
to select subnodes or ranges. A flexible Input/Output mechanism is
available, with existing HTTP and FTP modules and combined to an
URI library.

%package devel
Summary: Libraries, includes, etc. to develop XML and HTML applications
Group: Development/Libraries
Requires: libxml2 = %{version}-%{release}
Requires: zlib-devel
#Requires: xz-devel
Requires: pkgconfig

%description devel
Libraries, include files, etc you can use to develop XML applications.
This library allows to manipulate XML files. It includes support 
to read, modify and write XML and HTML files. There is DTDs support
this includes parsing and validation even with complex DtDs, either
at parse time or later once the document has been modified. The output
can be a simple SAX stream or and in-memory DOM like representations.
In this case one can use the built-in XPath and XPointer implementation
to select subnodes or ranges. A flexible Input/Output mechanism is
available, with existing HTTP and FTP modules and combined to an
URI library.

%package static
Summary: Static library for libxml2
Group: Development/Libraries
Requires: libxml2 = %{version}-%{release}

%description static
Static library for libxml2 provided for specific uses or shaving a few
microseconds when parsing, do not link to them for generic purpose packages.

%package -n python-%{name}
Summary: Python bindings for the libxml2 library
Group: Development/Libraries
Requires: libxml2 = %{version}-%{release}
Obsoletes: %{name}-python < %{version}-%{release}
Provides: %{name}-python = %{version}-%{release}

%description -n python-%{name}
The libxml2-python package contains a Python 2 module that permits applications
written in the Python programming language, version 2, to use the interface
supplied by the libxml2 library to manipulate XML files.

This library allows to manipulate XML files. It includes support
to read, modify and write XML and HTML files. There is DTDs support
this includes parsing and validation even with complex DTDs, either
at parse time or later once the document has been modified.

%if 0%{?with_python3}
%package -n python3-%{name}
Summary: Python 3 bindings for the libxml2 library
Group: Development/Libraries
Requires: libxml2 = %{version}-%{release}
Obsoletes: %{name}-python3 < %{version}-%{release}
Provides: %{name}-python3 = %{version}-%{release}

%description -n python3-%{name}
The libxml2-python3 package contains a Python 3 module that permits
applications written in the Python programming language, version 3, to use the
interface supplied by the libxml2 library to manipulate XML files.

This library allows to manipulate XML files. It includes support
to read, modify and write XML and HTML files. There is DTDs support
this includes parsing and validation even with complex DTDs, either
at parse time or later once the document has been modified.
%endif # with_python3

%debug_package

%prep
%if %{?svn_rev:%(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')}%{?!svn_rev):0}
%setup -q
%else
%setup -n "%{name}-%{version}" -Tc
svn export %{?svn_rev:-r %{svn_rev}} %{svn_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip" "%{name}-%{version}")
%endif

# Prepare forwarder DLLs.
for m in %{SOURCE10}; do
  cp ${m} .
done

%if 0%{?with_python3}
mkdir py3doc
cp doc/*.py py3doc
sed -i 's|#!/usr/bin/python |#!%{__python3} |' py3doc/*.py
%endif

export NOCONFIGURE=1
autogen.sh

%build
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
export VENDOR="%{vendor}"
%configure

make %{?smp_mflags}


%install
rm -fr %{buildroot}

make install DESTDIR=%{buildroot}

%if 0%{?with_python3}
make clean
%configure --with-python=%{__python3}
make install DESTDIR=%{buildroot}
%endif # with_python3

# multiarch crazyness on timestamp differences or Makefile/binaries for examples
touch -m --reference=$RPM_BUILD_ROOT/%{_includedir}/libxml2/libxml/parser.h $RPM_BUILD_ROOT/%{_bindir}/xml2-config

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/python*/site-packages/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/python*/site-packages/*.la
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/libxml2-%{version}/*
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/libxml2-python-%{version}/*
(cd doc/examples ; make clean ; rm -rf .deps Makefile)
gzip -9 -c doc/libxml2-api.xml > doc/libxml2-api.xml.gz

# Generate & install forwarder DLLs.
gcc -Zomf -Zdll libxml2.def -l$RPM_BUILD_ROOT/%{_libdir}/xml22.dll -o $RPM_BUILD_ROOT/%{_libdir}/libxml2.dll

# create a symlink for the python binding, as the dll itself is named xml2mod.dll
ln -s %{_libdir}/python2.7/site-packages/xml2mod.dll $RPM_BUILD_ROOT%{_libdir}/python2.7/site-packages/libxml2mod.pyd

%check
#make runtests

%clean
rm -fr %{buildroot}

#%post -p /sbin/ldconfig

#%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)

%{!?_licensedir:%global license %%doc}
%license Copyright
%doc AUTHORS NEWS README TODO
%doc %{_mandir}/man1/xmllint.1*
%doc %{_mandir}/man1/xmlcatalog.1*
%doc %{_mandir}/man3/libxml.3*

%{_libdir}/xml2*.dll
%{_bindir}/xmllint.exe
%{_bindir}/xmlcatalog.exe
#forwarder dll
%{_libdir}/libxml2.dll

%files devel
%defattr(-, root, root)

%doc %{_mandir}/man1/xml2-config.1*
%doc AUTHORS NEWS README Copyright
%doc doc/*.html doc/html doc/*.gif doc/*.png
%doc doc/tutorial doc/libxml2-api.xml.gz
%doc doc/examples
%doc %dir %{_datadir}/gtk-doc/html/libxml2
%doc %{_datadir}/gtk-doc/html/libxml2/*.devhelp
%doc %{_datadir}/gtk-doc/html/libxml2/*.html
%doc %{_datadir}/gtk-doc/html/libxml2/*.png
%doc %{_datadir}/gtk-doc/html/libxml2/*.css

%{_libdir}/xml2*_dll.a
%{_libdir}/*.sh
%{_includedir}/*
%{_bindir}/xml2-config
%{_datadir}/aclocal/libxml.m4
%{_libdir}/pkgconfig/libxml-2.0.pc
%{_libdir}/cmake/libxml2/libxml2-config.cmake

%files static
%defattr(-, root, root)

%{_libdir}/xml2.a

%files -n python-%{name}
%defattr(-, root, root)

%{_libdir}/python2*/site-packages/libxml2.py*
%{_libdir}/python2*/site-packages/drv_libxml2.py*
%{_libdir}/python2*/site-packages/libxml2mod*
%{_libdir}/python2*/site-packages/xml2mod.dll
%doc python/TODO
%doc python/libxml2class.txt
%doc doc/*.py
%doc doc/python.html

%if 0%{?with_python3}
%files -n python3-%{name}
%defattr(-, root, root)

%{_libdir}/python3*/site-packages/libxml2.py*
%{_libdir}/python3*/site-packages/drv_libxml2.py*
%{_libdir}/python3*/site-packages/__pycache__/*py*
%{_libdir}/python3*/site-packages/libxml2mod*
%doc python/TODO
%doc python/libxml2class.txt
%doc py3doc/*.py
%doc doc/python.html
%endif # with_python3

%changelog
* Fri Nov 25 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.9.4-1
- update to version 2.9.4
- adjust to the current toolchain
- build and install the python binding within this spec as well

* Mon Apr 07 2014 yd
- build for python 2.7.
- added debug package with symbolic info for exceptq.

* Mon Jan 16 2012 yd
- rebuild with libc 0.6.4 runtime.
