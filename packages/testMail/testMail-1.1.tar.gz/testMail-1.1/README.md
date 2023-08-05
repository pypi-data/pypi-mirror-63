# testMail

## How to install
```
git clone https://github.com/FKgk/testMail.git
```
or
```
pip install testMail
```

## Dependency
- this package don't need any reqiurements
- need built-in module (email, smtplib, re)

## Example
```
from testMail import Mail

mail = Mail("sender email", "app password")

mail.send("receiver(s) email", "title", "content")

mail.close()
```

### If you want to check validation
```
mail.valid("email")
```
- return true or flase

## Reference
- https://docs.python.org/3/library/smtplib.html

## PYPI
- https://pypi.org/project/testMail/1.0/