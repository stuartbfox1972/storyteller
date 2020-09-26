# Collections and Indexes

## Collections
|PK|SK|ATTR|
|--|--|--|
|STORY#storyId|DETAILS|storyId,GSIPK1,publishDate,author,ageRange,title,tags[],intro,lang|
||PARAGRAPH#number|body,next,previous|
||REVIEW#reviewId|displayName,rating,comments|
|USER#userId|PROFILE|displayName,email,dob,langs[]|
||STORY#storyId|title|
||PROGRESS#storyId|paragraph|
|TAG#tag|STORY#storyId|displayName,rating|

## Indexes
### ListOfStories
|PK|SK|ATTR|
|--|--|--|
|GSIPK1|storyId, ageRange, author, views, tags, title|

### GroupStoriesByAgeRangeIndex
|PK|ATTR|
|--|--|
|ageRange|views, tags, title, author|

### GroupStoriesByAuthorIndex
|PK|ATTR|
|--|--|
|author|storyId, ageRange, views, tags, title|