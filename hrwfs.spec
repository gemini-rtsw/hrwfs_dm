%define debug_package %{nil}
%define _build_id_links none

%define name hrwfs
%define version 3.7
%define release 3
%define repository gemini
%define _prefix /gemsoft
%define epics_arch linux-x86_64

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
# opiGEM supplies adl2dl (.adl -> .dl, see configure/CONFIG_SITE) and dm2-4.
# perl IS the EPICS 3.14.12 build system -- convertRelease.pl and
# installEpics.pl drive every install step -- and the Rocky base image ships
# the interpreter without the core modules they use (FindBin, File::Copy).
BuildRequires: epics-base-devel = 3.14.12-10%{?dist}.gemini
BuildRequires: epics_extension-opiGEM-devel = 1.0-11%{?dist}.gemini
BuildRequires: perl
Requires: epics_extension-opiGEM

%description
Package %{name} provides the DM screens for the module hrwfs.

%package ws
Summary: %{name}-ws Package
Group: Gemini
# hrwfs_dm.sh is a csh script.
Requires: epics_extension-opiGEM tcsh
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

cp -r bin/%{epics_arch}/* $RPM_BUILD_ROOT/%{_prefix}/bin/
cp -r data/*.dl $RPM_BUILD_ROOT/%{_prefix}/share/dl/%{name}

chmod -R u+w $RPM_BUILD_ROOT/%{_prefix}/bin
chmod -R u+w $RPM_BUILD_ROOT/%{_prefix}/share

%clean
rm -rf $RPM_BUILD_ROOT

%files ws
%defattr(-,root,root)
/%{_prefix}/bin/*
/%{_prefix}/share/dl/*

%changelog
 * Thu Jan 23 2008 Javier Lührs
 - Initial release
 * Fri Apr 25 2008 Javier Lührs
 - Updated rpm build files.
 - Created subpackage hrwfs-ws for the workstation stuff.
