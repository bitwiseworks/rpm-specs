#%%global nmu +nmu4

Name:		libpaper
Version:	1.1.28
Release:	1%{?dist}
Summary:	Library and tools for handling papersize
License:	GPLv2
URL:		http://packages.qa.debian.org/libp/libpaper.html
%if !0%{?os2_version}
Source0:	http://ftp.debian.org/debian/pool/main/libp/libpaper/%{name}_%{version}.tar.gz


# Filed upstream as:
# http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=481213
Patch2:		libpaper-useglibcfallback.patch
# Memory leak
Patch3:   libpaper-file-leak.patch
# memory leak found by covscan, reported to debian upstream
#Patch4: libpaper-covscan.patch
%else
Vendor:         bww bitwise works GmbH
%scm_source github http://github.com/bitwiseworks/%{name}-os2 v%{version}-os2
%endif


# gcc is no longer in buildroot by default
BuildRequires:  gcc
# use git for autosetup
BuildRequires:  git-core
# uses make
BuildRequires:  make
BuildRequires:	libtool, gettext, gawk

%description
The paper library and accompanying files are intended to provide a 
simple way for applications to take actions based on a system- or 
user-specified paper size. This release is quite minimal, its purpose 
being to provide really basic functions (obtaining the system paper name 
and getting the height and width of a given kind of paper) that 
applications can immediately integrate.

%package devel
Summary:	Headers/Libraries for developing programs that use libpaper
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains headers and libraries that programmers will need 
to develop applications which use libpaper.

%if 0%{?os2_version}
%debug_package
%endif

%prep
%if !0%{?os2_version}
%autosetup -S git
%else
%scm_setup
%endif
libtoolize

%build
touch AUTHORS NEWS
aclocal
autoheader
autoconf
automake -a
%if 0%{?os2_version}
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"
export LIBS="-lcx"
# Set BUILDLEVEL to be embedded to all DLLs built with Libtool.
export LT_BUILDLEVEL="@#%{vendor}:%{version}-%{release}#@##1## `LANG=C date +'%%d %%b %%Y %%H:%%M:%%S'`     `uname -n`::::0::"
%endif
%configure --disable-static
# Disable rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%if !0%{?os2_version}
%make_build
%else
make %{?_smp_mflags}
%endif

%install
%make_install
rm $RPM_BUILD_ROOT%{_libdir}/*.la
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
echo '# Simply write the paper name. See papersize(5) for possible values' > $RPM_BUILD_ROOT%{_sysconfdir}/papersize
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/libpaper.d
for i in cs da de es fr gl hu it ja nl pt_BR sv tr uk vi; do
	mkdir -p $RPM_BUILD_ROOT%{_datadir}/locale/$i/LC_MESSAGES/;
	msgfmt debian/po/$i.po -o $RPM_BUILD_ROOT%{_datadir}/locale/$i/LC_MESSAGES/%{name}.mo;
done
%find_lang %{name}

%if !0%{?os2_version}
%ldconfig_scriptlets
%endif

%files -f %{name}.lang
%doc ChangeLog README
%license COPYING
%config(noreplace) %{_sysconfdir}/papersize
%dir %{_sysconfdir}/libpaper.d
%if !0%{?os2_version}
%{_bindir}/paperconf
%{_libdir}/libpaper.so.1.1.2
%{_libdir}/libpaper.so.1
%else
%{_bindir}/paperconf.exe
%{_libdir}/paper*.dll
%endif
%{_sbindir}/paperconfig
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*

%files devel
%{_includedir}/paper.h
%if !0%{?os2_version}
%{_libdir}/libpaper.so
%else
%{_libdir}/paper*_dll.a
%endif
%{_mandir}/man3/*


%changelog
* Tue Dec 29 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.1.28-1
- update to vendor version 1.1.28
- resynced with fedora spec

* Tue Oct 11 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.1.24-1
- initial version
