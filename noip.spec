Name:		noip
Version:	2.1.9
Release:	1%{?dist}
Summary:	A dynamic DNS update client
Group:		System Environment/Daemons
License:	GPLv2+
URL:		http://www.no-ip.com
Source0:	http://www.no-ip.com/client/linux/noip-duc-linux.tar.gz
# Patch for Fedora specifics 
Patch0:		noip-2.1.9-1.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


%description
Keep your current IP address in sync with your No-IP host or domain with 
this Dynamic Update Client (DUC). The client continually checks for IP 
address changes in the background and automatically updates the DNS at 
No-IP whenever it changes.

N.B. You need to run
	%# noip2 -C
before starting the service.

%package debug
Summary: HLL debug data for exception handling support.

%description debug
HLL debug data for exception handling support.

%prep
%setup -q -n %{name}-%{version}-1
%patch0 -p1

%build
export LDFLAGS="-Zbin-files -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
make %{?_smp_mflags} CFLAGS="%{optflags}"

%install
rm -rf %{buildroot}
install -D -p -m 755 noip2.exe %{buildroot}/%{_sbindir}/noip2.exe

# Make dummy config file 
mkdir -p %{buildroot}/%{_sysconfdir}
touch %{buildroot}/%{_sysconfdir}/no-ip2.conf

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING README.FIRST
%{_sbindir}/noip2.exe
%attr(600,noip,noip) %config(noreplace) %{_sysconfdir}/no-ip2.conf

%files debug
%defattr(-,root,root)
%{_sbindir}/*.dbg

%changelog
* Thu Apr 10 2014 yd
- initial public build.
