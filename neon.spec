# $Revision: 1.101 $, $Date: 2011/05/05 07:42:12 $
#
# Conditional build:
%bcond_without	apidocs		# build and package API docs
%bcond_with	static_libs	# don't build static libraries
%bcond_with	kerberos5	# don't build Kerberos V support
%bcond_with	libproxy	# don't build libproxy support

Summary:	An HTTP and WebDAV client library
Name:		neon
Version:	0.30.0
Release:	1
License:	LGPL v2+
Group:		Libraries
# Source0:	http://www.webdav.org/neon/%{name}-%{version}.tar.gz

%define svn_url     http://svn.netlabs.org/repos/ports/neon/trunk
%define svn_rev     873

Source: %{name}-%{version}-r%{svn_rev}.zip

BuildRequires: gcc make subversion zip

# Source0-md5:	591e0c82e6979e7e615211b386b8f6bc
URL:		http://www.webdav.org/neon/

BuildRequires:	autoconf >= 2.58
BuildRequires:	automake
%{?with_kerberos5:BuildRequires:	heimdal-devel}
%{?with_libproxy:BuildRequires:	libproxy-devel}
BuildRequires:	libtool >= 2.4
BuildRequires:	expat-devel
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	pkgconfig
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
neon is an HTTP and WebDAV client library, with a C interface.
Featuring:
 - High-level interface to HTTP and WebDAV methods (PUT, GET, HEAD
   etc).
 - Low-level interface to HTTP request handling, to allow implementing
   new methods easily.
 - HTTP/1.1 and HTTP/1.0 persistent connections.
 - RFC2617 basic and digest authentication (including auth-int,
   md5-sess).
 - Proxy support (including basic/digest authentication).
 - Generic WebDAV 207 XML response handling mechanism.
 - XML parsing using the expat or libxml parsers.
 - Easy generation of error messages from 207 error responses.
 - WebDAV resource manipulation: MOVE, COPY, DELETE, MKCOL.
 - WebDAV metadata support: set and remove properties, query any set of
   properties (PROPPATCH/PROPFIND).

%package devel
Summary:	Header files for neon
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%{?with_kerberos5:Requires:	heimdal-devel}
%{?with_libproxy:Requires:	libproxy-devel}
Requires:	expat-devel
Requires:	openssl-devel >= 0.9.7c

%description devel
C header files for the neon library.

%package static
Summary:	Static libraries for neon
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static neon libraries.

%package apidocs
Summary:	neon API documentation
Group:		Documentation

%description apidocs
API and internal documentation for neon library.

%prep
%if %(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')
%setup -q
%else
%setup -n "%{name}-%{version}" -Tc
svn export -r %{svn_rev} %{svn_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" "%{name}-%{version}")
%endif

%build
export LIBS="-lpthread"
export NEON_LIBS="-lintl -lpthread"
./autogen.sh
%configure \
	--enable-shared \
	--with-ssl \
	--enable-threadsafe-ssl=posix \
	%{!?with_static_libs:--disable-static} \
	%{!?with_kerberos5:--without-gssapi} \
	%{!?with_libproxy:--without-libproxy}

%{__make} %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

#%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

#%post	-p /sbin/ldconfig
#%postun	-p /sbin/ldconfig

%files
# -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS BUGS ChangeLog NEWS README THANKS TODO
%attr(755,root,root) %{_libdir}/neon*.dll
%{_usr}/share/locale/*

%files devel
%defattr(644,root,root,755)
%doc doc/*.txt
%attr(755,root,root) %{_bindir}/neon-config
%attr(755,root,root) %{_libdir}/neon*_dll.a
%{_libdir}/libneon.la
%{_libdir}/pkgconfig/neon.pc
%{_includedir}/neon
%{_mandir}/man1/neon-config.1*
%{_mandir}/man3/ne_*.3*
%{_mandir}/man3/neon.3*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/neon_s.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/html/*
%endif

%changelog
* Tue Sep 23 2014 Silvan Scherrer <silvan.scherrer@aroa.ch> 0.30.0-1
- updated neon to 0.30.0