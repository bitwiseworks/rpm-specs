Name: libcx
Summary: kLIBC Extension Library
Version: 0.1
Release: 1%{?dist}
License: LGPLv2.1+
Group: System/Libraries
Vendor: bww bitwise works GmbH
URL: https://github.com/bitwiseworks/libcx

%define github_name libcx
%define github_url  https://github.com/bitwiseworks/%{github_name}/archive
%define github_rev  c00f8621f6a67e8cde3e7cdb84188b66191d8678

Source: %{github_name}-%{github_rev}.zip

BuildRequires: gcc make curl zip

%description
The kLIBC Extension Library extends the functionality of the kLIBC library
by adding a number of high demand features required by modern applications.

%package devel
Summary: Development package for %{name}
Requires: %{name} = %{version}-%{release}
Requires: libc-devel
Requires: pkgconfig

%description devel
Libraries, header files and documentation for %{name}.

%debug_package

%prep
%if %(sh -c 'if test -f "%{_sourcedir}/%{github_name}-%{github_rev}.zip" ; then echo 1 ; else echo 0 ; fi')
%setup -n "%{github_name}-%{github_rev}" -q
%else
%setup -n "%{github_name}-%{github_rev}" -Tc
rm -f "%{_sourcedir}/%{github_name}-%{github_rev}.zip"
curl -sSL "%{github_url}/%{github_rev}.zip" -o "%{_sourcedir}/%{github_name}-%{github_rev}.zip"
unzip "%{_sourcedir}/%{github_name}-%{github_rev}.zip" -d ..
%endif

%define kmk_env \
    KMK_FLAGS="\
        KBUILD_VERBOSE=2 \
        BUILD_TYPE=release \
        INST_PREFIX=%{_prefix}"

%build
CFLAGS="$RPM_OPT_FLAGS"
LDFLAGS="-Zhigh-mem"
%{kmk_env}
kmk $KMK_FLAGS CFLAGS="$CFLAGS" LDFLAGS="$LDFLAGS"

%install
rm -rf %{buildroot}
%{kmk_env}
kmk $KMK_FLAGS DESTDIR="%{buildroot}" install
# Remove tests as we don't need them now
rm -rf %{buildroot}%{_bindir}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc LICENSE README.md
%{_libdir}/libcx*.dll

%files devel
%defattr(-,root,root)
%{_libdir}/libcx*.a

%changelog

* Fri Jun 10 2016 Dmitriy Kuminov <coding@dmik.org> 0.1-1
- Initial package for version 0.1.
