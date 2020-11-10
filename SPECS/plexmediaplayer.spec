Name:           plexmediaplayer
Version:        2.58.0.1076
Release:        1%{?dist}
Summary:        Plex Media Player for Fedora 28+

License:        GPLv2
URL:            https://plex.tv/
# See: https://fedoraproject.org/wiki/Packaging:SourceURL?rd=Packaging/SourceURL#Git_Tags
Source0:        https://github.com/plexinc/plex-media-player/archive/v2.58.0.1076-38e019da.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{name}.desktop
Source2:        %{name}.appdata.xml
Source3:        %{name}.service
Source4:        %{name}.target
Source5:        %{name}.pkla.disabled
Source6:        %{name}-standalone
Source7:        %{name}.te
Source8:        %{name}.pp
Source9:       %{name}-standalone-enable

BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  mpv-libs
BuildRequires:  mpv-libs-devel
BuildRequires:  libdrm-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  SDL2-devel
BuildRequires:  libcec-devel >= 4.0.0
BuildRequires:  libappstream-glib
BuildRequires:  desktop-file-utils
BuildRequires:  qt5-qtbase-devel >= 5.9.5
BuildRequires:  qt5-qtdeclarative-devel >= 5.9.5
BuildRequires:  qt5-qtwebchannel-devel >= 5.9.5
BuildRequires:  qt5-qtwebengine-devel >= 5.9.5
BuildRequires:  qt5-qtx11extras-devel >= 5.9.5

Requires:       mpv-libs
Requires:       libdrm
Requires:       mesa-libGL
Requires:       SDL2
Requires:       libcec >= 4.0.0
Requires:       minizip
Requires:       opencv-core
Requires:       qt5-qtbase >= 5.9.5
Requires:       qt5-qtbase-gui >= 5.9.5
Requires:       qt5-qtdeclarative >= 5.9.5
Requires:       qt5-qtwebchannel >= 5.9.5
Requires:       qt5-qtwebengine >= 5.9.5
Requires:       qt5-qtx11extras >= 5.9.5
Requires:       qt5-qtquickcontrols >= 5.9.5
# User creation.
Requires(pre):  shadow-utils

%description
Plex Media Player - Client for Plex Media Server.

%prep
#%setup -n %{name}-%{version} -q
%setup -n plex-media-player-2.58.0.1076-38e019da -q

%build
rm -Rf build
mkdir build
cd build
cmake -GNinja -DCMAKE_BUILD_TYPE=RelWithDebInfo -DQTROOT=/usr/lib64/qt5 -DMPV_INCLUDE_DIR=/usr/include/mpv -DMPV_LIBRARY=/usr/lib64/libmpv.so.1 -DLINUX_DBUS=ON -DCMAKE_INSTALL_PREFIX=/usr ..
ninja-build

%install
rm -rf $RPM_BUILD_ROOT

cd build
DESTDIR=%{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch} ninja-build install
cd ../

%{__mkdir_p} %{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}%{_bindir}
%{__install} -m0755 %{_builddir}/%{buildsubdir}/build/src/plexmediaplayer %{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}%{_bindir}/plexmediaplayer
%{__install} -m0755 %{_builddir}/%{buildsubdir}/build/src/pmphelper       %{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}%{_bindir}/pmphelper
%{__install} -m0755 %{_sourcedir}/%{name}-standalone                      %{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}%{_bindir}/%{name}-standalone

appstream-util validate-relax --nonet %{_sourcedir}/%{name}.appdata.xml
%{__mkdir_p} %{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}%{_datadir}/appdata
%{__install} -m0644 %{_sourcedir}/%{name}.appdata.xml                     %{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}%{_datadir}/appdata/%{name}.appdata.xml

%{__mkdir_p} %{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}%{_datadir}/%{name}
%{__install} -m0755 %{_sourcedir}/%{name}-standalone-enable               %{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}%{_datadir}/%{name}/%{name}-standalone-enable

%{__mkdir_p} %{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}%{_datadir}/%{name}/selinux
%{__install} -m0644 %{_sourcedir}/%{name}.te                              %{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}%{_datadir}/%{name}/selinux/%{name}.te
%{__install} -m0644 %{_sourcedir}/%{name}.pp                              %{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}%{_datadir}/%{name}/selinux/%{name}.pp

%{__mkdir_p} %{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}%{_prefix}/lib/systemd/system
%{__install} -m0644 %{_sourcedir}/%{name}.service                         %{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}%{_prefix}/lib/systemd/system/%{name}.service
%{__install} -m0644 %{_sourcedir}/%{name}.target                          %{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}%{_prefix}/lib/systemd/system/%{name}.target

%{__mkdir_p} %{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}%{_sysconfdir}/polkit-1/localauthority/50-local.d
%{__install} -m0644 %{_sourcedir}/%{name}.pkla.disabled                   %{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}%{_sysconfdir}/polkit-1/localauthority/50-local.d/%{name}.pkla.disabled

desktop-file-validate %{_sourcedir}/%{name}.desktop
desktop-file-install --dir=%{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}%{_datadir}/applications %{_sourcedir}/%{name}.desktop


%files
/usr/bin/plexmediaplayer
/usr/bin/pmphelper
/usr/bin/plexmediaplayer-standalone
/usr/lib/systemd/system/plexmediaplayer.service
/usr/lib/systemd/system/plexmediaplayer.target
/usr/share/appdata/plexmediaplayer.appdata.xml
/usr/share/applications/plexmediaplayer.desktop
/usr/share/icons/hicolor/scalable/apps/plexmediaplayer.svg
/usr/share/plexmediaplayer/plexmediaplayer-standalone-enable
/usr/share/plexmediaplayer/selinux/plexmediaplayer.te
/usr/share/plexmediaplayer/selinux/plexmediaplayer.pp
/usr/share/plexmediaplayer/web-client/*
/etc/polkit-1/localauthority/50-local.d/plexmediaplayer.pkla.disabled


%pre
# Create "plexmediaplayer" if it not already exists.
#
# NEVER delete an user or group created by an RPM package. See:
# https://fedoraproject.org/wiki/Packaging:UsersAndGroups#Allocation_Strategies
/usr/bin/getent passwd plexmediaplayer >/dev/null || \
  /sbin/useradd -r -G dialout,video,lock,audio \
  -d %{_sharedstatedir}/plexmediaplayer --create-home -s /sbin/nologin \
  -c "Plex Media Player (Standalone)" plexmediaplayer
%{__chmod} 0750 %{_sharedstatedir}/plexmediaplayer
%{__chown} plexmediaplayer:plexmediaplayer %{_sharedstatedir}/plexmediaplayer


%post
%{__ln_s} -f %{_prefix}/lib/systemd/system/%{name}.service %{_sysconfdir}/systemd/system/
%{__ln_s} -f %{_prefix}/lib/systemd/system/%{name}.target  %{_sysconfdir}/systemd/system/

touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache -q %{_datadir}/icons/hicolor;
fi
update-mime-database %{_datadir}/mime &> /dev/null || :
update-desktop-database &> /dev/null || :


%postun
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache -q %{_datadir}/icons/hicolor;
fi
update-mime-database %{_datadir}/mime &> /dev/null || :
update-desktop-database &> /dev/null || :


%changelog
