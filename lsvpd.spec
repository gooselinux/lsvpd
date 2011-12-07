Name:		lsvpd
Version:	1.6.7
Release:	3%{?dist}
Summary:	VPD/hardware inventory utilities for Linux

Group:		Applications/System
License:	GPLv2+
URL:		http://linux-diag.sf.net/Lsvpd.html
Source:		http://downloads.sourceforge.net/linux-diag/%{name}-%{version}.tar.gz
Patch0:		lsvpd-1.6.4-sg3_utils-1.26.patch
Patch1:		lsvpd-1.6.7-ids-lookup.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	sg3_utils-devel libvpd-devel zlib-devel
Requires(post): /usr/sbin/vpdupdate

# By default, build without librtas because it does not yet exist in Fedora

# librtas is now part of Fedora, lsvpd provides much more information with
# librtas on POWER
#%{!?_with_librtas: %{!?_without_librtas: %define _without_librtas --without-librtas }}

%ifarch ppc
%{?_with_librtas:BuildRequires: librtas-devel }
%endif
%ifarch ppc64
%{?_with_librtas:BuildRequires: librtas-devel }
%endif

%description
The lsvpd package contains all of the lsvpd, lscfg and lsmcode
commands. These commands, along with a scanning program
called vpdupdate, constitute a hardware inventory
system. The lsvpd command provides Vital Product Data (VPD) about
hardware components to higher-level serviceability tools. The lscfg
command provides a more human-readable format of the VPD, as well as
some system-specific information.  lsmcode lists microcode and
firmware levels.  lsvio lists virtual devices, usually only found
on POWER PC based systems.

%prep
%setup -q
%patch0 -p1
%patch1 -p0

%build
%configure
%{__make} %{?_smp_mflags}

%clean 
%{__rm} -rf $RPM_BUILD_ROOT

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT

%post -p /usr/sbin/vpdupdate

%files 
%defattr(-,root,root,-)
%doc COPYING INSTALL NEWS README TODO
%{_sbindir}/lsvpd
%{_sbindir}/lscfg
%{_sbindir}/lsmcode
%{_sbindir}/lsvio
%{_sbindir}/vpdupdate
%{_mandir}/man8/vpdupdate.8.gz
%{_mandir}/man8/lsvpd.8.gz
%{_mandir}/man8/lscfg.8.gz
%{_mandir}/man8/lsvio.8.gz
%{_mandir}/man8/lsmcode.8.gz
%config %{_sysconfdir}/lsvpd/scsi_templates.conf
%config %{_sysconfdir}/lsvpd/cpu_mod_conv.conf
%dir %{_sysconfdir}/lsvpd

%changelog
* Thu Feb 18 2010 Roman Rakus <rrakus@redhat.com> 1.6.7-3
- Get a rid of define {name,version}

* Thu Feb 11 2010 Roman Rakus <rrakus@redhat.com> 1.6.7-2
- Initial RHEL-6 build

* Wed Dec 02 2009 Eric Munson <ebmunson@us.ibm.com> - 1.6.7-1
- Update to latest lsvpd release
- Add librtas support to build on POWERPC
- Add patch to lookup *.ids file location at runtime

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Apr 28 2009 - Dan Horak <dan[at]danny.cz> - 1.6.5-2
- rebuild for sg3_utils 1.27

* Mon Mar 16 2009 Eric Munson <ebmunson@us.ibm.com> - 1.6.5-1
- Update source to use new glibc C header includes

* Mon Mar 16 2009 Eric Munson <ebmunson@us.ibm.com> - 1.6.4-6
- Bump for rebuild against latest build of libvpd

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Aug 14 2008 - Eric Munson <ebmunson@us.ibm.com> - 1.6.4-4
- Bump for rebuild with new libvpd.

* Mon Jun 30 2008 - Dan Horak <dan[at]danny.cz> - 1.6.4-3
- add patch for sg3_utils 1.26 and rebuild

* Fri Jun 06 2008 - Caolán McNamara <caolanm@redhat.com> - 1.6.4-2
- rebuild for dependancies

* Fri Apr 25 2008 - Brad Peters <bpeters@us.ibm.com> - 1.6.4-1
- Adding ability to limit SCSI direct inquiry size, fixing Windows SCSI
  device inquiry problem

* Fri Mar 21 2008 - Eric Munson <ebmunson@us.ibm.com> - 1.6.3-1
- Adding proper conf file handling
- Removing executable bit on config and documentation files
- Removing second listing for config files

* Fri Mar 14 2008 - Eric Munson <ebmunson@us.ibm.com> - 1.6.2-3
- Becuase librtas is not yet in Fedora, the extra ppc dependency should
  be ignored

* Thu Mar 13 2008 - Eric Munson <ebmunson@us.ibm.com> - 1.6.2-2
- Adding arch check for ppc[64] dependency.

* Tue Mar 4 2008 - Eric Munson <ebmunson@us.ibm.com> - 1.6.2-1
- Updating for lsvpd-1.6.2

* Tue Mar 3 2008 - Eric Munson <ebmunson@us.ibm.com> - 1.6.1-1
- Updating for lsvpd-1.6.1

* Sat Feb 2 2008 - Eric Munson <ebmunson@us.ibm.com> - 1.6.0-1
- Updating lsvpd to use the new libvpd-2.0.0
- Removing %%{_mandir}/man8/* from %%files and replacing it with each
  individual file installed in the man8 directory

* Fri Dec 7 2007 - Brad Peters <bpeters@us.ibm.com> - 1.5.0
- Major changes in device detection code, basing detection on /sys/devices
  rather than /sys/bus as before
- Enhanced aggressiveness of AIX naming, ensuring that every detected device
  has at least one AIX name, and thus appears in lscfg output
- Changed method for discovering /sys/class entries
- Added some new VPD fields, one example of which is the device driver
  associated with the device
- Some minor changes to output formating
- Some changes to vpd collection
- Removing unnecessary Requires field

* Fri Nov 16 2007 - Eric Munson <ebmunson@us.ibm.com> - 1.4.0-1
- Removing udev rules from install as they are causing problems.  Hotplug 
  will be disabled until we find a smarter way of handling it.
- Updating License
- Adjusting the way vpdupdater is inserted into run control
- Removing #! from the beginning of the file.
- Fixes requested by Fedora Community

* Wed Oct 30 2007 - Eric Munson <ebmunson@us.ibm.com> - 1.3.5-1
- Remove calls to ldconfig
