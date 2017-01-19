#define svn_url     e:/trees/doxygen/trunk
%define svn_url     http://svn.netlabs.org/repos/ports/doxygen/trunk
%define svn_rev     1937

# set this to 1 to enable
%global with_docs 0
%global with_search 0


Summary: A documentation system for C/C++
Name:    doxygen
Version: 1.8.13
Release: 1%{?dist}

# No version is specified.
License: GPL+
Url: http://www.stack.nl/~dimitri/doxygen/index.html
Vendor: bww bitwise works GmbH
Source: %{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip


BuildRequires: perl
%if %{with_docs}
BuildRequires: tex(dvips)
BuildRequires: tex(latex)
BuildRequires: tex(multirow.sty)
BuildRequires: tex(sectsty.sty)
BuildRequires: tex(tocloft.sty)
BuildRequires: tex(xtab.sty)
BuildRequires: tex(import.sty)
BuildRequires: tex(tabu.sty)
BuildRequires: tex(appendix.sty)
BuildRequires: /@unixroot/usr/bin/epstopdf
BuildRequires: texlive-epstopdf
%endif
BuildRequires: ghostscript
BuildRequires: gettext
BuildRequires: flex
BuildRequires: bison
BuildRequires: cmake
#BuildRequires: graphviz
%if %{with_search}
BuildRequires: xapian-core-devel
%endif
Requires: perl

%description
Doxygen can generate an online class browser (in HTML) and/or a
reference manual (in LaTeX) from a set of documented source files. The
documentation is extracted directly from the sources. Doxygen can
also be configured to extract the code structure from undocumented
source files.

%package doxywizard
Summary: A GUI for creating and editing configuration files
Requires: %{name} = %{version}-%{release}
BuildRequires: libqt4-devel
%description doxywizard
Doxywizard is a GUI for creating and editing configuration files that
are used by doxygen.


%debug_package


%prep
%if %{?svn_rev:%(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')}%{!?svn_rev):0}
%setup -q
%else
%setup -n "%{name}-%{version}" -Tc
svn export %{?svn_rev:-r %{svn_rev}} %{svn_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip" "%{name}-%{version}")
%endif


%build
export LDFLAGS="-Zhigh-mem -Zomf -lcx"

mkdir -p build
cd build
#      -DBUILD_SHARED_LIBS=OFF \
%cmake \
      -Dbuild_wizard=ON \
      -Dbuild_xmlparser=ON \
      -DMAN_INSTALL_DIR=%{_mandir}/man1 \
      -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
%if %{with_docs}
      -Dbuild_doc=ON \
%endif
%if %{with_search}
      -Dbuild_search=ON \
%endif
      ..
cd ..

%if %{with_docs}
make docs -C build
%endif
make -C build


%install
make install DESTDIR=%{buildroot} -C build

# install man pages
%if %{with_docs}
mkdir -p %{buildroot}/%{_mandir}/man1
cp doc/*.1 %{buildroot}/%{_mandir}/man1/
%endif

# remove duplicate
rm -rf %{buildroot}/%{_docdir}/packages


%files
%doc LANGUAGE.HOWTO README.md
%if %{with_docs}
%doc build/latex/doxygen_manual.pdf
%doc build/html
%endif
%{_bindir}/doxygen.exe
%if %{with_docs}
%{_bindir}/doxyindexer.exe
%{_bindir}/doxysearch*.cgi
%endif
%if %{with_docs}
%{_mandir}/man1/doxygen.1*
%{_mandir}/man1/doxyindexer.1*
%{_mandir}/man1/doxysearch.1*
%endif


%files doxywizard
%{_bindir}/doxywizard.exe
%if %{with_docs}
%{_mandir}/man1/doxywizard*
%endif


%changelog
* Tue Jan 19 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.8.13-1
- fix doxywizzard rpm
- update to version 1.8.13

* Tue Dec 13 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.8.12-1
- initial port
