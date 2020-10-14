%define _enable_debug_packages %{nil}
%define debug_package          %{nil}
%bcond_without bundled_qt5
%global bundled_qt_version 5.9.9

Summary: Video and Web Conferencing Service Client
Name: zoom
Version: 5.3.472687.1012
Release: 1
URL: https://www.zoom.us/
Source0: https://zoom.us/client/%{version}/zoom_x86_64.tar.xz#/zoom-%{version}.x86_64.tar.xz
Source1: Zoom.desktop
Source2: Zoom.png
Source3: zoom.xml
License: Zoom
ExclusiveArch: x86_64
BuildRequires: chrpath
BuildRequires: crudini
BuildRequires: desktop-file-utils
Requires: ca-certificates
Requires: hicolor-icon-theme
Requires: libmpg123.so.0()(64bit)
Requires: libquazip.so.1()(64bit)
Requires: libturbojpeg.so.0()(64bit)
Provides: bundled(libicu) = 56.1
%if %{with bundled_qt5}
Provides: bundled(qt5-qtbase) = %{bundled_qt_version}
Provides: bundled(qt5-qtbase-gui) = %{bundled_qt_version}
Provides: bundled(qt5-qtdeclarative) = %{bundled_qt_version}
Provides: bundled(qt5-qtgraphicaleffects) = %{bundled_qt_version}
Provides: bundled(qt5-qtimageformats) = %{bundled_qt_version}
Provides: bundled(qt5-qtquickcontrols) = %{bundled_qt_version}
Provides: bundled(qt5-qtquickcontrols2) = %{bundled_qt_version}
Provides: bundled(qt5-qtscript) = %{bundled_qt_version}
Provides: bundled(qt5-qtsvg) = %{bundled_qt_version}
Provides: bundled(qt5-qtx11extras) = %{bundled_qt_version}
Provides: bundled(qt5-qtxmlpatterns) = %{bundled_qt_version}

# Qt5 cannot be unbundled as the application uses private APIs
%global __requires_exclude ^lib\(icu\(data\|i18n\|uc\)\|Qt5\(3D\(Core\|Input\|Logic\|Quick\(Scene2D\)\?\|Render\)\|Concurrent\|Core\|DBus\|Egl\(FSDeviceIntegration\|FsKmsSupport\)\|Gamepad\|Gui\|Multimedia\(Quick_p\|Widgets\)\?\|Network\|OpenGL\|Positioning\|PrintSupport\|Qml\|Quick\(Widgets\|Controls2\|Particles\|Templates2\)\?\|Sensors\|Script\|Sql\|Svg\|WebChannel\|WebEngine\(Core\|Widgets\)\?\|WebKit\(Widgets\)\?\|Widgets\|X11Extras\|XcbQpa\|XmlPatterns\)\)\\.so\\.5.*$
%else
%global __requires_exclude ^lib\(icu\(data\|i18n\|uc\)\)
%endif
%global __provides_exclude_from ^%{_libdir}/zoom

%description
Zoom, the cloud meeting company, unifies cloud video conferencing, simple online
meetings, and group messaging into one easy-to-use platform. Our solution offers
the best video, audio, and screen-sharing experience across Zoom Rooms, Windows,
Mac, Linux, iOS, Android, and H.323/SIP room systems.

%prep
%setup -q -n zoom
chmod -x \
  *.pcm \
  *.pem \
  sip/*.wav \
  Qt*/{qmldir,*.qml} \
  timezones/*/timezones.txt \

chrpath -d zoom
chrpath -d zopen
rm -r \
%if ! %{with bundled_qt5}
  audio \
  egldeviceintegrations \
  generic \
  iconengines \
  imageformats \
  libQt5* \
  platforminputcontexts \
  platforms \
  platformthemes \
  Qt{,GraphicalEffects,Qml,Quick{,.2}} \
  qtdiag \
  xcbglintegrations \
%endif
  libmpg123.so \
  libquazip.so* \
  libturbojpeg.so* \
  getbssid.sh \
  zcacert.pem \

crudini --set qt.conf Paths Prefix %{_libdir}/zoom

%build

%install
install -dm755 %{buildroot}{%{_bindir},%{_libdir}/zoom}
cp -pr * %{buildroot}%{_libdir}/zoom/

desktop-file-install --dir %{buildroot}%{_datadir}/applications %{S:1}
install -Dpm644 %{S:2} %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/Zoom.png
install -Dpm644 %{S:3} %{buildroot}%{_datadir}/mime/packages/zoom.xml

ln -s ../%{_lib}/zoom/ZoomLauncher %{buildroot}%{_bindir}/zoom
ln -s ../libmpg123.so.0 %{buildroot}%{_libdir}/zoom/libmpg123.so
ln -s ../libquazip.so.1 %{buildroot}%{_libdir}/zoom/libquazip.so
ln -s ../libturbojpeg.so.0 %{buildroot}%{_libdir}/zoom/libturbojpeg.so
ln -s ../../bin/true %{buildroot}%{_libdir}/zoom/getbssid.sh
ln -s ../../../etc/pki/tls/certs/ca-bundle.crt %{buildroot}%{_libdir}/zoom/zcacert.pem

%files
%{_bindir}/zoom
%{_datadir}/applications/Zoom.desktop
%{_datadir}/icons/hicolor/256x256/apps/Zoom.png
%{_datadir}/mime/packages/zoom.xml
%{_libdir}/zoom

%changelog
* Wed Oct 14 2020 Dominik Mierzejewski <rpm@greysector.net> 5.3.472687.1012-1
- update to 5.3.472687.1012

* Tue Sep 29 2020 Dominik Mierzejewski <rpm@greysector.net> 5.3.469451.0927-1
- update to 5.3.469451.0927
- update bundled Qt5 version declaration

* Tue Sep 22 2020 Dominik Mierzejewski <rpm@greysector.net> 5.3.465578.0920-1
- update to 5.3.465578.0920
- FAAC is no longer required
- drop execstack call, no longer required

* Tue Sep 08 2020 Dominik Mierzejewski <rpm@greysector.net> 5.2.458699.0906-1
- update to 5.2.458699.0906

* Tue Sep 01 2020 Dominik Mierzejewski <rpm@greysector.net> 5.2.454870.0831-1
- update to 5.2.454870.0831
- correct Qt Prefix in qt.conf

* Mon Aug 17 2020 Dominik Mierzejewski <rpm@greysector.net> 5.2.446620.0816-1
- update to 5.2.446620.0816

* Wed Aug 05 2020 Dominik Mierzejewski <rpm@greysector.net> 5.2.440215.0803-1
- update to 5.2.440215.0803
- unbundle CA certificates

* Tue Jul 07 2020 Dominik Mierzejewski <rpm@greysector.net> 5.1.422789.0705-1
- update to 5.1.422789.0705
- add bundled libs to Provides:

* Tue Jun 30 2020 Dominik Mierzejewski <rpm@greysector.net> 5.1.418436.0628-1
- update to 5.1.418436.0628

* Thu Jun 18 2020 Dominik Mierzejewski <rpm@greysector.net> 5.1.412382.0614-1
- update to 5.1.412382.0614

* Tue Jun 09 2020 Dominik Mierzejewski <rpm@greysector.net> 5.0.418682.0603-1
- update to 5.0.418682.0603
- drop 32-bit support

* Thu May 28 2020 Dominik Mierzejewski <rpm@greysector.net> 5.0.413237.0524-1
- update to 5.0.413237.0524

* Fri May 15 2020 Dominik Mierzejewski <rpm@greysector.net> 5.0.403652.0509-1
- update to 5.0.403652.0509

* Fri May 08 2020 Dominik Mierzejewski <rpm@greysector.net> 5.0.399860.0429-1
- update to 5.0.399860.0429
- add missing build dependency on execstack

* Wed Apr 29 2020 Dominik Mierzejewski <rpm@greysector.net> 5.0.398100.0427-1
- update to 5.0.398100.0427
- drop executable stack bit from main binary

* Thu Apr 16 2020 Dominik Mierzejewski <rpm@greysector.net> 3.5.385850.0413-1
- update to 3.5.385850.0413

* Thu Apr 09 2020 Dominik Mierzejewski <rpm@greysector.net> 3.5.383291.0407-1
- update to 3.5.383291.0407

* Tue Mar 31 2020 Dominik Mierzejewski <rpm@greysector.net> 3.5.374815.0324-1
- update to 3.5.374815.0324

* Fri Mar 13 2020 Dominik Mierzejewski <rpm@greysector.net> 3.5.361976.0301-1
- update to 3.5.361976.0301
- support building the 32-bit version
- update requires filter
- replace getbssid.sh with /bin/true
- remove unnecessary executable bits from text files

* Wed Dec 18 2019 Dominik Mierzejewski <rpm@greysector.net> 3.5.336627.1216-1
- update to 3.5.336627.1216

* Mon Oct 21 2019 Dominik Mierzejewski <rpm@greysector.net> 3.0.306796.1020-1
- update to latest release

* Thu Oct 03 2019 Dominik Mierzejewski <rpm@greysector.net> 3.0.301026.0930-1
- initial build
- unbundle faac, mpg123, quazip and turbojpeg
- add desktop file, icon and MIME type drop-in
