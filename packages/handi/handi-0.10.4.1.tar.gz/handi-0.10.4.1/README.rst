handi(handy)

Legacy Commands & Utilities

Installation

$ pip install -U handi


Utilities

1. Basic Utility
    | [public ip]
    | $ pubip
    | $ 143.87.25.158
    |
    | [private ip]
    | $ prvip
    | $ 192.168.10.121
    |
    | [wifi password]
    | $ sudo wifipass
    | $ /etc/NetworkManager/system-connections/My-Office:psk=12345678...
    |
    | [gps]
    | $ gps
    | $ [22.7702, 112.9578]
    |
    | [timer]
    | $ timer cp 1.iso ../
    | $ 3 seconds
    |
    | [encode]
    | $ encode [string]
    | $ encode 12345678
    | $ 3132333435363738
    |
    | [decode]
    | $ decode [string]
    | $ decode 3132333435363738
    | $ 12345678
    |
    | [encrypt]
    | $ encrypt [string] [password] 
    | $ encrypt "Nothing is Unlimited." 12345678
    | $ gAAAAABeIA9OWhfmu6U97CoCdKj0LctEHfs4biG3ts-XULYPR98p1nQ6XKGmW-7D3wIGAWiTvtN73heuO7L7-QLwQZJtPv9qD_kCcofBfJ6UJ--pKcQ8tqY=
    |
    | [decrypt]
    | $ decrypt [string] [password]
    | $ decrypt gAAAAABeIA9OWhfmu6U97CoCdKj0LctEHfs4biG3ts-XULYPR98p1nQ6XKGmW-7D3wIGAWiTvtN73heuO7L7-QLwQZJtPv9qD_kCcofBfJ6UJ--pKcQ8tqY= 12345678
    | $ Nothing is Unlimited.
    |
    | [strong remove]
    | $ srm [repeats] [filename]
    | $ srm 15 accounts.txt
    |
    | [shutdonw]
    | $ boo
    |
    | [terminal clear]
    | $ cls
    |
    | [replace]
    | $ repl [fromstr] [tostr] [path1] [path2] ...
    | $ repl junying frank accounts.txt
    |
    | [statistics]
    | $ hash
    | >>hitscommand
    | 1/usr/bin/which
    | 1/usr/local/bin/ipinfo
    | 4/usr/local/bin/version
    | 1/usr/local/bin/prvip
    | 6/usr/local/bin/timer
    | 3/usr/local/bin/srm
    | 2/usr/local/bin/oneline
    | 1/usr/local/bin/sumup
    | 1/bin/rm
    | 1/usr/bin/vim
    | 1/usr/local/bin/cls
    | 1/usr/bin/touch
    | 1/usr/bin/sudo
    | 1/usr/local/bin/rmlnno
    | 11/usr/local/bin/mac
    | 1/usr/local/bin/printkey
    | 3/bin/ls
    | 1/usr/local/bin/gps
    |
2. Code Management
    | [totalines]
    | $ totalines [ext1] [ext2] ...
    | $ totalines py go cpp h java
    | $ 124535
    |
    | [git commit]
    | $ commit
    |
3. Text Handling
    | [findstr] 
    | $ findstr [keystring] [path]
    |
    | [column]
    | $ echo Time Machine|column 2
    | $ Machine
    |
    | [row]
    | $ cat accounts.txt|row 2
    | $ frank 9980
    |
    | [sumup]
    | $ sumup [filename]
    | $ cat accounts.txt|column 2|sumup
    | $ 1199899.0125
    |
    | [fromstr]
    | $ fromstr [startmark] [string]
    | $ echo Nothing Lasts.|fromstr "Nothing "
    | $ Lasts.
    |
    | [endstr]
    | $ endstr [endstring] [string]
    | $ echo Nothing lasts.||endstr .
    | $ Nothing Lasts
    |
    | [excludestr]
    | $ excludestr [excludestring1]
    | $ echo abcdEFG|excludestr EFG
    | $ abcd
    |
    | [lenstr]
    | $ lenstr [string]
    | $ lenstr 123456789
    | $ 9
    |
    | [upperstr]
    | $ upperstr [string]
    | $ upperstr gustavKo
    | $ GUSTAVKO
    |
    | [lowerstr]
    | $ lowerstr [string]
    | $ lowerstr ABcD
    | $ abcd
    |
    | [linecount]
    | $ linecount [filename]
    | $ linecount accounts.list
    | $ 14273
    |
    | [concastr]
    | $ concatstr [juncword] [filepath]
    | $ concatstr , 1 2 3 4 5
    | $ 1,2,3,4,5
    |
    | [delete specific lines in file]
    | $ deline [keystring] [filename]
    | $ deline junying accounts.txt
    |
4. JSON Handling
    | $ chkey [keyname] [inpath]
    | $ delkey [key] [inpath] [outpath]
    | $ findkey [keyname] [inpath]
    | $ printkey [keyname] [inpath] [subkey1] [subkey2]
    | $ replconfval [filepath] [keystring]  [findstr] [replacestr] [seperator]
    | $ replconfkey [keystring] [filepath] [quotechar] [replacestring/replacefile]
    | $ rmempty [inpath] [outpath]

License

MIT License <https://choosealicense.com/licenses/mit>