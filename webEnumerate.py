import os
import sys
import socket
import signal
import requests
import concurrent.futures

# User input for target domain
target_domain = input("Enter the domain you want to enumerate: ").strip()

# Flag to track script termination
stop_execution = False

def handle_interrupt(signal, frame):
    """Handle Ctrl + C (SIGINT) gracefully"""
    global stop_execution
    print("\nCtrl + C detected. Exiting...")
    stop_execution = True
    sys.exit(0)

# Register the signal handler
signal.signal(signal.SIGINT, handle_interrupt)

def load_subdomains(wordlist):
    """Load subdomains from a file"""
    if not os.path.exists(wordlist):
        print(f"Error: The file {wordlist} does not exist!")
        return []
    
    with open(wordlist, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def check_subdomain(subdomain):
    """Check if a subdomain is active"""
    if stop_execution:  # Stop execution if Ctrl + C was pressed
        return None
    
    full_domain = f"{subdomain}.{target_domain}"
    url = f"http://{full_domain}/"
    
    try:
        # Resolve DNS
        ip = socket.gethostbyname(full_domain)

        # Check if HTTP is responding
        response = requests.get(url, timeout=2)
        
        if response.status_code < 400:
            print(f"[+] Active: {url} ({ip})")
            return url
        
    except socket.gaierror:
        pass  # Ignore DNS resolution failures
    except requests.exceptions.RequestException:
        pass  # Ignore HTTP errors

    return None

def enumerate_subdomains(wordlist):
    """Enumerate active subdomains using threading"""
    active_subdomains = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        try:
            results = executor.map(check_subdomain, wordlist)
            active_subdomains = [r for r in results if r]  # Filter out None values
        except KeyboardInterrupt:
            print("\nStopping enumeration...")
            executor.shutdown(wait=False)
            sys.exit(0)
    
    return active_subdomains

if __name__ == "__main__":
    # Load wordlist
    wordlist_path = r"WORDLIST" # Replace this string with the wordlist you want to use
    wordlist = load_subdomains(wordlist_path)

    # If wordlist is empty, exit
    if not wordlist:
        print("No subdomains found in the wordlist. Exiting.")
        sys.exit(0)

    # Start enumeration
    active_subdomains = enumerate_subdomains(wordlist)

    # Display results
    print("\n--- Active Subdomains ---")
    for sub in active_subdomains:
        print(sub)
