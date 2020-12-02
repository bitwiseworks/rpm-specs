Name:          opusfile
Version:       0.12
Release:       3%{?dist}
Summary:       A high-level API for decoding and seeking within .opus files
License:       BSD
URL:           https://www.opus-codec.org/
%if !0%{?os2_version}
Source0:       https://downloads.xiph.org/releases/opus/%{name}-%{version}.tar.gz
%else
Vendor:        bww bitwise works GmbH
%scm_source github https://github.com/bitwiseworks/%{name}-os2 %{version}-os2
%endif

BuildRequires: gcc
BuildRequires: libogg-devel
BuildRequires: openssl-devel
BuildRequires: opus-devel

%description
libopusfile provides a high-level API for decoding and seeking 
within .opus files. It includes:
* Support for all files with at least one Opus stream (including
multichannel files or Ogg files where Opus is muxed with something else).
* Full support, including seeking, for chained files.
* A simple stereo downmixing API (allowing chained files to be
decoded with a single output format, even if the channel count changes).
* Support for reading from a file, memory buffer, or over HTTP(S)
(including seeking).
* Support for both random access and streaming data sources.

%package devel
Summary: Development package for %{name}
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
Files for development with %{name}.

%debug_package

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
# Set BUILDLEVEL to be embedded to all DLLs built with Libtool.
export LT_BUILDLEVEL="@#%{vendor}:%{version}-%{release}#@##1## `LANG=C date +'%%d %%b %%Y %%H:%%M:%%S'`     `uname -n`::::0::"
%endif

%configure --disable-static

%if !0%{?os2_version}
%make_build
%else
make %{?_smp_mflags}
%endif

%install
%make_install

#Remove libtool archives.
find %{buildroot} -type f -name "*.la" -delete

%if !0%{?os2_version}
%ldconfig_scriptlets
%endif

%files
%license COPYING
%doc AUTHORS
%if !0%{?os2_version}
%{_libdir}/libopusfile.so.*
%{_libdir}/libopusurl.so.*
%else
%{_libdir}/*.dll
%endif

%files devel
%doc %{_docdir}/%{name}
%{_includedir}/opus/opus*
%{_libdir}/pkgconfig/opusfile.pc
%{_libdir}/pkgconfig/opusurl.pc
%if !0%{?os2_version}
%{_libdir}/libopusfile.so
%{_libdir}/libopusurl.so
%else
%{_libdir}/*_dll.a
%endif

%changelog
* Tue Dec 01 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.12-3
- fix spec file a bit
- add a nice buildlevel to the dll

* Tue Oct 20 2020 Elbert Pol <elbert.pol@gmail.com> - 0.12-2
- Update cause i had a wrong macros.dist

* Tue Sep 08 2020 Elbert Pol <elbert.pol@gmail.com> - 0.12-1
- First rpm for OS2

