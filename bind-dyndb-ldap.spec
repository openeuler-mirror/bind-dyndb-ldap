%define bind_version 32:9.11.3-5

Name:           bind-dyndb-ldap
Version:        11.3
Release:        1
Summary:        LDAP back-end plug-in for BIND
License:        GPLv2+
URL:            https://releases.pagure.org/bind-dyndb-ldap
Source0:        https://releases.pagure.org/%{name}/%{name}-%{version}.tar.bz2
Source1:        https://releases.pagure.org/%{name}/%{name}-%{version}.tar.bz2.asc
BuildRequires:  bind-devel >= %{bind_version}, bind-pkcs11-devel >= %{bind_version}
BuildRequires:  krb5-devel
BuildRequires:  openldap-devel
BuildRequires:  libuuid-devel
BuildRequires:  automake, autoconf, libtool
BuildRequires:  openssl-devel
Requires:       bind-pkcs11 >= %{bind_version}, bind-pkcs11-utils >= %{bind_version}

%description
This package provides an LDAP back-end, the dynamic LDAP back-end is
a plug-in for BIND that provides an LDAP database back-end capabilities.

%prep
%autosetup -n %{name}-%{version} -p1

%build
autoreconf -fiv
%configure
%make_build

%install
rm -rf %{buildroot}
%make_install
install -d -m 770 %{buildroot}/%{_localstatedir}/named/dyndb-ldap

%post
# Transform named.conf if it still has old-style API.
PLATFORM=$(uname -m)

if [ $PLATFORM == "x86_64" ] ; then
    LIBPATH=/usr/lib64
else
    LIBPATH=/usr/lib
fi

while read -r PATTERN
do
    SEDSCRIPT+="$PATTERN"
done <<EOF
/^\s*dynamic-db/,/};/ {
  s/\(\s*\)arg\s\+\(["']\)\([a-zA-Z_]\+\s\)/\1\3\2/g;
  s/^dynamic-db/dyndb/;
  s@\(dyndb "[^"]\+"\)@\1 "$LIBPATH/bind/ldap.so"@;
  s@\(dyndb '[^']\+'\)@\1 '$LIBPATH/bind/ldap.so'@;
  /\s*library[^;]\+;/d;
  /\s*cache_ttl[^;]\+;/d;
  /\s*psearch[^;]\+;/d;
  /\s*serial_autoincrement[^;]\+;/d;
  /\s*zone_refresh[^;]\+;/d;
}
EOF

sed -i.bak -e "$SEDSCRIPT" /etc/named.conf

%files
%exclude %{_libdir}/bind/ldap.la
%doc NEWS README.md COPYING doc/{example,schema}.ldif
%dir %attr(770, root, named) %{_localstatedir}/named/dyndb-ldap
%{_libdir}/bind/ldap.so


%changelog
* Mon Jul 27 2020 gaihuiying <gaihuiying1@huawei.com> - 11.3-1
- Type:requirement
- ID:NA
- SUG:NA
- DESC:update to 11.3

* Mon Jun 22 2020 gaihuiying <gaihuiying1@huawei.com> - 11.1-14
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix build error with gcc9 

* Wed Sep 11 2019 AlexChao <zhaolei746@huawei.com> - 11.1-13
- Package init
