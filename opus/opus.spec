#global candidate rc2

Name:     opus
Version:  1.3.1
Release:  2%{?candidate:.%{candidate}}%{?dist}
Summary:  An audio codec for use in low-delay speech and audio communication
License:  BSD
URL:      https://www.opus-codec.org/

Vendor:   bww bitwise works GmbH
%scm_source github https://github.com/bitwiseworks/%{name}-os2 %{version}-os2
# This is the final IETF Working Group RFC
Source1:  rfc6716.txt 
Source2:  rfc8251.txt

BuildRequires: gcc
BuildRequires: doxygen

%description
The Opus codec is designed for interactive speech and audio transmission over 
the Internet. It is designed by the IETF Codec Working Group and incorporates 
technology from Skype's SILK codec and Xiph.Org's CELT codec.

%package  devel
Summary:  Development package for opus
%if !0%{?os2_version}
Requires: libogg-devel
%endif
Requires: opus = %{version}-%{release}

%description devel
Files for development with opus.

%debug_package

%prep
%scm_setup
cp %{SOURCE1} .
cp %{SOURCE2} .
echo PACKAGE_VERSION="%{version}" > package_version
autoreconf -fvi

%build
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"
export LIBS="-lcx"
%configure --enable-custom-modes --disable-static \
           --enable-hardening --enable-ambisonics

# Set BUILDLEVEL to be embedded to all DLLs built with Libtool.
export LT_BUILDLEVEL="@#%{vendor}:%{version}-%{release}#@##1## `LANG=C date +'%%d %%b %%Y %%H:%%M:%%S'`     `uname -n`::::0::"

make %{?_smp_mflags}

%install
%make_install

# Remove libtool archives
find %{buildroot} -type f -name "*.la" -delete
rm -rf %{buildroot}%{_datadir}/doc/opus/html

%check
export BEGINLIBPATH=%{_builddir}/%{buildsubdir}/.libs
make check %{?_smp_mflags} V=1

#ldconfig_scriptlets

%files
%license COPYING
%{_libdir}/opus*.dll

%files devel
%doc README doc/html rfc6716.txt rfc8251.txt
%{_includedir}/opus
%{_libdir}/*.a
%{_libdir}/pkgconfig/opus.pc
%{_datadir}/aclocal/opus.m4
%{_datadir}/man/man3/opus_*.3.gz

%changelog
* Mon Sep 07 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.3.1-2
- make sure we get the right version in the .pc file and in config.h

* Wed Apr 15 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.3.1-1
- cloned source to out github repo
- updated to latest version
- syncronized the spec with lated fedora spec
- add bldlevel info to the dll

* Mon Mar 04 2019 Elbert Pol <elbert.pol@gmail.com> - 1.3-2
- Add dll to right section

* Sun Mar 03 2019 Elbert Pol <elbert.pol@gmail.com> - 1.3-1
- first RPM release for OS2
