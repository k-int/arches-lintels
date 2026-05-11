equals(QT_MAJOR_VERSION, 6)
!versionAtLeast(QT_VERSION, 6.11.0):error("Use at least Qt version 6.11.0")

# add all .ui files (arches-qgis dialogs) from this dir
FORMS += $$files(*.ui)