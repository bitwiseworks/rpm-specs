# Note: this .spec is borrowed from git://pkgs.fedoraproject.org/rpms/fontconfig.git

# OS/2 rpm macros don't define this (yet), do it manually:
%global _fontconfig_masterdir %{_sysconfdir}/fonts
%global _fontconfig_confdir %{_sysconfdir}/fonts/conf.d
%global _fontconfig_templatedir %{_datadir}/fontconfig/conf.avail

%global freetype_version 2.10.0

Summary:	Font configuration and customization library
Name:		fontconfig
Version:	2.13.1
Release:	1%{?dist}
# src/ftglue.[ch] is in Public Domain
# src/fccache.c contains Public Domain code
# fc-case/CaseFolding.txt is in the UCD
# otherwise MIT
License:	MIT and Public Domain and UCD
Group:		System Environment/Libraries
URL:		http://fontconfig.org
Vendor:		bww bitwise works GmbH
%scm_source     github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2

Source1: 30-os2-unsupported.conf
Source2: 80-os2-tnr-fix.conf

BuildRequires:	expat-devel
BuildRequires:	freetype-devel >= %{freetype_version}
#BuildRequires:	fontpackages-devel
BuildRequires:	autoconf automake libtool gettext
#BuildRequires:	gperf

#Requires:	fontpackages-filesystem
Requires:	freetype
Requires(pre):	freetype >= 2.10.0
Requires(post):	grep coreutils
#Requires:	font(:lang=en)
#Sugests:        dejavu-sans-fonts

# @todo Temporary enforce dependency on the legacy package (that was previously named
# fontconfig) to have it installed. This should be dropped at some point.
Requires: fontconfig-legacy

%description
Fontconfig is designed to locate fonts within the
system and select them according to requirements specified by
applications.

%package	devel
Summary:	Font configuration and customization library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	freetype-devel >= %{freetype_version}
Requires:	pkgconfig
Requires:	gettext

%description	devel
The fontconfig-devel package includes the header files,
and developer docs for the fontconfig package.

Install fontconfig-devel if you want to develop programs which
will use fontconfig.


%package	devel-doc
Summary:	Development Documentation files for fontconfig library
Group:		Documentation
BuildArch:	noarch
Requires:	%{name}-devel = %{version}-%{release}

%description	devel-doc
The fontconfig-devel-doc package contains the documentation files
which is useful for developing applications that uses fontconfig.

%debug_package

%prep
%scm_setup

%build
# We don't want to rebuild the docs, but we want to install the included ones.
export HASDOCBOOK=no
export CFLAGS="%{optflags}"
export LDFLAGS="-Zomf -Zhigh-mem"
export LIBS="-lcx"
export VENDOR="%{vendor}"

# Generate configure and friends
autoreconf -fvi

%configure \
        --with-add-fonts=%{_prefix}/local/share/fonts,%{_datadir}/fonts \
        --disable-static

make %{?_smp_mflags} V=1

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# install OS/2-specific configs and activate them
install -p -m 0644 %{SOURCE1} %{SOURCE2} $RPM_BUILD_ROOT%{_fontconfig_templatedir}/
ln -s %{_fontconfig_templatedir}/30-os2-unsupported.conf $RPM_BUILD_ROOT%{_fontconfig_confdir}/
ln -s %{_fontconfig_templatedir}/80-os2-tnr-fix.conf $RPM_BUILD_ROOT%{_fontconfig_confdir}/

# move installed doc files back to build directory to package them
# in the right place
mv $RPM_BUILD_ROOT%{_docdir}/fontconfig/* .
rmdir $RPM_BUILD_ROOT%{_docdir}/fontconfig/

%find_lang %{name}
%find_lang %{name}-conf
cat %{name}-conf.lang >> %{name}.lang

%check
# @todo Some tests will fail if there is no working system config (upstream bug)
if [ -f "%{_fontconfig_masterdir}/fonts.conf" ] ; then
# this export is needed, as else the dll for the tests are not found
export BEGINLIBPATH=%{_builddir}/%{buildsubdir}/src/.libs
#make check
fi

%post
#%{?ldconfig}

umask 0022

mkdir -p %{_localstatedir}/cache/fontconfig

# Force regeneration of all fontconfig cache files
rm -rf %{_localstatedir}/cache/fontconfig/*
BEGINLIBPATH="$(echo %{_libdir} | sed -re 's,/@unixroot,'$UNIXROOT',g' -e 's,/,\\,g');$BEGINLIBPATH" \
LIBPATHSTRICT=T \
%{_bindir}/fc-cache -f

%postun

#%transfiletriggerin -- %{_prefix}/local/share/fonts %{_datadir}/fonts
#%{_bindir}/fc-cache -s

#%transfiletriggerpostun -- %{_prefix}/local/share/fonts %{_datadir}/fonts
#%{_bindir}/fc-cache -s

%files -f %{name}.lang
%doc README AUTHORS
%doc fontconfig-user.txt fontconfig-user.html
%doc %{_fontconfig_confdir}/README
%license COPYING
%{_libdir}/fntcnf*.dll
%{_bindir}/fc-cache.exe
%{_bindir}/fc-cat.exe
%{_bindir}/fc-conflist.exe
%{_bindir}/fc-list.exe
%{_bindir}/fc-match.exe
%{_bindir}/fc-pattern.exe
%{_bindir}/fc-query.exe
%{_bindir}/fc-scan.exe
%{_bindir}/fc-validate.exe
%{_fontconfig_templatedir}/*.conf
%{_datadir}/xml/fontconfig
# fonts.conf is not supposed to be modified.
# If you want to do so, you should use local.conf instead.
%config %{_fontconfig_masterdir}/fonts.conf
%config(noreplace) %{_fontconfig_confdir}/*.conf
%dir %{_localstatedir}/cache/fontconfig
%{_mandir}/man1/*
%{_mandir}/man5/*

%files devel
%{_libdir}/fontconfig*_dll.a
%{_libdir}/pkgconfig/*
%{_includedir}/fontconfig
%{_mandir}/man3/*
%{_datadir}/gettext/its/fontconfig.its
%{_datadir}/gettext/its/fontconfig.loc

%files devel-doc
%doc fontconfig-devel.txt fontconfig-devel

%changelog
* Fri May 24 2019 Silvan Scherrer <silvan.scherrer@aroa.com> 2.13.1-1
- update to version 2.13.1
- moved source to github
- adjusted spec according to fedora one

* Wed Aug 09 2017 Silvan Scherrer <silvan.scherrer@aroa.com> 2.12.4-1
- Update to version 2.12.4.
- use new scm_ macros
- fixes ticket #168, #169

* Fri Nov 25 2016 Silvan Scherrer <silvan.scherrer@aroa.com> 2.12.1-2
- add buildlevel information to the dll

* Tue Oct 25 2016 Silvan Scherrer <silvan.scherrer@aroa.com> 2.12.1-1
- Update to version 2.12.1.

* Sat Apr 23 2016 Dmitriy Kuminov <coding@dmik.org> 2.11.95-1
- Update to version 2.11.95.
- Fix selecting Type 1 fonts from OS/2 PM font registry.
- Add aliases for system OS/2 fonts not reconginzed by FreeType
  (this includes Tms Rmn, Helv and Times New Roman MT 30).
- Remove trailing space from Times New Roman Type 1 system font.
- Temporarily disable assertions that sometimes abort Firefox at exit.

* Tue Mar 1 2016 Dmitriy Kuminov <coding@dmik.org> 2.11.94-2
- Allow loading DLL into high memory.

* Mon Dec 14 2015 Dmitriy Kuminov <coding@dmik.org> 2.11.94-1
- Initial package for version 2.11.94.
