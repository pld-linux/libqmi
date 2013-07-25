#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
#
Summary:	GLib library for talking to WWAN modems and devices using QMI protocol
Name:		libqmi
Version:	1.4.0
Release:	1
License:	LGPL v2
Group:		Libraries
Source0:	http://www.freedesktop.org/software/libqmi/%{name}-%{version}.tar.xz
# Source0-md5:	f8e2c17240c21c7d48d5df4ab04c77e7
URL:		http://www.freedesktop.org/wiki/Software/libqmi/
BuildRequires:	autoconf >= 2.68
BuildRequires:	automake >= 1:1.11
BuildRequires:	glib2-devel >= 1:2.32.0
BuildRequires:	libtool >= 2:2.2
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libqmi is a GLib library for talking to WWAN modems and devices which
speak the Qualcomm MSM Interface (QMI) protocol.

%package devel
Summary:	Header files for libqmi library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libqmi
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.32.0

%description devel
Header files for libqmi library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libqmi.

%package static
Summary:	Static libqmi library
Summary(pl.UTF-8):	Statyczna biblioteka libqmi
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libqmi library.

%description static -l pl.UTF-8
Statyczna biblioteka libqmi.

%package apidocs
Summary:	libqmi API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki libqmi
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
API documentation for libqmi library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libqmi.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{__enable_disable apidocs gtk-doc} \
	--disable-silent-rules \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README TODO
%attr(755,root,root) %{_bindir}/qmi-network
%attr(755,root,root) %{_bindir}/qmicli
%attr(755,root,root) %{_libdir}/libqmi-glib.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libqmi-glib.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libqmi-glib.so
%{_includedir}/libqmi-glib
%{_pkgconfigdir}/qmi-glib.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libqmi-glib.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libqmi-glib
%endif
