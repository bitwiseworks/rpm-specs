Name:           lzip
Version:        1.24
Release:        3%{?dist}
Summary:        LZMA compressor with integrity checking

License:        GPL-3.0-or-later
URL:            http://www.nongnu.org/lzip/lzip.html
%if 0%{?os2_version}
Vendor:         TeLLie OS2 forever
Distribution:   OS/2
Packager:       TeLLeRBoP
%endif
%if !0%{?os2_version}
Source0:        http://download.savannah.gnu.org/releases/lzip/lzip-%{version}.tar.gz
Source1:        http://download.savannah.gnu.org/releases/lzip/lzip-%{version}.tar.gz.sig
%else
%scm_source github https://github.com/Tellie/%{name}-os2 %{version}-os2-1
%endif
BuildRequires: make
BuildRequires:  gcc-c++

%description
Lzip compresses data using LZMA (Lempel-Ziv-Markov chain-Algorithm). It
supports integrity checking using CRC (Cyclic Redundancy Check). To archive
multiple files, tar can be used with lzip. Please note, that the lzip file
format (.lz) is not compatible with the lzma file format (.lzma).


%prep
%if !0%{?os2_version}
%setup -q
# file needs to be copied, because it is used in "make check"
cp -a COPYING{,.txt}
%else
%scm_setup
cp -a COPYING COPYING.txt
%endif
# convert CRLF to LF
sed -i 's/\r//' COPYING.txt 


%build
%configure CXXFLAGS="%{build_cxxflags}" LDFLAGS="%{build_ldflags}"

%make_build


%install
%make_install install-man

# if install-info is present, this is created by upstream's makefile
rm -Rf $RPM_BUILD_ROOT%{_infodir}/dir

%check
make check

%files
%license COPYING.txt
# TODO is currently empty
%doc AUTHORS ChangeLog NEWS README
%if !0%{?os2_version}
%{_bindir}/lzip
%else
%{_bindir}/lzip.exe
%endif
%{_infodir}/lzip.info*
%{_mandir}/man1/lzip.1*


%changelog
* Fri Feb 02 2024 Elbert Pol <elbert.pol@gmail.com> - 1.24-3
- Update makefile.in and configure the right OS2 way, Thankz to Silvan
- Also some changes in the spec file

* Wed Jan 31 2024 Elbert Pol <elbert.pol@gmail.com> - 1.24-2
- Remove unneeded prefix

* Wed Jan 31 2024 Elbert Pol <elbert.pol@gmail.com> - 1.24-1
- Updated to latest version
- resynced with latest fedora spec file

* Fri Feb 4 2022 Elbert Pol <elbert.pol@gmail.com> - 1.23 - 1
- Update to latest version

* Sun Jan 10 2021 Elbert Pol <elbert.pol@gmail.com> - 1.22 - 1
- Update to latest version

* Thu Jan 31 2019 Elbert Pol <elbert.pol@gmail.com> - 1.21-2
- Upload src to github

* Sun Jan 13 2019 Elbert Pol <elbert.pol@gmail.com> 1.21-1
- Updated to latest source

* Sat Sep 08 2018 Elbert Pol <elbert.pol@gmail.com> 1.20-2
- Fix error about infodir

* Fri Sep 07 2018 Elbert Pol <elbert.pol@gmail.com> 1.20-1
- First OS/2 rpm release
