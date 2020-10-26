
# enable bootstrap mode (e.g. disables doc generation)
#global bootstrap 1

Name:           libtheora
Epoch:          1
Version:        1.1.1
Release:        1%{?dist}
Summary:        Theora Video Compression Codec
License:        BSD
URL:            http://www.theora.org
%scm_source github http://github.com/bitwiseworks/theora-os2 %{version}-os2
Vendor:		bww bitwise works GmbH

BuildRequires:  autoconf automake libtool
BuildRequires:  libogg-devel >= 2:1.1
BuildRequires:  libvorbis-devel
BuildRequires:  SDL-devel libpng-devel
%if 0%{?bootstrap}
Obsoletes: %{name}-devel-docs < %{epoch}:%{version}-%{release}
%else
BuildRequires:  doxygen
BuildRequires:  transfig
%if !0%{?os2_version}
BuildRequires:  tetex-latex
%endif
%endif

%description
Theora is Xiph.Org's first publicly released video codec, intended
for use within the Ogg's project's Ogg multimedia streaming system.
Theora is derived directly from On2's VP3 codec; Currently the two are
nearly identical, varying only in encapsulating decoder tables in the
bitstream headers, but Theora will make use of this extra freedom
in the future to improve over what is possible with VP3.


%package devel
Summary:        Development tools for Theora applications
Requires:       libogg-devel >= 2:1.1
Requires:       %{name} = %{epoch}:%{version}-%{release}
# the new experimental decoder is now part of the regular libtheora
# we do not obsolete theora-exp itself as that had a different soname and we
# do not want to break deps, however we do now provide the same headers as
# theora-exp-devel did.
Obsoletes:      theora-exp-devel
Provides:       theora-exp-devel

%description devel
The libtheora-devel package contains the header files needed to develop
applications with libtheora.


%package devel-docs
Summary:        Documentation for developing Theora applications
BuildArch:      noarch

%description devel-docs
The libtheora-devel-docs package contains the documentation needed
to develop applications with libtheora.


%package -n theora-tools
Summary:        Command line tools for Theora videos
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description -n theora-tools
The theora-tools package contains simple command line tools for use
with theora bitstreams.


%debug_package


%prep
%scm_setup

# no custom CFLAGS please
%if !0%{?os2_version}
sed -i 's/CFLAGS="$CFLAGS $cflags_save"/CFLAGS="$cflags_save"/g' configure
%endif

# Update config.guess/sub to fix builds on new architectures (aarch64/ppc64le)
%if !0%{?os2_version}
cp /usr/lib/rpm/config.* .
%endif

%build
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"
export LIBS="-lcx"

%if !0%{?os2_version}
autogen.sh
%else
autoreconf -fvi -I m4
%endif
%configure --enable-shared --disable-static

# Set BUILDLEVEL to be embedded to all DLLs built with Libtool.
export LT_BUILDLEVEL="@#%{vendor}:%{version}-%{release}#@##1## `LANG=C date +'%%d %%b %%Y %%H:%%M:%%S'`     `uname -n`::::0::"

# Don't use rpath!
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}

%if ! 0%{?bootstrap}
make -C doc/spec %{?_smp_mflags}
%endif


%install
%make_install

rm $RPM_BUILD_ROOT/%{_libdir}/*.la
rm -r $RPM_BUILD_ROOT/%{_docdir}/*

mkdir -p $RPM_BUILD_ROOT/%{_bindir}
install -m 755 examples/dump_video.exe $RPM_BUILD_ROOT/%{_bindir}/theora_dump_video.exe
install -m 755 examples/encoder_example.exe $RPM_BUILD_ROOT/%{_bindir}/theora_encode.exe
%if !0%{?os2_version}
install -m 755 examples/player_example.exe $RPM_BUILD_ROOT/%{_bindir}/theora_player.exe
%endif
install -m 755 examples/png2theora.exe $RPM_BUILD_ROOT/%{_bindir}/png2theora.exe


%if !0%{?os2_version}
%ldconfig_scriptlets
%endif


%files
%doc README COPYING
%{_libdir}/*.dll

%files devel
%{_includedir}/theora
%{_libdir}/*_dll.a
%{_libdir}/pkgconfig/theora*.pc

%if ! 0%{?bootstrap}
%files devel-docs
%doc doc/libtheora/html doc/vp3-format.txt
%if !0%{?os2_version}
%doc doc/spec/Theora.pdf
%endif
%doc doc/color.html doc/draft-ietf-avt-rtp-theora-00.txt
%endif

%files -n theora-tools
%{_bindir}/*
%exclude %{_bindir}/*.dbg

%changelog
* Fri May 01 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.1.1-1
- first OS/2 rpm
