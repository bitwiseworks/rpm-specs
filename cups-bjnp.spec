Summary:        CUPS backend for the Canon BJNP network printers 
Name:           cups-bjnp
Version:        2.0
Release:        1%{?dist}
License:        GPLv2
Group:          System Environment/Daemons
URL:            https://sourceforge.net/projects/cups-bjnp/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Vendor:         bww bitwise works GmbH
%scm_source  github https://github.com/bitwiseworks/cups-bjnp-os2 %{version}-os2

# cups is required so we can check that the backend directory is really correct
BuildRequires:  cups
BuildRequires:  cups-devel
Requires:       cups

%global cups_backend_dir %{_exec_prefix}/lib/cups/backend

%description
This package contains a backend for CUPS for Canon printers using the 
proprietary BJNP network protocol.

%debug_package

%prep
%scm_setup

%build
autoreconf -fvi

export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"
%configure --prefix=%{_exec_prefix} --with-cupsbackenddir=%{cups_backend_dir}
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p" install

%clean
rm -Rf $RPM_BUILD_ROOT
 
%files
%{cups_backend_dir}/bjnp.exe
%doc COPYING ChangeLog TODO NEWS README README.levels

%changelog
* Fri Sep 15 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.0-1
- first version rpm version
