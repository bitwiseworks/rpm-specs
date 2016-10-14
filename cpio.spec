#define svn_url     e:/trees/cpio/trunk
%define svn_url     http://svn.netlabs.org/repos/ports/cpio/trunk
%define svn_rev     1750

Summary: A GNU archiving program
Name: cpio
Version: 2.11
Release: 5%{?dist}
License: GPLv3+
Group: Applications/Archiving
URL: http://www.gnu.org/software/cpio/
Vendor:  bww bitwise works GmbH
Source:  %{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip

#Requires(post): /sbin/install-info
#Requires(preun): /sbin/install-info
BuildRequires: texinfo, autoconf, gettext
#BuildRequires: rmt
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

%debug_package


%prep
%if %{?svn_rev:%(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')}%{!?svn_rev):0}
%setup -q
%else
%setup -n "%{name}-%{version}" -Tc
svn export %{?svn_rev:-r %{svn_rev}} %{svn_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip" "%{name}-%{version}")
%endif

autoreconf -fvi

%build
export LDFLAGS="-Zbin-files -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
%configure --with-rmt="%{_sysconfdir}/rmt"

make %{?_smp_mflags}

%install
rm -rf ${RPM_BUILD_ROOT}

make DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p" install

rm -f $RPM_BUILD_ROOT%{_libexecdir}/rmt
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%find_lang %{name}

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

%files -f %{name}.lang
%defattr(-,root,root,0755)
%doc AUTHORS ChangeLog NEWS README THANKS TODO COPYING
%{_bindir}/*.exe
%{_mandir}/man*/*
%{_infodir}/*.info*
%{_usr}/share/locale/*

%changelog
* Fri Oct 14 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.11-5
- add debug package
- adapt to latest toolchain
- fixed utimes usage
- rolled back r164 partially

* Mon Dec 03 2012 yd
- remove file name ending \r due to binary stdin. fixes ticket:16.
