from typing import Any
from kivymd.app import MDApp
from kivy.uix.relativelayout import RelativeLayout
from kivy.core.window import Window
from scr.screen_size import get_screen_size
from scr.port_scanner import PortScanner
from scr.domain_lookup import DomainLookUp
from kivy.clock import Clock

class WebScan(RelativeLayout):
    start_port = 0
    end_port = 0
    current_port = 1
    ip = ''

    def check_domain(self, domain: str) -> None:
        domain_check = DomainLookUp(domain).get_domain_info()
        if domain_check != None:
            self.ids.info_label.text = f'{domain_check}'
        else:
            self.ids.info_label.text = 'Domain is not registered.'
            
    def port_scan(self, ip: str, s_port: int | str, e_port: int | str) -> None:
        self.ids.info_label.text = ''
        # show progress bar
        self.ids.progress_bar.opacity = 1
        
        if s_port == '':
            s_port = 0
        if e_port == '':
            e_port = 1024
        e_port = int(e_port) if int(e_port) > int(s_port) else int(s_port)
        
        self.start_port = int(s_port)
        self.end_port = int(e_port)
        self.current_port = self.start_port
        self.ip = ip
        
        self.ids.progress_bar.max = self.end_port - self.start_port
        
        self.ids.info_label.text = f'Scanning Ports: {self.start_port} - {self.end_port}\nOpen Ports:\n'
        Clock.schedule_interval(self.callback, 0.1)

    def callback(self, *args: Any) -> None:
        scanner = PortScanner(self.ip)
        if self.current_port <= self.end_port:
            open_port = scanner.scan_port(self.current_port)
            if open_port:
                self.ids.info_label.text = f'{self.ids.info_label.text} {self.current_port} '
            self.current_port += 1
            self.ids.progress_bar.value += 1
        else:
            Clock.unschedule(self.callback)
            self.ids.progress_bar.opacity = 0
            self.ids.progress_bar.value = 0


class Application(MDApp):
    title = 'Web Scanner'
    icon = './res/icon.png'
    
    def build(self) -> RelativeLayout:
        if get_screen_size != None:
            Window.size = (400, 500)
        return WebScan()
