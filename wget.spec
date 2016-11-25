#define svn_url     e:/trees/wget/trunk
%define svn_url     http://svn.netlabs.org/repos/ports/wget/trunk
%define svn_rev     1807


Summary: A utility for retrieving files using the HTTP or FTP protocols
Name: wget
Version: 1.18
Release: 2%{?dist}
License: GPLv3+
Group: Applications/Internet
Url: http://www.gnu.org/software/wget/
Vendor:  bww bitwise works GmbH
Source:  %{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip


Provides: webclient
Requires: libcx >= 0.4
#Requires(post): /sbin/install-info
#Requires(preun): /sbin/install-info
# needed for test suite
#BuildRequires: perl-HTTP-Daemon, python2
BuildRequires: openssl-devel, pkgconfig, texinfo
BuildRequires: gettext >= 0.19, autoconf
BuildRequires: libidn-devel, libpsl-devel
#BuildRequires: libuuid-devel, libmetalink-devel, perl-podlators
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
GNU Wget is a file retrieval utility which can use either the HTTP or
FTP protocols. Wget features include the ability to work in the
background while you are logged out, recursive retrieval of
directories, file name wildcard matching, remote file timestamp
storage and comparison, use of Rest with FTP servers and Range with
HTTP servers to retrieve files over slow or unstable connections,
support for Proxy servers, and configurability.


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
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
#    --with-metalink
%configure \
    --with-ssl=openssl \
    --with-openssl \
    --with-libpsl \
    --enable-largefile \
    --enable-opie \
    --enable-digest \
    --enable-ntlm \
    --enable-nls \
    --disable-rpath

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT CFLAGS="$RPM_OPT_FLAGS"
rm -f $RPM_BUILD_ROOT/%{_infodir}/dir

%find_lang %{name}


%check
#make check


%post
#/sbin/install-info %{_infodir}/wget.info.gz %{_infodir}/dir || :


%preun
#if [ "$1" = 0 ]; then
#    /sbin/install-info --delete %{_infodir}/wget.info.gz %{_infodir}/dir || :
#fi


%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS MAILING-LIST NEWS README COPYING doc/sample.wgetrc
%config(noreplace) %{_sysconfdir}/wgetrc
#{_mandir}/man1/wget.*
%{_bindir}/wget.exe
%{_infodir}/*

%changelog
* Fri Nov 25 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.18-2
- enable libidn and libpsl

* Mon Nov 14 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.18-1
- Initial version 1.18