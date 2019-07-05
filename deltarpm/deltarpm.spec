%bcond_with python3

Name:           deltarpm
Summary:        Create deltas between rpms
Version:        3.6
Release:        1%{?dist}
License:        BSD
URL:            http://gitorious.org/deltarpm/deltarpm

Vendor:         bww bitwise works GmbH
%scm_source  svn http://svn.netlabs.org/repos/ports/deltarpm/trunk 2264

BuildRequires:  gcc
BuildRequires:  bzip2-devel
BuildRequires:  perl-generators
BuildRequires:  xz-devel
BuildRequires:  rpm-devel
BuildRequires:  popt-devel
BuildRequires:  zlib-devel
BuildRequires:  python2-devel

%description
A deltarpm contains the difference between an old
and a new version of a rpm, which makes it possible
to recreate the new rpm from the deltarpm and the old
one. You don't have to have a copy of the old rpm,
deltarpms can also work with installed rpms.

%package -n drpmsync
Summary:        Sync a file tree with deltarpms
Requires:       %{name}%{_isa} = %{version}-%{release}

%description -n drpmsync
This package contains a tool to sync a file tree with
deltarpms.

%package -n deltaiso
Summary:        Create deltas between isos containing rpms
Requires:       %{name}%{_isa} = %{version}-%{release}

%description -n deltaiso
This package contains tools for creating and using deltasisos,
a difference between an old and a new iso containing rpms.

%package -n python2-%{name}
Summary:        Python bindings for deltarpm
%{?python_provide:%python_provide python2-%{name}}
BuildRequires:  python2-devel
Requires:       %{name}%{_isa} = %{version}-%{release}

%description -n python2-%{name}
This package contains python bindings for deltarpm.

Python 2 version.

%if 0%{?with_python3}
%package -n python3-%{name}
Summary:        Python bindings for deltarpm
%{?python_provide:%python_provide python3-%{name}}
BuildRequires:  python3-devel
Requires:       %{name}%{_isa} = %{version}-%{release}

%description -n python3-%{name}
This package contains python bindings for deltarpm.

Python 3 version.
%endif

%debug_package

%prep
%scm_setup

%build
export LDFLAGS="-Zomf -Zhigh-mem -lcx %{?__global_ldflags}"
export CFLAGS="%{optflags}"
export VENDOR="%{vendor}"

%{__make} %{?_smp_mflags} \
    bindir=%{_bindir} libdir=%{_libdir} mandir=%{_mandir} prefix=%{_prefix} \
    zlibbundled='' zlibldflags='-lz' zlibcppflags=''
%{__make} %{?_smp_mflags} \
    bindir=%{_bindir} libdir=%{_libdir} mandir=%{_mandir} prefix=%{_prefix} \
    zlibbundled='' zlibldflags='-lz' zlibcppflags='' \
    python

%install
%make_install pylibprefix=%{python2_sitearch} bindir=%{_bindir} libdir=%{_libdir} mandir=%{_mandir} prefix=%{_prefix}

%if %{with python3}
# nothing to do
%else
rm -rf %{buildroot}%{_libdir}/python3*
ln -sf %{python2_sitearch}/_deltrpm.pyd $RPM_BUILD_ROOT%{python2_sitearch}/_%{name}module.pyd
%endif

%files
%license LICENSE.BSD
%doc README NEWS
%{_bindir}/applydeltarpm.exe
%{_mandir}/man8/applydeltarpm.8*
%{_bindir}/combinedeltarpm.exe
%{_mandir}/man8/combinedeltarpm.8*
%{_bindir}/makedeltarpm.exe
%{_mandir}/man8/makedeltarpm.8*
%{_bindir}/rpmdumpheader.exe

%files -n deltaiso
%{_bindir}/applydeltaiso.exe
%{_mandir}/man8/applydeltaiso.8*
%{_bindir}/fragiso.exe
%{_mandir}/man8/fragiso.8*
%{_bindir}/makedeltaiso.exe
%{_mandir}/man8/makedeltaiso.8*

%files -n drpmsync
%{_bindir}/drpmsync
%{_mandir}/man8/drpmsync.8*

%files -n python2-%{name}
%{python2_sitearch}/%{name}.py*
%{python2_sitearch}/_%{name}module.pyd
%{python2_sitearch}/_deltrpm.pyd

%if %{with python3}
%files -n python3-%{name}
%{python3_sitearch}/%{name}.py
%{python3_sitearch}/_%{name}module.so
%{python3_sitearch}/__pycache__/%{name}.*
%endif

%changelog
* Mon Dec 18 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.6-1
- initial rpm version
