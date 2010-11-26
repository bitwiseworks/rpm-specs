Name:           check
Version:        0.9.8
Release:        2%{?dist}
Summary:        A unit test framework for C
Source0:        http://downloads.sourceforge.net/check/%{name}-%{version}.tar.gz
Patch0:         check-os2.diff

Group:          Development/Tools
License:        LGPLv2+
URL:            http://check.sourceforge.net/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

#Requires(post): /sbin/install-info
#Requires(preun): /sbin/install-info

%description
Check is a unit test framework for C. It features a simple interface for 
defining unit tests, putting little in the way of the developer. Tests 
are run in a separate address space, so Check can catch both assertion 
failures and code errors that cause segmentation faults or other signals. 
The output from unit tests can be used within source code editors and IDEs.

%package devel
Summary:        Libraries and headers for developing programs with check
Group:          Development/Libraries
Requires:       pkgconfig
Requires:       %{name} = %{version}-%{release}

%description devel
Libraries and headers for developing programs with check

%package static
Summary:        Static libraries of check
Group:          Development/Libraries

%description static
Static libraries of check.

%prep
%setup -q
%patch0 -p1 -b .os2~

%build
export CONFIG_SHELL="/bin/sh"
export LDFLAGS="-Zbin-files -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp" ; \
%configure \
    --enable-shared --disable-static \
    "--cache-file=%{_topdir}/cache/%{name}.cache"

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -rf $RPM_BUILD_ROOT%{_infodir}/dir
rm -rf $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}

install -m 755 src/check.dll $RPM_BUILD_ROOT/%{_libdir}
install -m 755 src/.libs/check_s.a $RPM_BUILD_ROOT/%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

#%post
#/sbin/ldconfig
#if [ -e %{_infodir}/%{name}.info* ]; then
#  /sbin/install-info \
#    --entry='* Check: (check).               A unit testing framework for C.' \
#    %{_infodir}/%{name}.info %{_infodir}/dir || :
#fi

#%postun -p /sbin/ldconfig

#%preun
#if [ $1 = 0 -a -e %{_infodir}/%{name}.info* ]; then
#  /sbin/install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir || :
#fi

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING.LESSER ChangeLog ChangeLogOld NEWS README SVNChangeLog
%doc THANKS TODO
%{_libdir}/*.dll
%{_infodir}/check*

%files devel
%defattr(-,root,root,-)
%doc doc/example
%{_includedir}/check.h
%{_libdir}/*.dll
%{_libdir}/check.a
%{_libdir}/pkgconfig/check.pc
%{_datadir}/aclocal/check.m4

#check used to be static only, hence this.
%files static
%defattr(-,root,root,-)
%{_libdir}/check_s.a

%changelog
