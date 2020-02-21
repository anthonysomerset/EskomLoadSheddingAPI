# EskomLoadShedding API

This is somewhat of a wrapper API around Eskom's Load Shedding interfaces

The reason for this API is that Eskom's interface doesn't generate suitable data formats for automated systems without a lot of parsing effort to decipher the html output and process it into some useful data structure. There are also other current limitations such as only including Stages 1-4, and there is additionally a desire for other helper calls like, time to next load shedding etc.

This is still very much work in progress and is built using the [Chalice](https://github.com/aws/chalice) serverless microframework for python. and runs on AWS Lambda - Currently hosted at

* https://loadshedding.sts.io/dev : Dev API - may have breakage!
* https://loadshedding.sts.io/v1 : Production API - not complete as per the below

New versions which make breaking changes will result in a version increment and the current and previous version will be maintained, older versions may be kept around on a best effort basis but otherwise unmaintained

##Current Working Calls

* Get Current Load Shedding Stage : `GET /Stage`

Gets Current Load shedding stage from Eskom and presents as an integer (proper JSON structure WIP) it represents the real stage not stage + 1 like eskom does, therefore 0 = No Load Shedding, 1 = Stage 1 etc

##Not Yet Working but WIP

* Get Next Load Shedding for "current" stage : `GET /NextShedding/{area_id}`
Where area_id = the area_id as per Eskom website - more info on how to get this later but this Reference is a useful start - https://mybroadband.co.za/forum/threads/loadshedding-api.672196/page-2
Will return various values - e.g. the exact date/time, hours to go, minutes to go etc

* Get Next Load Shedding for a specific stage: `GET /NextShedding/{area_id}/{stage}`
Where area_id is same as above and stage is an integer reflecting the desired stage - NOTE: Eskom only appears to show stages 1-4 via their "API's" so stages 5-8 not implemented until such time as Eskom make them programatically available or we crowdsource a database much like [EskomSePush](https://sepush.co.za/) team has excellently done

##Not Yet Started

* Get Schedule for a given area
Should return a JSON object of schedules by date/day - possibly with some other configurable parameters like "stage" and number of days to return or perhaps even date ranges??

* Get areas/suburb search
Eskom interfaces already have this and it does appear to return json, theres no real need to re-implement this but it might be nice from a feature completeness aspect

##Others?
Let us know