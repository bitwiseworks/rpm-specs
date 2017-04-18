Name: hunspell-nl
Summary: Dutch hunspell dictionaries
Version: 2.10
Release: 1%{?dist}
#http://www.opentaal.org/bestanden/doc_download/20-woordenlijst-v-210g-voor-openofficeorg-3
#annoying click through makes direct link apparently impossible
#Source: OpenTaal-210G-LO.oxt
Source:  %{name}-%{version}.zip
URL: http://www.opentaal.org/english.php
License: BSD or CC-BY
BuildArch: noarch

Requires: hunspell
Supplements: (hunspell and langpacks-nl)

%description
Dutch hunspell dictionaries.

%prep
%setup -q -c

%build
#chmod -x nl_NL.*

%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/myspell
#cp -p nl_NL.aff nl_NL.dic $RPM_BUILD_ROOT/%{_datadir}/myspell
cp -p C:/rpmbuild/BUILD/hunspell-nl-2.10/usr/share/myspell/nl_??.dic C:/rpmbuild/BUILD/hunspell-nl-2.10/usr/share/myspell/nl_??.aff $RPM_BUILD_ROOT/%{_datadir}/myspell

#pushd $RPM_BUILD_ROOT/%{_datadir}/myspell/
cd $RPM_BUILD_ROOT/%{_datadir}/myspell/
nl_NL_aliases="nl_AW nl_BE"
for lang in $nl_NL_aliases; do
        ln -s nl_NL.aff $lang.aff
        ln -s nl_NL.dic $lang.dic
done


%files
%doc C:/rpmbuild/BUILD/hunspell-nl-2.10/usr/share/doc/hunspell-nl/*.txt 
%{_datadir}/myspell/*

%changelog
* Tue Apr 18 2017 Elbert Pol <elbert.pol@gmail.com> - 2.10-1
- First RPM build OS2

