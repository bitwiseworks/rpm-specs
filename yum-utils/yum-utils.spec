#define svn_url     F:/rd/ports/yum-utils/trunk
%define svn_url     http://svn.netlabs.org/repos/ports/yum-utils/trunk
%define svn_rev     1598

%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Summary: Utilities based around the yum package manager
Name: yum-utils
Version: 1.1.31
Release: 3%{?dist}
License: GPLv2+
Group: Development/Tools

Source: %{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip

URL: http://yum.baseurl.org/download/yum-utils/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
Requires: yum >= 3.2.27
Requires: python(abi) = 2.7

#Requires: python-kitchen
BuildRequires: python-devel
BuildRequires: rpm-build
BuildRequires: gettext
BuildRequires: intltool
Provides: yum-utils-translations = %{version}-%{release}


%description
yum-utils is a collection of utilities and examples for the yum package
manager. It includes utilities by different authors that make yum easier and
more powerful to use. These tools include: debuginfo-install, 
find-repos-of-install, needs-restarting, package-cleanup, repoclosure, 
repodiff, repo-graph, repomanage, repoquery, repo-rss, reposync,
repotrack, show-installed, show-changed-rco, verifytree, yumdownloader,
yum-builddep, yum-complete-transaction, yum-config-manager, yum-debug-dump,
yum-debug-restore and yum-groups-manager.

%package -n yum-updateonboot
Summary: Run yum update on system boot
Group: System Environment/Base
Requires: python, yum >= 2.4
Requires(pre): chkconfig
Requires(post): chkconfig

%description -n yum-updateonboot
Runs yum update on system boot. This allows machines that have been turned
off for an extended amount of time to become secure immediately, instead of
waiting until the next early morning cron job.

%package -n yum-plugin-changelog
Summary: Yum plugin for viewing package changelogs before/after updating
Group: System Environment/Base
Provides: yum-changelog = %{version}-%{release}
Obsoletes: yum-changelog < 1.1.20-0
Conflicts: yum-changelog < 1.1.20-0
# changelog requires new update_md.UpdateMetadata() API in 3.2.23
Requires: yum >= 3.2.23
Requires: python-dateutil

%description -n yum-plugin-changelog
This plugin adds a command line option to allow viewing package changelog
deltas before or after updating packages.

%package -n yum-plugin-fastestmirror
Summary: Yum plugin which chooses fastest repository from a mirrorlist
Group: System Environment/Base
Provides: yum-fastestmirror = %{version}-%{release}
Obsoletes: yum-fastestmirror < 1.1.20-0
Conflicts: yum-fastestmirror < 1.1.20-0
Requires: yum >= 3.0

%description -n yum-plugin-fastestmirror
This plugin sorts each repository's mirrorlist by connection speed
prior to downloading packages.

%package -n yum-plugin-protectbase
Summary: Yum plugin to protect packages from certain repositories.
Group: System Environment/Base
Provides: yum-protectbase = %{version}-%{release}
Obsoletes: yum-protectbase < 1.1.20-0
Conflicts: yum-protectbase < 1.1.20-0
Requires: yum >= 3.0

%description -n yum-plugin-protectbase
This plugin allows certain repositories to be protected. Packages in the
protected repositories can't be overridden by packages in non-protected
repositories even if the non-protected repo has a later version.

%package -n yum-plugin-versionlock
Summary: Yum plugin to lock specified packages from being updated
Group: System Environment/Base
Provides: yum-versionlock = %{version}-%{release}
Obsoletes: yum-versionlock < 1.1.20-0
Conflicts: yum-versionlock < 1.1.20-0
Requires: yum >= 3.2.24

%description -n yum-plugin-versionlock
This plugin takes a set of name/versions for packages and excludes all other
versions of those packages (including optionally following obsoletes). This
allows you to protect packages from being updated by newer versions,
for example.

%package -n yum-plugin-tsflags
Summary: Yum plugin to add tsflags by a commandline option
Group: System Environment/Base
Provides: yum-tsflags = %{version}-%{release}
Obsoletes: yum-tsflags < 1.1.20-0
Conflicts: yum-tsflags < 1.1.20-0
Requires: yum >= 3.0

%description -n yum-plugin-tsflags
This plugin allows you to specify optional transaction flags on the yum
command line

%package -n yum-plugin-downloadonly
Summary: Yum plugin to add downloadonly command option
Group: System Environment/Base
Provides: yum-downloadonly = %{version}-%{release}
Obsoletes: yum-downloadonly < 1.1.20-0
Conflicts: yum-downloadonly < 1.1.20-0
Requires: yum >= 3.0

%description -n yum-plugin-downloadonly
This plugin adds a --downloadonly flag to yum so that yum will only download
the packages and not install/update them.

%package -n yum-plugin-priorities
Summary: plugin to give priorities to packages from different repos
Group: System Environment/Base
Provides: yum-priorities = %{version}-%{release}
Obsoletes: yum-priorities < 1.1.20-0
Conflicts: yum-priorities < 1.1.20-0
Requires: yum >= 3.0

%description -n yum-plugin-priorities
This plugin allows repositories to have different priorities.
Packages in a repository with a lower priority can't be overridden by packages
from a repository with a higher priority even if repo has a later version.

%package -n yum-plugin-refresh-updatesd
Summary: Tell yum-updatesd to check for updates when yum exits
Group: System Environment/Base
Provides: yum-refresh-updatesd = %{version}-%{release}
Obsoletes: yum-refresh-updatesd < 1.1.20-0
Conflicts: yum-refresh-updatesd < 1.1.20-0
Requires: yum >= 3.0
Requires: yum-updatesd

%description -n yum-plugin-refresh-updatesd
yum-refresh-updatesd tells yum-updatesd to check for updates when yum exits.
This way, if you run 'yum update' and install all available updates, puplet
will almost instantly update itself to reflect this.

%package -n yum-plugin-merge-conf
Summary: Yum plugin to merge configuration changes when installing packages
Group: System Environment/Base
Provides: yum-merge-conf = %{version}-%{release}
Obsoletes: yum-merge-conf < 1.1.20-0
Conflicts: yum-merge-conf < 1.1.20-0
Requires: yum >= 3.0

%description -n yum-plugin-merge-conf
This yum plugin adds the "--merge-conf" command line option. With this option,
Yum will ask you what to do with config files which have changed on updating a
package.

%package -n yum-plugin-security
Summary: Yum plugin to enable security filters
Group: System Environment/Base
Provides: yum-security = %{version}-%{release}
Obsoletes: yum-security < 1.1.20-0
Conflicts: yum-security < 1.1.20-0
Requires: yum >= 3.2.18

%description -n yum-plugin-security
This plugin adds the options --security, --cve, --bz and --advisory flags
to yum and the list-security and info-security commands.
The options make it possible to limit list/upgrade of packages to specific
security relevant ones. The commands give you the security information.

%package -n yum-plugin-upgrade-helper
Summary: Yum plugin to help upgrades to the next distribution version
Group: System Environment/Base
Provides: yum-upgrade-helper = %{version}-%{release}
Obsoletes: yum-upgrade-helper < 1.1.20-0
Conflicts: yum-upgrade-helper < 1.1.20-0
Requires: yum >= 3.0

%description -n yum-plugin-upgrade-helper
this plugin allows yum to erase specific packages on install/update based on an additional
metadata file in repositories. It is used to simplify distribution upgrade hangups.

%package -n yum-plugin-aliases
Summary: Yum plugin to enable aliases filters
Group: System Environment/Base
Provides: yum-aliases = %{version}-%{release}
Obsoletes: yum-aliases < 1.1.20-0
Conflicts: yum-aliases < 1.1.20-0
# Requires args_hook
Requires: yum >= 3.2.23
Requires: yum-utils-translations = %{version}-%{release}

%description -n yum-plugin-aliases
This plugin adds the command alias, and parses the aliases config. file to
enable aliases.

%package -n yum-plugin-list-data
Summary: Yum plugin to list aggregate package data
Group: System Environment/Base
Provides: yum-list-data = %{version}-%{release}
Obsoletes: yum-list-data < 1.1.20-0
Conflicts: yum-list-data < 1.1.20-0
Requires: yum >= 3.0.5

%description -n yum-plugin-list-data
This plugin adds the commands list- vendors, groups, packagers, licenses,
arches, committers, buildhosts, baseurls, package-sizes, archive-sizes and
installed-sizes.

%package -n yum-plugin-filter-data
Summary: Yum plugin to list filter based on package data
Group: System Environment/Base
Provides: yum-filter-data = %{version}-%{release}
Obsoletes: yum-filter-data < 1.1.20-0
Conflicts: yum-filter-data < 1.1.20-0
Requires: yum >= 3.2.17

%description -n yum-plugin-filter-data
This plugin adds the options --filter- vendors, groups, packagers, licenses,
arches, committers, buildhosts, baseurls, package-sizes, archive-sizes and
installed-sizes. Note that each package must match at least one pattern/range in
each category, if any were specified.

%package -n yum-plugin-tmprepo
Summary: Yum plugin to add temporary repositories
Group: System Environment/Base
Provides: yum-tmprepo = %{version}-%{release}
Obsoletes: yum-tmprepo < 1.1.20-0
Conflicts: yum-tmprepo < 1.1.20-0
Requires: yum >= 3.2.11
Requires: createrepo

%description -n yum-plugin-tmprepo
This plugin adds the option --tmprepo which takes a url to a .repo file
downloads it and enables it for a single run. This plugin tries to ensure
that temporary repositories are safe to use, by default, by not allowing
gpg checking to be disabled.

%package -n yum-plugin-verify
Summary: Yum plugin to add verify command, and options
Group: System Environment/Base
Provides: yum-verify = %{version}-%{release}
Obsoletes: yum-verify < 1.1.20-0
Conflicts: yum-verify < 1.1.20-0
Requires: yum >= 3.2.12

%description -n yum-plugin-verify
This plugin adds the commands verify, verify-all and verify-rpm. There are
also a couple of options. This command works like rpm -V, to verify your
installation.

%package -n yum-plugin-keys
Summary: Yum plugin to deal with signing keys
Group: System Environment/Base
Provides: yum-keys = %{version}-%{release}
Obsoletes: yum-keys < 1.1.20-0
Conflicts: yum-keys < 1.1.20-0
Requires: yum >= 3.2.19

%description -n yum-plugin-keys
This plugin adds the commands keys, keys-info, keys-data and keys-remove. They
allow you to query and remove signing keys.

%package -n yum-plugin-remove-with-leaves
Summary: Yum plugin to remove dependencies which are no longer used because of a removal
Group: System Environment/Base
Provides: yum-remove-with-leaves = %{version}-%{release}
Obsoletes: yum-remove-with-leaves < 1.1.20-0
Conflicts: yum-remove-with-leaves < 1.1.20-0
Requires: yum >= 3.2.19

%description -n yum-plugin-remove-with-leaves
This plugin removes any unused dependencies that were brought in by an install
but would not normally be removed. It helps to keep a system clean of unused
libraries and packages.

%package -n yum-plugin-post-transaction-actions
Summary: Yum plugin to run arbitrary commands when certain pkgs are acted on
Group: System Environment/Base
Provides: yum-post-transaction-actions = %{version}-%{release}
Obsoletes: yum-post-transaction-actions < 1.1.20-0
Conflicts: yum-post-transaction-actions < 1.1.20-0
Requires: yum >= 3.2.19

%description -n yum-plugin-post-transaction-actions
This plugin allows the user to run arbitrary actions immediately following a
transaction when specified packages are changed.

%package -n yum-NetworkManager-dispatcher
Summary: NetworkManager script which tells yum to check it's cache on network change
Group: System Environment/Base
Requires: yum >= 3.2.17

%description -n yum-NetworkManager-dispatcher
This NetworkManager "dispatch script" forces yum to check its cache if/when a
new network connection happens in NetworkManager. Note that currently there is
no checking of previous data, so if your WiFi keeps going up and down (or you
suspend/resume a lot) yum will recheck its cached data a lot.

%package -n yum-plugin-rpm-warm-cache
Summary: Yum plugin to access the rpmdb files early to warm up access to the db 
Group: System Environment/Base
Provides: yum-rpm-warm-cache = %{version}-%{release}
Obsoletes: yum-rpm-warm-cache < 1.1.20-0
Conflicts: yum-rpm-warm-cache < 1.1.20-0
Requires: yum >= 3.2.19

%description -n yum-plugin-rpm-warm-cache
This plugin reads the rpmdb files into the system cache before accessing the
rpmdb directly. In some cases this should speed up access to rpmdb information

%package -n yum-plugin-auto-update-debug-info
# Works by searching for *-debuginfo ... so it shouldn't trigger on itself.
Summary: Yum plugin to enable automatic updates to installed debuginfo packages
Group: System Environment/Base
Obsoletes: yum-plugin-auto-update-debuginfo < 1.1.21-0
Conflicts: yum-plugin-auto-update-debuginfo < 1.1.21-0
Provides: yum-plugin-auto-update-debuginfo = %{version}-%{release}
Requires: yum >= 3.2.19

%description -n yum-plugin-auto-update-debug-info
This plugin looks to see if any debuginfo packages are installed, and if there
are it enables all debuginfo repositories that are "children" of enabled
repositories.

%package -n yum-plugin-show-leaves
Summary: Yum plugin which shows newly installed leaf packages
Group: System Environment/Base
Requires: yum >= 3.2.23

%description -n yum-plugin-show-leaves
Yum plugin which shows newly installed leaf packages
and packages that became leaves after a transaction

%package -n yum-plugin-local
Summary: Yum plugin to automatically manage a local repo. of downloaded packages
Group: System Environment/Base
# Who the hell knows what version :)
Requires: yum >= 3.2.22
Requires: createrepo

%description -n yum-plugin-local
When this plugin is installed it will automatically copy all downloaded packages
to a repository on the local filesystem, and (re)build that repository. This
means that anything you've downloaded will always exist, even if the original
repo. removes it (and can thus. be reinstalled/downgraded/etc.).

%package -n yum-plugin-fs-snapshot
Summary: Yum plugin to automatically snapshot your filesystems during updates
Group: System Environment/Base
Requires: yum >= 3.2.22

%description -n yum-plugin-fs-snapshot
When this plugin is installed it will automatically snapshot any
filesystem that is touched by the packages in a yum update or yum remove.

%package -n yum-plugin-ps
Summary: Yum plugin to look at processes, with respect to packages
Group: System Environment/Base
Requires: yum >= 3.2.27

%description -n yum-plugin-ps
When this plugin is installed it adds the yum command "ps", which allows you
to see which running processes are accociated with which packages (and if they
need rebooting, or have updates, etc.)

%package -n yum-plugin-puppetverify
Summary: Yum plugin to add puppet checksums to verify data
Group: System Environment/Base
Provides: yum-puppetverify = %{version}-%{release}
Requires: yum >= 3.2.12
Requires: PyYAML >= 3.09
Requires: puppet

%description -n yum-plugin-puppetverify
Supplies checksums for files in packages from puppet's state file. 

%prep
%if %{?svn_rev:%(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')}%{!?svn_rev):0}
%setup -q
%else
%setup -n "%{name}-%{version}" -Tc
svn export %{?svn_rev:-r %{svn_rev}} %{svn_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip" "%{name}-%{version}")
%endif

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
#make -C updateonboot DESTDIR=$RPM_BUILD_ROOT install

%find_lang %name

# Plugins to install
plugins="\
 changelog \
 fastestmirror \
 protectbase \
 versionlock \
 tsflags \
 downloadonly \
 priorities \
 refresh-updatesd \
 merge-conf \
 security \
 upgrade-helper \
 aliases \
 list-data \
 filter-data \
 tmprepo \
 verify \
 keys \
 remove-with-leaves \
 post-transaction-actions \
 rpm-warm-cache \
 auto-update-debuginfo \
 show-leaves \
 local \
 fs-snapshot \
 ps \
 puppetverify \
"

mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/yum/pluginconf.d/ $RPM_BUILD_ROOT/%{_prefix}/lib/yum-plugins/
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/yum/post-actions

cd plugins
for plug in $plugins; do
    install -m 644 $plug/*.conf $RPM_BUILD_ROOT/%{_sysconfdir}/yum/pluginconf.d/
    install -m 644 $plug/*.py $RPM_BUILD_ROOT/%{_prefix}/lib/yum-plugins/
    %{__python} -c "import compileall; compileall.compile_dir('$RPM_BUILD_ROOT/%{_prefix}/lib/yum-plugins', 1)"
done
install -m 644 aliases/aliases $RPM_BUILD_ROOT/%{_sysconfdir}/yum/aliases.conf
install -m 644 versionlock/versionlock.list $RPM_BUILD_ROOT/%{_sysconfdir}/yum/pluginconf.d/
# need for for the ghost in files section of yum-plugin-local
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/yum.repos.d
touch $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d/_local.repo


%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-, root, root)
%doc README yum-util-cli-template
%doc COPYING
%doc plugins/README
%{_sysconfdir}/bash_completion.d
%{_bindir}/debuginfo-install
%{_bindir}/find-repos-of-install
%{_bindir}/needs-restarting
%{_bindir}/package-cleanup
%{_bindir}/repoclosure
%{_bindir}/repodiff
%{_bindir}/repomanage
%{_bindir}/repoquery
%{_bindir}/repotrack
%{_bindir}/reposync
%{_bindir}/repo-graph
%{_bindir}/repo-rss
%{_bindir}/verifytree
%{_bindir}/yumdownloader
%{_bindir}/yum-builddep
%{_bindir}/yum-config-manager
%{_bindir}/yum-debug-dump
%{_bindir}/yum-groups-manager
%{_bindir}/yum-debug-restore
%{_bindir}/show-installed
%{_bindir}/show-changed-rco
%{_sbindir}/yum-complete-transaction
%{_sbindir}/yumdb
%{python_sitelib}/yumutils/
%{_mandir}/man1/yum-utils.1
%{_mandir}/man1/debuginfo-install.1
%{_mandir}/man1/package-cleanup.1
%{_mandir}/man1/repo-rss.1
%{_mandir}/man1/repoquery.1
%{_mandir}/man1/repodiff.1
%{_mandir}/man1/reposync.1
%{_mandir}/man1/show-changed-rco.1
%{_mandir}/man1/show-installed.1
%{_mandir}/man1/yum-builddep.1
%{_mandir}/man1/yum-debug-dump.1
%{_mandir}/man8/yum-complete-transaction.8
%{_mandir}/man1/yum-groups-manager.1
%{_mandir}/man8/yumdb.8
%{_mandir}/man1/yumdownloader.1

%files -n yum-updateonboot
%defattr(-, root, root)
%doc updateonboot/README COPYING
#%config(noreplace) %{_sysconfdir}/sysconfig/yum-updateonboot
#%{_initrddir}/yum-updateonboot

%files -n yum-plugin-changelog
%defattr(-, root, root)
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/changelog.conf
%doc COPYING
%{_libdir}/yum-plugins/changelog.*
%{_mandir}/man1/yum-changelog.1
%{_mandir}/man5/yum-changelog.conf.5

%files -n yum-plugin-fastestmirror
%defattr(-, root, root)
%doc COPYING
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/fastestmirror.conf
%{_libdir}/yum-plugins/fastestmirror*.*

%files -n yum-plugin-protectbase
%defattr(-, root, root)
%doc COPYING
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/protectbase.conf
%{_libdir}/yum-plugins/protectbase.*

%files -n yum-plugin-versionlock
%defattr(-, root, root)
%doc plugins/versionlock/README COPYING
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/versionlock.conf
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/versionlock.list
%{_libdir}/yum-plugins/versionlock.*
%{_mandir}/man1/yum-versionlock.1
%{_mandir}/man5/yum-versionlock.conf.5

%files -n yum-plugin-tsflags
%defattr(-, root, root)
%doc COPYING
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/tsflags.conf
%{_libdir}/yum-plugins/tsflags.*

%files -n yum-plugin-downloadonly
%defattr(-, root, root)
%doc COPYING
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/downloadonly.conf
%{_libdir}/yum-plugins/downloadonly.*

%files -n yum-plugin-priorities
%defattr(-, root, root)
%doc COPYING
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/priorities.conf
%{_libdir}/yum-plugins/priorities.*

%files -n yum-plugin-refresh-updatesd
%defattr(-, root, root)
%doc COPYING
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/refresh-updatesd.conf
%{_libdir}/yum-plugins/refresh-updatesd.*

%files -n yum-plugin-merge-conf
%defattr(-, root, root)
%doc COPYING
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/merge-conf.conf
%{_libdir}/yum-plugins/merge-conf.*

%files -n yum-plugin-security
%defattr(-, root, root)
%doc COPYING
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/security.conf
%{_libdir}/yum-plugins/security.*
%{_mandir}/man8/yum-security.8

%files -n yum-plugin-upgrade-helper
%defattr(-, root, root)
%doc COPYING
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/upgrade-helper.conf
%{_libdir}/yum-plugins/upgrade-helper.*

%files -n yum-plugin-aliases
%defattr(-, root, root)
%doc COPYING
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/aliases.conf
%config(noreplace) %{_sysconfdir}/yum/aliases.conf
%{_libdir}/yum-plugins/aliases.*
%{_mandir}/man1/yum-aliases.1

%files -n yum-plugin-list-data
%defattr(-, root, root)
%doc COPYING
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/list-data.conf
%{_libdir}/yum-plugins/list-data.*
%{_mandir}/man1/yum-list-data.1

%files -n yum-plugin-filter-data
%defattr(-, root, root)
%doc COPYING
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/filter-data.conf
%{_libdir}/yum-plugins/filter-data.*
%{_mandir}/man1/yum-filter-data.1

%files -n yum-plugin-tmprepo
%defattr(-, root, root)
%doc COPYING
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/tmprepo.conf
%{_libdir}/yum-plugins/tmprepo.*

%files -n yum-plugin-verify
%defattr(-, root, root)
%doc COPYING
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/verify.conf
%{_libdir}/yum-plugins/verify.*
%{_mandir}/man1/yum-verify.1

%files -n yum-plugin-keys
%defattr(-, root, root)
%doc COPYING
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/keys.conf
%{_libdir}/yum-plugins/keys.*

%files -n yum-NetworkManager-dispatcher
%defattr(-, root, root)
%doc COPYING
/@unixroot/etc/NetworkManager/dispatcher.d/*

%files -n yum-plugin-remove-with-leaves
%defattr(-, root, root)
%doc COPYING
%{_libdir}/yum-plugins/remove-with-leaves.*
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/remove-with-leaves.conf

%files -n yum-plugin-post-transaction-actions
%defattr(-, root, root)
%doc COPYING
%{_libdir}/yum-plugins/post-transaction-actions.*
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/post-transaction-actions.conf
%doc plugins/post-transaction-actions/sample.action
# Default *.action file dropping dir.
%dir %{_sysconfdir}/yum/post-actions

%files -n yum-plugin-rpm-warm-cache
%defattr(-, root, root)
%doc COPYING
%{_libdir}/yum-plugins/rpm-warm-cache.*
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/rpm-warm-cache.conf

%files -n yum-plugin-auto-update-debug-info
%defattr(-, root, root)
%doc COPYING
%{_libdir}/yum-plugins/auto-update-debuginfo.*
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/auto-update-debuginfo.conf

%files -n yum-plugin-show-leaves
%defattr(-, root, root)
%doc COPYING
%{_libdir}/yum-plugins/show-leaves.*
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/show-leaves.conf

%files -n yum-plugin-local
%defattr(-, root, root)
%doc COPYING
%ghost %{_sysconfdir}/yum.repos.d/_local.repo
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/local.conf
%{_libdir}/yum-plugins/local.*

%files -n yum-plugin-fs-snapshot
%defattr(-, root, root)
%doc COPYING
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/fs-snapshot.conf
%{_libdir}/yum-plugins/fs-snapshot.*
%{_mandir}/man1/yum-fs-snapshot.1
%{_mandir}/man5/yum-fs-snapshot.conf.5

%files -n yum-plugin-ps
%defattr(-, root, root)
%doc COPYING
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/ps.conf
%{_libdir}/yum-plugins/ps.*

%files -n yum-plugin-puppetverify
%defattr(-, root, root)
%doc COPYING
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/puppetverify.conf
%{_libdir}/yum-plugins/puppetverify.*

%changelog
* Mon Jun 13 2016 yd <yd@os2power.com> 1.1.31-3
- r1598, hardcode install path until ticket#71 gets fixed.
- use correct set of files for installation, fixes ticket#92.
- added macros to allow building from svn

* Mon Apr 07 2014 yd
- build for python 2.7.

* Wed Jun 05 2013 yd
- r639, initial public build.
