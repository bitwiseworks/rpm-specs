Name:           lziprecover
Version:        1.25
Release:        2%{?dist}
Summary:        Data recovery tool and decompressor for files in the lzip compressed format

License:        GPLv3+
URL:            http://www.nongnu.org/lzip/lziprecover.html
%if 0%{?os2_version}
Vendor:         TeLLie OS2 forever
Distribution:   OS/2
Packager:       TeLLeRBoP
%endif
%if !0%{?os2_version}
Source0:        http://download.savannah.gnu.org/releases/lzip/lziprecover/lziprecover-%{version}.tar.lz
Source1:        http://download.savannah.gnu.org/releases/lzip/lziprecover/lziprecover-%{version}.tar.lz.sig
%else
%scm_source github http://github.com/TeLLie/%{name}-os2 %{version}-os2
%endif
BuildRequires:  lzip gcc

%if !0%{?os2_version}
Requires(post): info
Requires(preun): info
%endif

%description
Lziprecover is a data recovery tool and decompressor for files in the lzip 
compressed data format (.lz) able to repair slightly damaged files, recover 
badly damaged files from two or more copies, extract undamaged members 
from multi-member files, decompress files and test integrity of files.

Lziprecover is able to recover or decompress files produced by any of the 
compressors in the lzip family; lzip, plzip, minilzip/lzlib, clzip and 
pdlzip. This recovery capability contributes to make the lzip format one 
of the best options for long-term data archiving. 


%prep
%if !0%{?os2_version}
%setup -q
%else
%scm_setup
%endif

# file needs to be copied, because it is used in "make check"
%if !0%{?os2_version}
cp -a COPYING{,.txt}
%else
cp -a COPYING COPYING.txt
%endif
# convert CRLF to LF
sed -i 's/\r//' COPYING.txt 

%build
./configure  LDFLAGS="-Zomf -Zexe -lcx" \
    --prefix="%{_prefix}" \
    --bindir="%{_bindir}" \
    --includedir="%{_includedir}" \
    --infodir="%{_infodir}" \
    --libdir="%{_libdir}" \
    --mandir="%{_mandir}"

%make_build

%install
%if !0%{?os2_version}
make install install-man DESTDIR=$RPM_BUILD_ROOT
%else
make install INSTALL_ROOT=%{buildroot} install-man DESTDIR=$RPM_BUILD_ROOT
%endif

# if install-info is present, this is created by upstream's makefile
rm -Rf $RPM_BUILD_ROOT%{_infodir}/dir
install -Dm 0755 lziprecover.exe %{buildroot}%{_bindir}

%check
make -k check

%post
%if !0%{?os2_version}
/sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir || :
%endif

%preun
%if !0%{?os2_version}
if [ $1 = 0 ] ; then
/sbin/install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir || :
fi
%endif

%files
# TODO is currently empty
%license COPYING.txt
%doc AUTHORS ChangeLog NEWS README
%exclude /@unixroot/usr/bin/lziprecover
%if !0%{?os2_version}
%{_bindir}/%{name}
%else
%{_bindir}/%{name}.exe
%endif
%{_infodir}/lziprecover.info*
%{_mandir}/man1/lziprecover.1*

%changelog
* Tue Feb 04 2025 Elbert Pol <elbert.pol@gmail.com> - 1.25-1
- Updated to latest version

* Fri Jan 26 2024 Elbert pol <elbert.pol@gmail.com> - 1.24-1
- Update to latest version

* Fri Feb 04 2022 Elbert Pol <elbert.pol@gmail.com> - 1.23 - 1
- Update to latest version

* Wed Jan 06 2021 Elbert Pol <elbert.pol@gmail.com> - 1.22 - 1
- Update to latest version
- Finetuning the spec file

* Thu Jan 31 2019 Elbert Pol <elbert.pol@gmail.com> - 1.21-2
- Upload src to github

* Sat Jan 12 2019 Elbert Pol <elbert.pol@gmail.com> 1.21-1
- Updated to latest source

* Sun Sep 09 2018 Elbert Pol <elbert.pol@gmail.com> 1.20-2
- Some changes for Spec file

* Sun Sep 09 2018 Elbert Pol <elbert.pol@gmail.com> 1.20-1
- First OS/2 rpm release
