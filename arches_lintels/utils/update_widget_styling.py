def update_widget_styling(widget, key, value):
    """
    This util function is for dynamically changing a widget styling
    via qss.
    """
    widget.setProperty(key, value)
    widget.style().unpolish(widget)
    widget.style().polish(widget)
    widget.update()