import win32api
import psutil

class DriveInfo:
    units = [
        (1<<50, ' PB'),
        (1<<40, ' TB'),
        (1<<30, ' GB'),
        (1<<20, ' MB'),
        (1<<10, ' KB'),
        (1, (' byte', ' bytes')),
    ]
    
    def convert_bytes(self, bytes: int) -> str:
        for factor, suffix in self.units:
            if bytes >= factor:
                break
        amount = bytes / factor
        if isinstance(suffix, tuple):
            singular, plural = suffix
            if amount == 1:
                suffix = singular
            else:
                suffix = plural
        return f'{amount:.2f} {suffix}'
        
    def get_partitions(self) -> list[str]:
        drives = win32api.GetLogicalDriveStrings()
        drives = drives.split('\000')[:-1]
        partitions: list[str] = []
        for drive in drives:
            partitions.append(drive)
        return partitions
    
    def get_drive_size(self, drive: str) -> str:
        total, used, free, perc = psutil.disk_usage(drive)
        drive = drive.replace(':', '').replace('\\', '').replace('/', '')
        _drive = f'''
Drive: {drive}
    Total: {self.convert_bytes(total)}
    Used:  {self.convert_bytes(used)}
    Free:  {self.convert_bytes(free)}
    Percent: {perc} %'''
        return _drive
