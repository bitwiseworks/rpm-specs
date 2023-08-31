%global revision 20230520
Summary: Ncurses support utilities
Name: ncurses
Version: 6.4
Release: 1%{?dist}
License: MIT
URL: https://invisible-island.net/ncurses/ncurses.html
%if !0%{?os2_version}
Source0: https://invisible-mirror.net/archives/ncurses/current/ncurses-%{version}-%{revision}.tgz
Source1: https://invisible-mirror.net/archives/ncurses/current/ncurses-%{version}-%{revision}.tgz.asc
Source2: https://invisible-island.net/public/dickey@invisible-island.net-rsa3072.asc

Patch8: ncurses-config.patch
Patch9: ncurses-libs.patch
Patch11: ncurses-urxvt.patch
Patch12: ncurses-kbs.patch
BuildRequires: gcc gcc-c++ gpm-devel gnupg2 make pkgconfig
%else
Vendor: bww bitwise works GmbH
%scm_source     github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2
BuildRequires: gcc gcc-c++ make pkgconfig
%endif

%if !0%{?os2_version}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
%else
Requires: %{name}-libs = %{version}-%{release}
%endif

%description
The curses library routines are a terminal-independent method of
updating character screens with reasonable optimization.  The ncurses
(new curses) library is a freely distributable replacement for the
discontinued 4.4 BSD classic curses library.

This package contains support utilities, including a terminfo compiler
tic, a decompiler infocmp, clear, tput, tset, and a termcap conversion
tool captoinfo.

%package libs
Summary: Ncurses libraries
Requires: %{name}-base = %{version}-%{release}

%description libs
The curses library routines are a terminal-independent method of
updating character screens with reasonable optimization.  The ncurses
(new curses) library is a freely distributable replacement for the
discontinued 4.4 BSD classic curses library.

This package contains the ncurses libraries.

%package compat-libs
Summary: Ncurses compatibility libraries
Requires: %{name}-base = %{version}-%{release}

%description compat-libs
The curses library routines are a terminal-independent method of
updating character screens with reasonable optimization.  The ncurses
(new curses) library is a freely distributable replacement for the
discontinued 4.4 BSD classic curses library.

This package contains the ABI version 5 of the ncurses libraries for
compatibility.

%package c++-libs
Summary: Ncurses C++ bindings
%if !0%{?os2_version}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
%else
Requires: %{name}-libs = %{version}-%{release}
%endif

%description c++-libs
The curses library routines are a terminal-independent method of
updating character screens with reasonable optimization.  The ncurses
(new curses) library is a freely distributable replacement for the
discontinued 4.4 BSD classic curses library.

This package contains C++ bindings of the ncurses ABI version 6 libraries.

%package base
Summary: Descriptions of common terminals
# rxvt-unicode-256color entry used to be in rxvt-unicode and briefly
# in rxvt-unicode-terminfo
Conflicts: rxvt-unicode < 9.22-15
Obsoletes: rxvt-unicode-terminfo < 9.22-18
BuildArch: noarch

%description base
This package contains descriptions of common terminals. Other terminal
descriptions are included in the ncurses-term package.

%if !0%{?os2_version}
%package term
Summary: Terminal descriptions
Requires: %{name}-base = %{version}-%{release}
BuildArch: noarch

%description term
This package contains additional terminal descriptions not found in
the ncurses-base package.
%endif

%package devel
Summary: Development files for the ncurses library
%if !0%{?os2_version}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: %{name}-c++-libs%{?_isa} = %{version}-%{release}
%else
Requires: %{name}-libs = %{version}-%{release}
Requires: %{name}-c++-libs = %{version}-%{release}
%endif
Requires: pkgconfig

%description devel
The header files and libraries for developing applications that use
the ncurses terminal handling library.

Install the ncurses-devel package if you want to develop applications
which will use ncurses.

%package static
Summary: Static libraries for the ncurses library
%if !0%{?os2_version}
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
%else
Requires: %{name}-devel = %{version}-%{release}
%endif

%description static
The ncurses-static package includes static libraries of the ncurses library.

%if 0%{?os2_version}
%debug_package
%endif

%prep
%if !0%{?os2_version}
%{gpgverify} --keyring=%{SOURCE2} --signature=%{SOURCE1} --data=%{SOURCE0}

%setup -q -n %{name}-%{version}-%{revision}

%patch8 -p1 -b .config
%patch9 -p1 -b .libs
%patch11 -p1 -b .urxvt
%patch12 -p1 -b .kbs

for f in ANNOUNCE; do
    iconv -f iso8859-1 -t utf8 -o ${f}{_,} &&
        touch -r ${f}{,_} && mv -f ${f}{_,}
done
%else
%scm_setup
%endif

%build
common_options="\
    --enable-colorfgbg \
    --enable-hard-tabs \
    --enable-overwrite \
    --enable-pc-files \
    --enable-xmc-glitch \
    --disable-root-access \
    --disable-setuid-environ \
    --disable-stripping \
    --disable-wattr-macros \
    --with-cxx-shared \
    --with-ospeed=unsigned \
    --with-pkg-config-libdir=%{_libdir}/pkgconfig \
    --with-shared \
    --with-terminfo-dirs=%{_sysconfdir}/terminfo:%{_datadir}/terminfo \
    --with-termlib=tinfo \
%if !0%{?os2_version}
    --with-ticlib=tic \
    --with-xterm-kbs=DEL \
%endif
    --without-ada"
abi5_options="--with-chtype=long"

%if 0%{?os2_version}
export GREP="grep"
export CC="gcc"
export CXX="g++"
export CXXCPP="g++ -E"
export CXXLIBS="-lstdc++"
export AR_OPTS="cru"
export LDFLAGS="-Zbin-files -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx -lpthread"
%endif

for abi in 5 6; do
    for char in narrowc widec; do
        mkdir $char$abi
%if !0%{?os2_version}
        pushd $char$abi
%else
        cd $char$abi
%endif
        ln -s ../configure .

        [ $abi = 6 -a $char = widec ] && progs=yes || progs=no

        %configure $(
            echo $common_options --with-abi-version=$abi
            [ $abi = 5 ] && echo $abi5_options
            [ $char = widec ] && echo --enable-widec
            [ $progs = yes ] || echo --without-progs
        )

        %make_build libs
        [ $progs = yes ] && %make_build -C progs

%if !0%{?os2_version}
        popd
%else
        cd ..
%endif
    done
done

%install
make -C narrowc5 DESTDIR=$RPM_BUILD_ROOT install.libs
%if !0%{?os2_version}
rm ${RPM_BUILD_ROOT}%{_libdir}/lib{tic,tinfo}.so.5*
%else
rm ${RPM_BUILD_ROOT}%{_libdir}/*tinfo*.a
%endif
make -C widec5 DESTDIR=$RPM_BUILD_ROOT install.libs
make -C narrowc6 DESTDIR=$RPM_BUILD_ROOT install.libs
%if !0%{?os2_version}
rm ${RPM_BUILD_ROOT}%{_libdir}/lib{tic,tinfo}.so.6*
make -C widec6 DESTDIR=$RPM_BUILD_ROOT install.{libs,progs,data,includes,man}
%else
rm ${RPM_BUILD_ROOT}%{_libdir}/*tinfo*.a
make -C widec6 DESTDIR=$RPM_BUILD_ROOT install.libs
make -C widec6 DESTDIR=$RPM_BUILD_ROOT install.progs
make -C widec6 DESTDIR=$RPM_BUILD_ROOT install.data
make -C widec6 DESTDIR=$RPM_BUILD_ROOT install.includes
make -C widec6 DESTDIR=$RPM_BUILD_ROOT install.man
%endif
make DESTDIR=$RPM_BUILD_ROOT install

%if !0%{?os2_version}
chmod 755 ${RPM_BUILD_ROOT}%{_libdir}/lib*.so.*.*
chmod 644 ${RPM_BUILD_ROOT}%{_libdir}/lib*.a
%endif

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/terminfo

baseterms=

# prepare -base and -term file lists
%if !0%{?os2_version}
for termname in \
    alacritty ansi dumb foot\* linux vt100 vt100-nav vt102 vt220 vt52 \
    Eterm\* aterm bterm cons25 cygwin eterm\* gnome gnome-256color hurd jfbterm \
    kitty konsole konsole-256color mach\* mlterm mrxvt nsterm putty{,-256color} pcansi \
    rxvt{,-\*} screen{,-\*color,.[^mlp]\*,.linux,.mlterm\*,.putty{,-256color},.mrxvt} \
    st{,-\*color} sun teraterm teraterm2.3 tmux{,-\*} vte vte-256color vwmterm \
    wsvt25\* xfce xterm xterm-\*
do
    for i in $RPM_BUILD_ROOT%{_datadir}/terminfo/?/$termname; do
        for t in $(find $RPM_BUILD_ROOT%{_datadir}/terminfo -samefile $i); do
            baseterms="$baseterms $(basename $t)"
        done
    done
done 2> /dev/null
for t in $baseterms; do
    echo "%dir %{_datadir}/terminfo/${t::1}"
    echo %{_datadir}/terminfo/${t::1}/$t
done 2> /dev/null | sort -u > terms.base
find $RPM_BUILD_ROOT%{_datadir}/terminfo \! -type d | \
    sed "s|^$RPM_BUILD_ROOT||" | while read t
do
    echo "%dir $(dirname $t)"
    echo $t
done 2> /dev/null | sort -u | comm -2 -3 - terms.base > terms.term
%endif

# can't replace directory with symlink (rpm bug), symlink all headers
%if !0%{?os2_version}
mkdir $RPM_BUILD_ROOT%{_includedir}/ncurses{,w}
%else
mkdir $RPM_BUILD_ROOT%{_includedir}/ncurses
mkdir $RPM_BUILD_ROOT%{_includedir}/ncursesw
%endif
for l in $RPM_BUILD_ROOT%{_includedir}/*.h; do
    ln -s ../$(basename $l) $RPM_BUILD_ROOT%{_includedir}/ncurses
    ln -s ../$(basename $l) $RPM_BUILD_ROOT%{_includedir}/ncursesw
done

%if !0%{?os2_version}
# don't require -ltinfo when linking with --no-add-needed
for l in $RPM_BUILD_ROOT%{_libdir}/libncurses{,w}.so; do
    soname=$(basename $(readlink $l))
    rm -f $l
    echo "INPUT($soname -ltinfo)" > $l
done

rm -f $RPM_BUILD_ROOT%{_libdir}/libcurses{,w}.so
echo "INPUT(-lncurses)" > $RPM_BUILD_ROOT%{_libdir}/libcurses.so
echo "INPUT(-lncursesw)" > $RPM_BUILD_ROOT%{_libdir}/libcursesw.so

echo "INPUT(-ltinfo)" > $RPM_BUILD_ROOT%{_libdir}/libtermcap.so
%endif

rm -f $RPM_BUILD_ROOT%{_bindir}/ncurses*5-config
rm -f $RPM_BUILD_ROOT%{_libdir}/terminfo
rm -f $RPM_BUILD_ROOT%{_libdir}/pkgconfig/*_g.pc

xz NEWS

%if !0%{?os2_version}
%ldconfig_scriptlets libs

%ldconfig_scriptlets c++-libs

%ldconfig_scriptlets compat-libs
%endif

%files
%doc ANNOUNCE AUTHORS NEWS.xz README TO-DO
%if !0%{?os2_version}
%{_bindir}/[cirt]*
%else
%{_bindir}/[cirt]*.exe
%endif
%{_mandir}/man1/[cirt]*
%{_mandir}/man5/*
%{_mandir}/man7/*

%files libs
%if !0%{?os2_version}
%exclude %{_libdir}/libncurses++*.so.6*
%{_libdir}/lib*.so.6*
%else
%exclude %{_libdir}/ncurs++6.dll
%{_libdir}/*.dll
%endif

%files compat-libs
%if !0%{?os2_version}
%{_libdir}/lib*.so.5*
%else
%{_libdir}/*5.dll
%endif

%files c++-libs
%if !0%{?os2_version}
%{_libdir}/libncurses++*.so.6*
%else
%{_libdir}/ncurs++6.dll
%endif

%if !0%{?os2_version}
%files base -f terms.base
%else
%files base
%endif
%license COPYING
%doc README
%dir %{_sysconfdir}/terminfo
%{_datadir}/tabset
%if !0%{?os2_version}
%dir %{_datadir}/terminfo
%else
%{_datadir}/terminfo
%endif

%if !0%{?os2_version}
%files term -f terms.term
%endif

%files devel
%doc doc/html/hackguide.html
%doc doc/html/ncurses-intro.html
%doc c++/README*
%doc misc/ncurses.supp
%{_bindir}/ncurses*-config
%if !0%{?os2_version}
%{_libdir}/lib*.so
%else
%{_libdir}/*_dll.a
%{_libdir}/*.lib
%endif
%{_libdir}/pkgconfig/*.pc
%dir %{_includedir}/ncurses
%dir %{_includedir}/ncursesw
%{_includedir}/ncurses/*.h
%{_includedir}/ncursesw/*.h
%{_includedir}/*.h
%{_mandir}/man1/ncurses*-config*
%{_mandir}/man3/*

%files static
%if !0%{?os2_version}
%{_libdir}/lib*.a
%else
%exclude %{_libdir}/*_dll.a
%{_libdir}/*.a
%endif

%changelog
* Fri Aug 25 2023 Silvan Scherrer <silvan.scherrer@aroa.ch> 6.4-1
- update to version 6.4
- added version5 and version6
- added wide support
- rework spec completely

* Sat Jan 14 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 5.9-1
- update to version 5.9
- add correct keyboard and mouse handling (borrowed from KO Myung-Hun)

* Mon Jan 16 2012 yd
- rebuild with libc 0.6.4 runtime.
