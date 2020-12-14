Name:          opus-tools
Version:       0.2
Release:       1%{?dist}
Summary:       A set of tools for the opus audio codec
License:       BSD and GPLv2
URL:           http://www.opus-codec.org/
%if !0%{?os2_version}
Source0:       http://downloads.xiph.org/releases/opus/%{name}-%{version}.tar.gz
%else
Vendor:        bww bitwise works GmbH
%scm_source    github https://github.com/bitwiseworks/%{name}-os2 v%{version}-os2
%endif

BuildRequires: gcc
BuildRequires: flac-devel
BuildRequires: libogg-devel
BuildRequires: opus-devel
BuildRequires: opusfile-devel
BuildRequires: libopusenc-devel

%description
The Opus codec is designed for interactive speech and audio transmission over 
the Internet. It is designed by the IETF Codec Working Group and incorporates 
technology from Skype's SILK codec and Xiph.Org's CELT codec.

This is a set of tools for the opus codec.

%if 0%{?os2_version}
%debug_package
%endif

%prep
%if !0%{?os2_version}
%setup -q
%else
%scm_setup
echo PACKAGE_VERSION="%{version}" > package_version
autoreconf -vif
%endif

%build
%if 0%{?os2_version}
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
%endif

%configure

%if !0%{?os2_version}
%make_build
%else
make %{?_smp_mflags}
%endif

%install
%make_install

%check
make check %{?_smp_mflags} V=1

%if !0%{?os2_version}
%ldconfig_scriptlets
%endif

%files
%license COPYING
%doc AUTHORS
%{_bindir}/opus*
%if 0%{?os2_version}
%exclude %{_bindir}/opus*.dbg
%endif
%{_datadir}/man/man1/opus*

%changelog
* Tue Dec 01 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.2-1
- first OS/2 rpm
