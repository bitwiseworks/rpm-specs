
Summary: A GNU archiving program
Name: cpio
Version: 2.11
Release: 2%{?dist}
License: GPLv3+
Group: Applications/Archiving
URL: http://www.gnu.org/software/cpio/
Source: ftp://ftp.gnu.org/gnu/cpio/cpio-%{version}.tar.gz
Source1: cpio.1

Patch1: cpio-os2.diff

#Requires(post): /sbin/install-info
#Requires(preun): /sbin/install-info
#BuildRequires: texinfo, autoconf, gettext, rmt
BuildRequires: gettext
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: gettext-libs

%description
GNU cpio copies files into or out of a cpio or tar archive.  Archives
are files which contain a collection of other files plus information
about them, such as their file name, owner, timestamps, and access
permissions.  The archive can be another file on the disk, a magnetic
tape, or a pipe.  GNU cpio supports the following archive formats:  binary,
old ASCII, new ASCII, crc, HPUX binary, HPUX old ASCII, old tar and POSIX.1
tar.  By default, cpio creates binary format archives, so that they are
compatible with older cpio programs.  When it is extracting files from
archives, cpio automatically recognizes which kind of archive it is reading
and can read archives created on machines with a different byte-order.

Install cpio if you need a program to manage file archives.

%prep
%setup -q
%patch1 -p1 -b .os2~
#autoheader

%build

export CFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGEFILE64_SOURCE -pedantic -fno-strict-aliasing -Wall" ; \
export LDFLAGS="-Zbin-files -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp" ; \
export LIBS="-lintl -lurpo" ; \
%configure --with-rmt="%{_sysconfdir}/rmt" \
    "--cache-file=%{_topdir}/cache/%{name}-%{_target_cpu}.cache"

make %{?_smp_mflags}

%install
rm -rf ${RPM_BUILD_ROOT}

make DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p" install

rm -f $RPM_BUILD_ROOT%{_libexecdir}/rmt
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/*.1*
install -c -p -m 0644 %{SOURCE1} ${RPM_BUILD_ROOT}%{_mandir}/man1

rm -f $RPM_BUILD_ROOT%{_usr}/lib/charset.alias

#%find_lang %{name}

%clean
rm -rf ${RPM_BUILD_ROOT}

#%check
#rm -f ${RPM_BUILD_ROOT}/test/testsuite
#make check


#%post
#if [ -f %{_infodir}/cpio.info.gz ]; then
#	/sbin/install-info %{_infodir}/cpio.info.gz %{_infodir}/dir || :
#fi

#%preun
#if [ $1 = 0 ]; then
#	if [ -f %{_infodir}/cpio.info.gz ]; then
#		/sbin/install-info --delete %{_infodir}/cpio.info.gz %{_infodir}/dir || :
#	fi
#fi

%files
# -f %{name}.lang
%defattr(-,root,root,0755)
%doc AUTHORS ChangeLog NEWS README THANKS TODO COPYING
%{_bindir}/*
%{_mandir}/man*/*
%{_infodir}/*.info*
%{_usr}/share/locale/*

%changelog
