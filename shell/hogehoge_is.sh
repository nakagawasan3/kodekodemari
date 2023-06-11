#!/bin/bash

# webisディレクトリに移動
cd /home/nakagawa/webis

# ディレクトリ内のファイルを取得
files=$(ls)

# ファイルごとに内容を表示
for file in $files; do   
    # 行を取得
    grep -oP '<div id="row[0-9]{1,2}" style="text-align:left;width:100%;padding:0px;display:table">(.*?)</a></div></div>' $file | while read row; do
        
        # urlを取得
        urls=$(echo "$row" | grep -oP 'alt="screenshot of (.*?)"' | sed 's/.\{19\}\(.*\).\{1\}/\1/')
        url=$(echo ${urls:0:62})
        
        # created_datetimeを取得
        intId=$(echo "$url" | grep -oP '[0-9]{1,}')
        unixTime=$((intId / 2**22 + 1288834974657))
        created_datetime=$(date -d @$((unixTime/1000-(9*60*60))) '+%Y%m%d%H%M%S')
        
        # snapshot_urlを取得
        snapshot_urls=$(echo "$row" | grep -oP '<a style="text-decoration:none" href="(.*?)">' | sed 's/.\{38\}\(.*\).\{2\}/\1/')
        snapshot_url=$(echo ${snapshot_urls:0:24})
        
        # snapshot_datetimeを取得
        dates=$(echo "$row" | grep -oP '<div style="color:black;white-space:nowrap;font-size:9px;text-align:right">(.*?)</div>' | sed 's/<div[^>]*>\(.*\)<\/div>/\1/g')
        date=$(echo ${dates:0:17})
        snapshot_datetime=$(date -d "$date" +"%Y%m%d%H%M%S")
        
        # textを取得
        texts=$(echo "$row" | grep -oP 'title="(.*?)"' | sed 's/.\{7\}\(.*\).\{1\}/\1/')
        text=${texts//$'\n'/\\n}
        
        echo "${url},${created_datetime},${snapshot_url},${snapshot_datetime},${text}" >> /home/nakagawa/hogehoge_21.csv
    done
done
echo "終了"
