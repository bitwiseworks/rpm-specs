Name: hunspell-en
Summary: English hunspell dictionaries
%global upstreamid 20140811.1
Version: 0.%{upstreamid}
Release: 1%{?dist}
Source:  %{name}-%{version}.zip
URL: http://wordlist.sourceforge.net/
License: LGPLv2+ and LGPLv2 and BSD
BuildArch: noarch
BuildRequires: aspell, zip, dos2unix
#BuildRequires: perl-Getopt-Long
Requires: hunspell
Requires: hunspell-en-US = %{version}-%{release}
Requires: hunspell-en-GB = %{version}-%{release}
Supplements: (hunspell and langpacks-en)

%description
English (US, UK, etc.) hunspell dictionaries

%package US
Requires: hunspell
Summary: US English hunspell dictionaries

%description US
US English hunspell dictionaries

%package GB
Requires: hunspell
Summary: UK English hunspell dictionaries

%description GB
UK English hunspell dictionaries

%prep
%setup -n "%{name}-%{version}" -Tc
unzip -q %{_sourcedir}/%{name}-%{version}.zip

%build

%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/myspell
cp -p C:/rpmbuild/BUILD/hunspell-en-0.20140811.1/usr/share/myspell/en_??.dic C:/rpmbuild/BUILD/hunspell-en-0.20140811.1/usr/share/myspell/en_??.aff $RPM_BUILD_ROOT/%{_datadir}/myspell

cd $RPM_BUILD_ROOT/%{_datadir}/myspell/
en_GB_aliases="en_AG en_AU en_BS en_BW en_BZ en_DK en_GH en_HK en_IE en_IN en_JM en_MW en_NA en_NG en_NZ en_SG en_TT en_ZA en_ZM en_ZW"
for lang in $en_GB_aliases; do
	ln -s en_GB.aff $lang.aff
	ln -s en_GB.dic $lang.dic
done
en_US_aliases="en_PH"
for lang in $en_US_aliases; do
	ln -s en_US.aff $lang.aff
	ln -s en_US.dic $lang.dic
done


%files
%doc C:/rpmbuild/BUILD/hunspell-en-0.20140811.1/usr/share/doc/hunspell-en/README_en_CA.txt
%{_datadir}/myspell/*
%exclude %{_datadir}/myspell/en_GB.*
%exclude %{_datadir}/myspell/en_US.*

%files US
%doc C:/rpmbuild/BUILD/hunspell-en-0.20140811.1/usr/share/doc/hunspell-en-US/README_en_US.txt
%{_datadir}/myspell/en_US.*

%files GB
%doc C:/rpmbuild/BUILD/hunspell-en-0.20140811.1/usr/share/doc/hunspell-en-GB/README_en_GB.txt
%{_datadir}/myspell/en_GB.*

%changelog
* Sat Apr 08 2017 Elbert Pol <elbert.pol@gmail.com> - 0.20140811.1-1
- first rpm version
