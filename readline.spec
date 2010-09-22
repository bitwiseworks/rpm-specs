Summary: A library for editing typed command lines
Name: readline
Version: 6.1
Release: 1
License: GPLv3+
Group: System Environment/Libraries
URL: http://cnswww.cns.cwru.edu/php/chet/readline/rltop.html
Source: ftp://ftp.gnu.org/gnu/readline/readline-%{version}.tar.gz

# sent upstream
Patch0: readline-6.1-os2.diff

#Requires(post): /sbin/install-info
#Requires(preun): /sbin/install-info
BuildRequires: ncurses-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
The Readline library provides a set of functions that allow users to
edit command lines. Both Emacs and vi editing modes are available. The
Readline library includes additional functions for maintaining a list
of previously-entered command lines for recalling or editing those
lines, and for performing csh-like history expansion on previous
commands.

%package devel
Summary: Files needed to develop programs which use the readline library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: ncurses-devel
#Requires(post): /sbin/install-info
#Requires(preun): /sbin/install-info

%description devel
The Readline library provides a set of functions that allow users to
edit typed command lines. If you want to develop programs that will
use the readline library, you need to have the readline-devel package
installed. You also need to have the readline package installed.

%package static
Summary: Static libraries for the readline library
Group: Development/Libraries
Requires: %{name}-devel = %{version}-%{release}

%description static
The readline-static package contains the static version of the readline
library.

%prep
%setup -q
%patch0 -p1 -b .os2~

#pushd examples
#rm -f rlfe/configure
#iconv -f iso8859-1 -t utf8 -o rl-fgets.c{_,}
#touch -r rl-fgets.c{,_}
#mv -f rl-fgets.c{_,}
#popd

%build
#export CPPFLAGS="-I%{_includedir}/ncurses"
CONFIG_SHELL="/bin/sh" ; export CONFIG_SHELL ; \
LDFLAGS="-Zbin-files -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp" ; export LDFLAGS ; \
%configure \
    --disable-shared \
    "--cache-file=%{_topdir}/cache/%{name}.cache"

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

#mkdir $RPM_BUILD_ROOT/%{_lib}
#mv $RPM_BUILD_ROOT%{_libdir}/libreadline.so.* $RPM_BUILD_ROOT/%{_lib}
#for l in $RPM_BUILD_ROOT%{_libdir}/libreadline.so; do
#    ln -sf $(echo %{_libdir} | \
#        sed 's,\(^/\|\)[^/][^/]*,..,g')/%{_lib}/$(readlink $l) $l
#done

rm -rf $RPM_BUILD_ROOT%{_datadir}/readline
rm -f $RPM_BUILD_ROOT%{_infodir}/dir*

cp readln6.dll $RPM_BUILD_ROOT%{_libdir}
cp libreadline_s.a $RPM_BUILD_ROOT%{_libdir}
cp libreadline.lib $RPM_BUILD_ROOT%{_libdir}
cp histor6.dll $RPM_BUILD_ROOT%{_libdir}
cp libhistory_s.a $RPM_BUILD_ROOT%{_libdir}
cp libhistory.lib $RPM_BUILD_ROOT%{_libdir}


%clean
rm -rf $RPM_BUILD_ROOT

#%post
#/sbin/ldconfig
#/sbin/install-info %{_infodir}/history.info.gz %{_infodir}/dir &> /dev/null
#/sbin/install-info %{_infodir}/rluserman.info.gz %{_infodir}/dir &> /dev/null
#:

#%postun -p /sbin/ldconfig

#%preun
#if [ $1 = 0 ]; then
#   /sbin/install-info --delete %{_infodir}/history.info.gz %{_infodir}/dir &> /dev/null
#   /sbin/install-info --delete %{_infodir}/rluserman.info.gz %{_infodir}/dir &> /dev/null
#fi
#:

#%post devel
#/sbin/install-info %{_infodir}/readline.info.gz %{_infodir}/dir &> /dev/null
#:

#%preun devel
#if [ $1 = 0 ]; then
#   /sbin/install-info --delete %{_infodir}/readline.info.gz %{_infodir}/dir &> /dev/null
#fi
#:

%files
%defattr(-,root,root,-)
%doc CHANGES COPYING NEWS README USAGE
%{_libdir}/*.dll
%{_infodir}/history.info*
%{_infodir}/rluserman.info*

%files devel
%defattr(-,root,root,-)
%doc examples/*.c examples/*.h examples/rlfe
%{_includedir}/readline
%{_libdir}/*.dll
%{_libdir}/libreadline.a
%{_libdir}/libhistory.a
%{_libdir}/*.lib
%{_mandir}/man3/*
%{_infodir}/readline.info*

%files static
%defattr(-,root,root,-)
%{_libdir}/*_s.a

%changelog
