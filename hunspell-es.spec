Name: hunspell-es
Summary: Spanish hunspell dictionaries
Version: 0.7
Release: 1%{?dist}
Epoch: 1
Source: http://forja.rediris.es/frs/download.php/2890/es_ANY.oxt
URL: https://forja.rediris.es/projects/rla-es/
License: LGPLv3+ or GPLv3+ or MPLv1.1
BuildArch: noarch

Requires: hunspell
Supplements: (hunspell and langpacks-es)

%description
Spanish (Spain, Mexico, etc.) hunspell dictionaries.

%prep
%setup -q -c -n hunspell-es

%build
chmod -x *

%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/myspell
cp -p es_ANY.dic $RPM_BUILD_ROOT/%{_datadir}/myspell/es.dic
cp -p es_ANY.aff $RPM_BUILD_ROOT/%{_datadir}/myspell/es.aff

#push $RPM_BUILD_ROOT/%{_datadir}/myspell/
cd $RPM_BUILD_ROOT/%{_datadir}/myspell/
es_ES_aliases="es_ES es_AR es_BO es_CL es_CO es_CR es_CU es_DO es_EC es_GT es_HN es_MX es_NI es_PA es_PE es_PR es_PY es_SV es_US es_UY es_VE"

for lang in $es_ES_aliases; do
	ln -s es.aff $lang.aff
	ln -s es.dic $lang.dic
done
#popd

%files
%doc README.txt Changelog.txt GPLv3.txt MPL-1.1.txt LGPLv3.txt
%{_datadir}/myspell/*

%changelog
* Tue Apr 18 2017 Elbert Pol <elbert.pol@gmail.com> - 1:0.7-1
- First Os2 Rpm build
