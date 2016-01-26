

Name:           glib2
%define _name glib
Version:        2.25.15
Release:        5%{?dist}
License:        LGPLv2.1+
Summary:        A Library with Convenient Functions Written in C
Url:            http://www.gtk.org/
Group:          Development/Libraries/C and C++

%define svn_url     http://svn.netlabs.org/repos/ports/glib/trunk
%define svn_rev     508

Source: %{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip

BuildRequires: gcc make subversion zip

# @todo (dmik) later (see below about autogen.sh usage)
#BuildRequires: autoconf automake
## @todo (dmik) We need this for the moment, see #93
#BuildRequires: libtool = 2.4.2

#BuildRequires:  fam-devel
#BuildRequires:  fdupes
#BuildRequires:  gcc-c++
#BuildRequires:  pcre-devel
BuildRequires:  pkgconfig
#BuildRequires:  translation-update-upstream
BuildRequires:  zlib-devel
BuildRequires:  libffi-devel gettext-devel bind-devel
# For temporary %%posttrans script only.
#PreReq:         coreutils
#PreReq:         /bin/sed
#Requires:       %{name}-branding
#Requires:       %{name}-lang = %{version}
#
Provides:       glib2-doc = 2.19.6
Obsoletes:      glib2-doc < 2.19.6
# YD this must be added to force dll install
Requires:       libglib-2_0-0 = %{version}
Requires:       libgmodule-2_0-0 = %{version}
Requires:       libgthread-2_0-0 = %{version}
Requires:       libgobject-2_0-0 = %{version}

BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
This library provides convenient functions, such as lists and hashes,
to a C programmer and is used by Gtk+ and GNOME.

#%package branding-upstream
#License:        LGPLv2.1+
#Summary:        Definition of GNOME Default Applications
#Group:          Development/Libraries/C and C++
#Provides:       %{name}-branding = %{version}
#Conflicts:      otherproviders(%{name}-branding)
#Supplements:    packageand(%{name}:branding-upstream)
#BRAND: The /etc/gnome_defaults.conf allows to define arbitrary
#BRAND: applications as preferred defaults.
# NOTE: gnome_defaults is not an upstream feature, but a SuSE
# enhancement, but to conform branding conventions, the package is named
# as glib2-branding-upstream.

#%description branding-upstream
#This branding-style package sets default applications in GNOME in
#openSUSE.

This is a dumb package, which provides only upstream GNOME packages as
preferred defaults. You most probably don't want this package. You
probably want to install distribution default glib2-branding and prefer
distribution wise GNOME defaults.

%package devel
#'
License:        GPLv2+
Requires:       %{name} = %{version} pkgconfig
# glibc-devel
# Now require the subpackages too
Requires:       libglib-2_0-0 = %{version}
Requires:       libgmodule-2_0-0 = %{version}
#Requires:       libgio-2_0-0 = %{version}
Requires:       libgthread-2_0-0 = %{version}
Requires:       libgobject-2_0-0 = %{version}
Summary:        Include files and libraries mandatory for development
Group:          Development/Libraries/C and C++

%description devel
This package contains all necessary include files, libraries,
configuration files and development tools (with manual pages) needed to
compile and link applications using the glib library.

The glib library provides convenient functions, such as lists and
hashes, to a C programmer and is used by Gtk+ and GNOME.

%package -n libglib-2_0-0
License:        LGPLv2.1+
Summary:        A Library with Convenient Functions Written in C
Group:          Development/Libraries/C and C++
#Recommends:     %{name}-lang = %{version}

%description -n libglib-2_0-0
This library provides convenient functions, such as lists and hashes,
to a C programmer and is used by Gtk+ and GNOME.

%package -n libgmodule-2_0-0
License:        LGPLv2.1+
Summary:        A Library with Convenient Functions Written in C
Group:          Development/Libraries/C and C++

%description -n libgmodule-2_0-0
This library provides convenient functions, such as lists and hashes,
to a C programmer and is used by Gtk+ and GNOME.

#%package -n libgio-2_0-0
#License:        LGPLv2.1+
#Summary:        A Library with Convenient Functions Written in C
#Group:          Development/Libraries/C and C++
#
# Temporarily disable this, pending further discussion
# Recommends:     gvfs

#%description -n libgio-2_0-0
#This library provides convenient functions, such as lists and hashes,
#to a C programmer and is used by Gtk+ and GNOME.

#%package -n libgio-fam
#License:        LGPLv2.1+
#Summary:        A Library with Convenient Functions Written in C
#Group:          Development/Libraries/C and C++
# we need gio-querymodules in %post/%postun
#Requires(post): %{name}
#Requires(postun): %{name}
#Supplements:    packageand(libgio-2_0-0:fam)

#%description -n libgio-fam
#This library provides convenient functions, such as lists and hashes,
#to a C programmer and is used by Gtk+ and GNOME.

%package -n libgthread-2_0-0
License:        LGPLv2.1+
Summary:        A Library with Convenient Functions Written in C
Group:          Development/Libraries/C and C++
Requires:       %{name} = %{version}

%description -n libgthread-2_0-0
This library provides convenient functions, such as lists and hashes,
to a C programmer and is used by Gtk+ and GNOME.

%package -n libgobject-2_0-0
License:        LGPLv2.1+
Summary:        A Library with Convenient Functions Written in C
Group:          Development/Libraries/C and C++

%description -n libgobject-2_0-0
This library provides convenient functions, such as lists and hashes,
to a C programmer and is used by Gtk+ and GNOME.

# @todo (dmik) We don't support this macro, put language files into the main package
#%lang_package

%prep
%if %{?svn_rev:%(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')}%{!?svn_rev):0}
%setup -q
%else
%setup -n "%{name}-%{version}" -Tc
svn export %{?svn_rev:-r %{svn_rev}} %{svn_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip" "%{name}-%{version}")
%endif

# pick up m4 fix necessary for configure to work (remove when switched to that rev)
svn export  %{svn_url}/m4macros/glib-gettext.m4@892 m4macros/glib-gettext.m4 --force
# fix emxexp exports (r904), also to be removed
sed -e 's/:space:/[:space:]/g' configure.ac -i

# @todo (dmik) we can't use autogen.sh ATM because a newer trunk revison (2.33 with fixes) is necesary for that,
# also there are some problems with libtool (see #93) so we also can't use autoreconf -fvi (because we need the
# fixed ltmain.sh from SVN), and even when it finally works it will rename glib2.dll to glib200.dll so some
# -legacy package is necessary...
autoconf
## Generate configure and friends
#export NOCONFIGURE=1
#autogen.sh

%build
export CONFIG_SHELL="/@unixroot/usr/bin/sh.exe"
export LDFLAGS="-Zbin-files -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lurpo -lmmap -lpthread"
%configure \
        --enable-shared --disable-static

# YD fix extra CRLF after pass_all and execute it again (libtool hack breaks sed substitutions)
sed -i "s/pass_all/pass_all\'\n_os2_dummy_var=\'/" config.status
config.status

make OPT="$CFLAGS" %{?_smp_mflags}

%check
# make check does not work on x86_64. See http://bugzilla.gnome.org/show_bug.cgi?id=554969
# %{__make} %{?jobs:-j%jobs} check

%install
%makeinstall
#%if 0%{?suse_version} <= 1120
#%{__rm} %{buildroot}%{_datadir}/locale/en@shaw/LC_MESSAGES/*
#%endif
mkdir -p $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-%{version}
cp AUTHORS $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-%{version}
cp COPYING $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-%{version}
cp README $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-%{version}
cp NEWS $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-%{version}
cp ChangeLog $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-%{version}

cp glib/.libs/*.dll $RPM_BUILD_ROOT%{_libdir}
cp glib/.libs/*.lib $RPM_BUILD_ROOT%{_libdir}
cp gmodule/.libs/*.dll $RPM_BUILD_ROOT%{_libdir}
cp gmodule/.libs/*.lib $RPM_BUILD_ROOT%{_libdir}
cp gthread/.libs/*.dll $RPM_BUILD_ROOT%{_libdir}
cp gthread/.libs/*.lib $RPM_BUILD_ROOT%{_libdir}
cp gobject/.libs/*.dll $RPM_BUILD_ROOT%{_libdir}
cp gobject/.libs/*.lib $RPM_BUILD_ROOT%{_libdir}

rm $RPM_BUILD_ROOT%{_libdir}/charset.alias
rm $RPM_BUILD_ROOT%{_mandir}/man1/gdbus.1
rm $RPM_BUILD_ROOT%{_mandir}/man1/gio-querymodules.1
rm $RPM_BUILD_ROOT%{_mandir}/man1/gsettings.1

#install -D -m0644 glib2.sh $RPM_BUILD_ROOT/etc/profile.d/zzz-glib2.sh
#install -D -m0644 glib2.csh $RPM_BUILD_ROOT/etc/profile.d/zzz-glib2.csh
#install -D -m0755 SuSEconfig.glib2 $RPM_BUILD_ROOT/sbin/conf.d/SuSEconfig.glib2
#install -D -m0644 gnome_defaults.conf $RPM_BUILD_ROOT%{_sysconfdir}/gnome_defaults.conf
# default apps magic
#mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/cache/gio-2.0 $RPM_BUILD_ROOT%{_datadir}/applications
#touch $RPM_BUILD_ROOT%{_localstatedir}/cache/gio-2.0/defaults.list
#ln -s %{_localstatedir}/cache/gio-2.0/defaults.list $RPM_BUILD_ROOT%{_datadir}/applications/defaults.list
# fix some permission issue, but only if needed
#test ! -x $RPM_BUILD_ROOT/%{_bindir}/gtester-report
#chmod +x $RPM_BUILD_ROOT/%{_bindir}/gtester-report
# gio-querymodules magic
#%if "%{_lib}" == "lib64"
#mv $RPM_BUILD_ROOT%{_bindir}/gio-querymodules $RPM_BUILD_ROOT%{_bindir}/gio-querymodules-64
#%endif
#touch $RPM_BUILD_ROOT%{_libdir}/gio/modules/giomodule.cache
# remove files we don't care about
#rm $RPM_BUILD_ROOT%{_libdir}/gio/modules/libgiofam.*a
# We do not need the la files for 11.1 and newer
#%if %suse_version > 1100
rm $RPM_BUILD_ROOT%{_libdir}/*.la
#%endif
%find_lang %{_name}20
#%fdupes $RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{_name}20.lang
%defattr(-,root,root)
%doc AUTHORS COPYING README NEWS ChangeLog
#/etc/profile.d/zzz-glib2.*
#/sbin/conf.d/SuSEconfig.glib2
#%{_bindir}/gio-querymodules*

#%files branding-upstream
#%defattr(-,root,root)
#%config (noreplace) %{_sysconfdir}/gnome_defaults.conf

%files -n libglib-2_0-0
%defattr(-, root, root)
%{_libdir}/glib*.dll

%files -n libgmodule-2_0-0
%defattr(-, root, root)
%{_libdir}/gmod*.dll

%files -n libgobject-2_0-0
%defattr(-, root, root)
%{_libdir}/gobj*.dll

%files -n libgthread-2_0-0
%defattr(-, root, root)
%{_libdir}/gthr*.dll

#%files -n libgio-2_0-0
#%defattr(-, root, root)
#%{_libdir}/libgio*.so.*
#%dir %{_libdir}/gio
#%dir %{_libdir}/gio/modules
#%ghost %{_libdir}/gio/modules/giomodule.cache
##%{_datadir}/applications/defaults.list
#%dir %{_localstatedir}/cache/gio-2.0
#%ghost %{_localstatedir}/cache/gio-2.0/defaults.list

#%files -n libgio-fam
#%defattr(-,root,root)
#%{_libdir}/gio/modules/libgiofam.so

# @todo (dmik) We don't support this macro, put language files into the main package
#%files lang -f %{_name}20.lang

%files devel
%defattr(-,root,root)
%{_bindir}/glib-*
%{_bindir}/gobject-*
%{_bindir}/gtester*
%doc %{_mandir}/man?/glib-*.*
%doc %{_mandir}/man?/gobject-*.*
%doc %{_mandir}/man?/gtester*.*
%{_datadir}/aclocal/*.m4
%{_datadir}/glib-2.0
%{_includedir}/glib-2.0
#%{_includedir}/gio-unix-2.0
%{_libdir}/*.a
%{_libdir}/*.lib
%{_libdir}/glib-2.0
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gtk-doc/html/gio
%{_datadir}/gtk-doc/html/glib
%{_datadir}/gtk-doc/html/gobject
#%{_datadir}/gdb/auto-load/%{_libdir}/*-gdb.py
%{_datadir}/gdb/auto-load/*
# Own these directories to not depend on gtk-doc while building:
%dir %{_datadir}/gtk-doc
%dir %{_datadir}/gtk-doc/html
# Own these directories to not depend on gdb
%dir %{_datadir}/gdb
%dir %{_datadir}/gdb/auto-load
#%dir %{_datadir}/gdb/auto-load/%{_prefix}
#%dir %{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}

%changelog
* Wed Jan 27 2016 Dmitriy Kuminov <coding@dmik.org> 2.25.15-5
- Remove .la files from distribution.
- Build with gcc-4.9.2 against libc-0.6.6.
- Switch to downloading sources from SVN.

* Wed Jul 18 2012 yd
- include Dmitry's changes for OpenJDK build.
