%if 0%{?rhel} >= 8
%global debug_package %{nil}
%endif

Name:    ea-nodejs10
Vendor:  cPanel, Inc.
Summary: Node.js 10
Version: 10.22.0
# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4572 for more details
%define release_prefix 1
Release: %{release_prefix}%{?dist}.cpanel
License: MIT
Group:   Development/Languages
URL:  https://nodejs.org
Source0: https://nodejs.org/dist/v%{version}/node-v%{version}-linux-x64.tar.xz
Patch1: 0001-Ensure-the-RPM-s-npm-and-npx-use-the-RPM-s-node.patch

%description
Node.js is a JavaScript runtime built on Chrome's V8 JavaScript engine.

%prep
%setup -qn node-v%{version}-linux-x64
%if 0%{?rhel} < 8
%patch1 -p1 -b .shebang
%endif

%build
# empty build section since we're just putting the tarball's contents in place

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf %{buildroot}
mkdir -p $RPM_BUILD_ROOT/opt/cpanel/ea-nodejs10
cp -r ./* $RPM_BUILD_ROOT/opt/cpanel/ea-nodejs10
%if 0%{?rhel} >= 8
cd $RPM_BUILD_ROOT/opt/cpanel/ea-nodejs10
# I am not sure why but the equivalent patch did not work, so using the sed hammer
find . -name "*.py" -print | xargs sed -i '1s:^#!/usr/bin/env python$:#!/usr/bin/env python2:' 
sed -i '1s:^#!/usr/bin/python$:#!/usr/bin/python2:' lib/node_modules/npm/node_modules/node-gyp/gyp/samples/samples

# Patch01 only edits 2 files, there are many with node referenced in the
# shebang

for file in `find . -type f -print | xargs grep -l '^#![ \t]*/usr/bin/env node'`
do
    echo "Changing Shebang (env) for" $file
    sed -i '1s:^#![ \t]*/usr/bin/env node:#!/opt/cpanel/ea-nodejs10/bin/node:' $file
done
%endif

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf %{buildroot}

%files
/opt/cpanel/ea-nodejs10
%attr(0755,root,root) /opt/cpanel/ea-nodejs10/bin/*


%changelog
* Mon Aug 03 2020 Cory McIntire <cory@cpanel.net> - 10.22.0-1
- EA-9210: Update ea-nodejs10 from v10.21.0 to v10.22.0

* Mon Jun 29 2020 Julian Brown <julian.brown@cpanel.net> - 10.21.0-2
- ZC-6846: Build on C8

* Mon Jun 08 2020 Cory McIntire <cory@cpanel.net> - 10.21.0-1
- EA-9099: Update ea-nodejs10 from v10.20.1 to v10.21.0

* Wed Apr 15 2020 Cory McIntire <cory@cpanel.net> - 10.20.1-1
- EA-9004: Update ea-nodejs10 from v10.20.0 to v10.20.1

* Thu Apr 09 2020 Cory McIntire <cory@cpanel.net> - 10.20.0-1
- EA-8985: Update ea-nodejs10 from v10.19.0 to v10.20.0

* Tue Mar 03 2020 Cory McIntire <cory@cpanel.net> - 10.19.0-1
- EA-8895: Update ea-nodejs10 from v10.18.1 to v10.19.0

* Wed Jan 22 2020 Cory McIntire <cory@cpanel.net> - 10.18.1-1
- EA-8841: Update ea-nodejs10 from v10.17.0 to v10.18.1

* Wed Oct 23 2019 Cory McIntire <cory@cpanel.net> - 10.17.0-1
- EA-8715: Update ea-nodejs10 from v10.16.3 to v10.17.0

* Tue Sep 03 2019 Cory McIntire <cory@cpanel.net> - 10.16.3-1
- EA-8633: Update ea-nodejs10 from v10.16.2 to v10.16.3

* Thu Aug 08 2019 Cory McIntire <cory@cpanel.net> - 10.16.2-1
- EA-8608: Update ea-nodejs10 from v10.16.1 to v10.16.2

* Thu Aug 01 2019 Cory McIntire <cory@cpanel.net> - 10.16.1-1
- EA-8592: Update ea-nodejs10 from v10.16.0 to v10.16.1

* Thu Jun 27 2019 Cory McIntire <cory@cpanel.net> - 10.16.0-1
- EA-8545: Update ea-nodejs10 from v10.15.3 to v10.16.0

* Thu May 23 2019 Daniel Muey <dan@cpanel.net> - 10.15.3-2
- ZC-5152: Remove `mod_passenger` Requirement from `ea-nodejs`

* Wed May 15 2019 Cory McIntire <cory@cpanel.net> - 10.15.3-1
- EA-8469: Update ea-nodejs10 from v10.15.0 to v10.15.3

* Mon Jan 07 2019 Dan Muey <dan@cpanel.net> - 10.15.0-1
- ZC-3244: Initial ea-nodejs10 (v10.15.0)
