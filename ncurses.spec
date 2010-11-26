
Summary: Ncurses support utilities
Name: ncurses
Version: 5.7
Release: 2%{?dist}
License: MIT
Group: System Environment/Base
URL: http://invisible-island.net/ncurses/ncurses.html
Source0: ftp://invisible-island.net/ncurses/ncurses-%{version}.tar.gz

Patch1: ncurses-5.7-os2.diff

#BuildRequires: gpm-devel pkgconfig
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires: %{name}-libs = %{version}-%{release}

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
Group: System Environment/Libraries
Requires: %{name}-base = %{version}-%{release}
# libs introduced in 5.6-13 
Obsoletes: ncurses < 5.6-13
Conflicts: ncurses < 5.6-13
Obsoletes: libtermcap < 2.0.8-48

%description libs
The curses library routines are a terminal-independent method of
updating character screens with reasonable optimization.  The ncurses
(new curses) library is a freely distributable replacement for the
discontinued 4.4 BSD classic curses library.

This package contains the ncurses libraries.

%package base
Summary: Descriptions of common terminals
Group: System Environment/Base
Obsoletes: termcap < 1:5.5-2
# base introduced in 5.6-13 
Conflicts: ncurses < 5.6-13

%description base
This package contains descriptions of common terminals. Other terminal
descriptions are included in the ncurses-term package.

#%package term
#Summary: Terminal descriptions
#Group: System Environment/Base
#Requires: %{name}-base = %{version}-%{release}

#%description term
#This package contains additional terminal descriptions not found in
#the ncurses-base package.

%package devel
Summary: Development files for the ncurses library
Group: Development/Libraries
Requires: %{name}-libs = %{version}-%{release}
Requires: pkgconfig
Obsoletes: libtermcap-devel < 2.0.8-48
Provides: libtermcap-devel = 2.0.8-48

%description devel
The header files and libraries for developing applications that use
the ncurses terminal handling library.

Install the ncurses-devel package if you want to develop applications
which will use ncurses.

#%package static
#Summary: Static libraries for the ncurses library
#Group: Development/Libraries
#Requires: %{name}-devel = %{version}-%{release}

#%description static
#The ncurses-static package includes static libraries of the ncurses library.

%prep
%setup -q

%patch1 -p1 -b .os2~

# this will be in documentation, drop executable bits
#cp -p install-sh test
#chmod 644 test/*

#for f in ANNOUNCE; do
#	iconv -f iso8859-1 -t utf8 -o ${f}{_,} &&
#		touch -r ${f}{,_} && mv -f ${f}{_,}
#done

%build
%define rootdatadir /@unixroot/lib
%define ncurses_options \\\
    --with-shared --without-ada --with-ospeed=unsigned \\\
    --enable-hard-tabs --enable-xmc-glitch --enable-colorfgbg \\\
    --with-terminfo-dirs=%{_sysconfdir}/terminfo:%{_datadir}/terminfo:%{rootdatadir}/terminfo \\\
    --enable-overwrite \\\
    --enable-pc-files \\\
    --with-termlib=tinfo \\\
    --with-chtype=long

#export PKG_CONFIG_LIBDIR=%{_libdir}/pkgconfig

export AWK="awk" ; \
export CC="gcc" ; \
export CXX="gcc" ; \
export AR_OPTS="cru" ; \
export CONFIG_SHELL="/bin/sh" ; \
export LDFLAGS="-Zbin-files -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp" ; \
export LIBS="-lurpo -lmmap -lpthread" ; \
%configure \
    --with-shared --without-normal --without-debug \
    --without-cxx-binding \
    --without-ada --with-ospeed=unsigned \
    --enable-hard-tabs --enable-xmc-glitch --enable-colorfgbg \
    --with-default-terminfo-dir=/@unixroot/usr/share/terminfo \
    --enable-overwrite \
    --enable-pc-files \
    --with-termlib=tinfo \
    --with-chtype=long \
    "--cache-file=%{_topdir}/cache/%{name}.cache"

make %{_smp_mflags}

%install
rm -rf ${RPM_BUILD_ROOT}

#make -C narrowc DESTDIR=$RPM_BUILD_ROOT install.{libs,progs,data}
#rm -f $RPM_BUILD_ROOT%{_libdir}/libtinfo.*
#make -C widec DESTDIR=$RPM_BUILD_ROOT install.{libs,includes,man}

make DESTDIR=$RPM_BUILD_ROOT install

#chmod 755 ${RPM_BUILD_ROOT}%{_libdir}/lib*.so.*.*
#chmod 644 ${RPM_BUILD_ROOT}%{_libdir}/lib*.a

# move lib{ncurses{,w},tinfo}.so.* to /lib*
#mkdir $RPM_BUILD_ROOT/%{_lib}
#mv $RPM_BUILD_ROOT%{_libdir}/lib{ncurses{,w},tinfo}.so.* $RPM_BUILD_ROOT/%{_lib}
#for l in $RPM_BUILD_ROOT%{_libdir}/lib{ncurses{,w},tinfo}.so; do
#    ln -sf $(echo %{_libdir} | \
#        sed 's,\(^/\|\)[^/][^/]*,..,g')/%{_lib}/$(readlink $l) $l
#done

mv "$RPM_BUILD_ROOT%{_bindir}/*.dll" $RPM_BUILD_ROOT/%{_libdir}

#mkdir -p $RPM_BUILD_ROOT%{rootdatadir}/terminfo
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/terminfo

# move few basic terminfo entries to /lib
#baseterms=
#for termname in \
#        ansi dumb linux vt100 vt100-nav vt102 vt220 vt52
#do
#    for t in $(find $RPM_BUILD_ROOT%{_datadir}/terminfo \
#        -samefile $RPM_BUILD_ROOT%{_datadir}/terminfo/${termname::1}/$termname)
#    do
#        baseterms="$baseterms $(basename $t)"
#    done
#done
#for termname in $baseterms; do
#    termpath=terminfo/${termname::1}/$termname
#    mkdir $RPM_BUILD_ROOT%{rootdatadir}/terminfo/${termname::1} &> /dev/null || :
#    mv $RPM_BUILD_ROOT%{_datadir}/$termpath $RPM_BUILD_ROOT%{rootdatadir}/$termpath
#    ln -s $(dirname %{_datadir}/$termpath | \
#        sed 's,\(^/\|\)[^/][^/]*,..,g')%{rootdatadir}/$termpath \
#        $RPM_BUILD_ROOT%{_datadir}/$termpath
#done

# prepare -base and -term file lists
#for termname in \
#    Eterm\* aterm bterm cons25 cygwin eterm\* gnome gnome-256color hurd jfbterm \
#    konsole konsole-256color mach\* mlterm mrxvt nsterm putty\* pcansi \
#    rxvt rxvt-\* screen screen-\* screen.\* sun teraterm teraterm2.3 \
#    vwmterm wsvt25\* xfce xterm xterm-\*
#do
#    for i in $RPM_BUILD_ROOT%{_datadir}/terminfo/?/$termname; do
#        for t in $(find $RPM_BUILD_ROOT%{_datadir}/terminfo -samefile $i); do
#            baseterms="$baseterms $(basename $t)"
#        done
#    done
#done 2> /dev/null
#for t in $baseterms; do
#    echo "%dir %{_datadir}/terminfo/${t::1}"
#    echo %{_datadir}/terminfo/${t::1}/$t
#done 2> /dev/null | sort -u > terms.base
#find $RPM_BUILD_ROOT%{_datadir}/terminfo \! -type d | \
#    sed "s|^$RPM_BUILD_ROOT||" | while read t
#do
#    echo "%dir $(dirname $t)"
#    echo $t
#done 2> /dev/null | sort -u | comm -2 -3 - terms.base > terms.term

# can't replace directory with symlink (rpm bug), symlink all headers
#mkdir $RPM_BUILD_ROOT%{_includedir}/ncurses{,w}
#for l in $RPM_BUILD_ROOT%{_includedir}/*.h; do
#    ln -s ../$(basename $l) $RPM_BUILD_ROOT%{_includedir}/ncurses
#    ln -s ../$(basename $l) $RPM_BUILD_ROOT%{_includedir}/ncursesw
#done

# don't require -ltinfo when linking with --no-add-needed
#for l in $RPM_BUILD_ROOT%{_libdir}/libncurses{,w}.so; do
#    soname=$(basename $(readlink $l))
#    rm -f $l
#    echo "INPUT($soname -ltinfo)" > $l
#done

#rm -f $RPM_BUILD_ROOT%{_libdir}/libcurses{,w}.so
#echo "INPUT(-lncurses)" > $RPM_BUILD_ROOT%{_libdir}/libcurses.so
#echo "INPUT(-lncursesw)" > $RPM_BUILD_ROOT%{_libdir}/libcursesw.so

#echo "INPUT(-ltinfo)" > $RPM_BUILD_ROOT%{_libdir}/libtermcap.so

rm -f $RPM_BUILD_ROOT%{_libdir}/terminfo
#rm -f $RPM_BUILD_ROOT%{_libdir}/pkgconfig/{*_g,ncurses++*}.pc

#bzip2 NEWS

#%post libs -p /sbin/ldconfig

#%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc ANNOUNCE AUTHORS NEWS README TO-DO
%{_bindir}/[cirt]*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man7/*

%files libs
%defattr(-,root,root)
%{_libdir}/*.dll

%files base
# -f terms.base
%defattr(-,root,root)
%dir %{_sysconfdir}/terminfo
#%dir %{rootdatadir}/terminfo
%{_datadir}/tabset
%{_datadir}/terminfo

#%files term
# -f terms.term
#%defattr(-,root,root)

%files devel
%defattr(-,root,root)
#%doc test
#%doc doc/html/hackguide.html
#%doc doc/html/ncurses-intro.html
#%doc c++/README*
#%doc misc/ncurses.supp
%{_bindir}/ncurses*-config
%{_libdir}/*.dll
%{_libdir}/*.a
%{_libdir}/*.lib
#%{_libdir}/pkgconfig/*.pc
#%dir %{_includedir}/ncurses
#%dir %{_includedir}/ncursesw
#%{_includedir}/ncurses/*.h
#%{_includedir}/ncursesw/*.h
%{_includedir}/*.h
%{_mandir}/man3/*

#%files static
#%defattr(-,root,root)
#%{_libdir}/lib*.a

%clean
rm -rf ${RPM_BUILD_ROOT}

%changelog
