
## to bootstrap and avoid the circular dependency with ghostscript
## define this to be the ghostscript version
#define gs_bootstrap 9.10

Summary: Encoding files 
Name:    poppler-data
Version: 0.4.7
Release: 1%{?dist}

# The cMap data files installed by the poppler-data package are
# under the COPYING.adobe license
# cidToUnicode, nameToUnicode and unicodeMap data files
# are under the COPYING.gpl2 license
License: BSD and GPLv2
URL:     http://poppler.freedesktop.org/
Source0: http://poppler.freedesktop.org/poppler-data-%{version}.tar.gz
Source1: http://downloads.sourceforge.net/project/cmap.adobe/cmapresources_identity0.tar.z
# extracted from ghostscript-9.05 tarball
Source2: Identity-UTF16-H

BuildArch: noarch

%if ! 0%{?gs_bootstrap:1}
BuildRequires: ghostscript
%endif
%global gs_ver %(gs --version 2> \\dev\\nul || echo %{gs_bootstrap})
BuildRequires: pkgconfig

%description
This package consists of encoding files for poppler.  When installed,
the encoding files enables poppler to correctly render CJK and Cyrillic 
properly.

%package devel
Summary: Developer files for %{name}
Requires: %{name} = %{version}-%{release}
%description devel
%{summary}.


%prep
%setup -q -a 1

%build
# intentionally left blank

%install
export MAKESHELL="/@unixroot/usr/bin/sh.exe";
make install  DESTDIR=%{buildroot} datadir=%{_datadir}

# manually install Identity-* files
# http://bugzilla.redhat.com/842351
install -m644 -p %{SOURCE2} ai0/CMap/Identity-* %{buildroot}%{_datadir}/poppler/cMap/

# create cmap symlinks for ghostscript
mkdir -p %{buildroot}%{_datadir}/ghostscript/%{gs_ver}/Resource/CMap/
cmap_files=$(find %{buildroot}%{_datadir}/poppler/cMap/ -type f | sed -e "s|%{buildroot}%{_datadir}|../../../..|g")
cd %{buildroot}%{_datadir}/ghostscript/%{gs_ver}/Resource/CMap/
for target in ${cmap_files} ; do
ln -s $target
test -f $(basename $target)
done
#popd


%files
%doc COPYING COPYING.adobe COPYING.gpl2 README
%{_datadir}/poppler/
%dir %{_datadir}/ghostscript/%{gs_ver}
%dir %{_datadir}/ghostscript/%{gs_ver}/Resource
%{_datadir}/ghostscript/%{gs_ver}/Resource/CMap/

%files devel
%{_datadir}/pkgconfig/poppler-data.pc


%changelog
* Fri Dec 12 2014 yd
- initial unixroot build.
