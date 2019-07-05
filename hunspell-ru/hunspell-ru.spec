Name: hunspell-ru
Summary: Russian hunspell dictionaries
Version: 0.99g5
Release: 1%{?dist}
Epoch: 1
Source: http://releases.mozilla.org/pub/mozilla.org/addons/3703/russian_spellchecking_dictionary-0.4.4-fx+tb+sm.xpi
URL: http://scon155.phys.msu.su/eng/lebedev.html
License: BSD
BuildArch: noarch

Requires: hunspell
Supplements: (hunspell and langpacks-ru)

%description
Russian hunspell dictionaries.

%prep
%setup -q -c -n hunspell-ru

%build

%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/myspell
cp -p dictionaries/ru.dic $RPM_BUILD_ROOT/%{_datadir}/myspell/ru_RU.dic
cp -p dictionaries/ru.aff $RPM_BUILD_ROOT/%{_datadir}/myspell/ru_RU.aff
cd $RPM_BUILD_ROOT/%{_datadir}/myspell/
ru_RU_aliases="ru_UA"
for lang in $ru_RU_aliases; do
        ln -s ru_RU.aff $lang.aff
        ln -s ru_RU.dic $lang.dic
done


%files
%doc dictionaries/Changelog dictionaries/LICENSE dictionaries/README
%{_datadir}/myspell/*

%changelog
* Wed Apr 19 2017 Elbert Pol <elbert.pol@gmail.com> - 0.99g5-1
- First Os2 Rpm build
