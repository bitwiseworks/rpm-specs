Name: hunspell-fr
Summary: French hunspell dictionaries
Version: 6.0.2
Release: 1%{?dist}
Source: http://www.dicollecte.org/download/fr/hunspell-french-dictionaries-v%{version}.zip
URL: http://www.dicollecte.org/home.php?prj=fr
License: MPLv2.0
BuildArch: noarch

Requires: hunspell
Supplements: (hunspell and langpacks-fr)

%description
French (France, Belgium, etc.) hunspell dictionaries.

%prep
%setup -q -c -n hunspell-fr

%build

%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/myspell
cp -p C:/rpmbuild/BUILD/hunspell-fr/usr/share/myspell/fr_FR.dic $RPM_BUILD_ROOT/%{_datadir}/myspell/fr_FR.dic
cp -p C:/rpmbuild/BUILD/hunspell-fr/usr/share/myspell/fr_FR.aff $RPM_BUILD_ROOT/%{_datadir}/myspell/fr_FR.aff
#cp -p fr-toutesvariantes.dic $RPM_BUILD_ROOT/%{_datadir}/myspell/fr_FR.dic
#cp -p fr-toutesvariantes.aff $RPM_BUILD_ROOT/%{_datadir}/myspell/fr_FR.aff

#pushd $RPM_BUILD_ROOT/%{_datadir}/myspell/
cd $RPM_BUILD_ROOT/%{_datadir}/myspell/
fr_FR_aliases="fr_BE fr_CA fr_CH fr_LU fr_MC"
for lang in $fr_FR_aliases; do
	ln -s fr_FR.aff $lang.aff
	ln -s fr_FR.dic $lang.dic
done
#popd


%files
%doc C:/rpmbuild/BUILD/hunspell-fr/usr/share/doc/hunspell-fr/README_dict_fr.txt
%{_datadir}/myspell/*

%changelog
* Wed Apr 19 2017 Elbert Pol <elbert.pol@gmail.com> - 6.0.2-1
- First Os2 Rpm build
