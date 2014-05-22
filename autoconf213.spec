Summary:    A GNU tool for automatically configuring source code
Name:       autoconf213
Version:    2.13
Release:    1%{?dist}
License:    GPLv2+ and GFDL
Group:      Development/Tools
Source:     http://hobbes.nmsu.edu/download/pub/os2/dev/util/autoconf213.zip
URL:        http://www.gnu.org/software/autoconf/
BuildArch: noarch
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      m4 >= 1.4.13
Requires:           m4 >= 1.4.13
#Requires(post):     /sbin/install-info
#Requires(preun):    /sbin/install-info

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
rm share/autoconf/*.m4f
# remove the dir with the os2 diff
rm -rf src

%install

rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}/%{_bindir}
mkdir -p ${RPM_BUILD_ROOT}/%{_datadir}
mkdir -p ${RPM_BUILD_ROOT}/%{_infodir}
for f in `cd bin && echo *`
do sed -r \
  -e 's|/usr/local|/@unixroot/usr|g' \
  -e 's|/share/autoconf|/share/autoconf213|g' \
  < bin/$f > ${RPM_BUILD_ROOT}/%{_bindir}/${f}213
done
cp -R share/autoconf ${RPM_BUILD_ROOT}/%{_datadir}/autoconf213
cp info/autoconf.info ${RPM_BUILD_ROOT}/%{_infodir}/autoconf213.info

#rm -f $RPM_BUILD_ROOT%{_infodir}/dir

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
%{_infodir}/autoconf213.info*
# don't include standards.info, because it comes from binutils...
#%exclude %{_infodir}/standards*
%{_datadir}/autoconf213/
#%{_mandir}/man1/*
%doc doc/autoconf/*

%changelog
* Thu May 22 2014 Dmitriy Kuminov <coding@dmik.org> 2.13-1
- Initial version with some fixes (e.g. allow options with spaces).
