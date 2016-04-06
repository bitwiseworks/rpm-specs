%global _icu_full_version 4.2.1
%global _icu_dll_version 42

Summary:        International Components for Unicode
Name:           icu
License:        X11/MIT
Group:          System/Libraries
Version:        %{_icu_full_version}
Release:        2%{?dist}
Url:            http://ibm.com/software/globalization/icu

Source0:        icu-legacy.zip

BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
ICU is a set of C and C++ libraries that provides robust and
full-featured Unicode and locale support. The library provides calendar
support, conversions for many character sets, language sensitive
collation, date and time formatting, support for many locales, message
catalogs and resources, message formatting, normalization, number and
currency formatting, time zone support, transliteration, and word,
line, and sentence breaking, etc.

This package contains the Unicode character database and derived
properties along with converters and time zone data.

This package contains the runtime libraries for ICU. It does not
contain any of the data files needed at runtime and present in the icu
and icu-locales packages.



Authors:
--------
    The ICU project, International Business Machines (IBM) and Others.  <icu@oss.software.ibm.com>

%package -n libicu-legacy
License:        IBM Public License
Summary:        International Components for Unicode (development files)
Group:          Development/Libraries/C and C++

%description -n libicu-legacy
ICU is a set of C and C++ libraries that provides robust and
full-featured Unicode support. This package contains the runtime
libraries for ICU. It does not contain any of the data files needed at
runtime and present in the `icu' and `icu-locales` packages.



Authors:
--------
    The ICU project, International Business Machines (IBM) and Others.  <icu@oss.software.ibm.com>


%prep
%setup -q -n icu

%build
mkdir -p %{buildroot}%{_libdir}
cp -p *.dll %{buildroot}%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%doc license.html readme.html

%files -n libicu-legacy
%defattr(-, root, root)
%attr (755, root, root) %{_libdir}/*.dll

%changelog
* Wed Apr 06 2016 yd <yd@os2power.com> 4.2.1-2
- repackage legacy dlls.
