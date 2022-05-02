import whois

class DomainLookUp():
    def __init__(self, domain: str):
        self.domain = domain

    def is_registered(self) -> bool:
        try:
            whois.whois(self.domain) # type: ignore
            return True
        except:
            return False
        
    def get_domain_info(self) -> dict[str, str] | None:
        if self.is_registered:
            return whois.whois(self.domain) # type: ignore
        return None
