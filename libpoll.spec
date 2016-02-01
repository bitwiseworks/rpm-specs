# Note: this package should go away (become an alias for libc-devel)
# once http://trac.netlabs.org/libc/ticket/353 is resolved.

Summary: System V poll system call emulation.
Name: libpoll-devel
Version: 1.5.1
Release: 4%{?dist}
License: BSD
Vendor:  bww bitwise works GmbH
URL: http://software.clapper.org/poll/

Group: Development/Libraries

# https://github.com/bmc/poll/archive/release-1.5.1.zip
Source: poll-release-1.5.1.zip

BuildRequires: gcc

Requires: libc-devel

%description
This package implements the System V poll(2) system call for Unix-like systems
that do not support poll. For instance, the following Unix-like operating
systems do not support poll:

    NetBSD, prior to version 1.3
    FreeBSD, prior to version 3.0
    OpenBSD, prior to version 2.0
    BSD/OS. (See the BSD/OS man pages.)
    Apple's Mac OS X (prior to OS X 10.3)
    QNX version 6
    4.4 BSD Lite 2 (not generally used by production systems)
    386BSD (pretty much obsolete these days)
    OS/2 (and derivatives)

poll provides a method for multiplexing input and output on multiple open file
descriptors; in traditional BSD systems, that capability is provided by
select(2). While the semantics of select differ from those of poll, poll can
be readily emulated in terms of select, which is exactly what this small piece
of software does.

%prep
%setup -q -n poll-release-%{version}

# Add extra POLL constants used by some sources.
# @todo We can't use patch directly because of EOLs (forced --binary on OS/2).
tr -d '\r' > poll.diff <<"EOF"
--- poll.h.b
+++ poll.h
@@ -78,6 +78,11 @@
 #define POLLHUP        0x10
 #define POLLNVAL   0x20

+#define POLLRDNORM  0x0040
+#define POLLRDBAND  0x0080
+#define POLLWRNORM  0x0100
+#define POLLWRBAND  0x0200
+
 struct pollfd
 {
     int     fd;
EOF
patch < poll.diff

%build
gcc %{optflags} -c poll.c -o poll.o
ar rv poll_s.a poll.o
emxomf poll_s.a -o poll_s.lib

# Add support for #include <poll.h>
echo "#include <sys/poll.h>" > nosys_poll.h

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_includedir}
install -m 644 nosys_poll.h %{buildroot}%{_includedir}/poll.h
mkdir -p %{buildroot}%{_includedir}/sys
install -m 644 poll.h %{buildroot}%{_includedir}/sys
mkdir -p %{buildroot}%{_libdir}
install -m 755 poll_s.a poll_s.lib %{buildroot}%{_libdir}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc CHANGELOG.md INSTALL README.md LICENSE
%{_includedir}/poll.h
%{_includedir}/sys/poll.h
%{_libdir}/poll_s.a
%{_libdir}/poll_s.lib

%changelog
* Mon Feb 1 2016 Dmitriy Kuminov <coding@dmik.org> 1.5.1-4
- Correct package description.
- Add vendor tag.

* Wed Jan 27 2016 Dmitriy Kuminov <coding@dmik.org> 1.5.1-3
- Add poll_s.a (for use with ld, e.g. in non-Zomf mode).

* Wed Dec 22 2015 Dmitriy Kuminov <coding@dmik.org> 1.5.1-2
- Add POLLRD* and POLLWR* constants.

* Tue Dec 22 2015 Dmitriy Kuminov <coding@dmik.org> 1.5.1-1
- Initial package for version 1.5.1.
