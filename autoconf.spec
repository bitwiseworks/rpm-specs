Summary:    A GNU tool for automatically configuring source code
Name:       autoconf
Version:    2.69
Release:    5%{?dist}
License:    GPLv2+ and GFDL
Group:      Development/Tools
URL:        http://www.gnu.org/software/autoconf/
BuildArch:  noarch
Vendor:     bww bitwise works GmbH

%scm_source svn http://svn.netlabs.org/repos/ports/autoconf/trunk 2192

# m4 >= 1.4.6 is required, >= 1.4.13 is recommended:
BuildRequires:      m4 >= 1.4.13
Requires:           m4 >= 1.4.13
#BuildRequires:      emacs

%info_requires

# for autoreconf
Requires: autoconf

# for docs (makeinfo etc)
BuildRequires:      texinfo help2man

# for check only:
#BuildRequires: automake libtool gcc-gfortran

%description
GNU's Autoconf is a tool for configuring source code and Makefiles.
Using Autoconf, programmers can create portable and configurable
packages, since the person building the package is allowed to
specify various configuration options.

You should install Autoconf if you are developing software and
would like to create shell scripts that configure your source code
packages. If you are installing Autoconf, you will also need to
install the GNU m4 package.

Note that the Autoconf package is not required for the end-user who
may be configuring software with an Autoconf-generated script;
Autoconf is only required for the generation of the scripts, not
their use.

%prep
%scm_setup

%build

# make sure configure is updated to properly support OS/2
autoreconf -fvi

%configure

# not parallel safe
make

#%check
# The following test is failing.
# 188: autotest.at:1195   parallel autotest and signal handling
# In test/autotest.at, under comment "Test PIPE", the exit code written
# to file "status" is 0.  Report mailed to bug-autoconf.
#make check TESTSUITEFLAGS='-187 189-'

%install
rm -rf ${RPM_BUILD_ROOT}
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%clean
rm -rf ${RPM_BUILD_ROOT}

%post
%info_post autoconf.info

%preun
%info_preun autoconf.info

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_infodir}/autoconf.info*
# don't include standards.info, because it comes from binutils...
%exclude %{_infodir}/standards*
%{_datadir}/autoconf/
#%dir %{_datadir}/emacs/
#%{_datadir}/emacs/site-lisp/
%{_mandir}/man1/*
%doc AUTHORS COPYING ChangeLog NEWS README THANKS TODO

%changelog
* Fri May 12 2017 Dmitriy Kuminov <coding@dmik.org> 2.69-5
- Use scm_source and friends.
- Fix fatal failure in postun script (missing percent in macro).
- Support escaping and quoting in LDFLAGS and similar vars (#156).

* Wed Oct 19 2016 Dmitriy Kuminov <coding@dmik.org> 2.69-4
- Overcome 32k command line limit on OS/2 in autom4te.

* Tue Oct 18 2016 Dmitriy Kuminov <coding@dmik.org> 2.69-3
- Disable too strict MAP_FIXED test on OS/2. Note that in order to let autoconf
  detect mmap presense, LIBCx must be installed and used (LIBS="-lcx").
- Install documentation in INFO format.
- Rebuild against LIBC 0.6.6 and GCC 4.9.2.

* Wed Sep 3 2014 Dmitriy Kuminov <coding@dmik.org> 2.69-2
- Use /@unixroot in generated files instead of absolute paths to programs.

* Fri Aug 29 2014 Dmitriy Kuminov <coding@dmik.org> 2.69-1
- Update to version 2.69.
- Fix PATH_SEPARATOR misdetection.
- Remove annoying $ac_executable_extensions warning.
- Apply various fixes to improve OS/2 and kLIBC support.

* Wed Oct 26 2011 yd
- fixed m4 path
