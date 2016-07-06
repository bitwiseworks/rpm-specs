#define svn_url     F:/rd/ports/glib/trunk
%define svn_url     http://svn.netlabs.org/repos/ports/glib/trunk
%define svn_rev     1643

Name:           glib2
%define _name glib
Version:        2.33.12
Release:        2%{?dist}
License:        LGPLv2.1+
Summary:        A Library with Convenient Functions Written in C
Url:            http://www.gtk.org/
Group:          Development/Libraries/C and C++
Vendor:         bww bitwise works GmbH

Source: %{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip
Source1: glib2-legacy.zip

BuildRequires: gcc make subversion zip

BuildRequires: autoconf automake
BuildRequires: libtool > 2.4.5

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

%package -n libgio-2_0-0
License:        LGPLv2.1+
Summary:        A Library with Convenient Functions Written in C
Group:          Development/Libraries/C and C++
# Temporarily disable this, pending further discussion
# Recommends:     gvfs

%description -n libgio-2_0-0
This library provides convenient functions, such as lists and hashes,
to a C programmer and is used by Gtk+ and GNOME.

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

%package legacy
Summary: The 2.25 glib2 library.

%description legacy
The 2.25 glib2 library.

%debug_package

# @todo (dmik) We don't support this macro, put language files into the main package
#%lang_package

%prep
%if %{?svn_rev:%(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')}%{!?svn_rev):0}
%setup -q
%else
%setup -n "%{name}-%{version}" -Tc -a 1
svn export %{?svn_rev:-r %{svn_rev}} %{svn_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip" "%{name}-%{version}")
%endif

cat > gtk-doc.make <<EOF
EXTRA_DIST =
CLEANFILES =
EOF
touch README INSTALL

autoreconf -fi

%build
export LDFLAGS="-Zbin-files -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export CFLAGS="%optflags -I/@unixroot/usr/include/bind9"
export LIBS="-lurpo -lmmap -lpthread -llwres"
%configure \
        --disable-modular-tests \
        --enable-shared --disable-static

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

rm $RPM_BUILD_ROOT%{_libdir}/charset.alias

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

# copy legacy files
cp -p gio2.dll %{buildroot}%{_libdir}
cp -p glib2.dll %{buildroot}%{_libdir}
cp -p gmod2.dll %{buildroot}%{_libdir}
cp -p gobj2.dll %{buildroot}%{_libdir}
cp -p gthr2.dll %{buildroot}%{_libdir}

%find_lang %{_name}20
#%fdupes $RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{_name}20.lang
%defattr(-,root,root)
%doc AUTHORS COPYING README NEWS ChangeLog
#/etc/profile.d/zzz-glib2.*
#/sbin/conf.d/SuSEconfig.glib2
%{_bindir}/gio-querymodules*
%{_datadir}/bash-completion/completions/*

#%files branding-upstream
#%defattr(-,root,root)
#%config (noreplace) %{_sysconfdir}/gnome_defaults.conf

%files -n libglib-2_0-0
%defattr(-, root, root)
%{_libdir}/glib*.dll
%exclude %{_libdir}/*2.dll

%files -n libgmodule-2_0-0
%defattr(-, root, root)
%{_libdir}/gmod*.dll
%exclude %{_libdir}/*2.dll

%files -n libgobject-2_0-0
%defattr(-, root, root)
%{_libdir}/gobj*.dll
%exclude %{_libdir}/*2.dll

%files -n libgthread-2_0-0
%defattr(-, root, root)
%{_libdir}/gthr*.dll
%exclude %{_libdir}/*2.dll

%files -n libgio-2_0-0
%defattr(-, root, root)
%{_libdir}/gio*.dll
%exclude %{_libdir}/*2.dll
#%dir %{_libdir}/gio
#%dir %{_libdir}/gio/modules
#%ghost %{_libdir}/gio/modules/giomodule.cache
##%{_datadir}/applications/defaults.list
#%dir %{_localstatedir}/cache/gio-2.0
#%ghost %{_localstatedir}/cache/gio-2.0/defaults.list

#%files -n libgio-fam
#%defattr(-,root,root)
#%{_libdir}/gio/modules/libgiofam.so

%files devel
%defattr(-,root,root)
%{_bindir}/glib-*
%{_bindir}/gobject-*
%{_bindir}/gtester*
%{_bindir}/gresource*
%{_bindir}/gsettings*
%{_bindir}/gdbus*
#%doc %{_mandir}/man?/glib-*.*
#%doc %{_mandir}/man?/gobject-*.*
#%doc %{_mandir}/man?/gtester*.*
%{_datadir}/aclocal/*.m4
%{_datadir}/glib-2.0
%{_includedir}/glib-2.0
%{_includedir}/gio-unix-2.0
%{_libdir}/*.a
%{_libdir}/glib-2.0
%{_libdir}/pkgconfig/*.pc
%{_libdir}/gdbus-2.0/*
#%{_datadir}/gtk-doc/html/gio
#%{_datadir}/gtk-doc/html/glib
#%{_datadir}/gtk-doc/html/gobject
#%{_datadir}/gdb/auto-load/%{_libdir}/*-gdb.py
%{_datadir}/gdb/auto-load/*
# Own these directories to not depend on gtk-doc while building:
#%dir %{_datadir}/gtk-doc
#%dir %{_datadir}/gtk-doc/html
# Own these directories to not depend on gdb
%dir %{_datadir}/gdb
%dir %{_datadir}/gdb/auto-load
#%dir %{_datadir}/gdb/auto-load/%{_prefix}
#%dir %{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}

%files legacy
%defattr(-,root,root)
%{_libdir}/*2.dll

%changelog
* Tue Jul 05 2016 yd <yd@os2power.com> 2.33.12-2
- r1643, use gettext code to embed codepage aliases. ticket#14.

* Sat Jun 18 2016 yd <yd@os2power.com> 2.33.12-1
- r1605, use ISO8859-1 as default mapping, added _EURO locales.
- add legacy package for 2.25 compatibility.
- build public version.

* Wed Jan 27 2016 Dmitriy Kuminov <coding@dmik.org> 2.25.15-5
- Remove .la files from distribution.
- Build with gcc-4.9.2 against libc-0.6.6.
- Switch to downloading sources from SVN.

* Wed Jul 18 2012 yd
- include Dmitry's changes for OpenJDK build.
