Name:           libxml2
Version:        2.9.10
Release:        2%{?dist}
Summary:        Library providing XML and HTML support

License:        MIT
URL:            http://xmlsoft.org/
%if !0%{?os2_version}
Source:         ftp://xmlsoft.org/libxml2/libxml2-%{version}.tar.gz
Patch0:         libxml2-multilib.patch
# Patch from openSUSE.
# See:  https://bugzilla.gnome.org/show_bug.cgi?id=789714
Patch1:         libxml2-2.9.8-python3-unicode-errors.patch
%else
%scm_source     github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2-1
Vendor:         bww bitwise works GmbH

# DEF files to create forwarders for the legacy package
Source10:       libxml2.def
%endif

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  cmake-rpm-macros
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(liblzma)

%description
This library allows to manipulate XML files. It includes support
to read, modify and write XML and HTML files. There is DTDs support
this includes parsing and validation even with complex DtDs, either
at parse time or later once the document has been modified. The output
can be a simple SAX stream or and in-memory DOM like representations.
In this case one can use the built-in XPath and XPointer implementation
to select sub nodes or ranges. A flexible Input/Output mechanism is
available, with existing HTTP and FTP modules and combined to an
URI library.

%package devel
Summary:        Libraries, includes, etc. to develop XML and HTML applications
Requires:       %{name} = %{version}-%{release}
Requires:       zlib-devel
Requires:       xz-devel

%description devel
Libraries, include files, etc you can use to develop XML applications.
This library allows to manipulate XML files. It includes support
to read, modify and write XML and HTML files. There is DTDs support
this includes parsing and validation even with complex DtDs, either
at parse time or later once the document has been modified. The output
can be a simple SAX stream or and in-memory DOM like representations.
In this case one can use the built-in XPath and XPointer implementation
to select sub nodes or ranges. A flexible Input/Output mechanism is
available, with existing HTTP and FTP modules and combined to an
URI library.

%package static
Summary:        Static library for libxml2

%description static
Static library for libxml2 provided for specific uses or shaving a few
microseconds when parsing, do not link to them for generic purpose packages.

%package -n python2-%{name}
%{?python_provide:%python_provide python2-%{name}}
Summary:        Python bindings for the libxml2 library
BuildRequires:  python2-devel
Requires:       %{name} = %{version}-%{release}
Obsoletes:      %{name}-python < %{version}-%{release}
Provides:       %{name}-python = %{version}-%{release}

%description -n python2-%{name}
The libxml2-python package contains a Python 2 module that permits applications
written in the Python programming language, version 2, to use the interface
supplied by the libxml2 library to manipulate XML files.

This library allows to manipulate XML files. It includes support
to read, modify and write XML and HTML files. There is DTDs support
this includes parsing and validation even with complex DTDs, either
at parse time or later once the document has been modified.

%package -n python3-%{name}
Summary:        Python 3 bindings for the libxml2 library
BuildRequires:  python3-devel
Requires:       %{name} = %{version}-%{release}
Obsoletes:      %{name}-python3 < %{version}-%{release}
Provides:       %{name}-python3 = %{version}-%{release}

%description -n python3-%{name}
The libxml2-python3 package contains a Python 3 module that permits
applications written in the Python programming language, version 3, to use the
interface supplied by the libxml2 library to manipulate XML files.

This library allows to manipulate XML files. It includes support
to read, modify and write XML and HTML files. There is DTDs support
this includes parsing and validation even with complex DTDs, either
at parse time or later once the document has been modified.

%if 0%{?os2_version}
%debug_package
%endif

%prep
%if !0%{?os2_version}
%autosetup -p1
%else
%scm_setup

# Prepare forwarder DLLs.
for m in %{SOURCE10}; do
  cp ${m} .
done

export NOCONFIGURE=1
autogen.sh
%endif
find doc -type f -executable -print -exec chmod 0644 {} ';'

%build
%if 0%{?os2_version}
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
export VENDOR="%{vendor}"
%endif
mkdir py2 py3
%if !0%{?os2_version}
%global _configure ../configure
%else
%global _configure ../configure --enable-ipv6=no --with-icu
%endif
%global _configure_disable_silent_rules 1
( cd py2 && %configure --cache-file=../config.cache --with-python=%{__python2} )
( cd py3 && %configure --cache-file=../config.cache --with-python=%{__python3} )
%if !0%{?os2_version}
%make_build -C py2
%make_build -C py3
%else
make %{?smp_mflags} -C py2
make %{?smp_mflags} -C py3
%endif

%install
%make_install -C py2
%make_install -C py3

# multiarch crazyness on timestamp differences or Makefile/binaries for examples
touch -m --reference=%{buildroot}%{_includedir}/libxml2/libxml/parser.h %{buildroot}%{_bindir}/xml2-config

find %{buildroot} -type f -name '*.la' -print -delete
%if !0%{?os2_version}
rm -vf %{buildroot}{%{python2_sitearch},%{python3_sitearch}}/*.a
%else
rm -vf %{buildroot}%{python2_sitearch}/*.a
rm -vf %{buildroot}%{python3_sitearch}/*.a
%endif
rm -vrf %{buildroot}%{_datadir}/doc/
#(cd doc/examples ; make clean ; rm -rf .deps Makefile)
gzip -9 -c doc/libxml2-api.xml > doc/libxml2-api.xml.gz

%if 0%{?os2_version}
# Generate & install forwarder DLLs.
gcc -Zomf -Zdll -nostdlib libxml2.def -l$RPM_BUILD_ROOT/%{_libdir}/xml22.dll -lend -o $RPM_BUILD_ROOT/%{_libdir}/libxml2.dll

# create a symlink for the python binding, as the dll itself is named xml2mod.dll
ln -s %{python2_sitearch}/xml2mod.dll $RPM_BUILD_ROOT%{python2_sitearch}/libxml2mod.pyd
ln -s %{python3_sitearch}/xml2mod.dll $RPM_BUILD_ROOT%{python3_sitearch}/libxml2mod.pyd
%endif

%check
%if !0%{?os2_version}
%make_build runtests -C py2
%make_build runtests -C py3
%else
# tests work just by luck right now
# tests/Makefile.am needs some changes
#export BEGINLIBPATH=%{_builddir}/%{buildsubdir}/py2/.libs
#make runtests -C py2
#export BEGINLIBPATH=%{_builddir}/%{buildsubdir}/py3/.libs
#make runtests -C py3
%endif

%if !0%{?os2_version}
%ldconfig_scriptlets
%endif

%files
%license Copyright
%doc AUTHORS NEWS README TODO
%if !0%{?os2_version}
%{_libdir}/libxml2.so.2*
%else
%{_libdir}/xml2*.dll
#forwarder dll
%{_libdir}/libxml2.dll
%endif
%{_mandir}/man3/libxml.3*
%if !0%{?os2_version}
%{_bindir}/xmllint
%else
%{_bindir}/xmllint.exe
%endif
%{_mandir}/man1/xmllint.1*
%if !0%{?os2_version}
%{_bindir}/xmlcatalog
%else
%{_bindir}/xmlcatalog.exe
%endif
%{_mandir}/man1/xmlcatalog.1*

%files devel
%doc doc/*.html doc/html doc/*.gif doc/*.png
%doc doc/tutorial doc/libxml2-api.xml.gz
%doc doc/examples
%dir %{_datadir}/gtk-doc
%dir %{_datadir}/gtk-doc/html
%{_datadir}/gtk-doc/html/libxml2/
%if !0%{?os2_version}
%{_libdir}/libxml2.so
%else
%{_libdir}/xml2*_dll.a
%endif
%{_libdir}/xml2Conf.sh
%{_includedir}/libxml2/
%{_bindir}/xml2-config
%{_mandir}/man1/xml2-config.1*
%{_datadir}/aclocal/libxml.m4
%{_libdir}/pkgconfig/libxml-2.0.pc
%{_libdir}/cmake/libxml2/

%files static
%license Copyright
%if !0%{?os2_version}
%{_libdir}/libxml2.a
%else
%{_libdir}/xml2.a
%endif

%files -n python2-%{name}
%doc python/TODO python/libxml2class.txt
%doc doc/*.py doc/python.html
%{python2_sitearch}/libxml2.py*
%{python2_sitearch}/drv_libxml2.py*
%if !0%{?os2_version}
%{python2_sitearch}/libxml2mod.so
%else
%{python2_sitearch}/libxml2mod.pyd
%{python2_sitearch}/xml2mod.dll
%endif

%files -n python3-%{name}
%doc python/TODO python/libxml2class.txt
%doc doc/*.py doc/python.html
%{python3_sitearch}/libxml2.py
%if !0%{?os2_version}
%{python3_sitearch}/__pycache__/libxml2.*
%endif
%{python3_sitearch}/drv_libxml2.py
%if !0%{?os2_version}
%{python3_sitearch}/__pycache__/drv_libxml2.*
%endif
%if !0%{?os2_version}
%{python3_sitearch}/libxml2mod.so
%else
%{python3_sitearch}/libxml2mod.pyd
%{python3_sitearch}/xml2mod.dll
%endif

%changelog
* Fri Jan 14 2022 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.9.10-2
- enable python3
- resync with fedora spec

* Wed Apr 22 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.9.10-1
- update to vendor version 2.9.10
- enable icu support

* Mon Feb 17 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.9.9-2
- fixed libxslt ticket #1 (enable loading of symbols with _)

* Wed Feb 12 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.9.9-1
- update to vendor version 2.9.9

* Fri Jan 18 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.9.8-2
- enable file:// with drive letters

* Thu Jul 26 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.9.8-1
- update to vendor version 2.9.8
- moved source to github

* Thu May 04 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.9.4-3
- prefix /etc path with /@unixroot
- use the new scm_source and scm_setup macros

* Wed Nov 30 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.9.4-2
- add -nostdlib to forwarders, to need less heap

* Fri Nov 25 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.9.4-1
- update to version 2.9.4
- adjust to the current toolchain
- build and install the python binding within this spec as well

* Mon Apr 07 2014 yd
- build for python 2.7.
- added debug package with symbolic info for exceptq.

* Mon Jan 16 2012 yd
- rebuild with libc 0.6.4 runtime.
