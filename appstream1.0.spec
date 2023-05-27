%define git 20230527
%define oname AppStream

%bcond_with gcruft

%define major 5
%define girmajor 1.0
%define libname %mklibname %{name} %{major}
%define girname %mklibname %{name}-gir %{girmajor}
%define devname %mklibname %{name} -d

%define qt_major 3
%define libnameqt %mklibname AppStreamQt %{qt_major}
%define devnameqt %mklibname AppStreamQt -d

Summary:	Utilities to generate, maintain and access the AppStream Xapian database
Name:		appstream1.0
Version:	1.0.0
Release:	%{?git:0.%{git}.}1
# lib LGPLv2.1+, tools GPLv2+
License:	GPLv2+ and LGPLv2.1+
Group:		System/Configuration/Packaging
Url:		http://www.freedesktop.org/wiki/Distributions/AppStream/Software
#Source0:	http://www.freedesktop.org/software/appstream/releases/%{oname}-%{version}.tar.xz
Source0:	https://github.com/ximion/appstream/archive/refs/heads/main.tar.gz#/%{oname}-%{git}.tar.gz
BuildRequires:	meson
BuildRequires:	intltool
BuildRequires:	itstool
BuildRequires:	xmlto
BuildRequires:	gperf
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(xmlb) >= 0.3.6
BuildRequires:	pkgconfig(packagekit-glib2)
BuildRequires:	pkgconfig(Qt6Core)
BuildRequires:	pkgconfig(Qt6Gui)
BuildRequires:	pkgconfig(Qt6Test)
BuildRequires:	cmake(Qt6LinguistTools)
BuildRequires:	pkgconfig(yaml-0.1)
BuildRequires:	pkgconfig(libsoup-2.4)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	gtk-doc
%if %{with gcruft}
BuildRequires:  pkgconfig(vapigen)
BuildRequires:  vala-tools
%endif
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:	libstemmer-devel
BuildRequires:	lmdb-devel
Requires:	%{libname} = %{EVRD}
# Should be added later, requires generation script
# Requires:	appstream-data

%description
AppStream-Core makes it easy to access application information from the
AppStream database over a nice GObject-based interface.

%if 0
%files -f appstream.lang
%doc AUTHORS
%config(noreplace) %{_sysconfdir}/appstream.conf
%{_bindir}/appstreamcli
%{_mandir}/man1/appstreamcli.1.*
%dir %{_datadir}/app-info/
%dir %{_datadir}/app-info/icons
%dir %{_datadir}/app-info/xmls
%{_datadir}/metainfo/org.freedesktop.appstream.cli.metainfo.xml
%ghost %{_var}/cache/app-info/cache.watch
%dir %{_var}/cache/app-info
%dir %{_var}/cache/app-info/icons
%dir %{_var}/cache/app-info/gv
%dir %{_var}/cache/app-info/xapian
%dir %{_var}/cache/app-info/xmls
%{_datadir}/gettext/its/metainfo.*

%posttrans
%{_bindir}/appstreamcli refresh --force >& /dev/null ||:
 
%transfiletriggerin -- %{_datadir}/app-info/xmls
%{_bindir}/appstreamcli refresh --force >& /dev/null ||:
 
%transfiletriggerpostun -- %{_datadir}/app-info/xmls
%{_bindir}/appstreamcli refresh --force >& /dev/null ||:
%endif

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Shared library for %{name}
Group:		System/Libraries
Obsoletes:	%{mklibname appstream 2} < 0.9.0

%description -n %{libname}
Shared library for %{name}.

%files -n %{libname}
%{_libdir}/libappstream.so.%{major}*
%{_libdir}/libappstream.so.%{version}

#----------------------------------------------------------------------------

%if %{with gcruft}
%package -n %{girname}
Summary:	GObject Introspection files for %{name}
Group:		System/Libraries
Requires:	%{libname} = %{EVRD}
Obsoletes:	%{mklibname appstream-git 0.8} < 0.9.0

%description -n %{girname}
GObject Introspection files for %{name}.

%files -n %{girname}
%{_libdir}/girepository-1.0/AppStream-%{girmajor}.typelib
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/AppStream-%{girmajor}.gir

%package vala
Summary:	Vala bindings for %{name}
Group:		Development/Other
Requires:	%{name}%{?_isa} = %{EVRD}
Requires:	vala

%description vala
Vala files for %{name}.

%files vala
%{_datadir}/vala/vapi/appstream.deps
%{_datadir}/vala/vapi/appstream.vapi
%endif

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{EVRD}
%if %{with gcruft}
Requires:	%{girname} = %{EVRD}
%endif
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
Development files for %{name}.

%files -n %{devname}
%{_includedir}/appstream/
%{_libdir}/libappstream.so
%{_libdir}/pkgconfig/appstream.pc

#----------------------------------------------------------------------------

%package -n %{libnameqt}
Summary:	Shared library for %{name}
Group:		System/Libraries
Requires:	%{libname} = %{EVRD}

%description -n %{libnameqt}
Shared library for %{name}.

%files -n %{libnameqt}
%{_libdir}/libAppStreamQt.so.%{qt_major}*
%{_libdir}/libAppStreamQt.so.%{version}*

#----------------------------------------------------------------------------

%package -n %{devnameqt}
Summary:	Development files for %{name}
Group:		Development/KDE and Qt
Requires:	%{libnameqt} = %{EVRD}
Provides:	appstream-qt6-devel = %{EVRD}
Obsoletes:	%{mklibname appstreamqt -d} < 0.10.4

%description -n %{devnameqt}
Development files for %{name}.

%files -n %{devnameqt}
%{_includedir}/AppStreamQt/
%{_libdir}/cmake/AppStreamQt/
%{_libdir}/libAppStreamQt.so

#----------------------------------------------------------------------------

%prep
%autosetup -n appstream-main
#%{version}

%build
%meson \
    -Dqt=true \
%if %{with gcruft}
    -Dvapi=true
%endif

%meson_build

%install
%meson_install
mkdir -p %{buildroot}%{_datadir}/app-info/{icons,xmls}
mkdir -p %{buildroot}%{_var}/cache/app-info/{icons,gv,xapian,xmls}
touch %{buildroot}%{_var}/cache/app-info/cache.watch

%find_lang appstream

# Drop the G cruft for now, we only care about the snapshot because it has Qt6
rm -rf %{buildroot}%{_datadir}/vala
rm -rf %{buildroot}%{_libdir}/girepository-1.0
rm -rf %{buildroot}%{_sysconfdir}
rm -rf %{buildroot}%{_bindir}/appstreamcli
rm -rf %{buildroot}%{_mandir}/man1
rm -rf %{buildroot}%{_datadir}
rm -rf %{buildroot}%{_var}
