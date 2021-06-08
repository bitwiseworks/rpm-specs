Summary: Sandbox
Name: sandbox
Version: 1.0
Release: 1%{?dist}
License: none

Group: Applications/System

%scm_source svn http://svn.netlabs.org/repos/sandbox/trunk 118

BuildRequires: gcc make

# To create WPS objects
BuildRequires: bww-resources-rpm-build >= 1.1.0

Source1: sandbox.txt

#{error:ERRORRRR}

%description
Sandbox package for testing RPM.

%package doc
Summary: Sandbox Manual
Group:   Documentation
BuildArch: noarch

%description doc
Whatever

%package wps1
Summary: Sandbox WPS obj 1
BuildArch: noarch
Requires: bww-resources-rpm >= 1.1.3

%description wps1
Whatever

%package wps2
Summary: Sandbox WPS obj 2
BuildArch: noarch
Requires: bww-resources-rpm >= 1.1.3

%description wps2
Whatever

%prep
%scm_setup

%build
echo [$LANG]
echo [$LANG2]
#echo "%(echo [$PATH])"
#exit 1

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_libdir}/sandbox/
cp -rp * %{buildroot}/%{_libdir}/sandbox/
%{__cp} %SOURCE1 .

echo "WPS Obj 1" > %{buildroot}/%{_libdir}/sandbox/wpsobj1.txt
echo "WPS Obj 2" > %{buildroot}/%{_libdir}/sandbox/wpsobj2.txt


#find_lang %{name}

echo '
%exclude %{_libdir}/sandbox/testfile2
'> sandbox.files

%clean
rm -rf %{buildroot}

%post
#echo WILL FAIL NOW...
#exit 100
#echo AFTER FAILURE...
if [ "$1" -ge 1 ]; then # (upon update)
    #wps_object_delete_all
fi
#wps_object_create_begin
#sandbox_FOLDER:WPFolder|sandbox|<WP_DESKTOP>|TITLE=Sandbox;
#wps_object_create_end
#cube {ADDLINE "SET SANDBOX=YES" (IFNOT "SET SANDBOX=")} c:\config.sys > NUL

%postun
if [ "$1" -eq 0 ]; then # (upon removal)
    #wps_object_delete_all
fi

%files -f sandbox.files
#{_libdir}/sandbox/RPMBUILD_SOURCE
%{_libdir}/*

%files doc
%doc sandbox.txt

%files wps1
%{_libdir}/sandbox/wpsobj1.txt

%files wps2
%{_libdir}/sandbox/wpsobj2.txt


%global wps_title Sandbox Examples

%post wps1
if [ "$1" -ge 1 ]; then # (upon update)
    %wps_object_delete_all -n %{name}-wps1
fi
%bww_folder -t %{wps_title} -n %{name}-wps1 -s %{name}-WPS
%bww_file EXAMPLES -f %{_libdir}/sandbox/wpsobj1.txt -n %{name}-wps1

%postun wps1
if [ "$1" -eq 0 ]; then # (upon removal)
    %wps_object_delete_all -n %{name}-wps1
fi

%post wps2
if [ "$1" -ge 1 ]; then # (upon update)
    %wps_object_delete_all -n %{name}-wps2
fi
#bww_folder -t %{wps_title} -n %{name}-wps2 -s %{name}-WPS
%bww_file EXAMPLES
# -f %{_libdir}/sandbox/wpsobj2.txt -n %{name}-wps2

%postun wps2
if [ "$1" -eq 0 ]; then # (upon removal)
    %wps_object_delete_all -n %{name}-wps2
fi


%changelog
* Thu Feb 16 2017 Dmitriy Kuminov <coding@dmik.org> 1.0-1
- Initial thingy.
