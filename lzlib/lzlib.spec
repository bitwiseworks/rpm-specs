Name:           lzlib
Version:        1.12
Release:	1%{?dist}
Summary:        LZMA Compression and Decompression Library
License:        GPL-2.0+
Group:          Development/Libraries/C and C++
Url:            http://www.nongnu.org/lzip/lzlib.html
%scm_source github http://github.com/TeLLie/%{name}-os2 %{version}-os2
%if !0%{?os2_version}
Source3:        %name.keyring
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description 
The lzlib compression library provides in-memory LZMA compression and
decompression functions, including integrity checking of the
decompressed data. The compressed data format used by the library is
the lzip format.

%package devel
Summary:        LZMA Compression and Decompression Library
Group:          Development/Libraries/C and C++
Obsoletes:      lzlib-devel < %version-%release
Provides:       lzlib-devel = %version-%release

%description devel
The lzlib compression library provides in-memory LZMA compression and
decompression functions, including integrity checking of the
decompressed data. The compressed data format used by the library is
the lzip format.

This subpackage contains libraries and header files for developing
applications that want to make use of libcerror.

%prep
%scm_setup

%build
# not autoconf!
# don't use the configure macro here, as it will cause the configure script to
# skip parameters as soon as it encounters one that it doesn't understand
./configure  LDFLAGS="-Zomf -Zexe" LIBS="-lcx" \
   --prefix="%{_prefix}" \
   --bindir="%{_bindir}" \
   --includedir="%{_includedir}" \
   --infodir="%{_infodir}" \
   --libdir="%{_libdir}" \
   --mandir="%{_mandir}" 
        
make %{?_smp_flags}

%install
make DESTDIR="%{buildroot}" LDCONFIG=echo install
%if !0%{?os2_version}
# configure had no --disable-static
#rm -f "%buildroot/%_libdir"/*.a
%endif

%check
make -k check

%post devel
%if !0%{?os2_version}
%install_info --info-dir="%_infodir" "%_infodir/%name.info%ext_info"
%endif

%postun devel
%if !0%{?os2_version}
%install_info_delete --info-dir="%_infodir" "%_infodir/%name.info"
%endif

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING NEWS README

%files devel
%defattr(-,root,root)
%{_includedir}/lzlib.h
%{_libdir}/liblz.a
%exclude /@unixroot/usr/share/info/dir
%if !0%{?os2_version}
%{_infodir}/*.info*
%endif
%doc %{_infodir}/lzlib.info*

%changelog
* Wed Jan 06 2021 Elbert Pol <elbert.pol@gmail.com> - 1.12 - 1
- Updated to latest version

* Sun Feb 03 2019 Elbert Pol <elbert.pol@gmail.com> - 1.11-4
- Fix for the Transaction Check Error

* Thu Jan 31 2019 Elbert Pol <elbert.pol@gmail.com> - 1.11-3
- Upload src to github

* Sun Jan 13 2019 Elbert Pol <elbert.pol@gmail.com> - 1.11-2
- Fix error about info

* Sat Jan  12 2019 Elbert Pol <elbert.pol@gmail.com> - 1.11-1
- First Rpm version OS/2
