#define svn_url     e:/trees/less/trunk
%define svn_url     http://svn.netlabs.org/repos/ports/less/trunk
%define svn_rev     1763

Summary: A text file browser similar to more, but better
Name: less
Version: 481
Release: 3%{?dist}
License: GPLv3+ or BSD
Group: Applications/Text
URL: http://www.greenwoodsoftware.com/less/
Vendor:  bww bitwise works GmbH
Source:  %{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip

BuildRequires: ncurses-devel
BuildRequires: autoconf automake libtool


%description
The less utility is a text file browser that resembles more, but has
more capabilities.  Less allows you to move backwards in the file as
well as forwards.  Since less doesn't have to read the entire input file
before it starts, less starts up more quickly than text editors (for
example, vi). 

You should install less because it is a basic utility for viewing text
files, and you'll use it frequently.


%debug_package


%prep
%if %{?svn_rev:%(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')}%{!?svn_rev):0}
%setup -q
%else
%setup -n "%{name}-%{version}" -Tc
svn export %{?svn_rev:-r %{svn_rev}} %{svn_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip" "%{name}-%{version}")
%endif

autoreconf -fiv


%build
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
%configure

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc README NEWS INSTALL
%license LICENSE COPYING
%{_bindir}/*.exe
%{_mandir}/man1/*


%changelog
* Fri Oct 21 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 481-3
- fix to the below bring more keys to work
- enable ctrl-c by default
- workaround ticket 124

* Wed Oct 19 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 481-2
- bring more keys to work 
- fix a charset issue

* Thu Oct 13 2016 Herwig Bauernfeind <herwig.bauernfeind@bitwiseworks.com> - 481-1
- initial build
