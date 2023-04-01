# TODO: -Dqmi_username=???
#
# Conditional build:
%bcond_without	apidocs	# (gtk-doc based) API documentation

Summary:	GLib library for talking to WWAN modems and devices using QMI protocol
Summary(pl.UTF-8):	Biblioteka GLib do komunikacji z modemami i urządzeniami WWAN z użyciem protokołu QMI
Name:		libqmi
Version:	1.32.4
Release:	1
License:	LGPL v2+
Group:		Libraries
#Source0Download: https://gitlab.freedesktop.org/mobile-broadband/libqmi/-/tags
Source0:	https://gitlab.freedesktop.org/mobile-broadband/libqmi/-/archive/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	c062cba26c2fca75d0a49ba48557f198
URL:		https://www.freedesktop.org/wiki/Software/libqmi/
BuildRequires:	glib2-devel >= 1:2.56
%if %(locale -a | grep -q '^C\.utf8$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
BuildRequires:	gobject-introspection-devel >= 0.9.6
BuildRequires:	gtk-doc >= 1.0
BuildRequires:	help2man
BuildRequires:	libgudev-devel >= 232
BuildRequires:	libmbim-devel >= 1.18.0
BuildRequires:	libqrtr-glib-devel >= 1.0.0
BuildRequires:	linux-libc-headers >= 7:4.15
BuildRequires:	meson >= 0.53.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.752
Requires:	glib2 >= 1:2.56
Requires:	libgudev >= 232
Requires:	libmbim >= 1.18.0
Requires:	libqrtr-glib >= 1.0.0
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
Requires:	glib2-devel >= 1:2.56
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
Requires:	bash-completion >= 1:2.0
BuildArch:	noarch

%description -n bash-completion-libqmi
Bash completion for qmictl command.

%description -n bash-completion-libqmi -l pl.UTF-8
Bashowe dopełnianie składni polecenia qmictl.

%prep
%setup -q

%build
%meson build \
	%{?with_apidocs:-Dgtk_doc=true}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README.md TODO
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
