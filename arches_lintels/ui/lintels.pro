equals(QT_MAJOR_VERSION, 6)
!versionAtLeast(QT_VERSION, 6.11.0):error("Use at least Qt version 6.11.0")

FORMS += $$files(*.ui) \
    ui_create_arches_project.ui \
    ui_active_project_widget.ui