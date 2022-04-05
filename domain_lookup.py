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
            
def main() -> None:
    domain = input('Enter domain to scan: ')
    domain_lookup = DomainLookUp(domain)
    if domain_lookup.is_registered():
        for key, value in domain_lookup.get_domain_info().items(): # type: ignore
            print(f'{key}: {value}')
    else:
        print('Domain is not registered.')

if __name__ == '__main__':
    main()
