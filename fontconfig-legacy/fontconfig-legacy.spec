Summary:	Font configuration and customization library
Name:		fontconfig-legacy
Version:	2.11.94
Release:	1%{?dist}
# src/ftglue.[ch] is in Public Domain
# src/fccache.c contains Public Domain code
# fc-case/CaseFolding.txt is in the UCD
# otherwise MIT
License:	MIT and Public Domain and UCD
Group:		System Environment/Libraries
#Source:	http://fontconfig.org/release/%{name}-%{version}.tar.bz2
URL:		http://fontconfig.org

%define svn_url     http://svn.netlabs.org/repos/ports/fontconfig_os2/trunk
%define svn_rev     1188

Source: %{name}-%{version}-r%{svn_rev}.zip

BuildRequires: gcc make subversion zip

BuildRequires:	freetype-devel >= 2.5.3
BuildRequires:  kbuild

Requires(pre):	freetype

# fontconfig-legacy used to be fontconfig before 2.11.94 (fontconfig is now a different
# package containing the complete upstream version with a differnt DLL name).
Obsoletes:  fontconfig < 2.11.94

%description
Fontconfig is designed to locate fonts within the
system and select them according to requirements specified by
applications.

%package	devel
Summary:	Font configuration and customization library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	freetype-devel >= 2.5.3
Requires:	pkgconfig

Obsoletes:  fontconfig-devel < 2.11.94

%description	devel
The fontconfig-devel package includes the header files,
and developer docs for the fontconfig package.

Install fontconfig-devel if you want to develop programs which
will use fontconfig.

%debug_package


%prep
%if %(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')
%setup -q
%else
%setup -n "%{name}-%{version}" -Tc
svn export -r %{svn_rev} %{svn_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" "%{name}-%{version}")
%endif


%define kmk_env \
    KMK_FLAGS="\
        KBUILD_VERBOSE=2 \
        BUILD_TYPE=release \
        INST_PREFIX=%{_prefix}"


%build

%{kmk_env}

cmd /c kmk $KMK_FLAGS


%install
%{kmk_env}

rm -rf "%{buildroot}"

cmd /c kmk $KMK_FLAGS DESTDIR="%{buildroot}" install


%clean
rm -rf "%{buildroot}"


%files
%defattr(-,root,root)
#%doc README AUTHORS COPYING
%{_libdir}/fntcfg2.dll


%files devel
%defattr(-,root,root)
%{_libdir}/fontconfig*.lib
%{_libdir}/pkgconfig/*
%{_includedir}/fontconfig


%changelog
* Mon Dec 14 2015 Dmitriy Kuminov <coding@dmik.orgh> - 2.11.94-1
- Import version 2.11.94 and add many new exports.
- Complete support for many APIs (FcPattern*, FcStr*, FcLang*)
  which makes this version much closer to original fontconfig.
- Hard-code substitution of WarpSans with Workplace Sans.
- Makefiles cleanup.
- Rename package from fontconfig to fontconfig-legacy due to the OS/2
  release of the full version of the original fontconfig library.

* Wed Oct 28 2014 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.8.0-2
- build with svn source now

* Mon Oct 6 2014 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.8.0-1
- first public version
