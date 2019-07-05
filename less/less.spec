#define svn_url     e:/trees/less/trunk
%define svn_url     http://svn.netlabs.org/repos/ports/less/trunk
%define svn_rev     1763

Summary: A text file browser similar to more, but better
Name: less
Version: 530
Release: 1%{?dist}
License: GPLv3+ or BSD
Group: Applications/Text
URL: http://www.greenwoodsoftware.com/less/
Vendor:  bww bitwise works GmbH
%scm_source  github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2

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
%scm_setup


%build
autoreconf -fiv
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
%configure

make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT


%files
%doc README NEWS INSTALL
%license LICENSE COPYING
%{_bindir}/*.exe
%{_mandir}/man1/*


%changelog
* Fri May 17 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> - 530-1
- update source to version 530
- move source to github

* Fri Oct 21 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 481-3
- fix to the below bring more keys to work
- enable ctrl-c by default
- workaround ticket 124

* Wed Oct 19 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 481-2
- bring more keys to work 
- fix a charset issue

* Thu Oct 13 2016 Herwig Bauernfeind <herwig.bauernfeind@bitwiseworks.com> - 481-1
- initial build
