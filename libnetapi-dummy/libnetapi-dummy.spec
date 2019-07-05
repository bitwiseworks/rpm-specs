
Summary: Dummy NETAPI library
Name: libnetapi-dummy
Version: 0.0.0
Release: 2%{?dist}

License: free

Provides:   netapi.dll
Provides:   netapi32.dll

%description
This dummy virtual package is to satisfy the requrement of NETAPI.DLL and
NETAPI32.DLL by other packages in case if a real DLL is installed not
through RPM. No actual DLLs are installed by this package.

%files
# no files in a virtual package
