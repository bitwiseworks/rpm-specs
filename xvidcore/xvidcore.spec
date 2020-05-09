#global pre -rc1

Name:           xvidcore
Version:        1.3.7
Release:        1%{?dist}
Summary:        MPEG-4 Simple and Advanced Simple Profile codec
License:        GPLv2+
URL:            https://www.xvid.com/
Vendor:         bww bitwise works GmbH
%scm_source     github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2


BuildRequires:  gcc
%ifarch %{ix86} x86_64
BuildRequires:  nasm >= 2.0
%endif

%description
The Xvid video codec implements MPEG-4 Simple Profile and Advanced Simple
Profile standards. It permits compressing and decompressing digital video
in order to reduce the required bandwidth of video data for transmission
over computer networks or efficient storage on CDs or DVDs. Due to its
unrivalled quality Xvid has gained great popularity and is used in many
other GPLed applications, like e.g. Transcode, MEncoder, MPlayer, Xine and
many more.

%package        devel
Summary:        Development files for the Xvid video codec
Requires:       %{name}%{_isa} = %{version}-%{release}

%description    devel
This package contains header files, static library and API
documentation for the Xvid video codec.


%debug_package


%prep
%scm_setup
cd build/generic
autoreconf -fvi
cd ..
cd ..

chmod -x examples/*.pl
# Convert to utf-8
for file in AUTHORS ChangeLog; do
    iconv -f ISO-8859-1 -t UTF-8 -o $file.new $file && \
    touch -r $file $file.new && \
    mv $file.new $file
done
# Fix rpmlint wrong-file-end-of-line-encoding
for file in ChangeLog; do
 sed "s|\r||g" $file > $file.new && \
 touch -r $file $file.new && \
 mv $file.new $file
done
# Yes, we want to see the build output.
%{__sed} -i -e 's|@$(|$(|g' build/generic/Makefile
# Fix permissions
%{__sed} -i -e 's|644 $(BUILD_DIR)/$(SHARED_LIB)|755 $(BUILD_DIR)/$(SHARED_LIB)|g' build/generic/Makefile

%build
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"
cd build/generic
%configure
make


%install
%make_install -C build/generic
find %{buildroot} -name "xvidcore.a" -delete


%if !0%{?os2_version}
%ldconfig_scriptlets
%endif


%files
%doc README AUTHORS ChangeLog
%license LICENSE
%{_libdir}/*.dll

%files devel
%doc CodingStyle TODO examples/
%{_includedir}/xvid.h
%{_libdir}/*_dll.a


%changelog
* Sat May 09 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.3.7-1
- Initial OS/2 RPM release.
