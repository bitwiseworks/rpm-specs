Summary:    A GNU tool for automatically configuring source code
Name:       autoconf213
Version:    2.13
Release:    2%{?dist}
License:    GPLv2+ and GFDL
Group:      Development/Tools
Source:     http://hobbes.nmsu.edu/download/pub/os2/dev/util/autoconf213.zip
URL:        http://www.gnu.org/software/autoconf/
BuildArch:  noarch
Vendor:     bww bitwise works GmbH

BuildRequires:      m4 >= 1.4.13
Requires:           m4 >= 1.4.13

%info_requires

Patch1: autoconf213-1-remove_hardcoded_exe.patch
Patch2: autoconf213-2-support_spaces_in_opts.patch

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

%setup -q -c %{name}-%{version}

%patch1 -p1
[ $? = 0 ] || exit 1
%patch2 -p1
[ $? = 0 ] || exit 1

%build

# remove frozen states as they are wrong after patching
%{__rm} share/autoconf/*.m4f
# remove the dir with the os2 diff
%{__rm} -rf src

%install

%{__rm} -rf ${RPM_BUILD_ROOT}
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_bindir}
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_datadir}
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_infodir}
(cd bin
for f in *
do %{__sed} -r \
  -e 's|/usr/local|/@unixroot/usr|g' \
  -e 's|/share/autoconf|/share/autoconf213|g' \
  < $f > ${RPM_BUILD_ROOT}%{_bindir}/${f}213
done)
chmod +x ${RPM_BUILD_ROOT}%{_bindir}/*
%{__cp} -a share/autoconf ${RPM_BUILD_ROOT}%{_datadir}/autoconf213
%{__cp} -a info/autoconf.info ${RPM_BUILD_ROOT}%{_infodir}/autoconf213.info

#{__rm} -f $RPM_BUILD_ROOT%{_infodir}/dir

%clean
%{__rm} -rf ${RPM_BUILD_ROOT}
cd .. && %{__rm} -rf %{buildsubdir}

%post
%info_post autoconf213.info

%preun
%info_preun autoconf213.info

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_infodir}/autoconf213.info*
# don't include standards.info, because it comes from binutils...
%exclude %{_infodir}/standards*
%{_datadir}/autoconf213/
#{_mandir}/man1/*
%doc doc/autoconf/*

%changelog
* Fri Jun 2 2017 Dmitriy Kuminov <coding@dmik.org> 2.13-2
- Add executable bit to scripts in /usr/bin to make them recognizable by which,
  test -x etc.
- Brush up the .spec by using proper RPM macros.

* Thu May 22 2014 Dmitriy Kuminov <coding@dmik.org> 2.13-1
- Initial version with some fixes (e.g. allow options with spaces).
