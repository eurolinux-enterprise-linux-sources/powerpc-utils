Name:           powerpc-utils
Version:        1.2.18
Release:        1%{?dist}
Summary:        Utilities for PowerPC platforms

Group:          System Environment/Base
License:        CPL
URL:            http://sourceforge.net/projects/%{name}/
Source0:        http://prdownloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source1:        nvsetenv
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  zlib-devel doxygen automake librtas-devel libservicelog-devel >= 1.0.1-2

# should be fixed - libservicelog is not right name
Requires:       libservicelog bc which
ExclusiveArch:  ppc ppc64

# This hack is needed only for platforms with autoconf < 2.63
Patch0:		powerpc-utils-autoconf.patch
Patch1:		powerpc-utils-1.2.15-man.patch

# This is done before release of F12
Obsoletes:      powerpc-utils-papr < 1.1.6-3
Provides:       powerpc-utils-papr = 1.1.6-3

Requires:       powerpc-utils-python

%description
Utilities for PowerPC platforms.

%prep
%setup -q

# This hack is needed only for platforms with autoconf < 2.63
%if 0%{?fedora} < 9 && 0%{?rhel} < 6
%patch0 -p1 -b .aconf
%endif
%patch1 -p1 -b .man

%build
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT FILES= RCSCRIPTS=
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_sbindir}/nvsetenv

%define pkgdocdir %{_datadir}/doc/%{name}-%{version}
# move doc files
mkdir -p $RPM_BUILD_ROOT%{pkgdocdir}
install $RPM_BUILD_ROOT/usr/share/doc/packages/powerpc-utils/* -t $RPM_BUILD_ROOT%{pkgdocdir}
rm -rf $RPM_BUILD_ROOT/usr/share/doc/packages/powerpc-utils

# remove init script and perl script. They are deprecated
rm -rf $RPM_BUILD_ROOT/etc/init.d/ibmvscsis.sh $RPM_BUILD_ROOT/usr/sbin/vscsisadmin

# nvsetenv is just a wrapper to nvram
ln -s nvram.8.gz $RPM_BUILD_ROOT/%{_mandir}/man8/nvsetenv.8.gz

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_sbindir}/nvsetenv
%{_sbindir}/nvram
%{_sbindir}/snap
%{_sbindir}/bootlist
%{_sbindir}/ofpathname
%{_sbindir}/ppc64_cpu
%{_sbindir}/lsdevinfo
%{_sbindir}/lsprop
%{_mandir}/man8/nvram.8*
%{_mandir}/man8/nvsetenv.8*
%{_mandir}/man8/snap.8*
%{_mandir}/man8/bootlist.8*
%{_mandir}/man8/ofpathname.8*

%{_sbindir}/update_flash
%{_sbindir}/activate_firmware
%{_sbindir}/set_poweron_time
%{_sbindir}/rtas_ibm_get_vpd
%{_sbindir}/serv_config
%{_sbindir}/uesensor
%{_sbindir}/hvcsadmin
%{_sbindir}/rtas_dump
%{_sbindir}/rtas_event_decode
%{_sbindir}/sys_ident
%{_sbindir}/drmgr
%{_sbindir}/lsslot
%{_sbindir}/ls-vdev
%{_sbindir}/ls-veth
%{_sbindir}/ls-vscsi
%{_sbindir}/lparstat

%{_bindir}/amsstat
%{_mandir}/man8/update_flash.8*
%{_mandir}/man8/activate_firmware.8*
%{_mandir}/man8/set_poweron_time.8*
%{_mandir}/man8/rtas_ibm_get_vpd.8*
%{_mandir}/man8/serv_config.8*
%{_mandir}/man8/uesensor.8*
%{_mandir}/man8/hvcsadmin.8*
%{_mandir}/man8/rtas_dump.8*
%{_mandir}/man8/sys_ident.8*
%{_mandir}/man8/lparstat.8*
%{_mandir}/man5/lparcfg.5*
%{_mandir}/man1/amsstat.1*
%{_mandir}/man8/lsdevinfo.8*
%{_mandir}/man8/rtas_event_decode.8*
%{_mandir}/man8/ls-vdev.8*
%{_mandir}/man8/lsslot.8*
%{_mandir}/man8/lsprop.8*
%{_mandir}/man8/drmgr.8*
%{_mandir}/man8/ls-veth.8*
%{_mandir}/man8/ppc64_cpu.8*
%{_mandir}/man8/ls-vscsi.8*
%doc README COPYRIGHT Changelog

%post

%preun

%changelog
* Wed Sep 25 2013 Filip Kocina <fkocina@redhat.com> - 1.2.18-1
- Resolves: #1011038 - updated to latest upstream 1.2.18

* Thu Sep 12 2013 Filip Kocina <fkocina@redhat.com> - 1.2.17-1
- Resolves: #947179 - updated to latest upstream 1.2.17 && applying patch nvram

* Wed Jun 26 2013 Tony Breeds <tony@bakeyournoodle.com> - 1.2.16-2
- drmgr: Check for rpadlpar_io module
- resolves: #972606

* Tue May 21 2013 Vasant Hegde <hegdevasant@linux.vnet.ibm.com> - 1.2.16
- Update to latest upstream 1.2.16

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 16 2013 Karsten Hopp <karsten@redhat.com> 1.2.15-1
- update to 1.2.15
- usysident/usysattn got moved to ppc64-diag package
- multipath ofpathname patch removed as it is upstream now

* Tue Dec 18 2012 Filip Kocina <fkocina@redhat.com> 1.2.14-1
- Resolves: #859222 - updated to latest upstream 1.2.14

* Thu Dec 13 2012 Karsten Hopp <karsten@redhat.com> 1.2.12-4
- Add multipath support to ofpathname for bug #884826

* Tue Sep 04 2012 Karsten Hopp <karsten@redhat.com> 1.2.12-3
- require powerpc-utils-python (#852326 comment 7)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Mar 22 2012 Jiri Skala <jskala@redhat.com> - 1.2.12-1
- updated to latest upstream 1.2.12

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 03 2011 Jiri Skala <jskala@redhat.com> - 1.2.11-2
- updated dependecy

* Mon Oct 31 2011 Jiri Skala <jskala@redhat.com> - 1.2.11-1
- updated to latest upstream 1.2.11
-fixes #749892 - powerpc-utils spec file missing dependency

* Mon Aug 05 2011 Jiri Skala <jskala@redhat.com> - 1.2.10-1
- updated to latest upstream 1.2.10

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 24 2011 Jiri Skala <jskala@redhat.com> - 1.2.6-1
- updated to latest upstream 1.2.6
- removed amsvis man page (amsvis moved to powerpc-utils-python)
- added lparcfg man page - doc to /proc/ppc64/lparcfg

* Thu Jun 24 2010 Roman Rakus <rrakus@redhat.com> - 1.2.2-14
- Compile with -fno-strict-aliasing CFLAG
- linked nvsetenv man page to nvram man page
- Updated man page of ofpathname
- Updated amsstat script

* Tue Jun 15 2010 Roman Rakus <rrakus@redhat.com> - 1.2.2-11
- Correct the parameter handling of ppc64_cpu when setting the run-mode

* Wed Jun 09 2010 Roman Rakus <rrakus@redhat.com> - 1.2.2-10
- Added some upstream patches
- also bump release

* Wed Jun 02 2010 Roman Rakus <rrakus@redhat.com> - 1.2.2-4
- correct the parameter checking when attempting to set the run mode
- also bump release

* Fri Mar 05 2010 Roman Rakus <rrakus@redhat.com> - 1.2.2-2
- Removed deprecated init script and perl script

* Thu Oct 29 2009 Stepan Kasal <skasal@redhat.com> - 1.2.2-1
- new upstream version
- amsvis removed, this package has no longer anything with python
- change the manual pages in the file list so that it does not depend on
  particular compression used
- add patch for configure.ac on platforms with autoconf < 2.63
- use standard %%configure/make in %%build

* Mon Aug 17 2009 Roman Rakus <rrakus@redhat.com> - 1.2.0-1
- Bump tu version 1.2.0 - powerpc-utils and powerpc-utils-papr get merged

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Apr 06 2009 Roman Rakus <rrakus@redhat.com> - 1.1.3-1
- new upstream version 1.1.3

* Tue Mar 03 2009 Roman Rakus <rrakus@redhat.com> - 1.1.2-1
- new upstream version 1.1.2

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 19 2009 Roman Rakus <rrakus@redhat.com> - 1.1.1-1
- new upstream version 1.1.1

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.6-3
- Autorebuild for GCC 4.3

* Mon Dec  3 2007 David Woodhouse <dwmw2@redhat.com> 1.0.6-2
- Add --version to nvsetenv, for ybin compatibility

* Fri Nov 23 2007 David Woodhouse <dwmw2@redhat.com> 1.0.6-1
- New package, split from ppc64-utils
