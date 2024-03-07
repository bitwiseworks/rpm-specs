Name:		jansson
Version:	2.13.1
Release:	2%{?dist}
Summary:	C library for encoding, decoding and manipulating JSON data

License:	MIT
URL:		http://www.digip.org/jansson/
%if !0%{?os2_version}
Source0:	http://www.digip.org/jansson/releases/jansson-%{version}.tar.bz2
%else
%scm_source github https://github.com/TesphinxLLie/jansson-os2 %{version}-os2
%endif

# Fix docs build failures with Sphinx 3
# Resolved upstream: https://github.com/akheron/jansson/pull/543
%if !0%{?os2_version}
Patch0:     fix-docs-build-with-sphinx-3.patch
BuildRequires:	python3-sphinx
%endif

BuildRequires:	gcc


%description
Small library for parsing and writing JSON documents.

%package devel
Summary: Header files for jansson
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Header files for developing applications making use of jansson.

%package devel-doc
Summary: Development documentation for jansson
BuildArch: noarch

%description devel-doc
Development documentation for jansson.

%debug_package

%prep

%if !0%{?os2_version}
%autosetup -p1
%else
%scm_setup
%endif

%if 0%{?rhel} == 6
%{__sed} -i 's/code-block:: shell/code-block:: none/g' doc/*.rst
%endif

%build
autoreconf -ifv
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"

%configure --disable-static
%if !0%{?os2_version}
%make_build
make html
%else
make %{?_smp_mflags}
%endif

%check
%if !0%{?os2_version}
make check
%endif

%install
%make_install
rm "$RPM_BUILD_ROOT%{_libdir}"/*.la

%if !0%{?os2_version}
%ldconfig_scriptlets
%endif

%files
%license LICENSE
%doc CHANGES
%if !0%{?os2_version}
%{_libdir}/*.so.*
%else
%{_libdir}/*.dll
%endif

%files devel
%if !0%{?os2_version}
%{_libdir}/*.so
%else
%{_libdir}/*.a
%endif
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/*

%files devel-doc
%if !0%{?os2_version}
%doc doc/_build/html/*
%endif

%changelog
* Mon Oct 19 2020 Elbert Pol <elbert.pol@gmail.com> - 2.13.1-2
- fix a  version number in changelog
- Forget to add older changelog

* Thu Oct 15 2020 Elbert Pol <elbert.pol@gmail.com> - 2.13.1-1
- Updated to latest version

* Mon Nov 19 2018 Elbert Pol <elbert.pol@gmail.com> - 2.11-2
- first os2 rpm package
