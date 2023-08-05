# Typegame

a small dash app for creating quizes for programming education

### install
`pip install typegame`

or

`pip install git+https://github.com/endremborza/typegame.git`

for latest version

### use

run with 

```
python -m typegame \
    --host=0.0.0.0 \
    --port=6999 \
    --quiz-path=./quizes \
    --answer-path=./answers
```

(all parameters are optional, these are the defaults)

optional parameters:
- `--value-game`: asks for values, not just type of last line