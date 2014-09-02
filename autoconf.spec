Summary:    A GNU tool for automatically configuring source code
Name:       autoconf
Version:    2.69
Release:    2%{?dist}
License:    GPLv2+ and GFDL
Group:      Development/Tools
#Source:     http://ftp.gnu.org/gnu/autoconf/autoconf-%{version}.tar.xz
#Source1:    filter-provides-automake.sh
#Source2:    filter-requires-automake.sh
URL:        http://www.gnu.org/software/autoconf/
BuildArch: noarch
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%define svn_url     http://svn.netlabs.org/repos/ports/autoconf/trunk
%define svn_rev     845

Source: %{name}-%{version}-r%{svn_rev}.zip

BuildRequires: gcc make subversion zip

# m4 >= 1.4.6 is required, >= 1.4.13 is recommended:
BuildRequires:      m4 >= 1.4.13
Requires:           m4 >= 1.4.13
#BuildRequires:      emacs
#Requires(post):     /sbin/install-info
#Requires(preun):    /sbin/install-info

# for autoreconf
Requires: autoconf

# for check only:
#BuildRequires: automake libtool gcc-gfortran
#%if 0%{?fedora}
#BuildRequires: erlang
#%endif

# Make AC_FUNC_MMAP work with C++ again.
# Committed to Autoconf git soon after 2.65.
#Patch1: autoconf_ac_func_mmap.patch

# filter out bogus perl(Autom4te*) dependencies
#define _use_internal_dependency_generator 0
#define __find_provides %{SOURCE1}
#define __find_requires %{SOURCE2}

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
%if %(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')
%setup -q
%else
%setup -n "%{name}-%{version}" -Tc
svn export -r %{svn_rev} %{svn_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" "%{name}-%{version}")
%endif

%build

# make sure configure is updated to properly support OS/2
autoreconf --verbose --install

# we don't have makeinfo/help2man yet; fake them (this will wipe docs out)
export MAKEINFO=:
export HELP2MAN=:

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

#%post
#/sbin/install-info %{_infodir}/autoconf.info %{_infodir}/dir || :

#%preun
#if [ "$1" = 0 ]; then
#    /sbin/install-info --del %{_infodir}/autoconf.info %{_infodir}/dir || :
#fi

%files
%defattr(-,root,root,-)
%{_bindir}/*
#%{_infodir}/autoconf.info*
# don't include standards.info, because it comes from binutils...
%exclude %{_infodir}/standards*
%{_datadir}/autoconf/
#%dir %{_datadir}/emacs/
#%{_datadir}/emacs/site-lisp/
%{_mandir}/man1/*
%doc AUTHORS COPYING ChangeLog NEWS README THANKS TODO

%changelog
* Wed Sep 3 2014 Dmitriy Kuminov <coding@dmik.org> 2.69-2
- Use /@unixroot in generated files instead of absolute paths to programs.

* Fri Aug 29 2014 Dmitriy Kuminov <coding@dmik.org> 2.69-1
- Update to version 2.69.
- Fix PATH_SEPARATOR misdetection.
- Remove annoying $ac_executable_extensions warning.
- Apply various fixes to improve OS/2 and kLIBC support.

* Wed Oct 26 2011 yd
- fixed m4 path
