%{!?__python_ver:%global __python_ver EMPTY}
#global __python_ver 2.7
%global unicode ucs4

%global _default_patch_fuzz 2

%if "%{__python_ver}" != "EMPTY"
%global main_python 0
%global python python%{__python_ver}
%global tkinter tkinter%{__python_ver}
%else
%global main_python 1
%global python python
%global tkinter tkinter
%endif

%global pybasever 2.7
%global pybasever_cond 27
%global pylibdir %{_libdir}/python%{pybasever}
%global tools_dir %{pylibdir}/Tools
%global demo_dir %{pylibdir}/Demo
%global doc_tools_dir %{pylibdir}/Doc/tools
%global dynload_dir %{pylibdir}/lib-dynload
%global site_packages %{pylibdir}/site-packages

%global with_gdb_hooks 0

%global with_systemtap 0

%global with_valgrind 0

# Some of the files below /usr/lib/pythonMAJOR.MINOR/test  (e.g. bad_coding.py)
# are deliberately invalid, leading to SyntaxError exceptions if they get
# byte-compiled.
#
# These errors are ignored by the normal python build, and aren't normally a
# problem in the buildroots since /usr/bin/python isn't present.
#
# However, for the case where we're rebuilding the python srpm on a machine
# that does have python installed we need to set this to avoid
# brp-python-bytecompile treating these as fatal errors:
#
%global _python_bytecompile_errors_terminate_build 0

# Completely disable python dependency generators as we enforce the right
# provides/requires manually. This, in particular, prevents python-libs from
# having the python(abi) dependency so that it can be installed anone.
%global __python_provides %{nil}
%global __python_requires %{nil}

# Exclude Windows installer stubs from debug info stripping
%define _strip_opts --debuginfo -x "wininst-*.exe"

Summary: An interpreted, interactive, object-oriented programming language
Name: %{python}
Version: 2.7.6
Release: 24%{?dist}
License: Python
Group: Development/Languages
Vendor: bww bitwise works GmbH

Requires: %{name}-libs = %{version}-%{release}
Provides: python-abi = %{pybasever}
Provides: python(abi) = %{pybasever}

%scm_source svn http://svn.netlabs.org/repos/rpm/python/trunk 1565

%if %{main_python}
Obsoletes: Distutils
Provides: Distutils
Obsoletes: python2
Provides: python2 = %{version}
Obsoletes: python-elementtree <= 1.2.6
Obsoletes: python-sqlite < 2.3.2
Provides: python-sqlite = 2.3.2
Obsoletes: python-ctypes < 1.0.1
Provides: python-ctypes = 1.0.1
Obsoletes: python-hashlib < 20081120
Provides: python-hashlib = 20081120
Obsoletes: python-uuid < 1.31
Provides: python-uuid = 1.31
%endif

# Because of getaddrinfo
Requires: libcx >= 0.6.3
# Because of DosEnterCritSec removal
Requires: pthread >= 20171227

# YD because of libcx
Requires: db4 > 4.8.30-6

# YD because of ucs4
Conflicts: python-pycurl < 7.19.5.1-2
Conflicts: rpm < 4.13.0-8
Conflicts: yum-metadata-parser < 1.1.4-6

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: readline-devel, openssl-devel, gmp-devel
#BuildRequires: gdbm-devel, zlib-devel, expat-devel
BuildRequires: ncurses-devel, zlib-devel, expat-devel
#BuildRequires: libGL-devel tk tix gcc-c++ libX11-devel glibc-devel
#BuildRequires: tar findutils pkgconfig tcl-devel tk-devel
BuildRequires: bzip2 pkgconfig tcl-devel
#BuildRequires: tix-devel
BuildRequires: bzip2-devel sqlite-devel
BuildRequires: autoconf
BuildRequires: db4-devel >= 4.8
BuildRequires: libffi-devel
%if 0%{?with_valgrind}
BuildRequires: valgrind-devel
%endif

%if 0%{?with_systemtap}
BuildRequires: systemtap-sdt-devel
%global tapsetdir      /usr/share/systemtap/tapset
%endif

BuildRequires: libcx-devel >= 0.6.1-2
BuildRequires: pthread-devel >= 20171227

URL: http://www.python.org/

%description
Python is an interpreted, interactive, object-oriented programming
language often compared to Tcl, Perl, Scheme or Java. Python includes
modules, classes, exceptions, very high level dynamic data types and
dynamic typing. Python supports interfaces to many system calls and
libraries, as well as to various windowing systems (X11, Motif, Tk,
Mac and MFC).

Programmers can write new built-in modules for Python in C or C++.
Python can be used as an extension language for applications that need
a programmable interface. This package contains most of the standard
Python modules, as well as modules for interfacing to the Tix widget
set for Tk and RPM.

Note that documentation for Python is provided in the python-docs
package.

%package common
Summary: An interpreted, interactive, object-oriented programming language
Group: Development/Languages

%description common
Only binary files without versioned name. Allows multiple installations.

%package libs
Summary: The libraries for python runtime
Group: Applications/System

# Needed for ctypes, to load libraries, worked around for Live CDs size
# Requires: binutils

%description libs
The python interpreter can be embedded into applications wanting to
use python as an embedded scripting language.  The python-libs package
provides the libraries needed for this.

%package devel
Summary: The libraries and header files needed for Python development
Group: Development/Libraries
Requires: %{python} = %{version}-%{release}
Requires: python-rpm-macros
Requires: python2-rpm-macros
# Needed here because of the migration of Makefile from -devel to the main
# package
Conflicts: %{python} < %{version}-%{release}
%if %{main_python}
Obsoletes: python2-devel
Provides: python2-devel = %{version}-%{release}
%endif

%description devel
The Python programming language's interpreter can be extended with
dynamically loaded extensions and can be embedded in other programs.
This package contains the header files and libraries needed to do
these types of tasks.

Install python-devel if you want to develop Python extensions.  The
python package will also need to be installed.  You'll probably also
want to install the python-docs package, which contains Python
documentation.

%package tools
Summary: A collection of development tools included with Python
Group: Development/Tools
Requires: %{name} = %{version}-%{release}
Requires: %{tkinter} = %{version}-%{release}
%if %{main_python}
Obsoletes: python2-tools
Provides: python2-tools = %{version}-%{release}
%endif

%description tools
This package includes several tools to help with the development of Python
programs, including IDLE (an IDE with editing and debugging facilities), a
color editor (pynche), and a python gettext program (pygettext.py).

%package -n %{tkinter}
Summary: A graphical user interface for the Python scripting language
Group: Development/Languages
#BuildRequires:  tcl, tk
Requires: %{name} = %{version}-%{release}
%if %{main_python}
Obsoletes: tkinter2
Provides: tkinter2 = %{version}-%{release}
%endif

%description -n %{tkinter}

The Tkinter (Tk interface) program is an graphical user interface for
the Python scripting language.

You should install the tkinter package if you'd like to use a graphical
user interface for Python programming.

%package test
Summary: The test modules from the main python package
Group: Development/Languages
Requires: %{name} = %{version}-%{release}

%description test

The test modules from the main python package: %{name}
These have been removed to save space, as they are never or almost
never used in production.

You might want to install the python-test package if you're developing python
code that uses more than just unittest and/or test_support.py.

%debug_package

%prep
%scm_setup

%if 0%{?with_systemtap}
# Provide an example of usage of the tapset:
cp -a %{SOURCE4} .
cp -a %{SOURCE5} .
%endif # with_systemtap

# Ensure that we're using the system copy of various libraries, rather than
# copies shipped by upstream in the tarball:
#   Remove embedded copy of expat:
#rm -r Modules/expat || exit 1
#   Remove embedded copy of libffi:
#for SUBDIR in darwin libffi libffi_arm_wince libffi_msvc libffi_osx ; do
#  rm -r Modules/_ctypes/$SUBDIR || exit 1 ;
#done
#   Remove embedded copy of zlib:
#rm -r Modules/zlib || exit 1

# This shouldn't be necesarry, but is right now (2.2a3)
find -name "*~" |xargs rm -f

# generate configure & friends
autoreconf -fvi

%build

# NOTE: Put -lcx to LDFLAGS instead of LIBS to have LIBCx linked to all shared
# (.pyd) modules in addition to the python DLL and EXE itself
export LDFLAGS="-g -Zbin-files -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -Zmap -lcx"
export LIBS="-lssl -lcrypto -lintl"
%configure \
        --enable-shared \
        --with-system-expat \
        --enable-unicode=ucs4 \
        --with-system-ffi

make OPT="$CFLAGS" %{?_smp_mflags}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_prefix} %{buildroot}%{_mandir}

make install DESTDIR=%{buildroot}

# YD fix binaries
ln -s %{_bindir}/python.exe %{buildroot}%{_bindir}/python
rm -f %{buildroot}%{_bindir}/python%{pybasever_cond}.dll

# Junk, no point in putting in -test sub-pkg
rm -f %{buildroot}/%{pylibdir}/idlelib/testcode.py*

# don't include tests that are run at build time in the package
# This is documented, and used: rhbz#387401
if /bin/false; then
 # Move this to -test subpackage.
mkdir save_bits_of_test
for i in test_support.py __init__.py; do
  cp -a %{buildroot}/%{pylibdir}/test/$i save_bits_of_test
done
rm -rf %{buildroot}/%{pylibdir}/test
mkdir %{buildroot}/%{pylibdir}/test
cp -a save_bits_of_test/* %{buildroot}/%{pylibdir}/test
fi

#%if %{main_python}
#ln -s python %{buildroot}%{_bindir}/python2
#%else
#mv %{buildroot}%{_bindir}/python %{buildroot}%{_bindir}/%{python}
#mv %{buildroot}/%{_mandir}/man1/python.1 %{buildroot}/%{_mandir}/man1/python%{pybasever}.1
#%endif

# tools

mkdir -p ${RPM_BUILD_ROOT}%{site_packages}

#gettext
install -m755  Tools/i18n/pygettext.py %{buildroot}%{_bindir}/
install -m755  Tools/i18n/msgfmt.py %{buildroot}%{_bindir}/

# Useful development tools
install -m755 -d %{buildroot}%{tools_dir}/scripts
install Tools/README %{buildroot}%{tools_dir}/
install Tools/scripts/*py %{buildroot}%{tools_dir}/scripts/

# Documentation tools
install -m755 -d %{buildroot}%{doc_tools_dir}
#install -m755 Doc/tools/mkhowto %{buildroot}%{doc_tools_dir}

# Useful demo scripts
install -m755 -d %{buildroot}%{demo_dir}
cp -ar Demo/* %{buildroot}%{demo_dir}

# Get rid of crap
find %{buildroot}/ -name "*~"|xargs rm -f
find %{buildroot}/ -name ".cvsignore"|xargs rm -f
find . -name "*~"|xargs rm -f
find . -name ".cvsignore"|xargs rm -f
#zero length
rm -f %{buildroot}%{site_packages}/modulator/Templates/copyright

rm -f %{buildroot}%{pylibdir}/LICENSE.txt


#make the binaries install side by side with the main python
#%if !%{main_python}
#pushd %{buildroot}%{_bindir}
#mv idle idle%{__python_ver}
#mv modulator modulator%{__python_ver}
#mv pynche pynche%{__python_ver}
#mv pygettext.py pygettext%{__python_ver}.py
#mv msgfmt.py msgfmt%{__python_ver}.py
#mv smtpd.py smtpd%{__python_ver}.py
#mv pydoc pydoc%{__python_ver}
#popd
#%endif

# Fix for bug #136654
rm -f %{buildroot}%{pylibdir}/email/test/data/audiotest.au %{buildroot}%{pylibdir}/test/audiotest.au

%global _pyconfig_h pyconfig.h

# Get rid of egg-info files (core python modules are installed through rpms)
rm %{buildroot}%{pylibdir}/*.egg-info

# Get rid of all .pyo files as they are identical to .pyc (only needed in
# python -O mode which is used rarely or not at all on OS/2)
find %{buildroot}%{pylibdir} -type f -name *.pyo -exec rm -f {} +

%clean
rm -fr %{buildroot}

#%post libs -p /sbin/ldconfig

#%postun libs -p /sbin/ldconfig


%post
if [ "$1" = 1 ] ; then
#execute only on first install
%cube {DELLINE "SET PYTHONPATH="} %{os2_config_sys} > NUL
%cube {DELLINE "SET PYTHONHOME="} %{os2_config_sys} > NUL
fi


%files -f %{debug_package_exclude_files}
%defattr(-, root, root, -)
%doc LICENSE README
%{_bindir}/pydoc*
%{_bindir}/python
%{_bindir}/python.exe
%{_bindir}/python2
%if %{main_python}
#%{_bindir}/python2
%endif
%{_bindir}/python%{pybasever}.exe
%{_mandir}/*/*

%dir %{pylibdir}
%dir %{dynload_dir}
%{dynload_dir}/Python-%{version}-py%{pybasever}.egg-info
%{dynload_dir}/*.pyd
%exclude %{dynload_dir}/*.map
%exclude %{dynload_dir}/_ctypes_test.pyd
%exclude %{dynload_dir}/_ct3574.pyd
%exclude %{dynload_dir}/_testcapi.pyd
%exclude %{dynload_dir}/_te3228.pyd

%dir %{site_packages}
%{site_packages}/README
%{pylibdir}/*.py*
%{pylibdir}/*.doc
%dir %{pylibdir}/bsddb
%{pylibdir}/bsddb/*.py*
%{pylibdir}/compiler
%dir %{pylibdir}/ctypes
%{pylibdir}/ctypes/*.py*
%{pylibdir}/ctypes/macholib
%{pylibdir}/curses
%dir %{pylibdir}/distutils
%{pylibdir}/distutils/*.py*
%{pylibdir}/distutils/README
%{pylibdir}/distutils/command
%dir %{pylibdir}/email
%{pylibdir}/email/*.py*
%{pylibdir}/email/mime
%{pylibdir}/encodings
%{pylibdir}/hotshot
%{pylibdir}/idlelib
%{pylibdir}/importlib
%dir %{pylibdir}/json
%{pylibdir}/json/*.py*
%{pylibdir}/lib2to3
%{pylibdir}/logging
%{pylibdir}/multiprocessing
%{pylibdir}/plat-os2knix
%{pylibdir}/pydoc_data
%dir %{pylibdir}/sqlite3
%{pylibdir}/sqlite3/*.py*
%dir %{pylibdir}/test
%{pylibdir}/test/test_support.py*
%{pylibdir}/test/__init__.py*
%{pylibdir}/wsgiref
%{pylibdir}/xml

# "Makefile" and the config-32/64.h file are needed by
# distutils/sysconfig.py:_init_posix(), so we include them in the core
# package, along with their parent directories (bug 531901):
%dir %{pylibdir}/config
%{pylibdir}/config/Makefile
%dir %{_includedir}/python%{pybasever}
%{_includedir}/python%{pybasever}/%{_pyconfig_h}

%files libs -f %{debug_package_exclude_files}
%defattr(-,root,root,-)
#%doc LICENSE README
%{_libdir}/python%{pybasever_cond}.dll
%if 0%{?with_systemtap}
%{tapsetdir}/%{libpython_stp}
%doc systemtap-example.stp pyfuntop.stp
%endif
%{pylibdir}/unittest/*

%files devel
%defattr(-,root,root,-)
%{pylibdir}/config/*
%exclude %{pylibdir}/config/Makefile
%{_includedir}/python%{pybasever}/*.h
%exclude %{_includedir}/python%{pybasever}/%{_pyconfig_h}
%doc Misc/README.valgrind Misc/valgrind-python.supp Misc/gdbinit
%if %{main_python}
%{_bindir}/python-config
%endif
%{_bindir}/python?*-config
#%{_libdir}/libpython%{pybasever}.pyd
%{_libdir}/python%{pybasever}_dll.a
%{_libdir}/pkgconfig

%files tools
%defattr(-,root,root,755)
#%doc Tools/modulator/README.modulator
#%doc Tools/pynche/README.pynche
#%{site_packages}/modulator
#%{site_packages}/pynche
%{_bindir}/smtpd*.py*
%{_bindir}/2to3*
%{_bindir}/idle*
#%{_bindir}/modulator*
#%{_bindir}/pynche*
%{_bindir}/pygettext*.py*
%{_bindir}/msgfmt*.py*
%{tools_dir}
%{demo_dir}
%{pylibdir}/Doc

%files -n %{tkinter}
%defattr(-,root,root,755)
%{pylibdir}/lib-tk
#%{dynload_dir}/_tkinter.pyd

%files test
%defattr(-, root, root, -)
%{pylibdir}/bsddb/test
%{pylibdir}/ctypes/test
%{pylibdir}/distutils/tests
%{pylibdir}/email/test
%{pylibdir}/json/tests
%{pylibdir}/sqlite3/test
%{pylibdir}/test/*
# These two are shipped in the main subpackage:
%exclude %{pylibdir}/test/test_support.py*
%exclude %{pylibdir}/test/__init__.py*
%{dynload_dir}/_ctypes_test.pyd
%{dynload_dir}/_ct3574.pyd
%{dynload_dir}/_testcapi.pyd
%{dynload_dir}/_te3228.pyd

# We put the debug-gdb.py file inside /usr/lib/debug to avoid noise from
# ldconfig (rhbz:562980).
#
# The /usr/lib/rpm/redhat/macros defines %__debug_package to use
# debugfiles.list, and it appears that everything below /usr/lib/debug and
# (/usr/src/debug) gets added to this file (via LISTFILES) in
# /usr/lib/rpm/find-debuginfo.sh
#
# Hence by installing it below /usr/lib/debug we ensure it is added to the
# -debuginfo subpackage
# (if it doesn't, then the rpmbuild ought to fail since the debug-gdb.py
# payload file would be unpackaged)

%changelog
* Wed Jan 23 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.7.6-24
- fix ticket #328

* Mon Jan 14 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.7.6-23
- fix ticket #326

* Fri Dec 21 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.7.6-22
- adjust getaddrinfo and friends to latest libcx
- don't add .exe to symlinks

* Mon Jun 18 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.7.6-21
- use %{os2_config_sys} macro instead of fixed c:\config.sys

* Wed Apr 18 2018 Dmitriy Kuminov <coding@dmik.org> 2.7.6-20.
- Understand `*module.pyd` and `*module.dll` extensions for Python modules.
- Improve handling of BEGINLIBPATH and other pseudo-env vars (#299).

* Mon Jan 8 2018 Dmitriy Kuminov <coding@dmik.org> 2.7.6-19
- Make sys.executable work for fancy python exe names on OS/2.
- Enable real os.spawnv* implementation on OS/2.
- Use LIBCx spawn2 instead of fork in subprocess module to improve performance.
- Don't flatten case of tempdir (fixes file name comparison in some apps).
- Support NUMBER_OF_PROCESSORS in multitasking.cpu_count() on OS/2.
- Fix handling drive letters in urllib.url2pathname and pathname2url on OS/2.
- Bring pthread dependency back (it's still used).

* Sat Jun 3 2017 Dmitriy Kuminov <coding@dmik.org> 2.7.6-18
- Put the LIBCx library to LDFLAGS rather than LIBS to have all module DLLs
  linked against it as well.
- Rebuild against LIBCx 0.5.3 to incorporate DosRead JFS workaround for fread.
- Remove urpo as it conflicts with LIBCx.
- Remove pthread from libraries as not needed any more.
- Remove .pyo files (needed only in python -O mode which is rarely used).
- Remove .dbg files for Windows stubs (wininst-*.exe).
- Use scm_source/scm_setup for downloading sources.

* Mon Apr 24 2017 yd <yd@os2power.com> 2.7.6-17
- add new requirements and move unittest files. ticket#248.

* Fri Feb 17 2017 yd <yd@os2power.com> 2.7.6-16
- force db4 minimal version (libcx req).

* Thu Feb 09 2017 yd <yd@os2power.com> 2.7.6-15
- link with libcx for memory mapping support.

* Fri Jun 10 2016 yd <yd@os2power.com> 2.7.6-14
- fixed Obsoletes vs Conflicts.
- fixed python2-devel and -tools version.

* Thu Jun 09 2016 yd <yd@os2power.com> 2.7.6-13
- enable support for ucs4 unicode set. ticket#182.
- r780, fix file deletion. ticket#185.
- r779, remove 8.3 file name truncation, use opendir() to avoid resolving symlinks. ticket#185.
- r775, generate both 8.3 and long names for pyd dynamic libraries. fixes ticket#185.

* Sat Dec 12 2015 Dmitriy Kuminov <coding@dmik.org> 2.7.6-12
- r611, Add dummy plat-os2knix directory.
- r610, Fix silly typo.
- r609, Fix a typo in r529.
- r608, Make os.path.defpath return '$UNIXROOT/usr/bin' on OS/2 when it is set.
- r607, Replace altsep to sep in paths returned by os.path.join.
- r606, Add ignore patterns for *.pyc and generated files.
- r605, configure: Generate correct OS/2 defs and remove pre-built configure.
- r604, Fix building with no OS/2 Toolkit headers in include paths.
- r603, Use configured SHELL in subprocess module.
- Provide dummy _dlopen in ctypes to make colorama package happy.
- Use configured SHELL for subprocess.Popen(shell=True) instead of
  hardcoded '/bin/sh'.
- Make os.path.join replace all altsep (\) with sep (/) on return (to
  fix joining names with components of PATH-like env. vars and passing
  the results to a unix shell).
- Make os.path.defpath return '$UNIXROOT\\usr\\bin'.
- r568, build mmap module, by psmedley.

* Thu Feb 26 2015 yd <yd@os2power.com> 2.7.6-11
- r560, -O3 breaks the build, at least for pentium4 march.
- r529, use unixroot path for script path replacement. Fixes ticket#114.

* Mon Apr 07 2014 yd
- build for python 2.7.

* Sat Mar 15 2014 yd
- r385 and others, added support for virtualenv.
- added debug package with symbolic info for exceptq.

* Wed Jun 05 2013 yd
- r348, add samefile, sameopenfile, samestat to os.path module.

* Thu Dec 27 2012 yd
- fix local/bin requirements for python-tools.

* Mon Jan 16 2012 yd
- rebuild with libc 0.6.4 runtime.