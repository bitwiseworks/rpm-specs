# Note: Based on http://pkgs.fedoraproject.org/cgit/rpms/libvpx.git/tree/libvpx.spec?id=f7d58329e129a2102939cc28a31afa129b5318ff

Name:			libvpx
Summary:		VP8/VP9 Video Codec SDK
Version:		1.6.1
Release:		1%{?dist}
License:		BSD
Group:			System Environment/Libraries
URL:			http://www.webmproject.org/code/
BuildRequires:		nasm
BuildRequires:		doxygen

%define svn_url     http://svn.netlabs.org/repos/ports/libvpx/trunk
%define svn_rev     1963

Source: %{name}-%{version}-r%{svn_rev}.zip

BuildRequires: gcc make subversion zip

%description
libvpx provides the VP8/VP9 SDK, which allows you to integrate your applications
with the VP8 and VP9 video codecs, high quality, royalty free, open source codecs
deployed on millions of computers and devices worldwide.

%package devel
Summary:		Development files for libvpx
Group:			Development/Libraries
Requires:		%{name} = %{version}-%{release}

%description devel
Development libraries and headers for developing software against
libvpx.

%package devel-doc
Summary:    Development documentation files for %{name}
Group:      Documentation
BuildArch:  noarch
Requires:   %{name}-devel = %{version}-%{release}

%description devel-doc
This package contains the documentation files useful for
developing applications that use %{name}.

%package utils
Summary:		VP8 utilities and tools
Group:			Development/Tools
Requires:		%{name} = %{version}-%{release}

%description utils
A selection of utilities and tools for VP8, including a sample encoder
and decoder.

%legacy_runtime_packages

%debug_package

%prep
%if %{?svn_rev:%(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')}%{!?svn_rev):0}
%setup -q
%else
%setup -n "%{name}-%{version}" -Tc
svn export %{?svn_rev:-r %{svn_rev}} %{svn_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip" "%{name}-%{version}")
%endif

%build
export LDFLAGS="-Zomf -Zmap -Zhigh-mem"

./configure \
--extra-cflags="%{optflags}" \
--enable-pic --disable-install-srcs \
--enable-vp9-decoder --enable-vp9-encoder \
--enable-experimental --enable-spatial-svc \
--enable-vp9-highbitdepth \
--enable-shared \
--prefix=%{_prefix} --libdir=%{_libdir} --size-limit=16384x16384 \

make %{?_smp_mflags} verbose=true

%install
rm -rf %{buildroot}
make DIST_DIR=%{buildroot}%{_prefix} dist

# Simpler to label the dir as %%doc (resides in the build dir).
if [ -d %{buildroot}%{_prefix}/docs ]; then
   rm -rf %{buildroot}%{_prefix}/docs
fi

(
cd %{buildroot}

# Stuff we don't need.
rm -rf .%{_prefix}/md5sums.txt ./%{_prefix}/lib/libvpx.a ./%{_prefix}/CHANGELOG ./%{_prefix}/README
# No, bad google. No treat.
mv .%{_bindir}/examples/* ./%{_bindir}
mv .%{_bindir}/tools/* ./%{_bindir}
rm -rf .%{_bindir}/examples .%{_bindir}/tools

# Rename a few examples
for f in `find .%{_bindir} -type f ! -name 'vpx*.exe' ! -name 'vp8*.exe' ! -name 'vp9*.exe'` ; do
  mv $f .%{_bindir}/vpx_${f##*/}
done
# Fix the binary permissions
chmod 755 .%{_bindir}/*
)

%clean
rm -rf $RPM_BUILD_ROOT

%files
%license LICENSE
%doc AUTHORS CHANGELOG README
%{_libdir}/libvpx4.dll

%files devel
%{_includedir}/vpx/
%{_libdir}/pkgconfig/vpx.pc
%{_libdir}/libvpx*.a

%files devel-doc
# These are SDK docs, not really useful to an end-user.
%doc docs/html/

%files utils
%{_bindir}/*.exe

%changelog
* Fri Feb 3 2017 Dmitriy Kuminov <coding@dmik.org> 1.6.1-1
- Update to version 1.6.1.
- Generate development documentation and provide it in a separate sub-package.
- Provide legacy packages with DLLs for old ABI.

* Fri Feb 3 2017 Dmitriy Kuminov <coding@dmik.org> 1.4.0-2
- Use -Zomf to preserve HLL debug info and significantly reduce DLL size.
- Use per-platform optimization flags.
- Remove static library and OMF libraries.

* Tue Nov 17 2015 Valery Sedletski <_valerius@mail.ru> - 1.4.0 OS/2 initial build
- initial OS/2 build
