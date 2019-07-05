#
# Subversion
#

Name:       subversion
Vendor:     netlabs.org
License:    ASL 1.1
Url:        http://subversion.apache.org/

%define ver_major   1
%define ver_minor   6
%define ver_patch   16

%define os2_release 2

%define rpm_release 1

%define descr_brief Subversion, known as svn, is a concurrent version control system which enables\
one or more users to collaborate in developing and maintaining a hierarchy of\
files and directories while keeping a history of all changes. It is intended\
to be a compelling replacement for CVS.

%define pkg_docdir  %{_docdir}/%{name}

%if 0%{?os2_release}
Version:    %{ver_major}.%{ver_minor}.%{ver_patch}.%{os2_release}
%else
Version:    %{ver_major}.%{ver_minor}.%{ver_patch}
%endif
Release:    %{rpm_release}

Source: http://download.smedley.info/subversion-1.6.16-os2-20110422.zip

#------------------------------------------------------------------------------
# commons
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# main package
#------------------------------------------------------------------------------

Summary:    Modern concurrent version control system
Group:      Development/Tools

%description
%{descr_brief}

This package contains Subversion command line tools.

%files
%defattr(-,root,root,-)
%docdir %{pkg_docdir}/
%{pkg_docdir}/
%{_bindir}/*
%{_mandir}/man*/*
%dir %{_sysconfdir}/subversion

#------------------------------------------------------------------------------
%package -n libsvn-devel
#------------------------------------------------------------------------------

Summary:    Development files for Subversion libraries
Group:      Development/LIbraries

Requires:   %{name} = %{version}-%{release}

%description -n libsvn-devel
%{descr_brief}

This package package includes the libraries and include files needed to build
applications interacting with the subversion tools.

%files -n libsvn-devel
%defattr(-,root,root,-)
%{_libdir}/*
%{_includedir}/*

#------------------------------------------------------------------------------
%prep
#------------------------------------------------------------------------------

%setup -qn "%{name}"

#------------------------------------------------------------------------------
%build
#------------------------------------------------------------------------------

# we use the binary distro for now, nothing to do here

#------------------------------------------------------------------------------
%install
#------------------------------------------------------------------------------

rm -rf "%{buildroot}"

mkdir -p "%{buildroot}/%{pkg_docdir}/"
cp -dp "readme.os2" "%{buildroot}/%{pkg_docdir}/"

mkdir -p "%{buildroot}/%{_bindir}/"
cp -Rdp "bin/*" "%{buildroot}/%{_bindir}/"

mkdir -p "%{buildroot}/%{_includedir}/"
cp -Rdp "include/*" "%{buildroot}/%{_includedir}/"

mkdir -p "%{buildroot}/%{_libdir}/"
cp -Rdp "lib/*" "%{buildroot}/%{_libdir}/"

mkdir -p "%{buildroot}/%{_mandir}/"
cp -Rdp "share/man/*" "%{buildroot}/%{_mandir}/"

mkdir -p "%{buildroot}/%{_sysconfdir}/subversion/"

#------------------------------------------------------------------------------
%clean
#------------------------------------------------------------------------------

rm -rf "%{buildroot}"

#------------------------------------------------------------------------------
%changelog

* Wed Oct 5 2011 Dmitriy Kuminov <dmik/coding.org> 1.6.16.2-1
- New binary release 1.6.16-20110422 from Paul Smedley.
  See %{pkg_docdir}/readme.os2 for more information.

