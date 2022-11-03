# Nginx + PHP-FPM environment 


from hxp CTF "Counter"


```
<?php ($_GET['action'] ?? 'read' ) === 'read' ? readfile($_GET['file'] ?? 'index.php') : include_once($_GET['file'] ?? 'index.php');
```

exploiting the additional fastcgi_buffering / readfile local file inclusion vulnerability.

We are presented with a minimal PHP's challenge with the goal of getting code execution:
It’s clear that we again have a (hard?) LFI PHP task via include_once($_GET['file'] ?? 'index.php').
Additionally, the challenge seems to contain a suspicious readfile branch in the otherwise aesthetically pleasing minimal appearance.
Let’s use this feature to write a file with attacker-chosen content in order to get code execution.

Note: this challenge can also be solved without the readfile feature, as demonstrated here.

readfile is a neat PHP function that: “Reads a file and writes it to the output buffer.”
Contrary to include, it also supports reading URL streams like http:// resources and directly writes them to the output buffer.

#Attack plan

Use readfile to read a big and slow HTTP resource (and keep the connection open)
Use Nginx’s fastcgi_buffering to create a tempfile
Include the freshly created tempfile
Usual racing and stuff
    
Profit

Annoyances:

readfile and fastcgi_buffering seems to only create a file when the client is connected via HTTP/1.0 (see curl part in exploit). 
Otherwise, chunked transfer can be used.

Nginx instantly unlinks the newly created file.

Including the new file via our friend procfs 
e.g /proc/$NGINX_WORKER_PID/fd/$FD only works within a very small time window and requires a lot of luck (or a lot of violent force). 
If we’re too slow, PHP’s include resolves this path to strings like /var/lib/nginx/fastcgi/4/01/0000000014 (deleted), 
which doesn’t exist in the filesystem. Luckily the logic in include can be confused via /proc/self/fd/$NGINX_WORKER_PID/../../../$NGINX_WORKER_PID/fd/$FD,
which will make it always interpret the content of the original file. 
This trick greatly reduces the amount of luck/force needed to make this exploit work reliably and quickly.


Local deploy via docker

```
docker build -t includers_revenge .
docker run -p 8088:80 --rm -it includers_revenge

```


Translated:

fastcgi_buffering / readfile のローカルファイル包含の脆弱性を追加で悪用する。

我々は、コード実行を得ることを目的とした最小限のPHPの課題を提示されています。
include_once($_GET['file'] ?? 'index.php')を介して、再びLFI PHPタスクを持っていることは明らかです。
さらに、この課題は、そうでなければ美しく見える最小限の外観の中に、怪しいreadfileブランチを含んでいるように見えます。
コード実行を得るために、攻撃者が選んだ内容のファイルを書くために、この機能を使いましょう。

注意：この課題は、ここで実証されているように、readfile 機能を使わずに解決することもできます。

readfile は PHP の関数で、次のような機能を持っています。「ファイルを読み込み、それを出力バッファに書き込む。
インクルードとは逆に、http:// リソースのような URL ストリームの読み込みもサポートしており、直接出力バッファに書き込むことができます。

攻撃計画

readfileを使って、大きくて遅いHTTPリソースを読み込む（そして接続を開いたままにする）。
Nginxのfastcgi_bufferingを使用してtempfileを作成する。
作成されたばかりのtempfileをインクルードする
通常の競合とその他
    


readfileとfastcgi_bufferingは、クライアントがHTTP/1.0で接続しているときだけファイルを作成するようです（exploitのcurl部分を参照してください）。
それ以外の場合は、チャンク転送が使える。

Nginx は新しく作成されたファイルを即座にリンク解除します。

procfs経由で新しいファイルをインクルードする 
例：/proc/$NGINX_WORKER_PID/fd/$FDは非常に小さな時間枠でしか動作しないので、かなりの運（または暴力的な力）が必要です。
あまりに遅い場合、PHPのincludeはこのパスを/var/lib/nginx/fastcgi/4/01/00000014 (deleted) のような文字列に解決しますが、これはファイルシステム上に存在しません。
幸運なことに、includeのロジックは/proc/self/fd/$NGINX_WORKER_PID/../../$NGINX_WORKER_PID/fd/$FDを介して混乱することができ、
これにより常に元のファイルのコンテンツを解釈するようになります。
このトリックにより、このエクスプロイトを確実かつ迅速に動作させるために必要な運や力の量が大幅に削減されます。

