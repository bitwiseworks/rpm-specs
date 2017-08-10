# Note: this .spec is borrowed from expat-2.1.0-10.fc22.src.rpm

Summary: An XML parser library
Name: expat
Version: 2.1.0
Release: 12%{?dist}
Group: System Environment/Libraries
#Source: http://downloads.sourceforge.net/expat/expat-%{version}.tar.gz
URL: http://www.libexpat.org/
License: MIT
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: autoconf, automake, libtool
#BuildRequires: check-devel

Vendor: bww bitwise works GmbH
%scm_source svn  http://svn.netlabs.org/repos/ports/expat/trunk 770

BuildRequires: gcc make subversion zip

%description
This is expat, the C library for parsing XML, written by James Clark. Expat
is a stream oriented XML parser. This means that you register handlers with
the parser prior to starting the parse. These handlers are called when the
parser discovers the associated structures in the document being parsed. A
start tag is an example of the kind of structures for which you may
register handlers.

%package devel
Summary: Libraries and header files to develop applications using expat
Group: Development/Libraries
Requires: expat = %{version}-%{release}

%description devel
The expat-devel package contains the libraries, include files and documentation
to develop XML applications with expat.

%package static
Summary: expat XML parser static library
Group: Development/Libraries
Requires: expat-devel%{?_isa} = %{version}-%{release}

%description static
The expat-static package contains the static version of the expat library.
Install it if you need to link statically with expat.

%debug_package

%prep
%scm_setup

# make sure configure is updated to properly support OS/2
buildconf.sh

%build
#rm -rf autom4te*.cache
#libtoolize --copy --force --automake && aclocal && autoheader && autoconf
export CFLAGS="$RPM_OPT_FLAGS"
export LDFLAGS="-Zomf -Zhigh-mem -Zargs-wild -Zargs-resp -Zbin-files"
%configure
make %{?_smp_mflags}

%install
rm -rf ${RPM_BUILD_ROOT}

rm -f examples/*.dsp examples/.cvsignore
chmod 644 README COPYING Changes doc/* examples/*

make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

#%check
#make check

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%doc README
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_bindir}/*
%{_libdir}/*.dll
%{_mandir}/*/*

%files devel
%defattr(-,root,root)
%doc Changes doc examples
%{_libdir}/*_dll.a
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*.h

%files static
%defattr(-,root,root)
%exclude %{_libdir}/*_dll.a
%{_libdir}/*.a


%changelog
* Thu Aug 10 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.1.0-12
- use scm_ macros

* Mon Sep 08 2014 yd
- added debug package with symbolic info for exceptq.

* Wed Sep 3 2014 Dmitriy Kuminov <coding@dmik.org> 2.1.0-11
- Rebuild with high memory support.

* Mon Sep 1 2014 Dmitriy Kuminov <coding@dmik.org> 2.1.0-10
- Initial package for version 2.1.0.
