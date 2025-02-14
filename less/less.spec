Summary: A text file browser similar to more, but better
Name: less
Version: 668
Release: 1%{?dist}
License: GPL-3.0-only and BSD-2-Clause
%if !0%{?os2_version}
Source0: https://www.greenwoodsoftware.com/less/%{name}-%{version}.tar.gz
Source1: lesspipe.sh
Source2: less.sh
Source3: less.csh
Patch4: less-394-time.patch
Patch5: less-475-fsync.patch
Patch6: less-436-manpage-add-old-bot-option.patch
Patch8: less-458-lessecho-usage.patch
Patch9: less-458-less-filters-man.patch
Patch10: less-458-lesskey-usage.patch
Patch11: less-458-old-bot-in-help.patch
Patch13: less-436-help.patch
%else
Vendor:  bww bitwise works GmbH
%scm_source  github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2
%endif
URL: https://www.greenwoodsoftware.com/less/
BuildRequires: ncurses-devel
BuildRequires: autoconf automake libtool
BuildRequires: make

%description
The less utility is a text file browser that resembles more, but has
more capabilities.  Less allows you to move backwards in the file as
well as forwards.  Since less doesn't have to read the entire input file
before it starts, less starts up more quickly than text editors (for
example, vi).

You should install less because it is a basic utility for viewing text
files, and you'll use it frequently.

%if 0%{?os2_version}
%debug_package
%endif

%prep
%if !0%{?os2_version}
%setup -q
%patch -P 4 -p1 -b .time
%patch -P 5 -p1 -b .fsync
%patch -P 6 -p1 -b .manpage-add-old-bot-option
%patch -P 8 -p1 -b .lessecho-usage
%patch -P 9 -p1 -b .less-filters-man
%patch -P 10 -p1 -b .lesskey-usage
%patch -P 11 -p1 -b .old-bot
%patch -P 13 -p1 -b .help
%else
%scm_setup
%endif


%build
rm -f ./configure
autoreconf -fiv
%if 0%{?os2_version}
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
%endif
%configure
%make_build CFLAGS="%{optflags} -D_GNU_SOURCE -D_LARGEFILE_SOURCE -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64"

%install
%make_install
%if !0%{?os2_version}
mkdir -p $RPM_BUILD_ROOT/etc/profile.d
install -p        %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}
install -p -m 644 %{SOURCE2} $RPM_BUILD_ROOT/etc/profile.d
install -p -m 644 %{SOURCE3} $RPM_BUILD_ROOT/etc/profile.d
%endif

%files
%doc README NEWS INSTALL
%license LICENSE COPYING
%if !0%{?os2_version}
/etc/profile.d/*
%{_bindir}/*
%else
%{_bindir}/*.exe
%endif
%{_mandir}/man1/*

%changelog
* Fri Feb 14 2025 Silvan Scherrer <silvan.scherrer@aroa.ch> - 668-1
- update source to version 668
- resync with fedora spec

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
