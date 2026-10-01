%define debug_package %{nil}
%define _build_id_links none

%define name hrwfs
%define version 3.7
%define release 5
%define repository gemini
%define _prefix /gemsoft
%define gemopt opt
# make runs as a 64-bit host build, so its scripts land in bin/linux-x86_64;
# the screens and the dm2-4 that shows them are 32-bit (linux-x86).
%define epics_arch linux-x86_64
%define dm_arch linux-x86

# $GIT_HASH first: build_rpm.sh computes the hash on the HOST and passes it
# into the build container. A bare `git rev-parse` resolves to "nogit"
# whenever git is absent from the builder or trips dubious-ownership, and the
# Release would then no longer name the commit the package came from.
%define git_hash %(if [ -n "$GIT_HASH" ]; then echo "$GIT_HASH"; else git rev-parse --short HEAD 2>/dev/null || echo nogit; fi)

Summary: %{name} Package
Name: %{name}
Version: %{version}
Release: %{release}.%{git_hash}.%{repository}%{?dist}
License: GPL
Group: Gemini
BuildRoot: /var/tmp/%{name}-%{version}-root
Source0: %{name}-%{version}.tar.gz
BuildArch: x86_64
Prefix: %{_prefix}

# Pinned exactly, and with %%{?dist}. The rpm-repo is flat -- el8 and el9 share
# one repo with no dist filtering -- so an unversioned epics-base-devel
# resolves to the highest EVR in it, which is the EPICS 7 build under
# /gem_base: a different tree entirely from the 3.14.12 one configure/RELEASE
# points at.
#
# The screens are 32-bit, as on the workstations, which run the i686 opiGEM:
# a .dl is word-size specific and dm2-4 segfaults reading the other kind. So
# the converter (see configure/CONFIG_SITE) and the runtime both come from the
# i686 opiGEM -- the same 1.0-8 the workstations have, and the pairing pr_dm
# ships with. It requires the i686 epics-base, which is why base is pinned to
# 3.14.12-8 rather than -10: the x86_64 base that runs make must be the same
# build as that i686 one, or the two collide in /gemsoft/opt/epics/base. Do
# not add the x86_64 opiGEM(-devel): it brings a 64-bit dm2-4 into the dev
# image (pr_dm ac1b9c1).
#
# perl IS the EPICS 3.14.12 build system -- convertRelease.pl and
# installEpics.pl drive every install step -- and the Rocky base image ships
# the interpreter without the core modules they use (FindBin, File::Copy).
BuildRequires: epics-base-devel = 3.14.12-8%{?dist}.gemini
BuildRequires: epics_extension-opiGEM(x86-32) = 1.0-8%{?dist}.gemini
BuildRequires: perl
Requires: epics_extension-opiGEM(x86-32)

%description
Package %{name} provides the DM screens for the module hrwfs.

%package ws
Summary: %{name}-ws Package
Group: Gemini
# hrwfs_dm.sh is a csh script.
Requires: epics_extension-opiGEM(x86-32) tcsh
%description ws
Package %{name}-ws provides the DM screens for the module %{name}.

%prep
%setup -n %{name}-%{version}

%build
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_prefix}/share/dl/%{name}
mkdir -p $RPM_BUILD_ROOT/%{_prefix}/bin/
mkdir -p $RPM_BUILD_ROOT/etc/profile.d/

cp -r bin/%{epics_arch}/* $RPM_BUILD_ROOT/%{_prefix}/bin/
cp -r data/*.dl $RPM_BUILD_ROOT/%{_prefix}/share/dl/%{name}

# hrwfs_dm.sh runs "dm2-4" by name, which lives in the opiGEM extensions bin.
# A workstation already has both directories on PATH; a bare container does
# not. /gemsoft/bin is appended, so it cannot shadow anything a site profile
# put ahead of it.
cat > $RPM_BUILD_ROOT/etc/profile.d/%{name}-epics.sh << 'EOF'
#!/bin/bash
export PATH="%{_prefix}/%{gemopt}/epics/extensions/bin/%{dm_arch}:$PATH"
export PATH="$PATH:%{_prefix}/bin"
EOF
chmod 755 $RPM_BUILD_ROOT/etc/profile.d/%{name}-epics.sh

chmod -R u+w $RPM_BUILD_ROOT/%{_prefix}/bin
chmod -R u+w $RPM_BUILD_ROOT/%{_prefix}/share

%clean
rm -rf $RPM_BUILD_ROOT

%files ws
%defattr(-,root,root)
/%{_prefix}/bin/*
/%{_prefix}/share/dl/*
/etc/profile.d/%{name}-epics.sh

%changelog
 * Thu Jan 23 2008 Javier Lührs
 - Initial release
 * Fri Apr 25 2008 Javier Lührs
 - Updated rpm build files.
 - Created subpackage hrwfs-ws for the workstation stuff.
