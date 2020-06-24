#% define beta_tag rc2
%define patchleveltag .11
%define baseversion 5.0
%bcond_with tests

%if 0%{?os2_version}
%global create_builtins 0
%else
%global create_builtins 1
%endif

Version: %{baseversion}%{patchleveltag}
Name: bash
Summary: The GNU Bourne Again shell
Release: 3%{?dist}
License: GPLv3+
Url: https://www.gnu.org/software/bash
Vendor: bww bitwise works GmbH
%scm_source github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2-3

# For now there isn't any doc
#Source2: ftp://ftp.gnu.org/gnu/bash/bash-doc-%%{version}.tar.gz


BuildRequires:  gcc
BuildRequires: texinfo bison
BuildRequires: ncurses-devel
BuildRequires: autoconf, gettext
%if 0%{?os2_version}
BuildRequires: readline-devel >= 8.0
%endif
%if !0%{?os2_version}
# Required for bash tests
BuildRequires: glibc-all-langpacks
Requires: filesystem >= 3
Provides: /bin/sh
Provides: /bin/bash
%else
Provides: /@unixroot/bin/bash
Provides: /@unixroot/usr/bin/bash
%endif

%description
The GNU Bourne Again shell (Bash) is a shell or command language
interpreter that is compatible with the Bourne shell (sh). Bash
incorporates useful features from the Korn shell (ksh) and the C shell
(csh). Most sh scripts can be run by bash without modification.

%package devel
Summary: Development headers for %{name}
Requires: %{name} = %{version}-%{release}

%description devel
This package contains development headers for %{name}.

%package doc
Summary: Documentation files for %{name}
Requires: %{name} = %{version}-%{release}

%description doc
This package contains documentation files for %{name}.

%debug_package

%prep
%scm_setup

echo %{version} > _distribution
echo %{release} > _patchlevel

# force refreshing the generated files
rm y.tab.*

%build
autoreconf -fvi

export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"
%configure --with-bash-malloc=no \
  --with-installed-readline=yes

# Recycles pids is neccessary. When bash's last fork's pid was X
# and new fork's pid is also X, bash has to wait for this same pid.
# Without Recycles pids bash will not wait.
make "CPPFLAGS=-D_GNU_SOURCE -DRECYCLES_PIDS" %{?_smp_mflags}

%install
%if !0%{?os2_version}
if [ -e autoconf ]; then
  # Yuck. We're using autoconf 2.1x.
  export PATH=.:$PATH
fi
%endif

# Fix bug #83776
sed -i -e 's,bashref\.info,bash.info,' doc/bashref.info

%make_install install-headers

%if !0%{?os2_version}
mkdir -p %{buildroot}/%{_sysconfdir}
%endif

# make manpages for bash builtins as per suggestion in DOC/README
%if 0%{?create_builtins}
cd doc
sed -e '
/^\.SH NAME/, /\\- bash built-in commands, see \\fBbash\\fR(1)$/{
/^\.SH NAME/d
s/^bash, //
s/\\- bash built-in commands, see \\fBbash\\fR(1)$//
s/,//g
b
}
d
' builtins.1 > man.pages
for i in echo pwd test kill; do
  sed -i -e "s,$i,,g" man.pages
  sed -i -e "s,  , ,g" man.pages
done

install -p -m 644 builtins.1 %{buildroot}%{_mandir}/man1/builtins.1

for i in `cat man.pages` ; do
  echo .so man1/builtins.1 > %{buildroot}%{_mandir}/man1/$i.1
  chmod 0644 %{buildroot}%{_mandir}/man1/$i.1
done
cd ..
%endif

# Link bash man page to sh so that man sh works.
%if !0%{?os2_version}
ln -s bash.1 %{buildroot}%{_mandir}/man1/sh.1
%endif

# Not for printf, true and false (conflict with coreutils)
rm -f %{buildroot}/%{_mandir}/man1/printf.1
rm -f %{buildroot}/%{_mandir}/man1/true.1
rm -f %{buildroot}/%{_mandir}/man1/false.1

%if !0%{?os2_version}
ln -sf bash %{buildroot}%{_bindir}/sh
%endif
rm -f %{buildroot}%{_infodir}/dir
%if !0%{?os2_version}
mkdir -p %{buildroot}%{_sysconfdir}/skel
install -p -m644 %SOURCE1 %{buildroot}/etc/skel/.bashrc
install -p -m644 %SOURCE2 %{buildroot}/etc/skel/.bash_profile
install -p -m644 %SOURCE3 %{buildroot}/etc/skel/.bash_logout
LONG_BIT=$(getconf LONG_BIT)
mv %{buildroot}%{_bindir}/bashbug \
   %{buildroot}%{_bindir}/bashbug-"${LONG_BIT}"
ln -s bashbug-"${LONG_BIT}" %{buildroot}%{_bindir}/bashbug
ln -s bashbug.1 %{buildroot}/%{_mandir}/man1/bashbug-"$LONG_BIT".1
%endif

# Fix missing sh-bangs in example scripts (bug #225609).
for script in \
  examples/scripts/shprompt
# I don't know why these are gone in 4.3
  #examples/scripts/krand.bash \
  #examples/scripts/bcsh.sh \
  #examples/scripts/precedence \
do
  cp "$script" "$script"-orig
  echo '#!/bin/bash' > "$script"
  cat "$script"-orig >> "$script"
  rm -f "$script"-orig
done

# bug #820192, need to add execable alternatives for regular built-ins
%if 0%{?create_builtins}
for ea in alias bg cd command fc fg getopts hash jobs read type ulimit umask unalias wait
do
  cat <<EOF > "%{buildroot}"/%{_bindir}/"$ea"
#!/bin/sh
builtin $ea "\$@"
EOF
chmod +x "%{buildroot}"/%{_bindir}/"$ea"
done
%endif

%find_lang %{name}

# copy doc to /usr/share/doc
cat /dev/null > %{name}-doc.files
mkdir -p %{buildroot}%{_pkgdocdir}
# loadables aren't buildable
rm -rf examples/loadables
rm -rf %{buildroot}/%{_docdir}/bash
for file in CHANGES COMPAT NEWS NOTES POSIX examples
do
  cp -rp "$file" %{buildroot}%{_pkgdocdir}/"$file"
  echo "%%doc %{_pkgdocdir}/$file" >> %{name}-doc.files
done



%if %{with tests}
%check
make check
%endif

# post is in lua so that we can run it without any external deps.  Helps
# for bootstrapping a new install.
# Jesse Keating 2009-01-29 (code from Ignacio Vazquez-Abrams)
# Roman Rakus 2011-11-07 (code from Sergey Romanov) #740611
%if !0%{?os2_version}
%post -p <lua>
nl        = '\n'
sh        = '/bin/sh'..nl
bash      = '/bin/bash'..nl
f = io.open('/etc/shells', 'a+')
if f then
  local shells = nl..f:read('*all')..nl
  if not shells:find(nl..sh) then f:write(sh) end
  if not shells:find(nl..bash) then f:write(bash) end
  f:close()
end

%postun -p <lua>
-- Run it only if we are uninstalling
if arg[2] == "0"
then
  t={}
  for line in io.lines("/etc/shells")
  do
    if line ~= "/bin/bash" and line ~= "/bin/sh"
    then
      table.insert(t,line)
    end
  end

  f = io.open("/etc/shells", "w+")
  for n,line in pairs(t)
  do
    f:write(line.."\n")
  end
  f:close()
end
%endif

%files -f %{name}.lang
%if !0%{?os2_version}
%config(noreplace) /@unixroot/etc/skel/.b*
%{_bindir}/sh
%endif
%{_bindir}/bash.exe
%if 0%{?create_builtins}
%{_bindir}/alias
%{_bindir}/bg
%{_bindir}/cd
%{_bindir}/command
%{_bindir}/fc
%{_bindir}/fg
%{_bindir}/hash
%{_bindir}/getopts
%{_bindir}/jobs
%{_bindir}/read
%{_bindir}/type
%{_bindir}/ulimit
%{_bindir}/umask
%{_bindir}/unalias
%{_bindir}/wait
%endif
%license COPYING
%{_bindir}/bashbug
%{_infodir}/bash.info*
%{_mandir}/*/*
%if 0%{?create_builtins}
%{_mandir}/*/..1*
%endif
%doc RBASH README
%doc doc/FAQ
%doc doc/INTRO
%doc doc/bash.html
%doc doc/bashref.html


%files doc -f %{name}-doc.files
%doc doc/*.ps doc/*.0 doc/*.html doc/article.txt

%files devel
%{_includedir}/%{name}
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Wed Jun 24 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 5.0.11-3
- fixed a double fault, which leads to a kernel trap :( sorry about that

* Mon Jun 22 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 5.0.11-2
- enable system readline
- added BEGINLIBPATH and friends

* Wed May 20 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 5.0.11-1
- updated to version 5.0.11
- use scm_macros and friends
- synced with latest fedora spec

* Fri Feb 19 2016 yd <yd@os2power.com> 3.2.0-8
- added Provides for virtual /@unixroot/usr/bin/bash file.

* Sat Feb 04 2012 yd
- added Provides for virtual /@unixroot/bin/bash file.
- Remove symlinks from /bin.

* Wed Nov 16 2011 yd
- keep all executables to /usr/bin and place symlinks in /bin
