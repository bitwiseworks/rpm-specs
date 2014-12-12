Summary: Fonts for the Ghostscript PostScript interpreter
Name: ghostscript-fonts
Version: 6.0
Release: 1%{?dist}

# Contacted Kevin Hartig, who agreed to relicense his fonts under the SIL Open Font 
# License. Hershey fonts are under the "Hershey Font License", which is not what Fontmap 
# says (Fontmap is wrong).
License: GPLv2+ and Hershey and MIT and OFL and Public Domain
Group: Applications/Publishing
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
URL: http://www.gnu.org/software/ghostscript/

Source0: gnu-gs-fonts-other-%{version}.tar.gz

Requires: fontconfig
BuildArchitectures: noarch

%define fontdir %{_datadir}/fonts/default/ghostscript
%define catalogue %{_sysconfdir}/X11/fontpath.d

%description
Ghostscript-fonts contains a set of fonts that Ghostscript, a
PostScript interpreter, uses to render text. These fonts are in
addition to the fonts shared by Ghostscript and the X Window System.

%prep
%setup -q -c ghostscript-fonts-%{version}

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{fontdir}
cp -p fonts/* $RPM_BUILD_ROOT%{fontdir}

# Touch ghosted files
touch $RPM_BUILD_ROOT%{fontdir}/fonts.dir
touch $RPM_BUILD_ROOT%{fontdir}/fonts.scale

# Install catalogue symlink
mkdir -p $RPM_BUILD_ROOT%{catalogue}
ln -sf %{fontdir} $RPM_BUILD_ROOT%{catalogue}/default-ghostscript

#post
#{
#   mkfontscale %{fontdir}
#   mkfontdir %{fontdir}
#   fc-cache %{_datadir}/fonts
#} &> /dev/null || :

#postun
#{
#   if [ "$1" = "0" ]; then
#      fc-cache %{_datadir}/fonts
#   fi
#} &> /dev/null || :

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_datadir}/fonts/default/
%{catalogue}/default-ghostscript
%ghost %verify(not md5 size mtime) %{fontdir}/fonts.dir
%ghost %verify(not md5 size mtime) %{fontdir}/fonts.scale

%changelog
* Fri Dec 12 2014 yd
- initial unixroot build.
