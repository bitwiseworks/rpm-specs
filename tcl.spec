%define major 8
%define minor 5
%define majorver %{major}.%{minor}
%define	vers %{majorver}.9
%{!?sdt:%global sdt 0}

Summary: Tool Command Language, pronounced tickle
Name: tcl
Version: %{vers}
Release: 4%{?dist}
Epoch: 1
License: TCL
Group: Development/Languages
URL: http://tcl.sourceforge.net/
Vendor: bww bitwise works GmbH

%scm_source svn http://svn.netlabs.org/repos/ports/tcl/trunk 2344

Buildrequires: autoconf
Provides: tcl(abi) = %{majorver}
Obsoletes: tcl-tcldict <= %{vers}
Provides: tcl-tcldict = %{vers}

%if %sdt
BuildRequires: systemtap-sdt-devel
%endif

%description
The Tcl (Tool Command Language) provides a powerful platform for
creating integration applications that tie together diverse
applications, protocols, devices, and frameworks. When paired with the
Tk toolkit, Tcl provides a fastest and powerful way to create
cross-platform GUI applications.  Tcl can also be used for a variety
of web-related tasks and for creating powerful command languages for
applications.

%package devel
Summary: Tcl scripting language development environment
Group: Development/Languages
Requires: %{name} = %{epoch}:%{version}-%{release}

%description devel
The Tcl (Tool Command Language) provides a powerful platform for
creating integration applications that tie together diverse
applications, protocols, devices, and frameworks. When paired with the
Tk toolkit, Tcl provides a fastest and powerful way to create
cross-platform GUI applications.  Tcl can also be used for a variety
of web-related tasks and for creating powerful command languages for
applications.

The package contains the development files and man pages for tcl.

%package static
Summary: Tcl scripting language development environment
Group: Development/Languages
Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: %{name}-devel = %{epoch}:%{version}-%{release}

%description static
The Tcl (Tool Command Language) provides a powerful platform for
creating integration applications that tie together diverse
applications, protocols, devices, and frameworks. When paired with the
Tk toolkit, Tcl provides a fastest and powerful way to create
cross-platform GUI applications.  Tcl can also be used for a variety
of web-related tasks and for creating powerful command languages for
applications.

The package contains the static library in aout format.

%debug_package


%prep
%scm_setup
cd unix
autoreconf -fvi


%build
cd unix
export LDFLAGS="-Zbin-files -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
export VENDOR="%{vendor}"
%configure \
%if %sdt
    --enable-dtrace \
%endif
    --disable-shared \
    --enable-load --enable-dll-unloading

make %{?_smp_mflags} TCL_LIBRARY=%{_datadir}/%{name}%{majorver}

#%check
# don't run "make test" by default
#%{?_without_check: %define _without_check 0}
#%{!?_without_check: %define _without_check 1}
#%if ! %{_without_check}
#  make test
#%endif

%install
rm -rf $RPM_BUILD_ROOT
make install -C unix INSTALL_ROOT=$RPM_BUILD_ROOT TCL_LIBRARY=%{_datadir}/%{name}%{majorver}

cp $RPM_BUILD_ROOT%{_bindir}/tclsh%{majorver}.exe $RPM_BUILD_ROOT%{_bindir}/tclsh.exe
cp unix/tcl*.dll $RPM_BUILD_ROOT%{_libdir}
cp unix/libtcl%{majorver}_s.a $RPM_BUILD_ROOT%{_libdir}

# for linking with -lib%{name}
#ln -s lib%{name}%{majorver}.so $RPM_BUILD_ROOT%{_libdir}/lib%{name}.so

mkdir -p $RPM_BUILD_ROOT/%{_libdir}/%{name}%{majorver}

# postgresql and maybe other packages too need tclConfig.sh
# paths don't look at /usr/lib for efficiency, so we symlink into tcl8.5 for now
ln -s %{_libdir}/%{name}Config.sh $RPM_BUILD_ROOT/%{_libdir}/%{name}%{majorver}/%{name}Config.sh

#mkdir -p $RPM_BUILD_ROOT/%{_includedir}/%{name}-private/{generic,unix}
#find generic unix -name "*.h" -exec cp -p '{}' $RPM_BUILD_ROOT/%{_includedir}/%{name}-private/'{}' ';'
#( cd $RPM_BUILD_ROOT/%{_includedir}
#	for i in *.h ; do
#		[ -f $RPM_BUILD_ROOT/%{_includedir}/%{name}-private/generic/$i ] && ln -sf ../../$i $RPM_BUILD_ROOT/%{_includedir}/%{name}-private/generic ;
#	done
#)

# remove buildroot traces
sed -i -e "s|$PWD/unix|%{_libdir}|; s|$PWD|%{_includedir}/%{name}-private|" $RPM_BUILD_ROOT/%{_libdir}/%{name}Config.sh
rm -rf $RPM_BUILD_ROOT/%{_datadir}/%{name}%{majorver}/tclAppInit.c
rm -rf $RPM_BUILD_ROOT/%{_datadir}/%{name}%{majorver}/ldAix

%clean
rm -rf $RPM_BUILD_ROOT

#%post -p /sbin/ldconfig

#%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_bindir}/tclsh*
%exclude %{_bindir}/*.dbg
%{_datadir}/%{name}%{majorver}
%{_datadir}/%{name}8
%{_libdir}/%{name}%{major}%{minor}.dll
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_mandir}/mann/*
%dir %{_libdir}/%{name}%{majorver}
%doc README changes 
%doc license.terms

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/lib%{name}stub%{majorver}.a
%{_libdir}/lib%{name}%{majorver}.a
%{_libdir}/%{name}Config.sh
%{_libdir}/%{name}8.5/%{name}Config.sh

%files static
%defattr(-,root,root,-)
%{_libdir}/lib%{name}%{majorver}_s.a

%changelog
* Fri Mar 22 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> 8.5.9-4
- reworked fd handling in the mkstemp() case, to make it work
- create a nice bldlevel
- rebuild with latest scm_macros
- remove the dll from the devel rpm
- add debug package

* Tue Jun 14 2016 yd <yd@os2power.com> 8.5.9-3
- rebuild package, fixes ticket#183.
