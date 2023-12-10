Name:          tea
Version:       62.1.2
Release:       1%{?dist}
Summary:       A powerful and easy-to-use Qt4-based editor with many useful features for HTML, Docbook, and LaTeX editing
Group:         Graphical Desktop/Applications/Development
Vendor:        TeLLie OS2 forever
Distribution:  OS/2
Packager:      TeLLie 
URL:           http://semiletov.org/tea/
%if !0%{?os2_version}
Source:       http://downloads.sourceforge.net/project/tea-editor/tea-editor/%{version}/tea-%{version}.tar.bz2
%else
%scm_source github https://github.com/psemiletov/tea-qt master
%endif

License:       GPL
%if !0%{?os2_version}
# AUTOBUILDREQ-BEGIN
BuildRequires: glibc-devel
BuildRequires: libGL-devel
%else
BuildRequires: hunspell-devel
BuildRequires: qt5-qtbase-devel
BuildRequires: poppler-devel
BuildRequires: zlib-devel
BuildRequires: aspell-devel
%endif
## AUTOBUILDREQ-END
BuildRoot:     %{_tmppath}/%{name}-%{version}-root

%description
TEA is a powerful and easy-to-use Qt4-based editor with many useful features for HTML, Docbook, and LaTeX editing.
It features a small footprint, a tabbed layout engine, support for multiple encodings, code snippets, templates, customizable hotkeys,
an "open at cursor" function for HTML files and images, miscellaneous HTML tools, preview in external browser, string manipulation functions,
Morse-code tools, bookmarks, syntax highlighting, and more.

%debug_package

%prep
%scm_setup

%build
export LDFLAGS="-Zhigh-mem -Zomf -lcx"
export CFLAGS="-O2 -g -march=pentium4"
export CXXFLAGS="-O2 -g -march=pentium4"
export FFLAGS="-O2 -g -march=pentium4"
export FCFLAGS="-O2 -g -march=pentium4"

mkdir builder
cd builder

cmake -DCMAKE_INSTALL_PREFIX:PATH=/@unixroot/usr \
      -DCMAKE_SKIP_RPATH:BOOL=YES \
      -DCMAKE_BUILD_TYPE=release \
      -DUSE_ASPELL=ON \
      -DUSE_PRINTER=ON \
      -DUSE_PDF=ON \
      -DUSE_DJVU=ON \
      -Wno-dev ..

make %{?_smp_mflags}

%install  
%make_install INSTALL_ROOT=%{buildroot} DESTDIR=$RPM_BUILD_ROOT
mkdir -p %{buildroot}%{_bindir}
install -Dm 0755 builder/%{name}.exe %{buildroot}%{_bindir}
     
%files
%defattr(-,root,root)
%doc AUTHORS COPYING README.md NEWS NEWS-RU
%{_bindir}/tea.exe

%changelog
* Sat Dec 09 2023 Elbert Pol <elbert.pol@gmail.com> 62.1.2-1
- Updated to latest version

* Sun Nov 05 2023 Elbert Pol <elbert.pol@gmail.com> 62.1.0-1
- Updated to latest version

* Sun Nov 13 2022 Elbert Pol <elbert.pol@gmail.com> 62.0.1-1
- Updated to latest version

* Mon Oct 31 2022 Elbert Pol <elbert.pol@gmail.com> 61-2.0-1
- Updated to latest version
 
* Mon Sep 26 2022 Elbert Pol <elbert.pol@gmail.com> 61.1.0-1
- Updated to latest version.

* Fri Jul 22 2022 Elbert Pol <elbert.pol@gmail.com> 61.0.0-1
- Updated to latest version

* Wed Jan 19 2022 Elbert Pol <elbert.pol@gmail.com> 60-7.0-1
- Updated to latest version

* Tue Oct 19 2021 Elbert Pol <elbert.pol@gmail.com> 60-6.1-1
- Updated to latest version

* Thu Sep 30 2021 Elbert Pol <elbert.pol@gmail.com> 60-5.1-1
- Updated to latest version

* Thu Jul 15 2021 Elbert Pol <elbert.pol@gmail.com> 60.4.0-1
- Updated to latest version

* Thu Jun 03 2021 Elbert Pol <elbert.pol@gmail.com> 60.3.0-1
- Updated to latest version

* Thu May 06 2021 Elbert Pol <elbert.pol@gmail.com> 60.1.0-1
- Updated to latest version

* Mon Apr 12 2021 Elbert Pol <elbert.pol@gmail.com> 60.0.3-1
- Updated to latest version

* Tue Apr 06 2021 Elbert Pol <elbert.pol@gmail.com> 60.0.2-1
- Updated to latest version

* Sat Oct 03 2020 Elbert Pol <elbert.pol@gmail.com> 50.1.0-1
- Updated to latest source

* Thu Apr 02 2020 Elbert Pol <elbert.pol@gmail.com> 50.0.4-2
- Requirement from some files not needed and build with gcc 9.2.0
- Also fix some other definitions for OS2 

* Tue Dec 10 2019 Elbert Pol <elbert.pol@gmail.com> 50.0.4-1
- Updated to latest source
- Some more OS/2 fixes

* Sat Dec 07 2019 Elbert Pol <elbert.pol@gmail.com> 50.0.3-1
- Updated to latest source
- Some OS/2 fix

* Fri Nov 29 2019 Elbert Pol <elbert.pol@gmail.com> 50.0.0-1
- Updated to latest source

* Sun Sep 22 2019 Elbert Pol <elbert.pol@gmail.com> 48.0.0-1
- Updated to latest source

* Mon May 06 2019 Elbert Pol <elbert.pol@gmail.com> 47.1.0-1
- Updated to latest source

* Sun Dec 02 2018 Elbert Pol <elbert.pol@gmail.com> 47.0.0-1
- Update to latest source

* Sun Sep 30 2018 Elbert Pol <elbert.pol@gmail.com> 46.3.0-1
- Some OS2 fixes to enable PDF and DJVU
- First OS/2 rpm release
