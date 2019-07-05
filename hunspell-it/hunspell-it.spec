Name: hunspell-it
Summary: Italian hunspell dictionaries
%global upstreamid 20070901
Version: 2.4
Release: 0.1%{upstreamid}%{?dist}
Source: http://downloads.sourceforge.net/sourceforge/linguistico/italiano_2_4_2007_09_01.zip
URL: http://linguistico.sourceforge.net
License: GPLv3+
BuildArch: noarch
Requires: hunspell
Supplements: (hunspell and langpacks-it)
#dic contains free-form text inside the .dic, i.e. "error: line 3: bad flagvector"
#  https://sourceforge.net/tracker/?func=detail&aid=2994177&group_id=128318&atid=711333
Patch0: hunspell-it-sf2994177.cleandic.patch

%description
Italian hunspell dictionaries.

%prep
%setup -q -c -n hunspell-it
%patch0 -p0 -b .cleandic

%build
chmod -x *

%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/myspell
cp -p *.dic *.aff $RPM_BUILD_ROOT/%{_datadir}/myspell
#pushd $RPM_BUILD_ROOT/%{_datadir}/myspell/
cd $RPM_BUILD_ROOT/%{_datadir}/myspell/
it_IT_aliases="it_CH"
for lang in $it_IT_aliases; do
        ln -s it_IT.aff $lang.aff
        ln -s it_IT.dic $lang.dic
done



%files
%doc it_IT_README.txt it_IT_COPYING it_IT_AUTHORS it_IT_license.txt it_IT_notes.txt
%{_datadir}/myspell/*

%changelog
* Tue Apr 18 2017 Elbert Pol <elbert.pol@gmail.com> - 2.4-0.01.20070901
- First Os2 Rpm build