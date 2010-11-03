Summary: A GNU file archiving program
Name: tar
Epoch: 2
Version: 1.23
Release: 2
License: GPLv3+
Group: Applications/Archiving
URL: http://www.gnu.org/software/tar/
Source0: ftp://ftp.gnu.org/pub/gnu/tar/tar-%{version}.tar.bz2

Patch1: tar-os2.diff

#Requires: info
#BuildRequires: autoconf automake gzip texinfo gettext libacl-devel gawk rsh
BuildRequires: gettext
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
#Requires(post): /sbin/install-info
#Requires(preun): /sbin/install-info

Requires: gettext-libs

%description
The GNU tar program saves many files together in one archive and can
restore individual files (or all of the files) from that archive. Tar
can also be used to add supplemental files to an archive and to update
or list files in the archive. Tar includes multivolume support,
automatic archive compression/decompression, the ability to perform
remote archives, and the ability to perform incremental and full
backups.

If you want to use tar for remote backups, you also need to install
the rmt package.

%prep
%setup -q
%patch1 -p1 -b .os2~

#autoreconf

%build
export CONFIG_SHELL="/bin/sh"
export LDFLAGS="-Zbin-files -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lintl -lurpo"
%configure \
    --bindir=/@unixroot/bin --libexecdir=/@unixroot/sbin \
    "--cache-file=%{_topdir}/cache/%{name}.cache"
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT bindir=/@unixroot/bin libexecdir=/@unixroot/sbin install

ln -s tar.exe ${RPM_BUILD_ROOT}/@unixroot/bin/gtar.exe
rm -f $RPM_BUILD_ROOT/%{_infodir}/dir
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man1
#install -c -p -m 0644 %{SOURCE2} ${RPM_BUILD_ROOT}%{_mandir}/man1
ln -s tar.1.gz ${RPM_BUILD_ROOT}%{_mandir}/man1/gtar.1

# XXX Nuke unpackaged files.
rm -f ${RPM_BUILD_ROOT}/sbin/rmt
rm -f ${RPM_BUILD_ROOT}%{_libdir}/charset.alias

#%find_lang %name

#%check
#rm -f ${RPM_BUILD_ROOT}/test/testsuite
#make check

%clean
rm -rf ${RPM_BUILD_ROOT}

#%post
#if [ -f %{_infodir}/tar.info.gz ]; then
#   /sbin/install-info %{_infodir}/tar.info.gz %{_infodir}/dir || :
#fi

#%preun
#if [ $1 = 0 ]; then
#   if [ -f %{_infodir}/tar.info.gz ]; then
#      /sbin/install-info --delete %{_infodir}/tar.info.gz %{_infodir}/dir || :
#   fi
#fi

%files
# -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS ChangeLog ChangeLog.1 COPYING NEWS README THANKS TODO
/@unixroot/bin/*
%{_mandir}/man*/*
%{_infodir}/tar.info*
%{_usr}/share/locale/*

%changelog
