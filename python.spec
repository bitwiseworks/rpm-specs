%{!?__python_ver:%global __python_ver EMPTY}
#global __python_ver 26
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

%global pybasever 2.6
%global pybasever_cond 26
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

Summary: An interpreted, interactive, object-oriented programming language
Name: %{python}
Version: 2.6.5
Release: 1
License: Python
Group: Development/Languages
Provides: python-abi = %{pybasever}
Provides: python(abi) = %{pybasever}
Source: http://www.python.org/ftp/python/%{version}/Python-%{version}.tgz

Patch0: Python-%{version}-os2.diff
Patch1: Python-%{version}-os2knix.diff

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

# YD unix adds this automatically by parsing elf binaries
Requires: %{name}-libs = %{version}-%{release}

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
#BuildRequires: readline-devel, openssl-devel, gmp-devel
#BuildRequires: ncurses-devel, gdbm-devel, zlib-devel, expat-devel
BuildRequires: zlib-devel
#BuildRequires: libGL-devel tk tix gcc-c++ libX11-devel glibc-devel
#BuildRequires: bzip2 tar findutils pkgconfig tcl-devel tk-devel
BuildRequires: bzip2 pkgconfig
#BuildRequires: tix-devel bzip2-devel sqlite-devel
BuildRequires: bzip2-devel sqlite-devel
#BuildRequires: autoconf
#BuildRequires: db4-devel >= 4.8
#BuildRequires: libffi-devel
%if 0%{?with_valgrind}
BuildRequires: valgrind-devel
%endif

%if 0%{?with_systemtap}
BuildRequires: systemtap-sdt-devel
%global tapsetdir      /usr/share/systemtap/tapset
%endif

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

%package libs
Summary: The libraries for python runtime
Group: Applications/System
Requires: %{name} = %{version}-%{release}
# Needed for ctypes, to load libraries, worked around for Live CDs size
# Requires: binutils

%description libs
The python interpreter can be embedded into applications wanting to 
use python as an embedded scripting language.  The python-libs package 
provides the libraries needed for this.

%package devel
Summary: The libraries and header files needed for Python development
Group: Development/Libraries
Requires: %{python}%{?_isa} = %{version}-%{release}
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
Provides: python2-tools = %{version}
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
Provides: tkinter2 = %{version}
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

%prep
%setup -q -n Python-%{version}

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

#
# Apply patches:
#
%patch0 -p1 -b .os2
%patch1 -p1 -b .os2knix

mkdir Lib/plat-os2knix

# This shouldn't be necesarry, but is right now (2.2a3)
find -name "*~" |xargs rm -f

%build
CONFIG_SHELL=/bin/sh
export CONFIG_SHELL
LDFLAGS="-Zbin-files -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LDFLAGS
LIBS="-lssl -lcrypto -lurpo -lmmap -lpthread"
export LIBS
BASECFLAGS="-O2 -g -march=i386 -mtune=i686"
export BASECFLAGS
%configure \
        --enable-shared --disable-static \
        "--cache-file=%{_topdir}/cache/%{name}.cache"

make OPT="$CFLAGS" %{?_smp_mflags}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_prefix} %{buildroot}%{_mandir}

make install DESTDIR=%{buildroot}

# YD fix binaries
cp %{buildroot}%{_bindir}/python.exe %{buildroot}%{_bindir}/python
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

%clean
rm -fr %{buildroot}

#%post libs -p /sbin/ldconfig

#%postun libs -p /sbin/ldconfig


%files
%defattr(-, root, root, -)
%doc LICENSE README
%{_bindir}/pydoc*
%{_bindir}/%{python}
%{_bindir}/%{python}.exe
%if %{main_python}
#%{_bindir}/python2
%endif
%{_bindir}/python%{pybasever}.exe
%{_mandir}/*/*

%dir %{pylibdir}
%dir %{dynload_dir}
%{dynload_dir}/Python-%{version}-py%{pybasever}.egg-info
%{dynload_dir}/_bisect.pyd
%{dynload_dir}/_bsddb.pyd
%{dynload_dir}/_bytesio.pyd
%{dynload_dir}/_codecs_.pyd
#%{dynload_dir}/_codecs_hk.pyd
#%{dynload_dir}/_codecs_iso2022.pyd
#%{dynload_dir}/_codecs_jp.pyd
#%{dynload_dir}/_codecs_kr.pyd
#%{dynload_dir}/_codecs_tw.pyd
%{dynload_dir}/_collect.pyd
%{dynload_dir}/_csv.pyd
#%{dynload_dir}/_ctypes.pyd
%{dynload_dir}/_curses.pyd
%{dynload_dir}/_curses_.pyd
%{dynload_dir}/_element.pyd
%{dynload_dir}/_fileio.pyd
%{dynload_dir}/_functoo.pyd
%{dynload_dir}/_hashlib.pyd
%{dynload_dir}/_heapq.pyd
%{dynload_dir}/_hotshot.pyd
%{dynload_dir}/_json.pyd
%{dynload_dir}/_locale.pyd
%{dynload_dir}/_lsprof.pyd
#%{dynload_dir}/_md5.pyd
%{dynload_dir}/_multiby.pyd
%{dynload_dir}/_multipr.pyd
%{dynload_dir}/_random.pyd
#%{dynload_dir}/_sha256.pyd
#%{dynload_dir}/_sha512.pyd
#%{dynload_dir}/_sha.pyd
%{dynload_dir}/_socket.pyd
%{dynload_dir}/_sqlite3.pyd
%{dynload_dir}/_ssl.pyd
%{dynload_dir}/_struct.pyd
%{dynload_dir}/_weakref.pyd
%{dynload_dir}/array.pyd
%{dynload_dir}/audioop.pyd
%{dynload_dir}/binascii.pyd
%{dynload_dir}/bz2.pyd
%{dynload_dir}/cPickle.pyd
%{dynload_dir}/cStringI.pyd
%{dynload_dir}/cmath.pyd
%{dynload_dir}/crypt.pyd
%{dynload_dir}/datetime.pyd
%{dynload_dir}/dbm.pyd
%{dynload_dir}/dl.pyd
%{dynload_dir}/fcntl.pyd
%{dynload_dir}/future_b.pyd
#%{dynload_dir}/gdbm.pyd
%{dynload_dir}/grp.pyd
%{dynload_dir}/imageop.pyd
%{dynload_dir}/itertool.pyd
#%{dynload_dir}/linuxaudiodev.pyd
%{dynload_dir}/math.pyd
#%{dynload_dir}/mmap.pyd
#%{dynload_dir}/nis.pyd
%{dynload_dir}/operator.pyd
#%{dynload_dir}/ossaudiodev.pyd
%{dynload_dir}/parser.pyd
%{dynload_dir}/pyexpat.pyd
#%{dynload_dir}/readline.pyd
%{dynload_dir}/resource.pyd
%{dynload_dir}/select.pyd
#%{dynload_dir}/spwd.pyd
%{dynload_dir}/strop.pyd
%{dynload_dir}/syslog.pyd
%{dynload_dir}/termios.pyd
%{dynload_dir}/time.pyd
#%{dynload_dir}/timing.pyd
%{dynload_dir}/unicoded.pyd
#%{dynload_dir}/xxsubtype.pyd
%{dynload_dir}/zlib.pyd

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
%dir %{pylibdir}/json
%{pylibdir}/json/*.py*
%{pylibdir}/lib2to3
%{pylibdir}/logging
%{pylibdir}/multiprocessing
%{pylibdir}/plat-os2knix
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

%files libs
%defattr(-,root,root,-)
#%doc LICENSE README
%{_libdir}/python%{pybasever_cond}.dll
%if 0%{?with_systemtap}
%{tapsetdir}/%{libpython_stp}
%doc systemtap-example.stp pyfuntop.stp
%endif

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
%{_bindir}/python%{pybasever}-config
#%{_libdir}/libpython%{pybasever}.pyd
%{_libdir}/python%{pybasever}_dll.a

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
%{dynload_dir}/_ctypes_.pyd
%{dynload_dir}/_testcap.pyd

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
