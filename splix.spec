Summary:       Driver for QPDL/SPL2 printers (Samsung and several Xerox printers)
Name:          splix
Version:       2.0.0
Release:       1
License:       GPLv2
URL:           http://splix.sourceforge.net/

Vendor:        bww bitwise works GmbH
%scm_source  svn http://svn.netlabs.org/repos/ports/splix/trunk 2000

Requires:      cups

BuildRequires: cups-devel
BuildRequires: dos2unix

#BuildRequires: python3-cups, cups
#BuildRequires: jbigkit-devel

%description
This driver is usable by all printer devices which understand the QPDL
(Quick Page Description Language) also known as SPL2 (Samsung Printer Language)
language. It covers several Samsung, Xerox and Dell printers.
Splix doesn't support old SPL(1) printers.

%debug_package

%prep
%scm_setup

cd ppd
# remove old PPDs
make distclean
cd ..

%build
make drv

# the shell script generating the drv files uses redirect. so we get CRLF files
# but we need LF (unix style files) here
for f in `find ppd -type f -name '*.drv'` ; do
  dos2unix $f
done

CXXFLAGS="%{optflags} -fno-strict-aliasing" \
LDFLAGS="-Zomf -Zhigh-mem -lcx" \
make all V=1 DISABLE_JBIG=1 DRV_ONLY=1 %{?_smp_mflags}

%install
make install DISABLE_JBIG=1 DRV_ONLY=1 CUPSDRV=%{_datadir}/cups/drv/splix DESTDIR=%{buildroot}

%files
%license COPYING
%doc AUTHORS ChangeLog THANKS
%{_cups_serverbin}/filter/pstoqpdl.exe
%{_cups_serverbin}/filter/rastertoqpdl.exe
%{_datadir}/cups/drv/splix

%changelog
* Sat Feb 11 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.0.0-1
- initial port
