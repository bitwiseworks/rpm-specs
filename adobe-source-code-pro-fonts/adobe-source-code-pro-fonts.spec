%global fontname adobe-source-code-pro
%global fontconf 61-%{fontname}.conf

%global version_roman  2.030
%global version_italic 1.050

# OS/2 rpm macros don't define this (yet), do it manually:
# Fontconfig directory for active configuration snippets
%global _fontconfig_confdir %{_sysconfdir}/fonts/conf.d

# Fontconfig configuration template directory
# Templates are activated by symlinking in _fontconfig_confdir
%global _fontconfig_templatedir %{_datadir}/fontconfig/conf.avail

# Font installation directory root
%global _fontbasedir %{_datadir}/fonts

# Actual font installation directory
%global _fontdir %{_fontbasedir}/%{?fontname:%{fontname}}%{?!fontname:%{name}}

Name:           %{fontname}-fonts
Version:        %{version_roman}.%{version_italic}
Release:        1%{?dist}
Summary:        A set of mono-spaced OpenType fonts designed for coding environments

Group:          User Interface/X
License:        OFL
URL:            https://github.com/adobe-fonts/source-code-pro
Vendor:         bww bitwise works GmbH
Source0:        https://github.com/adobe-fonts/source-code-pro/archive/%{version_roman}R-ro%2f%{version_italic}R-it.tar.gz#/SourceCodePro-%{version_roman}R-ro-%{version_italic}R-it.tar.gz
Source1:        %{name}-fontconfig.conf
#Source2:        %{fontname}.metainfo.xml

BuildArch:      noarch
#BuildRequires:  fontpackages-devel
#Requires:       fontpackages-filesystem

%description
This font was designed by Paul D. Hunt as a companion to Source Sans. It has
the same weight range as the corresponding Source Sans design.  It supports
a wide range of languages using the Latin script, and includes all the
characters in the Adobe Latin 4 glyph set.


%prep
%setup -qn source-code-pro-%{version_roman}R-ro-%{version_italic}R-it
sed -i 's/\r//' LICENSE.txt
chmod 644 LICENSE.txt

%build

%install
install -m 0755 -d %{buildroot}%{_fontdir}
install -m 0644 -p OTF/*.otf %{buildroot}%{_fontdir}

install -m 0755 -d %{buildroot}%{_fontconfig_templatedir} \
                   %{buildroot}%{_fontconfig_confdir}


install -m 0644 -p %{SOURCE1} %{buildroot}%{_fontconfig_templatedir}/%{fontconf}
ln -s %{_fontconfig_templatedir}/%{fontconf} %{buildroot}%{_fontconfig_confdir}/%{fontconf}

# Add AppStream metadata
#install -Dm 0644 -p %{SOURCE2} \
#        %{buildroot}%{_datadir}/appdata/%{fontname}.metainfo.xml

%post
if [ -x %{_bindir}/fc-cache ]; then
    %{_bindir}/fc-cache %{_fontdir} || :
fi

%postun
if [ $1 -eq 0 -a -x %{_bindir}/fc-cache ] ; then
    %{_bindir}/fc-cache %{_fontdir} || :
fi

%files
%doc README.md
%license LICENSE.txt
%dir %{_fontdir}
%{_fontdir}/*.otf
%{_fontconfig_templatedir}/%{fontconf}
%config(noreplace) %{_fontconfig_confdir}/%{fontconf}
#%{_datadir}/appdata/%{fontname}.metainfo.xml


%changelog
* Wed Mar 07 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.030.1.050-1
- initial rpm version
