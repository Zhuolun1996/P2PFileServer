#README

##Description
This project would simulate message transmission in P2PNetwork

##Manual
###Arguments:  
-P, --peers, Number of Peers initiated , e.g. 10  
-M, --files, Number of Files assigned to each peer, e.g. 10  
-N, --requests, Number of requests to download a file in simulation, e.g. 3  
-F, --frequency, The frequency to submit download request, e.g. 10 --> wait 0.1 miliseconds between two requests  
-L, --length, File length, e.g. 10  
-C, --centralized, Run in centralized mode, e.g. T --> will run in centralized mode, otherwise, decentrazlied mode  
-O, --output, Output mode, `clean` || `debug` || `false`  

###Example
`python3 main.py -P 10 -M 10 -N 1 -F 10 -C F -L 10 -O clean `  
output:
```angular2
Server 0 loop running in thread: Thread-1
Update Cached Index Server to (0, ('127.0.0.1', 50000))
clean directory success
Server 1 loop running in thread: Thread-13
Update Cached Index Server to (0, ('127.0.0.1', 50000))
clean directory success
Server 2 loop running in thread: Thread-27
Update Cached Index Server to (0, ('127.0.0.1', 50000))
clean directory success
Server 3 loop running in thread: Thread-43
Update Cached Index Server to (0, ('127.0.0.1', 50000))
clean directory success
Server 4 loop running in thread: Thread-61
Update Cached Index Server to (0, ('127.0.0.1', 50000))
clean directory success
Server 5 loop running in thread: Thread-81
Update Cached Index Server to (0, ('127.0.0.1', 50000))
clean directory success
Server 6 loop running in thread: Thread-103
Update Cached Index Server to (0, ('127.0.0.1', 50000))
clean directory success
Server 7 loop running in thread: Thread-127
Update Cached Index Server to (0, ('127.0.0.1', 50000))
clean directory success
Server 8 loop running in thread: Thread-153
Update Cached Index Server to (0, ('127.0.0.1', 50000))
clean directory success
Server 9 loop running in thread: Thread-181
Update Cached Index Server to (0, ('127.0.0.1', 50000))
clean directory success
Server 1000 loop running in thread: Thread-211
Update Cached Index Server to (0, ('127.0.0.1', 50000))
clean directory success
Start download with Thread-234
Start download with Thread-235
====================================
download from peer 9 for file 0
request file chunk: 0
file Length: 150
download piece from: 0 to 15
====================================

Start download with Thread-236
Start download with Thread-237
====================================
download from peer 1 for file 0
request file chunk: 1
file Length: 150
download piece from: 15 to 30
====================================

Start download with Thread-238
Start download with Thread-239
Start download with Thread-240
====================================
download from peer 2 for file 0
request file chunk: 5
file Length: 150
download piece from: 75 to 90
====================================

====================================
download from peer 0 for file 0
request file chunk: 3
file Length: 150
download piece from: 45 to 60
====================================

====================================
download from peer 6 for file 0
request file chunk: 6
file Length: 150
download piece from: 90 to 105
====================================

====================================
download from peer 3 for file 0
request file chunk: 2
file Length: 150
download piece from: 30 to 45
====================================
Start download with Thread-241

Start download with Thread-242
====================================
====================================
download from peer 4 for file 0
request file chunk: 4
file Length: 150
download piece from: 60 to 75
====================================

download from peer 8 for file 0
request file chunk: 7
file Length: 150
download piece from: 105 to 120
====================================

Start download with Thread-243
====================================
download from peer 7 for file 0
request file chunk: 8
file Length: 150
download piece from: 120 to 135
====================================

====================================
download from peer 5 for file 0
request file chunk: 9
file Length: 150
download piece from: 135 to 150
====================================

cached file chunks:  ['{"head": "DownloadResponse", "fileName": "0", "index": 0, "chunks": 10, "chunkMd5": "17527f4bd3c85b7f57ca8123f40a353c", "fileContent": "Peer test File0"}', '{"head": "DownloadResponse", "fileName": "0", "index": 1, "chunks": 10, "chunkMd5": "17527f4bd3c85b7f57ca8123f40a353c", "fileContent": "Peer test File0"}', '{"head": "DownloadResponse", "fileName": "0", "index": 5, "chunks": 10, "chunkMd5": "17527f4bd3c85b7f57ca8123f40a353c", "fileContent": "Peer test File0"}', '{"head": "DownloadResponse", "fileName": "0", "index": 3, "chunks": 10, "chunkMd5": "17527f4bd3c85b7f57ca8123f40a353c", "fileContent": "Peer test File0"}', '{"head": "DownloadResponse", "fileName": "0", "index": 2, "chunks": 10, "chunkMd5": "17527f4bd3c85b7f57ca8123f40a353c", "fileContent": "Peer test File0"}', '{"head": "DownloadResponse", "fileName": "0", "index": 6, "chunks": 10, "chunkMd5": "17527f4bd3c85b7f57ca8123f40a353c", "fileContent": "Peer test File0"}', '{"head": "DownloadResponse", "fileName": "0", "index": 7, "chunks": 10, "chunkMd5": "17527f4bd3c85b7f57ca8123f40a353c", "fileContent": "Peer test File0"}', '{"head": "DownloadResponse", "fileName": "0", "index": 4, "chunks": 10, "chunkMd5": "17527f4bd3c85b7f57ca8123f40a353c", "fileContent": "Peer test File0"}', '{"head": "DownloadResponse", "fileName": "0", "index": 8, "chunks": 10, "chunkMd5": "17527f4bd3c85b7f57ca8123f40a353c", "fileContent": "Peer test File0"}', '{"head": "DownloadResponse", "fileName": "0", "index": 9, "chunks": 10, "chunkMd5": "17527f4bd3c85b7f57ca8123f40a353c", "fileContent": "Peer test File0"}']
downloaded file:  0
downloaded file's MD5:  e3fc8f9fca9979c5466bf0f86502d6f8
original file's MD5:  e3fc8f9fca9979c5466bf0f86502d6f8
Peer 0 Message Sent: 277
Peer 0 Message Received: 11
Peer 0 Bytes Sent: 30151
Peer 0 Bytes Received: 1249
Peer 0 Average Response Time: 0.19174320391275018 milliseconds
Peer 1 Message Sent: 51
Peer 1 Message Received: 13
Peer 1 Bytes Sent: 4435
Peer 1 Bytes Received: 1443
Peer 1 Average Response Time: 0.40964211309078097 milliseconds
Peer 2 Message Sent: 49
Peer 2 Message Received: 15
Peer 2 Bytes Sent: 4241
Peer 2 Bytes Received: 1637
Peer 2 Average Response Time: 0.4151874764479139 milliseconds
Peer 3 Message Sent: 47
Peer 3 Message Received: 17
Peer 3 Bytes Sent: 4047
Peer 3 Bytes Received: 1831
Peer 3 Average Response Time: 0.46901598224356844 milliseconds
Peer 4 Message Sent: 45
Peer 4 Message Received: 19
Peer 4 Bytes Sent: 3853
Peer 4 Bytes Received: 2025
Peer 4 Average Response Time: 0.4642187197915112 milliseconds
Peer 5 Message Sent: 43
Peer 5 Message Received: 21
Peer 5 Bytes Sent: 3659
Peer 5 Bytes Received: 2219
Peer 5 Average Response Time: 0.34218658489325543 milliseconds
Peer 6 Message Sent: 41
Peer 6 Message Received: 23
Peer 6 Bytes Sent: 3465
Peer 6 Bytes Received: 2413
Peer 6 Average Response Time: 0.43673124655922524 milliseconds
Peer 7 Message Sent: 39
Peer 7 Message Received: 25
Peer 7 Bytes Sent: 3271
Peer 7 Bytes Received: 2607
Peer 7 Average Response Time: 0.45840795972397286 milliseconds
Peer 8 Message Sent: 37
Peer 8 Message Received: 27
Peer 8 Bytes Sent: 3077
Peer 8 Bytes Received: 2801
Peer 8 Average Response Time: 0.5095546759150847 milliseconds
Peer 9 Message Sent: 35
Peer 9 Message Received: 29
Peer 9 Bytes Sent: 2883
Peer 9 Bytes Received: 2995
Peer 9 Average Response Time: 0.4924454217577763 milliseconds
Peer 1000 Message Sent: 32
Peer 1000 Message Received: 32
Peer 1000 Bytes Sent: 2128
Peer 1000 Bytes Received: 4034
Peer 1000 Average Response Time: 1.281226919237972 milliseconds
average message sent: 63.27272727272727
average message received: 21.09090909090909
average bytes sent: 5928.181818181818
average bytes received: 2295.818181818182
average response time: 0.49730548214307374 miliseconds
Server0 shutdown
Server1 shutdown
Server2 shutdown
Server3 shutdown
Server4 shutdown
Server5 shutdown
Server6 shutdown
Server7 shutdown
Server8 shutdown
Server9 shutdown
Server1000 shutdown
```