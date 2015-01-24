#define svn_url     F:/rd/ports/gettext/trunk
%define svn_url     http://svn.netlabs.org/repos/ports/gettext/trunk
%define svn_rev     981

%bcond_with jar
%bcond_with java
%bcond_without check
%bcond_without git

Summary: GNU libraries and utilities for producing multi-lingual messages
Name: gettext
Version: 0.18.1.1
Release: 5%{?dist}
License: GPLv3+ and LGPLv2+
Group: Development/Tools
URL: http://www.gnu.org/software/gettext/
Source: %{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip
Source1: gettext-legacy-os2.zip

BuildRequires: autoconf >= 2.62
BuildRequires: automake
BuildRequires: libtool, bison
%if %{with java}
# libintl.jar requires gcj >= 4.3 to build
#BuildRequires: gcc-java, libgcj
# For javadoc
#BuildRequires: java-1.6.0-openjdk-devel
%if %{with jar}
#BuildRequires: %{_bindir}/fastjar
# require zip and unzip for brp-java-repack-jars
BuildRequires: zip, unzip
%endif
%endif
# need expat for xgettext on glade
#Buildrequires: expat-devel
# for po-mode.el
#BuildRequires: emacs
%if %{with git}
# for autopoint:
#BuildRequires: git
%endif
#BuildRequires: chrpath

Buildroot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Requires: gettext-libs = %{version}-%{release}

%description
The GNU gettext package provides a set of tools and documentation for
producing multi-lingual messages in programs. Tools include a set of
conventions about how programs should be written to support message
catalogs, a directory and file naming organization for the message
catalogs, a runtime library which supports the retrieval of translated
messages, and stand-alone programs for handling the translatable and
the already translated strings. Gettext provides an easy to use
library and tools for creating, using, and modifying natural language
catalogs and is a powerful and simple method for internationalizing
programs.


%package devel
Summary: Development files for %{name}
Group: Development/Tools
# autopoint is GPLv3+
License: LGPLv2+ and GPLv3+
Requires: %{name} = %{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}
# for autopoint
#Requires: git
Obsoletes: gettext-autopoint < 0.18.1.1-3
Provides: gettext-autopoint = %{version}-%{release}


%description devel
This package contains all development related files necessary for
developing or compiling applications/libraries that needs
internationalization capability. You also need this package if you
want to add gettext support for your project.


%package libs
Summary: Libraries for %{name}
Group: System Environment/Libraries
License: LGPLv2+

%description libs
This package contains libraries used internationalization support.


#%package -n emacs-%{name}
#Summary: Support for editing po files within GNU Emacs
#Group: Applications/Editors
#BuildArch: noarch
# help users find po-mode.el
#Provides: emacs-po-mode
#Requires: emacs(bin) >= %{_emacs_version}

#%description -n emacs-%{name}
#This package provides a major mode for editing po files within GNU Emacs.


#%package -n emacs-%{name}-el
#Summary: Elisp source files for editing po files within GNU Emacs
#Group: Applications/Editors
#BuildArch: noarch
#Requires: emacs-%{name} = %{version}-%{release}

#%description -n emacs-%{name}-el
#This package contains the Elisp source files for editing po files within GNU
#Emacs.


%package legacy
Summary: The old gettext library.

%description legacy
The old gettext library.


%package debug
Summary: HLL debug data for exception handling support.

%description debug
HLL debug data for exception handling support.


%prep
%if %{?svn_rev:%(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')}%{!?svn_rev):0}
%setup -q
%else
%setup -n "%{name}-%{version}" -Tc -a 1
echo %{svn_rev}
svn export %{?svn_rev:-r %{svn_rev}} %{svn_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip" "%{name}-%{version}")
%endif

%build
%if %{with java}
export JAVAC=gcj
%if %{with jar}
export JAR=fastjar
%endif
%endif

export LDFLAGS="-Zbin-files -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp" ; \
export LIBS="-lurpo -lmmap" ; \

autogen.sh --skip-gnulib --quick

%configure \
    --without-included-gettext --enable-nls \
    --without-included-libxml \
    --disable-csharp \
    --disable-java --disable-native-java\
    --disable-git \
    --disable-rpath \
    --enable-shared --disable-static

cd gettext-tools/gnulib-lib
make fcntl.h
cd ../..

make %{?_smp_mflags} %{?with_java:GCJFLAGS="-findirect-dispatch"}


%install
rm -rf %{buildroot}
#INSTALL="%{__install} -p"
make install DESTDIR=${RPM_BUILD_ROOT} \
    lispdir=%{_datadir}/emacs/site-lisp/gettext \
    aclocaldir=%{_datadir}/aclocal EXAMPLESFILES=""

rm -f ${RPM_BUILD_ROOT}%{_datadir}/gettext/archive.git.tar.gz

# OS/2 specific files
rm -f ${RPM_BUILD_ROOT}%{_libdir}/charset.alias
cp -p kintl.dll %{buildroot}%{_libdir}


# move gettext to /bin
#mkdir -p ${RPM_BUILD_ROOT}/bin
#mv ${RPM_BUILD_ROOT}%{_bindir}/gettext ${RPM_BUILD_ROOT}/bin
#ln -s ../../bin/gettext ${RPM_BUILD_ROOT}%{_bindir}/gettext

#install -pm 755 %SOURCE2 ${RPM_BUILD_ROOT}/%{_bindir}/msghack


# make preloadable_libintl.so executable
#chmod 755 ${RPM_BUILD_ROOT}%{_libdir}/preloadable_libintl.so

rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir

# doc relocations
for i in gettext-runtime/man/*.html; do
  rm ${RPM_BUILD_ROOT}%{_datadir}/doc/gettext/`basename $i`
done
rm -r ${RPM_BUILD_ROOT}%{_datadir}/doc/gettext/javadoc*

rm -rf ${RPM_BUILD_ROOT}%{_datadir}/doc/gettext/examples

rm -rf htmldoc
mkdir htmldoc
mv ${RPM_BUILD_ROOT}%{_datadir}/doc/gettext/* ${RPM_BUILD_ROOT}/%{_datadir}/doc/libasprintf/* htmldoc
rm -r ${RPM_BUILD_ROOT}%{_datadir}/doc/libasprintf
rm -r ${RPM_BUILD_ROOT}%{_datadir}/doc/gettext

## note libintl.jar does not build with gcj < 4.3
## since it would not be fully portable
%if %{with jar}
### this is no longer needed since examples not packaged
## set timestamp of examples ChangeLog timestamp for brp-java-repack-jars
#for i in `find ${RPM_BUILD_ROOT} examples -newer ChangeLog -type f -name ChangeLog`; do
#  touch -r ChangeLog  $i
#done
%else
# in case another java compiler is installed
rm -f ${RPM_BUILD_ROOT}%{_datadir}/%{name}/libintl.jar
%endif

rm -f ${RPM_BUILD_ROOT}%{_datadir}/%{name}/gettext.jar

# remove unpackaged files from the buildroot
rm ${RPM_BUILD_ROOT}%{_libdir}/lib*.la

# move po-mode initialization elisp file to the right place, and remove byte
# compiled file
#install -d ${RPM_BUILD_ROOT}%{_emacs_sitestartdir}
#mv ${RPM_BUILD_ROOT}%{_emacs_sitelispdir}/%{name}/start-po.el ${RPM_BUILD_ROOT}%{_emacs_sitestartdir}
#rm ${RPM_BUILD_ROOT}%{_emacs_sitelispdir}/%{name}/start-po.elc

#%find_lang %{name}-runtime
#%find_lang %{name}-tools
#cat %{name}-*.lang > %{name}.lang

# cleanup rpaths
#for i in $RPM_BUILD_ROOT%{_bindir}/* `find $RPM_BUILD_ROOT%{_libdir} -type f`; do
#  if file $i | grep "ELF 64-bit" >/dev/null; then
#     chrpath -l $i && chrpath --delete $i
#  fi
#done


%clean
rm -rf ${RPM_BUILD_ROOT}


#%if %{with check}
#%check
## this takes quite a lot of time to run
#make check
#%endif


#%post
#/sbin/ldconfig
#/sbin/install-info %{_infodir}/gettext.info.gz %{_infodir}/dir || :


#%preun
#if [ "$1" = 0 ]; then
#  /sbin/install-info --delete %{_infodir}/gettext.info.gz %{_infodir}/dir || :
#fi


#%postun -p /sbin/ldconfig


#%post devel
#/sbin/ldconfig
#/sbin/install-info %{_infodir}/autosprintf.info %{_infodir}/dir || :


#%preun devel
#if [ "$1" = 0 ]; then
#  /sbin/install-info --delete %{_infodir}/autosprintf.info %{_infodir}/dir || :
#fi


#%postun devel -p /sbin/ldconfig

#%post libs -p /sbin/ldconfig
#%postun libs -p /sbin/ldconfig

%files
# -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS gettext-runtime/BUGS
%doc COPYING gettext-tools/misc/DISCLAIM README
%doc NEWS THANKS 
%doc gettext-runtime/man/*.1.html
%doc gettext-runtime/intl/COPYING*
#/bin/*
#%exclude %{_bindir}/autopoint
%{_bindir}/*
%{_infodir}/gettext*
%exclude %{_mandir}/man1/autopoint.1*
%{_mandir}/man1/*
%{_libdir}/%{name}
%if %{with java}
%exclude %{_libdir}/%{name}/gnu.gettext.*
%endif
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/ABOUT-NLS
%{_datadir}/%{name}/intl
%{_datadir}/%{name}/po
%{_datadir}/%{name}/styles
%{_datadir}/locale/*

%files devel
%defattr(-,root,root,-)
#%doc gettext-runtime/man/*.3.html ChangeLog
#%{_bindir}/autopoint
#%{_datadir}/%{name}/archive.*.tar.gz
%{_datadir}/%{name}/projects/
%{_datadir}/%{name}/config.rpath
%{_datadir}/%{name}/*.h
%{_datadir}/%{name}/msgunfmt.tcl
%{_datadir}/aclocal/*
%{_includedir}/*
%{_infodir}/autosprintf*
%{_libdir}/*.a
%{_mandir}/man1/autopoint.1*
%{_mandir}/man3/*
%{_datadir}/%{name}/javaversion.class
#%doc gettext-runtime/intl-java/javadoc*
%if %{with java}
%{_libdir}/%{name}/gnu.gettext.*
%endif

%files libs
%defattr(-,root,root,-)
%{_libdir}/*.dll
%exclude %{_libdir}/kintl.dll
%if %{with jar}
%{_datadir}/%{name}/libintl.jar
%endif

#%files -n emacs-%{name}
#%defattr(-,root,root,-)
#%dir %{_emacs_sitelispdir}/%{name}
#%{_emacs_sitelispdir}/%{name}/*.elc
#%{_emacs_sitestartdir}/*.el

#%files -n emacs-%{name}-el
#%defattr(-,root,root,-)
#%{_emacs_sitelispdir}/%{name}/*.el

%files legacy
%defattr(-,root,root)
%{_libdir}/kintl.dll

%files debug
%defattr(-,root,root)
%{_bindir}/*.dbg
%{_libdir}/*.dbg

%changelog
* Sat Jan 24 2015 yd
- r981, ignore pthreads rwlock(), they are only stubs.

* Wed Jan 14 2015 yd
- r963, rebuilt with new libtool, which gave new dll names
- added legacy package.
- added debug package with symbolic info for exceptq.
