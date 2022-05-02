def get_screen_size(appsize: bool=False) -> tuple[int, int] | None:
    import sys
    """
    Returns Monitor size x and y in pixels for desktop platforms, or None for
    mobile platforms.
    """
    if sys.platform == 'linux2' and not appsize:
        import subprocess
        output = subprocess.Popen(
            'xrandr | grep "\\*" | cut -d" " -f4',
            shell=True,
            stdout=subprocess.PIPE).communicate()[0]
        screen_x = int(output.replace('\n', '').split('x')[0])
        screen_y = int(output.replace('\n', '').split('x')[1])
    elif sys.platform == 'win32' and not appsize:
        from win32api import GetSystemMetrics
        screen_x: int = GetSystemMetrics(0)
        screen_y: int = GetSystemMetrics(1)
    elif sys.platform == 'darwin' and not appsize:
        try:
            from AppKit import NSScreen
        except ImportError:
            # iOS
            return None
        frame_size = NSScreen.mainScreen().frame().size
        screen_x = frame_size.width
        screen_y = frame_size.height
    else:
        # For mobile devices, use full screen
        return None
    print(f'Monitor: {screen_x}x{screen_y}')
    return (screen_x, screen_y)