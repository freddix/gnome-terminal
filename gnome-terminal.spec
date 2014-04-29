Summary:	GNOME Terminal
Name:		gnome-terminal
Version:	3.12.1
Release:	1
License:	GPL
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/gnome/sources/gnome-terminal/3.12/%{name}-%{version}.tar.xz
# Source0-md5:	ea25923b736d451504635668eb850895
URL:		http://www.gnome.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gnome-shell-devel
BuildRequires:	gsettings-desktop-schemas-devel >= 3.12.0
BuildRequires:	gtk+3-devel >= 3.12.0
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	nautilus-devel
BuildRequires:	pkg-config
BuildRequires:	startup-notification-devel
BuildRequires:	vte-devel >= 0.36.1
Requires(post,postun):	glib-gio-gsettings
Requires:	gsettings-desktop-schemas >= 3.12.0
Requires:	terminfo
Requires:	vte >= 0.36.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/gnome-terminal

%description
This is a terminal thing that isn't finished at all.

%package shell-search-provider
Summary:	GNOME Shell search provider
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires:	gnome-shell

%description shell-search-provider
Search result provider for GNOME Shell.

%package -n nautilus-extension-terminal
Summary:	GNOME Terminal extension for Nautilus
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires:	nautilus

%description -n nautilus-extension-terminal
GNOME Terminal extension for Nautilus.

%prep
%setup -q

# kill gnome common deps
%{__sed} -i -e 's/GNOME_COMPILE_WARNINGS.*//g'	\
    -i -e 's/GNOME_MAINTAINER_MODE_DEFINES//g'	\
    -i -e 's/GNOME_COMMON_INIT//g'		\
    -i -e 's/GNOME_CXX_WARNINGS.*//g'		\
    -i -e 's/GNOME_DEBUG_CHECK//g'		\
    -i -e 's/AC_MSG_ERROR(\[appdata-validate/AC_MSG_WARN(\[appdata-validate/' configure.ac

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--disable-migration		\
	--disable-schemas-compile	\
	--disable-silent-rules		\
	--disable-static
%{__make} \
        APPDATA_VALIDATE=%{_bindir}/true

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \

%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/{ca@valencia,en@shaw}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/nautilus/extensions-3.0/*.la

%find_lang %{name} --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_gsettings_cache

%postun
%update_gsettings_cache

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS
%attr(755,root,root) %{_bindir}/gnome-terminal
%dir %{_libexecdir}
%attr(755,root,root) %{_libexecdir}/gnome-terminal-server
%{_datadir}/dbus-1/services/org.gnome.Terminal.service
%{_datadir}/glib-2.0/schemas/org.gnome.Terminal.gschema.xml
%{_desktopdir}/gnome-terminal.desktop

%files shell-search-provider
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/nautilus/extensions-3.0/libterminal-nautilus.so

%files -n nautilus-extension-terminal
%defattr(644,root,root,755)
%{_datadir}/gnome-shell/search-providers/gnome-terminal-search-provider.ini

