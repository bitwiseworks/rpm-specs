
Summary: A getopt implementation with --longoptions support
Name: getopt
Version: 1.1.6
Release: 1%{?dist}
License: GPLv2+
URL: http://software.frodo.looijaard.name/getopt/

Vendor: bww bitwise works GmbH
%scm_source github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2

BuildRequires: gcc


%description
This package contains a reimplementation of getopt(1).


%debug_package

%prep
%scm_setup

%build
make EXEEXT=.exe LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx -lintl"

%check
make tests EXEEXT=.exe

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT prefix=%{_prefix} mandir=%{_mandir} INSTALL="install -p" EXEEXT=.exe

%find_lang %{name}

%files -f %{name}.lang
%doc COPYING README 
%{_bindir}/*
%exclude %{_bindir}/*.dbg
%{_mandir}/*/*


%changelog
* Tue Nov 12 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.0.28-1
- first OS/2 rpm version
