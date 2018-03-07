%global fontname source-sans-pro
%global fontconf 63-%{fontname}.conf

%global roman_version  2.020
%global italic_version 1.075
%global github_tag %{roman_version}R-ro/%{italic_version}R-it
%global source_dir %{fontname}-%{roman_version}R-ro-%{italic_version}R-it

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

Name:           adobe-source-sans-pro-fonts
Version:        %{roman_version}
Release:        1%{?dist}
Summary:        A set of OpenType fonts designed for user interfaces

License:        OFL
URL:            https://github.com/adobe-fonts/source-sans-pro
Vendor:         bww bitwise works GmbH
#unable to build from source: source format is unbuildable with free software
Source0:        https://github.com/adobe-fonts/source-sans-pro/archive/%{github_tag}/%{name}-%{version}.tar.gz
Source1:        %{name}-fontconfig.conf
#Source2:        %{fontname}.metainfo.xml

#BuildRequires:  fontpackages-devel
#Requires:       fontpackages-filesystem
BuildArch:      noarch


%description
Source Sans is a set of OpenType fonts that have been designed to work well in
user interface (UI) environments, as well as in text setting for screen and
print.


%prep
%autosetup -n %{source_dir}

# Fix permissions
chmod 0644 LICENSE.txt README.md

# Fix wrong EOLs
sed -i.orig "s/\r//" LICENSE.txt && \
touch -r LICENSE.txt.orig LICENSE.txt && \
rm LICENSE.txt.orig


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
if [ -x %{_bindir}/fc-cache ]; then \
    %{_bindir}/fc-cache %{_fontdir} || : \
fi


%postun
if [ $1 -eq 0 -a -x %{_bindir}/fc-cache ] ; then \
    %{_bindir}/fc-cache %{_fontdir} || : \
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
* Wed Mar 07 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.020-1
- initial rpm version
