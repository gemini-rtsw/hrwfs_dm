%define _prefix __auto__
%define gemopt opt
%define name hrwfs
%define version __auto__
%define release __auto__
%define repository gemini
%define debug_package %{nil}

Summary: %{name} Package
Name: %{name}
Version: %{version}
Release: %{release}.%{dist}.%{repository}
License: GPL
## Source:%{name}-%{version}.tar.gz
Group: Gemini
Source0: %{name}-%{version}.tar.gz
BuildArch: %{arch}
Prefix: %{_prefix}
## You may specify dependencies here
# BuildRequires:
Requires: epics_extension-opiGEM
## Switch dependency checking off
# AutoReqProv: no

%description
Package %{name} provides the DM screens for the module hrwfs.

%package ws
Summary: %{name}-ws Package
Group: Gemini
BuildRequires: epics_extension-opiGEM
Requires: epics_extension-opiGEM
%description ws
Package %{name}-ws provides the DM screens for the module %{name}.

## If you want to have a devel-package to be generated uncomment the following:
# %package devel
# Summary: %{name}-devel Package
# Group: Development/Gemini
# Requires: %{name}
# %description devel
# This is a default description for the %{name}-devel package

## Of course, you also can create additional packages, e.g for "doc". Just
## follow the same way as I did with "%package devel".

%prep
%setup -n %{name}

%build
make

%install
## Write install instructions here, e.g
## install -D zzz/zzz  $RPM_BUILD_ROOT/%{_prefix}/zzz/zzz
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_prefix}/share/dl/hrwfs
#mkdir -p $RPM_BUILD_ROOT/%{_prefix}/share/alh/hrwfs
mkdir -p $RPM_BUILD_ROOT/%{_prefix}/bin/
#mkdir -p $RPM_BUILD_ROOT/%{_prefix}/var/log

cp -r bin/linux-x86*/* $RPM_BUILD_ROOT/%{_prefix}/bin/
cp -r data/*.dl $RPM_BUILD_ROOT/%{_prefix}/share/dl/hrwfs
#cp -r data/*.tk $RPM_BUILD_ROOT/%{_prefix}/share/dl/hrwfs
#cp -r data/*.config $RPM_BUILD_ROOT/%{_prefix}/share/alh/hrwfs

#touch $RPM_BUILD_ROOT/%{_prefix}/var/log/alarms.log
#touch $RPM_BUILD_ROOT/%{_prefix}/var/log/opmod.log

chmod -R u+w $RPM_BUILD_ROOT/%{_prefix}/bin
chmod -R u+w $RPM_BUILD_ROOT/%{_prefix}/share
#chmod -R u+w $RPM_BUILD_ROOT/%{_prefix}/var/log
#chmod a+w $RPM_BUILD_ROOT/%{_prefix}/var/log/alarms.log
#chmod a+w $RPM_BUILD_ROOT/%{_prefix}/var/log/opmod.log


## if you want to do something after installation uncomment the following
## and list the actions to perform:
# %post
## actions, e.g. /sbin/ldconfig

## If you want to have a devel-package to be generated and do some
## %post-stuff regarding it uncomment the following:
# %post devel

## if you want to do something after uninstallation uncomment the following
## and list the actions to perform. But be aware of e.g. deleting directories,
## see the example below how to do it:
# %postun
## if [ "$1" = "0" ]; then
##	rm -rf %{_prefix}/zzz
## fi

## If you want to have a devel-package to be generated and do some
## %postun-stuff regarding it uncomment the following:
# %postun devel

## Its similar for %pre, %preun, %pre devel, %preun devel.

%clean
## Usually you won't do much more here than
rm -rf $RPM_BUILD_ROOT

%files ws
%defattr(-,root,root)
## list files that are installed here, e.g
## %{_prefix}/zzz/zzz
/%{_prefix}/bin/*
/%{_prefix}/share/dl/*
#/%{_prefix}/share/alh/*
#/%{_prefix}/var/*

## If you want to have a devel-package to be generated uncomment the following
# %files devel
# %defattr(-,root,root)
## list files that are installed by the devel package here, e.g
## %{_prefix}/zzz/zzz


%changelog
## Write changes here, e.g.
# * Thu Dec 6 2007 John Doe <jdoe@gemini.edu> VERSION-RELEASE
# - change made
# - other change made
 * Thu Jan 23 2008 Javier Lührs
 - Initial release
 * Fri Apr 25 2008 Javier Lührs
 - Updated rpm build files.
 - Created subpackage hrwfs-ws for the workstation stuff.
