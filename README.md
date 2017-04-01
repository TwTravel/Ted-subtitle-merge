# Ted subtitle merge

 
此專案是用於 merge Ted 的字幕，
會輸出 中英字幕合併之後的結果，以 json 格式呈現。


	{
	    "url": "http:xxx", 
	    "title": ""
	    "Paragraphs": [
	        {
	            "chinese": "Roy Price這個人，各位可能都未曾聽過，即使他曾負責過你生命中平凡無奇的22分鐘，在2013年4月19日這一天。他也許也曾負責帶給各位非常歡樂的22分鐘，但你們其中也許很多人並沒有。而這一切全部要回到Roy在三年前的一個決定。", 
	            "english": "Roy Price is a man that most of you have probably never heard about, even though he may have been responsible for 22 somewhat mediocre  minutes of your life on April 19, 2013. He may have also been responsible for 22 very entertaining minutes, but not very many of you. And all of that goes back to a decision that Roy had to make about three years ago."
	        }, 
	        {
	            "chinese": "所以，你明白，Roy Price是Amazon廣播公司的一位資深決策者。這是Amazon旗下的一家電視節目製作公司。他47歲，身材不錯，尖頭髮，在Twitter上形容自己是“電影、電視、科技、墨西哥捲餅 。”Roy Price有一個責任非常重大的工作，因為他要負責幫Amazon挑選即將製作的原創內容節目。", 
	            "english": "So you see, Roy Price is a senior executive with Amazon Studios. That's the TV production company of Amazon. He's 47 years old, slim, spiky hair, describes himself on Twitter as \"movies, TV, technology, tacos.\" And Roy Price has a very responsible job, because it's his responsibility to pick the shows, the original content that Amazon is going to make."
	        } ... ]
	}


一開始先給一個 talk 網址：   
https://www.ted.com/talks/sebastian_wernicke_how_to_use_data_to_make_a_hit_tv_show


先在 TedTalkFetcher.py 使用 curl + grep + awk 拿到 talk id   

	curl -s https://www.ted.com/talks/sebastian_wernicke_how_to_use_data_to_make_a_hit_tv_show | grep al:ios:ur  | awk -F '/' '{print $4}'  | awk -F '?' '{print $1}'
	
	
再用 talk id 去 get 網頁

https://www.ted.com/talks/subtitles/id/2403/lang/en    
https://www.ted.com/talks/subtitles/id/2403/lang/zh-tw

get 出來的 json 長這樣：

	{  
	   "captions":[  
	      {  
	         "duration":4276,
	         "content":"Roy Price is a man that most of you\nhave probably never heard about,",
	         "startOfParagraph":true,
	         "startTime":820
	      },
	      {  
	         "duration":2496,
	         "content":"even though he may have been responsible",
	         "startOfParagraph":false,
	         "startTime":5120
	      },
	      {  
	         "duration":6896,
	         "content":"for 22 somewhat mediocre \nminutes of your life on April 19, 2013.",
	         "startOfParagraph":false,
	         "startTime":7640
	      },
	      {  
	         "duration":3176,
	         "content":"He may have also been responsible\nfor 22 very entertaining minutes,",
	         "startOfParagraph":false,
	         "startTime":14560
	      } ...
	   ]
	}


**startOfParagraph** 沒什麼用，因為搜尋中英字幕的  `"startOfParagraph":true` 的個數是不一樣的，  
由此可見不能單純用這個來做 merge 條件。


所以剩下幾個有用的資訊：

1. startTime
2. duration

根據這兩個資訊來做 merge。

但有時候不想一段落太多句子，所以用 ParagraphDetector.py 來判斷目前字串是否算一個句子。
	

	 

