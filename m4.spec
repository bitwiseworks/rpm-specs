Summary: The GNU macro processor
Name: m4
Version: 1.4.15
Release: 2%{?dist}
License: GPLv3+
Group: Applications/Text
Source: http://ftp.gnu.org/gnu/m4/m4-%{version}.tar.xz
URL: http://www.gnu.org/software/m4/

Patch0: m4-os2.diff

Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
#Requires(post): /sbin/install-info
#Requires(preun): /sbin/install-info

%description
A GNU implementation of the traditional UNIX macro processor.  M4 is
useful for writing text files which can be logically parsed, and is used
by many programs as part of their build process.  M4 has built-in
functions for including files, running shell commands, doing arithmetic,
etc.  The autoconf program needs m4 for generating configure scripts, but
not for running configure scripts.

Install m4 if you need a macro processor.

%prep
%setup -q
%patch0 -p1 -b .os2~
#chmod 644 COPYING

%build
# YD do not use -Zbin-files
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lintl -lurpo"
%configure \
        "--cache-file=%{_topdir}/cache/%{name}.cache"

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install INSTALL="%{__install} -p" DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
rm -f $RPM_BUILD_ROOT%{_libdir}/charset.alias


#%check
#make %{?_smp_mflags} check

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog NEWS README THANKS TODO
%{_bindir}/m4.exe
%{_infodir}/*
%{_mandir}/man1/m4.1*

#%post
#if [ -f %{_infodir}/m4.info ]; then # --excludedocs?
#    /sbin/install-info %{_infodir}/m4.info %{_infodir}/dir || :
#fi

#%preun
#if [ "$1" = 0 ]; then
#    if [ -f %{_infodir}/m4.info ]; then # --excludedocs?
#        /sbin/install-info --delete %{_infodir}/m4.info %{_infodir}/dir || :
#    fi
#fi

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
