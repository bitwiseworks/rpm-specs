Summary: Library providing XML and HTML support
Name: libxml2
Version: 2.7.7
Release: 1
License: MIT
Group: Development/Libraries
Source: ftp://xmlsoft.org/libxml2/libxml2-%{version}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: python python-devel zlib-devel pkgconfig
URL: http://xmlsoft.org/

Patch1: libxml2-os2.diff

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

%package python
Summary: Python bindings for the libxml2 library
Group: Development/Libraries
Requires: libxml2 = %{version}-%{release}

%description python
The libxml2-python package contains a module that permits applications
written in the Python programming language to use the interface
supplied by the libxml2 library to manipulate XML files.

This library allows to manipulate XML files. It includes support 
to read, modify and write XML and HTML files. There is DTDs support
this includes parsing and validation even with complex DTDs, either
at parse time or later once the document has been modified.

%prep
%setup -q
%patch001 -p1 -b .os2~

%build
export CONFIG_SHELL="/bin/sh" ; \
export LDFLAGS="-Zbin-files -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp" ; \
export LIBS="-lurpo -lmmap -lpthread" ; \
%configure \
    --without-python \
    --enable-shared --disable-static \
    "--cache-file=%{_topdir}/cache/%{name}.cache"

make %{?smp_mflags}

gzip -9 ChangeLog

%install
rm -fr %{buildroot}

%makeinstall
gzip -9 doc/libxml2-api.xml
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/libxml2-python*

cp libxml2.dll $RPM_BUILD_ROOT%{_libdir}
cp .libs/xml2.lib $RPM_BUILD_ROOT%{_libdir}
cp .libs/xml2_s.a $RPM_BUILD_ROOT%{_libdir}
rm  $RPM_BUILD_ROOT%{_libdir}/xml2Conf.sh

# multiarch crazyness on timestamp differences or Makefile/binaries for examples
touch -m --reference=$RPM_BUILD_ROOT/%{_includedir}/libxml2/libxml/parser.h $RPM_BUILD_ROOT/%{_bindir}/xml2-config
(cd doc/examples ; make clean ; rm -rf .deps Makefile)

%clean
rm -fr %{buildroot}

#%post -p /sbin/ldconfig

#%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)

%doc AUTHORS ChangeLog.gz NEWS README Copyright TODO
%doc %{_mandir}/man1/xmllint.1*
%doc %{_mandir}/man1/xmlcatalog.1*
%doc %{_mandir}/man3/libxml.3*

%{_libdir}/lib*.dll
%{_bindir}/xmllint.exe
%{_bindir}/xmlcatalog.exe

%files devel
%defattr(-, root, root)

%doc %{_mandir}/man1/xml2-config.1*
%doc doc/*.html doc/html doc/*.gif doc/*.png
%doc doc/tutorial doc/libxml2-api.xml.gz
%doc doc/examples
%doc %dir %{_datadir}/gtk-doc/html/libxml2
%doc %{_datadir}/gtk-doc/html/libxml2/*.devhelp
%doc %{_datadir}/gtk-doc/html/libxml2/*.html
%doc %{_datadir}/gtk-doc/html/libxml2/*.png
%doc %{_datadir}/gtk-doc/html/libxml2/*.css

%{_libdir}/lib*.dll
%{_libdir}/xml2.a
%{_libdir}/xml2.lib
#%{_libdir}/*.sh
%{_includedir}/*
%{_bindir}/xml2-config
%{_datadir}/aclocal/libxml.m4
%{_libdir}/pkgconfig/libxml-2.0.pc

%files static
%defattr(-, root, root)

%{_libdir}/xml2_s.a

#%files python
#%defattr(-, root, root)
#%{_libdir}/python*/site-packages/libxml2.py*
#%{_libdir}/python*/site-packages/drv_libxml2.py*
#%{_libdir}/python*/site-packages/libxml2mod*
#%doc python/TODO
#%doc python/libxml2class.txt
#%doc python/tests/*.py
#%doc doc/*.py
#%doc doc/python.html

%changelog