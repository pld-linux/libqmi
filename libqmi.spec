# TODO: --enable-qmi-username=???
#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs

Summary:	GLib library for talking to WWAN modems and devices using QMI protocol
Summary(pl.UTF-8):	Biblioteka GLib do komunikacji z modemami i urządzeniami WWAN z użyciem protokołu QMI
Name:		libqmi
Version:	1.28.6
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	https://www.freedesktop.org/software/libqmi/%{name}-%{version}.tar.xz
# Source0-md5:	4361ff7eed22f9cd696b812947cd8813
URL:		https://www.freedesktop.org/wiki/Software/libqmi/
BuildRequires:	autoconf >= 2.68
BuildRequires:	autoconf-archive >= 2017.03.21
BuildRequires:	automake >= 1:1.11
BuildRequires:	glib2-devel >= 1:2.48
%if %(locale -a | grep -q '^C\.utf8$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
BuildRequires:	gobject-introspection-devel >= 0.9.6
BuildRequires:	gtk-doc >= 1.0
BuildRequires:	help2man
BuildRequires:	libmbim-devel >= 1.18.0
BuildRequires:	libqrtr-glib-devel >= 1.0.0
BuildRequires:	linux-libc-headers >= 7:4.15
BuildRequires:	libtool >= 2:2.2
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.752
BuildRequires:	udev-glib-devel >= 1:147
Requires:	glib2 >= 1:2.48
Requires:	libmbim >= 1.18.0
Requires:	libqrtr-glib >= 1.0.0
Requires:	udev-glib >= 1:147
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libqmi is a GLib library for talking to WWAN modems and devices which
speak the Qualcomm MSM Interface (QMI) protocol.

%description -l pl.UTF-8
libqmi to biblioteka GLib do komunikacji z modemami i urządzeniami
WWAN, obsługującymi protokół QMI (Qualcomm MSM Interface).

%package devel
Summary:	Header files for libqmi library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libqmi
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.48
Requires:	libmbim-devel >= 1.18.0
Requires:	libqrtr-glib-devel >= 1.0.0

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
BuildArch:	noarch

%description apidocs
API documentation for libqmi library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libqmi.

%package -n bash-completion-libqmi
Summary:	Bash completion for qmictl command
Summary(pl.UTF-8):	Bashowe dopełnianie składni polecenia qmictl
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion >= 2.0
BuildArch:	noarch

%description -n bash-completion-libqmi
Bash completion for qmictl command.

%description -n bash-completion-libqmi -l pl.UTF-8
Bashowe dopełnianie składni polecenia qmictl.

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
	--enable-qrtr \
	--disable-silent-rules \
	--with-html-dir=%{_gtkdocdir}

LC_ALL=C.UTF-8 \
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
%attr(755,root,root) %{_bindir}/qmi-firmware-update
%attr(755,root,root) %{_bindir}/qmi-network
%attr(755,root,root) %{_bindir}/qmicli
%attr(755,root,root) %{_libdir}/libqmi-glib.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libqmi-glib.so.5
%{_libdir}/girepository-1.0/Qmi-1.0.typelib
%attr(755,root,root) %{_libexecdir}/qmi-proxy
%{_mandir}/man1/qmi-firmware-update.1*
%{_mandir}/man1/qmi-network.1*
%{_mandir}/man1/qmicli.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libqmi-glib.so
%{_includedir}/libqmi-glib
%{_datadir}/gir-1.0/Qmi-1.0.gir
%{_pkgconfigdir}/qmi-glib.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libqmi-glib.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libqmi-glib
%endif

%files -n bash-completion-libqmi
%defattr(644,root,root,755)
%{bash_compdir}/qmicli
