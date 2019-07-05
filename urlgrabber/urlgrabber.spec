
%define name urlgrabber
%define version 3.10.1
%define unmangled_version 3.10.1

Summary: A high-level cross-protocol url-grabber
Name: %{name}
Version: %{version}
Release: 10%{?dist}
Source0: %{name}-%{unmangled_version}.tar.gz
Patch0: urlgrabber-os2.patch

License: LGPL
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: Michael D. Stenner, Ryan Tomayko <mstenner@linux.duke.edu, rtomayko@naeblis.cx>
Url: http://linux.duke.edu/projects/urlgrabber/

Requires: python(abi) = %{python_version}
Requires: python-pycurl

%description
A high-level cross-protocol url-grabber.

Using urlgrabber, data can be fetched in three basic ways:

  urlgrab(url) copy the file to the local filesystem
  urlopen(url) open the remote file and return a file object
     (like urllib2.urlopen)
  urlread(url) return the contents of the file as a string

When using these functions (or methods), urlgrabber supports the
following features:

  * identical behavior for http://, ftp://, and file:// urls
  * http keepalive - faster downloads of many files by using
    only a single connection
  * byte ranges - fetch only a portion of the file
  * reget - for a urlgrab, resume a partial download
  * progress meters - the ability to report download progress
    automatically, even when using urlopen!
  * throttling - restrict bandwidth usage
  * retries - automatically retry a download if it fails. The
    number of retries and failure types are configurable.
  * authenticated server access for http and ftp
  * proxy support - support for authenticated http and ftp proxies
  * mirror groups - treat a list of mirrors as a single source,
    automatically switching mirrors if there is a failure.


%prep
%setup -n %{name}-%{unmangled_version}
%patch0 -p1 -b .os2~

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --root=$RPM_BUILD_ROOT --prefix %{_prefix} --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)

%changelog
* Sat Feb 28 2015 yd <yd@os2power.com> 3.10.1-10
- rebuild with new python, fixes ticket#114.

* Mon Feb 16 2015 yd <yd@os2power.com> 3.10.1-9
- fix progress bar display for multifile download.

* Mon Feb 09 2015 yd <yd@os2power.com> 3.10.1-8
- fix progress bar display for multifile download.

* Fri Feb 06 2015 yd <yd@os2power.com> 3.10.1-7
- add python-curl requirement.

* Thu Feb 05 2015 yd <yd@os2power.com> 3.10.1-6
- source code update to 3.10.1.

* Wed Jun 18 2014 yd
- rebuild to fix for http://trac.netlabs.org/rpm/ticket/77

* Tue Apr 08 2014 yd
- workaround for http://trac.netlabs.org/rpm/ticket/71

* Mon Apr 07 2014 yd
- build for python 2.7.
