Summary:        Extension for creating pdf-Files with CUPS
Name:           cups-pdf
Version:        3.0.1
Release:        3%{?dist}
Group:          Applications/Publishing
URL:            http://www.cups-pdf.de/
License:        GPLv2+
Vendor:         bww bitwise works GmbH

%scm_source  github https://github.com/bitwiseworks/%{name}-os2 master-os2


BuildRequires:  gcc
BuildRequires:  cups-devel

Requires:       ghostscript, cups
%if !0%{?os2_version}
Requires(post): %{_bindir}/pgrep
%endif

# These are the defaults paths defined in config.h
# CUPS-PDF spool directory
%global CPSPOOL   %{_localstatedir}/spool/cups-pdf/SPOOL

# CUPS-PDF output directory
%global CPOUT     %{_localstatedir}/spool/cups-pdf

# CUPS-PDF log directory
%global CPLOG     %{_localstatedir}/log/cups

# CUPS-PDF cups-pdf.conf config file
%global ETCCUPS   %(cups-config --serverroot 2>/dev/null || echo %{_sysconfdir}/cups)

# Additional path to backend directory
%global CPBACKEND %(cups-config --serverbin  2>/dev/null || echo %{_libdir}/cups)/backend


%description
"cups-pdf" is a backend script for use with CUPS - the "Common UNIX Printing
System" (see more for CUPS under http://www.cups.org/). 
"cups-pdf" uses the ghostscript pdfwrite device to produce PDF Files.


%debug_package


%prep
%scm_setup


%build
cd src
gcc $RPM_OPT_FLAGS -lcups -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx -o cups-pdf.exe cups-pdf.c
cd ..


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{CPBACKEND}
mkdir -p %{buildroot}%{CPSPOOL}
mkdir -p %{buildroot}%{CPOUT}
mkdir -p %{buildroot}%{CPLOG}
mkdir -p %{buildroot}%{CPBACKEND}
mkdir -p %{buildroot}%{ETCCUPS}
mkdir -p %{buildroot}%{_datadir}/cups/model/
install -m644 extra/CUPS-PDF_noopt.ppd  %{buildroot}%{_datadir}/cups/model/
install -m644 extra/CUPS-PDF_opt.ppd  %{buildroot}%{_datadir}/cups/model/
install -m644 extra/cups-pdf.conf %{buildroot}%{ETCCUPS}/
install -m700 src/cups-pdf.exe %{buildroot}%{CPBACKEND}/


%post
# First install : create the printer if cupsd is running
if [ "$1" -eq "1" ] && plist y | grep CUPSD >/dev/null
then
    /@unixroot/usr/sbin/lpadmin -p Cups-PDF -v cups-pdf:/ -m CUPS-PDF_noopt.ppd -E || :
fi

%postun
if [ "$1" -eq "0" ]; then
    # Delete the printer
    /@unixroot/usr/sbin/lpadmin -x Cups-PDF || :
fi


%files
%doc ChangeLog COPYING README INSTALL.RPM
%dir %{CPSPOOL}
%dir %{CPOUT}
%attr(700, root, root) %{CPBACKEND}/cups-pdf.exe
%config(noreplace) %{ETCCUPS}/cups-pdf.conf
%{_datadir}/cups/model/CUPS-PDF_noopt.ppd
%{_datadir}/cups/model/CUPS-PDF_opt.ppd


%changelog
* Fri Nov 06 2020 Silvan Scherrer <silvan.scherrer@aroa> 3.0.1-3
- rebuild with latest toolchain

* Wed Dec 18 2018 Silvan Scherrer <silvan.scherrer@aroa> 3.0.1-2
- fix ticket #3
- handle title better in documents
- install the printer when cupsd runs

* Mon Dec 10 2018 Silvan Scherrer <silvan.scherrer@aroa> 3.0.1-1
- first rpm version
