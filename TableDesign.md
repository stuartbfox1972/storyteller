# Collections and Indexes

## Collections
|PK|SK|ATTR|JSON|
|--|--|--|--|
|STORY#storyid|DETAILS#storyid|publishDate,author,age,title,tags[]|intro|
||PARAGRAPH#number||body,next,previous|
||TAGS#tag#tag|||
||REVIEW#userid|rating,comments||
|USER#userid|PROFILE|||
||STORY#storyid|title||
|| PROGRESS#STORYID|paragraph||
|TAG#tag|storyid|||


## Indexes
### GroupByAgeRangeIndex
|PK|SK|ATTR|
|--|--|--|
|ageRange|storyID|title,author|
