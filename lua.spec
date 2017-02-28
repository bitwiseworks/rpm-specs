%global major_version 5.3

Name:           lua
Version:        %{major_version}.4
Release:        1%{?dist}
Summary:        Powerful light-weight programming language
Group:          Development/Languages
License:        MIT
URL:            http://www.lua.org/

Vendor:         bww bitwise works GmbH
%scm_source svn http://svn.netlabs.org/repos/ports/lua/trunk 2099

BuildRequires:  automake autoconf libtool readline-devel ncurses-devel
Provides:       lua(abi) = %{major_version}
Requires:       lua-libs = %{version}-%{release}

%description
Lua is a powerful light-weight programming language designed for
extending applications. Lua is also frequently used as a
general-purpose, stand-alone language. Lua is free software.
Lua combines simple procedural syntax with powerful data description
constructs based on associative arrays and extensible semantics. Lua
is dynamically typed, interpreted from bytecodes, and has automatic
memory management with garbage collection, making it ideal for
configuration, scripting, and rapid prototyping.

%package devel
Summary:        Development files for %{name}
Group:          System Environment/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description devel
This package contains development files for %{name}.

%package libs
Summary:        Libraries for %{name}

%description libs
This package contains the shared libraries for %{name}.

%package static
Summary:        Static library for %{name}
Group:          System Environment/Libraries
Requires:       %{name} = %{version}-%{release}

%description static
This package contains the static version of liblua for %{name}.

%debug_package

%prep
%scm_setup

autoreconf -fvi

%build
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"
export VENDOR="%{vendor}"

%configure --with-readline --with-compat-module
# Autotools give me a headache sometimes.
sed -i 's|@pkgdatadir@|%{_datadir}|g' src/luaconf.h.template

# hack so that only /usr/bin/lua gets linked with readline as it is the
# only one which needs this and otherwise we get License troubles
make %{?_smp_mflags} LIBS="-lm -ldl"
# only /usr/bin/lua links with readline now #luac_LDADD="liblua.la -lm -ldl"


%check
#cd ./lua-%{version}-tests/

# Removing tests that fail under mock/koji
#sed -i.orig -e '
#    /db.lua/d;
#    /errors.lua/d;
#    ' all.lua
#LD_LIBRARY_PATH=$RPM_BUILD_ROOT/%{_libdir} $RPM_BUILD_ROOT/%{_bindir}/lua -e"_U=true" all.lua

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/*.la
mkdir -p $RPM_BUILD_ROOT%{_libdir}/lua/%{major_version}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/lua/%{major_version}


%files
%{!?_licensedir:%global license %%doc}
%license mit.txt

%doc README doc/*.html doc/*.css doc/*.gif doc/*.png
%{_bindir}/lua.exe
%{_bindir}/luac.exe
%{_mandir}/man1/lua*.1*
%dir %{_libdir}/lua
%dir %{_libdir}/lua/%{major_version}
%dir %{_datadir}/lua
%dir %{_datadir}/lua/%{major_version}

%files libs
%{_libdir}/lua*.dll

%files devel
%{_includedir}/l*.h
%{_includedir}/l*.hpp
%{_libdir}/*_dll.a
%{_libdir}/pkgconfig/*.pc

%files static
%{_libdir}/lua.a


%changelog
* Tue Feb 28 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 5.3.4-1
- first rpm version
