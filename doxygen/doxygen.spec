# set this to 1 to enable
%global with_docs 0
%global with_latex 0
%global xapian_core_support OFF


Summary: A documentation system for C/C++
Name:    doxygen
Version: 1.8.15
Release: 1%{?dist}

# No version is specified.
License: GPL+
Url: http://www.doxygen.nl
Vendor: bww bitwise works GmbH
%scm_source  github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2

BuildRequires: %{_bindir}/python2

BuildRequires: gcc perl
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
BuildRequires: graphviz
%endif
BuildRequires: ghostscript
BuildRequires: gettext
BuildRequires: flex
BuildRequires: bison
BuildRequires: cmake
%if %{xapian_core_support} == "ON"
BuildRequires: xapian-core-devel
BuildRequires: zlib-devel
%endif
Requires: perl
#Requires: graphviz

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

%if %{with_latex}
%package latex
Summary: Support for producing latex/pdf output from doxygen
Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: tex(latex)
Requires: tex(multirow.sty)
Requires: tex(sectsty.sty)
Requires: tex(tocloft.sty)
Requires: tex(xtab.sty)
Requires: tex(import.sty)
Requires: tex(tabu.sty)
Requires: tex(appendix.sty)
Requires: tex(newunicodechar.sty)
Requires: texlive-epstopdf-bin	

%description latex
%{summary}.
%endif

%debug_package


%prep
%scm_setup


%build
export LDFLAGS="-Zhigh-mem -Zomf -lcx"
export VENDOR="%{vendor}"

mkdir -p %{_build}
cd %{_build}
#      -DBUILD_SHARED_LIBS=OFF \
%cmake \
%if %{with_docs}
      -Dbuild_doc=ON \
%lse
      -Dbuild_doc=OFF \
%endif
      -Dbuild_wizard=ON \
      -Dbuild_xmlparser=ON \
      -Dbuild_search=%{xapian_core_support} \
      -DMAN_INSTALL_DIR=%{_mandir}/man1 \
      -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
      ..
cd ..

%if %{with_docs}
make docs -C %{_build}
%endif
make -C %{_build}


%install
make install DESTDIR=%{buildroot} -C %{_build}

# install man pages
mkdir -p %{buildroot}/%{_mandir}/man1
cp doc/*.1 %{buildroot}/%{_mandir}/man1/

%if %{xapian_core_support} == "OFF"
rm -f %{buildroot}/%{_mandir}/man1/doxyindexer.1* %{buildroot}/%{_mandir}/man1/doxysearch.1*
%endif

# remove duplicate
rm -rf %{buildroot}/%{_docdir}/packages

%check
#still disabled as we dont have bibtext tools. and one test needs it
#make tests -C %{_build}

%files
%doc LANGUAGE.HOWTO README.md
%license LICENSE
%if %{with_docs}
%if %{xapian_core_support} == "ON"
%{_bindir}/doxyindexer.exe
%{_bindir}/doxysearch*
%exclude %{_bindir}/*.dbg
%endif
%endif
%{_bindir}/doxygen.exe
%{_mandir}/man1/doxygen.1*
%if %{xapian_core_support} == "ON"
%{_mandir}/man1/doxyindexer.1*
%{_mandir}/man1/doxysearch.1*
%endif


%files doxywizard
%{_bindir}/doxywizard.exe
%{_mandir}/man1/doxywizard*

%if %{with_latex}
%files latex
# intentionally left blank
%endif

%changelog
* Wed Jun 12 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.8.15-1
- move source to github
- use scm_ macros
- update to version 1.8.15

* Fri Jan 27 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.8.13-2
- add buildlevel to the exe

* Thu Jan 19 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.8.13-1
- fix doxywizzard rpm
- update to version 1.8.13

* Tue Dec 13 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.8.12-1
- initial port
