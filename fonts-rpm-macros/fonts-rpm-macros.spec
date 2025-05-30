# SPDX-License-Identifier: MIT
%if !0%{?os2_version}
%global forgeurl https://pagure.io/fonts-rpm-macros
%else
%global rpmmacrodir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)
%global forgesource https://pagure.io/fonts-rpm-macros-%{version}.zip
Vendor:         bww bitwise works GmbH
%endif
Epoch: 1
Version: 2.0.5
%if !0%{?os2_version}
%forgemeta
%endif

#https://src.fedoraproject.org/rpms/redhat-rpm-config/pull-request/51
%global _spectemplatedir %{_datadir}/rpmdevtools/fedora
%global _docdir_fmt     %{name}
%global ftcgtemplatedir %{_datadir}/fontconfig/templates

# Master definition that will be written to macro files
%global _fontbasedir            %{_datadir}/fonts
%global _fontconfig_masterdir   %{_sysconfdir}/fonts
%global _fontconfig_confdir     %{_sysconfdir}/fonts/conf.d
%global _fontconfig_templatedir %{_datadir}/fontconfig/conf.avail

BuildArch: noarch

Name:      fonts-rpm-macros
Release:   2%{?dist}
Summary:   Build-stage rpm automation for fonts packages

License:   GPLv3+
URL:       https://docs.fedoraproject.org/en-US/packaging-guidelines/FontsPolicy/
Source:    %{forgesource}

Requires:  fonts-srpm-macros = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:  fonts-filesystem  = %{?epoch:%{epoch}:}%{version}-%{release}

Provides:  fontpackages-devel = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes: fontpackages-devel < %{?epoch:%{epoch}:}%{version}-%{release}
# Tooling dropped for now as no one was willing to maintain it
Obsoletes: fontpackages-tools < %{?epoch:%{epoch}:}%{version}-%{release}

Requires:  fontconfig
%if !0%{?os2_version}
Requires:  libappstream-glib
Requires:  uchardet
%endif

# For the experimental generator
%if !0%{?os2_version}
Requires:  python3-ruamel-yaml
%endif
Requires:  python3-lxml

%description
This package provides build-stage rpm automation to simplify the creation of
fonts packages.

It does not need to be included in the default build root: fonts-srpm-macros
will pull it in for fonts packages only.

%package -n fonts-srpm-macros
Summary:   Source-stage rpm automation for fonts packages
%if !0%{?os2_version}
Requires:  redhat-rpm-config
%endif

%description -n fonts-srpm-macros
This package provides SRPM-stage rpm automation to simplify the creation of
fonts packages.

It limits itself to the automation subset required to create fonts SRPM
packages and needs to be included in the default build root.

The rest of the automation is provided by the fonts-rpm-macros package, that
fonts-srpm-macros will pull in for fonts packages only.

%package -n fonts-filesystem
Summary:   Directories used by font packages
License:   MIT

Provides:  fontpackages-filesystem = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes: fontpackages-filesystem < %{?epoch:%{epoch}:}%{version}-%{release}

%description -n fonts-filesystem
This package contains the basic directory layout used by font packages,
including the correct permissions for the directories.

%package -n fonts-rpm-templates
Summary:   Example fonts packages rpm spec templates
License:   MIT

Requires:    fonts-rpm-macros = %{?epoch:%{epoch}:}%{version}-%{release}
Supplements: fonts-rpm-macros = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n fonts-rpm-templates
This package contains documented rpm spec templates showcasing how to use the
macros provided by fonts-rpm-macros to create fonts packages.

%prep
%if !0%{?os2_version}
%forgesetup
%else
%autosetup -p1 -n %{name}-%{version}
%endif
%writevars -f rpm/macros.d/macros.fonts-srpm _fontbasedir _fontconfig_masterdir _fontconfig_confdir _fontconfig_templatedir
for template in templates/rpm/*\.spec ; do
  target=$(echo "${template}" | sed "s|^\(.*\)\.spec$|\1-bare.spec|g")
  grep -v '^%%dnl' "${template}" > "${target}"
  touch -r "${template}" "${target}"
done

%install
install -m 0755 -d    %{buildroot}%{_fontbasedir} \
                      %{buildroot}%{_fontconfig_masterdir} \
                      %{buildroot}%{_fontconfig_confdir} \
                      %{buildroot}%{_fontconfig_templatedir}

install -m 0755 -vd   %{buildroot}%{_spectemplatedir}
install -m 0644 -vp   templates/rpm/*spec \
                      %{buildroot}%{_spectemplatedir}
install -m 0755 -vd   %{buildroot}%{ftcgtemplatedir}
%if !0%{?os2_version}
install -m 0644 -vp   templates/fontconfig/*{conf,txt} \
                      %{buildroot}%{ftcgtemplatedir}
%else
install -m 0644 -vp   templates/fontconfig/*conf \
                      %{buildroot}%{ftcgtemplatedir}
install -m 0644 -vp   templates/fontconfig/*txt \
                      %{buildroot}%{ftcgtemplatedir}
%endif

install -m 0755 -vd   %{buildroot}%{rpmmacrodir}
install -m 0644 -vp   rpm/macros.d/macros.fonts-* \
                      %{buildroot}%{rpmmacrodir}
install -m 0755 -vd   %{buildroot}%{_rpmluadir}/fedora/srpm
install -m 0644 -vp   rpm/lua/srpm/*lua \
                      %{buildroot}%{_rpmluadir}/fedora/srpm
install -m 0755 -vd   %{buildroot}%{_rpmluadir}/fedora/rpm
install -m 0644 -vp   rpm/lua/rpm/*lua \
                      %{buildroot}%{_rpmluadir}/fedora/rpm

install -m 0755 -vd   %{buildroot}%{_bindir}
install -m 0755 -vp   bin/* %{buildroot}%{_bindir}

%files
%license LICENSE.txt
%{_bindir}/*
%{rpmmacrodir}/macros.fonts-rpm*
%{_rpmluadir}/fedora/rpm/*.lua

%files -n fonts-srpm-macros
%license LICENSE.txt
%doc     *.md changelog.txt
%{rpmmacrodir}/macros.fonts-srpm*
%{_rpmluadir}/fedora/srpm/*.lua

%files -n fonts-filesystem
%dir %{_datadir}/fontconfig
%dir %{_fontbasedir}
%dir %{_fontconfig_masterdir}
%dir %{_fontconfig_confdir}
%dir %{_fontconfig_templatedir}

%files -n fonts-rpm-templates
%license LICENSE-templates.txt
%doc     *.md changelog.txt
%{_spectemplatedir}/*.spec
%dir %{ftcgtemplatedir}
%doc %{ftcgtemplatedir}/*conf
%doc %{ftcgtemplatedir}/*txt

%changelog
* Tue May 13 2025 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1:2.0.5-2
- rebuild with python 3.13

* Thu Apr 28 2022 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1:2.0.5-1
- first os/2 rpm
