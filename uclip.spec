%define svn_url     F:/rd/AOO/tools/UniClip
#define svn_url     https://svn.netlabs.org/repos/openoffice/trunk/tools/UniClip
%define svn_rev     955

%define kmk_dist out/os2.x86/release/dist

Summary: UClip, enhanced OS/2 clipboard support
Name: uclip
Version: 0.3.0
Release: 1%{?dist}
License: unknown
Group: Development/Libraries
Source: %{name}-%{version}-r%{svn_rev}.zip


%description
UClip is designed to allow OS/2 programs to exchange unicode text using the clipboard
with other native programs or with odin-ized programs.
It is compiled using Odin source code, so it shares the same clipboard formats recognized
in win32 native programs.
Note: UClip will not enable your existing OS/2 software, it will work only for programs
specifically developed with it.


%package devel
Summary: Header files developing apps which will use UClip
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
Header files and a library of UClip functions, for developing apps
which will use the library.


%debug_package


%prep
%if %(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')
%setup -q
%else
%setup -n "%{name}-%{version}" -T -c
svn export -r %{svn_rev} %{svn_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" "%{name}-%{version}")
%endif

%build
export KCFLAGS="%{optflags}"
kmk -C src

%install
rm -rf %{buildroot}

kmk -C src PATH_INS="%{buildroot}/@unixroot/usr" install

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/UClip.dll
%doc License.txt ReadMe.txt

%files devel
%defattr(-,root,root)
%{_libdir}/*.lib
%{_includedir}/*

%changelog
* Thu Mar 17 2016 yd <yd@os2power.com> 0.3.0-1
- r955, move to kmk build system.
- r954, Update code to compile with gcc 4.9.2, revert to full c++ build.
- r953, Add libwrap from current odin tree build.
- r952, Tree cleanup.
- First rpm build.
