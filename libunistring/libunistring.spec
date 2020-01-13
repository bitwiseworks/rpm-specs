Version: 0.9.10
Release: 1%{?dist}
Name: libunistring
Summary: GNU Unicode string library
License: GPLV2+ or LGPLv3+
Url: http://www.gnu.org/software/libunistring/

Vendor:  bww bitwise works GmbH
%scm_source github http://github.com/bitwiseoworks/%{name}-os2 %{version}-os2

BuildRequires: gcc
#Provides: bundled(gnulib)

%description
This portable C library implements Unicode string types in three flavours:
(UTF-8, UTF-16, UTF-32), together with functions for character processing
(names, classifications, properties) and functions for string processing
(iteration, formatted output, width, word breaks, line breaks, normalization,
case folding and regular expressions).

%package devel
Summary: GNU Unicode string library - development files
Requires: %{name} = %{version}-%{release}

%description devel
Development files for programs using libunistring.

%debug_package

%prep
%scm_setup

%build
# we do autoreconf even fedora doesn't do it
autoreconf -fvi
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
export VENDOR="%{vendor}"
%configure --disable-static --disable-rpath
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
rm -f $RPM_BUILD_ROOT/%{_infodir}/dir
rm -f $RPM_BUILD_ROOT/%{_libdir}/%{name}.la
# Move staged docs so not picked up by %%doc in main package
mv $RPM_BUILD_ROOT%{_datadir}/doc/%{name} __doc

%files
%license COPYING COPYING.LIB
%doc AUTHORS NEWS README
%{_libdir}/*.dll

%files devel
%doc HACKING DEPENDENCIES THANKS ChangeLog
%doc __doc/*
%{_infodir}/%{name}.info*
%{_libdir}/*_dll.a
%{_includedir}/unistring
%{_includedir}/*.h

#ldconfig_scriptlets

%changelog
* Mon Jan 13 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.9.10-1
- first OS/2 rpm
