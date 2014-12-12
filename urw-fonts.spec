%define filippov_version 1.0.7pre44
%define fontdir %{_datadir}/fonts/default/Type1
%define catalogue %{_sysconfdir}/X11/fontpath.d

Summary: Free versions of the 35 standard PostScript fonts.
Name: urw-fonts
Version: 2.4
Release: 0%{?dist}
Source: %{name}-%{filippov_version}.tar.bz2
URL: http://svn.ghostscript.com/ghostscript/tags/urw-fonts-1.0.7pre44/
# URW holds copyright
# No version specified
License: GPL+
Group: User Interface/X
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: noarch

#Requires(post): fontconfig
#Requires(postun): fontconfig

%description 
Free, good quality versions of the 35 standard PostScript(TM) fonts,
donated under the GPL by URW++ Design and Development GmbH.

Install the urw-fonts package if you need free versions of standard
PostScript fonts.

%prep
%setup -q -c

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{fontdir}
install -m 0644 *.afm *.pfb $RPM_BUILD_ROOT%{fontdir}/

# Touch ghosted files
touch $RPM_BUILD_ROOT%{fontdir}/encodings.dir
touch $RPM_BUILD_ROOT%{fontdir}/fonts.dir
touch $RPM_BUILD_ROOT%{fontdir}/fonts.scale
touch $RPM_BUILD_ROOT%{fontdir}/fonts.cache-1

# Install catalogue symlink
mkdir -p $RPM_BUILD_ROOT%{catalogue}
ln -sf %{fontdir} $RPM_BUILD_ROOT%{catalogue}/fonts-default

#%post
#{
#   umask 133
#   mkfontscale %{fontdir} || :
#   `which mkfontdir` %{fontdir} || :
#   fc-cache %{_datadir}/fonts
#} &> /dev/null || :

#%postun
#{
#   if [ "$1" = "0" ]; then
#      fc-cache %{_datadir}/fonts
#   fi
#} &> /dev/null || :

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644,root,root,0755)
%doc COPYING README README.tweaks
%dir %{_datadir}/fonts/default
%dir %{fontdir}
%{catalogue}/fonts-default
%ghost %verify(not md5 size mtime) %{fontdir}/fonts.dir
%ghost %verify(not md5 size mtime) %{fontdir}/fonts.scale
%ghost %verify(not md5 size mtime) %{fontdir}/fonts.cache-1
%ghost %verify(not md5 size mtime) %{fontdir}/encodings.dir
%{fontdir}/*.afm
%{fontdir}/*.pfb

%changelog
* Fri Dec 12 2014 yd
- initial unixroot build.
