Summary: A spelling checker
Name: aspell
Version: 0.60.6.1
Release: 1%{?dist} 
License: LGPL
Group: Applications/Text
URL: http://aspell.net/
#define svn_url	    e:/trees/aspell/trunk
%define svn_url     http://svn.netlabs.org/repos/ports/aspell/trunk
%define svn_rev     1041

Source: %{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip

BuildRoot: %{tmpdir}/%{name}-%{version}-root-%(id -u -n)

BuildRequires: gettext, ncurses-devel, pkgconfig
Requires: aspell-en
Provides: pspell < 0.13
Obsoletes: pspell < 0.13


%description
GNU Aspell is a spell checker designed to eventually replace Ispell. It can
either be used as a library or as an independent spell checker. Its main
feature is that it does a much better job of coming up with possible
suggestions than just about any other spell checker out there for the
English language, including Ispell and Microsoft Word. It also has many
other technical enhancements over Ispell such as using shared memory for
dictionaries and intelligently handling personal dictionaries when more
than one Aspell process is open at once.

%package	devel
Summary: Static libraries and header files for Aspell development
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig
Provides: pspell-devel < 0.13
Obsoletes: pspell-devel < 0.13

%description	devel
Aspell is a spelling checker. The aspell-devel package includes the
static libraries and header files needed for Aspell development.

%package debug
Summary: HLL debug data for exception handling support

%description debug
%{summary}.

%prep
%if %{?svn_rev:%(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')}%{?!svn_rev):0}
%setup -q
%else
%setup -n "%{name}-%{version}" -Tc
svn export %{?svn_rev:-r %{svn_rev}} %{svn_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip" "%{name}-%{version}")
%endif

autoreconf -fi

%build
export LDFLAGS="-Zbin-files -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp" ; \
export LIBS="-ltinfo" ; \

%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/aspell-0.60

mv ${RPM_BUILD_ROOT}%{_libdir}/aspell-0.60/ispell ${RPM_BUILD_ROOT}%{_bindir}
mv ${RPM_BUILD_ROOT}%{_libdir}/aspell-0.60/spell ${RPM_BUILD_ROOT}%{_bindir}

rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la
rm -f ${RPM_BUILD_ROOT}%{_libdir}/aspell-0.60/*.la
chmod 644 ${RPM_BUILD_ROOT}%{_bindir}/aspell-import

#find_lang %{name}


%files
# -f %{name}.lang
%defattr(-,root,root)
%doc README TODO COPYING
%dir %{_libdir}/aspell-0.60
%{_bindir}/a*
%{_bindir}/ispell
%{_bindir}/pr*
%exclude %{_bindir}/*.dbg
%{_bindir}/run-with-aspell
%{_bindir}/spell
%{_bindir}/word-list-compress.exe
%{_libdir}/*.dll
%{_libdir}/aspell-0.60/*
%{_datadir}/locale/*/LC_MESSAGES/aspell.mo
%{_infodir}/aspell.*
%{_mandir}/man1/aspell*
%{_mandir}/man1/run-with-aspell.1*
%{_mandir}/man1/word-list-compress.1*
%{_mandir}/man1/prezip-bin.1*

%files		devel
%defattr(-,root,root)
%dir %{_includedir}/pspell
%{_bindir}/pspell-config
%{_includedir}/aspell.h
%{_includedir}/pspell/pspell.h
%{_libdir}/*.a
%{_infodir}/aspell-dev.*
%{_mandir}/man1/pspell-config.1*

%files debug
%defattr(-,root,root)
%{_libdir}/*.dbg
%{_bindir}/*.dbg

%changelog
* Thu Feb 12 2015 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.60.6.1-1
- first version