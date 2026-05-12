Name:           xmltoman
Version:        0.4
Release:        2%{?dist}
Summary:        Scripts for converting XML to roff or HTML

License:        GPL-2.0-or-later
URL:            http://sourceforge.net/projects/xmltoman/
%if 0%{?os2_version}
Vendor:         bww bitwise works GmbH
%endif
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Patch0:         xmltoman-0.3-timestamps.patch

BuildRequires: make
BuildRequires:  perl-generators
BuildRequires:  perl(XML::Parser)
BuildArch:      noarch

%description
This package provides xmltoman and xmlmantohtml scripts, to compile
the xml representation of manual page to either roff source, or HTML
(while providing the CSS stylesheet for eye-candy look). XSL stylesheet
for doing rougly the same job is provided.


%prep
%setup -q
%patch -P0 -p1 -b .timestamps


%build
make %{?_smp_mflags}


%install
make install PREFIX=%{_prefix} DESTDIR=%{buildroot}
mkdir -p %{buildroot}%{_mandir}/man1
cp -p *.1 %{buildroot}%{_mandir}/man1


%files
%{_bindir}/xmltoman
%{_bindir}/xmlmantohtml
%{_datadir}/xmltoman
%{_mandir}/*/*
%doc COPYING README


%changelog
* Mon May 11 2026 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.4-2
- rebuild with perl 5.42.2
- resync with fedora spec

* Tue Dec 31 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.4-1
- first OS/2 rpm version
