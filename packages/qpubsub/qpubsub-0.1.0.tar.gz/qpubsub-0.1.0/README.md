# library.qpubsub

pubsub layer for NLP services

## Usages
### Configs
You need to configure these in your service:
```python
{
    "PROJECT_ID": "...",
    "SUBSCRIPTION_NAME": "...",
    "TOPIC_NAME": "...",
    "MAX_MESSAGES": ...
}
```
Where:
`PROJECT_ID`: qordoba project id e.g. qordoba-devel
`SUBSCRIPTION_NAME`: a subscription to pull the messages from e.g. dev4.segment-delegator.gender-tone-pubsub.allLang
`TOPIC_NAME`: where to publish the result messages e.g. dev4.segment-delegator.gender-tone-pubsub-latch.allLang
`MAX_MESSAGES`: The maximum number of messages in the subscriber queue e.g. 100



### Use PubSub only
Add this to the service `application.py`
```python
    ps_connection = QPubSub(
        analyzer,
        white_lister=whitelister,
        category=category,
        verbose=VERBOSE,
        debug=DEBUG,
        ignore_html=IGNORE_HTML,
        sentence_token_limit=SENTENCE_TOKEN_LIMIT,
        ignore_inside_quotes=False
    )

    ps_connection.connect()
```

### Use PubSub with REST
Add this to the service `application.py`
```python
    rest_connection = QRest(
        analyzer,
        white_lister=whitelister,
        category=category,
        verbose=VERBOSE,
        debug=DEBUG,
        ignore_html=IGNORE_HTML,
        sentence_token_limit=SENTENCE_TOKEN_LIMIT,
        ignore_inside_quotes=False
    )
    ps_connection = QPubSub(
        analyzer,
        white_lister=whitelister,
        category=category,
        verbose=VERBOSE,
        debug=DEBUG,
        ignore_html=IGNORE_HTML,
        sentence_token_limit=SENTENCE_TOKEN_LIMIT,
        ignore_inside_quotes=False
    )

    ps_connection.connect_with_rest(rest_connection)
```

### Service docker changes to compile `google-cloud-pubsub`
add the following lines before `pip install -r requirements.txt` command
```dockerfile 
    apk update && \
    apk add --virtual build-dependencies linux-headers build-base gcc && \
```


add the following lines after `pip install -r requirements.txt` command
```dockerfile
    apk del build-dependencies && \
    rm -rf /var/cache/apk/* && \
```

## License

This software is not licensed. If you do not work at Qordoba, you are not legally allowed to use it. Also, it's just helper functions that really won't help you. If something in it does look interesting, and you would like access, open an issue.


## TODO
- reduce compile time
- add tests
- handle errors, e.g. publish it to an error topic or return empty issues to the same topic.