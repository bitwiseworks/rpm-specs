# Note: this .spec is borrowed from fontconfig-2.11.94-5.fc24.src.rpm

# OS/2 rpm macros don't define this (yet), do it manually:
%global _fontconfig_masterdir %{_sysconfdir}/fonts
%global _fontconfig_confdir %{_sysconfdir}/fonts/conf.d
%global _fontconfig_templatedir %{_datadir}/fontconfig/conf.avail

%global freetype_version 2.1.4

Summary:	Font configuration and customization library
Name:		fontconfig
Version:	2.11.94
Release:	2%{?dist}
# src/ftglue.[ch] is in Public Domain
# src/fccache.c contains Public Domain code
# fc-case/CaseFolding.txt is in the UCD
# otherwise MIT
License:	MIT and Public Domain and UCD
Group:		System Environment/Libraries
#Source:		http://fontconfig.org/release/%{name}-%{version}.tar.bz2
URL:		http://fontconfig.org

%define svn_url     http://svn.netlabs.org/repos/ports/fontconfig/trunk
%define svn_rev     1221

Source: %{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip

BuildRequires: gcc make subversion zip

BuildRequires:	expat-devel%{?aaa:bbb:ccc}
BuildRequires:	freetype-devel >= %{freetype_version}
#BuildRequires:	fontpackages-devel
BuildRequires:	autoconf automake libtool
BuildRequires:	python python-lxml

#Requires:	fontpackages-filesystem
Requires(pre):	freetype
Requires(post):	grep coreutils
#Requires:	font(:lang=en)

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

%description	devel
The fontconfig-devel package includes the header files,
and developer docs for the fontconfig package.

Install fontconfig-devel if you want to develop programs which
will use fontconfig.

# @todo temporarily disable docs until we got docbook-utils (which needs jade etc.)

#%package	devel-doc
#Summary:	Development Documentation files for fontconfig library
#Group:		Documentation
#BuildArch:	noarch
#Requires:	%{name}-devel = %{version}-%{release}
#
#%description	devel-doc
#The fontconfig-devel-doc package contains the documentation files
#which is useful for developing applications that uses fontconfig.

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

# Generate configure and friends
NOCONFIGURE=1 autogen.sh

%build
# We don't want to rebuild the docs, but we want to install the included ones.
export HASDOCBOOK=no

CFLAGS="%{optflags}" \
LDFLAGS="-Zhigh-mem" \
%configure \
        --with-add-fonts=%{_prefix}/local/share/fonts,%{_datadir}/fonts \
        --disable-static

make %{?_smp_mflags} V=1

%install
rm -rf "$RPM_BUILD_ROOT"
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# move installed doc files back to build directory to package themm
# in the right place
# @todo docs mv $RPM_BUILD_ROOT%{_docdir}/fontconfig/* .
# @todo docs rmdir $RPM_BUILD_ROOT%{_docdir}/fontconfig/

%check
# @todo Some tests will fail if there is no working system config (upstream bug)
if [ -f "%{_fontconfig_masterdir}/fonts.conf" ] ; then
make check
fi

%post
#/sbin/ldconfig

umask 0022

mkdir -p %{_localstatedir}/cache/fontconfig

# Force regeneration of all fontconfig cache files
%{_bindir}/fc-cache -f

#%postun -p /sbin/ldconfig

#%transfiletriggerin -- %{_prefix}/local/share/fonts %{_datadir}/fonts
#%{_bindir}/fc-cache -s

#%transfiletriggerpostun -- %{_prefix}/local/share/fonts %{_datadir}/fonts
#%{_bindir}/fc-cache -s

%files
%doc README AUTHORS COPYING
# @todo docs %doc fontconfig-user.txt fontconfig-user.html
%doc %{_fontconfig_confdir}/README
%{_libdir}/fntcnf*.dll
%{_bindir}/fc-cache.exe
%{_bindir}/fc-cat.exe
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
# @todo docs %{_mandir}/man1/*
# @todo docs %{_mandir}/man5/*

%files devel
%{_libdir}/fontconfig*.a
%{_libdir}/pkgconfig/*
%{_includedir}/fontconfig
# @todo %{_mandir}/man3/*

# @todo docs %files devel-doc
# @todo docs %doc fontconfig-devel.txt fontconfig-devel

%changelog
* Tue Mar 1 2016 Dmitriy Kuminov <coding@dmik.org> 2.11.94-2
- Allow loading DLL into high memory.

* Mon Dec 14 2015 Dmitriy Kuminov <coding@dmik.org> 2.11.94-1
- Initial package for version 2.11.94.
