# spec source :http://pkgs.fedoraproject.org/cgit/rpms/aspell.git/tree/aspell.spec

Summary: Spell checker
Name: aspell
Version: 0.60.6.1
Release: 2%{?dist} 
License: LGPLv2+ and LGPLv2 and GPLv2+ and BSD
Group: Applications/Text
URL: http://aspell.net/

Vendor: bww bitwise works GmbH
%scm_source github https://github.com/bitwiseworks/%{name}-os2 master

BuildRequires: gettext, ncurses-devel, pkgconfig
Requires(pre): %{_sbindir}/install-info.exe
Requires(preun): %{_sbindir}/install-info.exe
Requires: aspell-en


%description
GNU Aspell is a spell checker designed to eventually replace Ispell. It can
either be used as a library or as an independent spell checker. Its main
feature is that it does a much better job of coming up with possible
suggestions than just about any other spell checker out there for the
English language, including Ispell and Microsoft Word. It also has many
other technical enhancements over Ispell such as using shared memory for
dictionaries and intelligently handling personal dictionaries when more
than one Aspell process is open at once.

%package devel
Summary: Libraries and header files for Aspell development
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires(pre): %{_sbindir}/install-info.exe
Requires(preun): %{_sbindir}/install-info.exe
Requires: pkgconfig

%description devel
Aspell is a spelling checker. The aspell-devel package includes the
static libraries and header files needed for Aspell development.


%debug_package

%prep
%scm_setup

autoreconf -fvi

%build
export LDFLAGS="-Zbin-files -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-ltinfo -lcx"
export VENDOR="%{vendor}"

%configure --disable-static
make %{?_smp_mflags}
cp scripts/aspell-import examples/aspell-import
cp manual/aspell-import.1 examples/aspell-import.1


%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/aspell-0.60

mv ${RPM_BUILD_ROOT}%{_libdir}/aspell-0.60/ispell ${RPM_BUILD_ROOT}%{_bindir}
mv ${RPM_BUILD_ROOT}%{_libdir}/aspell-0.60/spell ${RPM_BUILD_ROOT}%{_bindir}

rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la
rm -f ${RPM_BUILD_ROOT}%{_libdir}/aspell-0.60/*.la
rm -f ${RPM_BUILD_ROOT}%{_bindir}/aspell-import
rm -f ${RPM_BUILD_ROOT}%{_mandir}/man1/aspell-import.1
rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir

%find_lang %{name}

%post
# /sbin/ldconfig
if [ -f %{_infodir}/aspell.info.gz ]; then  
    %{_sbindir}/install-info %{_infodir}/aspell.info.gz %{_infodir}/dir --entry="* Aspell: (aspell). "  || : 
fi

%post devel
if [ -f %{_infodir}/aspell-dev.info.gz ]; then  
    %{_sbindir}/install-info %{_infodir}/aspell-dev.info.gz %{_infodir}/dir --entry="* Aspell-dev: (aspell-dev). " || :
fi

%preun
if [ $1 = 0 ]; then
    if [ -f %{_infodir}/aspell.info.gz ]; then  
        %{_sbindir}/install-info --delete %{_infodir}/aspell.info.gz %{_infodir}/dir || :
    fi
fi

%preun devel
if [ $1 = 0 ]; then
    if [ -f %{_infodir}/aspell-dev.info.gz ]; then  
        %{_sbindir}/install-info --delete %{_infodir}/aspell-dev.info.gz %{_infodir}/dir || :
    fi
fi

#postun -p /sbin/ldconfig

%files -f %{name}.lang
%doc README TODO COPYING examples/aspell-import examples/aspell-import.1
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
%exclude %{_libdir}/aspell-0.60/*.dbg
%{_infodir}/aspell.*
%{_mandir}/man1/aspell.1.*
%{_mandir}/man1/run-with-aspell.1*
%{_mandir}/man1/word-list-compress.1*
%{_mandir}/man1/prezip-bin.1*

%files devel
%dir %{_includedir}/pspell
%{_bindir}/pspell-config
%{_includedir}/aspell.h
%{_includedir}/pspell/pspell.h
%{_libdir}/*.a
%{_infodir}/aspell-dev.*
%{_mandir}/man1/pspell-config.1*


%changelog
* Wed Dec 20 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.60.6.1-2
- use new scm_ macros
- fix loading of filters
- add bldlevel to the dll
- move source to github

* Thu Feb 12 2015 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.60.6.1-1
- first version
