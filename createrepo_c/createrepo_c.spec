%global libmodulemd_version 2.3.0

%define __cmake_in_source_build 1

%global bash_completion %{_datadir}/bash-completion/completions/*

# Fedora infrastructure needs it for producing Fedora  39 and EPEL  7 repositories
# See https://github.com/rpm-software-management/createrepo_c/issues/398
%if ( 0%{?rhel} && ( 0%{?rhel} <= 7 || 0%{?rhel} >= 9 ) ) || ( 0%{?fedora} && 0%{?fedora} >= 45 ) || 0%{?os2_version}
%bcond_with drpm
%else
%bcond_without drpm
%endif

%if 0%{?rhel} || 0%{?os2_version}
%bcond_with zchunk
%else
%bcond_without zchunk
%endif

%if 0%{?rhel} && 0%{?rhel} < 8 || 0%{?os2_version}
%bcond_with libmodulemd
%else
%bcond_without libmodulemd
%endif

%if 0%{?rhel} && 0%{?rhel} <= 8
%bcond_without legacy_hashes
%else
%bcond_with legacy_hashes
%endif

%bcond_with sanitizers

Summary:        Creates a common metadata repository
Name:           createrepo_c
Version:        1.2.1
Release:        2%{?dist}
License:        GPL-2.0-or-later
%if !0%{?os2_version}
URL:            https://github.com/rpm-software-management/createrepo_c
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
%else
Vendor:         bww bitwise works GmbH
%scm_source github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2
%endif

%global epoch_dep %{?epoch:%{epoch}:}

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  bzip2-devel
BuildRequires:  doxygen
BuildRequires:  glib2-devel >= 2.22.0
BuildRequires:  libcurl-devel
BuildRequires:  libxml2-devel
BuildRequires:  openssl-devel
BuildRequires:  rpm-devel >= 4.8.0-28
BuildRequires:  sqlite-devel >= 3.6.18
BuildRequires:  xz
BuildRequires:  xz-devel
BuildRequires:  zlib-devel
%if %{with zchunk}
BuildRequires:  pkgconfig(zck) >= 0.9.11
BuildRequires:  zchunk
%endif
%if %{with libmodulemd}
BuildRequires:  pkgconfig(modulemd-2.0) >= %{libmodulemd_version}
%if 0%{?rhel} && 0%{?rhel} <= 7
BuildRequires:  libmodulemd2
Requires:       libmodulemd2%{?_isa} >= %{libmodulemd_version}
%else
BuildRequires:  libmodulemd
Requires:       libmodulemd%{?_isa} >= %{libmodulemd_version}
%endif
%endif
Requires:       %{name}-libs = %{epoch_dep}%{version}-%{release}
%if !0%{?os2_version}
%if 0%{?fedora} > 40 || 0%{?rhel} > 10
BuildRequires:  bash-completion-devel
%else
BuildRequires:  bash-completion
%endif
%endif
Requires: rpm >= 4.9.0
%if %{with drpm}
BuildRequires:  drpm-devel >= 0.4.0
%endif
# dnf supports zstd since 8.4: https://bugzilla.redhat.com/show_bug.cgi?id=1914876
BuildRequires:  pkgconfig(libzstd)

%if %{with sanitizers}
BuildRequires:  libasan
BuildRequires:  liblsan
BuildRequires:  libubsan
%endif

%if 0%{?fedora} || 0%{?rhel} > 7 || 0%{?os2_version}
Obsoletes:      createrepo < 0.11.0
Provides:       createrepo = %{epoch_dep}%{version}-%{release}
%endif

%description
C implementation of Createrepo.
A set of utilities (createrepo_c, mergerepo_c, modifyrepo_c)
for generating a common metadata repository from a directory of
rpm packages and maintaining it.

%package libs
Summary:    Library for repodata manipulation

%description libs
Libraries for applications using the createrepo_c library
for easy manipulation with a repodata.

%package devel
Summary:    Library for repodata manipulation
%if !0%{?os2_version}
Requires:   %{name}-libs%{?_isa} = %{epoch_dep}%{version}-%{release}
%else
Requires:   %{name}-libs = %{epoch_dep}%{version}-%{release}
%endif

%description devel
This package contains the createrepo_c C library and header files.
These development files are for easy manipulation with a repodata.

%package -n python3-%{name}
Summary:        Python 3 bindings for the createrepo_c library
%{?python_provide:%python_provide python3-%{name}}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if !0%{?os2_version}
BuildRequires:  python3-sphinx
%endif
Requires:       %{name}-libs = %{epoch_dep}%{version}-%{release}

%description -n python3-%{name}
Python 3 bindings for the createrepo_c library.

%if 0%{?os2_version}
%debug_package
%endif

%prep
%if !0%{?os2_version}
%autosetup -p1
%else
%scm_setup
# we need to restore the symlink, as git archive doesnt preserve it
rm -f tests/createrepo
ln -s ../src/ tests/createrepo
%endif

%py3_shebang_fix examples/python
mkdir build-py3

%build
# Build createrepo_c with Pyhon 3
%if !0%{?os2_version}
pushd build-py3
%else
cd build-py3
# !!!!! remove -Zbin-files again when rpm 4.15.0 has removed it as well !!!!
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -Zbin-files -lcx"
export VENDOR="%{vendor}"
%endif
  %cmake .. \
      -DWITH_ZCHUNK=%{?with_zchunk:ON}%{!?with_zchunk:OFF} \
      -DWITH_LIBMODULEMD=%{?with_libmodulemd:ON}%{!?with_libmodulemd:OFF} \
      -DWITH_LEGACY_HASHES=%{?with_legacy_hashes:ON}%{!?with_legacy_hashes:OFF} \
      -DENABLE_DRPM=%{?with_drpm:ON}%{!?with_drpm:OFF} \
%if 0%{?os2_version}
      -DOS2_USE_C_EMXEXP=ON \
%endif
      -DWITH_SANITIZERS=%{?with_sanitizers:ON}%{!?with_sanitizers:OFF}
  make %{?_smp_mflags} RPM_OPT_FLAGS="%{optflags}"
  # Build C documentation
  make doc-c
%if !0%{?os2_version}
popd
%else
cd ..
%endif

%check
# Run Python 3 tests
%if !0%{?os2_version}
pushd build-py3
%else
cd build-py3
%endif
  # Compile C tests
  make tests

  # Run Python 3 tests
  # one day we might have all tests running, who knows
%if !0%{?os2_version}
  make ARGS="-V" test
%endif
%if !0%{?os2_version}
popd
%else
cd ..
%endif

%install
%if !0%{?os2_version}
pushd build-py3
%else
cd build-py3
%endif
  # Install createrepo_c with Python 3
  make install DESTDIR=%{buildroot}
%if !0%{?os2_version}
popd
%else
cd ..
%endif

%if 0%{?fedora} || 0%{?rhel} > 7
ln -sr %{buildroot}%{_bindir}/createrepo_c %{buildroot}%{_bindir}/createrepo
ln -sr %{buildroot}%{_bindir}/mergerepo_c %{buildroot}%{_bindir}/mergerepo
ln -sr %{buildroot}%{_bindir}/modifyrepo_c %{buildroot}%{_bindir}/modifyrepo
%endif
%if 0%{?os2_version}
ln -sr %{buildroot}%{_bindir}/createrepo_c.exe %{buildroot}%{_bindir}/createrepo
ln -sr %{buildroot}%{_bindir}/mergerepo_c.exe %{buildroot}%{_bindir}/mergerepo
ln -sr %{buildroot}%{_bindir}/modifyrepo_c.exe %{buildroot}%{_bindir}/modifyrepo
%endif

%if 0%{?rhel} && 0%{?rhel} <= 7
%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig
%else
%if !0%{?os2_version}
%ldconfig_scriptlets libs
%endif
%endif

%files
%doc README.md
%{_mandir}/man8/createrepo_c.8*
%{_mandir}/man8/mergerepo_c.8*
%{_mandir}/man8/modifyrepo_c.8*
%{_mandir}/man8/sqliterepo_c.8*
%if !0%{?os2_version}
%{bash_completion}
%{_bindir}/createrepo_c
%{_bindir}/mergerepo_c
%{_bindir}/modifyrepo_c
%{_bindir}/sqliterepo_c
%else
%{_bindir}/createrepo_c.exe
%{_bindir}/mergerepo_c.exe
%{_bindir}/modifyrepo_c.exe
%{_bindir}/sqliterepo_c.exe
%endif

%if 0%{?fedora} || 0%{?rhel} > 7 || 0%{?os2_version}
%{_bindir}/createrepo
%{_bindir}/mergerepo
%{_bindir}/modifyrepo
%endif

%files libs
%license COPYING
%if !0%{?os2_version}
%{_libdir}/lib%{name}.so.*
%else
%{_libdir}/*.dll
%endif

%files devel
%doc build-py3/doc/html
%if !0%{?os2_version}
%{_libdir}/lib%{name}.so
%else
%{_libdir}/*_dll.a
%endif
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/%{name}/

%files -n python3-%{name}
%doc examples/python/*
%{python3_sitearch}/%{name}/
%{python3_sitearch}/%{name}-%{version}-py%{python3_version}.egg-info

%changelog
* Fri May 16 2025 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.2.1-2
- rebuild with python 3.13

* Wed Apr 30 2025 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.2.1-1
- update to version 1.2.1

* Fri Dec 15 2023 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.0.2-1
- update to version 1.0.2
- enable python3
- merge with latest fedora spec

* Thu Sep 23 2021 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.17.3-2
- add -Zbin-files, as the rpm dll need it. which is a rpm dll flaw!!!

* Wed Jul 14 2021 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.17.3-1
- first OS/2 rpm
