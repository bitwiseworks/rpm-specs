%define isprerelease 0

%if %isprerelease
%define prerelease pre1
%endif

Summary: A program for synchronizing files over a network
Name: rsync
Version: 3.0.9
Release: 1%{?prerelease}%{?dist}
Group: Applications/Internet
URL: http://rsync.samba.org/
License: GPLv3+

Source0: ftp://rsync.samba.org/pub/rsync/rsync-%{version}%{?prerelease}.tar.gz


Patch0: rsync-3.0.7-buf-overflow.patch
Patch1: rsync-os2.diff

#BuildRequires: libacl-devel
#BuildRequires: libattr-devel
#BuildRequires: autoconf
BuildRequires: popt-devel

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Rsync uses a reliable algorithm to bring remote and host files into
sync very quickly. Rsync is fast because it just sends the differences
in the files over the network instead of sending the complete
files. Rsync is often used as a very powerful mirroring process or
just as a more capable replacement for the rcp command. A technical
report which describes the rsync algorithm is included in this
package.

%prep
# TAG: for pre versions use

%if %isprerelease
%setup -q -n rsync-%{version}%{?prerelease}
%setup -q -b 1 -n rsync-%{version}%{?prerelease}
%else
%setup -q
%setup -q
%endif

chmod -x support/*

%patch0 -p1 -b .buf-overflow
%patch1 -p1 -b .os2~

%build
rm -fr autom4te.cache
#autoconf
#autoheader

export CONFIG_SHELL="/bin/sh"
export LDFLAGS="-Zbin-files -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
%configure \
    --enable-xattr-support \
    "--cache-file=%{_topdir}/cache/%{name}-%{_target_cpu}.cache"

make proto
make %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall INSTALLCMD='install -p' INSTALLMAN='install -p'


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc COPYING NEWS OLDNEWS README support/ tech_report.tex
#%config(noreplace) %{_sysconfdir}/xinetd.d/%{name}
%{_bindir}/%{name}.exe
%{_mandir}/man1/%{name}.1*
%{_mandir}/man5/rsyncd.conf.5*

%changelog
