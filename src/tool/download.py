import requests
def download_file(url):
    local_filename = url.split('=')[-1]
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    return local_filename
if __name__ == '__main__':
    download_file('http://20.26.2.23:18088/iCloud/download/download.dox?filename=c5aacf230c254029aa40ff6ac4374e89.war&outFilename=abc.war')