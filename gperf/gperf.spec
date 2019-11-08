Summary: A perfect hash function generator
Name: gperf
Version: 3.1
Release: 1%{?dist}
License: GPLv3+
URL: http://www.gnu.org/software/gperf/

Vendor:  bww bitwise works GmbH
%scm_source  github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2

BuildRequires:  gcc
#BuildRequires:  gcc-c++

%description
Gperf is a perfect hash function generator written in C++. Simply
stated, a perfect hash function is a hash function and a data
structure that allows recognition of a key word in a set of words
using exactly one probe into the data structure.

%debug_package

%prep
%scm_setup

%build
# we do autoreconf even fedora doesn't do it
autoreconf -fvi -I ..
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"

%configure
make %{?_smp_mflags}

%install
%make_install

# remove the stuff from the buildroot
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc

%files
%doc README NEWS doc/*.html doc/*.pdf COPYING
%{_bindir}/%{name}.exe
%{_mandir}/man1/gperf.1*
%{_infodir}/gperf.info*

%changelog
* Thu Nov 07 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.1-1
- initial OS/2 rpm
