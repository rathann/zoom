%define _enable_debug_packages %{nil}
%define debug_package          %{nil}
%global _build_id_links alldebug
%bcond_without bundled_qt5
%global bundled_qt_version 5.15.18

Summary: Video and Web Conferencing Service Client
Name: zoom
Version: 6.4.5.1259
Release: 1
URL: https://www.zoom.us/
Source0: https://zoom.us/client/%{version}/zoom_x86_64.tar.xz#/zoom-%{version}.x86_64.tar.xz
Source1: Zoom.desktop
Source2: Zoom.png
Source3: zoom.xml
Source4: Zoom-v4l2convert.desktop
Source5: zoom-v4l2convert.sh
License: Zoom
ExclusiveArch: x86_64
BuildRequires: chrpath
BuildRequires: crudini
BuildRequires: desktop-file-utils
Requires: %{_bindir}/pacmd
Requires: %{_bindir}/pactl
Requires: hicolor-icon-theme
Requires: libmpg123.so.0()(64bit)
Requires: libsqlite3.so.0()(64bit)
Requires: libvulkan.so.1()(64bit)
Requires: procps-ng
Provides: bundled(cef) = 130.1.15
Provides: bundled(libavcodec) = 5.1.3
Provides: bundled(libavformat) = 5.1.3
Provides: bundled(libavutil) = 5.1.3
Provides: bundled(libicu) = 56.1
Provides: bundled(libswresample) = 5.1.3
Provides: bundled(openvino)
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
Provides: bundled(qt5-qtwayland) = %{bundled_qt_version}
Provides: bundled(qt5-qtx11extras) = %{bundled_qt_version}
Provides: bundled(qt5-qtxmlpatterns) = %{bundled_qt_version}
Provides: bundled(quazip-qt5) = 0.9.1

# Qt5 cannot be unbundled as the application doesn't work with Fedora Qt5
%global __requires_exclude ^lib\(\(avcodec\|avformat\|avutil\|cef\|ffmpeg\|swresample\)\\.so\|\(icu\(data\|i18n\|uc\)\|Qt5\(3D\(Animation\|Core\|Input\|Logic\|Quick\(Scene2D\)\?\|Render\)\|Bodymovin\|Concurrent\|Core\|DBus\|Egl\(FSDeviceIntegration\|FsKmsSupport\)\|Gamepad\|Gui\|Location\|Multimedia\(Quick_p\|Widgets\)\?\|Network\|OpenGL\|Positioning\(Quick\)\?\|PrintSupport\|Qml\|QmlModels\|QmlWorkerScript\|Quick\(Controls2\|Particles\|Shapes\|Templates2\|Widgets\)\?\|RemoteObjects\|Sensors\|Script\|Sql\|Svg\|Wayland\(Client\|Compositor\)\|WebChannel\|WebEngine\(Core\|Widgets\)\?\|WebKit\(Widgets\)\?\|Widgets\|X11Extras\|XcbQpa\|Xml\|XmlPatterns\)\)\\.so\\.5\).*$
%else
%global __requires_exclude ^lib\(\(avcodec\|avformat\|avutil\|cef\|ffmpeg\|swresample\)\\.so\|icu\(data\|i18n\|uc\)\)
%endif
%global __provides_exclude_from ^%{_libdir}/zoom

%description
Zoom, the cloud meeting company, unifies cloud video conferencing, simple online
meetings, and group messaging into one easy-to-use platform. Our solution offers
the best video, audio, and screen-sharing experience across Zoom Rooms, Windows,
Mac, Linux, iOS, Android, and H.323/SIP room systems.

%package v4l2convert
Summary: v4l2convert wrapper for Zoom
Requires: %{name} = %{version}-%{release}
Requires: libv4l%{_isa}

%description v4l2convert
This package contains a v4l2convert wrapper for Zoom to fix video issues with
webcams missing support for colorspace formats required by Zoom

%prep
%setup -q -n zoom
find Qt/qml -type f -name qmldir -o -name *.qml | xargs chmod -x
chmod -x \
  {,ringtone/}ring.pcm \
  sip/*.wav \
  timezones/*/timezones.txt \

chmod +x \
  cef/libcef.so \
  libclDNN64.so \
  libmkldnn.so \
  libquazip.so \

for f in \
  aomhost \
  zo{om,pen} \
  libaomagent.so \
  libdvf.so \
  Qt/lib/libicu{data,i18n,uc}.so.56 \
  libquazip.so \
  ZoomLauncher \
  ZoomWebviewHost \
; do chrpath -d $f ; done
rm -r \
%if ! %{with bundled_qt5}
  Qt \
  libquazip.so \
  qt.conf \
%endif
  cef/libsqlite3.so.0 \
  cef/libvulkan.so.1 \
  libmpg123.so \
  libOpenCL.so.1 \
  getbssid.sh \

%if %{with bundled_qt5}
crudini --set qt.conf Paths Prefix %{_libdir}/zoom/Qt
%endif

%build

%install
install -dm755 %{buildroot}{%{_bindir},%{_libdir}/zoom}
cp -pr * %{buildroot}%{_libdir}/zoom/

desktop-file-install --dir %{buildroot}%{_datadir}/applications %{S:1}
desktop-file-install --dir %{buildroot}%{_datadir}/applications %{S:4}
install -Dpm755 %{S:5} %{buildroot}%{_bindir}/zoom-v4l2convert
install -Dpm644 %{S:2} %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/Zoom.png
install -Dpm644 %{S:3} %{buildroot}%{_datadir}/mime/packages/zoom.xml

ln -s ../%{_lib}/zoom/ZoomLauncher %{buildroot}%{_bindir}/zoom
ln -s ../libmpg123.so.0 %{buildroot}%{_libdir}/zoom/libmpg123.so
ln -s ../../bin/true %{buildroot}%{_libdir}/zoom/getbssid.sh
ln -s ../../libsqlite3.so.0 %{buildroot}%{_libdir}/zoom/cef/libsqlite3.so.0
ln -s ../../libvulkan.so.1 %{buildroot}%{_libdir}/zoom/cef/libvulkan.so.1

%files
%{_bindir}/zoom
%{_datadir}/applications/Zoom.desktop
%{_datadir}/icons/hicolor/256x256/apps/Zoom.png
%{_datadir}/mime/packages/zoom.xml
%dir %{_libdir}/zoom
%{_libdir}/zoom/aomhost
%{_libdir}/zoom/calendar
%dir %{_libdir}/zoom/cef
%attr(4755,root,root) %{_libdir}/zoom/cef/chrome-sandbox
%{_libdir}/zoom/cef/chrome_*_percent.pak
%{_libdir}/zoom/cef/icudtl.dat
%{_libdir}/zoom/cef/libcef.so
%{_libdir}/zoom/cef/libEGL.so
%{_libdir}/zoom/cef/libffmpeg.so
%{_libdir}/zoom/cef/libGLESv2.so
%{_libdir}/zoom/cef/libvk_swiftshader.so
%{_libdir}/zoom/cef/libsqlite3.so.0
%{_libdir}/zoom/cef/libvulkan.so.1
%{_libdir}/zoom/cef/locales
%{_libdir}/zoom/cef/resources.pak
%{_libdir}/zoom/cef/snapshot_blob.bin
%{_libdir}/zoom/cef/v8_context_snapshot.bin
%{_libdir}/zoom/cef/vk_swiftshader_icd.json
%{_libdir}/zoom/chatapp
%{_libdir}/zoom/diagnostic/diagnostic.zip
%{_libdir}/zoom/email
%{_libdir}/zoom/Embedded.properties
%{_libdir}/zoom/getbssid.sh
%{_libdir}/zoom/js/html_sanitizer_mail.js
%{_libdir}/zoom/json
%{_libdir}/zoom/libaomagent.so
%{_libdir}/zoom/libavcodec.so.59
%{_libdir}/zoom/libavformat.so.59
%{_libdir}/zoom/libavutil.so.57
%{_libdir}/zoom/libswresample.so.4
%{_libdir}/zoom/libclDNN64.so
%{_libdir}/zoom/libcml.so
%{_libdir}/zoom/libdvf.so
%{_libdir}/zoom/libmkldnn.so
%{_libdir}/zoom/libmpg123.so
%{_libdir}/zoom/ringtone
%{_libdir}/zoom/sip
%{_libdir}/zoom/timezones
%{_libdir}/zoom/translations
%{_libdir}/zoom/version.txt
%{_libdir}/zoom/zoom
%{_libdir}/zoom/ZoomLauncher
%{_libdir}/zoom/ZoomWebviewHost
%{_libdir}/zoom/zopen
%{_libdir}/zoom/*.pcm
%if %{with bundled_qt5}
%{_libdir}/zoom/Qt
%{_libdir}/zoom/libquazip.so
%{_libdir}/zoom/qt.conf
%endif

%files v4l2convert
%{_bindir}/zoom-v4l2convert
%{_datadir}/applications/Zoom-v4l2convert.desktop

%changelog
* Thu Apr 17 2025 Dominik Mierzejewski <dominik@greysector.net> - 6.4.5.1259-1
- update to 6.4.5 (1259)
- move the v4l2convert wrapper to a separate subpackage

* Fri Mar 28 2025 Dominik Mierzejewski <dominik@greysector.net> - 6.4.0.471-1
- update to 6.4.0 (471)

* Fri Nov 29 2024 Dominik Mierzejewski <dominik@greysector.net> - 6.2.11.5069-1
- update to 6.2.11.5069

* Mon Jul 08 2024 Dominik Mierzejewski <dominik@greysector.net> - 6.1.1.443-1
- update to 6.1.1.443

* Tue Apr 30 2024 Dominik Mierzejewski <dominik@greysector.net> - 6.0.2.4680-1
- update to 6.0.2.4680

* Mon Jan 29 2024 Dominik Mierzejewski <dominik@greysector.net> - 5.17.5.2543-1
- update to 5.17.5.2543
- update bundled components versions
- fdk-aac and turbojpeg are no longer as separate libraries
- keep bundled libswresample from FFmpeg 5.1.3

* Thu Oct 12 2023 Dominik Mierzejewski <dominik@greysector.net> - 5.16.2.8828-1
- update to 5.16.2.8828
- keep bundled libavcodec libavformat and libavutil from FFmpeg 5.1.3
- update Requires: filter to include bundled libQt5Xml

* Thu May 04 2023 Dominik Mierzejewski <dominik@greysector.net> - 5.14.5.2430-1
- update to 5.14.5.2430
- update bundled components versions

* Fri Mar 24 2023 Dominik Mierzejewski <rpm@greysector.net> - 5.14.0.1720-1
- update to 5.14.0.1720

* Wed Feb 15 2023 Dominik Mierzejewski <rpm@greysector.net> - 5.13.7.683-1
- update to 5.13.7.683
- unbundle sqlite3 and ffmpeg-libs

* Mon Jan 02 2023 Dominik Mierzejewski <dominik@greysector.net> - 5.13.3.651-1
- update to 5.13.3.651

* Mon Nov 28 2022 Dominik Mierzejewski <dominik@greysector.net> - 5.12.9.367-1
- update to 5.12.9.367

* Thu Nov 17 2022 Dominik Mierzejewski <rpm@greysector.net> - 5.12.6.173-1
- update to 5.12.6.173
- unbundle libvulkan

* Fri Oct 14 2022 Dominik Mierzejewski <dominik@greysector.net> - 5.12.2.4816-1
- update to 5.12.2.4816

* Wed Sep 28 2022 Dominik Mierzejewski <rpm@greysector.net> - 5.12.0.4682-1
- update to 5.12.0.4682

* Thu Sep 08 2022 Dominik Mierzejewski <dominik@greysector.net> - 5.11.10.4400-1
- update to 5.11.10.4400
- add missing dependencies

* Thu Aug 25 2022 Dominik Mierzejewski <dominik@greysector.net> - 5.11.9.4300-1
- update to 5.11.9.4300
- fix building without bundled Qt5
- mark chrome-sandbox as setuid

* Tue Jul 05 2022 Dominik Mierzejewski <dominik@greysector.net> - 5.11.1.3595-1
- update to 5.11.1.3595

* Thu Jun 09 2022 Dominik Mierzejewski <dominik@greysector.net> - 5.10.7.3311-1
- update to 5.10.7.3311

* Thu May 26 2022 Dominik Mierzejewski <dominik@greysector.net> - 5.10.6.3192-1
- update to 5.10.6.3192

* Wed May 04 2022 Dominik Mierzejewski <dominik@greysector.net> - 5.10.4.2845-1
- update to 5.10.4.2845

* Thu Apr 21 2022 Dominik Mierzejewski <dominik@greysector.net> - 5.10.3.2778-1
- update to 5.10.3.2778

* Fri Apr 01 2022 Dominik Mierzejewski <dominik@greysector.net> - 5.10.0.2450-2
- filter-out bundled libcef.so Requires:

* Thu Mar 31 2022 Dominik Mierzejewski <rpm@greysector.net> - 5.10.0.2450-1
- update to 5.10.0.2450

* Thu Mar 10 2022 Dominik Mierzejewski <rpm@greysector.net> - 5.9.6.2225-1
- update to 5.9.6.2225

* Wed Jan 26 2022 Dominik Mierzejewski <rpm@greysector.net> - 5.9.3.1911-1
- update to 5.9.3.1911

* Sat Jan 15 2022 Dominik Mierzejewski <rpm@greysector.net> - 5.9.1.1380-1
- update to 5.9.1.1380

* Wed Dec 22 2021 Dominik Mierzejewski <rpm@greysector.net> - 5.9.0.1273-1
- update to 5.9.0.1273

* Tue Dec 14 2021 Dominik Mierzejewski <rpm@greysector.net> - 5.8.6.739-1
- update to 5.8.6.739

* Tue Nov 16 2021 Dominik Mierzejewski <rpm@greysector.net> - 5.8.4.210-1
- update to 5.8.4.210

* Mon Nov 01 2021 Dominik Mierzejewski <rpm@greysector.net> - 5.8.3.145-1
- update to 5.8.3.145

* Sat Oct 02 2021 Dominik Mierzejewski <rpm@greysector.net> - 5.8.0.16-1
- update to 5.8.0.16

* Tue Sep 07 2021 Dominik Mierzejewski <rpm@greysector.net> - 5.7.31792.0820-1
- update to 5.7.31792.0820
- unbundle OpenCL

* Tue Aug 17 2021 Dominik Mierzejewski <rpm@greysector.net> - 5.7.29123.0808-1
- update to 5.7.29123.0808

* Thu Jul 22 2021 Dominik Mierzejewski <rpm@greysector.net> - 5.7.28852.0718-1
- update to 5.7.28852.0718

* Thu Jul 01 2021 Dominik Mierzejewski <rpm@greysector.net> - 5.7.26030.0627-1
- update to 5.7.26030.0627

* Sat Jun 19 2021 Dominik Mierzejewski <rpm@greysector.net> - 5.6.22045.0607-1
- update to 5.6.22045.0607

* Tue Jun 08 2021 Dominik Mierzejewski <rpm@greysector.net> 5.6.20278.0524-1
- update to 5.6.20278.0524

* Thu Apr 29 2021 Dominik Mierzejewski <rpm@greysector.net> 5.6.16888.0424-1
- update to 5.6.16888.0424

* Sat Apr 24 2021 Dominik Mierzejewski <rpm@greysector.net> 5.6.16775.0418-1
- update to 5.6.16775.0418

* Wed Mar 24 2021 Dominik Mierzejewski <rpm@greysector.net> 5.6.13558.0321-1
- update to 5.6.13558.0321

* Tue Mar 02 2021 Dominik Mierzejewski <rpm@greysector.net> 5.5.7938.0228-1
- update to 5.5.7938.0228

* Thu Feb 11 2021 Dominik Mierzejewski <rpm@greysector.net> 5.5.7011.0206-1
- update to 5.5.7011.0206
- sync desktop file with upstream

* Thu Feb 04 2021 Dominik Mierzejewski <rpm@greysector.net> 5.5.6981.0202-1
- update to 5.5.6981.0202

* Tue Feb 02 2021 Dominik Mierzejewski <rpm@greysector.net> 5.5.6955.0131-1
- update to 5.5.6955.0131

* Mon Jan 11 2021 Dominik Mierzejewski <rpm@greysector.net> 5.4.57862.0110-1
- update to 5.4.57862.0110

* Sun Dec 27 2020 Dominik Mierzejewski <rpm@greysector.net> 5.4.57450.1220-1
- update to 5.4.57450.1220
- unbundle fdk-aac

* Wed Dec 09 2020 Dominik Mierzejewski <rpm@greysector.net> 5.4.56259.1207-1
- update to 5.4.56259.1207

* Wed Nov 18 2020 Dominik Mierzejewski <rpm@greysector.net> 5.4.54779.1115-1
- update to 5.4.54779.1115
- switch to bundled quazip to avoid two Qt5 clash with system version
- certificates seem to be built into the binary now

* Thu Nov 12 2020 Dominik Mierzejewski <rpm@greysector.net> 5.4.53391.1108-1
- update to 5.4.53391.1108

* Fri Nov 06 2020 Dominik Mierzejewski <rpm@greysector.net> 5.4.53350.1027-4
- use quazip-qt5 instead of quazip (qt4)

* Thu Nov 05 2020 Dominik Mierzejewski <rpm@greysector.net> 5.4.53350.1027-3
- work around build-id links conflicts with zoomvmwareplugin

* Sun Nov 01 2020 Dominik Mierzejewski <rpm@greysector.net> 5.4.53350.1027-2
- add zoom launcher wrapped with v4l2convert.so library to fix some webcams

* Wed Oct 28 2020 Dominik Mierzejewski <rpm@greysector.net> 5.4.53350.1027-1
- update to 5.4.53350.1027
- update bundled Qt5 version declaration
- unbundle wayland

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
