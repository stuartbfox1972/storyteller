# Collections and Indexes

## Collections
|PK|SK|ATTR|
|--|--|--|
|STORY#storyId|STORY#DETAILS|storyId,GSIPK1,publishDate,author,ageRange,title,tags[],intro,lang|
||PARAGRAPH#number|body,next,previous|
||REVIEW#reviewId|displayName,rating,comments|
|USER#userId|PROFILE|displayName,email,dob,languages[]|
||PROGRESS#storyId|paragraphId,timestamp,mode|
|TAG#tag|STORY#storyId|displayName,rating|

## Indexes
### ListOfStories
|PK|SK|ATTR|
|--|--|--|
|STORY#DETAILS|storyId|views, ageRange, author, storyId, tags, title|

### GroupStoriesByAgeRangeIndex
|PK|ATTR|
|--|--|
|ageRange|storyId,views, tags, title, author|

### GroupStoriesByAuthorIndex
|PK|ATTR|
|--|--|
|author|storyId, ageRange, views, tags, title|