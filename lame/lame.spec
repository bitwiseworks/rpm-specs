Name:           lame
Version:        3.100
Release:        1%{?dist}
Summary:        Free MP3 audio compressor

License:        GPLv2+
URL:            http://lame.sourceforge.net/
%scm_source github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2
Vendor:		bww bitwise works GmbH

BuildRequires:  gcc
BuildRequires:  ncurses-devel
%ifarch %{ix86}
BuildRequires:  nasm
%endif
Requires:       %{name}-libs = %{version}-%{release}
%if 0%{?fedora} >= 32 || 0%{?rhel} >= 8
Obsoletes:      %{name}-mp3x < 3.100-7
%endif

%description
LAME is an open source MP3 encoder whose quality and speed matches
commercial encoders. LAME handles MPEG1,2 and 2.5 layer III encoding
with both constant and variable bitrates.

%package        libs
Summary:        LAME MP3 encoding library

%description    libs
LAME MP3 encoding library.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}-libs = %{version}-%{release}

%description    devel
This package development files for %{name}.

%if (0%{?fedora} && 0%{?fedora} < 32) || (0%{?rhel} && 0%{?rhel} < 8)
%package        mp3x
Summary:        MP3 frame analyzer
Requires:       %{name} = %{version}-%{release}
BuildRequires:  gtk+-devel

%description    mp3x
This package contains the mp3x frame analyzer.
%endif


%debug_package


%prep
%scm_setup


%build
autoreconf -fvi

export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"
export LIBS="-lcx -ltinfo"

sed -i -e 's/^\(\s*hardcode_libdir_flag_spec\s*=\).*/\1/' configure
%ifarch %{ix86}
export CFLAGS="$RPM_OPT_FLAGS -ffast-math"
#From LFS:http://www.linuxfromscratch.org/blfs/view/svn/multimedia/lame.html
export ac_cv_header_xmmintrin_h=no
%endif
%configure \
  --disable-dependency-tracking \
  --disable-static \
%ifarch %{ix86}
  --enable-nasm \
%endif
%if (0%{?fedora} && 0%{?fedora} < 32) || (0%{?rhel} && 0%{?rhel} < 8)
  --enable-mp3x \
%endif
  --enable-mp3rtp

# Set BUILDLEVEL to be embedded to all DLLs built with Libtool.
export LT_BUILDLEVEL="@#%{vendor}:%{version}-%{release}#@##1## `LANG=C date +'%%d %%b %%Y %%H:%%M:%%S'`     `uname -n`::::0::"

make %{?_smp_mflags}


%install
%make_install INSTALL="install -p"
rm -f %{buildroot}%{_libdir}/*.la
# Some apps still expect to find <lame.h>
ln -sf lame/lame.h %{buildroot}%{_includedir}/lame.h
rm -rf %{buildroot}%{_docdir}/%{name}


%check
export BEGINLIBPATH=%{_builddir}/%{buildsubdir}/libmp3lame/.libs
make test


%if !0%{?os2_version}
%ldconfig_scriptlets libs
%endif


%files
%doc README TODO USAGE doc/html/*.html
%{_bindir}/lame.exe
%{_bindir}/mp3rtp.exe
%{_mandir}/man1/lame.1*

%files libs
%doc ChangeLog
%license COPYING LICENSE
%{_libdir}/mp3lame*.dll

%files devel
%doc API HACKING STYLEGUIDE
%{_libdir}/mp3lame*_dll.a
%{_includedir}/lame
%{_includedir}/lame.h

%if (0%{?fedora} && 0%{?fedora} < 32) || (0%{?rhel} && 0%{?rhel} < 8)
%files mp3x
%{_bindir}/mp3x
%endif

%changelog
* Sat May 02 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.100-1
- first OS/2 rpm
