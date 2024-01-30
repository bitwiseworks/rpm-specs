Name:           libxml2
Version:        2.12.4
Release:        1%{?dist}
Summary:        Library providing XML and HTML support

# list.c, dict.c and few others use ISC-Veillard
# the conformance and test suite data in
# Source1, Source2 and Source3 is covered by W3C
License:        MIT AND ISC-Veillard AND W3C
URL:            https://gitlab.gnome.org/GNOME/libxml2/-/wikis/home
%if !0%{?os2_version}
Source0:        https://download.gnome.org/sources/%{name}/2.12/%{name}-%{version}.tar.xz
# https://www.w3.org/XML/Test/xmlconf-20080827.html
Source1:        https://www.w3.org/XML/Test/xmlts20080827.tar.gz
# https://www.w3.org/XML/2004/xml-schema-test-suite/index.html
Source2:        https://www.w3.org/XML/2004/xml-schema-test-suite/xmlschema2002-01-16/xsts-2002-01-16.tar.gz
Source3:        https://www.w3.org/XML/2004/xml-schema-test-suite/xmlschema2004-01-14/xsts-2004-01-14.tar.gz
Patch0:         libxml2-multilib.patch
# Patch from openSUSE.
# See:  https://bugzilla.gnome.org/show_bug.cgi?id=789714
Patch1:         libxml2-2.12.0-python3-unicode-errors.patch
%else
%scm_source     github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2
Vendor:         bww bitwise works GmbH

# DEF files to create forwarders for the legacy package
Source10:       libxml2.def
%endif

BuildRequires:  cmake-rpm-macros
BuildRequires:  gcc
BuildRequires:  make
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
%if !0%{?os2_version}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       zlib-devel%{?_isa}
Requires:       xz-devel%{?_isa}
%else
Requires:       %{name} = %{version}-%{release}
Requires:       zlib-devel
Requires:       xz-devel
%endif

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

%package -n python3-%{name}
Summary:        Python 3 bindings for the libxml2 library
BuildRequires:  python3-devel
%if !0%{?os2_version}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%else
Requires:       %{name} = %{version}-%{release}
%endif
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
# see https://bugzilla.redhat.com/show_bug.cgi?id=2139546 , several
# of these options are needed to (mostly) retain ABI compatibility
# with earlier versions
%configure \
    --enable-static \
    --with-legacy \
    --with-ftp \
%if 0%{?os2_version}
    --enable-ipv6=no --with-icu \
%endif
    --with-python=%{__python3}
%make_build

%install
%make_install

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
gzip -9 -c doc/libxml2-api.xml > doc/libxml2-api.xml.gz

%if 0%{?os2_version}
# Generate & install forwarder DLLs.
gcc -Zomf -Zdll -nostdlib libxml2.def -l$RPM_BUILD_ROOT/%{_libdir}/xml22.dll -lend -o $RPM_BUILD_ROOT/%{_libdir}/libxml2.dll

# create a symlink for the python binding, as the dll itself is named xml2mod.dll
ln -s %{python3_sitearch}/xml2mod.dll $RPM_BUILD_ROOT%{python3_sitearch}/libxml2mod.pyd
%endif

%check
%if !0%{?os2_version}
# Tests require the XML conformance suite.
tar -xzvf %{SOURCE1}
%make_build check
rm -rf xmlconf
# Schema tests use the schema test suite.
cp %{SOURCE2} %{SOURCE3} xstc/
pushd xstc
mkdir Tests
%make_build tests
popd
# As the directory is copied to the devel subpackage, remove any build
# artifacts.
(cd doc/examples ; make clean ; rm -rf .deps Makefile)
%else
# PYTHON/tests/Makefile.am needs some changes to have all tests working
# once done, enable make check
#export BEGINLIBPATH=%{_builddir}/%{buildsubdir}/py3/.libs
%endif

%if !0%{?os2_version}
%ldconfig_scriptlets
%endif

%files
%license Copyright
%doc NEWS README.md
%if !0%{?os2_version}
%{_libdir}/libxml2.so.2*
%else
%{_libdir}/xml2*.dll
#forwarder dll
%{_libdir}/libxml2.dll
%endif
%if !0%{?os2_version}
%{_bindir}/xmlcatalog
%else
%{_bindir}/xmlcatalog.exe
%endif
%if !0%{?os2_version}
%{_bindir}/xmllint
%else
%{_bindir}/xmllint.exe
%endif
%{_mandir}/man1/xmlcatalog.1*
%{_mandir}/man1/xmllint.1*

%files devel
%doc doc/*.html
%doc doc/tutorial doc/libxml2-api.xml.gz
%doc doc/examples
%dir %{_datadir}/gtk-doc
%dir %{_datadir}/gtk-doc/html
%{_datadir}/aclocal/libxml.m4
%{_datadir}/gtk-doc/html/libxml2/
%{_includedir}/libxml2/
%if !0%{?os2_version}
%{_libdir}/libxml2.so
%else
%{_libdir}/xml2*_dll.a
%endif
%{_libdir}/pkgconfig/libxml-2.0.pc
%{_libdir}/cmake/libxml2/
%{_bindir}/xml2-config
%{_mandir}/man1/xml2-config.1*

%files static
%license Copyright
%if !0%{?os2_version}
%{_libdir}/libxml2.a
%else
%{_libdir}/xml2.a
%endif

%files -n python3-%{name}
%doc doc/*.py
%if !0%{?os2_version}
%{python3_sitearch}/libxml2mod.so
%else
%{python3_sitearch}/libxml2mod.pyd
%{python3_sitearch}/xml2mod.dll
%endif
%{python3_sitelib}/libxml2.py
%{python3_sitelib}/__pycache__/libxml2.*
%{python3_sitelib}/drv_libxml2.py
%{python3_sitelib}/__pycache__/drv_libxml2.*

%changelog
* Mon Jan 29 2024 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.12.4-1
- update to version 2.12.4
- remove python2 binding
- resync with fedora spec

* Tue Jan 18 2022 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.9.10-3
- provide a python-libxml2 for python2-libxml2

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
