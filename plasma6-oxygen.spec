%bcond_without qt5

%define major 5
%define libname %mklibname oxygenstyle%{major} %{major}
%define clibname %mklibname oxygenstyleconfig%{major} %{major}
%define plasmaver %(echo %{version} |cut -d. -f1-3)
%define stable %([ "`echo %{version} |cut -d. -f3`" -ge 80 ] && echo -n un; echo -n stable)

%define git 20230901

Summary: The Oxygen style for KDE 5
Name: plasma6-oxygen
Version:	5.240.0
Release:	%{?git:0.%{git}.}1
URL: http://kde.org/
License: GPL
Group: Graphical desktop/KDE
%if 0%{?git:1}
Source0:	https://invent.kde.org/plasma/oxygen/-/archive/master/oxygen-master.tar.bz2#/oxygen-%{git}.tar.bz2
%else
Source0: http://download.kde.org/%{stable}/plasma/%{plasmaver}/%{name}-%{version}.tar.xz
%endif
Patch0: oxygen-5.5.3-use-openmandriva-icon-and-background.patch
BuildRequires: cmake(Qt6)
BuildRequires: cmake(Qt6Core)
BuildRequires: cmake(Qt6Gui)
BuildRequires: cmake(Qt6DBus)
BuildRequires: cmake(Qt6Widgets)
BuildRequires: pkgconfig(xcb)
BuildRequires: cmake(KF6DocTools)
BuildRequires: cmake(ECM)
BuildRequires: cmake(KF6WindowSystem)
BuildRequires: cmake(KF6Completion)
BuildRequires: cmake(KF6Service)
BuildRequires: cmake(KDecoration2) >= 5.27.80
BuildRequires: cmake(Gettext)
BuildRequires: cmake(KF6FrameworkIntegration)
BuildRequires: cmake(KF6KCMUtils)
BuildRequires: cmake(KF6Wayland)
%if %{with qt5}
BuildRequires: cmake(Qt5)
BuildRequires: cmake(Qt5Core)
BuildRequires: cmake(Qt5Gui)
BuildRequires: cmake(Qt5DBus)
BuildRequires: cmake(Qt5Widgets)
BuildRequires: cmake(KF5I18n)
BuildRequires: cmake(KF5Config)
BuildRequires: cmake(KF5CoreAddons)
BuildRequires: cmake(KF5GuiAddons)
BUildRequires: cmake(KF5WidgetsAddons)
%endif
# Really BuildConflicts: xdg-desktop-portal-kde, but dnf builddep doesn't handle conflicts
BuildRequires: plasma6-xdg-desktop-portal-kde
Requires: %{libname} = %{EVRD}
Requires: kf6-oxygen-icons
Recommends: plasma6-oxygen-sounds
# needed for backgrounds and patch 2
Requires: distro-theme-OpenMandriva
%if %{with qt5}
BuildRequires:	cmake(Qt5Core)
BuildRequires:	cmake(Qt5Gui)
BuildRequires:	cmake(Qt5Widgets)
%endif

%description
The Oxygen style for KDE 5.

%package -n %{libname}
Summary: KDE Frameworks 5 Oxygen framework
Group: System/Libraries
Requires: %{name} = %{EVRD}

%description -n %{libname}
KDE Frameworks 5 Oxygen framework.

%package -n %{clibname}
Summary: KDE Frameworks 5 Oxygen configuration framework
Group: System/Libraries
Requires: %{name} = %{EVRD}

%description -n %{clibname}
KDE Frameworks 5 Oxygen configuration framework.

%prep
%autosetup -p1 -n oxygen-%{?git:master}%{!?git:%{version}}
%cmake \
	-DBUILD_QCH:BOOL=ON \
	-DBUILD_WITH_QT6:BOOL=ON \
	-DKDE_INSTALL_USE_QT_SYS_PATHS:BOOL=ON \
	-G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build

# omv backgrounds
rm -rf %{buildroot}%{_datadir}/plasma/look-and-feel/org.kde.oxygen/contents/splash/images/background.png
ln -sf %{_datadir}/mdk/backgrounds/default.png %{buildroot}%{_datadir}/plasma/look-and-feel/org.kde.oxygen/contents/splash/images/background.png

# Useless, we don't have headers
rm -f %{buildroot}%{_libdir}/liboxygenstyle%{major}.so
rm -f %{buildroot}%{_libdir}/liboxygenstyleconfig%{major}.so

# automatic gtk icon cache update on rpm installs/removals
# (see http://wiki.mandriva.com/en/Rpm_filetriggers)
install -d %{buildroot}%{_var}/lib/rpm/filetriggers
cat > %{buildroot}%{_var}/lib/rpm/filetriggers/gtk-icon-cache-plasma-oxygen.filter << EOF
^./usr/share/icons/KDE_Classic
^./usr/share/icons/Oxygen_Black
^./usr/share/icons/Oxygen_Blue
^./usr/share/icons/Oxygen_White
^./usr/share/icons/Oxygen_Yellow
^./usr/share/icons/Oxygen_Zion
EOF

cat > %{buildroot}%{_var}/lib/rpm/filetriggers/gtk-icon-cache-plasma-oxygen.script << EOF
#!/bin/sh
if [ -x /usr/bin/gtk-update-icon-cache ]; then
    for i in KDE_Classic Oxygen_Black Oxygen_Blue Oxygen_White Oxygen_Yellow Oxygen_Zion; do
	/usr/bin/gtk-update-icon-cache --force --quiet /usr/share/icons/$i
    done
fi
EOF

chmod 755 %{buildroot}%{_var}/lib/rpm/filetriggers/gtk-icon-cache-plasma-oxygen.script

%find_lang liboxygenstyleconfig || touch liboxygenstyleconfig.lang
%find_lang oxygen_style_config || touch oxygen_style_config.lang
%find_lang oxygen_style_demo || touch oxygen_style_demo.lang
%find_lang oxygen_kdecoration || touch oxygen_kdecoration.lang

cat *.lang >oxygen-all.lang

%files -f oxygen-all.lang
%{_bindir}/oxygen-demo5
%{_bindir}/oxygen-demo6
%{_libdir}/liboxygenstyle6.so.5*
%{_libdir}/liboxygenstyleconfig6.so.5*
%{_bindir}/oxygen-settings6
%{_datadir}/color-schemes/Oxygen.colors
%{_datadir}/color-schemes/OxygenCold.colors
%{_iconsdir}/KDE_Classic
%{_iconsdir}/Oxygen_Black
%{_iconsdir}/Oxygen_Blue
%{_iconsdir}/Oxygen_White
%{_iconsdir}/Oxygen_Yellow
%{_iconsdir}/Oxygen_Zion
%{_iconsdir}/hicolor/*/apps/oxygen-settings.png
%{_datadir}/kstyle/themes/oxygen.*
%{_datadir}/plasma/look-and-feel/org.kde.oxygen
%{_libdir}/qt5/plugins/styles/oxygen5.so
%{_qtdir}/plugins/styles/oxygen6.so
%{_qtdir}/plugins/org.kde.kdecoration2/org.kde.oxygen.so
%{_var}/lib/rpm/filetriggers/gtk-icon-cache-plasma-oxygen.*
%{_qtdir}/plugins/kstyle_config/kstyle_oxygen_config.so
%{_qtdir}/plugins/org.kde.kdecoration2.kcm/kcm_oxygendecoration.so
%{_datadir}/applications/kcm_oxygendecoration.desktop

%files -n %{libname}
%{_libdir}/liboxygenstyle%{major}.so.%{major}*

%files -n %{clibname}
%{_libdir}/liboxygenstyleconfig%{major}.so.%{major}*
