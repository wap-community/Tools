def find_subdomains_shodan(domain, shodan_api):
    SD = [] 
    api = shodan.Shodan(shodan_api)

    if shodan_api == "":
        print("  \__", colored("No Shodan API key configured", "red"))
        return []

    else:
        try:
            results = api.search("hostname:.{0}".format(domain))
            print(results)
            try:
                for res in results["matches"]:
                    SD.append("".join(res["hostnames"]))

            except KeyError as errk:
                print("  \__", colored(errk, "red"))
                return []

            SD = set(SD)

            print("  \__ {0}: {1}".format(colored("Unique subdomains found", "cyan"), colored(len(SD), "yellow")))
            return SD

        except shodan.exception.APIError as err:
            print("  \__", colored(err, "red"))
            return []

        except Exception:
            print("  \__", colored("Something went wrong!", "red"))
            return []



def cert_spotter_parseResponse(response, domain):
    hostnameRegex = "([\w\.\-]+\.%s)" % (domain.replace(".", "\."))
    hosts = findall(hostnameRegex, str(response))

    return [host.lstrip(".") for host in hosts]

def find_subdomains_cert_spotter(domain):
    CS = []

    print(colored("[*]-Searching CertSpotter...", "yellow"))

    base_url = "https://api.certspotter.com"
    next_link = "/v1/issuances?domain={0}&include_subdomains=true&expand=dns_names".format(domain)
    # headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:52.0) Gecko/20100101 Firefox/52.0"}

    while next_link:
        try:
            response = requests.get(base_url + next_link)

            if response.status_code == 429:
                print("  \__", colored("Search rate limit exceeded.", "red"))
                return []

            CS += cert_spotter_parseResponse(response.content, domain)

            try:
                next_link = response.headers["Link"].split(";")[0][1:-1]

            except KeyError:
                break

        except requests.exceptions.RequestException as err:
            print("  \__", colored(err, "red"))
            return []

        except requests.exceptions.HTTPError as errh:
            print("  \__", colored(errh, "red"))
            return []

        except requests.exceptions.ConnectionError as errc:
            print("  \__", colored(errc, "red"))
            return []

        except requests.exceptions.Timeout as errt:
            print("  \__", colored(errt, "red"))
            return []

        except Exception:
            print("  \__", colored("Something went wrong!", "red"))
            return []

    CS = set(CS)

    print("  \__ {0}: {1}".format(colored("Unique subdomains found", "cyan"), colored(len(CS), "yellow")))
    print(CS)
    return CS