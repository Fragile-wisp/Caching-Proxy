import argparse
import hashlib
import requests
import http.server

#CLI
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, help='Port to connect to', required=True)
    parser.add_argument('--origin', type=str, help='Url to forward requests to', required=True)
    parser.add_argument('--clear-cache', type=str, help='Clear cache')
    args = parser.parse_args()
    
    if args.clear_cache:
        Clear_Cache()
    elif args.port and args.origin:
        Start_proxy(args.port, args.origin)
    else:
        parser.print_help()

#Server start
def Start_proxy(port, origin):
    Caching_Proxy_Handler.origin = origin
    server = http.server.HTTPServer(("", port), Caching_Proxy_Handler)
    print(f"Caching proxy running on port {port}, forwarding to {origin}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n Server stopped.")
        server.server_close()

#Cache
Cache={}

class Caching_Proxy_Handler(http.server.BaseHTTPRequestHandler):
    origin=""

    def do_GET(self):
        key=hashlib.sha256(f"{self.command}:{self.path}".encode()).hexdigest()
        
        #Cache Hit
        if key in Cache:
            Cached_response=Cache[key]
            self.send_response(Cached_response["status"])

            for header, value in Cached_response["headers"].items():
                self.send_header(header, value)
            self.send_header("X-Cache", "HIT")
            self.end_headers()
            self.wfile.write(Cached_response["body"])
    
        else:
            target_url = self.origin.rstrip("/") + self.path
            try:
                response=requests.get(target_url)
                self.send_response(response.status_code)

                header_cache={}
                for header, value in response.headers.items():
                    if header.lower() not in ["transfer_encoding", "content-length"]:
                        self.send_header(header, value)
                        header_cache[header] = value

                self.send_header("Cache", "Miss")
                self.end_headers()

                body = response.content
                self.wfile.write(body)
                
                Cache[key] = {
                    "status": response.status_code,
                    "headers": header_cache,
                    "body": body,
                }
            except Exception as e:
                self.send_error(502, f"Bad Gateway: {e}")

def Clear_Cache():
    Cache.clear()
    print("Cache cleared!")

if __name__=="__main__":
    main()