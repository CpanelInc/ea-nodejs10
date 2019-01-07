Name:    ea-nodejs10
Vendor:  cPanel, Inc.
Summary: Node.js 10
Version: 10.15.0
# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4572 for more details
%define release_prefix 1
Release: %{release_prefix}%{?dist}.cpanel
License: MIT
Group:   Development/Languages
URL:  https://nodejs.org
Source0: https://nodejs.org/dist/v10.15.0/node-v10.15.0-linux-x64.tar.xz

%description
Node.js is a JavaScript runtime built on Chrome's V8 JavaScript engine.

%prep
%setup -qn node-v%{version}-linux-x64

%build
# empty build section since we're just putting the tarball's contents in place

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf %{buildroot}
mkdir -p $RPM_BUILD_ROOT/opt/cpanel/ea-nodejs10
cp -r ./* $RPM_BUILD_ROOT/opt/cpanel/ea-nodejs10

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf %{buildroot}

%files
/opt/cpanel/ea-nodejs10
%attr(0755,root,root) /opt/cpanel/ea-nodejs10/bin/*

%changelog
* Mon Jan 07 2019 Dan Muey <dan@cpanel.net> - 10.15.0-1
- ZC-3244: Initial ea-nodejs10 (v10.15.0)
