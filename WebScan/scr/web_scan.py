from kivymd.app import MDApp
from kivy.uix.relativelayout import RelativeLayout
from kivy.core.window import Window
from scr.screen_size import get_screen_size
from scr.port_scanner import PortScanner
from scr.domain_lookup import DomainLookUp


class WebScan(RelativeLayout):
    
    def reset_progress_bar(self) -> None:
        self.ids.progress_bar.value = 0
        self.ids.progress_bar.max = 0
        self.ids.progress_bar.min = 0
        self.ids.progress_bar.opacity = 0

    def check_domain(self, domain: str) -> None:
        domain_check = DomainLookUp(domain).get_domain_info()
        if domain_check != None:
            self.ids.info_label.text = f'{domain_check}'
        else:
            self.ids.info_label.text = 'Domain is not registered.'
            
    def port_scan(self, ip: str, s_port: int | str, e_port: int | str) -> None:
        self.reset_progress_bar()
        # show progress bar
        self.ids.progress_bar.opacity = 1
        print(s_port, e_port)
        # set start and end port if not provided
        if s_port == '':
            s_port = 0
        if e_port == '':
            e_port = 1024
        e_port = e_port if e_port > s_port else s_port # type: ignore e_port and s_port
                                                       # are ints at this stage.
        # set progress bar values
        self.ids.progress_bar.max = int(e_port)
        self.ids.progress_bar.min = int(s_port)
        self.ids.progress_bar.value = int(s_port)
        self.ids.info_label.text = f' PORTS {s_port}-{e_port}\n OPEN PORTS:\n'
        
        scanner = PortScanner(ip)
        for port in range(int(s_port), int(e_port) + 1):
            self.ids.progress_bar.value += 1
            open_port = scanner.scan_port(port)
            if open_port:
                self.ids.info_label.text = f'{self.ids.info_label.text} {port} '

class Application(MDApp):
    title = 'Web Scanner'
    icon = './res/icon.png'
    
    def build(self) -> RelativeLayout:
        if get_screen_size != None:
            Window.size = (400, 500)
        return WebScan()
