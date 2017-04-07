%define double_profiling_build 0

Name:      hunspell
Summary:   A spell checker and morphological analyzer library
Version:   1.6.1
Release:   1%{?dist}
URL:       https://github.com/hunspell/hunspell
Group:     System Environment/Libraries
License:   LGPLv2+ or GPLv2+ or MPLv1.1

Vendor:    bww bitwise works GmbH
%scm_source github https://github.com/bitwiseworks/hunspell-os2 %{version}-os2

BuildRequires: ncurses-devel, gettext
BuildRequires: perl-generators
%ifarch %{ix86} x86_64
#BuildRequires: valgrind
%endif
%if %{double_profiling_build}
BuildRequires: words
%endif
Requires:  hunspell-en-US


%description
Hunspell is a spell checker and morphological analyzer library and program 
designed for languages with rich morphology and complex word compounding or 
character encoding. Hunspell interfaces: Ispell-like terminal interface using 
Curses library, Ispell pipe interface, OpenOffice.org UNO module.

%package devel
Requires: hunspell = %{version}-%{release}, pkgconfig
Summary: Files for developing with hunspell
Group: Development/Libraries

%description devel
Includes and definitions for developing with hunspell

%prep
%scm_setup
autoreconf -fvi

%build
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx -ltinfo"
export VENDOR="%{vendor}"

configureflags="--disable-static --enable-shared --with-ui --with-readline"

%define profilegenerate \
    CFLAGS="${RPM_OPT_FLAGS} -fprofile-generate"\
    CXXFLAGS="${RPM_OPT_FLAGS} -fprofile-generate"
%define profileuse \
    CFLAGS="${RPM_OPT_FLAGS} -fprofile-use"\
    CXXFLAGS="${RPM_OPT_FLAGS} -fprofile-use"

%if !%{double_profiling_build}
%configure $configureflags
make %{?_smp_mflags}
%else
#Generate a word list to use for profiling, take half of it to ensure
#that the original word list is then considered to contain correctly
#and incorrectly spelled words
head -n $((`cat /usr/share/dict/words | wc -l`/2)) /usr/share/dict/words |\
    sed '/\//d'> words

#generate profiling
%{profilegenerate} %configure $configureflags
make %{?_smp_mflags}
./src/tools/affixcompress words > /dev/null 2>&1
./src/tools/hunspell -d words -l /usr/share/dict/words > /dev/null
make check
make distclean

#use profiling
%{profileuse} %configure $configureflags
make %{?_smp_mflags}
%endif
cd po && make %{?_smp_mflags} update-gmo && cd ..

%check
%ifarch %{ix86} x86_64
#VALGRIND=memcheck make check
#make check
%endif

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la
mkdir $RPM_BUILD_ROOT/%{_datadir}/myspell
%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc README README.myspell COPYING COPYING.LESSER COPYING.MPL AUTHORS AUTHORS.myspell license.hunspell license.myspell THANKS
%{_libdir}/*.dll
%{_datadir}/myspell
%{_bindir}/hunspell.exe
%{_mandir}/man1/hunspell.1.gz
%lang(hu) %{_mandir}/hu/man1/hunspell.1.gz

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}
%{_libdir}/*_dll.a
%{_bindir}/affixcompress
%{_bindir}/makealias
%{_bindir}/munch.exe
%{_bindir}/unmunch.exe
%{_bindir}/analyze.exe
%{_bindir}/chmorph.exe
%{_bindir}/hzip.exe
%{_bindir}/hunzip.exe
%{_bindir}/ispellaff2myspell
%{_bindir}/wordlist2hunspell
%{_bindir}/wordforms
%{_libdir}/pkgconfig/hunspell.pc
%{_mandir}/man1/hunzip.1.gz
%{_mandir}/man1/hzip.1.gz
%{_mandir}/man3/hunspell.3.gz
%{_mandir}/man5/hunspell.5.gz

%changelog
* Fri Apr 07 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.6.1-1
- initial port
