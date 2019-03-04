# for now we don't provide a devel, because it clashes with our libc
# after we have resolved the libc issue, we will build the devel as well
%global build_devel 0

Summary:	Character set conversion library
Name:		libiconv
Version:	1.15
Release:	1%{?dist}
License:	LGPL v2+
Group:		Libraries
URL:		https://www.gnu.org/software/libiconv/
Vendor:         bww bitwise works GmbH
%scm_source github https://github.com/bitwiseworks/%{name}-os2 %{version}-os2
#%scm_source git file://e:/Trees/libiconv/git master-os2

BuildRequires:	autoconf >= 2.60
BuildRequires:	automake
BuildRequires:	libtool

# for the password stuff, as a private repo
BuildRequires: os2-rpm-build >= 1-4

%description
This library provides an iconv() implementation, for use on systems
which don't have one, or whose implementation cannot convert from/to
Unicode.

%if %{build_devel}
%package devel
Summary:	libiconv header files
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains libiconv header files.

%package static
Summary:	libiconv static library
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
This package contains static libiconv library.
%endif


%package utils
Summary:	iconv utility
License:	GPL v3+
Group:		Applications/Text
Requires:	%{name} = %{version}-%{release}

%description utils
iconv utility.


%debug_package


%prep
%scm_setup

rm -f po/stamp-po
autoreconf -fvi

%build

export LDFLAGS=" -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
export VENDOR="%{vendor}"

%configure

%{__make}

%install
%{__make} install DESTDIR=$RPM_BUILD_ROOT

# remove not installed files
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
rm -f $RPM_BUILD_ROOT/%{_libdir}/charset.alias

# if no devel, we need to remove them
%if !%{build_devel}
rm -f $RPM_BUILD_ROOT/%{_libdir}/*_dll.a
rm -f $RPM_BUILD_ROOT/%{_includedir}/*.h
rm -f $RPM_BUILD_ROOT/%{_mandir}/man3/iconv*.3*
rm -f $RPM_BUILD_ROOT/%{_docdir}/iconv*.html
rm -f $RPM_BUILD_ROOT/%{_libdir}/charset.a
%endif


%find_lang %{name}


#post	-p /sbin/ldconfig
#postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog COPYING COPYING.LIB DEPENDENCIES DESIGN HACKING INSTALL.generic NEWS NOTES README README.djgpp README.windows THANKS
%attr(755,root,root) %{_libdir}/*.dll

%if %{build_devel}
%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*_dll.a
%{_includedir}/iconv.h
%{_includedir}/libcharset.h
%{_includedir}/localcharset.h
%{_mandir}/man3/iconv*.3*
%{_docdir}/iconv*.html

%files static
%defattr(644,root,root,755)
%{_libdir}/charset.a
%endif

%files utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/iconv.exe
%{_mandir}/man1/iconv.1*

%changelog
* Fri Nov 09 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.15-1
- first rpm version
