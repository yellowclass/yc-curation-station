## Create index on embeddings for Atlas Search

```json
{
	"mappings": {
		"dynamic": true,
		"fields": {
			"embedding": {
				"dimensions": 1536,
				"similarity": "cosine",
				"type": "knnVector"
			},
			"sender": {
				"type": "token"
			},
			"userId": {
				"type": "number"
			},
			"botId": {
				"type": "number"
			}
		}
	}
}
```
