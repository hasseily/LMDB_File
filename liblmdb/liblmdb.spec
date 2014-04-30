%define	LMDBVER	0.9.8

Name:		liblmdb
Version:	%{LMDBVER}
Release:	0.%{_disttag}
Summary:	An ultra-fast, ultra-compact key-value data store
Group:		System Environment/Libraries
License:	OpenLDAP
URL:		http://symas.com/mdb/
Source0:	liblmdb-%{LMDBVER}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
The OpenLDAP's Lightning Memory-Mapped Database (LMDB)
LMDB is an ultra-fast, ultra-compact key-value data store developed by Symas for
the OpenLDAP Project. It uses memory-mapped files, so it has the read performance
of a pure in-memory database while still offering the persistence of standard
disk-based databases, and is only limited to the size of the virtual address space,
(it is not limited to the size of physical RAM). 

%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Provides:	liblmdb.so()(64bit)

%description devel
The %{name}-devel package contains header files for developing
applications that use %{name}.

%prep
%setup -q -n liblmdb

# set prefix
sed -i 's|/usr/local|%{_prefix}|' Makefile

# fix hardcoded lib
sed -i 's|/lib|/%{_lib}|' Makefile

# fix manpage location
sed -i 's|man|share/man|' Makefile

%build
make %{?_smp_mflags}
make %{?_smp_mflags} test

%install
rm -rf %{buildroot}

# create required directories
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_libdir}
mkdir -p %{buildroot}/%{_includedir}
mkdir -p %{buildroot}/%{_mandir}/man1

make install DESTDIR=%{buildroot}
mv %{buildroot}/%{_libdir}/liblmdb.so %{buildroot}/%{_libdir}/liblmdb.so.%{LMDBVER}
cd %{buildroot}/%{_libdir}
ln -s liblmdb.so.%{LMDBVER} liblmdb.so

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc LICENSE COPYRIGHT
%attr(0755,root,root) %{_bindir}/mdb_copy
%attr(0755,root,root) %{_bindir}/mdb_stat
%attr(0644,root,root) %{_mandir}/man1/mdb_copy.1*
%attr(0644,root,root) %{_mandir}/man1/mdb_stat.1*
%attr(0755,root,root) %{_libdir}/liblmdb.so.%{LMDBVER}

%files devel
%defattr(-,root,root,-)
%attr(0644,root,root) %{_includedir}/lmdb.h
%attr(0755,root,root) %{_libdir}/liblmdb.a
%{_libdir}/liblmdb.so

%changelog
* Thu Aug 29 2013 Salvador Ortiz <sog@msg.com.mx> - 0.9.8-0
- Updated to git "3d59ca3"

* Sat Aug 10 2013 Salvador Ortiz <sog@msg.com.mx> - 0.9.7-2
- Remove local patches, now in upstream
- use git version "9c49ef1"

* Wed Aug 07 2013 Salvador Ortiz <sog@msg.com.mx> - 0.9.7-1
- Add txn_env patch

* Fri Aug 02 2013 Salvador Ortiz <sog@msg.com.mx> - 0.9.7-0
- Updated to last version on time

* Sun Jul 07 2013 Salvador Ortiz <sog@msg.com.mx> - 0.9.6-0
- Use standalone library from symax.com
- Use published gitorious version "06a3ad0"

* Mon Feb 25 2013 Patrick <patrickl@fedoraproject.org> - 0-0.1
- initial spec file for liblmdb
