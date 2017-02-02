%define svn_url     http://svn.netlabs.org/repos/ports/libvpx/trunk
%define svn_rev     1355

Name: libvpx
Summary: VP8 Video Codec SDK
Version: 1.4.0
Release: 2%{?dist}
License: BSD
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Source0: %{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip
URL: http://www.webmproject.org/tools/vp8-sdk/
BuildRequires:  nasm
BuildRequires:  libgcc1, pthread-devel
#BuildRequires: doxygen, php-cli

%description
libvpx provides the VP8 SDK, which allows you to integrate your applications
with the VP8 video codec, a high quality, royalty free, open source codec
deployed on millions of computers and devices worldwide.

%package devel
Summary: Development files for libvpx
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
Development libraries and headers for developing software against
libvpx.

%debug_package

%prep
# %setup -q

%if %{?svn_rev:%(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')}%{!?svn_rev):0}
%setup -q
%else
%setup -n "%{name}-%{version}" -Tc
svn export %{?svn_rev:-r %{svn_rev}} %{svn_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip" "%{name}-%{version}")
%endif

%build
%ifarch %{ix86}
%global vpxtarget x86-os2-gcc
%else
%ifarch x86_64
%global vpxtarget x86_64-os2-gcc
%else
%global vpxtarget generic-gnu
%endif
%endif

export LDFLAGS="-Zomf -Zhigh-mem" \
       ASFLAGS="-g -f aout" AS=nasm

./configure \
	--extra-cflags="%{optflags}" \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--target=%{vpxtarget} \
	--disable-install-srcs \
	--enable-vp8 \
	--enable-vp9 \
	--enable-postproc \
	--enable-onthefly-bitpacking \
	--enable-multi-res-encoding \
	--enable-runtime-cpu-detect \
	--enable-postproc-visualizer \
	--enable-error-concealment \
	--disable-examples \
	--disable-install-docs \
	--enable-pic \
	--enable-shared \
	--enable-small

%{__make} %{?_smp_mflags} verbose=true target=libs

%install
rm -rf $RPM_BUILD_ROOT
%{__make} DIST_DIR=%{buildroot}%{_prefix} install
mkdir -p %{buildroot}%{_includedir}/vpx/
# No static library
rm -rf %{buildroot}%{_libdir}/libvpx.a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc AUTHORS CHANGELOG LICENSE README PATENTS
%{_libdir}/libvpx2.dll

%files devel
%defattr(-,root,root,-)
# These are SDK docs, not really useful to an end-user.
#%doc docs/
%{_includedir}/vpx/
%{_libdir}/pkgconfig/vpx.pc
%{_libdir}/libvpx*.a

%changelog
* Fri Feb 3 2017 Dmitriy Kuminov <coding@dmik.org> 1.4.0-2
- Use -Zomf to preserve HLL debug info and significantly reduce DLL size.
- Use per-platform optimization flags.
- Remove static library and OMF libraries.

* Tue Nov 17 2015 Valery Sedletski <_valerius@mail.ru> 1.4.0-1
- initial OS/2 build
