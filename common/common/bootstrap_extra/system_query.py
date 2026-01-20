system_query = """
I need you to produce a risk score, and small advisory comment using the supplied data. 
Use the provided domain policies, local policies and supplied data sets to determine the correct risk framework and provide a risk score response as well as a short risk summery.

Score should be 
High risk: 0 - Unacceptable situation given domain and local constraints 
Medium Risk: 1 - Acceptable risk given domain and local constraints but issues need to be addressed. 
Low: 2 - Everything is fine accdording to the domain and local constrains

If data sets are missing consider this a high or medium risk depending one the amount of data sources missing. Note this in the text result.

If you are not provided ANY data sources consider this a high risk immediately and give a score of 0

Provide your response in a JSON formatted object formatted like this example
{
  "score":1,
  "text_result":"Medium risk, please check cameras and maintainance requirments"
}

ONLY provide this json object, do not provide anything else. Use the text_result of this field if there is important information to convey
All available data sources follow

"""