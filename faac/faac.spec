Name:           faac
Version:        1.29.9.2
Release:        1%{?dist}
Summary:        Encoder and encoding library for MPEG2/4 AAC

License:        LGPLv2+
URL:            http://www.audiocoding.com/
#Source0:        http://downloads.sourceforge.net/sourceforge/%{name}/%{name}-%{version}.tar.gz
%scm_source github https://github.com/komh/faac-os2 master
BuildRequires:  gcc
#Patch0:         faac-1.29.9.2-drm.patch


%description
FAAC is an AAC audio encoder. It currently supports MPEG-4 LTP, MAIN and LOW
COMPLEXITY object types and MAIN and LOW MPEG-2 object types. It also supports
multichannel and gapless encoding.

%package devel
Summary:        Development libraries of the FAAC AAC encoder
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
FAAC is an AAC audio encoder. It currently supports MPEG-4 LTP, MAIN and LOW
COMPLEXITY object types and MAIN and LOW MPEG-2 object types. It also supports
multichannel and gapless encoding.

This package contains development files and documentation for libfaac.

%prep
#%setup -q
#%patch0 -p1 -b .drm
%scm_setup
autoreconf -vif
#fix encoding
#/usr/bin/iconv -f iso8859-1 -t utf-8 AUTHORS > AUTHORS.conv && touch -r AUTHORS AUTHORS.conv && /bin/mv -f AUTHORS.conv AUTHORS

%build
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
%configure --disable-static
#sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
#sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}


%install

make DESTDIR=$RPM_BUILD_ROOT install
#Remove libtool archives.
#find %buildroot -name '*.la' -or -name '*.a' | xargs rm -f
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la
#%ldconfig_scriptlets

%files
%doc AUTHORS ChangeLog NEWS README TODO docs/*
%license COPYING
%{_bindir}/*.exe
%{_libdir}/faac*.dll
%{_mandir}/man1/%{name}*

%files devel
%{_libdir}/*.a
%{_includedir}/*.h

%changelog
* Wed Oct 09 2019 Elbert Pol <elbert.pol@gmail.com> - 1.29.9.2-1
- First rpm for OS2
- Thankz KO Myung-Hun for the OS2 source

* Tue Mar 05 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.29.9.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild
