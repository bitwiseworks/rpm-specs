%define rname magicolor5430dl

Summary:	Cups Driver for KONICA MINOLTA magicolor 5430 DL
Name:		cups-drivers-%{rname}
Version:	1.8.1
Release:	1
License:	GPL
Group:		System/Printing
URL:		http://printer.konicaminolta.net/
Vendor:         bww bitwise works GmbH
%scm_source  github https://github.com/bitwiseworks/magicolor-5430DL-os2 %{version}-os2

BuildRequires:	automake
BuildRequires:	cups-devel
BuildRequires:	jbigkit-devel
BuildRequires:	lcms2-devel
Requires:	cups


%description
This package contains KONICA MINOLTA CUPS LavaFlow stream(PCL-like) filter
rastertokm5430dl and the PPD file. The filter converts CUPS raster data to
KONICA MINOLTA LavaFlow stream.

This package contains CUPS drivers (PPD) for the following printers:

 o KONICA MINOLTA magicolor 5430 DL printer


%debug_package


%prep
%scm_setup


# Remove asterisks from group names in PPD file
gzip -dc src/km_en.ppd.gz | perl -p -e 's/(Group:\s+)\*/$1/g' | gzip > src/km_en.tmp.ppd.gz && mv -f src/km_en.tmp.ppd.gz src/km_en.ppd.gz


%build
autoreconf -fvi

export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"
export VENDOR="%{vendor}"
%configure
make


%install
rm -rf %{buildroot}
%make_install


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog
%{_cups_serverbin}/filter/rastertokm5430dl.exe
%{_datadir}/KONICA_MINOLTA/mc5430DL
%attr(0644,root,root) %{_datadir}/cups/model/KONICA_MINOLTA/km5430dl.ppd*


%changelog
* Tue Nov 28 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.8.1-1
- first version
