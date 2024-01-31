Name:           lzip
Version:        1.23
Release:        1%{?dist}
Summary:        LZMA compressor with integrity checking

License:        GPLv3+
URL:            http://www.nongnu.org/lzip/lzip.html
%if !0%{?os2_version}
Source0:        http://download.savannah.gnu.org/releases/lzip/lzip-%{version}.tar.gz
Source1:        http://download.savannah.gnu.org/releases/lzip/lzip-%{version}.tar.gz.sig
%else
%scm_source github http://github.com/TeLLie/%{name}-os2 %{version}-os2
%endif

BuildRequires:  gcc

%if !0%{?os2_version}
Requires(post): info
Requires(preun): info
%endif

BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
Lzip compresses data using LZMA (Lempel-Ziv-Markov chain-Algorithm). It
supports integrity checking using CRC (Cyclic Redundancy Check). To archive
multiple files, tar can be used with lzip. Please note, that the lzip file
format (.lz) is not compatible with the lzma file format (.lzma).


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
./configure \
    --prefix="%{_prefix}" \
    --bindir="%{_bindir}" \
    --infodir="%{_infodir}" \
    --mandir="%{_mandir}" \
    LDFLAGS="-Zomf -Zexe" \
    LIBS="-lcx"
make %{?_smp_mflags}

%install
make install INSTALL_ROOT=%{buildroot} install-man DESTDIR=$RPM_BUILD_ROOT
mkdir -p %{buildroot}%{_bindir}
#cp D:/rpmbuild/Build/lzip-1.20/lzip.exe %{buildroot}%{_bindir}
# if install-info is present, this is created by upstream's makefile
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
install -Dm 0755 lzip.exe %{buildroot}%{_bindir}

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
%defattr(-,root,root,-)
%exclude /@unixroot/usr/bin/lzip
%license COPYING.txt
# TODO is currently empty
%doc AUTHORS ChangeLog NEWS README
%if !0%{?os2_version}
%{_bindir}/lzip
%else
%{_bindir}/lzip.exe
%{_infodir}/lzip.info*
%{_mandir}/man1/lzip.1*
%endif 

%changelog
* Fri Feb 4 2022 Elbert Pol <elbert.pol@gmail.com> - 1.23 - 1
- Update to latest version

* Sun Jan 10 2021 Elbert Pol <elbert.pol@gmail.com> - 1.22 - 1
- Update to latest version

* Thu Jan 31 2019 Elbert Pol <elbert.pol@gmail.com> - 1.21-2
- Upload src to github

Sun Jan 13 2019 Elbert Pol <elbert.pol@gmail.com> 1.21-1
- Updated to latest source

* Sat Sep 08 2018 Elbert Pol <elbert.pol@gmail.com> 1.20-2
- Fix error about infodir

* Fri Sep 07 2018 Elbert Pol <elbert.pol@gmail.com> 1.20-1
- First OS/2 rpm release
