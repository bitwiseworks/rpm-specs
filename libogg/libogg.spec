Summary:        The Ogg bitstream file format library
Name:           libogg
Epoch:          2
Version:        1.3.4
Release:        1%{?dist}
License:        BSD
URL:            http://www.xiph.org/

%scm_source github https://github.com/bitwiseworks/ogg-os2 %{version}-os2
Vendor:		bww bitwise works GmbH

BuildRequires:  gcc

%description
Libogg is a library for manipulating Ogg bitstream file formats.
Libogg supports both making Ogg bitstreams and getting packets from
Ogg bitstreams.


%package devel
Summary:        Files needed for development using libogg
Requires:       libogg = %{epoch}:%{version}-%{release}
Requires:       pkgconfig
Requires:       automake


%description devel
Libogg is a library used for manipulating Ogg bitstreams. The
libogg-devel package contains the header files and documentation
needed for development using libogg.


%package devel-docs
Summary:        Documentation for developing Ogg applications
BuildArch:      noarch


%description devel-docs
Documentation for developing applications with libogg


%debug_package


%prep
%scm_setup
autoreconf -fiv

%build
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"

sed -i "s|-O20|$RPM_OPT_FLAGS|" configure
sed -i "s|-ffast-math||" configure
%configure --disable-static

# Set BUILDLEVEL to be embedded to all DLLs built with Libtool.
export LT_BUILDLEVEL="@#%{vendor}:%{version}-%{release}#@##1## `LANG=C date +'%%d %%b %%Y %%H:%%M:%%S'`     `uname -n`::::0::"

make %{?_smp_mflags}


%install
make DESTDIR=$RPM_BUILD_ROOT install

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

mv $RPM_BUILD_ROOT%{_docdir}/%{name} __installed_docs


%if !0%{?os2_version}
%ldconfig_scriptlets
%endif


%files
%doc AUTHORS CHANGES COPYING README.md
%{_libdir}/ogg*.dll


%files devel
%dir %{_includedir}/ogg
%{_includedir}/ogg/ogg.h
%{_includedir}/ogg/os_types.h
%{_includedir}/ogg/config_types.h
%{_libdir}/*_dll.a
%{_libdir}/pkgconfig/ogg.pc
%{_datadir}/aclocal/ogg.m4


%files devel-docs
%doc __installed_docs/*


%changelog
* Fri May 01 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.3.4-1
- updated to latest source
- moved the source to github.com/bitwiseworks
- added a debug package
- added a buildlevel to the dll

* Thu Mar 05 2019 Elbert Pol <elbert.pol@gmail.com> 1.3.3-3
- Change to right version

* Mon Mar 04 2019 Elbert Pol <elbert.pol@gmail.com> 1.3.3-2
- Switch back to Fedora orginal spec file

* Fri Mar 01 2019 Elbert Pol <elbert.pol@gmail.com> 1.3.3-1
- update to 1.3.3

* Tue Mar 15 2016 Valery V.Sedletski <_valerius@mail.ru> - 1.3.2-1
- Initial OS/2 packaging
