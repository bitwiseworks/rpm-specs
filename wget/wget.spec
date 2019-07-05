Summary: A utility for retrieving files using the HTTP or FTP protocols
Name: wget
Version: 1.18
Release: 3%{?dist}
License: GPLv3+
Group: Applications/Internet
Url: http://www.gnu.org/software/wget/

Vendor:  bww bitwise works GmbH
%scm_source  svn http://svn.netlabs.org/repos/ports/wget/trunk 1982


Provides: webclient
Requires: libcx >= 0.4
Requires(post): %{_sbindir}/install-info.exe
Requires(preun): %{_sbindir}/install-info.exe
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
%scm_setup

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
if [ -f %{_infodir}/wget.info.gz ]; then
  %{_sbindir}/install-info.exe %{_infodir}/wget.info.gz %{_infodir}/dir || :
fi

%preun
if [ "$1" = 0 ]; then
  if [ -f %{_infodir}/wget.info.gz ]; then
    %{_sbindir}/install-info.exe --delete %{_infodir}/wget.info.gz %{_infodir}/dir || :
  fi
fi


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
* Wed Feb 08 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.18-3
- workaround libc ticket #310 pathconf()
- use the new scm_source and scm_setup macros

* Fri Nov 25 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.18-2
- enable libidn and libpsl

* Mon Nov 14 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.18-1
- Initial version 1.18