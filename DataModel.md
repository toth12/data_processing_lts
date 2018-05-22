Testimonies collection data model

```javascript
{
  testimony_id: str | ''
  interviewee_name: str | ''
  gender: 'male' | 'female' | ''
  collection: str
  shelfmark: str
  recording_year: int | null
  camp_names: [str] | []
  ghetto_names: [str] | []
  html_transcript: str | ''
  media_url: [str] | []
  thumbnail_url: str | ''
  testimony_title: str | ''
  interview_summary: str | ''
  provenance: str | ''
}
```


Tokens Collection Schema 

```javascript
{
  'testimony_id': str,
  'tokens': [
    {'token_index': 0, 'sentence_index': 0},
    {'token_index': 1, 'sentence_index': 0},
    ...
  ]
}
```