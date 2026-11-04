src=open('index.src.html').read(); data=open('data.js').read().strip()
open('index.html','w').write(src.replace('__DATA__',data))
