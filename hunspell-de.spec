Name: hunspell-de
Summary: German hunspell dictionaries
%global upstreamid 20160407
Version: 0.%{upstreamid}
Release: 1%{?dist}
Source: https://www.j3e.de/ispell/igerman98/dict/igerman98-%{upstreamid}.tar.bz2
URL: https://www.j3e.de/ispell/igerman98
License: GPLv2 or GPLv3
BuildArch: noarch
BuildRequires: aspell, hunspell, perl

Requires: hunspell
Supplements: (hunspell and langpacks-de)

%description
German (Germany, Switzerland, etc.) hunspell dictionaries.

%prep
#%setup -q -n igerman98-%{upstreamid}
%setup -q -n usr
#sed -i -e "s/AFFIX_EXPANDER = ispell/AFFIX_EXPANDER = aspell/g" Makefile

%build
chmod -x *


%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/myspell
cp -p C:/rpmbuild/BUILD/usr/share/myspell/de_DE.dic $RPM_BUILD_ROOT/%{_datadir}/myspell/de_DE.dic
cp -p C:/rpmbuild/BUILD/usr/share/myspell/de_DE.aff $RPM_BUILD_ROOT/%{_datadir}/myspell/de_DE.aff

#mkdir -p $RPM_BUILD_ROOT/%{_datadir}/myspell
#cd hunspell
#cp -p de_??.dic de_??.aff $RPM_BUILD_ROOT/%{_datadir}/myspell

#pushd $RPM_BUILD_ROOT/%{_datadir}/myspell/
cd $RPM_BUILD_ROOT/%{_datadir}/myspell/
de_DE_aliases="de_BE de_LU"
for lang in $de_DE_aliases; do
	ln -s de_DE.aff $lang.aff
	ln -s de_DE.dic $lang.dic
done
de_CH_aliases="de_LI"
for lang in $de_CH_aliases; do
	ln -s de_CH.aff $lang.aff
	ln -s de_CH.dic $lang.dic
done
#popd


%files
#%doc C:/rpmbuild/BUILD/usr/share/doc/hunspell/README_de_DE.txt hunspell/COPYING_GPLv2 hunspell/COPYING_GPLv3 hunspell/Copyright
%doc C:/rpmbuild/BUILD/usr/share/doc/hunspell-de/*.txt
%{_datadir}/myspell/*

%changelog
* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20160407-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

