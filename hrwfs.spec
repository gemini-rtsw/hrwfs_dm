%define _prefix __auto__
%define gemopt opt
%define name hrwfs
%define version 3.7
%define release 2
%define repository gemini
%define debug_package %{nil}

Summary: %{name} Package
Name: %{name}
Version: %{version}
Release: %{release}.%{dist}.%{repository}
License: GPL
Group: Gemini
BuildRoot: /var/tmp/%{name}-%{version}-root
Source0: %{name}-%{version}.tar.gz
BuildArch: %{arch}
Prefix: %{_prefix}
Requires: epics_extension-opiGEM%{?_isa}

%description
Package %{name} provides the DM screens for the module hrwfs.

%package ws
Summary: %{name}-ws Package
Group: Gemini
BuildRequires: epics_extension-opiGEM%{?_isa}
Requires: epics_extension-opiGEM%{?_isa}
%description ws
Package %{name}-ws provides the DM screens for the module %{name}.

%prep
%setup -n %{name}

%build
make

%install
## Write install instructions here, e.g
## install -D zzz/zzz  $RPM_BUILD_ROOT/%{_prefix}/zzz/zzz
%if %{__isa_bits} == 64
host_arch=linux-x86_64
%else
host_arch=linux-x86
%endif

rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_prefix}/share/dl/hrwfs
mkdir -p $RPM_BUILD_ROOT/%{_prefix}/bin/

cp -r bin/$host_arch/* $RPM_BUILD_ROOT/%{_prefix}/bin/
cp -r data/*.dl $RPM_BUILD_ROOT/%{_prefix}/share/dl/hrwfs

chmod -R u+w $RPM_BUILD_ROOT/%{_prefix}/bin
chmod -R u+w $RPM_BUILD_ROOT/%{_prefix}/share


%clean
## Usually you won't do much more here than
rm -rf $RPM_BUILD_ROOT

%files ws
%defattr(-,root,root)
## list files that are installed here, e.g
## %{_prefix}/zzz/zzz
/%{_prefix}/bin/*
/%{_prefix}/share/dl/*


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
