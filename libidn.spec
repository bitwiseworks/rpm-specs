#define svn_url     e:/trees/libidn/trunk
%define svn_url     http://svn.netlabs.org/repos/ports/libidn/trunk
%define svn_rev     1828

# set this to 1 to enable
%global with_java 0
%global with_emacs 0

Summary: Internationalized Domain Name support library
Name: libidn
Version: 1.33
Release: 1%{?dist}
URL: http://www.gnu.org/software/libidn/
License: LGPLv2+ and GPLv3+ and GFDL

Vendor:  bww bitwise works GmbH
Source:  %{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip

Group: System Environment/Libraries
BuildRequires: pkgconfig gettext
#BuildRequires: emacs
#Requires(post): /sbin/install-info /sbin/ldconfig
#Requires(preun): /sbin/install-info
#Requires(postun): /sbin/ldconfig
Requires: libcx >= 0.4.0

%if 0%{?with_emacs}
# emacs-libidn merged with main package in 1.30-4
Obsoletes: emacs-libidn < 1.30-4
Provides: emacs-libidn < 1.30-4
Requires: emacs-filesystem >= %{_emacs_version}
%endif

%description
GNU Libidn is an implementation of the Stringprep, Punycode and
IDNA specifications defined by the IETF Internationalized Domain
Names (IDN) working group, used for internationalized domain
names.

%package devel
Summary: Development files for the libidn library
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: pkgconfig

%description devel
This package includes header files and libraries necessary for
developing programs which use the GNU libidn library.

%if 0%{?with_java}
%package java
Summary:       Java port of the GNU Libidn library
BuildRequires: java-devel
BuildRequires: javapackages-local
BuildRequires: mvn(com.google.code.findbugs:annotations)
BuildRequires: mvn(com.google.guava:guava)
BuildRequires: mvn(junit:junit)
BuildArch:     noarch

%description java
GNU Libidn is a fully documented implementation of the Stringprep,
Punycode and IDNA specifications. Libidn's purpose is to encode
and decode internationalized domain names.

This package contains the native Java port of the library.

%package javadoc
Summary:       Javadoc for %{name}-java
BuildArch:     noarch

%description javadoc
This package contains javadoc for %{name}-java.
%endif


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

autoreconf -fvi

# Cleanup
find . -name '*.jar' -print -delete
find . -name '*.class' -print -delete


%build
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
export VENDOR="%{vendor}"
#--with-lispdir=%{_emacs_sitelispdir}/%{name} --enable-java
%configure --disable-csharp --disable-static

make %{?_smp_mflags}

%check
# without RPATH this needs to be set to test the compiled library
#export LD_LIBRARY_PATH=$(pwd)/lib/.libs
#make %{?_smp_mflags} -C tests check VALGRIND=env

%install
# libidn_jardir=%{_javadir}
make install DESTDIR=$RPM_BUILD_ROOT pkgconfigdir=%{_libdir}/pkgconfig

# provide more examples
make %{?_smp_mflags} -C examples distclean

# clean up docs
find doc -name "Makefile*" | xargs rm
rm -rf $RPM_BUILD_ROOT%{_datadir}/info/dir

rm -rf $RPM_BUILD_ROOT%{_datadir}/emacs

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la \
      $RPM_BUILD_ROOT%{_datadir}/info/*.png

#{_emacs_bytecompile} $RPM_BUILD_ROOT%{_emacs_sitelispdir}/%{name}/*.el

# regenerate java documentation
rm -rf doc/java/*
%if 0%{?with_java}
%javadoc -source 1.6 -d doc/java $(find java/src/main/java -name "*.java")
# generate maven depmap
rm -rf $RPM_BUILD_ROOT%{_javadir}/libidn*.jar
%mvn_artifact java/pom.xml java/libidn-%{version}.jar
%mvn_file org.gnu.inet:libidn libidn
%mvn_install -J doc/java
%endif

%find_lang %{name}

%post
#/sbin/install-info %{_infodir}/%{name}.info.gz %{_infodir}/dir
#/sbin/ldconfig

%preun
#if [ $1 = 0 ]; then
#    /sbin/install-info --delete %{_infodir}/%{name}.info.gz %{_infodir}/dir || :
#fi

#%postun -p /sbin/ldconfig

%files -f %{name}.lang
%{!?_licensedir:%global license %%doc}
%license COPYING*
%doc AUTHORS NEWS FAQ README THANKS
%{_bindir}/idn.exe
%{_mandir}/man1/idn.1*
%{_libdir}/idn*.dll
%{_infodir}/%{name}.info

%if 0%{?with_emacs}
%{_emacs_sitelispdir}/%{name}
%endif

%files devel
%doc doc/libidn.html examples
%{_libdir}/idn*_dll.a
%{_includedir}/*.h
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*

%if 0%{?with_java}
%files java -f .mfiles
%license COPYING* java/LICENSE-2.0.txt

%files javadoc -f .mfiles-javadoc
%license COPYING* java/LICENSE-2.0.txt
%endif

%changelog
* Tue Nov 15 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.33-1
- first version