# Ted subtitle merge

## 這東西有什麼用？(What)

此專案是用合併 Ted 的中英字幕，
會輸出 中英字幕合併之後的結果：


```json
[  
   {  
      "en":"How do you explain\nwhen things don't go as we assume?",
      "zh-tw":"你會怎麼解釋當事情不如我們所想的一般時？"
   },
   {  
      "en":"Or better, how do you explain",
      "zh-tw":"或者更好的是，你如何解釋"
   },
   {  
      "en":"when others are able to achieve things\nthat seem to defy all of the assumptions?",
      "zh-tw":"當其他人能夠完成似乎違反所有假設的事時？"
   }
]
```


## 為什麼需要這個？(Why)

因為想要中英字幕對照一起看，但是從 `Ted` 拿到的中英字幕，發現沒辦法很容易的把中英字幕集結起來，因為有些話英文講可能要三句，中文只要一句，例如 Simon Sinek 的 [How great leaders inspire action](https://www.ted.com/talks/simon_sinek_how_great_leaders_inspire_action)

我們可以先透過解析 `html` 去拿到 `talk id` ：

```bash
curl -s https://www.ted.com/talks/simon_sinek_how_great_leaders_inspire_action | grep al:ios:ur  | awk -F '/' '{print $4}'  | awk -F '?' '{print $1}'
// 848
```	

再用 `talk id` 去拿到該 `talk` 的中英字幕：

https://www.ted.com/talks/subtitles/id/848/lang/en    
https://www.ted.com/talks/subtitles/id/848/lang/zh-tw

就可以拿到中英字幕：


```json
{  
   "captions":[  
      {  
         "duration":2000,
         "content":"你會怎麼解釋",
         "startOfParagraph":true,
         "startTime":1000
      },
      {  
         "duration":2000,
         "content":"當事情不如我們所想的一般時？",
         "startOfParagraph":false,
         "startTime":3000
      },
      {  
         "duration":3000,
         "content":"或者更好的是，你如何解釋",
         "startOfParagraph":false,
         "startTime":5000
      },
      {  
         "duration":2000,
         "content":"當其他人能夠完成似乎",
         "startOfParagraph":false,
         "startTime":8000
      },
      {  
         "duration":2000,
         "content":"違反所有假設的事時？",
         "startOfParagraph":false,
         "startTime":10000
      }
   ]
}
```


```json
{  
   "captions":[  
      {  
         "duration":3976,
         "content":"How do you explain\nwhen things don't go as we assume?",
         "startOfParagraph":true,
         "startTime":1000
      },
      {  
         "duration":2976,
         "content":"Or better, how do you explain",
         "startOfParagraph":false,
         "startTime":5000
      },
      {  
         "duration":3976,
         "content":"when others are able to achieve things\nthat seem to defy all of the assumptions?",
         "startOfParagraph":false,
         "startTime":8000
      }
   ]
}
```

其中各欄位的意義：

| 欄位名稱 | 意義 |  
|---|---|
| `duration` | 這句話講了多久，單位為毫秒 |  
| `content` | 講什麼 |  
| `startOfParagraph` | 是不是段落的開始 |  
| `startTime` | 開始講的時間，單位為毫秒 |  

這個例子可以看出同樣的話，中文的字幕是六句；而英文是三句。  
而這個程式的功能就是**將兩個字幕合併**，將同樣的話**對齊**：

```json
[  
   {  
      "en":"How do you explain\nwhen things don't go as we assume?",
      "zh-tw":"你會怎麼解釋當事情不如我們所想的一般時？"
   },
   {  
      "en":"Or better, how do you explain",
      "zh-tw":"或者更好的是，你如何解釋"
   },
   {  
      "en":"when others are able to achieve things\nthat seem to defy all of the assumptions?",
      "zh-tw":"當其他人能夠完成似乎違反所有假設的事時？"
   }
]
```

## 要怎麼做到合併呢？(How)

首先先觀察 `startOfParagraph` 能不能當作合併的條件，
要先搜尋中英字幕的`"startOfParagraph":true` 的個數，  
因為 `"startOfParagraph":true` 代表這是一個段落的開始，  
搜尋此 talk 發現中文的個數是 `24` 個，英文是 `30` 個，  
所以不能單純用這個來做合併條件。


所以剩下幾個有用的資訊：

1. `startTime`
2. `duration`

目前是根據這兩個資訊來做合併的條件，大致上分為兩個步驟：


1. 找出英文幾句話是一個段落。 
  - 偵測到句尾有 `.`，就可能是一個段落)，會得到一個段落的 `startTimeOfParagraph` 跟 `durationOfParagraph`。
2. 找出中文哪個段落 是 對應剛剛找到的英文段落。 
  - 將中文字幕一句一句的 `duration` 加起來，等於剛剛英文的 `durationOfParagraph` 就是中文的一個段落。



	 

