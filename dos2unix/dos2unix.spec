Summary:       Text file format converters
Name:          dos2unix
Version:       7.3.4
Release:       1%{?dist}
Group:         Applications/Text
License:       BSD
URL:           http://waterlan.home.xs4all.nl/dos2unix.html

Vendor:        bww bitwise works GmbH
%scm_source  svn http://svn.netlabs.org/repos/ports/dos2unix/trunk 2012

BuildRequires: gettext
#BuildRequires: perl-Pod-Checker
Provides: unix2dos = %{version}-%{release}
Obsoletes: unix2dos < 5.1-1

%description
Convert text files with DOS or Mac line endings to Unix line endings and 
vice versa.

%debug_package

%prep
%scm_setup

%build
export prefix=%{_prefix}
export LIBS_EXTRA=-lcx
make %{?_smp_mflags}

%install
export prefix=%{_prefix}
make DESTDIR=$RPM_BUILD_ROOT install

# We add doc files manually to %%doc
rm -rf $RPM_BUILD_ROOT%{_docdir}

%find_lang %{name} --with-man --all-name

%files -f %{name}.lang
%defattr(-,root,root,0755)
%doc man/man1/dos2unix.htm  ChangeLog.txt COPYING.txt
%doc NEWS.txt README.txt TODO.txt
%{_bindir}/dos2unix.exe
%{_bindir}/mac2unix.exe
%{_bindir}/unix2dos.exe
%{_bindir}/unix2mac.exe
%{_mandir}/man1/*.1*

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Sat Feb 11 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 7.3.4-1
- initial port
