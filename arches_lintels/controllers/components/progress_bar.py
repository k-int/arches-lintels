def progress_bar_ui(progress_bar):
        
    # Indeterminate progress bar
    progress_bar.setTextVisible(False)        # Hide percentage text
    progress_bar.setRange(0, 0)               # Indeterminate mode
    progress_bar.setFixedHeight(6)            # Thin bar
