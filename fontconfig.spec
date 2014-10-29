Summary:	Font configuration and customization library
Name:		fontconfig
Version:	2.8.0
Release:	2%{?dist}
# src/ftglue.[ch] is in Public Domain
# src/fccache.c contains Public Domain code
# fc-case/CaseFolding.txt is in the UCD
# otherwise MIT
License:	MIT and Public Domain and UCD
Group:		System Environment/Libraries
#Source:	http://fontconfig.org/release/%{name}-%{version}.tar.bz2
URL:		http://fontconfig.org
%define svn_url     http://svn.netlabs.org/repos/ports/fontconfig_os2/trunk
%define svn_rev     918
Source: %{name}-%{version}-r%{svn_rev}.zip

BuildRoot: %{tmpdir}/%{name}-%{version}-root-%(id -u -n)

BuildRequires:	freetype-devel >= 2.5.3
BuildRequires:  kbuild

Requires(pre):	freetype

%description
Fontconfig is designed to locate fonts within the
system and select them according to requirements specified by 
applications.

%package	devel
Summary:	Font configuration and customization library
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	freetype-devel >= 2.5.3
Requires:	pkgconfig

%description	devel
The fontconfig-devel package includes the header files,
and developer docs for the fontconfig package.

Install fontconfig-devel if you want to develop programs which 
will use fontconfig.


%prep
%if %(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')
%setup -q
%else
%setup -n "%{name}-%{version}" -Tc
svn export -r %{svn_rev} %{svn_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" "%{name}-%{version}")
%endif


%build
%define kmk_env \
    KMK_FLAGS="\
        KBUILD_VERBOSE=2 \
        BUILD_TYPE=release \
        NIX_INST_DIR=%{_prefix}" \
    unset BUILD_PLATFORM

%{kmk_env}

cmd /c kmk $KMK_FLAGS


%install
%{kmk_env}

rm -rf "%{buildroot}"

cmd /c kmk $KMK_FLAGS PATH_INS="%{buildroot}/%{_prefix}" install
emximp -o %{buildroot}/%{_libdir}/fontconfig_dll.a %{buildroot}/%{_libdir}/fontconfig.lib
rm %{buildroot}/%{_libdir}/*.lib

%clean
rm -rf "%{buildroot}"


%files
%defattr(-,root,root)
#%doc README AUTHORS COPYING
%{_libdir}/fntcfg2.dll


%files devel
%defattr(-,root,root)
%{_libdir}/fontconfig*.a
%{_libdir}/pkgconfig/*
%{_includedir}/fontconfig


%changelog
* Wed Oct 28 2014 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.8.0-2
- build with svn source now

* Mon Oct 6 2014 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.8.0-1
- first public version
