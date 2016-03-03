# Add *.mymod files to the default list of files to be processed
%define _strip_opts --debuginfo -i "libvpx2.dll"
# whether to use Github, or Netlabs's svn
%define _github      0

# define _version     1.5.0
%define _version     1.4.0
%define github_name  libvpx

%if %_github
%define github_url   https://github.com/webmproject/%{github_name}/archive
%define github_rev   %{_version}
%else
%define github_url     http://svn.netlabs.org/repos/ports/libvpx/trunk
%define github_rev     1355
%endif

Name: %{github_name}
Summary: VP8 Video Codec SDK
Version: %{_version}
Release: 1%{?dist}
License: BSD
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
%if %_github
Source0: %{github_name}-%{github_rev}.zip
#Source0: http://webm.googlecode.com/files/%{name}-%{version}.tar.bz2
%else
Source0: %{name}-%{version}%{?github_rev:-r%{github_rev}}.zip
%endif
# Thanks to debian.
#Source2: libvpx.ver
Source1: donation.txt
Source2: libvpx-1.4.0.txt
Patch0: %{name}-rtcd.patch
# uncomment for version 1.4.0 or below
Patch1: %{name}-komh.patch
Patch2: %{name}-conf.patch
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

%if %_github

%if %(sh -c 'if test -f "%{_sourcedir}/%{github_name}-%{github_rev}.zip" ; then echo 1 ; else echo 0 ; fi')
%setup -n "%{github_name}-%{github_rev}" -q
%else
%setup -n "%{github_name}-%{github_rev}" -Tc
rm -f "%{_sourcedir}/%{github_name}-%{github_rev}.zip"
curl -sSL "%{github_url}/v%{github_rev}.zip" -o "%{_sourcedir}/%{github_name}-%{github_rev}.zip"
unzip -oC "%{_sourcedir}/%{github_name}-%{github_rev}.zip" -d ..
%endif

%else

%if %{?github_rev:%(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{github_rev}.zip" ; then echo 1 ; else echo 0 ; fi')}%{!?github_rev):0}
%setup -q
%else
%setup -n "%{name}-%{version}" -Tc
svn export %{?github_rev:-r %{github_rev}} %{github_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}%{?github_rev:-r%{github_rev}}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}%{?github_rev:-r%{github_rev}}.zip" "%{name}-%{version}")
%endif

%endif

#autoreconf -fi

%if %_github

%patch0 -p1
# uncomment for version 1.4.0 or below
%patch1 -p1

%patch2 -p1

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

export LDFLAGS="-Zhigh-mem -lsocket -lmmap -g" \
       CFLAGS="-g" CXXFLAGS="-g" ASFLAGS="-g -f aout" AS=nasm

./configure \
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

# Hack our optflags in.
#sed -i "s|\"vpx_config.h\"|\"vpx_config.h\" %{optflags} -fPIC|g" libs-%{vpxtarget}.mk
##sed -i "s|\"vpx_config.h\"|\"vpx_config.h\" %{optflags} -fPIC|g" examples-%{vpxtarget}.mk
#sed -i "s|\"vpx_config.h\"|\"vpx_config.h\" %{optflags} -fPIC|g" docs-%{vpxtarget}.mk

%{__make} %{?_smp_mflags} verbose=true target=libs

# Really? You couldn't make this a shared library? Ugh.
# Oh well, I'll do it for you.
#mkdir tmp
#cd tmp
#ar x ../libvpx_g.a
#cd ..
# gcc -fPIC -shared -pthread -lm -Wl,--no-undefined -Wl,-soname,libvpx.so.0 -Wl,--version-script,%{SOURCE2} -Wl,-z,noexecstack -o libvpx.so.0.0.0 tmp/*.o
#rm -rf tmp
# Temporarily dance the static libs out of the way
#mv libvpx.a libNOTvpx.a
#mv libvpx_g.a libNOTvpx_g.a
# We need to do this so the examples can link against it.
#ln -sf libvpx.so.0.0.0 libvpx.so
##make %{?_smp_mflags} verbose=true target=examples
#make %{?_smp_mflags} verbose=true target=docs
# Put them back so the install doesn't fail
#mv libNOTvpx.a libvpx.a
#mv libNOTvpx_g.a libvpx_g.a

%install
rm -rf $RPM_BUILD_ROOT
%{__make} DIST_DIR=%{buildroot}%{_prefix} install
mkdir -p %{buildroot}%{_includedir}/vpx/
#install -p libvpx.so.0.0.0 %{buildroot}%{_libdir}
#pushd %{buildroot}%{_libdir}
#ln -sf libvpx.so.0.0.0 libvpx.so
#ln -sf libvpx.so.0.0.0 libvpx.so.0
#ln -sf libvpx.so.0.0.0 libvpx.so.0.0
#popd
#pushd %{buildroot}
# Stuff we don't need.
rm -rf usr/build/ usr/md5sums.txt usr/lib*/*.a usr/CHANGELOG usr/README
#popd
emxomf -o %{buildroot}%{_libdir}/libvpx.lib %{buildroot}%{_libdir}/libvpx.a
emximp -o %{buildroot}%{_libdir}/libvpx_dll.lib %{buildroot}%{_libdir}/libvpx2.dll

%clean
rm -rf $RPM_BUILD_ROOT

#%post -p /sbin/ldconfig

#%postun -p /sbin/ldconfig

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
%{_libdir}/libvpx*.lib
#%{_libdir}/libvpx*.dbg

%changelog
* Tue Nov 17 2015 Valery Sedletski <_valerius@mail.ru> - 1.4.0 OS/2 initial build
- initial OS/2 build
