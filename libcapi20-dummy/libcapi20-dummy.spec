
Summary: Dummy CAPI 2.0 library
Name: libcapi20-dummy
Version: 0.0.0
Release: 2%{?dist}

License: free

Provides:   capi20.dll

%description
This virtual dummy package is to satisfy the requrement of CAPI20.DLL by other
packages in case if a real DLL is installed not through RPM. No actual DLLs are
installed by this package.

%files
# no files in a virtual package
